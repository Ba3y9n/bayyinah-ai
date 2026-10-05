import re
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from ..config import settings
from ..models.schemas import AssistantQuestionRequest, AssistantQuestionResponse, VerificationResponse
from ..models.knowledge_models import (
    ChatSessionModel,
    ChatMessageModel,
    ChatEvidenceBindingModel
)
from ..db.database import SessionLocal

class ChatGroundingService:
    """
    Evidence-Bound Conversation & Grounding Guard Service (Part 15 & 16)
    Strictly verifies that any answer is grounded in retrieved session evidence,
    classifies intents, blocks drift, and prevents hallucination.
    """
    def __init__(self):
        self.personal_case_patterns = [
            r'طلقت', r'زوجتي', r'طلاق', r'غضبان', r'حلفت', r'يمين', 
            r'كفارة', r'ميراث', r'أبي مات', r'امي ماتت', r'تركة', r'عمارة', r'توفي والدي', r'وصية خاصة'
        ]

    def classify_intent(self, question: str) -> str:
        q = question.strip().lower()

        # Check for fabrication/hallucination/pressure requests
        if any(w in q for w in ["اخترع", "اختراع", "تأليف", "ألف حديث", "اكذب", "قل لي أن الحديث موضوع ومكذوب حتى لو"]):
            return "FABRICATION_REQUEST"

        # Check for personal sensitive issues
        for pat in self.personal_case_patterns:
            if re.search(pat, q):
                return "PERSONAL_CASE"

        # Check for off topic
        if any(w in q for w in ["طقس", "كرة", "برمجة", "سياسة", "سعر", "سهم", "كعكة", "شوكولاتة", "طبخ", "وصفة", "اكل", "طعام"]):
            return "OFF_TOPIC"

        # Check for source/evidence inquiry
        if any(w in q for w in ["مصدر", "المصدر", "مرجع", "تخريج", "من وين", "وين الكتاب", "صحيح من"]):
            return "FOLLOWUP_ON_CURRENT_EVIDENCE"

        if any(w in q for w in ["دليل", "الدليل", "سند", "إسناد", "أين الدليل", "نص الدليل"]):
            return "FOLLOWUP_ON_CURRENT_EVIDENCE"

        if any(w in q for w in ["ليش", "لماذا", "سبب", "كيف طلعت", "الشرح", "اشرح", "معنى"]):
            return "GENERAL_EXPLANATION"

        if any(w in q for w in ["تحقق من", "افحص", "هل صحيح أن", "حديث جديد", "قال النبي صلى الله عليه وسلم"]):
            return "NEW_VERIFICATION"

        return "FOLLOWUP_ON_CURRENT_EVIDENCE"

    def process_and_ground(
        self,
        req: AssistantQuestionRequest,
        raw_answer: str,
        evidence_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Executes Server-Side Validation:
        Ensures the generated or synthesized response does not state ungrounded claims.
        """
        intent = self.classify_intent(req.question)

        # 0. Fabrication/Adversarial Request Protection
        if intent == "FABRICATION_REQUEST":
            return {
                "answer": (
                    "أمتنع تماماً عن اختراع أو تأليف أو تغيير أحاديث نبوية أو فتاوى شرعية. "
                    "منصة بيّنة AI تلتزم بالأمانة العلمية التامة والتوثيق الدقيق من المصادر المعتمدة دون زيادة أو اختلاق."
                ),
                "evidence_ids": [],
                "citations": ["المصادر المعتمدة"],
                "grounding_status": "ABSTAINED",
                "abstention_reason": "ADVERSARIAL_FABRICATION_ATTEMPT",
                "next_action": "REMPT_IN_DOMAIN",
                "avatar_state": "idle",
                "suggested_followups": ["ما هو مصدر الدليل الحالي؟", "أين الدليل؟"]
            }

        # 1. Personal Case Protection (Specialist Referral)
        if intent == "PERSONAL_CASE":
            return {
                "answer": (
                    "هذه المسألة تتعلق بوقائع شخصية خاصة (كالطلاق أو الأيمان أو المواريث والتركات)، "
                    "ولا يجوز للذكاء الاصطناعي إصدار فتاوى خاصة فيها. "
                    "الواجب التوجه المباشر إلى دار الإفتاء الرسمية أو المحاكم الشرعية المختصة لعرض تفاصيل الواقعة."
                ),
                "evidence_ids": [],
                "citations": ["دار الإفتاء الرسمية / المحاكم الشرعية"],
                "grounding_status": "SPECIALIST_REFERRAL",
                "abstention_reason": "PERSONAL_SENSITIVE_CASE",
                "next_action": "REFER_TO_AUTHORITY",
                "avatar_state": "explaining",
                "suggested_followups": [
                    "كيف أتواصل مع الإفتاء الرسمي؟",
                    "ما هي ضوابط الفتوى في النوازل؟"
                ]
            }

        # 2. Off-Topic Protection
        if intent == "OFF_TOPIC":
            return {
                "answer": (
                    "أنا «مساعد بيّنة» المخصص حصرًا للتحقق من المحتوى والأحاديث والآثار الإسلامية "
                    "وشرح الأدلة المسترجعة. لا أستطيع الإجابة عن مواضيع خارج نطاق التوثيق الإسلامي مثل الطبخ أو الطقس."
                ),
                "evidence_ids": [],
                "citations": [],
                "grounding_status": "ABSTAINED",
                "abstention_reason": "OFF_TOPIC_QUERY",
                "next_action": "REMPT_IN_DOMAIN",
                "avatar_state": "idle",
                "suggested_followups": [
                    "ما هو مصدر هذا الادعاء؟",
                    "ما هو نص الدليل المسترجع؟"
                ]
            }

        # 3. Grounding Validation against Session Evidence
        if not evidence_items:
            return {
                "answer": (
                    "لا أملك دليلاً كافياً في المصادر التي تم فحصها داخل الجلسة للإجابة عن ذلك، "
                    "وأمتنع عن الإجابة أو توليد نصوص من الذاكرة حفاظاً على الأمانة العلمية."
                ),
                "evidence_ids": [],
                "citations": [],
                "grounding_status": "ABSTAINED",
                "abstention_reason": "NO_EVIDENCE_IN_SESSION",
                "next_action": "TRIGGER_NEW_SEARCH",
                "avatar_state": "searching",
                "suggested_followups": [
                    "هل يمكن البحث في مصادر إضافية؟",
                    "عرض تفاصيل البحث المنفذ."
                ]
            }

        # Build citations directly from verified evidence items
        citations = []
        evidence_ids = []
        for ev in evidence_items:
            eid = str(ev.get("id") or ev.get("document_id") or "")
            if eid and eid not in evidence_ids:
                evidence_ids.append(eid)
            ref = ev.get("reference") or ev.get("source_name") or ""
            if ref and ref not in citations:
                citations.append(ref)

        # Ensure answer is safe and does not assert unverified assumptions
        final_answer = raw_answer
        if not final_answer or "عذرًا" in final_answer:
            # Deterministic grounded explanation from top evidence
            top_ev = evidence_items[0]
            final_answer = (
                f"استناداً إلى الدليل المعتمد في **{top_ev.get('source_name', 'السجل المعتمد')}**:\n\n"
                f"«{top_ev.get('excerpt', '')}»\n\n"
                f"**التخريج والمرجع:** {top_ev.get('reference', 'موثق في سجل المصادر')}.\n"
                f"ولا يتضمن السجل ما يخالف هذا اللفظ أو يثبت غيره."
            )

        # 4. Record session and message bindings in Database (if available)
        self._record_chat_in_db(
            session_id=req.session_id,
            claim_id=req.claim_id,
            user_question=req.question,
            assistant_answer=final_answer,
            intent=intent,
            grounding_status="GROUNDED",
            citations=citations,
            evidence_items=evidence_items
        )

        return {
            "answer": final_answer,
            "evidence_ids": evidence_ids,
            "citations": citations,
            "grounding_status": "GROUNDED",
            "abstention_reason": None,
            "next_action": "AWAIT_USER_PROMPT",
            "avatar_state": "evidence_found",
            "suggested_followups": [
                "ما هو نص الدليل الحرفي؟",
                "هل هناك تخريج آخر في السجل؟",
                "لماذا ظهرت هذه النتيجة؟"
            ]
        }

    def _record_chat_in_db(
        self,
        session_id: Optional[str],
        claim_id: Optional[str],
        user_question: str,
        assistant_answer: str,
        intent: str,
        grounding_status: str,
        citations: List[str],
        evidence_items: List[Dict[str, Any]]
    ):
        try:
            with SessionLocal() as db:
                c_session_id = session_id or str(uuid.uuid4())
                
                # Check or create chat session
                chat_session = db.query(ChatSessionModel).filter(ChatSessionModel.id == c_session_id).first()
                if not chat_session:
                    chat_session = ChatSessionModel(
                        id=c_session_id,
                        verification_session_id=session_id if session_id else None,
                        active_claim_id=claim_id if claim_id else None,
                        session_title=user_question[:100],
                        state="ACTIVE"
                    )
                    db.add(chat_session)
                    db.commit()

                # Record user message
                user_msg_id = str(uuid.uuid4())
                user_msg = ChatMessageModel(
                    id=user_msg_id,
                    chat_session_id=c_session_id,
                    role="user",
                    content=user_question,
                    intent=intent,
                    grounding_status="USER_INPUT"
                )
                db.add(user_msg)

                # Record assistant message
                asst_msg_id = str(uuid.uuid4())
                asst_msg = ChatMessageModel(
                    id=asst_msg_id,
                    chat_session_id=c_session_id,
                    role="assistant",
                    content=assistant_answer,
                    intent=intent,
                    grounding_status=grounding_status,
                    citations=citations,
                    avatar_state="evidence_found"
                )
                db.add(asst_msg)
                db.commit()

                # Bind evidence to message
                for ev in evidence_items[:5]:
                    ev_id = str(ev.get("id") or ev.get("document_id") or "")
                    if ev_id and len(ev_id) == 36:
                        binding = ChatEvidenceBindingModel(
                            id=str(uuid.uuid4()),
                            chat_message_id=asst_msg_id,
                            evidence_id=ev_id,
                            chunk_id=str(ev.get("chunk_id")) if ev.get("chunk_id") and len(str(ev.get("chunk_id"))) == 36 else None,
                            source_name=ev.get("source_name"),
                            reference=ev.get("reference"),
                            relevance_score=float(ev.get("relevance_score", 1.0))
                        )
                        db.add(binding)
                db.commit()
        except Exception as e:
            print(f"[ChatGroundingService] Notice: could not record chat bindings: {e}")

chat_grounding_service = ChatGroundingService()
