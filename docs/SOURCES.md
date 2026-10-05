# Official 11 Islamic Scientific Sources | المصادر العلمية الرسمية الـ 11

## Overview (نظرة عامة)

**Bayyinah AI** enforces strict source grounding. Claims are evaluated exclusively against the 11 official Islamic scientific sources established by the competition standards.

---

## Source Index & Scope Table

| # | Domain / Link | Name (Arabic) | Category / Type | Scientific Authority Scope |
|---|---|---|---|---|
| 1 | `dawa.center` | مجمع الملك فهد لطباعة المصحف الشريف | Quranic Text | Quranic Text, Uthmani Script, Official Translation |
| 2 | `islamic-content.com` | المنصة الرقمية للمحتوى الإسلامي | Knowledge Platform | Verified Islamic Knowledge & Encyclopedias |
| 3 | `quranpedia.net` | الموسوعة القرآنية | Quranic Sciences | Tafseer, Qira'at, Quranic Vocabulary & Context |
| 4 | `dorar.net/tafseer` | موسوعة التفسير - الدرر السنية | Tafseer Encyclopedia | Sunni Tafseer Exegesis & Verse Context |
| 5 | `dorar.net/hadith` | الموسوعة الحديثية - الدرر السنية | Hadith Verification | Hadith Authenticity, Chains (Isnad), Scholars' Rulings |
| 6 | `shamela.ws` | المكتبة الشاملة الرقمية | Heritage Library | Classical Turath Works, Fiqh Treatises & References |
| 7 | `dorar.net/aqeeda` | موسوعة العقيدة - الدرر السنية | Creed & Aqeedah | Islamic Aqeedah, Monotheism, Comparative Sects |
| 8 | `dorar.net/feqhia` | الموسوعة الفقهية - الدرر السنية | Comparative Fiqh | Four Sunni Madhhabs (Hanafi, Maliki, Shafi'i, Hanbali) |
| 9 | `dorar.net/history` | الموسوعة التاريخية - الدرر السنية | History & Seerah | Prophetic Biography, Sahabah & Islamic History |
| 10 | `dawa.center/file/7937` | الدليل الإرشادي للمحتوى الإسلامي | Guidelines Guide | Digital Publishing Guidelines & Abstention Rules |
| 11 | `islamic-content.com/dictionary` | قاموس المصطلحات الإسلامية | Terminology | Islamic Terminology, Definitions & Translations |

---

## 11-Source Coverage Status Model

For every claim verified by Bayyinah AI, each of the 11 sources receives an explicit status record in `sources_breakdown`:

```json
{
  "source_id": "dorar_hadith",
  "source_name": "موسوعة الحديث - الدرر السنية",
  "domain": "dorar.net/hadith",
  "search_attempt": "EXECUTED",
  "query_used": "وما زاد الله عبدا بعفو إلا عزا",
  "access_status": "SUCCESS_200",
  "result_status": "MATCH_FOUND",
  "evidence_count": 1,
  "canonical_url": "https://dorar.net/hadith/sharh/26252",
  "reference": "صحيح مسلم (2588)"
}
```

### Possible Result Status Values:
- `MATCH_FOUND`: Relevant authentic evidence found with canonical citation.
- `NO_MATCH`: Domain searched; no matching text or ruling found.
- `NOT_RELEVANT`: Domain scope does not apply to this claim type (e.g. Fiqh encyclopedia queried for a Hadith authenticity check).
- `ACCESS_ERROR`: Live HTTP timeout or rate limit; fallback system utilized.

---

## Usage Policies & Copyright Compliance

1. **Non-Commercial Educational Use**: All content extracted from official sources is used solely for verification, quotation, and academic attribution.
2. **Canonical Links Only**: Outputs link directly back to the original source web page (`canonical_url`), driving user traffic back to official publisher sites.
3. **No Paraphrasing of Textual Evidence**: Primary texts (Quranic verses, Hadith texts, classical Fiqh quotes) are preserved verbatim without AI rewrite.
