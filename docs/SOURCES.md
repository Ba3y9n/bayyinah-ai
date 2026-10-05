# Official Approved Sources

Bayyinah AI operates on a strictly closed ecosystem of 11 officially vetted scholarly and institutional sources. The AI is completely prohibited from trusting outside links or its own pre-trained knowledge.

### The Allowlist (`official_allowlist.py`)

| Source Name | Domain | Content Type | Retrieval Method |
|-------------|--------|--------------|------------------|
| **Dawa Center** | `dawa.center` | General / Articles | pgvector / URL Resolve |
| **Islamic Content** | `islamic-content.com` | Comprehensive | pgvector / URL Resolve |
| **Islamic Dictionary** | `islamic-content.com/dictionary` | Definitions | pgvector / URL Resolve |
| **QuranPedia** | `quranpedia.net` | Quranic Sciences | pgvector / URL Resolve |
| **Dorar Tafseer** | `dorar.net/tafseer` | Exegesis (Tafseer) | pgvector / URL Resolve |
| **Dorar Hadith** | `dorar.net/hadith` | Prophetic Traditions | pgvector / API |
| **Shamela** | `shamela.ws` | Classical Texts | pgvector / URL Resolve |
| **Dorar Aqeeda** | `dorar.net/aqeeda` | Creed (Aqeeda) | pgvector / URL Resolve |
| **Dorar Feqhia** | `dorar.net/feqhia` | Jurisprudence | pgvector / URL Resolve |
| **Dorar History** | `dorar.net/history` | Islamic History | pgvector / URL Resolve |
| **Dawa Resources**| `dawa.center/file/7937` | Dedicated Media | Exact Match |

### Excluded Sources
For strict ideological neutrality, institutional alignment, and competition parameters, the following widely-used platforms are **EXPLICITLY EXCLUDED** and will be rejected by the Evidence Gate:
- `sunnah.com`
- `islamqa.info`
- `islamweb.net`
- `wikipedia.org`
- `google.com` (as a source of truth)

*If SerpAPI is utilized, it is strictly bound as a Discovery Tool (using `site:` operators) to locate the canonical pages within the 11 domains above. SerpAPI snippets are never treated as Evidence.*
