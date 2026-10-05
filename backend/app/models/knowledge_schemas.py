from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class SourceCategory(str, Enum):
    DAWA = "DAWA"
    QURAN = "QURAN"
    TAFSEER = "TAFSEER"
    HADITH = "HADITH"
    AQEEDAH = "AQEEDAH"
    FIQH = "FIQH"
    SEERAH_HISTORY = "SEERAH_HISTORY"
    QUESTIONS_DOUBTS = "QUESTIONS_DOUBTS"
    DICTIONARY_TRANSLATION = "DICTIONARY_TRANSLATION"
    OTHER = "OTHER"

class SourceType(str, Enum):
    OFFICIAL_PLATFORM = "OFFICIAL_PLATFORM"
    DIGITAL_LIBRARY = "DIGITAL_LIBRARY"
    BOOK = "BOOK"
    ENCYCLOPEDIA = "ENCYCLOPEDIA"
    QURAN_DATABASE = "QURAN_DATABASE"
    HADITH_DATABASE = "HADITH_DATABASE"
    DICTIONARY = "DICTIONARY"
    REFERENCE_WORK = "REFERENCE_WORK"
    OTHER = "OTHER"

class TrustStatus(str, Enum):
    APPROVED = "APPROVED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    RESTRICTED = "RESTRICTED"
    DISABLED = "DISABLED"

class LicenseStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    RESTRICTED = "RESTRICTED"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"

class IngestionStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    INDEXED = "INDEXED"
    FAILED = "FAILED"
    DISABLED = "DISABLED"

class EvidenceType(str, Enum):
    DIRECT_SUPPORT = "DIRECT_SUPPORT"
    PARTIAL_SUPPORT = "PARTIAL_SUPPORT"
    CONTEXT = "CONTEXT"
    CONTRADICTING = "CONTRADICTING"
    RELATED = "RELATED"
    NO_MATCH = "NO_MATCH"

class ClaimType(str, Enum):
    QURAN_VERSE = "QURAN_VERSE"
    HADITH_CLAIM = "HADITH_CLAIM"
    HADITH_AUTHENTICITY = "HADITH_AUTHENTICITY"
    SCHOLAR_QUOTE = "SCHOLAR_QUOTE"
    FIQH_CLAIM = "FIQH_CLAIM"
    AQEEDAH_CLAIM = "AQEEDAH_CLAIM"
    HISTORICAL_CLAIM = "HISTORICAL_CLAIM"
    DAWA_CONTENT = "DAWA_CONTENT"
    TRANSLATION = "TRANSLATION"
    DEFINITION = "DEFINITION"
    GENERAL_INFORMATION = "GENERAL_INFORMATION"
    PERSONAL_FATWA = "PERSONAL_FATWA"
    OTHER = "OTHER"

class ContentLevel(str, Enum):
    LEVEL_A = "LEVEL_A"  # معلومات أصلية مستقرة
    LEVEL_B = "LEVEL_B"  # شرح وتعريف واستدلال
    LEVEL_C = "LEVEL_C"  # مسائل خلافية أو عالية الحساسية
    LEVEL_D = "LEVEL_D"  # فتوى أو حالة شخصية

class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    WEAK = "WEAK"
    FABRICATED = "FABRICATED"
    NOT_ESTABLISHED = "NOT_ESTABLISHED"
    INSUFFICIENT = "INSUFFICIENT"
    CONFLICT = "CONFLICT"
    SPECIALIST = "SPECIALIST"

class AllowedOperations(BaseModel):
    METADATA_ONLY: bool = True
    SEARCH_SNIPPETS: bool = True
    INDEX_CONTENT: bool = False
    STORE_CONTENT: bool = False
    QUOTE_LIMITED: bool = False
    DISPLAY_EXCERPT: bool = False
    LINK_TO_SOURCE: bool = True
    TRANSLATE: bool = False
    DERIVE_EMBEDDINGS: bool = False

class ProvenanceInfo(BaseModel):
    source_id: str
    source_name: str
    document_id: str
    document_title: str
    chunk_id: str
    locator: str
    url: str
    content_hash: str
    retrieved_at: str
    retrieval_method: Optional[str] = "HYBRID"

# Schema for Trusted Source creation / read
class TrustedSourceCreate(BaseModel):
    id: str
    name_ar: str
    name_en: str
    slug: str
    category: SourceCategory
    description: str
    official_url: str
    base_domain: str
    source_type: SourceType
    authority_level: str = "PRIMARY_CANONICAL"
    trust_status: TrustStatus = TrustStatus.REVIEW_REQUIRED
    usage_status: str = "METADATA_AND_SNIPPETS"
    license_status: LicenseStatus = LicenseStatus.PENDING_VERIFICATION
    license_name: Optional[str] = None
    license_url: Optional[str] = None
    copyright_holder: Optional[str] = None
    allowed_operations: AllowedOperations = Field(default_factory=AllowedOperations)
    content_scope: Optional[str] = None
    language: str = "ar"
    publisher: Optional[str] = None
    author: Optional[str] = None
    country: Optional[str] = None
    verification_method: str = "EDITORIAL_REVIEW"
    verification_notes: Optional[str] = None
    verified_by: Optional[str] = None
    is_active: bool = True

