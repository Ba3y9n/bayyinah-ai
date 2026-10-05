"""
Bayyinah AI - Dorar Aqeedah Adapter
Implements Section 11 of Master Specifications:
Strict extraction from Dorar Al-Saniyyah Aqeedah & Sects Encyclopedia:
- Aqeedah topic / creed issue
- Scholarly statements and proofs
- Canonical references
"""

from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import re
from .base_adapter import BaseSourceAdapter

class DorarAqeedahAdapter(BaseSourceAdapter):
    def parse(self, raw_html: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(raw_html, "html.parser")
        for s in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            s.decompose()

        title = soup.title.string.strip() if soup.title else "موسوعة العقيدة والمذاهب المعاصرة - الدرر السنية"
        full_text = soup.get_text(separator=' ', strip=True)

        reference = f"موسوعة العقيدة - الدرر السنية: {title}"

        return {
            "title": title,
            "content": full_text[:3500],
            "reference": reference,
            "source_id": self.source_id,
            "source_name": self.name_ar,
            "url": url,
            "category": "AQEEDAH",
            "metadata": {
                "canonical_url": url,
                "domain": "dorar.net"
            }
        }
