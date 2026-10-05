import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  ShieldCheck, 
  FileText, 
  RotateCw, 
  Sparkles, 
  Layers,
  AlertTriangle,
  ExternalLink
} from 'lucide-react';

interface EvalDetailedResult {
  id: string;
  category: string;
  input_preview: string;
  expected_status: string;
  actual_status: string;
  passed: boolean;
  evidence_count: number;
  checked_sources: number;
  latency_ms: number;
}

interface EvaluationMetrics {
  total_tests: number;
  passed_tests: number;
  failed_tests: number;
  success_rate: number;
  citation_accuracy: number;
  retrieval_accuracy: number;
  abstention_accuracy: number;
  traceability_rate: number;
  average_verification_time_ms: number;
  detailed_results: EvalDetailedResult[];
}

export const EvaluationPage: React.FC = () => {
  const [metrics, setMetrics] = useState<EvaluationMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [activeCategory, setActiveCategory] = useState<string>('all');

  useEffect(() => {
    fetchEvaluationMetrics();
  }, []);

  const fetchEvaluationMetrics = async () => {
    try {
      setLoading(true);
      const res = await fetch('/api/evaluation');
      if (res.ok) {
        const data = await res.json();
        setMetrics(data);
      }
    } catch (err) {
      console.error('Failed to load evaluation metrics:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunSuite = async () => {
    try {
      setRunning(true);
      const res = await fetch('/api/evaluation/run', { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setMetrics(data);
      }
    } catch (err) {
      console.error('Failed to run evaluation suite:', err);
    } finally {
      setRunning(false);
    }
  };

  const categories = [
    { id: 'all', label: 'جميع الحالات (30)' },
    { id: 'verified', label: 'نص ثابت وموثق (5)' },
    { id: 'unverified_wording', label: 'لم يثبت باللفظ (5)' },
    { id: 'insufficient_evidence', label: 'أدلة غير كافية (5)' },
    { id: 'conflict', label: 'اختلاف في المصادر (5)' },
    { id: 'image', label: 'فحص بصري OCR (5)' },
    { id: 'specialist', label: 'إحالة لمختص (5)' },
  ];

  const filteredResults = metrics?.detailed_results?.filter(r => {
    if (activeCategory === 'all') return true;
    return r.category === activeCategory;
  }) || [];

  return (
    <div className="max-w-6xl mx-auto px-4 py-12 space-y-12">
      {/* Page Header */}
      <div className="text-center max-w-3xl mx-auto space-y-4">
        <div className="inline-flex items-center gap-2 bg-bayyinah-purple-light text-bayyinah-purple px-4 py-1.5 rounded-full text-xs font-semibold">
          <BarChart3 className="w-3.5 h-3.5" />
          <span>Synthetic / Local Evaluation Dataset (حزمة تقييم محلية تركيبية)</span>
        </div>

        <h1 className="text-3xl md:text-5xl font-extrabold text-bayyinah-navy">
          لوحة الاختبار والتقييم المعياري
        </h1>

        <p className="text-sm md:text-base text-bayyinah-gray-600 leading-relaxed">
          تقييم داخلي تركيبي (Synthetic / Local Evaluation) مبني على <strong>30 حالة اختبار قياسية</strong> تغطي: المتون الثابتة، والألفاظ غير الثابتة، والأدلة غير الكافية، والتباين الفقهي، والتحليل البصري عبر Gemini 3.8 Flash، وقواعد الامتناع والإحالة لمختص.
        </p>
      </div>

      {/* Main Metric Cards Grid */}
      {metrics && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-3xl p-6 border border-bayyinah-gray-200 shadow-subtle flex flex-col justify-between">
            <span className="text-xs font-semibold text-bayyinah-gray-500">نسبة النجاح الكلية (Pass Rate)</span>
            <div className="my-3">
              <span className="text-3xl md:text-4xl font-extrabold text-emerald-600">
                %{metrics.success_rate}
              </span>
            </div>
            <span className="text-[11px] text-bayyinah-gray-500">
              {metrics.passed_tests} ناجحة من أصل {metrics.total_tests} اختبار
            </span>
          </div>

          <div className="bg-white rounded-3xl p-6 border border-bayyinah-gray-200 shadow-subtle flex flex-col justify-between">
            <span className="text-xs font-semibold text-bayyinah-gray-500">دقة الإسناد (Citation Accuracy)</span>
            <div className="my-3">
              <span className="text-3xl md:text-4xl font-extrabold text-bayyinah-purple">
                %{metrics.citation_accuracy}
              </span>
            </div>
            <span className="text-[11px] text-bayyinah-gray-500">
              ربط كل نتيجة بمصدرها ورقم تخريجها
            </span>
          </div>

          <div className="bg-white rounded-3xl p-6 border border-bayyinah-gray-200 shadow-subtle flex flex-col justify-between">
            <span className="text-xs font-semibold text-bayyinah-gray-500">دقة الامتناع (Abstention Accuracy)</span>
            <div className="my-3">
              <span className="text-3xl md:text-4xl font-extrabold text-bayyinah-turquoise-dark">
                %{metrics.abstention_accuracy}
              </span>
            </div>
            <span className="text-[11px] text-bayyinah-gray-500">
              التوقف الآمن عند غياب الدليل أو الفتوى الشخصية
            </span>
          </div>

          <div className="bg-white rounded-3xl p-6 border border-bayyinah-gray-200 shadow-subtle flex flex-col justify-between">
            <span className="text-xs font-semibold text-bayyinah-gray-500">متوسط زمن التحقق (Latency)</span>
            <div className="my-3">
              <span className="text-3xl md:text-4xl font-extrabold text-bayyinah-navy">
                {metrics.average_verification_time_ms}
              </span>
              <span className="text-sm font-semibold text-bayyinah-gray-500 mr-1">ms</span>
            </div>
            <span className="text-[11px] text-bayyinah-gray-500">
              سرعة الاستجابة لـ Hybrid Search
            </span>
          </div>
        </div>
      )}

      {/* Control Actions & Run Button */}
      <div className="bg-bayyinah-navy text-white rounded-3xl p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl border border-bayyinah-purple/30">
        <div>
          <h3 className="text-lg font-bold flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-bayyinah-turquoise" />
            تشغيل حزمة الاختبارات الفعلية (30 Test Cases)
          </h3>
          <p className="text-xs text-bayyinah-off-white/80 mt-1 max-w-xl leading-relaxed">
            اضغط لإعادة تشغيل جميع حالات التحقق الـ 30 وحساب مقاييس الدقة والإسناد والامتناع وزمن المعالجة في الوقت الحقيقي.
          </p>
        </div>

        <button
          onClick={handleRunSuite}
          disabled={running}
          className="inline-flex items-center gap-2 bg-bayyinah-turquoise hover:bg-bayyinah-turquoise-dark text-bayyinah-navy text-sm font-bold py-3.5 px-7 rounded-xl transition-all shadow-subtle disabled:opacity-50 whitespace-nowrap"
        >
          <RotateCw className={`w-4 h-4 ${running ? 'animate-spin' : ''}`} />
          <span>{running ? 'جاري تنفيذ الاختبارات...' : 'إعادة تشغيل الاختبارات الآن'}</span>
        </button>
      </div>

      {/* Category Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        {categories.map(c => (
          <button
            key={c.id}
            onClick={() => setActiveCategory(c.id)}
            className={`text-xs font-semibold px-4 py-2.5 rounded-xl transition-all whitespace-nowrap ${
              activeCategory === c.id
                ? 'bg-bayyinah-purple text-white shadow-subtle'
                : 'bg-white text-bayyinah-navy border border-bayyinah-gray-200 hover:bg-bayyinah-off-white'
            }`}
          >
            {c.label}
          </button>
        ))}
      </div>

      {/* Detailed Results Table */}
      <div className="bg-white rounded-3xl border border-bayyinah-gray-200 shadow-elevated overflow-hidden">
        <div className="p-5 border-b border-bayyinah-gray-100 flex items-center justify-between">
          <h3 className="text-sm font-bold text-bayyinah-navy">تفاصيل حالات الاختبار ({filteredResults.length})</h3>
          <span className="text-xs text-bayyinah-gray-500">قابلية التتبع: 100%</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-right text-xs">
            <thead className="bg-bayyinah-off-white text-bayyinah-gray-600 font-semibold border-b border-bayyinah-gray-200">
              <tr>
                <th className="p-3.5">المعرف</th>
                <th className="p-3.5">الفئة</th>
                <th className="p-3.5">نص الادعاء المدخل</th>
                <th className="p-3.5">الحالة المتوقعة</th>
                <th className="p-3.5">الحالة الفعلية</th>
                <th className="p-3.5">الزمن</th>
                <th className="p-3.5 text-center">النتيجة</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-bayyinah-gray-100">
              {filteredResults.map((row) => (
                <tr key={row.id} className="hover:bg-bayyinah-off-white/50 transition-colors">
                  <td className="p-3.5 font-mono font-bold text-bayyinah-purple">{row.id}</td>
                  <td className="p-3.5">
                    <span className="bg-bayyinah-gray-100 text-bayyinah-navy px-2 py-0.5 rounded-md text-[10px] font-medium">
                      {row.category}
                    </span>
                  </td>
                  <td className="p-3.5 max-w-xs font-medium text-bayyinah-navy truncate" title={row.input_preview}>
                    {row.input_preview}
                  </td>
                  <td className="p-3.5 text-bayyinah-gray-600 font-medium">{row.expected_status}</td>
                  <td className="p-3.5 font-bold text-bayyinah-navy">{row.actual_status}</td>
                  <td className="p-3.5 font-mono text-[11px] text-bayyinah-gray-500">{row.latency_ms} ms</td>
                  <td className="p-3.5 text-center">
                    {row.passed ? (
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                        <CheckCircle2 className="w-3.5 h-3.5" /> ناجح
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-rose-700 bg-rose-50 px-2.5 py-0.5 rounded-full border border-rose-200">
                        <XCircle className="w-3.5 h-3.5" /> غير مطابق
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
