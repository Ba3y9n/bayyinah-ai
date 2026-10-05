import unittest
import json
import hashlib
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from app.db.database import init_db, SessionLocal
from app.db.seed_knowledge_base import seed_trusted_sources_and_documents
from app.models.knowledge_models import (
    TrustedSourceModel,
    DocumentModel,
    DocumentChunkModel,
    TermModel
)
from app.models.knowledge_schemas import KnowledgeSearchRequest, EvidenceType, VerificationStatus
from app.knowledge.retrieval_service import knowledge_retrieval_service
from app.knowledge.evidence_service import evidence_validation_service
from app.knowledge.source_registry import source_registry_service
from app.knowledge.source_health import source_health_service
from app.knowledge.specialized_handlers import quran_special_handler, terminology_special_handler
from app.knowledge.gemini_knowledge_tools import knowledge_tools_dispatcher

class TestTrustedKnowledgeBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.db = SessionLocal()
        seed_trusted_sources_and_documents(cls.db)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_01_challenge_sources_registered(self):
        """Verifies official challenge sources are registered with governance metadata."""
        official_slugs = ["dawa-center", "islamic-content-aljumhrah", "dorar-net", "shamela-ws", "quranpedia"]
        for slug in official_slugs:
            src = self.db.query(TrustedSourceModel).filter_by(slug=slug).first()
            self.assertIsNotNone(src, f"Source with slug {slug} must be registered in trusted_sources")
            self.assertTrue(src.is_active)
            self.assertIn(src.trust_status, ["APPROVED", "REVIEW_REQUIRED"])
            # Allowed operations must be valid JSON with restrictions
            ops = json.loads(src.allowed_operations) if isinstance(src.allowed_operations, str) else src.allowed_operations
            self.assertIsInstance(ops, dict)
            self.assertTrue(ops.get("LINK_TO_SOURCE") or ops.get("LINK"))

    def test_02_licensing_governance_boundaries(self):
        """Verifies that external sources without explicit written reuse licenses are NOT marked VERIFIED."""
        dawa_src = self.db.query(TrustedSourceModel).filter_by(slug="dawa-center").first()
        self.assertIn(dawa_src.license_status, ["PENDING", "PENDING_VERIFICATION"])
        self.assertNotEqual(dawa_src.license_status, "VERIFIED")
        shamela_src = self.db.query(TrustedSourceModel).filter_by(slug="shamela-ws").first()
        self.assertIn(shamela_src.license_status, ["PENDING", "PENDING_VERIFICATION"])
        self.assertNotEqual(shamela_src.license_status, "VERIFIED")

    def test_03_documents_and_chunks_integrity(self):
        """Verifies SHA-256 content hashes, locators, and foreign keys."""
        chunks = self.db.query(DocumentChunkModel).all()
        self.assertGreaterEqual(len(chunks), 10)
        for chk in chunks:
            self.assertTrue(chk.source_locator, "Each chunk must have a non-empty source_locator")
            self.assertTrue(chk.canonical_url, "Each chunk must have a canonical_url")
            # Verify SHA-256 hash match
            computed = hashlib.sha256(chk.content.encode("utf-8")).hexdigest()
            self.assertEqual(chk.content_hash, computed, "Chunk content_hash must match SHA-256 of content")

    def test_04_exact_match_quran(self):
        """Verifies exact match retrieval for authentic Quranic verse."""
        req = KnowledgeSearchRequest(
            query="اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ",
            category="QURAN",
            top_k=3
        )
        res = knowledge_retrieval_service.search(self.db, req)
        self.assertGreater(len(res.results), 0)
        top = res.results[0]
        self.assertEqual(top.support_level, EvidenceType.DIRECT_SUPPORT)
        self.assertEqual(top.document["category"], "QURAN")
        ref = (top.chunk.get("verse_reference") or "") + " " + (top.chunk.get("source_locator") or "")
        self.assertIn("255", ref)

    def test_05_hybrid_retrieval_rrf(self):
        """Verifies reciprocal rank fusion combines exact and semantic search."""
        req = KnowledgeSearchRequest(
            query="إنما الأعمال بالنيات ولكل امرئ ما نوى",
            category="HADITH",
            top_k=5
        )
        res = knowledge_retrieval_service.search(self.db, req)
        self.assertGreater(len(res.results), 0)
        top = res.results[0]
        self.assertGreater(top.scores.get("rrf", 0), 0)
        self.assertIn("النيات", top.document["title_ar"] + top.chunk["content"] + top.source["name_ar"])

    def test_06_provenance_traceability(self):
        """Verifies that evidence provenance is complete and traceable."""
        req = KnowledgeSearchRequest(query="إنما الأعمال بالنيات", category="HADITH", top_k=1)
        res = knowledge_retrieval_service.search(self.db, req)
        top = res.results[0]
        prov = top.provenance
        self.assertTrue(prov.source_id)
        self.assertTrue(prov.document_id)
        self.assertTrue(prov.chunk_id)
        self.assertTrue(prov.locator)
        self.assertTrue(prov.url.startswith("http"))
        self.assertEqual(len(prov.content_hash), 64)

    def test_07_quran_typo_correction(self):
        """Verifies that altered wording in a verse triggers respectful correction."""
        altered_verse = "الله لا إله إلا هو الحي القيوم لا تأخذه نوم ولا سنة" # altered order
        check = quran_special_handler.inspect_verse(self.db, altered_verse)
        self.assertIsNotNone(check)
        self.assertFalse(check["is_exact_match"])
        self.assertIn("تنبيه", check["notes"])
        self.assertIn("البقرة: 255", check["verse_reference"])

    def test_08_hadith_weak_and_fabricated_detection(self):
        """Verifies that fabricated and weak hadiths are properly flagged with source references."""
        # Case A: Fabricated / Batil
        req_china = KnowledgeSearchRequest(query="اطلبوا العلم ولو بالصين", category="HADITH", top_k=3)
        res_china = knowledge_retrieval_service.search(self.db, req_china)
        self.assertGreater(len(res_china.results), 0)
        val_china = evidence_validation_service.validate(self.db, "اطلبوا العلم ولو بالصين", "HADITH_CLAIM", "HADITH", res_china.results)
        self.assertEqual(val_china["status"], VerificationStatus.FABRICATED.value)

        # Case B: Weak
        req_fast = KnowledgeSearchRequest(query="صوموا تصحوا", category="HADITH", top_k=3)
        res_fast = knowledge_retrieval_service.search(self.db, req_fast)
        self.assertGreater(len(res_fast.results), 0)
        val_fast = evidence_validation_service.validate(self.db, "صوموا تصحوا", "HADITH_CLAIM", "HADITH", res_fast.results)
        self.assertEqual(val_fast["status"], VerificationStatus.WEAK.value)

    def test_09_personal_fatwa_level_d_referral(self):
        """Verifies that personal fatwas (Level D) are immediately redirected to SPECIALIST referral."""
        personal_query = "أنا طلقت زوجتي مرتين في حالة غضب فما حكم رجعتها؟"
        val_res = evidence_validation_service.validate(
            self.db, personal_query, "PERSONAL_FATWA", "FIQH", []
        )
        self.assertEqual(val_res["status"], VerificationStatus.SPECIALIST.value)
        self.assertEqual(val_res["content_level"], "LEVEL_D")
        self.assertIn("المفتي المختص", val_res["reason"])

    def test_10_fiqh_conflict_detection(self):
        """Verifies that matters with scholarly difference return CONFLICT."""
        conflict_query = "حكم قراءة المأموم للفاتحة خلف الإمام في الصلاة الجهرية"
        req = KnowledgeSearchRequest(query=conflict_query, category="FIQH", top_k=3)
        res = knowledge_retrieval_service.search(self.db, req)
        val_res = evidence_validation_service.validate(self.db, conflict_query, "FIQH_CLAIM", "FIQH", res.results)
        self.assertEqual(val_res["status"], VerificationStatus.CONFLICT.value)
        self.assertEqual(val_res["content_level"], "LEVEL_C")

    def test_11_abstention_on_insufficient_evidence(self):
        """Verifies honest abstention (NOT_ESTABLISHED) when no evidence exists."""
        unknown_text = "قال الشاعر القديم في مجلس هشام بن عبد الملك كلاماً لم يروه أحد قط في أي كتاب"
        val_res = evidence_validation_service.validate(self.db, unknown_text, "SCHOLAR_QUOTE", "OTHER", [])
        self.assertEqual(val_res["status"], VerificationStatus.NOT_ESTABLISHED.value)
        self.assertIn("امتناع تحفظي", val_res["explanation"])

    def test_12_terminology_standard_lookup(self):
        """Verifies dictionary lookup of sensitive Islamic terms from Al-Jumhrah / Islamic Content."""
        term_info = terminology_special_handler.lookup_term(self.db, "ما هو التوحيد؟")
        self.assertIsNotNone(term_info)
        self.assertEqual(term_info["term_ar"], "التوحيد")
        self.assertGreater(len(term_info["translations"]), 0)
        self.assertEqual(term_info["translations"][0]["approved_translation"], "Monotheism (Islamic Tawhid)")

    def test_13_gemini_knowledge_tools_dispatcher(self):
        """Verifies dispatching of the 9 knowledge tools for Gemini Function Calling."""
        # 1. search_knowledge_base
        s_res = knowledge_tools_dispatcher.dispatch("search_knowledge_base", {"query": "الأعمال بالنيات", "category": "HADITH"})
        self.assertIn("results", s_res)

        # 2. get_source_metadata
        src_meta = knowledge_tools_dispatcher.dispatch("get_source_metadata", {"source_id": "src-bukhari"})
        self.assertIn(src_meta["slug"], ["sahih-bukhari", "bukhari"])

        # 3. get_term_definition
        t_res = knowledge_tools_dispatcher.dispatch("get_term_definition", {"term": "الجهاد"})
        self.assertEqual(t_res["term_ar"], "الجهاد")

        # 4. get_quran_reference
        q_res = knowledge_tools_dispatcher.dispatch("get_quran_reference", {"text": "قل هو الله أحد"})
        self.assertTrue(q_res["is_exact_match"])

        # 5. source health
        health = source_health_service.check_all_sources_health(self.db)
        self.assertGreater(len(health), 0)

if __name__ == "__main__":
    unittest.main()
