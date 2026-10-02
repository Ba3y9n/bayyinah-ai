import React, { useState } from 'react';
import { 
  ShieldCheck, 
  ExternalLink, 
  BookOpen, 
  Share2, 
  MessageSquare, 
  Search, 
  CheckCircle2, 
  Layers, 
  AlertTriangle,
  FileText,
  Building,
  Scale,
  Sparkles,
  ArrowRight,
  HelpCircle,
  Copy,
  Check
} from 'lucide-react';
import { VerificationResponse } from '../types';
import { ResultBadge } from '../components/ResultBadge';
import { VerificationTimeline } from '../components/VerificationTimeline';
import { ShareCard } from '../components/ShareCard';
import { GroundedChat } from '../components/GroundedChat';

interface ResultPageProps {
  result: VerificationResponse;
  onNewVerification: () => void;
}

export const ResultPage: React.FC<ResultPageProps> = ({
  result,
  onNewVerification
}) => {
  const [showShareModal, setShowShareModal] = useState(false);
  const [showChatModal, setShowChatModal] = useState(false);
  const [copiedLink, setCopiedLink] = useState(false);

  const handleCopyClaim = () => {
    navigator.clipboard.writeText(result.extracted_claim);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2000);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-10 space-y-10">
      {/* Top Header Actions */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-bayyinah-gray-200">
        <button
          onClick={onNewVerification}
          className="inline-flex items-center gap-2 text-xs font-semibold text-bayyinah-purple hover:text-bayyinah-purple-hover bg-bayyinah-purple-light/70 px-4 py-2 rounded-xl transition-all"
        >
          <Search className="w-4 h-4" />
          <span>فحص محتوى جديد</span>
        </button>

        <div className="flex items-center gap-3">
          {result.is_demo && (
            <span className="text-xs bg-amber-50 text-amber-800 border border-amber-200 px-3 py-1 rounded-full font-medium">
              مثال تجريبي
            </span>
          )}

          <button
            onClick={() => setShowShareModal(true)}
            className="inline-flex items-center gap-2 bg-bayyinah-navy hover:bg-bayyinah-navy-light text-white text-xs font-semibold py-2 px-4 rounded-xl transition-all shadow-subtle"
          >
            <Share2 className="w-3.5 h-3.5 text-bayyinah-turquoise" />
            <span>إنشاء بطاقة بيّنة</span>
          </button>
        </div>
      </div>

      {/* Main Result Card */}
      <div className="bg-white rounded-3xl p-6 md:p-10 border border-bayyinah-gray-200 shadow-elevated space-y-8">
        {/* Verification Status Header */}
        <div className="space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <span className="text-xs font-semibold text-bayyinah-gray-500">نتيجة فحص المحتوى:</span>
            <span className="text-xs bg-bayyinah-off-white text-bayyinah-navy border border-bayyinah-gray-200 px-3 py-1 rounded-full">
              تم فحص {result.checked_sources_count} مصدر معتمد
            </span>
          </div>

          <div>
            <ResultBadge status={result.status} statusSlug={result.status_slug} size="lg" />
          </div>

          <p className="text-base md:text-lg font-bold text-bayyinah-navy leading-snug">
            {result.reason}
          </p>
        </div>

        {/* Claim Box */}
        <div className="bg-bayyinah-off-white rounded-2xl p-5 border border-bayyinah-gray-200 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-bayyinah-purple">
              الادعاء الذي تم التحقق منه: ({result.content_type_ar})
            </span>
            <button
              onClick={handleCopyClaim}
              className="text-[11px] text-bayyinah-gray-500 hover:text-bayyinah-navy inline-flex items-center gap-1"
            >
              {copiedLink ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copiedLink ? 'تم النسخ' : 'نسخ الادعاء'}</span>
            </button>
          </div>
          <p className="text-sm md:text-base font-medium text-bayyinah-navy leading-relaxed">
            «{result.extracted_claim}»
          </p>
        </div>

        {/* Detailed Explanation */}
        <div className="space-y-2">
          <h3 className="text-sm font-semibold text-bayyinah-navy flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-bayyinah-purple" />
            ملخص النتيجة والشرح الموثق:
          </h3>
          <p className="text-sm text-bayyinah-gray-700 leading-relaxed bg-white p-4 rounded-2xl border border-bayyinah-gray-200/80">
            {result.detailed_explanation}
          </p>
        </div>

        {/* Evidence & Sources List */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-bayyinah-navy flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-bayyinah-purple" />
              الأدلة والمصادر المسترجعة ({result.evidence.length})
            </h3>
            <span className="text-xs text-bayyinah-gray-500">مسترجعة عبر محرك Hybrid Search</span>
          </div>

          {result.evidence.length === 0 ? (
            <div className="p-6 bg-slate-50 border border-slate-200 rounded-2xl text-center text-xs text-slate-600">
              لم نعثر على أدلة مسندة مطابقة لهذا الادعاء في سجل المصادر المفحوصة.
            </div>
          ) : (
            <div className="space-y-4">
              {result.evidence.map((ev, index) => (
                <div
                  key={ev.document_id || index}
                  className="bg-white rounded-2xl p-5 md:p-6 border border-bayyinah-gray-200 hover:border-bayyinah-purple/40 hover:shadow-subtle transition-all space-y-4"
                >
                  {/* Evidence Source Header */}
                  <div className="flex flex-wrap items-start justify-between gap-3 pb-3 border-b border-bayyinah-gray-100">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-bold text-bayyinah-navy">{ev.source_name}</span>
                        {ev.ruling_or_grade && (
                          <span className="text-[11px] font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 px-2.5 py-0.5 rounded-full">
                            {ev.ruling_or_grade}
                          </span>
                        )}
                      </div>
                      {ev.author && (
                        <span className="text-xs text-bayyinah-gray-500 block mt-0.5">
                          المؤلف/المحقق: {ev.author}
                        </span>
                      )}
                    </div>

                    <a
                      href={ev.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1.5 text-xs font-semibold text-bayyinah-purple hover:underline bg-bayyinah-purple-light/50 px-3 py-1 rounded-xl"
                    >
                      <span>زيارة المصدر الأصلي</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  </div>

                  {/* Excerpt */}
                  <div className="bg-bayyinah-off-white/80 rounded-xl p-4 border border-bayyinah-gray-200/60">
                    <span className="text-[11px] font-semibold text-bayyinah-purple block mb-1">
                      نص الدليل المعتمد:
                    </span>
                    <p className="text-xs md:text-sm text-bayyinah-navy leading-relaxed font-sans italic">
                      {ev.excerpt}
                    </p>
                  </div>

                  {/* Reference & License */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs text-bayyinah-gray-600 pt-1">
                    <div>
                      <strong className="text-bayyinah-navy">المرجع والتخريج: </strong>
                      <span>{ev.reference}</span>
                    </div>
                    <div>
                      <strong className="text-bayyinah-navy">حقوق الاستخدام: </strong>
                      <span>{ev.license}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Evidence Chain Transparency */}
        <div className="pt-2">
          <VerificationTimeline steps={result.evidence_chain} defaultOpen={false} />
        </div>

        {/* Interactive Assistant Trigger */}
        <div className="bg-gradient-to-r from-bayyinah-navy to-bayyinah-navy-light text-white rounded-3xl p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-5 h-5 text-bayyinah-turquoise" />
              <h3 className="text-lg font-bold">هل لديك سؤال حول هذه النتيجة؟</h3>
            </div>
            <p className="text-xs md:text-sm text-bayyinah-off-white/80 max-w-xl leading-relaxed">
              اسأل «مساعد بيّنة» لشرح تفاصيل الدليل، أو إبراز المراجع الأخرى، أو توضيح سبب إصدار هذا التقييم بناءً على الأدلة المسترجعة فقط.
            </p>
          </div>

          <button
            onClick={() => setShowChatModal(!showChatModal)}
            className="inline-flex items-center gap-2 bg-bayyinah-turquoise hover:bg-bayyinah-turquoise-dark text-bayyinah-navy text-sm font-bold py-3.5 px-7 rounded-xl transition-all shadow-subtle whitespace-nowrap"
          >
            <MessageSquare className="w-4 h-4" />
            <span>{showChatModal ? 'إخفاء مساعد بيّنة' : 'اسأل بيّنة'}</span>
          </button>
        </div>

        {/* Inline Grounded Assistant Chat (toggleable) */}
        {showChatModal && (
          <div className="pt-2">
            <GroundedChat verificationContext={result} />
          </div>
        )}
      </div>

      {/* Share Card Modal */}
      {showShareModal && (
        <div className="fixed inset-0 z-50 bg-bayyinah-navy/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-2xl w-full p-6 md:p-8 space-y-6 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between pb-3 border-b border-bayyinah-gray-200">
              <h3 className="text-lg font-bold text-bayyinah-navy">بطاقة تحقق بيّنة AI</h3>
              <button
                onClick={() => setShowShareModal(false)}
                className="text-xs font-semibold text-bayyinah-gray-500 hover:text-bayyinah-navy p-1.5"
              >
                إغلاق
              </button>
            </div>

            <ShareCard data={result.share_card} />
          </div>
        </div>
      )}
    </div>
  );
};
