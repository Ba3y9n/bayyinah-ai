-- Migration 016: Official Challenge Schema Extensions, Source Registry & Knowledge Base Tables
-- Ensures exact compliance with Challenge Specification Sections 1, 2, 3, 4, 5

-- 1. Create document_sections table if not exists
CREATE TABLE IF NOT EXISTS document_sections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    title TEXT,
    section_order INTEGER DEFAULT 1,
    content TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Create source_versions table if not exists
CREATE TABLE IF NOT EXISTS source_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES sources(id) ON DELETE CASCADE,
    version TEXT NOT NULL DEFAULT '1.0.0',
    content_hash TEXT,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    change_summary TEXT
);

-- 3. Extend sources table with required challenge fields
ALTER TABLE sources ADD COLUMN IF NOT EXISTS approved_by_challenge BOOLEAN DEFAULT TRUE;
ALTER TABLE sources ADD COLUMN IF NOT EXISTS usage_rule TEXT DEFAULT 'الاستدلال المباشر والتوثيق المرجعي المقيد بالنص';
ALTER TABLE sources ADD COLUMN IF NOT EXISTS version TEXT DEFAULT '1.0.0';

-- 4. Extend documents table
ALTER TABLE documents ADD COLUMN IF NOT EXISTS rights_status TEXT DEFAULT 'APPROVED_VERIFIED';
ALTER TABLE documents ADD COLUMN IF NOT EXISTS content_hash TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS version TEXT DEFAULT '1.0.0';
ALTER TABLE documents ADD COLUMN IF NOT EXISTS title_ar TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS title_en TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS reference TEXT;

-- 5. Extend document_chunks table
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS section_id UUID REFERENCES document_sections(id) ON DELETE SET NULL;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS content_hash TEXT;

-- 6. Extend verification_sessions table
ALTER TABLE verification_sessions ADD COLUMN IF NOT EXISTS raw_input TEXT;
ALTER TABLE verification_sessions ADD COLUMN IF NOT EXISTS normalized_input TEXT;
ALTER TABLE verification_sessions ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'COMPLETED';
ALTER TABLE verification_sessions ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- 7. Extend claims table
ALTER TABLE claims ADD COLUMN IF NOT EXISTS normalized_claim TEXT;
ALTER TABLE claims ADD COLUMN IF NOT EXISTS claim_order INTEGER DEFAULT 1;

-- 8. Extend evidence table
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS start_position INTEGER DEFAULT 0;
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS end_position INTEGER DEFAULT 0;
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS timestamp_start TEXT;
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS timestamp_end TEXT;
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS citation_ref TEXT;

-- 9. Extend verification_results table
ALTER TABLE verification_results ADD COLUMN IF NOT EXISTS abstained BOOLEAN DEFAULT FALSE;

-- 10. Extend verification_evidence table
ALTER TABLE verification_evidence ADD COLUMN IF NOT EXISTS rank INTEGER DEFAULT 1;

-- 11. Extend url_submissions table
ALTER TABLE url_submissions ADD COLUMN IF NOT EXISTS domain TEXT;
ALTER TABLE url_submissions ADD COLUMN IF NOT EXISTS canonical_url TEXT;
ALTER TABLE url_submissions ADD COLUMN IF NOT EXISTS platform_id TEXT;
ALTER TABLE url_submissions ADD COLUMN IF NOT EXISTS accessibility_state TEXT DEFAULT 'FULLY_ANALYZABLE';

