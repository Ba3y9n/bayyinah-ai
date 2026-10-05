import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence, useAnimation } from 'framer-motion';
import { NavTab } from '../components/Navbar';
import { ArrowLeft, ArrowRight, Search, FileText, CheckCircle, Database, Link2, ShieldCheck, AlertCircle, Layout, BookOpen, Layers, Image as ImageIcon, Video as FileVideo } from 'lucide-react';

interface HomePageProps {
  onStartVerification: () => void;
  setActiveTab: (tab: NavTab) => void;
}

// 1. Hero Orbit Component (Rule 37)

const HeroOrbit = () => {
  const [activeIndex, setActiveIndex] = useState(0);
  const [isHovered, setIsHovered] = useState(false);

  const steps = [
    { id: 'content', label: 'محتوى', icon: <FileText className="w-5 h-5" />, desc: 'تستقبل بيّنة النص أو الصورة أو الفيديو أو الرابط.' },
    { id: 'claim', label: 'ادعاء', icon: <Layers className="w-5 h-5" />, desc: 'تفكك المحتوى وتحدد الادعاءات التي تحتاج إلى تحقق.' },
    { id: 'search', label: 'بحث', icon: <Search className="w-5 h-5" />, desc: 'تبحث بالمطابقة اللفظية والدلالية في المصادر المعتمدة.' },
    { id: 'source', label: 'مصدر', icon: <Database className="w-5 h-5" />, desc: 'تحصر البحث في المصادر الشرعية الـ 11 المعتمدة فقط.' },
    { id: 'evidence', label: 'دليل', icon: <BookOpen className="w-5 h-5" />, desc: 'تربط كل نتيجة بالمتن المعتمد والسند والتخريج.' },
    { id: 'result', label: 'نتيجة', icon: <ShieldCheck className="w-5 h-5" />, desc: 'تعرض حالة التحقق بوضوح وأمانة علمية دون تخمين.' }
  ];

  useEffect(() => {
    if (isHovered) return;
    const interval = setInterval(() => {
      setActiveIndex((prev) => (prev + 1) % steps.length);
    }, 4500);
    return () => clearInterval(interval);
  }, [isHovered, steps.length]);

  return (
    <div className="flex flex-col items-center w-full">
      <div
        className="relative w-[320px] h-[320px] md:w-[440px] md:h-[440px] flex items-center justify-center"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        <div className="absolute z-10 w-24 h-24 md:w-32 md:h-32 rounded-full bg-white flex flex-col items-center justify-center text-center p-2 shadow-[0_0_35px_rgba(255,255,255,0.3)] border border-[#D2EFE9]">
          <span className="text-[#0a2d2b] font-bold text-base md:text-lg tracking-wide">بيّنة AI</span>
          <span className="text-[10px] md:text-xs text-[#1b5f59] mt-0.5">محرك التحقق</span>
        </div>

        {steps.map((step, idx) => {
          const angle = (idx * (360 / steps.length) - 90) * (Math.PI / 180);
          const radius = window.innerWidth < 768 ? 125 : 170;
          const x = Math.cos(angle) * radius;
          const y = Math.sin(angle) * radius;
          const isActive = activeIndex === idx;

          return (
            <div
              key={step.id}
              className="absolute z-20 flex flex-col items-center"
              style={{
                transform: `translate(${x}px, ${y}px)`,
                left: '50%', top: '50%'
              }}
            >
              <motion.button
                onClick={() => setActiveIndex(idx)}
                className={`w-11 h-11 md:w-14 md:h-14 rounded-full flex items-center justify-center transition-all duration-500 cursor-pointer border border-[#DDEFEA]
                  ${isActive ? 'bg-[#0f8b7e] text-white shadow-[0_0_30px_rgba(15,139,126,0.75)] scale-110' : 'bg-white text-[#10201D] hover:bg-[#EAF7F4] shadow-sm'}`}
                whileHover={{ scale: 1.15 }}
                whileTap={{ scale: 0.95 }}
              >
                {step.icon}
              </motion.button>
              <div className={`mt-1.5 font-bold transition-all duration-300 ${isActive ? 'text-white text-base drop-shadow-md' : 'text-white/75 text-xs'}`}>
                {step.label}
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-10 p-5 bg-white/95 rounded-2xl shadow-[0_12px_30px_rgba(0,0,0,0.12)] border border-white/40 max-w-md w-full text-center z-40 transition-all duration-300 transform min-h-[92px] flex flex-col justify-center backdrop-blur-sm">
        <p className="text-lg font-bold text-[#0b5d53] mb-2">{steps[activeIndex].label}</p>
        <p className="text-sm md:text-base text-[#10201D]/80 leading-relaxed">{steps[activeIndex].desc}</p>
      </div>
    </div>
  );
};

// 2. CountUp Component
const CountUp = ({ to, duration = 2 }: { to: number | string; duration?: number }) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = parseInt(String(to).replace(/[^0-9]/g, ''));
    if (start === end) return;

    let totalMilSecDur = duration * 1000;
    let incrementTime = (totalMilSecDur / end) * 2;
    
    let timer = setInterval(() => {
      start += 1;
      setCount(start);
      if (start === end) clearInterval(timer);
    }, incrementTime);
    
    return () => clearInterval(timer);
  }, [to, duration]);

  return <span>{count}%</span>;
};

// 3. Why Bayyinah Section

const WhyBayyinah = () => {
  const steps = [
    { title: 'الفهم الذكي قبل التحقق', desc: 'لا تتعامل بيّنة مع المحتوى ككتلة نصية فقط، بل تفهم السياق وتحدد الادعاءات التي تحتاج إلى تحقق.', icon: <Layout className="w-8 h-8"/> },
    { title: 'المصدر أولًا', desc: 'تبحث بيّنة في المصادر المعتمدة والمرتبطة بنوع المحتوى والادعاء، بعيدًا عن التخمين.', icon: <Database className="w-8 h-8"/> },
    { title: 'الدليل ظاهر', desc: 'لا تكتفي بيّنة بالنتيجة، بل تعرض الدليل والمصدر والمرجع والرابط ليتمكن المستخدم من مراجعتها.', icon: <BookOpen className="w-8 h-8"/> },
    { title: 'الأمانة العلمية', desc: 'إذا لم تجد بيّنة دليلًا كافيًا، لا تنشئ يقينًا من الفراغ، بل توضّح حدود ما تم التوصل إليه.', icon: <ShieldCheck className="w-8 h-8"/> },
    { title: 'معالجة متعددة الوسائط', desc: 'يمكن التحقق من: النص، الصورة، الفيديو، الرابط.', icon: <Link2 className="w-8 h-8"/> }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {steps.map((step, idx) => (
        <motion.div
          key={idx}
          whileHover={{ y: -5, scale: 1.02 }}
          className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 hover:border-bayyinah-emerald/40 transition-all duration-300 flex flex-col items-start gap-4 cursor-default"
        >
          <div className="p-4 bg-bayyinah-ivory text-bayyinah-emerald rounded-2xl">
            {step.icon}
          </div>
          <h3 className="text-xl font-bold text-bayyinah-dark-text mt-2">{step.title}</h3>
          <p className="text-bayyinah-secondary-text leading-relaxed font-light">{step.desc}</p>
        </motion.div>
      ))}
    </div>
  );
};

// 4. How It Works Timeline
const HowItWorks = () => {
  const [activeTab, setActiveTab] = useState(0);
  
  const steps = [
    { num: '01', title: 'يفهم المحتوى', short: 'الفهم' },
    { num: '02', title: 'يستخرج الادعاء', short: 'الاستخراج' },
    { num: '03', title: 'يبحث في المصادر', short: 'البحث' },
    { num: '04', title: 'يجمع الأدلة', short: 'الجمع' },
    { num: '05', title: 'يتحقق من المصدر', short: 'التحقق' },
    { num: '06', title: 'تحدد حالة النتيجة', short: 'النتيجة' },
    { num: '07', title: 'تعرض الدليل', short: 'الدليل' }
  ];

  return (
    <div className="w-full mt-16">
      {/* Horizontal Timeline Navigation */}
      <div className="relative mb-12 flex items-center justify-between overflow-x-auto pb-6 hide-scrollbar" role="tablist">
        <div className="absolute top-1/2 left-0 right-0 h-px bg-gray-200 -translate-y-1/2 z-0 min-w-[800px]"></div>
        <div className="absolute top-1/2 right-0 h-0.5 bg-bayyinah-emerald -translate-y-1/2 z-0 transition-all duration-500 ease-out" style={{ width: `${(activeTab / (steps.length - 1)) * 100}%`, minWidth: '0' }}></div>
        
        {steps.map((step, idx) => {
          const isActive = activeTab === idx;
          const isPast = activeTab > idx;
          return (
            <button 
              key={idx}
              onClick={() => setActiveTab(idx)}
              className="relative z-10 flex flex-col items-center gap-3 min-w-[120px] cursor-pointer group focus:outline-none focus:ring-2 focus:ring-bayyinah-emerald/50 rounded-lg p-2" aria-selected={isActive} role="tab"
            >
              <div className={`w-4 h-4 rounded-full transition-all duration-300 border-2 ${
                isActive ? 'bg-bayyinah-emerald border-bayyinah-emerald scale-150 shadow-[0_0_15px_rgba(8,127,104,0.5)]' 
                : isPast ? 'bg-bayyinah-emerald border-bayyinah-emerald' 
                : 'bg-white border-gray-300 group-hover:border-bayyinah-emerald'
              }`} />
              <div className="text-center">
                <span className={`block text-xs font-bold mb-1 transition-colors ${isActive || isPast ? 'text-bayyinah-emerald' : 'text-gray-400'}`}>{step.num}</span>
                <span className={`block text-sm font-medium transition-colors ${isActive ? 'text-bayyinah-dark-text' : 'text-gray-500'}`}>{step.short}</span>
              </div>
            </button>
          );
        })}
      </div>

      {/* Active Panel Content */}
      <div className="bg-white border border-gray-100 rounded-3xl p-8 lg:p-12 shadow-sm min-h-[300px] flex flex-col justify-center relative overflow-hidden">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="flex flex-col items-center text-center max-w-3xl mx-auto"
          >
            <h3 className="text-2xl font-bold text-bayyinah-dark-text mb-4">
              {steps[activeTab].num} — {steps[activeTab].title}
            </h3>
            
            {/* Visuals per step */}
            <div className="mt-8 w-full">
              {activeTab === 0 && <p className="text-lg text-bayyinah-secondary-text">تستقبل بيّنة النص أو الصورة أو الفيديو وتقوم بتحليل البنية الأساسية للمحتوى باستخدام الذكاء الاصطناعي.</p>}
              {activeTab === 1 && <p className="text-lg text-bayyinah-secondary-text">تستخرج الادعاءات الرئيسية وتتجاهل الحشو، ليتم التركيز على ما يتطلب التحقق المرجعي.</p>}
              {activeTab === 2 && (
                <div className="flex justify-center gap-4">
                  <div className="px-6 py-3 bg-bayyinah-ivory text-bayyinah-emerald font-semibold rounded-lg border border-bayyinah-emerald/20">بحث دلالي (Semantic)</div>
                  <div className="px-6 py-3 bg-bayyinah-ivory text-bayyinah-emerald font-semibold rounded-lg border border-bayyinah-emerald/20">بحث نصي (Full Text)</div>
                </div>
              )}
              {activeTab === 3 && <p className="text-lg text-bayyinah-secondary-text">جمع الأدلة المتوافقة والمتعارضة من المصادر المعتمدة لبناء قاعدة حكم متوازنة.</p>}
              {activeTab === 4 && <p className="text-lg text-bayyinah-secondary-text">مقارنة الادعاء مع الدليل المستخرج والتأكد من عدم وجود اختلافات في سياق النقل.</p>}
              {activeTab === 5 && (
                <div className="flex flex-wrap justify-center gap-3">
                  <span className="px-4 py-2 bg-bayyinah-emerald text-bayyinah-dark-text rounded-lg text-sm">ثابت بحسب المصدر</span>
                  <span className="px-4 py-2 bg-red-600 text-bayyinah-dark-text rounded-lg text-sm">لم يثبت بهذا اللفظ</span>
                  <span className="px-4 py-2 bg-gray-600 text-bayyinah-dark-text rounded-lg text-sm">لم نجد دليلًا كافيًا</span>
                </div>
              )}
              {activeTab === 6 && (
                <div className="flex items-center justify-center gap-2 text-bayyinah-emerald font-bold">
                  <span>المصدر</span> <ArrowLeft className="w-4 h-4" /> <span>المرجع</span> <ArrowLeft className="w-4 h-4" /> <span>الدليل</span> <ArrowLeft className="w-4 h-4" /> <span className="text-bayyinah-dark-text">النتيجة</span>
                </div>
              )}
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
};


// --- MAIN PAGE EXPORT ---
export const HomePage: React.FC<HomePageProps> = ({ onStartVerification, setActiveTab }) => {
  const [activeStat, setActiveStat] = useState(0);
  const [activeQuestion, setActiveQuestion] = useState(0);

  const stats = [
    {
      value: '63%',
      label: 'رصد المحتوى',
      description: 'من محتوى الأحاديث على Instagram في إحدى الدراسات المنشورة عام 2025 لم يتضمن بيانًا لحالة الحديث من حيث الأصالة.',
      insight: 'في العينة المذكورة، لم يتضمن المحتوى بيان حالة الحديث من حيث الأصالة.'
    },
    {
      value: '37.5%',
      label: 'حالة التوثيق',
      description: 'من العينة المدروسة في دراسة أخرى منشورة عام 2025 لم تتضمن حالة توثيق الحديث.',
      insight: 'الرقم يصف العينة المدروسة، ولا يحكم على كل ما يُنشر أو يُتداول.'
    },
    {
      value: '3,281',
      label: 'مرجع تراثي',
      description: 'مادة وحديثًا مما اشتهر على ألسنة الناس في كتاب "كشف الخفاء ومزيل الإلباس" للإمام العجلوني.',
      insight: 'يشير الرقم إلى مواد وأحاديث اشتهرت على الألسنة وجُمعت في الكتاب المذكور.'
    }
  ];

  const verificationQuestions = [
    { num: '01', text: 'هل تم توثيقه؟', detail: 'تأكد من وجود إحالة يمكن الرجوع إليها، لا مجرد نسبة عامة.' },
    { num: '02', text: 'ما مصدره؟', detail: 'ارجع إلى المرجع الأصلي، وتحقق من اسم المصدر وموضع النص.' },
    { num: '03', text: 'هل النص مطابق؟', detail: 'قارن النص المتداول بما ورد في مصدره، وانتبه للاختصار أو التغيير.' },
    { num: '04', text: 'ما درجة ثبوته؟', detail: 'اعرض الحكم كما ورد في مرجع متخصص، مع مصدره وسياقه.' },
    { num: '05', text: 'هل توجد مصادر أخرى؟', detail: 'قارن النتيجة بمراجع معتمدة أخرى عند الحاجة.' }
  ];

  return (
    <div className="flex flex-col bg-bayyinah-ivory text-bayyinah-dark-text overflow-x-hidden">
      
      {/* 1. HERO SECTION */}
      <section className="relative min-h-[90vh] flex flex-col items-center pt-28 pb-16 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: "linear-gradient(90deg, rgba(9, 49, 45, 0.10) 0%, rgba(9, 49, 45, 0.10) 100%), url('/hero-bg.jpg')",
            backgroundSize: 'cover',
            backgroundPosition: 'center'
          }}
        />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(12,93,82,0.15),_rgba(8,26,22,0.82)_55%,_rgba(7,17,14,0.9)_100%)]" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full flex flex-col lg:flex-row items-center justify-between gap-8">
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="w-full lg:w-[48%] text-right"
          >
            <h1 className="text-shadow-soft text-4xl md:text-6xl lg:text-[5rem] font-black text-white leading-[1.1] tracking-tight mb-5">
              تحقّق قبل أن تنشر.
            </h1>
            <p className="text-lg md:text-2xl text-white/80 max-w-2xl mr-auto leading-relaxed font-medium">
              بيّنة تساعدك على التحقق من الادعاءات الإسلامية بالرجوع إلى المصادر المعتمدة وإظهار الدليل.
            </p>

            <motion.div
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="mt-8 flex justify-start"
            >
              <button
                onClick={onStartVerification}
                className="bg-[#0f8b7e] hover:bg-[#0c776d] text-white px-10 py-4 rounded-2xl font-bold text-xl transition-all shadow-[0_0_24px_rgba(15,139,126,0.35)] cursor-pointer flex items-center justify-center gap-3"
              >
                ابدأ التحقق
                <ArrowLeft className="w-6 h-6" />
              </button>
            </motion.div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.92, y: 12 }}
            animate={{ opacity: 1, scale: 1, y: 12 }}
            transition={{ duration: 0.8, delay: 0.15 }}
            className="w-full lg:w-[52%] flex justify-start"
          >
            <HeroOrbit />
          </motion.div>
        </div>
      </section>

      {/* 2. PROBLEM SECTION (Rule 38) */}
      <section
        className="overflow-hidden py-20 md:py-24"
        style={{ background: 'linear-gradient(120deg, #ffffff 0%, #f8faf8 52%, #fffdf8 100%)' }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid gap-8 border-b border-[#d9d2bd] pb-9 md:grid-cols-[1.15fr_0.85fr] md:items-end md:gap-14">
            <div className="text-right">
              <span className="inline-flex items-center gap-3 text-xs font-bold text-[#8b7135]">
                <span className="h-px w-8 bg-[#b49a5b]" />
                واقع المحتوى المتداول
              </span>
              <h2 className="mt-4 text-3xl font-bold leading-tight text-[#123d34] md:text-4xl lg:text-5xl">
                سرعة الانتشار...<br className="hidden sm:block" /> وغياب التحقق
              </h2>
            </div>
            <div className="space-y-3 text-right text-sm leading-relaxed text-[#596660] md:text-base">
              <p>
                مع الانتشار السريع للمحتوى الرقمي، أصبح الوصول إلى المحتوى الإسلامي المتداول أسهل، لكن التحقق من مصدره ودرجة ثبوته لا يكون واضحًا دائمًا للمستخدم.
              </p>
              <p className="font-medium text-[#263c34]">
                تنتشر الأحاديث والأدعية والمقولات دون توثيق واضح؛ وتزداد الحاجة إلى الوصول للمصدر والدليل بدل الاكتفاء بإجابة مولدة.
              </p>
            </div>
            </div>

          <div className="mt-10 grid items-stretch gap-8 lg:grid-cols-[1.15fr_0.85fr] lg:gap-16">
            <div className="relative flex min-h-[340px] flex-col justify-center border-y border-[#cfc5a8] bg-white/35 px-5 py-8 sm:px-9 md:min-h-[390px] md:px-12">
              <div className="mb-7 flex items-center justify-between border-b border-[#e9e5d9] pb-4 text-xs font-semibold text-[#718078]">
                <span>قراءة إحصائية</span>
                <span dir="ltr" className="font-mono text-[#a68b4d]">{String(activeStat + 1).padStart(2, '0')} / 03</span>
              </div>
              <AnimatePresence mode="wait" initial={false}>
                <motion.div
                  key={activeStat}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.24 }}
                  aria-live="polite"
                >
                  <span className="block text-xs font-bold text-[#8b7135]">{stats[activeStat].label}</span>
                  <span dir="ltr" className="mt-2 block text-right text-7xl font-black leading-none tracking-tight text-[#0b493f] sm:text-8xl">
                    {stats[activeStat].value}
                  </span>
                  <span className="my-6 block h-px w-20 bg-[#b49a5b]" />
                  <p className="max-w-2xl text-base leading-relaxed text-[#354940] md:text-lg">
                    {stats[activeStat].description}
                  </p>
                  <p className="mt-4 text-sm leading-relaxed text-[#7a817a] md:text-base">
                    {stats[activeStat].insight}
                  </p>
                </motion.div>
              </AnimatePresence>
            </div>

            <div className="flex flex-col justify-center divide-y divide-[#e5e1d6] border-y border-[#e5e1d6]" aria-label="إحصاءات المحتوى والتوثيق">
              {stats.map((stat, index) => {
                const isActive = activeStat === index;

                return (
                  <motion.button
                    key={stat.value}
                    type="button"
                    aria-pressed={isActive}
                    onClick={() => setActiveStat(index)}
                    whileHover={{ x: -3 }}
                    className={`flex w-full items-center gap-4 border-r-2 px-4 py-6 text-right transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-[#9b8246]/50 md:px-5 ${
                      isActive ? 'border-[#b49a5b] bg-white/65' : 'border-transparent hover:border-[#c9d8ce] hover:bg-white/40'
                    }`}
                  >
                    <span className="font-mono text-xs text-[#a68b4d]">0{index + 1}</span>
                    <span className="min-w-0 flex-1">
                      <span className="block text-xs text-[#718078]">{stat.label}</span>
                      <span dir="ltr" className="mt-1 block text-right text-2xl font-bold tracking-tight text-[#183f35] md:text-3xl">
                        {stat.value}
                      </span>
                    </span>
                    <span className={`h-1.5 w-1.5 shrink-0 rounded-full ${isActive ? 'bg-[#b49a5b]' : 'bg-[#d9ded8]'}`} />
                  </motion.button>
                );
              })}
            </div>
          </div>

          <div className="mt-16 border-t border-[#d9d2bd] pt-9">
            <div className="flex flex-col gap-3 text-right md:flex-row md:items-end md:justify-between">
              <div>
                <span className="text-xs font-bold text-[#8b7135]">من الرقم إلى التحقق</span>
                <h3 className="mt-2 text-2xl font-bold text-[#123d34] md:text-3xl">ماذا ينبغي أن نسأل؟</h3>
              </div>
              <p className="max-w-xl text-sm leading-relaxed text-[#69736d] md:text-base">
                لا تعني هذه الأرقام أن كل ما يُنشر على وسائل التواصل غير صحيح؛ بل تدعونا إلى أسئلة أوضح قبل مشاركة المحتوى.
              </p>
            </div>

            <div className="mt-7 grid grid-cols-2 gap-x-4 md:grid-cols-5 md:gap-x-7" aria-label="أسئلة التحقق">
              {verificationQuestions.map((question, index) => {
                const isActive = activeQuestion === index;

                return (
                  <button
                    key={question.num}
                    type="button"
                    aria-pressed={isActive}
                    onClick={() => setActiveQuestion(index)}
                    className={`min-h-[104px] border-b-2 py-4 text-right transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-[#9b8246]/50 ${
                      isActive ? 'border-[#b49a5b]' : 'border-[#e4e4dd] hover:border-[#c9d8ce]'
                    }`}
                  >
                    <span className="mb-3 block font-mono text-xs text-[#a68b4d]">{question.num}</span>
                    <span className={`block text-sm font-bold leading-relaxed md:text-base ${isActive ? 'text-[#123d34]' : 'text-[#68716c]'}`}>
                      {question.text}
                    </span>
                  </button>
                );
              })}
            </div>

            <AnimatePresence mode="wait" initial={false}>
              <motion.p
                key={activeQuestion}
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -6 }}
                transition={{ duration: 0.2 }}
                aria-live="polite"
                className="mt-5 max-w-3xl text-right text-sm leading-relaxed text-[#65716a] md:text-base"
              >
                <span className="ml-2 text-[#b49a5b]">—</span>
                {verificationQuestions[activeQuestion].detail}
              </motion.p>
            </AnimatePresence>
          </div>

        </div>
      </section>

      {/* 3. WHY BAYYINAH (Rule 41) */}
      <section className="py-24 bg-bayyinah-ivory border-t border-gray-100 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-16">
            <h2 className="text-3xl md:text-5xl font-bold text-bayyinah-dark-text mb-4">لماذا بيّنة؟</h2>
            <p className="text-xl text-bayyinah-secondary-text font-light">لأن التحقق لا يبدأ من الإجابة... بل من الدليل.</p>
          </div>
          
          <WhyBayyinah />
        </div>
      </section>

      {/* 4. HOW IT WORKS (Rule 42) */}
      <section id="how-it-works" className="py-24 bg-white overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-4">
            <h2 className="text-3xl md:text-5xl font-bold text-bayyinah-dark-text mb-4">كيف تعمل بيّنة؟</h2>
            <p className="text-xl text-bayyinah-secondary-text font-light">من المحتوى المتداول إلى سلسلة دليل واضحة.</p>
          </div>
          
          <HowItWorks />
        </div>
      </section>

      {/* 5. MISSION & VISION (Rules 53 & 54) */}
      <section className="py-24 bg-bayyinah-ivory border-t border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-16">
            {/* Mission (Rule 53) */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.6 }}
              className="relative bg-white p-10 rounded-3xl border border-gray-100 shadow-sm hover:shadow-elevated transition-all duration-300 hover:border-bayyinah-emerald/30"
            >
              <div className="absolute right-0 top-0 w-1.5 h-full bg-gradient-to-b from-bayyinah-emerald to-transparent rounded-full"></div>
              <div className="pr-8 py-4">
                <span className="text-xs font-bold tracking-widest text-bayyinah-emerald uppercase block mb-3">رسالتنا</span>
                <h3 className="text-2xl md:text-3xl font-bold text-bayyinah-dark-text leading-tight mb-4">
                  أن نجعل الوصول إلى المحتوى الإسلامي الموثوق أكثر وضوحًا، وأسهل تحققًا، وأقرب إلى الدليل.
                </h3>
                <p className="text-base text-bayyinah-secondary-text leading-relaxed font-light mb-6">
                  نسعى إلى توظيف الذكاء الاصطناعي في خدمة المحتوى الإسلامي من خلال البحث، والتحقق، والوصول إلى المصادر، وتقديم المعرفة بطريقة واضحة يمكن للمستخدم تتبعها ومراجعتها.
                </p>
                <div className="p-4 rounded-2xl bg-white border border-bayyinah-emerald/30 text-bayyinah-deep-emerald font-bold text-sm">
                  «الذكاء الاصطناعي يساعدك في الوصول إلى الدليل، والمصدر هو الذي تتبعه.»
                </div>
              </div>
            </motion.div>

            {/* Vision (Rule 54) */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="bg-white p-10 rounded-3xl border border-gray-100 shadow-sm hover:shadow-elevated transition-all duration-300 hover:border-bayyinah-emerald/30 relative overflow-hidden flex flex-col justify-between"
            >
              <div>
                <span className="text-xs font-bold tracking-widest text-bayyinah-soft-emerald uppercase block mb-3">رؤيتنا</span>
                <p className="text-xl md:text-2xl text-bayyinah-dark-text leading-relaxed font-light mb-8">
                  أن تصبح منصة بيّنة AI مرجعًا ذكيًا عالميًا للتحقق من المحتوى الإسلامي، ونموذجًا للذكاء الاصطناعي المسؤول والآمن في خدمة المعرفة الإسلامية.
                </p>
              </div>
              
              <div className="pt-6 border-t border-gray-100 flex items-center justify-between text-xs md:text-sm font-medium text-bayyinah-emerald">
                <span>المحتوى</span>
                <ArrowLeft className="w-4 h-4 text-gray-300" />
                <span>الادعاء</span>
                <ArrowLeft className="w-4 h-4 text-gray-300" />
                <span>المصدر</span>
                <ArrowLeft className="w-4 h-4 text-gray-300" />
                <span className="bg-bayyinah-emerald text-bayyinah-dark-text px-3 py-1.5 rounded-lg font-bold">الدليل</span>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* 6. IMMERSIVE CTA */}
      <section className="relative py-32 bg-bayyinah-emerald/10 text-bayyinah-dark-text overflow-hidden">
        <div className="max-w-4xl mx-auto px-4 text-center relative z-10">
          <motion.h2 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="text-4xl md:text-6xl font-bold mb-6 text-bayyinah-dark-text"
          >
            قبل أن تشارك... <span className="text-bayyinah-emerald">تحقّق.</span>
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="text-xl md:text-2xl text-bayyinah-dark-text/70 mb-12 font-medium leading-relaxed max-w-2xl mx-auto"
          >
            أرسل المحتوى الذي تريد التحقق منه، ودع بيّنة تقودك من الادعاء إلى المصدر والدليل.
          </motion.p>
          <motion.button 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.4 }}
            onClick={onStartVerification}
            className="bg-bayyinah-emerald hover:bg-bayyinah-soft-emerald text-white px-12 py-5 rounded-2xl font-bold text-xl transition-all shadow-[0_0_40px_rgba(8,127,104,0.2)] hover:shadow-[0_0_60px_rgba(8,127,104,0.3)] flex items-center gap-3 mx-auto"
          >
            ابدأ التحقق
            <ArrowLeft className="w-6 h-6" />
          </motion.button>
        </div>
      </section>

    </div>
  );
};
