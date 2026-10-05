"""
Bayyinah AI - Dorar Fiqh Adapter
Implements Section 12 of Master Specifications:
Strict extraction from Dorar Al-Saniyyah Fiqh Encyclopedia:
- Fiqh issue (المسألة الفقهية)
- Views of Islamic Schools of Thought (المذاهب الأربعة)
- Presence of scholarly disagreement (اختلاف معتبر / إجماع / ترجيح)
- Canonical references
"""

from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import re
from .base_adapter import BaseSourceAdapter

class DorarFiqhAdapter(BaseSourceAdapter):
    def parse(self, raw_html: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(raw_html, "html.parser")
        for s in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            s.decompose()

        title = soup.title.string.strip() if soup.title else "الموسوعة الفقهية - الدرر السنية"
        full_text = soup.get_text(separator=' ', strip=True)

        # Detect divergence vs consensus
        has_disagreement = False
        disagreement_terms = ["اختلف", "الجمهور", "وفيها قولان", "ذهب الحنفية", "ذهب المالكية", "ذهب الشافعية", "ذهب الحنابلة", "القول الأول", "القول الثاني"]
        for term in disagreement_terms:
            if term in full_text:
                has_disagreement = True
                break

        has_consensus = "إجماع" in full_text or "اتفاق المذاهب الأربعة" in full_text or "لا خلاف" in full_text

        madhab_opinions = []
        for madhab in ["الحنفية", "المالكية", "الشافعية", "الحنابلة"]:
            if madhab in full_text:
                madhab_opinions.append(madhab)

        reference = f"الموسوعة الفقهية المحررة - الدرر السنية: {title}"

        return {
            "title": title,
            "content": full_text[:3500],
            "has_disagreement": has_disagreement,
            "has_consensus": has_consensus,
            "cited_schools": madhab_opinions,
            "reference": reference,
            "source_id": self.source_id,
            "source_name": self.name_ar,
            "url": url,
            "category": "FIQH",
            "metadata": {
                "has_disagreement": has_disagreement,
                "has_consensus": has_consensus,
                "schools": madhab_opinions,
                "canonical_url": url,
                "domain": "dorar.net"
            }
        }
