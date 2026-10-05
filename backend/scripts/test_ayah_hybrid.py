import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.search_service import search_service

q = "الله لا إله إلا هو الحي القيوم لا تأخذه سنة ولا نوم"
res = search_service.hybrid_search([q], limit=5)
print(f"Hybrid Results for '{q}': count = {len(res)}")
for r in res:
    print(f"  Score: {r.relevance_score:.3f} | Title: {r.title} | Source: {r.source_name}")
