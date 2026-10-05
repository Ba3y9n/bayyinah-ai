"""
Bayyinah AI - PDF Verification Test Suite (Phase 2)
Tests:
TEST 1: Simple text PDF parsing -> extraction succeeds
TEST 2: Multi-page PDF preserves page_number and structure
TEST 3: PDF claim extraction enters Unified Verification Retrieval Pipeline
TEST 4: PDF claim with evidence in approved source -> APPROVED evidence returned
TEST 5: Links / sources inside PDF outside official allowlist -> BLOCKED by EvidenceGate
TEST 6: PDF claim with no evidence anywhere -> INSUFFICIENT / ABSTAIN
TEST 7: Malformed / non-PDF bytes -> graceful error handling
TEST 8: User PDF content itself is NEVER converted to approved evidence
"""

import sys
import os
import unittest
import io
from pypdf import PdfWriter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.ingestion.pdf_processor import pdf_processor
from app.agents.claim_agent import claim_agent
from app.agents.retrieval_agent import retrieval_agent
from app.services.evidence_gate import evidence_gate
from app.ingestion.official_allowlist import is_url_in_allowlist

class TestPDFVerificationPipeline(unittest.TestCase):

    def test_1_simple_pdf_extraction(self):
        """TEST 1: Simple text PDF parsing -> extraction succeeds."""
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)
        buf = io.BytesIO()
        writer.write(buf)
        pdf_bytes = buf.getvalue()

        pages = pdf_processor.extract_pdf_pages(pdf_bytes, filename="sample.pdf")
        self.assertEqual(len(pages), 1)
        self.assertEqual(pages[0]["page_number"], 1)
        self.assertEqual(pages[0]["file_name"], "sample.pdf")

    def test_2_multipage_pdf_provenance(self):
        """TEST 2: Multi-page PDF preserves page_number and structure."""
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)
        writer.add_blank_page(width=612, height=792)
        writer.add_blank_page(width=612, height=792)
        buf = io.BytesIO()
        writer.write(buf)
        pdf_bytes = buf.getvalue()

        pages = pdf_processor.extract_pdf_pages(pdf_bytes, filename="doc_3pages.pdf")
        self.assertEqual(len(pages), 3)
        self.assertEqual(pages[0]["page_number"], 1)
        self.assertEqual(pages[1]["page_number"], 2)
        self.assertEqual(pages[2]["page_number"], 3)
        self.assertEqual(pages[1]["file_name"], "doc_3pages.pdf")

    def test_3_pdf_claim_extraction_and_pipeline(self):
        """TEST 3: PDF claim extraction enters Unified Verification Retrieval Pipeline."""
        mock_pages = [
            {
                "page_number": 1,
                "text": "القول الأول: قال رسول الله صلى الله عليه وسلم إنما الأعمال بالنيات وانما لكل امرئ ما نوى",
                "file_name": "research.pdf"
            },
            {
                "page_number": 2,
                "text": "مقال دعوي يوضح منهج أهل السنة والجماعة في العبادة",
                "file_name": "research.pdf"
            }
        ]
        claims = claim_agent.extract_claims_from_pdf_pages(mock_pages, filename="research.pdf")
        self.assertGreater(len(claims), 0)
        c1 = claims[0]
        self.assertEqual(c1.file_name, "research.pdf")
        self.assertEqual(c1.page_number, 1)
        self.assertIn("إنما الأعمال بالنيات", c1.claim_text)

        # Route claim through Phase 1 Unified Retrieval Pipeline
        evidence_items = retrieval_agent.orchestrate_hybrid_retrieval(
            queries=[c1.claim_text],
            limit=3,
            category=c1.content_type,
            claim_text=c1.claim_text
        )
        self.assertGreater(len(evidence_items), 0)
        top_ev = evidence_items[0]
        self.assertTrue(is_url_in_allowlist(top_ev.url))

    def test_4_pdf_claim_approved_evidence(self):
        """TEST 4: PDF claim with evidence in approved source -> APPROVED evidence returned."""
        queries = ["الكلمة الطيبة صدقة"]
        ev_items = retrieval_agent.orchestrate_hybrid_retrieval(
            queries=queries,
            limit=3,
            category="Hadith",
            claim_text="الكلمة الطيبة صدقة"
        )
        self.assertGreater(len(ev_items), 0)
        for ev in ev_items:
            self.assertTrue(evidence_gate.validate_source(ev.source_id, ev.url))

    def test_5_pdf_unapproved_source_blocked(self):
        """TEST 5: Links / sources inside PDF outside official allowlist -> BLOCKED by EvidenceGate."""
        unapproved_url = "https://unapproved-pdf-link.com/article"
        self.assertFalse(is_url_in_allowlist(unapproved_url))
        self.assertFalse(evidence_gate.validate_source(None, source_url=unapproved_url))

    def test_6_pdf_no_evidence_yields_insufficient(self):
        """TEST 6: PDF claim with no evidence anywhere -> INSUFFICIENT / ABSTAIN."""
        gate_res = evidence_gate.validate(
            evidences=[],
            confidence_score=0.8,
            claim_text="نص افتراضي غير معروف 998877",
            verdict="ثابت بحسب المصدر"
        )
        self.assertTrue(gate_res["abstention_required"])
        self.assertEqual(gate_res["sanitized_verdict"], "مجهول / غير ثابت بحسب البحث الحالي")

    def test_7_malformed_pdf_error(self):
        """TEST 7: Malformed / non-PDF bytes -> graceful error handling."""
        malformed_bytes = b"NOT_A_PDF_FILE_HEADER"
        with self.assertRaises(ValueError) as ctx:
            pdf_processor.extract_pdf_pages(malformed_bytes, filename="bad.pdf")
        self.assertIn("صيغة الملف غير صالحة", str(ctx.exception))

    def test_8_user_pdf_never_classified_as_evidence(self):
        """TEST 8: User PDF content itself is NEVER converted to approved evidence."""
        user_pdf_url = "blob:http://localhost:3000/user-upload-123.pdf"
        self.assertFalse(is_url_in_allowlist(user_pdf_url))
        self.assertFalse(evidence_gate.validate_source("user-upload", user_pdf_url))

if __name__ == "__main__":
    unittest.main(verbosity=2)
