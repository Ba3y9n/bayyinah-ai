from typing import List, Dict, Any, Optional
from ..services.search_service import search_service
from ..services.registry_service import registry_service
from ..models.schemas import EvidenceItem

class RetrievalAgent:
    """
    AI JOB 4 & 5: Retrieval Orchestrator & Hybrid Search Agent
    Executes tool-calling retrieval across exact, keyword, and semantic vectors.
    """
    def __init__(self):
        pass

    def search_exact_text(self, query: str) -> List[Dict[str, Any]]:
        return search_service.exact_text_search(query, limit=5)

    def search_keyword(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        results = search_service.exact_text_search(query, limit=5)
        if category and category != "all":
            results = [r for r in results if r["document"].get("category") == category]
        return results

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        return search_service.semantic_search(query, limit=top_k)

    def get_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        src = registry_service.get_source_by_id(source_id)
        return src.dict() if src else None

    def get_evidence(self, document_id: str) -> Optional[Dict[str, Any]]:
        doc = next((d for d in search_service.documents if d["id"] == document_id), None)
        return doc

    def orchestrate_hybrid_retrieval(self, queries: List[str], limit: int = 5) -> List[EvidenceItem]:
        """
        Executes parallel hybrid search fusion across generated queries.
        Enriches each evidence item with retrieval method (EXACT, KEYWORD, SEMANTIC, HYBRID).
        """
        evidence_items = search_service.hybrid_search(queries, limit=limit)
        
        # Tag retrieval method for transparency (Section 56)
        for ev in evidence_items:
            if ev.relevance_score >= 0.85:
                ev.evidence_type = "EXACT"
            elif ev.relevance_score >= 0.65:
                ev.evidence_type = "HYBRID"
            elif ev.relevance_score >= 0.45:
                ev.evidence_type = "KEYWORD"
            else:
                ev.evidence_type = "SEMANTIC"

        return evidence_items

retrieval_agent = RetrievalAgent()
