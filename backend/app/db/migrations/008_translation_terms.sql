-- ==============================================================================
-- Bayyinah AI - Supabase Knowledge Base Migration 008: Translation Terms
-- Standardized Islamic terminology and approved translations with lexicographical notes
-- ==============================================================================

CREATE TABLE IF NOT EXISTS translation_terms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    term_ar TEXT NOT NULL UNIQUE,
    term_en TEXT,
    preferred_translation TEXT,
    alternative_translation TEXT,
    explanation TEXT,
    usage_notes TEXT,
    source_id UUID REFERENCES sources(id),
    source_url TEXT,
    verified BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now()
);
