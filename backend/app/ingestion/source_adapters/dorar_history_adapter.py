"""
Bayyinah AI - Dorar History Adapter
Implements Section 13 of Master Specifications:
Strict extraction from Dorar Al-Saniyyah History Encyclopedia:
- Historical event / Seerah milestone
- Date / Hijri year
- Verified historical narrations
- Canonical reference
"""

from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import re
from .base_adapter import BaseSourceAdapter

class DorarHistoryAdapter(BaseSourceAdapter):
    def parse(self, raw_html: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(raw_html, "html.parser")
        for s in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            s.decompose()

        title = soup.title.string.strip() if soup.title else "الموسوعة التاريخية - الدرر السنية"
        full_text = soup.get_text(separator=' ', strip=True)

        year_match = re.search(r'(?:سنة|عام)\s*(\d+)\s*(?:هـ|هجرية)', full_text[:300])
        hijri_year = year_match.group(1) if year_match else None

        reference = f"الموسوعة التاريخية وأحداث السيرة - الدرر السنية: {title}"

        return {
            "title": title,
            "content": full_text[:3500],
            "hijri_year": hijri_year,
            "reference": reference,
            "source_id": self.source_id,
            "source_name": self.name_ar,
            "url": url,
            "category": "SEERAH_HISTORY",
            "metadata": {
                "hijri_year": hijri_year,
                "canonical_url": url,
                "domain": "dorar.net"
            }
        }
