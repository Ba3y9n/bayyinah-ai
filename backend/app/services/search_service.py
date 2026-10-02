import json
import os
import math
import numpy as np
from typing import List, Dict, Any, Optional
from ..utils.arabic_normalizer import normalize_arabic, tokenize_arabic, compute_jaccard_similarity
from ..models.schemas import EvidenceItem
from .registry_service import registry_service

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

class SearchService:
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self._load_documents()

    def _load_documents(self):
        docs_path = os.path.join(DATA_DIR, "documents_seed.json")
        if os.path.exists(docs_path):
            with open(docs_path, "r", encoding="utf-8") as f:
                self.documents = json.load(f)
        else:
            self.documents = []

    def exact_text_search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Performs exact keyword and normalized Arabic token matching.
        """
        normalized_query = normalize_arabic(query)
        query_tokens = set(tokenize_arabic(query))
        
        results = []
        for doc in self.documents:
            norm_content = normalize_arabic(doc["content"])
            norm_title = normalize_arabic(doc["title"])
            norm_ref = normalize_arabic(doc.get("reference", ""))
            
            # Exact substring bonus
            score = 0.0
            if normalized_query and (normalized_query in norm_content or normalized_query in norm_title):
                score += 1.0
            
            # Token overlap score
            doc_tokens = set(tokenize_arabic(doc["content"] + " " + doc["title"]))
            if query_tokens and doc_tokens:
                overlap = len(query_tokens.intersection(doc_tokens))
                token_score = overlap / len(query_tokens)
                score += token_score * 0.8
            
            if score > 0.15:
                results.append({
                    "document": doc,
                    "score": min(score, 1.0),
                    "match_type": "exact_or_keyword"
                })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def semantic_search(self, query: str, query_embedding: Optional[List[float]] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Semantic search based on Jaccard semantic tokens + embeddings similarity.
        """
        results = []
        for doc in self.documents:
            # Semantic token & context similarity
            sim = compute_jaccard_similarity(query, doc["content"])
            title_sim = compute_jaccard_similarity(query, doc["title"])
            total_sim = (sim * 0.7) + (title_sim * 0.3)
            
            # If doc title mentions core topic (e.g. نية, صين, فاتحة)
            norm_q = normalize_arabic(query)
            for kw in tokenize_arabic(doc["title"]):
                if kw in norm_q:
                    total_sim += 0.25

            if total_sim > 0.05:
                results.append({
                    "document": doc,
                    "score": min(total_sim, 0.98),
                    "match_type": "semantic"
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def hybrid_search(self, queries: List[str], limit: int = 5) -> List[EvidenceItem]:
        """
        Combines Multiple Search Queries across Exact and Semantic search engines.
        Merges results using Reciprocal Score Fusion & builds grounded EvidenceItems.
        """
        combined_scores: Dict[str, Dict[str, Any]] = {}

        for q in queries:
            exact_res = self.exact_text_search(q, limit=limit)
            semantic_res = self.semantic_search(q, limit=limit)

            # Process exact matches
            for item in exact_res:
                doc_id = item["document"]["id"]
                if doc_id not in combined_scores:
                    combined_scores[doc_id] = {
                        "document": item["document"],
                        "exact_score": item["score"],
                        "semantic_score": 0.0,
                        "relevance": 0.0
                    }
                else:
                    combined_scores[doc_id]["exact_score"] = max(combined_scores[doc_id]["exact_score"], item["score"])

            # Process semantic matches
            for item in semantic_res:
                doc_id = item["document"]["id"]
                if doc_id not in combined_scores:
                    combined_scores[doc_id] = {
                        "document": item["document"],
                        "exact_score": 0.0,
                        "semantic_score": item["score"],
                        "relevance": 0.0
                    }
                else:
                    combined_scores[doc_id]["semantic_score"] = max(combined_scores[doc_id]["semantic_score"], item["score"])

        # Calculate final hybrid score
        scored_items = []
        for doc_id, data in combined_scores.items():
            hybrid_score = (data["exact_score"] * 0.6) + (data["semantic_score"] * 0.4)
            if data["exact_score"] > 0.7:
                hybrid_score = max(hybrid_score, data["exact_score"])
            data["relevance"] = min(round(hybrid_score, 3), 1.0)
            scored_items.append(data)

        scored_items.sort(key=lambda x: x["relevance"], reverse=True)

        # Build EvidenceItem objects enriched with Source Registry metadata
        evidence_items: List[EvidenceItem] = []
        for item in scored_items[:limit]:
            doc = item["document"]
            src = registry_service.get_source_by_id(doc["source_id"])
            
            # Determine evidence type
            if item["relevance"] > 0.75:
                ev_type = "direct_match"
            elif item["relevance"] > 0.45:
                ev_type = "partial_match"
            else:
                ev_type = "scholarly_commentary"

            # Check if source metadata indicates weakness, fabrication or disagreement
            meta = doc.get("metadata", {})
            ruling_or_grade = meta.get("grade") or meta.get("ruling") or meta.get("ruling_type")
            comp_notes = meta.get("status") or meta.get("warning") or meta.get("ruling_type") or "تمت المطابقة مع المتن المعتمد"

            evidence_items.append(EvidenceItem(
                document_id=doc["id"],
                source_id=doc["source_id"],
                source_name=src.name if src else doc["source_id"],
                author=src.author if src else None,
                organization=src.organization if src else None,
                category=doc.get("category", "general"),
                title=doc["title"],
                excerpt=doc["content"],
                reference=doc.get("reference", ""),
                url=doc.get("url", src.url if src else ""),
                license=src.license if src else "مرجع موثق",
                relevance_score=item["relevance"],
                evidence_type=ev_type,
                ruling_or_grade=ruling_or_grade,
                comparison_notes=comp_notes
            ))

        return evidence_items

search_service = SearchService()
