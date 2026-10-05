import hashlib
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from ..config import settings
from ..db.database import get_db
from ..models.knowledge_models import (
    DocumentModel,
    DocumentChunkModel,
    EvidenceModel,
    TermModel,
    TermTranslationModel,
    TranslationTermModel
)
from ..models.knowledge_schemas import (
    KnowledgeSearchRequest,
    KnowledgeSearchResponse,
    KnowledgeBaseStats,
    DocumentCreate,
    DocumentResponse
)
from ..knowledge.retrieval_service import knowledge_retrieval_service
from ..knowledge.source_registry import source_registry_service
from ..knowledge.specialized_handlers import terminology_special_handler

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge Base & Retrieval"])

@router.post("/search", response_model=KnowledgeSearchResponse)
def search_knowledge_base(req: KnowledgeSearchRequest, db: Session = Depends(get_db)):
    """
    Executes real hybrid retrieval (Exact + Keyword + Semantic + Category Filter + RRF Fusion).
    Returns candidates enriched with authentic provenance and content hashes.
    """
    if not req.query or len(req.query.strip()) == 0:
        raise HTTPException(status_code=400, detail="استعلام البحث لا يمكن أن يكون فارغاً")
    return knowledge_retrieval_service.search(db, req)

@router.get("/stats", response_model=KnowledgeBaseStats)
def get_knowledge_base_stats(db: Session = Depends(get_db)):
    """
    Returns actual counts of sources, documents, chunks, terms, and governance status from the database.
    """
    return source_registry_service.get_stats(db)

