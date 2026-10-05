-- ==============================================================================
-- Bayyinah AI - Supabase Knowledge Base Migration 011: Indexes
-- Performance indexes: B-tree, GIN FTS, Trigram, and pgvector HNSW
-- ==============================================================================

-- Sources indexes
CREATE INDEX IF NOT EXISTS idx_sources_category ON sources(category);
CREATE INDEX IF NOT EXISTS idx_sources_scientific_status ON sources(scientific_status);
CREATE INDEX IF NOT EXISTS idx_sources_license_status ON sources(license_status);

-- Documents indexes
CREATE INDEX IF NOT EXISTS idx_documents_source_id ON documents(source_id);
CREATE INDEX IF NOT EXISTS idx_documents_category ON documents(category);
CREATE INDEX IF NOT EXISTS idx_documents_indexing_status ON documents(indexing_status);
CREATE INDEX IF NOT EXISTS idx_documents_content_hash ON documents(content_hash);

-- Document chunks indexes
CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON document_chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_content_hash ON document_chunks(content_hash);

-- PostgreSQL Full Text Search GIN index
CREATE INDEX IF NOT EXISTS idx_chunks_search_vector_gin ON document_chunks USING gin(search_vector);

-- Trigram text search index for Arabic sub-phrase matching
CREATE INDEX IF NOT EXISTS idx_chunks_normalized_trgm ON document_chunks USING gin(normalized_text gin_trgm_ops);

-- pgvector HNSW vector similarity search index (Cosine Distance)
CREATE INDEX IF NOT EXISTS idx_chunks_embedding_hnsw ON document_chunks USING hnsw (embedding vector_cosine_ops);

-- Claims indexes
CREATE INDEX IF NOT EXISTS idx_claims_claim_type ON claims(claim_type);
CREATE INDEX IF NOT EXISTS idx_claims_category ON claims(category);
CREATE INDEX IF NOT EXISTS idx_claims_created_at ON claims(created_at);

-- Evidence indexes
CREATE INDEX IF NOT EXISTS idx_evidence_claim_id ON evidence(claim_id);
CREATE INDEX IF NOT EXISTS idx_evidence_source_id ON evidence(source_id);
CREATE INDEX IF NOT EXISTS idx_evidence_document_id ON evidence(document_id);
CREATE INDEX IF NOT EXISTS idx_evidence_chunk_id ON evidence(chunk_id);

-- Verification results indexes
CREATE INDEX IF NOT EXISTS idx_verifications_claim_id ON verification_results(claim_id);
CREATE INDEX IF NOT EXISTS idx_verifications_status ON verification_results(status);

-- Knowledge audit logs indexes
CREATE INDEX IF NOT EXISTS idx_audit_claim_id ON knowledge_audit_logs(claim_id);
CREATE INDEX IF NOT EXISTS idx_audit_created_at ON knowledge_audit_logs(created_at);

-- Translation terms indexes
CREATE INDEX IF NOT EXISTS idx_trans_terms_ar ON translation_terms(term_ar);
CREATE INDEX IF NOT EXISTS idx_trans_terms_en ON translation_terms(term_en);
