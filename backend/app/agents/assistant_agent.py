from typing import List, Dict, Any, Optional
from ..models.schemas import AssistantQuestionRequest, AssistantQuestionResponse, VerificationResponse

class AssistantAgent:
    """
    Bayyinah Conversational Assistant Agent (Section 31)
    Operates strictly on top of retrieved evidence for the active claim_id.
    """
    def __init__(self):
        pass

    async def answer(self, req: AssistantQuestionRequest) -> AssistantQuestionResponse:
        q = req.question.strip()
        q_lower = q.lower()
        ctx: Optional[VerificationResponse] = req.verification_context
        
        citations = []
        if ctx and ctx.evidence:
            for ev in ctx.evidence[:3]:
                citations.append(f"{ev.source_name} ({ev.reference})")

        # 1. "وش المصدر؟" / What is the source?
        if any(w in q_lower for w in ["وش المصدر", "ما هو المصدر", "المصادر", "وين المصدر", "ما المصدر"]):
            if ctx and ctx.evidence:
                sources_text = "\n".join([f"• **{ev.source_name}**\n  المرجع: {ev.reference}\n  الرابط: {ev.url}" for ev in ctx.evidence])
                answer = f"المصادر المفحوصة والمستند إليها هي:\n\n{sources_text}\n\nتم التحقق من النصوص استناداً إلى هذه السجلات الموثقة."
            else:
                answer = "لم يُعثر على مصدر موثق لهذا الادعاء في سجل المصادر المعتمدة المفحوصة."
            
            return AssistantQuestionResponse(
                answer=answer,
                grounded_citations=citations,
                avatar_state="evidence_found",
                suggested_followups=["اقرأ لي الدليل.", "ليش طلعت النتيجة كذا؟", "هل فيه مصادر ثانية؟"]
            )

        # 2. "اقرأ لي الدليل." / "وش الدليل؟" / Read the evidence
        if any(w in q_lower for w in ["اقرا لي الدليل", "وش الدليل", "ما الدليل", "نص الدليل", "الدليل"]):
            if ctx and ctx.evidence:
                top_ev = ctx.evidence[0]
                answer = (
                    f"نص الدليل المسترجع من **{top_ev.source_name}** هو:\n\n"
                    f"> «{top_ev.excerpt}»\n\n"
                    f"📌 **التخريج المعتمد:** {top_ev.reference}"
                )
            else:
                answer = "لا يوجد نص دليل مسند في قواعد البيانات المفحوصة."

            return AssistantQuestionResponse(
                answer=answer,
                grounded_citations=citations,
                avatar_state="evidence_found",
                suggested_followups=["اشرح لي النتيجة.", "هل فيه مصادر ثانية؟", "وش المصدر؟"]
            )

        # 3. "ليش قلت لم يثبت؟" / "ليش طلعت النتيجة كذا؟" / Why this result?
        if any(w in q_lower for w in ["ليش", "لماذا", "سبب", "علل", "كيف وصلت"]):
            if ctx:
                answer = (
                    f"صُنفت النتيجة كـ **[{ctx.status}]** لأن:\n\n"
                    f"1. {ctx.reason}\n"
                    f"2. {ctx.detailed_explanation}\n\n"
                    f"تنبيه: بيّنة لا تصدر أحكامًا خاصة، بل تطابق المتن الحرفي مع المتون المعتمدة."
                )
            else:
                answer = "النتيجة مبنية على مطابقة المتن مع قواعد البيانات المعتمدة."

            return AssistantQuestionResponse(
                answer=answer,
                grounded_citations=citations,
                avatar_state="explaining",
                suggested_followups=["اقرأ لي الدليل.", "وش المصدر؟", "اشرح لي النتيجة."]
            )

        # 4. "وش الفرق بين المصدرين؟" / Difference between sources?
        if any(w in q_lower for w in ["الفرق بين المصدرين", "خلاف", "اختلاف", "فرق"]):
            if ctx and len(ctx.evidence) >= 2:
                ev1, ev2 = ctx.evidence[0], ctx.evidence[1]
                answer = (
                    f"المقارنة بين المصادر المسترجعة:\n\n"
                    f"• **{ev1.source_name}:** {ev1.title} ({ev1.reference})\n"
                    f"  مقتطف: «{ev1.excerpt[:120]}...»\n\n"
                    f"• **{ev2.source_name}:** {ev2.title} ({ev2.reference})\n"
                    f"  مقتطف: «{ev2.excerpt[:120]}...»\n\n"
                    f"المسألة تم إسنادها لأصحابها دون ترجيح شخصي."
                )
            else:
                answer = "لم يتم رصد اختلاف بين مصادر متعددة في نطاق هذه النتيجة."

            return AssistantQuestionResponse(
                answer=answer,
                grounded_citations=citations,
                avatar_state="explaining",
                suggested_followups=["وش المصدر؟", "اقرأ لي الدليل."]
            )

        # 5. "هل فيه مصادر ثانية؟" / Other sources?
        if any(w in q_lower for w in ["مصادر ثانية", "مصدر ثاني", "مصادر اخرى"]):
            if ctx and len(ctx.evidence) > 1:
                others = "\n".join([f"• **{ev.source_name}**: {ev.title} ({ev.reference})" for ev in ctx.evidence[1:]])
                answer = f"نعم، تم استرجاع مراجع أخرى ذات صلة:\n\n{others}"
            else:
                answer = "اقتصر البحث على المصدر المعتمد الرئيسي المسترجع في قاعدة البيانات."

            return AssistantQuestionResponse(
                answer=answer,
                grounded_citations=citations,
                avatar_state="explaining",
                suggested_followups=["اقرأ لي الدليل.", "اشرح لي النتيجة."]
            )

        # Default grounded response
        if ctx:
            answer = (
                f"استناداً إلى أدلة الادعاء: «{ctx.extracted_claim[:80]}...»:\n\n"
                f"{ctx.reason}\n\n"
                f"يمكنك سؤالي عن الدليل أو المصدر أو التخريج المعتمد وسأجيبك من واقع الأدلة المسترجعة."
            )
        else:
            answer = "أنا مساعد بيّنة لشرح أدلة التحقق والمصادر المعتمدة."

        return AssistantQuestionResponse(
            answer=answer,
            grounded_citations=citations,
            avatar_state="idle",
            suggested_followups=["وش المصدر؟", "اقرأ لي الدليل.", "ليش طلعت النتيجة كذا؟"]
        )

assistant_agent = AssistantAgent()
