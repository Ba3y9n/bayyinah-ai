import React, { useState, useEffect, useRef } from 'react';
import {
  Link2,
  Image as ImageIcon,
  FileVideo,
  FileText,
  ArrowLeft,
  ArrowRight,
  Loader2,
  Play,
  ShieldCheck,
  AlertCircle,
  CheckCircle2,
  Globe,
  Clock,
  Info,
  UploadCloud,
  ChevronLeft,
} from 'lucide-react';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';
import { VerificationResponse } from '../types';
import { api } from '../services/api';

/* ─────────────────────────────────────────────
   Types — preserved exactly
───────────────────────────────────────────── */
type InputMode = 'none' | 'url' | 'image' | 'video' | 'text' | 'pdf';

interface VerificationPageProps {
  inputText?: string;
  imageBase64?: string;
  urlInput?: string;
  isDemo?: boolean;
  demoId?: string;
  result?: VerificationResponse | null;
  error?: string | null;
  onVerificationComplete: (result: VerificationResponse) => void;
  onCancel: () => void;
}

/* ─────────────────────────────────────────────
   Decorative SVG — Gold divider
───────────────────────────────────────────── */
const GoldDivider = () => (
  <div className="flex items-center justify-center gap-3 my-6" aria-hidden="true">
    <span
      className="block h-px flex-1 max-w-[120px]"
      style={{ background: 'linear-gradient(to left, rgba(210,165,35,0.55), transparent)' }}
    />
    <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
      <path d="M5 0L6.18 3.82L10 5L6.18 6.18L5 10L3.82 6.18L0 5L3.82 3.82Z" fill="#C99418" />
    </svg>
    <span
      className="block h-px flex-1 max-w-[120px]"
      style={{ background: 'linear-gradient(to right, rgba(210,165,35,0.55), transparent)' }}
    />
  </div>
);

/* ─────────────────────────────────────────────
   Background decoration — waves & nodes
───────────────────────────────────────────── */
const BackgroundDecor = () => (
  <div
    className="pointer-events-none absolute inset-0 overflow-hidden"
    aria-hidden="true"
  >
    {/* SVG curves bottom */}
    <svg
      className="absolute bottom-0 left-0 right-0 w-full opacity-60"
      viewBox="0 0 1440 220"
      preserveAspectRatio="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M0,160 C240,100 480,200 720,150 C960,100 1200,180 1440,130 L1440,220 L0,220 Z"
        fill="rgba(84,220,160,0.06)"
      />
      <path
        d="M0,185 C300,130 600,200 900,165 C1100,140 1300,190 1440,160 L1440,220 L0,220 Z"
        fill="rgba(84,220,160,0.04)"
      />
      {/* Thin gold curves */}
      <path
        d="M0,195 C360,155 720,195 1080,170 C1260,158 1380,178 1440,175"
        stroke="rgba(201,148,24,0.18)"
        strokeWidth="1"
        fill="none"
      />
      {/* Gold nodes */}
      {[180, 480, 760, 1050, 1320].map((x, i) => (
        <circle key={i} cx={x} cy={192 + (i % 2) * 10} r="2.5" fill="rgba(201,148,24,0.35)" />
      ))}
    </svg>

    {/* Top-right faint gold glow */}
    <div
      className="absolute -top-10 right-0 w-80 h-80 rounded-full opacity-[0.035]"
      style={{ background: 'radial-gradient(circle, #D8A72B 0%, transparent 70%)' }}
    />
  </div>
);

/* ─────────────────────────────────────────────
   Shared page background style
───────────────────────────────────────────── */
const pageBg = `
  radial-gradient(circle at 50% 35%, rgba(75,220,160,0.07), transparent 35%),
  radial-gradient(circle at 10% 85%, rgba(50,200,140,0.10), transparent 32%),
  radial-gradient(circle at 90% 85%, rgba(50,200,140,0.10), transparent 32%),
  radial-gradient(circle at 50% 15%, rgba(215,170,40,0.035), transparent 26%),
  linear-gradient(180deg, #ffffff 0%, #fbfefc 50%, #f1faf5 100%)
`.trim();

/* ─────────────────────────────────────────────
   Sub-page layout wrapper
───────────────────────────────────────────── */
const SubPageWrapper: React.FC<{
  onBack: () => void;
  iconEl: React.ReactNode;
  title: string;
  description: string;
  children: React.ReactNode;
}> = ({ onBack, iconEl, title, description, children }) => (
  <main
    className="relative isolate overflow-hidden px-4 py-10 sm:py-14"
    style={{ background: pageBg }}
  >
    <BackgroundDecor />
    <div className="mx-auto max-w-3xl relative z-10">
      {/* Back button */}
      <motion.button
        initial={{ opacity: 0, x: 10 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3 }}
        onClick={onBack}
        className="mb-8 inline-flex items-center gap-2 rounded-full border border-[#c89418]/40 bg-white/90 px-4 py-2.5 text-sm font-semibold text-[#315747] shadow-sm transition-all hover:border-[#006a4e]/40 hover:text-[#005b42] hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#00835d]/45"
      >
        <ChevronLeft className="w-4 h-4 ml-1" />
        العودة لاختيار وسيلة الإدخال
      </motion.button>

      {/* Page header */}
      <motion.div
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, delay: 0.05 }}
        className="flex flex-col items-center text-center mb-8"
      >
        {/* Icon circle */}
        <div
          className="mb-5 flex h-[68px] w-[68px] items-center justify-center rounded-full border border-[#c89418]/55 bg-white text-[#005b42] shadow-[0_0_0_8px_rgba(84,220,160,0.08),0_4px_16px_rgba(0,90,60,0.10)]"
        >
          {iconEl}
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-[#005b42] mb-3 leading-tight">
          {title}
        </h1>
        <p className="max-w-xl text-base text-[rgba(0,70,50,0.75)] leading-relaxed">
          {description}
        </p>
      </motion.div>

      {/* Children (form content) */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.15 }}
      >
        {children}
      </motion.div>
    </div>
  </main>
);

