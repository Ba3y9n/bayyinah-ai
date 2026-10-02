from typing import List, Dict, Any
from ..models.schemas import EvidenceItem

class AbstentionAgent:
    """
    AI JOB 9: Abstention & Safety Guardrail Agent
    Enforces abstention when evidence is insufficient or when the inquiry requires specialist human referral.
    """
    def __init__(self):
        pass

    def evaluate_abstention(
        self, 
        claim_data: Dict[str, Any], 
        evidence_items: List[EvidenceItem]
    ) -> Dict[str, Any]:
        requires_specialist = claim_data.get("requires_specialist", False)
        claim_type = claim_data.get("claim_type", "")

        # 1. Personal Fatwa Guardrail
        if requires_specialist or claim_type == "PersonalCase":
            return {
                "must_abstain": True,
                "status": "SPECIALIST",
                "status_ar": "يحتاج مراجعة مختص",
                "reason": "المسألة شخصية أو نازلة تتطلب الاستفتاء المباشر وسماع التفاصيل من مفتٍ مختص أو المحكمة الشرعية.",
                "limitations": [
                    "لا يقدم الذكاء الاصطناعي فتاوى في مسائل الأيمان والطلاق والنزاعات الشخصية.",
                    "الواجب مراجعة دار الإفتاء الرسمية أو القضاء الشرعي."
                ]
            }

        # 2. Insufficient Evidence Guardrail
        if not evidence_items or (len(evidence_items) > 0 and evidence_items[0].relevance_score < 0.38):
            return {
                "must_abstain": True,
                "status": "INSUFFICIENT",
                "status_ar": "لم نجد دليلًا كافيًا",
                "reason": "لم نجد دليلًا كافيًا في المصادر التي تم فحصها داخل قاعدة بيّنة.",
                "limitations": [
                    "عدم العثور على دليل في المصادر المفحوصة لا يعني إثبات البطلان القطعي.",
                    "النظام يتوقف عن الحكم لعدم ثبوت السند في نطاق البحث المفحوص."
                ]
            }

        return {
            "must_abstain": False,
            "status": None,
            "status_ar": None,
            "reason": None,
            "limitations": [
                "هذه النتيجة مبنية على المصادر التي تم فحصها داخل بيّنة، ولا تعني مسح جميع كتب الأرض."
            ]
        }

abstention_agent = AbstentionAgent()
