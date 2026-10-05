import React from 'react';
import { 
  Cpu, 
  Search, 
  Database, 
  ShieldCheck, 
  GitBranch, 
  FileCheck, 
  Sparkles, 
  Layers, 
  Code2, 
  CheckCircle2,
  HelpCircle
} from 'lucide-react';

export const HowItWorksPage: React.FC = () => {
  const tools = [
    { name: 'search_exact_text', desc: 'البحث بالمطابقة اللفظية الدقيقة وأسماء الأبواب وأرقام المراجع' },
    { name: 'search_sources', desc: 'استعلام سجل المصادر المعتمدة وتصنيفاتها المعرفية' },
    { name: 'semantic_search', desc: 'البحث الدلالي المتجهي عبر pgvector والنصوص المتقاربة في المعنى' },
    { name: 'get_source', desc: 'استرجاع بطاقة المصدر والجهة المشرفة والترخيص والرابط' },
    { name: 'get_evidence', desc: 'استخراج المقتطف الدليلي الحرفي وتوثيقه' },
    { name: 'check_conflicts', desc: 'رصد تباين الأقوال والمذاهب الفقهية وتحديد مساحات الخلاف' },
    { name: 'get_reference', desc: 'استرجاع التخريج الكامل ورقم الصفحة والمجلد أو الآية' },
  ];

  return (
    <div className="max-w-5xl mx-auto px-4 py-12 space-y-16">
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto space-y-4">
        <div className="inline-flex items-center gap-2 bg-bayyinah-purple-light text-bayyinah-purple px-4 py-1.5 rounded-full text-xs font-semibold">
          <Cpu className="w-3.5 h-3.5" />
          <span>الهندسة التقنية والمعمارية</span>
        </div>

        <h1 className="text-3xl md:text-4xl font-bold text-bayyinah-navy">
          كيف تعمل منصة بيّنة AI؟
        </h1>

        <p className="text-sm md:text-base text-bayyinah-gray-600 leading-relaxed">
          تعمل بيّنة كمنظومة استدلالية متكاملة تدمج بين الذكاء الاصطناعي متعدد الوسائط (Gemini 3.8 Flash مع سياسات التفكير Medium/High)، والبحث الهجين (Hybrid Search)، ومحرك التثبت من الأدلة الموثقة (Grounded RAG).
        </p>
      </div>

      {/* RAG Architecture Diagram Section */}
      <section className="bg-white rounded-3xl p-8 md:p-10 border border-bayyinah-gray-200 shadow-elevated space-y-6">
        <h2 className="text-xl font-bold text-bayyinah-navy flex items-center gap-2">
          <Layers className="w-5 h-5 text-bayyinah-purple" />
          معمارية RAG الموجهة بالأدلة (Evidence-Grounded RAG)
        </h2>

        <p className="text-xs md:text-sm text-bayyinah-gray-600 leading-relaxed">
          النموذج اللغوي لا يولد الأحكام الدينية من ذاكرته التوليدية، بل يتبع مسارًا صارمًا:
        </p>

        {/* Pipeline Grid Steps */}
        <div className="grid grid-cols-1 md:grid-cols-7 gap-2 pt-2 text-center text-xs font-semibold">
          {[
            { step: '1', title: 'Content', desc: 'المحتوى المدخل' },
            { step: '2', title: 'Claim', desc: 'استخراج الادعاء' },
            { step: '3', title: 'Search', desc: 'توليد الاستعلام' },
            { step: '4', title: 'Retrieval', desc: 'استرجاع الأدلة' },
            { step: '5', title: 'Validation', desc: 'فحص المطابقة' },
            { step: '6', title: 'Source', desc: 'توثيق المرجع' },
            { step: '7', title: 'Result', desc: 'إعلان النتيجة' }
          ].map((item, idx) => (
            <div key={idx} className="bg-bayyinah-off-white rounded-2xl p-4 border border-bayyinah-gray-200 flex flex-col justify-center items-center">
              <span className="w-6 h-6 rounded-full bg-bayyinah-purple text-white text-[11px] font-bold flex items-center justify-center mb-2">
                {item.step}
              </span>
              <span className="text-bayyinah-navy text-sm font-bold">{item.title}</span>
              <span className="text-[11px] text-bayyinah-gray-500 font-normal mt-1">{item.desc}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Hybrid Search Architecture */}
      <section className="bg-bayyinah-navy text-white rounded-3xl p-8 md:p-10 shadow-xl border border-bayyinah-purple/30 space-y-6">
        <h2 className="text-xl font-bold text-bayyinah-turquoise flex items-center gap-2">
          <Search className="w-5 h-5" />
          البحث الهجين (Hybrid Search Engine)
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs text-bayyinah-off-white/80 leading-relaxed">
          <div className="bg-white/5 border border-white/10 rounded-2xl p-5 space-y-2">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Database className="w-4 h-4 text-bayyinah-purple" />
              1. البحث بالكلمات الدقيقة (Exact FTS):
            </h3>
            <p>
              يستخدم PostgreSQL Full Text Search مع المعالجة اللغوية المخصصة للعربية (إزالة التشكيل، وتوحيد الهمزات والتاء المربوطة) للوصول إلى النصوص المطابقة بدقة 100%.
            </p>
          </div>

          <div className="bg-white/5 border border-white/10 rounded-2xl p-5 space-y-2">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-bayyinah-turquoise" />
              2. البحث الدلالي (Semantic pgvector):
            </h3>
            <p>
              يقوم بتوليد Embeddings عبر Gemini text-embedding-004 ومقارنتها عبر مسافة الجيب تمام (Cosine Distance) داخل pgvector للعثور على النصوص المشابهة في المعنى حتى مع اختلاف الصياغة.
            </p>
          </div>
        </div>
      </section>

      {/* Gemini Function Calling & Tool Use */}
      <section className="bg-white rounded-3xl p-8 md:p-10 border border-bayyinah-gray-200 shadow-elevated space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-bayyinah-navy flex items-center gap-2">
            <Code2 className="w-5 h-5 text-bayyinah-purple" />
            أدوات Gemini 3.8 Flash التفاعلية (Function Calling / Tool Orchestration)
          </h2>
          <span className="text-xs bg-bayyinah-purple-light text-bayyinah-purple px-3 py-1 rounded-full font-semibold">
            7 أدوات معيارية (Thinking: High)
          </span>
        </div>

        <p className="text-xs md:text-sm text-bayyinah-gray-600 leading-relaxed">
          يقرر النموذج استدعاء الأدوات البرمجية المحددة للبحث وفحص المراجع، ولا يُسمح له بالإجابة من معرفته المسبقة إذا كانت الإجابة دينية:
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {tools.map((tool, i) => (
            <div key={i} className="bg-bayyinah-off-white/80 p-4 rounded-2xl border border-bayyinah-gray-200 space-y-1">
              <span className="text-xs font-mono font-bold text-bayyinah-purple bg-white px-2 py-0.5 rounded-md border border-bayyinah-gray-200 inline-block">
                {tool.name}()
              </span>
              <p className="text-xs text-bayyinah-gray-600 leading-relaxed pt-1">
                {tool.desc}
              </p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};
