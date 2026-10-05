"""
Bayyinah AI - Intelligent Islamic Text Chunker
Splits Islamic texts while preserving verse, hadith, and section boundaries.
"""

import re
import hashlib
from typing import List, Dict, Any
from ..utils.arabic_normalizer import normalize_arabic

class IslamicTextChunker:
    """
    Context-aware chunker for Quranic verses, Hadith narrations,
    and scholarly treatises. Preserves references and semantic integrity.
    """

    def __init__(self, target_chunk_size: int = 500, overlap: int = 80):
        self.target_chunk_size = target_chunk_size
        self.overlap = overlap

    def chunk_document(self, text: str, doc_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not text or not text.strip():
            return []

        # Check if text contains structured delimiter (e.g. paragraphs or numbered hadiths)
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks = []
        chunk_idx = 0

        for p in paragraphs:
            if len(p) <= self.target_chunk_size:
                c_hash = hashlib.sha256(p.encode("utf-8")).hexdigest()
                chunks.append({
                    "chunk_index": chunk_idx,
                    "content": p,
                    "content_ar": p,
                    "normalized_content": normalize_arabic(p),
                    "chunk_text": p,
                    "normalized_text": normalize_arabic(p),
                    "reference": doc_metadata.get("reference") or f"الفقرة {chunk_idx + 1}",
                    "locator": f"p-{chunk_idx + 1}",
                    "source_locator": f"Section {chunk_idx + 1}",
                    "content_hash": c_hash,
                    "metadata": {
                        "category": doc_metadata.get("category", "GENERAL"),
                        "doc_title": doc_metadata.get("title", "")
                    }
                })
                chunk_idx += 1
            else:
                # Subdivide long paragraph into sentences
                sentences = re.split(r'([.؛!؟\n]+)', p)
                current_chunk = ""
                for s in sentences:
                    if len(current_chunk) + len(s) > self.target_chunk_size and current_chunk:
                        c_hash = hashlib.sha256(current_chunk.strip().encode("utf-8")).hexdigest()
                        chunks.append({
                            "chunk_index": chunk_idx,
                            "content": current_chunk.strip(),
                            "content_ar": current_chunk.strip(),
                            "normalized_content": normalize_arabic(current_chunk.strip()),
                            "chunk_text": current_chunk.strip(),
                            "normalized_text": normalize_arabic(current_chunk.strip()),
                            "reference": doc_metadata.get("reference") or f"الفقرة {chunk_idx + 1}",
                            "locator": f"p-{chunk_idx + 1}",
                            "source_locator": f"Section {chunk_idx + 1}",
                            "content_hash": c_hash,
                            "metadata": {
                                "category": doc_metadata.get("category", "GENERAL"),
                                "doc_title": doc_metadata.get("title", "")
                            }
                        })
                        chunk_idx += 1
                        current_chunk = s
                    else:
                        current_chunk += s

                if current_chunk.strip():
                    c_hash = hashlib.sha256(current_chunk.strip().encode("utf-8")).hexdigest()
                    chunks.append({
                        "chunk_index": chunk_idx,
                        "content": current_chunk.strip(),
                        "content_ar": current_chunk.strip(),
                        "normalized_content": normalize_arabic(current_chunk.strip()),
                        "chunk_text": current_chunk.strip(),
                        "normalized_text": normalize_arabic(current_chunk.strip()),
                        "reference": doc_metadata.get("reference") or f"الفقرة {chunk_idx + 1}",
                        "locator": f"p-{chunk_idx + 1}",
                        "source_locator": f"Section {chunk_idx + 1}",
                        "content_hash": c_hash,
                        "metadata": {
                            "category": doc_metadata.get("category", "GENERAL"),
                            "doc_title": doc_metadata.get("title", "")
                        }
                    })
                    chunk_idx += 1

        return chunks

chunker = IslamicTextChunker()
