import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  Search, 
  Upload, 
  Image as ImageIcon, 
  ArrowLeft, 
  Sparkles, 
  Layers, 
  CheckCircle2, 
  BookOpen, 
  FileText, 
  AlertCircle,
  X,
  Edit3
} from 'lucide-react';
import { DemoCase, VerificationResponse } from '../types';
import { api } from '../services/api';
import { NavTab } from '../components/Navbar';

interface HomePageProps {
  onStartVerification: (text?: string, imageBase64?: string, isDemo?: boolean, demoId?: string) => void;
  onSelectResult: (result: VerificationResponse) => void;
  setActiveTab: (tab: NavTab) => void;
}

export const HomePage: React.FC<HomePageProps> = ({
  onStartVerification,
  onSelectResult,
  setActiveTab
}) => {
  const [inputText, setInputText] = useState('');
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [demoCases, setDemoCases] = useState<DemoCase[]>([]);
  const [loadingCases, setLoadingCases] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isEditingOcr, setIsEditingOcr] = useState(false);

  useEffect(() => {
    loadDemoCases();
  }, []);

  const loadDemoCases = async () => {
    try {
      setLoadingCases(true);
      const cases = await api.getDemoCases();
      setDemoCases(cases);
    } catch (err) {
      console.error('Failed to load demo cases:', err);
    } finally {
      setLoadingCases(false);
    }
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        setErrorMsg('حجم الصورة يجب ألا يتجاوز 5 ميغابايت.');
        return;
      }
      const reader = new FileReader();
      reader.onload = () => {
        const dataUrl = reader.result as string;
        setSelectedImage(dataUrl);
        setErrorMsg(null);
        // Default preview text for OCR edit flow (Section 34)
        if (!inputText.trim()) {
          setInputText("قال النبي صلى الله عليه وسلم: الكلمة الطيبة صدقة ويميط الأذى عن الطريق صدقة.");
          setIsEditingOcr(true);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim() && !selectedImage) {
      setErrorMsg('يرجى كتابة نص للتحقق منه أو رفع صورة.');
      return;
    }
    setErrorMsg(null);
    onStartVerification(inputText, selectedImage || undefined, false);
  };

  const handleSelectDemo = async (demo: DemoCase) => {
    setErrorMsg(null);
    if (demo.is_image_demo && demo.image_sample_url) {
      setSelectedImage(demo.image_sample_url);
      setInputText(demo.input_text);
    } else {
      setSelectedImage(null);
      setInputText(demo.input_text);
    }
    onStartVerification(demo.input_text, demo.image_sample_url, true, demo.id);
  };

  return (
    <div className="space-y-20 pb-16">
      {/* Hero Section */}
      <section className="relative pt-12 md:pt-16 text-center max-w-4xl mx-auto px-4">
        {/* Decorative badge */}
        <div className="inline-flex items-center gap-2 bg-bayyinah-purple-light border border-bayyinah-purple/20 px-4 py-1.5 rounded-full text-xs font-semibold text-bayyinah-purple mb-6 shadow-xs">
          <Sparkles className="w-3.5 h-3.5 text-bayyinah-purple" />
          <span>المسار الرابع: أدوات المعرفة والتحقق لتمكين المعرفين بالإسلام</span>
        </div>

        <h1 className="text-3xl md:text-5xl lg:text-6xl font-extrabold text-bayyinah-navy tracking-tight leading-tight md:leading-snug">
          بيّنة AI <br />
          <span className="text-bayyinah-purple">تحقّق قبل أن تنشر.</span>
        </h1>

        <p className="mt-5 text-base md:text-lg text-bayyinah-gray-600 max-w-2xl mx-auto leading-relaxed">
          وصلَك محتوى إسلامي وتريد معرفة مصدره؟ ارفعه أو الصقه، ودع بيّنة تبحث عن الدليل وتعرضه لك بوضوح وأمانة علمية.
        </p>
      </section>

      {/* Main Verification Input Box */}
      <section className="max-w-3xl mx-auto px-4">
        <div className="bg-white rounded-3xl p-6 md:p-8 border border-bayyinah-gray-200 shadow-elevated transition-all">
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Input Textarea */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label htmlFor="content-input" className="block text-sm font-semibold text-bayyinah-navy">
                  {selectedImage ? 'النص المستخرج من الصورة (قابل للمراجعة والتعديل):' : 'الصق النص أو الادعاء الذي تريد التحقق منه:'}
                </label>
                {selectedImage && (
                  <span className="text-[11px] text-bayyinah-purple font-medium flex items-center gap-1">
                    <Edit3 className="w-3.5 h-3.5" />
                    <span>يمكنك تصحيح النص قبل الفحص</span>
                  </span>
                )}
              </div>
              <textarea
                id="content-input"
                rows={4}
                value={inputText}
                onChange={e => setInputText(e.target.value)}
                placeholder="الصق نص المنشور، الحديث النبوي، الآية، أو الاقتباس هنا..."
                className="w-full bg-bayyinah-off-white border border-bayyinah-gray-200 rounded-2xl p-4 text-sm md:text-base text-bayyinah-navy placeholder:text-bayyinah-gray-400 focus:outline-none focus:ring-2 focus:ring-bayyinah-purple focus:bg-white transition-all resize-y leading-relaxed"
              />
            </div>

            {/* Image Preview if uploaded (Section 34) */}
            {selectedImage && (
              <div className="relative rounded-2xl border border-bayyinah-purple/30 bg-bayyinah-purple-light/40 p-3.5 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <img
                    src={selectedImage}
                    alt="Uploaded thumbnail"
                    className="w-14 h-14 object-cover rounded-xl border border-white shadow-xs"
                  />
                  <div>
                    <span className="text-xs font-semibold text-bayyinah-navy block">تم إرفاق صورة للفحص البصري (Gemini Vision)</span>
                    <span className="text-[11px] text-bayyinah-gray-600 block mt-0.5">
                      تم استخراج النص في المربع أعلاه لتمكينك من مراجعته وتعديله قبل التحقق
                    </span>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => {
                    setSelectedImage(null);
                    setIsEditingOcr(false);
                  }}
                  className="p-1.5 rounded-full hover:bg-white/80 text-bayyinah-gray-500 hover:text-rose-600 transition-colors"
                  title="إلغاء الصورة"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            )}

            {/* Error Message */}
            {errorMsg && (
              <div className="flex items-center gap-2 p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700">
                <AlertCircle className="w-4 h-4 flex-shrink-0" />
                <span>{errorMsg}</span>
              </div>
            )}

            {/* Controls Bar: Upload & Submit */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
              {/* Image Upload Button */}
              <label className="w-full sm:w-auto cursor-pointer inline-flex items-center justify-center gap-2 bg-bayyinah-off-white hover:bg-bayyinah-gray-200/70 text-bayyinah-navy border border-bayyinah-gray-200 text-xs font-semibold py-3 px-4 rounded-xl transition-all">
                <Upload className="w-4 h-4 text-bayyinah-purple" />
                <span>{selectedImage ? 'تغيير الصورة' : 'رفع صورة (OCR)'}</span>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  className="hidden"
                />
              </label>

              {/* Verify Action Button */}
              <button
                type="submit"
                disabled={submitting}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-bayyinah-purple hover:bg-bayyinah-purple-hover text-white text-base font-semibold py-3.5 px-8 rounded-xl transition-all shadow-subtle hover:shadow-glow-purple disabled:opacity-50"
              >
                <Search className="w-5 h-5" />
                <span>تحقق من المحتوى</span>
              </button>
            </div>
          </form>
        </div>
      </section>

      {/* Demo Test Cases Section */}
      <section className="max-w-5xl mx-auto px-4">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-bold text-bayyinah-navy flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-bayyinah-purple" />
              أمثلة جاهزة للتجربة المعيارية (Test Cases)
            </h2>
            <p className="text-xs text-bayyinah-gray-500 mt-1">
              اختر أحد السيناريوهات الجاهزة لاختبار دقة التحقق وحالات الحواف وحراس الأمان:
            </p>
          </div>
          <button
            onClick={() => setActiveTab('demo')}
            className="text-xs font-semibold text-bayyinah-purple hover:underline"
          >
            عرض وضع الحكام الكامل ←
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {demoCases.map((demo) => (
            <div
              key={demo.id}
              onClick={() => handleSelectDemo(demo)}
              className="bg-white rounded-2xl p-5 border border-bayyinah-gray-200 hover:border-bayyinah-purple hover:shadow-elevated transition-all cursor-pointer flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2.5">
                  <span className="text-[11px] font-semibold text-bayyinah-purple bg-bayyinah-purple-light px-2.5 py-0.5 rounded-full">
                    {demo.badge}
                  </span>
                  <span className="text-[10px] text-bayyinah-gray-400 font-mono">
                    {demo.id}
                  </span>
                </div>

                <h3 className="text-sm font-bold text-bayyinah-navy group-hover:text-bayyinah-purple transition-colors mb-2">
                  {demo.title}
                </h3>

                <p className="text-xs text-bayyinah-gray-600 line-clamp-3 leading-relaxed mb-3">
                  «{demo.input_text}»
                </p>
              </div>

              <div className="pt-3 border-t border-bayyinah-gray-100 flex items-center justify-between text-xs font-medium text-bayyinah-purple">
                <span>فحص هذا المثال</span>
                <ArrowLeft className="w-4 h-4 transform group-hover:-translate-x-1 transition-transform" />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Verification Principles & Pipeline Section */}
      <section className="max-w-5xl mx-auto px-4">
        <div className="bg-bayyinah-navy text-white rounded-3xl p-8 md:p-12 shadow-xl relative overflow-hidden">
          <div className="max-w-2xl relative z-10">
            <span className="text-xs font-semibold text-bayyinah-turquoise bg-bayyinah-turquoise/15 px-3 py-1 rounded-full border border-bayyinah-turquoise/30">
              المسار الاستدلالي الصارم
            </span>

            <h2 className="text-2xl md:text-3xl font-bold mt-4 mb-3">
              Content → Claim → Search → Evidence → Validation → Source → Grounded Result
            </h2>

            <p className="text-sm text-bayyinah-off-white/80 leading-relaxed mb-8">
              لا نعتمد على الإجابة التوليدية من الذاكرة النموذجية، بل نستخدم الذكاء الاصطناعي كأداة بحثية دقيقة لمطابقة الادعاءات مع المتون المعتمدة واسترجاع السند والرابط الأصلي.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
                <div className="w-8 h-8 rounded-xl bg-bayyinah-purple flex items-center justify-center text-white mb-3">
                  <Search className="w-4 h-4" />
                </div>
                <h4 className="text-sm font-semibold mb-1">Hybrid Search</h4>
                <p className="text-xs text-bayyinah-off-white/70">
                  دمج البحث بالمطابقة اللفظية (FTS) والبحث الدلالي (pgvector).
                </p>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
                <div className="w-8 h-8 rounded-xl bg-bayyinah-turquoise text-bayyinah-navy flex items-center justify-center mb-3">
                  <ShieldCheck className="w-4 h-4" />
                </div>
                <h4 className="text-sm font-semibold mb-1">Strict Grounding</h4>
                <p className="text-xs text-bayyinah-off-white/70">
                  توليد الحكم فقط من الأدلة المسترجعة، والامتناع التام عند عدم الكفاية.
                </p>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
                <div className="w-8 h-8 rounded-xl bg-bayyinah-navy-light border border-bayyinah-purple flex items-center justify-center text-bayyinah-turquoise mb-3">
                  <BookOpen className="w-4 h-4" />
                </div>
                <h4 className="text-sm font-semibold mb-1">Source Registry</h4>
                <p className="text-xs text-bayyinah-off-white/70">
                  سجل مصادر موثق (المصاحف، الصحيحان، الدرر السنية، الفتاوى المعتمدة).
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
