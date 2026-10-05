"""
Bayyinah AI - Quranpedia Source Adapter
Implements Section 9 of Master Specifications:
Strict extraction for Quranic verses:
- Surah Name & Number
- Ayah Number
- Rasm Uthmani text
- Standard Tafsir / Recitation / Translation
"""

from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import re
from .base_adapter import BaseSourceAdapter
from ...utils.arabic_normalizer import normalize_arabic

class QuranpediaAdapter(BaseSourceAdapter):
    def parse(self, raw_html: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(raw_html, "html.parser")
        for s in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            s.decompose()

        title = soup.title.string.strip() if soup.title else "موسوعة القرآن الكريم - قرآن بيديا"
        
        # Extract ayah text, surah name, ayah number
        ayah_text = ""
        surah_name = ""
        ayah_num = None
        tafsir_text = ""

        # Try to find quranic verse containers
        verse_containers = soup.find_all(class_=re.compile(r'(ayah|verse|quran|uthmani)', re.I))
        if verse_containers:
            ayah_text = " ".join([c.get_text(separator=' ', strip=True) for c in verse_containers])

        # Try to find tafsir containers
        tafsir_containers = soup.find_all(class_=re.compile(r'(tafseer|tafsir|meaning|sharh)', re.I))
        if tafsir_containers:
            tafsir_text = " ".join([c.get_text(separator=' ', strip=True) for c in tafsir_containers])

        full_text = soup.get_text(separator=' ', strip=True)
        if not ayah_text:
            ayah_text = full_text[:400]

        # Match surah and ayah in title or text: e.g. سورة البقرة الآية 255
        surah_match = re.search(r'سورة\s+([\u0621-\u064A]+)', title + " " + full_text[:200])
        if surah_match:
            surah_name = surah_match.group(1).strip()

        ayah_match = re.search(r'(?:الآية|آية)\s*(\d+)', title + " " + full_text[:200])
        if ayah_match:
            ayah_num = int(ayah_match.group(1))

        reference = f"موسوعة القرآن الكريم (قرآن بيديا) - سورة {surah_name or 'القرآن'} : {ayah_num or ''}".strip(" :")

        return {
            "title": title,
            "content": full_text[:2500],
            "ayah_text": ayah_text,
            "surah_name": surah_name,
            "ayah_num": ayah_num,
            "tafsir_text": tafsir_text[:1500] if tafsir_text else None,
            "reference": reference,
            "source_id": self.source_id,
            "source_name": self.name_ar,
            "url": url,
            "category": "QURAN",
            "metadata": {
                "surah": surah_name,
                "ayah": ayah_num,
                "canonical_url": url,
                "domain": "quranpedia.net"
            }
        }
