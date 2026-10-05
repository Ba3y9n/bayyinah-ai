# بيّنة AI | BAYYINAH AI
> **تحقّق قبل أن تنشر.**  
> *Evidence-First Multimodal Islamic Content Verification Platform*  
> **منصة التحقق العلمي من المحتوى الإسلامي الرقمي لتمكين المعرّفين بالإسلام والجمهور العام.**

---

## 1. الرؤية والمبدأ الأساسي (Core Vision & Principle)

**بيّنة AI** ليست روبوت محادثة عاماً (Generic Chatbot)، وليست نظام إفتاء آلي (Automated Fatwa Engine)، ولا تعتمد إطلاقاً على الذاكرة التوليدية غير الموثقة للذكاء الاصطناعي.

### المبدأ الصارم:
$$\text{الذكاء الاصطناعي ليس مصدر الحقيقة الدينية}$$
دور الذكاء الاصطناعي محدد بدقة كأداة تحليل واسترجاع ومقارنة:
$$\text{Content} \longrightarrow \text{Claim Extraction} \longrightarrow \text{Hybrid Search} \longrightarrow \text{Evidence Retrieval} \longrightarrow \text{Disagreement Detection} \longrightarrow \text{Abstention/Validation} \longrightarrow \text{Grounded Result}$$

إذا لم يعثر النظام على دليل صريح موثق في مصادره المعتمدة، فإن النظام **يمتنع منهجياً (Abstains)** بحسب قاعدة التحدي الرسمية:
> *"عدم العثور على دليل في المصادر المعتمدة لا يعني إثبات البطلان، وإنما يعني عدم ثبوت الادعاء في حدود ما تم فحصه."*

---

## 2. النطاق العلمي والمستويات الأربعة المعتمدة (Official Challenge Scope)

تلتزم المنصة حرفياً بالنطاق العلمي والمنهجي لتحدي المحتوى الإسلامي:

| المستوى العلمي | التوصيف المنهجي | طريقة المعالجة في بيّنة AI | مثال تطبيقي |
| :--- | :--- | :--- | :--- |
| **المستوى (أ)** | **الثوابت والقطعيات والأصول الكلية** | إثبات قطعي مدعوم بنصوص القرآن والسنة والإجماع | أصل التوحيد، كعبة المشرفة قِبلة لا معبود، حفظ القرآن {إِنَّا نَحْنُ نَزَّلْنَا الذِّكْرَ}، نفي الإكراه في الدين |
| **المستوى (ب)** | **المسائل الخلافية الفرعية المعتبرة** | عرض مقارن لمذاهب الفقهاء دون إهدار الخلاف السائغ (`CONFLICT`) | قراءة الفاتحة خلف الإمام، رفع اليدين عند الركوع في الصلاة |
| **المستوى (ج)** | **الاستفسارات والفتاوى الفردية والنوازل** | الامتناع والإحالة الصريحة للجهات الرسمية المعتمدة (`SPECIALIST`) | قضايا الطلاق، نزاعات المواريث والتركات، النوازل الطبية والجنائية |
| **المستوى (د)** | **المحتوى الواهي والمكذوب وغير الثابت** | بيان علة الإسناد وحكم أئمة الحديث بالوضع أو النكارة (`FABRICATED` / `WEAK`) | حديث: «صوموا تصحوا» (لم يثبت بهذا اللفظ)، حديث: «اطلبوا العلم ولو في الصين» (باطل وموضوع) |

---

## 3. المصادر العلمية الرسمية الـ 11 (The 11 Official Scientific Sources)

ترتكز المنصة على فهرس معتمد يضم المصادر الرسمية الصادرة عن التحدي:
1. **مجمع الملك فهد لطباعة المصحف الشريف** (`dawa.center`) - النص القرآني والرسم العثماني.
2. **المنصة الرقمية للمحتوى الإسلامي** (`islamic-content.com`) - المعارف والموسوعات المعتمدة.
3. **الموسوعة القرآنية** (`quranpedia.net`) - التفاسير والقراءات وعلوم القرآن.
4. **موسوعة التفسير - الدرر السنية** (`dorar.net/tafseer`) - تفاسير أهل السنة المحررة.
5. **الموسوعة الحديثية - الدرر السنية** (`dorar.net/hadith`) - أحكام المحدثين وتخريج الأحاديث.
6. **المكتبة الشاملة** (`shamela.ws`) - أمهات كتب التراث والمصنفات الفقهية والتاريخية.
7. **موسوعة العقيدة والفرق المعاصرة - الدرر السنية** (`dorar.net/aqeeda`) - أصول التوحيد والمعتقد.
8. **الموسوعة الفقهية - الدرر السنية** (`dorar.net/feqhia`) - الفقه المقارن والمذاهب الأربعة.
9. **الموسوعة التاريخية - الدرر السنية** (`dorar.net/history`) - السيرة النبوية والتاريخ الإسلامي.
10. **الدليل الإرشادي للمحتوى الإسلامي** (`dawa.center/file/7937`) - ضوابط النشر والفتوى والامتناع.
11. **قاموس المصطلحات والمفاهيم الإسلامية** (`islamic-content.com/dictionary`) - المصطلحات والترجمات المعتمدة.

