import json
import os
from typing import List, Optional, Dict
from ..models.schemas import SourceRegistryItem

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

class RegistryService:
    def __init__(self):
        self._sources: List[SourceRegistryItem] = []
        self._load_sources()

    def _load_sources(self):
        sources_path = os.path.join(DATA_DIR, "sources_registry.json")
        if os.path.exists(sources_path):
            with open(sources_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._sources = [SourceRegistryItem(**item) for item in data]
        else:
            self._sources = []

    def get_all_sources(self) -> List[SourceRegistryItem]:
        return self._sources

    def get_source_by_id(self, source_id: str) -> Optional[SourceRegistryItem]:
        for src in self._sources:
            if src.id == source_id:
                return src
        return None

    def get_sources_by_category(self, category: str) -> List[SourceRegistryItem]:
        if category == "all":
            return self._sources
        return [src for src in self._sources if src.category == category]

registry_service = RegistryService()
