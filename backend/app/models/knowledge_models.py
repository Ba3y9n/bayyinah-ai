import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Float, DateTime, ForeignKey, Index, BigInteger
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class SourceModel(Base):
    __tablename__ = "sources"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String(100), nullable=True, unique=True, index=True)
    name = Column(String(255), nullable=True)
    name_ar = Column(String(255), nullable=True)
    name_en = Column(String(255), nullable=True)
    organization = Column(String(255), nullable=True)
    author = Column(String(255), nullable=True)
    category = Column(String(50), nullable=True, index=True)
    source_type = Column(String(50), nullable=True)
    url = Column(Text, nullable=True)
    official_url = Column(Text, nullable=True)
    specific_url = Column(Text, nullable=True)
    license = Column(Text, nullable=True)
    license_status = Column(String(50), default="PENDING_VERIFICATION")
    license_name = Column(String(255), nullable=True)
    license_url = Column(Text, nullable=True)
    license_reference = Column(Text, nullable=True)
    copyright_holder = Column(String(255), nullable=True)
    rights_status = Column(String(50), default="PUBLIC_OR_ACADEMIC")
    status = Column(String(50), default="ACTIVE")
    is_active = Column(Boolean, default=True)
    trust_status = Column(String(50), default="APPROVED")
    usage_status = Column(String(50), default="SEARCH_SNIPPETS_AND_REFERRAL")
    base_domain = Column(String(255), nullable=True)
    authority_level = Column(String(50), default="PRIMARY_CANONICAL")
    content_scope = Column(Text, nullable=True)
    publisher = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    verification_method = Column(String(100), default="EDITORIAL_REVIEW")
    verified_by = Column(String(150), nullable=True)
    description = Column(Text, nullable=True)
    language = Column(String(10), default="ar")
    scientific_status = Column(String(50), default="APPROVED")
    
    # Allowed operations
    allowed_operations = Column(Text, default="{}")
    indexing_allowed = Column(Boolean, default=True)
    storage_allowed = Column(Boolean, default=False)
    excerpt_allowed = Column(Boolean, default=True)
    link_allowed = Column(Boolean, default=True)
    translation_allowed = Column(Boolean, default=False)
    embedding_allowed = Column(Boolean, default=True)
    verification_notes = Column(Text, nullable=True)
    
    approved_by_challenge = Column(Boolean, default=True)
    usage_rule = Column(Text, nullable=True)
    version = Column(String(50), default="1.0.0")
    
    last_verified_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    documents = relationship("DocumentModel", back_populates="source", cascade="all, delete-orphan")

# Alias for backwards compatibility
TrustedSourceModel = SourceModel


class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String(36), ForeignKey("sources.id"), nullable=False, index=True)
    title = Column(String(500), nullable=True)
    title_ar = Column(String(500), nullable=True)
    title_en = Column(String(500), nullable=True)
    content = Column(Text, nullable=True)
    content_ar = Column(Text, nullable=True)
    author = Column(String(255), nullable=True)
    publisher = Column(String(255), nullable=True)
    document_type = Column(String(100), nullable=True)
    category = Column(String(50), nullable=False, index=True)
    reference = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    original_url = Column(Text, nullable=True)
    official_url = Column(Text, nullable=True)
    canonical_url = Column(Text, nullable=True)
    language = Column(String(10), default="ar")
    publication_date = Column(String(50), nullable=True)
    publication_info = Column(Text, nullable=True)
    edition = Column(String(100), nullable=True)
    isbn = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    rights_status = Column(String(50), default="PUBLIC_ACCESS")
    copyright_holder = Column(String(255), nullable=True)
    license_status = Column(String(50), default="PENDING_VERIFICATION")
    license_name = Column(String(255), nullable=True)
    license_url = Column(Text, nullable=True)
    ingestion_method = Column(String(100), default="CURATED_SEED")
    ingestion_status = Column(String(50), default="INDEXED", index=True)
    indexing_status = Column(String(50), default="INDEXED", index=True)
    content_hash = Column(String(64), nullable=True, index=True)
    version = Column(String(20), default="1.0")
    metadata_json = Column("metadata", Text, default="{}")
    last_checked_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    source = relationship("SourceModel", back_populates="documents")
    chunks = relationship("DocumentChunkModel", back_populates="document", cascade="all, delete-orphan")


class SourceVersionModel(Base):
    __tablename__ = "source_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String(36), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(String(50), nullable=False, default="1.0.0")
    content_hash = Column(Text, nullable=True)
    changed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    change_summary = Column(Text, nullable=True)


