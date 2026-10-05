import React, { useState } from 'react';
import { VerificationResponse, EvidenceItem } from '../types';
import { 
  BookOpen, 
  ExternalLink, 
  ShieldCheck, 
  AlertCircle, 
  HelpCircle, 
  ArrowLeft, 
  ChevronDown, 
  ChevronUp,
  Share2,
  Copy,
  Check,
  MessageSquare,
  Clock,
  Layers,
  FileText,
  Search,
  User,
  ArrowDown,
  Info,
  Sparkles
} from 'lucide-react';
import { ShareCard } from '../components/ShareCard';
import { EvidenceGraph } from '../components/EvidenceGraph';

interface ResultPageProps {
  result: VerificationResponse;
  onNewVerification: () => void;
  onOpenHelp?: (claim: string, result: VerificationResponse) => void;
}

export const ResultPage: React.FC<ResultPageProps> = ({ 
  result, 
  onNewVerification,
  onOpenHelp 
}) => {
  const [copied, setCopied] = useState(false);
  const [selectedSource, setSelectedSource] = useState<EvidenceItem | null>(null);
  const [selectedEvidence, setSelectedEvidence] = useState<EvidenceItem | null>(null);
  const [showEvidenceChain, setShowEvidenceChain] = useState(true);
  const [showSearchTransparency, setShowSearchTransparency] = useState(false);
  const [showShareModal, setShowShareModal] = useState(false);

  // Arabic Verdict Labels Mapping (Section 8)
  const getStatusBadge = (statusStr: string, slug?: string) => {
    if (statusStr.includes('ثابت') || slug === 'verified_authentic') {
      return {
        label: 'ثابت بحسب المصدر',
        bgColor: 'bg-bayyinah-emerald text-white',
        icon: <ShieldCheck className="w-5 h-5" />,
        type: 'VERIFIED'
      };
    }
    if (statusStr.includes('موضوع') || statusStr.includes('مكذوب') || slug === 'fabricated_per_source') {
      return {
        label: 'موضوع/مكذوب بحسب المصدر',
        bgColor: 'bg-red-700 text-white',
        icon: <AlertCircle className="w-5 h-5" />,
        type: 'FABRICATED'
      };
    }
    if (statusStr.includes('ضعيف') || slug === 'weak_per_source') {
      return {
        label: 'ضعيف بحسب المصدر',
        bgColor: 'bg-orange-600 text-white',
        icon: <AlertCircle className="w-5 h-5" />,
        type: 'WEAK'
      };
    }
    if (statusStr.includes('لم يثبت') || slug === 'unverified_wording') {
      return {
        label: 'لم يثبت بهذا اللفظ',
        bgColor: 'bg-amber-600 text-white',
        icon: <AlertCircle className="w-5 h-5" />,
        type: 'NOT_ESTABLISHED'
      };
    }
    if (statusStr.includes('اختلاف') || slug === 'scholarly_disagreement') {
      return {
        label: 'اختلاف في المصادر',
        bgColor: 'bg-purple-700 text-white',
        icon: <Layers className="w-5 h-5" />,
        type: 'CONFLICT'
      };
    }
    if (statusStr.includes('مختص') || slug === 'needs_specialist') {
      return {
        label: 'يحتاج مراجعة مختص',
        bgColor: 'bg-blue-600 text-white',
        icon: <AlertCircle className="w-5 h-5" />,
        type: 'SPECIALIST'
      };
    }
    // Default: INSUFFICIENT
    return {
      label: 'لم نجد دليلًا كافيًا',
      bgColor: 'bg-gray-600 text-white',
      icon: <HelpCircle className="w-5 h-5" />,
      type: 'INSUFFICIENT'
    };
  };

  const badge = getStatusBadge(result.status || '', result.status_slug);

  const handleCopySummary = () => {
    const textToCopy = `بيّنة AI | تحقّق قبل أن تنشر.\nالادعاء: ${result.extracted_claim || result.original_input}\nالحالة: ${badge.label}\nالمصدر: ${result.evidence?.[0]?.source_name || 'سجل المصادر المعتمدة'}\nالمرجع: ${result.evidence?.[0]?.reference || 'توثيق معتمد'}\nالرابط: ${result.evidence?.[0]?.url || 'https://bayyinah.ai'}`;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Prepare Share Card Data
  const shareData = {
    platform_name: 'بيّنة AI',
    slogan: 'تحقّق قبل أن تنشر.',
    claim: result.extracted_claim || result.original_input,
    status: badge.label,
    status_slug: result.status_slug || 'insufficient_evidence',
    evidence_excerpt: result.evidence?.[0]?.excerpt || result.reason || 'لم يتوفر مقتطف نصي مباشر.',
    source_name: result.evidence?.[0]?.source_name || 'سجل المصادر المعتمدة',
    reference: result.evidence?.[0]?.reference || 'توثيق معتمد',
    source_url: result.evidence?.[0]?.url || 'https://bayyinah.ai',
    verified_at: new Date().toLocaleDateString('ar-SA')
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-12 min-h-[85vh] space-y-8" dir="rtl">
      
      {/* Top Header & Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-gray-200">
        <div>
          <div className="inline-flex items-center gap-2 bg-bayyinah-ivory text-bayyinah-emerald px-3 py-1 rounded-full text-xs font-bold mb-1 border border-bayyinah-emerald/20">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>توثيق معرفي بالرجوع للمصادر الرسمية</span>
          </div>
          <h1 className="text-3xl font-extrabold text-bayyinah-deep-emerald">نتيجة التحقق الموثقة</h1>
        </div>

        <div className="flex items-center gap-3">
          <button 
            onClick={() => setShowShareModal(!showShareModal)}
            className="flex items-center gap-1.5 text-xs px-4 py-2.5 rounded-xl bg-white border border-gray-200 hover:border-bayyinah-emerald text-bayyinah-dark-text transition-colors cursor-pointer shadow-xs font-bold"
          >
            <Share2 className="w-4 h-4 text-bayyinah-emerald" />
            <span>مشاركة البطاقة</span>
          </button>

          <button 
            onClick={handleCopySummary}
            className="flex items-center gap-1.5 text-xs px-4 py-2.5 rounded-xl bg-white border border-gray-200 hover:border-bayyinah-emerald text-bayyinah-dark-text transition-colors cursor-pointer shadow-xs font-bold"
          >
            {copied ? <Check className="w-4 h-4 text-bayyinah-emerald" /> : <Copy className="w-4 h-4 text-gray-500" />}
            <span>{copied ? 'تم النسخ' : 'نسخ ملخص النتيجة'}</span>
          </button>

          <button 
            onClick={onNewVerification}
            className="bg-bayyinah-emerald hover:bg-bayyinah-deep-emerald text-white text-xs font-bold px-6 py-2.5 rounded-xl transition-colors cursor-pointer shadow-sm"
          >
            فحص جديد
          </button>
        </div>
      </div>

      {/* Share Card Modal Overlay */}
      {showShareModal && (
        <div className="bg-white rounded-3xl p-6 border border-bayyinah-emerald/30 shadow-xl space-y-4">
          <div className="flex items-center justify-between border-b border-gray-100 pb-3">
            <h3 className="text-base font-bold text-bayyinah-deep-emerald flex items-center gap-2">
              <Share2 className="w-5 h-5 text-bayyinah-emerald" />
              بطاقة مشاركة النتيجة الرقمية
            </h3>
            <button 
              onClick={() => setShowShareModal(false)}
              className="text-xs font-bold text-gray-500 hover:text-gray-800"
            >
              إغلاق
            </button>
          </div>
          <ShareCard data={shareData} />
        </div>
      )}

      {/* Main Result Card */}
      <div className="bg-white rounded-3xl border border-gray-100 shadow-elevated overflow-hidden">
        
        {/* Result Header & Verdict Badge */}
        <div className="p-6 md:p-8 border-b border-gray-100 flex flex-wrap items-center justify-between gap-4 bg-bayyinah-ivory/40">
          <div className={`flex items-center gap-3 px-6 py-3.5 rounded-2xl font-bold shadow-sm ${badge.bgColor}`}>
            {badge.icon}
            <span className="text-lg">{badge.label}</span>
          </div>

          <div className="text-xs text-bayyinah-secondary-text font-medium flex items-center gap-3">
            <span>نوع المحتوى: <strong className="text-bayyinah-dark-text">{result.content_type_ar || 'معلومة إسلامية'}</strong></span>
            <span>•</span>
            <span>نطاق الفحص: <strong className="text-bayyinah-dark-text">{result.checked_sources_count || 11} مصادر معتمدة</strong></span>
          </div>
        </div>

        {/* Core Content Body */}
        <div className="p-6 md:p-10 space-y-8">

          {/* SECTION 1: SOURCE TRUST BOUNDARY (User Content vs Approved Evidence) */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-bayyinah-emerald uppercase tracking-wider block">
                حدود الموثوقية (Source Trust Boundary)
              </span>
              <span className="text-[11px] bg-bayyinah-ivory text-bayyinah-emerald px-2.5 py-0.5 rounded-md border border-bayyinah-emerald/20">
                مفصول بصرياً وأمنياً
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-stretch">
              
              {/* USER CONTENT BOX (Untrusted Content) */}
              <div className="bg-amber-50/60 border border-amber-200/80 rounded-2xl p-6 space-y-3 relative">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-amber-900 flex items-center gap-1.5">
                    <User className="w-4 h-4 text-amber-700" />
                    المحتوى المدخل (محتوى المستخدم)
                  </span>
                  <span className="text-[10px] font-bold text-amber-800 bg-amber-100 px-2 py-0.5 rounded">
                    {result.media_metadata?.platform || result.input_type || 'USER_CONTENT'} — محتوى خاضع للتحقق
                  </span>
                </div>

                <div className="text-sm font-semibold text-gray-900 bg-white p-4 rounded-xl border border-amber-200/60 leading-relaxed">
                  «{result.extracted_claim || result.original_input}»
                </div>

                {/* Additional Media Metadata Provenance details */}
                {result.media_metadata && (
                  <div className="text-xs text-amber-900/80 space-y-1 pt-1 font-medium">
                    {result.media_metadata.video_title && (
                      <div>عنوان المقطع: <strong>{result.media_metadata.video_title}</strong></div>
                    )}
                    {result.media_metadata.channel_title && (
                      <div>القناة الناشرة: <strong>{result.media_metadata.channel_title}</strong></div>
                    )}
                    {result.media_metadata.original_filename && (
                      <div>اسم الملف المرفوع: <strong>{result.media_metadata.original_filename}</strong></div>
                    )}
                  </div>
                )}
              </div>

              {/* APPROVED EVIDENCE BOX (Official Allowlisted Evidence) */}
              <div className="bg-emerald-50/60 border border-emerald-200/80 rounded-2xl p-6 space-y-3 relative">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-emerald-950 flex items-center gap-1.5">
                    <BookOpen className="w-4 h-4 text-emerald-700" />
                    الدليل المسترجع (مصدر إسلامي معتمد)
                  </span>
                  <span className="text-[10px] font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded">
                    APPROVED_EVIDENCE
                  </span>
                </div>

                {result.evidence && result.evidence.length > 0 ? (
                  <div className="text-sm text-emerald-950 bg-white p-4 rounded-xl border border-emerald-200/60 leading-relaxed font-medium">
                    «{result.evidence[0].excerpt}»
                    <div className="mt-2 text-xs text-emerald-800 font-bold border-t border-emerald-100 pt-2 flex items-center justify-between">
                      <span>{result.evidence[0].source_name} ({result.evidence[0].reference})</span>
                      {result.evidence[0].url && (
                        <a 
                          href={result.evidence[0].url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-bayyinah-emerald hover:underline flex items-center gap-1"
                        >
                          المصدر الاصلي ↗
                        </a>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="text-xs text-emerald-900/80 bg-white p-4 rounded-xl border border-emerald-200/60 leading-relaxed">
                    لم يُسترجع مقتطف مباشر، وتم الاعتماد على التخريج المرجعي وقواعد التثبت.
                  </div>
                )}
              </div>

            </div>
          </div>

          {/* SECTION 2: CRITICAL SAFETY UX CALLOUTS (Abstention / Safety Notations) */}
          {badge.type === 'INSUFFICIENT' && (
            <div className="p-6 rounded-2xl bg-gray-50 border border-gray-300 text-gray-900 space-y-2">
              <div className="flex items-center gap-2 text-sm font-bold text-gray-900">
                <HelpCircle className="w-5 h-5 text-gray-600" />
                توضيح هائل للأمانة العلمية (لم نجد دليلًا كافيًا):
              </div>
              <p className="text-xs md:text-sm leading-relaxed text-gray-700">
                لم نجد دليلًا كافيًا في المصادر التي تم التحقق منها. <strong>هذا لا يعني أن الادعاء مكذوب</strong>؛ بل يعني أن بيّنة لم تجد دليلًا كافيًا ضمن نطاق بحثها الحالي.
              </p>
            </div>
          )}

          {badge.type === 'NOT_ESTABLISHED' && (
            <div className="p-6 rounded-2xl bg-amber-50 border border-amber-300 text-amber-950 space-y-2">
              <div className="flex items-center gap-2 text-sm font-bold text-amber-900">
                <AlertCircle className="w-5 h-5 text-amber-700" />
                تنبيه التثبت من اللفظ (لم يثبت بهذا اللفظ):
              </div>
              <p className="text-xs md:text-sm leading-relaxed text-amber-900">
                لم يثبت هذا النص بهذا اللفظ في المصادر التي تم التحقق منها. قد يكون معناه صحيحاً أو مأخوذاً من مقولة مشهورة، لكن نسبيته باللفظ المذكور غير ثابتة في أمهات كتب الحديث والمصادر المعتمدة.
              </p>
            </div>
          )}

          {badge.type === 'CONFLICT' && (
            <div className="p-6 rounded-2xl bg-purple-50 border border-purple-300 text-purple-950 space-y-2">
              <div className="flex items-center gap-2 text-sm font-bold text-purple-900">
                <Layers className="w-5 h-5 text-purple-700" />
                تنبيه الأمانة الفقهية (اختلاف في المصادر):
              </div>
              <p className="text-xs md:text-sm leading-relaxed text-purple-900">
                وجدنا اختلافًا بين المصادر المعتمدة في هذه المسألة؛ لذلك لا تقدم بيّنة حكمًا قطعيًا، وتُبرز أقوال العلماء والمذاهب بأمانة ودون ترجيح شخصي.
              </p>
            </div>
          )}

          {badge.type === 'SPECIALIST' && (
            <div className="p-6 rounded-2xl bg-blue-50 border border-blue-300 text-blue-950 space-y-2">
              <div className="flex items-center gap-2 text-sm font-bold text-blue-900">
                <AlertCircle className="w-5 h-5 text-blue-700" />
                تنبيه الإحالة الشرعية (تحتاج مراجعة مختص):
              </div>
              <p className="text-xs md:text-sm leading-relaxed text-blue-900">
                هذه المسألة شخصية أو نازلة تتطلب فتوى دقيقة أو نظر قضاء شرعي؛ لذلك يمتنع النظام عن الإجابة الآلية ويُحيل إلى دور الإفتاء الرسمية والمختصين.
              </p>
            </div>
          )}

          {/* SECTION 3: EXPLANATION FROM REASON */}
          <div>
            <h3 className="text-xs font-bold text-bayyinah-secondary-text uppercase tracking-wider mb-2">
              تحليل بيّنة والدليل المباشر
            </h3>
            <p className="text-base md:text-lg text-bayyinah-dark-text leading-loose font-normal bg-bayyinah-ivory/20 p-6 rounded-2xl border border-gray-100">
              {result.detailed_explanation || result.reason}
            </p>
          </div>

          {/* SECTION 4: INTERACTIVE EVIDENCE CHAIN (Rule 50 & 58) */}
          <div className="border border-gray-100 rounded-2xl p-6 bg-bayyinah-ivory/30 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-bayyinah-dark-text flex items-center gap-2">
                <Layers className="w-4 h-4 text-bayyinah-emerald" />
                مسار سلسلة الأدلة (Evidence Chain)
              </h3>
              <button 
                onClick={() => setShowEvidenceChain(!showEvidenceChain)}
                className="text-xs text-bayyinah-secondary-text hover:text-bayyinah-emerald flex items-center gap-1 cursor-pointer font-bold"
              >
                {showEvidenceChain ? 'إخفاء المسار' : 'عرض المسار'}
                {showEvidenceChain ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
              </button>
            </div>

            {showEvidenceChain && (
              <div className="flex flex-wrap items-center gap-2 md:gap-3 text-xs md:text-sm font-medium">
                <div className="px-3.5 py-2 rounded-xl bg-white border border-gray-200 text-bayyinah-dark-text shadow-xs">
                  1. محتوى المستخدم
                </div>
                <ArrowLeft className="w-4 h-4 text-gray-300 shrink-0" />
                <div className="px-3.5 py-2 rounded-xl bg-white border border-gray-200 text-bayyinah-dark-text shadow-xs">
                  2. الادعاء المستخرج
                </div>
                <ArrowLeft className="w-4 h-4 text-gray-300 shrink-0" />
                <div 
                  onClick={() => result.evidence?.[0] && setSelectedSource(result.evidence[0])}
                  className="px-3.5 py-2 rounded-xl bg-bayyinah-emerald/10 border border-bayyinah-emerald/30 text-bayyinah-emerald font-bold cursor-pointer hover:bg-bayyinah-emerald/20 transition-colors shadow-xs"
                >
                  3. المصدر ({result.evidence?.[0]?.source_name || 'سجل المراجع'})
                </div>
                <ArrowLeft className="w-4 h-4 text-gray-300 shrink-0" />
                <div 
                  onClick={() => result.evidence?.[0] && setSelectedEvidence(result.evidence[0])}
                  className="px-3.5 py-2 rounded-xl bg-bayyinah-emerald/10 border border-bayyinah-emerald/30 text-bayyinah-emerald font-bold cursor-pointer hover:bg-bayyinah-emerald/20 transition-colors shadow-xs"
                >
                  4. الدليل المسترجع
                </div>
                <ArrowLeft className="w-4 h-4 text-gray-300 shrink-0" />
                <div className={`px-4 py-2 rounded-xl font-bold ${badge.bgColor} shadow-xs`}>
                  5. {badge.label}
                </div>
              </div>
            )}
          </div>

          {/* SECTION 5: EVIDENCE ITEMS CARDS */}
          {result.evidence && result.evidence.length > 0 && (
            <div className="space-y-4">
              <h3 className="text-xs font-bold text-bayyinah-secondary-text uppercase tracking-wider">
                الأدلة المعتمدة المسترجعة ({result.evidence.length})
              </h3>
              
              <div className="space-y-4">
                {result.evidence.map((ev, idx) => (
                  <div key={idx} className="bg-white border border-gray-200 rounded-2xl p-6 hover:border-bayyinah-emerald transition-all shadow-xs space-y-4">
                    <div className="flex items-center justify-between text-xs text-bayyinah-emerald font-bold border-b border-gray-100 pb-3">
                      <span className="flex items-center gap-1.5">
                        <BookOpen className="w-4 h-4 text-bayyinah-emerald" />
                        المصدر: {ev.source_name || "مصدر معتمد"}
                      </span>
                      <span className="bg-bayyinah-ivory text-bayyinah-emerald px-2.5 py-0.5 rounded border border-bayyinah-emerald/20">
                        {ev.category || "حديث / تفسير / فقه"}
                      </span>
                    </div>

                    <p className="text-bayyinah-dark-text leading-loose font-medium text-base md:text-lg bg-bayyinah-ivory/30 p-4 rounded-xl">
                      «{ev.excerpt}»
                    </p>

                    <div className="flex flex-wrap items-center justify-between gap-4 text-xs pt-2 border-t border-gray-100">
                      <div className="text-bayyinah-secondary-text">
                        المرجع والتخريج: <strong className="text-bayyinah-dark-text">{ev.reference || "توثيق معتمد"}</strong>
                      </div>
                      
                      {ev.url && (
                        <a 
                          href={ev.url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="bg-bayyinah-emerald/10 hover:bg-bayyinah-emerald text-bayyinah-emerald hover:text-white font-bold px-4 py-2 rounded-xl transition-colors flex items-center gap-1.5 text-xs cursor-pointer"
                        >
                          <span>عرض المصدر الأصلي</span>
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* SECTION 6: SEARCH TRANSPARENCY ("كيف تحققنا؟") */}
          <div className="border border-gray-100 rounded-2xl p-6 bg-gray-50 space-y-3">
            <button 
              onClick={() => setShowSearchTransparency(!showSearchTransparency)}
              className="w-full flex items-center justify-between text-xs font-bold text-bayyinah-dark-text cursor-pointer"
            >
              <span className="flex items-center gap-2">
                <Search className="w-4 h-4 text-bayyinah-emerald" />
                كيف تحققنا؟ (Search & Verification Transparency)
              </span>
              <span className="text-bayyinah-emerald">
                {showSearchTransparency ? 'إخفاء التفاصيل' : 'عرض الاستعلام والمصادر'}
              </span>
            </button>

            {showSearchTransparency && (
              <div className="pt-3 border-t border-gray-200 space-y-2 text-xs text-bayyinah-secondary-text">
                <div>الاستعلام الذي تم إرساله للمستودع: <code className="bg-white px-2 py-0.5 rounded border text-bayyinah-dark-text">{result.extracted_claim || result.original_input}</code></div>
                <div>عدد المصادر المفحوصة في سجل التحدي: <strong className="text-bayyinah-dark-text">{result.checked_sources_count || 11} مصادر موثقة</strong></div>
                <div>عدد الأدلة المسترجعة ذات الصلة: <strong className="text-bayyinah-dark-text">{result.evidence?.length || 0} أفراد أدلة</strong></div>
                <div>آلية البحث: <strong className="text-bayyinah-dark-text">مطابقة لفظية (FTS) + بحث دلالي (pgvector RRF) + تصفية بحظر الهلوسة</strong></div>
              </div>
            )}
          </div>

          {/* SECTION 7: LIMITATIONS & NOTES */}
          {result.limitations && result.limitations.length > 0 && (
            <div className="p-5 rounded-2xl bg-bayyinah-ivory/50 border border-gray-200 text-xs text-bayyinah-secondary-text space-y-1.5">
              <strong className="block text-bayyinah-dark-text font-bold">حدود النتيجة والأمانة العلمية:</strong>
              {result.limitations.map((lim, i) => (
                <div key={i}>• {lim}</div>
              ))}
            </div>
          )}

        </div>
      </div>

      {/* AI DISCLAIMER FOOTER (Section 15) */}
      <div className="p-6 rounded-2xl bg-white border border-gray-200 text-center text-xs text-bayyinah-secondary-text leading-relaxed shadow-xs">
        <AlertCircle className="w-5 h-5 text-bayyinah-emerald mx-auto mb-2" />
        <p className="font-bold text-bayyinah-dark-text">
          "بيّنة نظام ذكاء اصطناعي للمساعدة في البحث والتحقق. لا تُعد جهة إفتاء، ولا تصدر فتاوى شخصية مستقلة."
        </p>
      </div>

    </div>
  );
};
