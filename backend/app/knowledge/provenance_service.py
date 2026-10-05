import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from ..models.knowledge_models import DocumentChunkModel, DocumentModel, TrustedSourceModel
from ..models.knowledge_schemas import ProvenanceInfo

class ProvenanceService:
    """
    Constructs immutable, cryptographically verifiable provenance chains
    connecting User Output -> Chunk -> Document -> Source -> Canonical URL -> Content Hash.
    """

    @staticmethod
    def build_provenance(
        source: TrustedSourceModel,
        document: DocumentModel,
        chunk: DocumentChunkModel
    ) -> ProvenanceInfo:
        return ProvenanceInfo(
            source_id=source.id,
            source_name=source.name_ar,
            document_id=document.id,
            document_title=document.title_ar,
            chunk_id=chunk.id,
            locator=chunk.source_locator,
            url=chunk.canonical_url or document.canonical_url or document.official_url or source.official_url,
            content_hash=chunk.content_hash,
            retrieved_at=datetime.now(timezone.utc).isoformat()
        )

    @staticmethod
    def verify_provenance_integrity(chunk_content: str, recorded_hash: str) -> bool:
        computed = hashlib.sha256(chunk_content.encode("utf-8")).hexdigest()
        return computed == recorded_hash

provenance_service = ProvenanceService()