class DocumentSectionModel(Base):
    __tablename__ = "document_sections"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(Text, nullable=True)
    section_order = Column(Integer, default=1)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DocumentChunkModel(Base):
    __tablename__ = "document_chunks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False, index=True)
    section_id = Column(String(36), ForeignKey("document_sections.id", ondelete="SET NULL"), nullable=True, index=True)
    chunk_index = Column(Integer, default=0)
    chunk_text = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    content_ar = Column(Text, nullable=True)
    normalized_text = Column(Text, nullable=True)
    normalized_content = Column(Text, nullable=True)
    language = Column(String(10), default="ar")
    page_number = Column(Integer, nullable=True)
    section = Column(String(255), nullable=True)
    section_title = Column(String(255), nullable=True)
    chapter_title = Column(String(255), nullable=True)
    paragraph = Column(String(100), nullable=True)
    paragraph_number = Column(Integer, nullable=True)
    paragraph_reference = Column(String(100), nullable=True)
    verse_reference = Column(String(100), nullable=True, index=True)
    hadith_reference = Column(String(100), nullable=True, index=True)
    book_reference = Column(String(255), nullable=True)
    volume = Column(String(50), nullable=True)
    page = Column(String(50), nullable=True)
    reference = Column(String(255), nullable=True)
    locator = Column(Text, nullable=True)
    source_locator = Column(Text, nullable=True)
    source_url = Column(Text, nullable=True)
    canonical_url = Column(Text, nullable=True)
    content_hash = Column(String(64), nullable=True, index=True)
    version = Column(String(20), default="1.0")
    embedding = Column(Text, nullable=True)
    embedding_model = Column(String(100), default="models/text-embedding-004")
    embedding_version = Column(String(20), default="v1")
    search_vector = Column(Text, nullable=True)
    metadata_json = Column("metadata", Text, default="{}")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    document = relationship("DocumentModel", back_populates="chunks")


class VerificationSessionModel(Base):
    __tablename__ = "verification_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_status = Column(String(50), default="ACTIVE")
    input_type = Column(String(50), default="TEXT")
    input_reference = Column(Text, nullable=True)
    active_claim_id = Column(String(36), nullable=True)
    result_id = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    claims = relationship("ClaimModel", back_populates="session", cascade="all, delete-orphan")
    messages = relationship("ConversationMessageModel", back_populates="session", cascade="all, delete-orphan")
    media = relationship("MediaAssetModel", back_populates="session", cascade="all, delete-orphan")
    urls = relationship("UrlSubmissionModel", back_populates="session", cascade="all, delete-orphan")


class ClaimModel(Base):
    __tablename__ = "claims"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    verification_session_id = Column(String(36), ForeignKey("verification_sessions.id"), nullable=True, index=True)
    user_input = Column(Text, nullable=True)
    original_input = Column(Text, nullable=True)
    original_text = Column(Text, nullable=True)
    claim_text = Column(Text, nullable=True)
    normalized_claim = Column(Text, nullable=True)
    normalized_text = Column(Text, nullable=True)
    main_claim = Column(Text, nullable=True)
    claim_type = Column(String(50), default="CLAIM", index=True)
    category = Column(String(50), default="GENERAL", index=True)
    content_level = Column(String(20), default="LEVEL_A", index=True)
    language = Column(String(10), default="ar")
    sensitivity = Column(String(20), default="LOW")
    sensitivity_level = Column(String(20), default="low")
    entities = Column(Text, default="[]")
    keywords = Column(Text, default="[]")
    references = Column(Text, default="[]")
    generated_queries = Column(Text, default="[]")
    risk_level = Column(String(20), default="LOW")
    requires_specialist = Column(Boolean, default=False)
    requires_conflict_check = Column(Boolean, default=False)
    requires_source_verification = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    session = relationship("VerificationSessionModel", back_populates="claims")
    evidence = relationship("EvidenceModel", back_populates="claim", cascade="all, delete-orphan")
    results = relationship("VerificationResultModel", back_populates="claim", cascade="all, delete-orphan")


