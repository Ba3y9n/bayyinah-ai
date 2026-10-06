import React, { useState } from 'react';
import { motion, useReducedMotion } from 'framer-motion';
import {
  BookCheck,
  BookMarked,
  BookOpen,
  BookOpenCheck,
  ExternalLink,
  History,
  Info,
  Languages,
  Library,
  MessageCircleQuestion,
  Search,
  Scale
} from 'lucide-react';

const trustedSources = [
  {
    id: '01',
    categoryId: 'DAWA',
    category: 'الموضوعات الدعوية',
    name: 'المستودع الدعوي الرقمي',
    description: 'مستودع رقمي للمحتوى والموضوعات الدعوية.',
    domain: 'dawa.center',
    url: 'https://dawa.center/',
    icon: Library
  },
  {
    id: '02',
    categoryId: 'DAWA',
    category: 'المحتوى الإسلامي',
    name: 'الجمهرة',
    description: 'موسوعة لمفردات ومحتوى إسلامي متعدد المجالات.',
    domain: 'islamic-content.com',
    url: 'https://islamic-content.com/',
    icon: BookOpen
  },
  {
    id: '03',
    categoryId: 'QURAN',
    category: 'القرآن الكريم',
    name: 'القرآن الكريم',
    subtitle: 'Quranpedia',
    description: 'مرجع للنص القرآني والترجمات والمحتوى المرتبط بالقرآن الكريم.',
    domain: 'quranpedia.net',
    url: 'https://quranpedia.net/',
    icon: BookOpen
  },
  {
    id: '04',
    categoryId: 'TAFSEER',
    category: 'التفسير',
    name: 'موسوعة التفسير – الدرر السنية',
    description: 'موسوعة علمية للرجوع إلى التفسير والمادة المتعلقة بشرح الآيات.',
    domain: 'dorar.net/tafseer',
    url: 'https://dorar.net/tafseer',
    icon: BookMarked
  },
  {
    id: '05',
    categoryId: 'HADITH',
    category: 'الحديث النبوي',
    name: 'الموسوعة الحديثية – الدرر السنية',
    description: 'مرجع للبحث في الأحاديث ومصادرها وأحكامها.',
    domain: 'dorar.net/hadith',
    url: 'https://dorar.net/hadith',
    icon: BookCheck
  },
  {
    id: '06',
    categoryId: 'BOOKS',
    category: 'كتب السنة والمراجع',
    name: 'المكتبة الشاملة',
    description: 'مكتبة رقمية للكتب والمراجع الإسلامية.',
    domain: 'shamela.ws',
    url: 'https://shamela.ws/',
    icon: Library
  },
  {
    id: '07',
    categoryId: 'AQEEDAH',
    category: 'العقيدة والتعريف بالإسلام',
    name: 'الموسوعة العقدية – الدرر السنية',
    description: 'مرجع للمادة العقدية والتعريف بمسائل الاعتقاد.',
    domain: 'dorar.net/aqeeda',
    url: 'https://dorar.net/aqeeda',
    icon: BookOpenCheck
  },
  {
    id: '08',
    categoryId: 'FIQH',
    category: 'الفقه العام',
    name: 'الموسوعة الفقهية – الدرر السنية',
    description: 'موسوعة فقهية للمسائل المستندة إلى المذاهب الفقهية.',
    domain: 'dorar.net/feqhia',
    url: 'https://dorar.net/feqhia',
    icon: Scale
  },
  {
    id: '09',
    categoryId: 'SEERAH_HISTORY',
    category: 'السيرة والتاريخ',
    name: 'الموسوعة التاريخية – الدرر السنية',
    description: 'مرجع للسيرة والأحداث والوقائع التاريخية.',
    domain: 'dorar.net/history',
    url: 'https://dorar.net/history',
    icon: History
  },
  {
    id: '10',
    categoryId: 'QUESTIONS_DOUBTS',
    category: 'الشبهات والأسئلة المتكررة',
    name: 'بينات: أسئلة وأجوبة عن الإسلام',
    description: 'مادة للأسئلة والأجوبة عن الإسلام ومعالجة الشبهات العامة.',
    domain: 'dawa.center/file/7937',
    url: 'https://dawa.center/file/7937',
    icon: MessageCircleQuestion
  },
  {
    id: '11',
    categoryId: 'DICTIONARY_TRANSLATION',
    category: 'الترجمة والمصطلحات',
    name: 'موسوعة الجمهرة – مفردات المحتوى الإسلامي',
    description: 'قاموس وموسوعة للمصطلحات ومفردات المحتوى الإسلامي.',
    domain: 'islamic-content.com/dictionary',
    url: 'https://islamic-content.com/dictionary',
    icon: Languages
  }
];

const categories = [
  { id: 'all', label: 'جميع المجالات' },
  { id: 'DAWA', label: 'الدعوة والمحتوى' },
  { id: 'QURAN', label: 'القرآن الكريم' },
  { id: 'TAFSEER', label: 'التفسير' },
  { id: 'HADITH', label: 'الحديث النبوي' },
  { id: 'BOOKS', label: 'الكتب والمراجع' },
  { id: 'AQEEDAH', label: 'العقيدة' },
  { id: 'FIQH', label: 'الفقه' },
  { id: 'SEERAH_HISTORY', label: 'السيرة والتاريخ' },
  { id: 'QUESTIONS_DOUBTS', label: 'الأسئلة والشبهات' },
  { id: 'DICTIONARY_TRANSLATION', label: 'الترجمة والمصطلحات' }
];

