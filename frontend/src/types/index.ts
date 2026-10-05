export type VerificationStatusType = 
  | 'ثابت بحسب المصدر'
  | 'لم يثبت بهذا اللفظ'
  | 'لم نجد دليلًا كافيًا'
  | 'اختلاف في المصادر'
  | 'يحتاج مراجعة مختص'
  | 'ضعيف بحسب المصدر'
  | 'موضوع/مكذوب بحسب المصدر';

export type StatusSlug = 
  | 'verified_authentic'
  | 'unverified_wording'
  | 'insufficient_evidence'
  | 'scholarly_disagreement'
  | 'needs_specialist'
  | 'weak_per_source'
  | 'fabricated_per_source';

export interface VerificationStepLog {
  step_number: number;
  title: string;
  description: string;
  status: 'completed' | 'in_progress' | 'pending' | 'failed';
  data?: Record<string, any>;
}

export interface EvidenceItem {
  document_id: string;
  source_id: string;
  source_name: string;
  author?: string;
  organization?: string;
  category: string;
  title: string;
  excerpt: string;
  reference: string;
  url: string;
  license: string;
  relevance_score: number;
  evidence_type: 'direct_match' | 'partial_match' | 'conflicting_view' | 'scholarly_commentary' | 'not_found' | string;
  comparison_notes?: string;
  ruling_or_grade?: string;
}

export interface ShareCardData {
  platform_name: string;
  slogan: string;
  claim: string;
  status: string;
  status_slug: string;
  evidence_excerpt: string;
  source_name: string;
  reference: string;
  source_url: string;
  verified_at: string;
}

export interface VerificationResponse {
  claim_id: string;
  original_input: string;
  extracted_claim: string;
  content_type: string;
  content_type_ar: string;
  status: VerificationStatusType;
  status_slug: StatusSlug;
  confidence: number;
  reason: string;
  detailed_explanation: string;
  checked_sources_count: number;
  evidence: EvidenceItem[];
  evidence_chain: VerificationStepLog[];
  share_card: ShareCardData;
  latency_breakdown?: Record<string, number>;
  is_demo?: boolean;
  session_id?: string;
  input_type?: 'TEXT' | 'URL' | 'IMAGE' | 'VIDEO' | string;
  result_object?: StructuredVerificationResult;
  multi_claims?: MultiClaimItem[];
  evidence_graph?: EvidenceGraphResponse;
  conflicts_found?: boolean;
  limitations?: string[];
  specialist_required?: boolean;
  url_metadata?: {
    platform?: string;
    title?: string;
    description?: string;
    author?: string;
    thumbnail_url?: string;
    extracted_text?: string;
    raw_url?: string;
  };
  media_metadata?: {
    file_url?: string;
    original_filename?: string;
    extracted_text?: string;
    confidence?: number;
    provenance_type?: string;
    platform?: string;
    video_id?: string;
    video_title?: string;
    channel_title?: string;
    canonical_url?: string;
    acquisition_method?: string;
    timestamps?: Array<{ start: string; end: string; text: string; claim?: string }>;
  };
}

export interface MultiClaimItem {
  claim_index: number;
  claim_text: string;
  content_type: string;
  timestamp_start?: string;
  timestamp_end?: string;
  is_visual?: boolean;
}

export interface EvidenceGraphNode {
  id: string;
  type: string;
  label: string;
  metadata?: Record<string, any>;
}

export interface EvidenceGraphEdge {
  source: string;
  target: string;
  relationship: string;
}

export interface EvidenceGraphResponse {
  session_id: string;
  nodes: EvidenceGraphNode[];
  edges: EvidenceGraphEdge[];
}

export interface StructuredVerificationResult {
  status: string;
  label_ar: string;
  claim: string;
  reason: string;
  evidence_ids: string[];
  source_ids: string[];
  citations: string[];
  conflict_status: string;
  grounding_status: string;
  abstained: boolean;
  specialist_required: boolean;
}

export interface VerificationRequest {
  text?: string;
  image_base64?: string;
  content_type_hint?: string;
}

