import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from ..models.knowledge_models import (
    TrustedSourceModel,
    DocumentModel,
    DocumentChunkModel,
    TermModel,
    TranslationTermModel,
    EvidenceModel,
    KnowledgeAuditLogModel
)
from ..models.knowledge_schemas import (
    TrustedSourceCreate,
    TrustedSourceResponse,
    TrustedSourceUpdate,
    KnowledgeBaseStats,
    SourceCategory,
    SourceType,
    TrustStatus,
    LicenseStatus
)

def _safe_source_type(stype: str) -> SourceType:
    if stype in [e.value for e in SourceType]:
        return SourceType(stype)
    mapping = {
        "PRIMARY_TEXT": SourceType.HADITH_DATABASE,
        "scholarly_corpus": SourceType.REFERENCE_WORK,
        "verified_fatwa_center": SourceType.OFFICIAL_PLATFORM,
        "encyclopedia": SourceType.ENCYCLOPEDIA,
        "primary_text": SourceType.HADITH_DATABASE
    }
    return mapping.get(stype, SourceType.OTHER)

def _safe_category(cat: str) -> SourceCategory:
    if cat in [e.value for e in SourceCategory]:
        return SourceCategory(cat)
    mapping = {
        "FATWA": SourceCategory.FIQH,
        "SEERAH": SourceCategory.SEERAH_HISTORY,
        "TAFSIR": SourceCategory.TAFSEER
    }
    return mapping.get(cat, SourceCategory.OTHER)

