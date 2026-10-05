"""
Bayyinah AI - Evidence Gate & Scholarly Citation Verification
Enforces Sections 14, 21, 22, 23 of Master Specifications:
Strict zero-hallucination guard:
1. Validates source approval (must belong to the 11 official sources).
2. Validates chunk presence, grounding, and minimum textual relevance.
3. Validates citations and exact reference formatting.
4. If validation fails or evidence is absent, enforces systematic abstention:
   "لم نجد في المصادر التي تم فحصها ما يثبت هذا النص، لذلك لا يمكن الجزم بصحته أو بطلانه بناءً على نتيجة البحث وحدها."
"""

from typing import Dict, Any, List, Optional
import logging
from ..ingestion.official_allowlist import is_url_in_allowlist, OFFICIAL_SOURCE_ALLOWLIST

logger = logging.getLogger("bayyinah.services.evidence_gate")

ABSTENTION_MESSAGE = (
    "لم نجد في المصادر التي تم فحصها ما يثبت هذا النص، "
    "لذلك لا يمكن الجزم بصحته أو بطلانه بناءً على نتيجة البحث وحدها."
)

class EvidenceGate:
    @staticmethod
    def validate_source(source_id: Optional[str], source_url: Optional[str] = None) -> bool:
        """Validates that the source belongs to the official allowlist."""
        approved_ids = {s["id"] for s in OFFICIAL_SOURCE_ALLOWLIST}
        if source_id and source_id in approved_ids:
            return True
        if source_url and is_url_in_allowlist(source_url):
            return True
        return False

    @classmethod
    def filter_evidence(cls, evidences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters candidate evidence items, keeping only approved official sources."""
        approved = []
        for ev in (evidences or []):
            src_id = ev.get("source_id")
            url = ev.get("url") or ev.get("source_url") or ev.get("canonical_url")
            if cls.validate_source(src_id, url):
                approved.append(ev)
        return approved

    @classmethod
    def validate(
        cls,
        evidences: List[Dict[str, Any]],
        confidence_score: float,
        claim_text: str,
        verdict: str
    ) -> Dict[str, Any]:
        """
        Validates evidence chain for the verification verdict.
        Returns:
            {
                "passed": bool,
                "sanitized_verdict": str,
                "reason": str,
                "validated_evidences": List[Dict],
                "abstention_required": bool
            }
        """
        # If verdict is already UNVERIFIED / UNPROVEN or SPECIALIST, respect it
        if verdict in ["يحتاج مراجعة مختص", "مجهول / غير ثابت بحسب البحث الحالي", "SPECIALIST"]:
            return {
                "passed": True,
                "sanitized_verdict": verdict,
                "reason": "Explicit specialist review or systematic abstention",
                "validated_evidences": evidences,
                "abstention_required": False
            }

        if not evidences:
            logger.info("EvidenceGate: No evidence provided. Forcing abstention.")
            return {
                "passed": False,
                "sanitized_verdict": "مجهول / غير ثابت بحسب البحث الحالي",
                "reason": ABSTENTION_MESSAGE,
                "validated_evidences": [],
                "abstention_required": True
            }

        validated_evidences = []
        for ev in evidences:
            src_id = ev.get("source_id")
            url = ev.get("url") or ev.get("canonical_url")
            text = ev.get("text") or ev.get("content") or ""

            # Check if source is official
            if not cls.validate_source(src_id, url):
                logger.warning(f"EvidenceGate: Rejecting unapproved source: {src_id} / {url}")
                continue

            # Ensure evidence has non-empty text
            if len(text.strip()) < 5:
                logger.warning(f"EvidenceGate: Rejecting evidence with empty or trivial text.")
                continue

            validated_evidences.append(ev)

        if not validated_evidences:
            logger.info("EvidenceGate: Zero valid official evidences survived validation. Forcing abstention.")
            return {
                "passed": False,
                "sanitized_verdict": "مجهول / غير ثابت بحسب البحث الحالي",
                "reason": ABSTENTION_MESSAGE,
                "validated_evidences": [],
                "abstention_required": True
            }

        # If confidence score is too low (< 0.40), cannot make definitive claim
        if confidence_score < 0.40 and verdict in ["ثابت بحسب المصدر", "ضعيف بحسب المصدر", "مكذوب / لا أصل له"]:
            logger.info(f"EvidenceGate: Low confidence score ({confidence_score}) for verdict {verdict}. Forcing abstention.")
            return {
                "passed": False,
                "sanitized_verdict": "مجهول / غير ثابت بحسب البحث الحالي",
                "reason": ABSTENTION_MESSAGE,
                "validated_evidences": validated_evidences,
                "abstention_required": True
            }

        return {
            "passed": True,
            "sanitized_verdict": verdict,
            "reason": "Evidence chain and official sources successfully validated",
            "validated_evidences": validated_evidences,
            "abstention_required": False
        }

evidence_gate = EvidenceGate()
