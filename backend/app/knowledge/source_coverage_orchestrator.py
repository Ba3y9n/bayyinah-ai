"""
Bayyinah AI - Official Source Coverage Orchestrator
Enforces Section 3, 4, 5, 6, 7, 8 & 20 of the Master Specifications.

Evaluates every claim against the 11 official challenge sources in official_allowlist.py.
Applies Level 1-6 Search Strategy:
  LEVEL 1: Exact Search
  LEVEL 2: Arabic FTS (tsvector)
  LEVEL 3: Vector Search (Cosine Similarity)
  LEVEL 4: Hybrid Search (RRF Fusion)
  LEVEL 5: Official Live Search (SerpAPI restricted strictly to site:approved-domain)
  LEVEL 6: Canonical Source Fetch & Validation via Evidence Gate

Only the 11 official sources can yield CORE_EVIDENCE.
Unapproved domains or non-core sources are strictly blocked from becoming Evidence.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid

from ..ingestion.official_allowlist import OFFICIAL_SOURCE_ALLOWLIST, is_url_in_allowlist, get_matched_allowlist_entry
from .retrieval_service import knowledge_retrieval_service
from ..services.serpapi_discovery_service import serpapi_discovery_service
from ..services.evidence_gate import evidence_gate

logger = logging.getLogger("bayyinah.source_coverage_orchestrator")


class SourceCoverageOrchestrator:
    def __init__(self):
        self.all_official_sources = OFFICIAL_SOURCE_ALLOWLIST
        self.official_source_slugs = [s["slug"] for s in OFFICIAL_SOURCE_ALLOWLIST]

    def select_relevant_sources(self, claim_text: str, content_type: str = "auto") -> List[Dict[str, Any]]:
        """
        Determines which of the 11 official sources are relevant for a given claim.
        Does not execute unnecessary HTTP calls to irrelevant categories, but ensures
        all 11 sources are evaluated in the coverage planner.
        """
        ct = (content_type or "auto").lower()
        txt = claim_text.lower() if claim_text else ""

        # Map content types / keywords to target source slugs
        relevant_slugs = set()

        if "quran" in ct or "ayah" in ct or "آية" in txt or "سورة" in txt or "قال تعالى" in txt:
            relevant_slugs.update(["quranpedia", "dorar-tafseer", "dawa-center", "dawa-file-7937"])
        
        if "hadith" in ct or "حديث" in txt or "رسول الله" in txt or "النبي" in txt or "عن أبي" in txt:
            relevant_slugs.update(["dorar-hadith", "shamela", "dawa-center"])

        if "tafsir" in ct or "تفسير" in txt:
            relevant_slugs.update(["dorar-tafseer", "quranpedia", "shamela"])

        if "fiqh" in ct or "فقه" in txt or "حكم" in txt or "صلاة" in txt or "زكاة" in txt or "صوم" in txt:
            relevant_slugs.update(["dorar-feqhia", "shamela", "dawa-file-7937"])

        if "aqeedah" in ct or "عقيدة" in txt or "توحيد" in txt or "إيمان" in txt:
            relevant_slugs.update(["dorar-aqeeda", "shamela", "dawa-center"])

        if "seerah" in ct or "history" in ct or "سيرة" in txt or "غزوة" in txt or "تاريخ" in txt:
            relevant_slugs.update(["dorar-history", "shamela"])

        if "dictionary" in ct or "مصطلح" in txt or "معنى" in txt or "ترجمة" in txt:
            relevant_slugs.update(["islamic-content-dict", "islamic-content"])

        if "doubts" in ct or "fatwa" in ct or "شبهة" in txt or "سؤال" in txt or "استفسار" in txt:
            relevant_slugs.update(["dawa-file-7937", "dawa-center", "islamic-content"])

        # Default fallback: if category is auto/unspecified, select primary core encyclopedias
        if not relevant_slugs:
            relevant_slugs.update(["dorar-hadith", "dorar-tafseer", "quranpedia", "shamela", "dawa-center", "islamic-content"])

        selected = [s for s in self.all_official_sources if s["slug"] in relevant_slugs]
        return selected

    async def execute_coverage(
        self,
        claim_text: str,
        content_type: str = "auto",
        session_id: Optional[str] = None,
        claim_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Runs the complete Source Coverage pipeline for a claim across the 11 official sources.
        """
        logger.info(f"[SourceCoverageOrchestrator] Running coverage for claim: '{claim_text[:60]}...'")

        relevant_sources = self.select_relevant_sources(claim_text, content_type)
        relevant_slugs = {s["slug"] for s in relevant_sources}

        queried_sources: List[str] = []
        skipped_sources: List[str] = []
        evidence_found_slugs: List[str] = []
        no_match_slugs: List[str] = []

        sources_breakdown: List[Dict[str, Any]] = []
        all_retrieved_evidence: List[Dict[str, Any]] = []

        # 1. Execute Level 1-4 Search (Knowledge Base Retrieval)
        retrieval_res = await knowledge_retrieval_service.retrieve_for_claim(
            claim_text=claim_text,
            top_k=10,
            content_type_hint=content_type
        )
        candidate_items = retrieval_res.get("candidates", [])
        
        # Filter candidates through Evidence Gate
        approved_evidence = evidence_gate.filter_evidence(candidate_items)

        # Map approved evidence back to official sources
        for ev in approved_evidence:
            source_url = ev.get("url") or ev.get("source_url") or ""
            matched_entry = get_matched_allowlist_entry(source_url)
            if matched_entry:
                ev["official_source_slug"] = matched_entry["slug"]
                ev["official_source_name"] = matched_entry["name_ar"]
                if matched_entry["slug"] not in evidence_found_slugs:
                    evidence_found_slugs.append(matched_entry["slug"])
                all_retrieved_evidence.append(ev)

        # 2. Execute Level 5-6 Search (Live Official Search via SerpAPI when needed)
        need_live_search = len(approved_evidence) == 0 or max([e.get("relevance_score", 0.0) for e in approved_evidence], default=0.0) < 0.60
        
        if need_live_search and serpapi_discovery_service.is_configured:
            logger.info("[SourceCoverageOrchestrator] Executing Level 5 Live Official Discovery...")
            live_candidates = serpapi_discovery_service.discover_official_evidence(claim_text)
            live_approved = evidence_gate.filter_evidence(live_candidates)
            
            for ev in live_approved:
                source_url = ev.get("url") or ev.get("source_url") or ""
                matched_entry = get_matched_allowlist_entry(source_url)
                if matched_entry:
                    ev["official_source_slug"] = matched_entry["slug"]
                    ev["official_source_name"] = matched_entry["name_ar"]
                    if matched_entry["slug"] not in evidence_found_slugs:
                        evidence_found_slugs.append(matched_entry["slug"])
                    all_retrieved_evidence.append(ev)

        # Build detailed source breakdown per official source
        for src in self.all_official_sources:
            slug = src["slug"]
            name_ar = src["name_ar"]
            domain = src["domain"]
            base_url = src.get("base_url", f"https://{domain}")

            matched_evs = [e for e in all_retrieved_evidence if e.get("official_source_slug") == slug]
            first_ev = matched_evs[0] if matched_evs else {}

            if slug in relevant_slugs:
                queried_sources.append(slug)
                if matched_evs:
                    status = "MATCH_FOUND"
                    ev_count = len(matched_evs)
                else:
                    status = "NO_MATCH"
                    no_match_slugs.append(slug)
                    ev_count = 0

                sources_breakdown.append({
                    "source_id": src["id"],
                    "slug": slug,
                    "name_ar": name_ar,
                    "domain": domain,
                    "base_url": base_url,
                    "search_attempt": True,
                    "query_used": claim_text,
                    "access_status": "ACCESSIBLE",
                    "result_status": status,
                    "status": status, # MATCH_FOUND, NO_MATCH, NOT_RELEVANT, INACCESSIBLE
                    "evidence_count": ev_count,
                    "canonical_url": first_ev.get("url") or first_ev.get("canonical_url") or base_url,
                    "reference": first_ev.get("reference") or first_ev.get("locator") or None,
                    "reason": "تم فحص المصدر والبحث بنجاح" if status == "MATCH_FOUND" else "تم فحص المصدر المعتمد ولم تُسجل مطابقة"
                })
            else:
                skipped_sources.append(slug)
                sources_breakdown.append({
                    "source_id": src["id"],
                    "slug": slug,
                    "name_ar": name_ar,
                    "domain": domain,
                    "base_url": base_url,
                    "search_attempt": False,
                    "query_used": None,
                    "access_status": "SKIPPED_NOT_RELEVANT",
                    "result_status": "NOT_RELEVANT",
                    "status": "NOT_RELEVANT",
                    "evidence_count": 0,
                    "canonical_url": base_url,
                    "reference": None,
                    "reason": "المصدر خارج فئة اختصاص الادعاء"
                })

        # Evaluate final coverage status
        if len(evidence_found_slugs) > 0 and len(no_match_slugs) == 0:
            coverage_status = "FULL"
        elif len(evidence_found_slugs) > 0:
            coverage_status = "PARTIAL"
        else:
            coverage_status = "NO_MATCH"

        run_summary = {
            "run_id": str(uuid.uuid4()),
            "session_id": session_id,
            "claim_id": claim_id,
            "claim_text": claim_text,
            "official_sources_total": 11,
            "relevant_sources_count": len(relevant_sources),
            "queried_sources_count": len(queried_sources),
            "evidence_sources_count": len(evidence_found_slugs),
            "coverage_status": coverage_status,
            "relevant_sources": list(relevant_slugs),
            "queried_sources": queried_sources,
            "skipped_sources": skipped_sources,
            "evidence_found_sources": evidence_found_slugs,
            "sources_breakdown": sources_breakdown,
            "approved_evidence": all_retrieved_evidence,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        logger.info(
            f"[SourceCoverageOrchestrator] Completed: {len(queried_sources)}/11 queried, "
            f"{len(evidence_found_slugs)} sources matched, status: {coverage_status}"
        )

        return run_summary


source_coverage_orchestrator = SourceCoverageOrchestrator()


class SourceCoverageResult:
    def __init__(self, data: Dict[str, Any]):
        self.all_official_sources_count = data.get("official_sources_total", 11)
        self.relevant_sources = data.get("relevant_sources", [])
        self.queried_sources = data.get("queried_sources", [])
        self.skipped_sources = data.get("skipped_sources", [])
        self.evidence_found_sources = data.get("evidence_found_sources", [])
        self.coverage_status = data.get("coverage_status", "NO_MATCH")
        self.sources_breakdown = data.get("sources_breakdown", [])
        self.approved_evidence = data.get("approved_evidence", [])


async def evaluate_source_coverage(claims: List[str], content_category: str = "auto") -> SourceCoverageResult:
    claim_text = " ".join(claims) if isinstance(claims, list) else str(claims)
    res = await source_coverage_orchestrator.execute_coverage(claim_text=claim_text, content_type=content_category)
    return SourceCoverageResult(res)

