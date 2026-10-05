import React, { useState } from 'react';
import { Send, Sparkles, MessageSquare, Info, CheckCircle2 } from 'lucide-react';
import { VerificationResponse, AssistantQuestionResponse } from '../types';
import { AvatarAssistant } from './AvatarAssistant';
import { api } from '../services/api';

interface GroundedChatProps {
  verificationContext: VerificationResponse;
}

interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  citations?: string[];
}

export const GroundedChat: React.FC<GroundedChatProps> = ({ verificationContext }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'assistant',
      text: `مرحبًا بك. أنا مساعد بيّنة لشرح أدلة التحقق. يمكنك سؤالي عن مصدر هذا الادعاء أو الدليل المعتمد أو سبب التقييم. أعتمد حصرًا على الأدلة الموثقة المسترجعة ولا أفتي أو أصدر أحكامًا خاصة.`
    }
  ]);
  const [inputQuestion, setInputQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [avatarState, setAvatarState] = useState<'idle' | 'thinking' | 'searching' | 'evidence_found' | 'explaining'>('idle');

  const defaultSuggestions = [
    'ما المصدر؟',
    'أين الدليل؟',
    'لماذا ظهرت هذه النتيجة؟',
    'هل توجد مصادر مختلفة؟'
  ];

  const handleAsk = async (questionText: string) => {
    if (!questionText.trim() || loading) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: questionText
    };

    setMessages(prev => [...prev, userMsg]);
    setInputQuestion('');
    setLoading(true);
    setAvatarState('thinking');

    try {
      setTimeout(() => setAvatarState('searching'), 300);

      const response: AssistantQuestionResponse = await api.askAssistant({
        claim_id: verificationContext.claim_id,
        question: questionText,
        verification_context: verificationContext
      });

      setAvatarState(response.avatar_state || 'explaining');

      const assistantMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: response.answer,
        citations: response.grounded_citations
      };

      setMessages(prev => [...prev, assistantMsg]);
      setTimeout(() => setAvatarState('idle'), 4000);
    } catch (err: any) {
      setAvatarState('idle');
      setMessages(prev => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: 'assistant',
          text: 'عذرًا، حدث خطأ أثناء فحص الأدلة المسترجعة. يرجى المحاولة لاحقًا.'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-3xl border border-bayyinah-gray-200 shadow-subtle overflow-hidden flex flex-col h-[560px]">
      {/* Assistant Header */}
      <div className="p-4 md:p-5 bg-gradient-to-r from-bayyinah-navy to-bayyinah-navy-light text-white flex items-center justify-between">
        <div className="flex items-center gap-3">
          <AvatarAssistant state={avatarState} size="md" />
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              مساعد بيّنة
              <span className="text-[10px] font-normal px-2 py-0.5 bg-bayyinah-purple/40 text-bayyinah-off-white rounded-full border border-bayyinah-purple/50">
                مرتبط بالأدلة فقط
              </span>
            </h3>
            <p className="text-xs text-bayyinah-off-white/70 mt-0.5">
              شرح وتوضيح نتيجة التحقق من واقع المراجع المفحوصة
            </p>
          </div>
        </div>
      </div>

      {/* Safety Notice Banner */}
      <div className="bg-bayyinah-off-white px-4 py-2 border-b border-bayyinah-gray-200 flex items-center gap-2 text-[11px] text-bayyinah-gray-600">
        <Info className="w-3.5 h-3.5 text-bayyinah-purple flex-shrink-0" />
        <span>تنبيه أمان: مساعد بيّنة ليس شيخًا أو مفتيًا ولا يضيف أي معلومة دينية غير مسترجعة من الأدلة.</span>
      </div>

      {/* Chat Messages List */}
      <div className="flex-1 p-4 md:p-5 overflow-y-auto space-y-4">
        {messages.map(msg => (
          <div
            key={msg.id}
            className={`flex flex-col ${msg.sender === 'user' ? 'items-start' : 'items-end'}`}
          >
            <div
              className={`max-w-[85%] rounded-2xl p-4 text-sm leading-relaxed ${
                msg.sender === 'user'
                  ? 'bg-bayyinah-purple text-white rounded-tr-none'
                  : 'bg-bayyinah-off-white text-bayyinah-navy border border-bayyinah-gray-200 rounded-tl-none'
              }`}
            >
              <div className="whitespace-pre-wrap">{msg.text}</div>

              {msg.citations && msg.citations.length > 0 && (
                <div className="mt-3 pt-2.5 border-t border-bayyinah-gray-300/60 text-xs text-bayyinah-gray-600 space-y-1">
                  <span className="font-semibold text-[11px] text-bayyinah-purple block">المراجع المستند إليها:</span>
                  {msg.citations.map((c, idx) => (
                    <div key={idx} className="flex items-center gap-1.5 text-[11px]">
                      <CheckCircle2 className="w-3 h-3 text-emerald-600 flex-shrink-0" />
                      <span>{c}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
            <span className="text-[10px] text-bayyinah-gray-400 mt-1 px-1">
              {msg.sender === 'user' ? 'أنت' : 'مساعد بيّنة'}
            </span>
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-2 text-xs text-bayyinah-gray-500 bg-bayyinah-off-white p-3 rounded-xl max-w-[60%] animate-pulse">
            <Sparkles className="w-4 h-4 text-bayyinah-purple animate-spin" />
            <span>جاري مطابقة السؤال مع الأدلة المسترجعة...</span>
          </div>
        )}
      </div>

      {/* Suggested Quick Questions */}
      <div className="p-3 bg-bayyinah-gray-50 border-t border-bayyinah-gray-200 overflow-x-auto">
        <div className="flex items-center gap-2 whitespace-nowrap">
          <span className="text-[11px] font-semibold text-bayyinah-gray-500 flex-shrink-0">أسئلة مقترحة:</span>
          {defaultSuggestions.map((sug, i) => (
            <button
              key={i}
              onClick={() => handleAsk(sug)}
              disabled={loading}
              className="text-xs bg-white hover:bg-bayyinah-purple-light hover:text-bayyinah-purple text-bayyinah-navy border border-bayyinah-gray-200 px-3 py-1 rounded-full transition-colors disabled:opacity-50"
            >
              {sug}
            </button>
          ))}
        </div>
      </div>

      {/* Question Input Form */}
      <form
        onSubmit={e => {
          e.preventDefault();
          handleAsk(inputQuestion);
        }}
        className="p-3 md:p-4 bg-white border-t border-bayyinah-gray-200 flex items-center gap-2"
      >
        <input
          type="text"
          value={inputQuestion}
          onChange={e => setInputQuestion(e.target.value)}
          placeholder="اسأل مساعد بيّنة عن الأدلة والمصادر..."
          disabled={loading}
          className="flex-1 bg-bayyinah-off-white border border-bayyinah-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-bayyinah-purple focus:bg-white transition-all text-bayyinah-navy placeholder:text-bayyinah-gray-400"
        />
        <button
          type="submit"
          disabled={!inputQuestion.trim() || loading}
          className="bg-bayyinah-purple hover:bg-bayyinah-purple-hover text-white p-2.5 rounded-xl transition-all disabled:opacity-40 flex-shrink-0"
        >
          <Send className="w-4 h-4 transform rotate-180" />
        </button>
      </form>
    </div>
  );
};
