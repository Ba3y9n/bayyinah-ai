"""
Bayyinah AI - Islamic Content Portal Adapter
Implements Section 8 of Master Specifications:
Strict extraction from the Islamic Content Portal (islamic-content.com):
- Title and editorial text
- Methodological standards for Dawa content
- Canonical references
"""

from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import re
from .base_adapter import BaseSourceAdapter

class IslamicContentAdapter(BaseSourceAdapter):
    def parse(self, raw_html: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(raw_html, "html.parser")
        for s in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            s.decompose()

        title = soup.title.string.strip() if soup.title else "موسوعة المحتوى الإسلامي المترجم"
        full_text = soup.get_text(separator=' ', strip=True)

        reference = f"موسوعة المحتوى الإسلامي المترجم: {title}"

        return {
            "title": title,
            "content": full_text[:3500],
            "reference": reference,
            "source_id": self.source_id,
            "source_name": self.name_ar,
            "url": url,
            "category": "DAWA",
            "metadata": {
                "canonical_url": url,
                "domain": "islamic-content.com"
            }
        }
