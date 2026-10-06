import React, { useState, useEffect, useRef, useCallback } from 'react';
import { VerificationResponse, EvidenceItem } from '../types';
import {
  BookOpen,
  ExternalLink,
  ShieldCheck,
  AlertCircle,
  HelpCircle,
  ChevronDown,
  ChevronUp,
  Share2,
  Copy,
  Check,
  Layers,
  FileText,
  Search,
  User,
  Info,
  Sparkles,
  ArrowRight
} from 'lucide-react';
import { ShareCard } from '../components/ShareCard';

/* ─────────────────────────────────────────────
   Props — identical to the original ResultPage
   ───────────────────────────────────────────── */
interface TextResultPageProps {
  result: VerificationResponse;
  onNewVerification: () => void;
  onOpenHelp?: (claim: string, result: VerificationResponse) => void;
}

/* ─────────────────────────────────────────────
   STATUS BADGE LOGIC  (identical to original)
   ───────────────────────────────────────────── */
const getStatusBadge = (statusStr: string, slug?: string) => {
  if (statusStr.includes('ثابت') || slug === 'verified_authentic') {
    return { label: 'ثابت بحسب المصدر', ring: '#005C43', type: 'VERIFIED' };
  }
  if (statusStr.includes('موضوع') || statusStr.includes('مكذوب') || slug === 'fabricated_per_source') {
    return { label: 'موضوع/مكذوب بحسب المصدر', ring: '#991B1B', type: 'FABRICATED' };
  }
  if (statusStr.includes('ضعيف') || slug === 'weak_per_source') {
    return { label: 'ضعيف بحسب المصدر', ring: '#C2410C', type: 'WEAK' };
  }
  if (statusStr.includes('لم يثبت') || slug === 'unverified_wording') {
    return { label: 'لم يثبت بهذا اللفظ', ring: '#B45309', type: 'NOT_ESTABLISHED' };
  }
  if (statusStr.includes('اختلاف') || slug === 'scholarly_disagreement') {
    return { label: 'اختلاف في المصادر', ring: '#6B21A8', type: 'CONFLICT' };
  }
  if (statusStr.includes('مختص') || slug === 'needs_specialist') {
    return { label: 'يحتاج مراجعة مختص', ring: '#1E40AF', type: 'SPECIALIST' };
  }
  return { label: 'لم نجد دليلًا كافيًا', ring: '#4B5563', type: 'INSUFFICIENT' };
};

/* ─────────────────────────────────────────────
   EVIDENCE JOURNEY STAGES
   ───────────────────────────────────────────── */
const journeyStages = [
  { id: 1, label: 'محتوى المستخدم', key: 'user' },
  { id: 2, label: 'الادعاء المستخرج', key: 'claim' },
  { id: 3, label: 'المصدر المعتمد', key: 'source' },
  { id: 4, label: 'الدليل المسترجع', key: 'evidence' },
  { id: 5, label: 'النتيجة', key: 'verdict' },
];

/* ═══════════════════════════════════════════════
   COMPONENT
   ═══════════════════════════════════════════════ */
