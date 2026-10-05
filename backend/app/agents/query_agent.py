from typing import List, Dict, Any
from ..utils.arabic_normalizer import normalize_arabic, tokenize_arabic

class QueryAgent:
    """
    AI JOB 3: Evidence Search Query Generator
    Generates exact phrase, normalized, arabic keyword, reference, and semantic queries.
    """
    def __init__(self):
        pass

    def generate_queries(self, claim_data: Dict[str, Any]) -> List[str]:
        from ..services.gemini_service import gemini_service, ClaimExtraction
        claim_obj = ClaimExtraction(**claim_data)
        return gemini_service.generate_queries_structured(claim_obj)

        # 1. Exact phrase query
        queries.append(raw.strip())

        # 2. Normalized query
        if norm and norm != raw:
            queries.append(norm)

        # 3. Arabic keyword query
        if tokens:
            kw_query = " ".join(tokens[:7])
            if kw_query not in queries:
                queries.append(kw_query)

        # 4. Reference query based on claim type
        if claim_type == "Hadith":
            queries.append(f"تخريج متن حديث {' '.join(tokens[:5])}")
        elif claim_type == "Quran":
            queries.append(f"نص سورة آية {' '.join(tokens[:5])}")
        elif claim_type == "Fiqh":
            queries.append(f"حكم مسألة {' '.join(tokens[:5])}")
        elif claim_type == "Seerah":
            queries.append(f"سيرة نبوية {' '.join(tokens[:5])}")
        elif claim_type == "PersonalCase":
            queries.append("ضوابط الفتوى والأحوال الشخصية")

        # 5. Semantic core query
        if len(tokens) > 2:
            semantic_query = " ".join(tokens[:4])
            if semantic_query not in queries:
                queries.append(semantic_query)

        return queries

query_agent = QueryAgent()
