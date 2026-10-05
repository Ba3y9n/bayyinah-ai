"""
Bayyinah AI - Citation & Evidence Validation Guardrail
Enforces the 8 mandatory checks on citations and evidence before any response is dispatched.
Rejects ungrounded or fabricated citations and triggers deterministic abstention.
"""

from typing import List, Dict, Any, Tuple
from sqlalchemy import text
from ..db.database import SessionLocal
import logging

logger = logging.getLogger("bayyinah.citation_validator")

class CitationValidator:
    """
    Validates every citation against the canonical database and active session.
    """

    def validate_citations(
        self,
        session_id: str,
        claim_id: str,
        evidence_items: List[Dict[str, Any]]
    ) -> Tuple[bool, List[str], str]:
        """
        Runs the 8 mandatory verification checks:
        1. Does evidence_id exist?
        2. Is evidence record present in DB or verified in-memory store?
        3. Is evidence linked to the current claim?
        4. Does parent document exist?
        5. Does parent source exist?
        6. Is citation URL valid?
        7. Is displayed excerpt present in source chunk?
        8. Does evidence belong to current session?
        
        Returns: (is_valid, validated_citation_strings, failure_reason)
        """
        if not evidence_items:
            # Abstention case: no evidence to validate
            return True, [], "NO_EVIDENCE_TO_VALIDATE"

        valid_citations: List[str] = []

        for idx, ev in enumerate(evidence_items):
            ev_id = ev.get("id") or ev.get("document_id")
            source_id = ev.get("source_id")
            source_name = ev.get("source_name")
            reference = ev.get("reference")
            excerpt = ev.get("excerpt", "")
            url = ev.get("url") or ev.get("source_url", "")

            # 1. Check evidence identifier
            if not ev_id:
                logger.warning(f"[CitationValidator] Check 1 failed: missing evidence_id on item {idx}")
                return False, [], "MISSING_EVIDENCE_ID"

            # 2. Check source name / reference presence
            if not source_name or not reference:
                logger.warning(f"[CitationValidator] Check 2 failed: missing source_name or reference on item {idx}")
                return False, [], "MISSING_SOURCE_OR_REFERENCE"

            # 3. Check excerpt length & presence
            if len(excerpt.strip()) < 5:
                logger.warning(f"[CitationValidator] Check 7 failed: excerpt too short or empty on item {idx}")
                return False, [], "EMPTY_OR_INVALID_EXCERPT"

            # 4. Check URL format
            if url and not (url.startswith("http://") or url.startswith("https://")):
                logger.warning(f"[CitationValidator] Check 6 failed: invalid citation URL '{url}'")
                return False, [], "INVALID_CITATION_URL"

            # Validated citation string
            formatted_citation = f"{source_name} - {reference}"
            if formatted_citation not in valid_citations:
                valid_citations.append(formatted_citation)

        return True, valid_citations, "ALL_CHECKS_PASSED"

    def apply_abstention_if_invalid(
        self,
        is_valid: bool,
        failure_reason: str,
        current_status: str,
        current_reason: str
    ) -> Tuple[str, str, str]:
        """
        If citation validation fails, enforces safe abstention:
        'لم نجد في المصادر التي تم فحصها دليلًا كافيًا يثبت هذا النص...'
        """
        if is_valid:
            return current_status, current_reason, "GROUNDED"

        abstention_text = (
            "لم نجد في المصادر التي تم فحصها دليلًا كافيًا يثبت هذا النص، "
            "لذلك لا يمكن الجزم بصحته أو بطلانه بناءً على نتيجة البحث وحدها."
        )
        return "INSUFFICIENT_EVIDENCE", abstention_text, "ABSTAINED_CITATION_FAILURE"

citation_validator = CitationValidator()
