# دليل النشر والتشغيل السحابي | Production Deployment Guide

> **دليل الإعداد والتشغيل السحابي، تهيئة المتغيرات، وفحص الجاهزية لمنصة بيّنة AI**

---

## 1. متطلبات البنية التحتية (Infrastructure Requirements)

- **قاعدة البيانات:** مشروع Supabase مفعل به امتداد `pgvector` وامتداد `pg_trgm` ومخطط `public`.
- **الخادم الخلفي (Backend):** Python 3.11+، يعمل عبر Uvicorn مع خادم إطاري مثل Docker أو Google Cloud Run أو VPS.
- **الواجهة الأمامية (Frontend):** بيئة Node.js 18+ لبناء حزمة الإنتاج (`npm run build`) والنشر على Cloudflare Pages أو Vercel أو خادم Nginx.

---

## 2. جدول المتغيرات البيئية الإلزامية (Environment Variables)

يجب ضبط المتغيرات التالية داخل ملف `backend/.env`:

| المتغير البيئي | القيمة المعتمدة للإنتاج | الوصف |
| :--- | :--- | :--- |
| `DATABASE_MODE` | `supabase` | فرض استخدام Supabase PostgreSQL حصراً ومنع أي تراجع محلي |
| `DATABASE_URL` | `postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres` | رابط الاتصال المباشر بقاعدة بيانات PostgreSQL |
| `SUPABASE_URL` | `https://[PROJECT-REF].supabase.co` | رابط واجهة برمجة تطبيقات Supabase |
| `SUPABASE_ANON_KEY` | `sb_publishable_...` | مفتاح الوصول العام الموثق |
| `SUPABASE_SERVICE_ROLE_KEY` | `sb_secret_...` | مفتاح العمليات الموثقة بالخادم (سري) |
| `GEMINI_API_KEY` | `AIzaSy...` | مفتاح Google Gemini API الرسمي |
| `GEMINI_MODEL` | `gemini-3.8-flash` | نموذج الذكاء الاصطناعي المعتمد للتحليل والتحقق |
| `GEMINI_EMBEDDING_MODEL` | `models/gemini-embedding-001` | نموذج التوليد المتجهي 768 بعداً |
| `EMBEDDING_DIMENSION` | `768` | عدد أبعاد متجهات pgvector |
| `GEMINI_THINKING_LEVEL` | `high` | سياسة التفكير لتدقيق الأدلة ورصد الاختلاف |
| `ENVIRONMENT` | `production` | وضع التشغيل الإنتاجي |

---

## 3. تشغيل الترقيات وتغذية البيانات (Migrations & Seeding)

لتطبيق المخطط الكامل وتغذية البيانات المعتمدة في بيئة جديدة:

```bash
# 1. الدخول لمجلد الخادم وتفعيل البيئة
cd backend
python -m venv venv
source venv/bin/activate  # في Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. تشغيل أداة الترقيات التلقائية لـ 18 جدولاً
python app/db/supabase_migration_runner.py

# 3. تغذية المصادر والوثائق والمتجهات الرسمية
python scripts/seed_official_challenge_knowledge.py
```

---

## 4. التشغيل والمراقبة الحية (Running & Monitoring)

### تشغيل خادم الواجهة الخلفية:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### بناء ونشر الواجهة الأمامية:
```bash
cd frontend
npm install
npm run build
# الملفات الجاهزة للنشر ستكون داخل مجلد: frontend/dist
```

### فحص الجاهزية الحية الشامل (Health Monitoring):
يتم إرسال نداء فحص دوري لنقطة النهاية:
```bash
curl -f -s http://[DOMAIN]/api/system/health
```
الاستجابة الناجحة تتضمن `"mode": "supabase"` و`"database": {"status": "PASS"}` و`"pgvector": {"status": "PASS"}`.
