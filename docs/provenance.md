# سلسلة التتبع والإسناد الموثق (Evidence Provenance)
## التتبع التراجعي للأدلة من النتيجة إلى المصدر الأصلي في بيّنة AI

---

### 1. فلسفة الإسناد (Provenance Architecture)
في بيّنة AI، لا يوجد شيء اسمه *"وجدنا نصاً يشبه السؤال"*.
كل نتيجة يراها المستخدم مقترنة بسلسلة إسناد تراجعية كاملة (Full Provenance Chain) يمكن تتبعها خطوة بخطوة إلى مصدرها الأصلي:

```
النتيجة المعروضة للمستخدم (Verification Result)
       ↓
الدليل المسترجع (Evidence Item)
       ↓
المقطع النصي المحدد (Document Chunk: chunk_id)
       ↓
الموضع الدقيق (Locator: السورة والآية / الباب ورقم الحديث / المجلد والصفحة)
       ↓
الوثيقة المسجلة (Document: doc_id + content_hash)
       ↓
المصدر المعتمد (Trusted Source: source_id + Official URL)
```

---

### 2. بنية كائن التتبع (Provenance Object Schema)
تحمل كل نتيجة كائناً برمجياً موثقاً يتضمن:
```json
{
  "source_id": "src-bukhari",
  "source_name": "صحيح البخاري",
  "document_id": "doc-bukhari-hadith-1",
  "document_title": "حديث: إنما الأعمال بالنيات",
  "chunk_id": "chk-bukhari-01",
  "locator": "صحيح البخاري، كتاب بدء الوحي، باب كيف كان بدء الوحي، حديث رقم 1",
  "url": "https://sunnah.com/bukhari:1",
  "content_hash": "4d10f23a...87c3",
  "retrieved_at": "2026-10-02T18:10:00Z"
}
```

---

### 3. التحقق الرياضي التشفيري (Cryptographic Integrity)
يقوم محرك التحقق بمقارنة محتوى النص مع `content_hash` المسجل باستخدام دالة **SHA-256** قبل إقراره في الإسناد، مما يمنع قطعياً أي تلاعب أو حقن نصوص من خارج المصادر المعتمدة.
