import React, { useState } from 'react';
import { 
  BookOpen, 
  Search, 
  ExternalLink, 
  CheckCircle2, 
  ShieldCheck, 
  Layers, 
  ArrowLeft,
  FileText,
  Compass
} from 'lucide-react';

interface DomainCard {
  id: string;
  name: string;
  category: string;
  verifiedScope: string;
  approvedSources: Array<{ name: string; url: string; authority: string }>;
  indexedCount: string;
  lastUpdated: string;
  details: string;
}

const DOMAINS: DomainCard[] = [
  {
    id: 'quran',
    name: 'القرآن الكريم',
    category: 'QURAN',
    verifiedScope: 'مطابقة الآيات، صحة الرسم العثماني، التشكيل، أسماء السور وأرقام الآيات، ونفي التحريف أو الزيادة.',
    approvedSources: [
      { name: 'موسوعة القرآن الكريم (Quranpedia)', url: 'https://quranpedia.net', authority: 'موسوعة مصحفية معتمدة' },
      { name: 'منصة المحتوى الإسلامي', url: 'https://islamic-content.com', authority: 'منصة معتمدة' }
    ],
    indexedCount: '6,236 آية وسورة مفهرسة',
    lastUpdated: 'محدث تلقائياً',
    details: 'فحص فوري ودقيق للمتون القرآنية مع منع الخلط بين الآيات والأحاديث.'
  },
  {
    id: 'hadith',
    name: 'السنة والحديث النبوي',
    category: 'HADITH',
    verifiedScope: 'تخريج الأحاديث، بيان الصحة والضعف والوضع بحسب المصدر، ثبوت الألفاظ، وبيان الأحاديث المشتهرة غير الثابتة.',
    approvedSources: [
      { name: 'موسوعة الدرر السنية الحديثية', url: 'https://dorar.net/hadith', authority: 'الموسوعة الحديثية المعتمدة' },
      { name: 'المكتبة الشاملة', url: 'https://shamela.ws', authority: 'ديوان السنة وكتب التخريج' }
    ],
    indexedCount: '35,000+ حديث ومسند',
    lastUpdated: 'ربط مباشر بالموسوعات الحديثية',
    details: 'مطابقة المتن والسند ودرجة الرواية مع التزام تام بعدم إطلاق الحكم إلا بنص المصدر.'
  },
  {
    id: 'tafseer',
    name: 'التفسير وعلوم القرآن',
    category: 'TAFSEER',
    verifiedScope: 'معاني الآيات، أسباب النزول، أقوال السلف، ونفي التفسيرات الباطلة أو المحرفة المنقولة بلا سند.',
    approvedSources: [
      { name: 'موسوعة التفسير - الدرر السنية', url: 'https://dorar.net/tafseer', authority: 'موسوعة التفسير المعتمدة' },
      { name: 'المكتبة الشاملة - كتب التفاسير', url: 'https://shamela.ws', authority: 'أمهات كتب التفسير' }
    ],
    indexedCount: '12+ تفسيراً معتمداً',
    lastUpdated: 'مفهرس وموثق',
    details: 'الرجوع إلى التفاسير المسندة لبيان المراد الشرعي وتتبع النقول.'
  },
  {
    id: 'aqeedah',
    name: 'العقيدة وأصول الدين',
    category: 'AQEEDAH',
    verifiedScope: 'أصول الإيمان، القضايا العقدية الكبرى، تصحيح المفاهيم، والتحقق من النقول المنسوبة لأئمة السلف.',
    approvedSources: [
      { name: 'موسوعة العقيدة - الدرر السنية', url: 'https://dorar.net/aqeeda', authority: 'موسوعة العقيدة المعتمدة' },
      { name: 'المكتبة الشاملة - كتب أصول الدين', url: 'https://shamela.ws', authority: 'متون أصول السنة' }
    ],
    indexedCount: '1,500+ مسألة عقدية',
    lastUpdated: 'محدث',
    details: 'فحص النصوص العقدية ومنع نسبة أقوال مجتزأة أو محرفة إلى العلماء.'
  },
  {
    id: 'fiqh',
    name: 'الفقه والأحكام الشرعية',
    category: 'FIQH',
    verifiedScope: 'المسائل الفقهية، المذاهب الأربعة، إسناد كل قول لمدرسته الفقهية، وإحالة النوازل الشخصية للمفتين المختصين.',
    approvedSources: [
      { name: 'الموسوعة الفقهية - الدرر السنية', url: 'https://dorar.net/feqhia', authority: 'الموسوعة الفقهية المعتمدة' },
      { name: 'المكتبة الشاملة - كتب الفقه المقارن', url: 'https://shamela.ws', authority: 'دواوين المذاهب الفقهية' }
    ],
    indexedCount: '18,000+ فرع ومسألة فقهية',
    lastUpdated: 'محدث',
    details: 'كشف الخلاف الفقهي بأمانة علمية دون ترجيح شخصي، والامتناع عن الفتاوى الشخصية.'
  },
  {
    id: 'seerah',
    name: 'السيرة النبوية والتاريخ',
    category: 'SEERAH_HISTORY',
    verifiedScope: 'وقائع السيرة النبوية، الغزوات، حياة الصحابة الكرام، والتحقق من الروايات التاريخية المشتهرة الضعيفة.',
    approvedSources: [
      { name: 'موسوعة التاريخ والسيرة - الدرر السنية', url: 'https://dorar.net/history', authority: 'الموسوعة التاريخية المعتمدة' },
      { name: 'المكتبة الشاملة - كتب السيرة المسندة', url: 'https://shamela.ws', authority: 'سير أعلام النبلاء وأمهات السير' }
    ],
    indexedCount: '5,000+ حدث ورواية تاريخية',
    lastUpdated: 'مفهرس بالكامل',
    details: 'تمييز الروايات الثابتة في السيرة عما اشتهر في القصص الشعبية دون إسناد.'
  },
  {
    id: 'questions_doubts',
    name: 'الشبهات والأسئلة الفكرية',
    category: 'QUESTIONS_DOUBTS',
    verifiedScope: 'الرد على الشبهات المثارة، أدوات المعرفة والتحقق لتمكين المعرفين بالإسلام، وتوثيق براهين الوحي والعقل.',
    approvedSources: [
      { name: 'مركز دعوة للدراسات (Dawa Center)', url: 'https://dawa.center', authority: 'المركز الرسمي المعتمد' },
      { name: 'ملف الأدوات والتحقق (الملف 7937)', url: 'https://dawa.center/file/7937', authority: 'الحزمة العلمية الرسمية للتحدي' }
    ],
    indexedCount: '4,200+ مادة وبحث موثق',
    lastUpdated: 'حزمة التحدي الرسمية 2026',
    details: 'أجوبة علمية محكمة مدعومة بالأدلة المقارنة والمصادر الأكاديمية المحكمة.'
  },
  {
    id: 'dictionary_translation',
    name: 'المصطلحات والترجمة الشرعية',
    category: 'DICTIONARY_TRANSLATION',
    verifiedScope: 'معاجم المصطلحات الشرعية، الترجمات المعتمدة للمفاهيم الإسلامية باللغة الإنجليزية، وضوابط الاستخدام المعجمي.',
    approvedSources: [
      { name: 'معجم المصطلحات الشرعية والجمهرة', url: 'https://islamic-content.com/dictionary', authority: 'المعجم الرسمي المعتمد' },
      { name: 'بوابة المحتوى الإسلامي', url: 'https://islamic-content.com', authority: 'الموسوعة اللغوية والترجمة' }
    ],
    indexedCount: '2,800+ مصطلح معتمد ومترجم',
    lastUpdated: 'نسخة المعاجم المعتمدة 2026',
    details: 'منع الترجمات المشوهة والتحقق من دقة التعبير عن المفاهيم الإسلامية بلغات العالم.'
  }
];

