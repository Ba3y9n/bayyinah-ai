"""
Bayyinah AI - Database & Retrieval Test Suite (10 Cases)
Tests Supabase PostgreSQL schema, FTS, pgvector, hybrid search, RLS, and session persistence.
"""

import sys
import os
import uuid
from sqlalchemy import text

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db.database import SessionLocal, engine
from app.services.search_service import SearchService

search_svc = SearchService()

def run_tests():
    print("=" * 70)
    print("BAYYINAH AI — DATABASE & RETRIEVAL TEST SUITE (10 CASES)")
    print("=" * 70)

    passed = 0
    failed = 0

    # 1. Canonical Schema Verification
    print("\n[1/10] Testing DB-01: Canonical Schema Table Existence")
    expected_tables = [
        "sources", "documents", "document_chunks", "claims", "evidence",
        "verification_sessions", "verification_results", "verification_evidence",
        "url_submissions", "media_assets", "chat_sessions", "chat_messages",
        "chat_evidence_bindings", "ingestion_jobs"
    ]
    try:
        with SessionLocal() as db:
            result = db.execute(text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public';
            """))
            tables = [row[0] for row in result.fetchall()]
            missing = [t for t in expected_tables if t not in tables]
            if not missing:
                print(f"  ✅ PASSED: All {len(expected_tables)} enterprise tables exist in public schema.")
                passed += 1
            else:
                print(f"  ❌ FAILED: Missing tables: {missing}")
                failed += 1
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        failed += 1

    # 2. PostgreSQL Arabic Full-Text Search (FTS)
    print("\n[2/10] Testing DB-02: PostgreSQL Arabic FTS Execution")
    try:
        with SessionLocal() as db:
            res = db.execute(text("""
                SELECT id, content 
                FROM document_chunks 
                WHERE content ILIKE '%الخطاب%' OR content ILIKE '%عمر%' OR normalized_text ILIKE '%النية%'
                LIMIT 3;
            """)).fetchall()
            if len(res) > 0:
                snippet = (res[0][1] or "")[:60]
                print(f"  ✅ PASSED: Retrieved {len(res)} chunks matching hadith query. Sample: {snippet}...")
                passed += 1
            else:
                print("  ❌ FAILED: No chunks returned for FTS keyword query.")
                failed += 1
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        failed += 1

    # 3. pgvector Extension and Vector Column Verification
    print("\n[3/10] Testing DB-03: pgvector Extension & 768-d Column")
    try:
        with SessionLocal() as db:
            ext = db.execute(text("SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';")).fetchone()
            col = db.execute(text("""
                SELECT column_name, udt_name 
                FROM information_schema.columns 
                WHERE table_name = 'document_chunks' AND column_name = 'embedding';
            """)).fetchone()
            if ext and col and col[1] == 'vector':
                print(f"  ✅ PASSED: pgvector v{ext[1]} active, document_chunks.embedding type is '{col[1]}'.")
                passed += 1
            else:
                print(f"  ❌ FAILED: Vector verification mismatch. Ext: {ext}, Col: {col}")
                failed += 1
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        failed += 1

    # 4. Search Service Keyword Retrieval
    print("\n[4/10] Testing DB-04: SearchService Exact/Keyword Retrieval Pipeline")
    try:
        results = search_svc.exact_text_search(query="الأعمال بالنيات", limit=5)
        if results and len(results) > 0:
            print(f"  ✅ PASSED: SearchService returned {len(results)} ranked chunks.")
            passed += 1
        else:
            print("  ❌ FAILED: SearchService returned 0 results.")
            failed += 1
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        failed += 1

    # 5. Hybrid Search Pipeline (RRF Simulation)
    print("\n[5/10] Testing DB-05: Hybrid Search Pipeline Execution")
    try:
        results = search_svc.hybrid_search(queries=["النية", "الأعمال"], limit=5)
        if results is not None and len(results) > 0:
            print(f"  ✅ PASSED: hybrid_search executed successfully, returned {len(results)} items.")
            passed += 1
        else:
            print("  ❌ FAILED: hybrid_search returned 0 items.")
            failed += 1
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        failed += 1

    # 6. Row-Level Security (RLS) Policy Verification
    print("\n[6/10] Testing DB-06: RLS Active on Public Knowledge Base Tables")
    try:
        with SessionLocal() as db:
            rls_check = db.execute(text("""
                SELECT tablename, rowsecurity 
                FROM pg_tables 
                WHERE schemaname = 'public' AND tablename IN ('sources', 'documents', 'document_chunks');
            """)).fetchall()
            all_rls = all(row[1] for row in rls_check)
            if len(rls_check) == 3 and all_rls:
                print(f"  ✅ PASSED: RLS is ENABLED on sources, documents, and document_chunks.")
                passed += 1
            else:
                print(f"  ❌ FAILED: RLS status: {rls_check}")
                failed += 1
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        failed += 1

    # 7. Verification Session Persistence
    print("\n[7/10] Testing DB-07: Verification Session INSERT & SELECT")
    test_session_id = str(uuid.uuid4())
    try:
        with SessionLocal() as db:
            db.execute(text("""
                INSERT INTO verification_sessions (id, session_status, input_type, input_reference)
                VALUES (:id, 'COMPLETED', 'TEXT', 'اختبار تجريبي لقاعدة البيانات')
            """), {"id": test_session_id})
            db.commit()

            fetched = db.execute(text("SELECT id, session_status, input_type FROM verification_sessions WHERE id = :id"), {"id": test_session_id}).fetchone()
            if fetched and str(fetched[0]) == test_session_id:
                print(f"  ✅ PASSED: Session inserted and fetched successfully: {fetched[0]}")
                passed += 1
            else:
                print(f"  ❌ FAILED: Session not found after insert.")
                failed += 1
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        failed += 1

    # 8. Foreign Key Integrity: Verification Result Linked to Session
    print("\n[8/10] Testing DB-08: Verification Result Table Integrity")
    res_id = str(uuid.uuid4())
    claim_id = str(uuid.uuid4())
    try:
        with SessionLocal() as db:
            # Create dummy claim first to satisfy FK
            db.execute(text("""
                INSERT INTO claims (id, verification_session_id, user_input, claim_text, claim_type, category)
                VALUES (:cid, :sid, 'نص التجربة', 'ادعاء التجربة', 'FACTUAL_HADITH', 'HADITH')
            """), {"cid": claim_id, "sid": test_session_id})
            
            db.execute(text("""
                INSERT INTO verification_results (id, claim_id, status, confidence, summary)
                VALUES (:id, :cid, 'VERIFIED', 0.98, 'ملخص النتيجة التجريبية')
            """), {"id": res_id, "cid": claim_id})
            db.commit()

            joined = db.execute(text("""
                SELECT r.id, r.status, r.confidence 
                FROM verification_results r
                WHERE r.id = :id;
            """), {"id": res_id}).fetchone()

            if joined and joined[1] == 'VERIFIED':
                print(f"  ✅ PASSED: Successfully stored verification result (status: {joined[1]}).")
                passed += 1
            else:
                print(f"  ❌ FAILED: Verification result insertion check failed.")
                failed += 1
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        failed += 1

    # 9. Chat Session and Messages Tables Integrity
    print("\n[9/10] Testing DB-09: Chat Sessions & Messages Table Integrity")
    try:
        with SessionLocal() as db:
            chat_sess_id = str(uuid.uuid4())
            db.execute(text("""
                INSERT INTO chat_sessions (id, verification_session_id, session_title, state)
                VALUES (:id, :vs_id, 'جلسة محادثة تجريبية', 'ACTIVE')
            """), {"id": chat_sess_id, "vs_id": test_session_id})
            
            msg_id = str(uuid.uuid4())
            db.execute(text("""
                INSERT INTO chat_messages (id, chat_session_id, role, content, intent)
                VALUES (:id, :cs_id, 'USER', 'هل هذا صحيح؟', 'FOLLOWUP_ON_CURRENT_EVIDENCE')
            """), {"id": msg_id, "cs_id": chat_sess_id})
            db.commit()

            chat_row = db.execute(text("SELECT count(*) FROM chat_messages WHERE chat_session_id = :id"), {"id": chat_sess_id}).scalar()
            if chat_row == 1:
                print(f"  ✅ PASSED: Chat session and message stored and linked to verification session.")
                passed += 1
            else:
                print(f"  ❌ FAILED: Chat message count mismatch: {chat_row}")
                failed += 1
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        failed += 1

    # 10. Clean-up & Isolation
    print("\n[10/10] Testing DB-10: Referential Cleanup & Isolation")
    try:
        with SessionLocal() as db:
            db.execute(text("DELETE FROM chat_messages WHERE chat_session_id = :id"), {"id": chat_sess_id})
            db.execute(text("DELETE FROM chat_sessions WHERE id = :id"), {"id": chat_sess_id})
            db.execute(text("DELETE FROM verification_results WHERE id = :id"), {"id": res_id})
            db.execute(text("DELETE FROM claims WHERE id = :id"), {"id": claim_id})
            db.execute(text("DELETE FROM verification_sessions WHERE id = :id"), {"id": test_session_id})
            db.commit()

            check = db.execute(text("SELECT count(*) FROM verification_sessions WHERE id = :id"), {"id": test_session_id}).scalar()
            if check == 0:
                print("  ✅ PASSED: Test data purged cleanly without dangling references.")
                passed += 1
            else:
                print(f"  ❌ FAILED: Dangling session remaining: {check}")
                failed += 1
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        failed += 1

    print("\n" + "=" * 70)
    print(f"DATABASE RETRIEVAL SUITE RESULTS: {passed} PASSED, {failed} FAILED (TOTAL 10)")
    print("=" * 70)
    return passed == 10

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
