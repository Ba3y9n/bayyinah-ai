"""
Bayyinah AI - Media Storage Abstraction Service
Supports LocalStorageProvider, SupabaseStorageProvider, and Cloudflare R2StorageProvider.
Ensures zero large media files stored inside PostgreSQL.
"""

import os
import uuid
import shutil
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..config import settings
import logging

logger = logging.getLogger("bayyinah.services.storage")

class StorageProvider(ABC):
    @abstractmethod
    def save_file(self, file_bytes: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def save_file_stream(self, file_obj: Any, filename: str, mime_type: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_file_url(self, storage_key: str) -> str:
        pass

class LocalStorageProvider(StorageProvider):
    """
    Local file storage provider for development and testing.
    """
    def __init__(self, upload_dir: Optional[str] = None):
        self.upload_dir = upload_dir or os.path.join(os.path.dirname(__file__), "..", "data", "uploads")
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_file(self, file_bytes: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        ext = os.path.splitext(filename)[1]
        storage_key = f"{uuid.uuid4().hex}{ext}"
        target_path = os.path.join(self.upload_dir, storage_key)

        with open(target_path, "wb") as f:
            f.write(file_bytes)

        return {
            "storage_provider": "LOCAL",
            "storage_key": storage_key,
            "file_path": target_path,
            "url": f"/api/media/files/{storage_key}",
            "size_bytes": len(file_bytes)
        }

    def save_file_stream(self, file_obj: Any, filename: str, mime_type: str) -> Dict[str, Any]:
        ext = os.path.splitext(filename)[1]
        storage_key = f"{uuid.uuid4().hex}{ext}"
        target_path = os.path.join(self.upload_dir, storage_key)

        total_size = 0
        with open(target_path, "wb") as f:
            while True:
                chunk = file_obj.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                total_size += len(chunk)

        return {
            "storage_provider": "LOCAL",
            "storage_key": storage_key,
            "file_path": target_path,
            "url": f"/api/media/files/{storage_key}",
            "size_bytes": total_size
        }

    def get_file_url(self, storage_key: str) -> str:
        return f"/api/media/files/{storage_key}"

class StorageUnavailableError(RuntimeError):
    pass

class SupabaseStorageProvider(StorageProvider):
    """
    Supabase Storage bucket provider.
    """
    def __init__(self, bucket_name: str = "bayyinah-media"):
        self.bucket_name = bucket_name
        self.local_fallback = LocalStorageProvider()

    def save_file(self, file_bytes: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
            if settings.ENVIRONMENT == "production":
                raise StorageUnavailableError("STORAGE_UNAVAILABLE: Supabase storage credentials missing in production")
            logger.info("Supabase storage keys not configured. Storing locally.")
            return self.local_fallback.save_file(file_bytes, filename, mime_type)

        try:
            from supabase import create_client
            client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
            ext = os.path.splitext(filename)[1]
            storage_key = f"{uuid.uuid4().hex}{ext}"
            
            client.storage.from_(self.bucket_name).upload(storage_key, file_bytes, {"content-type": mime_type})
            public_url = client.storage.from_(self.bucket_name).get_public_url(storage_key)
            return {
                "storage_provider": "SUPABASE",
                "storage_key": storage_key,
                "url": public_url,
                "size_bytes": len(file_bytes)
            }
        except Exception as e:
            if settings.ENVIRONMENT == "production":
                raise StorageUnavailableError(f"STORAGE_UNAVAILABLE: Supabase storage upload failed: {e}")
            logger.warning(f"Supabase storage upload failed: {e}. Falling back to local.")
            return self.local_fallback.save_file(file_bytes, filename, mime_type)

    def save_file_stream(self, file_obj: Any, filename: str, mime_type: str) -> Dict[str, Any]:
        return self.local_fallback.save_file_stream(file_obj, filename, mime_type)

    def get_file_url(self, storage_key: str) -> str:
        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{self.bucket_name}/{storage_key}"

class R2StorageProvider(StorageProvider):
    """
    Cloudflare R2 Object Storage Provider (S3-compatible).
    """
    def __init__(self):
        self.local_fallback = LocalStorageProvider()

    def save_file(self, file_bytes: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        if not settings.R2_ACCESS_KEY_ID or not settings.R2_SECRET_ACCESS_KEY or not settings.R2_ENDPOINT:
            if settings.ENVIRONMENT == "production":
                raise StorageUnavailableError("STORAGE_UNAVAILABLE: R2 storage credentials missing in production")
            logger.info("R2 credentials not provided. Using local storage.")
            return self.local_fallback.save_file(file_bytes, filename, mime_type)

        try:
            import boto3
            s3 = boto3.client(
                "s3",
                endpoint_url=settings.R2_ENDPOINT,
                aws_access_key_id=settings.R2_ACCESS_KEY_ID,
                aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
                region_name="auto"
            )
            ext = os.path.splitext(filename)[1]
            storage_key = f"{uuid.uuid4().hex}{ext}"
            s3.put_object(
                Bucket=settings.R2_BUCKET,
                Key=storage_key,
                Body=file_bytes,
                ContentType=mime_type
            )
            return {
                "storage_provider": "R2",
                "storage_key": storage_key,
                "url": f"https://{settings.R2_BUCKET}.r2.cloudflarestorage.com/{storage_key}",
                "size_bytes": len(file_bytes)
            }
        except Exception as e:
            if settings.ENVIRONMENT == "production":
                raise StorageUnavailableError(f"STORAGE_UNAVAILABLE: R2 upload failed: {e}")
            logger.warning(f"R2 upload failed: {e}. Falling back to local.")
            return self.local_fallback.save_file(file_bytes, filename, mime_type)

    def save_file_stream(self, file_obj: Any, filename: str, mime_type: str) -> Dict[str, Any]:
        return self.local_fallback.save_file_stream(file_obj, filename, mime_type)

    def get_file_url(self, storage_key: str) -> str:
        return f"https://{settings.R2_BUCKET}.r2.cloudflarestorage.com/{storage_key}"

def get_storage_provider() -> StorageProvider:
    provider = (settings.STORAGE_PROVIDER or "LOCAL").upper()
    if provider == "R2":
        return R2StorageProvider()
    elif provider == "SUPABASE":
        return SupabaseStorageProvider()
    return LocalStorageProvider()

storage_service = get_storage_provider()
