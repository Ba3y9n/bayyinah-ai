"""
Bayyinah AI - Production Conversational Assistant Agent
Implements:
1. Strict Claim Isolation (Part 24)
2. Structured Verification State Injection (Part 25)
3. Follow-up Classification (Part 26)
4. Chat Evidence Lock: No hallucinated assertions (Part 27)
5. Session Conversation Logging (Part 28)
"""

import json
from typing import List, Dict, Any, Optional
from ..models.schemas import AssistantQuestionRequest, AssistantQuestionResponse, VerificationResponse
from ..services.gemini_service import gemini_service
from ..config import settings
from ..db.database import SessionLocal
from ..models.knowledge_models import ConversationMessageModel, VerificationSessionModel

try:
    from google.genai import types
except ImportError:
    types = None

class AssistantAgent:
    """
    Production Anti-Hallucination Assistant.
    Never improvises or uses model memory as evidence.
    Strictly locked to supplied evidence for the active claim.
    """

    def classify_intent(self, question: str) -> str:
        q = question.strip().lower()
        if any(w in q for w in ["تحقق من", "طيب هذا الحديث", "ما صحة حديث آخر", "حديث ثاني", "تحقق من هذا النص"]):
            return "NEW_VERIFICATION"
        elif any(w in q for w in ["المصدر", "وش المصدر", "ما المصدر", "أين المصدر"]):
            return "SOURCE_REQUEST"
        elif any(w in q for w in ["الدليل", "نص الدليل", "وش الدليل", "اقرأ الدليل"]):
            return "EVIDENCE_REQUEST"
        elif any(w in q for w in ["ليش", "لماذا", "اشرح", "كيف وصلت", "السبب"]):
            return "EXPLANATION_REQUEST"
        elif any(w in q for w in ["خلاف", "اختلاف", "فرق", "هل فيه تعارض"]):
            return "CONFLICT_REQUEST"
        elif any(w in q for w in ["طقس", "كرة", "برمجة", "سعر", "سياسة"]):
            return "OUT_OF_SCOPE"
        return "FOLLOW_UP"

    def build_verification_state(self, ctx: Optional[VerificationResponse]) -> Dict[str, Any]:
        if not ctx:
            return {
                "active_claim": "غير محدد",
                "status": "لم يتم التحقق بعد",
                "evidence": [],
                "sources": [],
                "limitations": []
            }

        evidence_list = []
        sources_list = []
        for ev in (ctx.evidence or []):
            evidence_list.append({
                "id": str(getattr(ev, "id", "") or ""),
                "excerpt": ev.excerpt,
                "reference": ev.reference,
                "source_name": ev.source_name,
                "url": ev.url
            })
            if ev.source_name not in sources_list:
                sources_list.append(ev.source_name)

        claim_text = getattr(ctx, "extracted_claim", None) or getattr(ctx, "claim", "")
        return {
            "active_claim": claim_text,
            "status": ctx.status,
            "reason": ctx.reason,
            "evidence": evidence_list,
            "sources": sources_list,
            "conflicts": ctx.conflicts_found or False,
            "limitations": ctx.limitations or []
        }

    async def answer(self, req: AssistantQuestionRequest) -> AssistantQuestionResponse:
        from ..services.chat_grounding_service import chat_grounding_service
        q = req.question.strip()
        ctx: Optional[VerificationResponse] = req.verification_context
        v_state = self.build_verification_state(ctx)

        # Check intent with chat_grounding_service
        evidence_items = v_state.get("evidence", [])
        grounding_eval = chat_grounding_service.process_and_ground(req, "", evidence_items)
        if grounding_eval.get("grounding_status") in ("ABSTAINED", "SPECIALIST_REFERRAL"):
            return AssistantQuestionResponse(
                answer=grounding_eval["answer"],
                grounded_citations=grounding_eval.get("citations", []),
                avatar_state=grounding_eval.get("avatar_state", "idle"),
                suggested_followups=grounding_eval.get("suggested_followups", [])
            )

        intent = self.classify_intent(q)

        # Log to database if session exists
        session_id = getattr(req, "session_id", None)
        if session_id and SessionLocal:
            try:
                db = SessionLocal()
                msg = ConversationMessageModel(
                    verification_session_id=str(session_id),
                    role="user",
                    content=q
                )
                db.add(msg)
                db.commit()
                db.close()
            except Exception:
                pass

        # 1. NEW_VERIFICATION: Enforce Claim Isolation (Part 24)
        if intent == "NEW_VERIFICATION":
            answer = (
                "لقد طلبت التحقق من نص أو ادعاء جديد. لحفظ دقة وموثوقية الأدلة وعزل كل ادعاء عن غيره، "
                "يرجى إرسال النص الجديد عبر صندوق التحقق الرئيسي لفتح جلسة فحص مستقلة خاصة به."
            )
            return AssistantQuestionResponse(
                answer=answer,
                grounded_citations=[],
                avatar_state="ready",
                suggested_followups=["ما المصدر للنتيجة الحالية؟", "اقرأ لي الدليل الحالي."]
            )

        # 2. OUT_OF_SCOPE: Abstain immediately
        if intent == "OUT_OF_SCOPE":
            return AssistantQuestionResponse(
                answer="بيّنة AI منصة علمية متخصصة فقط في التحقق من صحة ونسبة المحتوى الإسلامي الرقمي وفق مصادره الموثقة.",
                grounded_citations=[],
                avatar_state="ready",
                suggested_followups=[]
            )

        # 3. Handle SOURCE_REQUEST
        if intent == "SOURCE_REQUEST":
            if v_state["sources"]:
                sources_str = "\n".join([f"• **{s}**" for s in v_state["sources"]])
                refs_str = "\n".join([f"  - مرجع: {e['reference']} ({e['source_name']})" for e in v_state["evidence"]])
                answer = f"المصادر المفحوصة والمستند إليها في هذا التحقق هي:\n\n{sources_str}\n\nالمراجع الدقيقة:\n{refs_str}"
            else:
                answer = "لم يُعثر على مصادر موثقة تثبت هذا النص ضمن نطاق البحث المفحوص."
            return AssistantQuestionResponse(
                answer=answer,
                grounded_citations=[e["reference"] for e in v_state["evidence"][:2]],
                avatar_state="evidence_found",
                suggested_followups=["اقرأ لي الدليل.", "اشرح لي النتيجة."]
            )

        # 4. Handle EVIDENCE_REQUEST
        if intent == "EVIDENCE_REQUEST":
            if v_state["evidence"]:
                top_e = v_state["evidence"][0]
                answer = (
                    f"نص الدليل المعتمد من **{top_e['source_name']}**:\n\n"
                    f"> «{top_e['excerpt']}»\n\n"
                    f"📍 **المرجع:** {top_e['reference']}"
                )
            else:
                answer = "لا يوجد نص دليل مسند في قواعد البيانات المفحوصة."
            return AssistantQuestionResponse(
                answer=answer,
                grounded_citations=[e["reference"] for e in v_state["evidence"][:2]],
                avatar_state="evidence_found",
                suggested_followups=["ما المصدر؟", "اشرح لي النتيجة."]
            )

        # 5. Handle EXPLANATION_REQUEST or general FOLLOW_UP with Gemini 3.8 Flash
        if gemini_service.is_configured and gemini_service.client and types:
            try:
                system_instruction = (
                    "أنت المساعد الذكي لمنصة بيّنة AI. مهمتك شرح وتفسير نتيجة التحقق المعروضة حصراً.\n"
                    "قواعد صارمة لا تقبل الاستثناء:\n"
                    "1. ممنوع نهائياً تأليف أو استدعاء أي معلومة أو حديث أو فتوى من ذاكرتك المسبقة.\n"
                    "2. استند حصراً إلى أدلة 'VERIFICATION_STATE' المزودة إليك أدناه.\n"
                    "3. إذا لم تجد الإجابة ضمن نصوص الأدلة المزودة، قل بوضوح تام: "
                    "'لا أملك دليلاً كافياً ضمن نتيجة التحقق الحالية لإجابة هذا السؤال.'\n"
                    "4. التزم بأسلوب علمي رصين ومختصر باللغة العربية الفصحى."
                )

                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    thinking_config=types.ThinkingConfig(thinking_level="high")
                )

                prompt = (
                    f"حالة التحقق الحالية (VERIFICATION_STATE):\n{json.dumps(v_state, ensure_ascii=False)}\n\n"
                    f"سؤال المستخدم: {q}\n"
                    "أجب باختصار باللغة العربية مع الاستناد للأدلة المذكورة فقط."
                )

                resp = gemini_service.client.models.generate_content(
                    model=gemini_service.model_name,
                    contents=prompt,
                    config=config
                )
                if resp and resp.text:
                    ans_text = resp.text.strip()
                    citations = [f"{e['source_name']} ({e['reference']})" for e in v_state["evidence"][:3]]
                    return AssistantQuestionResponse(
                        answer=ans_text,
                        grounded_citations=citations,
                        avatar_state="explaining",
                        suggested_followups=["ما المصدر؟", "أين الدليل؟", "هل يوجد اختلاف؟"]
                    )
            except Exception as e:
                print(f"[AssistantAgent] Gemini chat error: {e}")

        # Strict evidence lock fallback
        if not v_state["evidence"]:
            answer = "لا أملك دليلاً كافياً ضمن نتيجة التحقق الحالية للإجابة عن هذا السؤال، حفاظاً على الأمانة العلمية."
        else:
            top_e = v_state["evidence"][0]
            answer = (
                f"استناداً إلى الدليل المسترجع من **{top_e['source_name']}** ({top_e['reference']})، "
                f"فإن النتيجة مبنية على مطابقة المتن المعروض: «{top_e['excerpt'][:120]}...»."
            )

        return AssistantQuestionResponse(
            answer=answer,
            grounded_citations=[f"{e['source_name']} ({e['reference']})" for e in v_state["evidence"][:2]],
            avatar_state="explaining",
            suggested_followups=["ما المصدر؟", "أين الدليل؟"]
        )

assistant_agent = AssistantAgent()
