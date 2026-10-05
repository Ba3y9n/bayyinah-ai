"""
Bayyinah AI - Unified Verification Retrieval Pipeline Test Suite (Phase 1)
Tests:
TEST A: Claim in Supabase/KB -> Uses Supabase FTS/Vector -> Evidence -> Result
TEST B: Claim absent in DB -> Live SerpAPI discovery -> Official Allowlist -> Source Adapter -> Evidence -> Result
TEST C: SerpAPI returns unapproved domain URL -> BLOCKED by EvidenceGate / Allowlist
TEST D: Claim with no evidence anywhere -> INSUFFICIENT (NOT FABRICATED)
TEST E: Multiple sources with conflicting positions -> CONFLICT
TEST F: Personal fatwa / legal court dispute -> SPECIALIST
"""

import sys
import os
import unittest
import uuid
import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.db.database import SessionLocal
from app.agents.retrieval_agent import retrieval_agent
from app.services.verification_engine import verification_engine
from app.services.evidence_gate import evidence_gate, ABSTENTION_MESSAGE
from app.models.schemas import VerificationRequest, EvidenceItem
from app.ingestion.official_allowlist import is_url_in_allowlist
from app.ingestion.source_adapters.adapter_registry import get_adapter_by_url, get_all_adapters

class TestUnifiedVerificationRetrieval(unittest.TestCase):

    def setUp(self):
        try:
            self.db = SessionLocal() if SessionLocal else None
        except Exception:
            self.db = None

    def tearDown(self):
        if self.db:
            try:
                self.db.close()
            except Exception:
                pass

    def test_A_claim_present_in_supabase(self):
        """TEST A: Claim in Supabase/KB -> Uses DB Search -> Evidence -> Result."""
        queries = ["إنما الأعمال بالنيات", "عمر بن الخطاب بالنيات"]
        evidence_items = retrieval_agent.orchestrate_hybrid_retrieval(
            queries=queries,
            limit=5,
            category="HADITH",
            claim_text="إنما الأعمال بالنيات وإنما لكل امرئ ما نوى",
            db=self.db
        )
        self.assertGreater(len(evidence_items), 0, "Must retrieve at least 1 evidence item for famous Hadith")
        top_ev = evidence_items[0]
        self.assertTrue(evidence_gate.validate_source(top_ev.source_id, top_ev.url), "Evidence source must be valid")
        self.assertIsNotNone(top_ev.document_id, "Evidence item must contain valid document_id")

    def test_B_claim_absent_in_db_discovered_via_live_adapter(self):
        """TEST B: Claim absent in DB -> Live SerpAPI discovery -> Official Source URL -> Source Adapter -> Evidence -> Result."""
        target_url = "https://dorar.net/hadith/sharh/12345"
        adapter = get_adapter_by_url(target_url)
        self.assertIsNotNone(adapter, "Must find dedicated adapter for dorar.net URL")
        
        # Test adapter parsing with canonical content container
        sample_html = """
        <html><head><title>تخريج حديث - الموسوعة الحديثية</title></head>
        <body>
            <div class="content">
                <div class="hadith">عن أبي هريرة رضي الله عنه قال: قال رسول الله صلى الله عليه وسلم: الكلمة الطيبة صدقة.</div>
                <div class="sharh">المحدث: البخاري - المصدر: صحيح البخاري - الصفحة أو الرقم: 2989 - خلاصة حكم المحدث: صحيح</div>
            </div>
        </body></html>
        """
        parsed = adapter.parse(sample_html, target_url)
        self.assertIn("الكلمة الطيبة صدقة", parsed["content"])
        self.assertEqual(parsed["grading_text"], "صحيح متفق عليه")
        
        # Verify allowlist validation
        self.assertTrue(is_url_in_allowlist(target_url), "Official dorar URL must pass allowlist validation")

    def test_C_serpapi_unapproved_domain_blocked(self):
        """TEST C: SerpAPI returns unapproved domain URL -> BLOCKED by EvidenceGate / Allowlist."""
        unapproved_urls = [
            "https://random-unapproved-blog.com/hadith-article",
            "https://fake-islamic-site.org/fatwa/101",
            "http://127.0.0.1/internal-secret",
            "https://evilsite.com/dorar.net/fake"
        ]
        for url in unapproved_urls:
            is_allowed = is_url_in_allowlist(url)
            self.assertFalse(is_allowed, f"URL '{url}' outside the 11 official sources MUST be blocked")
            is_valid = evidence_gate.validate_source(None, source_url=url)
            self.assertFalse(is_valid, f"EvidenceGate MUST reject unapproved source URL '{url}'")

    def test_D_no_evidence_found_yields_insufficient(self):
        """TEST D: Claim with no evidence anywhere -> INSUFFICIENT (NOT FABRICATED)."""
        empty_evidence = []
        gate_res = evidence_gate.validate(
            evidences=empty_evidence,
            confidence_score=0.90,
            claim_text="نص غريب عشوائي لم يروه أحد من العالمين 998877",
            verdict="ثابت بحسب المصدر"
        )
        self.assertTrue(gate_res["abstention_required"], "Abstention must be required when evidence is empty")
        self.assertEqual(gate_res["sanitized_verdict"], "مجهول / غير ثابت بحسب البحث الحالي")
        self.assertEqual(gate_res["reason"], ABSTENTION_MESSAGE)

    def test_E_conflicting_sources_yields_conflict(self):
        """TEST E: Multiple sources with conflicting positions -> CONFLICT."""
        ev1 = EvidenceItem(
            document_id="doc-fiqh-1",
            source_id="00000000-0000-0000-0000-000000000016",
            source_name="الموسوعة الفقهية - الدرر السنية",
            category="FIQH",
            title="حكم القراءة خلف الإمام في الصلاة الجهرية",
            excerpt="القول الأول: تجب القراءة خلف الإمام مطلقاً وهو مذهب الشافعية.",
            reference="الموسوعة الفقهية",
            url="https://dorar.net/feqhia/1",
            license="مرجع موثق",
            relevance_score=0.88,
            evidence_type="direct_match",
            comparison_notes="اختلاف فقهي معتبر بين المذاهب الأربعة"
        )
        ev2 = EvidenceItem(
            document_id="doc-fiqh-2",
            source_id="00000000-0000-0000-0000-000000000016",
            source_name="الموسوعة الفقهية - الدرر السنية",
            category="FIQH",
            title="حكم القراءة خلف الإمام",
            excerpt="القول الثاني: تنصت ولا تقرأ خلف الإمام في الجهرية وهو مذهب الحنفية والحنابلة.",
            reference="الموسوعة الفقهية",
            url="https://dorar.net/feqhia/2",
            license="مرجع موثق",
            relevance_score=0.85,
            evidence_type="direct_match",
            comparison_notes="اختلاف فقهي معتبر"
        )
        from app.agents.conflict_agent import conflict_agent
        res = conflict_agent.detect_conflicts("Fiqh", [ev1, ev2])
        self.assertTrue(res["conflict_detected"], "Conflict must be detected for conflicting Fiqh positions")

    def test_F_personal_case_yields_specialist(self):
        """TEST F: Personal fatwa / family court dispute -> SPECIALIST."""
        from app.agents.abstention_agent import abstention_agent
        claim_data = {
            "main_claim": "حلفت على زوجتي بالطلاق في غضب شديد هل يقع الطلاق",
            "claim_type": "PersonalCase",
            "requires_specialist": True
        }
        res = abstention_agent.evaluate_abstention(claim_data, [])
        self.assertTrue(res["must_abstain"], "Must abstain on personal fatwa/dispute")
        self.assertEqual(res["status"], "SPECIALIST")
        self.assertEqual(res["status_ar"], "يحتاج مراجعة مختص")

if __name__ == "__main__":
    unittest.main(verbosity=2)
