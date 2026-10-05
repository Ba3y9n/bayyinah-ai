"""
Bayyinah AI - Islamic Content Dictionary Adapter
Implements Section 8 of Master Specifications:
Strict extraction from the official Islamic Terminology Dictionary (islamic-content.com/dictionary):
- Arabic Islamic Term (المصطلح الشرعي)
- Linguistic & Shariah Definition (التعريف الشرعي واللغوي)
- Canonical Approved Translations (الترجمات المعتمدة)
- Reference
"""

from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import re
from .base_adapter import BaseSourceAdapter

class DictionaryAdapter(BaseSourceAdapter):
    def parse(self, raw_html: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(raw_html, "html.parser")
        for s in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            s.decompose()

        title = soup.title.string.strip() if soup.title else "قاموس المصطلحات والمفاهيم الإسلامية المترجمة"
        full_text = soup.get_text(separator=' ', strip=True)

        # Term extraction
        term = ""
        term_elem = soup.find(class_=re.compile(r'(term|word|title)', re.I))
        if term_elem:
            term = term_elem.get_text(strip=True)
        else:
            term = title.replace("قاموس المصطلحات", "").strip(" -:|")

        # Definition extraction
        definition = ""
        def_elem = soup.find(class_=re.compile(r'(def|meaning|content|sharh)', re.I))
        if def_elem:
            definition = def_elem.get_text(separator=' ', strip=True)
        else:
            definition = full_text[:1000]

        reference = f"قاموس المصطلحات والمفاهيم الإسلامية المترجمة: {term or title}"

        return {
            "title": title,
            "term": term,
            "definition": definition,
            "content": full_text[:3000],
            "reference": reference,
            "source_id": self.source_id,
            "source_name": self.name_ar,
            "url": url,
            "category": "DICTIONARY_TRANSLATION",
            "metadata": {
                "term": term,
                "canonical_url": url,
                "domain": "islamic-content.com"
            }
        }