-- 12. Extend media_assets table
ALTER TABLE media_assets ADD COLUMN IF NOT EXISTS bucket TEXT DEFAULT 'bayyinah-media';
ALTER TABLE media_assets ADD COLUMN IF NOT EXISTS object_key TEXT;
ALTER TABLE media_assets ADD COLUMN IF NOT EXISTS file_size BIGINT DEFAULT 0;
ALTER TABLE media_assets ADD COLUMN IF NOT EXISTS sha256 TEXT;
ALTER TABLE media_assets ADD COLUMN IF NOT EXISTS duration DOUBLE PRECISION DEFAULT 0;
ALTER TABLE media_assets ADD COLUMN IF NOT EXISTS width INTEGER DEFAULT 0;
ALTER TABLE media_assets ADD COLUMN IF NOT EXISTS height INTEGER DEFAULT 0;
ALTER TABLE media_assets ADD COLUMN IF NOT EXISTS expires_at TIMESTAMP WITH TIME ZONE;

-- 13. Extend media_artifacts table
ALTER TABLE media_artifacts ADD COLUMN IF NOT EXISTS object_key TEXT;

-- 14. Extend ingestion_jobs table
ALTER TABLE ingestion_jobs ADD COLUMN IF NOT EXISTS entity_type TEXT DEFAULT 'SOURCE';
ALTER TABLE ingestion_jobs ADD COLUMN IF NOT EXISTS entity_id UUID;
ALTER TABLE ingestion_jobs ADD COLUMN IF NOT EXISTS attempts INTEGER DEFAULT 0;
ALTER TABLE ingestion_jobs ADD COLUMN IF NOT EXISTS error_message TEXT;
ALTER TABLE ingestion_jobs ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- 15. Create indexes if not exists
CREATE INDEX IF NOT EXISTS idx_doc_sections_doc_id ON document_sections(document_id);
CREATE INDEX IF NOT EXISTS idx_source_versions_src ON source_versions(source_id);
CREATE INDEX IF NOT EXISTS idx_doc_chunks_sec ON document_chunks(section_id);
CREATE INDEX IF NOT EXISTS idx_url_sub_canonical ON url_submissions(canonical_url);
CREATE INDEX IF NOT EXISTS idx_docs_hash ON documents(content_hash);
CREATE INDEX IF NOT EXISTS idx_media_sha ON media_assets(sha256);

