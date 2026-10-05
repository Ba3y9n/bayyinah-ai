# سجل المصادر المعرفية المعتمدة (Source Registry)
## منصة بيّنة AI — الحزمة العلمية للتحدي (المسار الرابع)

---

### 1. مصادر الحزمة العلمية الرسمية
تتبنى المنصة المصادر والمنصات المحددة في الحزمة العلمية للتحدي كأساس مرجعي لسجل المصادر:

| المصدر | المعرف (Slug) | الفئة (Category) | نوع المصدر (Source Type) | حالة الاعتماد | حالة الترخيص |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **مركز دعوة** | `dawa-center` | `DAWA` | `OFFICIAL_PLATFORM` | `APPROVED` | `PENDING_VERIFICATION` |
| **موسوعة المحتوى الإسلامي / الجمهرة** | `islamic-content-aljumhrah` | `DICTIONARY_TRANSLATION` | `ENCYCLOPEDIA` | `APPROVED` | `PENDING_VERIFICATION` |
| **مؤسسة الدرر السنية** | `dorar-net` | `HADITH` | `ENCYCLOPEDIA` | `APPROVED` | `PENDING_VERIFICATION` |
| **المكتبة الشاملة** | `shamela-ws` | `SEERAH_HISTORY` | `DIGITAL_LIBRARY` | `APPROVED` | `PENDING_VERIFICATION` |
| **موسوعة القرآن الكريم** | `quranpedia` | `QURAN` | `QURAN_DATABASE` | `APPROVED` | `PENDING_VERIFICATION` |
| **مجمع الملك فهد لطباعة المصحف** | `quran-complex` | `QURAN` | `QURAN_DATABASE` | `APPROVED` | `VERIFIED` |
| **صحيح البخاري** | `sahih-bukhari` | `HADITH` | `HADITH_DATABASE` | `APPROVED` | `VERIFIED` |
| **صحيح مسلم** | `sahih-muslim` | `HADITH` | `HADITH_DATABASE` | `APPROVED` | `VERIFIED` |
| **المجامع الفقهية ودور الإفتاء** | `senior-scholars-fatwa` | `FIQH` | `REFERENCE_WORK` | `APPROVED` | `VERIFIED` |

---

### 2. حالات الثقة (Trust Status)
- `APPROVED`: المصدر معتمد للاستخدام في نطاق محدد وتمت مراجعة بياناته الرسمية.
- `REVIEW_REQUIRED`: المصدر معروف/مرشح ولكن يحتاج مراجعة قبل الاعتماد في الإجابات النهائية.
- `RESTRICTED`: يمكن الرجوع إليه في استعلامات محددة فقط.
- `DISABLED`: معطل ولا يدخل في عمليات الاسترجاع.

---

### 3. مسار تفعيل المصادر (Source Verification Pipeline)
```
Source Registration → Metadata Validation → License / Usage Review → Content Scope Definition 
→ Document Registration → Content Ingestion → Normalization → Chunking → Hash Generation 
→ Indexing & Vectorization → Retrieval Sandbox Test → Source Activation
```
لا يُمنح أي مصدر حالة `APPROVED` أو `ACTIVE` إلا بعد استيفاء الشروط وتحديد جهة التحقق وتاريخه.
