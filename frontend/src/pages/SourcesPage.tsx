import React, { useState, useEffect } from 'react';
import { 
  BookOpen, 
  ExternalLink, 
  ShieldCheck, 
  Search, 
  Filter, 
  CheckCircle2, 
  AlertCircle,
  Clock,
  Layers,
  FileText,
  Info,
  Scale,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { TrustedSourceDetail } from '../types';
import { api } from '../services/api';

export const SourcesPage: React.FC = () => {
  const [sources, setSources] = useState<TrustedSourceDetail[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [expandedSourceId, setExpandedSourceId] = useState<string | null>(null);

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
    { id: 'QURAN', label: 'القرآن وعلومه' },
    { id: 'HADITH', label: 'الحديث الشريف' },
    { id: 'TAFSEER', label: 'التفسير' },
    { id: 'FIQH', label: 'الفقه والأصول' },
    { id: 'DAWA', label: 'الدعوة والتعريف بالإسلام' },
    { id: 'SEERAH_HISTORY', label: 'السيرة والتاريخ' },
    { id: 'DICTIONARY_TRANSLATION', label: 'المعاجم والترجمة' },
  ];

  const filteredSources = sources.filter(s => {
    const q = searchQuery.toLowerCase();
    const nameAr = (s.name_ar || '').toLowerCase();
    const nameEn = (s.name_en || '').toLowerCase();
    const desc = (s.description || '').toLowerCase();
    return nameAr.includes(q) || nameEn.includes(q) || desc.includes(q);
  });

  const getTrustBadge = (status: string) => {
    switch (status) {
      case 'APPROVED':
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>معتمد ونشط</span>
          </span>
        );
      case 'REVIEW_REQUIRED':
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-bold text-amber-700 bg-amber-50 px-2.5 py-0.5 rounded-full border border-amber-200">
            <Clock className="w-3.5 h-3.5" />
            <span>قيد المراجعة</span>
          </span>
        );
      case 'RESTRICTED':
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-bold text-orange-700 bg-orange-50 px-2.5 py-0.5 rounded-full border border-orange-200">
            <AlertCircle className="w-3.5 h-3.5" />
            <span>مقيد الاستخدام</span>
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-bold text-red-700 bg-red-50 px-2.5 py-0.5 rounded-full border border-red-200">
            <AlertCircle className="w-3.5 h-3.5" />
            <span>معطل</span>
          </span>
        );
    }
  };

  const getLicenseBadge = (licenseStatus: string) => {
    switch (licenseStatus) {
      case 'VERIFIED':
        return (
          <span className="text-[10px] font-semibold bg-blue-50 text-blue-700 border border-blue-200 px-2 py-0.5 rounded-md">
            ترخيص موثق
          </span>
        );
      case 'PENDING_VERIFICATION':
        return (
          <span className="text-[10px] font-semibold bg-amber-50 text-amber-800 border border-amber-200 px-2 py-0.5 rounded-md" title="المحتوى مرجعي ومقيد بالمقتطفات لحين استكمال التحقق من حقوق إعادة النشر">
            حقوق الاستخدام: قيد التحقق
          </span>
        );
      default:
        return (
          <span className="text-[10px] font-semibold bg-gray-100 text-gray-700 border border-gray-300 px-2 py-0.5 rounded-md">
            مرجع إحالة
          </span>
        );
    }
  };

  const renderAllowedOps = (ops: Record<string, boolean> | undefined) => {
    if (!ops || typeof ops !== 'object') return <span className="text-[10px] text-gray-400">إحالة برابط</span>;
    const labels: Record<string, string> = {
      DISPLAY_EXCERPT: 'عرض المقتطف',
      display_excerpt: 'عرض المقتطف',
      LINK_TO_SOURCE: 'إحالة بالرابط',
      link_to_source: 'إحالة بالرابط',
      TRANSLATE: 'ترجمة شرعية',
      translate: 'ترجمة شرعية',
      INDEX_CONTENT: 'فهرسة دقيقة',
      index_content: 'فهرسة دقيقة',
      STORE_CONTENT: 'تخزين كامل',
      store_content: 'تخزين كامل',
      DERIVE_EMBEDDINGS: 'تضمين دلالي',
      derive_embeddings: 'تضمين دلالي'
    };
    const active = Object.entries(ops).filter(([_, v]) => Boolean(v)).map(([k]) => labels[k] || k);
    if (active.length === 0) {
      return <span className="text-[10px] text-amber-700 bg-amber-50 px-2 py-0.5 rounded">إحالة بالرابط فقط</span>;
    }
    return (
      <div className="flex flex-wrap gap-1 mt-1">
        {active.slice(0, 4).map((label, idx) => (
          <span key={idx} className="text-[10px] bg-bayyinah-purple-light/60 text-bayyinah-purple font-medium px-2 py-0.5 rounded-md border border-bayyinah-purple/20">
            {label}
          </span>
        ))}
      </div>
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-12 space-y-10">
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto space-y-4">
        <div className="inline-flex items-center gap-2 bg-bayyinah-purple-light text-bayyinah-purple px-4 py-1.5 rounded-full text-xs font-semibold">
          <BookOpen className="w-3.5 h-3.5" />
          <span>الحزمة العلمية وحوكمة المراجع الموثقة</span>
        </div>

        <h1 className="text-3xl md:text-4xl font-bold text-bayyinah-navy">
          سجل المصادر المعرفية المعتمدة (Source Registry)
        </h1>

        <p className="text-sm md:text-base text-bayyinah-gray-600 leading-relaxed">
          تعتمد بيّنة AI على سياسة معرفية صارمة؛ فلا يُستخرج الدليل إلا من مصادر مسجلة وموثقة بحوكمتها، ونطاقها المعرفي، وحقوق استخدامها، وقابلية تتبعها الكاملة.
        </p>
      </div>

      {/* Governance & Licensing Principles */}
      <div className="bg-bayyinah-navy text-white rounded-3xl p-6 md:p-8 shadow-xl border border-bayyinah-purple/30">
        <h3 className="text-base font-bold text-bayyinah-turquoise mb-4 flex items-center gap-2">
          <ShieldCheck className="w-5 h-5" />
          مبادئ حوكمة المصادر وضوابط حقوق النشر:
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs text-bayyinah-off-white/80 leading-relaxed">
          <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
            <strong className="text-white block mb-1">1. التتبع الصارم (Provenance):</strong>
            كل دليل مسترجع موثق ببصمة محتوى SHA-256 ورقم الوثيقة وموقعها الدقيق في المصدر.
          </div>
          <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
            <strong className="text-white block mb-1">2. حماية حقوق الاستخدام:</strong>
            المصادر غير المحسومة في رخصة إعادة النشر تصنف <span className="text-bayyinah-turquoise">Pending Verification</span> ولا يُخزن محتواها كاملاً بل يُكتفى بالمقتطفات والإحالة.
          </div>
          <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
            <strong className="text-white block mb-1">3. أمانة الخلاف الفقهي:</strong>
            لا يُرجح النظام قولاً من تلقاء نفسه، بل يعرض الخلاف المعتبر مع عزو كل قول لمدرسته.
          </div>
          <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
            <strong className="text-white block mb-1">4. منع الإفتاء الآلي (Level D):</strong>
            المسائل الشخصية والنوازل لا تصدر فيها أحكام آلية وتُحال وجوباً للجهات الرسمية.
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
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-bayyinah-gray-400 absolute right-3.5 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            placeholder="ابحث بالاسم أو النطاق أو الفئة..."
            className="w-full bg-white border border-bayyinah-gray-200 rounded-xl pr-10 pl-4 py-2.5 text-xs focus:outline-none focus:ring-2 focus:ring-bayyinah-purple shadow-sm"
          />
        </div>
      </div>

      {/* Sources Grid */}
      {loading ? (
        <div className="text-center py-16 text-sm text-bayyinah-gray-500">
          جاري استرجاع سجل المصادر المعتمدة من قاعدة البيانات...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredSources.map((src) => {
            const isExpanded = expandedSourceId === src.id;
            return (
              <div
                key={src.id}
                className="bg-white rounded-3xl p-6 border border-bayyinah-gray-200 shadow-subtle hover:border-bayyinah-purple/40 transition-all flex flex-col justify-between space-y-4"
              >
                <div className="space-y-3">
                  {/* Top Badges */}
                  <div className="flex items-start justify-between gap-2">
                    <span className="text-[10px] font-bold uppercase tracking-wider bg-bayyinah-purple-light text-bayyinah-purple px-2.5 py-0.5 rounded-full border border-bayyinah-purple/20">
                      {src.category}
                    </span>
                    <div className="flex items-center gap-1.5 flex-wrap justify-end">
                      {getTrustBadge(src.trust_status)}
                    </div>
                  </div>

                  <div>
                    <h3 className="text-base font-bold text-bayyinah-navy leading-snug">
                      {src.name_ar}
                    </h3>
                    {src.name_en && (
                      <span className="text-[11px] text-bayyinah-gray-400 block font-mono">
                        {src.name_en}
                      </span>
                    )}
                  </div>

                  <p className="text-xs text-bayyinah-gray-600 leading-relaxed bg-bayyinah-off-white/70 p-3 rounded-2xl border border-bayyinah-gray-100 line-clamp-3">
                    {src.description}
                  </p>

                  {/* Metadata Stats */}
                  <div className="grid grid-cols-2 gap-2 text-[11px] pt-1">
                    <div className="flex items-center gap-1.5 text-bayyinah-gray-600 bg-gray-50 p-2 rounded-xl border border-gray-100">
                      <FileText className="w-3.5 h-3.5 text-bayyinah-purple" />
                      <span><strong>الوثائق:</strong> {src.documents_count > 0 ? `${src.documents_count} وثيقة` : 'قيد الفهرسة'}</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-bayyinah-gray-600 bg-gray-50 p-2 rounded-xl border border-gray-100">
                      <Layers className="w-3.5 h-3.5 text-bayyinah-turquoise" />
                      <span><strong>المقاطع:</strong> {src.chunks_count > 0 ? `${src.chunks_count} مقطع` : 'قيد التجزئة'}</span>
                    </div>
                  </div>

                  {/* Scientific Status & License Badges */}
                  <div className="pt-1 space-y-2">
                    <div className="flex items-center justify-between text-[11px]">
                      <span className="text-bayyinah-gray-500 font-medium">الحالة العلمية:</span>
                      <span className="font-semibold text-bayyinah-navy bg-bayyinah-off-white px-2 py-0.5 rounded border border-gray-200">
                        {src.authority_level || 'مرجع أصيل معتمد'}
                      </span>
                    </div>

                    <div className="flex items-center justify-between text-[11px]">
                      <span className="text-bayyinah-gray-500 font-medium">حالة الترخيص:</span>
                      {getLicenseBadge(src.license_status)}
                    </div>

                    <div className="text-[11px]">
                      <span className="text-bayyinah-gray-500 font-medium block">العمليات المسموح بها:</span>
                      {renderAllowedOps(src.allowed_operations)}
                    </div>

                    {src.last_verified_at && (
                      <div className="flex items-center justify-between text-[10px] text-bayyinah-gray-400 pt-1">
                        <span>تاريخ آخر تحقق:</span>
                        <span>{new Date(src.last_verified_at).toLocaleDateString('ar-SA')}</span>
                      </div>
                    )}
                  </div>

                  {/* Expandable Governance Details */}
                  {isExpanded && (
                    <div className="pt-3 border-t border-bayyinah-gray-100 space-y-2.5 text-xs text-bayyinah-gray-600 bg-gray-50/70 p-3.5 rounded-2xl">
                      {src.content_scope && (
                        <div>
                          <strong className="text-bayyinah-navy block mb-0.5">نطاق المحتوى:</strong>
                          <span>{src.content_scope}</span>
                        </div>
                      )}
                      {src.verification_notes && (
                        <div>
                          <strong className="text-bayyinah-navy block mb-0.5">ملاحظات التحقق والاعتماد:</strong>
                          <span>{src.verification_notes}</span>
                        </div>
                      )}
                      {src.author && (
                        <div>
                          <strong className="text-bayyinah-navy block mb-0.5">المؤلف / المحقق:</strong>
                          <span>{src.author}</span>
                        </div>
                      )}
                      {src.publisher && (
                        <div>
                          <strong className="text-bayyinah-navy block mb-0.5">الناشر / الجهة المشرفة:</strong>
                          <span>{src.publisher}</span>
                        </div>
                      )}
                      {src.last_verified_at && (
                        <div className="text-[10px] text-bayyinah-gray-400">
                          آخر مراجعة علمية: {new Date(src.last_verified_at).toLocaleDateString('ar-SA')}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Card Footer Actions */}
                <div className="pt-3 border-t border-bayyinah-gray-100 flex items-center justify-between text-xs">
                  <button
                    onClick={() => setExpandedSourceId(isExpanded ? null : src.id)}
                    className="inline-flex items-center gap-1 text-bayyinah-purple hover:underline text-[11px] font-semibold"
                  >
                    <span>{isExpanded ? 'إخفاء التفاصيل' : 'تفاصيل الحوكمة'}</span>
                    {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                  </button>

                  <a
                    href={src.official_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 font-bold text-bayyinah-navy hover:text-bayyinah-purple text-xs"
                  >
                    <span>زيارة المصدر</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