---

## 4. المعمارية التقنية والبنية التحتية الحية (Technical Architecture)

```
[ User Multimodal Input: Text / URL / Image / Video ]
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│  FastAPI Backend Engine (Python 3.13)                  │
│  ├── URL Resolver & Anti-SSRF Protection Engine        │
│  ├── Google Gemini 3.8 Flash (Multimodal OCR & Files)  │
│  ├── Multi-Claim Extraction & Normalization            │
│  └── Hybrid Search Engine (RRF Fusion)                 │
└───────────────────────┬────────────────────────────────┘
                        │
       ┌────────────────┴────────────────┐
       ▼                                 ▼
┌──────────────────────────────┐  ┌──────────────────────────────┐
│ PostgreSQL Full-Text Search  │  │ pgvector Extension (v0.8.2)  │
│ Arabic tsvector Dictionary   │  │ 768-d Gemini Embeddings      │
│ Exact Substring & Trigram    │  │ Cosine Similarity (<=>)      │
└──────────────┬───────────────┘  └──────────────┬───────────────┘
               └────────────────┬────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────┐
│  Verification & Evidence Synthesis Engine              │
│  ├── Zero-Hallucination Evidence-Bound Grounding       │
│  ├── Disagreement & Conflict Detection (4 Madhhabs)   │
│  ├── Interactive Evidence Graph (DAG Network)          │
│  └── Evidence-Bound Multi-turn Chat Assistant          │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│  Enterprise React 18 + Vite + Tailwind CSS Frontend    │
│  ├── Verification Timeline & Live Progress             │
│  ├── Evidence Graph Visualization & Node Inspector     │
│  ├── Knowledge Base Management & Search Sandbox        │
│  └── Production System Health Dashboard (`/system`)    │
└────────────────────────────────────────────────────────┘
```

---

## 5. قواعد البيانات الـ 18 المعتمدة في Supabase PostgreSQL

يعمل النظام حصرياً على **Supabase PostgreSQL** في وضع الإنتاج (`DATABASE_MODE=supabase`) مع تفعيل 18 جدولاً مترابطاً:
1. `sources`: سجل المصادر الموثوقة والاعتماد العلمي والتراخيص.
2. `documents`: الوثائق والمصنفات التراثية والرسمية.
3. `document_sections`: الأبواب والفصول الفقهية والحديثية.
4. `document_chunks`: قطع النصوص المفهرسة بروابط المتجهات و`search_vector`.
5. `verification_sessions`: جلسات التحقق وتتبع المدخلات متعددة الوسائط.
6. `claims`: الادعاءات المستخرجة وتصنيف مستوياتها ومخاطرها.
7. `evidence`: الأدلة المسترجعة ودرجات المطابقة والإسناد.
8. `verification_results`: نتائج التحقق النهائية ودرجة الثقة والمحددات.
9. `verification_evidence`: جدول الربط والترتيب بين النتائج والأدلة.
10. `url_submissions`: روابط منصات التواصل المفحوصة والمحللة.
11. `media_assets`: الصور ومقاطع الفيديو وسجلات Gemini Files API.
12. `media_artifacts`: المخرجات المستخرجة (OCR, Transcripts, Frames).
13. `ingestion_jobs`: مهام الفهرسة وسجلات المعالجة.
14. `source_versions`: إصدارات المصادر وتتبع التغييرات.
15. `chat_sessions`: جلسات المحادثة الموجهة بالأدلة.
16. `chat_messages`: رسائل المحادثة ومحددات الإسناد.
17. `chat_evidence_bindings`: ربط كل جملة في المحادثة بقطعة دليل حقيقية.
18. `audit_logs`: سجل التدقيق الرقابي والعمليات المحمية.

---

## 6. فحص الجاهزية الشامل (`/api/system/health`)

