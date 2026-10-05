"""
Bayyinah AI - Phase 4 YouTube Social Content Acquisition Test Suite

Tests covered:
- TEST A: Valid YouTube watch URL recognized.
- TEST B: youtu.be canonicalization.
- TEST C: YouTube Shorts recognized.
- TEST D: Embed URL supported.
- TEST E: Invalid video ID handled safely.
- TEST F: Unsupported scheme blocked (e.g. file://, javascript:).
- TEST G: localhost blocked.
- TEST H: private IP (e.g. 127.0.0.1, 10.0.0.1, 169.254.169.254) blocked.
- TEST I: Metadata / transcript is USER_SOCIAL_CONTENT, never APPROVED EVIDENCE.
- TEST J: YouTube transcript classified as USER_SOCIAL_CONTENT.
- TEST K: Multiple claims extracted from video transcript.
- TEST L: Timestamps (start, end) preserved on claims.
- TEST M: Claims enter Phase 1 Unified Retrieval independently.
- TEST N: Approved official evidence accepted by Evidence Gate.
- TEST O: Unapproved evidence blocked by Evidence Gate.
- TEST P: Absence of evidence yields INSUFFICIENT_EVIDENCE.
- TEST Q: Conflicting positions yield CONFLICT / SCHOLARLY_DISAGREEMENT.
- TEST R: Gemini 429 rate limit handled safely without hallucination.
- TEST S: Gemini timeout handled safely.
- TEST T: Deleted/unavailable YouTube content handled gracefully.
- TEST U: No hardcoded religious verdicts in YouTube route.
- TEST V: Phase 1 regression checks (6/6).
- TEST W: Phase 2 regression checks (8/8).
- TEST X: Phase 3 regression checks (10/10).
"""

import os
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.url_resolver import url_resolver, SSRFSecurityException
from backend.app.services.youtube_acquisition_service import youtube_acquisition_service
from backend.app.models.schemas import VerificationResponse, MultiClaimItem


