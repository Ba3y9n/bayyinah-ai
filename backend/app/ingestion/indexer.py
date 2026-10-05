"""
Bayyinah AI - Knowledge Base Indexer
Persists normalized chunks, computes PostgreSQL tsvector, and registers pgvector embeddings.
"""

import json
import uuid
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

logger = logging.getLogger("bayyinah.ingestion.indexer")

class KnowledgeIndexer:
    """
    Direct database indexer for Supabase PostgreSQL and local fallback.
    """

    def index_document_and_chunks(
        self, 
        db: Session, 
        document_data: Dict[str, Any], 
        chunks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        doc_id = document_data.get("id") or str(uuid.uuid4())
        source_id = document_data.get("source_id")

        # 1. Insert or update document
        insert_doc_sql = text("""
            INSERT INTO documents (
                id, source_id, title, title_ar, title_en, content, content_ar,
                author, publisher, document_type, category, reference, url,
                original_url, official_url, canonical_url, language,
                publication_date, rights_status, content_hash, version, metadata
            ) VALUES (
                :id, :source_id, :title, :title_ar, :title_en, :content, :content_ar,
                :author, :publisher, :document_type, :category, :reference, :url,
                :original_url, :official_url, :canonical_url, :language,
                :publication_date, :rights_status, :content_hash, :version, CAST(:metadata AS jsonb)
            )
            ON CONFLICT (id) DO UPDATE SET
                title = EXCLUDED.title,
                content = EXCLUDED.content,
                updated_at = now();
        """)
        
        db.execute(insert_doc_sql, {
            "id": doc_id,
            "source_id": source_id,
            "title": document_data.get("title") or document_data.get("title_ar"),
            "title_ar": document_data.get("title_ar") or document_data.get("title"),
            "title_en": document_data.get("title_en"),
            "content": document_data.get("content"),
            "content_ar": document_data.get("content_ar") or document_data.get("content"),
            "author": document_data.get("author"),
            "publisher": document_data.get("publisher"),
            "document_type": document_data.get("document_type", "ARTICLE"),
            "category": document_data.get("category", "GENERAL"),
            "reference": document_data.get("reference"),
            "url": document_data.get("url"),
            "original_url": document_data.get("original_url") or document_data.get("url"),
            "official_url": document_data.get("official_url") or document_data.get("url"),
            "canonical_url": document_data.get("canonical_url") or document_data.get("url"),
            "language": document_data.get("language", "ar"),
            "publication_date": document_data.get("publication_date"),
            "rights_status": document_data.get("rights_status", "PUBLIC_ACCESS"),
            "content_hash": document_data.get("content_hash"),
            "version": document_data.get("version", "1.0"),
            "metadata": json.dumps(document_data.get("metadata", {}), default=str)
        })

        # 2. Insert Chunks with pgvector and FTS vector
        indexed_chunks_count = 0
        for chunk in chunks:
            chunk_id = chunk.get("id") or str(uuid.uuid4())
            emb = chunk.get("embedding")
            vec_str = None
            if emb and isinstance(emb, list) and len(emb) == 768:
                vec_str = "[" + ",".join(str(float(x)) for x in emb) + "]"

            content_text = chunk.get("content") or chunk.get("chunk_text") or ""
            norm_text = chunk.get("normalized_content") or chunk.get("normalized_text") or content_text

            insert_chunk_sql = text("""
                INSERT INTO document_chunks (
                    id, document_id, chunk_index, content, content_ar, normalized_content,
                    chunk_text, normalized_text, section, section_title, reference,
                    locator, source_locator, content_hash, version,
                    embedding, search_vector, metadata
                ) VALUES (
                    :id, :document_id, :chunk_index, :content, :content_ar, :normalized_content,
                    :chunk_text, :normalized_text, :section, :section_title, :reference,
                    :locator, :source_locator, :content_hash, :version,
                    CAST(:vector_str AS vector), to_tsvector('simple', :norm_text), CAST(:metadata AS jsonb)
                )
                ON CONFLICT (id) DO UPDATE SET
                    content = EXCLUDED.content,
                    search_vector = EXCLUDED.search_vector,
                    embedding = EXCLUDED.embedding,
                    updated_at = now();
            """)

            db.execute(insert_chunk_sql, {
                "id": chunk_id,
                "document_id": doc_id,
                "chunk_index": chunk.get("chunk_index", 0),
                "content": content_text,
                "content_ar": chunk.get("content_ar") or content_text,
                "normalized_content": norm_text,
                "chunk_text": content_text,
                "normalized_text": norm_text,
                "section": chunk.get("section"),
                "section_title": chunk.get("section_title"),
                "reference": chunk.get("reference"),
                "locator": chunk.get("locator"),
                "source_locator": chunk.get("source_locator"),
                "content_hash": chunk.get("content_hash"),
                "version": chunk.get("version", "1.0"),
                "vector_str": vec_str,
                "norm_text": norm_text,
                "metadata": json.dumps(chunk.get("metadata", {}), default=str)
            })
            indexed_chunks_count += 1

        db.commit()
        return {
            "success": True,
            "document_id": doc_id,
            "chunks_indexed": indexed_chunks_count
        }

knowledge_indexer = KnowledgeIndexer()