export const TextResultPage: React.FC<TextResultPageProps> = ({
  result,
  onNewVerification,
  onOpenHelp
}) => {
  /* ── State ── */
  const [copied, setCopied] = useState(false);
  const [selectedSource, setSelectedSource] = useState<EvidenceItem | null>(null);
  const [selectedEvidence, setSelectedEvidence] = useState<EvidenceItem | null>(null);
  const [showShareModal, setShowShareModal] = useState(false);
  const [showSearchTransparency, setShowSearchTransparency] = useState(false);

  // Evidence Journey
  const [activeJourneyStage, setActiveJourneyStage] = useState(1);
  const [journeyAnimDone, setJourneyAnimDone] = useState(false);

  // Scroll progress
  const [scrollProgress, setScrollProgress] = useState(0);

  // Section reveal
  const [visibleSections, setVisibleSections] = useState<Set<string>>(new Set());
  const sectionRefs = useRef<Record<string, HTMLDivElement | null>>({});

  // Reduced motion
  const prefersReducedMotion = typeof window !== 'undefined'
    ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
    : false;

  /* ── Badge ── */
  const badge = getStatusBadge(result.status || '', result.status_slug);

  /* ── Copy handler (kept intact from original) ── */
  const handleCopySummary = useCallback(() => {
    const textToCopy = `بيّنة AI | تحقّق قبل أن تنشر.\nالادعاء: ${result.extracted_claim || result.original_input}\nالحالة: ${badge.label}\nالمصدر: ${result.evidence?.[0]?.source_name || 'سجل المصادر المعتمدة'}\nالمرجع: ${result.evidence?.[0]?.reference || 'توثيق معتمد'}\nالرابط: ${result.evidence?.[0]?.url || 'https://bayyinah.ai'}`;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }, [result, badge.label]);

  /* ── Share Card Data (kept intact) ── */
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

  /* ── Scroll progress bar ── */
  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      setScrollProgress(docHeight > 0 ? Math.min(scrollTop / docHeight, 1) : 0);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  /* ── Section reveal on scroll (IntersectionObserver) ── */
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setVisibleSections((prev) => new Set([...prev, entry.target.id]));
          }
        });
      },
      { threshold: 0.12 }
    );
    Object.values(sectionRefs.current).forEach((el) => {
      if (el) observer.observe(el);
    });
    return () => observer.disconnect();
  }, []);

  /* ── Journey intro animation ── */
  useEffect(() => {
    if (prefersReducedMotion) {
      setJourneyAnimDone(true);
      setActiveJourneyStage(1);
      return;
    }
    let step = 1;
    const interval = setInterval(() => {
      step++;
      setActiveJourneyStage(step);
      if (step >= 5) {
        clearInterval(interval);
        setTimeout(() => {
          setJourneyAnimDone(true);
          setActiveJourneyStage(1);
        }, 400);
      }
    }, 500);
    return () => clearInterval(interval);
  }, [prefersReducedMotion]);

  /* ── Helpers ── */
  const sectionClass = (id: string) =>
    `transition-all ${prefersReducedMotion ? '' : 'duration-700'} ${
      visibleSections.has(id) ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'
    }`;

  const registerRef = (id: string) => (el: HTMLDivElement | null) => {
    sectionRefs.current[id] = el;
  };

  /* ── Verdict colour helpers ── */
  const verdictBg = () => {
    switch (badge.type) {
      case 'VERIFIED': return 'bg-[#005C43]';
      case 'FABRICATED': return 'bg-red-800';
      case 'WEAK': return 'bg-orange-700';
      case 'NOT_ESTABLISHED': return 'bg-amber-700';
      case 'CONFLICT': return 'bg-purple-800';
      case 'SPECIALIST': return 'bg-blue-700';
      default: return 'bg-gray-600';
    }
  };

  /* ── Journey detail panel content ── */
  const journeyDetail = () => {
    switch (activeJourneyStage) {
      case 1:
        return (
          <div className="space-y-2">
            <h4 className="text-sm font-bold text-bayyinah-dark-text">المحتوى الأصلي</h4>
            <p className="text-sm text-bayyinah-secondary-text leading-relaxed">
              {result.original_input}
            </p>
          </div>
        );
      case 2:
        return (
          <div className="space-y-2">
            <h4 className="text-sm font-bold text-bayyinah-dark-text">الادعاء المستخرج</h4>
            <p className="text-sm text-bayyinah-secondary-text leading-relaxed">
              «{result.extracted_claim || result.original_input}»
            </p>
          </div>
        );
      case 3:
        return (
          <div className="space-y-2">
            <h4 className="text-sm font-bold text-bayyinah-dark-text">المصادر المعتمدة</h4>
            {result.evidence && result.evidence.length > 0 ? (
              <ul className="space-y-1">
                {result.evidence.map((ev, i) => (
                  <li key={i} className="text-sm text-bayyinah-secondary-text flex items-center gap-2">
                    <BookOpen className="w-3.5 h-3.5 text-[#005C43] shrink-0" />
                    <span>{ev.source_name}</span>
                    {ev.url && (
                      <a href={ev.url} target="_blank" rel="noopener noreferrer" className="text-[#005C43] hover:underline text-xs mr-1">↗</a>
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-bayyinah-secondary-text">تم فحص {result.checked_sources_count || 11} مصادر معتمدة</p>
            )}
          </div>
        );
      case 4:
        return (
          <div className="space-y-2">
            <h4 className="text-sm font-bold text-bayyinah-dark-text">الدليل المسترجع</h4>
            {result.evidence && result.evidence.length > 0 ? (
              <div className="text-sm text-bayyinah-secondary-text leading-relaxed bg-[#005C43]/5 p-3 rounded-xl border border-[#005C43]/10">
                «{result.evidence[0].excerpt}»
                <div className="mt-1.5 text-xs text-[#005C43] font-semibold">{result.evidence[0].source_name} — {result.evidence[0].reference}</div>
              </div>
            ) : (
              <div className="flex items-start gap-3 text-sm text-bayyinah-secondary-text">
                <Search className="w-5 h-5 text-gray-400 shrink-0 mt-0.5" />
                <p>لم يُسترجع مقتطف مباشر، وتم الاعتماد على التخريج المرجعي وقواعد التثبت.</p>
              </div>
            )}
          </div>
        );
      case 5:
        return (
          <div className="space-y-2">
            <h4 className="text-sm font-bold text-bayyinah-dark-text">النتيجة النهائية</h4>
            <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-xl text-white text-sm font-bold ${verdictBg()}`}>
              <ShieldCheck className="w-4 h-4" />
              {badge.label}
            </div>
            {(result.detailed_explanation || result.reason) && (
              <p className="text-sm text-bayyinah-secondary-text leading-relaxed mt-2">
                {(result.detailed_explanation || result.reason || '').slice(0, 200)}
                {(result.detailed_explanation || result.reason || '').length > 200 ? '…' : ''}
              </p>
            )}
          </div>
        );
      default:
        return null;
    }
  };

  /* ═══════════════════════════════════════════════
     RENDER
     ═══════════════════════════════════════════════ */
  return (
    <>
      {/* ── SCROLL PROGRESS BAR ── */}
      <div
        className="fixed top-16 left-0 right-0 h-[3px] z-40 pointer-events-none"
        style={{ background: 'transparent' }}
      >
        <div
          className="h-full transition-[width] duration-150"
          style={{
            width: `${scrollProgress * 100}%`,
            background: `linear-gradient(to left, #C89418, #005C43)`,
          }}
        />
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-10 md:py-14 min-h-[85vh] space-y-10" dir="rtl">

        {/* ════════════════════════════════════════
           SECTION 1 — HERO HEADER
           ════════════════════════════════════════ */}
        <div
          id="sec-hero"
          ref={registerRef('sec-hero')}
          className={sectionClass('sec-hero')}
        >
          <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-8">
            {/* Left: Title + Claim summary */}
            <div className="flex-1 space-y-3">
              <div className="inline-flex items-center gap-2 bg-[#005C43]/8 text-[#005C43] px-3.5 py-1.5 rounded-full text-xs font-bold border border-[#005C43]/15">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>نتيجة التحقق الموثقة</span>
              </div>
              <h1 className="text-3xl md:text-4xl font-extrabold text-[#063F36] leading-tight">
                نتيجة التحقق
              </h1>
              <p className="text-sm text-bayyinah-secondary-text max-w-lg leading-relaxed">
                تم تحليل الادعاء وربطه بالمصادر المعتمدة وبناء سلسلة الأدلة.
              </p>

              {/* Action buttons — share/copy text hidden, functions kept */}
              <div className="flex items-center gap-3 pt-2">
                {/* Share button — functionality preserved, label hidden */}
                <button
                  onClick={() => setShowShareModal(!showShareModal)}
                  className="flex items-center gap-1.5 text-xs px-4 py-2.5 rounded-xl bg-white border border-gray-200 hover:border-[#005C43] text-bayyinah-dark-text transition-colors cursor-pointer shadow-sm font-bold"
                  aria-label="مشاركة البطاقة"
                >
                  <Share2 className="w-4 h-4 text-[#005C43]" />
                </button>

                {/* Copy button — functionality preserved, label hidden */}
                <button
                  onClick={handleCopySummary}
                  className="flex items-center gap-1.5 text-xs px-4 py-2.5 rounded-xl bg-white border border-gray-200 hover:border-[#005C43] text-bayyinah-dark-text transition-colors cursor-pointer shadow-sm font-bold"
                  aria-label="نسخ ملخص النتيجة"
                >
                  {copied ? <Check className="w-4 h-4 text-[#005C43]" /> : <Copy className="w-4 h-4 text-gray-500" />}
                </button>

                <button
                  onClick={onNewVerification}
                  className="bg-[#005C43] hover:bg-[#063F36] text-white text-xs font-bold px-6 py-2.5 rounded-xl transition-colors cursor-pointer shadow-sm"
                >
                  فحص جديد
                </button>
              </div>
            </div>

            {/* Right: Verification Status Ring */}
            <div className="flex flex-col items-center gap-4 shrink-0">
              <div className="relative w-44 h-44 md:w-52 md:h-52">
                {/* Outer ring SVG */}
                <svg viewBox="0 0 200 200" className="w-full h-full -rotate-90">
                  {/* Background circle */}
                  <circle cx="100" cy="100" r="88" fill="none" stroke="#E5E7EB" strokeWidth="4" />
                  {/* Main emerald ring */}
                  <circle
                    cx="100" cy="100" r="88"
                    fill="none"
                    stroke={badge.ring}
                    strokeWidth="6"
                    strokeLinecap="round"
                    strokeDasharray={`${2 * Math.PI * 88 * 0.78} ${2 * Math.PI * 88 * 0.22}`}
                    className={prefersReducedMotion ? '' : 'animate-[ring-draw_1.2s_ease-out_forwards]'}
                    style={{ opacity: 1 }}
                  />
                  {/* Gold accent partial ring */}
                  <circle
                    cx="100" cy="100" r="82"
                    fill="none"
                    stroke="#C89418"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeDasharray={`${2 * Math.PI * 82 * 0.15} ${2 * Math.PI * 82 * 0.85}`}
                    strokeDashoffset={`${2 * Math.PI * 82 * 0.65}`}
                    className={prefersReducedMotion ? '' : 'animate-[ring-draw_1.5s_ease-out_0.6s_forwards]'}
                    style={{ opacity: 0.7 }}
                  />
                  {/* Animated dot */}
                  {!prefersReducedMotion && (
                    <circle r="4" fill={badge.ring} className="animate-[orbit_2s_ease-in-out_forwards]">
                      <animateMotion
                        dur="2s"
                        repeatCount="1"
                        fill="freeze"
                        path={`M ${100 + 88} ${100} A 88 88 0 1 1 ${100 + 88 * Math.cos(2 * Math.PI * 0.78)} ${100 + 88 * Math.sin(2 * Math.PI * 0.78)}`}
                      />
                    </circle>
                  )}
                </svg>
                {/* Center text */}
                <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-4">
                  <span className="text-sm md:text-base font-extrabold text-[#063F36] leading-snug">
                    {badge.label}
                  </span>
                </div>
              </div>

              {/* Meta info below ring */}
              <div className="text-center space-y-1 text-xs text-bayyinah-secondary-text">
                <div>نوع المحتوى: <strong className="text-bayyinah-dark-text">{result.content_type_ar || 'معلومة إسلامية'}</strong></div>
                <div>نطاق الفحص: <strong className="text-bayyinah-dark-text">{result.checked_sources_count || 11} مصادر</strong></div>
              </div>
            </div>
          </div>
        </div>

        {/* Share Card Modal (functionality preserved) */}
        {showShareModal && (
          <div className="bg-white rounded-3xl p-6 border border-[#005C43]/20 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-gray-100 pb-3">
              <h3 className="text-base font-bold text-[#063F36] flex items-center gap-2">
                <Share2 className="w-5 h-5 text-[#005C43]" />
                بطاقة مشاركة النتيجة
              </h3>
              <button onClick={() => setShowShareModal(false)} className="text-xs font-bold text-gray-500 hover:text-gray-800 cursor-pointer">إغلاق</button>
            </div>
            <ShareCard data={shareData} />
          </div>
        )}

        {/* ════════════════════════════════════════
           SECTION 2 — CLAIM
           ════════════════════════════════════════ */}
        <div
          id="sec-claim"
          ref={registerRef('sec-claim')}
          className={sectionClass('sec-claim')}
        >
          <div className="relative">
            <div className="absolute top-0 right-0 w-1 h-full bg-gradient-to-b from-[#C89418] to-[#C89418]/0 rounded-full" />
            <div className="pr-5 space-y-2">
              <span className="text-[11px] font-bold text-[#C89418] tracking-wide">محتوى المستخدم</span>
              <h2 className="text-lg font-bold text-[#063F36]">الادعاء الذي تم التحقق منه</h2>
              <p className="text-base md:text-lg text-bayyinah-dark-text leading-loose font-medium">
                «{result.extracted_claim || result.original_input}»
              </p>
              <span className="text-[11px] text-bayyinah-secondary-text">محتوى خاضع للتحقق</span>
            </div>
          </div>
        </div>

        {/* ════════════════════════════════════════
           SECTION 3 — EVIDENCE JOURNEY
           ════════════════════════════════════════ */}
        <div
          id="sec-journey"
          ref={registerRef('sec-journey')}
          className={`${sectionClass('sec-journey')} bg-white rounded-3xl border border-gray-100 shadow-subtle p-6 md:p-8`}
        >
          <div className="space-y-2 mb-6">
            <h2 className="text-lg font-bold text-[#063F36] flex items-center gap-2">
              <Layers className="w-5 h-5 text-[#005C43]" />
              رحلة الدليل
            </h2>
            <p className="text-xs text-bayyinah-secondary-text">من المحتوى المدخل إلى النتيجة الموثقة</p>
          </div>

          {/* Journey Path — Horizontal on Desktop, Vertical on Mobile */}
          <div className="hidden md:flex items-center justify-between mb-8 relative">
            {/* SVG connecting line */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ zIndex: 0 }}>
              <line x1="10%" y1="50%" x2="90%" y2="50%" stroke="#E5E7EB" strokeWidth="2" />
              {!prefersReducedMotion && (
                <line x1="10%" y1="50%" x2="90%" y2="50%" stroke="#005C43" strokeWidth="2"
                  strokeDasharray="100%"
                  className="animate-[line-draw_2s_ease-out_forwards]"
                />
              )}
            </svg>

            {journeyStages.map((stage) => {
              const isActive = journeyAnimDone ? activeJourneyStage === stage.id : activeJourneyStage >= stage.id;
              const isPast = journeyAnimDone ? false : activeJourneyStage > stage.id;
              return (
                <button
                  key={stage.id}
                  onClick={() => { if (journeyAnimDone) setActiveJourneyStage(stage.id); }}
                  className={`relative z-10 flex flex-col items-center gap-2 cursor-pointer transition-all ${prefersReducedMotion ? '' : 'duration-300'} group`}
                  aria-label={stage.label}
                >
                  <div
                    className={`w-11 h-11 rounded-full flex items-center justify-center text-sm font-bold border-2 transition-all ${prefersReducedMotion ? '' : 'duration-300'} ${
                      isActive
                        ? 'bg-[#005C43] text-white border-[#005C43] shadow-md scale-110'
                        : isPast
                        ? 'bg-[#005C43]/20 text-[#005C43] border-[#005C43]/40'
                        : 'bg-white text-gray-400 border-gray-200 group-hover:border-[#005C43]/40'
                    }`}
                  >
                    {String(stage.id).padStart(2, '0')}
                  </div>
                  <span className={`text-[11px] font-semibold transition-colors ${isActive ? 'text-[#005C43]' : 'text-bayyinah-secondary-text'}`}>
                    {stage.label}
                  </span>
                </button>
              );
            })}
          </div>

          {/* Mobile vertical journey */}
          <div className="flex md:hidden flex-col gap-1 mb-6">
            {journeyStages.map((stage, idx) => {
              const isActive = journeyAnimDone ? activeJourneyStage === stage.id : activeJourneyStage >= stage.id;
              return (
                <React.Fragment key={stage.id}>
                  <button
                    onClick={() => { if (journeyAnimDone) setActiveJourneyStage(stage.id); }}
                    className="flex items-center gap-3 py-2 cursor-pointer"
                  >
                    <div
                      className={`w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold border-2 transition-all shrink-0 ${
                        isActive
                          ? 'bg-[#005C43] text-white border-[#005C43]'
                          : 'bg-white text-gray-400 border-gray-200'
                      }`}
                    >
                      {String(stage.id).padStart(2, '0')}
                    </div>
                    <span className={`text-sm font-semibold ${isActive ? 'text-[#005C43]' : 'text-bayyinah-secondary-text'}`}>
                      {stage.label}
                    </span>
                  </button>
                  {idx < journeyStages.length - 1 && (
                    <div className="mr-[17px] w-0.5 h-4 bg-gray-200" />
                  )}
                </React.Fragment>
              );
            })}
          </div>

          {/* Detail Panel */}
          <div className="bg-bayyinah-ivory/60 rounded-2xl p-5 border border-gray-100 min-h-[80px]">
            {journeyDetail()}
          </div>
        </div>

        {/* ════════════════════════════════════════
           SECTION 4 — SOURCE TRUST BOUNDARY
           ════════════════════════════════════════ */}
        <div
          id="sec-trust"
          ref={registerRef('sec-trust')}
          className={sectionClass('sec-trust')}
        >
          <div className="space-y-2 mb-4">
            <h2 className="text-lg font-bold text-[#063F36]">حدود الثقة في المصادر</h2>
            <span className="text-[11px] text-bayyinah-secondary-text tracking-wider">SOURCE TRUST BOUNDARY</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-[1fr_auto_1fr] gap-4 items-stretch">
            {/* User Content */}
            <div className="bg-amber-50/50 border border-amber-200/60 rounded-2xl p-5 space-y-3">
              <div className="flex items-center gap-2">
                <User className="w-4 h-4 text-amber-700" />
                <span className="text-xs font-bold text-amber-900">محتوى المستخدم</span>
              </div>
              <span className="text-[10px] font-semibold text-amber-800 bg-amber-100 px-2 py-0.5 rounded inline-block">
                {result.input_type || 'TEXT'} — محتوى خاضع للتحقق
              </span>
              <div className="text-sm font-medium text-gray-900 bg-white p-3.5 rounded-xl border border-amber-200/40 leading-relaxed">
                «{result.extracted_claim || result.original_input}»
              </div>
            </div>

            {/* Gate visual */}
            <div className="hidden md:flex flex-col items-center justify-center gap-2 px-2">
              <div className="w-10 h-10 rounded-full bg-[#005C43]/10 border-2 border-[#005C43]/30 flex items-center justify-center">
                <ShieldCheck className="w-5 h-5 text-[#005C43]" />
              </div>
              <span className="text-[9px] font-bold text-[#005C43] text-center leading-tight">Verification<br/>Gate</span>
              <ArrowRight className="w-4 h-4 text-[#005C43]/40 rotate-180" />
            </div>
            {/* Mobile gate */}
            <div className="flex md:hidden items-center justify-center py-1">
              <div className="flex items-center gap-2 text-[#005C43]/60">
                <div className="h-px w-8 bg-[#005C43]/20" />
                <ShieldCheck className="w-5 h-5" />
                <span className="text-[10px] font-bold">Verification Gate</span>
                <div className="h-px w-8 bg-[#005C43]/20" />
              </div>
            </div>

            {/* Approved Evidence */}
            <div className="bg-emerald-50/50 border border-emerald-200/60 rounded-2xl p-5 space-y-3">
              <div className="flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-emerald-700" />
                <span className="text-xs font-bold text-emerald-950">الدليل من مصدر إسلامي معتمد</span>
              </div>
              <span className="text-[10px] font-semibold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded inline-block">
                APPROVED EVIDENCE
              </span>
              {result.evidence && result.evidence.length > 0 ? (
                <div className="text-sm text-emerald-950 bg-white p-3.5 rounded-xl border border-emerald-200/40 leading-relaxed font-medium">
                  «{result.evidence[0].excerpt}»
                  <div className="mt-2 text-xs text-emerald-800 font-bold border-t border-emerald-100 pt-2 flex items-center justify-between flex-wrap gap-2">
                    <span>{result.evidence[0].source_name} ({result.evidence[0].reference})</span>
                    {result.evidence[0].url && (
                      <a href={result.evidence[0].url} target="_blank" rel="noopener noreferrer" className="text-[#005C43] hover:underline flex items-center gap-1">
                        فتح المصدر <ExternalLink className="w-3 h-3" />
                      </a>
                    )}
                  </div>
                </div>
              ) : (
                <div className="flex items-start gap-3 text-xs text-emerald-900/80 bg-white p-3.5 rounded-xl border border-emerald-200/40 leading-relaxed">
                  <svg width="32" height="32" viewBox="0 0 32 32" fill="none" className="shrink-0 mt-0.5">
                    <circle cx="16" cy="16" r="14" stroke="#005C43" strokeWidth="1.5" strokeDasharray="4 3" opacity="0.4"/>
                    <path d="M12 16h8M16 12v8" stroke="#005C43" strokeWidth="1.5" strokeLinecap="round" opacity="0.5"/>
                  </svg>
                  <p>لم يُسترجع مقتطف مباشر، وتم الاعتماد على التخريج المرجعي وقواعد التثبت.</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* ════════════════════════════════════════
           SECTION 5 — SAFETY CALLOUTS
           ════════════════════════════════════════ */}
        {badge.type === 'INSUFFICIENT' && (
          <div id="sec-safety-insufficient" ref={registerRef('sec-safety-insufficient')} className={`${sectionClass('sec-safety-insufficient')} p-6 rounded-2xl bg-gray-50 border border-gray-200 text-gray-900 space-y-2`}>
            <div className="flex items-center gap-2 text-sm font-bold"><HelpCircle className="w-5 h-5 text-gray-500" />توضيح الأمانة العلمية (لم نجد دليلًا كافيًا):</div>
            <p className="text-sm leading-relaxed text-gray-700">لم نجد دليلًا كافيًا في المصادر التي تم التحقق منها. <strong>هذا لا يعني أن الادعاء مكذوب</strong>؛ بل يعني أن بيّنة لم تجد دليلًا كافيًا ضمن نطاق بحثها الحالي.</p>
          </div>
        )}
        {badge.type === 'NOT_ESTABLISHED' && (
          <div id="sec-safety-ne" ref={registerRef('sec-safety-ne')} className={`${sectionClass('sec-safety-ne')} p-6 rounded-2xl bg-amber-50 border border-amber-200 text-amber-950 space-y-2`}>
            <div className="flex items-center gap-2 text-sm font-bold text-amber-900"><AlertCircle className="w-5 h-5 text-amber-700" />تنبيه التثبت من اللفظ:</div>
            <p className="text-sm leading-relaxed text-amber-900">لم يثبت هذا النص بهذا اللفظ في المصادر التي تم التحقق منها. قد يكون معناه صحيحاً أو مأخوذاً من مقولة مشهورة، لكن نسبيته باللفظ المذكور غير ثابتة في أمهات كتب الحديث والمصادر المعتمدة.</p>
          </div>
        )}
        {badge.type === 'CONFLICT' && (
          <div id="sec-safety-c" ref={registerRef('sec-safety-c')} className={`${sectionClass('sec-safety-c')} p-6 rounded-2xl bg-purple-50 border border-purple-200 text-purple-950 space-y-2`}>
            <div className="flex items-center gap-2 text-sm font-bold text-purple-900"><Layers className="w-5 h-5 text-purple-700" />تنبيه الأمانة الفقهية:</div>
            <p className="text-sm leading-relaxed text-purple-900">وجدنا اختلافًا بين المصادر المعتمدة في هذه المسألة؛ لذلك لا تقدم بيّنة حكمًا قطعيًا، وتُبرز أقوال العلماء والمذاهب بأمانة ودون ترجيح شخصي.</p>
          </div>
        )}
        {badge.type === 'SPECIALIST' && (
          <div id="sec-safety-s" ref={registerRef('sec-safety-s')} className={`${sectionClass('sec-safety-s')} p-6 rounded-2xl bg-blue-50 border border-blue-200 text-blue-950 space-y-2`}>
            <div className="flex items-center gap-2 text-sm font-bold text-blue-900"><AlertCircle className="w-5 h-5 text-blue-700" />تنبيه الإحالة الشرعية:</div>
            <p className="text-sm leading-relaxed text-blue-900">هذه المسألة شخصية أو نازلة تتطلب فتوى دقيقة أو نظر قضاء شرعي؛ لذلك يمتنع النظام عن الإجابة الآلية ويُحيل إلى دور الإفتاء الرسمية والمختصين.</p>
          </div>
        )}

        {/* ════════════════════════════════════════
           SECTION 6 — BAYYINAH ANALYSIS
           ════════════════════════════════════════ */}
        <div
          id="sec-analysis"
          ref={registerRef('sec-analysis')}
          className={sectionClass('sec-analysis')}
        >
          <div className="space-y-2 mb-4">
            <h2 className="text-lg font-bold text-[#063F36] flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-[#C89418]" />
              تحليل بيّنة
            </h2>
            <p className="text-xs text-bayyinah-secondary-text">قراءة النتيجة في ضوء المصادر المفحوصة</p>
          </div>
          <div className="relative">
            <div className="absolute top-0 right-0 w-1 h-full bg-gradient-to-b from-[#005C43] to-[#005C43]/0 rounded-full" />
            <div className="absolute top-0 right-0 w-1 h-3 bg-[#C89418] rounded-full" />
            <p className="pr-5 text-base md:text-lg text-bayyinah-dark-text leading-[2] font-normal">
              {result.detailed_explanation || result.reason}
            </p>
          </div>
        </div>

        {/* ════════════════════════════════════════
           SECTION 7 — EVIDENCE ITEMS
           ════════════════════════════════════════ */}
        {result.evidence && result.evidence.length > 0 && (
          <div
            id="sec-evidence"
            ref={registerRef('sec-evidence')}
            className={sectionClass('sec-evidence')}
          >
            <h2 className="text-lg font-bold text-[#063F36] mb-4">
              المصادر التي شملها التحقق
            </h2>
            <div className="space-y-4">
              {result.evidence.map((ev, idx) => (
                <div key={idx} className="bg-white border border-gray-100 rounded-2xl p-5 hover:border-[#005C43]/30 transition-all shadow-sm space-y-3">
                  <div className="flex items-center justify-between text-xs text-[#005C43] font-bold border-b border-gray-50 pb-2.5">
                    <span className="flex items-center gap-1.5">
                      <BookOpen className="w-4 h-4" />
                      {ev.source_name || 'مصدر معتمد'}
                    </span>
                    {ev.category && (
                      <span className="bg-[#005C43]/8 text-[#005C43] px-2.5 py-0.5 rounded border border-[#005C43]/15 text-[11px]">
                        {ev.category}
                      </span>
                    )}
                  </div>
                  <p className="text-bayyinah-dark-text leading-loose font-medium text-base bg-bayyinah-ivory/40 p-4 rounded-xl">
                    «{ev.excerpt}»
                  </p>
                  <div className="flex flex-wrap items-center justify-between gap-3 text-xs pt-1.5 border-t border-gray-50">
                    <div className="text-bayyinah-secondary-text">
                      المرجع: <strong className="text-bayyinah-dark-text">{ev.reference || 'توثيق معتمد'}</strong>
                    </div>
                    {ev.url && (
                      <a
                        href={ev.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-[#005C43]/8 hover:bg-[#005C43] text-[#005C43] hover:text-white font-bold px-4 py-2 rounded-xl transition-colors flex items-center gap-1.5 text-xs cursor-pointer"
                      >
                        <span>فتح المصدر</span>
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ════════════════════════════════════════
           SECTION 8 — SEARCH TRANSPARENCY ACCORDION
           ════════════════════════════════════════ */}
        <div
          id="sec-transparency"
          ref={registerRef('sec-transparency')}
          className={`${sectionClass('sec-transparency')} border border-gray-100 rounded-2xl bg-white shadow-sm overflow-hidden`}
        >
          <button
            onClick={() => setShowSearchTransparency(!showSearchTransparency)}
            className="w-full flex items-center justify-between px-6 py-5 text-sm font-bold text-bayyinah-dark-text cursor-pointer hover:bg-bayyinah-ivory/40 transition-colors"
            aria-expanded={showSearchTransparency}
          >
            <span className="flex items-center gap-2">
              <Search className="w-4 h-4 text-[#005C43]" />
              كيف تحققنا؟
            </span>
            <span className="flex items-center gap-1.5 text-xs text-bayyinah-secondary-text">
              <span>{showSearchTransparency ? 'إخفاء التفاصيل' : 'تفاصيل البحث والتحقق'}</span>
              <ChevronDown className={`w-4 h-4 transition-transform ${showSearchTransparency ? 'rotate-180' : ''}`} />
            </span>
          </button>
          <div
            className={`transition-all overflow-hidden ${prefersReducedMotion ? '' : 'duration-300'} ${showSearchTransparency ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'}`}
          >
            <div className="px-6 pb-5 space-y-2.5 text-xs text-bayyinah-secondary-text border-t border-gray-100 pt-4">
              <div>الاستعلام: <code className="bg-bayyinah-ivory px-2 py-0.5 rounded border text-bayyinah-dark-text">{result.extracted_claim || result.original_input}</code></div>
              <div>عدد المصادر المفحوصة: <strong className="text-bayyinah-dark-text">{result.checked_sources_count || 11} مصادر معتمدة</strong></div>
              <div>عدد الأدلة المسترجعة: <strong className="text-bayyinah-dark-text">{result.evidence?.length || 0}</strong></div>
              <div>آلية البحث: <strong className="text-bayyinah-dark-text">مطابقة لفظية (FTS) + بحث دلالي (pgvector RRF) + تصفية بحظر الهلوسة</strong></div>
            </div>
          </div>
        </div>

        {/* ════════════════════════════════════════
           SECTION 9 — SCIENTIFIC INTEGRITY
           ════════════════════════════════════════ */}
        {result.limitations && result.limitations.length > 0 && (
          <div
            id="sec-integrity"
            ref={registerRef('sec-integrity')}
            className={`${sectionClass('sec-integrity')} p-6 rounded-2xl border border-[#005C43]/15 space-y-2`}
            style={{ background: 'linear-gradient(135deg, rgba(0,92,67,0.03) 0%, rgba(0,131,93,0.02) 100%)' }}
          >
            <h3 className="text-sm font-bold text-[#063F36] flex items-center gap-2">
              <Info className="w-4 h-4 text-[#005C43]" />
              حدود النتيجة والأمانة العلمية
            </h3>
            <div className="space-y-1.5 text-xs text-bayyinah-secondary-text">
              {result.limitations.map((lim, i) => (
                <div key={i} className="flex items-start gap-2">
                  <div className="w-1 h-1 rounded-full bg-[#C89418] mt-1.5 shrink-0" />
                  <span>{lim}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ════════════════════════════════════════
           SECTION 10 — FOOTER DISCLAIMER
           ════════════════════════════════════════ */}
        <div className="p-6 rounded-2xl bg-white border border-gray-100 text-center text-xs text-bayyinah-secondary-text leading-relaxed shadow-sm">
          <ShieldCheck className="w-5 h-5 text-[#005C43] mx-auto mb-2" />
          <p className="font-semibold text-bayyinah-dark-text leading-relaxed">
            بيّنة نظام ذكاء اصطناعي للمساعدة في البحث والتحقق. لا تُعد جهة إفتاء، ولا تصدر فتاوى شخصية مستقلة.
          </p>
        </div>

      </div>
    </>
  );
};
