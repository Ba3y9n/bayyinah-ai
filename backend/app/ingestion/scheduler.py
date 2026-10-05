"""
Bayyinah AI - Autonomous Knowledge Scheduler
Enforces Section 9 of Master Specifications:
1. Source-specific crawl scheduling configurations (intervals, rate limits, priority, enabled state).
2. Supports programmatic periodic triggers, background task orchestration, and immediate 'Sync Now' triggers.
"""

import time
import logging
import threading
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from .official_allowlist import OFFICIAL_SOURCE_ALLOWLIST
from .acquisition_engine import acquisition_engine

logger = logging.getLogger("bayyinah.ingestion.scheduler")

# Granular source configurations
SOURCE_CRAWL_CONFIGS: Dict[str, Dict[str, Any]] = {
    "dorar-hadith": {
        "slug": "dorar-hadith",
        "name_ar": "الموسوعة الحديثية - الدرر السنية",
        "crawl_interval_hours": 24,
        "enabled": True,
        "max_requests_per_minute": 30,
        "priority": "HIGH",
        "adapter": "DorarHadithAdapter"
    },
    "dorar-tafseer": {
        "slug": "dorar-tafseer",
        "name_ar": "موسوعة التفسير المحرر - الدرر السنية",
        "crawl_interval_hours": 24,
        "enabled": True,
        "max_requests_per_minute": 30,
        "priority": "HIGH",
        "adapter": "DorarTafsirAdapter"
    },
    "dorar-feqhia": {
        "slug": "dorar-feqhia",
        "name_ar": "الموسوعة الفقهية المحررة - الدرر السنية",
        "crawl_interval_hours": 24,
        "enabled": True,
        "max_requests_per_minute": 30,
        "priority": "HIGH",
        "adapter": "DorarFiqhAdapter"
    },
    "dorar-aqeeda": {
        "slug": "dorar-aqeeda",
        "name_ar": "موسوعة العقيدة والمذاهب - الدرر السنية",
        "crawl_interval_hours": 48,
        "enabled": True,
        "max_requests_per_minute": 30,
        "priority": "MEDIUM",
        "adapter": "DorarAqeedahAdapter"
    },
    "dorar-history": {
        "slug": "dorar-history",
        "name_ar": "الموسوعة التاريخية وأحداث السيرة - الدرر السنية",
        "crawl_interval_hours": 48,
        "enabled": True,
        "max_requests_per_minute": 30,
        "priority": "MEDIUM",
        "adapter": "DorarHistoryAdapter"
    },
    "quranpedia": {
        "slug": "quranpedia",
        "name_ar": "موسوعة القرآن الكريم - قرآن بيديا",
        "crawl_interval_hours": 72,
        "enabled": True,
        "max_requests_per_minute": 20,
        "priority": "HIGH",
        "adapter": "QuranpediaAdapter"
    },
    "islamic-content": {
        "slug": "islamic-content",
        "name_ar": "موسوعة المحتوى الإسلامي المترجم",
        "crawl_interval_hours": 24,
        "enabled": True,
        "max_requests_per_minute": 30,
        "priority": "HIGH",
        "adapter": "IslamicContentAdapter"
    },
    "islamic-content-dict": {
        "slug": "islamic-content-dict",
        "name_ar": "قاموس المصطلحات والمفاهيم الإسلامية المترجمة",
        "crawl_interval_hours": 48,
        "enabled": True,
        "max_requests_per_minute": 30,
        "priority": "HIGH",
        "adapter": "DictionaryAdapter"
    },
    "dawa-center": {
        "slug": "dawa-center",
        "name_ar": "مركز دعوة للتعريف بالإسلام",
        "crawl_interval_hours": 24,
        "enabled": True,
        "max_requests_per_minute": 30,
        "priority": "HIGH",
        "adapter": "DawaCenterAdapter"
    },
    "dawa-file-7937": {
        "slug": "dawa-file-7937",
        "name_ar": "دليل الأسئلة والشبهات المعاصرة - مركز دعوة (ملف 7937)",
        "crawl_interval_hours": 72,
        "enabled": True,
        "max_requests_per_minute": 15,
        "priority": "CRITICAL",
        "adapter": "DawaFileAdapter"
    },
    "shamela": {
        "slug": "shamela",
        "name_ar": "المكتبة الشاملة الرقمية الوقفية",
        "crawl_interval_hours": 168,
        "enabled": True,
        "max_requests_per_minute": 15,
        "priority": "MEDIUM",
        "adapter": "ShamelaAdapter"
    }
}

class KnowledgeScheduler:
    """
    Scheduler orchestrating background crawl runs and manual sync dispatches.
    """

    def __init__(self):
        self.configs = SOURCE_CRAWL_CONFIGS
        self._last_runs: Dict[str, float] = {}

    def get_source_configs(self) -> List[Dict[str, Any]]:
        """Returns configurations and last run status for all sources."""
        result = []
        for slug, cfg in self.configs.items():
            last_run = self._last_runs.get(slug)
            result.append({
                **cfg,
                "last_run_timestamp": last_run,
                "last_run_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(last_run)) if last_run else None
            })
        return result

    def trigger_sync_now(self, db: Session, source_slug: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes immediate manual sync for a specific official source or all 11 sources.
        """
        if source_slug:
            cfg = self.configs.get(source_slug)
            if not cfg:
                return {"success": False, "error": f"المصدر {source_slug} غير موجود في الإعدادات المعتمدة."}
            res = acquisition_engine.discover_and_expand_source(db, source_slug, max_documents=5)
            self._last_runs[source_slug] = time.time()
            return res
        else:
            res = acquisition_engine.sync_all_official_sources(db, max_docs_per_source=2)
            now = time.time()
            for s in self.configs:
                self._last_runs[s] = now
            return res

knowledge_scheduler = KnowledgeScheduler()
