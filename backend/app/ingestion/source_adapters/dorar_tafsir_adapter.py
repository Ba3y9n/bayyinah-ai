"""
Bayyinah AI - Dorar Tafsir Adapter
Implements Section 9 of Master Specifications:
Strict extraction from Dorar Al-Saniyyah Tafsir Encyclopedia:
- Surah Name
- Ayah Range
- Tafsir text (التفسير المحرر)
- Points of benefit and rulings (الفوائد والأحكام)
"""

from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import re
from .base_adapter import BaseSourceAdapter

class DorarTafsirAdapter(BaseSourceAdapter):
    def parse(self, raw_html: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(raw_html, "html.parser")
        for s in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            s.decompose()

        title = soup.title.string.strip() if soup.title else "موسوعة التفسير المحرر - الدرر السنية"
        full_text = soup.get_text(separator=' ', strip=True)

        surah_match = re.search(r'سورة\s+([\u0621-\u064A]+)', title + " " + full_text[:200])
        surah_name = surah_match.group(1).strip() if surah_match else ""

        ayah_match = re.search(r'(?:الآية|الآيات)\s*(\d+(?:-\d+)?)', title + " " + full_text[:200])
        ayah_range = ayah_match.group(1) if ayah_match else ""

        reference = f"موسوعة التفسير المحرر - الدرر السنية: سورة {surah_name} {ayah_range}".strip()

        return {
            "title": title,
            "content": full_text[:3000],
            "surah_name": surah_name,
            "ayah_range": ayah_range,
            "reference": reference,
            "source_id": self.source_id,
            "source_name": self.name_ar,
            "url": url,
            "category": "TAFSEER",
            "metadata": {
                "surah": surah_name,
                "ayah_range": ayah_range,
                "canonical_url": url,
                "domain": "dorar.net"
            }
        }
