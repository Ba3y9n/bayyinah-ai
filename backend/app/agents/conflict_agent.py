from typing import List, Dict, Any
from ..models.schemas import EvidenceItem

class ConflictAgent:
    """
    AI JOB 8: Source Conflict Detector Agent
    Detects if verified sources present differing positions, scholarly interpretations, or hadith gradings.
    """
    def __init__(self):
        pass

    def detect_conflicts(self, claim_type: str, evidence_items: List[EvidenceItem]) -> Dict[str, Any]:
        from ..services.gemini_service import gemini_service
        if len(evidence_items) < 2:
            return {
                "conflict_detected": False,
                "conflicts_summary": None,
                "differing_sources": []
            }

        # Check for Fiqh disagreements or explicitly tagged conflicting opinions
        is_fiqh = claim_type in ["Fiqh", "فتوى/مسألة فقهية", "مسألة فقهية"]
        disagreement_keywords = ["اختلاف", "خلاف", "مذاهب", "القول الأول", "القول الثاني", "روايتان"]

        has_conflicting_terms = any(
            any(kw in ev.title or kw in ev.excerpt or kw in (ev.comparison_notes or "") for kw in disagreement_keywords)
            for ev in evidence_items
        )

        if is_fiqh and has_conflicting_terms:
            differing = []
            for ev in evidence_items[:3]:
                differing.append({
                    "source": ev.source_name,
                    "title": ev.title,
                    "reference": ev.reference,
                    "url": ev.url,
                    "excerpt_snippet": ev.excerpt[:140] + "..."
                })

            return {
                "conflict_detected": True,
                "conflicts_summary": "المسألة فيها اختلاف فقهي معتبر بين المذاهب؛ حيث استدل كل مذهب بنصوص معتبرة دون ترجيح شخصي من النظام.",
                "differing_sources": differing
            }

        return {
            "conflict_detected": False,
            "conflicts_summary": None,
            "differing_sources": []
        }

conflict_agent = ConflictAgent()
