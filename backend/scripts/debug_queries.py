import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.gemini_service import ClaimExtraction
from app.agents.query_agent import query_agent
from app.services.search_service import search_service

data = {
    "main_claim": "الله لا إله إلا هو الحي القيوم لا تأخذه سنة ولا نوم",
    "context": "",
    "type": "Quran",
    "speaker_or_author": None,
    "confidence": 0.95,
    "requires_specialist": False,
    "is_personal_fatwa": False,
    "is_court_dispute": False,
    "is_inheritance": False,
    "is_divorce": False
}
queries = query_agent.generate_queries(data)
print("Generated queries:", queries)

for q in queries:
    exact = search_service.exact_text_search(q, limit=3)
    sem = search_service.semantic_search(q, limit=3)
    print(f"\nQuery: '{q}'")
    print("  Exact count:", len(exact), [f"{e['document']['title']} (score: {e['score']})" for e in exact])
    print("  Sem count:", len(sem), [f"{s['document']['title']} (score: {s['score']})" for s in sem])
