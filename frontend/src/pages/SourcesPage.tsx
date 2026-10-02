import React, { useState, useEffect } from 'react';
import { 
  BookOpen, 
  ExternalLink, 
  ShieldCheck, 
  Search, 
  Filter, 
  CheckCircle2, 
  Info,
  Scale
} from 'lucide-react';
import { SourceRegistryItem } from '../types';
import { api } from '../services/api';

export const SourcesPage: React.FC = () => {
  const [sources, setSources] = useState<SourceRegistryItem[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSources();
  }, [selectedCategory]);

  const loadSources = async () => {
    try {
      setLoading(true);
      const data = await api.getSources(selectedCategory);
      setSources(data);
    } catch (err) {
      console.error('Failed to load sources:', err);
    } finally {
      setLoading(false);
    }
  };

  const categories = [
    { id: 'all', label: 'جميع المصادر' },
    { id: 'quran', label: 'القرآن الكريم' },
    { id: 'hadith', label: 'الحديث الشريف' },
    { id: 'tafsir', label: 'التفسير' },
    { id: 'fiqh', label: 'الفقه والأصول' },
    { id: 'fatwa', label: 'الفتاوى المعتمدة' },
    { id: 'seerah', label: 'السيرة والتاريخ' },
  ];

  const filteredSources = sources.filter(s => {
    const q = searchQuery.toLowerCase();
    return s.name.toLowerCase().includes(q) || 
           (s.author && s.author.toLowerCase().includes(q)) || 
           (s.description && s.description.toLowerCase().includes(q));
  });

  return (
    <div className="max-w-6xl mx-auto px-4 py-12 space-y-12">
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto space-y-4">
        <div className="inline-flex items-center gap-2 bg-bayyinah-purple-light text-bayyinah-purple px-4 py-1.5 rounded-full text-xs font-semibold">
          <BookOpen className="w-3.5 h-3.5" />
          <span>سياسة المصادر وسجل المراجع الموثقة</span>
        </div>

        <h1 className="text-3xl md:text-4xl font-bold text-bayyinah-navy">
          سجل المصادر المعرفية المعتمدة (Source Registry)
        </h1>

        <p className="text-sm md:text-base text-bayyinah-gray-600 leading-relaxed">
          تعتمد بيّنة AI على سياسة معرفية صارمة؛ فلا يُستخرج الدليل إلا من قواعد ومصادر معتمدة ومعلنة وموثقة بروابطها وحقوق استخدامها وأصحابها.
        </p>
      </div>

      {/* Source Policy Principles Box */}
      <div className="bg-bayyinah-navy text-white rounded-3xl p-6 md:p-8 shadow-xl border border-bayyinah-purple/30">
        <h3 className="text-base font-bold text-bayyinah-turquoise mb-3 flex items-center gap-2">
          <ShieldCheck className="w-5 h-5" />
          مبادئ وسياسة المصادر في بيّنة AI:
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-bayyinah-off-white/80 leading-relaxed">
          <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
            <strong className="text-white block mb-1">1. قابلية التتبع الكاملة:</strong>
            كل دليل مسترجع مرتبط مباشرة باسم المرجع ورقم الحديث أو الآية ورابطه المعتمد.
          </div>
          <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
            <strong className="text-white block mb-1">2. حماية حقوق النشر:</strong>
            لا نقوم بنسخ محتوى ضخم، بل نكتفي بالمقتطفات اللازمة للاستدلال مع الإحالة للرابط الأصلي.
          </div>
          <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
            <strong className="text-white block mb-1">3. إسناد الخلاف بأمانة:</strong>
            عند تعدد الأقوال الفقهية المعتبرة يتم إسناد كل رأي إلى مدرسته الفقهية ومصدره الرسمي.
          </div>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Category Tabs */}
        <div className="flex items-center gap-1.5 overflow-x-auto w-full md:w-auto pb-2 md:pb-0">
          {categories.map(c => (
            <button
              key={c.id}
              onClick={() => setSelectedCategory(c.id)}
              className={`text-xs font-semibold px-4 py-2 rounded-xl transition-all whitespace-nowrap ${
                selectedCategory === c.id
                  ? 'bg-bayyinah-purple text-white shadow-subtle'
                  : 'bg-white text-bayyinah-navy border border-bayyinah-gray-200 hover:bg-bayyinah-off-white'
              }`}
            >
              {c.label}
            </button>
          ))}
        </div>

        {/* Search Input */}
        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 text-bayyinah-gray-400 absolute right-3.5 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            placeholder="ابحث في سجل المصادر..."
            className="w-full bg-white border border-bayyinah-gray-200 rounded-xl pr-10 pl-4 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-bayyinah-purple"
          />
        </div>
      </div>

      {/* Sources Grid */}
      {loading ? (
        <div className="text-center py-12 text-sm text-bayyinah-gray-500">
          جاري تحميل سجل المصادر المعتمدة...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredSources.map((src) => (
            <div
              key={src.id}
              className="bg-white rounded-3xl p-6 md:p-7 border border-bayyinah-gray-200 shadow-subtle hover:border-bayyinah-purple/50 transition-all space-y-4 flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <span className="text-[10px] font-semibold uppercase tracking-wider bg-bayyinah-off-white text-bayyinah-purple px-2.5 py-0.5 rounded-full border border-bayyinah-gray-200">
                      {src.category}
                    </span>
                    <h3 className="text-base font-bold text-bayyinah-navy mt-1.5">{src.name}</h3>
                  </div>

                  <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200 flex-shrink-0">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>معتمد ونشط</span>
                  </span>
                </div>

                {src.author && (
                  <p className="text-xs text-bayyinah-gray-600">
                    <strong className="text-bayyinah-navy">المؤلف/المحقق: </strong>
                    {src.author}
                  </p>
                )}

                {src.organization && (
                  <p className="text-xs text-bayyinah-gray-600">
                    <strong className="text-bayyinah-navy">الجهة المشرفة: </strong>
                    {src.organization}
                  </p>
                )}

                <p className="text-xs text-bayyinah-gray-700 leading-relaxed bg-bayyinah-off-white/60 p-3 rounded-xl border border-bayyinah-gray-100">
                  {src.description}
                </p>

                {src.usage_policy && (
                  <div className="text-[11px] text-bayyinah-gray-500">
                    <strong className="text-bayyinah-navy">ضابط الاستخدام: </strong>
                    <span>{src.usage_policy}</span>
                  </div>
                )}
              </div>

              <div className="pt-4 border-t border-bayyinah-gray-100 flex items-center justify-between text-xs">
                <span className="text-[11px] text-bayyinah-gray-400 font-mono">
                  {src.license}
                </span>

                <a
                  href={src.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 font-semibold text-bayyinah-purple hover:underline"
                >
                  <span>رابط المصدر</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
