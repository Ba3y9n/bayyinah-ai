-- ==============================================================================
-- بيّنة AI | Bayyinah AI
-- Migration 001: Trusted Knowledge Base & Source Registry
-- PostgreSQL + pgvector Schema with Provenance, Hybrid Search, and Governance
-- ==============================================================================

-- 1. Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 2. Enumerated Types
DO $$ BEGIN
    CREATE TYPE source_category_enum AS ENUM (
        'DAWA',
        'QURAN',
        'TAFSEER',
        'HADITH',
        'AQEEDAH',
        'FIQH',
        'SEERAH_HISTORY',
        'QUESTIONS_DOUBTS',
        'DICTIONARY_TRANSLATION',
        'OTHER'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE source_type_enum AS ENUM (
        'OFFICIAL_PLATFORM',
        'DIGITAL_LIBRARY',
        'BOOK',
        'ENCYCLOPEDIA',
        'QURAN_DATABASE',
        'HADITH_DATABASE',
        'DICTIONARY',
        'REFERENCE_WORK',
        'OTHER'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE trust_status_enum AS ENUM (
        'APPROVED',
        'REVIEW_REQUIRED',
        'RESTRICTED',
        'DISABLED'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE license_status_enum AS ENUM (
        'VERIFIED',
        'PENDING_VERIFICATION',
        'RESTRICTED',
        'UNKNOWN',
        'NOT_APPLICABLE'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE ingestion_status_enum AS ENUM (
        'PENDING',
        'PROCESSING',
        'INDEXED',
        'FAILED',
        'DISABLED'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE evidence_type_enum AS ENUM (
        'DIRECT_SUPPORT',
        'PARTIAL_SUPPORT',
        'CONTEXT',
        'CONTRADICTING',
        'RELATED',
        'NO_MATCH'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE claim_type_enum AS ENUM (
        'QURAN_VERSE',
        'HADITH_CLAIM',
        'HADITH_AUTHENTICITY',
        'SCHOLAR_QUOTE',
        'FIQH_CLAIM',
        'AQEEDAH_CLAIM',
        'HISTORICAL_CLAIM',
        'DAWA_CONTENT',
        'TRANSLATION',
        'DEFINITION',
        'GENERAL_INFORMATION',
        'PERSONAL_FATWA',
        'OTHER'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE content_level_enum AS ENUM (
        'LEVEL_A',  -- معلومات أصلية مستقرة
        'LEVEL_B',  -- شرح وتعريف واستدلال
        'LEVEL_C',  -- مسائل خلافية أو عالية الحساسية
        'LEVEL_D'   -- فتوى أو حالة شخصية
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE verification_status_enum AS ENUM (
        'VERIFIED',
        'WEAK',
        'FABRICATED',
        'NOT_ESTABLISHED',
        'INSUFFICIENT',
        'CONFLICT',
        'SPECIALIST'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 3. Table: trusted_sources
CREATE TABLE IF NOT EXISTS trusted_sources (
    id VARCHAR(100) PRIMARY KEY,
    name_ar VARCHAR(255) NOT NULL,
    name_en VARCHAR(255) NOT NULL,
    slug VARCHAR(120) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    official_url TEXT NOT NULL,
    base_domain VARCHAR(255) NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    authority_level VARCHAR(50) DEFAULT 'PRIMARY_CANONICAL',
    trust_status VARCHAR(50) DEFAULT 'REVIEW_REQUIRED',
    usage_status VARCHAR(50) DEFAULT 'METADATA_AND_SNIPPETS',
    license_status VARCHAR(50) DEFAULT 'PENDING_VERIFICATION',
    license_name VARCHAR(255),
    license_url TEXT,
    copyright_holder VARCHAR(255),
    allowed_operations JSONB NOT NULL DEFAULT '{"METADATA_ONLY": true, "SEARCH_SNIPPETS": true, "INDEX_CONTENT": false, "STORE_CONTENT": false, "QUOTE_LIMITED": false, "DISPLAY_EXCERPT": false, "LINK_TO_SOURCE": true, "TRANSLATE": false, "DERIVE_EMBEDDINGS": false}',
    content_scope TEXT,
    language VARCHAR(10) DEFAULT 'ar',
    publisher VARCHAR(255),
    author VARCHAR(255),
    country VARCHAR(100),
    verification_method VARCHAR(100) DEFAULT 'EDITORIAL_REVIEW',
    verification_notes TEXT,
    last_verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    verified_by VARCHAR(150),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_trusted_sources_category ON trusted_sources(category);
CREATE INDEX IF NOT EXISTS idx_trusted_sources_trust_status ON trusted_sources(trust_status);
CREATE INDEX IF NOT EXISTS idx_trusted_sources_license_status ON trusted_sources(license_status);
CREATE INDEX IF NOT EXISTS idx_trusted_sources_is_active ON trusted_sources(is_active);

-- 4. Table: documents
CREATE TABLE IF NOT EXISTS documents (
    id VARCHAR(100) PRIMARY KEY,
    source_id VARCHAR(100) NOT NULL REFERENCES trusted_sources(id) ON DELETE RESTRICT,
    title_ar VARCHAR(500) NOT NULL,
    title_en VARCHAR(500),
    author VARCHAR(255),
    publisher VARCHAR(255),
    document_type VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    official_url TEXT NOT NULL,
    canonical_url TEXT,
    language VARCHAR(10) DEFAULT 'ar',
    publication_date VARCHAR(50),
    edition VARCHAR(100),
    isbn VARCHAR(50),
    description TEXT,
    copyright_holder VARCHAR(255),
    license_status VARCHAR(50) DEFAULT 'PENDING_VERIFICATION',
    license_name VARCHAR(255),
    license_url TEXT,
    ingestion_method VARCHAR(100) DEFAULT 'CURATED_SEED',
    ingestion_status VARCHAR(50) DEFAULT 'INDEXED',
    content_hash VARCHAR(64) NOT NULL,
    version VARCHAR(20) DEFAULT '1.0',
    last_checked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_documents_source_id ON documents(source_id);
CREATE INDEX IF NOT EXISTS idx_documents_category ON documents(category);
CREATE INDEX IF NOT EXISTS idx_documents_content_hash ON documents(content_hash);
CREATE INDEX IF NOT EXISTS idx_documents_ingestion_status ON documents(ingestion_status);

-- 5. Table: document_chunks
CREATE TABLE IF NOT EXISTS document_chunks (
    id VARCHAR(100) PRIMARY KEY,
    document_id VARCHAR(100) NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    content TEXT NOT NULL,
    normalized_content TEXT NOT NULL,
    language VARCHAR(10) DEFAULT 'ar',
    page_number INT,
    section_title VARCHAR(255),
    chapter_title VARCHAR(255),
    paragraph_reference VARCHAR(100),
    verse_reference VARCHAR(100),
    hadith_reference VARCHAR(100),
    book_reference VARCHAR(255),
    volume VARCHAR(50),
    page VARCHAR(50),
    source_locator TEXT NOT NULL,
    canonical_url TEXT NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    embedding vector(768),
    embedding_model VARCHAR(100) DEFAULT 'models/text-embedding-004',
    embedding_version VARCHAR(20) DEFAULT 'v1',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_document_chunks_document_id ON document_chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_document_chunks_content_hash ON document_chunks(content_hash);
CREATE INDEX IF NOT EXISTS idx_document_chunks_hadith_ref ON document_chunks(hadith_reference);
CREATE INDEX IF NOT EXISTS idx_document_chunks_verse_ref ON document_chunks(verse_reference);

-- 6. Table: claims
CREATE TABLE IF NOT EXISTS claims (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    original_input TEXT NOT NULL,
    normalized_claim TEXT NOT NULL,
    claim_type VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    content_level VARCHAR(20) NOT NULL DEFAULT 'LEVEL_A',
    language VARCHAR(10) DEFAULT 'ar',
    entities JSONB DEFAULT '[]',
    keywords JSONB DEFAULT '[]',
    generated_queries JSONB DEFAULT '[]',
    risk_level VARCHAR(20) DEFAULT 'LOW',
    requires_specialist BOOLEAN DEFAULT FALSE,
    requires_conflict_check BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_claims_category ON claims(category);
CREATE INDEX IF NOT EXISTS idx_claims_claim_type ON claims(claim_type);
CREATE INDEX IF NOT EXISTS idx_claims_content_level ON claims(content_level);

-- 7. Table: evidence
CREATE TABLE IF NOT EXISTS evidence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claims(id) ON DELETE CASCADE,
    source_id VARCHAR(100) REFERENCES trusted_sources(id) ON DELETE SET NULL,
    document_id VARCHAR(100) REFERENCES documents(id) ON DELETE SET NULL,
    chunk_id VARCHAR(100) REFERENCES document_chunks(id) ON DELETE SET NULL,
    evidence_type VARCHAR(50) NOT NULL DEFAULT 'DIRECT_SUPPORT',
    matched_text TEXT NOT NULL,
    normalized_text TEXT NOT NULL,
    locator TEXT NOT NULL,
    url TEXT NOT NULL,
    retrieval_method VARCHAR(50) NOT NULL,
    keyword_score FLOAT DEFAULT 0.0,
    semantic_score FLOAT DEFAULT 0.0,
    exact_score FLOAT DEFAULT 0.0,
    metadata_score FLOAT DEFAULT 0.0,
    rrf_score FLOAT DEFAULT 0.0,
    support_level VARCHAR(50) NOT NULL DEFAULT 'DIRECT_SUPPORT',
    attribution_status VARCHAR(50) DEFAULT 'VERIFIED_ATTRIBUTION',
    verification_status VARCHAR(50) NOT NULL DEFAULT 'VERIFIED',
    provenance JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_evidence_claim_id ON evidence(claim_id);
CREATE INDEX IF NOT EXISTS idx_evidence_source_id ON evidence(source_id);
CREATE INDEX IF NOT EXISTS idx_evidence_document_id ON evidence(document_id);

-- 8. Table: Islamic Terminology Dictionary (terms, translations, sources)
CREATE TABLE IF NOT EXISTS terms (
    id VARCHAR(100) PRIMARY KEY,
    term_ar VARCHAR(255) NOT NULL UNIQUE,
    term_normalized VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    definition_ar TEXT NOT NULL,
    source_id VARCHAR(100) REFERENCES trusted_sources(id),
    locator TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS term_translations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    term_id VARCHAR(100) REFERENCES terms(id) ON DELETE CASCADE,
    language VARCHAR(10) NOT NULL,
    approved_translation VARCHAR(255) NOT NULL,
    contextual_explanation TEXT NOT NULL,
    usage_notes TEXT,
    is_standard BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. Table: knowledge_audit_logs (Observability and Transparency)
CREATE TABLE IF NOT EXISTS knowledge_audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    request_id VARCHAR(100) NOT NULL,
    claim_id UUID REFERENCES claims(id) ON DELETE SET NULL,
    query TEXT NOT NULL,
    category_filter VARCHAR(50),
    sources_searched JSONB NOT NULL DEFAULT '[]',
    documents_searched INT DEFAULT 0,
    retrieved_chunks INT DEFAULT 0,
    validation_result VARCHAR(50) NOT NULL,
    final_status VARCHAR(50) NOT NULL,
    model VARCHAR(100) DEFAULT 'gemini-3.8-flash',
    model_version VARCHAR(50) DEFAULT '3.8',
    embedding_model VARCHAR(100) DEFAULT 'models/text-embedding-004',
    embedding_version VARCHAR(20) DEFAULT 'v1',
    latency_breakdown JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_request_id ON knowledge_audit_logs(request_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_final_status ON knowledge_audit_logs(final_status);
