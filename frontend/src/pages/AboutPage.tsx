import React from 'react';
import { 
  ShieldCheck, 
  AlertTriangle, 
  BookOpen, 
  Users, 
  Sparkles, 
  Award, 
  Scale,
  CheckCircle2,
  XCircle,
  Cpu
} from 'lucide-react';

export const AboutPage: React.FC = () => {
  return (
    <div className="max-w-5xl mx-auto px-4 py-12 space-y-16">
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto space-y-4">
        <div className="inline-flex items-center gap-2 bg-bayyinah-purple-light text-bayyinah-purple px-4 py-1.5 rounded-full text-xs font-semibold">
          <Award className="w-3.5 h-3.5" />
          <span>المسار الرابع: أدوات المعرفة والتحقق لتمكين المعرفين بالإسلام</span>
        </div>

        <h1 className="text-3xl md:text-5xl font-extrabold text-bayyinah-navy">
          عن مشروع بيّنة AI
        </h1>

        <p className="text-base text-bayyinah-gray-600 leading-relaxed">
          مشروع تقني معرفي رائد يهدف إلى رفع موثوقية المحتوى الإسلامي الرقمي وتمكين الدعاة والمترجمين والمعرفين بالإسلام من التحقق الفوري من صحة النصوص ونسبتها إلى مصادرها المعتمدة قبل النشر.
        </p>
      </div>

      {/* Core Mission & Philosophy */}
      <div className="bg-white rounded-3xl p-8 md:p-10 border border-bayyinah-gray-200 shadow-elevated space-y-6">
        <h2 className="text-xl font-bold text-bayyinah-navy flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-bayyinah-purple" />
          فلسفة بيّنة ورسالتها المعرفية
        </h2>

        <div className="bg-bayyinah-purple-light/50 border border-bayyinah-purple/20 p-5 rounded-2xl">
          <p className="text-sm font-semibold text-bayyinah-navy leading-relaxed">
            «الذكاء الاصطناعي ليس مصدرًا للمعرفة الدينية، ولا يملك سلطة الإفتاء أو الحكم الشرعي؛ وإنما هو أداة تقنية متقدمة للبحث، والربط، واسترجاع الأدلة من مصادرها الموثقة بأمانة علمية.»
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
          <div className="space-y-2">
            <h3 className="text-sm font-bold text-bayyinah-navy">ما نقوم به:</h3>
            <ul className="space-y-2 text-xs text-bayyinah-gray-600 leading-relaxed">
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
                <span>استخراج الادعاءات بدقة وتصنيفها المعرفي.</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
                <span>البحث في سجل المصادر المعتمدة ونصوص التراث المحققة.</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
                <span>عرض الدليل المباشر مع رقمه وسنده ورابطه الرسمي.</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
                <span>إبراز التباين الفقهي المعتبر بأمانة دون تحيز.</span>
              </li>
            </ul>
          </div>

          <div className="space-y-2">
            <h3 className="text-sm font-bold text-rose-800">ما نمتنع عنه تمامًا (Safety Boundaries):</h3>
            <ul className="space-y-2 text-xs text-rose-700 leading-relaxed">
              <li className="flex items-start gap-2">
                <XCircle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
                <span>لا نصدر فتاوى شخصية أو أحكامًا في مسائل الطلاق والنزاعات الأسرية.</span>
              </li>
              <li className="flex items-start gap-2">
                <XCircle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
                <span>لا ندّعي "صفر هلوسة" أو الإحاطة بكل كتب التراث.</span>
              </li>
              <li className="flex items-start gap-2">
                <XCircle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
                <span>لا نحول غياب الدليل في المصادر المفحوصة إلى حكم قطعي بالبطلان.</span>
              </li>
              <li className="flex items-start gap-2">
                <XCircle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
                <span>لا نبتدع تصنيفات حديثية من عندنا.</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Target Audience: Track 4 */}
      <div className="bg-bayyinah-navy text-white rounded-3xl p-8 md:p-10 shadow-xl border border-bayyinah-purple/30 space-y-6">
        <h2 className="text-xl font-bold text-bayyinah-turquoise flex items-center gap-2">
          <Users className="w-5 h-5" />
          الفئات المستفيدة من بيّنة AI
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs text-bayyinah-off-white/80 leading-relaxed">
          <div className="bg-white/5 border border-white/10 rounded-2xl p-4 space-y-1">
            <strong className="text-white text-sm block">1. المعرفون بالإسلام والدعاة</strong>
            <p>للتأكد من صحة النصوص المنقولة والترجمات المعتمدة قبل نشرها للجمهور العالمي.</p>
          </div>
          <div className="bg-white/5 border border-white/10 rounded-2xl p-4 space-y-1">
            <strong className="text-white text-sm block">2. صناع المحتوى والمنصات الدعوية</strong>
            <p>لفحص الاقتباسات والأحاديث الشائعة والمنشورات الرائجة وتفادي نقل الأحاديث الضعيفة والموضوعة.</p>
          </div>
          <div className="bg-white/5 border border-white/10 rounded-2xl p-4 space-y-1">
            <strong className="text-white text-sm block">3. الباحثون والمترجمون</strong>
            <p>للوصول السريع إلى مراجع التخريج الموثقة وأرقام الأبواب في أصح دواوين السنة والتفاسير.</p>
          </div>
        </div>
      </div>

      {/* Model Specifications Card (Section 34) */}
      <div className="bg-white rounded-3xl p-8 md:p-10 border border-bayyinah-gray-200 shadow-elevated space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <h2 className="text-xl font-bold text-bayyinah-navy flex items-center gap-2">
            <Cpu className="w-5 h-5 text-bayyinah-purple" />
            بطاقة مواصفات نموذج الذكاء الاصطناعي (AI Model Transparency)
          </h2>
          <span className="text-xs bg-emerald-50 text-emerald-700 border border-emerald-200 px-3 py-1 rounded-full font-bold self-start sm:self-auto">
            Google GenAI SDK 2.27.0
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 text-xs">
          <div className="bg-bayyinah-off-white p-4 rounded-2xl border border-bayyinah-gray-200">
            <span className="text-bayyinah-gray-500 block mb-1">Model</span>
            <span className="text-base font-bold text-bayyinah-navy font-mono">Gemini 3.8 Flash</span>
          </div>

          <div className="bg-bayyinah-off-white p-4 rounded-2xl border border-bayyinah-gray-200">
            <span className="text-bayyinah-gray-500 block mb-1">Multimodal</span>
            <span className="text-base font-bold text-emerald-600 flex items-center gap-1">
              <CheckCircle2 className="w-4 h-4" /> Yes (OCR & Image Analysis)
            </span>
          </div>

          <div className="bg-bayyinah-off-white p-4 rounded-2xl border border-bayyinah-gray-200">
            <span className="text-bayyinah-gray-500 block mb-1">Function Calling</span>
            <span className="text-base font-bold text-emerald-600 flex items-center gap-1">
              <CheckCircle2 className="w-4 h-4" /> Yes (7 Verification Tools)
            </span>
          </div>

          <div className="bg-bayyinah-off-white p-4 rounded-2xl border border-bayyinah-gray-200">
            <span className="text-bayyinah-gray-500 block mb-1">Structured Outputs</span>
            <span className="text-base font-bold text-emerald-600 flex items-center gap-1">
              <CheckCircle2 className="w-4 h-4" /> Yes (Pydantic Schemas)
            </span>
          </div>

          <div className="bg-bayyinah-off-white p-4 rounded-2xl border border-bayyinah-gray-200">
            <span className="text-bayyinah-gray-500 block mb-1">Thinking Policy</span>
            <span className="text-base font-bold text-bayyinah-purple font-mono">Medium / High</span>
          </div>

          <div className="bg-bayyinah-off-white p-4 rounded-2xl border border-bayyinah-gray-200">
            <span className="text-bayyinah-gray-500 block mb-1">Vector Embedding</span>
            <span className="text-base font-bold text-bayyinah-navy font-mono">text-embedding-004</span>
          </div>
        </div>

        <div className="bg-bayyinah-purple-light/40 border border-bayyinah-purple/20 p-4 rounded-2xl text-xs text-bayyinah-navy leading-relaxed">
          <strong className="block mb-1 font-bold">Role:</strong>
          <span>Analysis, retrieval orchestration, evidence validation and grounded response. (الذكاء الاصطناعي وسيلة فهم وبحث وتوثيق واسترجاع للأدلة، وليس مصدراً مستقلاً للفتوى أو الحكم الشرعي).</span>
        </div>
      </div>
    </div>
  );
};
