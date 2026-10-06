import os
import logging
from typing import Generator, Dict, Any, Tuple, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from ..config import settings
from ..models.knowledge_models import Base

logger = logging.getLogger("bayyinah.database")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)
SQLITE_DB_PATH = os.path.join(DATA_DIR, "bayyinah_knowledge.db")

active_db_type = "UNKNOWN"
db_status_message = "INITIALIZING"
engine = None
SessionLocal = None

def _resolve_postgres_url(raw_url: str) -> str:
    if not raw_url:
        return ""
    url = raw_url
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif url.startswith("postgresql://") and not url.startswith("postgresql+psycopg2://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url

def init_engine():
    global active_db_type, db_status_message, engine, SessionLocal
    mode = (settings.DATABASE_MODE or "supabase").lower().strip()
    
    if mode == "supabase":
        raw_url = settings.DATABASE_URL
        if not raw_url:
            active_db_type = "NONE"
            db_status_message = "DATABASE_UNAVAILABLE: DATABASE_URL is not configured for supabase mode."
            logger.error(db_status_message)
            raise RuntimeError(db_status_message)
        
        pg_url = _resolve_postgres_url(raw_url)
        try:
            engine = create_engine(
                pg_url, 
                echo=False, 
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20,
                connect_args={"connect_timeout": 3}
            )
            # Lazy connection: Do not connect on boot to prevent Vercel timeouts!
            active_db_type = "SUPABASE_POSTGRESQL"
            db_status_message = "CONFIGURED (Lazy Connect)"
            logger.info("Supabase PostgreSQL configured.")
        except Exception as e:
            active_db_type = "ERROR"
            db_status_message = f"DATABASE_UNAVAILABLE: Failed to configure Supabase: {e}"
            logger.error(db_status_message)
            raise RuntimeError(db_status_message)

    elif mode == "sqlite":
        sqlite_url = f"sqlite:///{SQLITE_DB_PATH}"
        engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, echo=False)
        active_db_type = "LOCAL_SQLITE"
        db_status_message = "CONNECTED_DEV_FALLBACK"
        logger.warning("Running in local SQLite mode (Development only).")

    elif mode == "auto":
        raw_url = settings.DATABASE_URL
        if raw_url:
            try:
                pg_url = _resolve_postgres_url(raw_url)
                engine = create_engine(pg_url, echo=False, pool_pre_ping=True, connect_args={"connect_timeout": 3})
                active_db_type = "SUPABASE_POSTGRESQL"
                db_status_message = "CONFIGURED (Lazy Connect)"
            except Exception as e:
                logger.warning(f"Auto-mode: Supabase connection failed ({e}). Falling back to SQLite.")
        
        if not engine or active_db_type != "SUPABASE_POSTGRESQL":
            sqlite_url = f"sqlite:///{SQLITE_DB_PATH}"
            engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, echo=False)
            active_db_type = "LOCAL_SQLITE"
            db_status_message = "CONNECTED_FALLBACK"

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize on module load
try:
    init_engine()
except Exception as exc:
    logger.warning(f"Database initial setup notice: {exc}")

def init_db():
    """Initializes schema if needed."""
    if engine and active_db_type == "LOCAL_SQLITE":
        Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for database session."""
    if not SessionLocal:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="DATABASE_UNAVAILABLE: تعذر الاتصال بقاعدة البيانات.")
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            try:
                db.close()
            except Exception:
                pass

def get_db_info() -> Dict[str, Any]:
    """Returns database type and operational state."""
    return {
        "active_database": active_db_type,
        "status": db_status_message,
        "mode": settings.DATABASE_MODE,
        "is_production_ready": active_db_type == "SUPABASE_POSTGRESQL"
    }
