"""
Bayyinah AI - Official Source Allowlist & Governance Policy
Enforces Section 3, 4, 8, 29 of the Master Specifications:
Only the 11 officially approved challenge sources are permitted for core verification.
Any domain or URL outside this allowlist is strictly rejected from serving as religious truth evidence.
"""

from typing import Dict, Any, List, Optional
from urllib.parse import urlparse

OFFICIAL_SOURCE_ALLOWLIST: List[Dict[str, Any]] = [
    {
        "id": "00000000-0000-0000-0000-000000000001",
        "slug": "dawa-center",
        "name_ar": "مركز دعوة للتعريف بالإسلام",
        "name_en": "Dawa Center for Introducing Islam",
        "domain": "dawa.center",
        "base_url": "https://dawa.center",
        "category": "DAWA",
        "authority_level": "PRIMARY_CANONICAL",
        "content_scope": "المحتوى الدعوي الموثق والمقالات المنهجية للتعريف بالإسلام ومخاطبة غير المسلمين",
        "search_pattern": "site:dawa.center",
        "adapter_class": "DawaCenterAdapter"
    },
    {
        "id": "00000000-0000-0000-0000-000000000002",
        "slug": "islamic-content",
        "name_ar": "موسوعة المحتوى الإسلامي المترجم",
        "name_en": "Islamic Content Portal",
        "domain": "islamic-content.com",
        "base_url": "https://islamic-content.com",
        "category": "DAWA",
        "authority_level": "PRIMARY_CANONICAL",
        "content_scope": "المحتوى الإسلامي التحريري، المقالات المعتمدة، وضوابط المعايير المنهجية",
        "search_pattern": "site:islamic-content.com",
        "adapter_class": "IslamicContentAdapter"
    },
    {
        "id": "00000000-0000-0000-0000-000000000007",
        "slug": "islamic-content-dict",
        "name_ar": "قاموس المصطلحات والمفاهيم الإسلامية المترجمة",
        "name_en": "Islamic Content Terminology Dictionary",
        "domain": "islamic-content.com",
        "path_prefix": "/dictionary",
        "base_url": "https://islamic-content.com/dictionary",
        "category": "DICTIONARY_TRANSLATION",
        "authority_level": "PRIMARY_CANONICAL",
        "content_scope": "المصطلحات الشرعية المعتمدة، الشروح اللغوية والاصطلاحية، والترجمات الرسمية المعتمدة",
        "search_pattern": "site:islamic-content.com/dictionary",
        "adapter_class": "DictionaryAdapter"
    },
    {
        "id": "00000000-0000-0000-0000-000000000003",
        "slug": "quranpedia",
        "name_ar": "موسوعة القرآن الكريم - قرآن بيديا",
        "name_en": "Quranpedia Encyclopedia",
        "domain": "quranpedia.net",
        "base_url": "https://quranpedia.net",
        "category": "QURAN",
        "authority_level": "PRIMARY_CANONICAL",
        "content_scope": "النص القرآني بالرسم العثماني، التلاوات، القراءات، والتفاسير المعيارية للآيات",
        "search_pattern": "site:quranpedia.net",
        "adapter_class": "QuranpediaAdapter"
    },
    {
        "id": "00000000-0000-0000-0000-000000000014",
        "slug": "dorar-tafseer",
        "name_ar": "موسوعة التفسير المحرر - الدرر السنية",
        "name_en": "Dorar Al-Saniyyah Tafsir Encyclopedia",
        "domain": "dorar.net",
        "path_prefix": "/tafseer",
        "base_url": "https://dorar.net/tafseer",
        "category": "TAFSEER",
        "authority_level": "PRIMARY_CANONICAL",
        "content_scope": "التفسير المحرر لآيات القرآن الكريم واستنباط الفوائد والأحكام",
        "search_pattern": "site:dorar.net/tafseer",
        "adapter_class": "DorarTafsirAdapter"
    },
    {
        "id": "00000000-0000-0000-0000-000000000004",
        "slug": "dorar-hadith",
        "name_ar": "الموسوعة الحديثية - الدرر السنية",
        "name_en": "Dorar Al-Saniyyah Hadith Encyclopedia",
        "domain": "dorar.net",
        "path_prefix": "/hadith",
        "base_url": "https://dorar.net/hadith",
        "category": "HADITH",
        "authority_level": "PRIMARY_CANONICAL",
        "content_scope": "تخريج وتحقيق الأحاديث النبوية، أحكام المحدثين (صحيح، ضعيف، موضوع، لا أصل له)",
        "search_pattern": "site:dorar.net/hadith",
        "adapter_class": "DorarHadithAdapter"
    },
    {
        "id": "00000000-0000-0000-0000-000000000005",
        "slug": "shamela",
        "name_ar": "المكتبة الشاملة الرقمية الوقفية",
        "name_en": "Al-Maktaba Al-Shamela",
        "domain": "shamela.ws",
        "base_url": "https://shamela.ws",
        "category": "SEERAH_HISTORY",
        "authority_level": "PRIMARY_CANONICAL",
        "content_scope": "أمهات المصادر الإسلامية، كتب السنة، الفقه المقارن، والتراجم والتاريخ",
        "search_pattern": "site:shamela.ws",
        "adapter_class": "ShamelaAdapter"
    },
    {
        "id": "00000000-0000-0000-0000-000000000015",
        "slug": "dorar-aqeeda",
        "name_ar": "موسوعة العقيدة والمذاهب والأديان - الدرر السنية",
        "name_en": "Dorar Al-Saniyyah Aqeedah Encyclopedia",
        "domain": "dorar.net",
        "path_prefix": "/aqeeda",
        "base_url": "https://dorar.net/aqeeda",
        "category": "AQEEDAH",
        "authority_level": "PRIMARY_CANONICAL",
        "content_scope": "أصول التوحيد، العقيدة الإسلامية، ومسائل الفرق والمذاهب",
        "search_pattern": "site:dorar.net/aqeeda",
        "adapter_class": "DorarAqeedahAdapter"
    },
    {
        "id": "00000000-0000-0000-0000-000000000016",
        "slug": "dorar-feqhia",
        "name_ar": "الموسوعة الفقهية المحررة - الدرر السنية",
        "name_en": "Dorar Al-Saniyyah Fiqh Encyclopedia",
        "domain": "dorar.net",
        "path_prefix": "/feqhia",
        "base_url": "https://dorar.net/feqhia",
        "category": "FIQH",
        "authority_level": "PRIMARY_CANONICAL",
        "content_scope": "المسائل الفقهية المحررة، مقارنة المذاهب الأربعة، وبيان المسائل الخلافية المعتبرة",
        "search_pattern": "site:dorar.net/feqhia",
        "adapter_class": "DorarFiqhAdapter"
    },
    {
        "id": "00000000-0000-0000-0000-000000000017",
        "slug": "dorar-history",
        "name_ar": "الموسوعة التاريخية وأحداث السيرة - الدرر السنية",
        "name_en": "Dorar Al-Saniyyah History & Seerah",
        "domain": "dorar.net",
        "path_prefix": "/history",
        "base_url": "https://dorar.net/history",
        "category": "SEERAH_HISTORY",
        "authority_level": "PRIMARY_CANONICAL",
        "content_scope": "وقائع السيرة النبوية المحققة، والتاريخ الإسلامي المعتمد",
        "search_pattern": "site:dorar.net/history",
        "adapter_class": "DorarHistoryAdapter"
    },
    {
        "id": "00000000-0000-0000-0000-000000000006",
        "slug": "dawa-file-7937",
        "name_ar": "دليل الأسئلة والشبهات المعاصرة - مركز دعوة (ملف 7937)",
        "name_en": "Dawa Center Guideline File 7937",
        "domain": "dawa.center",
        "path_prefix": "/file/7937",
        "base_url": "https://dawa.center/file/7937",
        "category": "QUESTIONS_DOUBTS",
        "authority_level": "PRIMARY_CANONICAL",
        "content_scope": "الإجابات المنهجية عن الأسئلة والشبهات المعاصرة، وضوابط الامتناع عن الفتوى الفردية",
        "search_pattern": "site:dawa.center/file/7937",
        "adapter_class": "DawaFileAdapter"
    }
]

