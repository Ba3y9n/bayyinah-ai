import datetime
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from ..services.search_service import search_service
from ..services.registry_service import registry_service
from ..models.schemas import EvidenceItem
from ..knowledge.retrieval_service import knowledge_retrieval_service
from ..models.knowledge_schemas import KnowledgeSearchRequest
from ..services.serpapi_discovery_service import serpapi_discovery_service
from ..ingestion.official_allowlist import is_url_in_allowlist, get_matched_allowlist_entry
from ..ingestion.source_adapters.adapter_registry import get_adapter_by_url
from ..services.evidence_gate import evidence_gate

logger = logging.getLogger("bayyinah.retrieval_agent")

CATEGORY_ROUTER_MAP = {
    "hadith": "HADITH",
    "ط­ط¯ظٹط«": "HADITH",
    "quran": "QURAN",
    "ظ‚ط±ط¢ظ†": "QURAN",
    "ط¢ظٹط©": "QURAN",
    "tafsir": "TAFSEER",
    "طھظپط³ظٹط±": "TAFSEER",
    "fiqh": "FIQH",
    "ظپظ‚ظ‡": "FIQH",
    "ظپطھظˆظ‰/ظ…ط³ط£ظ„ط© ظپظ‚ظ‡ظٹط©": "FIQH",
    "ظ…ط³ط£ظ„ط© ظپظ‚ظ‡ظٹط©": "FIQH",
    "aqeedah": "AQEEDAH",
    "ط¹ظ‚ظٹط¯ط©": "AQEEDAH",
    "seerah": "SEERAH_HISTORY",
    "ط³ظٹط±ط©": "SEERAH_HISTORY",
    "طھط§ط±ظٹط®": "SEERAH_HISTORY",
    "dictionary": "DICTIONARY_TRANSLATION",
    "ظ‚ط§ظ…ظˆط³": "DICTIONARY_TRANSLATION",
    "ظ…طµط·ظ„ط­": "DICTIONARY_TRANSLATION",
}

def map_claim_type_to_category(claim_type: str) -> Optional[str]:
    if not claim_type:
        return None
    ct_lower = claim_type.lower()
    for key, val in CATEGORY_ROUTER_MAP.items():
        if key in ct_lower:
            return val
    return None

