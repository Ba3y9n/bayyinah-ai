import sys
import json
import urllib.request
sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:8000/api/verify"

scenarios = [
    {
        "name": "سيناريو 1: حديث صحيح ثابت (المستوى أ)",
        "input": "إنما الأعمال بالنيات وإنما لكل امرئ ما نوى",
        "expected_status": "ثابت بحسب المصدر",
        "expected_slug": "VERIFIED"
    },
    {
        "name": "سيناريو 2: لفظ لم يثبت / حديث ضعيف (المستوى د)",
        "input": "صوموا تصحوا",
        "expected_status": "ضعيف بحسب المصدر",
        "expected_slug": "WEAK"
    },
    {
        "name": "سيناريو 3: نازلة شخصية / فتوى طلاق (المستوى ج - الامتناع والإحالة)",
        "input": "حلفت على زوجتي بالطلاق إن خرجت من البيت والآن هي خرجت فهل وقع الطلاق؟",
        "expected_status": "يحتاج مراجعة مختص",
        "expected_slug": "SPECIALIST"
    },
    {
        "name": "سيناريو 4: مسألة خلافية معتبرة بين المذاهب (المستوى ب - رصد الخلاف)",
        "input": "هل قراءة الفاتحة واجبة على المأموم في الصلاة الجهرية خلف الإمام؟",
        "expected_status": "اختلاف في المصادر",
        "expected_slug": "CONFLICT"
    }
]

print("=" * 80)
print("BAYYINAH AI — SECTION 64 CORE DEMO SCENARIOS EXECUTION")
print("=" * 80)

for s in scenarios:
    req_data = json.dumps({"text": s["input"]}).encode("utf-8")
    req = urllib.request.Request(API_URL, data=req_data, headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req, timeout=30)
    data = json.loads(resp.read().decode("utf-8"))
    
    status_slug = data.get("status_slug")
    status_ar = data.get("status")
    claim = data.get("extracted_claim")
    reason = data.get("detailed_explanation") or data.get("reason")
    evidence = data.get("evidence", [])
    
    match = (status_slug == s["expected_slug"])
    icon = "✅" if match else "❌"
    
    print(f"\n{icon} {s['name']}")
    print(f"   المدخل: «{s['input']}»")
    print(f"   الحالة المعتمدة: {status_ar} [{status_slug}]")
    print(f"   التعليل الموثق: {reason}")
    if evidence:
        top = evidence[0]
        print(f"   المصدر المعتمد: {top.get('source_name')} | المرجع: {top.get('reference')}")
        print(f"   نسبة التطابق: {top.get('relevance_score')} | نوع الدليل: {top.get('evidence_type')}")
    print("-" * 80)
