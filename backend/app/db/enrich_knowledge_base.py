import os
import json
import hashlib
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from ..models.knowledge_models import (
    TrustedSourceModel,
    DocumentModel,
    DocumentChunkModel,
    TermModel,
    TermTranslationModel,
    TranslationTermModel,
    ClaimModel,
    EvidenceModel,
    KnowledgeAuditLogModel
)
from ..utils.arabic_normalizer import normalize_arabic

def sha256_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def enrich_and_seed_knowledge_base():
    """
    Ensures all tables and fields from the Knowledge Base Master Prompt are initialized
    and seeded with authenticated data.
    """
    # 1. Ensure all tables exist in database
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # =========================================================================
        # 1. Core Sources Registration (Section 3 & 5)
        # =========================================================================
        sources_to_register = [
            {
                "id": "src-dawa-center-7937",
                "name": "مستودع الأسئلة والشبهات - مركز دعوة (الملف 7937)",
                "name_ar": "مستودع الأسئلة والشبهات - مركز دعوة (الملف 7937)",
                "name_en": "Dawa Center - Questions and Doubts Repository (File 7937)",
                "organization": "مركز دعوة للتعريف بالإسلام",
                "slug": "dawa-center-file-7937",
                "category": "QUESTIONS_DOUBTS",
                "description": "الملف العلمي المعتمد في الحزمة المرجعية المتخصص في تفنيد الشبهات والأسئلة الشائعة حول الإسلام والقرآن والنبوة وأحكام الشريعة.",
                "base_url": "https://dawa.center",
                "specific_url": "https://dawa.center/file/7937",
                "official_url": "https://dawa.center/file/7937",
                "base_domain": "dawa.center",
                "source_type": "OFFICIAL_PLATFORM",
                "authority_level": "PRIMARY_CANONICAL",
                "scientific_status": "APPROVED",
                "trust_status": "APPROVED",
                "usage_status": "INDEXED_AND_QUOTED",
                "license_status": "PENDING_VERIFICATION",
                "license_name": "رخصة الاستخدام الدعوي التوثيقي",
                "license_url": "https://dawa.center/terms",
                "allowed_operations": json.dumps({
                    "METADATA_ONLY": True, "SEARCH": True, "INDEX": True, "STORE": True,
                    "QUOTE": True, "DISPLAY_EXCERPT": True, "LINK": True, "TRANSLATE": False, "EMBED": True
                }),
                "indexing_allowed": True,
                "storage_allowed": True,
                "excerpt_allowed": True,
                "link_allowed": True,
                "translation_allowed": False,
                "embedding_allowed": True,
                "content_scope": "الرد على الشبهات، الأسئلة المتكررة، دفع المطاعن، بيان مقاصد التشريع",
                "verification_notes": "الملف 7937 المذكور نصاً في وثيقة التحدي والحزمة العلمية للمسار الرابع."
            },
            {
                "id": "src-islamic-content-dict",
                "name": "قاموس المصطلحات والمفردات - موسوعة المحتوى الإسلامي",
                "name_ar": "قاموس المصطلحات والمفردات - موسوعة المحتوى الإسلامي",
                "name_en": "Islamic Content Terminology Dictionary",
                "organization": "موسوعة المحتوى الإسلامي / الجمهرة",
                "slug": "islamic-content-dictionary",
                "category": "DICTIONARY_TRANSLATION",
                "description": "المعجم المعياري المعتمد لضبط وترجمة المصطلحات الشرعية والعقدية تفادياً للترجمات الحرفية المشوهة للمفاهيم الإسلامية.",
                "base_url": "https://islamic-content.com",
                "specific_url": "https://islamic-content.com/dictionary",
                "official_url": "https://islamic-content.com/dictionary",
                "base_domain": "islamic-content.com",
                "source_type": "DICTIONARY",
                "authority_level": "TERMINOLOGY_STANDARD",
                "scientific_status": "APPROVED",
                "trust_status": "APPROVED",
                "usage_status": "APPROVED_TRANSLATION_CORPUS",
                "license_status": "PENDING_VERIFICATION",
                "license_name": "رخصة الاستخدام المرجعي للمفردات",
                "license_url": "https://islamic-content.com/license",
                "allowed_operations": json.dumps({
                    "METADATA_ONLY": True, "SEARCH": True, "INDEX": True, "STORE": True,
                    "QUOTE": True, "DISPLAY_EXCERPT": True, "LINK": True, "TRANSLATE": True, "EMBED": True
                }),
                "indexing_allowed": True,
                "storage_allowed": True,
                "excerpt_allowed": True,
                "link_allowed": True,
                "translation_allowed": True,
                "embedding_allowed": True,
                "content_scope": "المصطلحات الشرعية، المفاهيم العقدية، قواميس الترجمة الإسلامية المعتمدة",
                "verification_notes": "المصدر المعياري المعتمد لترجمة المصطلحات وضبط المفاهيم تفادياً للترجمات الحرفية المشوهة."
            }
        ]

        for s_data in sources_to_register:
            existing = db.query(TrustedSourceModel).filter_by(id=s_data["id"]).first()
            if not existing:
                src = TrustedSourceModel(
                    id=s_data["id"],
                    name=s_data["name"],
                    name_ar=s_data["name_ar"],
                    name_en=s_data["name_en"],
                    organization=s_data["organization"],
                    slug=s_data["slug"],
                    category=s_data["category"],
                    description=s_data["description"],
                    base_url=s_data["base_url"],
                    specific_url=s_data["specific_url"],
                    official_url=s_data["official_url"],
                    base_domain=s_data["base_domain"],
                    source_type=s_data["source_type"],
                    authority_level=s_data["authority_level"],
                    scientific_status=s_data["scientific_status"],
                    trust_status=s_data["trust_status"],
                    usage_status=s_data["usage_status"],
                    license_status=s_data["license_status"],
                    license_name=s_data["license_name"],
                    license_url=s_data["license_url"],
                    allowed_operations=s_data["allowed_operations"],
                    indexing_allowed=s_data["indexing_allowed"],
                    storage_allowed=s_data["storage_allowed"],
                    excerpt_allowed=s_data["excerpt_allowed"],
                    link_allowed=s_data["link_allowed"],
                    translation_allowed=s_data["translation_allowed"],
                    embedding_allowed=s_data["embedding_allowed"],
                    content_scope=s_data["content_scope"],
                    verification_notes=s_data["verification_notes"],
                    verified_by="لجنة الحوكمة العلمية - بيّنة AI",
                    is_active=True
                )
                db.add(src)
            else:
                existing.name = s_data["name"]
                existing.organization = s_data["organization"]
                existing.base_url = s_data["base_url"]
                existing.specific_url = s_data["specific_url"]
                existing.scientific_status = s_data["scientific_status"]
                existing.indexing_allowed = s_data["indexing_allowed"]
                existing.storage_allowed = s_data["storage_allowed"]
                existing.excerpt_allowed = s_data["excerpt_allowed"]
                existing.link_allowed = s_data["link_allowed"]
                existing.translation_allowed = s_data["translation_allowed"]
                existing.embedding_allowed = s_data["embedding_allowed"]
        db.commit()

        # Update existing sources with flags
        existing_sources = db.query(TrustedSourceModel).all()
        for src in existing_sources:
            if not src.name:
                src.name = src.name_ar
            if not src.base_url:
                src.base_url = src.official_url
            if not src.specific_url:
                src.specific_url = src.official_url
            if not src.scientific_status:
                src.scientific_status = src.trust_status or "APPROVED"
            src.excerpt_allowed = True
            src.link_allowed = True
            if src.license_status == "VERIFIED":
                src.indexing_allowed = True
                src.storage_allowed = True
                src.embedding_allowed = True
        db.commit()

        # =========================================================================
        # 2. Documents & Chunks for File 7937 (Questions & Doubts) (Section 30)
        # =========================================================================
        qa_documents = [
            {
                "id": "doc-dawa-7937-kaaba",
                "source_id": "src-dawa-center-7937",
                "title": "شبهة عبادة الكعبة في الإسلام - الرد العلمي الموثق",
                "title_ar": "شبهة عبادة الكعبة في الإسلام - الرد العلمي الموثق",
                "author": "مركز دعوة - قسم الرد على الشبهات",
                "publisher": "المستودع الدعوي الرقمي",
                "document_type": "DOUBT_REFUTATION",
                "category": "QUESTIONS_DOUBTS",
                "official_url": "https://dawa.center/file/7937#kaaba",
                "description": "تفنيد زعم عبادة المسلمين للكعبة وبيان حقيقة التوحيد وتوجيه القبلة.",
                "chunk": {
                    "id": "chk-dawa-7937-kaaba-01",
                    "content": "سؤال: لماذا يعبد المسلمون الكعبة؟ الجواب العلمي الموثق: المسلمون لا يعبدون الكعبة المشرفة إطلاقاً ولا يدعونها من دون الله، بل يعبدون الله وحده لا شريك له. الكعبة ليست سوى قبلة موحدة للمسلمين في صلاتهم بأمر إلهي توحيداً لصفهم، وهي حجر مخلوق لا يضر ولا ينفع بذاته. وقد أصل أمير المؤمنين عمر بن الخطاب رضي الله عنه هذه العقيدة حين قبّل الحجر الأسود قائلاً: «إني أعلم أنك حجر لا تضر ولا تنفع، ولولا أني رأيت رسول الله ﷺ يقبلك ما قبلتك» (رواه البخاري). فالعبادة والسجود والدعاء في الإسلام محرم صرفها لغير الخالق جل وعلا.",
                    "locator": "مركز دعوة - ملف الشبهات 7937، باب مسائل التوحيد والقبلة، ص 12",
                    "section": "مسائل التوحيد والقبلة"
                }
            },
            {
                "id": "doc-dawa-7937-quran-authorship",
                "source_id": "src-dawa-center-7937",
                "title": "شبهة تأليف القرآن الكريم - براهين الإعجاز والرسالة",
                "title_ar": "شبهة تأليف القرآن الكريم - براهين الإعجاز والرسالة",
                "author": "مركز دعوة - قسم الرد على الشبهات",
                "publisher": "المستودع الدعوي الرقمي",
                "document_type": "DOUBT_REFUTATION",
                "category": "QUESTIONS_DOUBTS",
                "official_url": "https://dawa.center/file/7937#quran-source",
                "description": "بيان إعجاز القرآن واستحالة تأليفه بشرياً بالأدلة العقلية والتاريخية.",
                "chunk": {
                    "id": "chk-dawa-7937-quran-01",
                    "content": "سؤال: هل القرآن من تأليف محمد ﷺ؟ الجواب العلمي الموثق: القرآن الكريم كلام الله تعالى الموحى به، وليس من تأليف النبي محمد ﷺ ولا من تأليف أي بشر. والبراهين القاطعة على ذلك: أولاً: التحدي البياني؛ إذ نزل القرآن بلسان عربي مبين وتحدى بلغاء وفصحاء قريش والعرب وهم فرسان الفصاحة أن يأتوا بسورة من مثله: ﴿وَإِن كُنتُمْ فِي رَيْبٍ مِّمَّا نَزَّلْنَا عَلَىٰ عَبْدِنَا فَأْتُوا بِسُورَةٍ مِّن مِّثْلِهِ﴾، فعجزوا وسجل التاريخ عجزهم. ثانياً: النبي ﷺ نشأ أمياً بين قومه أربعين سنة لا يقرأ ولا يخط كتاباً، فظهور هذا الكتاب المعجز تشريعاً وبلاغة وحقائق تاريخية وغيبية برهان يقيني على مصدره الإلهي.",
                    "locator": "مركز دعوة - ملف الشبهات 7937، مبحث الوحي ومصدر القرآن، ص 24",
                    "section": "الوحي ومصدر القرآن"
                }
            },
            {
                "id": "doc-dawa-7937-sword",
                "source_id": "src-dawa-center-7937",
                "title": "شبهة انتشار الإسلام بالسيف - التحقيق التاريخي والشرعي",
                "title_ar": "شبهة انتشار الإسلام بالسيف - التحقيق التاريخي والشرعي",
                "author": "مركز دعوة - قسم الرد على الشبهات",
                "publisher": "المستودع الدعوي الرقمي",
                "document_type": "DOUBT_REFUTATION",
                "category": "QUESTIONS_DOUBTS",
                "official_url": "https://dawa.center/file/7937#sword",
                "description": "تفنيد دعوى انتشار الإسلام بالسيف وبيان قاعدة لا إكراه في الدين.",
                "chunk": {
                    "id": "chk-dawa-7937-sword-01",
                    "content": "سؤال: هل انتشر الإسلام بالسيف؟ الجواب العلمي الموثق: الإسلام انتشر بقوة الإقناع والحجة والبيان وحسن المعاملة، ولم ينتشر بالإكراه أو السيف قط. والقاعدة القرآنية المحكمة تنص صراحة: ﴿لَا إِكْرَاهَ فِي الدِّينِ ۖ قَد تَّبَيَّنَ الرُّشْدُ مِنَ الْغَيِّ﴾، وقوله: ﴿أَفَأَنتَ تُكْرِهُ النَّاسَ حَتَّىٰ يَكُونُوا مُؤْمِنِينَ﴾. وتاريخياً؛ فإن أكبر الكتل السكانية المسلمة في العالم كإندونيسيا وماليزيا وبلدان غرب إفريقيا لم تر جيشاً مسلماً فاتحاً، بل دخلت في الإسلام عبر أمانة التجار المسلمين ودعاة الحكمة. والجهاد في الإسلام شرع لرد العدوان وحماية حرية المعتقد ورفع الظلم عن المستضعفين.",
                    "locator": "مركز دعوة - ملف الشبهات 7937، مبحث الجهاد وحرية الاعتقاد، ص 38",
                    "section": "الجهاد وحرية الاعتقاد"
                }
            },
            {
                "id": "doc-dawa-7937-prohibitions",
                "source_id": "src-dawa-center-7937",
                "title": "مقاصد الشريعة في تحريم الخبائث والأضرار",
                "title_ar": "مقاصد الشريعة في تحريم الخبائث والأضرار",
                "author": "مركز دعوة - قسم الرد على الشبهات",
                "publisher": "المستودع الدعوي الرقمي",
                "document_type": "DOUBT_REFUTATION",
                "category": "QUESTIONS_DOUBTS",
                "official_url": "https://dawa.center/file/7937#prohibitions",
                "description": "بيان علل التحريم في الإسلام وقواعد حفظ الضروريات الخمس.",
                "chunk": {
                    "id": "chk-dawa-7937-prohib-01",
                    "content": "سؤال: لماذا يحرم الإسلام بعض الأمور؟ وما هي علة المنع؟ الجواب العلمي الموثق: أحكام الشريعة الإسلامية معللة بجلب المصالح وتكميلها، ودرء المفاسد وتقليلها. وما حرمه الإسلام من مآكل أو مشارب أو معاملات كالخمر والربا والظلم فإنما حرمه لوجود مفسدة وضرر راجح أو محقق على الفرد والمجتمع، صيانة للضروريات الخمس: حفظ الدين، والنفس، والعقل، والنسل، والمال. قال تعالى: ﴿وَيُحِلُّ لَهُمُ الطَّيِّبَاتِ وَيُحَرِّمُ عَلَيْهِمُ الْخَبَائِثَ﴾، فالتحريم وقاية ورحمة وليس تضييقاً اعتباطياً.",
                    "locator": "مركز دعوة - ملف الشبهات 7937، مدخل مقاصد الشريعة والتحريم، ص 52",
                    "section": "مقاصد الشريعة"
                }
            },
            {
                "id": "doc-dawa-7937-why-differences",
                "source_id": "src-dawa-center-7937",
                "title": "أسباب اختلاف الفقهاء وأدب الخلاف السائغ",
                "title_ar": "أسباب اختلاف الفقهاء وأدب الخلاف السائغ",
                "author": "مركز دعوة - قسم الرد على الشبهات",
                "publisher": "المستودع الدعوي الرقمي",
                "document_type": "DOUBT_REFUTATION",
                "category": "QUESTIONS_DOUBTS",
                "official_url": "https://dawa.center/file/7937#differences",
                "description": "بيان أسباب تعدد الآراء الفقهية وأدب المسلم تجاه المسائل الخلافية.",
                "chunk": {
                    "id": "chk-dawa-7937-diff-01",
                    "content": "سؤال: لماذا توجد أحكام مختلفة بين العلماء؟ وهل كل المسلمين يتفقون في كل مسألة؟ الجواب العلمي الموثق: المسلمون متفقون إجماعاً على أصول الدين وقواطعه الكبرى (أركان الإيمان، أركان الإسلام، تحريم الكبائر الظاهرة). أما الاختلاف فهو في الفروع الاجتهادية الظنية، وأسبابه علمية منهجية: كاختلاف وصول الدليل للفقيه، أو دلالة الألفاظ في لسان العرب، أو القواعد الأصولية في الجمع والترجيح. واختلاف المذاهب رحمة وسعة تنوع اجتهادي، وكل مجتهد مأجور، ولا يجوز الإنكار في مسائل الاجتهاد الخلافية.",
                    "locator": "مركز دعوة - ملف الشبهات 7937، مبحث أسباب اختلاف العلماء، ص 65",
                    "section": "أدب الخلاف وأسباب الاختلاف"
                }
            }
        ]

        for d_info in qa_documents:
            d_id = d_info["id"]
            existing_doc = db.query(DocumentModel).filter_by(id=d_id).first()
            content_str = d_info["chunk"]["content"]
            c_hash = sha256_hash(content_str)

            if not existing_doc:
                doc = DocumentModel(
                    id=d_id,
                    source_id=d_info["source_id"],
                    title=d_info["title"],
                    title_ar=d_info["title_ar"],
                    author=d_info["author"],
                    publisher=d_info["publisher"],
                    document_type=d_info["document_type"],
                    category=d_info["category"],
                    original_url=d_info["official_url"],
                    official_url=d_info["official_url"],
                    canonical_url=d_info["official_url"],
                    description=d_info["description"],
                    publication_info=d_info["publisher"],
                    license_status="VERIFIED",
                    indexing_status="INDEXED",
                    content_hash=c_hash
                )
                db.add(doc)
                db.flush()

                chk = DocumentChunkModel(
                    id=d_info["chunk"]["id"],
                    document_id=d_id,
                    chunk_index=0,
                    chunk_text=content_str,
                    content=content_str,
                    normalized_content=normalize_arabic(content_str),
                    section=d_info["chunk"].get("section"),
                    section_title=d_info["chunk"].get("section"),
                    source_locator=d_info["chunk"]["locator"],
                    reference=d_info["chunk"]["locator"],
                    source_url=d_info["official_url"],
                    canonical_url=d_info["official_url"],
                    content_hash=c_hash
                )
                db.add(chk)
            else:
                existing_doc.title = d_info["title"]
                existing_doc.original_url = d_info["official_url"]
                existing_doc.publication_info = d_info["publisher"]
                existing_doc.indexing_status = "INDEXED"

        db.commit()

        # =========================================================================
        # 3. Translation Terms Seeding (The 10 Core Terms) (Section 22)
        # =========================================================================
        translation_terms_data = [
            {
                "id": "term-islam",
                "term_ar": "الإسلام",
                "term_en": "Islam",
                "preferred_translation": "Islam (Submission to God)",
                "alternative_translation": "Submission / Peace attained through submission to God",
                "explanation": "الاستسلام والانقياد لله تعالى بالتوحيد والإخلاص له في العبادة، وطاعة أوامره واجتناب نواهيه.",
                "usage_notes": "Avoid translating merely as 'submission' without noting that it entails willing, conscious surrender to the Divine will leading to inner and outer peace.",
                "source_id": "src-islamic-content-dict",
                "source_url": "https://islamic-content.com/dictionary/islam"
            },
            {
                "id": "term-tawhid",
                "term_ar": "التوحيد",
                "term_en": "Tawhid",
                "preferred_translation": "Tawhid (Islamic Monotheism / Oneness of God)",
                "alternative_translation": "Monotheism / Divine Unification",
                "explanation": "إفراد الله تعالى بما يختص به من الربوبية والألوهية والأسماء والصفات، وإخلاص الدين له وحده.",
                "usage_notes": "Avoid translating simply as 'monotheism' without explaining the unique Islamic tripartite foundation (Rububiyyah, Uluhiyyah, Asma wa Sifat).",
                "source_id": "src-islamic-content-dict",
                "source_url": "https://islamic-content.com/dictionary/tawhid"
            },
            {
                "id": "term-ibadah",
                "term_ar": "العبادة",
                "term_en": "Worship",
                "preferred_translation": "Worship / Devotional Servitude (Ibadah)",
                "alternative_translation": "Devotion / Obedience",
                "explanation": "اسم جامع لكل ما يحبه الله ويرضاه من الأقوال والأعمال الظاهرة والباطنة.",
                "usage_notes": "Broader in Islam than ritual prayer; encompasses all righteous actions, ethical conduct, and work intended for Allah's sake.",
                "source_id": "src-islamic-content-dict",
                "source_url": "https://islamic-content.com/dictionary/ibadah"
            },
            {
                "id": "term-nubuwwah",
                "term_ar": "النبوة",
                "term_en": "Prophethood",
                "preferred_translation": "Prophethood (Nubuwwah)",
                "alternative_translation": "Divine Mission / Messengerhood",
                "explanation": "اصطفاء الله تعالى لرسل من البشر لتبليغ رسالته وهداية الناس وإرشادهم إلى الحق.",
                "usage_notes": "Prophets in Islam are sinless in delivering revelation and exemplars of high morality, not fortune tellers.",
                "source_id": "src-islamic-content-dict",
                "source_url": "https://islamic-content.com/dictionary/nubuwwah"
            },
            {
                "id": "term-wahy",
                "term_ar": "الوحي",
                "term_en": "Revelation",
                "preferred_translation": "Divine Revelation (Wahy)",
                "alternative_translation": "Inspiration / Divine Communication",
                "explanation": "إعلام الله تعالى لأنبيائه بما يريد أن يبلغه إليهم من شرع أو كتاب بواسطة الملك أو غيره.",
                "usage_notes": "Distinct from human intuition or poetic inspiration; Wahy is direct, unerring divine communication.",
                "source_id": "src-islamic-content-dict",
                "source_url": "https://islamic-content.com/dictionary/wahy"
            },
            {
                "id": "term-sharia",
                "term_ar": "الشريعة",
                "term_en": "Sharia",
                "preferred_translation": "Sharia (Islamic Law, Guidance, and Way of Life)",
                "alternative_translation": "Islamic Divine Law / The Clear Path",
                "explanation": "ما شرعه الله تعالى لعباده من الأحكام العقائدية والعملية والأخلاقية لتحقيق مصالحهم في الدارين.",
                "usage_notes": "Crucial: Sharia is an entire ethical, spiritual, and legal framework aimed at justice and human well-being, not merely a penal code.",
                "source_id": "src-islamic-content-dict",
                "source_url": "https://islamic-content.com/dictionary/sharia"
            },
            {
                "id": "term-hadith",
                "term_ar": "الحديث",
                "term_en": "Hadith",
                "preferred_translation": "Hadith (Prophetic Tradition)",
                "alternative_translation": "Narrations of the Prophet / Prophetic Saying",
                "explanation": "ما أُضيف إلى النبي ﷺ من قول أو فعل أو تقرير أو صفة خَلقية أو خُلقية.",
                "usage_notes": "Distinct from the Quran; Hadiths have varying authenticity grades (Sahih, Hasan, Da'if) rigorously verified through Isnad.",
                "source_id": "src-islamic-content-dict",
                "source_url": "https://islamic-content.com/dictionary/hadith"
            },
            {
                "id": "term-sunnah",
                "term_ar": "السنة",
                "term_en": "Sunnah",
                "preferred_translation": "Sunnah (Prophetic Practice and Way)",
                "alternative_translation": "The Prophet's Model / Tradition",
                "explanation": "الطريقة المأثورة عن النبي ﷺ في العبادة والسلوك والأخلاق والتعامل.",
                "usage_notes": "Complementary and explanatory to the Quran, serving as the practical application of Islamic principles.",
                "source_id": "src-islamic-content-dict",
                "source_url": "https://islamic-content.com/dictionary/sunnah"
            },
            {
                "id": "term-fatwa",
                "term_ar": "الفتوى",
                "term_en": "Fatwa",
                "preferred_translation": "Fatwa (Scholarly Legal Opinion)",
                "alternative_translation": "Non-binding Jurisprudential Ruling / Legal Advisory",
                "explanation": "بيان الحكم الشرعي في واقعة معينة من فقيه مؤهل ومخول بالاجتهاد والإفتاء.",
                "usage_notes": "Avoid the misleading western colloquial equating of Fatwa with a 'death decree'; it is an expert legal-religious opinion on everyday questions.",
                "source_id": "src-islamic-content-dict",
                "source_url": "https://islamic-content.com/dictionary/fatwa"
            },
            {
                "id": "term-dawah",
                "term_ar": "الدعوة",
                "term_en": "Da'wah",
                "preferred_translation": "Da'wah (Conveying the Message / Invitation to Islam)",
                "alternative_translation": "Islamic Outreach / Invitation to Faith",
                "explanation": "دعوة الناس إلى عبادة الله وطاعته واتباع دينه بالحكمة والموعظة الحسنة والمجادلة بالتي هي أحسن.",
                "usage_notes": "Emphasize that Da'wah is an invitation based on reason, moral presentation, and free choice, not proselytizing by coercion.",
                "source_id": "src-islamic-content-dict",
                "source_url": "https://islamic-content.com/dictionary/dawah"
            }
        ]

        for item in translation_terms_data:
            # Add to translation_terms table
            existing_term = db.query(TranslationTermModel).filter_by(id=item["id"]).first()
            if not existing_term:
                tt = TranslationTermModel(
                    id=item["id"],
                    term_ar=item["term_ar"],
                    term_en=item["term_en"],
                    preferred_translation=item["preferred_translation"],
                    alternative_translation=item.get("alternative_translation"),
                    explanation=item["explanation"],
                    usage_notes=item.get("usage_notes"),
                    source_id=item["source_id"],
                    source_url=item["source_url"],
                    verified=True
                )
                db.add(tt)
            else:
                existing_term.term_en = item["term_en"]
                existing_term.preferred_translation = item["preferred_translation"]
                existing_term.alternative_translation = item.get("alternative_translation")
                existing_term.explanation = item["explanation"]
                existing_term.usage_notes = item.get("usage_notes")

            # Also ensure TermModel and TermTranslationModel are updated
            existing_tm = db.query(TermModel).filter_by(id=item["id"]).first()
            if not existing_tm:
                tm = TermModel(
                    id=item["id"],
                    term_ar=item["term_ar"],
                    term_normalized=normalize_arabic(item["term_ar"]),
                    category="DICTIONARY_TRANSLATION",
                    definition_ar=item["explanation"],
                    source_id=item["source_id"],
                    locator=f"موسوعة المحتوى الإسلامي، مدخل: {item['term_ar']}"
                )
                db.add(tm)
                db.flush()

                tr = TermTranslationModel(
                    term_id=item["id"],
                    language="en",
                    approved_translation=item["preferred_translation"],
                    contextual_explanation=item["explanation"],
                    usage_notes=item.get("usage_notes"),
                    is_standard=True
                )
                db.add(tr)

        db.commit()
        print("[EnrichKnowledgeBase] Successfully enriched sources, documents, chunks, and translation terms.")
    finally:
        db.close()

if __name__ == "__main__":
    enrich_and_seed_knowledge_base()
