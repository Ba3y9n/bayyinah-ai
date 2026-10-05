import React, { useState } from 'react';
import { 
  Send, 
  BookOpen, 
  ShieldCheck, 
  AlertCircle, 
  HelpCircle, 
  Layers, 
  ExternalLink,
  MessageSquare,
  Sparkles,
  Loader2
} from 'lucide-react';
import { VerificationResponse } from '../types';
import { api } from '../services/api';

interface HelpPageProps {
  initialClaim?: string;
  initialResult?: VerificationResponse | null;
}

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  grounded: boolean;
  citations?: Array<{ source_name: string; reference: string; url?: string }>;
}

export const HelpPage: React.FC<HelpPageProps> = ({ 
  initialClaim, 
  initialResult 
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'init-1',
      role: 'assistant',
      content: initialResult 
        ? `أهلاً بك في مساعدة بيّنة. لقد قمت بربط جلستنا بنتيجة التحقق الخاصة بـ: «${initialResult.extracted_claim || initialClaim}». يمكنك سؤالي عن الدليل، أو المصادر المعتمدة، أو أسباب اعتماد هذه النتيجة.`
        : 'أهلاً بك في مساعدة بيّنة الموثقة. لستُ روبوت محادثة عاماً، وإنما مساعد متخصص لشرح وتتبع الأدلة المسترجعة من المصادر الإسلامية المعتمدة وتوضيح معاني الحالات المعتمدة. كيف أساعدك؟',
      grounded: true,
      citations: initialResult?.evidence?.map(e => ({
        source_name: e.source_name,
        reference: e.reference,
        url: e.url
      }))
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const suggestedQuestions = [
    "لماذا ظهرت هذه النتيجة؟",
    "ما الدليل المستخدم في التحقق؟",
    "ما مصدر هذا النص بالتحديد؟",
    "هل توجد مصادر أخرى تناولت هذا اللفظ؟",
    "ماذا يعني تصنيف 'لم يثبت بهذا اللفظ'؟",
    "هل توجد اختلافات بين المصادر في هذه المسألة؟"
  ];

  const handleSendMessage = async (textToSend?: string) => {
    const q = (textToSend || inputMessage).trim();
    if (!q || isLoading) return;

    const userMsg: ChatMessage = {
      id: `usr-${Date.now()}`,
      role: 'user',
      content: q,
      grounded: false
    };

    setMessages(prev => [...prev, userMsg]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const resp = await api.askAssistant({
        claim_id: initialResult?.claim_id || "general-inquiry",
        question: q,
        history: messages.map(m => ({ role: m.role, content: m.content })),
        verification_context: initialResult || undefined
      });

      const assistantMsg: ChatMessage = {
        id: `asst-${Date.now()}`,
        role: 'assistant',
        content: resp.answer || "لا أملك دليلاً كافياً في المصادر التي تم فحصها للإجابة عن ذلك.",
        grounded: (resp.grounded_citations && resp.grounded_citations.length > 0) || false,
        citations: (resp.grounded_citations || []).map((c: string) => ({
          source_name: "مصدر معتمد",
          reference: c,
          url: ""
        }))
      };

      setMessages(prev => [...prev, assistantMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        role: 'assistant',
        content: "تعذر الاتصال بمحرك التحقق حالياً. يرجى المحاولة بعد قليل.",
        grounded: false
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 min-h-[85vh]">
      {/* Header */}
      <div className="flex items-center gap-4 mb-8 pb-6 border-b border-gray-100">
        {/* Logo circle icon - NOT a giant human avatar (Rule 52) */}
        <div className="w-12 h-12 rounded-full bg-bayyinah-emerald/10 border border-bayyinah-emerald/30 flex items-center justify-center text-bayyinah-emerald shrink-0">
          <ShieldCheck className="w-6 h-6" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-bayyinah-deep-emerald">مساعدة بيّنة الذكية</h1>
          <p className="text-xs text-bayyinah-secondary-text">
            نظام أسئلة وتفسير مقيد بالأدلة الموثقة (Evidence-Bound Assistance)
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Main Conversation Column (2 Cols) */}
        <div className="lg:col-span-2 flex flex-col bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden h-[680px]">
          
          {/* Chat Messages Log */}
          <div className="flex-1 p-6 overflow-y-auto space-y-6">
            {messages.map((msg) => (
              <div 
                key={msg.id}
                className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {msg.role === 'assistant' && (
                  <div className="w-8 h-8 rounded-full bg-bayyinah-ivory border border-bayyinah-emerald/30 flex items-center justify-center text-bayyinah-emerald shrink-0 mt-1">
                    <ShieldCheck className="w-4 h-4" />
                  </div>
                )}

                <div className={`max-w-[85%] rounded-2xl p-5 ${
                  msg.role === 'user' 
                    ? 'bg-bayyinah-emerald text-white font-medium' 
                    : 'bg-bayyinah-ivory/70 border border-gray-100 text-bayyinah-dark-text'
                }`}>
                  <p className="text-sm md:text-base leading-relaxed whitespace-pre-wrap">{msg.content}</p>

                  {/* Citations on assistant responses */}
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="mt-4 pt-3 border-t border-gray-200/50 space-y-1.5 text-xs">
                      <span className="font-bold text-bayyinah-emerald block">المراجع المستند إليها:</span>
                      {msg.citations.map((c, i) => (
                        <div key={i} className="flex items-center gap-1.5 text-bayyinah-secondary-text">
                          <BookOpen className="w-3 h-3 text-bayyinah-emerald" />
                          <span>{c.source_name} ({c.reference})</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex gap-3 justify-start">
                <div className="w-8 h-8 rounded-full bg-bayyinah-ivory border border-bayyinah-emerald/30 flex items-center justify-center text-bayyinah-emerald shrink-0 mt-1">
                  <Loader2 className="w-4 h-4 animate-spin" />
                </div>
                <div className="bg-bayyinah-ivory rounded-2xl p-4 text-xs text-bayyinah-secondary-text flex items-center gap-2">
                  <span>جاري مراجعة الأدلة وصياغة الشرح الموثق...</span>
                </div>
              </div>
            )}
          </div>

          {/* Suggested quick questions */}
          <div className="p-4 bg-gray-50 border-t border-gray-100 overflow-x-auto hide-scrollbar flex gap-2">
            {suggestedQuestions.map((q, idx) => (
              <button 
                key={idx}
                onClick={() => handleSendMessage(q)}
                className="whitespace-nowrap px-3.5 py-1.5 rounded-xl bg-white border border-gray-200 hover:border-bayyinah-emerald text-xs text-bayyinah-dark-text transition-colors cursor-pointer shrink-0 shadow-2xs"
              >
                {q}
              </button>
            ))}
          </div>

          {/* Input Bar */}
          <div className="p-4 bg-white border-t border-gray-100 flex gap-3">
            <input 
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="اطرح سؤالك حول الدليل أو النتيجة أو المصادر المعتمدة..."
              className="flex-1 bg-gray-50 border border-gray-200 rounded-2xl px-5 py-3 text-sm focus:outline-none focus:border-bayyinah-emerald focus:ring-1 focus:ring-bayyinah-emerald"
            />
            <button 
              onClick={() => handleSendMessage()}
              disabled={!inputMessage.trim() || isLoading}
              className="bg-bayyinah-emerald hover:bg-bayyinah-deep-emerald disabled:opacity-40 text-white p-3.5 rounded-2xl transition-colors cursor-pointer"
            >
              <Send className="w-4 h-4 -rotate-90" />
            </button>
          </div>
        </div>

        {/* Evidence Side Panel (Rule 52) */}
        <div className="bg-white rounded-3xl border border-gray-100 shadow-sm p-6 flex flex-col justify-between h-[680px] overflow-y-auto">
          <div>
            <div className="flex items-center gap-2 pb-4 mb-4 border-b border-gray-100 text-bayyinah-dark-text font-bold text-sm">
              <Layers className="w-4 h-4 text-bayyinah-emerald" />
              <span>لوحة الأدلة المرتبطة بالجلسة</span>
            </div>

            {initialResult ? (
              <div className="space-y-4">
                <div>
                  <span className="block text-xs text-bayyinah-secondary-text mb-1">الادعاء المفحوص:</span>
                  <p className="text-sm font-bold text-bayyinah-dark-text bg-bayyinah-ivory/80 p-3 rounded-xl border border-gray-100">
                    {initialResult.extracted_claim}
                  </p>
                </div>

                <div>
                  <span className="block text-xs text-bayyinah-secondary-text mb-1">الحالة المعتمدة:</span>
                  <span className="inline-block px-3 py-1 rounded-lg bg-bayyinah-emerald/10 text-bayyinah-emerald font-bold text-xs">
                    {initialResult.status}
                  </span>
                </div>

                <div>
                  <span className="block text-xs text-bayyinah-secondary-text mb-2">الأدلة المرفقة:</span>
                  <div className="space-y-3">
                    {initialResult.evidence?.slice(0, 3).map((ev, i) => (
                      <div key={i} className="p-3 rounded-xl border border-gray-100 bg-gray-50/70 text-xs">
                        <strong className="block text-bayyinah-emerald mb-1">{ev.source_name}</strong>
                        <p className="text-gray-700 line-clamp-3 mb-2 font-normal">«{ev.excerpt}»</p>
                        <span className="text-gray-400 block">{ev.reference}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-16 px-4">
                <BookOpen className="w-10 h-10 text-gray-300 mx-auto mb-3" />
                <h4 className="font-bold text-sm text-bayyinah-dark-text mb-1">لم يتم ربط نتيجة محددة</h4>
                <p className="text-xs text-bayyinah-secondary-text leading-relaxed">
                  عند الدخول من صفحة التحقق بعد فحص أي نص، ستظهر هنا وثائق الأدلة والمصادر المفحوصة تلقائياً.
                </p>
              </div>
            )}
          </div>

          <div className="p-4 rounded-2xl bg-bayyinah-ivory border border-bayyinah-emerald/20 text-[11px] text-bayyinah-secondary-text leading-relaxed">
            <strong className="text-bayyinah-deep-emerald block mb-1">ضمان الأمانة العلمية:</strong>
            يرفض مساعد بيّنة اختراع أحاديث أو أحكام من ذاكرته، ويقصر كل إجابة على الأدلة المسترجعة من المصادر الـ 11 المعتمدة فقط.
          </div>
        </div>

      </div>
    </div>
  );
};
