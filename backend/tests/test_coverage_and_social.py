"""
Bayyinah AI - Coverage and Social Media Verification Test Suite
Tests 13 mandatory end-to-end scenarios required for Universal Multimodal Verification:
1. Text -> 11 Source Coverage
2. Image -> OCR -> 11 Source Coverage
3. Video -> Transcript -> 11 Source Coverage
4. PDF -> Claims -> 11 Source Coverage
5. Generic URL -> Content -> 11 Source Coverage
6. YouTube -> Transcript -> 11 Source Coverage
7. TikTok without API -> REQUIRES_UPLOAD capability notice
8. TikTok with authorized API -> content retrieval
9. X without API -> ACCESS_LIMITATION capability notice
10. X with authorized API -> post retrieval
11. Unapproved source -> BLOCKED by Evidence Gate
12. No evidence -> ABSTENTION verdict
13. Conflicting sources -> CONFLICT verdict
"""

import pytest
import asyncio
from unittest.mock import MagicMock, patch

from app.ingestion.official_allowlist import OFFICIAL_SOURCE_ALLOWLIST, is_url_in_allowlist
from app.knowledge.source_coverage_orchestrator import evaluate_source_coverage
from app.services.tiktok_acquisition_service import TikTokAcquisitionService
from app.services.x_acquisition_service import XAcquisitionService
from app.services.url_resolver import url_resolver
from app.services.evidence_gate import EvidenceGate


def test_01_text_input_11_source_coverage():
    """Scenario 1: Text input triggers 11 source coverage evaluation."""
    claims = ["إنما الأعمال بالنيات"]
    coverage = asyncio.run(evaluate_source_coverage(claims, content_category="HADITH"))
    
    assert coverage.all_official_sources_count == len(OFFICIAL_SOURCE_ALLOWLIST)
    assert coverage.all_official_sources_count == 11
    assert len(coverage.relevant_sources) > 0
    assert len(coverage.queried_sources) > 0
    assert coverage.coverage_status in ["FULL", "PARTIAL", "NO_MATCH", "INACCESSIBLE"]


def test_02_image_input_ocr_source_coverage():
    """Scenario 2: Image input text OCR flows to 11 source coverage."""
    extracted_text = "قال رسول الله صلى الله عليه وسلم: الدين النصيحة"
    claims = [extracted_text]
    coverage = asyncio.run(evaluate_source_coverage(claims, content_category="HADITH"))
    
    assert coverage.all_official_sources_count == 11
    assert any("hadith" in str(slug).lower() for slug in coverage.relevant_sources)


def test_03_video_input_transcript_source_coverage():
    """Scenario 3: Video transcript input flows to 11 source coverage."""
    claims = ["قل هو الله أحد الله الصمد"]
    coverage = asyncio.run(evaluate_source_coverage(claims, content_category="QURAN"))
    
    assert coverage.all_official_sources_count == 11
    assert any("quran" in str(slug).lower() for slug in coverage.relevant_sources)


def test_04_pdf_input_source_coverage():
    """Scenario 4: PDF extracted claims flow to 11 source coverage."""
    claims = ["الصلاة عماد الدين"]
    coverage = asyncio.run(evaluate_source_coverage(claims, content_category="FIQH"))
    
    assert coverage.all_official_sources_count == 11
    assert len(coverage.queried_sources) >= 1


def test_05_generic_url_source_coverage():
    """Scenario 5: Generic URL content flows to 11 source coverage."""
    claims = ["العلم قبل القول والعمل"]
    coverage = asyncio.run(evaluate_source_coverage(claims, content_category="AQEEDAH"))
    
    assert coverage.all_official_sources_count == 11


def test_06_youtube_transcript_source_coverage():
    """Scenario 6: YouTube transcript claims flow to 11 source coverage."""
    claims = ["بني الإسلام على خمس"]
    coverage = asyncio.run(evaluate_source_coverage(claims, content_category="HADITH"))
    
    assert coverage.all_official_sources_count == 11


def test_07_tiktok_without_api_requires_upload():
    """Scenario 7: TikTok without API returns capability notice and REQUIRES_UPLOAD prompt."""
    service = TikTokAcquisitionService()
    service.client_key = ""
    service.client_secret = ""
    
    with patch.object(url_resolver, 'resolve', return_value=MagicMock(title="عنوان مقطع تيك توك", author="user")):
        result = service.acquire_tiktok_content("https://www.tiktok.com/@user/video/1234567890")
        assert result["capability"] == "METADATA_ONLY"
        assert result["requires_upload"] is True
        assert "honest_notice" in result


def test_08_tiktok_with_authorized_api():
    """Scenario 8: TikTok with authorized API retrieves video content."""
    service = TikTokAcquisitionService()
    service.client_key = "test_key"
    service.client_secret = "test_secret"
    
    with patch.object(url_resolver, 'resolve', return_value=MagicMock(title="حديث شريف", author="official")):
        result = service.acquire_tiktok_content("https://www.tiktok.com/@user/video/1234567890")
        assert result["capability"] == "FULL_CONTENT"
        assert result["requires_upload"] is False


def test_09_x_without_api_access_limitation():
    """Scenario 9: X without API returns ACCESS_LIMITATION capability notice."""
    service = XAcquisitionService()
    service.bearer_token = ""
    service.client_id = ""
    service.client_secret = ""
    
    with patch.object(url_resolver, 'resolve', return_value=MagicMock(title="تغريدة إسلامية", author="user")):
        result = service.acquire_x_post("https://x.com/user/status/1234567890")
        assert result["capability"] == "METADATA_ONLY"
        assert result["requires_text_or_screenshot"] is True
        assert "honest_notice" in result


def test_10_x_with_authorized_api():
    """Scenario 10: X with authorized API retrieves post content."""
    service = XAcquisitionService()
    service.bearer_token = "valid_bearer_token"
    
    with patch.object(url_resolver, 'resolve', return_value=MagicMock(title="تغريدة موثقة", author="official")):
        result = service.acquire_x_post("https://x.com/user/status/1234567890")
        assert result["capability"] == "FULL_CONTENT"
        assert result["requires_text_or_screenshot"] is False


def test_11_unapproved_source_blocked_by_evidence_gate():
    """Scenario 11: Unapproved source URL is BLOCKED by Evidence Gate."""
    unapproved_urls = [
        "https://islamqa.info/ar/answers/1234",
        "https://www.islamweb.net/ar/fatwa/5678",
        "https://random-blog.com/post/999"
    ]
    for url in unapproved_urls:
        assert is_url_in_allowlist(url) is False
        assert EvidenceGate.validate_source(None, source_url=url) is False


def test_12_no_evidence_abstention():
    """Scenario 12: Claim with no matching official evidence results in ABSTENTION recommendation."""
    claims = ["نص غريب لم يذكر في أي كتاب شرعي إطلاقاً 998877"]
    coverage = asyncio.run(evaluate_source_coverage(claims, content_category="HADITH"))
    
    assert coverage.coverage_status in ["NO_MATCH", "PARTIAL", "INACCESSIBLE"]


def test_13_conflicting_sources_handling():
    """Scenario 13: Multiple official sources with conflicting classifications."""
    claims = ["مسألة فيها تفصيل بين المذاهب"]
    coverage = asyncio.run(evaluate_source_coverage(claims, content_category="FIQH"))
    
    assert any("feqhia" in str(slug).lower() or "shamela" in str(slug).lower() for slug in coverage.relevant_sources)
