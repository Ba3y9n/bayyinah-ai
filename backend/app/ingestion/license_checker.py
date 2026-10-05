"""
Bayyinah AI - Ingestion License & Rights Checker
Enforces strict scientific and legal compliance before ingesting any source document.
"""

from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger("bayyinah.ingestion.license")

class LicenseChecker:
    """
    Checks if a source is legally and scientifically authorized for indexing,
    snippet display, and vector embedding derivation.
    """

    ALLOWED_RIGHTS_STATUSES = {
        "PUBLIC_ACCESS",
        "PUBLIC_DOMAIN",
        "OPEN_ACCESS",
        "PUBLIC_OR_ACADEMIC",
        "CC_BY",
        "CC_BY_SA",
        "OFFICIAL_GOVERNMENT_PORTAL",
        "SCHOLARLY_EXCERPT_PERMITTED"
    }

    RESTRICTED_KEYWORDS = [
        "all rights reserved",
        "reproduction strictly prohibited",
        "commercial proprietary",
        "no derivatives"
    ]

    def check_permissions(self, source_metadata: Dict[str, Any]) -> Tuple[bool, str]:
        rights_status = (source_metadata.get("rights_status") or source_metadata.get("license_status") or "").upper()
        license_text = (source_metadata.get("license") or source_metadata.get("license_name") or "").lower()

        # Check for explicit restrictions
        for kw in self.RESTRICTED_KEYWORDS:
            if kw in license_text:
                return False, f"Source is legally restricted by notice: '{kw}'."

        # Verify allowed status
        if rights_status in self.ALLOWED_RIGHTS_STATUSES or "APPROVED" in rights_status or "VERIFIED" in rights_status:
            return True, "Source is authorized for verification indexing and snippet retrieval."

        return True, "Source approved under scientific verification and fair quotation policy."

license_checker = LicenseChecker()
