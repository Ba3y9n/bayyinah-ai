import json
import os
from typing import List, Optional, Dict
from ..models.schemas import SourceRegistryItem

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

class RegistryService:
    def __init__(self):
        self._sources: List[SourceRegistryItem] = []
        self._loaded = False

    def _ensure_loaded(self):
        if not self._loaded:
            self._load_sources()
            self._loaded = True

    def _load_sources(self):
        try:
            from ..db.database import SessionLocal
            from ..models.knowledge_models import TrustedSourceModel
            with SessionLocal() as db:
                db_sources = db.query(TrustedSourceModel).all()
                if db_sources:
                    self._sources = [
                        SourceRegistryItem(
                            id=s.id,
                            name=s.name or s.name_ar,
                            author=s.author,
                            organization=s.organization,
                            category=s.category.lower(),
                            source_type=s.source_type or "OFFICIAL_PLATFORM",
                            url=s.official_url or s.base_url or "",
                            license=s.license_name or ("رخصة موثقة" if s.license_status == "VERIFIED" else "قيد التحقق"),
                            status="active" if s.is_active else "inactive",
                            description=s.description or ""
                        )
                        for s in db_sources
                    ]
                    return
        except Exception:
            pass

        sources_path = os.path.join(DATA_DIR, "sources_registry.json")
        if os.path.exists(sources_path):
            with open(sources_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._sources = [SourceRegistryItem(**item) for item in data]
        else:
            self._sources = []

    def get_all_sources(self) -> List[SourceRegistryItem]:
        self._ensure_loaded()
        return self._sources

    def get_source_by_id(self, source_id: str) -> Optional[SourceRegistryItem]:
        self._ensure_loaded()
        for src in self._sources:
            if src.id == source_id:
                return src
        return None

    def get_sources_by_category(self, category: str) -> List[SourceRegistryItem]:
        self._ensure_loaded()
        if category == "all":
            return self._sources
        return [src for src in self._sources if src.category == category]

registry_service = RegistryService()
