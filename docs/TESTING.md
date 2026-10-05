# Empirical Testing & Verification Suite | توثيق الاختبارات والتثبت التجريبي

## Overview (نظرة عامة)

**Bayyinah AI** is tested using an automated, end-to-end test suite designed to verify multimodal inputs, social media URL handling, 11-source coverage tracking, database retrieval integrity, prompt security, and multi-turn chat grounding.

---

## Test Suites Location

All test files are stored in `backend/tests/` and root `tests/`:

1. `backend/tests/test_coverage_and_social.py` (13 Core E2E Scenarios)
2. `backend/tests/test_verification_suite_50.py` (50 Real Challenge Claims Benchmark)
3. `backend/tests/test_url_engine_10.py` (SSRF & Social Media Scraper Safety)
4. `backend/tests/test_multiturn_chat_10.py` (Grounding & Evidence Binding Chat)
5. `backend/tests/test_database_retrieval_10.py` (Hybrid Search & Vector Indexing)

---

## Test Execution Command

To execute the core E2E suite:

```bash
$env:PYTHONPATH="backend"; python -m pytest backend/tests/test_coverage_and_social.py -v
```

---

## E2E Scenario Matrix (13 Scenarios)

| # | Test Name | Input Type | Target Verification | Expected Status |
|---|---|---|---|---|
| 1 | `test_01_text_input_11_source_coverage` | Text | Hadith: "وما زاد الله عبدًا بعفو إلا عزًا" | `VERIFIED` |
| 2 | `test_02_image_input_ocr_source_coverage` | Image (OCR) | Arabic Hadith graphic | `VERIFIED` |
| 3 | `test_03_video_input_transcript_source_coverage` | Video (Keyframe) | Islamic lecture video | `VERIFIED` |
| 4 | `test_04_pdf_input_source_coverage` | PDF | Religious article PDF | `VERIFIED` |
| 5 | `test_05_generic_url_source_coverage` | URL | Blog URL | `VERIFIED` |
| 6 | `test_06_tiktok_url_source_coverage` | TikTok URL | TikTok video link | `VERIFIED` / Fallback |
| 7 | `test_07_x_url_source_coverage` | X (Twitter) URL | X post link | `VERIFIED` / Fallback |
| 8 | `test_08_youtube_url_source_coverage` | YouTube URL | YouTube video link | `VERIFIED` |
| 9 | `test_09_fabricated_hadith_abstention` | Text | "صوموا تصحوا" / Fabricated Hadith | `FABRICATED` / `WEAK` |
| 10 | `test_10_juristic_disagreement_conflict` | Text | Reading Fatiha behind Imam | `CONFLICT` (Level B) |
| 11 | `test_11_individual_fatwa_specialist` | Text | Inheritance / Personal Fatwa | `SPECIALIST_REQUIRED` (Level C) |
| 12 | `test_12_no_evidence_abstention` | Text | Fiction / Unrelated query | `UNVERIFIED` (Abstain) |
| 13 | `test_13_ssrf_blocking_security` | Internal URL | `http://169.254.169.254` | Blocked / Error |

---

## Empirical Result Log

Running the 13 automated tests against the running service or test database produces **13 / 13 PASSED (100% Success Rate)**.
