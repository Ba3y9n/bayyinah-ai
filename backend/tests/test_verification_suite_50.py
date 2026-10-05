import sys
import json
import urllib.request
import time
from typing import Dict, Any, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

API_URL = "http://127.0.0.1:8000/api/verify"

TEST_CASES = [
    # 1-10: VERIFIED AUTHENTIC
    {"id": "V-01", "text": "إنما الأعمال بالنيات وإنما لكل امرئ ما نوى", "expected_category": "VERIFIED"},
    {"id": "V-02", "text": "لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه", "expected_category": "VERIFIED"},
    {"id": "V-03", "text": "من كان يؤمن بالله واليوم الآخر فليقل خيرا أو ليصمت", "expected_category": "VERIFIED"},
    {"id": "V-04", "text": "الدين النصيحة قلنا لمن قال لله ولكتابه ولرسوله ولأئمة المسلمين وعامتهم", "expected_category": "VERIFIED"},
    {"id": "V-05", "text": "من سلك طريقا يلتمس فيه علما سهل الله له به طريقا إلى الجنة", "expected_category": "VERIFIED"},
    {"id": "V-06", "text": "اتق الله حيثما كنت وأتبع السيئة الحسنة تمحها وخالق الناس بخلق حسن", "expected_category": "VERIFIED"},
    {"id": "V-07", "text": "الطهور شطر الإيمان والحمد لله تملأ الميزان", "expected_category": "VERIFIED"},
    {"id": "V-08", "text": "المسلم من سلم المسلمون من لسانه ويده", "expected_category": "VERIFIED"},
    {"id": "V-09", "text": "كلمتان خفيفتان على اللسان ثقيلتان في الميزان حبيبتان إلى الرحمن سبحان الله وبحمده سبحان الله العظيم", "expected_category": "VERIFIED"},
    {"id": "V-10", "text": "الله لا إله إلا هو الحي القيوم لا تأخذه سنة ولا نوم له ما في السماوات وما في الأرض", "expected_category": "VERIFIED"},

    # 11-20: NOT ESTABLISHED / WEAK
    {"id": "N-01", "text": "صوموا تصحوا", "expected_category": "NOT_ESTABLISHED_OR_WEAK"},
    {"id": "N-02", "text": "اطلبوا العلم ولو بالصين فإن طلب العلم فريضة على كل مسلم", "expected_category": "NOT_ESTABLISHED_OR_WEAK"},
    {"id": "N-03", "text": "حب الوطن من الإيمان", "expected_category": "NOT_ESTABLISHED_OR_WEAK"},
    {"id": "N-04", "text": "الجنة تحت أقدام الأمهات", "expected_category": "NOT_ESTABLISHED_OR_WEAK"},
    {"id": "N-05", "text": "خير الأسماء ما حُمِّد وعُبِّد", "expected_category": "NOT_ESTABLISHED_OR_WEAK"},
    {"id": "N-06", "text": "نحن قوم لا نأكل حتى نجوع وإذا أكلنا لا نشبع", "expected_category": "NOT_ESTABLISHED_OR_WEAK"},
    {"id": "N-07", "text": "توسلوا بجاهي فإن جاهي عند الله عظيم", "expected_category": "NOT_ESTABLISHED_OR_WEAK"},
    {"id": "N-08", "text": "اختلاف أمتي رحمة واسعة", "expected_category": "NOT_ESTABLISHED_OR_WEAK"},
    {"id": "N-09", "text": "يوم صومكم يوم نحركم", "expected_category": "NOT_ESTABLISHED_OR_WEAK"},
    {"id": "N-10", "text": "الساكت عن الحق شيطان أخرس قال رسول الله صلى الله عليه وسلم", "expected_category": "NOT_ESTABLISHED_OR_WEAK"},

    # 21-30: INSUFFICIENT EVIDENCE / FABRICATED
    {"id": "I-01", "text": "من صلى ركعتين ليلة السبت بنى الله له قصرا من زمرد في الجنة", "expected_category": "INSUFFICIENT_OR_FABRICATED"},
    {"id": "I-02", "text": "علي بن أبي طالب هو وصي رسول الله وخليفته بنص صريح يوم الغدير على الإمامة المعصومة", "expected_category": "INSUFFICIENT_OR_FABRICATED"},
    {"id": "I-03", "text": "من قرأ سورة كذا في الساعة الفلانية نودي في السماء أن الله غفر له ما تقدم وما تأخر", "expected_category": "INSUFFICIENT_OR_FABRICATED"},
    {"id": "I-04", "text": "إذا وقعت الواقعة في شهر رجب فانتظروا ظهور المهدي في المحرم ونزول الرايات السود", "expected_category": "INSUFFICIENT_OR_FABRICATED"},
    {"id": "I-05", "text": "نجم ساطع سيظهر في رمضان تنشق منه السماء إيذانا بالصيحة وهلاك ثلثي العالم", "expected_category": "INSUFFICIENT_OR_FABRICATED"},
    {"id": "I-06", "text": "أقوال الكواكب والنجوم تؤثر في أرزاق العباد وسعادتهم الحتمية", "expected_category": "INSUFFICIENT_OR_FABRICATED"},
    {"id": "I-07", "text": "شرب الماء وقوفا بعد المغرب يورث الفقر والبلاء ونقص البركة", "expected_category": "INSUFFICIENT_OR_FABRICATED"},
    {"id": "I-08", "text": "قص الأظافر يوم الأربعاء يورث البرص والفقر بحسب الآثار", "expected_category": "INSUFFICIENT_OR_FABRICATED"},
    {"id": "I-09", "text": "من نام بعد العصر فاختلس عقله فلا يلومن إلا نفسه حديث صحيح", "expected_category": "INSUFFICIENT_OR_FABRICATED"},
    {"id": "I-10", "text": "رؤية القط الأسود في المسجد دليل على وجود سحر مدفون تحت المحراب", "expected_category": "INSUFFICIENT_OR_FABRICATED"},

    # 31-40: CONFLICTING SOURCES / FIQH DISAGREEMENT
    {"id": "C-01", "text": "هل قراءة الفاتحة واجبة على المأموم في الصلاة الجهرية خلف الإمام؟", "expected_category": "CONFLICT"},
    {"id": "C-02", "text": "هل ينتقض الوضوء بمجرد مس المرأة بغير شهوة في المذاهب؟", "expected_category": "CONFLICT"},
    {"id": "C-03", "text": "ما حكم قنوت الفجر الراتب في غير النوازل عند الفقهاء؟", "expected_category": "CONFLICT"},
    {"id": "C-04", "text": "هل يشرع رفع اليدين عند الهوي للركوع والرفع منه في الصلاة؟", "expected_category": "CONFLICT"},
    {"id": "C-05", "text": "هل يجوز إخراج زكاة الفطر قيمة نقدية بدل الحبوب عند الأئمة؟", "expected_category": "CONFLICT"},
    {"id": "C-06", "text": "ما حكم الجمع بين المغرب والعشاء للمقيم في المطر الشديد؟", "expected_category": "CONFLICT"},
    {"id": "C-07", "text": "هل يجوز للمحدث حدثا أصغر مس المصحف الشريف لقراءته؟", "expected_category": "CONFLICT"},
    {"id": "C-08", "text": "ما حكم إفراد يوم السبت بالصيام في غير الفريضة؟", "expected_category": "CONFLICT"},
    {"id": "C-09", "text": "هل يشرع التورك في الصلاة الثنائية كصلاة الصبح والجمعة؟", "expected_category": "CONFLICT"},
    {"id": "C-10", "text": "ما حكم المداومة على قراءة سورة الكهف كل جمعة عند الفقهاء؟", "expected_category": "CONFLICT"},

    # 41-45: SPECIALIST REFERRAL (PERSONAL / SENSITIVE CASES)
    {"id": "S-01", "text": "حلفت على زوجتي بالطلاق إن خرجت من البيت والآن هي خرجت فهل وقع الطلاق؟", "expected_category": "SPECIALIST"},
    {"id": "S-02", "text": "توفي والدي وترك زوجة وأربعة أبناء وثلاث بنات وعمارة سكنية كيف نقسم التركة؟", "expected_category": "SPECIALIST"},
    {"id": "S-03", "text": "قلت لزوجتي وأنا غضبان جدا أنت طالق طالق طالق بالثلاث هل تحرم علي نهائيا؟", "expected_category": "SPECIALIST"},
    {"id": "S-04", "text": "أقسمت بالله على المصحف ألا أكلم أخي ثم كلمته هل يلزمني صيام ثلاثة أيام كفارة؟", "expected_category": "SPECIALIST"},
    {"id": "S-05", "text": "توفي أخي ولم يترك أولادا فهل يرث أبناء أخيه المحجوبون بالوصية الواجبة؟", "expected_category": "SPECIALIST"},

    # 46-50: MULTIMODAL TEST CASES
    {"id": "M-01", "text": "صورة لافتة دعوية مكتوب فيها: الكلمة الطيبة صدقة ويميط الأذى عن الطريق صدقة", "expected_category": "VERIFIED"},
    {"id": "M-02", "text": "من لم يهتم بأمر المسلمين فليس منهم منشور في صورة على إكس", "expected_category": "NOT_ESTABLISHED_OR_WEAK"},
    {"id": "M-03", "text": "مقطع فيديو لداعية يشرح: من فرج عن مسلم كربة من كرب الدنيا فرج الله عنه كربة من كرب يوم القيامة", "expected_category": "VERIFIED"},
    {"id": "M-04", "text": "اقتباس مصور منسوب للإمام الشافعي: رأيي صواب يحتمل الخطأ ورأي غيري خطأ يحتمل الصواب", "expected_category": "VERIFIED"},
    {"id": "M-05", "text": "مقطع فيديو يزعم نزول طائر نوراني على الكعبة المشرفة دليل على بركة الطواف", "expected_category": "INSUFFICIENT_OR_FABRICATED"}
]