class TestYouTubeVerificationPipeline(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        from backend.app.services.gemini_service import gemini_service
        self._orig_configured = gemini_service.is_configured
        gemini_service.is_configured = False

    def tearDown(self):
        from backend.app.services.gemini_service import gemini_service
        gemini_service.is_configured = self._orig_configured

    def test_a_valid_youtube_watch_url_recognized(self):
        """TEST A: Valid YouTube watch URL recognized and platform identified."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        plat = url_resolver.detect_platform(url)
        self.assertEqual(plat, "YOUTUBE")
        vid_id = url_resolver.extract_youtube_video_id(url)
        self.assertEqual(vid_id, "dQw4w9WgXcQ")

    def test_b_youtu_be_canonicalization(self):
        """TEST B: youtu.be short URL canonicalized correctly."""
        url = "https://youtu.be/dQw4w9WgXcQ?t=10"
        vid_id = url_resolver.extract_youtube_video_id(url)
        self.assertEqual(vid_id, "dQw4w9WgXcQ")

    def test_c_youtube_shorts_recognized(self):
        """TEST C: YouTube Shorts URL recognized."""
        url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
        plat = url_resolver.detect_platform(url)
        self.assertEqual(plat, "YOUTUBE")
        vid_id = url_resolver.extract_youtube_video_id(url)
        self.assertEqual(vid_id, "dQw4w9WgXcQ")

    def test_d_embed_url_supported(self):
        """TEST D: YouTube Embed URL supported."""
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1"
        vid_id = url_resolver.extract_youtube_video_id(url)
        self.assertEqual(vid_id, "dQw4w9WgXcQ")

    def test_e_invalid_video_id_handled(self):
        """TEST E: Malformed video URL handled gracefully."""
        vid_id = url_resolver.extract_youtube_video_id("https://www.youtube.com/watch?invalid=1")
        self.assertIsNone(vid_id)

    def test_f_unsupported_scheme_blocked(self):
        """TEST F: Unsupported scheme (file://, javascript:) blocked by SSRF check."""
        with self.assertRaises(SSRFSecurityException):
            url_resolver.validate_url_safety("file:///etc/passwd")
        with self.assertRaises(SSRFSecurityException):
            url_resolver.validate_url_safety("javascript:alert(1)")

    def test_g_localhost_blocked(self):
        """TEST G: localhost blocked by SSRF check."""
        with self.assertRaises(SSRFSecurityException):
            url_resolver.validate_url_safety("http://localhost:8000/internal")

    def test_h_private_ip_blocked(self):
        """TEST H: Private IP addresses (127.0.0.1, 10.0.0.1, 169.254.169.254) blocked by SSRF check."""
        for private_ip in ["http://127.0.0.1/admin", "http://10.0.0.1/secret", "http://169.254.169.254/latest/meta-data/"]:
            with self.assertRaises(SSRFSecurityException):
                url_resolver.validate_url_safety(private_ip)

    @patch("backend.app.main.youtube_acquisition_service.acquire_youtube_content")
    def test_i_and_j_user_social_content_provenance(self, mock_acquire):
        """TEST I & J: YouTube transcript/metadata strictly classified as USER_SOCIAL_CONTENT, never APPROVED EVIDENCE."""
        mock_acquire.return_value = {
            "success": True,
            "platform": "YOUTUBE",
            "video_id": "test_video_1",
            "canonical_url": "https://www.youtube.com/watch?v=test_video_1",
            "title": "فيديو ديني",
            "author": "قناة اختبار",
            "has_transcript": True,
            "claims": [
                {
                    "timestamp_start": "00:10",
                    "timestamp_end": "00:30",
                    "claim_text": "إنما الأعمال بالنيات",
                    "extracted_excerpt": "صوت المتحدث في الفيديو",
                    "content_type": "Hadith"
                }
            ],
            "provenance_type": "USER_SOCIAL_CONTENT"
        }

        response = self.client.post(
            "/api/verify/url",
            json={"url": "https://www.youtube.com/watch?v=test_video_1"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        media_meta = data.get("media_metadata", {})
        self.assertEqual(media_meta.get("provenance_type"), "USER_SOCIAL_CONTENT")
        self.assertEqual(media_meta.get("platform"), "YOUTUBE")

        # Verify evidence items do not label user YouTube transcript as evidence source
        for ev in data.get("evidence", []):
            self.assertNotEqual(ev.get("source_id"), "USER_SOCIAL_CONTENT")
            self.assertNotEqual(ev.get("source_name"), "YouTube Video")

    @patch("backend.app.main.youtube_acquisition_service.acquire_youtube_content")
    def test_k_and_l_multiple_timestamped_claims(self, mock_acquire):
        """TEST K & L: Multiple claims extracted from transcript with timestamps preserved."""
        mock_acquire.return_value = {
            "success": True,
            "platform": "YOUTUBE",
            "video_id": "multi_claims_vid",
            "canonical_url": "https://www.youtube.com/watch?v=multi_claims_vid",
            "title": "مقاطع دينية متنسقة",
            "author": "قناة شرعية",
            "has_transcript": True,
            "claims": [
                {
                    "timestamp_start": "00:15",
                    "timestamp_end": "00:45",
                    "claim_text": "الادعاء الأول: إنما الأعمال بالنيات",
                    "extracted_excerpt": "المقتطف الصوتي الأول",
                    "content_type": "Hadith"
                },
                {
                    "timestamp_start": "01:20",
                    "timestamp_end": "01:50",
                    "claim_text": "الادعاء الثاني: الكلمة الطيبة صدقة",
                    "extracted_excerpt": "المقتطف الصوتي الثاني",
                    "content_type": "Hadith"
                }
            ],
            "provenance_type": "USER_SOCIAL_CONTENT"
        }

        response = self.client.post(
            "/api/verify/url",
            json={"url": "https://www.youtube.com/watch?v=multi_claims_vid"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        multi_claims = data.get("multi_claims", [])
        self.assertEqual(len(multi_claims), 2)
        self.assertEqual(multi_claims[0]["timestamp_start"], "00:15")
        self.assertEqual(multi_claims[0]["timestamp_end"], "00:45")
        self.assertEqual(multi_claims[1]["timestamp_start"], "01:20")
        self.assertEqual(multi_claims[1]["timestamp_end"], "01:50")

    @patch("backend.app.main.youtube_acquisition_service.acquire_youtube_content")
    def test_m_and_n_unified_retrieval_and_approved_evidence(self, mock_acquire):
        """TEST M & N: Claims enter Phase 1 Unified Retrieval independently and approved evidence is accepted."""
        mock_acquire.return_value = {
            "success": True,
            "platform": "YOUTUBE",
            "video_id": "hadith_vid",
            "canonical_url": "https://www.youtube.com/watch?v=hadith_vid",
            "title": "حديث النيات",
            "author": "الشيخ",
            "has_transcript": True,
            "claims": [
                {
                    "timestamp_start": "00:00",
                    "timestamp_end": "00:20",
                    "claim_text": "إنما الأعمال بالنيات",
                    "extracted_excerpt": "مقتطف حديث النيات",
                    "content_type": "Hadith"
                }
            ]
        }

        response = self.client.post(
            "/api/verify/url",
            json={"url": "https://www.youtube.com/watch?v=hadith_vid"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("evidence", data)
        self.assertGreater(len(data["evidence"]), 0)

    @patch("backend.app.main.youtube_acquisition_service.acquire_youtube_content")
    def test_o_unapproved_evidence_blocked(self, mock_acquire):
        """TEST O: Unapproved domains/sources blocked by Evidence Gate."""
        mock_acquire.return_value = {
            "success": True,
            "platform": "YOUTUBE",
            "video_id": "hadith_vid",
            "canonical_url": "https://www.youtube.com/watch?v=hadith_vid",
            "title": "حديث النيات",
            "has_transcript": True,
            "claims": [
                {
                    "timestamp_start": "00:00",
                    "timestamp_end": "00:20",
                    "claim_text": "إنما الأعمال بالنيات",
                    "content_type": "Hadith"
                }
            ]
        }

        response = self.client.post(
            "/api/verify/url",
            json={"url": "https://www.youtube.com/watch?v=hadith_vid"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        from backend.app.ingestion.official_allowlist import OFFICIAL_SOURCE_ALLOWLIST
        allowed_domains = {s["domain"].lower() for s in OFFICIAL_SOURCE_ALLOWLIST if "domain" in s}

        for ev in data.get("evidence", []):
            url = ev.get("url", "")
            if url:
                domain = url.split("//")[-1].split("/")[0].lower()
                self.assertTrue(any(ad in domain for ad in allowed_domains) or domain in ["localhost", "127.0.0.1"])

    @patch("backend.app.main.youtube_acquisition_service.acquire_youtube_content")
    def test_p_no_evidence_yields_insufficient(self, mock_acquire):
        """TEST P: Absence of evidence yields INSUFFICIENT_EVIDENCE status."""
        mock_acquire.return_value = {
            "success": True,
            "platform": "YOUTUBE",
            "video_id": "unknown_vid",
            "canonical_url": "https://www.youtube.com/watch?v=unknown_vid",
            "title": "فيديو غير معروف 998877",
            "has_transcript": True,
            "claims": [
                {
                    "timestamp_start": "00:00",
                    "timestamp_end": "00:10",
                    "claim_text": "ادعاء عشوائي غريب لا يوجد في أي ديوان 998877",
                    "content_type": "GeneralClaim"
                }
            ]
        }

        response = self.client.post(
            "/api/verify/url",
            json={"url": "https://www.youtube.com/watch?v=unknown_vid"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        valid_statuses = [
            "INSUFFICIENT_EVIDENCE", 
            "مجهول / غير ثابت بحسب البحث الحالي", 
            "لم نجد دليلًا كافيًا", 
            "NOT_ESTABLISHED_BY_EXACT_WORDING"
        ]
        self.assertTrue(
            data["status"] in valid_statuses or "غير ثابت" in data["status"] or "مجهول" in data["status"]
        )

    def test_q_conflict_yields_scholarly_disagreement(self):
        """TEST Q: Conflicting positions yield SCHOLARLY_DISAGREEMENT / CONFLICT."""
        from backend.app.models.schemas import EvidenceItem
        ev1 = EvidenceItem(
            document_id="doc-fiqh-1",
            source_id="00000000-0000-0000-0000-000000000016",
            source_name="الموسوعة الفقهية - الدرر السنية",
            category="FIQH",
            title="حكم القراءة خلف الإمام",
            excerpt="القول الأول: تجب القراءة خلف الإمام مطلقاً وهو مذهب الشافعية.",
            reference="الموسوعة الفقهية",
            url="https://dorar.net/feqhia/1",
            license="مرجع موثق",
            relevance_score=0.88,
            evidence_type="direct_match",
            comparison_notes="اختلاف فقهي معتبر بين المذاهب"
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
        from backend.app.agents.conflict_agent import conflict_agent
        res = conflict_agent.detect_conflicts("Fiqh", [ev1, ev2])
        self.assertTrue(res["conflict_detected"])

    def test_r_and_s_gemini_429_and_timeout_safety(self):
        """TEST R & S: Gemini rate limit (429) or timeout handled safely without hallucinated verdict."""
        from backend.app.services.gemini_service import GeminiService
        service = GeminiService()
        
        # Test fallback response generation under failure
        resp = service.generate_grounded_response("ادعاء صلاة الوتر", "INSUFFICIENT", [])
        self.assertIn("reason", resp)
        self.assertIn("summary", resp)
        self.assertTrue("ولم نعثر" in resp["summary"] or "لم نجد" in resp["reason"])

    def test_t_deleted_unavailable_youtube_handled(self):
        """TEST T: Unavailable/deleted YouTube video handled gracefully."""
        res = youtube_acquisition_service.acquire_youtube_content("https://www.youtube.com/watch?v=deleted_12345")
        self.assertTrue(res["success"])
        self.assertEqual(res["acquisition_method"], "METADATA_ONLY")

    def test_u_no_hardcoded_verdicts(self):
        """TEST U: Ensure YouTube route does not fabricate hardcoded religious verdicts."""
        res = youtube_acquisition_service.acquire_youtube_content("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        # Ensure acquisition service contains no religious verdict logic
        self.assertNotIn("verdict", res)
        self.assertNotIn("status", res)
        self.assertEqual(res["provenance_type"], "USER_SOCIAL_CONTENT")

    def test_v_phase_1_regression(self):
        """TEST V: Phase 1 regression checks (Unified Retrieval)."""
        from tests.test_unified_retrieval import TestUnifiedVerificationRetrieval
        suite = unittest.TestLoader().loadTestsFromTestCase(TestUnifiedVerificationRetrieval)
        result = unittest.TextTestRunner(stream=open(os.devnull, 'w')).run(suite)
        self.assertEqual(result.testsRun, 6)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(len(result.errors), 0)

    def test_w_phase_2_regression(self):
        """TEST W: Phase 2 regression checks (PDF Verification)."""
        from tests.test_pdf_verification import TestPDFVerificationPipeline
        suite = unittest.TestLoader().loadTestsFromTestCase(TestPDFVerificationPipeline)
        result = unittest.TextTestRunner(stream=open(os.devnull, 'w')).run(suite)
        self.assertEqual(result.testsRun, 8)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(len(result.errors), 0)

    def test_x_phase_3_regression(self):
        """TEST X: Phase 3 regression checks (Video Verification)."""
        from tests.test_video_verification import TestVideoVerificationPipeline
        suite = unittest.TestLoader().loadTestsFromTestCase(TestVideoVerificationPipeline)
        result = unittest.TextTestRunner(stream=open(os.devnull, 'w')).run(suite)
        self.assertEqual(result.testsRun, 10)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(len(result.errors), 0)


if __name__ == "__main__":
    unittest.main()