export const SourcesPage: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const shouldReduceMotion = useReducedMotion() ?? false;
  const normalizedQuery = searchQuery.trim().toLocaleLowerCase('ar');
  const filteredSources = trustedSources.filter((source) => {
    const matchesCategory = selectedCategory === 'all' || source.categoryId === selectedCategory;
    const searchableText = `${source.category} ${source.name} ${source.subtitle || ''} ${source.domain} ${source.description}`.toLocaleLowerCase('ar');
    return matchesCategory && searchableText.includes(normalizedQuery);
  });

  return (
    <main
      className="relative isolate w-full overflow-hidden px-4 pb-20 pt-12 sm:px-6 md:pb-24 md:pt-16"
      style={{ background: 'radial-gradient(circle at 50% 25%, rgba(75,220,160,.07), transparent 32%), radial-gradient(circle at 5% 90%, rgba(40,180,120,.08), transparent 30%), radial-gradient(circle at 95% 90%, rgba(40,180,120,.07), transparent 30%), linear-gradient(180deg, #ffffff 0%, #fbfefc 52%, #eff9f4 100%)' }}
    >
      <svg className="pointer-events-none absolute inset-0 h-full w-full" viewBox="0 0 1440 1200" preserveAspectRatio="none" aria-hidden="true">
        <path d="M0 1040 C175 940 310 1140 520 1064 C760 975 845 960 1055 1035 C1210 1090 1330 1030 1440 965" fill="none" stroke="rgba(201,150,22,.15)" strokeWidth="1" />
        <path d="M0 1080 C190 990 320 1180 545 1094 C770 1010 890 1010 1090 1070 C1240 1115 1355 1075 1440 1030" fill="none" stroke="rgba(77,190,130,.12)" strokeWidth="1" />
        <circle cx="160" cy="1040" r="3" fill="rgba(201,150,22,.38)" />
        <circle cx="1250" cy="1010" r="3" fill="rgba(201,150,22,.38)" />
      </svg>

      <div className="relative z-10 mx-auto max-w-[1480px]">
        <motion.header
          initial={shouldReduceMotion ? false : { opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: shouldReduceMotion ? 0 : 0.5 }}
          className="mx-auto max-w-4xl text-center"
        >
          <div className="mx-auto flex h-[70px] w-[70px] items-center justify-center rounded-full border border-[#c89418]/55 bg-white/90 text-[#006b4d] shadow-[0_0_0_8px_rgba(77,224,160,.07),0_12px_30px_rgba(0,90,60,.07)]">
            <BookOpen className="h-8 w-8" strokeWidth={1.7} />
          </div>
          <h1 className="mt-5 text-[clamp(2.5rem,5vw,4rem)] font-extrabold leading-tight text-[#005c43]">
            المصادر <span className="bg-gradient-to-l from-[#c89418] to-[#dfb84d] bg-clip-text text-transparent">المعتمدة</span>
          </h1>
          <p className="mt-3 text-lg font-bold text-[#005c43] sm:text-xl">الدليل يبدأ من مصدر يمكن الرجوع إليه.</p>
          <p className="mx-auto mt-3 max-w-[850px] text-sm leading-[1.9] text-[#315747] sm:text-base">
            مجموعة من المصادر والمواقع الموثوقة المعتمدة في بيّنة، وتُستخدم في البحث والتحقق وتقديم المحتوى الإسلامي.
          </p>
          <div className="mx-auto mt-6 flex w-[170px] items-center gap-3" aria-hidden="true">
            <span className="h-px flex-1 bg-gradient-to-l from-transparent to-[#c89418]/70" />
            <span className="h-2 w-2 rotate-45 border border-[#c89418] bg-[#fffaf0]" />
            <span className="h-px flex-1 bg-gradient-to-r from-transparent to-[#c89418]/70" />
          </div>
        </motion.header>

        <div className="mx-auto mt-9 flex max-w-6xl flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <label className="relative block w-full sm:max-w-[320px]">
            <span className="sr-only">ابحث في المصادر المعتمدة</span>
            <Search className="pointer-events-none absolute right-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-[#527366]" />
            <input
              type="search"
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
              placeholder="ابحث بالاسم أو النطاق..."
              className="w-full rounded-xl border border-[#c89418]/30 bg-white/90 py-2.5 pl-4 pr-10 text-sm text-[#123d34] shadow-sm outline-none transition focus:border-[#00835d]/50 focus:ring-2 focus:ring-[#00835d]/15"
            />
          </label>
          <label className="flex w-full items-center gap-3 sm:w-auto">
            <span className="shrink-0 text-sm font-semibold text-[#315747]">المجال</span>
            <select
              value={selectedCategory}
              onChange={(event) => setSelectedCategory(event.target.value)}
              className="w-full rounded-xl border border-[#c89418]/30 bg-white/90 px-3 py-2.5 text-sm text-[#123d34] outline-none focus:border-[#00835d]/50 focus:ring-2 focus:ring-[#00835d]/15 sm:min-w-[210px]"
            >
              {categories.map((category) => <option key={category.id} value={category.id}>{category.label}</option>)}
            </select>
          </label>
          <p className="text-xs text-[#527366] sm:text-left" aria-live="polite">{filteredSources.length} مصدرًا</p>
        </div>

        <section aria-label="المصادر المعتمدة" className="mx-auto mt-6 grid max-w-6xl grid-cols-1 gap-4 sm:grid-cols-2 md:gap-5 lg:grid-cols-4">
          {filteredSources.map((source, index) => {
            const SourceIcon = source.icon;
            return (
              <motion.article
                key={source.id}
                initial={shouldReduceMotion ? false : { opacity: 0, y: 14 }}
                whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.12 }}
                transition={{ duration: shouldReduceMotion ? 0 : 0.42, delay: shouldReduceMotion ? 0 : (index % 8) * 0.045, ease: 'easeOut' }}
                whileHover={shouldReduceMotion ? undefined : { y: -4 }}
                className={`group relative flex min-h-[282px] flex-col overflow-hidden rounded-[23px] border border-[#c99b19]/40 bg-gradient-to-br from-white/[0.98] to-[#f6fdf9]/95 p-5 shadow-[0_14px_35px_rgba(0,90,60,.06)] transition-[border-color,box-shadow] duration-300 hover:border-[#00835d]/35 hover:shadow-[0_20px_45px_rgba(0,100,70,.09)] sm:p-6 ${source.id === '09' && selectedCategory === 'all' && !normalizedQuery ? 'lg:col-start-2' : ''}`}
              >
                <span className="pointer-events-none absolute -left-8 -top-8 h-28 w-28 rounded-full border border-[#c89418]/[0.08] transition-transform duration-500 group-hover:scale-110" />
                <div className="flex items-start justify-between gap-3">
                  <span className="inline-flex h-7 min-w-7 items-center justify-center rounded-full border border-[#c89418]/35 bg-gradient-to-br from-[#c89418] to-[#dfb84d] px-2 font-mono text-[11px] font-bold text-white shadow-sm">{source.id}</span>
                  <motion.span whileHover={shouldReduceMotion ? undefined : { scale: 1.04 }} className="flex h-12 w-12 shrink-0 items-center justify-center rounded-[15px] border border-[#c89418]/30 bg-white/90 text-[#006b4d] shadow-[0_6px_18px_rgba(0,90,60,.06)] sm:h-14 sm:w-14">
                    <SourceIcon className="h-6 w-6" strokeWidth={1.7} />
                  </motion.span>
                </div>

                <p className="mt-4 text-xs font-semibold text-[#527366]">{source.category}</p>
                <h2 className="mt-1 text-base font-bold leading-[1.6] text-[#005c43] sm:text-[17px]">{source.name}</h2>
                {source.subtitle && <p className="text-sm font-semibold text-[#a77b0e]">{source.subtitle}</p>}
                <p className="mt-2 flex-1 text-sm leading-[1.75] text-[#405d50]">{source.description}</p>

                <div className="mt-4 flex items-center justify-between gap-3 border-t border-[#d8e8df] pt-4">
                  <span dir="ltr" className="min-w-0 truncate text-left font-mono text-[11px] text-[#527366]">{source.domain}</span>
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={`زيارة مصدر ${source.name}`}
                    className="inline-flex h-10 shrink-0 items-center justify-center gap-2 rounded-full border border-[#c89418]/60 bg-white/90 px-3.5 text-xs font-bold text-[#005c43] transition-colors duration-200 hover:bg-gradient-to-br hover:from-[#00835d] hover:to-[#005a42] hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#00835d]/50 focus-visible:ring-offset-2"
                  >
                    <span>زيارة المصدر</span>
                    <ExternalLink className="h-3.5 w-3.5" />
                  </a>
                </div>
              </motion.article>
            );
          })}
          {filteredSources.length === 0 && <p className="col-span-full py-12 text-center text-sm text-[#527366]">لا توجد مصادر مطابقة للبحث.</p>}
        </section>

        <motion.aside
          initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }}
          whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.2 }}
          transition={{ duration: shouldReduceMotion ? 0 : 0.42 }}
          className="mx-auto mt-7 flex max-w-[980px] items-center gap-3 rounded-[22px] border border-[#c89418]/40 bg-white/85 px-5 py-4 text-sm leading-[1.8] text-[#315747] shadow-[0_10px_30px_rgba(0,90,60,.05)] backdrop-blur-md sm:mt-9 sm:rounded-full sm:px-7"
        >
          <Info className="h-5 w-5 shrink-0 text-[#006b4d]" />
          <p>تم اختيار هذه المصادر وفق المرجعية العلمية المعتمدة، وتُستخدم في البحث والتحقق وتقديم المحتوى الإسلامي.</p>
        </motion.aside>
      </div>
    </main>
  );
};