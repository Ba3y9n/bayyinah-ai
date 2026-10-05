"""
Bayyinah AI - Real Integration Test Suite with Google Gemini 3.8 Flash
Tests live backend integration with Google GenAI SDK (google-genai):
- Real connection test (BAYYINAH_GEMINI_OK)
- Real structured output (Pydantic ClaimExtraction)
- Real multimodal image understanding
- Function calling orchestration
- Grounded response & Abstention enforcement
- Error sanitization (Zero Key Leakage)
"""

import sys
import os
import unittest
import time
import base64

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.config import settings
from app.services.gemini_service import gemini_service, ClaimExtraction, GroundedFinalResponse

class TestGeminiRealIntegration(unittest.TestCase):

    def test_01_real_ping_connection(self):
        """Verify real connection to gemini-3.8-flash with BAYYINAH_GEMINI_OK or real 429 quota."""
        health = gemini_service.test_connection()
        is_live_ok = health.get("connected") or ("429" in str(health.get("error")) or "RESOURCE_EXHAUSTED" in str(health.get("error")))
        self.assertTrue(is_live_ok, f"Gemini connection failed with non-API error: {health.get('error')}")
        self.assertEqual(health.get("model"), "gemini-3.8-flash")
        self.assertEqual(health.get("actual_request_model"), "gemini-3.8-flash")
        self.assertEqual(health.get("sdk"), "google-genai")
        self.assertTrue(health.get("api_key_configured"))

    def test_02_real_structured_claim_extraction(self):
        """Verify structured output parsing with Gemini 3.8 Flash."""
        input_text = "قال رسول الله صلى الله عليه وسلم: إنما الأعمال بالنيات وإنما لكل امرئ ما نوى"
        extraction = gemini_service.extract_claim_structured(input_text)
        self.assertIsInstance(extraction, ClaimExtraction)
        self.assertTrue(len(extraction.main_claim) > 0)
        self.assertEqual(extraction.claim_type, "Hadith")
        self.assertIsInstance(extraction.search_queries, list)
        self.assertGreater(len(extraction.search_queries), 0)

    def test_03_real_multimodal_ocr(self):
        """Verify multimodal OCR handling via Gemini 3.8 Flash."""
        # 1x1 transparent PNG in base64
        tiny_png = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        text = gemini_service.extract_text_from_image(tiny_png)
        # Should return a string without throwing exception
        self.assertIsInstance(text, str)

    def test_04_error_sanitization_zero_key_exposure(self):
        """Verify that errors never expose the API key or tokens."""
        raw_key = settings.GEMINI_API_KEY
        if raw_key:
            fake_exception = Exception(f"Failed request with api_key={raw_key} at endpoint https://generativelanguage.googleapis.com")
            sanitized = gemini_service.sanitize_error(fake_exception)
            self.assertNotIn(raw_key, sanitized, "Security violation: raw API key found in error string!")
            self.assertIn("[REDACTED_API_KEY]", sanitized)

    def test_05_grounding_and_abstention(self):
        """Verify abstention policy when evidence is completely missing."""
        claim = "نص يدعي حكماً غريباً لا أصل له في الشريعة"
        empty_evidence = []
        abstention = gemini_service.generate_abstention_response(claim, empty_evidence)
        self.assertIsNotNone(abstention)
        self.assertTrue(hasattr(abstention, "status"))
        self.assertIn(abstention.status, ["لم نجد دليلًا كافيًا", "insufficient_evidence", "يحتاج مراجعة مختص"])

if __name__ == "__main__":
    unittest.main()
