"""
Bayyinah AI - Admin Knowledge Management & Expansion Router
Enforces Section 23, 24, 25 of Master Specifications:
Provides administrative endpoints for autonomous knowledge acquisition, review queue,
health monitoring, manual sync triggers, and live statistics from PostgreSQL.
"""

import time
import datetime
import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path
from sqlalchemy.orm import Session
from sqlalchemy import text, func

from ..db.database import get_db
from ..ingestion.acquisition_engine import acquisition_engine
from ..ingestion.acquisition_queue import acquisition_queue
from ..ingestion.scheduler import knowledge_scheduler
from ..ingestion.official_allowlist import OFFICIAL_SOURCE_ALLOWLIST
from ..ingestion.source_adapters.adapter_registry import get_all_adapters, get_adapter_by_slug
from ..models.knowledge_models import (
    SourceModel,
    DocumentModel,
    DocumentChunkModel,
    DocumentVersionModel,
    IngestionJobModel,
    KnowledgeReviewItemModel,
    VerificationResultModel,
    ClaimModel,
    EvidenceModel
)

logger = logging.getLogger("bayyinah.api.admin_knowledge")

router = APIRouter(prefix="/api/admin/knowledge", tags=["Admin Knowledge Management"])

# 1. Sync All
@router.post("/sync")
def sync_all_sources(
    max_docs_per_source: int = Query(2, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """
    Triggers autonomous discovery and incremental ingestion across all 11 official sources.
    """
    return knowledge_scheduler.trigger_sync_now(db)

# 2. Sync Specific Source
@router.post("/sources/{source_id_or_slug}/sync")
def sync_specific_source(
    source_id_or_slug: str,
    max_documents: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Triggers autonomous discovery and incremental acquisition for a single official source.
    """
    return acquisition_engine.discover_and_expand_source(db, source_id_or_slug, max_documents=max_documents)

# 3. Reprocess Document
@router.post("/documents/{document_id}/reprocess")
def reprocess_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Forces refetching, re-extracting, chunking, and re-embedding of an existing document.
    """
    doc = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="الوثيقة غير موجودة.")
    
    url = doc.canonical_url or doc.url
    if not url:
        raise HTTPException(status_code=400, detail="الوثيقة لا تحتوي على رابط أصلي لإعادة المعالجة.")

    # Re-acquire
    res = acquisition_engine.acquire_from_url(db, url, source_id=doc.source_id)
    return res

# 4. Reverify Document
@router.post("/documents/{document_id}/reverify")
def reverify_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Runs quality gate evaluation and citation verification on a document.
    """
    from ..ingestion.quality_gate import quality_gate
    doc = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="الوثيقة غير موجودة.")

    doc_data = {
        "id": doc.id,
        "url": doc.canonical_url or doc.url,
        "content": doc.content,
        "reference": doc.reference,
        "content_hash": doc.content_hash,
        "version": doc.version or "1.0",
        "title": doc.title
    }
    eval_res = quality_gate.evaluate_document(doc_data, doc.source_id, db=db)
    return {
        "document_id": doc.id,
        "quality_status": eval_res["status"],
        "reason": eval_res["reason"],
        "checklist": eval_res["checklist"]
    }

# 5. List Ingestion Jobs
@router.get("/jobs")
def get_knowledge_jobs(
    limit: int = Query(25, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Lists background acquisition and indexing jobs.
    """
    query = db.query(IngestionJobModel)
    if status:
        query = query.filter(IngestionJobModel.status == status)
    jobs = query.order_by(IngestionJobModel.started_at.desc().nullslast()).limit(limit).all()

    return {
        "total": len(jobs),
        "jobs": [
            {
                "id": j.id,
                "source_id": j.source_id,
                "job_type": j.job_type,
                "status": j.status,
                "documents_discovered": j.documents_discovered,
                "documents_processed": j.documents_processed,
                "chunks_created": j.chunks_created,
                "embeddings_created": j.embeddings_created,
                "error_count": j.error_count,
                "started_at": j.started_at.isoformat() if j.started_at else None,
                "finished_at": j.finished_at.isoformat() if j.finished_at else None
            }
            for j in jobs
        ]
    }

# 6. Review Queue
@router.get("/review-queue")
def get_review_queue(
    status: str = Query("PENDING"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Lists items requiring human review (Section 22: parsing failure, conflict, dead-letter, etc.)
    """
    items = db.query(KnowledgeReviewItemModel).filter(
        KnowledgeReviewItemModel.status == status
    ).order_by(KnowledgeReviewItemModel.created_at.desc()).limit(limit).all()

    return {
        "status": status,
        "count": len(items),
        "items": [
            {
                "id": it.id,
                "source_id": it.source_id,
                "document_id": it.document_id,
                "item_type": it.item_type,
                "severity": it.severity,
                "reason": it.reason,
                "url": it.url,
                "details": it.details,
                "created_at": it.created_at.isoformat() if it.created_at else None
            }
            for it in items
        ]
    }

# 7. Resolve Review Item
@router.post("/review-queue/{item_id}/resolve")
def resolve_review_item(
    item_id: str,
    action: str = Body(..., embed=True), # APPROVE, REJECT
    notes: Optional[str] = Body(None, embed=True),
    db: Session = Depends(get_db)
):
    """
    Allows admin to approve or reject items in the review queue.
    """
    item = db.query(KnowledgeReviewItemModel).filter(KnowledgeReviewItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="عنصر المراجعة غير موجود.")

    action_norm = action.upper()
    if action_norm not in ["APPROVE", "REJECT", "RESOLVE"]:
        raise HTTPException(status_code=400, detail="الإجراء يجب أن يكون APPROVE أو REJECT.")

    item.status = "APPROVED" if action_norm == "APPROVE" else "REJECTED"
    item.resolution_notes = notes or "تمت المعالجة بواسطة الإشراف العلمي."
    item.resolved_by = "ADMIN"
    item.resolved_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()

    return {
        "success": True,
        "item_id": item.id,
        "status": item.status,
        "resolution_notes": item.resolution_notes
    }

# 8. Detailed Real Statistics (Section 24)
@router.get("/stats")
def get_detailed_knowledge_stats(db: Session = Depends(get_db)):
    """
    Retrieves real live knowledge base statistics from PostgreSQL without any mocks.
    """
    sources_count = db.query(func.count(SourceModel.id)).filter(SourceModel.is_active == True).scalar() or 0
    docs_count = db.query(func.count(DocumentModel.id)).scalar() or 0
    chunks_count = db.query(func.count(DocumentChunkModel.id)).scalar() or 0
    versions_count = db.query(func.count(DocumentVersionModel.id)).scalar() or 0
    evidence_count = db.query(func.count(EvidenceModel.id)).scalar() or 0
    claims_count = db.query(func.count(ClaimModel.id)).scalar() or 0
    jobs_count = db.query(func.count(IngestionJobModel.id)).scalar() or 0
    pending_reviews = db.query(func.count(KnowledgeReviewItemModel.id)).filter(
        KnowledgeReviewItemModel.status == "PENDING"
    ).scalar() or 0

    # Counts by category
    cat_rows = db.query(DocumentModel.category, func.count(DocumentModel.id)).group_by(DocumentModel.category).all()
    by_category = {cat: count for cat, count in cat_rows if cat}

    return {
        "success": True,
        "database": "Supabase PostgreSQL (Production)",
        "vector_dimensions": 768,
        "search_engine": "Hybrid (Arabic FTS + pgvector Cosine)",
        "sources": sources_count,
        "documents": docs_count,
        "chunks": chunks_count,
        "document_versions": versions_count,
        "evidence_records": evidence_count,
        "claims_processed": claims_count,
        "ingestion_jobs": jobs_count,
        "pending_reviews": pending_reviews,
        "category_distribution": by_category,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

# 9. Source Health Monitor (Section 23)
@router.get("/sources-health")
def get_sources_health():
    """
    Performs real live HTTP connectivity and latency checks for all 11 official sources.
    """
    adapters = get_all_adapters()
    health_results = []
    for slug, adapter in adapters.items():
        res = adapter.health_check()
        health_results.append(res)
    return {
        "success": True,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_sources": len(health_results),
        "sources": health_results
    }

# 10. Scheduler Configurations
@router.get("/scheduler")
def get_scheduler_status():
    """
    Returns scheduling configurations and intervals for all 11 sources.
    """
    return {
        "success": True,
        "configs": knowledge_scheduler.get_source_configs()
    }
