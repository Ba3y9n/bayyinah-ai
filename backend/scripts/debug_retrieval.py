import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.retrieval_agent import retrieval_agent
from app.services.query_agent import query_agent

claim = "الله لا إله إلا هو الحي القيوم لا تأخذه سنة ولا نوم له ما في السماوات وما في الأرض"
queries = query_agent.generate_queries({"main_claim": claim, "type": "Quran"})
print("Generated queries:", queries)

evs = retrieval_agent.orchestrate_hybrid_retrieval(queries, limit=5)
print("Retrieved count:", len(evs))
for i, ev in enumerate(evs):
    print(f"[{i}] score: {ev.relevance_score:.3f} | title: {ev.source_name} | locator: {ev.locator}")
    print(f"    grade: {ev.ruling_or_grade}")
    print(f"    excerpt[:100]: {ev.excerpt[:100] if ev.excerpt else None}")
