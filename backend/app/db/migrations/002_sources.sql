-- ==============================================================================
-- Bayyinah AI - Supabase Knowledge Base Migration 002: Trusted Sources Table
-- Stores authoritative Islamic references with explicit scientific and licensing governance
-- ==============================================================================

CREATE TABLE IF NOT EXISTS sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    organization TEXT,
    author TEXT,
    category TEXT NOT NULL CHECK (
        category IN (
            'DAWA', 'QURAN', 'TAFSEER', 'HADITH', 'AQEEDAH', 
            'FIQH', 'SEERAH_HISTORY', 'QUESTIONS_DOUBTS', 
            'DICTIONARY_TRANSLATION', 'OTHER'
        )
    ),
    description TEXT,
    url TEXT NOT NULL,
    specific_url TEXT,
    source_type TEXT,
    scientific_status TEXT NOT NULL DEFAULT 'REVIEW_REQUIRED' CHECK (
        scientific_status IN ('APPROVED', 'REVIEW_REQUIRED', 'RESTRICTED', 'DISABLED')
    ),
    license_status TEXT NOT NULL DEFAULT 'UNKNOWN' CHECK (
        license_status IN ('VERIFIED', 'PENDING', 'RESTRICTED', 'UNKNOWN', 'NOT_APPLICABLE')
    ),
    license_reference TEXT,
    allowed_operations JSONB DEFAULT '{}'::jsonb,
    indexing_allowed BOOLEAN DEFAULT false,
    storage_allowed BOOLEAN DEFAULT false,
    excerpt_allowed BOOLEAN DEFAULT false,
    link_allowed BOOLEAN DEFAULT true,
    translation_allowed BOOLEAN DEFAULT false,
    embedding_allowed BOOLEAN DEFAULT false,
    verification_notes TEXT,
    last_verified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
