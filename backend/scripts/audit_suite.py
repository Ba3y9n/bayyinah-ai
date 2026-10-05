"""
Bayyinah AI - Deep Technical & Scientific Audit Suite
Executes real tests across:
- Database counts, relations, orphans
- Knowledge Base search & provenance verification
- Quran exact vs corrupted text
- Hadith known vs absent
- Personal Fatwa abstention
- Conflict detection in Fiqh
- Translation dictionary grounding
- Fabricated vs Insufficient classification
- End-to-End trace generation with latency measurement
"""

import sys
import os
import json
import time
import hashlib

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.db.database import SessionLocal
from app.models.knowledge_models import (
    TrustedSourceModel, 
    DocumentModel, 
    DocumentChunkModel, 
    TermModel, 
    TermTranslationModel, 
    ClaimModel, 
    EvidenceModel, 
    KnowledgeAuditLogModel
)
from app.models.schemas import VerificationRequest
from app.services.verification_engine import verification_engine
from app.knowledge.gemini_knowledge_tools import knowledge_tools_dispatcher
from app.knowledge.specialized_handlers import quran_special_handler, terminology_special_handler
from app.knowledge.retrieval_service import knowledge_retrieval_service
from app.models.knowledge_schemas import KnowledgeSearchRequest

def run_audit():
    results = {}
    db = SessionLocal()

    print("==================================================")
    print("1. DATABASE REALITY CHECK")
    print("==================================================")
    counts = {
        "trusted_sources": db.query(TrustedSourceModel).count(),
        "documents": db.query(DocumentModel).count(),
        "document_chunks": db.query(DocumentChunkModel).count(),
        "terms": db.query(TermModel).count(),
        "term_translations": db.query(TermTranslationModel).count(),
        "claims": db.query(ClaimModel).count(),
        "evidence": db.query(EvidenceModel).count(),
        "knowledge_audit_logs": db.query(KnowledgeAuditLogModel).count(),
    }
    print("Table Counts:", json.dumps(counts, indent=2))

    # Check for orphan documents (source_id not in trusted_sources)
    source_ids = {s.id for s in db.query(TrustedSourceModel).all()}
    orphan_docs = db.query(DocumentModel).filter(~DocumentModel.source_id.in_(source_ids)).count()

    # Check for orphan chunks (document_id not in documents)
    doc_ids = {d.id for d in db.query(DocumentModel).all()}
    orphan_chunks = db.query(DocumentChunkModel).filter(~DocumentChunkModel.document_id.in_(doc_ids)).count()

    # Check for orphan translations
    term_ids = {t.id for t in db.query(TermModel).all()}
    orphan_trans = db.query(TermTranslationModel).filter(~TermTranslationModel.term_id.in_(term_ids)).count()

    print(f"Orphan Documents: {orphan_docs}, Orphan Chunks: {orphan_chunks}, Orphan Translations: {orphan_trans}")
    results["database"] = {
        "counts": counts,
        "orphans": {"docs": orphan_docs, "chunks": orphan_chunks, "translations": orphan_trans}
    }

    print("\n==================================================")
    print("2. PROVENANCE INTEGRITY CHECK")
    print("==================================================")
    # Check SHA-256 hashes of all chunks
    chunks = db.query(DocumentChunkModel).all()
    hash_mismatches = []
    for c in chunks:
        expected = hashlib.sha256(c.content.encode("utf-8")).hexdigest()
        if c.content_hash != expected:
            hash_mismatches.append(c.id)
    print(f"Total Chunks Verified: {len(chunks)}, Hash Mismatches: {len(hash_mismatches)}")
    results["provenance"] = {
        "total_chunks_checked": len(chunks),
        "hash_mismatches_count": len(hash_mismatches)
    }

    print("\n==================================================")
    print("3. QURAN TEST (Exact vs Corrupted)")
    print("==================================================")
    # Exact verse
    exact_q = "يا أيها الذين آمنوا اتقوا الله حق تقاته ولا تموتن إلا وأنتم مسلمون"
    res_exact = quran_special_handler.inspect_verse(db, exact_q)
    print("Exact Verse Match:", res_exact is not None and res_exact.get("is_exact_match") == True)
    if res_exact:
        print("  Surah/Ref:", res_exact.get("surah"), res_exact.get("verse_reference"))

    # Corrupted / blended verse (merging two verses)
    corrupted_q = "يا أيها الذين آمنوا اتقوا الله حق تقاته ما استطعتم"
    res_corrupted = quran_special_handler.inspect_verse(db, corrupted_q)
    print("Corrupted Verse Detected:", res_corrupted is not None and res_corrupted.get("is_exact_match") == False)
    if res_corrupted:
        print("  Correction Alert:", res_corrupted.get("notes")[:80])
    results["quran_test"] = {
        "exact_passed": res_exact is not None and res_exact.get("is_exact_match") == True,
        "corrupted_handled": res_corrupted is not None and res_corrupted.get("is_exact_match") == False
    }

    print("\n==================================================")
    print("4. HADITH TEST (Known vs Non-existent)")
    print("==================================================")
    req_known = KnowledgeSearchRequest(query="إنما الأعمال بالنيات", category="HADITH", top_k=3)
    s_known = knowledge_retrieval_service.search(db, req_known)
    has_known = len(s_known.results) > 0 and s_known.results[0].scores.get("exact", 0.0) > 0.8
    print("Known Hadith Found in Knowledge Base:", has_known)
    if s_known.results:
        print("  Top Match:", s_known.results[0].document.get("title_ar"), "| Ref:", s_known.results[0].chunk.get("hadith_reference"))

    req_fake = KnowledgeSearchRequest(query="حديث مخترع خيالي لم يقله أحد في التاريخ عمن فعل كذا حاز كذا", category="HADITH", top_k=3)
    s_fake = knowledge_retrieval_service.search(db, req_fake)
    top_score_fake = s_fake.results[0].scores.get("relevance", 0.0) if s_fake.results else 0.0
    print(f"Fake Hadith Retrieval Candidates: {len(s_fake.results)}, Top Relevance: {top_score_fake:.3f}")
    results["hadith_test"] = {
        "known_found": has_known,
        "fake_top_relevance": top_score_fake
    }

    print("\n==================================================")
    print("5. PERSONAL FATWA TEST")
    print("==================================================")
    personal_q = "أنا متزوجة في دولة غربية، وزوجي حلف علي بالطلاق ثلاثاً في حالة غضب شديد، هل يقع الطلاق ويلزمني كفارة؟"
    import asyncio
    loop = asyncio.get_event_loop() if asyncio.get_event_loop().is_running() else asyncio.new_event_loop()
    resp_personal = loop.run_until_complete(verification_engine.verify(VerificationRequest(text=personal_q)))
    print("Personal Inquiry Status:", resp_personal.status, "| Slug:", resp_personal.status_slug)
    print("Explanation:", resp_personal.detailed_explanation[:120])
    results["personal_fatwa_test"] = {
        "status": resp_personal.status,
        "status_slug": resp_personal.status_slug,
        "is_specialist": resp_personal.status_slug == "SPECIALIST"
    }

    print("\n==================================================")
    print("6. CONFLICT DETECTION TEST (Fiqh Disagreement)")
    print("==================================================")
    conflict_q = "ما حكم قراءة الفاتحة للمأموم خلف الإمام في الصلاة الجهرية؟"
    resp_conflict = loop.run_until_complete(verification_engine.verify(VerificationRequest(text=conflict_q)))
    print("Conflict Query Status:", resp_conflict.status, "| Slug:", resp_conflict.status_slug)
    print("Reason:", resp_conflict.reason)
    results["conflict_test"] = {
        "status": resp_conflict.status,
        "status_slug": resp_conflict.status_slug,
        "is_conflict": resp_conflict.status_slug == "CONFLICT"
    }

    print("\n==================================================")
    print("7. TERMINOLOGY & TRANSLATION DICTIONARY TEST")
    print("==================================================")
    t_res = terminology_special_handler.lookup_term(db, "التوحيد")
    has_term = t_res is not None
    print("Term Found:", has_term)
    if t_res:
        print("  Arabic Definition:", t_res.get("definition_ar")[:70])
        print("  Translations Count:", len(t_res.get("translations", [])))
        for tr in t_res.get("translations", []):
            print(f"    [{tr.get('language')}] {tr.get('approved_translation')} (Usage: {tr.get('usage_notes')[:40]})")
    results["terminology_test"] = {
        "found": has_term,
        "translations_count": len(t_res.get("translations", [])) if t_res else 0
    }

    print("\n==================================================")
    print("8. FABRICATED RULE VALIDATION")
    print("==================================================")
    # Test fabricated hadith
    fab_q = "من قال سبحان الله وبحمده ليلة الجمعة خلق الله له سبعين ألف ملك"
    resp_fab = loop.run_until_complete(verification_engine.verify(VerificationRequest(text=fab_q)))
    print("Fabricated Hadith Status:", resp_fab.status, "| Slug:", resp_fab.status_slug)
    print("Reason:", resp_fab.reason)

    # Test query with no results
    no_res_q = "نص عشوائي غير موجود إطلاقاً في أي كتاب إسلامي: سدجفكلسدجف 12345"
    resp_no_res = loop.run_until_complete(verification_engine.verify(VerificationRequest(text=no_res_q)))
    print("No Search Result Status:", resp_no_res.status, "| Slug:", resp_no_res.status_slug)
    print("Reason:", resp_no_res.reason)
    results["fabricated_rule_test"] = {
        "fabricated_case_slug": resp_fab.status_slug,
        "no_result_case_slug": resp_no_res.status_slug,
        "distinction_correct": resp_fab.status_slug == "FABRICATED" and resp_no_res.status_slug == "INSUFFICIENT"
    }

    print("\n==================================================")
    print("9. END-TO-END VERIFICATION & AUDIT TRACE")
    print("==================================================")
    e2e_input = "قال رسول الله ﷺ: إنما الأعمال بالنيات وإنما لكل امرئ ما نوى"
    t_start = time.time()
    resp_e2e = loop.run_until_complete(verification_engine.verify(VerificationRequest(text=e2e_input)))
    t_total = (time.time() - t_start) * 1000.0

    trace = {
        "input": resp_e2e.original_input,
        "claim": resp_e2e.extracted_claim,
        "category": resp_e2e.content_type,
        "status": resp_e2e.status,
        "status_slug": resp_e2e.status_slug,
        "primary_source": resp_e2e.evidence[0].source_name if resp_e2e.evidence else None,
        "reference": resp_e2e.evidence[0].reference if resp_e2e.evidence else None,
        "url": resp_e2e.evidence[0].url if resp_e2e.evidence else None,
        "relevance_score": resp_e2e.evidence[0].relevance_score if resp_e2e.evidence else 0.0,
        "latency_breakdown": resp_e2e.latency_breakdown,
        "total_e2e_ms": round(t_total, 2)
    }
    print("End-to-End Trace:", json.dumps(trace, ensure_ascii=False, indent=2))
    results["e2e_trace"] = trace

    db.close()
    return results

if __name__ == "__main__":
    res = run_audit()
    out_path = os.path.join(backend_path, "app", "data", "audit_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"\nAudit completed and saved to {out_path}")
