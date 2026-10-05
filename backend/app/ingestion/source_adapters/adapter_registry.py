"""
Bayyinah AI - Source Adapter Registry
Central dispatcher for all 11 official source adapters.
Guarantees that every approved domain/source is mapped to its specialized parser.
"""

from typing import Optional, Dict, Any, Type
from urllib.parse import urlparse
from ..official_allowlist import OFFICIAL_SOURCE_ALLOWLIST, get_matched_allowlist_entry, is_url_in_allowlist
from .base_adapter import BaseSourceAdapter
from .dorar_hadith_adapter import DorarHadithAdapter
from .quranpedia_adapter import QuranpediaAdapter
from .dorar_tafsir_adapter import DorarTafsirAdapter
from .dorar_fiqh_adapter import DorarFiqhAdapter
from .dorar_aqeedah_adapter import DorarAqeedahAdapter
from .dorar_history_adapter import DorarHistoryAdapter
from .dictionary_adapter import DictionaryAdapter
from .dawa_center_adapter import DawaCenterAdapter
from .dawa_file_adapter import DawaFileAdapter
from .islamic_content_adapter import IslamicContentAdapter
from .shamela_adapter import ShamelaAdapter

ADAPTER_CLASSES: Dict[str, Type[BaseSourceAdapter]] = {
    "DorarHadithAdapter": DorarHadithAdapter,
    "QuranpediaAdapter": QuranpediaAdapter,
    "DorarTafsirAdapter": DorarTafsirAdapter,
    "DorarFiqhAdapter": DorarFiqhAdapter,
    "DorarAqeedahAdapter": DorarAqeedahAdapter,
    "DorarHistoryAdapter": DorarHistoryAdapter,
    "DictionaryAdapter": DictionaryAdapter,
    "DawaCenterAdapter": DawaCenterAdapter,
    "DawaFileAdapter": DawaFileAdapter,
    "IslamicContentAdapter": IslamicContentAdapter,
    "ShamelaAdapter": ShamelaAdapter,
}

_ADAPTER_INSTANCES: Dict[str, BaseSourceAdapter] = {}

def get_adapter_by_slug(slug: str) -> Optional[BaseSourceAdapter]:
    """Retrieves the adapter instance for a specific official source slug."""
    for entry in OFFICIAL_SOURCE_ALLOWLIST:
        if entry["slug"] == slug:
            adapter_class_name = entry.get("adapter_class")
            if adapter_class_name in ADAPTER_CLASSES:
                if slug not in _ADAPTER_INSTANCES:
                    _ADAPTER_INSTANCES[slug] = ADAPTER_CLASSES[adapter_class_name](entry)
                return _ADAPTER_INSTANCES[slug]
    return None

def get_adapter_by_url(url: str) -> Optional[BaseSourceAdapter]:
    """Retrieves the adapter instance matching the given URL from the official allowlist."""
    entry = get_matched_allowlist_entry(url)
    if not entry:
        return None
    slug = entry["slug"]
    adapter_class_name = entry.get("adapter_class")
    if adapter_class_name in ADAPTER_CLASSES:
        if slug not in _ADAPTER_INSTANCES:
            _ADAPTER_INSTANCES[slug] = ADAPTER_CLASSES[adapter_class_name](entry)
        return _ADAPTER_INSTANCES[slug]
    return None

def get_all_adapters() -> Dict[str, BaseSourceAdapter]:
    """Returns all 11 source adapter instances."""
    for entry in OFFICIAL_SOURCE_ALLOWLIST:
        slug = entry["slug"]
        if slug not in _ADAPTER_INSTANCES:
            adapter_class_name = entry.get("adapter_class")
            if adapter_class_name in ADAPTER_CLASSES:
                _ADAPTER_INSTANCES[slug] = ADAPTER_CLASSES[adapter_class_name](entry)
    return _ADAPTER_INSTANCES
