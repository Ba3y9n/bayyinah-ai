import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.search_service import search_service

print("Count:", len(search_service.documents))
for i, d in enumerate(search_service.documents):
    print(f"[{i}] {d['title']}")
