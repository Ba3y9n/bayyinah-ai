-- ==============================================================================
-- Bayyinah AI - Supabase Knowledge Base Migration 004: Document Chunks
-- Stores retrievable text chunks with SHA-256 integrity hashes and 768-dim embeddings
-- ==============================================================================

CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_text TEXT NOT NULL,
    normalized_text TEXT,
    page_number INTEGER,
    section TEXT,
    paragraph_number INTEGER,
    reference TEXT,
    locator TEXT,
    source_url TEXT,
    canonical_url TEXT,
    content_hash TEXT,
    version TEXT,
    embedding VECTOR(768),
    embedding_model TEXT DEFAULT 'models/text-embedding-004',
    search_vector TSVECTOR,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Trigger to automatically update search_vector for PostgreSQL Full Text Search
CREATE OR REPLACE FUNCTION document_chunks_search_vector_trigger() RETURNS trigger AS $$
BEGIN
    NEW.search_vector := to_tsvector('simple', COALESCE(NEW.normalized_text, '') || ' ' || COALESCE(NEW.chunk_text, '') || ' ' || COALESCE(NEW.reference, ''));
    RETURN NEW;
END
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_document_chunks_search_vector ON document_chunks;
CREATE TRIGGER trg_document_chunks_search_vector
BEFORE INSERT OR UPDATE ON document_chunks
FOR EACH ROW EXECUTE FUNCTION document_chunks_search_vector_trigger();
