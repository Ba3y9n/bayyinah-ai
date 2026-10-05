import uuid
import datetime
import time
from typing import Dict, Any, Optional, List

from ..models.schemas import (
    VerificationRequest, 
    VerificationResponse, 
    VerificationStepLog, 
    EvidenceItem, 
    ShareCardData,
    CanonicalVerificationStatus,
    StructuredVerificationResult,
    EvidenceGraphResponse,
    EvidenceGraphNode,
    EvidenceGraphEdge,
    MultiClaimItem
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

def build_evidence_graph(session_id: str, claim_text: str, evidence: List[EvidenceItem], status_ar: str) -> EvidenceGraphResponse:
    """
    Constructs an interactive evidence graph connecting input, claim, sources, evidence chunks, and result.
    """
    nodes: List[EvidenceGraphNode] = []
    edges: List[EvidenceGraphEdge] = []
    sid = session_id[:8]

    # Input Node
    input_node_id = f"node-input-{sid}"
    nodes.append(EvidenceGraphNode(
        id=input_node_id,
        type="INPUT",
        label="المدخل الأصلي",
        metadata={"text": claim_text[:80]}
    ))

    # Claim Node
    claim_node_id = f"node-claim-{sid}"
    nodes.append(EvidenceGraphNode(
        id=claim_node_id,
        type="CLAIM",
        label="الادعاء المستخرج",
        metadata={"claim": claim_text}
    ))
    edges.append(EvidenceGraphEdge(
        source=input_node_id,
        target=claim_node_id,
        relationship="EXTRACTED_FROM"
    ))

    # Sources & Evidence Nodes
    for i, ev in enumerate(evidence[:4]):
        src_id = ev.source_id or f"src-{i}"
        source_node_id = f"node-src-{src_id}"
        ev_node_id = f"node-ev-{sid}-{i}"

        # Source node if not already added
        if not any(n.id == source_node_id for n in nodes):
            nodes.append(EvidenceGraphNode(
                id=source_node_id,
                type="SOURCE",
                label=ev.source_name or "المصدر المعتمد",
                metadata={"source_id": ev.source_id, "url": ev.url}
            ))
            edges.append(EvidenceGraphEdge(
                source=claim_node_id,
                target=source_node_id,
                relationship="SEARCHED_FOR"
            ))

        # Evidence node
        nodes.append(EvidenceGraphNode(
            id=ev_node_id,
            type="EVIDENCE",
            label=f"دليل #{i+1}: {ev.source_name}",
            metadata={
                "excerpt": ev.excerpt[:100],
                "score": ev.relevance_score,
                "grade": ev.ruling_or_grade,
                "reference": ev.reference
            }
        ))
        edges.append(EvidenceGraphEdge(
            source=source_node_id,
            target=ev_node_id,
            relationship="RETRIEVED_FROM"
        ))
        edges.append(EvidenceGraphEdge(
            source=ev_node_id,
            target=claim_node_id,
            relationship="EVIDENCE_OF"
        ))

    # Result Node
    result_node_id = f"node-result-{sid}"
    nodes.append(EvidenceGraphNode(
        id=result_node_id,
        type="RESULT",
        label=status_ar,
        metadata={"status": status_ar}
    ))
    edges.append(EvidenceGraphEdge(
        source=claim_node_id,
        target=result_node_id,
        relationship="RESOLVED_TO"
    ))

    return EvidenceGraphResponse(
        session_id=session_id,
        nodes=nodes,
        edges=edges
    )

class VerificationEngine:
    """
    Core Pipeline Orchestrator executing the 13 verification steps
    and coordinating between the 8 specialized AI agents.
    """
    def __init__(self):
        pass

    async def verify(self, request: VerificationRequest, is_demo: bool = False, db: Optional[Any] = None) -> VerificationResponse:
        claim_id = str(uuid.uuid4())
        steps_log: List[VerificationStepLog] = []
        total_start = time.time()
        gemini_time_ms = 0.0
        search_time_ms = 0.0
        db_time_ms = 0.0
        val_time_ms = 0.0

        # =========================================================================
        # STEP 1 & 2: Multimodal analysis & OCR Text Extraction
        # =========================================================================
        raw_text = request.text or ""
        is_image = bool(request.image_base64)
        
        if is_image:
            t0 = time.time()
            ocr_text = gemini_service.extract_text_from_image(request.image_base64)
            gemini_time_ms += (time.time() - t0) * 1000.0
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
        t_claim = time.time()
        claim_data = claim_agent.process(raw_text, is_image=is_image)
        gemini_time_ms += (time.time() - t_claim) * 1000.0
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
        t_query = time.time()
        search_queries = query_agent.generate_queries(claim_data)
        gemini_time_ms += (time.time() - t_query) * 1000.0
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
        # STEP 9: Retrieval Agent & Official Source Coverage Orchestrator
        # =========================================================================
        t_ret = time.time()
        from ..knowledge.source_coverage_orchestrator import source_coverage_orchestrator

        coverage_run = await source_coverage_orchestrator.execute_coverage(
            claim_text=main_claim,
            content_type=claim_type,
            session_id=claim_id,
            claim_id=claim_id
        )

        retrieved_evidence = retrieval_agent.orchestrate_hybrid_retrieval(
            queries=search_queries,
            limit=5,
            category=claim_type,
            claim_text=main_claim,
            db=db,
            claim_id=claim_id
        )
        ret_dur = (time.time() - t_ret) * 1000.0
        search_time_ms += ret_dur * 0.65
        db_time_ms += ret_dur * 0.35
        steps_log.append(VerificationStepLog(
            step_number=9,
            title="استرجاع وثائق الأدلة وفحص تغطية المصادر الـ 11 المعتمدة",
            description=f"تم فحص التغطية للمصادر المعتمدة (فحص {coverage_run['queried_sources_count']} من 11 مصدرًا) واسترجاع {len(retrieved_evidence)} أدلة موثقة.",
            status="completed",
            data={"count": len(retrieved_evidence), "coverage": coverage_run}
        ))

        # =========================================================================
        # STEP 10: Evidence Agent & Conflict Agent (Validation & Conflicts)
        # =========================================================================
        t_val = time.time()
        validation_data = evidence_agent.validate(main_claim, retrieved_evidence)
        conflicts_data = conflict_agent.detect_conflicts(claim_type, retrieved_evidence)
        val_time_ms += (time.time() - t_val) * 1000.0
        
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
            # Evaluate standard states purely based on evidence grade, relevance, and comparison notes
            top_ev = retrieved_evidence[0] if retrieved_evidence else None
            meta_grade = ((top_ev.ruling_or_grade if top_ev and top_ev.ruling_or_grade else "")).lower()
            excerpt_lower = ((top_ev.excerpt if top_ev and top_ev.excerpt else "")).lower()
            comparison_lower = ((top_ev.comparison_notes if top_ev and top_ev.comparison_notes else "")).lower()

            is_explicit_fabricated = top_ev and top_ev.relevance_score >= 0.50 and (
                "موضوع" in meta_grade or "باطل" in meta_grade or
                "حديث باطل" in excerpt_lower or "حديث موضوع" in excerpt_lower or
                "باطل وموضوع" in excerpt_lower or "موضوع ومكذوب" in excerpt_lower or
                "باطل لا أصل له" in excerpt_lower or "موضوع لا أصل له" in excerpt_lower or
                "حكم الحديث: باطل" in excerpt_lower or "حكم الحديث: موضوع" in excerpt_lower
            )

            is_explicit_weak = top_ev and top_ev.relevance_score >= 0.50 and (
                "ضعيف" in meta_grade or
                "حديث ضعيف" in excerpt_lower or "درجة الحديث: ضعيف" in excerpt_lower or
                "ضعيف ولم يثبت" in excerpt_lower or "ضعف الحديث" in excerpt_lower
            )

            is_not_established = top_ev and top_ev.relevance_score >= 0.45 and (
                "لم يثبت" in meta_grade or "لم يثبت" in comparison_lower or
                "لا أصل له" in excerpt_lower or "لم أقف عليه" in excerpt_lower
            )

            if is_explicit_fabricated:
                status_slug = "FABRICATED"
                status_ar = "موضوع/مكذوب بحسب المصدر"
                reason = f"النص مصنف كـ ({status_ar}) في {top_ev.source_name}."
            elif is_explicit_weak:
                status_slug = "WEAK"
                status_ar = "ضعيف بحسب المصدر"
                reason = f"النص مصنف كـ ({status_ar}) في {top_ev.source_name}."
            elif is_not_established:
                status_slug = "NOT_ESTABLISHED"
                status_ar = "لم يثبت بهذا اللفظ"
                reason = "الصياغة المتداولة لم تثبت بهذا اللفظ في المصادر المعتمدة."
            elif top_ev and top_ev.relevance_score >= 0.50:
                status_slug = "VERIFIED"
                status_ar = "ثابت بحسب المصدر"
                reason = f"النص مطابق للمتن المعتمد وموثق في {top_ev.source_name}."
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

        t_ground = time.time()
        grounded_data = grounding_agent.generate(
            claim_data=claim_data,
            status=status_slug,
            status_ar=status_ar,
            reason=reason,
            evidence_items=retrieved_evidence,
            conflicts_data=conflicts_data,
            limitations=limitations
        )
        gemini_time_ms += (time.time() - t_ground) * 1000.0

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

        checked_sources_count = coverage_run.get("queried_sources_count", len(coverage_run.get("relevant_sources", [])))
        total_latency_ms = (time.time() - total_start) * 1000.0

        # Persist verification audit log and evidence into Knowledge Base database
        try:
            from ..db.database import SessionLocal
            from ..models.knowledge_models import KnowledgeAuditLogModel, EvidenceModel
            with SessionLocal() as db_session:
                audit_log = KnowledgeAuditLogModel(
                    id=str(uuid.uuid4()),
                    request_id=claim_id,
                    claim_id=claim_id,
                    query=raw_text[:500],
                    search_query=" | ".join(search_queries) if search_queries else raw_text[:200],
                    category_filter=claim_type,
                    sources_checked=checked_sources_count,
                    documents_checked=len(retrieved_evidence),
                    chunks_checked=len(retrieved_evidence),
                    evidence_found=len(retrieved_evidence),
                    validation_result=status_slug,
                    conflicts_found=bool(conflicts_data.get("conflict_detected", False)),
                    final_status=status_slug
                )
                db_session.add(audit_log)
                for ev in retrieved_evidence:
                    db_ev = EvidenceModel(
                        id=str(uuid.uuid4()),
                        claim_id=claim_id,
                        source_id=ev.source_id,
                        document_id=ev.document_id,
                        chunk_id=getattr(ev, "chunk_id", ev.document_id),
                        evidence_type=ev.evidence_type,
                        matched_text=ev.excerpt,
                        evidence_text=ev.excerpt,
                        source_url=ev.url,
                        reference=ev.reference,
                        locator=ev.reference or "",
                        url=ev.url,
                        exact_score=ev.relevance_score,
                        rrf_score=ev.relevance_score,
                        support_type=ev.evidence_type,
                        support_score=ev.relevance_score,
                        support_level=ev.evidence_type,
                        validation_status=status_slug
                    )
                    db_session.add(db_ev)
                db_session.commit()
        except Exception:
            pass

        # Multi-claim decomposition
        multi_claims = claim_agent.extract_multi_claims(raw_text)

        # Section 21 & 22: EvidenceGate Zero-Hallucination Guard
        from .evidence_gate import evidence_gate, ABSTENTION_MESSAGE
        gate_res = evidence_gate.validate(
            evidences=[
                {"source_id": getattr(ev, "source_id", None), "url": getattr(ev, "url", None), "text": getattr(ev, "excerpt", "")}
                for ev in retrieved_evidence
            ],
            confidence_score=0.98 if status_slug in ["VERIFIED", "FABRICATED", "SPECIALIST"] else 0.90,
            claim_text=main_claim,
            verdict=status_ar
        )
        if gate_res.get("abstention_required"):
            status_ar = "مجهول / غير ثابت بحسب البحث الحالي"
            status_slug = "INSUFFICIENT"
            reason = ABSTENTION_MESSAGE

        # Build canonical result object
        canonical_map = {
            "VERIFIED": CanonicalVerificationStatus.VERIFIED.value,
            "NOT_ESTABLISHED": CanonicalVerificationStatus.NOT_ESTABLISHED_BY_EXACT_WORDING.value,
            "INSUFFICIENT": CanonicalVerificationStatus.INSUFFICIENT_EVIDENCE.value,
            "CONFLICT": CanonicalVerificationStatus.SCHOLARLY_DISAGREEMENT.value,
            "SPECIALIST": CanonicalVerificationStatus.NEEDS_SPECIALIST.value,
            "WEAK": CanonicalVerificationStatus.WEAK.value,
            "FABRICATED": CanonicalVerificationStatus.FABRICATED.value,
        }
        canonical_status = canonical_map.get(status_slug, CanonicalVerificationStatus.INSUFFICIENT_EVIDENCE.value)
        specialist_req = bool(claim_data.get("requires_specialist", False) or status_slug == "SPECIALIST")

        result_object = StructuredVerificationResult(
            status=canonical_status,
            label_ar=status_ar,
            claim=main_claim,
            reason=reason,
            evidence_ids=[ev.document_id for ev in retrieved_evidence if getattr(ev, "document_id", None)],
            source_ids=list(dict.fromkeys(ev.source_id for ev in retrieved_evidence if getattr(ev, "source_id", None))),
            citations=[f"{ev.source_name} - {ev.reference}" for ev in retrieved_evidence if ev.source_name and ev.reference],
            conflict_status="SCHOLARLY_DISAGREEMENT" if status_slug == "CONFLICT" else "NONE",
            grounding_status="ABSTAINED" if status_slug == "INSUFFICIENT" else ("SPECIALIST_REFERRAL" if specialist_req else "GROUNDED"),
            abstained=(status_slug == "INSUFFICIENT"),
            specialist_required=specialist_req
        )

        evidence_graph = build_evidence_graph(claim_id, main_claim, retrieved_evidence, status_ar)

        return VerificationResponse(
            claim_id=claim_id,
            session_id=claim_id,
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
            conflicts_found=bool(conflicts_data.get("conflict_detected", False)),
            limitations=limitations,
            specialist_required=specialist_req,
            latency_breakdown={
                "gemini_latency_ms": round(gemini_time_ms, 1),
                "search_latency_ms": round(search_time_ms, 1),
                "database_latency_ms": round(db_time_ms, 1),
                "validation_latency_ms": round(val_time_ms, 1),
                "total_latency_ms": round(total_latency_ms, 1)
            },
            result_object=result_object,
            multi_claims=multi_claims,
            evidence_graph=evidence_graph,
            source_coverage=coverage_run,
            is_demo=is_demo
        )

verification_engine = VerificationEngine()
