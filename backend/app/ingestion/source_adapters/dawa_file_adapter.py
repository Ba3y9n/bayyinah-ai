"""
Bayyinah AI - Dawa File 7937 Adapter
Implements Section 8 & Section 14 of Master Specifications:
Strict extraction from Dawa Center Guideline File 7937 (Questions & Doubts):
- Systematic guidance on contemporary intellectual challenges
- Clear classification of fatwa abstention rules (e.g. personal matrimonial, talaq, inheritance)
- Reference and verified methodology
"""

from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import re
from .base_adapter import BaseSourceAdapter

class DawaFileAdapter(BaseSourceAdapter):
    def parse(self, raw_html: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(raw_html, "html.parser")
        for s in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            s.decompose()

        title = soup.title.string.strip() if soup.title else "دليل الأسئلة والشبهات المعاصرة - مركز دعوة (ملف 7937)"
        full_text = soup.get_text(separator=' ', strip=True)

        reference = "دليل الأسئلة والشبهات المعاصرة - مركز دعوة (ملف 7937)"

        return {
            "title": title,
            "content": full_text[:4000],
            "reference": reference,
            "source_id": self.source_id,
            "source_name": self.name_ar,
            "url": url,
            "category": "QUESTIONS_DOUBTS",
            "metadata": {
                "file_code": "7937",
                "canonical_url": url,
                "domain": "dawa.center"
            }
        }
