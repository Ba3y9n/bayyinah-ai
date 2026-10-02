-- ==============================================================================
-- بيّنة AI - Supabase PostgreSQL & pgvector Schema
-- Bayyinah AI - Section 26 Schema Definition
-- ==============================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Drop existing tables in reverse dependency order
DROP TABLE IF EXISTS search_logs CASCADE;
DROP TABLE IF EXISTS verification_results CASCADE;
DROP TABLE IF EXISTS evidence CASCADE;
DROP TABLE IF EXISTS claims CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS sources CASCADE;

-- 1. sources table
CREATE TABLE sources (
    id TEXT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    organization VARCHAR(255),
    category VARCHAR(100) NOT NULL, -- Quran, Hadith, Tafsir, Fiqh, Aqeedah, Seerah, Fatwa, General
    url TEXT NOT NULL,
    license VARCHAR(255) NOT NULL,
    source_type VARCHAR(100) NOT NULL, -- primary_text, encyclopedia, verified_fatwa_center, academic_corpus
    status VARCHAR(50) DEFAULT 'active', -- active, under_review, deprecated
    last_verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. documents table (Full Text Search Vector + pgvector Embeddings)
CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    source_id TEXT REFERENCES sources(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    reference VARCHAR(500) NOT NULL,
    category VARCHAR(100) NOT NULL,
    url TEXT NOT NULL,
    embedding vector(768), -- Gemini text-embedding-004 vector
    search_vector tsvector GENERATED ALWAYS AS (to_tsvector('arabic', coalesce(title, '') || ' ' || coalesce(content, '') || ' ' || coalesce(reference, ''))) STORED,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Performance & Hybrid Search Indexes
CREATE INDEX idx_documents_source_id ON documents(source_id);
CREATE INDEX idx_documents_category ON documents(category);
CREATE INDEX idx_documents_search_vector ON documents USING GIN(search_vector);
CREATE INDEX idx_documents_title_trgm ON documents USING GIN(title gin_trgm_ops);
CREATE INDEX idx_documents_content_trgm ON documents USING GIN(content gin_trgm_ops);
CREATE INDEX idx_documents_embedding_hnsw ON documents USING hnsw (embedding vector_cosine_ops);

-- 3. claims table
CREATE TABLE claims (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_input TEXT NOT NULL,
    normalized_claim TEXT NOT NULL,
    claim_type VARCHAR(100) NOT NULL, -- Quran, Hadith, Dua, Fiqh, Aqeedah, Seerah, History, ScholarQuote, IslamicDefinition, Translation, GeneralReligiousClaim, PersonalCase, Unknown
    sensitivity VARCHAR(50) DEFAULT 'low', -- low, medium, high
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. evidence table
CREATE TABLE evidence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claims(id) ON DELETE CASCADE,
    document_id TEXT REFERENCES documents(id) ON DELETE SET NULL,
    excerpt TEXT NOT NULL,
    relevance_score FLOAT NOT NULL DEFAULT 0.0,
    evidence_type VARCHAR(100) NOT NULL, -- EXACT, KEYWORD, SEMANTIC, HYBRID, CONFLICT
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_evidence_claim_id ON evidence(claim_id);

-- 5. verification_results table
CREATE TABLE verification_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claims(id) ON DELETE CASCADE,
    status VARCHAR(100) NOT NULL, -- VERIFIED, WEAK, FABRICATED, NOT_ESTABLISHED, INSUFFICIENT, CONFLICT, SPECIALIST
    reason TEXT NOT NULL,
    checked_sources_count INT DEFAULT 0,
    evidence_count INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_verification_results_claim_id ON verification_results(claim_id);

-- 6. search_logs table (Anonymized & strictly for observability)
CREATE TABLE search_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claims(id) ON DELETE SET NULL,
    query TEXT NOT NULL,
    search_type VARCHAR(50) NOT NULL, -- exact, keyword, semantic, hybrid
    result_count INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
