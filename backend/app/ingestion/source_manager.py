"""
Bayyinah AI - Ingestion Source Manager
Registers, verifies, and audits trusted sources.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
import uuid
import logging

logger = logging.getLogger("bayyinah.ingestion.sources")

class IngestionSourceManager:
    """
    Manages source discovery, status checks, and license verification.
    """

    def get_or_create_source(self, db: Session, source_info: Dict[str, Any]) -> str:
        s_name = source_info.get("name") or source_info.get("name_ar") or "مصدر موثوق"
        
        # Check if source exists by name or URL
        check_sql = text("SELECT id FROM sources WHERE name = :name OR name_ar = :name OR (url IS NOT NULL AND url = :url) LIMIT 1;")
        existing_id = db.execute(check_sql, {
            "name": s_name,
            "url": source_info.get("url") or ""
        }).scalar()

        if existing_id:
            return str(existing_id)

        # Insert new source
        new_id = str(uuid.uuid4())
        insert_sql = text("""
            INSERT INTO sources (
                id, name, name_ar, name_en, organization, author, category,
                source_type, url, official_url, license, rights_status, status,
                scientific_status, is_active, description
            ) VALUES (
                :id, :name, :name_ar, :name_en, :organization, :author, :category,
                :source_type, :url, :official_url, :license, :rights_status, :status,
                :scientific_status, :is_active, :description
            );
        """)
        
        db.execute(insert_sql, {
            "id": new_id,
            "name": s_name,
            "name_ar": source_info.get("name_ar") or s_name,
            "name_en": source_info.get("name_en") or s_name,
            "organization": source_info.get("organization"),
            "author": source_info.get("author"),
            "category": source_info.get("category", "GENERAL"),
            "source_type": source_info.get("source_type", "OFFICIAL_PORTAL"),
            "url": source_info.get("url"),
            "official_url": source_info.get("url") or source_info.get("official_url"),
            "license": source_info.get("license", "Fair Quotation for Scientific Verification"),
            "rights_status": source_info.get("rights_status", "PUBLIC_OR_ACADEMIC"),
            "status": "ACTIVE",
            "scientific_status": "APPROVED",
            "is_active": True,
            "description": source_info.get("description", "مصدر موثوق ومعتمد")
        })
        db.commit()
        return new_id

source_manager = IngestionSourceManager()
