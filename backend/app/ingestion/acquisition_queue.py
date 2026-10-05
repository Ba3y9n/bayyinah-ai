"""
Bayyinah AI - Knowledge Acquisition Job Queue & Dead-Letter Queue
Enforces Sections 10, 11 of Master Specifications:
1. Asynchronous job queue handling large multi-stage acquisition workflows.
2. Tracks job state transitions: QUEUED -> RUNNING -> SUCCESS / FAILED / RETRYING / DEAD_LETTER.
3. Automatically routes failed jobs exceeding retry limits to the Dead-Letter Review Queue.
"""

import uuid
import json
import datetime
import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from ..models.knowledge_models import IngestionJobModel, KnowledgeReviewItemModel

logger = logging.getLogger("bayyinah.ingestion.queue")

class AcquisitionQueue:
    """
    Manages robust background acquisition jobs and Dead Letter Queue.
    """

    def create_job(
        self,
        db: Session,
        job_type: str,
        source_id: Optional[str] = None,
        entity_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        priority: str = "NORMAL"
    ) -> IngestionJobModel:
        """Creates a new queued job record in PostgreSQL."""
        job_id = str(uuid.uuid4())
        job = IngestionJobModel(
            id=job_id,
            source_id=source_id,
            job_type=job_type,
            status="QUEUED",
            documents_discovered=0,
            documents_processed=0,
            chunks_created=0,
            embeddings_created=0,
            error_count=0,
            metadata_json=json.dumps(metadata or {}),
            started_at=None,
            finished_at=None
        )
        # Set additional columns if present
        if hasattr(job, "entity_type"):
            job.entity_type = "DOCUMENT" if entity_id else "SOURCE"
        if hasattr(job, "entity_id") and entity_id:
            job.entity_id = entity_id
        if hasattr(job, "attempts"):
            job.attempts = 0

        db.add(job)
        db.commit()
        db.refresh(job)
        logger.info(f"Queued acquisition job: {job_id} ({job_type}) for source: {source_id}")
        return job

    def start_job(self, db: Session, job_id: str) -> Optional[IngestionJobModel]:
        """Transitions job to RUNNING state."""
        job = db.query(IngestionJobModel).filter(IngestionJobModel.id == job_id).first()
        if not job:
            return None
        job.status = "RUNNING"
        job.started_at = datetime.datetime.now(datetime.timezone.utc)
        db.commit()
        return job

    def finish_job(
        self,
        db: Session,
        job_id: str,
        stats: Optional[Dict[str, int]] = None
    ) -> Optional[IngestionJobModel]:
        """Transitions job to SUCCESS state."""
        job = db.query(IngestionJobModel).filter(IngestionJobModel.id == job_id).first()
        if not job:
            return None
        job.status = "SUCCESS"
        job.finished_at = datetime.datetime.now(datetime.timezone.utc)
        if stats:
            if "documents_discovered" in stats:
                job.documents_discovered = stats["documents_discovered"]
            if "documents_processed" in stats:
                job.documents_processed = stats["documents_processed"]
            if "chunks_created" in stats:
                job.chunks_created = stats["chunks_created"]
            if "embeddings_created" in stats:
                job.embeddings_created = stats["embeddings_created"]
        db.commit()
        logger.info(f"Acquisition job {job_id} succeeded.")
        return job

    def fail_job(
        self,
        db: Session,
        job_id: str,
        error_message: str,
        allow_retry: bool = True
    ) -> Optional[IngestionJobModel]:
        """
        Handles job failure with retry backoff and routes to Dead Letter Queue if exhausted.
        """
        job = db.query(IngestionJobModel).filter(IngestionJobModel.id == job_id).first()
        if not job:
            return None

        job.error_count = (job.error_count or 0) + 1
        max_retries = getattr(job, "max_retries", 3) or 3

        if allow_retry and job.error_count < max_retries:
            job.status = "RETRYING"
            logger.warning(f"Job {job_id} failed with: {error_message}. Will retry (Attempt {job.error_count}/{max_retries})")
        else:
            job.status = "DEAD_LETTER"
            job.finished_at = datetime.datetime.now(datetime.timezone.utc)
            if hasattr(job, "is_dead_letter"):
                job.is_dead_letter = True
            if hasattr(job, "dead_letter_reason"):
                job.dead_letter_reason = error_message

            # Log to human review queue
            try:
                review_item = KnowledgeReviewItemModel(
                    source_id=str(job.source_id) if job.source_id else None,
                    item_type="DEAD_LETTER",
                    severity="CRITICAL",
                    status="PENDING",
                    reason=f"Exhausted {max_retries} retries in job {job_id}: {error_message}",
                    details={"job_id": str(job.id), "job_type": job.job_type, "error": str(error_message)}
                )
                db.add(review_item)
            except Exception as e:
                logger.error(f"Failed to record Dead-Letter review item: {e}")

            logger.error(f"Job {job_id} permanently moved to DEAD_LETTER: {error_message}")

        db.commit()
        return job

acquisition_queue = AcquisitionQueue()