class TrustedSourceResponse(BaseModel):
    id: str
    name_ar: str
    name_en: str
    slug: str
    category: SourceCategory
    description: str
    official_url: str
    base_domain: str
    source_type: SourceType
    authority_level: str
    trust_status: TrustStatus
    usage_status: str
    license_status: LicenseStatus
    license_name: Optional[str] = None
    license_url: Optional[str] = None
    copyright_holder: Optional[str] = None
    allowed_operations: Dict[str, bool]
    content_scope: Optional[str] = None
    language: str
    publisher: Optional[str] = None
    author: Optional[str] = None
    country: Optional[str] = None
    verification_method: str
    verification_notes: Optional[str] = None
    last_verified_at: Optional[datetime] = None
    verified_by: Optional[str] = None
    is_active: bool
    documents_count: int = 0
    chunks_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TrustedSourceUpdate(BaseModel):
    trust_status: Optional[TrustStatus] = None
    license_status: Optional[LicenseStatus] = None
    is_active: Optional[bool] = None
    verification_notes: Optional[str] = None
    allowed_operations: Optional[Dict[str, bool]] = None

# Document schemas
class DocumentCreate(BaseModel):
    id: str
    source_id: str
    title_ar: str
    title_en: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    document_type: str
    category: SourceCategory
    official_url: str
    canonical_url: Optional[str] = None
    language: str = "ar"
    publication_date: Optional[str] = None
    edition: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None
    copyright_holder: Optional[str] = None
    license_status: LicenseStatus = LicenseStatus.PENDING_VERIFICATION
    license_name: Optional[str] = None
    license_url: Optional[str] = None
    ingestion_method: str = "CURATED_SEED"
    ingestion_status: IngestionStatus = IngestionStatus.INDEXED
    content_hash: str
    version: str = "1.0"

class DocumentResponse(BaseModel):
    id: str
    source_id: str
    title_ar: str
    title_en: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    document_type: str
    category: SourceCategory
    official_url: str
    canonical_url: Optional[str] = None
    language: str
    edition: Optional[str] = None
    description: Optional[str] = None
    license_status: LicenseStatus
    ingestion_status: IngestionStatus
    content_hash: str
    version: str
    chunks_count: int = 0
    created_at: Optional[datetime] = None

# Chunk schemas
class DocumentChunkResponse(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    content: str
    normalized_content: str
    language: str
    section_title: Optional[str] = None
    chapter_title: Optional[str] = None
    verse_reference: Optional[str] = None
    hadith_reference: Optional[str] = None
    book_reference: Optional[str] = None
    source_locator: str
    canonical_url: str
    content_hash: str
    embedding_model: str
    embedding_version: str

# Search & Retrieval Schemas
class KnowledgeSearchRequest(BaseModel):
    query: str
    category: Optional[str] = "all"
    language: Optional[str] = "ar"
    top_k: int = 10
    exact_only: bool = False
    source_id: Optional[str] = None

class KnowledgeSearchResultItem(BaseModel):
    source: Dict[str, Any]
    document: Dict[str, Any]
    chunk: Dict[str, Any]
    scores: Dict[str, float]
    provenance: ProvenanceInfo
    support_level: EvidenceType
    attribution_status: str
    verification_status: VerificationStatus

class KnowledgeSearchResponse(BaseModel):
    query: str
    category_filter: Optional[str] = None
    total_candidates: int
    results: List[KnowledgeSearchResultItem]
    latency_ms: float

# Source Health Schema
class SourceHealthItem(BaseModel):
    source_id: str
    source_name: str
    status: str # healthy, warning, failed
    url_accessible: bool
    metadata_complete: bool
    license_status: str
    trust_status: str
    documents_count: int
    chunks_count: int
    missing_items: List[str]

class KnowledgeBaseStats(BaseModel):
    total_sources: int
    active_sources: int
    sources_by_category: Dict[str, int]
    sources_by_trust: Dict[str, int]
    sources_by_license: Dict[str, int]
    total_documents: int
    total_chunks: int
    total_terms: int
    total_evidence: int = 0
    total_verifications: int = 0
    total_insufficient: int = 0
    total_conflicts: int = 0
    evidence_count: int = 0
    verifications_count: int = 0
    insufficient_count: int = 0
    conflict_count: int = 0
    sources_needing_review: int
    last_verified: Optional[str] = None

