import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.search_service import search_service

print(f"Total loaded: {len(search_service.documents)}")
for idx, d in enumerate(search_service.documents):
    print(f"[{idx}] Source ID: {d.get('source_id')} | Title: {d.get('title')}")
