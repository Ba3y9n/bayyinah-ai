"""
Bayyinah AI - End-to-End Ingestion Pipeline
Orchestrates: Source -> Document -> Chunking -> Embedding -> FTS -> pgvector Indexing.
"""

from typing import Dict, Any, List
from sqlalchemy.orm import Session
import logging

from .source_manager import source_manager
from .license_checker import license_checker
from .document_ingestor import document_ingestor
from .chunker import chunker
from .embedding_worker import embedding_worker
from .indexer import knowledge_indexer

logger = logging.getLogger("bayyinah.ingestion.pipeline")

class IngestionPipeline:
    """
    Production ingestion pipeline for authentic Islamic sources.
    """

    def ingest_document(
        self, 
        db: Session, 
        source_data: Dict[str, Any], 
        document_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        # 1. License & Rights Check
        allowed, reason = license_checker.check_permissions(source_data)
        if not allowed:
            logger.error(f"Ingestion rejected: {reason}")
            return {"success": False, "error": f"Permission denied: {reason}"}

        # 2. Register or fetch Source
        source_id = source_manager.get_or_create_source(db, source_data)

        # 3. Clean and prepare Document
        prep_doc, raw_text = document_ingestor.prepare_document(document_data, source_id)

        # 4. Chunk document
        doc_chunks = chunker.chunk_document(raw_text, prep_doc)
        if not doc_chunks:
            return {"success": False, "error": "Document contains no readable text."}

        # 5. Generate 768-d Vector Embeddings
        chunks_with_embeddings = embedding_worker.process_chunks(doc_chunks)

        # 6. Index into Supabase PostgreSQL (pgvector + FTS)
        index_result = knowledge_indexer.index_document_and_chunks(db, prep_doc, chunks_with_embeddings)

        return {
            "success": True,
            "source_id": source_id,
            "document_id": index_result.get("document_id"),
            "chunks_count": index_result.get("chunks_indexed")
        }

ingestion_pipeline = IngestionPipeline()
