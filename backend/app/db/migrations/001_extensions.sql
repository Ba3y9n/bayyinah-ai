-- ==============================================================================
-- Bayyinah AI - Supabase Knowledge Base Migration 001: Extensions
-- Enables essential PostgreSQL extensions: uuid-ossp, pgvector, pg_trgm, btree_gin
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";
