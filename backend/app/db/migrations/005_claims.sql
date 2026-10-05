-- ==============================================================================
-- Bayyinah AI - Supabase Knowledge Base Migration 005: Claims Table
-- Stores user claims extracted by AI for verifiable Islamic content auditing
-- ==============================================================================

CREATE TABLE IF NOT EXISTS claims (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_input TEXT NOT NULL,
    claim_text TEXT NOT NULL,
    claim_type TEXT NOT NULL CHECK (
        claim_type IN (
            'QURAN_VERSE', 'HADITH', 'HADITH_ATTRIBUTION', 'TAFSEER', 
            'AQEEDAH', 'FIQH', 'SEERAH', 'HISTORY', 'DAWAH', 
            'DOUBT', 'QUESTION', 'TRANSLATION', 'TERM', 'QUOTE', 
            'RULING', 'GENERAL_INFORMATION', 'PERSONAL_CASE', 'UNKNOWN'
        )
    ),
    category TEXT,
    language TEXT DEFAULT 'ar',
    sensitivity_level TEXT DEFAULT 'low' CHECK (
        sensitivity_level IN ('low', 'medium', 'high', 'critical')
    ),
    content_level TEXT DEFAULT 'LEVEL_A' CHECK (
        content_level IN ('LEVEL_A', 'LEVEL_B', 'LEVEL_C', 'LEVEL_D')
    ),
    requires_specialist BOOLEAN DEFAULT false,
    requires_source_verification BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now()
);
