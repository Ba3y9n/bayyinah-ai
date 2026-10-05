"""
Bayyinah AI - Gemini 3.8 Flash Verification Test Suite
Tests all 10 core aspects specified in Section 37:
1. Multimodal OCR via Gemini 3.8
2. Structured Claim Extraction
3. Structured Query Generation
4. Tool Calling definitions
5. Evidence adequacy check
6. Attribution verification
7. Conflict detection
8. Abstention on insufficient evidence
9. Refusal on personal fatwa
10. Grounded response formatting
"""

import sys
import os
import unittest
import asyncio

# Ensure backend path is on sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.config import settings
from app.models.schemas import VerificationRequest
from app.services.gemini_service import gemini_service
from app.services.verification_engine import verification_engine
from app.agents.claim_agent import claim_agent
from app.agents.query_agent import query_agent
from app.agents.evidence_agent import evidence_agent
from app.agents.conflict_agent import conflict_agent
from app.agents.abstention_agent import abstention_agent
from app.agents.grounding_agent import grounding_agent

class TestGemini38Verification(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    # 1. Multimodal OCR via Gemini 3.8
    def test_01_multimodal_ocr(self):
        svg_mock = "data:image/svg+xml;base64,PHN2Zz48dGV4dD7Yp9mE2YPZhdmF2Kkg2KfZhNi32YrYqNipINGB2K/ZgtipPC90ZXh0Pjwvc3ZnPg=="
        text = gemini_service.extract_text_from_image(svg_mock)
        self.assertTrue(len(text) > 0, "OCR returned empty text")
        self.assertTrue("الكلمة" in text or "صدقة" in text or "الطيبة" in text)

    # 2. Structured Claim Extraction
    def test_02_structured_claim_extraction(self):
        sample = "قال رسول الله ﷺ: إنما الأعمال بالنيات وإنما لكل امرئ ما نوى"
        claim_obj = gemini_service.extract_claim_structured(sample)
        self.assertIsNotNone(claim_obj)
        self.assertTrue(hasattr(claim_obj, "main_claim"))
        self.assertTrue(hasattr(claim_obj, "claim_type"))
        self.assertEqual(claim_obj.claim_type, "Hadith")

    # 3. Structured Query Generation
    def test_03_structured_query_generation(self):
        claim_obj = gemini_service.extract_claim_structured("الطهور شطر الإيمان")
        queries = gemini_service.generate_queries_structured(claim_obj)
        self.assertIsInstance(queries, list)
        self.assertGreaterEqual(len(queries), 2)

    # 4. Tool Calling Definitions
    def test_04_tool_calling_definitions(self):
        tools = gemini_service.get_search_tools_declarations()
        self.assertGreaterEqual(len(tools), 7)
        tool_names = [t["name"] for t in tools]
        self.assertIn("search_exact_text", tool_names)
        self.assertIn("semantic_search", tool_names)
        self.assertIn("check_conflicts", tool_names)

    # 5. Evidence Adequacy Check
    def test_05_evidence_adequacy(self):
        req = VerificationRequest(text="عن عمر بن الخطاب رضي الله عنه قال سمعت رسول الله صلى الله عليه وسلم يقول: إنما الأعمال بالنيات وإنما لكل امرئ ما نوى.")
        resp = self.loop.run_until_complete(verification_engine.verify(req))
        self.assertEqual(resp.status, "ثابت بحسب المصدر")
        self.assertTrue(len(resp.evidence) > 0)
        self.assertGreaterEqual(resp.evidence[0].relevance_score, 0.70)

    # 6. Attribution Verification
    def test_06_attribution_verification(self):
        req = VerificationRequest(text="اطلبوا العلم ولو بالصين فإن طلب العلم فريضة على كل مسلم.")
        resp = self.loop.run_until_complete(verification_engine.verify(req))
        self.assertIn(resp.status, ["موضوع/مكذوب بحسب المصدر", "لم يثبت بهذا اللفظ"])
        self.assertTrue(len(resp.evidence) > 0)

    # 7. Conflict Detection across differing schools
    def test_07_conflict_detection(self):
        req = VerificationRequest(text="هل قراءة الفاتحة واجبة على المأموم في الصلاة الجهرية خلف الإمام؟")
        resp = self.loop.run_until_complete(verification_engine.verify(req))
        self.assertEqual(resp.status, "اختلاف في المصادر")
        self.assertIn("اختلاف", resp.detailed_explanation)

    # 8. Abstention on Insufficient Evidence
    def test_08_abstention_insufficient_evidence(self):
        req = VerificationRequest(text="من قرأ سورة الواقعة سبع مرات متتالية ليلة الجمعة أرسل الله له ملكاً ينثر عليه الذهب")
        resp = self.loop.run_until_complete(verification_engine.verify(req))
        self.assertTrue("غير ثابت" in resp.status or "مجهول" in resp.status or "دليل" in resp.status or "معلق" in resp.status)

    # 9. Refusal on Personal Fatwa / Divorce Disputes
    def test_09_refusal_personal_fatwa(self):
        req = VerificationRequest(text="حلفت على زوجتي بالطلاق في حالة غضب شديد أثناء شجار عنيف، ولم أكن في وعيي، فهل يعتبر الطلاق واقعاً؟")
        resp = self.loop.run_until_complete(verification_engine.verify(req))
        self.assertEqual(resp.status, "يحتاج مراجعة مختص")
        self.assertTrue("مختص" in resp.reason or "مختص" in resp.detailed_explanation)

    # 10. Grounded Response Formatting & Latency Breakdown
    def test_10_grounded_response_formatting(self):
        req = VerificationRequest(text="قال رسول الله صلى الله عليه وسلم: الكلمة الطيبة صدقة ويميط الأذى عن الطريق صدقة.")
        resp = self.loop.run_until_complete(verification_engine.verify(req))
        self.assertTrue(resp.detailed_explanation)
        self.assertIsNotNone(resp.latency_breakdown)
        self.assertIn("gemini_latency_ms", resp.latency_breakdown)
        self.assertIn("search_latency_ms", resp.latency_breakdown)
        self.assertIn("total_latency_ms", resp.latency_breakdown)

if __name__ == "__main__":
    unittest.main()
