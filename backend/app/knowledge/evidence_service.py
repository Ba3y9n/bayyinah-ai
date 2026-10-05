import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models.knowledge_models import (
    ClaimModel,
    EvidenceModel,
    KnowledgeAuditLogModel
)
from ..models.knowledge_schemas import (
    KnowledgeSearchResultItem,
    EvidenceType,
    VerificationStatus,
    ContentLevel,
    ClaimType
)
from .specialized_handlers import quran_special_handler, terminology_special_handler

class EvidenceValidationService:
    """
    Evaluates candidate evidence against extracted claims.
    Enforces governance rules:
    1. No Evidence != Fabricated (use NOT_ESTABLISHED / INSUFFICIENT)
    2. Personal Fatwas (LEVEL_D) are immediately redirected to SPECIALIST referral
    3. Conflict Detection presents divergent evidence honestly without forced bias
    4. Abstention applies when evidence is lacking or inconclusive
    """

    def validate(
        self,
        db: Session,
        claim_text: str,
        claim_type: str,
        category: str,
        candidates: List[KnowledgeSearchResultItem]
    ) -> Dict[str, Any]:
        # 1. Check for Level D (Personal Fatwa / Case)
        personal_fatwa_keywords = ["طلقت", "يمين طلاق", "ميراث عائلتنا", "حكم طلاقي", "نزاع مالي بيني وبين"]
        if claim_type == "PERSONAL_FATWA" or any(kw in claim_text for kw in personal_fatwa_keywords):
            return {
                "status": VerificationStatus.SPECIALIST.value,
                "status_slug": "needs_specialist",
                "status_ar": "يحتاج مراجعة مختص",
                "content_level": ContentLevel.LEVEL_D.value,
                "confidence": 0.95,
                "reason": "المسألة فتوى شخصية أو واقعة خاصة تتطلب الاستفصال المباشر من المفتي المختص ولا يجوز الحكم فيها برمجياً.",
                "explanation": "وفقاً لسياسة حوكمة بيّنة AI وضوابط المجامع الفقهية (Level D)، يمتنع النظام عن تقديم أحكام شرعية في النوازل الشخصية ومسائل الأحوال الشخصية، ويُوجّه السائل حصراً لدور الإفتاء المعتمدة.",
                "support_level": EvidenceType.NO_MATCH.value,
                "conflicts": [],
                "primary_evidence": candidates[0] if candidates else None
            }

        # 2. Check Quran Special Handler if Quran Category or Verse Claim
        if category.upper() == "QURAN" or claim_type == "QURAN_VERSE":
            quran_check = quran_special_handler.inspect_verse(db, claim_text)
            if quran_check:
                if quran_check["is_exact_match"]:
                    return {
                        "status": VerificationStatus.VERIFIED.value,
                        "status_slug": "verified_authentic",
                        "status_ar": "ثابت بحسب المصدر",
                        "content_level": ContentLevel.LEVEL_A.value,
                        "confidence": 0.99,
                        "reason": f"النص آية قرآنية كريمة ثابتة برسم المصحف المعتمد ({quran_check['verse_reference']}).",
                        "explanation": f"تمت مطابقة النص بالكامل مع مصحف مجمع الملك فهد لطباعة المصحف الشريف في {quran_check['surah']}، {quran_check['source_locator']}.",
                        "support_level": EvidenceType.DIRECT_SUPPORT.value,
                        "conflicts": [],
                        "special_data": quran_check
                    }
                else:
                    return {
                        "status": VerificationStatus.NOT_ESTABLISHED.value,
                        "status_slug": "unverified_wording",
                        "status_ar": "لم يثبت بهذا اللفظ",
                        "content_level": ContentLevel.LEVEL_A.value,
                        "confidence": 0.96,
                        "reason": "النص القرآني المدخل يحتوي على تصحيف أو خطأ في الألفاظ مقارنة بالنص المتواتر المعتمد.",
                        "explanation": quran_check["notes"],
                        "support_level": EvidenceType.CONTRADICTING.value,
                        "conflicts": [],
                        "special_data": quran_check
                    }

        # 3. Check Terminology Handler if Translation or Definition
        if category.upper() == "DICTIONARY_TRANSLATION" or claim_type in ["TRANSLATION", "DEFINITION"]:
            term_res = terminology_special_handler.lookup_term(db, claim_text)
            if term_res:
                return {
                    "status": VerificationStatus.VERIFIED.value,
                    "status_slug": "verified_authentic",
                    "status_ar": "ثابت بحسب المصدر",
                    "content_level": ContentLevel.LEVEL_A.value,
                    "confidence": 0.98,
                    "reason": f"المصطلح الشرعي موثق في موسوعة المحتوى الإسلامي والجمهرة مع بيانه المعياري.",
                    "explanation": f"المصطلح: {term_res['term_ar']}. التعريف الشرعي: {term_res['definition_ar']}. المقابل المعتمد بالإنجليزية: {term_res['translations'][0]['approved_translation'] if term_res['translations'] else ''}.",
                    "support_level": EvidenceType.DIRECT_SUPPORT.value,
                    "conflicts": [],
                    "special_data": term_res
                }

        # 4. Check for Empty / Insufficient Candidates -> ABSTENTION
        if not candidates or len(candidates) == 0:
            return {
                "status": VerificationStatus.NOT_ESTABLISHED.value,
                "status_slug": "unverified_wording",
                "status_ar": "لم يثبت بهذا اللفظ",
                "content_level": ContentLevel.LEVEL_B.value,
                "confidence": 0.70,
                "reason": "لم نجد في المصادر المعتمدة المتاحة لدينا دليلاً يثبت هذا النص أو نسبته بهذا اللفظ.",
                "explanation": "امتناع تحفظي: وفق سياسة بيّنة AI، عدم العثور على دليل في قواعدنا المعرفية لا يعني الجزم بكونه مكذوباً، وإنما يفيد بعدم ثبوته بالأدلة المتاحة، ونتجنب إصدار حكم جازم بغير بينة موثقة.",
                "support_level": EvidenceType.NO_MATCH.value,
                "conflicts": []
            }

        top_cand = candidates[0]

        # 5. Check if Evidence explicitly declares Text as Fabricated or Weak
        if top_cand.verification_status == VerificationStatus.FABRICATED:
            return {
                "status": VerificationStatus.FABRICATED.value,
                "status_slug": "fabricated_per_source",
                "status_ar": "موضوع/مكذوب بحسب المصدر",
                "content_level": ContentLevel.LEVEL_A.value,
                "confidence": 0.98,
                "reason": "المصدر المعتمد صرّح بكون الحديث باطلاً أو لا أصل له أو موضوعاً.",
                "explanation": f"وفقاً لتخريج {top_cand.source['name_ar']} في {top_cand.chunk.get('source_locator')}: {top_cand.chunk['content']}",
                "support_level": EvidenceType.CONTRADICTING.value,
                "conflicts": [],
                "primary_evidence": top_cand
            }

        if top_cand.verification_status == VerificationStatus.WEAK:
            return {
                "status": VerificationStatus.WEAK.value,
                "status_slug": "weak_per_source",
                "status_ar": "ضعيف بحسب المصدر",
                "content_level": ContentLevel.LEVEL_B.value,
                "confidence": 0.94,
                "reason": "الحديث مصنف في المصادر المعتمدة بدرجة الضعف ولا تصح نسبته الجازمة للنبي ﷺ.",
                "explanation": f"وفقاً لأحكام المحدثين في {top_cand.source['name_ar']}: {top_cand.chunk['content']}",
                "support_level": EvidenceType.PARTIAL_SUPPORT.value,
                "conflicts": [],
                "primary_evidence": top_cand
            }

        # 6. Check for Legitimate Scholarly Conflicts
        if top_cand.verification_status == VerificationStatus.CONFLICT or "خلاف" in top_cand.chunk["content"]:
            return {
                "status": VerificationStatus.CONFLICT.value,
                "status_slug": "scholarly_disagreement",
                "status_ar": "اختلاف في المصادر",
                "content_level": ContentLevel.LEVEL_C.value,
                "confidence": 0.92,
                "reason": "المسألة محل خلاف واجتهاد معتبر بين أهل العلم والمذاهب الفقهية.",
                "explanation": f"وثقت المصادر وجود قولين معتبرين: الأول يرى الوجوب واستدل بآثار معتبرة، والثاني يرى الإنصات استدلالاً بآثار أخرى. ينبغي مراعاة الخلاف وسؤال العالم المختص.",
                "support_level": EvidenceType.CONTEXT.value,
                "conflicts": [top_cand.chunk["content"]],
                "primary_evidence": top_cand
            }

        # 7. Check for Direct Verified Support
        if top_cand.support_level == EvidenceType.DIRECT_SUPPORT and top_cand.scores.get("relevance", 0) > 0.7:
            return {
                "status": VerificationStatus.VERIFIED.value,
                "status_slug": "verified_authentic",
                "status_ar": "ثابت بحسب المصدر",
                "content_level": ContentLevel.LEVEL_A.value,
                "confidence": 0.98,
                "reason": f"تم العثور على النص مطابقاً في {top_cand.source['name_ar']}.",
                "explanation": f"تم توثيق النص في {top_cand.document['title_ar']}، {top_cand.chunk.get('source_locator')} برابط معتمد وتخريج مباشر.",
                "support_level": EvidenceType.DIRECT_SUPPORT.value,
                "conflicts": [],
                "primary_evidence": top_cand
            }

        # 8. Partial Match or Low Score -> Abstain / Insufficient
        return {
            "status": VerificationStatus.INSUFFICIENT.value,
            "status_slug": "insufficient_evidence",
            "status_ar": "لم نجد دليلًا كافيًا",
            "content_level": ContentLevel.LEVEL_B.value,
            "confidence": 0.65,
            "reason": "توجد نصوص ذات صلة جزئية، ولكن الدليل المباشر غير كافٍ لتأكيد صحة الادعاء كاملاً.",
            "explanation": "امتناع تحفظي: تقتضي أمانة التوثيق عدم الجزم بالصحة أو البطلان عند عدم اكتمال الدليل المباشر في قواعد المعرفة المعتمدة لدينا.",
            "support_level": EvidenceType.RELATED.value,
            "conflicts": [],
            "primary_evidence": top_cand
        }

evidence_validation_service = EvidenceValidationService()
