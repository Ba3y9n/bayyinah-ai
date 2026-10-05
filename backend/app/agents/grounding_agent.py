from typing import List, Dict, Any, Optional
from ..models.schemas import EvidenceItem
from ..services.gemini_service import gemini_service

class GroundingAgent:
    """
    AI JOB 10: Grounded Response Generator Agent
    Synthesizes the final verified response strictly grounded in retrieved evidence.
    """
    def __init__(self):
        pass

    def generate(
        self,
        claim_data: Dict[str, Any],
        status: str,
        status_ar: str,
        reason: str,
        evidence_items: List[EvidenceItem],
        conflicts_data: Dict[str, Any],
        limitations: List[str]
    ) -> Dict[str, Any]:
        
        top_ev = evidence_items[0] if evidence_items else None

        # Check if Gemini 3.8 Flash grounded generation can be utilized
        if gemini_service.is_configured and gemini_service.client and status not in ["SPECIALIST", "CONFLICT"]:
            try:
                ev_list = [ev.model_dump() if hasattr(ev, "model_dump") else ev.dict() for ev in evidence_items]
                ai_res = gemini_service.generate_grounded_response(
                    claim_text=claim_data.get("main_claim", ""),
                    evidence_context=ev_list,
                    status=status
                )
                if ai_res and ai_res.get("summary"):
                    summary = ai_res["summary"]
                else:
                    summary = None
            except Exception:
                summary = None
        else:
            summary = None

        if not summary:
            if status == "VERIFIED":
                summary = (
                    f"تم التحقق من صحة النص ومطابقته بدقة مع {top_ev.source_name if top_ev else 'المصادر المعتمدة'} "
                    f"({top_ev.reference if top_ev else ''})، وتبين ثبوت نسبته وسلامة لفظه."
                )
            elif status == "WEAK":
                summary = (
                    f"نص الحديث متداول ولكنه مصنف كـ (ضعيف بحسب المصدر) في "
                    f"{top_ev.source_name if top_ev else 'كتب الحديث المعتمدة'}."
                )
            elif status == "FABRICATED":
                summary = (
                    f"النص غير صحيح ومصنف كـ (موضوع/مكذوب بحسب المصدر) في "
                    f"{top_ev.source_name if top_ev else 'المصادر الحديثية'}؛ ولا تصح نسبته للنبي ﷺ."
                )
            elif status == "NOT_ESTABLISHED":
                summary = (
                    "وجدت بيّنة نصًا قريبًا من الادعاء في المصادر المعتمدة، لكن الصياغة المتداولة تشتمل على خلط أو زيادة "
                    "تختلف عن النص الثابت في المصدر؛ لذلك لم تصنفه بيّنة على أنه ثابت بهذا اللفظ."
                )
            elif status == "CONFLICT":
                summary = (
                    "أظهرت المصادر المعتمدة وجود اختلاف فقهي معتبر في المسألة بين كبار أئمة المذاهب، "
                    "مع إسناد كل قول إلى دليله الشرعي ومصدره دون ترجيح شخصي من النظام."
                )
            elif status == "SPECIALIST":
                summary = (
                    "هذه المسألة تتعلق بأحوال شخصية أو وقائع فردية لا يبت فيها الذكاء الاصطناعي، "
                    "وتتطلب الاستفتاء المباشر من المفتين المخولين أو المحاكم الشرعية."
                )
            else: # INSUFFICIENT
                summary = (
                    "لم نجد في المصادر التي تم فحصها دليلًا مسندًا كافيًا لإثبات هذا الادعاء أو هذا اللفظ المتداول. "
                    "ونؤكد أن عدم العثور على دليل لا يعني إثبات البطلان القطعي."
                )

        return {
            "result_status": status,
            "result_status_ar": status_ar,
            "claim": claim_data.get("main_claim", ""),
            "summary": summary,
            "reason": reason,
            "evidence": [ev.model_dump() for ev in evidence_items],
            "conflicts": conflicts_data.get("differing_sources", []),
            "limitations": limitations,
            "specialist_note": (
                "يرجى مراجعة دار الإفتاء الرسمية أو المحكمة الشرعية المختصة." if status == "SPECIALIST" else None
            )
        }

grounding_agent = GroundingAgent()
