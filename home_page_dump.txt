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
    <div 
      className="relative w-[340px] h-[340px] md:w-[480px] md:h-[480px] mx-auto lg:mr-auto lg:ml-0 flex items-center justify-center"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Center Element: بيّنة AI */}
      <div className="absolute z-30 w-24 h-24 md:w-32 md:h-32 rounded-full bg-bayyinah-deep-emerald/90 backdrop-blur-md border-2 border-bayyinah-soft-emerald/60 flex flex-col items-center justify-center text-center p-2 shadow-[0_0_40px_rgba(53,185,154,0.3)]">
        <span className="text-white font-bold text-base md:text-lg tracking-wide">بيّنة AI</span>
        <span className="text-[10px] md:text-xs text-bayyinah-soft-emerald mt-0.5">محرك التحقق</span>
      </div>

      {/* Background Orbit Rings */}
      <motion.div 
        className="absolute inset-0 rounded-full border-2 border-bayyinah-emerald/40 shadow-[inset_0_0_50px_rgba(53,185,154,0.1)]"
        animate={{ rotate: isHovered ? 0 : 360 }}
        transition={{ duration: 70, repeat: Infinity, ease: "linear" }}
      />
      <motion.div 
        className="absolute inset-6 md:inset-10 rounded-full border border-bayyinah-emerald/20 border-dashed"
        animate={{ rotate: isHovered ? 0 : -360 }}
        transition={{ duration: 90, repeat: Infinity, ease: "linear" }}
      />

      {/* Orbit Nodes (6 nodes - Rule 37) */}
      {steps.map((step, idx) => {
        const angle = (idx * (360 / steps.length) - 90) * (Math.PI / 180);
        const radius = window.innerWidth < 768 ? 135 : 195; 
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
              className={`w-11 h-11 md:w-14 md:h-14 rounded-full flex items-center justify-center transition-all duration-500 backdrop-blur-md cursor-pointer border-2
                ${isActive ? 'bg-bayyinah-emerald text-white border-bayyinah-soft-emerald shadow-[0_0_30px_rgba(53,185,154,0.9)] scale-115' : 'bg-[#042822]/80 text-white hover:bg-bayyinah-emerald/40 hover:border-bayyinah-emerald border-bayyinah-emerald/40'}`}
              whileHover={{ scale: 1.15 }}
              whileTap={{ scale: 0.95 }}
            >
              {step.icon}
            </motion.button>
            <div className={`mt-1.5 font-bold transition-all duration-300 ${isActive ? 'text-white text-base drop-shadow-md' : 'text-white/70 text-xs'}`}>
              {step.label}
            </div>
            
            {/* Tooltip Card */}
            <AnimatePresence>
              {isActive && (
                <motion.div
                  initial={{ opacity: 0, y: 10, scale: 0.9 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="absolute top-16 md:top-20 w-48 md:w-56 p-4 rounded-xl bg-bayyinah-deep-emerald/95 backdrop-blur-xl border border-white/20 text-white shadow-2xl text-center z-50 pointer-events-none"
                >
                  <p className="text-xs md:text-sm font-medium leading-relaxed drop-shadow-sm">{step.desc}</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        );
      })}
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
  const [activeStep, setActiveStep] = useState(0);
  
  const steps = [
    { title: 'الفهم الذكي قبل التحقق', desc: 'لا تتعامل بيّنة مع المحتوى ككتلة نصية فقط، بل تفهم السياق وتحدد الادعاءات التي تحتاج إلى تحقق.', icon: <Layout className="w-6 h-6"/> },
    { title: 'المصدر أولًا', desc: 'تبحث بيّنة في المصادر المعتمدة والمرتبطة بنوع المحتوى والادعاء، بعيدًا عن التخمين.', icon: <Database className="w-6 h-6"/> },
    { title: 'الدليل ظاهر', desc: 'لا تكتفي بيّنة بالنتيجة، بل تعرض الدليل والمصدر والمرجع والرابط ليتمكن المستخدم من مراجعتها.', icon: <BookOpen className="w-6 h-6"/> },
    { title: 'الأمانة العلمية', desc: 'إذا لم تجد بيّنة دليلًا كافيًا، لا تنشئ يقينًا من الفراغ، بل توضّح حدود ما تم التوصل إليه.', icon: <ShieldCheck className="w-6 h-6"/> },
    { title: 'معالجة متعددة الوسائط', desc: 'يمكن التحقق من: النص، الصورة، الفيديو، الرابط.', icon: <Link2 className="w-6 h-6"/> }
  ];

  return (
    <div className="flex flex-col lg:flex-row gap-16 items-center">
      <div className="flex-1 flex flex-col gap-6 w-full">
        {steps.map((step, idx) => {
          const isActive = activeStep === idx;
          return (
            <button
              key={idx}
              onClick={() => setActiveStep(idx)}
              className={`flex items-start gap-4 p-6 rounded-2xl transition-all duration-300 text-right border ${
                isActive 
                  ? 'bg-bayyinah-emerald text-white border-bayyinah-soft-emerald shadow-elevated' 
                  : 'bg-white border-gray-100 hover:border-bayyinah-emerald/30'
              }`}
            >
              <div className={`mt-1 p-2 rounded-xl transition-colors ${isActive ? 'bg-white/20 text-white' : 'bg-bayyinah-ivory text-bayyinah-emerald'}`}>
                {step.icon}
              </div>
              <div>
                <h3 className={`text-lg font-bold mb-2 ${isActive ? 'text-white' : 'text-bayyinah-dark-text'}`}>
                  0{idx + 1} — {step.title}
                </h3>
                <AnimatePresence>
                  {isActive && (
                    <motion.p 
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="text-sm md:text-base text-white/90 leading-relaxed overflow-hidden"
                    >
                      {step.desc}
                    </motion.p>
                  )}
                </AnimatePresence>
              </div>
            </button>
          );
        })}
      </div>
      
      <div className="flex-1 w-full bg-white rounded-3xl p-8 lg:p-16 relative overflow-hidden min-h-[400px] flex items-center justify-center border border-gray-100 shadow-sm">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-bayyinah-ivory to-transparent"></div>
        <AnimatePresence mode="wait">
          <motion.div
            key={activeStep}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.4 }}
            className="relative z-10 w-full"
          >
            {/* Visual representation based on step */}
            {activeStep === 0 && (
              <div className="flex flex-col gap-4 text-bayyinah-dark-text">
                <div className="bg-bayyinah-ivory p-4 rounded-xl border border-gray-200">كتلة المحتوى الأصلية...</div>
                <div className="flex justify-center"><ArrowLeft className="w-5 h-5 -rotate-90 text-bayyinah-emerald" /></div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-white p-4 rounded-xl text-center text-sm font-medium border border-bayyinah-emerald/30 shadow-sm text-bayyinah-emerald">ادعاء 1</div>
                  <div className="bg-white p-4 rounded-xl text-center text-sm font-medium border border-bayyinah-emerald/30 shadow-sm text-bayyinah-emerald">ادعاء 2</div>
                </div>
              </div>
            )}
            {activeStep === 1 && (
              <div className="flex flex-col items-center gap-6 text-bayyinah-dark-text">
                <Database className="w-16 h-16 text-bayyinah-emerald mb-2" />
                <div className="flex flex-col w-full gap-3">
                  <div className="bg-bayyinah-ivory p-4 rounded-xl border border-bayyinah-emerald border-dashed text-center">بحث في القرآن الكريم</div>
                  <div className="bg-bayyinah-ivory p-4 rounded-xl border border-bayyinah-emerald border-dashed text-center">بحث في السنة النبوية</div>
                </div>
              </div>
            )}
            {activeStep === 2 && (
              <div className="flex flex-col gap-4 text-bayyinah-dark-text w-full max-w-sm mx-auto">
                <div className="bg-bayyinah-ivory p-4 rounded-xl flex items-center justify-between border border-gray-200">
                  <span>المصدر</span>
                  <span className="text-bayyinah-emerald font-bold">صحيح البخاري</span>
                </div>
                <div className="w-px h-6 bg-bayyinah-emerald/30 mx-auto"></div>
                <div className="bg-bayyinah-ivory p-4 rounded-xl flex items-center justify-between border border-gray-200">
                  <span>المرجع</span>
                  <span className="text-bayyinah-emerald font-bold">حديث رقم 1</span>
                </div>
                <div className="w-px h-6 bg-bayyinah-emerald/30 mx-auto"></div>
                <div className="bg-white p-4 rounded-xl flex flex-col gap-2 border border-bayyinah-emerald shadow-sm text-center">
                  <span className="text-xs text-bayyinah-secondary-text">النتيجة</span>
                  <span className="font-bold text-bayyinah-emerald-dark">ثابت بحسب المصدر</span>
                </div>
              </div>
            )}
            {activeStep === 3 && (
              <div className="flex flex-col items-center justify-center gap-6 text-bayyinah-dark-text h-full">
                <div className="w-24 h-24 rounded-full border-4 border-dashed border-bayyinah-emerald/50 flex items-center justify-center relative bg-bayyinah-ivory">
                  <ShieldCheck className="w-10 h-10 text-bayyinah-emerald" />
                  <motion.div className="absolute inset-0 border-4 border-bayyinah-emerald rounded-full border-t-transparent" animate={{ rotate: 360 }} transition={{ duration: 4, repeat: Infinity, ease: "linear" }} />
                </div>
                <div className="text-center font-medium bg-white px-6 py-3 rounded-xl border border-gray-200 shadow-sm">
                  عرض الأدلة المتوفرة بشفافية
                </div>
              </div>
            )}
            {activeStep === 4 && (
              <div className="grid grid-cols-2 gap-4 text-bayyinah-dark-text">
                <div className="bg-bayyinah-ivory p-6 rounded-xl flex flex-col items-center gap-3 border border-gray-200 hover:border-bayyinah-emerald/50 transition-colors cursor-default">
                  <FileText className="w-8 h-8 text-bayyinah-emerald" />
                  <span>نص</span>
                </div>
                <div className="bg-bayyinah-ivory p-6 rounded-xl flex flex-col items-center gap-3 border border-gray-200 hover:border-bayyinah-emerald/50 transition-colors cursor-default">
                  <ImageIcon className="w-8 h-8 text-bayyinah-emerald" />
                  <span>صورة</span>
                </div>
                <div className="bg-bayyinah-ivory p-6 rounded-xl flex flex-col items-center gap-3 border border-gray-200 hover:border-bayyinah-emerald/50 transition-colors cursor-default">
                  <FileVideo className="w-8 h-8 text-bayyinah-emerald" />
                  <span>فيديو</span>
                </div>
                <div className="bg-bayyinah-ivory p-6 rounded-xl flex flex-col items-center gap-3 border border-gray-200 hover:border-bayyinah-emerald/50 transition-colors cursor-default">
                  <Link2 className="w-8 h-8 text-bayyinah-emerald" />
                  <span>رابط</span>
                </div>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>
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
      <div className="relative mb-12 flex items-center justify-between overflow-x-auto pb-6 hide-scrollbar">
        <div className="absolute top-1/2 left-0 right-0 h-px bg-gray-200 -translate-y-1/2 z-0 min-w-[800px]"></div>
        
        {steps.map((step, idx) => {
          const isActive = activeTab === idx;
          const isPast = activeTab > idx;
          return (
            <button 
              key={idx}
              onClick={() => setActiveTab(idx)}
              className="relative z-10 flex flex-col items-center gap-3 min-w-[120px] cursor-pointer group"
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
                  <span className="px-4 py-2 bg-bayyinah-emerald text-white rounded-lg text-sm">ثابت بحسب المصدر</span>
                  <span className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm">لم يثبت بهذا اللفظ</span>
                  <span className="px-4 py-2 bg-gray-600 text-white rounded-lg text-sm">لم نجد دليلًا كافيًا</span>
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
      <section className="relative min-h-[90vh] flex items-center pt-20 overflow-hidden">
        {/* Background Image Layer exactly as Dawr reference */}
        <div className="absolute inset-0 z-0 bg-bayyinah-deep-emerald">
          <img 
            src="/hero-bg.jpg" 
            alt="Islamic Skyline" 
            className="w-full h-full object-cover object-center mix-blend-overlay opacity-60"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-bayyinah-deep-emerald/90 via-bayyinah-deep-emerald/60 to-transparent"></div>
        </div>
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full flex flex-col-reverse lg:flex-row items-center gap-12 lg:gap-8">
          
          {/* Right Content (RTL) - Typography */}
          <div className="flex-1 flex flex-col items-start text-right">
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md border border-white/20 text-bayyinah-soft-emerald px-4 py-1.5 rounded-full text-xs font-semibold mb-6 shadow-sm"
            >
              <ShieldCheck className="w-4 h-4 text-bayyinah-soft-emerald" />
              <span>Evidence-First Islamic Content Verification</span>
            </motion.div>

            <motion.h1 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 text-white leading-[1.2] drop-shadow-md"
            >
              تحقّق قبل<br/>أن تنشر.
            </motion.h1>
            
            <motion.p 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-lg md:text-2xl text-white/90 max-w-xl mb-6 leading-relaxed font-light drop-shadow-sm"
            >
              بيّنة تساعدك على التحقق من الادعاءات الإسلامية بالرجوع إلى المصادر المعتمدة وإظهار الدليل.
            </motion.p>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="text-sm text-bayyinah-soft-emerald/90 max-w-lg mb-8 font-medium bg-white/5 border border-white/10 p-3.5 rounded-2xl"
            >
              «بيّنة لا تطلب منك أن تثق بالذكاء الاصطناعي؛ بل تمكّنك من رؤية المصدر بنفسك.»
            </motion.p>
            
            <motion.div 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto"
            >
              <button 
                onClick={onStartVerification}
                className="bg-bayyinah-emerald hover:bg-bayyinah-soft-emerald text-white px-8 py-4 rounded-xl font-bold text-lg transition-colors flex items-center justify-center gap-2 shadow-[0_0_20px_rgba(53,185,154,0.4)] border border-white/10 cursor-pointer"
              >
                ابدأ التحقق
                <ArrowLeft className="w-5 h-5" />
              </button>
              <button 
                onClick={() => setActiveTab('judge-demo')}
                className="bg-transparent border border-white/30 hover:border-white hover:bg-white/10 text-white px-8 py-4 rounded-xl font-medium text-lg transition-colors cursor-pointer flex items-center justify-center gap-2"
              >
                <span>عرض الحكّام (Demo)</span>
                <ArrowLeft className="w-5 h-5" />
              </button>
            </motion.div>

            <div className="mt-8 text-xs text-white/60 flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-bayyinah-soft-emerald shrink-0" />
              <span>بيّنة نظام ذكاء اصطناعي للتحقق والمساعدة، وليست جهة إفتاء.</span>
            </div>
          </div>

          {/* Left Content (RTL) - Interactive Orbit */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="flex-1 w-full flex justify-center lg:justify-end"
          >
            <HeroOrbit />
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
              <a 
                href="https://dawa.center" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="mt-6 text-xs text-bayyinah-emerald hover:underline font-bold flex items-center gap-1"
              >
                <span>دراسة توثيق المحتوى الرقمي 2025</span>
                <ArrowLeft className="w-3.5 h-3.5" />
              </a>
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
              <a 
                href="https://islamic-content.com" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="mt-6 text-xs text-bayyinah-emerald hover:underline font-bold flex items-center gap-1"
              >
                <span>دراسة عينة المنصات الرقمية 2025</span>
                <ArrowLeft className="w-3.5 h-3.5" />
              </a>
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
              <a 
                href="https://shamela.ws" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="mt-6 text-xs text-bayyinah-emerald hover:underline font-bold flex items-center gap-1"
              >
                <span>كشف الخفاء ومزيل الإلباس</span>
                <ArrowLeft className="w-3.5 h-3.5" />
              </a>
            </div>
          </div>

          {/* WHAT DO THESE NUMBERS MEAN? (Rule 40) */}
          <div className="bg-white rounded-3xl p-10 border border-bayyinah-emerald/20 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-bayyinah-ivory to-white">
            <h3 className="text-2xl font-bold text-bayyinah-deep-emerald mb-4">ماذا تعني هذه الأرقام؟</h3>
            <p className="text-base md:text-lg text-bayyinah-secondary-text leading-relaxed mb-6">
              لا تعني هذه الأرقام أن كل ما يُنشر على وسائل التواصل غير صحيح. بل تكشف مشكلة أكثر تحديدًا:
            </p>
            
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 mb-8 text-center text-xs md:text-sm font-semibold">
              <div className="p-3 bg-white rounded-xl border border-gray-200 text-bayyinah-dark-text shadow-2xs">هل تم توثيقه؟</div>
              <div className="p-3 bg-white rounded-xl border border-gray-200 text-bayyinah-dark-text shadow-2xs">ما مصدره؟</div>
              <div className="p-3 bg-white rounded-xl border border-gray-200 text-bayyinah-dark-text shadow-2xs">هل النص مطابق؟</div>
              <div className="p-3 bg-white rounded-xl border border-gray-200 text-bayyinah-dark-text shadow-2xs">ما درجة ثبوته؟</div>
              <div className="p-3 bg-white rounded-xl border border-gray-200 text-bayyinah-dark-text shadow-2xs">هل توجد مصادر أخرى؟</div>
            </div>

            <div className="pt-6 border-t border-gray-200/60 flex flex-col md:flex-row items-center justify-between gap-4">
              <span className="font-bold text-bayyinah-deep-emerald text-sm md:text-base">وهنا يأتي دور بيّنة:</span>
              <div className="flex flex-wrap items-center justify-center gap-2 text-xs font-bold text-bayyinah-emerald">
                <span>تفهم المحتوى</span>
                <ArrowLeft className="w-3.5 h-3.5 text-gray-400" />
                <span>تحدد الادعاء</span>
                <ArrowLeft className="w-3.5 h-3.5 text-gray-400" />
                <span>تبحث في المصادر</span>
                <ArrowLeft className="w-3.5 h-3.5 text-gray-400" />
                <span>تجمع الدليل</span>
                <ArrowLeft className="w-3.5 h-3.5 text-gray-400" />
                <span>تتحقق</span>
                <ArrowLeft className="w-3.5 h-3.5 text-gray-400" />
                <span className="bg-bayyinah-emerald text-white px-2.5 py-1 rounded-md">تعرض النتيجة</span>
              </div>
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
              className="relative"
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
              className="bg-white p-10 rounded-3xl border border-gray-100 shadow-sm relative overflow-hidden flex flex-col justify-between"
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
                <span className="bg-bayyinah-emerald text-white px-3 py-1.5 rounded-lg font-bold">الدليل</span>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* 6. IMMERSIVE CTA */}
      <section className="relative py-32 bg-bayyinah-deep-emerald text-white overflow-hidden">
        {/* Background Visuals */}
        <div className="absolute inset-0 z-0 opacity-10">
          <div className="absolute right-0 top-1/2 w-full h-px bg-gradient-to-l from-white to-transparent transform -translate-y-1/2"></div>
          <div className="absolute right-1/4 top-0 w-px h-full bg-gradient-to-b from-white to-transparent"></div>
        </div>

        <div className="max-w-4xl mx-auto px-4 text-center relative z-10">
          <motion.h2 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="text-4xl md:text-6xl font-bold mb-6 text-white"
          >
            قبل أن تشارك... <span className="text-bayyinah-gold">تحقّق.</span>
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="text-xl md:text-2xl text-white/70 mb-12 font-light leading-relaxed max-w-2xl mx-auto"
          >
            أرسل المحتوى الذي تريد التحقق منه، ودع بيّنة تقودك من الادعاء إلى المصدر والدليل.
          </motion.p>
          <motion.button 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.4 }}
            onClick={onStartVerification}
            className="bg-white hover:bg-bayyinah-ivory text-bayyinah-deep-emerald px-12 py-5 rounded-2xl font-bold text-xl transition-all shadow-[0_0_40px_rgba(255,255,255,0.15)] hover:shadow-[0_0_60px_rgba(255,255,255,0.25)] flex items-center gap-3 mx-auto"
          >
            ابدأ التحقق
            <ArrowLeft className="w-6 h-6" />
          </motion.button>
        </div>
      </section>

    </div>
  );
};
