from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class CanonicalVerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"                                     # ثابت بحسب المصدر
    NOT_ESTABLISHED_BY_EXACT_WORDING = "NOT_ESTABLISHED_BY_EXACT_WORDING" # لم يثبت بهذا اللفظ
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"           # لم نجد دليلًا كافيًا
    SCHOLARLY_DISAGREEMENT = "SCHOLARLY_DISAGREEMENT"         # اختلاف في المصادر
    NEEDS_SPECIALIST = "NEEDS_SPECIALIST"                     # يحتاج مراجعة مختص
    WEAK = "WEAK"                                             # ضعيف بحسب المصدر
    FABRICATED = "FABRICATED"                                 # موضوع/مكذوب بحسب المصدر

STATUS_ARABIC_LABELS = {
    CanonicalVerificationStatus.VERIFIED: "ثابت بحسب المصدر",
    CanonicalVerificationStatus.NOT_ESTABLISHED_BY_EXACT_WORDING: "لم يثبت بهذا اللفظ",
    CanonicalVerificationStatus.INSUFFICIENT_EVIDENCE: "لم نجد دليلًا كافيًا",
    CanonicalVerificationStatus.SCHOLARLY_DISAGREEMENT: "اختلاف في المصادر",
    CanonicalVerificationStatus.NEEDS_SPECIALIST: "يحتاج مراجعة مختص",
    CanonicalVerificationStatus.WEAK: "ضعيف بحسب المصدر",
    CanonicalVerificationStatus.FABRICATED: "موضوع/مكذوب بحسب المصدر",
}

class PlatformEnum(str, Enum):
    YOUTUBE = "YOUTUBE"
    YOUTUBE_SHORT = "YOUTUBE_SHORT"
    TIKTOK = "TIKTOK"
    X = "X"
    INSTAGRAM = "INSTAGRAM"
    WEB = "WEB"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    PDF = "PDF"
    UNKNOWN = "UNKNOWN"

class StructuredVerificationResult(BaseModel):
    status: str = Field(..., description="Canonical verification status enum")
    label_ar: str = Field(..., description="Arabic label for the status")
    claim: str = Field(..., description="The exact extracted claim text")
    reason: str = Field(..., description="Grounded explanation of why this verdict was reached")
    evidence_ids: List[str] = Field(default_factory=list, description="IDs of linked evidence records")
    source_ids: List[str] = Field(default_factory=list, description="IDs of trusted sources verified")
    citations: List[str] = Field(default_factory=list, description="Exact locator citations")
    conflict_status: str = Field("NONE", description="Conflict status: NONE, SCHOLARLY_DISAGREEMENT")
    grounding_status: str = Field("GROUNDED", description="GROUNDED, ABSTAINED, SPECIALIST_REFERRAL")
    abstained: bool = Field(False, description="True if the system abstained from making a claim")
    specialist_required: bool = Field(False, description="True if personal fatwa/specialist is required")

class URLResolutionResult(BaseModel):
    original_url: str
    canonical_url: str
    platform: str
    content_type: str # video, image, article, social_post, pdf, unknown
    content_id: Optional[str] = None
    author: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration: Optional[str] = None
    embed_url: Optional[str] = None
    extraction_status: str = "RESOLVED" # RESOLVED, BLOCKED_SSRF, PARTIAL, FAILED
    analysis_capability: str = "FULL" # FULL, METADATA_ONLY, REQUIRES_UPLOAD
    extracted_text: Optional[str] = None
    requires_media_upload: bool = False
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class VerificationRequest(BaseModel):
    text: Optional[str] = Field(None, description="Input text to verify")
    image_base64: Optional[str] = Field(None, description="Base64 encoded image or data URL for multimodal analysis")
    content_type_hint: Optional[str] = Field("auto", description="Optional hint for content type")
    session_id: Optional[str] = Field(None, description="Optional existing session ID")

class VerificationStepLog(BaseModel):
    step_number: int
    title: str
    description: str
    status: str = "completed" # completed, in_progress, pending, failed
    data: Optional[Dict[str, Any]] = None

