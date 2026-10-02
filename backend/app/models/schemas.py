from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Verification Status Types as specified
# - ثابت بحسب المصدر
# - لم يثبت بهذا اللفظ
# - لم نجد دليلًا كافيًا
# - اختلاف في المصادر
# - يحتاج مراجعة مختص
# - ضعيف بحسب المصدر
# - موضوع/مكذوب بحسب المصدر

class VerificationRequest(BaseModel):
    text: Optional[str] = Field(None, description="Input text to verify")
    image_base64: Optional[str] = Field(None, description="Base64 encoded image or data URL for multimodal analysis")
    content_type_hint: Optional[str] = Field("auto", description="Optional hint for content type")

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
    is_demo: bool = False

class AssistantMessage(BaseModel):
    role: str # user, assistant, system
    content: str

class AssistantQuestionRequest(BaseModel):
    claim_id: str
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
