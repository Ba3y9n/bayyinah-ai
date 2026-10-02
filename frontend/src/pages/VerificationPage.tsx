import React, { useEffect, useState } from 'react';
import { 
  ShieldCheck, 
  Search, 
  CheckCircle2, 
  Layers, 
  Database, 
  FileText, 
  Sparkles, 
  ArrowRight,
  AlertCircle
} from 'lucide-react';
import { VerificationResponse } from '../types';
import { AvatarAssistant } from '../components/AvatarAssistant';

interface VerificationPageProps {
  inputText?: string;
  imageBase64?: string;
  isDemo?: boolean;
  demoId?: string;
  onVerificationComplete: (result: VerificationResponse) => void;
  onCancel: () => void;
  result: VerificationResponse | null;
  error: string | null;
}

export const VerificationPage: React.FC<VerificationPageProps> = ({
  inputText,
  imageBase64,
  isDemo,
  onVerificationComplete,
  onCancel,
  result,
  error
}) => {
  const [currentStepIndex, setCurrentStepIndex] = useState(1);

  const stepTitles = [
    'تحليل المحتوى والمدخلات الرقمية',
    'استخراج النص وتطبيع الكلمات العربية',
    'عزل واستخراج الادعاء الأساسي',
    'تصنيف نوع المحتوى (حديث، آية، فقه، سيرة)',
    'توليد استعلامات البحث الدقيقة',
    'تنفيذ البحث بالمطابقة اللفظية (Exact FTS)',
    'تنفيذ البحث الدلالي (Semantic Search / pgvector)',
    'دمج نتائج البحث (Hybrid Search Fusion)',
    'استرجاع وثائق الأدلة الأكثر صلة',
    'مطابقة متن الادعاء وفحص صحة الإسناد',
    'بناء النتيجة الموثقة (Grounded Verification)',
    'التحقق من كفاية الأدلة وحراس الأمان',
    'إصدار النتيجة النهائية والتوثيق المرجعي'
  ];

  // Simulating step progress indicator until API response completes
  useEffect(() => {
    if (result) {
      setCurrentStepIndex(13);
      const timer = setTimeout(() => {
        onVerificationComplete(result);
      }, 700);
      return () => clearTimeout(timer);
    }

    const interval = setInterval(() => {
      setCurrentStepIndex((prev) => {
        if (prev < 12) return prev + 1;
        return prev;
      });
    }, 280);

    return () => clearInterval(interval);
  }, [result]);

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      {/* Header */}
      <div className="text-center mb-10">
        <div className="inline-block mb-3">
          <AvatarAssistant state={result ? 'evidence_found' : 'searching'} size="lg" />
        </div>
        <h1 className="text-2xl md:text-3xl font-bold text-bayyinah-navy">
          جاري التحقق من المحتوى ومطابقة الأدلة...
        </h1>
        <p className="text-xs md:text-sm text-bayyinah-gray-600 mt-2">
          يتم فحص المتن عبر محرك Hybrid Search ومطابقته مع سجل المصادر المعتمدة
        </p>
      </div>

      {/* Input Preview Card */}
      <div className="bg-white rounded-2xl p-5 border border-bayyinah-gray-200 shadow-subtle mb-8">
        <div className="flex items-center justify-between gap-2 mb-2">
          <span className="text-[11px] font-semibold text-bayyinah-purple bg-bayyinah-purple-light px-2.5 py-0.5 rounded-full">
            المحتوى قيد الفحص
          </span>
          {isDemo && (
            <span className="text-[10px] bg-amber-50 text-amber-700 border border-amber-200 px-2 py-0.5 rounded-full font-medium">
              مثال تجريبي
            </span>
          )}
        </div>
        <p className="text-xs md:text-sm text-bayyinah-navy font-medium leading-relaxed">
          «{inputText || (imageBase64 ? 'صورة مرفقة للتحليل البصري' : '')}»
        </p>
      </div>

      {/* Error state */}
      {error && (
        <div className="bg-rose-50 border border-rose-200 rounded-2xl p-6 text-center space-y-4">
          <div className="w-12 h-12 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center mx-auto">
            <AlertCircle className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-rose-800">تعذر إكمال التحقق</h3>
            <p className="text-xs text-rose-600 mt-1">{error}</p>
          </div>
          <button
            onClick={onCancel}
            className="bg-white hover:bg-rose-100/50 text-rose-700 border border-rose-200 text-xs font-semibold py-2 px-5 rounded-xl transition-colors"
          >
            العودة للرئيسية
          </button>
        </div>
      )}

      {/* 13 Steps Live Progress List */}
      {!error && (
        <div className="bg-white rounded-3xl p-6 md:p-8 border border-bayyinah-gray-200 shadow-elevated">
          <div className="space-y-3.5">
            {stepTitles.map((title, index) => {
              const stepNum = index + 1;
              const isCompleted = stepNum < currentStepIndex || (result && stepNum <= 13);
              const isCurrent = stepNum === currentStepIndex && !result;
              const isPending = stepNum > currentStepIndex && !result;

              return (
                <div
                  key={stepNum}
                  className={`flex items-center justify-between p-3 rounded-xl border transition-all ${
                    isCurrent
                      ? 'bg-bayyinah-purple-light/50 border-bayyinah-purple text-bayyinah-navy font-semibold shadow-xs'
                      : isCompleted
                        ? 'bg-bayyinah-off-white/80 border-bayyinah-gray-200 text-bayyinah-navy'
                        : 'bg-white/40 border-bayyinah-gray-100 text-bayyinah-gray-400 opacity-60'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                        isCompleted
                          ? 'bg-emerald-500 text-white'
                          : isCurrent
                            ? 'bg-bayyinah-purple text-white animate-pulse'
                            : 'bg-bayyinah-gray-200 text-bayyinah-gray-500'
                      }`}
                    >
                      {isCompleted ? <CheckCircle2 className="w-4 h-4" /> : stepNum}
                    </div>
                    <span className="text-xs md:text-sm">{title}</span>
                  </div>

                  <div>
                    {isCompleted && (
                      <span className="text-[11px] text-emerald-600 font-medium">مكتمل</span>
                    )}
                    {isCurrent && (
                      <span className="text-[11px] text-bayyinah-purple font-semibold animate-pulse">جاري المعالجة...</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          <div className="mt-8 pt-4 border-t border-bayyinah-gray-100 flex items-center justify-between text-xs text-bayyinah-gray-500">
            <span>مسار التحقق: 13 خطوة معيارية</span>
            <button
              onClick={onCancel}
              className="text-bayyinah-gray-500 hover:text-bayyinah-navy font-medium"
            >
              إلغاء الفحص
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
