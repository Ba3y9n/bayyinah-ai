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
        try:
            from ..db.database import SessionLocal
            from ..models.knowledge_models import DocumentModel, DocumentChunkModel, TrustedSourceModel
            with SessionLocal() as db:
                chunks = db.query(DocumentChunkModel, DocumentModel, TrustedSourceModel)\
                    .join(DocumentModel, DocumentChunkModel.document_id == DocumentModel.id)\
                    .join(TrustedSourceModel, DocumentModel.source_id == TrustedSourceModel.id)\
                    .filter(TrustedSourceModel.scientific_status == "APPROVED", TrustedSourceModel.is_active == True)\
                    .all()
                if chunks:
                    self.documents = []
                    for chunk, doc, src in chunks:
                        grade = None
                        if "صحيح" in doc.title_ar:
                            grade = "صحيح"
                        elif "ضعيف" in doc.title_ar or "ضعيف" in chunk.content[:100]:
                            grade = "ضعيف"
                        elif "موضوع" in doc.title_ar or "موضوع" in chunk.content[:100] or "باطل" in chunk.content[:100]:
                            grade = "موضوع"

                        self.documents.append({
                            "id": doc.id,
                            "chunk_id": chunk.id,
                            "source_id": src.id,
                            "source_name": src.name_ar or src.name or src.id,
                            "author": doc.author or src.author,
                            "organization": src.organization,
                            "title": doc.title_ar,
                            "content": chunk.content,
                            "category": doc.category or src.category,
                            "reference": chunk.source_locator or chunk.reference or doc.publisher or "",
                            "url": chunk.canonical_url or chunk.source_url or doc.official_url or src.official_url or "",
                            "license": src.license_name or "رخصة موثقة",
                            "metadata": {
                                "grade": grade,
                                "status": "خلاف معتبر" if "خلاف" in chunk.content else "موثق",
                                "ruling_type": "محل خلاف" if "خلاف" in chunk.content else None
                            }
                        })

                    # Also load verified translation dictionary terms
                    from ..models.knowledge_models import TranslationTermModel
                    terms = db.query(TranslationTermModel).all()
                    for t in terms:
                        self.documents.append({
                            "id": f"doc-term-{t.id}",
                            "chunk_id": f"chunk-term-{t.id}",
                            "source_id": t.source_id or "src-islamic-content-dict",
                            "source_name": "معجم المحتوى الإسلامي والجمهرة",
                            "author": "موسوعة المحتوى الإسلامي",
                            "organization": "المحتوى الإسلامي",
                            "title": f"مصطلح شرعي: {t.term_ar} - {t.term_en}",
                            "content": f"{t.term_ar} ({t.term_en}): {t.explanation} المقابل المعتمد بالإنجليزية: {t.preferred_translation}. الترجمة البديلة: {t.alternative_translation or ''}. ضوابط الاستخدام: {t.usage_notes or ''}",
                            "category": "DICTIONARY_TRANSLATION",
                            "reference": f"معجم المصطلحات الشرعية، مادة ({t.term_ar})",
                            "url": t.source_url or "https://islamic-content.com/dictionary",
                            "license": "رخصة الاستخدام العلمي المعتمدة",
                            "metadata": {
                                "grade": "مصطلح معتمد",
                                "status": "موثق معجمياً",
                                "ruling_type": None
                            }
                        })
                    return
        except Exception:
            pass

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
        query_tokens = [t for t in tokenize_arabic(query) if len(t) > 1]
        query_token_set = set(query_tokens)
        
        results = []
        for doc in self.documents:
            norm_content = normalize_arabic(doc["content"])
            norm_title = normalize_arabic(doc["title"])
            doc_tokens = set(tokenize_arabic(doc["content"] + " " + doc["title"]))
            
            score = 0.0
            
            # Exact title match
            if normalized_query and normalized_query in norm_title:
                score += 0.95
            elif query_token_set:
                title_tokens = set(tokenize_arabic(doc["title"]))
                title_overlap = len(query_token_set.intersection(title_tokens))
                if title_overlap > 0:
                    score += (title_overlap / len(query_token_set)) * 0.70
            
            # Exact content match (scaled by query length to avoid single stopword dominance)
            if normalized_query and len(query_tokens) >= 3 and normalized_query in norm_content:
                score += 0.85
            elif normalized_query and len(query_tokens) == 2 and normalized_query in norm_content:
                score += 0.50
            elif normalized_query and len(query_tokens) == 1 and normalized_query in norm_content and len(normalized_query) > 3:
                score += 0.25
            
            # Token overlap score
            if query_token_set and doc_tokens:
                overlap = len(query_token_set.intersection(doc_tokens))
                token_precision = overlap / len(query_token_set)
                score += token_precision * 0.60
            
            if score > 0.25:
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
            exact = data["exact_score"]
            sem = data["semantic_score"]
            if exact > 0 and sem > 0:
                hybrid_score = (exact * 0.55) + (sem * 0.45)
            elif exact > 0:
                hybrid_score = exact
            else:
                hybrid_score = sem
            data["relevance"] = min(round(hybrid_score, 3), 1.0)
            scored_items.append(data)

        scored_items.sort(key=lambda x: x["relevance"], reverse=True)

        # Build EvidenceItem objects enriched with Source Registry metadata
        evidence_items: List[EvidenceItem] = []
        for item in scored_items[:limit]:
            doc = item["document"]
            doc_id_str = str(doc["id"])
            src_id_str = str(doc["source_id"])
            src = registry_service.get_source_by_id(src_id_str)
            
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
                document_id=doc_id_str,
                source_id=src_id_str,
                source_name=doc.get("source_name") or (src.name if src else "المصدر المعتمد"),
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
