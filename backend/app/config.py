import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env from backend directory and root directory
backend_dir = Path(__file__).resolve().parent.parent
root_dir = backend_dir.parent

load_dotenv(backend_dir / ".env")
load_dotenv(root_dir / ".env")

class Settings(BaseSettings):
    PROJECT_NAME: str = "بيّنة AI - Bayyinah AI"
    PROJECT_SLOGAN: str = "تحقّق قبل أن تنشر."
    API_V1_STR: str = "/api"
    
    # Gemini AI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    GEMINI_THINKING_LEVEL: str = os.getenv("GEMINI_THINKING_LEVEL", "high")
    GEMINI_EMBEDDING_MODEL: str = os.getenv("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001")
    GEMINI_TIMEOUT: int = int(os.getenv("GEMINI_TIMEOUT", "30"))
    GEMINI_MAX_RETRIES: int = int(os.getenv("GEMINI_MAX_RETRIES", "2"))
    
    # Database Settings
    DATABASE_MODE: str = os.getenv("DATABASE_MODE", "supabase") # supabase, sqlite, auto
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", os.getenv("SUPABASE_KEY", ""))
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", "768"))
    
    # Storage & Cloudflare R2
    STORAGE_PROVIDER: str = os.getenv("STORAGE_PROVIDER", "LOCAL") # LOCAL, SUPABASE, R2
    R2_ACCOUNT_ID: str = os.getenv("R2_ACCOUNT_ID", "")
    R2_ACCESS_KEY_ID: str = os.getenv("R2_ACCESS_KEY_ID", "")
    R2_SECRET_ACCESS_KEY: str = os.getenv("R2_SECRET_ACCESS_KEY", "")
    R2_BUCKET: str = os.getenv("R2_BUCKET", "")
    R2_ENDPOINT: str = os.getenv("R2_ENDPOINT", "")
    
    # Safety Limits
    MAX_IMAGE_MB: int = int(os.getenv("MAX_IMAGE_MB", "20"))
    MAX_VIDEO_MB: int = int(os.getenv("MAX_VIDEO_MB", "100"))
    MAX_PDF_MB: int = int(os.getenv("MAX_PDF_MB", "50"))
    MAX_URL_RESPONSE_MB: int = int(os.getenv("MAX_URL_RESPONSE_MB", "10"))

    # Search & Discovery (SerpAPI Discovery Layer - Sections 27-31)
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "")
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")

    class Config:
        case_sensitive = True

settings = Settings()