class EvidenceModel(Base):
    __tablename__ = "evidence"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    claim_id = Column(String(36), ForeignKey("claims.id"), nullable=True, index=True)
    source_id = Column(String(36), ForeignKey("sources.id"), nullable=True, index=True)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=True, index=True)
    chunk_id = Column(String(36), ForeignKey("document_chunks.id"), nullable=True, index=True)
    evidence_type = Column(String(50), default="DIRECT_SUPPORT")
    evidence_text = Column(Text, nullable=True)
    excerpt = Column(Text, nullable=True)
    matched_text = Column(Text, nullable=True)
    normalized_text = Column(Text, nullable=True)
    source_url = Column(Text, nullable=True)
    reference = Column(Text, nullable=True)
    locator = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    retrieval_method = Column(String(50), default="HYBRID")
    keyword_score = Column(Float, default=0.0)
    semantic_score = Column(Float, default=0.0)
    exact_score = Column(Float, default=0.0)
    metadata_score = Column(Float, default=0.0)
    rrf_score = Column(Float, default=0.0)
    relevance_score = Column(Float, default=0.0)
    support_type = Column(String(50), default="DIRECT_SUPPORT")
    support_score = Column(Float, default=0.0)
    support_level = Column(String(50), default="DIRECT_SUPPORT")
    attribution_status = Column(String(50), default="VERIFIED_ATTRIBUTION")
    validation_status = Column(String(50), default="VERIFIED")
    provenance = Column(Text, default="{}")
    metadata_json = Column("metadata", Text, default="{}")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    claim = relationship("ClaimModel", back_populates="evidence")


class VerificationResultModel(Base):
    __tablename__ = "verification_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    claim_id = Column(String(36), ForeignKey("claims.id"), nullable=True, index=True)
    status = Column(String(50), default="NOT_ESTABLISHED", index=True)
    confidence = Column(Float, default=0.0)
    summary = Column(Text, nullable=True)
    reason = Column(Text, nullable=True)
    checked_sources_count = Column(Integer, default=0)
    source_count = Column(Integer, default=0)
    evidence_count = Column(Integer, default=0)
    conflict_count = Column(Integer, default=0)
    conflict_detected = Column(Boolean, default=False)
    specialist_required = Column(Boolean, default=False)
    primary_source_id = Column(String(36), nullable=True)
    primary_evidence_id = Column(String(36), nullable=True)
    limitations = Column(Text, default="[]")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    claim = relationship("ClaimModel", back_populates="results")


class ConversationMessageModel(Base):
    __tablename__ = "conversation_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    verification_session_id = Column(String(36), ForeignKey("verification_sessions.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    claim_id = Column(String(36), ForeignKey("claims.id"), nullable=True)
    evidence_ids = Column(Text, default="[]")
    source_ids = Column(Text, default="[]")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    session = relationship("VerificationSessionModel", back_populates="messages")


class MediaAssetModel(Base):
    __tablename__ = "media_assets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    verification_session_id = Column(String(36), ForeignKey("verification_sessions.id"), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    original_filename = Column(String(255), nullable=True)
    mime_type = Column(String(100), nullable=True)
    size_bytes = Column(BigInteger, default=0)
    storage_provider = Column(String(50), default="LOCAL")
    storage_key = Column(Text, nullable=True)
    source_url = Column(Text, nullable=True)
    gemini_file_name = Column(String(255), nullable=True)
    gemini_file_uri = Column(Text, nullable=True)
    processing_status = Column(String(50), default="PENDING")
    metadata_json = Column("metadata", Text, default="{}")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    session = relationship("VerificationSessionModel", back_populates="media")


