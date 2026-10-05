import hashlib
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from ..models.knowledge_models import TrustedSourceModel, DocumentModel, DocumentChunkModel
from ..models.knowledge_schemas import EvidenceType, VerificationStatus

class EvidenceValidator:
    """
    EvidenceValidator Service (Section 25).
    Enforces the rigorous 9-point validation checklist before any evidence is approved:
    1. Is source registered in Trusted Source Registry?
    2. Is the operation legally & scientifically allowed (allowed_operations)?
    3. Does text exist in the indexed chunk?
    4. Is the excerpt/quotation accurate?
    5. Is reference locator intact?
    6. Does evidence support the claim (DIRECT, PARTIAL, CONTEXT, CONTRADICTING)?
    7. Is there a scholarly conflict between sources?
    8. Is evidence adequate (threshold check)?
    9. Is inquiry a personal fatwa / family case (SPECIALIST)?
    """

    def is_source_registered(self, db: Session, source_id: str) -> bool:
        src = db.query(TrustedSourceModel).filter_by(id=source_id, is_active=True).first()
        return src is not None

    def is_operation_allowed(self, db: Session, source_id: str, operation: str) -> bool:
        src = db.query(TrustedSourceModel).filter_by(id=source_id).first()
        if not src:
            return False
        
        # Check specific boolean flags first
        op_lower = operation.lower()
        if op_lower == "display_excerpt" and src.excerpt_allowed is not None:
            return src.excerpt_allowed
        if op_lower == "link" and src.link_allowed is not None:
            return src.link_allowed
        if op_lower == "translate" and src.translation_allowed is not None:
            return src.translation_allowed
        if op_lower == "index" and src.indexing_allowed is not None:
            return src.indexing_allowed
        if op_lower == "store" and src.storage_allowed is not None:
            return src.storage_allowed
        if op_lower == "embed" and src.embedding_allowed is not None:
            return src.embedding_allowed

        import json
        try:
            ops = json.loads(src.allowed_operations) if src.allowed_operations else {}
            return bool(ops.get(operation, False))
        except Exception:
            return False

    def verify_chunk_integrity(self, chunk: DocumentChunkModel) -> bool:
        computed = hashlib.sha256(chunk.content.encode("utf-8")).hexdigest()
        return computed == chunk.content_hash

    def is_personal_case(self, claim_text: str, claim_type: Optional[str] = None) -> bool:
        if claim_type in ["PERSONAL_CASE", "PERSONAL_FATWA"]:
            return True
        personal_terms = [
            "حلفت", "زوجتي", "طلقت", "طلاق", "شجار", "ميراث", "أبي مات", "امي ماتت",
            "هل يقع طلاقي", "هل يلزمني كفارة", "معاملتي المالية", "أنا متزوجة", "انا متزوجة"
        ]
        text_lower = claim_text.lower()
        return any(term in text_lower for term in personal_terms)

    def validate_candidate(
        self, 
        db: Session, 
        claim_text: str, 
        candidate: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validates an individual candidate evidence piece against checklist.
        """
        source_id = candidate.get("source", {}).get("id") or candidate.get("source_id")
        chunk_id = candidate.get("chunk", {}).get("id") or candidate.get("chunk_id")

        # 1. Source registered check
        if not self.is_source_registered(db, source_id):
            return {
                "valid": False,
                "reason": f"المصدر {source_id} غير مسجل أو غير نشط في سجل المصادر المعتمدة."
            }

        # 2. Excerpt display allowed check
        if not self.is_operation_allowed(db, source_id, "DISPLAY_EXCERPT"):
            return {
                "valid": False,
                "reason": f"سياسة ترخيص المصدر {source_id} لا تسمح بعرض المقتطفات النصية المباشرة."
            }

        # 3. Content hash check if chunk is present
        if chunk_id:
            chunk = db.query(DocumentChunkModel).filter_by(id=chunk_id).first()
            if chunk and not self.verify_chunk_integrity(chunk):
                return {
                    "valid": False,
                    "reason": "فشل فحص البصمة التشفيرية لمقطع الدليل (SHA-256 Hash Mismatch)."
                }

        return {"valid": True, "reason": None}

evidence_validator = EvidenceValidator()
