-- Migration 017: Autonomous Knowledge Acquisition Engine & Versioning Schema
-- Enforces: Incremental Crawling, Document Versioning, Human Review Queue, and Dead Letter Queue

-- 1. Document Versions Table
CREATE TABLE IF NOT EXISTS document_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    version TEXT NOT NULL DEFAULT '1.0',
    content_hash TEXT,
    normalized_hash TEXT,
    title TEXT,
    content TEXT,
    reference TEXT,
    diff_summary TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_doc_versions_doc_id ON document_versions(document_id);
CREATE INDEX IF NOT EXISTS idx_doc_versions_hash ON document_versions(content_hash);

-- 2. Human Review Queue Table
CREATE TABLE IF NOT EXISTS knowledge_review_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES sources(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    item_type TEXT NOT NULL, -- PARSING_FAILURE, SOURCE_CONFLICT, LOW_QUALITY_EVIDENCE, CHANGED_DOCUMENT, INACCESSIBLE_SOURCE, SUSPICIOUS_EXTRACTION, DEAD_LETTER
    severity TEXT DEFAULT 'MEDIUM', -- LOW, MEDIUM, HIGH, CRITICAL
    status TEXT DEFAULT 'PENDING', -- PENDING, APPROVED, REJECTED, RESOLVED
    reason TEXT NOT NULL,
    url TEXT,
    details JSONB DEFAULT '{}'::jsonb,
    resolution_notes TEXT,
    resolved_by TEXT,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_review_items_status ON knowledge_review_items(status);
CREATE INDEX IF NOT EXISTS idx_review_items_type ON knowledge_review_items(item_type);

-- 3. Extend documents for incremental crawling
ALTER TABLE documents ADD COLUMN IF NOT EXISTS normalized_hash TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS last_seen_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE documents ADD COLUMN IF NOT EXISTS last_changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE documents ADD COLUMN IF NOT EXISTS etag TEXT;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS last_modified TEXT;

-- 4. Extend ingestion_jobs for robust retry and DLQ
ALTER TABLE ingestion_jobs ADD COLUMN IF NOT EXISTS retry_count INTEGER DEFAULT 0;
ALTER TABLE ingestion_jobs ADD COLUMN IF NOT EXISTS max_retries INTEGER DEFAULT 3;
ALTER TABLE ingestion_jobs ADD COLUMN IF NOT EXISTS is_dead_letter BOOLEAN DEFAULT FALSE;
ALTER TABLE ingestion_jobs ADD COLUMN IF NOT EXISTS dead_letter_reason TEXT;
