-- ==============================================================================
-- 015_canonical_enterprise_schema.sql
-- Bayyinah AI: Canonical Enterprise Schema Alignment with UUID Types
-- ==============================================================================

-- 1. Media Artifacts (OCR slices, audio transcripts, video frame extractions)
CREATE TABLE IF NOT EXISTS media_artifacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    media_asset_id UUID REFERENCES media_assets(id) ON DELETE CASCADE,
    artifact_type VARCHAR(50) NOT NULL, -- TRANSCRIPT, OCR_TEXT, FRAME, THUMBNAIL, AUDIO_CHUNK
    file_path TEXT,
    public_url TEXT,
    artifact_hash VARCHAR(64),
    timestamp_start VARCHAR(20),
    timestamp_end VARCHAR(20),
    extracted_text TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_media_artifacts_asset ON media_artifacts(media_asset_id);
CREATE INDEX IF NOT EXISTS idx_media_artifacts_type ON media_artifacts(artifact_type);

-- 2. Chat Sessions (Evidence-Bound Conversation Sessions)
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    verification_session_id UUID REFERENCES verification_sessions(id) ON DELETE SET NULL,
    active_claim_id UUID REFERENCES claims(id) ON DELETE SET NULL,
    session_title VARCHAR(255),
    state VARCHAR(50) DEFAULT 'ACTIVE',
    model VARCHAR(50) DEFAULT 'gemini-3.8-flash',
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chat_sessions_verification ON chat_sessions(verification_session_id);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_claim ON chat_sessions(active_claim_id);

-- 3. Chat Messages (Grounded Messages with Intent & Verification State)
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- user, assistant, system
    content TEXT NOT NULL,
    intent VARCHAR(50) DEFAULT 'FOLLOWUP_ON_CURRENT_EVIDENCE', -- NEW_VERIFICATION, FOLLOWUP_ON_CURRENT_EVIDENCE, GENERAL_EXPLANATION, PERSONAL_CASE, OFF_TOPIC
    grounding_status VARCHAR(50) DEFAULT 'GROUNDED', -- GROUNDED, ABSTAINED, REJECTED, SPECIALIST_REFERRAL
    abstention_reason TEXT,
    citations JSONB DEFAULT '[]'::jsonb,
    suggested_followups JSONB DEFAULT '[]'::jsonb,
    avatar_state VARCHAR(30) DEFAULT 'idle',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chat_messages_session ON chat_messages(chat_session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_role ON chat_messages(role);
CREATE INDEX IF NOT EXISTS idx_chat_messages_intent ON chat_messages(intent);

-- 4. Chat Evidence Bindings (Strict Server-Side Link between Message & Grounding Evidence)
CREATE TABLE IF NOT EXISTS chat_evidence_bindings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_message_id UUID REFERENCES chat_messages(id) ON DELETE CASCADE,
    evidence_id UUID REFERENCES evidence(id) ON DELETE CASCADE,
    chunk_id UUID REFERENCES document_chunks(id) ON DELETE SET NULL,
    source_name VARCHAR(255),
    reference TEXT,
    relevance_score FLOAT DEFAULT 1.0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chat_evidence_msg ON chat_evidence_bindings(chat_message_id);
CREATE INDEX IF NOT EXISTS idx_chat_evidence_ev ON chat_evidence_bindings(evidence_id);

-- 5. Verification Evidence Mapping (Many-to-Many Linking Results to Evidence)
CREATE TABLE IF NOT EXISTS verification_evidence (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    verification_result_id UUID REFERENCES verification_results(id) ON DELETE CASCADE,
    evidence_id UUID REFERENCES evidence(id) ON DELETE CASCADE,
    relevance_score FLOAT DEFAULT 1.0,
    support_level VARCHAR(50) DEFAULT 'DIRECT_SUPPORT',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_verif_ev_result ON verification_evidence(verification_result_id);
CREATE INDEX IF NOT EXISTS idx_verif_ev_evidence ON verification_evidence(evidence_id);

-- 6. Canonical audit_logs View (Alias for knowledge_audit_logs)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_views WHERE viewname = 'audit_logs') AND 
       NOT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'audit_logs') THEN
        CREATE VIEW audit_logs AS SELECT * FROM knowledge_audit_logs;
    END IF;
END $$;

-- 7. Security: Row Level Security (RLS) enforcement on Knowledge Base
ALTER TABLE sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;

-- Allow public read access to verified knowledge base
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Public read sources' AND tablename = 'sources') THEN
        CREATE POLICY "Public read sources" ON sources FOR SELECT USING (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Public read documents' AND tablename = 'documents') THEN
        CREATE POLICY "Public read documents" ON documents FOR SELECT USING (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Public read chunks' AND tablename = 'document_chunks') THEN
        CREATE POLICY "Public read chunks" ON document_chunks FOR SELECT USING (true);
    END IF;
END $$;
