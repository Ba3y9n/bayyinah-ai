import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence, useAnimation, useReducedMotion } from 'framer-motion';
import { NavTab } from '../components/Navbar';
import { ArrowLeft, ArrowRight, ArrowDown, Search, FileText, CheckCircle, Database, Link2, ShieldCheck, AlertCircle, Layout, BookOpen, Layers, Image as ImageIcon, Video as FileVideo } from 'lucide-react';

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
  const [activeCard, setActiveCard] = useState(0);
  const [activeQuestion, setActiveQuestion] = useState(0);
  const shouldReduceMotion = useReducedMotion() ?? false;
  const verificationSectionRef = useRef<HTMLElement | null>(null);
  const verificationSectionVisible = useRef(false);
  const manualPauseUntil = useRef(0);

  const stats = [
    {
      value: '63%',
      label: 'رصد المحتوى',
      icon: <FileText className="h-5 w-5" />,
      description: 'من محتوى الأحاديث على Instagram في إحدى الدراسات المنشورة عام 2025 لم يتضمن بيانًا لحالة الحديث من حيث الأصالة.'
    },
    {
      value: '37.5%',
      label: 'حالة التوثيق',
      icon: <ShieldCheck className="h-5 w-5" />,
      description: 'من العينة المدروسة في دراسة أخرى منشورة عام 2025 لم تتضمن حالة توثيق الحديث.'
    },
    {
      value: '3,281',
      label: 'مرجع تراثي',
      icon: <BookOpen className="h-5 w-5" />,
      description: 'مادة وحديثًا مما اشتهر على ألسنة الناس في كتاب "كشف الخفاء ومزيل الإلباس" للإمام العجلوني.'
    }
  ];

  const verificationQuestions = [
    { num: '01', text: 'هل تم توثيقه؟', detail: 'تأكد من وجود إحالة يمكن الرجوع إليها، لا مجرد نسبة عامة.', icon: <CheckCircle className="h-6 w-6" /> },
    { num: '02', text: 'ما مصدره؟', detail: 'ارجع إلى المرجع الأصلي، وتحقق من اسم المصدر وموضع النص.', icon: <Database className="h-6 w-6" /> },
    { num: '03', text: 'هل النص مطابق؟', detail: 'قارن النص المتداول بما ورد في مصدره، وانتبه للاختصار أو التغيير.', icon: <FileText className="h-6 w-6" /> },
    { num: '04', text: 'ما درجة ثبوته؟', detail: 'اعرض الحكم كما ورد في مرجع متخصص، مع مصدره وسياقه.', icon: <ShieldCheck className="h-6 w-6" /> },
    { num: '05', text: 'هل توجد مصادر أخرى؟', detail: 'قارن النتيجة بمراجع معتمدة أخرى عند الحاجة.', icon: <BookOpen className="h-6 w-6" /> }
  ];

  const desktopJourneyPath = 'M 900 70 C 850 15, 750 15, 700 70 C 650 125, 550 125, 500 70 C 450 15, 350 15, 300 70 C 250 125, 150 125, 100 70';
  const desktopJourneyPoints = [
    [900, 70], [855, 37], [800, 41], [745, 37], [700, 70],
    [655, 103], [600, 99], [545, 103], [500, 70],
    [455, 37], [400, 41], [345, 37], [300, 70],
    [255, 103], [200, 99], [145, 103], [100, 70]
  ];

  useEffect(() => {
    if (shouldReduceMotion) return;

    const section = verificationSectionRef.current;
    if (!section) return;

    const observer = new IntersectionObserver(([entry]) => {
      verificationSectionVisible.current = entry.isIntersecting;
    }, { threshold: 0.2 });
    observer.observe(section);

    const interval = window.setInterval(() => {
      if (!verificationSectionVisible.current || Date.now() < manualPauseUntil.current) return;
      setActiveQuestion((current) => (current + 1) % verificationQuestions.length);
    }, 2300);

    return () => {
      observer.disconnect();
      window.clearInterval(interval);
    };
  }, [shouldReduceMotion, verificationQuestions.length]);

  const selectVerificationQuestion = (index: number) => {
    manualPauseUntil.current = Date.now() + 7000;
    setActiveQuestion(index);
  };

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
        className="relative isolate overflow-hidden py-20 md:py-24"
        style={{ background: 'radial-gradient(circle at 15% 50%, rgba(16,185,129,0.08), transparent 35%), radial-gradient(circle at 85% 55%, rgba(16,185,129,0.07), transparent 35%), linear-gradient(180deg, #ffffff 0%, #fbfdfb 50%, #f5fbf7 100%)' }}
      >
        <div aria-hidden="true" className="pointer-events-none absolute inset-0 -z-10 overflow-hidden">
          <span className="absolute -right-24 top-[32%] h-80 w-80 rounded-full border border-emerald-900/[0.04]" />
          <span className="absolute -right-12 top-[36%] h-56 w-56 rounded-full border border-emerald-900/[0.035]" />
          <span className="absolute -left-28 top-[52%] h-72 w-72 rounded-full border border-emerald-900/[0.04]" />
          <span className="absolute left-[14%] top-[43%] h-1.5 w-1.5 rounded-full bg-emerald-700/10" />
          <span className="absolute right-[24%] top-[72%] h-1 w-1 rounded-full bg-emerald-700/10" />
        </div>

        <div className="relative z-10 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 14 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.35 }}
            transition={{ duration: 0.45 }}
            className="ml-auto max-w-3xl text-right"
          >
            <span className="text-xs font-bold text-emerald-800">واقع المحتوى المتداول</span>
            <h2 className="mt-4 text-4xl font-extrabold leading-tight text-[#123d34] md:text-5xl">
              سرعة الانتشار...
              <span className="mt-1 block text-emerald-700">وغياب التحقق</span>
            </h2>
            <p className="ml-auto mt-5 max-w-3xl text-base leading-[1.8] text-[#53665c] md:text-lg">
              مع الانتشار السريع للمحتوى الرقمي، أصبح الوصول إلى المحتوى الإسلامي المتداول أسهل، لكن التحقق من مصدره ودرجة ثبوته قد يستغرق وقتًا أطول.
            </p>
          </motion.div>

          <div className="mx-auto mt-12 max-w-6xl">
            <div className="grid grid-cols-1 items-stretch gap-y-0 md:grid-cols-[minmax(0,1fr)_44px_minmax(0,1fr)_44px_minmax(0,1fr)] md:gap-x-1 lg:grid-cols-[minmax(0,1fr)_64px_minmax(0,1fr)_64px_minmax(0,1fr)] lg:gap-x-2">
              {stats.map((stat, index) => {
                const isActive = activeCard === index;

                return (
                  <React.Fragment key={stat.value}>
                    <motion.button
                      type="button"
                      aria-pressed={isActive}
                      aria-controls="stat-detail-panel"
                      aria-label={`${stat.label} ${stat.value}`}
                      onClick={() => setActiveCard(index)}
                      initial={shouldReduceMotion ? false : { opacity: 0, y: 14 }}
                      whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
                      viewport={{ once: true, amount: 0.2 }}
                      transition={{ duration: shouldReduceMotion ? 0 : 0.42, delay: shouldReduceMotion ? 0 : index * 0.12, ease: 'easeOut' }}
                      whileHover={shouldReduceMotion ? undefined : { y: -4 }}
                      whileTap={shouldReduceMotion ? undefined : { scale: 0.99 }}
                      className={`group relative flex min-h-[174px] w-full flex-col justify-between overflow-hidden rounded-[24px] border bg-white/90 p-5 text-right shadow-[0_10px_28px_rgba(20,72,50,0.06)] backdrop-blur-sm transition-[border-color,box-shadow] duration-300 motion-reduce:transition-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-700/35 sm:p-6 ${
                        index === 1 ? 'md:-translate-y-1 md:shadow-[0_15px_34px_rgba(20,72,50,0.09)]' : ''
                      } ${
                        isActive
                          ? 'border-emerald-600/45 shadow-[0_16px_36px_rgba(16,185,129,0.13)]'
                          : 'border-emerald-900/10 hover:border-emerald-500/30 hover:shadow-[0_15px_32px_rgba(16,185,129,0.1)]'
                      }`}
                    >
                      <span className="pointer-events-none absolute right-0 top-0 h-12 w-14 rounded-tr-[24px] border-r border-t border-emerald-600/20 transition-colors duration-300 group-hover:border-emerald-500/50" />
                      <span className={`pointer-events-none absolute inset-x-5 bottom-0 h-[3px] rounded-full transition-colors duration-300 ${isActive ? 'bg-emerald-600/70' : 'bg-transparent group-hover:bg-emerald-500/35'}`} />
                      <span className="flex w-full items-center justify-between">
                        <span className="font-mono text-xs font-semibold text-emerald-800/70">0{index + 1}</span>
                        <motion.span
                          whileHover={shouldReduceMotion ? undefined : { scale: 1.07 }}
                          className="flex h-11 w-11 items-center justify-center rounded-full border border-emerald-800/5 bg-emerald-50 text-emerald-800 shadow-[0_4px_14px_rgba(16,185,129,0.08)] transition-shadow duration-300 group-hover:shadow-[0_5px_18px_rgba(16,185,129,0.2)]"
                        >
                          {stat.icon}
                        </motion.span>
                      </span>
                      <span className="mt-4 block text-sm font-semibold text-[#315747] sm:text-base">{stat.label}</span>
                      <span dir="ltr" className={`mt-2 block text-right text-4xl font-extrabold leading-none tracking-tight transition-colors duration-300 motion-reduce:transition-none sm:text-5xl ${isActive ? 'text-emerald-700' : 'text-[#0b493f]'}`}>
                        {stat.value}
                      </span>
                    </motion.button>

                    {index < stats.length - 1 && (
                      <motion.div
                        initial={shouldReduceMotion ? false : { opacity: 0 }}
                        whileInView={shouldReduceMotion ? undefined : { opacity: 1 }}
                        viewport={{ once: true, amount: 0.5 }}
                        transition={{ duration: shouldReduceMotion ? 0 : 0.4, delay: shouldReduceMotion ? 0 : index * 0.16 + 0.12 }}
                        className={`journey-connector group/connector relative flex h-14 items-center justify-center md:h-auto md:min-h-[174px] ${isActive || activeCard === index + 1 ? 'is-active' : ''}`}
                        aria-hidden="true"
                      >
                        <svg className="absolute inset-0 h-full w-full md:hidden" viewBox="0 0 64 56" preserveAspectRatio="none">
                          <path d="M32 0 C 10 18, 54 38, 32 56" fill="none" stroke="#ccebd9" strokeWidth="1.5" />
                          <motion.path
                            d="M32 0 C 10 18, 54 38, 32 56"
                            fill="none"
                            stroke={isActive || activeCard === index + 1 ? '#20a96d' : '#72c99a'}
                            strokeWidth="2"
                            strokeDasharray="2 18"
                            strokeLinecap="round"
                            animate={shouldReduceMotion ? { strokeDashoffset: 0 } : { strokeDashoffset: [0, -40] }}
                            transition={{ duration: 5, delay: shouldReduceMotion ? 0 : index * 2.5, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'linear' }}
                          />
                          <motion.circle
                            r="3.5"
                            fill="#20a96d"
                            animate={shouldReduceMotion ? { cx: 32, cy: 28 } : { cx: [32, 26, 32, 38, 32], cy: [0, 14, 28, 42, 56] }}
                            transition={{ duration: 4.8, delay: shouldReduceMotion ? 0 : index * 2.4, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'easeInOut' }}
                          />
                        </svg>
                        <svg className="absolute inset-0 hidden h-full w-full overflow-visible md:block" viewBox="0 0 100 220" preserveAspectRatio="none">
                          <path
                            d={index === 0 ? 'M100 110 C 74 20, 26 20, 0 110' : 'M100 110 C 74 200, 26 200, 0 110'}
                            fill="none"
                            stroke="#ccebd9"
                            strokeWidth="1.5"
                          />
                          <motion.path
                            d={index === 0 ? 'M100 110 C 74 20, 26 20, 0 110' : 'M100 110 C 74 200, 26 200, 0 110'}
                            fill="none"
                            stroke={isActive || activeCard === index + 1 ? '#20a96d' : '#72c99a'}
                            strokeWidth="2"
                            strokeDasharray="2 20"
                            strokeLinecap="round"
                            animate={shouldReduceMotion ? { strokeDashoffset: 0 } : { strokeDashoffset: [0, -44] }}
                            transition={{ duration: 5, delay: shouldReduceMotion ? 0 : index * 2.5, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'linear' }}
                          />
                          <motion.circle
                            r="3.5"
                            fill="#20a96d"
                            animate={shouldReduceMotion
                              ? { cx: 50, cy: 110 }
                              : {
                                  cx: [100, 77, 50, 23, 0],
                                  cy: index === 0 ? [110, 58, 43, 58, 110] : [110, 162, 177, 162, 110]
                                }}
                            transition={{ duration: 4.8, delay: shouldReduceMotion ? 0 : index * 2.4, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'easeInOut' }}
                          />
                        </svg>
                        <span className={`absolute left-1/2 top-1/2 z-10 flex h-9 w-9 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full border border-emerald-600/25 bg-white text-emerald-800 shadow-[0_3px_14px_rgba(16,185,129,0.12)] transition duration-300 motion-reduce:transition-none ${shouldReduceMotion ? '' : 'group-hover/connector:scale-110'} group-hover/connector:border-emerald-500/60 group-hover/connector:shadow-[0_4px_20px_rgba(16,185,129,0.22)]`}>
                          <motion.span
                            className="hidden md:flex"
                            animate={shouldReduceMotion ? { x: 0 } : { x: [0, -4, 0] }}
                            transition={{ duration: 2.4, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'easeInOut' }}
                          >
                            <ArrowLeft className="h-4 w-4" />
                          </motion.span>
                          <motion.span
                            className="md:hidden"
                            animate={shouldReduceMotion ? { y: 0 } : { y: [0, 3, 0] }}
                            transition={{ duration: 2.4, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'easeInOut' }}
                          >
                            <ArrowDown className="h-4 w-4" />
                          </motion.span>
                        </span>
                      </motion.div>
                    )}
                  </React.Fragment>
                );
              })}
            </div>
          </div>

          <div className="mx-auto mt-9 max-w-[850px] rounded-[18px] border border-emerald-800/[0.08] bg-emerald-50/[0.035] px-5 py-5 sm:px-8">
            <div className="relative mx-auto grid max-w-md grid-cols-3" role="tablist" aria-label="اختيار الإحصائية">
              <span className="absolute left-[16.666%] right-[16.666%] top-4 h-px bg-emerald-900/10" />
              <motion.span
                className="absolute right-[16.666%] top-4 h-0.5 bg-emerald-600"
                animate={{ width: `${activeCard * 33.333}%` }}
                transition={{ duration: shouldReduceMotion ? 0 : 0.5, ease: 'easeInOut' }}
              />
              {stats.map((stat, index) => {
                const isActive = activeCard === index;

                return (
                  <button
                    key={stat.value}
                    id={`stat-tab-${index}`}
                    type="button"
                    role="tab"
                    aria-selected={isActive}
                    aria-controls="stat-detail-panel"
                    tabIndex={isActive ? 0 : -1}
                    onClick={() => setActiveCard(index)}
                    onKeyDown={(event) => {
                      const direction = event.key === 'ArrowLeft' ? 1 : event.key === 'ArrowRight' ? -1 : 0;
                      if (!direction) return;
                      event.preventDefault();
                      const nextIndex = (index + direction + stats.length) % stats.length;
                      setActiveCard(nextIndex);
                      document.getElementById(`stat-tab-${nextIndex}`)?.focus();
                    }}
                    className="relative z-10 flex flex-col items-center gap-2 rounded-md py-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-700/40"
                  >
                    <span className={`relative flex h-8 w-8 items-center justify-center rounded-full border text-xs font-bold transition-colors duration-300 motion-reduce:transition-none ${isActive ? 'border-emerald-600 bg-white text-white' : 'border-emerald-900/15 bg-white text-[#718078]'}`}>
                      {isActive && (
                        <motion.span
                          layoutId="active-stat-indicator"
                          className="absolute inset-0 rounded-full bg-emerald-600"
                          transition={{ duration: shouldReduceMotion ? 0 : 0.5, ease: 'easeInOut' }}
                        />
                      )}
                      <span className="relative z-10">0{index + 1}</span>
                    </span>
                    <span className={`text-[11px] font-medium sm:text-xs ${isActive ? 'text-emerald-900' : 'text-[#8a938d]'}`}>{stat.label}</span>
                  </button>
                );
              })}
            </div>

            <div
              id="stat-detail-panel"
              role="tabpanel"
              aria-labelledby={`stat-tab-${activeCard}`}
              className="mx-auto mt-5 flex min-h-[150px] max-w-[740px] flex-col items-center justify-center border-t border-emerald-900/[0.07] px-1 pt-5 text-center sm:px-4"
            >
              <AnimatePresence mode="wait" initial={false}>
                <motion.div
                  key={activeCard}
                  initial={shouldReduceMotion ? false : { opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={shouldReduceMotion ? undefined : { opacity: 0, y: -8 }}
                  transition={{ duration: shouldReduceMotion ? 0 : 0.3, ease: 'easeOut' }}
                  aria-live="polite"
                >
                  <div className="flex flex-wrap items-baseline justify-center gap-x-3 gap-y-1">
                    <h3 id="stat-detail-heading" className="text-lg font-bold text-[#214f3d] sm:text-xl">{stats[activeCard].label}</h3>
                    <span dir="ltr" className="text-2xl font-extrabold text-emerald-800 sm:text-3xl">{stats[activeCard].value}</span>
                  </div>
                  <p className="mx-auto mt-3 max-w-[650px] rounded-md border-r-4 border-emerald-500 bg-emerald-50/70 px-4 py-3 text-sm leading-[1.8] text-[#43594d] sm:text-base">
                    {stats[activeCard].description}
                  </p>
                </motion.div>
              </AnimatePresence>
            </div>
          </div>

        </div>
      </section>

      <section
        ref={verificationSectionRef}
        className="relative isolate overflow-hidden py-20 text-white md:py-24"
        style={{ background: 'radial-gradient(circle at 10% 20%, rgba(55,255,170,0.2), transparent 30%), radial-gradient(circle at 90% 75%, rgba(35,210,140,0.14), transparent 35%), linear-gradient(135deg, #087653 0%, #006747 45%, #004c38 100%)' }}
      >
        <div aria-hidden="true" className="pointer-events-none absolute inset-0 overflow-hidden">
          <motion.span
            animate={shouldReduceMotion ? { rotate: 0 } : { rotate: 360 }}
            transition={{ duration: 70, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'linear' }}
            className="absolute -right-52 -top-44 h-[600px] w-[600px] rounded-full border border-emerald-100/10"
          />
          <motion.span
            animate={shouldReduceMotion ? { rotate: 0 } : { rotate: -360 }}
            transition={{ duration: 82, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'linear' }}
            className="absolute -bottom-72 -left-48 h-[700px] w-[700px] rounded-full border border-emerald-100/[0.08]"
          />
          <span className="absolute -right-28 top-1/3 h-80 w-80 rounded-full border border-emerald-100/[0.06]" />
          <motion.span
            animate={shouldReduceMotion ? { y: 0, opacity: 0.12 } : { y: [0, -12, 0], opacity: [0.1, 0.2, 0.1] }}
            transition={{ duration: 7, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'easeInOut' }}
            className="absolute right-[17%] top-[22%] h-1.5 w-1.5 rounded-full bg-[#5ef2b1]"
          />
          <motion.span
            animate={shouldReduceMotion ? { y: 0, opacity: 0.12 } : { y: [0, 10, 0], opacity: [0.1, 0.18, 0.1] }}
            transition={{ duration: 9, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'easeInOut' }}
            className="absolute bottom-[24%] left-[21%] h-1 w-1 rounded-full bg-[#5ef2b1]"
          />
        </div>

        <div className="relative z-10 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <motion.header
            initial={shouldReduceMotion ? false : { opacity: 0, y: 12 }}
            whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.35 }}
            transition={{ duration: 0.4 }}
            className="mx-auto max-w-3xl text-right"
          >
            <span className="inline-flex items-center gap-3 text-sm font-medium text-white/75">
              <span className="h-px w-8 bg-[#5ef2b1]/65" />
              من الرقم إلى التحقق
            </span>
            <h2 className="mt-4 text-3xl font-extrabold leading-tight text-white sm:text-4xl md:text-5xl">
              ماذا ينبغي أن <span className="text-[#5ef2b1]">نسأل؟</span>
            </h2>
            <p className="mt-4 text-sm leading-[1.85] text-white/80 sm:text-base md:text-lg">
              لا تعني هذه الأرقام أن كل ما يُنشر على وسائل التواصل غير صحيح؛ بل تدعونا إلى أسئلة أوضح قبل مشاركة المحتوى.
            </p>
          </motion.header>

          <div className="relative mx-auto mt-10 max-w-6xl md:mt-14">
            <svg className="pointer-events-none absolute inset-x-0 top-5 hidden h-[130px] w-full overflow-visible md:block" viewBox="0 0 1000 140" preserveAspectRatio="none" aria-hidden="true">
              <path d={desktopJourneyPath} fill="none" stroke="rgba(94,242,177,0.3)" strokeWidth="2.5" />
              {!shouldReduceMotion && (
                <motion.path
                  d={desktopJourneyPath}
                  fill="none"
                  stroke="#5ef2b1"
                  strokeWidth="3"
                  strokeLinecap="round"
                  strokeDasharray="34 1150"
                  animate={{ strokeDashoffset: [0, -1184] }}
                  transition={{ duration: 11.5, repeat: Infinity, ease: 'linear' }}
                />
              )}
              {!shouldReduceMotion && (
                <motion.circle
                  r="5"
                  fill="#b3ffdc"
                  style={{ filter: 'drop-shadow(0 0 7px rgba(94,242,177,0.9))' }}
                  initial={{ cx: desktopJourneyPoints[0][0], cy: desktopJourneyPoints[0][1] }}
                  animate={{
                    cx: desktopJourneyPoints.map(([x]) => x),
                    cy: desktopJourneyPoints.map(([, y]) => y)
                  }}
                  transition={{ duration: 11.5, repeat: Infinity, ease: 'linear' }}
                />
              )}
            </svg>

            {verificationQuestions.slice(0, 4).map((_, index) => (
              <motion.span
                key={`desktop-arrow-${index}`}
                aria-hidden="true"
                animate={shouldReduceMotion ? { x: 0, scale: 1 } : { x: [0, -4, 0], scale: [1, 1.04, 1] }}
                transition={{ duration: 2.2, delay: index * 0.12, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'easeInOut' }}
                className="absolute top-[68px] z-20 hidden h-9 w-9 items-center justify-center rounded-full border border-[#5ef2b1]/45 bg-[#006747] text-white shadow-[0_0_18px_rgba(94,242,177,0.18)] md:flex"
                style={{ right: `${18 + index * 20}%` }}
              >
                <ArrowLeft className="h-4 w-4" />
              </motion.span>
            ))}

            <div className="relative z-10 grid grid-cols-1 md:grid-cols-5 md:gap-2" role="tablist" aria-label="مراحل التحقق">
              {verificationQuestions.map((question, index) => {
                const isActive = activeQuestion === index;

                return (
                  <React.Fragment key={question.num}>
                    <motion.button
                      id={`verification-step-${index}`}
                      type="button"
                      role="tab"
                      aria-selected={isActive}
                      aria-controls="verification-detail-panel"
                      tabIndex={isActive ? 0 : -1}
                      onClick={() => selectVerificationQuestion(index)}
                      onFocus={() => { manualPauseUntil.current = Date.now() + 7000; }}
                      onKeyDown={(event) => {
                        const direction = event.key === 'ArrowLeft' || event.key === 'ArrowDown'
                          ? 1
                          : event.key === 'ArrowRight' || event.key === 'ArrowUp'
                            ? -1
                            : 0;
                        if (!direction) return;
                        event.preventDefault();
                        const nextIndex = (index + direction + verificationQuestions.length) % verificationQuestions.length;
                        selectVerificationQuestion(nextIndex);
                        document.getElementById(`verification-step-${nextIndex}`)?.focus();
                      }}
                      initial={shouldReduceMotion ? false : { opacity: 0, y: 12 }}
                      whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
                      viewport={{ once: true, amount: 0.25 }}
                      transition={{ duration: shouldReduceMotion ? 0 : 0.35, delay: shouldReduceMotion ? 0 : index * 0.08 }}
                      whileHover={shouldReduceMotion ? undefined : { y: -4 }}
                      className="group flex min-h-[200px] w-full flex-col items-center rounded-2xl px-2 py-2 text-center focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#5ef2b1]/70 md:min-h-[218px]"
                    >
                      <span className={`mb-3 font-mono text-xs transition-colors ${isActive ? 'text-[#a4ffd2]' : 'text-white/55 group-hover:text-white/80'}`}>
                        {question.num}
                      </span>
                      <motion.span
                        animate={isActive && !shouldReduceMotion ? { scale: [1, 1.04, 1] } : { scale: 1 }}
                        transition={{ duration: 2.1, repeat: isActive && !shouldReduceMotion ? Infinity : 0, ease: 'easeInOut' }}
                        className={`flex h-24 w-24 items-center justify-center rounded-[26px] border backdrop-blur-xl transition-[border-color,background-color,box-shadow] duration-300 motion-reduce:transition-none sm:h-[100px] sm:w-[100px] ${isActive
                          ? 'border-[#5ef2b1]/75 bg-[#ffffff]/15 text-[#b3ffdc] shadow-[0_0_0_1px_rgba(94,242,177,0.35),0_0_28px_rgba(94,242,177,0.22)]'
                          : 'border-[#a4ffd2]/25 bg-white/[0.07] text-white/85 shadow-[0_8px_30px_rgba(0,0,0,0.1)] group-hover:border-[#5ef2b1]/55 group-hover:bg-white/[0.1]'
                        }`}
                      >
                        {question.icon}
                      </motion.span>
                      <span className={`mt-4 max-w-[170px] text-sm font-semibold leading-relaxed transition-colors sm:text-base ${isActive ? 'text-white' : 'text-white/70 group-hover:text-white/90'}`}>
                        {question.text}
                      </span>
                      <span className={`mt-2 h-0.5 rounded-full bg-[#5ef2b1] transition-all duration-300 motion-reduce:transition-none ${isActive ? 'w-8 opacity-100' : 'w-0 opacity-0'}`} />
                    </motion.button>

                    {index < verificationQuestions.length - 1 && (
                      <div className="relative flex h-12 items-center justify-center md:hidden" aria-hidden="true">
                        <svg className="absolute inset-0 h-full w-full" viewBox="0 0 100 56" preserveAspectRatio="none">
                          <path d="M50 0 C 48 15, 52 41, 50 56" fill="none" stroke="rgba(94,242,177,0.3)" strokeWidth="2" />
                          {!shouldReduceMotion && (
                            <motion.path
                              d="M50 0 C 48 15, 52 41, 50 56"
                              fill="none"
                              stroke="#5ef2b1"
                              strokeWidth="2.5"
                              strokeDasharray="7 80"
                              animate={{ strokeDashoffset: [0, -87] }}
                              transition={{ duration: 2.3, delay: index * 0.08, repeat: Infinity, ease: 'linear' }}
                            />
                          )}
                          {!shouldReduceMotion && (
                            <motion.circle
                              r="4"
                              fill="#b3ffdc"
                              style={{ filter: 'drop-shadow(0 0 5px rgba(94,242,177,0.9))' }}
                              animate={{ cx: [50, 49, 50, 51, 50], cy: [0, 14, 28, 42, 56] }}
                              transition={{ duration: 2.3, delay: index * 0.08, repeat: Infinity, ease: 'easeInOut' }}
                            />
                          )}
                        </svg>
                        <motion.span
                          animate={shouldReduceMotion ? { y: 0, scale: 1 } : { y: [0, 3, 0], scale: [1, 1.04, 1] }}
                          transition={{ duration: 2.2, delay: index * 0.12, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'easeInOut' }}
                          className="relative z-10 flex h-9 w-9 items-center justify-center rounded-full border border-[#5ef2b1]/45 bg-[#006747] text-white shadow-[0_0_16px_rgba(94,242,177,0.18)]"
                        >
                          <ArrowDown className="h-4 w-4" />
                        </motion.span>
                      </div>
                    )}
                  </React.Fragment>
                );
              })}
            </div>
          </div>

          <motion.div
            id="verification-detail-panel"
            role="tabpanel"
            aria-labelledby={`verification-step-${activeQuestion}`}
            initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }}
            whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: shouldReduceMotion ? 0 : 0.4 }}
            className="mx-auto mt-8 max-w-4xl rounded-[28px] border border-[#78ffbe]/25 bg-[#004c38]/35 p-5 shadow-[0_18px_50px_rgba(0,42,30,0.12)] backdrop-blur-[18px] sm:p-8"
          >
            <div className="relative h-3 overflow-visible rounded-full bg-white/[0.12]" aria-label={`التقدم ${((activeQuestion + 1) * 20)}%`}>
              <motion.span
                className="absolute right-0 top-0 h-full rounded-full bg-gradient-to-l from-[#54f3b0] to-[#00c77b] shadow-[0_0_16px_rgba(84,243,176,0.35)]"
                animate={{ width: `${(activeQuestion + 1) * 20}%` }}
                transition={{ duration: shouldReduceMotion ? 0 : 0.7, ease: [0.22, 1, 0.36, 1] }}
              />
              <span
                className="absolute top-1/2 h-4 w-4 -translate-y-1/2 rounded-full border-2 border-[#c5ffe3] bg-[#54f3b0] shadow-[0_0_14px_rgba(84,243,176,0.8)] transition-[right] duration-700 motion-reduce:transition-none"
                style={{ right: `calc(${(activeQuestion + 1) * 20}% - 8px)` }}
              />
            </div>

            <div className="mt-7 min-h-[170px] sm:min-h-[150px]">
              <AnimatePresence mode="wait" initial={false}>
                <motion.div
                  key={activeQuestion}
                  initial={shouldReduceMotion ? false : { opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={shouldReduceMotion ? undefined : { opacity: 0, y: -8 }}
                  transition={{ duration: shouldReduceMotion ? 0 : 0.35, ease: 'easeOut' }}
                  aria-live="polite"
                  className="flex min-h-[170px] flex-col items-center justify-center text-center sm:min-h-[150px] sm:flex-row sm:gap-6 sm:text-right"
                >
                  <motion.span
                    animate={shouldReduceMotion ? { scale: 1 } : { scale: [1, 1.04, 1] }}
                    transition={{ duration: 2.2, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'easeInOut' }}
                    className="mb-4 flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl border border-[#78ffbe]/35 bg-white/[0.08] text-[#aaffd3] shadow-[0_0_22px_rgba(94,242,177,0.12)] sm:mb-0"
                  >
                    {verificationQuestions[activeQuestion].icon}
                  </motion.span>
                  <div>
                    <div className="flex flex-wrap items-baseline justify-center gap-x-3 gap-y-1 sm:justify-start">
                      <span className="font-mono text-sm text-[#aaffd3]/75">{verificationQuestions[activeQuestion].num}</span>
                      <h3 className="text-xl font-bold text-white sm:text-2xl">{verificationQuestions[activeQuestion].text}</h3>
                    </div>
                    <p className="mt-3 max-w-2xl text-sm leading-[1.85] text-white/80 sm:text-base">
                      {verificationQuestions[activeQuestion].detail}
                    </p>
                  </div>
                </motion.div>
              </AnimatePresence>
            </div>
          </motion.div>
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