يوفر النظام نقطة نهاية برمجية تفصيلية تفحص جاهزية جميع المكونات الحية:
```bash
curl -s http://127.0.0.1:8000/api/system/health
```
نموذج الاستجابة الحية:
```json
{
  "frontend": "PASS",
  "backend": "PASS",
  "gemini": {
    "status": "PASS",
    "model": "gemini-3.8-flash",
    "latency_ms": 42
  },
  "database": {
    "status": "PASS",
    "active_database": "PostgreSQL (Supabase)",
    "mode": "supabase"
  },
  "pgvector": {
    "status": "PASS",
    "available": true,
    "dimension": 768,
    "extension_version": "0.8.2"
  },
  "fts": {
    "status": "PASS",
    "available": true,
    "config": "arabic"
  },
  "knowledge_base": {
    "status": "PASS",
    "documents_count": 20,
    "chunks_count": 21,
    "embeddings_count": 21,
    "published_sources_count": 19
  },
  "citation_validator": { "status": "PASS" },
  "evidence_engine": { "status": "PASS" },
  "storage": { "status": "PASS", "provider": "LOCAL" },
  "url_resolver": {
    "status": "PASS",
    "platforms": ["TWITTER", "TIKTOK", "YOUTUBE", "GENERIC", "DIRECT_MEDIA"]
  },
  "media_processing": {
    "status": "PASS",
    "ocr_model": "gemini-3.8-flash",
    "video_api": "Gemini Files API"
  },
  "mode": "supabase"
}
```

---

## 7. حزم التوثيق التقني التفصيلي (Documentation Package)

للاطلاع على التوثيق الهندسي والشرعي الكامل، يرجى مراجعة الدلائل التالية:

1. [معمارية النظام ومسار التحقق (docs/ARCHITECTURE.md)](file:///c:/Users/Bayan%20Alutiri/OneDrive/Desktop/Bayyinah%20AI/docs/ARCHITECTURE.md)
2. [قاعدة المعرفة والاسترجاع الهجين (docs/KNOWLEDGE_BASE.md)](file:///c:/Users/Bayan%20Alutiri/OneDrive/Desktop/Bayyinah%20AI/docs/KNOWLEDGE_BASE.md)
3. [مخطط قاعدة البيانات وpgvector (docs/DATABASE.md)](file:///c:/Users/Bayan%20Alutiri/OneDrive/Desktop/Bayyinah%20AI/docs/DATABASE.md)
4. [معالجة الوسائط المتعددة والفيديو (docs/MEDIA_PIPELINE.md)](file:///c:/Users/Bayan%20Alutiri/OneDrive/Desktop/Bayyinah%20AI/docs/MEDIA_PIPELINE.md)
5. [محرك الروابط وحماية SSRF (docs/URL_PIPELINE.md)](file:///c:/Users/Bayan%20Alutiri/OneDrive/Desktop/Bayyinah%20AI/docs/URL_PIPELINE.md)
6. [منهجية التقييم وحالات الاختبار (docs/EVALUATION.md)](file:///c:/Users/Bayan%20Alutiri/OneDrive/Desktop/Bayyinah%20AI/docs/EVALUATION.md)
7. [سياسات الأمان والحماية الرقابية (docs/SECURITY.md)](file:///c:/Users/Bayan%20Alutiri/OneDrive/Desktop/Bayyinah%20AI/docs/SECURITY.md)
8. [تراخيص المصادر والحقوق الفكرية (docs/SOURCE_LICENSES.md)](file:///c:/Users/Bayan%20Alutiri/OneDrive/Desktop/Bayyinah%20AI/docs/SOURCE_LICENSES.md)
9. [دليل التشغيل والنشر السحابي (docs/DEPLOYMENT.md)](file:///c:/Users/Bayan%20Alutiri/OneDrive/Desktop/Bayyinah%20AI/docs/DEPLOYMENT.md)

---

## 8. التشغيل السريع (Quickstart)

### المتطلبات المسبقة:
- Python 3.11+
- Node.js 18+
- حساب Supabase مفعل به `pgvector`
- مفتاح Google Gemini API

### إعداد الخادم الخلفي (Backend):
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### إعداد الواجهة الأمامية (Frontend):
```bash
cd frontend
npm install
npm run dev
```
افتح المتصفح على: `http://localhost:3000`

---
**بيّنة AI** — تم بناؤه وتطويره وفق أعلى المعايير الهندسية والمنهجية الإسلامية لخدمة المحتوى الرقمي الموثق.