# Quick domain/path lookup structures
APPROVED_DOMAINS = {"dawa.center", "islamic-content.com", "quranpedia.net", "dorar.net", "shamela.ws"}
APPROVED_SOURCE_DOMAINS = APPROVED_DOMAINS

def normalize_url(url: str) -> str:
    """Cleans and normalizes URL for domain verification."""
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url

def is_url_in_allowlist(url: str) -> bool:
    """
    Strict validation: returns True ONLY if the URL matches one of the 11 official sources.
    Rejects any unapproved domain, IP, or path outside allowed bounds.
    """
    if not url:
        return False
    try:
        parsed = urlparse(normalize_url(url))
        hostname = (parsed.hostname or "").lower()
        path = parsed.path.lower()

        # Strip www. prefix
        if hostname.startswith("www."):
            hostname = hostname[4:]

        if hostname not in APPROVED_DOMAINS:
            return False

        # For specific path prefixes, ensure containment
        if hostname == "dorar.net":
            allowed_prefixes = ["/tafseer", "/hadith", "/aqeeda", "/feqhia", "/history"]
            return any(path.startswith(p) for p in allowed_prefixes)

        if hostname == "islamic-content.com":
            return True  # Both root portal and /dictionary are approved

        if hostname == "dawa.center":
            return True  # Root portal and /file/7937 are approved

        if hostname in ("quranpedia.net", "shamela.ws"):
            return True

        return False
    except Exception:
        return False

def get_matched_allowlist_entry(url: str) -> Optional[Dict[str, Any]]:
    """Returns the matching allowlist entry for a given URL."""
    if not is_url_in_allowlist(url):
        return None
    
    parsed = urlparse(normalize_url(url))
    hostname = (parsed.hostname or "").lower()
    if hostname.startswith("www."):
        hostname = hostname[4:]
    path = parsed.path.lower()

    # Specific path prefixes first (e.g. /dictionary, /file/7937, /tafseer, etc.)
    for entry in OFFICIAL_SOURCE_ALLOWLIST:
        if entry["domain"] == hostname and "path_prefix" in entry:
            if path.startswith(entry["path_prefix"].lower()):
                return entry

    # General domain match
    for entry in OFFICIAL_SOURCE_ALLOWLIST:
        if entry["domain"] == hostname and "path_prefix" not in entry:
            return entry

    return None
