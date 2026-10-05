"""
Bayyinah AI - Autonomous Knowledge Acquisition Engine
The central engine for continuous, verified knowledge base expansion.
Enforces the full 10-step lifecycle:
1. Official Allowlist Validation (Strictly the 11 Challenge Sources)
2. Discovery (Adapter index crawling, sitemap, or SerpAPI site-restricted discovery)
3. Safe Fetching (Ethical headers, respectful rate-limits)
4. Extraction (Domain-specific structured extraction via adapters)
5. Arabic Normalization (Original preserved verbatim, normalized alongside for FTS)
6. Incremental Deduplication & Provenance Hashing (SHA-256)
7. Versioning (document_versions history with diffs on content changes)
8. Semantic Chunking (Structure-preserving chunks)
9. 768-d Vector Embeddings & pgvector + Arabic FTS Indexing
10. Quality Gate Evaluation & Review Queue Flagging
"""

import hashlib
import uuid
import datetime
import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text

from .official_allowlist import (
    is_url_in_allowlist,
    get_matched_allowlist_entry,
    OFFICIAL_SOURCE_ALLOWLIST,
    APPROVED_SOURCE_DOMAINS
)
from .source_adapters.adapter_registry import get_adapter_by_url, get_adapter_by_slug
from .quality_gate import quality_gate
from .chunker import chunker
from .embedding_worker import embedding_worker
from .indexer import knowledge_indexer
from .acquisition_queue import acquisition_queue
from ..utils.arabic_normalizer import normalize_arabic
from ..models.knowledge_models import (
    SourceModel,
    DocumentModel,
    DocumentChunkModel,
    DocumentVersionModel,
    KnowledgeReviewItemModel
)

logger = logging.getLogger("bayyinah.ingestion.acquisition_engine")

