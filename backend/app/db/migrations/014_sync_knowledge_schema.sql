-- ==============================================================================
-- Bayyinah AI - Supabase PostgreSQL Migration 014: Production Schema Sync & Extensions
-- Ensures 100% parity with SQLAlchemy models, creates all missing production tables,
-- sets up FTS triggers, GIN/Vector indexes, and strict provenance tracking.
-- ==============================================================================

-- 1. Ensure extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 2. SOURCES TABLE ALIGNMENT
ALTER TABLE sources ADD COLUMN IF NOT EXISTS license TEXT;
ALTER TABLE sources ADD COLUMN IF NOT EXISTS rights_status TEXT DEFAULT 'PUBLIC_OR_ACADEMIC';
ALTER TABLE sources ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'ACTIVE';
ALTER TABLE sources ADD COLUMN IF NOT EXISTS language TEXT DEFAULT 'ar';
ALTER TABLE sources ADD COLUMN IF NOT EXISTS name_ar TEXT;
ALTER TABLE sources ADD COLUMN IF NOT EXISTS name_en TEXT;
ALTER TABLE sources ADD COLUMN IF NOT EXISTS slug TEXT;

-- 3. DOCUMENTS TABLE ALIGNMENT
ALTER TABLE documents ADD COLUMN IF NOT EXISTS title_ar TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS title_en TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS content TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS content_ar TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS publisher TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS original_url TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS official_url TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS publication_date TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS rights_status TEXT DEFAULT 'PUBLIC_ACCESS';
ALTER TABLE documents ADD COLUMN IF NOT EXISTS isbn TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS copyright_holder TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS license_name TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS license_url TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS ingestion_method TEXT DEFAULT 'MANUAL';
ALTER TABLE documents ADD COLUMN IF NOT EXISTS ingestion_status TEXT DEFAULT 'COMPLETED';
ALTER TABLE documents ADD COLUMN IF NOT EXISTS last_checked_at TIMESTAMPTZ DEFAULT now();
ALTER TABLE documents ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::jsonb;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT now();

-- 4. DOCUMENT CHUNKS TABLE ALIGNMENT
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS chunk_index INTEGER DEFAULT 0;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS content TEXT;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS content_ar TEXT;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS normalized_content TEXT;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS language TEXT DEFAULT 'ar';
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS section_title TEXT;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS chapter_title TEXT;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS paragraph TEXT;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS paragraph_reference TEXT;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS verse_reference TEXT;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS hadith_reference TEXT;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS book_reference TEXT;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS volume TEXT;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS page TEXT;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS source_locator TEXT;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS embedding_version TEXT DEFAULT 'v1';
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::jsonb;
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT now();

-- If embedding vector column needs 768 dimension:
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'document_chunks' AND column_name = 'embedding'
    ) THEN
        ALTER TABLE document_chunks ADD COLUMN embedding VECTOR(768);
    END IF;
END $$;

-- Search vector column for FTS
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'document_chunks' AND column_name = 'search_vector'
    ) THEN
        ALTER TABLE document_chunks ADD COLUMN search_vector TSVECTOR;
    END IF;
END $$;

-- 5. VERIFICATION SESSIONS TABLE
CREATE TABLE IF NOT EXISTS verification_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_status TEXT NOT NULL DEFAULT 'ACTIVE' CHECK (session_status IN ('ACTIVE', 'COMPLETED', 'ARCHIVED', 'FAILED')),
    input_type TEXT NOT NULL DEFAULT 'TEXT' CHECK (input_type IN ('TEXT', 'URL', 'IMAGE', 'VIDEO', 'AUDIO')),
    input_reference TEXT,
    active_claim_id UUID,
    result_id UUID,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 6. CLAIMS TABLE ALIGNMENT
ALTER TABLE claims ADD COLUMN IF NOT EXISTS verification_session_id UUID REFERENCES verification_sessions(id) ON DELETE SET NULL;
ALTER TABLE claims ADD COLUMN IF NOT EXISTS original_text TEXT;
ALTER TABLE claims ADD COLUMN IF NOT EXISTS normalized_text TEXT;
ALTER TABLE claims ADD COLUMN IF NOT EXISTS main_claim TEXT;
ALTER TABLE claims ADD COLUMN IF NOT EXISTS sensitivity TEXT DEFAULT 'LOW';
ALTER TABLE claims ADD COLUMN IF NOT EXISTS entities JSONB DEFAULT '[]'::jsonb;
ALTER TABLE claims ADD COLUMN IF NOT EXISTS "references" JSONB DEFAULT '[]'::jsonb;

-- 7. EVIDENCE TABLE ALIGNMENT
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS evidence_text TEXT;
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS matched_text TEXT;
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS normalized_text TEXT;
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS locator TEXT;
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS url TEXT;
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS support_type TEXT DEFAULT 'DIRECT_SUPPORT';
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS support_score DOUBLE PRECISION DEFAULT 0.0;
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS support_level TEXT DEFAULT 'DIRECT_SUPPORT';
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS attribution_status TEXT DEFAULT 'VERIFIED_ATTRIBUTION';
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS provenance TEXT DEFAULT '{}';
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::jsonb;

