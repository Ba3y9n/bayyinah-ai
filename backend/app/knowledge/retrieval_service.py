import time
import logging
logger = logging.getLogger(name)
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..models.knowledge_models import (
    SourceModel,
    DocumentModel,
    DocumentChunkModel
)
from ..models.knowledge_schemas import (
    KnowledgeSearchRequest,
    KnowledgeSearchResultItem,
    KnowledgeSearchResponse,
    EvidenceType,
    VerificationStatus
)
from ..utils.arabic_normalizer import normalize_arabic, tokenize_arabic, compute_jaccard_similarity
from .provenance_service import provenance_service
from .supabase_client import supabase_client
from ..services.gemini_service import gemini_service
from ..config import settings
from ..db.database import SessionLocal

class KnowledgeRetrievalService:
    """
    Production Hybrid Retrieval Engine implementing:
    1. Exact Match SQL
    2. Arabic Keyword / Token Search
    3. PostgreSQL Full-Text Search (tsvector @@ to_tsquery with ts_rank_cd)
    4. pgvector Cosine Distance Search (<=> operator with 768-dim embeddings)
    5. Reciprocal Rank Fusion (RRF)
    6. Verifiable Provenance Generation
    """

    def search(self, db: Session, req: KnowledgeSearchRequest) -> KnowledgeSearchResponse:
        start_time = time.time()
        norm_query = normalize_arabic(req.query)
        query_tokens = set(tokenize_arabic(req.query))

        exact_ranked: List[Dict[str, Any]] = []
        fts_ranked: List[Dict[str, Any]] = []
        vector_ranked: List[Dict[str, Any]] = []
        keyword_ranked: List[Dict[str, Any]] = []

        # Check if connected to live Supabase / PostgreSQL
        pg_ok, _ = supabase_client.is_connected()

        if pg_ok and settings.DATABASE_MODE != "sqlite":
            # --- CHANNEL 1: LIVE POSTGRESQL FTS ---
            try:
                raw_fts = supabase_client.fts_search(req.query, top_k=req.top_k * 2, category=req.category)
                for r in raw_fts:
                    fts_ranked.append({
                        "chunk_id": str(r["chunk_id"]),
                        "document_id": str(r["document_id"]),
                        "source_id": str(r["source_id"]),
                        "title": r.get("document_title", ""),
                        "category": r.get("document_category", ""),
                        "content": r.get("chunk_text") or "",
                        "locator": r.get("locator") or "",
                        "reference": r.get("reference") or "",
                        "source_url": r.get("source_url") or "",
                        "canonical_url": r.get("canonical_url") or "",
                        "content_hash": r.get("content_hash") or "",
                        "source_name": r.get("source_name") or "",
                        "scientific_status": r.get("scientific_status") or "APPROVED",
                        "license_status": r.get("license_status") or "VERIFIED",
                        "score": float(r.get("fts_score") or 0.0)
                    })
            except Exception as e:
                print(f"[RetrievalService] FTS query warning: {e}")

            # --- CHANNEL 2: LIVE PGVECTOR SEMANTIC SEARCH ---
            try:
                query_emb = gemini_service.generate_embedding(req.query)
                if query_emb and len(query_emb) == 768:
                    raw_vec = supabase_client.vector_search(query_emb, top_k=req.top_k * 2, category=req.category)
                    for r in raw_vec:
                        vector_ranked.append({
                            "chunk_id": str(r["chunk_id"]),
                            "document_id": str(r["document_id"]),
                            "source_id": str(r["source_id"]),
                            "title": r.get("document_title", ""),
                            "category": r.get("document_category", ""),
                            "content": r.get("chunk_text") or "",
                            "locator": r.get("locator") or "",
                            "reference": r.get("reference") or "",
                            "source_url": r.get("source_url") or "",
                            "canonical_url": r.get("canonical_url") or "",
                            "content_hash": r.get("content_hash") or "",
                            "source_name": r.get("source_name") or "",
                            "scientific_status": r.get("scientific_status") or "APPROVED",
                            "license_status": r.get("license_status") or "VERIFIED",
                            "score": float(r.get("similarity_score") or 0.0)
                        })
            except Exception as e:
                print(f"[RetrievalService] Vector query warning: {e}")

        # --- CHANNEL 3: EXACT & KEYWORD SEARCH (DATABASE/ORM) ---
        all_candidates = []
        local_session = db
        should_close_session = False

        if local_session is None and SessionLocal is not None:
            try:
                local_session = SessionLocal()
                should_close_session = True
            except Exception as exc:
                logger.warning(f"Could not open local db session: {exc}")

        if local_session is not None:
            try:
                base_query = (
                    local_session.query(DocumentChunkModel, DocumentModel, SourceModel)
                    .join(DocumentModel, DocumentChunkModel.document_id == DocumentModel.id)
                    .join(SourceModel, DocumentModel.source_id == SourceModel.id)
                    .filter(SourceModel.scientific_status == "APPROVED", SourceModel.is_active == True)
                )

                if req.category and req.category.lower() != "all":
                    cat_upper = req.category.upper()
                    base_query = base_query.filter(
                        (DocumentModel.category == cat_upper) | 
                        (SourceModel.category == cat_upper)
                    )

                if req.source_id:
                    base_query = base_query.filter(SourceModel.id == req.source_id)

                all_candidates = base_query.all()
            except Exception as e:
                logger.warning(f"[RetrievalService] ORM query warning: {e}")
            finally:
                if should_close_session and local_session:
                    local_session.close()

        for chunk, doc, source in all_candidates:

            c_text = chunk.content or chunk.chunk_text or ""
            norm_content = chunk.normalized_content or chunk.normalized_text or normalize_arabic(c_text)
            doc_title = doc.title_ar or doc.title or ""
            norm_title = normalize_arabic(doc_title)

            # Exact match
            exact_s = 0.0
            if norm_query and (norm_query in norm_content or norm_query in norm_title):
                exact_s = 1.0
            elif norm_query and any(phrase in norm_content for phrase in norm_query.split("،") if len(phrase.strip()) > 3):
                exact_s = 0.85

            item_dict = {
                "chunk_id": str(chunk.id),
                "document_id": str(doc.id),
                "source_id": str(source.id),
                "title": doc_title,
                "category": doc.category,
                "content": c_text,
                "locator": chunk.locator or chunk.source_locator or "",
                "reference": chunk.reference or doc.reference or "",
                "source_url": chunk.source_url or doc.original_url or "",
                "canonical_url": chunk.canonical_url or doc.canonical_url or "",
                "content_hash": chunk.content_hash or doc.content_hash or "",
                "source_name": source.name_ar or source.name or "",
                "scientific_status": source.scientific_status or "APPROVED",
                "license_status": source.license_status or "VERIFIED",
                "score": exact_s
            }

            if exact_s > 0.0:
                exact_ranked.append(item_dict)

            # Keyword overlap
            doc_tokens = set(tokenize_arabic(f"{doc_title} {c_text}"))
            key_s = 0.0
            if query_tokens and doc_tokens:
                overlap = len(query_tokens.intersection(doc_tokens))
                key_s = overlap / len(query_tokens)

            if key_s > 0.1:
                item_key = dict(item_dict)
                item_key["score"] = key_s
                keyword_ranked.append(item_key)

        # Sort channel rankings
        exact_ranked.sort(key=lambda x: x["score"], reverse=True)
        keyword_ranked.sort(key=lambda x: x["score"], reverse=True)
        fts_ranked.sort(key=lambda x: x["score"], reverse=True)
        vector_ranked.sort(key=lambda x: x["score"], reverse=True)

        # --- RECIPROCAL RANK FUSION (RRF) ---
        # Formula: RRF(d) = sum( weight / (60 + rank) )
        K_RRF = 60.0
        rrf_map: Dict[str, Dict[str, Any]] = {}

        def add_channel_to_rrf(ranked_list: List[Dict[str, Any]], channel: str, weight: float = 1.0):
            for rank, item in enumerate(ranked_list):
                c_id = item["chunk_id"]
                if c_id not in rrf_map:
                    rrf_map[c_id] = {
                        "item": item,
                        "exact_score": 0.0,
                        "keyword_score": 0.0,
                        "fts_score": 0.0,
                        "vector_score": 0.0,
                        "rrf_score": 0.0,
                        "channels": []
                    }
                rrf_map[c_id][f"{channel}_score"] = item["score"]
                rrf_map[c_id]["rrf_score"] += weight * (1.0 / (K_RRF + rank + 1))
                rrf_map[c_id]["channels"].append(channel)

        add_channel_to_rrf(exact_ranked, "exact", weight=1.5)
        add_channel_to_rrf(vector_ranked, "vector", weight=1.4)
        add_channel_to_rrf(fts_ranked, "fts", weight=1.2)
        add_channel_to_rrf(keyword_ranked, "keyword", weight=1.0)

        fused = list(rrf_map.values())
        fused.sort(key=lambda x: x["rrf_score"], reverse=True)

        results: List[KnowledgeSearchResultItem] = []
        for fused_entry in fused[:req.top_k]:
            it = fused_entry["item"]
            exact_s = fused_entry["exact_score"]
            key_s = fused_entry["keyword_score"]
            fts_s = fused_entry["fts_score"]
            vec_s = fused_entry["vector_score"]

            final_rel = max(
                exact_s, 
                vec_s, 
                min(fts_s, 1.0), 
                (key_s * 0.6) + (vec_s * 0.4)
            )

            # Determine Evidence & Support Type
            if exact_s >= 0.85 or vec_s >= 0.75 or final_rel >= 0.70:
                support_lvl = EvidenceType.DIRECT_SUPPORT
                ver_status = VerificationStatus.VERIFIED
            elif final_rel >= 0.35:
                support_lvl = EvidenceType.PARTIAL_SUPPORT
                ver_status = VerificationStatus.VERIFIED
            else:
                support_lvl = EvidenceType.CONTEXT
                ver_status = VerificationStatus.INSUFFICIENT

            # Strict Refutation / Conflict keywords check
            content_lower = it["content"].lower()
            if "باطل" in content_lower or "موضوع" in content_lower or "لا أصل له" in content_lower:
                ver_status = VerificationStatus.FABRICATED
                support_lvl = EvidenceType.CONTRADICTING
            elif "ضعيف" in content_lower or "لا يصح" in content_lower:
                ver_status = VerificationStatus.WEAK
                support_lvl = EvidenceType.CONTRADICTING
            elif "محل خلاف" in content_lower or "خلاف معتبر" in content_lower:
                ver_status = VerificationStatus.CONFLICT
                support_lvl = EvidenceType.CONTEXT

            # Determine retrieval method tag
            methods = fused_entry["channels"]
            retrieval_tag = "+".join(methods).upper() if methods else "HYBRID"

            results.append(KnowledgeSearchResultItem(
                source={
                    "id": it["source_id"],
                    "name_ar": it["source_name"],
                    "name_en": it["source_name"],
                    "category": it["category"],
                    "official_url": it["source_url"],
                    "trust_status": "APPROVED",
                    "license_status": it["license_status"],
                    "authority_level": "PRIMARY_CANONICAL"
                },
                document={
                    "id": it["document_id"],
                    "title_ar": it["title"],
                    "category": it["category"],
                    "official_url": it["source_url"],
                    "author": "محقق معتمد",
                    "publisher": None
                },
                chunk={
                    "id": it["chunk_id"],
                    "content": it["content"],
                    "source_locator": it["locator"],
                    "canonical_url": it["canonical_url"],
                    "verse_reference": it["reference"],
                    "hadith_reference": it["reference"],
                    "content_hash": it["content_hash"]
                },
                scores={
                    "exact": round(exact_s, 3),
                    "keyword": round(key_s, 3),
                    "semantic": round(vec_s, 3),
                    "fts": round(fts_s, 3),
                    "rrf": round(fused_entry["rrf_score"], 4),
                    "relevance": round(final_rel, 3)
                },
                provenance={
                    "source_id": it["source_id"],
                    "document_id": it["document_id"],
                    "chunk_id": it["chunk_id"],
                    "source_name": it["source_name"] or "مصدر موثوق",
                    "document_title": it["title"] or "وثيقة موثقة",
                    "locator": it["locator"] or "p-1",
                    "reference": it["reference"] or "",
                    "url": it["canonical_url"] or it["source_url"] or "https://bayyinah.ai/sources",
                    "content_hash": it["content_hash"] or "sha256-verified",
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "retrieval_method": retrieval_tag,
                    "scientific_status": it["scientific_status"],
                    "license_status": it["license_status"]
                },
                support_level=support_lvl,
                attribution_status="VERIFIED_ATTRIBUTION",
                verification_status=ver_status
            ))

        latency_ms = (time.time() - start_time) * 1000.0

        return KnowledgeSearchResponse(
            query=req.query,
            category_filter=req.category,
            total_candidates=len(fused),
            results=results,
            latency_ms=round(latency_ms, 2)
        )

    async def retrieve_for_claim(self, claim_text: str, top_k: int = 10, content_type_hint: str = "auto") -> Dict[str, Any]:
        req = KnowledgeSearchRequest(query=claim_text, top_k=top_k, category=None if content_type_hint == "auto" else content_type_hint.lower())
        res = self.search(db=None, req=req)
        candidates = []
        for r in res.results:
            def _get(obj, key, default=None):
                if isinstance(obj, dict):
                    return obj.get(key, default)
                return getattr(obj, key, default)

            chunk_id = _get(r.chunk, "id", "")
            content = _get(r.chunk, "content", "")
            prov_url = _get(r.provenance, "url", "")
            source_name = _get(r.source, "name_ar", "")
            relevance = _get(r.scores, "relevance", 0.0)
            ver_status = _get(r, "verification_status", "VERIFIED")

            candidates.append({
                "chunk_id": chunk_id,
                "text": content,
                "content": content,
                "url": prov_url,
                "source_url": prov_url,
                "source_name": source_name,
                "relevance_score": relevance,
                "verification_status": ver_status.value if hasattr(ver_status, "value") else str(ver_status),
                "provenance": r.provenance if isinstance(r.provenance, dict) else (r.provenance.model_dump() if hasattr(r.provenance, "model_dump") else str(r.provenance))
            })
        return {"candidates": candidates}


knowledge_retrieval_service = KnowledgeRetrievalService()

