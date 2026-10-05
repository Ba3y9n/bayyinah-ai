import sys
import requests
sys.stdout.reconfigure(encoding='utf-8')

res = requests.post("http://127.0.0.1:8000/api/verify", json={"text": "الله لا إله إلا هو الحي القيوم لا تأخذه سنة ولا نوم له ما في السماوات وما في الأرض"})
data = res.json()
print("Status:", data.get("status"))
print("Status Slug:", data.get("status_slug"))
print("Reason:", data.get("reason"))
print("Evidence count:", len(data.get("evidence", [])))
for ev in data.get("evidence", []):
    print("  -> Source Name:", ev.get("source_name"))
    print("  -> Title:", ev.get("title"))
    print("  -> Reference:", ev.get("reference"))
    print("  -> Ruling/Grade:", ev.get("ruling_or_grade"))
    print("  -> Relevance:", ev.get("relevance_score"))
    print("  -> Excerpt[:80]:", ev.get("excerpt", "")[:80])
