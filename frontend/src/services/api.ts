import { 
  VerificationRequest, 
  VerificationResponse, 
  DemoCase, 
  SourceRegistryItem, 
  AssistantQuestionRequest, 
  AssistantQuestionResponse 
} from '../types';

const API_BASE = '/api';

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

  async getSources(category: string = 'all'): Promise<SourceRegistryItem[]> {
    const res = await fetch(`${API_BASE}/sources?category=${encodeURIComponent(category)}`);
    if (!res.ok) {
      throw new Error('فشل في جلب سجل المصادر');
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
  }
};