class RetrievalAgent:
    """
    AI JOB 4 & 5: Unified Retrieval Orchestrator & Hybrid Search Agent
    Implements Phase 1 Pipeline:
    1. INTERNAL_DB: Primary live search in Supabase (Arabic FTS + pgvector 768-d + Exact + RRF)
    2. LIVE_DISCOVERY: Targeted discovery via SerpAPI restricted strictly to official allowlist
    3. SOURCE_ADAPTER: Canonical page fetch and extraction from official source
    4. EVIDENCE_GATE: Strict validation against 11 approved sources allowlist
    """
    def __init__(self):
        pass

    def search_exact_text(self, query: str) -> List[Dict[str, Any]]:
        return search_service.exact_text_search(query, limit=5)

    def search_keyword(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        results = search_service.exact_text_search(query, limit=5)
        if category and category != "all":
            results = [r for r in results if r["document"].get("category") == category]
        return results

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        return search_service.semantic_search(query, limit=top_k)

    def get_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        src = registry_service.get_source_by_id(source_id)
        return src.dict() if src else None

    def get_evidence(self, document_id: str) -> Optional[Dict[str, Any]]:
        doc = next((d for d in search_service.documents if d["id"] == document_id), None)
        return doc

    def orchestrate_hybrid_retrieval(
        self,
        queries: List[str],
        limit: int = 5,
        category: Optional[str] = None,
        claim_text: Optional[str] = None,
        db: Optional[Session] = None,
        claim_id: Optional[str] = None
    ) -> List[EvidenceItem]:
        """
        Unified Verification Retrieval Pipeline (Phase 1).
        Runs Internal DB (Supabase FTS + pgvector + RRF) -> Live Discovery (SerpAPI site-restricted) -> Source Adapters -> Evidence Gate.
        """
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        mapped_cat = map_claim_type_to_category(category) if category else None
        evidence_items: List[EvidenceItem] = []

        # =========================================================================
        # STEP 1: INTERNAL_DB (Supabase FTS + pgvector + RRF)
        # =========================================================================
        logger.info(f"[INTERNAL_DB] Executing primary retrieval in Supabase (category={mapped_cat}) for queries: {queries[:2]}")
        if db:
            try:
                for q in queries[:2]:
                    search_req = KnowledgeSearchRequest(
                        query=q,
                        category=mapped_cat or "all",
                        top_k=limit
                    )
                    search_res = knowledge_retrieval_service.search(db, search_req)
                    if search_res and search_res.results:
                        for item in search_res.results:
                            prov = item.provenance
                            score = float(item.scores.get("rrf", 0.0) or item.scores.get("relevance", 0.0))
                            ev = EvidenceItem(
                                document_id=str(prov.document_id),
                                source_id=str(prov.source_id),
                                source_name=prov.source_name or "ط§ظ„ظ…طµط¯ط± ط§ظ„ظ…ط¹طھظ…ط¯",
                                author=None,
                                organization=None,
                                category=item.document.get("category") or mapped_cat or "general",
                                title=prov.document_title or "ظˆط«ظٹظ‚ط© ظ…ط¹طھظ…ط¯ط©",
                                excerpt=item.chunk.get("content", ""),
                                reference=prov.reference or prov.locator or "",
                                url=prov.url or "",
                                license=prov.license_status or "ظ…ط±ط¬ط¹ ظ…ظˆط«ظ‚",
                                relevance_score=min(score, 1.0) if score > 0 else 0.0,
                                evidence_type="EXACT" if score >= 0.85 else ("HYBRID" if score >= 0.65 else "SEMANTIC"),
                                ruling_or_grade=prov.scientific_status,
                                comparison_notes="ظ…ط·ط§ط¨ظ‚ط© ظ…ظ† ظ‚ط§ط¹ط¯ط© ط§ظ„ط¨ظٹط§ظ†ط§طھ ط§ظ„ط­ظٹط© (Supabase FTS + pgvector)"
                            )
                            evidence_items.append(ev)
            except Exception as e:
                logger.warning(f"[INTERNAL_DB] Live Supabase query error: {e}. Falling back to search_service.")

        # Fallback to search_service if DB yielded nothing
        if not evidence_items:
            logger.info("[INTERNAL_DB] Primary DB yielded 0 items. Utilizing search_service fallback.")
            mem_items = search_service.hybrid_search(queries, limit=limit)
            evidence_items.extend(mem_items)

        top_score = max([ev.relevance_score for ev in evidence_items], default=0.0)
        logger.info(f"[INTERNAL_DB] Completed. Evidence count: {len(evidence_items)}, top_score: {top_score:.3f}")

        # =========================================================================
        # STEP 2: LIVE_DISCOVERY (SerpAPI Discovery -> Official Allowlist -> Adapters)
        # =========================================================================
        # As per strict verification architecture, general search engines (Google, SerpAPI, Bing)
        # are explicitly banned from providing evidence. We rely strictly on the INTERNAL_DB
        # (pgvector) which indexes the official sources, or direct URL acquisition.
        # Live Discovery via SerpAPI is DISABLED to prevent snippet leakage and general web reliance.

        # STEP 3: EVIDENCE_GATE Filter
        # =========================================================================
        validated_items: List[EvidenceItem] = []
        for ev in evidence_items:
            if evidence_gate.validate_source(ev.source_id, ev.url) and ev.excerpt and ev.reference and ev.url:
                validated_items.append(ev)
            else:
                logger.warning(f"[EVIDENCE_GATE] Discarded item from unapproved source: {ev.source_id} / {ev.url}")

        validated_items.sort(key=lambda x: x.relevance_score, reverse=True)
        return validated_items[:limit]

retrieval_agent = RetrievalAgent()



