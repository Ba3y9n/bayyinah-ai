# مخطط قاعدة البيانات والبحث المتجهي | Database Schema & pgvector Guide

> **التوثيق الهندسي الشامل لقاعدة بيانات Supabase PostgreSQL وامتداد pgvector في بيّنة AI**

---

## 1. وضع الإنتاج الصارم (Production Enforcement)

تعمل منصة **بيّنة AI** حصرياً على قاعدة بيانات **Supabase PostgreSQL** المدارة سحابياً:
- **المتغير البيئي الحاكم:** `DATABASE_MODE=supabase`
- **حظر التحويل الصامت:** يُحظر التراجع إلى SQLite في وضع الإنتاج لضمان توفر pgvector وArabic FTS في كل عملية فحص.

---

## 2. مصفوفة الجداول الـ 18 المعتمدة (The 18 Enterprise Canonical Tables)

| اسم الجدول | الوظيفة الهندسية | المفتاح الأساسي | المفاتيح الأجنبية والروابط |
| :--- | :--- | :--- | :--- |
| `sources` | سجل المصادر والمواقع الرسمية | `id (uuid)` | رخصة الاستخدام والاعتماد العلمي |
| `documents` | الوثائق والمصنفات التراثية | `id (uuid)` | `source_id -> sources.id` |
| `document_sections` | الفصول والأبواب والكتب الفرعية | `id (uuid)` | `document_id -> documents.id` |
| `document_chunks` | القطع المفهرسة والمتجهات | `id (uuid)` | `document_id`, `section_id` |
| `verification_sessions` | تتبع الجلسات المتعددة | `id (uuid)` | `active_claim_id`, `result_id` |
| `claims` | الادعاءات المستخرجة والمصنفة | `id (uuid)` | `verification_session_id` |
| `evidence` | الأدلة المكتشفة ودرجات التطابق | `id (uuid)` | `claim_id`, `source_id`, `chunk_id` |
| `verification_results` | الأحكام النهائية وسلسلة الاستدلال | `id (uuid)` | `claim_id`, `primary_source_id` |
| `verification_evidence` | الربط الترتيبي بين الأحكام والأدلة | `id (uuid)` | `verification_result_id`, `evidence_id`|
| `url_submissions` | سجل الروابط المفحوصة والمحللة | `id (uuid)` | `verification_session_id` |
| `media_assets` | الأصول المرئية والصوتية | `id (uuid)` | `verification_session_id` |
| `media_artifacts` | مخرجات التحليل (OCR، تفريغ صوتي) | `id (uuid)` | `media_asset_id` |
| `ingestion_jobs` | مهام التغذية وسجلات المعالجة | `id (uuid)` | `source_id` |
| `source_versions` | تاريخ تنقيح وإصدار المصادر | `id (uuid)` | `source_id` |
| `chat_sessions` | جلسات الحوار الموجه بالأدلة | `id (uuid)` | `verification_session_id`, `active_claim_id` |
| `chat_messages` | رسائل المحادثة ومحددات السند | `id (uuid)` | `chat_session_id` |
| `chat_evidence_bindings`| ربط عبارات الحوار بقطع الدليل | `id (uuid)` | `chat_message_id`, `chunk_id` |
| `audit_logs` | سجلات التدقيق الرقابي والأمان | `id (uuid)` | `claim_id` |

---

## 3. إعدادات pgvector والبحث الدلالي (pgvector Engine)

- **إصدار الامتداد:** `vector 0.8.2` مفعل داخل مخطط `public`.
- **أبعاد المتجه:** `vector(768)` متطابقة بدقة مع مخرجات `models/gemini-embedding-001` الرسمية.
- **معامل المسافة:** Cosine Distance (`<=>`).
- **استعلام البحث المتجهي الحقيقي:**
```sql
SELECT 
    c.id AS chunk_id,
    c.chunk_text,
    c.reference,
    s.name AS source_name,
    1 - (c.embedding <=> CAST(:query_vector AS vector)) AS similarity_score
FROM document_chunks c
JOIN documents d ON c.document_id = d.id
JOIN sources s ON d.source_id = s.id
WHERE c.embedding IS NOT NULL
  AND s.scientific_status = 'APPROVED'
ORDER BY c.embedding <=> CAST(:query_vector AS vector) ASC
LIMIT :top_k;
```

---

## 4. البحث النصي العربي المتقدم (PostgreSQL Arabic FTS)

- **القاموس المعتمد:** `arabic` (أو `simple` للتطابق اللفظي الشامل).
- **فهرس GIN المسرع:**
```sql
CREATE INDEX IF NOT EXISTS idx_document_chunks_search_vector 
ON document_chunks USING gin(search_vector);
```
- **استعلام البحث النصي وتصنيف الرتبة (Rank):**
```sql
SELECT 
    c.id AS chunk_id,
    c.chunk_text,
    ts_rank_cd(c.search_vector, to_tsquery('arabic', :query)) AS fts_score
FROM document_chunks c
WHERE c.search_vector @@ to_tsquery('arabic', :query)
ORDER BY fts_score DESC
LIMIT :top_k;
```

---

## 5. سياسات الأمان والتحكم بالوصول (Row-Level Security)

- الجداول الحساسة مثل `audit_logs` و`ingestion_jobs` و`sources` محمية بسياسات RLS صارمة.
- يُسمح بالوصول العام المقروء للمصادر والوثائق المعتمدة (`scientific_status = 'APPROVED'`).
- عمليات التعديل والإدخال مقصورة على مفتاح الخدمة الداخلي للخادم (`SUPABASE_SERVICE_ROLE_KEY`).
