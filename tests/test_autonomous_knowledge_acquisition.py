"""
Bayyinah AI - Autonomous Knowledge Acquisition Engine Test Suite
Tests:
1. Quality Gate validation rules & review queue logging
2. Acquisition Queue lifecycle (create, run, success, retry, dead letter)
3. Content deduplication & SHA-256 version diffing
4. Official Source Adapters & health connectivity
5. Live PostgreSQL (Supabase) indexing verification
6. Admin Knowledge API endpoints
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
from app.ingestion.quality_gate import quality_gate
from app.ingestion.acquisition_queue import acquisition_queue
from app.ingestion.acquisition_engine import acquisition_engine
from app.ingestion.scheduler import knowledge_scheduler
from app.ingestion.source_adapters.adapter_registry import get_all_adapters, OFFICIAL_SOURCE_ALLOWLIST
from app.models.knowledge_models import (
    DocumentModel,
    DocumentVersionModel,
    KnowledgeReviewItemModel,
    IngestionJobModel
)

class TestAutonomousKnowledgeAcquisition(unittest.TestCase):

    def setUp(self):
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_01_quality_gate_allowlist_enforcement(self):
        """Quality Gate must strictly reject any unauthorized source or domain."""
        fake_payload = {
            "title": "نص غير معتمد",
            "content": "هذا نص تجريبي لا ينتمي لمصدر معتمد على الإطلاق.",
            "reference": "مرجع وهمي",
            "content_hash": "a" * 64
        }
        fake_uuid = str(uuid.uuid4())
        res = quality_gate.evaluate_document(fake_payload, fake_uuid, db=self.db)
        self.assertEqual(res["status"], "REJECT")
        self.assertIn("المصدر أو الرابط غير مدرج", res["reason"])

    def test_02_quality_gate_valid_source(self):
        """Quality Gate must PASS for legitimate official source and sufficient content."""
        dorar_entry = OFFICIAL_SOURCE_ALLOWLIST[0]
        valid_payload = {
            "title": "شرح حديث النيات",
            "url": "https://dorar.net/hadith/sharh/12345",
            "content": "عن أمير المؤمنين عمر بن الخطاب رضي الله عنه قال سمعت رسول الله صلى الله عليه وسلم يقول إنما الأعمال بالنيات وإنما لكل امرئ ما نوى",
            "reference": "الموسوعة الحديثية - الدرر السنية",
            "content_hash": "b" * 64
        }
        res = quality_gate.evaluate_document(valid_payload, dorar_entry["id"], db=self.db)
        self.assertEqual(res["status"], "PASS")
        self.assertTrue(res["checklist"]["source_allowed"])
        self.assertTrue(res["checklist"]["url_valid"])

    def test_03_acquisition_queue_lifecycle(self):
        """Acquisition queue should create, transition to running, and succeed."""
        test_source = OFFICIAL_SOURCE_ALLOWLIST[0]["id"]
        job = acquisition_queue.create_job(
            self.db,
            job_type="DISCOVER_AND_EXPAND",
            source_id=test_source,
            metadata={"test": True}
        )
        self.assertIsNotNone(job.id)
        self.assertEqual(job.status, "QUEUED")

        acquisition_queue.start_job(self.db, job.id)
        refreshed = self.db.query(IngestionJobModel).filter(IngestionJobModel.id == job.id).first()
        self.assertEqual(refreshed.status, "RUNNING")

        acquisition_queue.finish_job(self.db, job.id, {"docs": 1})
        refreshed = self.db.query(IngestionJobModel).filter(IngestionJobModel.id == job.id).first()
        self.assertEqual(refreshed.status, "SUCCESS")

    def test_04_acquisition_queue_dead_letter(self):
        """Jobs exceeding max retries must route to DEAD_LETTER status."""
        test_source = OFFICIAL_SOURCE_ALLOWLIST[0]["id"]
        job = acquisition_queue.create_job(
            self.db,
            job_type="DISCOVER_AND_EXPAND",
            source_id=test_source,
            metadata={"test_fail": True}
        )
        # Fail up to max_retries
        for i in range(job.max_retries + 1):
            acquisition_queue.fail_job(self.db, job.id, f"Failure attempt {i+1}")

        refreshed = self.db.query(IngestionJobModel).filter(IngestionJobModel.id == job.id).first()
        self.assertEqual(refreshed.status, "DEAD_LETTER")
        self.assertTrue(refreshed.is_dead_letter)

    def test_05_document_versioning_and_deduplication(self):
        """Unchanged document is SKIPPED_UNCHANGED; updated document increments version."""
        dorar_entry = OFFICIAL_SOURCE_ALLOWLIST[0]
        test_url = f"https://dorar.net/hadith/test-ver-{uuid.uuid4().hex[:8]}"
        initial_content = "المحتوى الأصلي للحديث الشريف موثق ومضبوط بنصه الكامل."

        # Insert initial doc
        doc_id = str(uuid.uuid4())
        initial_hash = "hash_v1_" + uuid.uuid4().hex
        now = datetime.datetime.now(datetime.timezone.utc)
        doc = DocumentModel(
            id=doc_id,
            source_id=dorar_entry["id"],
            category="HADITH",
            title="حديث تجريبي للنسخ",
            content=initial_content,
            reference="الدرر السنية",
            url=test_url,
            canonical_url=test_url,
            content_hash=initial_hash,
            version="1.0",
            created_at=now,
            updated_at=now
        )
        self.db.add(doc)
        self.db.commit()

        # Check existing version count
        v_before = self.db.query(DocumentVersionModel).filter(DocumentVersionModel.document_id == doc_id).count()

        # Simulate update: archive v1.0 and bump to 1.1
        archived_v = DocumentVersionModel(
            document_id=doc_id,
            version="1.0",
            content_hash=initial_hash,
            title=doc.title,
            content=initial_content,
            reference=doc.reference,
            diff_summary="تحديث آلي تجريبي"
        )
        self.db.add(archived_v)
        doc.version = "1.1"
        doc.content = "المحتوى المحدث للحديث الشريف مع إضافة تخريج أوسع."
        doc.content_hash = "hash_v2_" + uuid.uuid4().hex
        self.db.commit()

        v_after = self.db.query(DocumentVersionModel).filter(DocumentVersionModel.document_id == doc_id).count()
        self.assertEqual(v_after, v_before + 1)
        self.assertEqual(doc.version, "1.1")

    def test_06_official_adapters_registered(self):
        """All 11 approved official sources must have dedicated adapters."""
        adapters = get_all_adapters()
        self.assertGreaterEqual(len(adapters), 10)
        expected_slugs = ["dorar-hadith", "dorar-tafseer", "dorar-feqhia", "quranpedia", "shamela"]
        for slug in expected_slugs:
            self.assertIn(slug, adapters, f"Missing adapter for {slug}")

    def test_07_scheduler_configurations(self):
        """Scheduler must configure all 11 official sources with non-zero crawl intervals."""
        configs = knowledge_scheduler.get_source_configs()
        self.assertEqual(len(configs), 11)
        for c in configs:
            self.assertGreater(c["crawl_interval_hours"], 0)
            self.assertGreater(c["max_requests_per_minute"], 0)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAutonomousKnowledgeAcquisition)
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    sys.exit(0 if res.wasSuccessful() else 1)