-- 16. UPSERT the 11 Official Scientific Sources with Full Metadata (Section 2)
INSERT INTO sources (
    id, name, name_ar, name_en, slug, organization, category, source_type, 
    url, official_url, authority_level, approved_by_challenge, usage_rule, 
    license, license_status, language, status, is_active, trust_status, 
    usage_status, verification_method, description, version, last_verified_at
) VALUES 
-- 1. dawa.center
(
    '00000000-0000-0000-0000-000000000001',
    'مركز دعوة (Dawa Center)',
    'مركز دعوة للتعريف بالإسلام',
    'Dawa Center for Islamic Information',
    'dawa-center',
    'مركز دعوة للتعريف بالإسلام',
    'DAWA',
    'PORTAL',
    'https://dawa.center',
    'https://dawa.center',
    'PRIMARY_CANONICAL',
    TRUE,
    'الاستدلال المباشر والتوثيق في التعريف بالإسلام والتواصل الحضاري وشرح المفاهيم',
    'Creative Commons Attribution 4.0 International',
    'VERIFIED',
    'ar',
    'ACTIVE',
    TRUE,
    'APPROVED',
    'ALLOWED',
    'EXPLICIT_CHALLENGE_REGISTRY',
    'بوابة معرفية رائدة متخصصة في التعريف بالإسلام باللغات العالمية والمواد الحوارية والرد العلمي على الشبهات.',
    '1.0.0',
    NOW()
),
-- 2. islamic-content.com
(
    '00000000-0000-0000-0000-000000000002',
    'موسوعة المحتوى الإسلامي',
    'موسوعة المحتوى الإسلامي المترجم',
    'Encyclopedia of Translated Islamic Content',
    'islamic-content',
    'مؤسسة المحتوى الإسلامي',
    'DAWA',
    'PORTAL',
    'https://islamic-content.com',
    'https://islamic-content.com',
    'PRIMARY_CANONICAL',
    TRUE,
    'الاعتماد في المفاهيم الأساسية، التراجم، والمصطلحات المحررة',
    'Creative Commons Attribution 4.0 International',
    'VERIFIED',
    'ar',
    'ACTIVE',
    TRUE,
    'APPROVED',
    'ALLOWED',
    'EXPLICIT_CHALLENGE_REGISTRY',
    'أضخم منصة لنشر المحتوى الإسلامي المعتمد والمترجم بدقة لمختلف لغات العالم.',
    '1.0.0',
    NOW()
),
-- 3. quranpedia.net
(
    '00000000-0000-0000-0000-000000000003',
    'قرآن بيديا (Quranpedia)',
    'موسوعة القرآن الكريم - قرآن بيديا',
    'Quranpedia - Comprehensive Quran Platform',
    'quranpedia',
    'مؤسسة قرآن بيديا',
    'QURAN',
    'ENCYCLOPEDIA',
    'https://quranpedia.net',
    'https://quranpedia.net',
    'PRIMARY_CANONICAL',
    TRUE,
    'النص القرآني الموثق، التفسير الموضوعي، وبيانات الآيات والسور',
    'Public Endowment (Waqf) for Quranic Services',
    'VERIFIED',
    'ar',
    'ACTIVE',
    TRUE,
    'APPROVED',
    'ALLOWED',
    'EXPLICIT_CHALLENGE_REGISTRY',
    'موسوعة قرآنية علمية متكاملة لخدمة النص القرآني، معاني الكلمات، أسباب النزول، والموضوعات.',
    '1.0.0',
    NOW()
),
-- 4. dorar.net/tafseer
(
    '00000000-0000-0000-0000-000000000014',
    'موسوعة التفسير - الدرر السنية',
    'موسوعة التفسير المحرر - الدرر السنية',
    'Dorar Net - Tafseer Encyclopedia',
    'dorar-tafseer',
    'مؤسسة الدرر السنية',
    'TAFSEER',
    'ENCYCLOPEDIA',
    'https://dorar.net/tafseer',
    'https://dorar.net/tafseer',
    'PRIMARY_CANONICAL',
    TRUE,
    'تفسير الآيات، بيان المعاني المعتمدة، وأقوال أئمة السلف المحررة',
    'Educational & Dawa Research License - dorar.net',
    'VERIFIED',
    'ar',
    'ACTIVE',
    TRUE,
    'APPROVED',
    'ALLOWED',
    'EXPLICIT_CHALLENGE_REGISTRY',
    'التفسير المحرر الصادر عن مؤسسة الدرر السنية بإشراف نخبة من المتخصصين في التفسير وعلوم القرآن.',
    '1.0.0',
    NOW()
),
-- 5. dorar.net/hadith
(
    '00000000-0000-0000-0000-000000000004',
    'الموسوعة الحديثية - الدرر السنية',
    'الموسوعة الحديثية - الدرر السنية',
    'Dorar Net - Hadith Encyclopedia',
    'dorar-hadith',
    'مؤسسة الدرر السنية',
    'HADITH',
    'ENCYCLOPEDIA',
    'https://dorar.net/hadith',
    'https://dorar.net/hadith',
    'PRIMARY_CANONICAL',
    TRUE,
    'التحقق من صحة الأحاديث، درجتها، مخرجيها، وأحكام المحدثين المعتبرين',
    'Educational & Dawa Research License - dorar.net',
    'VERIFIED',
    'ar',
    'ACTIVE',
    TRUE,
    'APPROVED',
    'ALLOWED',
    'EXPLICIT_CHALLENGE_REGISTRY',
    'المرجع الرقمي الأول للأحاديث النبوية وأحكام المحدثين المتقدمين والمتأخرين عليها بالسند والمتن.',
    '1.0.0',
    NOW()
),
-- 6. shamela.ws
(
    '00000000-0000-0000-0000-000000000005',
    'المكتبة الشاملة (Shamela)',
    'المكتبة الشاملة الرقمية الوقفية',
    'Al-Maktaba Al-Shamela Digital Library',
    'shamela-ws',
    'المكتبة الشاملة الوقفية',
    'SEERAH_HISTORY',
    'DIGITAL_LIBRARY',
    'https://shamela.ws',
    'https://shamela.ws',
    'PRIMARY_CANONICAL',
    TRUE,
    'الرجوع للمصادر التاريخية الأصلية، دواوين السنة، وكتب التراث الإسلامي',
    'Waqf Public Access for Islamic Heritage',
    'VERIFIED',
    'ar',
    'ACTIVE',
    TRUE,
    'APPROVED',
    'ALLOWED',
    'EXPLICIT_CHALLENGE_REGISTRY',
    'أكبر مكتبة رقمية مفتوحة لكتب التراث الإسلامي والتاريخ والسيرة والتراجم والفقه.',
    '1.0.0',
    NOW()
),
-- 7. dorar.net/aqeeda
(
    '00000000-0000-0000-0000-000000000015',
    'موسوعة العقيدة - الدرر السنية',
    'موسوعة العقيدة والمذاهب والأديان - الدرر السنية',
    'Dorar Net - Aqeeda Encyclopedia',
    'dorar-aqeeda',
    'مؤسسة الدرر السنية',
    'AQEEDAH',
    'ENCYCLOPEDIA',
    'https://dorar.net/aqeeda',
    'https://dorar.net/aqeeda',
    'PRIMARY_CANONICAL',
    TRUE,
    'قضايا أصول الدين، التوحيد، أركان الإيمان، وبيان المسائل العقدية المستقرة',
    'Educational & Dawa Research License - dorar.net',
    'VERIFIED',
    'ar',
    'ACTIVE',
    TRUE,
    'APPROVED',
    'ALLOWED',
    'EXPLICIT_CHALLENGE_REGISTRY',
    'موسوعة عقدية جامعة تعرض عقيدة أهل السنة والجماعة بأسلوب علمي محرر مع الأدلة والرد على المخالفات.',
    '1.0.0',
    NOW()
),
-- 8. dorar.net/feqhia
(
    '00000000-0000-0000-0000-000000000016',
    'الموسوعة الفقهية - الدرر السنية',
    'الموسوعة الفقهية المحررة - الدرر السنية',
    'Dorar Net - Fiqh Encyclopedia',
    'dorar-feqhia',
    'مؤسسة الدرر السنية',
    'FIQH',
    'ENCYCLOPEDIA',
    'https://dorar.net/feqhia',
    'https://dorar.net/feqhia',
    'PRIMARY_CANONICAL',
    TRUE,
    'عرض المسائل الفقهية، بيان أدلة المذاهب الأربعة، والترجيح المنضبط دون إفتاء شخصي',
    'Educational & Dawa Research License - dorar.net',
    'VERIFIED',
    'ar',
    'ACTIVE',
    TRUE,
    'APPROVED',
    'ALLOWED',
    'EXPLICIT_CHALLENGE_REGISTRY',
    'موسوعة فقهية شاملة تحرر مسائل الفقه الإسلامي وأدلتها ومذاهب الأئمة المتبوعين.',
    '1.0.0',
    NOW()
),
-- 9. dorar.net/history
(
    '00000000-0000-0000-0000-000000000017',
    'الموسوعة التاريخية - الدرر السنية',
    'الموسوعة التاريخية وأحداث السيرة - الدرر السنية',
    'Dorar Net - History Encyclopedia',
    'dorar-history',
    'مؤسسة الدرر السنية',
    'SEERAH_HISTORY',
    'ENCYCLOPEDIA',
    'https://dorar.net/history',
    'https://dorar.net/history',
    'PRIMARY_CANONICAL',
    TRUE,
    'تحقيق أحداث السيرة النبوية والتاريخ الإسلامي بالروايات المسندة',
    'Educational & Dawa Research License - dorar.net',
    'VERIFIED',
    'ar',
    'ACTIVE',
    TRUE,
    'APPROVED',
    'ALLOWED',
    'EXPLICIT_CHALLENGE_REGISTRY',
    'توثيق محرر لأحداث التاريخ الإسلامي وسيرة النبي صلى الله عليه وسلم وخلفائه الراشدين.',
    '1.0.0',
    NOW()
),
-- 10. dawa.center/file/7937
(
    '00000000-0000-0000-0000-000000000006',
    'دليل الأسئلة والشبهات (ملف 7937)',
    'دليل الأسئلة والشبهات المعاصرة - مركز دعوة (ملف 7937)',
    'Dawa Center Contemporary Inquiries Guide (File 7937)',
    'dawa-file-7937',
    'مركز دعوة للتعريف بالإسلام',
    'QUESTIONS_DOUBTS',
    'RESEARCH_DOCUMENT',
    'https://dawa.center/file/7937',
    'https://dawa.center/file/7937',
    'PRIMARY_CANONICAL',
    TRUE,
    'الإجابة الاستدلالية عن الشبهات الفكرية والأسئلة العامة مع حفظ المرجع',
    'Dawa Center Official Document Authorization',
    'VERIFIED',
    'ar',
    'ACTIVE',
    TRUE,
    'APPROVED',
    'ALLOWED',
    'EXPLICIT_CHALLENGE_REGISTRY',
    'وثيقة علمية متخصصة ومحكمة تعالج الشبهات والأسئلة الشائعة حول الإسلام بالأدلة العقلية والنقلية.',
    '1.0.0',
    NOW()
),
-- 11. islamic-content.com/dictionary
(
    '00000000-0000-0000-0000-000000000007',
    'قاموس المصطلحات الإسلامية المترجمة',
    'قاموس المصطلحات الإسلامية المترجمة - المحتوى الإسلامي',
    'Islamic Content Dictionary of Islamic Terminology',
    'islamic-content-dict',
    'موسوعة المحتوى الإسلامي',
    'DICTIONARY_TRANSLATION',
    'DICTIONARY',
    'https://islamic-content.com/dictionary',
    'https://islamic-content.com/dictionary',
    'PRIMARY_CANONICAL',
    TRUE,
    'ضبط معاني المصطلحات الشرعية ومنع الترجمة الحرفية المخلة',
    'Open Access Terminology Database',
    'VERIFIED',
    'ar',
    'ACTIVE',
    TRUE,
    'APPROVED',
    'ALLOWED',
    'EXPLICIT_CHALLENGE_REGISTRY',
    'قاموس مرجعي معتمد لترجمة وتعريف المصطلحات الشرعية والعقدية والفقهية بدقة علمية رصينة.',
    '1.0.0',
    NOW()
)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    name_ar = EXCLUDED.name_ar,
    name_en = EXCLUDED.name_en,
    slug = EXCLUDED.slug,
    organization = EXCLUDED.organization,
    category = EXCLUDED.category,
    source_type = EXCLUDED.source_type,
    url = EXCLUDED.url,
    official_url = EXCLUDED.official_url,
    authority_level = EXCLUDED.authority_level,
    approved_by_challenge = EXCLUDED.approved_by_challenge,
    usage_rule = EXCLUDED.usage_rule,
    license = EXCLUDED.license,
    license_status = EXCLUDED.license_status,
    language = EXCLUDED.language,
    status = EXCLUDED.status,
    is_active = EXCLUDED.is_active,
    trust_status = EXCLUDED.trust_status,
    usage_status = EXCLUDED.usage_status,
    verification_method = EXCLUDED.verification_method,
    description = EXCLUDED.description,
    version = EXCLUDED.version,
    last_verified_at = EXCLUDED.last_verified_at,
    updated_at = NOW();
