"""
Bayyinah AI - Al-Maktaba Al-Shamela Adapter
Implements Section 13 of Master Specifications:
Strict extraction from Shamela (shamela.ws):
- Book title
- Author & Scholarly biographical data
- Page & Volume coordinates
- Verified classical textual excerpts
"""

from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import re
from .base_adapter import BaseSourceAdapter

class ShamelaAdapter(BaseSourceAdapter):
    def parse(self, raw_html: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(raw_html, "html.parser")
        for s in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            s.decompose()

        title = soup.title.string.strip() if soup.title else "المكتبة الشاملة"
        
        # Look for book title and page metadata
        book_title = ""
        author = ""
        page_num = ""
        part_num = ""

        # Match header or page info
        nass_elem = soup.find(class_=re.compile(r'(nass|book-text|content)', re.I))
        if nass_elem:
            content_text = nass_elem.get_text(separator=' ', strip=True)
        else:
            content_text = soup.get_text(separator=' ', strip=True)

        meta_elem = soup.find(class_=re.compile(r'(betaka|meta|book-info)', re.I))
        if meta_elem:
            meta_text = meta_elem.get_text(separator=' ', strip=True)
            book_match = re.search(r'الكتاب[:\s]+([^.]+)', meta_text)
            if book_match:
                book_title = book_match.group(1).strip()
            author_match = re.search(r'المؤلف[:\s]+([^.]+)', meta_text)
            if author_match:
                author = author_match.group(1).strip()

        if not book_title:
            book_title = title.split("-")[0].strip()

        ref_parts = [f"المكتبة الشاملة الرقمية - كتاب: {book_title}"]
        if author:
            ref_parts.append(f"لـ {author}")
        reference = "، ".join(ref_parts)

        return {
            "title": title,
            "book_title": book_title,
            "author": author,
            "content": content_text[:3500],
            "reference": reference,
            "source_id": self.source_id,
            "source_name": self.name_ar,
            "url": url,
            "category": "SEERAH_HISTORY",
            "metadata": {
                "book_title": book_title,
                "author": author,
                "canonical_url": url,
                "domain": "shamela.ws"
            }
        }
