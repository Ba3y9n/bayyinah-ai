"""
Bayyinah AI - URL Engine Test Suite (10 Cases)
Tests platform detection, metadata/content extraction, and /api/verify/url pipeline.
"""

import sys
import os
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:8000"

# Import URLResolverService directly for unit tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.services.url_resolver import URLResolverService, SSRFSecurityException

resolver = URLResolverService()

TEST_CASES = [
    # 1. YouTube standard URL
    {
        "id": "URL-01",
        "name": "YouTube standard URL detection & ID extraction",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "expected_platform": "YOUTUBE",
        "expected_vid_id": "dQw4w9WgXcQ"
    },
    # 2. YouTube short URL (youtu.be)
    {
        "id": "URL-02",
        "name": "YouTube short URL detection",
        "url": "https://youtu.be/dQw4w9WgXcQ?si=test1234",
        "expected_platform": "YOUTUBE",
        "expected_vid_id": "dQw4w9WgXcQ"
    },
    # 3. TikTok URL detection
    {
        "id": "URL-03",
        "name": "TikTok URL detection",
        "url": "https://www.tiktok.com/@user/video/7123456789012345678",
        "expected_platform": "TIKTOK"
    },
    # 4. X / Twitter URL detection
    {
        "id": "URL-04",
        "name": "X / Twitter URL detection",
        "url": "https://x.com/islamic_heritage/status/1234567890123456789",
        "expected_platform": "X"
    },
    # 5. Direct Media URL detection (.mp4)
    {
        "id": "URL-05",
        "name": "Direct media detection (.mp4)",
        "url": "https://example.com/videos/hadith_lecture.mp4",
        "expected_platform": "DIRECT_MEDIA"
    },
    # 6. Direct Media URL detection (.jpg)
    {
        "id": "URL-06",
        "name": "Direct media detection (.jpg)",
        "url": "https://example.com/images/fatwa_document.jpg",
        "expected_platform": "DIRECT_MEDIA"
    },
    # 7. Generic Web URL resolution
    {
        "id": "URL-07",
        "name": "Generic Web URL resolution",
        "url": "https://example.com",
        "expected_platform": "GENERIC"
    },
    # 8. Invalid URL scheme blocking
    {
        "id": "URL-08",
        "name": "Invalid URL scheme rejection (ftp://)",
        "url": "ftp://files.example.com/hadith.txt",
        "expect_ssrf_exception": True
    },
    # 9. API Integration: /api/verify/url with YouTube URL
    {
        "id": "URL-09",
        "name": "API Endpoint: POST /api/verify/url (YouTube)",
        "is_api": True,
        "payload": {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
    },
    # 10. API Integration: /api/verify/url with Generic URL
    {
        "id": "URL-10",
        "name": "API Endpoint: POST /api/verify/url (Generic Web)",
        "is_api": True,
        "payload": {"url": "https://example.com"}
    }
]

def run_tests():
    print("=" * 70)
    print("BAYYINAH AI — URL ENGINE TEST SUITE (10 CASES)")
    print("=" * 70)

    passed = 0
    failed = 0

    for idx, tc in enumerate(TEST_CASES, 1):
        test_id = tc["id"]
        name = tc["name"]
        print(f"\n[{idx}/10] Testing {test_id}: {name}")

        try:
            if tc.get("expect_ssrf_exception"):
                try:
                    resolver.validate_url_safety(tc["url"])
                    print(f"  ❌ FAILED: Expected SSRFSecurityException for {tc['url']}, but none raised.")
                    failed += 1
                except SSRFSecurityException as e:
                    print(f"  ✅ PASSED: Correctly rejected with SSRFSecurityException: {e}")
                    passed += 1

            elif tc.get("is_api"):
                res = requests.post(f"{BASE_URL}/api/verify/url", json=tc["payload"], timeout=45)
                if res.status_code == 200:
                    data = res.json()
                    status = data.get("verification_status") or data.get("status")
                    session_id = data.get("session_id")
                    print(f"  ✅ PASSED: HTTP 200, Session: {session_id}, Status: {status}")
                    passed += 1
                else:
                    print(f"  ❌ FAILED: HTTP {res.status_code}: {res.text}")
                    failed += 1

            else:
                platform = resolver.detect_platform(tc["url"])
                if platform != tc["expected_platform"]:
                    print(f"  ❌ FAILED: Platform mismatch. Expected {tc['expected_platform']}, got {platform}")
                    failed += 1
                    continue

                if "expected_vid_id" in tc:
                    resolved = resolver.resolve_url(tc["url"])
                    if resolved.get("video_id") != tc["expected_vid_id"]:
                        print(f"  ❌ FAILED: Video ID mismatch. Expected {tc['expected_vid_id']}, got {resolved.get('video_id')}")
                        failed += 1
                        continue

                print(f"  ✅ PASSED: Detected platform '{platform}' correctly.")
                passed += 1

        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"URL ENGINE SUITE RESULTS: {passed} PASSED, {failed} FAILED (TOTAL 10)")
    print("=" * 70)
    return passed == 10

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
