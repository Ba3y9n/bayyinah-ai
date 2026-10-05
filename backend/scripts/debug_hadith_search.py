import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.search_service import search_service
from app.utils.arabic_normalizer import normalize_arabic, tokenize_arabic

q = "الأعمال بالنيات"
print(f"Query: {q}")
print(f"Normalized query: {normalize_arabic(q)}")
print(f"Tokenized query: {tokenize_arabic(q)}")

results = search_service.exact_text_search(q, limit=5)
print(f"Exact results count: {len(results)}")

for idx, doc in enumerate(search_service.documents):
    content = doc["content"]
    title = doc["title"]
    norm_content = normalize_arabic(content)
    norm_title = normalize_arabic(title)
    if "النيات" in content or "النيات" in norm_content or "نيات" in norm_content or "النيه" in norm_content or "نيه" in norm_content:
        print(f"Doc {idx} matches intent:")
        print(f"  Title: {title}")
        print(f"  Ref: {doc.get('reference')}")
        print(f"  Content[:100]: {content[:100]}")
