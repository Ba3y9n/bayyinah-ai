"""
Bayyinah AI - Supabase & PostgreSQL Engine Interface
Manages live connectivity to Supabase, pgvector similarity search,
PostgreSQL Full-Text Search (FTS), and transactional knowledge base operations.
"""

import os
import json
import hashlib
import time
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from ..config import settings
from ..utils.arabic_normalizer import normalize_arabic

class SupabaseKnowledgeClient:
    """
    Production-grade Supabase & PostgreSQL Knowledge Base Client.
    Handles:
    - Live connectivity testing
    - pgvector Cosine similarity queries (<=> operator, 768-dim)
    - PostgreSQL FTS ranking (ts_rank_cd with 'simple' / Arabic tokens)
    - Complete provenance traceability and content integrity verification
    """

    def __init__(self):
        self.db_url: str = self._resolve_db_url()
        self.engine = None
        self.SessionLocal = None
        self.supabase_client = None
        self._init_connections()

    def _resolve_db_url(self) -> str:
        url = settings.DATABASE_URL
        if url and url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif url and url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return url

    def _init_connections(self):
        if self.db_url:
            try:
                self.engine = create_engine(
                    self.db_url,
                    pool_pre_ping=True,
                    echo=False
                )
                self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            except Exception as e:
                print(f"[SupabaseClient] Database engine initialization warning: {e}")

        # Supabase Python SDK Client
        if settings.SUPABASE_URL and (settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY or settings.SUPABASE_KEY):
            try:
                from supabase import create_client, Client
                key = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY or settings.SUPABASE_KEY
                self.supabase_client: Optional[Client] = create_client(settings.SUPABASE_URL, key)
            except Exception as e:
                print(f"[SupabaseClient] Supabase SDK client initialization warning: {e}")

    def is_connected(self) -> Tuple[bool, str]:
        """
        Executes real 'SELECT 1;' check against PostgreSQL.
        """
        if not self.engine:
            return False, "DATABASE_URL is not configured."
        try:
            with self.engine.connect() as conn:
                res = conn.execute(text("SELECT 1;")).scalar()
                if res == 1:
                    return True, "PostgreSQL connected successfully."
                return False, f"Unexpected ping result: {res}"
        except Exception as e:
            return False, str(e)

    def is_pgvector_available(self) -> Tuple[bool, str]:
        """
        Checks if the pgvector extension is active in PostgreSQL.
        """
        if not self.engine:
            return False, "Database not connected."
        try:
            with self.engine.connect() as conn:
                res = conn.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector';")).scalar()
                if res == "vector":
                    return True, "pgvector extension is active."
                return False, "pgvector extension is not installed in database."
        except Exception as e:
            return False, str(e)

    def is_fts_available(self) -> Tuple[bool, str]:
        """
        Tests PostgreSQL tsvector full text search execution.
        """
        if not self.engine:
            return False, "Database not connected."
        try:
            with self.engine.connect() as conn:
                res = conn.execute(text("SELECT to_tsvector('simple', 'الحمد لله رب العالمين');")).scalar()
                if res:
                    return True, "PostgreSQL FTS is active and functioning."
                return False, "to_tsvector returned empty result."
        except Exception as e:
            return False, str(e)

    def vector_search(self, embedding: List[float], top_k: int = 5, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Executes Cosine similarity search using pgvector (<=> operator).
        Calculates similarity as: 1 - (embedding <=> query_vector).
        """
        if not self.engine or not embedding:
            return []

        vec_str = "[" + ",".join(str(float(x)) for x in embedding) + "]"
        query_sql = """
            SELECT 
                c.id AS chunk_id,
                c.document_id,
                c.chunk_text,
                c.normalized_text,
                c.locator,
                c.reference,
                c.source_url,
                c.canonical_url,
                c.content_hash,
                d.title AS document_title,
                d.category AS document_category,
                s.id AS source_id,
                s.name AS source_name,
                s.category AS source_category,
                s.url AS source_official_url,
                s.scientific_status,
                s.license_status,
                1 - (c.embedding <=> CAST(:vector AS vector)) AS similarity_score
            FROM document_chunks c
            JOIN documents d ON c.document_id = d.id
            JOIN sources s ON d.source_id = s.id
            WHERE c.embedding IS NOT NULL
              AND s.scientific_status = 'APPROVED'
        """
        params: Dict[str, Any] = {"vector": vec_str}

        if category and category.lower() != "all":
            query_sql += " AND (d.category = :cat OR s.category = :cat)"
            params["cat"] = category.upper()

        query_sql += " ORDER BY c.embedding <=> CAST(:vector AS vector) ASC LIMIT :top_k;"
        params["top_k"] = top_k

        try:
            with self.engine.connect() as conn:
                rows = conn.execute(text(query_sql), params).mappings().all()
                results = []
                for r in rows:
                    results.append(dict(r))
                return results
        except Exception as e:
            print(f"[SupabaseClient] Vector search error: {e}")
            return []

    def fts_search(self, query: str, top_k: int = 5, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Executes PostgreSQL Full-Text Search with ts_rank_cd on 'search_vector'.
        """
        if not self.engine or not query.strip():
            return []

        norm_query = normalize_arabic(query)
        # Convert words into tsquery format: word1 | word2 | ...
        words = [w for w in norm_query.split() if len(w) > 1]
        if not words:
            words = [query.strip()]
        tsquery_str = " | ".join(words)

        query_sql = """
            SELECT 
                c.id AS chunk_id,
                c.document_id,
                c.chunk_text,
                c.normalized_text,
                c.locator,
                c.reference,
                c.source_url,
                c.canonical_url,
                c.content_hash,
                d.title AS document_title,
                d.category AS document_category,
                s.id AS source_id,
                s.name AS source_name,
                s.category AS source_category,
                s.url AS source_official_url,
                s.scientific_status,
                s.license_status,
                ts_rank_cd(c.search_vector, to_tsquery('simple', :tsquery)) AS fts_score
            FROM document_chunks c
            JOIN documents d ON c.document_id = d.id
            JOIN sources s ON d.source_id = s.id
            WHERE c.search_vector @@ to_tsquery('simple', :tsquery)
              AND s.scientific_status = 'APPROVED'
        """
        params: Dict[str, Any] = {"tsquery": tsquery_str}

        if category and category.lower() != "all":
            query_sql += " AND (d.category = :cat OR s.category = :cat)"
            params["cat"] = category.upper()

        query_sql += " ORDER BY fts_score DESC LIMIT :top_k;"
        params["top_k"] = top_k

        try:
            with self.engine.connect() as conn:
                rows = conn.execute(text(query_sql), params).mappings().all()
                results = []
                for r in rows:
                    results.append(dict(r))
                return results
        except Exception as e:
            print(f"[SupabaseClient] FTS search error: {e}")
            return []

    def exact_keyword_search(self, query: str, top_k: int = 5, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Executes exact substring and token overlap search using ILIKE and Trigram similarity.
        """
        if not self.engine or not query.strip():
            return []

        norm_query = normalize_arabic(query)
        query_sql = """
            SELECT 
                c.id AS chunk_id,
                c.document_id,
                c.chunk_text,
                c.normalized_text,
                c.locator,
                c.reference,
                c.source_url,
                c.canonical_url,
                c.content_hash,
                d.title AS document_title,
                d.category AS document_category,
                s.id AS source_id,
                s.name AS source_name,
                s.category AS source_category,
                s.url AS source_official_url,
                s.scientific_status,
                s.license_status,
                CASE 
                    WHEN c.normalized_text ILIKE :exact_pattern THEN 1.0
                    WHEN d.title ILIKE :exact_pattern THEN 0.9
                    ELSE similarity(c.normalized_text, :norm_query)
                END AS exact_score
            FROM document_chunks c
            JOIN documents d ON c.document_id = d.id
            JOIN sources s ON d.source_id = s.id
            WHERE (
                c.normalized_text ILIKE :exact_pattern 
                OR d.title ILIKE :exact_pattern 
                OR similarity(c.normalized_text, :norm_query) > 0.15
            )
            AND s.scientific_status = 'APPROVED'
        """
        params: Dict[str, Any] = {
            "exact_pattern": f"%{norm_query}%",
            "norm_query": norm_query
        }

        if category and category.lower() != "all":
            query_sql += " AND (d.category = :cat OR s.category = :cat)"
            params["cat"] = category.upper()

        query_sql += " ORDER BY exact_score DESC LIMIT :top_k;"
        params["top_k"] = top_k

        try:
            with self.engine.connect() as conn:
                rows = conn.execute(text(query_sql), params).mappings().all()
                results = []
                for r in rows:
                    results.append(dict(r))
                return results
        except Exception as e:
            print(f"[SupabaseClient] Exact keyword search error: {e}")
            return []

supabase_client = SupabaseKnowledgeClient()
