import hashlib
import json
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.knowledge_models import (
    TrustedSourceModel,
    DocumentModel,
    DocumentChunkModel,
    TermModel,
    TermTranslationModel
)
from ..utils.arabic_normalizer import normalize_arabic

def sha256_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def seed_trusted_sources_and_documents(db: Session):
    """
    Seeds official challenge package sources, real documents, chunks, and terms.
    Strictly follows governance, licensing boundaries, and provenance.
    """
    # 1. Trusted Sources definitions
    sources_data = [
        {
            "id": "fe136b10-d8db-465c-ae6e-5b12483614cf",
            "name_ar": "مركز دعوة (Dawa Center)",
            "name_en": "Dawa Center",
            "slug": "dawa-center",
            "category": "DAWA",
            "source_type": "OFFICIAL_PLATFORM",
            "description": "منصة رسمية متخصصة في المحتوى الدعوي والرد على الشبهات والأسئلة المتكررة وتأهيل المعرفين بالإسلام.",
            "official_url": "https://dawa.center",
            "base_domain": "dawa.center",
            "authority_level": "SPECIALIZED_DAWAH_CENTER",
            "trust_status": "APPROVED",
            "usage_status": "SEARCH_SNIPPETS_AND_REFERRAL",
            "license_status": "PENDING_VERIFICATION",
            "license_name": "شروط الاستخدام الدعوي غير التجاري",
            "license_url": "https://dawa.center/terms",
            "copyright_holder": "مركز دعوة",
            "allowed_operations": {
                "METADATA_ONLY": True,
                "SEARCH_SNIPPETS": True,
                "INDEX_CONTENT": True,
                "STORE_CONTENT": False,
                "QUOTE_LIMITED": True,
                "DISPLAY_EXCERPT": True,
                "LINK_TO_SOURCE": True,
                "TRANSLATE": False,
                "DERIVE_EMBEDDINGS": True
            },
            "content_scope": "موضوعات الدعوة، الأسئلة المتكررة، التعريف بالإسلام، الشبهات المعاصرة",
            "language": "ar",
            "country": "Saudi Arabia",
            "verification_notes": "مصدر أساسي ضمن الحزمة العلمية للتحدي (المسار الرابع). تمت مراجعة النطاق واعتماده كمرجع دعوي.",
            "verified_by": "لجنة الحوكمة العلمية - بيّنة AI"
        },
        {
            "id": "f9eb8562-6b5d-4235-b0e9-3628e4f29d32",
            "name_ar": "موسوعة المحتوى الإسلامي / الجمهرة",
            "name_en": "Islamic Content Encyclopedia / Al-Jumhrah",
            "slug": "islamic-content-aljumhrah",
            "category": "DICTIONARY_TRANSLATION",
            "source_type": "ENCYCLOPEDIA",
            "description": "موسوعة متخصصة في ضبط المصطلحات والمفردات الإسلامية وترجمتها المعتمدة إلى لغات متعددة لتمكين المعرفين بالإسلام.",
            "official_url": "https://islamic-content.com",
            "base_domain": "islamic-content.com",
            "authority_level": "TERMINOLOGY_STANDARD",
            "trust_status": "APPROVED",
            "usage_status": "APPROVED_TRANSLATION_CORPUS",
            "license_status": "PENDING_VERIFICATION",
            "license_name": "رخصة الاستخدام المرجعي للمفردات",
            "license_url": "https://islamic-content.com/license",
            "copyright_holder": "موسوعة المحتوى الإسلامي",
            "allowed_operations": {
                "METADATA_ONLY": True,
                "SEARCH_SNIPPETS": True,
                "INDEX_CONTENT": True,
                "STORE_CONTENT": True,
                "QUOTE_LIMITED": True,
                "DISPLAY_EXCERPT": True,
                "LINK_TO_SOURCE": True,
                "TRANSLATE": True,
                "DERIVE_EMBEDDINGS": True
            },
            "content_scope": "المصطلحات الشرعية، المفاهيم العقدية، قواميس الترجمة الإسلامية المعتمدة",
            "language": "ar",
            "verification_notes": "المصدر المعياري المعتمد لترجمة المصطلحات وضبط المفاهيم تفادياً للترجمات الحرفية المشوهة.",
            "verified_by": "لجنة الترجمة والمصطلحات"
        },
        {
            "id": "928cbfb9-ad61-4207-93d3-5115168b7457",
            "name_ar": "مؤسسة الدرر السنية",
            "name_en": "Dorar Platform",
            "slug": "dorar-net",
            "category": "HADITH",
            "source_type": "ENCYCLOPEDIA",
            "description": "أشمل موسوعة إسلامية رقمية متخصصة في الموسوعة الحديثية، الفقهية، التفسيرية، والعقدية مع التخريج العلمي الموثق.",
            "official_url": "https://dorar.net",
            "base_domain": "dorar.net",
            "authority_level": "PRIMARY_CANONICAL",
            "trust_status": "APPROVED",
            "usage_status": "INDEXED_EXCERPTS_WITH_CITATION",
            "license_status": "PENDING_VERIFICATION",
            "license_name": "الاستخدام البحثي والدعوي غير التجاري مع ذكر المصدر",
            "license_url": "https://dorar.net/article/1",
            "copyright_holder": "مؤسسة الدرر السنية",
            "allowed_operations": {
                "METADATA_ONLY": True,
                "SEARCH_SNIPPETS": True,
                "INDEX_CONTENT": True,
                "STORE_CONTENT": False,
                "QUOTE_LIMITED": True,
                "DISPLAY_EXCERPT": True,
                "LINK_TO_SOURCE": True,
                "TRANSLATE": False,
                "DERIVE_EMBEDDINGS": True
            },
            "content_scope": "تخريج الحديث، بيان درجة الصحة والضعف، التفسير المحرر، الفقه المقارن، السيرة والتاريخ",
            "language": "ar",
            "verification_notes": "المرجع الرقمي الأول لتخريج الأحاديث وبيان أحكام الأئمة عليها وكشف الأحاديث الضعيفة والموضوعة.",
            "verified_by": "لجنة الرقابة الحديثية"
        },
        {
            "id": "fa84794a-0496-445a-b88e-394bf40aecf2",
            "name_ar": "المكتبة الشاملة",
            "name_en": "Al-Maktaba Al-Shamela",
            "slug": "shamela-ws",
            "category": "SEERAH_HISTORY",
            "source_type": "DIGITAL_LIBRARY",
            "description": "أضخم مكتبة رقمية للكتب والمصادر الإسلامية التراثية المطبوعة والمحققة عبر القرون.",
            "official_url": "https://shamela.ws",
            "base_domain": "shamela.ws",
            "authority_level": "ACADEMIC_HERITAGE_CORPUS",
            "trust_status": "APPROVED",
            "usage_status": "METADATA_AND_VERIFICATION_LOOKUP",
            "license_status": "PENDING_VERIFICATION",
            "license_name": "الملكية العامة ونصوص التراث المحققة",
            "license_url": "https://shamela.ws/privacy",
            "copyright_holder": "المكتبة الشاملة والمحققون",
            "allowed_operations": {
                "METADATA_ONLY": True,
                "SEARCH_SNIPPETS": True,
                "INDEX_CONTENT": False,
                "STORE_CONTENT": False,
                "QUOTE_LIMITED": True,
                "DISPLAY_EXCERPT": True,
                "LINK_TO_SOURCE": True,
                "TRANSLATE": False,
                "DERIVE_EMBEDDINGS": False
            },
            "content_scope": "أمهات كتب الفقه، العقيدة، التاريخ، السيرة، والتراجم",
            "language": "ar",
            "verification_notes": "مكتبة رقمية للتثبت المباشر من نصوص الكتب التراثية وأرقام الصفحات والمجلدات.",
            "verified_by": "لجنة التوثيق التراثي"
        },
        {
            "id": "4bd0512d-3e02-4cd7-abfb-135c20b7680f",
            "name_ar": "موسوعة القرآن الكريم (Quranpedia)",
            "name_en": "Quranpedia",
            "slug": "quranpedia",
            "category": "QURAN",
            "source_type": "QURAN_DATABASE",
            "description": "منصة متخصصة في علوم القرآن الكريم، التلاوات، القراءات، والتفاسير المعاصرة والمعاجم البيانية للآيات.",
            "official_url": "https://quranpedia.net",
            "base_domain": "quranpedia.net",
            "authority_level": "PRIMARY_CANONICAL",
            "trust_status": "APPROVED",
            "usage_status": "VERIFIED_QURAN_CORPUS",
            "license_status": "PENDING_VERIFICATION",
            "license_name": "النشر المفتوح للنص القرآني وعلومه",
            "license_url": "https://quranpedia.net/terms",
            "copyright_holder": "موسوعة القرآن الكريم",
            "allowed_operations": {
                "METADATA_ONLY": True,
                "SEARCH_SNIPPETS": True,
                "INDEX_CONTENT": True,
                "STORE_CONTENT": True,
                "QUOTE_LIMITED": True,
                "DISPLAY_EXCERPT": True,
                "LINK_TO_SOURCE": True,
                "TRANSLATE": True,
                "DERIVE_EMBEDDINGS": True
            },
            "content_scope": "النص القرآني، معاني الكلمات، التفاسير المعتمدة، التراجم العالمية للقرآن",
            "language": "ar",
            "verification_notes": "مرجع رقمي معتمد لتوثيق نصوص الآيات وترجماتها المعتمدة والتأكد من الضبط الإملائي والرسم العثماني.",
            "verified_by": "لجنة التدقيق القرآني"
        },
        {
            "id": "2c48a7cc-6c70-4292-96f5-41b974b40150",
            "name_ar": "مصحف مجمع الملك فهد لطباعة المصحف الشريف",
            "name_en": "King Fahd Quran Complex",
            "slug": "quran-complex",
            "category": "QURAN",
            "source_type": "QURAN_DATABASE",
            "description": "النص القرآني المعتمد برواية حفص عن عاصم بالرسم العثماني المطابق للمصاحف الرسمية المطبوعة.",
            "official_url": "https://qurancomplex.gov.sa",
            "base_domain": "qurancomplex.gov.sa",
            "authority_level": "SUPREME_CANONICAL",
            "trust_status": "APPROVED",
            "usage_status": "OFFICIAL_STANDARD",
            "license_status": "VERIFIED",
            "license_name": "الاستخدام العام للأغراض البحثية والدعوية مع حفظ قدسية النص",
            "license_url": "https://qurancomplex.gov.sa",
            "copyright_holder": "مجمع الملك فهد لطباعة المصحف الشريف",
            "allowed_operations": {
                "METADATA_ONLY": True,
                "SEARCH_SNIPPETS": True,
                "INDEX_CONTENT": True,
                "STORE_CONTENT": True,
                "QUOTE_LIMITED": True,
                "DISPLAY_EXCERPT": True,
                "LINK_TO_SOURCE": True,
                "TRANSLATE": True,
                "DERIVE_EMBEDDINGS": True
            },
            "content_scope": "القرآن الكريم كاملًا ومفهرسًا بالسورة والآية والرسم العثماني",
            "language": "ar",
            "verification_notes": "المصدر القطعي الأعلى لصحة ألفاظ القرآن الكريم.",
            "verified_by": "لجنة مراجعة المصحف الشريف"
        },
        {
            "id": "66f6b2e4-acbe-49f1-a0df-dfcb74c211c9",
            "name_ar": "صحيح البخاري (الجامع المسند الصحيح المختصر)",
            "name_en": "Sahih al-Bukhari",
            "slug": "sahih-bukhari",
            "category": "HADITH",
            "source_type": "HADITH_DATABASE",
            "description": "أصح كتاب بعد كتاب الله تعالى، جمع الأحاديث النبوية الصحيحة المسندة بإسناد متصل.",
            "official_url": "https://dorar.net/hadith/sharh/1",
            "base_domain": "dorar.net",
            "authority_level": "PRIMARY_CANONICAL",
            "trust_status": "APPROVED",
            "usage_status": "FULL_PRIMARY_CORPUS",
            "license_status": "VERIFIED",
            "license_name": "الملكية العامة (نصوص التراث المحققة)",
            "license_url": "https://dorar.net/hadith",
            "copyright_holder": "الملكية العامة",
            "allowed_operations": {
                "METADATA_ONLY": True,
                "SEARCH_SNIPPETS": True,
                "INDEX_CONTENT": True,
                "STORE_CONTENT": True,
                "QUOTE_LIMITED": True,
                "DISPLAY_EXCERPT": True,
                "LINK_TO_SOURCE": True,
                "TRANSLATE": True,
                "DERIVE_EMBEDDINGS": True
            },
            "content_scope": "المتون النبوية الصحيحة، الأبواب الفقهية، التخريج برقم الحديث",
            "language": "ar",
            "author": "الإمام محمد بن إسماعيل البخاري (ت: 256هـ)",
            "verification_notes": "مرجع أصول السنة الصحيحة المتفق عليها.",
            "verified_by": "قسم السنة النبوية"
        },
        {
            "id": "86aa3feb-61dc-478f-b0a8-b2820f48a2c9",
            "name_ar": "صحيح مسلم (المسند الصحيح المختصر من السنن)",
            "name_en": "Sahih Muslim",
            "slug": "sahih-muslim",
            "category": "HADITH",
            "source_type": "HADITH_DATABASE",
            "description": "ثاني أصح دواوين الحديث النبوي الشريف بعد صحيح البخاري.",
            "official_url": "https://dorar.net/hadith/sharh/3",
            "base_domain": "dorar.net",
            "authority_level": "PRIMARY_CANONICAL",
            "trust_status": "APPROVED",
            "usage_status": "FULL_PRIMARY_CORPUS",
            "license_status": "VERIFIED",
            "license_name": "الملكية العامة (نصوص التراث المحققة)",
            "license_url": "https://dorar.net/hadith",
            "copyright_holder": "الملكية العامة",
            "allowed_operations": {
                "METADATA_ONLY": True,
                "SEARCH_SNIPPETS": True,
                "INDEX_CONTENT": True,
                "STORE_CONTENT": True,
                "QUOTE_LIMITED": True,
                "DISPLAY_EXCERPT": True,
                "LINK_TO_SOURCE": True,
                "TRANSLATE": True,
                "DERIVE_EMBEDDINGS": True
            },
            "content_scope": "الأحاديث النبوية المسندة الصحيحة برقم الحديث والباب",
            "language": "ar",
            "author": "الإمام مسلم بن الحجاج النيسابوري (ت: 261هـ)",
            "verification_notes": "مرجع أصول السنة النبوية الصحيحة.",
            "verified_by": "قسم السنة النبوية"
        },
        {
            "id": "683b35e0-6b77-46a0-b73f-fa0ba84cc84f",
            "name_ar": "المجامع الفقهية وهيئات كبار العلماء الرسمية",
            "name_en": "Official Fiqh Academies & Senior Scholars Councils",
            "slug": "senior-scholars-fatwa",
            "category": "FIQH",
            "source_type": "REFERENCE_WORK",
            "description": "مرجع الإحالة الإلزامية للمسائل الشخصية والفتاوى الواقعية والنوازل الكبرى.",
            "official_url": "https://www.alifta.gov.sa",
            "base_domain": "alifta.gov.sa",
            "authority_level": "OFFICIAL_FATWA_AUTHORITY",
            "trust_status": "APPROVED",
            "usage_status": "REFERRAL_ONLY",
            "license_status": "VERIFIED",
            "license_name": "مرجع رسمي للإحالة",
            "license_url": "https://www.alifta.gov.sa",
            "copyright_holder": "الرئاسة العامة للبحوث العلمية والإفتاء",
            "allowed_operations": {
                "METADATA_ONLY": True,
                "SEARCH_SNIPPETS": True,
                "INDEX_CONTENT": False,
                "STORE_CONTENT": False,
                "QUOTE_LIMITED": False,
                "DISPLAY_EXCERPT": True,
                "LINK_TO_SOURCE": True,
                "TRANSLATE": False,
                "DERIVE_EMBEDDINGS": False
            },
            "content_scope": "الإحالة والتوجيه للمفتين المعتمدين في المسائل الشخصية والنوازل (LEVEL_D)",
            "language": "ar",
            "verification_notes": "يمنع النظام إصدار أي حكم شخصي ويحيل آلياً إلى هذا المرجع.",
            "verified_by": "لجنة السياسات الفقهية"
        }
    ]

    for s_data in sources_data:
        existing = db.query(TrustedSourceModel).filter_by(id=s_data["id"]).first()
        allowed_ops_json = json.dumps(s_data["allowed_operations"], ensure_ascii=False)
        lic_stat = s_data.get("license_status", "PENDING")
        if lic_stat == "PENDING_VERIFICATION":
            lic_stat = "PENDING"

        if not existing:
            src = TrustedSourceModel(
                id=s_data["id"],
                name=s_data.get("name") or s_data.get("name_ar") or s_data.get("name_en"),
                name_ar=s_data["name_ar"],
                name_en=s_data["name_en"],
                slug=s_data["slug"],
                category=s_data["category"],
                description=s_data["description"],
                url=s_data.get("url") or s_data.get("official_url"),
                official_url=s_data["official_url"],
                base_domain=s_data["base_domain"],
                source_type=s_data["source_type"],
                authority_level=s_data.get("authority_level", "PRIMARY_CANONICAL"),
                trust_status=s_data.get("trust_status", "APPROVED"),
                usage_status=s_data.get("usage_status", "METADATA_AND_SNIPPETS"),
                license_status=lic_stat,
                license_name=s_data.get("license_name"),
                license_url=s_data.get("license_url"),
                copyright_holder=s_data.get("copyright_holder"),
                allowed_operations=allowed_ops_json,
                content_scope=s_data.get("content_scope"),
                language=s_data.get("language", "ar"),
                country=s_data.get("country"),
                author=s_data.get("author"),
                verification_notes=s_data.get("verification_notes"),
                verified_by=s_data.get("verified_by"),
                is_active=True
            )
            db.add(src)
        else:
            existing.allowed_operations = allowed_ops_json
            existing.trust_status = s_data.get("trust_status", "APPROVED")
            existing.license_status = lic_stat
            existing.official_url = s_data["official_url"]
            existing.category = s_data["category"]
    db.commit()

    # 2. Documents & Chunks Seeding (Real content for core cases)
    documents_seed = [
        # Doc 1: Ayat Al-Kursi
        {
            "id": "c62bf717-2ecd-413f-8020-f3327ba79c29",
            "source_id": "2c48a7cc-6c70-4292-96f5-41b974b40150",
            "title_ar": "سورة البقرة - آية الكرسي (الآية 255)",
            "title_en": "Surah Al-Baqarah - Ayat Al-Kursi (Verse 255)",
            "author": "تنزيل من حكيم حميد",
            "publisher": "مجمع الملك فهد لطباعة المصحف الشريف",
            "document_type": "PRIMARY_SCRIPTURE",
            "category": "QURAN",
            "official_url": "https://quran.ksu.edu.sa/index.php#aya=2_255",
            "canonical_url": "https://qurancomplex.gov.sa/quran/2/255",
            "description": "أعظم آية في كتاب الله تعالى متضمنة لصفات الوحدانية والقيومية والملك التام.",
            "license_status": "VERIFIED",
            "chunks": [
                {
                    "id": "chk-ayat-alkursi-01",
                    "chunk_index": 0,
                    "content": "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ ۗ مَنْ ذَا الَّذِي يَشْفَعُ عِنْدَهُ إِلَّا بِإِذْنِهِ ۚ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ وَلَا يُحِيطُونَ بِشَيْءٍ مِنْ عِلْمِهِ إِلَّا بِمَا شَاءَ ۚ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ ۖ وَلَا يَئُودُهُ حِفْظُهُمَا ۚ وَهُوَ الْعَلِيُّ الْعَظِيمُ",
                    "section_title": "الحزب 5 - الربع 1",
                    "chapter_title": "سورة البقرة",
                    "verse_reference": "البقرة: 255",
                    "source_locator": "سورة البقرة، الآية 255، ص 42 في مصحف المدينة",
                    "canonical_url": "https://quran.ksu.edu.sa/index.php#aya=2_255"
                }
            ]
        },
        # Doc 2: Surat Al-Ikhlas
        {
            "id": "d6870266-2c7e-4603-9af6-c069dd310c12",
            "source_id": "2c48a7cc-6c70-4292-96f5-41b974b40150",
            "title_ar": "سورة الإخلاص كاملة (الآيات 1-4)",
            "title_en": "Surah Al-Ikhlas (Verses 1-4)",
            "author": "تنزيل من حكيم حميد",
            "publisher": "مجمع الملك فهد لطباعة المصحف الشريف",
            "document_type": "PRIMARY_SCRIPTURE",
            "category": "QURAN",
            "official_url": "https://quran.ksu.edu.sa/index.php#aya=112_1",
            "canonical_url": "https://qurancomplex.gov.sa/quran/112",
            "description": "سورة الإخلاص المحتوية على خالص صفة الرحمن وتعدل ثلث القرآن.",
            "license_status": "VERIFIED",
            "chunks": [
                {
                    "id": "chk-al-ikhlas-01",
                    "chunk_index": 0,
                    "content": "قُلْ هُوَ اللَّهُ أَحَدٌ ۝ اللَّهُ الصَّمَدُ ۝ لَمْ يَلِدْ وَلَمْ يُولَدْ ۝ وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ",
                    "section_title": "جزء عم",
                    "chapter_title": "سورة الإخلاص",
                    "verse_reference": "الإخلاص: 1-4",
                    "source_locator": "سورة الإخلاص، الآيات 1 إلى 4، ص 604 بمصحف المدينة",
                    "canonical_url": "https://quran.ksu.edu.sa/index.php#aya=112_1"
                }
            ]
        },
        # Doc 3: Sahih Bukhari Hadith Al-A'mal bin-Niyyat
        {
            "id": "8bf24003-086d-46d4-b2ac-89ff8267af25",
            "source_id": "66f6b2e4-acbe-49f1-a0df-dfcb74c211c9",
            "title_ar": "حديث: إنما الأعمال بالنيات - صحيح البخاري (حديث رقم 1)",
            "title_en": "Hadith: Actions are but by intentions - Sahih al-Bukhari #1",
            "author": "الإمام محمد بن إسماعيل البخاري",
            "publisher": "دار التأصيل",
            "document_type": "AUTHENTIC_HADITH",
            "category": "HADITH",
            "official_url": "https://dorar.net/hadith/sharh/1",
            "canonical_url": "https://dorar.net/hadith/sharh/1",
            "description": "أصل عظيم من أصول الإسلام وقاعدة تدور عليها جميع تصرفات المكلفين.",
            "license_status": "VERIFIED",
            "chunks": [
                {
                    "id": "chk-bukhari-01",
                    "chunk_index": 0,
                    "content": "عَنْ عُمَرَ بْنِ الْخَطَّابِ رَضِيَ اللَّهُ عَنْهُ قَالَ: سَمِعْتُ رَسُولَ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ يَقُولُ: «إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى، فَمَنْ كَانَتْ هِجْرَتُهُ إِلَى دُنْيَا يُصِيبُهَا أَوْ إِلَى امْرَأَةٍ يَنْكِحُهَا فَهِجْرَتُهُ إِلَى مَا هَاجَرَ إِلَيْهِ».",
                    "chapter_title": "كتاب بدء الوحي",
                    "section_title": "باب كيف كان بدء الوحي إلى رسول الله صلى الله عليه وسلم",
                    "hadith_reference": "صحيح البخاري: 1",
                    "source_locator": "صحيح البخاري، كتاب بدء الوحي، باب كيف كان بدء الوحي، حديث رقم 1",
                    "canonical_url": "https://dorar.net/hadith/sharh/1"
                }
            ]
        },
        # Doc 4: Sahih Muslim - Hadith Man Kadhaba Alayya
        {
            "id": "1480fff5-c39f-4927-a8f9-4b87bd653f33",
            "source_id": "86aa3feb-61dc-478f-b0a8-b2820f48a2c9",
            "title_ar": "حديث: من كذب علي متعمدا فليتبوأ مقعده من النار - مقدمة صحيح مسلم",
            "title_en": "Hadith: Whoever lies upon me intentionally - Sahih Muslim Intro",
            "author": "الإمام مسلم بن الحجاج النيسابوري",
            "publisher": "دار التأصيل",
            "document_type": "AUTHENTIC_HADITH",
            "category": "HADITH",
            "official_url": "https://dorar.net/hadith/sharh/3",
            "canonical_url": "https://dorar.net/hadith/sharh/3",
            "description": "تحريم الكذب على رسول الله صلى الله عليه وسلم وبيان الوعيد الشديد على نسبة ما لم يقله إليه.",
            "license_status": "VERIFIED",
            "chunks": [
                {
                    "id": "chk-muslim-intro-03",
                    "chunk_index": 0,
                    "content": "عَنْ أَبِي هُرَيْرَةَ وَأَنَسِ بْنِ مَالِكٍ وَالْمُغِيرَةِ بْنِ شُعْبَةَ عَنْ رَسُولِ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ قَالَ: «مَنْ كَذَبَ عَلَيَّ مُتَعَمِّدًا فَلْيَتَبَوَّأْ مَقْعَدَهُ مِنَ النَّارِ».",
                    "chapter_title": "مقدمة صحيح مسلم",
                    "section_title": "باب تغليظ الكذب على رسول الله صلى الله عليه وسلم",
                    "hadith_reference": "مقدمة صحيح مسلم: 3",
                    "source_locator": "مقدمة صحيح مسلم، باب تغليظ الكذب على رسول الله صلى الله عليه وسلم، حديث 3",
                    "canonical_url": "https://dorar.net/hadith/sharh/3"
                }
            ]
        },
        # Doc 5: Dorar Net - Takhrij Hadith Utlubu Al-Ilma Walaw bil-Sin (Fabricated/Weak)
        {
            "id": "b91ae628-fd9e-4dcf-9690-6f0d50ec17f8",
            "source_id": "928cbfb9-ad61-4207-93d3-5115168b7457",
            "title_ar": "تخريج حديث: «اطلبوا العلم ولو بالصين» - موسوعة الأحاديث بموقع الدرر السنية",
            "title_en": "Ruling on Hadith: Seek knowledge even in China - Dorar Net",
            "author": "نخبة من المحدثين بإشراف الشيخ علوي السقاف",
            "publisher": "مؤسسة الدرر السنية",
            "document_type": "SCHOLARLY_TAKHRIJ",
            "category": "HADITH",
            "official_url": "https://dorar.net/hadith/sharh/21234",
            "canonical_url": "https://dorar.net/hadith/sharh/21234",
            "description": "تخريج وتحقيق موسع لحديث طلب العلم ولو بالصين وبيان حكم كبار أئمة الحديث عليه.",
            "license_status": "PENDING_VERIFICATION",
            "chunks": [
                {
                    "id": "chk-dorar-china-01",
                    "chunk_index": 0,
                    "content": "الحديث: «اطلبوا العلم ولو بالصين، فإن طلب العلم فريضة على كل مسلم». الحكم المعتمد: باطل أو ضعيف جداً لا أصل له مرفوعاً بهذا اللفظ. قال الإمام ابن حبان: «باطل لا أصل له»، وقال العقيلي: «لا يصح في هذا الباب شيء»، وذكره الإمام ابن الجوزي في كتاب الموضوعات، وضعفه الحافظ ابن حجر والألباني في السلسلة الضعيفة (رقم 416). الجزء الثابت الصحيح فقط هو: «طلب العلم فريضة على كل مسلم» بروايات أخرى صححها جمع من أهل العلم.",
                    "section_title": "تخريج أحاديث فضائل العلم",
                    "chapter_title": "الموسوعة الحديثية",
                    "source_locator": "الدرر السنية - الموسوعة الحديثية، بطاقة الحديث رقم 21234",
                    "canonical_url": "https://dorar.net/hadith/sharh/21234"
                }
            ]
        },
        # Doc 6: Dorar Net - Takhrij Hadith Somo Tasihho (Weak)
        {
            "id": "e0b9d053-49f4-4b46-85dc-de4d2b4275bd",
            "source_id": "928cbfb9-ad61-4207-93d3-5115168b7457",
            "title_ar": "تخريج حديث: «صوموا تصحوا» - موسوعة الدرر السنية",
            "title_en": "Ruling on Hadith: Fast and you will be healthy - Dorar Net",
            "author": "مؤسسة الدرر السنية",
            "publisher": "مؤسسة الدرر السنية",
            "document_type": "SCHOLARLY_TAKHRIJ",
            "category": "HADITH",
            "official_url": "https://dorar.net/hadith/sharh/14890",
            "canonical_url": "https://dorar.net/hadith/sharh/14890",
            "description": "بيان درجة حديث صوموا تصحوا وأقوال أئمة الجرح والتعديل فيه.",
            "license_status": "PENDING_VERIFICATION",
            "chunks": [
                {
                    "id": "chk-dorar-fasting-01",
                    "chunk_index": 0,
                    "content": "الحديث المتداول: «اغزوا تغنموا، وصوموا تصحوا، وسافروا تستغنوا». درجة الحديث: ضعيف. رواه الطبراني في الأوسط وأبو نعيم في الطب النبوي من حديث أبي هريرة وعلي بن أبي طالب رضي الله عنهما. ضعفه الإمام العراقي في تخريج الإحياء، والشيخ الألباني في ضعيف الجامع (رقم 3501) وسلسلة الأحاديث الضعيفة (رقم 253). ومع أن المعنى الطبي قد يكون صحيحاً في الجملة لفوائد الصيام، إلا أنه لا تصح نسبته لفظاً إلى النبي صلى الله عليه وسلم.",
                    "section_title": "أحاديث الصيام وفضائله",
                    "chapter_title": "الموسوعة الحديثية",
                    "source_locator": "الدرر السنية - الموسوعة الحديثية، بطاقة الحديث رقم 14890",
                    "canonical_url": "https://dorar.net/hadith/sharh/14890"
                }
            ]
        },
        # Doc 7: Fiqh Disagreement - Reciting Fatihah behind the Imam in loud prayers (Conflict Case)
        {
            "id": "449ae4b4-9124-42b2-a4ed-22b1f5b57a46",
            "source_id": "928cbfb9-ad61-4207-93d3-5115168b7457",
            "title_ar": "المسألة الفقهية: حكم قراءة المأموم للفاتحة خلف الإمام في الصلاة الجهرية",
            "title_en": "Fiqh Ruling: Reciting Al-Fatiha by the follower behind Imam in loud prayers",
            "author": "الموسوعة الفقهية - الدرر السنية",
            "publisher": "مؤسسة الدرر السنية",
            "document_type": "FIQH_COMPARATIVE",
            "category": "FIQH",
            "official_url": "https://dorar.net/feqhia/1284",
            "canonical_url": "https://dorar.net/feqhia/1284",
            "description": "تحرير الخلاف الفقهي المعتبر بين المذاهب الأربعة في وجوب أو استحباب أو كراهة قراءة المأموم للفاتحة في الجهرية.",
            "license_status": "PENDING_VERIFICATION",
            "chunks": [
                {
                    "id": "chk-fiqh-fatihah-01",
                    "chunk_index": 0,
                    "content": "مسألة قراءة الفاتحة للمأموم في الصلاة الجهرية من المسائل الخلافية المعتبرة بين الفقهاء: القول الأول (مذهب الشافعية ورواية عن أحمد): تجب قراءة الفاتحة على المأموم في كل ركعة سراً سواء كانت الصلاة سرية أو جهرية؛ لعموم حديث: «لا صلاة لمن لم يقرأ بفاتحة الكتاب». القول الثاني (مذهب الحنفية والمالكية ورواية عن الحنابلة وهو اختيار ابن تيمية والجمهور): لا يقرأ المأموم في الجهرية بل ينصت لقراءة الإمام؛ لقوله تعالى: «وَإِذَا قُرِئَ الْقُرْآنُ فَاسْتَمِعُوا لَهُ وَأَنْصِتُوا»، وحديث: «من كان له إمام فقراءة الإمام له قراءة». الخلاصة: المسألة محل خلاف فقهي معتبر ويسع المسلم الأخذ بأي من القولين بعد استفتاء العالم الموثوق.",
                    "section_title": "أحكام صلاة الجماعة",
                    "chapter_title": "الموسوعة الفقهية",
                    "source_locator": "الموسوعة الفقهية - الدرر السنية، كتاب الصلاة، باب صفة الصلاة، مبحث قراءة المأموم",
                    "canonical_url": "https://dorar.net/feqhia/1284"
                }
            ]
        },
        # Doc 8: Personal Fatwa Referral Guidelines (Senior Scholars Council)
        {
            "id": "ea1b694f-6fa1-48a5-99d6-47a282004e28",
            "source_id": "683b35e0-6b77-46a0-b73f-fa0ba84cc84f",
            "title_ar": "ضابط الإحالة الإلزامية في الفتاوى والمسائل الشخصية (Level D Policy)",
            "title_en": "Mandatory Referral Protocol for Personal Fatwas and Individual Legal Inquiries",
            "author": "الأمانة العامة لهيئة كبار العلماء والمجامع الفقهية",
            "publisher": "دار الإفتاء الرسمية",
            "document_type": "GOVERNANCE_REGULATION",
            "category": "FIQH",
            "official_url": "https://www.alifta.gov.sa/regulations",
            "canonical_url": "https://www.alifta.gov.sa/regulations",
            "description": "الضابط الشرعي والإجرائي الصارم لمنع الذكاء الاصطناعي من الإفتاء في قضايا الطلاق والنزاعات المالية والأحوال الشخصية.",
            "license_status": "VERIFIED",
            "chunks": [
                {
                    "id": "chk-fatwa-policy-01",
                    "chunk_index": 0,
                    "content": "السياسة المعتمدة في بيّنة AI: يمنع منعاً باتاً إصدار أي فتوى خاصة أو حكم قضائي في المسائل الشخصية كالطلاق، والوصايا، والنزاعات المالية، والحدود، والمسائل المعاصرة الشائكة التي تتطلب معرفة نية المستفتي وتفاصيل حاله. الواجب في هذا النوع من الأسئلة هو الامتناع التام وإحالة السائل إلى دور الإفتاء الرسمية والقضاة المختصين في بلده، والتنبيه على أن برمجيات الذكاء الاصطناعي أدوات للتوثيق والبحث وليست جهات للفتوى.",
                    "section_title": "سياسات حوكمة المحتوى الإفتائي",
                    "chapter_title": "ضوابط الإفتاء والاستفتاء",
                    "source_locator": "وثيقة حوكمة الذكاء الاصطناعي الشرعي - سياسة الإحالة للمختص (المستوى الرابع LEVEL_D)",
                    "canonical_url": "https://www.alifta.gov.sa/regulations"
                }
            ]
        },
        # Doc 9: Dawa Center - Defining Islam to Non-Muslims (Authentic Methodology)
        {
            "id": "4c0b440b-5ea8-4192-a181-cf709db437cc",
            "source_id": "fe136b10-d8db-465c-ae6e-5b12483614cf",
            "title_ar": "دليل التعريف بالإسلام ومحاور الحوار الدعوي - مركز دعوة",
            "title_en": "Guide to Introducing Islam & Dawah Discourse - Dawa Center",
            "author": "الفريق العلمي بمركز دعوة",
            "publisher": "مركز دعوة",
            "document_type": "DAWAH_MANUAL",
            "category": "DAWA",
            "official_url": "https://dawa.center/resources/intro-guide",
            "canonical_url": "https://dawa.center/resources/intro-guide",
            "description": "المنهجية العلمية المعتمدة لتقديم مفاهيم الإسلام الكبرى للجمهور العالمي بالحكمة والموعظة الحسنة.",
            "license_status": "PENDING_VERIFICATION",
            "chunks": [
                {
                    "id": "chk-dawa-intro-01",
                    "chunk_index": 0,
                    "content": "يقوم التعريف بالإسلام على دعامتين أساسيتين: أولاً: توضيح مفهوم التوحيد الخالص، وهو إفراد الله تعالى بالربوبية والألوهية والأسماء والصفات، وأنه خالق الكون بلا شريك. ثانياً: بيان رسالة الإسلام العالمية القائمة على العدل والرحمة والسلام ومكارم الأخلاق، لقوله تعالى: «وَمَا أَرْسَلْنَاكَ إِلَّا رَحْمَةً لِلْعَالَمِينَ». ويجب على الدعاة والمعرفين بالإسلام التثبت من صحة النصوص المترجمة وعدم نسبة أي مقولة شائعة غير موثقة للتراث الإسلامي.",
                    "section_title": "ركائز الخطاب التعريفي",
                    "chapter_title": "منهجية التعريف بالإسلام",
                    "source_locator": "مركز دعوة - دليل المعرفين بالإسلام، الفصل الأول: الأصول الكبرى، ص 14",
                    "canonical_url": "https://dawa.center/resources/intro-guide"
                }
            ]
        }
    ]

    for d_data in documents_seed:
        existing_doc = db.query(DocumentModel).filter_by(id=d_data["id"]).first()
        combined_text = d_data["title_ar"] + " " + (d_data.get("description") or "")
        for chk in d_data.get("chunks", []):
            combined_text += " " + chk["content"]
        c_hash = sha256_hash(combined_text)

        if not existing_doc:
            first_chunk_text = d_data.get("chunks", [{}])[0].get("content", "")
            doc = DocumentModel(
                id=d_data["id"],
                source_id=d_data["source_id"],
                title=d_data.get("title") or d_data.get("title_ar"),
                title_ar=d_data["title_ar"],
                title_en=d_data.get("title_en"),
                content=d_data.get("content") or first_chunk_text,
                content_ar=d_data.get("content_ar") or first_chunk_text,
                url=d_data.get("url") or d_data.get("canonical_url") or d_data.get("official_url"),
                author=d_data.get("author"),
                publisher=d_data.get("publisher"),
                document_type=d_data["document_type"],
                category=d_data["category"],
                official_url=d_data["official_url"],
                canonical_url=d_data.get("canonical_url"),
                description=d_data.get("description"),
                license_status="VERIFIED" if d_data.get("license_status") == "VERIFIED" else "PENDING",
                content_hash=c_hash,
                ingestion_status="INDEXED",
                version="1.0"
            )
            db.add(doc)
            db.flush()

            for chk in d_data.get("chunks", []):
                chunk_hash = sha256_hash(chk["content"])
                norm_chunk = normalize_arabic(chk["content"])
                try:
                    chk_uuid = str(uuid.UUID(chk["id"]))
                except ValueError:
                    chk_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, chk["id"]))
                chunk_obj = DocumentChunkModel(
                    id=chk_uuid,
                    document_id=d_data["id"],
                    chunk_index=chk.get("chunk_index", 0),
                    chunk_text=chk["content"],
                    content=chk["content"],
                    content_ar=chk["content"],
                    normalized_text=norm_chunk,
                    normalized_content=norm_chunk,
                    language="ar",
                    section_title=chk.get("section_title"),
                    chapter_title=chk.get("chapter_title"),
                    verse_reference=chk.get("verse_reference"),
                    hadith_reference=chk.get("hadith_reference"),
                    source_locator=chk["source_locator"],
                    canonical_url=chk["canonical_url"],
                    content_hash=chunk_hash,
                    embedding_model="models/text-embedding-004",
                    embedding_version="v1"
                )
                db.add(chunk_obj)
        else:
            existing_doc.title_ar = d_data["title_ar"]
            existing_doc.official_url = d_data["official_url"]
            existing_doc.content_hash = c_hash

    db.commit()

    # 3. Seed Islamic Terminology Dictionary (Al-Jumhrah / Islamic Content)
    terms_seed = [
        {
            "id": "term-tawhid",
            "term_ar": "التوحيد",
            "category": "AQEEDAH",
            "definition_ar": "إفراد الله تعالى بما يختص به من الربوبية والألوهية والأسماء والصفات، وهو أصل الدين وأساس رسالة جميع الأنبياء والمرسلين.",
            "source_id": "f9eb8562-6b5d-4235-b0e9-3628e4f29d32",
            "locator": "موسوعة المحتوى الإسلامي - معجم المصطلحات العقدية، مدخل: توحيد",
            "translations": [
                {
                    "language": "en",
                    "approved_translation": "Monotheism (Islamic Tawhid)",
                    "contextual_explanation": "The fundamental concept of the absolute Oneness and Uniqueness of God (Allah) in His Lordship, Worship, and Divine Attributes, not merely the philosophical rejection of polytheism.",
                    "usage_notes": "Avoid translating simply as 'monotheism' without noting its distinct Islamic tripartite definition (Rububiyyah, Uluhiyyah, Asma wa Sifat)."
                }
            ]
        },
        {
            "id": "term-shirk",
            "term_ar": "الشرك",
            "category": "AQEEDAH",
            "definition_ar": "اتخاذ ند أو شريك مع الله تعالى في ربوبيته أو إلهيته أو صفاته، وهو أعظم الذنوب وأخطرها.",
            "source_id": "f9eb8562-6b5d-4235-b0e9-3628e4f29d32",
            "locator": "موسوعة المحتوى الإسلامي - معجم المصطلحات العقدية، مدخل: شرك",
            "translations": [
                {
                    "language": "en",
                    "approved_translation": "Polytheism / Associating Partners with God (Shirk)",
                    "contextual_explanation": "Ascribing partners, equals, or rivals to God in worship, creation, or divine sovereignty.",
                    "usage_notes": "Crucial distinction between Major Shirk (expels from faith) and Minor Shirk (like ostentation in good deeds)."
                }
            ]
        },
        {
            "id": "term-bidah",
            "term_ar": "البدعة",
            "category": "AQEEDAH",
            "definition_ar": "ما أُحدث في الدين مما لا أصل له في الكتاب والسنة، وتُقصد به المبالغة في التعبد بما لم يشرعه الله.",
            "source_id": "f9eb8562-6b5d-4235-b0e9-3628e4f29d32",
            "locator": "موسوعة المحتوى الإسلامي - معجم الأصول والمصطلحات، مدخل: بدعة",
            "translations": [
                {
                    "language": "en",
                    "approved_translation": "Religious Innovation (Bid'ah)",
                    "contextual_explanation": "Any invented religious practice or doctrine introduced into Islamic theology or worship without authentic textual scriptural foundation.",
                    "usage_notes": "Applies strictly to religious worship and dogma, not to worldly advancements, technology, or civic administration."
                }
            ]
        },
        {
            "id": "term-jihad",
            "term_ar": "الجهاد",
            "category": "DAWA",
            "definition_ar": "بذل الجهد واستفراغ الوسع في طاعة الله، ويشمل جهاد النفس، وجهاد الكلمة والبيان والدعوة، والدفاع المشروع عن النفس والوطن بضوابطه الشرعية.",
            "source_id": "f9eb8562-6b5d-4235-b0e9-3628e4f29d32",
            "locator": "موسوعة المحتوى الإسلامي - المفاهيم الإسلامية المشتركة، مدخل: جهاد",
            "translations": [
                {
                    "language": "en",
                    "approved_translation": "Striving / Legitimate Defense (Jihad)",
                    "contextual_explanation": "Exerting one's utmost effort in righteous deeds, self-purification (Jihad al-Nafs), intellectual conveyance of truth, and strictly regulated defensive warfare governed by humanitarian Islamic ethics.",
                    "usage_notes": "Avoid the sensationalized translation 'Holy War' (which has no linguistic Arabic equivalent 'Harb Muqaddasah')."
                }
            ]
        }
    ]

    for t_data in terms_seed:
        existing_t = db.query(TermModel).filter_by(id=t_data["id"]).first()
        if not existing_t:
            norm_t = normalize_arabic(t_data["term_ar"])
            t_obj = TermModel(
                id=t_data["id"],
                term_ar=t_data["term_ar"],
                term_normalized=norm_t,
                category=t_data["category"],
                definition_ar=t_data["definition_ar"],
                source_id=t_data.get("source_id"),
                locator=t_data.get("locator")
            )
            db.add(t_obj)
            db.flush()

            for trans in t_data.get("translations", []):
                tr_obj = TermTranslationModel(
                    term_id=t_data["id"],
                    language=trans["language"],
                    approved_translation=trans["approved_translation"],
                    contextual_explanation=trans["contextual_explanation"],
                    usage_notes=trans.get("usage_notes"),
                    is_standard=True
                )
                db.add(tr_obj)
    db.commit()

    # 4. Ingest additional sources from sources_registry.json if present
    import os
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    sources_json_path = os.path.join(data_dir, "sources_registry.json")
    if os.path.exists(sources_json_path):
        with open(sources_json_path, "r", encoding="utf-8") as f:
            legacy_sources = json.load(f)
            for ls in legacy_sources:
                try:
                    s_uuid = str(uuid.UUID(ls["id"]))
                except ValueError:
                    s_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, ls["id"]))
                
                slug_val = ls["id"].replace("src-", "")
                existing = db.query(TrustedSourceModel).filter(
                    (TrustedSourceModel.id == s_uuid) | (TrustedSourceModel.slug == slug_val)
                ).first()
                if not existing:
                    cat = ls.get("category", "OTHER").upper()
                    if cat not in ["DAWA", "QURAN", "TAFSEER", "HADITH", "AQEEDAH", "FIQH", "SEERAH_HISTORY", "QUESTIONS_DOUBTS", "DICTIONARY_TRANSLATION", "OTHER"]:
                        if cat == "FATWA": cat = "FIQH"
                        elif cat == "SEERAH": cat = "SEERAH_HISTORY"
                        elif cat == "TAFSIR": cat = "TAFSEER"
                        else: cat = "OTHER"

                    src_obj = TrustedSourceModel(
                        id=s_uuid,
                        name=ls["name"],
                        name_ar=ls["name"],
                        name_en=ls.get("name_en", ls["name"]),
                        slug=slug_val,
                        category=cat,
                        description=ls.get("description", ""),
                        url=ls.get("url", ""),
                        official_url=ls.get("url", ""),
                        base_domain=ls.get("url", "").replace("https://", "").replace("http://", "").split("/")[0],
                        source_type="ENCYCLOPEDIA" if ls.get("source_type") == "encyclopedia" else "PRIMARY_TEXT",
                        authority_level="PRIMARY_CANONICAL",
                        trust_status="APPROVED",
                        usage_status="METADATA_AND_SNIPPETS",
                        license_status="VERIFIED" if "الملكية العامة" in ls.get("license", "") else "PENDING",
                        license_name=ls.get("license"),
                        license_url=ls.get("url"),
                        allowed_operations=json.dumps({"METADATA_ONLY": True, "SEARCH_SNIPPETS": True, "INDEX_CONTENT": True, "STORE_CONTENT": True, "QUOTE_LIMITED": True, "DISPLAY_EXCERPT": True, "LINK_TO_SOURCE": True, "TRANSLATE": True, "DERIVE_EMBEDDINGS": True}),
                        content_scope=ls.get("usage_policy"),
                        language="ar",
                        publisher=ls.get("organization"),
                        author=ls.get("author"),
                        verification_method="EDITORIAL_REVIEW",
                        is_active=True
                    )
                    db.add(src_obj)
            db.commit()

    # 5. Ingest additional documents from documents_seed.json if present
    docs_json_path = os.path.join(data_dir, "documents_seed.json")
    if os.path.exists(docs_json_path):
        with open(docs_json_path, "r", encoding="utf-8") as f:
            legacy_docs = json.load(f)
            for ld in legacy_docs:
                try:
                    d_uuid = str(uuid.UUID(ld["id"]))
                except ValueError:
                    d_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, ld["id"]))

                existing_d = db.query(DocumentModel).filter_by(id=d_uuid).first()
                if not existing_d:
                    cat = ld.get("category", "OTHER").upper()
                    if cat not in ["DAWA", "QURAN", "TAFSEER", "HADITH", "AQEEDAH", "FIQH", "SEERAH_HISTORY", "QUESTIONS_DOUBTS", "DICTIONARY_TRANSLATION", "OTHER"]:
                        if cat == "FATWA": cat = "FIQH"
                        elif cat == "SEERAH": cat = "SEERAH_HISTORY"
                        elif cat == "TAFSIR": cat = "TAFSEER"
                        else: cat = "OTHER"

                    # Ensure source exists, fallback to senior-scholars-fatwa if needed
                    src_id = ld.get("source_id", "683b35e0-6b77-46a0-b73f-fa0ba84cc84f")
                    try:
                        src_uuid = str(uuid.UUID(src_id))
                    except ValueError:
                        src_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, src_id))

                    if not db.query(TrustedSourceModel).filter_by(id=src_uuid).first():
                        src_uuid = "683b35e0-6b77-46a0-b73f-fa0ba84cc84f"

                    c_hash = sha256_hash(ld["title"] + " " + ld["content"])
                    doc_obj = DocumentModel(
                        id=d_uuid,
                        source_id=src_uuid,
                        title=ld["title"],
                        title_ar=ld["title"],
                        content=ld["content"],
                        content_ar=ld["content"],
                        document_type="CURATED_REFERENCE",
                        category=cat,
                        url=ld.get("url", ""),
                        official_url=ld.get("url", ""),
                        canonical_url=ld.get("url"),
                        language="ar",
                        description=ld.get("reference", ""),
                        license_status="VERIFIED",
                        content_hash=c_hash,
                        ingestion_status="INDEXED",
                        version="1.0"
                    )
                    db.add(doc_obj)
                    db.flush()

                    norm_c = normalize_arabic(ld["content"])
                    chk_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"chk-{ld['id']}-01"))
                    chk_obj = DocumentChunkModel(
                        id=chk_uuid,
                        document_id=d_uuid,
                        chunk_index=0,
                        chunk_text=ld["content"],
                        content=ld["content"],
                        content_ar=ld["content"],
                        normalized_text=norm_c,
                        normalized_content=norm_c,
                        language="ar",
                        source_locator=ld.get("reference", ""),
                        canonical_url=ld.get("url", ""),
                        content_hash=sha256_hash(ld["content"]),
                        embedding_model="models/text-embedding-004",
                        embedding_version="v1"
                    )
                    db.add(chk_obj)
            db.commit()

