-- ==============================================================================
-- Bayyinah AI - Supabase Knowledge Base Migration 012: Row Level Security (RLS)
-- Protects knowledge integrity: Public read via verified backend; mutations restricted
-- ==============================================================================

-- Enable RLS on all knowledge base tables
ALTER TABLE sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE claims ENABLE ROW LEVEL SECURITY;
ALTER TABLE evidence ENABLE ROW LEVEL SECURITY;
ALTER TABLE verification_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE translation_terms ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE source_health_checks ENABLE ROW LEVEL SECURITY;

-- 1. Public / Anon Read Policy on Sources & Reference Material
CREATE POLICY "Public Read Sources" ON sources FOR SELECT USING (true);
CREATE POLICY "Public Read Documents" ON documents FOR SELECT USING (true);
CREATE POLICY "Public Read Document Chunks" ON document_chunks FOR SELECT USING (true);
CREATE POLICY "Public Read Translation Terms" ON translation_terms FOR SELECT USING (true);
CREATE POLICY "Public Read Source Health" ON source_health_checks FOR SELECT USING (true);

-- 2. Verification Results & Evidence Read
CREATE POLICY "Public Read Claims" ON claims FOR SELECT USING (true);
CREATE POLICY "Public Read Evidence" ON evidence FOR SELECT USING (true);
CREATE POLICY "Public Read Verification Results" ON verification_results FOR SELECT USING (true);
CREATE POLICY "Public Read Audit Logs" ON knowledge_audit_logs FOR SELECT USING (true);

-- 3. Service Role Write Policies (Backend Service Key Only)
CREATE POLICY "Service Role All Sources" ON sources FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role All Documents" ON documents FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role All Chunks" ON document_chunks FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role All Claims" ON claims FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role All Evidence" ON evidence FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role All Verifications" ON verification_results FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role All Terms" ON translation_terms FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role All Audit Logs" ON knowledge_audit_logs FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role All Health Checks" ON source_health_checks FOR ALL TO service_role USING (true) WITH CHECK (true);
