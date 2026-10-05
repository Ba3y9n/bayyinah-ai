"""
Bayyinah AI - Dawa Center Adapter
Implements Section 8 of Master Specifications:
Strict extraction from Dawa Center for Introducing Islam (dawa.center):
- Guide / Article Title
- Methodological Content for Dawa & Dialogue
- Review status and canonical references
"""

from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import re
from .base_adapter import BaseSourceAdapter

class DawaCenterAdapter(BaseSourceAdapter):
    def parse(self, raw_html: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(raw_html, "html.parser")
        for s in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            s.decompose()

        title = soup.title.string.strip() if soup.title else "مركز دعوة للتعريف بالإسلام"
        full_text = soup.get_text(separator=' ', strip=True)

        reference = f"مركز دعوة للتعريف بالإسلام: {title}"

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
                "domain": "dawa.center"
            }
        }