class UrlSubmissionModel(Base):
    __tablename__ = "url_submissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    verification_session_id = Column(String(36), ForeignKey("verification_sessions.id"), nullable=False, index=True)
    url = Column(Text, nullable=False)
    normalized_url = Column(Text, nullable=False)
    platform = Column(String(50), default="GENERIC")
    content_type = Column(String(50), default="ARTICLE")
    resolution_status = Column(String(50), default="PENDING")
    title = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    author = Column(String(255), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    thumbnail_url = Column(Text, nullable=True)
    metadata_json = Column("metadata", Text, default="{}")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    session = relationship("VerificationSessionModel", back_populates="urls")


class IngestionJobModel(Base):
    __tablename__ = "ingestion_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String(36), ForeignKey("sources.id"), nullable=True, index=True)
    job_type = Column(String(50), default="FULL")
    status = Column(String(50), default="QUEUED")
    documents_discovered = Column(Integer, default=0)
    documents_processed = Column(Integer, default=0)
    chunks_created = Column(Integer, default=0)
    embeddings_created = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    is_dead_letter = Column(Boolean, default=False)
    dead_letter_reason = Column(Text, nullable=True)
    metadata_json = Column("metadata", Text, default="{}")


class SearchLogModel(Base):
    __tablename__ = "search_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("verification_sessions.id"), nullable=True, index=True)
    query = Column(Text, nullable=False)
    search_type = Column(String(50), default="HYBRID")
    results_count = Column(Integer, default=0)
    latency_ms = Column(Float, default=0.0)
    metadata_json = Column("metadata", Text, default="{}")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class SourceDocumentModel(Base):
    __tablename__ = "source_documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String(36), ForeignKey("sources.id"), nullable=False, index=True)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False, index=True)
    association_type = Column(String(50), default="PRIMARY")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class EvaluationCaseModel(Base):
    __tablename__ = "evaluation_cases"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    input_text = Column(Text, nullable=False)
    expected_status = Column(String(50), nullable=False)
    expected_claim = Column(Text, nullable=True)
    test_type = Column(String(50), default="SYNTHETIC")
    metadata_json = Column("metadata", Text, default="{}")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class EvaluationRunModel(Base):
    __tablename__ = "evaluation_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    run_mode = Column(String(50), default="LIVE_KNOWLEDGE_BASE")
    total_cases = Column(Integer, default=0)
    passed_cases = Column(Integer, default=0)
    failed_cases = Column(Integer, default=0)
    accuracy_score = Column(Float, default=0.0)
    latency_avg_ms = Column(Float, default=0.0)
    details = Column(Text, default="[]")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class TranslationTermModel(Base):
    __tablename__ = "translation_terms"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    term_ar = Column(String(255), nullable=False, index=True)
    term_en = Column(String(255), nullable=True)
    preferred_translation = Column(String(255), nullable=True)
    alternative_translation = Column(String(255), nullable=True)
    explanation = Column(Text, nullable=True)
    usage_notes = Column(Text, nullable=True)
    source_id = Column(String(36), ForeignKey("sources.id"), nullable=True)
    source_url = Column(Text, nullable=True)
    verified = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class TermModel(Base):
    __tablename__ = "terms"

    id = Column(String(100), primary_key=True)
    term_ar = Column(String(255), nullable=False, unique=True)
    term_normalized = Column(String(255), nullable=False, index=True)
    category = Column(String(50), nullable=False)
    definition_ar = Column(Text, nullable=False)
    source_id = Column(String(100), nullable=True)
    locator = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class TermTranslationModel(Base):
    __tablename__ = "term_translations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    term_id = Column(String(100), ForeignKey("terms.id"), nullable=False, index=True)
    language = Column(String(10), nullable=False)
    approved_translation = Column(String(255), nullable=False)
    contextual_explanation = Column(Text, nullable=False)
    usage_notes = Column(Text, nullable=True)
    is_standard = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class KnowledgeAuditLogModel(Base):
    __tablename__ = "knowledge_audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    request_id = Column(String(100), nullable=True, index=True)
    claim_id = Column(String(36), nullable=True)
    query = Column(Text, nullable=True)
    search_query = Column(Text, nullable=True)
    category_filter = Column(String(50), nullable=True)
    sources_checked = Column(Integer, default=0)
    documents_checked = Column(Integer, default=0)
    chunks_checked = Column(Integer, default=0)
    evidence_found = Column(Integer, default=0)
    sources_searched = Column(Text, default="[]")
    documents_searched = Column(Integer, default=0)
    retrieved_chunks = Column(Integer, default=0)
    validation_result = Column(String(50), nullable=True)
    conflicts_found = Column(Boolean, default=False)
    final_status = Column(String(50), nullable=True, index=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    model = Column(String(100), default="gemini-3.8-flash")
    model_version = Column(String(50), default="3.8")
    embedding_model = Column(String(100), default="models/text-embedding-004")
    embedding_version = Column(String(20), default="v1")
    latency_breakdown = Column(Text, default="{}")
    latency_ms = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class MediaArtifactModel(Base):
    __tablename__ = "media_artifacts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    media_asset_id = Column(String(36), ForeignKey("media_assets.id"), nullable=False, index=True)
    artifact_type = Column(String(50), nullable=False, index=True) # TRANSCRIPT, OCR_TEXT, FRAME, THUMBNAIL
    file_path = Column(Text, nullable=True)
    public_url = Column(Text, nullable=True)
    artifact_hash = Column(String(64), nullable=True)
    timestamp_start = Column(String(20), nullable=True)
    timestamp_end = Column(String(20), nullable=True)
    extracted_text = Column(Text, nullable=True)
    metadata_json = Column("metadata", JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ChatSessionModel(Base):
    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    verification_session_id = Column(String(36), ForeignKey("verification_sessions.id"), nullable=True, index=True)
    active_claim_id = Column(String(36), ForeignKey("claims.id"), nullable=True, index=True)
    session_title = Column(String(255), nullable=True)
    state = Column(String(50), default="ACTIVE")
    model = Column(String(50), default="gemini-3.8-flash")
    metadata_json = Column("metadata", JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    messages = relationship("ChatMessageModel", back_populates="session", cascade="all, delete-orphan")


class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_session_id = Column(String(36), ForeignKey("chat_sessions.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False, index=True) # user, assistant, system
    content = Column(Text, nullable=False)
    intent = Column(String(50), default="FOLLOWUP_ON_CURRENT_EVIDENCE", index=True)
    grounding_status = Column(String(50), default="GROUNDED")
    abstention_reason = Column(Text, nullable=True)
    citations = Column(JSONB, default=list)
    suggested_followups = Column(JSONB, default=list)
    avatar_state = Column(String(30), default="idle")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    session = relationship("ChatSessionModel", back_populates="messages")
    evidence_bindings = relationship("ChatEvidenceBindingModel", back_populates="message", cascade="all, delete-orphan")


class ChatEvidenceBindingModel(Base):
    __tablename__ = "chat_evidence_bindings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_message_id = Column(String(36), ForeignKey("chat_messages.id"), nullable=False, index=True)
    evidence_id = Column(String(36), ForeignKey("evidence.id"), nullable=False, index=True)
    chunk_id = Column(String(36), ForeignKey("document_chunks.id"), nullable=True)
    source_name = Column(String(255), nullable=True)
    reference = Column(Text, nullable=True)
    relevance_score = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    message = relationship("ChatMessageModel", back_populates="evidence_bindings")


class VerificationEvidenceModel(Base):
    __tablename__ = "verification_evidence"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    verification_result_id = Column(String(36), ForeignKey("verification_results.id"), nullable=False, index=True)
    evidence_id = Column(String(36), ForeignKey("evidence.id"), nullable=False, index=True)
    relevance_score = Column(Float, default=1.0)
    support_level = Column(String(50), default="DIRECT_SUPPORT")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DocumentVersionModel(Base):
    __tablename__ = "document_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(String(50), nullable=False, default="1.0")
    content_hash = Column(Text, nullable=True)
    normalized_hash = Column(Text, nullable=True)
    title = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    reference = Column(Text, nullable=True)
    diff_summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class KnowledgeReviewItemModel(Base):
    __tablename__ = "knowledge_review_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String(36), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False, index=True)
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True, index=True)
    item_type = Column(String(100), nullable=False, index=True)
    severity = Column(String(50), default="MEDIUM")
    status = Column(String(50), default="PENDING", index=True)
    reason = Column(Text, nullable=False)
    url = Column(Text, nullable=True)
    details = Column(JSONB, default=dict)
    resolution_notes = Column(Text, nullable=True)
    resolved_by = Column(String(150), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class SourceCoverageRunModel(Base):
    __tablename__ = "source_coverage_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    verification_session_id = Column(String(36), nullable=True, index=True)
    claim_id = Column(String(36), nullable=True, index=True)
    input_type = Column(String(50), default="TEXT")
    official_sources_total = Column(Integer, default=11)
    relevant_sources_count = Column(Integer, default=0)
    queried_sources_count = Column(Integer, default=0)
    evidence_sources_count = Column(Integer, default=0)
    coverage_status = Column(String(50), default="FULL")
    relevant_sources_json = Column("relevant_sources", Text, default="[]")
    queried_sources_json = Column("queried_sources", Text, default="[]")
    skipped_sources_json = Column("skipped_sources", Text, default="[]")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class SourceCoverageResultModel(Base):
    __tablename__ = "source_coverage_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String(36), ForeignKey("source_coverage_runs.id", ondelete="CASCADE"), nullable=True, index=True)
    verification_id = Column(String(36), nullable=True, index=True)
    claim_id = Column(String(36), nullable=True, index=True)
    source_id = Column(String(100), nullable=False)
    source_slug = Column(String(100), nullable=False, index=True)
    status = Column(String(50), default="SEARCHED")
    query = Column(Text, nullable=True)
    results_count = Column(Integer, default=0)
    evidence_count = Column(Integer, default=0)
    searched_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    error = Column(Text, nullable=True)


class SocialConnectionModel(Base):
    __tablename__ = "social_connections"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = Column(String(50), nullable=False, index=True)
    user_id = Column(String(255), nullable=True, index=True)
    encrypted_access_token = Column(Text, nullable=True)
    encrypted_refresh_token = Column(Text, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    scopes = Column(Text, default="[]")
    status = Column(String(50), default="CONNECTED")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class SocialAccessLogModel(Base):
    __tablename__ = "social_access_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = Column(String(50), nullable=False, index=True)
    action = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    details_json = Column("details", Text, default="{}")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