/* ─────────────────────────────────────────────
   Shared Dropzone label component
───────────────────────────────────────────── */
const DropzonePlaceholder: React.FC<{
  icon: React.ReactNode;
  mainText: string;
  subText: string;
  formats: string;
  accept: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}> = ({ icon, mainText, subText, formats, accept, onChange }) => (
  <label
    className="group relative flex cursor-pointer flex-col items-center justify-center gap-4 rounded-[24px] border border-dashed border-[#006a4e]/50 bg-white/70 px-6 py-14 text-center transition-all duration-300 hover:border-[#006a4e]/80 hover:bg-[rgba(84,220,160,0.04)] focus-within:border-[#006a4e]/80 focus-within:ring-2 focus-within:ring-[#00835d]/30"
    style={{
      boxShadow: '0 0 0 1px rgba(210,165,40,0.10), 0 14px 36px rgba(0,90,60,0.06)',
    }}
  >
    {/* Upload cloud icon with hover lift */}
    <div className="flex flex-col items-center gap-1 transition-transform duration-300 group-hover:-translate-y-1">
      <div
        className="flex h-[64px] w-[64px] items-center justify-center rounded-full border border-[#c89418]/45 bg-gradient-to-br from-white to-[#edfaf4] text-[#005b42] shadow-sm"
      >
        {icon}
      </div>
      <UploadCloud className="w-5 h-5 text-[#006a4e]/50 mt-1" />
    </div>
    <div>
      <p className="text-base font-bold text-[#005b42] mb-1">{mainText}</p>
      <p className="text-sm text-[rgba(0,70,50,0.65)]">{subText}</p>
    </div>
    <div className="flex flex-wrap justify-center gap-2">
      {formats.split(',').map((f) => (
        <span
          key={f}
          className="rounded-full border border-[#c89418]/35 bg-white px-3 py-1 text-xs font-semibold text-[#006a4e]"
        >
          {f.trim()}
        </span>
      ))}
    </div>
    <input type="file" accept={accept} className="sr-only" onChange={onChange} />
  </label>
);

/* ─────────────────────────────────────────────
   Shared Submit Button
───────────────────────────────────────────── */
const SubmitButton: React.FC<{
  onClick: () => void;
  disabled?: boolean;
  children: React.ReactNode;
}> = ({ onClick, disabled, children }) => (
  <motion.button
    whileTap={disabled ? undefined : { scale: 0.98 }}
    onClick={onClick}
    disabled={!!disabled}
    className="mx-auto mt-6 flex w-full max-w-[480px] items-center justify-center gap-2 rounded-[20px] border border-[#c89418]/40 py-[17px] text-base font-bold text-white shadow-[0_4px_20px_rgba(0,90,60,0.18)] transition-all duration-300 disabled:cursor-not-allowed disabled:opacity-40"
    style={{
      background: disabled
        ? '#9ab5ac'
        : 'linear-gradient(135deg, #00835d 0%, #006a4c 100%)',
    }}
  >
    {children}
  </motion.button>
);

/* ─────────────────────────────────────────────
   Shared Error Banner
───────────────────────────────────────────── */
const ErrorBanner: React.FC<{ message: string }> = ({ message }) => (
  <div className="mb-5 flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50/90 p-4 text-red-800">
    <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-red-600" />
    <div className="flex-1 text-sm leading-relaxed">{message}</div>
  </div>
);

