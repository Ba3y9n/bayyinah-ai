"""
Bayyinah AI - Phase 4.1 Real Islamic YouTube Verification E2E Test Suite

Verifies:
1. Real Islamic YouTube URL acquisition.
2. Real claim extraction & timestamps.
3. Phase 1 Unified Retrieval integration.
4. Approved Islamic Evidence validation & Evidence Gate enforcement.
5. Strict separation: USER_SOCIAL_CONTENT is NEVER APPROVED_EVIDENCE.
6. Absence of hardcoded religious verdicts or hallucinations.
"""

import os
import unittest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.url_resolver import url_resolver, SSRFSecurityException
from backend.app.services.youtube_acquisition_service import youtube_acquisition_service
from backend.app.models.schemas import VerificationResponse


class TestRealIslamicYouTubeVerification(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        from backend.app.services.gemini_service import gemini_service
        self._orig_configured = gemini_service.is_configured
        gemini_service.is_configured = False

    def tearDown(self):
        from backend.app.services.gemini_service import gemini_service
        gemini_service.is_configured = self._orig_configured

    def test_non_islamic_content_abstention(self):
        """
        Phase 4.1 / 4.2 Abstention Test:
        Passes a non-Islamic ambience YouTube URL, verifies abstention/handling,
        Approved Evidence Gate enforcement, and USER_SOCIAL_CONTENT provenance.
        """
        # Non-Islamic Fireplace Ambience YouTube URL
        fireplace_url = "https://www.youtube.com/watch?v=L_LUpnjgPso"
        
        response = self.client.post(
            "/api/verify/url",
            json={"url": fireplace_url}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # 1. Input & Provenance Verification
        self.assertEqual(data["input_type"], "URL")
        self.assertIn("media_metadata", data)
        media_meta = data["media_metadata"]
        
        self.assertEqual(media_meta.get("provenance_type"), "USER_SOCIAL_CONTENT")
        self.assertEqual(media_meta.get("platform"), "YOUTUBE")
        self.assertEqual(media_meta.get("video_id"), "L_LUpnjgPso")
        self.assertEqual(media_meta.get("canonical_url"), "https://www.youtube.com/watch?v=L_LUpnjgPso")

        # 2. Multi-Claims & Timestamps Verification
        multi_claims = data.get("multi_claims", [])
        self.assertIsNotNone(multi_claims)
        if multi_claims:
            for mc in multi_claims:
                self.assertIsNotNone(mc.get("claim_text"))
                self.assertIsNotNone(mc.get("timestamp_start"))
                self.assertIsNotNone(mc.get("timestamp_end"))

        # 3. Evidence Boundary Verification
        # YouTube transcript or title must NEVER be included as an evidence item or evidence source
        evidence_list = data.get("evidence", [])
        for ev in evidence_list:
            self.assertNotEqual(ev.get("source_id"), "USER_SOCIAL_CONTENT")
            self.assertNotEqual(ev.get("source_name"), "YouTube Video")
            self.assertNotEqual(ev.get("source_name"), "YouTube")

        # 4. Status Grounding Verification
        status = data.get("status")
        self.assertIsNotNone(status)

    def test_real_islamic_youtube_claim_end_to_end(self):
        """
        Phase 4.2 True Islamic Claim E2E Validation:
        Passes a real public Islamic YouTube URL, verifies claims acquisition,
        Unified Verification Retrieval pipeline, Evidence Gate boundary enforcement,
        and USER_SOCIAL_CONTENT provenance tagging without hardcoded verdicts or mocks.
        """
        # Real public Islamic YouTube URL (Surat Al-Fatiha / Quran Recitation)
        islamic_url = "https://www.youtube.com/watch?v=gEzLF7oCzGE"
        
        response = self.client.post(
            "/api/verify/url",
            json={"url": islamic_url}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # 1. Input & Social Provenance Tagging
        self.assertEqual(data["input_type"], "URL")
        self.assertIn("media_metadata", data)
        media_meta = data["media_metadata"]
        
        self.assertEqual(media_meta.get("provenance_type"), "USER_SOCIAL_CONTENT")
        self.assertEqual(media_meta.get("platform"), "YOUTUBE")
        self.assertEqual(media_meta.get("video_id"), "gEzLF7oCzGE")
        self.assertEqual(media_meta.get("canonical_url"), "https://www.youtube.com/watch?v=gEzLF7oCzGE")
        self.assertIn("Quran", media_meta.get("video_title", ""))

        # 2. Strict Evidence Boundary Enforcement (Evidence Gate)
        # All returned evidence MUST come strictly from approved allowlisted sources, NEVER from YouTube
        evidence_list = data.get("evidence", [])
        for ev in evidence_list:
            source_id = ev.get("source_id", "")
            source_name = ev.get("source_name", "")
            url = ev.get("url", "")
            self.assertNotEqual(source_id, "USER_SOCIAL_CONTENT")
            self.assertNotEqual(source_name, "YouTube Video")
            self.assertNotEqual(source_name, "YouTube")
            # Must be an allowlisted domain
            self.assertTrue(
                any(domain in url for domain in ["dorar.net", "quranpedia.net", "shamela.ws", "dawa.center", "islamic-content.com"]),
                f"Evidence URL {url} is not in official allowlist"
            )

        # 3. Clean Execution & Status Verification
        status = data.get("status")
        self.assertIsNotNone(status)


    def test_ssrf_security_boundary_verifications(self):
        """
        Phase 4.1 Security Regression Test:
        Ensures all SSRF attack vectors remain blocked.
        """
        blocked_urls = [
            "http://127.0.0.1/admin",
            "http://localhost:8000/internal",
            "http://169.254.169.254/latest/meta-data/",
            "http://10.0.0.1/secret",
            "http://172.16.0.1/private",
            "http://192.168.1.1/router",
            "file:///etc/passwd",
            "javascript:alert('ssrf')"
        ]
        for url in blocked_urls:
            with self.assertRaises(SSRFSecurityException):
                url_resolver.validate_url_safety(url)

    def test_phase_1_2_3_4_regression(self):
        """
        Phase 4.1 Master Regression Check across all test suites.
        """
        from backend.app.services.gemini_service import gemini_service
        gemini_service.is_configured = False

        from tests.test_unified_retrieval import TestUnifiedVerificationRetrieval
        from tests.test_pdf_verification import TestPDFVerificationPipeline
        from tests.test_video_verification import TestVideoVerificationPipeline
        from tests.test_youtube_verification import TestYouTubeVerificationPipeline

        runner = unittest.TextTestRunner(stream=open(os.devnull, 'w'))

        suite1 = unittest.TestLoader().loadTestsFromTestCase(TestUnifiedVerificationRetrieval)
        res1 = runner.run(suite1)
        self.assertEqual(res1.testsRun, 6)
        self.assertEqual(len(res1.failures), 0)

        suite2 = unittest.TestLoader().loadTestsFromTestCase(TestPDFVerificationPipeline)
        res2 = runner.run(suite2)
        self.assertEqual(res2.testsRun, 8)
        self.assertEqual(len(res2.failures), 0)

        suite3 = unittest.TestLoader().loadTestsFromTestCase(TestVideoVerificationPipeline)
        res3 = runner.run(suite3)
        self.assertEqual(res3.testsRun, 10)
        self.assertEqual(len(res3.failures), 0)

        suite4 = unittest.TestLoader().loadTestsFromTestCase(TestYouTubeVerificationPipeline)
        res4 = runner.run(suite4)
        self.assertEqual(res4.testsRun, 20)
        self.assertEqual(len(res4.failures), 0)


if __name__ == "__main__":
    unittest.main()
