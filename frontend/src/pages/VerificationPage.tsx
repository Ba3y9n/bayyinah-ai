import React, { useState } from 'react';
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
  RefreshCw,
  Globe,
  Youtube,
  Clock
} from 'lucide-react';
import { VerificationResponse } from '../types';
import { api } from '../services/api';

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

export const VerificationPage: React.FC<VerificationPageProps> = ({
  inputText,
  imageBase64,
  urlInput,
  onVerificationComplete,
  onCancel
}) => {
  const [inputMode, setInputMode] = useState<InputMode>(
    urlInput ? 'url' : (imageBase64 ? 'image' : (inputText ? 'text' : 'none'))
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

  // Handle URL changes & detect platform
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

  // 1. Submit URL verification
  // 1. Submit URL verification
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

  // 2. Upload Image and run OCR first (Rule 20 & 45)
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

  // Submit Image after OCR review
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

  // 3. Submit Video verification (Rule 21 & 46)
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

  // 4. Submit Text verification (Rule 47)
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

  // 5. Submit PDF verification
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

  // Processing state screen (Rule 48)
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
      <div className="max-w-2xl mx-auto px-4 py-20 min-h-[80vh] flex flex-col justify-center">
        <div className="bg-white p-10 rounded-3xl border border-gray-100 shadow-elevated">
          <div className="flex justify-center mb-8">
            <div className="w-16 h-16 rounded-full bg-bayyinah-ivory flex items-center justify-center text-bayyinah-emerald">
              <Loader2 className="w-8 h-8 animate-spin" />
            </div>
          </div>
          <h2 className="text-2xl font-bold text-center text-bayyinah-dark-text mb-2">جاري معالجة المحتوى والتحقق منه</h2>
          <p className="text-center text-bayyinah-secondary-text text-sm mb-10">
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
                  className={`flex items-start gap-4 p-4 rounded-xl border transition-all ${
                    isCurrent 
                      ? 'bg-bayyinah-ivory border-bayyinah-emerald/40 shadow-sm' 
                      : isDone 
                      ? 'bg-white border-gray-100' 
                      : 'bg-white border-transparent opacity-40'
                  }`}
                >
                  <div className="mt-0.5">
                    {isDone ? (
                      <CheckCircle2 className="w-5 h-5 text-bayyinah-emerald" />
                    ) : isCurrent ? (
                      <Loader2 className="w-5 h-5 text-bayyinah-emerald animate-spin" />
                    ) : (
                      <div className="w-5 h-5 rounded-full border-2 border-gray-300 flex items-center justify-center text-[10px] text-gray-400 font-bold">
                        {st.num}
                      </div>
                    )}
                  </div>
                  <div className="flex-1">
                    <h4 className={`text-sm font-bold ${isCurrent ? 'text-bayyinah-emerald' : 'text-bayyinah-dark-text'}`}>
                      {st.num} — {st.title}
                    </h4>
                    {isCurrent && (
                      <p className="text-xs text-bayyinah-secondary-text mt-1">{st.desc}</p>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  // 1. Initial Selection Screen (Rule 43)
  if (inputMode === 'none') {
    return (
      <div className="max-w-5xl mx-auto px-4 py-20 min-h-[80vh]">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold mb-4 text-bayyinah-deep-emerald">ماذا تريد أن تتحقق منه؟</h1>
          <p className="text-bayyinah-secondary-text text-lg">اختر طريقة إدخال المحتوى للبدء في رحلة التحقق المبنية على الأدلة.</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 max-w-5xl mx-auto">
          {/* URL */}
          <button 
            onClick={() => { setInputMode('url'); setErrorMessage(null); }}
            className="group bg-white p-6 rounded-3xl border border-gray-100 hover:border-bayyinah-emerald hover:shadow-elevated transition-all flex flex-col items-center text-center gap-4 cursor-pointer"
          >
            <div className="w-14 h-14 rounded-2xl bg-bayyinah-ivory flex items-center justify-center text-bayyinah-emerald group-hover:scale-110 transition-transform">
              <Link2 className="w-7 h-7" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-bayyinah-dark-text mb-1">رابط</h3>
              <p className="text-bayyinah-secondary-text text-xs">يوتيوب، تيك توك، X، ويب</p>
            </div>
          </button>

          {/* Image */}
          <button 
            onClick={() => { setInputMode('image'); setErrorMessage(null); }}
            className="group bg-white p-6 rounded-3xl border border-gray-100 hover:border-bayyinah-emerald hover:shadow-elevated transition-all flex flex-col items-center text-center gap-4 cursor-pointer"
          >
            <div className="w-14 h-14 rounded-2xl bg-bayyinah-ivory flex items-center justify-center text-bayyinah-emerald group-hover:scale-110 transition-transform">
              <ImageIcon className="w-7 h-7" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-bayyinah-dark-text mb-1">صورة</h3>
              <p className="text-bayyinah-secondary-text text-xs">OCR ومراجعة النص</p>
            </div>
          </button>

          {/* Video */}
          <button 
            onClick={() => { setInputMode('video'); setErrorMessage(null); }}
            className="group bg-white p-6 rounded-3xl border border-gray-100 hover:border-bayyinah-emerald hover:shadow-elevated transition-all flex flex-col items-center text-center gap-4 cursor-pointer"
          >
            <div className="w-14 h-14 rounded-2xl bg-bayyinah-ivory flex items-center justify-center text-bayyinah-emerald group-hover:scale-110 transition-transform">
              <FileVideo className="w-7 h-7" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-bayyinah-dark-text mb-1">فيديو</h3>
              <p className="text-bayyinah-secondary-text text-xs">تفريغ صوتي وتحليل</p>
            </div>
          </button>

          {/* PDF */}
          <button 
            onClick={() => { setInputMode('pdf'); setErrorMessage(null); }}
            className="group bg-white p-6 rounded-3xl border border-gray-100 hover:border-bayyinah-emerald hover:shadow-elevated transition-all flex flex-col items-center text-center gap-4 cursor-pointer"
          >
            <div className="w-14 h-14 rounded-2xl bg-bayyinah-ivory flex items-center justify-center text-bayyinah-emerald group-hover:scale-110 transition-transform">
              <FileText className="w-7 h-7" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-bayyinah-dark-text mb-1">وثيقة PDF</h3>
              <p className="text-bayyinah-secondary-text text-xs">تحليل الصفحات والنسب</p>
            </div>
          </button>

          {/* Text */}
          <button 
            onClick={() => { setInputMode('text'); setErrorMessage(null); }}
            className="group bg-white p-6 rounded-3xl border border-gray-100 hover:border-bayyinah-emerald hover:shadow-elevated transition-all flex flex-col items-center text-center gap-4 cursor-pointer"
          >
            <div className="w-14 h-14 rounded-2xl bg-bayyinah-ivory flex items-center justify-center text-bayyinah-emerald group-hover:scale-110 transition-transform">
              <FileText className="w-7 h-7" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-bayyinah-dark-text mb-1">نص</h3>
              <p className="text-bayyinah-secondary-text text-xs">لصق نص مباشر</p>
            </div>
          </button>
        </div>
      </div>
    );
  }

  // 2. Individual Forms (Rules 44, 45, 46, 47)
  return (
    <div className="max-w-3xl mx-auto px-4 py-16 min-h-[80vh]">
      <button 
        onClick={() => { setInputMode('none'); setErrorMessage(null); }}
        className="flex items-center gap-2 text-bayyinah-secondary-text hover:text-bayyinah-emerald mb-8 transition-colors cursor-pointer text-sm font-medium"
      >
        <ArrowRight className="w-4 h-4" />
        العودة لاختيار وسيلة الإدخال
      </button>

      {errorMessage && (
        <div className="mb-6 p-4 rounded-2xl bg-red-50 border border-red-200 text-red-800 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5 text-red-600" />
          <div className="flex-1 text-sm leading-relaxed">{errorMessage}</div>
        </div>
      )}

      {/* MODE: URL (Rule 44) */}
      {inputMode === 'url' && (
        <div className="bg-white p-10 rounded-3xl border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold text-bayyinah-dark-text">تحقق من رابط</h2>
            <span className="text-xs font-semibold px-3 py-1 rounded-full bg-bayyinah-ivory text-bayyinah-emerald border border-bayyinah-emerald/20 flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5" />
              SSRF Protected
            </span>
          </div>
          <p className="text-bayyinah-secondary-text text-sm mb-8">
            الصق رابط المنشور أو التغريدة أو الفيديو لفحص سلامته واستخراج المحتوى منه والتحقق من مصادره.
          </p>

          <div className="relative mb-6">
            <input 
              type="url"
              value={url}
              onChange={(e) => handleUrlChange(e.target.value)}
              placeholder="https://..."
              className="w-full text-left bg-gray-50 border border-gray-200 rounded-2xl px-5 py-4 pl-12 text-sm focus:outline-none focus:border-bayyinah-emerald focus:ring-1 focus:ring-bayyinah-emerald"
              dir="ltr"
            />
            <Globe className="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2" />
          </div>

          {url.trim() && (
            <div className="mb-6 p-4 rounded-xl bg-bayyinah-ivory border border-gray-100 flex items-center justify-between text-xs">
              <span className="text-bayyinah-secondary-text">المنصة المكتشفة:</span>
              <span className="font-bold text-bayyinah-emerald">{detectedPlatform}</span>
            </div>
          )}

          <div className="flex flex-wrap gap-2 mb-8 text-xs text-bayyinah-secondary-text">
            <span className="px-3 py-1 rounded-lg bg-gray-100">YouTube</span>
            <span className="px-3 py-1 rounded-lg bg-gray-100">TikTok</span>
            <span className="px-3 py-1 rounded-lg bg-gray-100">X (Twitter)</span>
            <span className="px-3 py-1 rounded-lg bg-gray-100">Instagram</span>
            <span className="px-3 py-1 rounded-lg bg-gray-100">Generic Web</span>
            <span className="px-3 py-1 rounded-lg bg-gray-100">PDF Document</span>
          </div>

          <button 
            onClick={handleUrlSubmit}
            disabled={!url.trim()}
            className="w-full bg-bayyinah-emerald hover:bg-bayyinah-deep-emerald disabled:opacity-40 text-white font-bold py-4 rounded-xl transition-colors cursor-pointer shadow-sm"
          >
            تحقق من الرابط
          </button>
        </div>
      )}

      {/* MODE: IMAGE (Rule 45) */}
      {inputMode === 'image' && (
        <div className="bg-white p-10 rounded-3xl border border-gray-100 shadow-sm">
          <h2 className="text-2xl font-bold text-bayyinah-dark-text mb-2">تحقق من صورة</h2>
          <p className="text-bayyinah-secondary-text text-sm mb-8">
            ارفع صورة تحتوي على منشور، لقطة شاشة، أو حديث ليتم استخراج النص أولاً ثم مراجعته.
          </p>

          {!imagePreview ? (
            <label className="border-2 border-dashed border-gray-200 hover:border-bayyinah-emerald/50 rounded-3xl p-16 flex flex-col items-center justify-center cursor-pointer bg-bayyinah-ivory/30 hover:bg-bayyinah-ivory/60 transition-all">
              <div className="w-16 h-16 rounded-2xl bg-white flex items-center justify-center text-bayyinah-emerald shadow-sm mb-4">
                <ImageIcon className="w-8 h-8" />
              </div>
              <span className="text-bayyinah-dark-text font-bold mb-1">اضغط لرفع الصورة</span>
              <span className="text-xs text-bayyinah-secondary-text">PNG, JPG, WEBP حتى 20 ميغابايت</span>
              <input type="file" accept="image/*" className="hidden" onChange={handleImageFileChange} />
            </label>
          ) : (
            <div className="space-y-6">
              <div className="rounded-2xl overflow-hidden border border-gray-200 bg-gray-50 p-2 max-h-[300px] flex justify-center relative">
                <img src={imagePreview} alt="Preview" className="max-h-full object-contain rounded-xl" />
                <button 
                  onClick={() => { setImageFile(null); setImagePreview(null); setExtractedOcrText(''); setOcrError(null); }}
                  className="absolute top-4 left-4 bg-white/90 hover:bg-white text-gray-700 text-xs px-3 py-1.5 rounded-lg shadow-sm border border-gray-200"
                >
                  تغيير الصورة
                </button>
              </div>

              {isExtractingOcr && (
                <div className="p-6 rounded-2xl bg-bayyinah-ivory border border-bayyinah-emerald/20 flex items-center justify-center gap-3 text-bayyinah-emerald font-medium">
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>جاري استخراج النص عبر Gemini Multimodal OCR...</span>
                </div>
              )}

              {ocrError && (
                <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-800 text-sm">
                  {ocrError}
                </div>
              )}

              {!isExtractingOcr && (
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-sm font-bold text-bayyinah-dark-text">النص المستخرج من الصورة (قابل للمراجعة والتعديل)</h3>
                    <span className="text-xs text-bayyinah-secondary-text">راجع النص قبل التحقق</span>
                  </div>
                  <textarea 
                    value={extractedOcrText}
                    onChange={(e) => setExtractedOcrText(e.target.value)}
                    placeholder="النص المستخرج يظهر هنا لتتمكن من مراجعته والتأكد من مطابقته قبل التحقق..."
                    className="w-full bg-gray-50 border border-gray-200 rounded-2xl p-4 min-h-[140px] text-sm focus:outline-none focus:border-bayyinah-emerald focus:ring-1 focus:ring-bayyinah-emerald resize-y"
                  />
                </div>
              )}

              <button 
                onClick={handleImageSubmit}
                disabled={isExtractingOcr || !extractedOcrText.trim()}
                className="w-full bg-bayyinah-emerald hover:bg-bayyinah-deep-emerald disabled:opacity-40 text-white font-bold py-4 rounded-xl transition-colors cursor-pointer shadow-sm"
              >
                ابدأ التحقق من النص المستخرج
              </button>
            </div>
          )}
        </div>
      )}

      {/* MODE: VIDEO (Rule 46) */}
      {inputMode === 'video' && (
        <div className="bg-white p-10 rounded-3xl border border-gray-100 shadow-sm">
          <h2 className="text-2xl font-bold text-bayyinah-dark-text mb-2">تحقق من فيديو</h2>
          <p className="text-bayyinah-secondary-text text-sm mb-8">
            ارفع ملف فيديو لتفريغ الصوت عبر Gemini Files API واستخراج الادعاءات مع الطوابع الزمنية.
          </p>

          {!videoFile ? (
            <label className="border-2 border-dashed border-gray-200 hover:border-bayyinah-emerald/50 rounded-3xl p-16 flex flex-col items-center justify-center cursor-pointer bg-bayyinah-ivory/30 hover:bg-bayyinah-ivory/60 transition-all">
              <div className="w-16 h-16 rounded-2xl bg-white flex items-center justify-center text-bayyinah-emerald shadow-sm mb-4">
                <FileVideo className="w-8 h-8" />
              </div>
              <span className="text-bayyinah-dark-text font-bold mb-1">اضغط لرفع مقطع الفيديو</span>
              <span className="text-xs text-bayyinah-secondary-text">MP4, MOV, WEBM حتى 100 ميغابايت</span>
              <input type="file" accept="video/*" className="hidden" onChange={handleVideoFileChange} />
            </label>
          ) : (
            <div className="space-y-6">
              <div className="p-4 rounded-2xl bg-bayyinah-ivory border border-gray-200 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Play className="w-5 h-5 text-bayyinah-emerald" />
                  <div>
                    <span className="block font-bold text-sm text-bayyinah-dark-text">{videoFile.name}</span>
                    <span className="block text-xs text-bayyinah-secondary-text">{(videoFile.size / (1024*1024)).toFixed(1)} MB</span>
                  </div>
                </div>
                <button 
                  onClick={() => { setVideoFile(null); setVideoPreview(null); }}
                  className="text-xs text-red-600 hover:underline"
                >
                  إلغاء
                </button>
              </div>

              {/* Timestamp selection */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-bayyinah-secondary-text mb-2 flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5" />
                    من الدقيقة (اختياري)
                  </label>
                  <input 
                    type="text" 
                    value={videoStartTime}
                    onChange={(e) => setVideoStartTime(e.target.value)}
                    placeholder="00:15"
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl p-3 text-center text-sm font-mono focus:outline-none focus:border-bayyinah-emerald"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-bayyinah-secondary-text mb-2 flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5" />
                    إلى الدقيقة (اختياري)
                  </label>
                  <input 
                    type="text" 
                    value={videoEndTime}
                    onChange={(e) => setVideoEndTime(e.target.value)}
                    placeholder="00:45"
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl p-3 text-center text-sm font-mono focus:outline-none focus:border-bayyinah-emerald"
                  />
                </div>
              </div>

              <button 
                onClick={handleVideoSubmit}
                className="w-full bg-bayyinah-emerald hover:bg-bayyinah-deep-emerald text-white font-bold py-4 rounded-xl transition-colors cursor-pointer shadow-sm"
              >
                ابدأ معالجة الفيديو والتحقق
              </button>
            </div>
          )}
        </div>
      )}

      {/* MODE: TEXT (Rule 47) */}
      {inputMode === 'text' && (
        <div className="bg-white p-10 rounded-3xl border border-gray-100 shadow-sm">
          <h2 className="text-2xl font-bold text-bayyinah-dark-text mb-2">تحقق من نص</h2>
          <p className="text-bayyinah-secondary-text text-sm mb-8">
            الصق النص الذي تريد التحقق منه للبحث عنه في أمهات المصادر والسنة والتفاسير.
          </p>

          <textarea 
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="الصق النص الذي تريد التحقق منه..."
            className="w-full bg-gray-50 border border-gray-200 rounded-2xl p-6 min-h-[220px] text-base leading-relaxed mb-4 focus:outline-none focus:border-bayyinah-emerald focus:ring-1 focus:ring-bayyinah-emerald resize-y"
          />

          <div className="flex justify-between items-center mb-6 text-xs text-bayyinah-secondary-text">
            <span>{text.length} حرف</span>
            <span>يدعم متون الأحاديث، الآيات، الفتاوى، والأقوال المنسوبة</span>
          </div>

          <button 
            onClick={handleTextSubmit}
            disabled={!text.trim()}
            className="w-full bg-bayyinah-emerald hover:bg-bayyinah-deep-emerald disabled:opacity-40 text-white font-bold py-4 rounded-xl transition-colors cursor-pointer shadow-sm"
          >
            ابدأ التحقق
          </button>
        </div>
      )}

      {/* MODE: PDF DOCUMENT */}
      {inputMode === 'pdf' && (
        <div className="bg-white p-10 rounded-3xl border border-gray-100 shadow-sm">
          <h2 className="text-2xl font-bold text-bayyinah-dark-text mb-2">تحقق من وثيقة PDF</h2>
          <p className="text-bayyinah-secondary-text text-sm mb-8">
            ارفع وثيقة أو بحثاً بصيغة PDF لاستخراج الادعاءات والتحقق منها مع حفظ أرقام الصفحات وترتيب النسب.
          </p>

          {!pdfFile ? (
            <div className="border-2 border-dashed border-gray-200 rounded-3xl p-12 text-center hover:border-bayyinah-emerald transition-colors relative cursor-pointer">
              <input 
                type="file" 
                accept=".pdf,application/pdf"
                onChange={handlePdfChange}
                className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
              />
              <div className="w-16 h-16 rounded-2xl bg-bayyinah-ivory flex items-center justify-center text-bayyinah-emerald mx-auto mb-4">
                <FileText className="w-8 h-8" />
              </div>
              <h4 className="font-bold text-bayyinah-dark-text mb-1">اسحب ملف PDF هنا أو انقر للاختيار</h4>
              <p className="text-xs text-bayyinah-secondary-text">يدعم ملفات PDF النصية والبحوث والكتب العلمية</p>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="p-6 rounded-2xl bg-bayyinah-ivory border border-gray-200 flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-xl bg-bayyinah-emerald/10 flex items-center justify-center text-bayyinah-emerald">
                    <FileText className="w-6 h-6" />
                  </div>
                  <div>
                    <span className="block font-bold text-sm text-bayyinah-dark-text">{pdfFile.name}</span>
                    <span className="block text-xs text-bayyinah-secondary-text">
                      {(pdfFile.size / (1024*1024)).toFixed(2)} MB {pdfPagesCount ? `• ${pdfPagesCount} صفحة` : ''}
                    </span>
                  </div>
                </div>
                <button 
                  onClick={() => { setPdfFile(null); setPdfPagesCount(null); }}
                  className="text-xs text-red-600 hover:underline cursor-pointer font-bold"
                >
                  تغيير الملف
                </button>
              </div>

              {pdfExtracting ? (
                <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-xl text-bayyinah-secondary-text text-sm">
                  <Loader2 className="w-4 h-4 animate-spin text-bayyinah-emerald" />
                  <span>جاري استخراج صفحات الوثيقة وتوثيق تسلسلها...</span>
                </div>
              ) : (
                <button 
                  onClick={handlePdfSubmit}
                  className="w-full bg-bayyinah-emerald hover:bg-bayyinah-deep-emerald text-white font-bold py-4 rounded-xl transition-colors cursor-pointer shadow-sm"
                >
                  ابدأ فحص الوثيقة والتحقق من الادعاءات
                </button>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