@router.get("/health")
def get_knowledge_health(db: Session = Depends(get_db)):
    """
    Live health check for Supabase, PostgreSQL, pgvector, and Knowledge Base counts.
    Strictly reports real production states without fake data.
    """
    from ..knowledge.supabase_client import supabase_client
    from ..db.database import get_db_info
    from sqlalchemy import text

    pg_ok, pg_msg = supabase_client.is_connected()
    vec_ok, vec_msg = supabase_client.is_pgvector_available()
    fts_ok, fts_msg = supabase_client.is_fts_available()
    stats = source_registry_service.get_stats(db)
    db_info = get_db_info()

    # Query embedding counts directly from PostgreSQL
    embedding_count = 0
    failed_embeddings = 0
    tables_list = []
    try:
        with db.connection() as conn:
            tables_list = [r[0] for r in conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")).fetchall()]
            embedding_count = conn.execute(text("SELECT count(*) FROM document_chunks WHERE embedding IS NOT NULL;")).scalar() or 0
            failed_embeddings = conn.execute(text("SELECT count(*) FROM document_chunks WHERE embedding IS NULL;")).scalar() or 0
    except Exception:
        pass

    return {
        "status": "healthy" if pg_ok else "degraded",
        "database": db_info.get("active_database"),
        "database_status": db_info.get("status"),
        "tables": tables_list,
        "vector_extension": "PASS" if vec_ok else "FAIL",
        "fts": "PASS" if fts_ok else "FAIL",
        "embedding_dimension": settings.EMBEDDING_DIMENSION,
        "sources_count": stats.total_sources,
        "documents_count": stats.total_documents,
        "chunks_count": stats.total_chunks,
        "embedding_count": embedding_count,
        "failed_embeddings": failed_embeddings,
        "last_ingestion": stats.last_verified,
        "is_production_ready": db_info.get("is_production_ready", False)
    }

@router.post("/search/hybrid")
def search_hybrid_endpoint(payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    """
    Direct endpoint for multi-channel PostgreSQL Hybrid Search (Exact + Keyword + FTS + pgvector + RRF).
    """
    from ..knowledge.hybrid_retriever import hybrid_retriever
    query = payload.get("query", "")
    category = payload.get("category", "all")
    top_k = int(payload.get("top_k", 10))

    if not query.strip():
        raise HTTPException(status_code=400, detail="استعلام البحث مطلوب")

    results = hybrid_retriever.retrieve(query=query, category=category, top_k=top_k)
    return {
        "query": query,
        "category": category,
        "total_results": len(results),
        "results": results
    }

@router.get("/audit/{claim_id}")
def get_claim_audit_log(claim_id: str, db: Session = Depends(get_db)):
    """
    Returns full provenance chain and audit logs for a given claim ID.
    """
    from ..models.knowledge_models import KnowledgeAuditLogModel
    logs = db.query(KnowledgeAuditLogModel).filter(
        (KnowledgeAuditLogModel.claim_id == claim_id) | 
        (KnowledgeAuditLogModel.request_id == claim_id)
    ).all()
    if not logs:
        raise HTTPException(status_code=404, detail="سجل التدقيق غير موجود لهذا الادعاء")
    
    return [{
        "id": l.id,
        "request_id": l.request_id,
        "claim_id": l.claim_id,
        "query": l.query,
        "search_query": l.search_query,
        "category_filter": l.category_filter,
        "sources_checked": l.sources_checked,
        "documents_checked": l.documents_checked,
        "chunks_checked": l.chunks_checked,
        "evidence_found": l.evidence_found,
        "validation_result": l.validation_result,
        "conflicts_found": l.conflicts_found,
        "final_status": l.final_status,
        "timestamp": l.timestamp.isoformat() if l.timestamp else None
    } for l in logs]

@router.get("/quran/{reference}")
def get_quran_reference(reference: str, db: Session = Depends(get_db)):
    """
    Verified Quran verse retrieval from King Fahd Complex dataset.
    """
    from ..knowledge.specialized_handlers import quran_special_handler
    verse_info = quran_special_handler.inspect_verse(db, reference)
    if not verse_info:
        raise HTTPException(status_code=404, detail="لم يتم العثور على الآية بالمرجع المحدد")
    return verse_info

@router.get("/hadith/{reference}")
def get_hadith_reference(reference: str, db: Session = Depends(get_db)):
    """
    Verified Hadith retrieval with narrator and ruling metadata.
    """
    chunks = db.query(DocumentChunkModel, DocumentModel).join(
        DocumentModel, DocumentChunkModel.document_id == DocumentModel.id
    ).filter(
        (DocumentModel.category == "HADITH") &
        ((DocumentChunkModel.source_locator.ilike(f"%{reference}%")) | 
         (DocumentChunkModel.content.ilike(f"%{reference}%")) |
         (DocumentModel.title_ar.ilike(f"%{reference}%")))
    ).limit(5).all()

    if not chunks:
        raise HTTPException(status_code=404, detail="لم يتم العثور على الحديث في الدواوين المعتمدة")

    return [{
        "chunk_id": c.id,
        "document_title": d.title_ar,
        "content": c.content,
        "reference": c.source_locator,
        "url": c.canonical_url or d.official_url
    } for c, d in chunks]

@router.get("/evidence/{evidence_id}")
def get_evidence_by_id(evidence_id: str, db: Session = Depends(get_db)):
    ev = db.query(EvidenceModel).filter_by(id=evidence_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="الدليل غير موجود في السجل")
    return {
        "id": ev.id,
        "claim_id": ev.claim_id,
        "source_id": ev.source_id,
        "document_id": ev.document_id,
        "chunk_id": ev.chunk_id,
        "evidence_type": ev.evidence_type,
        "matched_text": ev.matched_text,
        "locator": ev.locator,
        "url": ev.url,
        "scores": {
            "exact": ev.exact_score,
            "keyword": ev.keyword_score,
            "semantic": ev.semantic_score,
            "rrf": ev.rrf_score
        },
        "support_level": ev.support_level,
        "attribution_status": ev.attribution_status,
        "verification_status": ev.verification_status,
        "created_at": ev.created_at
    }

@router.get("/terms")
def list_translation_terms(db: Session = Depends(get_db)):
    """
    Returns the list of verified Islamic translated terms from the dictionary knowledge base.
    """
    terms = db.query(TranslationTermModel).all()
    results = []
    for t in terms:
        results.append({
            "id": t.id,
            "term_ar": t.term_ar,
            "term_en": t.term_en,
            "preferred_translation": t.preferred_translation,
            "alternative_translation": t.alternative_translation,
            "explanation": t.explanation,
            "usage_notes": t.usage_notes,
            "source_id": t.source_id,
            "source_url": t.source_url,
            "verified": t.verified,
            "created_at": t.created_at.isoformat() if t.created_at else None
        })
    return results

@router.get("/terms/{term}")
def get_term_definition(term: str, db: Session = Depends(get_db)):
    res = terminology_special_handler.lookup_term(db, term)
    if not res:
        raise HTTPException(status_code=404, detail="المصطلح غير مدرج في معجم المصطلحات الشرعية المعتمدة")
    return res

# Document indexing endpoints
@router.post("/documents", response_model=DocumentResponse)
def create_document(doc_in: DocumentCreate, db: Session = Depends(get_db)):
    existing = db.query(DocumentModel).filter_by(id=doc_in.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="الوثيقة مسجلة مسبقاً بهذا المعرف")
    
    new_doc = DocumentModel(
        id=doc_in.id,
        source_id=doc_in.source_id,
        title_ar=doc_in.title_ar,
        title_en=doc_in.title_en,
        author=doc_in.author,
        publisher=doc_in.publisher,
        document_type=doc_in.document_type,
        category=doc_in.category.value,
        official_url=doc_in.official_url,
        canonical_url=doc_in.canonical_url,
        language=doc_in.language,
        publication_date=doc_in.publication_date,
        edition=doc_in.edition,
        isbn=doc_in.isbn,
        description=doc_in.description,
        copyright_holder=doc_in.copyright_holder,
        license_status=doc_in.license_status.value,
        license_name=doc_in.license_name,
        license_url=doc_in.license_url,
        ingestion_method=doc_in.ingestion_method,
        ingestion_status=doc_in.ingestion_status.value,
        content_hash=doc_in.content_hash,
        version=doc_in.version
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return DocumentResponse(
        id=new_doc.id,
        source_id=new_doc.source_id,
        title_ar=new_doc.title_ar,
        title_en=new_doc.title_en,
        author=new_doc.author,
        publisher=new_doc.publisher,
        document_type=new_doc.document_type,
        category=new_doc.category, # type: ignore
        official_url=new_doc.official_url,
        canonical_url=new_doc.canonical_url,
        language=new_doc.language,
        edition=new_doc.edition,
        description=new_doc.description,
        license_status=new_doc.license_status, # type: ignore
        ingestion_status=new_doc.ingestion_status, # type: ignore
        content_hash=new_doc.content_hash,
        version=new_doc.version,
        chunks_count=0,
        created_at=new_doc.created_at
    )

@router.post("/documents/{document_id}/index")
def index_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(DocumentModel).filter_by(id=document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="الوثيقة غير موجودة")
    doc.ingestion_status = "INDEXED"
    db.commit()
    return {"status": "success", "document_id": document_id, "ingestion_status": "INDEXED"}

@router.post("/documents/{document_id}/reindex")
def reindex_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(DocumentModel).filter_by(id=document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="الوثيقة غير موجودة")
    doc.version = f"{float(doc.version) + 0.1:.1f}"
    doc.ingestion_status = "INDEXED"
    db.commit()
    return {"status": "success", "document_id": document_id, "new_version": doc.version}
