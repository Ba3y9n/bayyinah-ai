import { 
  VerificationRequest, 
  VerificationResponse, 
  DemoCase, 
  TrustedSourceDetail,
  KnowledgeBaseStats,
  KnowledgeSearchResponse,
  SourceHealthItem,
  AssistantQuestionRequest, 
  AssistantQuestionResponse,
  AIHealthStatus
} from '../types';

const rawApiBase = import.meta.env.VITE_API_BASE_URL || '';
const API_BASE = rawApiBase ? `${rawApiBase.replace(/\/+$/, '')}/api` : '/api';

export const api = {
  async verifyContent(req: VerificationRequest): Promise<VerificationResponse> {
    const res = await fetch(`${API_BASE}/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'حدث خطأ في الاتصال بالنظام' }));
      throw new Error(err.detail || 'فشل في التحقق من المحتوى');
    }
    return res.json();
  },

  async verifyDemoCase(caseId: string): Promise<VerificationResponse> {
    const res = await fetch(`${API_BASE}/verify/demo/${caseId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'حدث خطأ أثناء تحميل مثال الاختبار' }));
      throw new Error(err.detail || 'فشل في تحميل مثال الاختبار');
    }
    return res.json();
  },

  async getDemoCases(): Promise<DemoCase[]> {
    const res = await fetch(`${API_BASE}/demo-cases`);
    if (!res.ok) {
      throw new Error('فشل في جلب حالات الاختبار');
    }
    return res.json();
  },

  async getSources(category: string = 'all'): Promise<TrustedSourceDetail[]> {
    const res = await fetch(`${API_BASE}/sources?category=${encodeURIComponent(category)}`);
    if (!res.ok) {
      throw new Error('فشل في جلب سجل المصادر المعتمدة');
    }
    return res.json();
  },

  async getSourceById(id: string): Promise<TrustedSourceDetail> {
    const res = await fetch(`${API_BASE}/sources/${encodeURIComponent(id)}`);
    if (!res.ok) {
      throw new Error('فشل في جلب تفاصيل المصدر');
    }
    return res.json();
  },

  async getSourcesHealth(): Promise<SourceHealthItem[]> {
    const res = await fetch(`${API_BASE}/sources/health`);
    if (!res.ok) {
      throw new Error('فشل في فحص صحة المصادر');
    }
    return res.json();
  },

  async getKnowledgeStats(): Promise<KnowledgeBaseStats> {
    const res = await fetch(`${API_BASE}/knowledge/stats`);
    if (!res.ok) {
      throw new Error('فشل في جلب إحصائيات قاعدة المعرفة');
    }
    return res.json();
  },

  async searchKnowledge(query: string, category: string = 'all', top_k: number = 5): Promise<KnowledgeSearchResponse> {
    const res = await fetch(`${API_BASE}/knowledge/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, category, top_k })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'فشل في استعلام قاعدة المعرفة' }));
      throw new Error(err.detail || 'فشل في استعلام قاعدة المعرفة');
    }
    return res.json();
  },

  async askAssistant(req: AssistantQuestionRequest): Promise<AssistantQuestionResponse> {
    const res = await fetch(`${API_BASE}/assistant/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'حدث خطأ أثناء إجابة المساعد' }));
      throw new Error(err.detail || 'فشل في التواصل مع مساعد بيّنة');
    }
    return res.json();
  },

  async verifyUrl(url: string, sourceType?: string): Promise<any> {
    const res = await fetch(`${API_BASE}/verify/url`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, source_type: sourceType })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'حدث خطأ أثناء فحص الرابط' }));
      throw new Error(err.detail || 'فشل في التحقق من الرابط');
    }
    return res.json();
  },

  async extractImageText(file: File): Promise<{ success: boolean; extracted_text: string; file_url?: string; error?: string }> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/verify/extract-image`, {
      method: 'POST',
      body: formData
    });
    const data = await res.json().catch(() => ({ success: false, error: 'فشل استخراج النص من الصورة' }));
    if (!res.ok) {
      throw new Error(data.error || data.detail || 'تعذر قراءة المحتوى بشكل موثوق.');
    }
    return data;
  },

  async verifyImage(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/verify/upload-image`, {
      method: 'POST',
      body: formData
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'فشل في تحليل الصورة المرفوعة' }));
      throw new Error(err.detail || 'فشل في تحليل الصورة');
    }
    return res.json();
  },

  async verifyVideo(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/verify/video`, {
      method: 'POST',
      body: formData
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'فشل في تحليل الفيديو' }));
      throw new Error(err.detail || 'فشل في تحليل الفيديو');
    }
    return res.json();
  },

  async verifyPdf(file: File): Promise<VerificationResponse> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/verify/pdf`, {
      method: 'POST',
      body: formData
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'فشل في التحقق من وثيقة PDF المرفوعة' }));
      throw new Error(err.detail || 'فشل في تحليل وثيقة PDF');
    }
    return res.json();
  },

  async extractPdfText(file: File): Promise<{ success: boolean; filename: string; total_pages: number; pages: any[] }> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/verify/extract-pdf`, {
      method: 'POST',
      body: formData
    });
    const data = await res.json().catch(() => ({ success: false, error: 'فشل استخراج النصوص من وثيقة PDF' }));
    if (!res.ok) {
      throw new Error(data.detail || data.error || 'فشل في قراءة ملف PDF');
    }
    return data;
  },

  async getSystemHealth(): Promise<any> {
    const res = await fetch(`${API_BASE}/system/health`);
    if (!res.ok) {
      throw new Error('فشل في جلب الفحص الشامل للنظام');
    }
    return res.json();
  },

  async getAiHealth(): Promise<AIHealthStatus> {
    const res = await fetch(`${API_BASE}/health/ai`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'فشل في فحص اتصال الذكاء الاصطناعي' }));
      throw new Error(err.detail || 'فشل في فحص اتصال الذكاء الاصطناعي');
    }
    return res.json();
  }
};
