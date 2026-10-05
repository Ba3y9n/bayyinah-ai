-- ==============================================================================
-- Bayyinah AI - Supabase Knowledge Base Migration 010: Source Health Checks
-- Tracks live reachability, latency, and integrity of registered Islamic source domains
-- ==============================================================================

CREATE TABLE IF NOT EXISTS source_health_checks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    url TEXT,
    http_status INTEGER,
    reachable BOOLEAN,
    response_time_ms DOUBLE PRECISION,
    checked_at TIMESTAMPTZ DEFAULT now(),
    error_message TEXT
);
