"""
Bayyinah AI - Batch Embedding Generation Worker
Generates 768-dimensional embeddings for knowledge base chunks with retry and fallback.
"""

from typing import List, Dict, Any
import logging
from ..services.gemini_service import gemini_service
from ..config import settings

logger = logging.getLogger("bayyinah.ingestion.embeddings")

class EmbeddingWorker:
    """
    Manages vector embeddings generation in batches, ensuring dimension compatibility (768-d).
    """

    def __init__(self, target_dim: int = 768):
        self.target_dim = target_dim

    def process_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        processed = []
        for chunk in chunks:
            text_to_embed = chunk.get("normalized_content") or chunk.get("content") or chunk.get("chunk_text") or ""
            if not text_to_embed.strip():
                chunk["embedding"] = None
                processed.append(chunk)
                continue

            try:
                emb = gemini_service.generate_embedding(text_to_embed)
                if len(emb) == self.target_dim:
                    chunk["embedding"] = emb
                    chunk["embedding_model"] = settings.GEMINI_EMBEDDING_MODEL
                else:
                    logger.warning(f"Embedding dimension mismatch: got {len(emb)}, expected {self.target_dim}")
                    chunk["embedding"] = None
            except Exception as e:
                logger.error(f"Failed to generate embedding for chunk {chunk.get('chunk_index')}: {e}")
                chunk["embedding"] = None

            processed.append(chunk)
        return processed

embedding_worker = EmbeddingWorker(target_dim=settings.EMBEDDING_DIMENSION)
