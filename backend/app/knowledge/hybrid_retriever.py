"""
Bayyinah AI - Supabase & PostgreSQL Hybrid Retriever (Section 38 & 39)
Fuses:
1. Exact Substring Search (ILIKE)
2. Arabic Normalized Keyword Search
3. PostgreSQL Full-Text Search (ts_rank_cd on search_vector)
4. pgvector Semantic Cosine Similarity (vector(768) <=> query_embedding)
5. Metadata & Authority Level Filtering
6. Reciprocal Rank Fusion (RRF) algorithm
"""

import time
from typing import List, Dict, Any, Optional
from .supabase_client import supabase_client
from ..utils.arabic_normalizer import normalize_arabic, tokenize_arabic
from ..models.knowledge_schemas import (
    KnowledgeSearchRequest,
    KnowledgeSearchResultItem,
    KnowledgeSearchResponse,
    EvidenceType,
    VerificationStatus,
    ProvenanceInfo
)

class HybridRetriever:
    """
    Production Hybrid Retrieval Engine powered by PostgreSQL and pgvector.
    Combines lexical, keyword, FTS, and vector channels with RRF score aggregation.
    """

    def __init__(self):
        self.k_rrf: float = 60.0

    def generate_embedding(self, text_input: str) -> Optional[List[float]]:
        """
        Generates 768-dimensional text embedding via Gemini API text-embedding-004.
        """
        from ..services.gemini_service import gemini_service
        if not text_input or not text_input.strip():
            return None
        return gemini_service.generate_embedding(text_input)

    def retrieve(
        self,
        query: str,
        category: Optional[str] = "all",
        top_k: int = 10,
        query_embedding: Optional[List[float]] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes parallel multi-channel retrieval and fuses candidates with RRF.
        """
        start_time = time.time()
        norm_query = normalize_arabic(query)
        cat_filter = category if category and category.lower() != "all" else None

        # 1. Exact & Trigram Keyword Search
        exact_results = supabase_client.exact_keyword_search(query, top_k=top_k * 2, category=cat_filter)

        # 2. PostgreSQL Full-Text Search
        fts_results = supabase_client.fts_search(query, top_k=top_k * 2, category=cat_filter)

        # 3. pgvector Semantic Search
        if query_embedding is None:
            query_embedding = self.generate_embedding(query)

        vector_results = []
        if query_embedding:
            vector_results = supabase_client.vector_search(query_embedding, top_k=top_k * 2, category=cat_filter)

        # 4. Reciprocal Rank Fusion (RRF)
        # RRF_score(d) = sum( weight * (1 / (k + rank)) )
        fused_map: Dict[str, Dict[str, Any]] = {}

        def add_channel_rankings(results_list: List[Dict[str, Any]], channel: str, weight: float = 1.0):
            for rank, item in enumerate(results_list):
                c_id = str(item.get("chunk_id"))
                if c_id not in fused_map:
                    fused_map[c_id] = {
                        "item": item,
                        "exact_score": 0.0,
                        "fts_score": 0.0,
                        "vector_score": 0.0,
                        "rrf_score": 0.0,
                        "channels_matched": []
                    }
                score_val = item.get("exact_score") or item.get("fts_score") or item.get("similarity_score") or 0.0
                fused_map[c_id][f"{channel}_score"] = float(score_val)
                fused_map[c_id]["rrf_score"] += weight * (1.0 / (self.k_rrf + rank + 1))
                fused_map[c_id]["channels_matched"].append(channel)

        add_channel_rankings(exact_results, "exact", weight=1.5)
        add_channel_rankings(fts_results, "fts", weight=1.2)
        add_channel_rankings(vector_results, "vector", weight=1.0)

        # Sort candidates by final RRF score
        candidates = list(fused_map.values())
        candidates.sort(key=lambda x: x["rrf_score"], reverse=True)

        final_items = []
        for cand in candidates[:top_k]:
            raw = cand["item"]
            exact_s = cand["exact_score"]
            fts_s = cand["fts_score"]
            vec_s = cand["vector_score"]
            relevance = max(exact_s, vec_s, min(fts_s / 2.0, 1.0))

            # Determine Evidence Support Level
            if exact_s >= 0.85 or relevance >= 0.75:
                support_lvl = "DIRECT_SUPPORT"
                ver_status = "VERIFIED"
            elif relevance >= 0.40:
                support_lvl = "PARTIAL_SUPPORT"
                ver_status = "VERIFIED"
            else:
                support_lvl = "CONTEXT_SUPPORT"
                ver_status = "INSUFFICIENT"

            chunk_text = raw.get("chunk_text", "")
            if "باطل" in chunk_text or "موضوع" in chunk_text or "لا أصل له" in chunk_text:
                ver_status = "FABRICATED"
                support_lvl = "CONTRADICTING"
            elif "ضعيف" in chunk_text or "لا يصح" in chunk_text:
                ver_status = "WEAK"
                support_lvl = "CONTRADICTING"
            elif "محل خلاف" in chunk_text or "خلاف معتبر" in chunk_text or "أسباب اختلاف" in chunk_text:
                ver_status = "CONFLICT"
                support_lvl = "CONTEXT_SUPPORT"

            final_items.append({
                "chunk_id": raw.get("chunk_id"),
                "document_id": raw.get("document_id"),
                "source_id": raw.get("source_id"),
                "source_name": raw.get("source_name"),
                "source_url": raw.get("source_official_url"),
                "document_title": raw.get("document_title"),
                "document_category": raw.get("document_category"),
                "chunk_text": chunk_text,
                "reference": raw.get("reference") or raw.get("locator") or "",
                "locator": raw.get("locator") or "",
                "canonical_url": raw.get("canonical_url") or raw.get("source_url"),
                "content_hash": raw.get("content_hash"),
                "scores": {
                    "exact": round(exact_s, 3),
                    "fts": round(fts_s, 3),
                    "vector": round(vec_s, 3),
                    "rrf": round(cand["rrf_score"], 4),
                    "relevance": round(relevance, 3)
                },
                "support_level": support_lvl,
                "verification_status": ver_status,
                "scientific_status": raw.get("scientific_status"),
                "license_status": raw.get("license_status")
            })

        return final_items

hybrid_retriever = HybridRetriever()
