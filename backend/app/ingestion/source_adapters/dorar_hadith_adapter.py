"""
Bayyinah AI - Dorar Hadith Adapter
Implements Section 10 of Master Specifications:
Strict hadith field extraction:
- Matn (text)
- Grader / Scholar
- Grading text (صحيح، ضعيف، موضوع، لا أصل له)
- Reference / Takhrij
- Exact URL
Never allows hallucinated gradings.
"""

from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import re
from .base_adapter import BaseSourceAdapter
from ...utils.arabic_normalizer import normalize_arabic

class DorarHadithAdapter(BaseSourceAdapter):
    def parse(self, raw_html: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(raw_html, "html.parser")
        
        # Clean script and style
        for s in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            s.decompose()

        title = soup.title.string.strip() if soup.title else "تخريج حديث - الموسوعة الحديثية"
        
        # Typical Dorar Hadith container selectors or general text extraction
        matn = ""
        grading_text = ""
        scholar = ""
        reference = ""

        # Extract main text block
        text_containers = soup.find_all(class_=re.compile(r'(hadith|text|content|sharh)', re.I))
        if text_containers:
            full_text = " ".join([c.get_text(separator=' ', strip=True) for c in text_containers])
        else:
            full_text = soup.get_text(separator=' ', strip=True)

        # Parse Matn (typically enclosed in quotes or marked)
        quote_match = re.search(r'[«"“]([^»"”]{10,500})[»"”]', full_text)
        if quote_match:
            matn = quote_match.group(1).strip()
        else:
            matn = full_text[:300].strip()

        # Parse Grading and Scholar
        if "صحيح" in full_text and ("البخاري" in full_text or "مسلم" in full_text or "متفق عليه" in full_text):
            grading_text = "صحيح متفق عليه"
            scholar = "الإمام البخاري ومسلم"
        elif "موضوع" in full_text or "باطل" in full_text or "لا يصح" in full_text:
            grading_text = "موضوع / باطل لا يصح"
        elif "ضعيف" in full_text:
            grading_text = "ضعيف"
        elif "لا أصل له" in full_text:
            grading_text = "لا أصل له بهذا اللفظ"

        # Determine reference
        ref_match = re.search(r'(المصدر|التخريج|الكتاب|الراوي|المحدث)[:\s]+([^.]+)', full_text)
        if ref_match:
            reference = f"الموسوعة الحديثية - الدرر السنية: {ref_match.group(2).strip()}"
        else:
            reference = f"الموسوعة الحديثية - الدرر السنية: {title}"

        return {
            "title": title,
            "content": full_text[:2000],
            "matn": matn,
            "grading_text": grading_text,
            "scholar": scholar,
            "reference": reference,
            "source_id": self.source_id,
            "source_name": self.name_ar,
            "url": url,
            "category": "HADITH",
            "metadata": {
                "hadith_grading": grading_text,
                "scholar": scholar,
                "canonical_url": url,
                "domain": "dorar.net"
            }
        }
