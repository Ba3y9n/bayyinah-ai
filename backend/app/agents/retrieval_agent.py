import concurrent.futures
import time
from typing import List, Dict, Any, Optional
from ..models.schemas import EvidenceItem
from ..models.knowledge_schemas import KnowledgeSearchRequest
from ..knowledge.retrieval_service import knowledge_retrieval_service
from ..services.search_service import search_service
from ..services.evidence_gate import evidence_gate
from ..ingestion.source_adapters.adapter_registry import get_all_adapters
from ..ingestion.official_allowlist import OFFICIAL_SOURCE_ALLOWLIST
import logging

logger = logging.getLogger("bayyinah.agents.retrieval")

# Strict mapping: claim_type -> target allowed official categories
CATEGORY_ROUTER_MAP = {
    "quran": ["TAFSIR", "DAWA"],
    "tafsir": ["TAFSIR", "DAWA"],
    "hadith": ["HADITH", "DAWA"],
    "fiqh": ["FIQH", "DAWA", "QUESTIONS_DOUBTS"],
    "fatwa": ["FIQH", "QUESTIONS_DOUBTS", "DAWA"],
    "aqeedah": ["AQEEDAH", "DAWA"],
    "seerah": ["SEERAH_HISTORY", "DAWA"],
    "history": ["SEERAH_HISTORY", "DAWA"],
    "islamic history": ["SEERAH_HISTORY", "DAWA"],
    "general": ["DAWA", "QUESTIONS_DOUBTS", "DICTIONARY_TRANSLATION"]
}

def get_allowed_source_categories(claim_type: str) -> List[str]:
    if not claim_type:
        return ["DAWA"]
    ct_lower = claim_type.lower()
    for key, val in CATEGORY_ROUTER_MAP.items():
        if key in ct_lower:
            return val
    return ["DAWA", "QUESTIONS_DOUBTS", "DICTIONARY_TRANSLATION"]

class RetrievalAgent:
    def __init__(self):
        pass

    def _fetch_from_adapter(self, adapter, query: str, claim_text: str) -> List[EvidenceItem]:
        items = []
        try:
            urls = adapter.search(query, max_results=2)
            for url in urls[:2]:
                fetch_res = adapter.fetch(url, timeout=10)
                if fetch_res.get("success"):
                    parsed = adapter.parse(fetch_res["html"], url)
                    if parsed:
                        ev_data = adapter.extract_evidence(parsed, claim_text)
                        
                        # Basic relevance check
                        relevance = ev_data.get("relevance_score", 0.5)
                        
                        ev = EvidenceItem(
                            document_id=ev_data.get("id", ""),
                            source_id=adapter.source_id,
                            source_name=adapter.name_ar,
                            author=None,
                            organization=None,
                            category=adapter.category,
                            title=parsed.get("title", ""),
                            excerpt=ev_data.get("excerpt", "")[:1500],
                            reference=adapter.extract_reference(parsed),
                            url=url,
                            license="Approved Source",
                            relevance_score=relevance,
                            evidence_type="LIVE_ADAPTER",
                            ruling_or_grade=parsed.get("metadata", {}).get("grade"),
                            comparison_notes="Live concurrent search"
                        )
                        items.append(ev)
        except Exception as e:
            logger.warning(f"Adapter {adapter.slug} failed: {e}")
        return items

    def orchestrate_hybrid_retrieval(
        self,
        queries: List[str],
        limit: int = 5,
        category: Optional[str] = None,
        claim_text: Optional[str] = None,
        db: Optional[Any] = None,
        claim_id: Optional[str] = None
    ) -> List[EvidenceItem]:
        
        evidence_items: List[EvidenceItem] = []
        allowed_cats = get_allowed_source_categories(category)
        
        # Determine applicable sources
        applicable_sources = [s for s in OFFICIAL_SOURCE_ALLOWLIST if s.get("category") in allowed_cats]
        if not applicable_sources:
            applicable_sources = [s for s in OFFICIAL_SOURCE_ALLOWLIST if s.get("category") == "DAWA"]
            
        applicable_slugs = [s["slug"] for s in applicable_sources]
        adapters = get_all_adapters()
        active_adapters = [adapters[s] for s in applicable_slugs if s in adapters]

        logger.info(f"Searching across {len(active_adapters)} sources concurrently for claim type: {category}")

        # 1. Concurrent Live Adapter Search
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(active_adapters) or 1) as executor:
            futures = []
            for adapter in active_adapters:
                for q in queries[:2]:
                    futures.append(executor.submit(self._fetch_from_adapter, adapter, q, claim_text or ""))
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    res = future.result()
                    if res:
                        evidence_items.extend(res)
                except Exception as e:
                    pass
                    
        # 2. Database Fallback (if needed and applicable)
        if db:
            try:
                for q in queries[:2]:
                    search_req = KnowledgeSearchRequest(
                        query=q,
                        category=allowed_cats[0] if allowed_cats else "all",
                        top_k=3
                    )
                    search_res = knowledge_retrieval_service.search(db, search_req)
                    if search_res and search_res.results:
                        for item in search_res.results:
                            prov = item.provenance
                            if prov.source_id not in [s["id"] for s in applicable_sources]:
                                continue
                            score = float(item.scores.get("rrf", 0.0) or item.scores.get("relevance", 0.0))
                            ev = EvidenceItem(
                                document_id=str(prov.document_id),
                                source_id=str(prov.source_id),
                                source_name=prov.source_name or "Official Source",
                                author=None,
                                organization=None,
                                category=item.document.get("category") or "general",
                                title=prov.document_title or "Title",
                                excerpt=item.chunk.get("content", ""),
                                reference=prov.reference or prov.locator or "",
                                url=prov.url or "",
                                license=prov.license_status or "Verified",
                                relevance_score=min(score, 1.0) if score > 0 else 0.0,
                                evidence_type="INTERNAL_DB",
                                ruling_or_grade=prov.scientific_status,
                                comparison_notes="Supabase FTS"
                            )
                            evidence_items.append(ev)
            except Exception as e:
                logger.warning(f"DB search error: {e}")

        # 3. Deduplicate
        seen_urls = set()
        deduped_items = []
        for ev in evidence_items:
            if ev.url and ev.url not in seen_urls:
                seen_urls.add(ev.url)
                deduped_items.append(ev)

        # 4. Evidence Gate (Strict check)
        validated_items = []
        for ev in deduped_items:
            if evidence_gate.validate_source(ev.source_id, ev.url) and ev.excerpt and ev.url:
                validated_items.append(ev)

        validated_items.sort(key=lambda x: x.relevance_score, reverse=True)
        return validated_items[:limit]

retrieval_agent = RetrievalAgent()
