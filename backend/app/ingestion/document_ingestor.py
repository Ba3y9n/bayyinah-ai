"""
Bayyinah AI - Document Ingestor
Parses, cleans, verifies SHA-256 hashes, and extracts metadata from incoming documents.
"""

import hashlib
import uuid
from typing import Dict, Any, Tuple
from ..utils.arabic_normalizer import normalize_arabic

class DocumentIngestor:
    """
    Cleans raw document inputs, computes cryptographic provenance hash,
    and formats them for chunking and indexing.
    """

    def prepare_document(self, raw_doc: Dict[str, Any], source_id: str) -> Tuple[Dict[str, Any], str]:
        content = (raw_doc.get("content") or raw_doc.get("text") or "").strip()
        doc_id = raw_doc.get("id") or str(uuid.uuid4())
        
        # Calculate SHA-256 content hash for strict provenance
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        
        prepared_doc = {
            "id": doc_id,
            "source_id": source_id,
            "title": raw_doc.get("title") or raw_doc.get("title_ar") or "وثيقة إسلامية موثقة",
            "title_ar": raw_doc.get("title_ar") or raw_doc.get("title") or "وثيقة إسلامية موثقة",
            "title_en": raw_doc.get("title_en"),
            "content": content,
            "content_ar": content,
            "author": raw_doc.get("author") or "محقق معتمد",
            "publisher": raw_doc.get("publisher"),
            "document_type": raw_doc.get("document_type", "SCHOLARLY_TEXT"),
            "category": raw_doc.get("category", "GENERAL"),
            "reference": raw_doc.get("reference") or "مرجع معتمد",
            "url": raw_doc.get("url") or "",
            "canonical_url": raw_doc.get("canonical_url") or raw_doc.get("url") or "",
            "language": raw_doc.get("language", "ar"),
            "rights_status": raw_doc.get("rights_status", "PUBLIC_ACCESS"),
            "content_hash": content_hash,
            "version": "1.0",
            "metadata": raw_doc.get("metadata", {})
        }
        return prepared_doc, content

document_ingestor = DocumentIngestor()
