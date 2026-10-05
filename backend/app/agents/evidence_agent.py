from typing import List, Dict, Any
from ..models.schemas import EvidenceItem

class EvidenceAgent:
    """
    AI JOB 6 & 7: Evidence Ranking & Validation Agent
    Validates evidence existence, source trustworthiness, text-to-claim alignment, and sufficiency.
    """
    def __init__(self):
        pass

    def validate(self, claim_text: str, evidence_items: List[EvidenceItem]) -> Dict[str, Any]:
        from ..services.gemini_service import gemini_service
        if not evidence_items:
            return {
                "evidence_found": False,
                "source_verified": False,
                "claim_supported": False,
                "attribution_verified": False,
                "reference_verified": False,
                "conflict_detected": False,
                "sufficient_evidence": False,
                "reason": "لم يتم العثور على أي دليل مرتبط في المصادر المفحوصة."
            }

        excerpts = [ev.excerpt for ev in evidence_items]
        res = gemini_service.validate_evidence_structured(claim_text, excerpts)
        top_ev = evidence_items[0]

        return {
            "evidence_found": res.evidence_found,
            "source_verified": bool(top_ev.source_id and top_ev.source_name),
            "claim_supported": top_ev.relevance_score >= 0.50,
            "attribution_verified": top_ev.relevance_score >= 0.65,
            "reference_verified": bool(top_ev.reference and len(top_ev.reference) > 5),
            "sufficient_evidence": top_ev.relevance_score >= 0.38 and len(evidence_items) > 0,
            "reason": top_ev.comparison_notes or res.reason
        }

evidence_agent = EvidenceAgent()
