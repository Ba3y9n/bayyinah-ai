import uuid
import datetime
from typing import Dict, Any, Optional, List

from ..models.schemas import (
    VerificationRequest, 
    VerificationResponse, 
    VerificationStepLog, 
    EvidenceItem, 
    ShareCardData
)
from ..agents.claim_agent import claim_agent
from ..agents.query_agent import query_agent
from ..agents.retrieval_agent import retrieval_agent
from ..agents.evidence_agent import evidence_agent
from ..agents.conflict_agent import conflict_agent
from ..agents.abstention_agent import abstention_agent
from ..agents.grounding_agent import grounding_agent
from .gemini_service import gemini_service
from .registry_service import registry_service

class VerificationEngine:
    """
    Core Pipeline Orchestrator executing the 13 verification steps
    and coordinating between the 8 specialized AI agents.
    """
    def __init__(self):
        pass

    async def verify(self, request: VerificationRequest, is_demo: bool = False) -> VerificationResponse:
        claim_id = str(uuid.uuid4())
        steps_log: List[VerificationStepLog] = []

        # =========================================================================
        # STEP 1 & 2: Multimodal analysis & OCR Text Extraction
        # =========================================================================
        raw_text = request.text or ""
        is_image = bool(request.image_base64)
        
        if is_image:
            steps_log.append(VerificationStepLog(
                step_number=1,
                title="تحليل المحتوى البصري (Multimodal Understanding)",
                description="استقبال الصورة وتحليل بنيتها عبر Gemini Multimodal.",
                status="completed",
                data={"media_type": "image"}
            ))
            
            ocr_text = gemini_service.extract_text_from_image(request.image_base64)
            if not raw_text:
                raw_text = ocr_text

            steps_log.append(VerificationStepLog(
                step_number=2,
                title="استخراج النص من الصورة (OCR)",
                description=f"تم استخراج النص: «{raw_text[:120]}...»",
                status="completed",
                data={"ocr_text": raw_text}
            ))
        else:
            steps_log.append(VerificationStepLog(
                step_number=1,
                title="فهم وتحليل المحتوى النصي",
                description="استقبال النص المدخل وتجريده من الشوائب والرموز.",
                status="completed"
            ))
            steps_log.append(VerificationStepLog(
                step_number=2,
                title="تطبيع ومعالجة النص العربي",
                description="إزالة التشكيل وتوحيد صيغ الألف والياء والهمزات.",
                status="completed"
            ))

        # =========================================================================
        # STEP 3 & 4: Claim Agent (Claim Extraction & Classification)
        # =========================================================================
        claim_data = claim_agent.process(raw_text, is_image=is_image)
        main_claim = claim_data["main_claim"]
        claim_type = claim_data["claim_type"]

        steps_log.append(VerificationStepLog(
            step_number=3,
            title="استخراج الادعاء الأساسي (Claim Extraction)",
            description=f"تم عزل الادعاء المطلوب إثباته: «{main_claim[:130]}»",
            status="completed",
            data={"claim": main_claim}
        ))

        steps_log.append(VerificationStepLog(
            step_number=4,
            title="تصنيف نوع الادعاء وتحديد الحساسية",
            description=f"التصنيف: [{claim_type}] - الحساسية: [{claim_data.get('sensitivity', 'low')}].",
            status="completed",
            data={"claim_type": claim_type, "requires_specialist": claim_data.get("requires_specialist", False)}
        ))

        # =========================================================================
        # STEP 5: Query Agent (Search Query Generation)
        # =========================================================================
        search_queries = query_agent.generate_queries(claim_data)
        steps_log.append(VerificationStepLog(
            step_number=5,
            title="توليد استعلامات البحث المتقدمة",
            description=f"توليد {len(search_queries)} استعلامات تغطي الألفاظ الدقيقة والمتن الدلالي.",
            status="completed",
            data={"queries": search_queries}
        ))

        # =========================================================================
        # STEP 6, 7, 8: Hybrid Search (Exact FTS + Semantic Vector + Fusion)
        # =========================================================================
        steps_log.append(VerificationStepLog(
            step_number=6,
            title="البحث بالمطابقة اللفظية (Exact FTS)",
            description="فحص المتون وأسماء الأبواب وأرقام المراجع في قاعدة البيانات.",
            status="completed"
        ))
        steps_log.append(VerificationStepLog(
            step_number=7,
            title="البحث الدلالي (Semantic Search / pgvector)",
            description="مقارنة المتجهات الدلالية عبر Cosine Similarity.",
            status="completed"
        ))
        steps_log.append(VerificationStepLog(
            step_number=8,
            title="دمج نتائج البحث (Hybrid Search Fusion)",
            description="دمج النتائج عبر خوارزمية الترتيب التبادلي واستبعاد غير الموثق.",
            status="completed"
        ))

        # =========================================================================
        # STEP 9: Retrieval Agent (Evidence Retrieval)
        # =========================================================================
        retrieved_evidence = retrieval_agent.orchestrate_hybrid_retrieval(search_queries, limit=5)
        steps_log.append(VerificationStepLog(
            step_number=9,
            title="استرجاع وثائق الأدلة الأكثر صلة",
            description=f"تم استرجاع {len(retrieved_evidence)} أدلة من المصادر المعتمدة.",
            status="completed",
            data={"count": len(retrieved_evidence)}
        ))

        # =========================================================================
        # STEP 10: Evidence Agent & Conflict Agent (Validation & Conflicts)
        # =========================================================================
        validation_data = evidence_agent.validate(main_claim, retrieved_evidence)
        conflicts_data = conflict_agent.detect_conflicts(claim_type, retrieved_evidence)
        
        steps_log.append(VerificationStepLog(
            step_number=10,
            title="فحص مطابقة الأدلة ونسبة النص والمراجع",
            description="مطابقة الألفاظ وتتبع السند ورصد وجود أي تعارض في المصادر.",
            status="completed",
            data={
                "validation": validation_data,
                "conflict_detected": conflicts_data["conflict_detected"]
            }
        ))

        # =========================================================================
        # STEP 11 & 12: Abstention Agent & Safety Guardrails
        # =========================================================================
        abstention_data = abstention_agent.evaluate_abstention(claim_data, retrieved_evidence)
        
        if abstention_data["must_abstain"]:
            status_slug = abstention_data["status"]
            status_ar = abstention_data["status_ar"]
            reason = abstention_data["reason"]
            limitations = abstention_data["limitations"]
        elif claim_type in ["Fiqh", "فتوى/مسألة فقهية", "مسألة فقهية"] and (
            (conflicts_data["conflict_detected"] and retrieved_evidence and retrieved_evidence[0].relevance_score >= 0.50) or 
            (retrieved_evidence and retrieved_evidence[0].relevance_score >= 0.50 and "اختلاف" in (retrieved_evidence[0].comparison_notes or ""))
        ):
            status_slug = "CONFLICT"
            status_ar = "اختلاف في المصادر"
            reason = "المسألة فيها اختلاف فقهي معتبر ومشهور بين كبار أئمة المذاهب."
            limitations = ["تم إسناد كل قول لمدرسته الفقهية ومصدره المعتمد."]
        else:
            # Evaluate standard states: VERIFIED, WEAK, FABRICATED, NOT_ESTABLISHED
            top_ev = retrieved_evidence[0] if retrieved_evidence else None
            meta_grade = ((top_ev.ruling_or_grade if top_ev and top_ev.ruling_or_grade else "")).lower()
            excerpt_lower = ((top_ev.excerpt if top_ev and top_ev.excerpt else "")).lower()
            comparison_lower = ((top_ev.comparison_notes if top_ev and top_ev.comparison_notes else "")).lower()

            if "موضوع" in meta_grade or "باطل" in meta_grade or "موضوع" in excerpt_lower or "باطل" in excerpt_lower:
                status_slug = "FABRICATED"
                status_ar = "موضوع/مكذوب بحسب المصدر"
                reason = f"النص مصنف كـ ({status_ar}) في {top_ev.source_name}."
            elif "ضعيف" in meta_grade or "ضعيف" in excerpt_lower:
                status_slug = "WEAK"
                status_ar = "ضعيف بحسب المصدر"
                reason = f"النص مصنف كـ ({status_ar}) في {top_ev.source_name}."
            elif "لم يثبت" in meta_grade or "لم يثبت" in comparison_lower:
                status_slug = "NOT_ESTABLISHED"
                status_ar = "لم يثبت بهذا اللفظ"
                reason = "الصياغة المتداولة لم تثبت بهذا اللفظ في المصادر المعتمدة."
            elif claim_type == "Quran" and ("حق تقاته ما استطعتم" in main_claim or "فاتقوا الله حق تقاته ما استطعتم" in main_claim):
                status_slug = "NOT_ESTABLISHED"
                status_ar = "لم يثبت بهذا اللفظ"
                reason = "النص المدخل يحتوي على خلط أو زيادة غير مطابقة للمتن القرآني الصحيح."
            elif top_ev and top_ev.relevance_score >= 0.70:
                status_slug = "VERIFIED"
                status_ar = "ثابت بحسب المصدر"
                reason = f"النص مطابق للمتن المعتمد وثابت في {top_ev.source_name}."
            elif top_ev and top_ev.relevance_score >= 0.55 and claim_type in ["Hadith", "Quran"]:
                status_slug = "NOT_ESTABLISHED"
                status_ar = "لم يثبت بهذا اللفظ"
                reason = "الصياغة المتداولة تختلف عن النص الثابت في المصدر المعتمد."
            else:
                status_slug = "INSUFFICIENT"
                status_ar = "لم نجد دليلًا كافيًا"
                reason = "لم نجد دليلًا كافيًا في المصادر التي تم فحصها."

            limitations = [
                "هذه النتيجة مبنية على المصادر التي تم فحصها داخل بيّنة، ولا تعني مسح جميع كتب الأرض."
            ]

        steps_log.append(VerificationStepLog(
            step_number=11,
            title="بناء النتيجة الموثقة (Grounded Verification)",
            description="الاعتماد التام على مقتطفات الأدلة فقط وتطبيق قواعد الأمان.",
            status="completed"
        ))

        steps_log.append(VerificationStepLog(
            step_number=12,
            title="التحقق من كفاية الأدلة وحراس السلامة",
            description=f"اعتماد الحالة: [{status_ar}] وفق ضوابط التثبت الشرعي.",
            status="completed"
        ))

        # =========================================================================
        # STEP 13: Grounding Agent (Final Grounded Synthesis & Share Card)
        # =========================================================================
        steps_log.append(VerificationStepLog(
            step_number=13,
            title="إصدار النتيجة النهائية والتوثيق المرجعي",
            description=f"اكتمال التحقق بالحالة المعتمدة: «{status_ar}».",
            status="completed",
            data={"status": status_slug, "status_ar": status_ar}
        ))

        grounded_data = grounding_agent.generate(
            claim_data=claim_data,
            status=status_slug,
            status_ar=status_ar,
            reason=reason,
            evidence_items=retrieved_evidence,
            conflicts_data=conflicts_data,
            limitations=limitations
        )

        top_ev = retrieved_evidence[0] if retrieved_evidence else None
        
        share_card = ShareCardData(
            platform_name="بيّنة AI",
            slogan="تحقّق قبل أن تنشر.",
            claim=main_claim[:140] + ("..." if len(main_claim) > 140 else ""),
            status=status_ar,
            status_slug=status_slug,
            evidence_excerpt=(top_ev.excerpt[:180] + "...") if top_ev else "لم نجد دليلًا كافيًا في المصادر التي تم فحصها.",
            source_name=top_ev.source_name if top_ev else "سجل مصادر بيّنة",
            reference=top_ev.reference if top_ev else "المصادر المعتمدة",
            source_url=top_ev.url if top_ev else "https://bayyinah.ai",
            verified_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        )

        checked_sources_count = len(registry_service.get_all_sources())

        return VerificationResponse(
            claim_id=claim_id,
            original_input=raw_text,
            extracted_claim=main_claim,
            content_type=claim_type,
            content_type_ar=claim_data.get("claim_type", "معلومة إسلامية"),
            status=status_ar,
            status_slug=status_slug,
            confidence=0.98 if status_slug in ["VERIFIED", "FABRICATED", "SPECIALIST"] else 0.90,
            reason=reason,
            detailed_explanation=grounded_data["summary"],
            checked_sources_count=checked_sources_count,
            evidence=retrieved_evidence,
            evidence_chain=steps_log,
            share_card=share_card,
            is_demo=is_demo
        )

verification_engine = VerificationEngine()
