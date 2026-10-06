"""
Bayyinah AI - SerpAPI Official Source Discovery Service
Enforces Sections 27-31 of Master Specifications:
1. SerpAPI is strictly a discovery layer, NEVER a truth layer.
2. Search queries MUST be restricted via site-restricted directives (e.g. site:dorar.net, site:quranpedia.net).
3. Any URL outside the 11 official sources allowlist is discarded immediately.
4. Retrieved URLs are processed by their dedicated official source adapter to extract canonical text.
"""

import urllib.request
import urllib.parse
import json
import logging
from typing import List, Dict, Any, Optional
from ..config import settings
from ..ingestion.official_allowlist import (
    is_url_in_allowlist,
    get_matched_allowlist_entry,
    OFFICIAL_SOURCE_ALLOWLIST
)
from ..ingestion.source_adapters.adapter_registry import get_adapter_by_url

logger = logging.getLogger("bayyinah.services.serpapi_discovery")

class SerpAPIDiscoveryService:
    def __init__(self):
        self.api_key = settings.SERPAPI_API_KEY

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def discover_official_evidence(self, query: str) -> List[Dict[str, Any]]:
        return self.search_official_sources(query)

    def search_official_sources(
        self,
        query: str,
        category: Optional[str] = None,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Executes a targeted search using SerpAPI strictly restricted to official source allowlist domains.
        Returns a list of validated canonical entries parsed by official adapters.
        """
        if not self.api_key:
            logger.info("SerpAPI API key not configured. Discovery skipped.")
            return []

        # Build site restriction query based on category or official allowlist
        allowed_domains = ["dorar.net", "quranpedia.net", "shamela.ws", "islamic-content.com", "dawa.center"]
        
        # Build site filter
        site_filters = " OR ".join([f"site:{d}" for d in allowed_domains])
        restricted_query = f"{query} ({site_filters})"

        params = {
            "engine": "google",
            "q": restricted_query,
            "hl": "ar",
            "gl": "sa",
            "api_key": self.api_key,
            "num": max_results
        }

        search_url = f"https://serpapi.com/search.json?{urllib.parse.urlencode(params)}"

        try:
            req = urllib.request.Request(search_url, headers={"User-Agent": "BayyinahAI-Discovery/1.0"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            organic_results = data.get("organic_results", [])
            discovered_entries: List[Dict[str, Any]] = []

            for item in organic_results:
                link = item.get("link", "")
                snippet = item.get("snippet", "")
                title = item.get("title", "")

                # Rule: Strictly discard any URL outside the 11 official sources
                if not is_url_in_allowlist(link):
                    logger.debug(f"Discarding unapproved domain from SerpAPI discovery: {link}")
                    continue

                allowlist_entry = get_matched_allowlist_entry(link)
                adapter = get_adapter_by_url(link)

                # Attempt deep fetch & parse through adapter
                content = snippet
                reference = title
                metadata = {}

                if adapter:
                    fetch_res = adapter.fetch_page(link, timeout=6)
                    if fetch_res.get("success") and fetch_res.get("html"):
                        parsed = adapter.parse(fetch_res["html"], link)
                        content = parsed.get("content")
                        reference = parsed.get("reference") or title
                        metadata = parsed.get("metadata", {})
                        
                        if not content or len(content.strip()) < 10:
                            logger.debug(f"Discarding result due to empty extracted content from adapter: {link}")
                            continue
                    else:
                        logger.debug(f"Discarding result because original page could not be fetched: {link}")
                        continue
                else:
                    logger.debug(f"Discarding result because no adapter found for official source: {link}")
                    continue

                discovered_entries.append({
                    "url": link,
                    "title": title,
                    "content": content,
                    "reference": reference,
                    "source_id": allowlist_entry["id"] if allowlist_entry else None,
                    "source_name": allowlist_entry["name_ar"] if allowlist_entry else "مصدر معتمد",
                    "category": allowlist_entry.get("category", "GENERAL") if allowlist_entry else "GENERAL",
                    "metadata": metadata,
                    "discovery_layer": "SERPAPI_OFFICIAL_RESTRICTED"
                })

            return discovered_entries

        except Exception as e:
            logger.warning(f"SerpAPI discovery query failed: {e}")
            return []

serpapi_discovery_service = SerpAPIDiscoveryService()
