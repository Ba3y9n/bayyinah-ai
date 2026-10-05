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
        <div className="absolute inset-0 rounded-full border border-white/10 bg-white/5 backdrop-blur-[1px]" />
        <div className="absolute inset-[18%] rounded-full border border-dashed border-white/15" />
        <div className="absolute inset-[33%] rounded-full border border-white/10" />

        <div className="absolute z-30 w-24 h-24 md:w-32 md:h-32 rounded-full bg-white flex flex-col items-center justify-center text-center p-2 shadow-[0_0_40px_rgba(255,255,255,0.35)] border border-[#D2EFE9]">
          <span className="text-[#0a2d2b] font-bold text-base md:text-lg tracking-wide">بيّنة AI</span>
          <span className="text-[10px] md:text-xs text-[#1b5f59] mt-0.5">محرك التحقق</span>
        </div>

        {steps.map((step, idx) => {
          const angle = (idx * (360 / steps.length) - 90) * (Math.PI / 180);
          const radius = window.innerWidth < 768 ? 120 : 170;
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

      <div className="mt-8 p-5 bg-white/95 rounded-2xl shadow-[0_12px_30px_rgba(0,0,0,0.12)] border border-white/40 max-w-md w-full text-center z-40 transition-all duration-300 transform min-h-[92px] flex flex-col justify-center backdrop-blur-sm">
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
  return (
    <div className="flex flex-col bg-bayyinah-ivory text-bayyinah-dark-text overflow-x-hidden">
      
      {/* 1. HERO SECTION */}
      <section className="relative min-h-[90vh] flex flex-col items-center pt-28 pb-16 overflow-hidden bg-[#0a302d]">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(60,162,146,0.18),_rgba(10,48,45,0.96)_55%,_rgba(4,17,16,1)_100%)]" />
        <div className="absolute inset-0 opacity-60" style={{ backgroundImage: 'linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)', backgroundSize: '40px 40px' }} />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full flex flex-col items-center justify-center gap-12 text-center">
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="max-w-3xl"
          >
            <h1 className="text-shadow-soft text-4xl md:text-6xl lg:text-7xl font-black text-white leading-[1.15] tracking-tight mb-4">
              تحقّق قبل أن تنشر.
            </h1>
            <p className="text-lg md:text-2xl text-white/80 max-w-2xl mx-auto leading-relaxed font-medium">
              بيّنة تساعدك على التحقق من الادعاءات الإسلامية بالرجوع إلى المصادر المعتمدة وإظهار الدليل.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="w-full flex justify-center"
          >
            <HeroOrbit />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.35 }}
            className="flex justify-center"
          >
            <button
              onClick={onStartVerification}
              className="bg-[#0f8b7e] hover:bg-[#0c776d] text-white px-10 py-4 rounded-2xl font-bold text-xl transition-all shadow-[0_0_24px_rgba(15,139,126,0.35)] cursor-pointer flex items-center justify-center gap-3"
            >
              ابدأ التحقق
              <ArrowLeft className="w-6 h-6" />
            </button>
          </motion.div>
        </div>
      </section>

      {/* 2. PROBLEM SECTION (Rule 38) */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mb-16">
            <span className="text-xs font-bold text-bayyinah-emerald uppercase tracking-wider block mb-3">واقع المحتوى المتداول</span>
            <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-bayyinah-dark-text mb-6 leading-tight">
              سرعة الانتشار... وغياب التحقق
            </h2>
            <div className="space-y-4 text-lg md:text-xl text-bayyinah-secondary-text leading-relaxed font-light">
              <p>
                مع الانتشار السريع للمحتوى الرقمي، أصبح الوصول إلى المحتوى الإسلامي المتداول أسهل، لكن التحقق من مصدره ودرجة ثبوته لا يكون واضحًا دائمًا للمستخدم.
              </p>
              <p>
                تنتشر الأحاديث الضعيفة أو الموضوعة، والأدعية غير الثابتة، والمقولات المحرّفة أو المنسوبة إلى العلماء دون توثيق واضح.
              </p>
              <p className="font-medium text-bayyinah-dark-text">
                وتزداد الحاجة إلى أدوات تساعد المستخدم على الوصول إلى المصدر والدليل بدل الاكتفاء بإجابة مولدة بالذكاء الاصطناعي.
              </p>
            </div>
          </div>

          {/* 3. STATISTICS (Rule 39 & 40: 63%, 37.5%, 3,281) */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
            {/* Stat 1 */}
            <div className="bg-bayyinah-ivory p-8 rounded-3xl border border-gray-100 flex flex-col justify-between hover:border-bayyinah-emerald/30 transition-all">
              <div>
                <span className="text-6xl md:text-7xl font-bold text-bayyinah-deep-emerald block mb-4 tracking-tighter">
                  63%
                </span>
                <p className="text-sm md:text-base text-bayyinah-secondary-text leading-relaxed">
                  من محتوى الأحاديث على Instagram في إحدى الدراسات المنشورة عام 2025 لم يتضمن بيانًا لحالة الحديث من حيث الأصالة.
                </p>
              </div>

            </div>

            {/* Stat 2 */}
            <div className="bg-bayyinah-ivory p-8 rounded-3xl border border-gray-100 flex flex-col justify-between hover:border-bayyinah-emerald/30 transition-all">
              <div>
                <span className="text-6xl md:text-7xl font-bold text-bayyinah-deep-emerald block mb-4 tracking-tighter">
                  37.5%
                </span>
                <p className="text-sm md:text-base text-bayyinah-secondary-text leading-relaxed">
                  من العينة المدروسة في دراسة أخرى منشورة عام 2025 لم تتضمن حالة توثيق الحديث.
                </p>
              </div>

            </div>

            {/* Stat 3 */}
            <div className="bg-bayyinah-ivory p-8 rounded-3xl border border-gray-100 flex flex-col justify-between hover:border-bayyinah-emerald/30 transition-all">
              <div>
                <span className="text-6xl md:text-7xl font-bold text-bayyinah-deep-emerald block mb-4 tracking-tighter">
                  3,281
                </span>
                <p className="text-sm md:text-base text-bayyinah-secondary-text leading-relaxed">
                  مادة وحديثًا مما اشتهر على ألسنة الناس في كتاب "كشف الخفاء ومزيل الإلباس" للإمام العجلوني.
                </p>
              </div>

            </div>
          </div>

          {/* RESTUCTURED BOX */}
          <div className="mt-12">
            <div className="mb-6">
              <h3 className="text-2xl font-bold text-bayyinah-dark-text mb-2">ماذا تعني هذه الأرقام؟</h3>
              <p className="text-base text-bayyinah-secondary-text">لا تعني هذه الأرقام أن كل ما يُنشر على وسائل التواصل غير صحيح. بل تكشف مشكلة أكثر تحديدًا:</p>
            </div>
            
            <div className="flex flex-col lg:flex-row items-center justify-between gap-2 lg:gap-4 mt-8">
              {[
                { num: '01', text: 'هل تم توثيقه؟' },
                { num: '02', text: 'ما مصدره؟' },
                { num: '03', text: 'هل النص مطابق؟' },
                { num: '04', text: 'ما درجة ثبوته؟' },
                { num: '05', text: 'هل توجد مصادر أخرى؟' },
              ].map((item, i) => (
                <React.Fragment key={i}>
                  <motion.div 
                    whileHover={{ scale: 1.05, y: -5 }}
                    className="flex-1 w-full bg-white p-6 rounded-2xl border border-gray-100 hover:border-bayyinah-emerald shadow-sm hover:shadow-elevated transition-all duration-300 cursor-default text-center"
                  >
                    <span className="text-bayyinah-emerald font-bold mb-3 block text-xl">{item.num}</span>
                    <h4 className="text-bayyinah-dark-text font-bold text-base leading-relaxed">{item.text}</h4>
                  </motion.div>
                  {i < 4 && (
                    <div className="hidden lg:flex items-center text-gray-300">
                      <ArrowLeft className="w-6 h-6" />
                    </div>
                  )}
                </React.Fragment>
              ))}
            </div>
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
