-- ==============================================================================
-- Bayyinah AI - Supabase Knowledge Base Migration 006: Evidence Table
-- The core evidence nexus linking Claims -> Sources -> Documents -> Chunks
-- ==============================================================================

CREATE TABLE IF NOT EXISTS evidence (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id UUID NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE RESTRICT,
    document_id UUID REFERENCES documents(id) ON DELETE RESTRICT,
    chunk_id UUID REFERENCES document_chunks(id) ON DELETE RESTRICT,
    excerpt TEXT NOT NULL,
    reference TEXT,
    source_url TEXT,
    relevance_score DOUBLE PRECISION,
    exact_score DOUBLE PRECISION,
    keyword_score DOUBLE PRECISION,
    semantic_score DOUBLE PRECISION,
    evidence_type TEXT CHECK (
        evidence_type IN (
            'DIRECT_SUPPORT', 'PARTIAL_SUPPORT', 'CONTEXT_SUPPORT', 
            'CONTRADICTING', 'NOT_RELEVANT', 'INSUFFICIENT'
        )
    ),
    validation_status TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
