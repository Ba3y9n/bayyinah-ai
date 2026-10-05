"""
Bayyinah AI - Base Source Adapter Interface
Defines the required contract for all 11 official source adapters (Sections 6, 8, 9, 10, 11, 12, 13).
Contract:
- discover()
- search()
- fetch()
- parse()
- extract_metadata()
- extract_reference()
- extract_evidence()
- health_check()
"""

import abc
import time
import hashlib
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
from ...utils.arabic_normalizer import normalize_arabic
from ..official_allowlist import is_url_in_allowlist

class BaseSourceAdapter(abc.ABC):
    def __init__(self, source_info: Dict[str, Any]):
        self.source_id = source_info.get("id")
        self.slug = source_info.get("slug")
        self.name_ar = source_info.get("name_ar")
        self.name_en = source_info.get("name_en")
        self.domain = source_info.get("domain")
        self.base_url = source_info.get("base_url")
        self.category = source_info.get("category", "GENERAL")
        self.authority_level = source_info.get("authority_level", "PRIMARY_CANONICAL")
        self.search_pattern = source_info.get("search_pattern", f"site:{self.domain}")

    def fetch_page(self, url: str, timeout: int = 15) -> Dict[str, Any]:
        """Safely fetches a page from the official domain adhering to crawling ethics."""
        if not is_url_in_allowlist(url):
            return {"success": False, "error": f"URL {url} is not in OFFICIAL_SOURCE_ALLOWLIST"}

        headers = {
            "User-Agent": "BayyinahAI-ScholarlyVerifier/1.0 (+https://bayyinah.ai/verification-bot; scientific research & content verification)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ar,en;q=0.9"
        }
        t0 = time.time()
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status_code = resp.status
                content = resp.read()
                charset = resp.headers.get_content_charset() or "utf-8"
                html_text = content.decode(charset, errors="replace")
                latency_ms = (time.time() - t0) * 1000.0
                return {
                    "success": True,
                    "url": url,
                    "status_code": status_code,
                    "html": html_text,
                    "latency_ms": latency_ms,
                    "etag": resp.headers.get("ETag"),
                    "last_modified": resp.headers.get("Last-Modified")
                }
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": str(e),
                "latency_ms": (time.time() - t0) * 1000.0
            }

    def fetch(self, url: str, timeout: int = 15) -> Dict[str, Any]:
        """Alias for fetch_page to satisfy adapter interface."""
        return self.fetch_page(url, timeout=timeout)

    @abc.abstractmethod
    def parse(self, raw_html: str, url: str) -> Dict[str, Any]:
        """Extracts cleaned text, metadata, citations, and specific domain fields."""
        pass

    def extract_metadata(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts standardized metadata dictionary."""
        return parsed_data.get("metadata", {})

    def extract_reference(self, parsed_data: Dict[str, Any]) -> str:
        """Extracts standardized canonical citation reference."""
        return parsed_data.get("reference") or f"{self.name_ar}: {parsed_data.get('title', '')}"

    def extract_evidence(self, parsed_data: Dict[str, Any], claim_text: str = "") -> Dict[str, Any]:
        """Formats structured evidence item."""
        content = parsed_data.get("content", "")
        raw_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        norm_text = normalize_arabic(content)
        norm_hash = hashlib.sha256(norm_text.encode("utf-8")).hexdigest()

        return {
            "source_id": self.source_id,
            "source_name": self.name_ar,
            "source_domain": self.domain,
            "canonical_url": parsed_data.get("url") or self.base_url,
            "title": parsed_data.get("title", ""),
            "content": content,
            "normalized_content": norm_text,
            "content_type": parsed_data.get("category", self.category).lower(),
            "reference": self.extract_reference(parsed_data),
            "scholar": parsed_data.get("scholar"),
            "author": parsed_data.get("author"),
            "grading": parsed_data.get("grading_text"),
            "content_hash": raw_hash,
            "normalized_hash": norm_hash,
            "metadata": self.extract_metadata(parsed_data),
            "retrieved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    def discover(self, max_urls: int = 10) -> List[str]:
        """
        Discovers candidate URLs from the source through its official landing or index pages.
        Extracts valid links within the allowed path and domain boundaries.
        """
        fetch_res = self.fetch_page(self.base_url, timeout=10)
        if not fetch_res.get("success") or not fetch_res.get("html"):
            return [self.base_url]

        soup = BeautifulSoup(fetch_res["html"], "html.parser")
        discovered: List[str] = [self.base_url]

        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            full_url = urllib.parse.urljoin(self.base_url, href)
            # Remove anchors and query tracking
            parsed = urllib.parse.urlparse(full_url)
            clean_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))

            if is_url_in_allowlist(clean_url) and clean_url not in discovered:
                discovered.append(clean_url)
                if len(discovered) >= max_urls:
                    break

        return discovered

    def search(self, query: str, max_results: int = 5) -> List[str]:
        """
        Constructs source-specific discovery URLs for a given term.
        """
        encoded_query = urllib.parse.quote(query)
        # Standard search paths for approved platforms
        if self.domain == "dorar.net":
            prefix = self.base_url.replace("https://dorar.net", "")
            return [f"https://dorar.net{prefix}?q={encoded_query}"]
        elif self.domain == "quranpedia.net":
            return [f"https://quranpedia.net/search?q={encoded_query}"]
        elif self.domain == "shamela.ws":
            return [f"https://shamela.ws/search?q={encoded_query}"]
        elif self.domain == "islamic-content.com":
            return [f"https://islamic-content.com/search?q={encoded_query}"]
        return [self.base_url]

    def health_check(self) -> Dict[str, Any]:
        """Performs a live connectivity and responsiveness check on the official portal."""
        t0 = time.time()
        try:
            headers = {"User-Agent": "BayyinahAI-HealthCheck/1.0"}
            req = urllib.request.Request(self.base_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                latency = (time.time() - t0) * 1000.0
                status = "ONLINE" if resp.status == 200 else "DEGRADED"
                return {
                    "source_id": self.source_id,
                    "slug": self.slug,
                    "name_ar": self.name_ar,
                    "url": self.base_url,
                    "status": status,
                    "response_time_ms": round(latency, 1),
                    "error": None
                }
        except Exception as e:
            return {
                "source_id": self.source_id,
                "slug": self.slug,
                "name_ar": self.name_ar,
                "url": self.base_url,
                "status": "OFFLINE",
                "response_time_ms": round((time.time() - t0) * 1000.0, 1),
                "error": str(e)
            }