export interface DemoCase {
  id: string;
  title: string;
  badge: string;
  type: string;
  input_text: string;
  is_image_demo?: boolean;
  image_sample_url?: string;
  description: string;
  expected_status: string;
  expected_slug: string;
}

// Trusted Knowledge Base Schemas
export interface ProvenanceInfo {
  source_id: string;
  source_name: string;
  document_id: string;
  document_title: string;
  chunk_id: string;
  locator: string;
  url: string;
  content_hash: string;
  retrieved_at: string;
}

export interface TrustedSourceDetail {
  id: string;
  name_ar: string;
  name_en: string;
  slug: string;
  category: string;
  description: string;
  official_url: string;
  base_domain: string;
  source_type: string;
  authority_level: string;
  trust_status: 'APPROVED' | 'REVIEW_REQUIRED' | 'RESTRICTED' | 'DISABLED';
  usage_status: string;
  license_status: 'VERIFIED' | 'PENDING_VERIFICATION' | 'RESTRICTED' | 'UNKNOWN' | 'NOT_APPLICABLE';
  license_name?: string;
  license_url?: string;
  copyright_holder?: string;
  allowed_operations: Record<string, boolean>;
  content_scope?: string;
  language: string;
  publisher?: string;
  author?: string;
  country?: string;
  verification_method: string;
  verification_notes?: string;
  last_verified_at?: string;
  verified_by?: string;
  is_active: boolean;
  documents_count: number;
  chunks_count: number;
}

export interface SourceHealthItem {
  source_id: string;
  source_name: string;
  status: 'healthy' | 'warning' | 'failed';
  url_accessible: boolean;
  metadata_complete: boolean;
  license_status: string;
  trust_status: string;
  documents_count: number;
  chunks_count: number;
  missing_items: string[];
}

export interface KnowledgeBaseStats {
  total_sources: number;
  active_sources: number;
  sources_by_category: Record<string, number>;
  sources_by_trust: Record<string, number>;
  sources_by_license: Record<string, number>;
  total_documents: number;
  total_chunks: number;
  total_terms: number;
  total_evidence?: number;
  total_verifications?: number;
  total_insufficient?: number;
  total_conflicts?: number;
  evidence_count?: number;
  verifications_count?: number;
  insufficient_count?: number;
  conflict_count?: number;
  sources_needing_review: number;
  last_verified?: string;
}

export interface KnowledgeSearchResultItem {
  source: {
    id: string;
    name_ar: string;
    name_en: string;
    category: string;
    official_url: string;
    trust_status: string;
    license_status: string;
    authority_level: string;
  };
  document: {
    id: string;
    title_ar: string;
    category: string;
    official_url: string;
    author?: string;
    publisher?: string;
  };
  chunk: {
    id: string;
    content: string;
    source_locator: string;
    canonical_url: string;
    verse_reference?: string;
    hadith_reference?: string;
    content_hash: string;
  };
  scores: {
    exact: number;
    keyword: number;
    semantic: number;
    rrf: number;
    relevance: number;
  };
  provenance: ProvenanceInfo;
  support_level: string;
  attribution_status: string;
  verification_status: string;
}

export interface KnowledgeSearchResponse {
  query: string;
  category_filter?: string;
  total_candidates: number;
  results: KnowledgeSearchResultItem[];
  latency_ms: number;
}

export interface AssistantQuestionRequest {
  claim_id: string;
  question: string;
  history?: Array<{ role: string; content: string }>;
  verification_context?: VerificationResponse;
}

export interface AssistantQuestionResponse {
  answer: string;
  grounded_citations: string[];
  avatar_state: 'idle' | 'thinking' | 'searching' | 'evidence_found' | 'explaining';
  suggested_followups: string[];
}

// For backward compatibility
export type SourceRegistryItem = TrustedSourceDetail;

export interface AIHealthStatus {
  provider: string;
  connected: boolean;
  model: string;
  actual_request_model: string;
  api_key_configured: boolean;
  sdk: string;
  sdk_version?: string;
  multimodal: boolean;
  structured_output: boolean;
  function_calling: boolean;
  latency_ms: number;
  last_check: string;
  test_response?: string;
  error?: string | null;
}