class SourceRegistryService:
    """
    Manages the formal registry of trusted sources, permission policies,
    review statuses, and licensing parameters.
    """

    def get_all_sources(self, db: Session, category: Optional[str] = "all") -> List[TrustedSourceResponse]:
        query = db.query(TrustedSourceModel)
        if category and category.lower() != "all":
            query = query.filter(TrustedSourceModel.category == category.upper())
        sources = query.order_by(TrustedSourceModel.name_ar).all()

        results = []
        for s in sources:
            docs_count = db.query(DocumentModel).filter_by(source_id=s.id).count()
            chunks_count = (
                db.query(DocumentChunkModel)
                .join(DocumentModel, DocumentChunkModel.document_id == DocumentModel.id)
                .filter(DocumentModel.source_id == s.id)
                .count()
            )
            ops = json.loads(s.allowed_operations) if isinstance(s.allowed_operations, str) else s.allowed_operations
            results.append(TrustedSourceResponse(
                id=str(s.id),
                name_ar=s.name_ar or s.name or s.name_en or s.slug or "مصدر معتمد",
                name_en=s.name_en,
                slug=s.slug,
                category=_safe_category(s.category),
                description=s.description,
                official_url=s.official_url,
                base_domain=s.base_domain,
                source_type=_safe_source_type(s.source_type),
                authority_level=s.authority_level,
                trust_status=TrustStatus(s.trust_status) if s.trust_status in [t.value for t in TrustStatus] else TrustStatus.APPROVED,
                usage_status=s.usage_status,
                license_status=LicenseStatus(s.license_status) if s.license_status in [l.value for l in LicenseStatus] else LicenseStatus.PENDING_VERIFICATION,
                license_name=s.license_name,
                license_url=s.license_url,
                copyright_holder=s.copyright_holder,
                allowed_operations=ops,
                content_scope=s.content_scope,
                language=s.language,
                publisher=s.publisher,
                author=s.author,
                country=s.country,
                verification_method=s.verification_method,
                verification_notes=s.verification_notes,
                last_verified_at=s.last_verified_at,
                verified_by=s.verified_by,
                is_active=s.is_active,
                documents_count=docs_count,
                chunks_count=chunks_count,
                created_at=s.created_at,
                updated_at=s.updated_at
            ))
        return results

    def get_source_by_id(self, db: Session, source_id: str) -> Optional[TrustedSourceResponse]:
        import uuid
        s = None
        try:
            uuid_val = str(uuid.UUID(str(source_id)))
            s = db.query(TrustedSourceModel).filter(TrustedSourceModel.id == uuid_val).first()
        except (ValueError, AttributeError):
            pass
        if not s:
            clean_slug = str(source_id).strip()
            s = db.query(TrustedSourceModel).filter(
                (TrustedSourceModel.slug == clean_slug) |
                (TrustedSourceModel.slug == clean_slug.replace("src-", "")) |
                (TrustedSourceModel.slug == f"sahih-{clean_slug.replace('src-', '')}")
            ).first()
        if not s:
            return None
        docs_count = db.query(DocumentModel).filter_by(source_id=s.id).count()
        chunks_count = (
            db.query(DocumentChunkModel)
            .join(DocumentModel, DocumentChunkModel.document_id == DocumentModel.id)
            .filter(DocumentModel.source_id == s.id)
            .count()
        )
        ops = json.loads(s.allowed_operations) if isinstance(s.allowed_operations, str) else s.allowed_operations
        return TrustedSourceResponse(
            id=str(s.id),
            name_ar=s.name_ar or s.name or s.name_en or s.slug or "مصدر معتمد",
            name_en=s.name_en,
            slug=s.slug,
            category=_safe_category(s.category),
            description=s.description,
            official_url=s.official_url,
            base_domain=s.base_domain,
            source_type=_safe_source_type(s.source_type),
            authority_level=s.authority_level,
            trust_status=TrustStatus(s.trust_status) if s.trust_status in [t.value for t in TrustStatus] else TrustStatus.APPROVED,
            usage_status=s.usage_status,
            license_status=LicenseStatus(s.license_status) if s.license_status in [l.value for l in LicenseStatus] else LicenseStatus.PENDING_VERIFICATION,
            license_name=s.license_name,
            license_url=s.license_url,
            copyright_holder=s.copyright_holder,
            allowed_operations=ops,
            content_scope=s.content_scope,
            language=s.language,
            publisher=s.publisher,
            author=s.author,
            country=s.country,
            verification_method=s.verification_method,
            verification_notes=s.verification_notes,
            last_verified_at=s.last_verified_at,
            verified_by=s.verified_by,
            is_active=s.is_active,
            documents_count=docs_count,
            chunks_count=chunks_count,
            created_at=s.created_at,
            updated_at=s.updated_at
        )

    def register_source(self, db: Session, data: TrustedSourceCreate) -> TrustedSourceResponse:
        ops_str = json.dumps(data.allowed_operations.model_dump(), ensure_ascii=False)
        src = TrustedSourceModel(
            id=data.id,
            name_ar=data.name_ar,
            name_en=data.name_en,
            slug=data.slug,
            category=data.category.value,
            description=data.description,
            official_url=data.official_url,
            base_domain=data.base_domain,
            source_type=data.source_type.value,
            authority_level=data.authority_level,
            trust_status=data.trust_status.value,
            usage_status=data.usage_status,
            license_status=data.license_status.value,
            license_name=data.license_name,
            license_url=data.license_url,
            copyright_holder=data.copyright_holder,
            allowed_operations=ops_str,
            content_scope=data.content_scope,
            language=data.language,
            publisher=data.publisher,
            author=data.author,
            country=data.country,
            verification_method=data.verification_method,
            verification_notes=data.verification_notes,
            verified_by=data.verified_by,
            is_active=data.is_active
        )
        db.add(src)
        db.commit()
        db.refresh(src)
        return self.get_source_by_id(db, src.id) # type: ignore

    def update_source(self, db: Session, source_id: str, data: TrustedSourceUpdate) -> Optional[TrustedSourceResponse]:
        src = db.query(TrustedSourceModel).filter_by(id=source_id).first()
        if not src:
            return None
        if data.trust_status:
            src.trust_status = data.trust_status.value
        if data.license_status:
            src.license_status = data.license_status.value
        if data.is_active is not None:
            src.is_active = data.is_active
        if data.verification_notes:
            src.verification_notes = data.verification_notes
        if data.allowed_operations is not None:
            src.allowed_operations = json.dumps(data.allowed_operations, ensure_ascii=False)
        src.updated_at = datetime.utcnow()
        db.commit()
        return self.get_source_by_id(db, source_id)

    def verify_source(self, db: Session, source_id: str, verifier_name: str, notes: Optional[str] = None) -> Optional[TrustedSourceResponse]:
        src = db.query(TrustedSourceModel).filter_by(id=source_id).first()
        if not src:
            return None
        src.trust_status = TrustStatus.APPROVED.value
        src.last_verified_at = datetime.utcnow()
        src.verified_by = verifier_name
        if notes:
            src.verification_notes = notes
        src.updated_at = datetime.utcnow()
        db.commit()
        return self.get_source_by_id(db, source_id)

    def get_stats(self, db: Session) -> KnowledgeBaseStats:
        total_sources = db.query(TrustedSourceModel).count()
        active_sources = db.query(TrustedSourceModel).filter_by(is_active=True).count()
        
        # Sources by category
        sources = db.query(TrustedSourceModel).all()
        by_category = {}
        by_trust = {}
        by_license = {}
        needing_review = 0
        last_verified = None

        for s in sources:
            by_category[s.category] = by_category.get(s.category, 0) + 1
            by_trust[s.trust_status] = by_trust.get(s.trust_status, 0) + 1
            by_license[s.license_status] = by_license.get(s.license_status, 0) + 1
            if s.trust_status == "REVIEW_REQUIRED" or s.license_status == "PENDING_VERIFICATION":
                needing_review += 1
            if s.last_verified_at:
                if not last_verified or s.last_verified_at > last_verified:
                    last_verified = s.last_verified_at

        total_documents = db.query(DocumentModel).count()
        total_chunks = db.query(DocumentChunkModel).count()
        total_terms = db.query(TranslationTermModel).count() or db.query(TermModel).count()
        total_evidence = db.query(EvidenceModel).count()
        total_verifications = db.query(KnowledgeAuditLogModel).count()
        total_insufficient = db.query(KnowledgeAuditLogModel).filter(
            KnowledgeAuditLogModel.final_status.in_(["INSUFFICIENT", "NOT_ESTABLISHED"])
        ).count()
        total_conflicts = db.query(KnowledgeAuditLogModel).filter(
            KnowledgeAuditLogModel.final_status == "CONFLICT"
        ).count()

        return KnowledgeBaseStats(
            total_sources=total_sources,
            active_sources=active_sources,
            sources_by_category=by_category,
            sources_by_trust=by_trust,
            sources_by_license=by_license,
            total_documents=total_documents,
            total_chunks=total_chunks,
            total_terms=total_terms,
            total_evidence=total_evidence,
            total_verifications=total_verifications,
            total_insufficient=total_insufficient,
            total_conflicts=total_conflicts,
            evidence_count=total_evidence,
            verifications_count=total_verifications,
            insufficient_count=total_insufficient,
            conflict_count=total_conflicts,
            sources_needing_review=needing_review,
            last_verified=last_verified.isoformat() if last_verified else None
        )

source_registry_service = SourceRegistryService()