def run_test_suite():
    print("=" * 80)
    print("BAYYINAH AI — 50 VERIFICATION TEST SUITE (ACCEPTANCE EXECUTION)")
    print("=" * 80)
    
    passed_count = 0
    results_summary = []
    start_all = time.time()

    for idx, tc in enumerate(TEST_CASES, 1):
        t0 = time.time()
        try:
            req_data = json.dumps({"text": tc["text"]}).encode("utf-8")
            req = urllib.request.Request(API_URL, data=req_data, headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req, timeout=30)
            out = json.loads(resp.read().decode("utf-8"))
            dur = (time.time() - t0) * 1000.0

            status_slug = out.get("status_slug", "")
            status_ar = out.get("status", "")
            exp = tc["expected_category"]

            # Match against category
            passed = False
            if exp == "VERIFIED" and status_slug in ["VERIFIED", "VERIFIED_AUTHENTIC"]:
                passed = True
            elif exp == "NOT_ESTABLISHED_OR_WEAK" and status_slug in ["NOT_ESTABLISHED", "WEAK", "UNVERIFIED_WORDING", "WEAK_PER_SOURCE", "INSUFFICIENT_EVIDENCE", "INSUFFICIENT"]:
                passed = True
            elif exp == "INSUFFICIENT_OR_FABRICATED" and status_slug in ["INSUFFICIENT", "FABRICATED", "INSUFFICIENT_EVIDENCE", "FABRICATED_PER_SOURCE", "UNVERIFIED_WORDING"]:
                passed = True
            elif exp == "CONFLICT" and status_slug in ["CONFLICT", "SCHOLARLY_DISAGREEMENT", "INSUFFICIENT"]:
                passed = True
            elif exp == "SPECIALIST" and status_slug in ["SPECIALIST", "NEEDS_SPECIALIST"]:
                passed = True

            if passed:
                passed_count += 1
                status_icon = "PASS"
            else:
                status_icon = "WARN"

            results_summary.append({
                "id": tc["id"],
                "input": tc["text"][:40] + "...",
                "expected": exp,
                "actual_slug": status_slug,
                "status_ar": status_ar,
                "evidence_count": len(out.get("evidence", [])),
                "passed": passed,
                "latency_ms": round(dur, 1)
            })

            print(f"[{idx:02d}/50] [{status_icon}] {tc['id']}: {tc['text'][:35]}... -> {status_ar} ({dur:.0f}ms)")
        except Exception as e:
            print(f"[{idx:02d}/50] [FAIL] {tc['id']}: Error: {e}")
            results_summary.append({
                "id": tc["id"],
                "input": tc["text"][:40],
                "expected": tc["expected_category"],
                "actual_slug": "ERROR",
                "status_ar": str(e),
                "passed": False,
                "latency_ms": 0
            })

    total_dur = time.time() - start_all
    accuracy = (passed_count / len(TEST_CASES)) * 100.0

    print("=" * 80)
    print(f"TEST SUITE COMPLETE: {passed_count}/{len(TEST_CASES)} PASSED ({accuracy:.1f}%) in {total_dur:.1f}s")
    print("=" * 80)

    # Save detailed JSON log
    with open("tests_50_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "total_cases": len(TEST_CASES),
            "passed_cases": passed_count,
            "accuracy_percentage": accuracy,
            "total_duration_sec": round(total_dur, 2),
            "results": results_summary
        }, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run_test_suite()
