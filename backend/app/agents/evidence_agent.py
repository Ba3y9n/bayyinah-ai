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

        top_ev = evidence_items[0]
        evidence_found = True
        source_verified = bool(top_ev.source_id and top_ev.source_name)
        reference_verified = bool(top_ev.reference and len(top_ev.reference) > 5)
        
        # Check claim support threshold
        claim_supported = top_ev.relevance_score >= 0.50
        attribution_verified = top_ev.relevance_score >= 0.65

        sufficient_evidence = top_ev.relevance_score >= 0.38 and len(evidence_items) > 0

        return {
            "evidence_found": evidence_found,
            "source_verified": source_verified,
            "claim_supported": claim_supported,
            "attribution_verified": attribution_verified,
            "reference_verified": reference_verified,
            "sufficient_evidence": sufficient_evidence,
            "reason": top_ev.comparison_notes or "تم التحقق من مطابقة النص مع المصدر المعتمد."
        }

evidence_agent = EvidenceAgent()
