import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.search_service import search_service

print(f"Loaded {len(search_service.documents)} documents in search_service:")
for idx, d in enumerate(search_service.documents):
    print(f"[{idx}] Source: {d.get('source_name')} | Title: {d.get('title')} | Content: {d.get('content')[:50]}...")