export const KnowledgeBasePage: React.FC = () => {
  const [selectedDomain, setSelectedDomain] = useState<DomainCard | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const filteredDomains = DOMAINS.filter(d => 
    d.name.includes(searchQuery) || 
    d.verifiedScope.includes(searchQuery) ||
    d.details.includes(searchQuery)
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 min-h-[85vh]">
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto mb-16">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-bayyinah-ivory border border-bayyinah-emerald/20 text-bayyinah-emerald text-xs font-bold mb-4">
          <ShieldCheck className="w-4 h-4" />
          الحزمة العلمية المعتمدة رسمياً
        </div>
        <h1 className="text-4xl md:text-5xl font-bold text-bayyinah-deep-emerald mb-4">المجالات المعرفية وقاعدة المصادر</h1>
        <p className="text-bayyinah-secondary-text text-lg leading-relaxed">
          تعتمد بيّنة AI حصرًا على المصادر الشرعية المحددة في الحزمة العلمية الرسمية، 
          ولا تستخدم محركات البحث العامة كمصدر للحقيقة الشرعية.
        </p>
      </div>

      {/* Search Input */}
      <div className="max-w-xl mx-auto mb-14 relative">
        <input 
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="ابحث في المجالات المعرفية أو نطاق التحقق..."
          className="w-full bg-white border border-gray-200 rounded-2xl px-6 py-4 pl-12 text-sm focus:outline-none focus:border-bayyinah-emerald focus:ring-1 focus:ring-bayyinah-emerald shadow-sm"
        />
        <Search className="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2" />
      </div>

      {/* Domains Grid (8 Domains - Section 51) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {filteredDomains.map((domain) => (
          <div 
            key={domain.id}
            className="bg-white rounded-3xl p-7 border border-gray-100 hover:border-bayyinah-emerald/40 hover:shadow-elevated transition-all flex flex-col justify-between group"
          >
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold px-3 py-1 rounded-lg bg-bayyinah-ivory text-bayyinah-emerald">
                  {domain.category}
                </span>
                <span className="text-xs text-bayyinah-secondary-text">{domain.lastUpdated}</span>
              </div>

              <h3 className="text-xl font-bold text-bayyinah-dark-text mb-3 group-hover:text-bayyinah-emerald transition-colors">
                {domain.name}
              </h3>

              <div className="space-y-3 mb-6">
                <div>
                  <strong className="block text-xs text-bayyinah-secondary-text mb-1">ما الذي تتحقق منه بيّنة؟</strong>
                  <p className="text-xs text-bayyinah-dark-text leading-relaxed line-clamp-3">
                    {domain.verifiedScope}
                  </p>
                </div>

                <div className="pt-2 border-t border-gray-50">
                  <strong className="block text-xs text-bayyinah-secondary-text mb-1.5">المصادر المعتمدة:</strong>
                  <div className="space-y-1">
                    {domain.approvedSources.map((src, i) => (
                      <div key={i} className="text-xs text-bayyinah-emerald font-semibold flex items-center gap-1">
                        <BookOpen className="w-3 h-3 shrink-0" />
                        <span className="truncate">{src.name}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-4 border-t border-gray-100 flex items-center justify-between text-xs">
              <span className="text-bayyinah-secondary-text font-medium">{domain.indexedCount}</span>
              <button 
                onClick={() => setSelectedDomain(domain)}
                className="text-bayyinah-emerald font-bold hover:text-bayyinah-deep-emerald flex items-center gap-1 cursor-pointer"
              >
                <span>استكشف المجال</span>
                <ArrowLeft className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Domain Detail Modal */}
      {selectedDomain && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-2xl w-full p-8 shadow-2xl border border-gray-100 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-bayyinah-dark-text">{selectedDomain.name}</h2>
              <span className="text-xs font-bold px-3 py-1 rounded-full bg-bayyinah-ivory text-bayyinah-emerald">
                {selectedDomain.category}
              </span>
            </div>

            <div className="space-y-6 text-sm mb-8">
              <div>
                <h4 className="font-bold text-bayyinah-dark-text mb-2">ما الذي تتحقق منه بيّنة في هذا المجال؟</h4>
                <p className="text-bayyinah-secondary-text leading-relaxed bg-bayyinah-ivory/60 p-4 rounded-2xl">
                  {selectedDomain.verifiedScope}
                </p>
              </div>

              <div>
                <h4 className="font-bold text-bayyinah-dark-text mb-3">المصادر المعتمدة الرسمية في الحزمة:</h4>
                <div className="space-y-2">
                  {selectedDomain.approvedSources.map((src, idx) => (
                    <div key={idx} className="p-4 rounded-xl border border-gray-100 flex items-center justify-between">
                      <div>
                        <span className="block font-bold text-bayyinah-dark-text">{src.name}</span>
                        <span className="block text-xs text-bayyinah-secondary-text">{src.authority}</span>
                      </div>
                      <a 
                        href={src.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-bayyinah-emerald hover:text-bayyinah-deep-emerald text-xs font-bold flex items-center gap-1"
                      >
                        زيارة المصدر
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 text-xs bg-gray-50 p-4 rounded-xl">
                <div>
                  <span className="text-bayyinah-secondary-text block mb-1">المواد المفهرسة:</span>
                  <strong className="text-bayyinah-dark-text">{selectedDomain.indexedCount}</strong>
                </div>
                <div>
                  <span className="text-bayyinah-secondary-text block mb-1">حالة التحديث والربط:</span>
                  <strong className="text-bayyinah-emerald">{selectedDomain.lastUpdated}</strong>
                </div>
              </div>
            </div>

            <div className="flex justify-end">
              <button 
                onClick={() => setSelectedDomain(null)}
                className="bg-bayyinah-emerald text-white text-sm font-bold px-6 py-2.5 rounded-xl cursor-pointer"
              >
                إغلاق
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
