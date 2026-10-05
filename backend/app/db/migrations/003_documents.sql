-- ==============================================================================
-- Bayyinah AI - Supabase Knowledge Base Migration 003: Documents Registry
-- Stores verified documents and books tied to registered sources with strict provenance
-- ==============================================================================

CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE RESTRICT,
    title TEXT NOT NULL,
    author TEXT,
    document_type TEXT,
    category TEXT NOT NULL CHECK (
        category IN (
            'DAWA', 'QURAN', 'TAFSEER', 'HADITH', 'AQEEDAH', 
            'FIQH', 'SEERAH_HISTORY', 'QUESTIONS_DOUBTS', 
            'DICTIONARY_TRANSLATION', 'OTHER'
        )
    ),
    content TEXT,
    reference TEXT,
    url TEXT,
    canonical_url TEXT,
    language TEXT DEFAULT 'ar',
    edition TEXT,
    publication_info TEXT,
    license_status TEXT,
    content_hash TEXT,
    version TEXT,
    indexing_status TEXT DEFAULT 'NOT_INDEXED' CHECK (
        indexing_status IN ('NOT_INDEXED', 'INDEXING', 'INDEXED', 'FAILED', 'RESTRICTED')
    ),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
