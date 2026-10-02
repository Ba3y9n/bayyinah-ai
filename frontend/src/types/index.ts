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
  evidence_type: 'direct_match' | 'partial_match' | 'conflicting_view' | 'scholarly_commentary' | 'not_found';
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
  is_demo?: boolean;
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

export interface SourceRegistryItem {
  id: string;
  name: string;
  author?: string;
  organization?: string;
  category: string;
  source_type: string;
  url: string;
  license: string;
  status: string;
  description: string;
  usage_policy?: string;
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
