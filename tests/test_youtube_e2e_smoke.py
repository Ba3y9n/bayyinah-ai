"""
Bayyinah AI - Real YouTube E2E Smoke Test (Phase 4)
Executes a real request against /api/verify/url with a live YouTube URL.
"""

import unittest
from fastapi.testclient import TestClient
from backend.app.main import app

class TestRealYouTubeE2ESmoke(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_real_youtube_url_verification(self):
        # Real public YouTube URL
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        response = self.client.post(
            "/api/verify/url",
            json={"url": test_url}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data["input_type"], "URL")
        self.assertIn("media_metadata", data)
        media_meta = data["media_metadata"]
        self.assertEqual(media_meta.get("provenance_type"), "USER_SOCIAL_CONTENT")
        self.assertEqual(media_meta.get("platform"), "YOUTUBE")
        self.assertEqual(media_meta.get("video_id"), "dQw4w9WgXcQ")
        self.assertEqual(media_meta.get("canonical_url"), "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
        # Verify evidence items are present and Evidence Gate active
        self.assertIn("evidence", data)
        self.assertIn("status", data)

if __name__ == "__main__":
    unittest.main()
