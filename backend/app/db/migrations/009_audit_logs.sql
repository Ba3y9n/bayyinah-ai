-- ==============================================================================
-- Bayyinah AI - Supabase Knowledge Base Migration 009: Knowledge Audit Logs
-- Complete auditable journey: queries, checked sources, latency, and reasoning
-- ==============================================================================

CREATE TABLE IF NOT EXISTS knowledge_audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id UUID REFERENCES claims(id) ON DELETE SET NULL,
    search_query TEXT,
    search_type TEXT,
    sources_checked JSONB DEFAULT '[]'::jsonb,
    documents_checked JSONB DEFAULT '[]'::jsonb,
    chunks_checked JSONB DEFAULT '[]'::jsonb,
    evidence_found INTEGER DEFAULT 0,
    validation_result JSONB DEFAULT '{}'::jsonb,
    conflicts_found JSONB DEFAULT '[]'::jsonb,
    final_status TEXT,
    model TEXT,
    latency_ms DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT now()
);
