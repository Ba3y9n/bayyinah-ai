from typing import List, Dict, Any, Optional
from ..models.schemas import AssistantQuestionRequest, AssistantQuestionResponse, VerificationResponse
from ..config import settings

class AssistantService:
    def __init__(self):
        pass

    async def answer_question(self, req: AssistantQuestionRequest) -> AssistantQuestionResponse:
        q = req.question.strip()
        ctx: Optional[VerificationResponse] = req.verification_context
        
        # Default citations
        citations = []
        if ctx and ctx.evidence:
            for ev in ctx.evidence[:3]:
                citations.append(f"{ev.source_name} - {ev.reference}")

        # Intent handling for grounded questions
        q_lower = q.lower()
        
        # 1. "وش المصدر؟" / What is the source?
        if any(w in q_lower for w in ["وش المصدر", "ما هو المصدر", "منين المصدر", "المصادر", "وين المصدر", "ما المصدر"]):
            if ctx and ctx.evidence:
                sources_text = "\n".join([f"• **{ev.source_name}** ({ev.reference})\n  الرابط: {ev.url}" for ev in ctx.evidence])
                answer = (
                    f"المصادر التي استندت إليها نتيجة التحقق هي:\n\n{sources_text}\n\n"
                    f"وقد تم فحص وتوثيق النص بناءً على هذه المراجع المعتمدة فقط."
                )
            else:
                answer = "لم يتم العثور على مصدر موثق لهذا الادعاء في سجل المصادر المعتمدة المفحوصة."
            
            return AssistantQuestionResponse(
                answer=answer,
                grounded_citations=citations,
                avatar_state="evidence_found",
                suggested_followups=["وش الدليل من المتن؟", "ليش طلعت النتيجة كذا؟", "هل فيه مصدر ثاني؟"]
            )

        # 2. "وش الدليل؟" / What is the evidence?
        if any(w in q_lower for w in ["وش الدليل", "ما الدليل", "نص الدليل", "المتن", "الدليل"]):
            if ctx and ctx.evidence:
                top_ev = ctx.evidence[0]
                answer = (
                    f"الدليل المسترجع من **{top_ev.source_name}** هو:\n\n"
                    f"> «{top_ev.excerpt}»\n\n"
                    f"📌 **المرجع:** {top_ev.reference}"
                )
            else:
                answer = "الدليل غير متوفر في قواعد البيانات المعتمدة التي تم فحصها."

            return AssistantQuestionResponse(
                answer=answer,
                grounded_citations=citations,
                avatar_state="evidence_found",
                suggested_followups=["ليش طلعت النتيجة كذا؟", "هل فيه مصدر ثاني؟", "اشرح لي هذا الكلام."]
            )

        # 3. "ليش طلعت النتيجة كذا؟" / Why this result?
        if any(w in q_lower for w in ["ليش", "لماذا", "سبب النتيجة", "كيف بنيت", "علل"]):
            if ctx:
                answer = (
                    f"خرجت النتيجة بحالة: **[{ctx.status}]** للأسباب التالية:\n\n"
                    f"1. {ctx.reason}\n"
                    f"2. {ctx.detailed_explanation}\n\n"
                    f"تذكير: بيّنة AI لا تصدر أحكاماً دينية خاصة، بل تطابق النص مع المراجع المعتمدة."
                )
            else:
                answer = "النتيجة مبنية على مطابقة المتن مع قواعد البيانات المعتمدة."

            return AssistantQuestionResponse(
                answer=answer,
                grounded_citations=citations,
                avatar_state="explaining",
                suggested_followups=["وش المصدر؟", "وش الدليل؟", "اشرح لي هذا الكلام."]
            )

        # 4. "هل فيه مصدر ثاني؟" / Is there another source?
        if any(w in q_lower for w in ["مصدر ثاني", "مصادر اخرى", "مصادر ثانية", "مراجع ثانية"]):
            if ctx and len(ctx.evidence) > 1:
                other_sources = "\n".join([f"• **{ev.source_name}**: {ev.title} ({ev.reference})" for ev in ctx.evidence[1:]])
                answer = (
                    f"نعم، تم العثور على مراجع أخرى أثناء البحث:\n\n{other_sources}"
                )
            else:
                answer = "تم الاقتصار على المصدر المعتمد الرئيسي المسترجع في قاعدة البيانات."

            return AssistantQuestionResponse(
                answer=answer,
                grounded_citations=citations,
                avatar_state="explaining",
                suggested_followups=["وش الدليل؟", "اشرح لي هذا الكلام."]
            )

        # 5. "اشرح لي هذا الكلام" / Explain this
        if any(w in q_lower for w in ["اشرح", "توضيح", "ما معناه", "فهمني"]):
            if ctx:
                answer = (
                    f"شرح مبسط للأدلة المسترجعة:\n\n"
                    f"{ctx.detailed_explanation}\n\n"
                    f"يمكنك الاطلاع على النص الكامل للدليل عبر زيارة رابط المصدر الموثق مباشرة."
                )
            else:
                answer = "المعلومات المسترجعة تعتمد على التحقق المقارن مع أصل النص في المصادر المعتمدة."

            return AssistantQuestionResponse(
                answer=answer,
                grounded_citations=citations,
                avatar_state="explaining",
                suggested_followups=["وش المصدر؟", "وش الدليل؟", "ليش طلعت النتيجة كذا؟"]
            )

        # Generic grounded explanation
        if ctx:
            answer = (
                f"بناءً على الأدلة المسترجعة للادعاء: «{ctx.extracted_claim[:80]}...»:\n\n"
                f"{ctx.reason}\n\n"
                f"إذا كنت بحاجة لمعرفة تفصيل محدد عن المصدر أو الدليل أو سبب النتيجة، يمكنك سؤالي وسأشرحه لك من واقع الأدلة."
            )
        else:
            answer = "أنا مساعد بيّنة، وظيفتي شرح نتيجة التحقق والأدلة المسترجعة من المصادر المعتمدة."

        return AssistantQuestionResponse(
            answer=answer,
            grounded_citations=citations,
            avatar_state="explaining",
            suggested_followups=["وش المصدر؟", "وش الدليل؟", "ليش طلعت النتيجة كذا؟"]
        )

assistant_service = AssistantService()