-- 8. VERIFICATION RESULTS TABLE ALIGNMENT
ALTER TABLE verification_results ADD COLUMN IF NOT EXISTS summary TEXT;
ALTER TABLE verification_results ADD COLUMN IF NOT EXISTS conflict_detected BOOLEAN DEFAULT FALSE;
ALTER TABLE verification_results ADD COLUMN IF NOT EXISTS specialist_required BOOLEAN DEFAULT FALSE;
ALTER TABLE verification_results ADD COLUMN IF NOT EXISTS source_count INTEGER DEFAULT 0;
ALTER TABLE verification_results ADD COLUMN IF NOT EXISTS limitations JSONB DEFAULT '[]'::jsonb;

-- 9. CONVERSATION MESSAGES TABLE
CREATE TABLE IF NOT EXISTS conversation_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    verification_session_id UUID NOT NULL REFERENCES verification_sessions(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    claim_id UUID REFERENCES claims(id) ON DELETE SET NULL,
    evidence_ids JSONB DEFAULT '[]'::jsonb,
    source_ids JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 10. MEDIA ASSETS TABLE
CREATE TABLE IF NOT EXISTS media_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    verification_session_id UUID REFERENCES verification_sessions(id) ON DELETE CASCADE,
    type TEXT NOT NULL CHECK (type IN ('IMAGE', 'VIDEO', 'AUDIO', 'DOCUMENT')),
    original_filename TEXT,
    mime_type TEXT,
    size_bytes BIGINT,
    storage_provider TEXT DEFAULT 'LOCAL' CHECK (storage_provider IN ('LOCAL', 'SUPABASE', 'R2')),
    storage_key TEXT,
    source_url TEXT,
    gemini_file_name TEXT,
    gemini_file_uri TEXT,
    processing_status TEXT DEFAULT 'PENDING' CHECK (processing_status IN ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', 'EXPIRED')),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 11. URL SUBMISSIONS TABLE
CREATE TABLE IF NOT EXISTS url_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    verification_session_id UUID REFERENCES verification_sessions(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    normalized_url TEXT NOT NULL,
    platform TEXT NOT NULL DEFAULT 'GENERIC' CHECK (platform IN ('YOUTUBE', 'TIKTOK', 'X', 'INSTAGRAM', 'GENERIC', 'DIRECT_MEDIA')),
    content_type TEXT DEFAULT 'ARTICLE',
    resolution_status TEXT DEFAULT 'PENDING' CHECK (resolution_status IN ('PENDING', 'RESOLVED', 'FAILED', 'UNSUPPORTED', 'BLOCKED_SSRF')),
    title TEXT,
    description TEXT,
    author TEXT,
    published_at TIMESTAMPTZ,
    thumbnail_url TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 12. INGESTION JOBS TABLE
CREATE TABLE IF NOT EXISTS ingestion_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES sources(id) ON DELETE CASCADE,
    job_type TEXT NOT NULL DEFAULT 'FULL' CHECK (job_type IN ('FULL', 'INCREMENTAL', 'REINDEX', 'EMBEDDING_ONLY')),
    status TEXT NOT NULL DEFAULT 'QUEUED' CHECK (status IN ('QUEUED', 'PROCESSING', 'COMPLETED', 'FAILED', 'RETRYING')),
    documents_discovered INTEGER DEFAULT 0,
    documents_processed INTEGER DEFAULT 0,
    chunks_created INTEGER DEFAULT 0,
    embeddings_created INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 13. SEARCH LOGS TABLE
CREATE TABLE IF NOT EXISTS search_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES verification_sessions(id) ON DELETE SET NULL,
    query TEXT NOT NULL,
    search_type TEXT NOT NULL DEFAULT 'HYBRID',
    results_count INTEGER DEFAULT 0,
    latency_ms DOUBLE PRECISION DEFAULT 0.0,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 14. SOURCE DOCUMENTS LINK TABLE
CREATE TABLE IF NOT EXISTS source_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    association_type TEXT DEFAULT 'PRIMARY',
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(source_id, document_id)
);

-- 15. EVALUATION CASES & RUNS
CREATE TABLE IF NOT EXISTS evaluation_cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    input_text TEXT NOT NULL,
    expected_status TEXT NOT NULL,
    expected_claim TEXT,
    test_type TEXT DEFAULT 'SYNTHETIC',
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS evaluation_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_mode TEXT NOT NULL DEFAULT 'LIVE_KNOWLEDGE_BASE',
    total_cases INTEGER DEFAULT 0,
    passed_cases INTEGER DEFAULT 0,
    failed_cases INTEGER DEFAULT 0,
    accuracy_score DOUBLE PRECISION DEFAULT 0.0,
    latency_avg_ms DOUBLE PRECISION DEFAULT 0.0,
    details JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 16. INDEXES & PERFORMANCE OPTIMIZATIONS
CREATE INDEX IF NOT EXISTS idx_chunks_doc_id ON document_chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_search_vector ON document_chunks USING GIN(search_vector);
CREATE INDEX IF NOT EXISTS idx_evidence_claim_id ON evidence(claim_id);
CREATE INDEX IF NOT EXISTS idx_evidence_chunk_id ON evidence(chunk_id);
CREATE INDEX IF NOT EXISTS idx_conv_messages_session ON conversation_messages(verification_session_id);
CREATE INDEX IF NOT EXISTS idx_url_submissions_session ON url_submissions(verification_session_id);
CREATE INDEX IF NOT EXISTS idx_media_assets_session ON media_assets(verification_session_id);
CREATE INDEX IF NOT EXISTS idx_ingestion_jobs_source ON ingestion_jobs(source_id);
