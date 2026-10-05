-- ==============================================================================
-- Bayyinah AI - Supabase Knowledge Base Migration 007: Verification Results
-- Final grounded verification verdict tied to claim and validated evidence
-- ==============================================================================

CREATE TABLE IF NOT EXISTS verification_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id UUID NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
    status TEXT NOT NULL CHECK (
        status IN (
            'VERIFIED', 'WEAK', 'FABRICATED', 'NOT_ESTABLISHED', 
            'INSUFFICIENT', 'CONFLICT', 'SPECIALIST'
        )
    ),
    confidence DOUBLE PRECISION,
    reason TEXT,
    checked_sources_count INTEGER DEFAULT 0,
    evidence_count INTEGER DEFAULT 0,
    conflict_count INTEGER DEFAULT 0,
    primary_source_id UUID REFERENCES sources(id),
    primary_evidence_id UUID REFERENCES evidence(id),
    created_at TIMESTAMPTZ DEFAULT now()
);