class EvidenceItem(BaseModel):
    document_id: str
    source_id: str
    source_name: str
    author: Optional[str] = None
    organization: Optional[str] = None
    category: str
    title: str
    excerpt: str
    reference: str
    url: str
    license: str
    relevance_score: float
    evidence_type: str # direct_match, partial_match, conflicting_view, scholarly_commentary, not_found
    comparison_notes: Optional[str] = None
    ruling_or_grade: Optional[str] = None
    inference_strength: Optional[str] = "عالية" # عالية, متوسطة, محدودة
    strength_explanation: Optional[str] = None
    page_number: Optional[int] = None

class MultiClaimItem(BaseModel):
    claim_index: int
    claim_text: str
    content_type: str
    timestamp_start: Optional[str] = None
    timestamp_end: Optional[str] = None
    file_name: Optional[str] = None
    page_number: Optional[int] = None
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    extracted_excerpt: Optional[str] = None
    is_visual: bool = False
    verification_result: Optional[StructuredVerificationResult] = None

class EvidenceGraphNode(BaseModel):
    id: str
    type: str # INPUT, CLAIM, QUERY, SOURCE, DOCUMENT, CHUNK, EVIDENCE, CONFLICT, RESULT
    label: str
    metadata: Optional[Dict[str, Any]] = None

class EvidenceGraphEdge(BaseModel):
    source: str
    target: str
    relationship: str # EXTRACTED_FROM, SEARCHED_FOR, RETRIEVED_FROM, PART_OF, EVIDENCE_OF, RESOLVED_TO

class EvidenceGraphResponse(BaseModel):
    session_id: str
    nodes: List[EvidenceGraphNode]
    edges: List[EvidenceGraphEdge]

class ShareCardData(BaseModel):
    platform_name: str = "بيّنة AI"
    slogan: str = "تحقّق قبل أن تنشر."
    claim: str
    status: str
    status_slug: str
    evidence_excerpt: str
    source_name: str
    reference: str
    source_url: str
    verified_at: str

class VerificationResponse(BaseModel):
    claim_id: str
    session_id: Optional[str] = None
    input_type: Optional[str] = "TEXT"
    original_input: str
    extracted_claim: str
    content_type: str # hadith, ayah, tafsir, fiqh, aqeedah, seerah, dua, quote, fatwa, islamic_info, unspecified
    content_type_ar: str
    status: str
    status_slug: str
    confidence: float
    reason: str
    detailed_explanation: str
    checked_sources_count: int
    evidence: List[EvidenceItem]
    evidence_chain: List[VerificationStepLog]
    share_card: ShareCardData
    conflicts_found: Optional[bool] = False
    limitations: Optional[List[str]] = Field(default_factory=list)
    specialist_required: Optional[bool] = False
    url_metadata: Optional[Dict[str, Any]] = None
    media_metadata: Optional[Dict[str, Any]] = None
    video_analysis: Optional[Dict[str, Any]] = None
    latency_breakdown: Optional[Dict[str, float]] = None
    result_object: Optional[StructuredVerificationResult] = None
    multi_claims: Optional[List[MultiClaimItem]] = Field(default_factory=list)
    evidence_graph: Optional[EvidenceGraphResponse] = None
    source_coverage: Optional[Dict[str, Any]] = None
    is_demo: bool = False
    demo_case_id: Optional[str] = None

class AssistantMessage(BaseModel):
    role: str # user, assistant, system
    content: str

class AssistantQuestionRequest(BaseModel):
    claim_id: str
    session_id: Optional[str] = None
    question: str
    history: Optional[List[AssistantMessage]] = None
    verification_context: Optional[VerificationResponse] = None

class AssistantQuestionResponse(BaseModel):
    answer: str
    grounded_citations: List[str]
    avatar_state: str # idle, thinking, searching, evidence_found, explaining
    suggested_followups: List[str]

class SourceRegistryItem(BaseModel):
    id: str
    name: str
    author: Optional[str] = None
    organization: Optional[str] = None
    category: str
    source_type: str
    url: str
    license: str
    status: str
    description: str
    usage_policy: Optional[str] = None

class DemoCase(BaseModel):
    id: str
    title: str
    badge: str
    type: str
    input_text: str
    is_image_demo: Optional[bool] = False
    image_sample_url: Optional[str] = None
    description: str
    expected_status: str
    expected_slug: str