/* ─────────────────────────────────────────────
   Main Component
───────────────────────────────────────────── */
export const VerificationPage: React.FC<VerificationPageProps> = ({
  inputText,
  imageBase64,
  urlInput,
  onVerificationComplete,
  onCancel,
}) => {
  const shouldReduceMotion = useReducedMotion() ?? false;

  /* ── State (ALL ORIGINAL — no changes) ─── */
  const [inputMode, setInputMode] = useState<InputMode>(
    urlInput ? 'url' : imageBase64 ? 'image' : inputText ? 'text' : 'none'
  );
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStep, setProcessingStep] = useState(1);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // PDF state
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [pdfExtracting, setPdfExtracting] = useState(false);
  const [pdfPagesCount, setPdfPagesCount] = useState<number | null>(null);

  // URL state
  const [url, setUrl] = useState(urlInput || '');
  const [detectedPlatform, setDetectedPlatform] = useState<string>('GENERIC');

  // Text state
  const [text, setText] = useState(inputText || '');

  // Image state
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(imageBase64 || null);
  const [isExtractingOcr, setIsExtractingOcr] = useState(false);
  const [extractedOcrText, setExtractedOcrText] = useState('');
  const [ocrError, setOcrError] = useState<string | null>(null);

  // Video state
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [videoPreview, setVideoPreview] = useState<string | null>(null);
  const [videoStartTime, setVideoStartTime] = useState('00:00');
  const [videoEndTime, setVideoEndTime] = useState('');

  /* ── Auto-highlight state for selection screen ── */
  const [highlightIndex, setHighlightIndex] = useState(0);
  const [userInteracting, setUserInteracting] = useState(false);
  const interactTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (inputMode !== 'none' || shouldReduceMotion || userInteracting) return;
    const t = setInterval(() => {
      setHighlightIndex((p) => (p + 1) % 4);
    }, 3000);
    return () => clearInterval(t);
  }, [inputMode, shouldReduceMotion, userInteracting]);

  const handleCardInteract = () => {
    setUserInteracting(true);
    if (interactTimeout.current) clearTimeout(interactTimeout.current);
    interactTimeout.current = setTimeout(() => setUserInteracting(false), 5000);
  };

  /* ── Original handlers (UNCHANGED) ─────── */
  const handleUrlChange = (val: string) => {
    setUrl(val);
    const low = val.toLowerCase();
    if (low.includes('youtube.com') || low.includes('youtu.be')) setDetectedPlatform('YOUTUBE');
    else if (low.includes('tiktok.com')) setDetectedPlatform('TIKTOK');
    else if (low.includes('twitter.com') || low.includes('x.com')) setDetectedPlatform('X');
    else if (low.includes('instagram.com')) setDetectedPlatform('INSTAGRAM');
    else if (low.endsWith('.pdf')) setDetectedPlatform('PDF');
    else setDetectedPlatform('WEB');
  };

  const handleUrlSubmit = async () => {
    if (!url.trim()) return;
    setIsProcessing(true);
    setProcessingStep(1);
    setErrorMessage(null);
    try {
      setProcessingStep(2);
      const result = await api.verifyUrl(url);
      setProcessingStep(6);
      setTimeout(() => onVerificationComplete(result), 300);
    } catch (err: any) {
      setIsProcessing(false);
      setErrorMessage(err.message || 'فشل في التحقق من الرابط. تأكد من إمكانية الوصول إلى الرابط وصحته.');
    }
  };

  const handleImageFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || !e.target.files[0]) return;
    const file = e.target.files[0];
    setImageFile(file);
    setImagePreview(URL.createObjectURL(file));
    setOcrError(null);
    setIsExtractingOcr(true);
    try {
      const ocrRes = await api.extractImageText(file);
      if (ocrRes.success && ocrRes.extracted_text) {
        setExtractedOcrText(ocrRes.extracted_text);
      } else {
        setOcrError(ocrRes.error || 'تعذر قراءة المحتوى بشكل موثوق.');
      }
    } catch (err: any) {
      setOcrError(err.message || 'تعذر قراءة المحتوى بشكل موثوق.');
    } finally {
      setIsExtractingOcr(false);
    }
  };

  const handleImageSubmit = async () => {
    if (!extractedOcrText.trim()) return;
    setIsProcessing(true);
    setProcessingStep(1);
    setErrorMessage(null);
    try {
      setProcessingStep(3);
      const result = await api.verifyContent({ text: extractedOcrText });
      setProcessingStep(6);
      setTimeout(() => onVerificationComplete(result), 300);
    } catch (err: any) {
      setIsProcessing(false);
      setErrorMessage(err.message || 'تعذر استكمال فحص الصورة.');
    }
  };

  const handleVideoFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setVideoFile(file);
      setVideoPreview(URL.createObjectURL(file));
    }
  };

  const handleVideoSubmit = async () => {
    if (!videoFile) return;
    setIsProcessing(true);
    setProcessingStep(1);
    setErrorMessage(null);
    try {
      setProcessingStep(3);
      const result = await api.verifyVideo(videoFile);
      setProcessingStep(6);
      setTimeout(() => onVerificationComplete(result), 300);
    } catch (err: any) {
      setIsProcessing(false);
      setErrorMessage(err.message || 'تعذر معالجة المقطع المرئي وتحليله عبر مزود الذكاء الاصطناعي.');
    }
  };

  const handleTextSubmit = async () => {
    if (!text.trim()) return;
    setIsProcessing(true);
    setProcessingStep(1);
    setErrorMessage(null);
    try {
      setProcessingStep(2);
      const result = await api.verifyContent({ text: text.trim() });
      setProcessingStep(6);
      setTimeout(() => onVerificationComplete(result), 300);
    } catch (err: any) {
      setIsProcessing(false);
      setErrorMessage(err.message || 'حدث خطأ أثناء فحص النص.');
    }
  };

  const handlePdfChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || !e.target.files[0]) return;
    const file = e.target.files[0];
    setPdfFile(file);
    setErrorMessage(null);
    setPdfExtracting(true);
    try {
      const res = await api.extractPdfText(file);
      setPdfPagesCount(res.total_pages);
    } catch (err: any) {
      setErrorMessage(err.message || 'فشل في قراءة ملف الـ PDF');
    } finally {
      setPdfExtracting(false);
    }
  };

  const handlePdfSubmit = async () => {
    if (!pdfFile) return;
    setIsProcessing(true);
    setProcessingStep(1);
    setErrorMessage(null);
    try {
      setProcessingStep(3);
      const result = await api.verifyPdf(pdfFile);
      setProcessingStep(6);
      setTimeout(() => onVerificationComplete(result), 300);
    } catch (err: any) {
      setIsProcessing(false);
      setErrorMessage(err.message || 'تعذر استكمال فحص ملف الـ PDF المرفوع.');
    }
  };

  const goBack = () => {
    setInputMode('none');
    setErrorMessage(null);
  };

  /* ════════════════════════════════════════════
     PROCESSING SCREEN (UI only — logic preserved)
  ════════════════════════════════════════════ */
  if (isProcessing) {
    const steps = [
      { num: '01', title: 'فهم المحتوى وتطبيعه', desc: 'تحليل البنية اللغوية وتجريد النص من الشوائب' },
      { num: '02', title: 'استخراج الادعاءات وتصنيفها', desc: 'عزل الادعاءات وفحص حساسية المحتوى' },
      { num: '03', title: 'البحث في المصادر المعتمدة', desc: 'استعلام المطابقة اللفظية والبحث الدلالي pgvector' },
      { num: '04', title: 'جمع الأدلة وتوثيق الإسناد', desc: 'استرجاع متون الأحاديث والتفاسير المعتمدة' },
      { num: '05', title: 'التحقق ومطابقة المتن والسند', desc: 'تطبيق ضوابط التثبت الشرعي ورصد الاختلافات' },
      { num: '06', title: 'بناء النتيجة وسلسلة الأدلة', desc: 'إصدار التوثيق المرجعي وبطاقة المشاركة' },
    ];

    return (
      <main
        className="relative isolate flex min-h-[80vh] flex-col justify-center overflow-hidden px-4 py-14 sm:py-20"
        style={{ background: pageBg }}
      >
        <BackgroundDecor />
        <div className="mx-auto w-full max-w-2xl relative z-10">
          <section
            className="rounded-[24px] border border-[#c89418]/35 bg-white/90 p-6 shadow-[0_20px_50px_rgba(0,90,60,.08)] backdrop-blur sm:p-10"
          >
            <div className="flex justify-center mb-8">
              <div className="w-16 h-16 rounded-full border border-[#c89418]/35 bg-[#f1faf5] flex items-center justify-center text-[#006b4d]">
                <Loader2 className="w-8 h-8 animate-spin" />
              </div>
            </div>
            <h2 className="text-2xl font-bold text-center text-[#005b42] mb-2">
              جاري معالجة المحتوى والتحقق منه
            </h2>
            <p className="text-center text-[rgba(0,70,50,0.65)] text-sm mb-10">
              يقوم محرك بيّنة الآن بربط الادعاء بالمصادر المعتمدة واستخراج سلسلة الأدلة...
            </p>

            <div className="space-y-4">
              {steps.map((st, idx) => {
                const stepIdx = idx + 1;
                const isDone = processingStep > stepIdx;
                const isCurrent = processingStep === stepIdx;
                return (
                  <div
                    key={st.num}
                    className={`flex items-start gap-4 rounded-2xl border p-4 transition-all ${
                      isCurrent
                        ? 'border-[#00835d]/35 bg-[#effaf5] shadow-sm'
                        : isDone
                        ? 'border-[#dcebe3] bg-white'
                        : 'border-transparent bg-white opacity-40'
                    }`}
                  >
                    <div className="mt-0.5">
                      {isDone ? (
                        <CheckCircle2 className="w-5 h-5 text-[#006a4e]" />
                      ) : isCurrent ? (
                        <Loader2 className="w-5 h-5 text-[#006a4e] animate-spin" />
                      ) : (
                        <div className="w-5 h-5 rounded-full border-2 border-gray-300 flex items-center justify-center text-[10px] text-gray-400 font-bold">
                          {st.num}
                        </div>
                      )}
                    </div>
                    <div className="flex-1">
                      <h4 className={`text-sm font-bold ${isCurrent ? 'text-[#006a4e]' : 'text-[#1a2e28]'}`}>
                        {st.num} — {st.title}
                      </h4>
                      {isCurrent && (
                        <p className="text-xs text-[rgba(0,70,50,0.65)] mt-1">{st.desc}</p>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        </div>
      </main>
    );
  }

  /* ════════════════════════════════════════════
     SELECTION SCREEN — "ماذا تريد أن تتحقق منه؟"
  ════════════════════════════════════════════ */
  if (inputMode === 'none') {
    const cards = [
      {
        id: 'url' as const,
        title: 'رابط',
        description: 'لصق رابط ويب',
        detail: 'يوتيوب، منصات الويب المدعومة',
        icon: Link2,
      },
      {
        id: 'image' as const,
        title: 'صورة',
        description: 'رفع صورة أو لقطة شاشة',
        detail: 'JPG, PNG, WEBP',
        icon: ImageIcon,
      },
      {
        id: 'video' as const,
        title: 'فيديو',
        description: 'رفع مقطع فيديو',
        detail: 'MP4, MOV, WEBM',
        icon: FileVideo,
      },
      {
        id: 'pdf' as const,
        title: 'وثيقة PDF',
        description: 'ملفات ومستندات',
        detail: 'PDF',
        icon: FileText,
      },
      {
        id: 'text' as const,
        title: 'نص',
        description: 'الصق نصًا للتحقق منه',
        detail: 'نصوص مباشرة',
        icon: FileText,
      },
    ];

    const renderCard = (card: any, index: number) => {
      const CardIcon = card.icon;
      const isHighlighted = !userInteracting && highlightIndex === index;

      return (
        <motion.button
          key={card.id}
          type="button"
          onClick={() => {
            setInputMode(card.id);
            setErrorMessage(null);
          }}
          onMouseEnter={() => { handleCardInteract(); setHighlightIndex(index); }}
          onFocus={() => { handleCardInteract(); setHighlightIndex(index); }}
          onMouseLeave={() => handleCardInteract()}
          initial={shouldReduceMotion ? false : { opacity: 0, y: 14, scale: 0.985 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          whileHover={shouldReduceMotion ? undefined : { y: -5 }}
          whileTap={shouldReduceMotion ? undefined : { scale: 0.98 }}
          transition={{
            duration: shouldReduceMotion ? 0 : 0.5,
            delay: shouldReduceMotion ? 0 : index * 0.08,
            ease: 'easeOut',
          }}
          className="group relative flex min-h-[185px] w-full items-center gap-6 overflow-hidden rounded-[28px] p-7 text-right transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#00835d]/45 focus-visible:ring-offset-2 sm:min-h-[200px] sm:p-8"
          style={{
            background:
              'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(245,253,249,0.90) 100%)',
            border: isHighlighted
              ? '1px solid rgba(210,165,35,0.75)'
              : '1px solid rgba(210,165,35,0.45)',
            boxShadow: isHighlighted
              ? '0 22px 50px rgba(0,105,72,0.10), 0 0 0 1px rgba(210,165,40,0.20), 0 0 20px rgba(84,220,160,0.08)'
              : '0 16px 40px rgba(0,95,65,0.07), 0 4px 14px rgba(0,95,65,0.04)',
            backdropFilter: 'blur(14px)',
          }}
        >
          {/* Subtle geometric ring behind icon */}
          <span
            className="pointer-events-none absolute -right-12 -top-12 h-36 w-36 rounded-full border border-[#c89418]/08 opacity-[0.08] transition-transform duration-500 group-hover:scale-110"
            aria-hidden="true"
          />

          {/* Icon circle */}
          <span
            className="flex shrink-0 items-center justify-center rounded-full border text-[#005b42] transition-transform duration-300 group-hover:scale-105"
            style={{
              width: 88,
              height: 88,
              background:
                'radial-gradient(circle, rgba(255,255,255,1) 0%, rgba(235,250,242,0.85) 100%)',
              border: isHighlighted
                ? '1px solid rgba(210,165,40,0.70)'
                : '1px solid rgba(210,165,40,0.55)',
              boxShadow: isHighlighted
                ? '0 0 14px rgba(84,220,160,0.18)'
                : '0 2px 8px rgba(0,90,60,0.07)',
            }}
          >
            <CardIcon
              className="transition-transform duration-300 group-hover:scale-110"
              style={{ width: 36, height: 36 }}
              strokeWidth={1.6}
            />
          </span>

          {/* Text content */}
          <span className="min-w-0 flex-1">
            <span className="block text-xl font-bold text-[#005b42] sm:text-2xl">
              {card.title}
            </span>
            <span className="mt-1.5 block text-base text-[rgba(0,70,50,0.72)]">
              {card.description}
            </span>
            <span className="mt-2 block text-xs font-medium text-[rgba(0,90,60,0.50)]">
              {card.detail}
            </span>
          </span>

          {/* Arrow indicator */}
          <span
            className="flex shrink-0 items-center justify-center rounded-full border border-[#006a4e]/16 transition-all duration-300 group-hover:-translate-x-1 group-hover:border-[#006a4e]/30"
            style={{
              width: 44,
              height: 44,
              background: 'rgba(255,255,255,0.9)',
              boxShadow: '0 2px 8px rgba(0,90,60,0.07)',
            }}
          >
            <ArrowLeft className="h-4 w-4 text-[#005b42]" />
          </span>
        </motion.button>
      );
    };

    return (
      <main
        className="relative isolate overflow-hidden px-4 py-14 sm:py-20"
        style={{ background: pageBg }}
      >
        <BackgroundDecor />

        <div className="relative z-10 mx-auto max-w-[1120px]">
          {/* ── Header ── */}
          <motion.div
            initial={shouldReduceMotion ? false : { opacity: 0, y: -12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-2 text-center"
          >
            {/* Decorative icon */}
            <div className="mx-auto mb-5 flex h-[56px] w-[56px] items-center justify-center rounded-full border border-[#c89418]/45 bg-white text-[#005b42] shadow-[0_0_0_7px_rgba(84,220,160,0.07),0_4px_14px_rgba(0,90,60,0.08)]">
              <ShieldCheck className="h-7 w-7" strokeWidth={1.8} />
            </div>

            {/* Main title with color split */}
            <h1
              className="font-extrabold leading-tight"
              style={{ fontSize: 'clamp(38px, 4.5vw, 62px)', lineHeight: 1.2 }}
            >
              <span className="text-[#005b42]">ماذا تريد أن </span>
              <span
                style={{
                  background: 'linear-gradient(135deg, #C99418 0%, #D8A72B 55%, #b87e10 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text',
                }}
              >
                تتحقق منه
              </span>
              <span className="text-[#005b42]">؟</span>
            </h1>
          </motion.div>

          {/* Subtitle */}
          <motion.p
            initial={shouldReduceMotion ? false : { opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="mx-auto mt-4 max-w-2xl text-center text-xl font-medium leading-relaxed"
            style={{ color: 'rgba(0,70,50,0.82)' }}
          >
            اختر طريقة إدخال المحتوى لبدء رحلة التحقق المبنية على الأدلة.
          </motion.p>

          {/* Gold divider */}
          <motion.div
            initial={shouldReduceMotion ? false : { opacity: 0, scaleX: 0.5 }}
            animate={{ opacity: 1, scaleX: 1 }}
            transition={{ duration: 0.5, delay: 0.18 }}
          >
            <GoldDivider />
          </motion.div>

          {/* ── 2×2 Card Grid ── */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-[24px] max-w-[1050px] mx-auto">
            {cards.slice(0, 4).map((card, index) => renderCard(card, index))}
          </div>
          
          {/* ── 5th Card (Centered) ── */}
          <div className="mt-[24px] flex justify-center max-w-[1050px] mx-auto">
            <div className="w-full sm:w-[calc(50%-12px)]">
               {renderCard(cards[4], 4)}
            </div>
          </div>

          {/* ── Info strip ── */}
          <motion.div
            initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.42 }}
            className="mx-auto mt-10 flex max-w-[900px] items-center gap-3 px-6 py-4 text-center"
            style={{
              background: 'rgba(255,255,255,0.84)',
              border: '1px solid rgba(210,165,40,0.55)',
              borderRadius: 999,
              boxShadow: '0 10px 30px rgba(0,90,60,0.05)',
            }}
          >
            {/* Left diamond */}
            <svg width="8" height="8" viewBox="0 0 8 8" className="shrink-0 opacity-50" aria-hidden="true">
              <path d="M4 0L5 3L8 4L5 5L4 8L3 5L0 4L3 3Z" fill="#C99418" />
            </svg>

            <Info className="h-4 w-4 shrink-0 text-[#005b42]" />
            <p className="flex-1 text-sm font-medium text-[rgba(0,70,50,0.80)]">
              ندعم التحقق من مختلف أنواع المحتوى للمساعدة في الوصول إلى المصدر والدليل الموثوق.
            </p>

            {/* Right diamond */}
            <svg width="8" height="8" viewBox="0 0 8 8" className="shrink-0 opacity-50" aria-hidden="true">
              <path d="M4 0L5 3L8 4L5 5L4 8L3 5L0 4L3 3Z" fill="#C99418" />
            </svg>
          </motion.div>
        </div>
      </main>
    );
  }

  /* ════════════════════════════════════════════
     SUB-PAGES
  ════════════════════════════════════════════ */

  /* ── URL PAGE ── */
  if (inputMode === 'url') {
    return (
      <SubPageWrapper
        onBack={goBack}
        iconEl={<Link2 className="h-7 w-7" strokeWidth={1.7} />}
        title="تحقق من رابط"
        description="الصق رابط المنشور أو التغريدة أو الفيديو لفحص سلامته واستخراج المحتوى منه والتحقق من مصادره."
      >
        {errorMessage && <ErrorBanner message={errorMessage} />}

        {/* SSRF badge */}
        <div className="flex justify-center mb-5">
          <span className="inline-flex items-center gap-1.5 rounded-full border border-[#c89418]/35 bg-white px-3 py-1.5 text-xs font-semibold text-[#006a4e] shadow-sm">
            <ShieldCheck className="w-3.5 h-3.5" />
            SSRF Protected
          </span>
        </div>

        {/* URL input */}
        <div
          className="rounded-[22px] border border-[#006a4e]/25 bg-white p-6 shadow-sm"
          style={{ boxShadow: '0 14px 36px rgba(0,90,60,0.06)' }}
        >
          <div className="relative mb-5">
            <input
              type="url"
              value={url}
              onChange={(e) => handleUrlChange(e.target.value)}
              placeholder="https://..."
              className="w-full rounded-[18px] border border-[#006a4e]/25 bg-gray-50/60 py-4 pl-12 pr-4 text-sm text-left transition-all focus:border-[#006a4e]/60 focus:bg-white focus:outline-none focus:ring-2 focus:ring-[#00835d]/20"
              dir="ltr"
            />
            <Globe className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
          </div>

          {/* Detected platform */}
          {url.trim() && (
            <div className="mb-5 flex items-center justify-between rounded-xl border border-gray-100 bg-[#f5faf8] px-4 py-3 text-xs">
              <span className="text-[rgba(0,70,50,0.65)]">المنصة المكتشفة:</span>
              <span className="font-bold text-[#006a4e]">{detectedPlatform}</span>
            </div>
          )}

          {/* Supported platform chips */}
          <div className="flex flex-wrap gap-2 mb-2 text-xs">
            {['YouTube', 'TikTok', 'X (Twitter)', 'Instagram', 'Generic Web', 'PDF Document'].map((p) => (
              <span
                key={p}
                className="rounded-full border border-[#c89418]/30 bg-white px-3 py-1 font-medium text-[rgba(0,70,50,0.65)]"
              >
                {p}
              </span>
            ))}
          </div>
        </div>

        <SubmitButton onClick={handleUrlSubmit} disabled={!url.trim()}>
          تحقق من الرابط
          <ArrowLeft className="w-5 h-5" />
        </SubmitButton>
      </SubPageWrapper>
    );
  }

  /* ── IMAGE PAGE ── */
  if (inputMode === 'image') {
    return (
      <SubPageWrapper
        onBack={goBack}
        iconEl={<ImageIcon className="h-7 w-7" strokeWidth={1.7} />}
        title="تحقق من صورة"
        description="ارفع صورة تحتوي على منشور، لقطة شاشة، أو حديث ليتم استخراج النص أولاً ثم مراجعته."
      >
        {errorMessage && <ErrorBanner message={errorMessage} />}

        <div
          className="rounded-[22px] border border-[#006a4e]/20 bg-white p-6 shadow-sm"
          style={{ boxShadow: '0 14px 36px rgba(0,90,60,0.06)' }}
        >
          {!imagePreview ? (
            <DropzonePlaceholder
              icon={<ImageIcon className="w-8 h-8" strokeWidth={1.6} />}
              mainText="اضغط لرفع الصورة"
              subText="أو اسحب وأفلت الملف هنا"
              formats="JPG, PNG, WEBP"
              accept="image/*"
              onChange={handleImageFileChange}
            />
          ) : (
            <div className="space-y-5">
              <div className="relative rounded-2xl overflow-hidden border border-gray-200 bg-gray-50 p-2 max-h-[300px] flex justify-center">
                <img src={imagePreview} alt="Preview" className="max-h-full object-contain rounded-xl" />
                <button
                  onClick={() => { setImageFile(null); setImagePreview(null); setExtractedOcrText(''); setOcrError(null); }}
                  className="absolute top-4 left-4 rounded-lg border border-gray-200 bg-white/90 px-3 py-1.5 text-xs text-gray-700 shadow-sm hover:bg-white"
                >
                  تغيير الصورة
                </button>
              </div>

              {isExtractingOcr && (
                <div className="flex items-center justify-center gap-3 rounded-2xl border border-[#006a4e]/20 bg-[#f1faf5] p-5 text-[#006a4e] font-medium">
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>جاري استخراج النص عبر Gemini Multimodal OCR...</span>
                </div>
              )}

              {ocrError && (
                <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800">
                  {ocrError}
                </div>
              )}

              {!isExtractingOcr && (
                <div>
                  <div className="mb-2 flex items-center justify-between">
                    <h3 className="text-sm font-bold text-[#1a2e28]">النص المستخرج من الصورة (قابل للمراجعة والتعديل)</h3>
                    <span className="text-xs text-[rgba(0,70,50,0.55)]">راجع النص قبل التحقق</span>
                  </div>
                  <textarea
                    value={extractedOcrText}
                    onChange={(e) => setExtractedOcrText(e.target.value)}
                    placeholder="النص المستخرج يظهر هنا لتتمكن من مراجعته..."
                    className="w-full rounded-2xl border border-gray-200 bg-gray-50/60 p-4 text-sm min-h-[140px] resize-y focus:border-[#006a4e]/60 focus:outline-none focus:ring-2 focus:ring-[#00835d]/20"
                  />
                </div>
              )}
            </div>
          )}
        </div>

        {imagePreview && (
          <SubmitButton
            onClick={handleImageSubmit}
            disabled={isExtractingOcr || !extractedOcrText.trim()}
          >
            ابدأ التحقق من النص المستخرج
            <ArrowLeft className="w-5 h-5" />
          </SubmitButton>
        )}
      </SubPageWrapper>
    );
  }

  /* ── VIDEO PAGE ── */
  if (inputMode === 'video') {
    return (
      <SubPageWrapper
        onBack={goBack}
        iconEl={<FileVideo className="h-7 w-7" strokeWidth={1.7} />}
        title="تحقق من فيديو"
        description="ارفع مقطع فيديو ليتم استخراج المحتوى وتحليله والتحقق منه."
      >
        {errorMessage && <ErrorBanner message={errorMessage} />}

        <div
          className="rounded-[22px] border border-[#006a4e]/20 bg-white p-6 shadow-sm"
          style={{ boxShadow: '0 14px 36px rgba(0,90,60,0.06)' }}
        >
          {!videoFile ? (
            <DropzonePlaceholder
              icon={<FileVideo className="w-8 h-8" strokeWidth={1.6} />}
              mainText="اضغط لرفع مقطع الفيديو"
              subText="أو اسحب وأفلت الملف هنا"
              formats="MP4, MOV, WEBM"
              accept="video/*"
              onChange={handleVideoFileChange}
            />
          ) : (
            <div className="space-y-5">
              <div className="flex items-center justify-between rounded-2xl border border-gray-200 bg-[#f5faf8] p-4">
                <div className="flex items-center gap-3">
                  <Play className="w-5 h-5 text-[#006a4e]" />
                  <div>
                    <span className="block font-bold text-sm text-[#1a2e28]">{videoFile.name}</span>
                    <span className="block text-xs text-[rgba(0,70,50,0.55)]">
                      {(videoFile.size / (1024 * 1024)).toFixed(1)} MB
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => { setVideoFile(null); setVideoPreview(null); }}
                  className="text-xs font-bold text-red-600 hover:underline"
                >
                  إلغاء
                </button>
              </div>

              {/* Timestamp selection — preserved exactly */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="mb-2 flex items-center gap-1.5 text-xs font-semibold text-[rgba(0,70,50,0.65)]">
                    <Clock className="w-3.5 h-3.5" />
                    من الدقيقة (اختياري)
                  </label>
                  <input
                    type="text"
                    value={videoStartTime}
                    onChange={(e) => setVideoStartTime(e.target.value)}
                    placeholder="00:15"
                    className="w-full rounded-xl border border-gray-200 bg-gray-50 p-3 text-center text-sm font-mono focus:border-[#006a4e]/60 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="mb-2 flex items-center gap-1.5 text-xs font-semibold text-[rgba(0,70,50,0.65)]">
                    <Clock className="w-3.5 h-3.5" />
                    إلى الدقيقة (اختياري)
                  </label>
                  <input
                    type="text"
                    value={videoEndTime}
                    onChange={(e) => setVideoEndTime(e.target.value)}
                    placeholder="00:45"
                    className="w-full rounded-xl border border-gray-200 bg-gray-50 p-3 text-center text-sm font-mono focus:border-[#006a4e]/60 focus:outline-none"
                  />
                </div>
              </div>
            </div>
          )}
        </div>

        {videoFile && (
          <SubmitButton onClick={handleVideoSubmit}>
            ابدأ معالجة الفيديو والتحقق
            <ArrowLeft className="w-5 h-5" />
          </SubmitButton>
        )}
      </SubPageWrapper>
    );
  }

  /* ── TEXT PAGE (hidden from selector but functionality preserved) ── */
  if (inputMode === 'text') {
    return (
      <SubPageWrapper
        onBack={goBack}
        iconEl={<FileText className="h-7 w-7" strokeWidth={1.7} />}
        title="تحقق من نص"
        description="الصق النص الذي تريد التحقق منه للبحث عنه في أمهات المصادر والسنة والتفاسير."
      >
        {errorMessage && <ErrorBanner message={errorMessage} />}

        <div
          className="rounded-[22px] border border-[#006a4e]/20 bg-white p-6 shadow-sm"
          style={{ boxShadow: '0 14px 36px rgba(0,90,60,0.06)' }}
        >
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="الصق النص الذي تريد التحقق منه..."
            className="w-full rounded-2xl border border-gray-200 bg-gray-50/60 p-5 text-base leading-relaxed min-h-[220px] resize-y focus:border-[#006a4e]/60 focus:outline-none focus:ring-2 focus:ring-[#00835d]/20"
          />
          <div className="mt-3 flex justify-between text-xs text-[rgba(0,70,50,0.50)]">
            <span>{text.length} حرف</span>
            <span>يدعم متون الأحاديث، الآيات، الفتاوى، والأقوال المنسوبة</span>
          </div>
        </div>

        <SubmitButton onClick={handleTextSubmit} disabled={!text.trim()}>
          ابدأ التحقق
          <ArrowLeft className="w-5 h-5" />
        </SubmitButton>
      </SubPageWrapper>
    );
  }

  /* ── PDF PAGE ── */
  if (inputMode === 'pdf') {
    return (
      <SubPageWrapper
        onBack={goBack}
        iconEl={<FileText className="h-7 w-7" strokeWidth={1.7} />}
        title="تحقق من وثيقة PDF"
        description="ارفع وثيقة أو بحثاً بصيغة PDF لاستخراج الادعاءات والتحقق منها مع حفظ أرقام الصفحات وترتيب النسب."
      >
        {errorMessage && <ErrorBanner message={errorMessage} />}

        <div
          className="rounded-[22px] border border-[#006a4e]/20 bg-white p-6 shadow-sm"
          style={{ boxShadow: '0 14px 36px rgba(0,90,60,0.06)' }}
        >
          {!pdfFile ? (
            <div className="relative">
              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={handlePdfChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              />
              <div
                className="flex cursor-pointer flex-col items-center justify-center gap-4 rounded-[22px] border border-dashed border-[#006a4e]/50 bg-white/70 px-6 py-14 text-center transition-all duration-300 hover:border-[#006a4e]/80 hover:bg-[rgba(84,220,160,0.04)]"
                style={{ boxShadow: '0 0 0 1px rgba(210,165,40,0.10)' }}
              >
                <div className="flex h-[64px] w-[64px] items-center justify-center rounded-full border border-[#c89418]/45 bg-gradient-to-br from-white to-[#edfaf4] text-[#005b42] shadow-sm">
                  <FileText className="w-8 h-8" strokeWidth={1.6} />
                </div>
                <UploadCloud className="w-5 h-5 text-[#006a4e]/50" />
                <div>
                  <p className="text-base font-bold text-[#005b42] mb-1">اسحب ملف PDF هنا أو انقر للاختيار</p>
                  <p className="text-sm text-[rgba(0,70,50,0.65)]">يدعم ملفات PDF النصية والبحوث والكتب العلمية</p>
                </div>
                <span className="rounded-full border border-[#c89418]/35 bg-white px-3 py-1 text-xs font-semibold text-[#006a4e]">
                  PDF
                </span>
              </div>
            </div>
          ) : (
            <div className="space-y-5">
              <div className="flex items-center justify-between rounded-2xl border border-gray-200 bg-[#f5faf8] p-5">
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#006a4e]/10 text-[#006a4e]">
                    <FileText className="w-6 h-6" />
                  </div>
                  <div>
                    <span className="block font-bold text-sm text-[#1a2e28]">{pdfFile.name}</span>
                    <span className="block text-xs text-[rgba(0,70,50,0.55)]">
                      {(pdfFile.size / (1024 * 1024)).toFixed(2)} MB
                      {pdfPagesCount ? ` • ${pdfPagesCount} صفحة` : ''}
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => { setPdfFile(null); setPdfPagesCount(null); }}
                  className="text-xs font-bold text-red-600 hover:underline cursor-pointer"
                >
                  تغيير الملف
                </button>
              </div>

              {pdfExtracting && (
                <div className="flex items-center gap-3 rounded-xl bg-gray-50 p-4 text-sm text-[rgba(0,70,50,0.65)]">
                  <Loader2 className="w-4 h-4 animate-spin text-[#006a4e]" />
                  <span>جاري استخراج صفحات الوثيقة وتوثيق تسلسلها...</span>
                </div>
              )}
            </div>
          )}
        </div>

        {pdfFile && !pdfExtracting && (
          <SubmitButton onClick={handlePdfSubmit}>
            ابدأ فحص الوثيقة والتحقق من الادعاءات
            <ArrowLeft className="w-5 h-5" />
          </SubmitButton>
        )}
      </SubPageWrapper>
    );
  }

  return null;
};