class KnowledgeAcquisitionEngine:
    """
    Autonomous Knowledge Engine responsible for continuous, trusted knowledge expansion.
    """

    def acquire_from_url(
        self,
        db: Session,
        url: str,
        source_id: Optional[str] = None,
        job_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end knowledge acquisition for a single official canonical URL.
        """
        url = url.strip()
        # 1. Official Allowlist Guard
        if not is_url_in_allowlist(url):
            logger.warning(f"Rejected unapproved acquisition URL: {url}")
            return {
                "success": False,
                "status": "REJECTED_UNAPPROVED_DOMAIN",
                "error": "الرابط المطلوب لا ينتمي إلى أحد المصادر الـ 11 الرسمية المعتمدة للمشروع."
            }

        allowlist_entry = get_matched_allowlist_entry(url)
        if not allowlist_entry:
            return {"success": False, "status": "UNKNOWN_SOURCE", "error": "المصدر غير معروف في القائمة المعتمدة."}

        target_source_id = source_id or allowlist_entry["id"]

        # Ensure Source exists in DB
        src_record = db.query(SourceModel).filter(SourceModel.id == target_source_id).first()
        if not src_record:
            src_record = SourceModel(
                id=target_source_id,
                name=allowlist_entry["name_ar"],
                name_ar=allowlist_entry["name_ar"],
                name_en=allowlist_entry.get("name_en"),
                base_domain=allowlist_entry["domain"],
                url=allowlist_entry["base_url"],
                category=allowlist_entry.get("category", "GENERAL"),
                authority_level=allowlist_entry.get("authority_level", "PRIMARY_CANONICAL"),
                content_scope=allowlist_entry.get("content_scope"),
                is_active=True,
                trust_status="APPROVED",
                scientific_status="APPROVED",
                approved_by_challenge=True
            )
            db.add(src_record)
            db.commit()

        # 2. Fetch via Official Adapter
        adapter = get_adapter_by_url(url)
        if not adapter:
            adapter = get_adapter_by_slug(allowlist_entry["slug"])

        if not adapter:
            return {"success": False, "status": "NO_ADAPTER", "error": "لا يوجد محول برمجي مخصص لهذا المصدر."}

        fetch_res = adapter.fetch(url, timeout=15)
        if not fetch_res.get("success") or not fetch_res.get("html"):
            error_msg = fetch_res.get("error", "فشل جلب الصفحة من المصدر.")
            logger.error(f"Failed to fetch {url}: {error_msg}")
            # Flag in review queue
            try:
                rev = KnowledgeReviewItemModel(
                    source_id=target_source_id,
                    item_type="INACCESSIBLE_SOURCE",
                    severity="MEDIUM",
                    status="PENDING",
                    reason=f"تعذر جلب المحتوى من الرابط المعتمد: {error_msg}",
                    url=url
                )
                db.add(rev)
                db.commit()
            except Exception:
                pass
            return {"success": False, "status": "FETCH_FAILED", "error": error_msg}

        # 3. Parse and Extract Structured Evidence
        parsed = adapter.parse(fetch_res["html"], url)
        evidence_item = adapter.extract_evidence(parsed)

        raw_content = evidence_item["content"]
        if not raw_content or len(raw_content.strip()) < 15:
            return {"success": False, "status": "EMPTY_CONTENT", "error": "المحتوى المسترجع فارغ أو قصير جدًا."}

        content_hash = evidence_item["content_hash"]
        norm_text = evidence_item["normalized_content"]
        norm_hash = evidence_item["normalized_hash"]
        title = evidence_item["title"]
        reference = evidence_item["reference"]

        # 4. Incremental Crawling & Deduplication Check
        existing_doc = db.query(DocumentModel).filter(
            (DocumentModel.canonical_url == url) | (DocumentModel.url == url)
        ).first()

        now_utc = datetime.datetime.now(datetime.timezone.utc)

        if existing_doc:
            if existing_doc.content_hash == content_hash:
                # Content unchanged -> update last_seen_at and return
                existing_doc.last_seen_at = now_utc
                db.commit()
                logger.info(f"Incremental crawl: Document at {url} is unchanged. Skipped reprocessing.")
                return {
                    "success": True,
                    "status": "SKIPPED_UNCHANGED",
                    "document_id": existing_doc.id,
                    "source_id": target_source_id,
                    "version": existing_doc.version or "1.0",
                    "content_hash": content_hash,
                    "message": "الوثيقة موجودة بالفعل ولم يطرأ أي تعديل على محتواها."
                }
            else:
                # Content changed -> Archive old version in document_versions
                logger.info(f"Content changed for document {existing_doc.id}. Creating new version.")
                old_ver = DocumentVersionModel(
                    document_id=existing_doc.id,
                    version=existing_doc.version or "1.0",
                    content_hash=existing_doc.content_hash,
                    title=existing_doc.title,
                    content=existing_doc.content,
                    reference=existing_doc.reference,
                    diff_summary=f"تحديث آلي للمحتوى بتأريخ {now_utc.isoformat()}"
                )
                db.add(old_ver)

                # Bump version
                try:
                    curr_v = float(existing_doc.version or "1.0")
                    new_version = f"{curr_v + 0.1:.1f}"
                except ValueError:
                    new_version = "2.0"

                existing_doc.content = raw_content
                existing_doc.content_ar = raw_content
                existing_doc.content_hash = content_hash
                existing_doc.version = new_version
                existing_doc.last_changed_at = now_utc
                existing_doc.last_seen_at = now_utc
                existing_doc.updated_at = now_utc
                db.commit()
                doc_id = existing_doc.id
                current_version = new_version
        else:
            # New Document
            doc_id = str(uuid.uuid4())
            current_version = "1.0"
            new_doc = DocumentModel(
                id=doc_id,
                source_id=target_source_id,
                title=title,
                title_ar=title,
                content=raw_content,
                content_ar=raw_content,
                author=evidence_item.get("author") or evidence_item.get("scholar") or "محقق معتمد",
                document_type=evidence_item.get("content_type", "SCHOLARLY_TEXT").upper(),
                category=allowlist_entry.get("category", "GENERAL"),
                reference=reference,
                url=url,
                canonical_url=url,
                language="ar",
                content_hash=content_hash,
                version=current_version,
                last_seen_at=now_utc,
                last_changed_at=now_utc,
                created_at=now_utc,
                updated_at=now_utc,
                ingestion_method="AUTONOMOUS_ACQUISITION",
                ingestion_status="PROCESSING"
            )
            db.add(new_doc)
            db.commit()

        # 5. Quality Gate Evaluation
        doc_payload = {
            "id": doc_id,
            "source_id": target_source_id,
            "url": url,
            "canonical_url": url,
            "official_url": url,
            "content": raw_content,
            "content_ar": raw_content,
            "reference": reference,
            "content_hash": content_hash,
            "version": current_version,
            "title": title,
            "title_ar": title,
            "category": allowlist_entry.get("category", "GENERAL"),
            "author": evidence_item.get("author") or evidence_item.get("scholar") or "محقق معتمد",
            "publisher": allowlist_entry.get("name_ar"),
            "rights_status": "PUBLIC_ACCESS",
            "metadata": {"discovered_by": "acquisition_engine", "job_id": str(job_id) if job_id else None}
        }
        q_eval = quality_gate.evaluate_document(doc_payload, target_source_id, db=db)
        if q_eval["status"] == "REJECT":
            return {
                "success": False,
                "status": "REJECTED_QUALITY_GATE",
                "document_id": doc_id,
                "reason": q_eval["reason"],
                "checklist": q_eval["checklist"]
            }

        # 6. Semantic Chunking
        doc_chunks = chunker.chunk_document(raw_content, {
            "title": title,
            "reference": reference,
            "category": allowlist_entry.get("category", "GENERAL")
        })

        if not doc_chunks:
            return {"success": False, "status": "CHUNKING_FAILED", "error": "تعذر تجزئة الوثيقة."}

        # 7. Generate 768-d Vector Embeddings
        chunks_with_embeddings = embedding_worker.process_chunks(doc_chunks)

        # 8. Index into PostgreSQL (pgvector + FTS)
        index_res = knowledge_indexer.index_document_and_chunks(db, doc_payload, chunks_with_embeddings)

        # Update document status to INDEXED
        doc_record = db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
        if doc_record:
            doc_record.ingestion_status = "INDEXED"
            doc_record.indexing_status = "INDEXED"
            db.commit()

        return {
            "success": True,
            "status": "INDEXED",
            "document_id": doc_id,
            "source_id": target_source_id,
            "source_name": allowlist_entry["name_ar"],
            "title": title,
            "canonical_url": url,
            "version": current_version,
            "chunks_count": index_res.get("chunks_indexed", len(doc_chunks)),
            "content_hash": content_hash,
            "quality_status": q_eval["status"],
            "quality_reason": q_eval["reason"]
        }

    def discover_and_expand_source(
        self,
        db: Session,
        source_id_or_slug: str,
        max_documents: int = 5
    ) -> Dict[str, Any]:
        """
        Discovers candidate URLs from the target official source and incrementally acquires them.
        """
        entry = next(
            (s for s in OFFICIAL_SOURCE_ALLOWLIST if s["id"] == source_id_or_slug or s["slug"] == source_id_or_slug),
            None
        )
        if not entry:
            return {"success": False, "error": f"المصدر {source_id_or_slug} ليس ضمن المصادر الـ 11 المعتمدة."}

        adapter = get_adapter_by_slug(entry["slug"])
        if not adapter:
            return {"success": False, "error": f"لا يوجد محول للمصدر {entry['slug']}"}

        # Create acquisition job
        job = acquisition_queue.create_job(
            db=db,
            job_type="DISCOVER_AND_EXPAND",
            source_id=entry["id"],
            metadata={"slug": entry["slug"], "max_documents": max_documents}
        )
        acquisition_queue.start_job(db, job.id)

        try:
            candidate_urls = adapter.discover(max_urls=max_documents)
            results = []
            indexed_count = 0
            skipped_count = 0
            chunks_total = 0

            for url in candidate_urls:
                try:
                    res = self.acquire_from_url(db=db, url=url, source_id=entry["id"], job_id=job.id)
                    results.append(res)
                    if res.get("success"):
                        if res.get("status") == "INDEXED":
                            indexed_count += 1
                            chunks_total += res.get("chunks_count", 0)
                        elif res.get("status") == "SKIPPED_UNCHANGED":
                            skipped_count += 1
                except Exception as url_err:
                    db.rollback()
                    logger.error(f"Error acquiring {url}: {url_err}")
                    results.append({"url": url, "success": False, "error": str(url_err)})

            acquisition_queue.finish_job(db, job.id, {
                "documents_discovered": len(candidate_urls),
                "documents_processed": indexed_count + skipped_count,
                "chunks_created": chunks_total,
                "embeddings_created": chunks_total
            })

            return {
                "success": True,
                "job_id": job.id,
                "source_id": entry["id"],
                "source_name": entry["name_ar"],
                "discovered_urls_count": len(candidate_urls),
                "newly_indexed_documents": indexed_count,
                "skipped_unchanged_documents": skipped_count,
                "total_chunks_created": chunks_total,
                "details": results
            }
        except Exception as e:
            try:
                db.rollback()
            except Exception:
                pass
            acquisition_queue.fail_job(db, job.id, str(e))
            logger.error(f"Discovery and expansion failed for {entry['slug']}: {e}")
            return {"success": False, "job_id": job.id, "error": str(e)}

    def sync_all_official_sources(
        self,
        db: Session,
        max_docs_per_source: int = 2
    ) -> Dict[str, Any]:
        """
        Iterates over all 11 official sources, runs live discovery, and indexes fresh content.
        """
        overall_results = []
        total_indexed = 0
        total_chunks = 0

        for entry in OFFICIAL_SOURCE_ALLOWLIST:
            try:
                res = self.discover_and_expand_source(db, entry["slug"], max_documents=max_docs_per_source)
                overall_results.append(res)
                if res.get("success"):
                    total_indexed += res.get("newly_indexed_documents", 0)
                    total_chunks += res.get("total_chunks_created", 0)
            except Exception as e:
                logger.error(f"Sync error for {entry['slug']}: {e}")
                overall_results.append({"slug": entry["slug"], "success": False, "error": str(e)})

        return {
            "success": True,
            "sources_synced_count": len(overall_results),
            "total_newly_indexed_documents": total_indexed,
            "total_chunks_created": total_chunks,
            "sources_results": overall_results
        }

acquisition_engine = KnowledgeAcquisitionEngine()
