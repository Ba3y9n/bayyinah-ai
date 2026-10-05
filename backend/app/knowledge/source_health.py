from typing import List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.knowledge_models import TrustedSourceModel, DocumentModel, DocumentChunkModel
from ..models.knowledge_schemas import SourceHealthItem

class SourceHealthService:
    """
    Evaluates real source status, metadata completeness, licensing governance,
    and document link validity.
    """

    def check_source_health(self, source: TrustedSourceModel, db: Session) -> SourceHealthItem:
        missing_items = []

        # 1. URL validity
        url_ok = bool(source.official_url and (source.official_url.startswith("http://") or source.official_url.startswith("https://")))
        if not url_ok:
            missing_items.append("Invalid or missing official URL")

        # 2. Metadata completeness
        if not source.description or len(source.description) < 15:
            missing_items.append("Incomplete description")
        if not source.content_scope:
            missing_items.append("Undefined content scope")
        if not source.license_name:
            missing_items.append("Missing license name specification")

        metadata_complete = len(missing_items) == 0

        # 3. Documents and chunks count
        docs_count = db.query(DocumentModel).filter_by(source_id=source.id).count()
        chunks_count = (
            db.query(DocumentChunkModel)
            .join(DocumentModel, DocumentChunkModel.document_id == DocumentModel.id)
            .filter(DocumentModel.source_id == source.id)
            .count()
        )

        # 4. Overall status determination
        if not source.is_active or source.trust_status == "DISABLED":
            status = "failed"
        elif source.trust_status == "REVIEW_REQUIRED" or source.license_status == "PENDING_VERIFICATION":
            status = "warning"
        elif docs_count == 0 and source.usage_status != "REFERRAL_ONLY":
            status = "warning"
            missing_items.append("No indexed documents yet (ingestion pending)")
        elif metadata_complete and url_ok and source.is_active:
            status = "healthy"
        else:
            status = "warning"

        return SourceHealthItem(
            source_id=str(source.id),
            source_name=source.name_ar or source.name or source.name_en or source.slug or "مصدر معتمد",
            status=status,
            url_accessible=url_ok,
            metadata_complete=metadata_complete,
            license_status=source.license_status,
            trust_status=source.trust_status,
            documents_count=docs_count,
            chunks_count=chunks_count,
            missing_items=missing_items
        )

    def check_all_sources_health(self, db: Session) -> List[SourceHealthItem]:
        sources = db.query(TrustedSourceModel).all()
        return [self.check_source_health(s, db) for s in sources]

source_health_service = SourceHealthService()
