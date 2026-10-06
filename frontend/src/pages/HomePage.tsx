import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence, useAnimation, useReducedMotion, useMotionValue, useSpring } from 'framer-motion';
import { NavTab } from '../components/Navbar';
import { ArrowLeft, ArrowRight, ArrowDown, Search, FileText, CheckCircle, Database, Link2, ShieldCheck, AlertCircle, Layout, BookOpen, Layers, Image as ImageIcon, Video as FileVideo } from 'lucide-react';

interface HomePageProps {
  onStartVerification: () => void;
  setActiveTab: (tab: NavTab) => void;
}

// 1. Hero Orbit Component (Rule 37)

const HeroOrbit = () => {
  const [activeIndex, setActiveIndex] = useState(0);
  const [progressRun, setProgressRun] = useState(0);
  const [orbitRadius, setOrbitRadius] = useState(() =>
    typeof window === 'undefined' || window.innerWidth < 768 ? 125 : 170
  );
  const manualPauseUntil = useRef(0);
  const autoCycleScheduler = useRef<(delay: number) => void>(() => {});
  const shouldReduceMotion = useReducedMotion() ?? false;
  const rawTiltX = useMotionValue(0);
  const rawTiltY = useMotionValue(0);
  const tiltX = useSpring(rawTiltX, { stiffness: 120, damping: 22 });
  const tiltY = useSpring(rawTiltY, { stiffness: 120, damping: 22 });

  const steps = [
    { id: 'content', label: 'محتوى', icon: <FileText className="w-5 h-5 md:w-6 md:h-6" />, desc: 'تستقبل بيّنة النص أو الصورة أو الفيديو أو الرابط.' },
    { id: 'claim', label: 'ادعاء', icon: <Layers className="w-5 h-5 md:w-6 md:h-6" />, desc: 'تفكك المحتوى وتحدد الادعاءات التي تحتاج إلى تحقق.' },
    { id: 'search', label: 'بحث', icon: <Search className="w-5 h-5 md:w-6 md:h-6" />, desc: 'تبحث بالمطابقة اللفظية والدلالية في المصادر المعتمدة.' },
    { id: 'source', label: 'مصدر', icon: <Database className="w-5 h-5 md:w-6 md:h-6" />, desc: 'تحصر البحث في المصادر الشرعية الـ 11 المعتمدة فقط.' },
    { id: 'evidence', label: 'دليل', icon: <BookOpen className="w-5 h-5 md:w-6 md:h-6" />, desc: 'تربط كل نتيجة بالمتن المعتمد والسند والتخريج.' },
    { id: 'result', label: 'نتيجة', icon: <ShieldCheck className="w-5 h-5 md:w-6 md:h-6" />, desc: 'تعرض حالة التحقق بوضوح وأمانة علمية دون تخمين.' }
  ];

  useEffect(() => {
    const updateRadius = () => {
      const viewportWidth = window.innerWidth;
      const stageSize = viewportWidth < 768 ? Math.min(320, viewportWidth - 32) : 440;
      setOrbitRadius(stageSize * (viewportWidth < 768 ? 0.39 : 170 / 440));
    };
    updateRadius();
    window.addEventListener('resize', updateRadius);
    return () => window.removeEventListener('resize', updateRadius);
  }, []);

  useEffect(() => {
    if (shouldReduceMotion) {
      autoCycleScheduler.current = () => {};
      return;
    }

    let timeoutId = 0;
    const scheduleNext = (delay: number) => {
      window.clearTimeout(timeoutId);
      timeoutId = window.setTimeout(() => {
        if (document.hidden) {
          scheduleNext(300);
          return;
        }
        const pauseRemaining = manualPauseUntil.current - Date.now();
        if (pauseRemaining > 0) {
          scheduleNext(pauseRemaining);
          return;
        }
      setActiveIndex((current) => (current + 1) % steps.length);
      setProgressRun((run) => run + 1);
        scheduleNext(2300);
      }, delay);
    };

    autoCycleScheduler.current = scheduleNext;
    scheduleNext(2300);
    return () => {
      window.clearTimeout(timeoutId);
      autoCycleScheduler.current = () => {};
    };
  }, [shouldReduceMotion, steps.length]);

  const orbitPoints = steps.map((_, index) => {
    const angle = (index * (360 / steps.length) - 90) * (Math.PI / 180);
    return {
      x: 220 + Math.cos(angle) * 170,
      y: 220 + Math.sin(angle) * 170,
      angle
    };
  });
  const activePoint = orbitPoints[activeIndex];
  const orbitRoute = [...orbitPoints, orbitPoints[0]];

  const selectStep = (index: number) => {
    manualPauseUntil.current = Date.now() + 7000;
    setActiveIndex(index);
    setProgressRun((run) => run + 1);
    autoCycleScheduler.current(7000);
  };

  const handleStagePointerMove = (event: React.PointerEvent<HTMLDivElement>) => {
    if (shouldReduceMotion || event.pointerType !== 'mouse') return;
    if (event.target instanceof Element && event.target.closest('[role="tab"]')) return;
    const bounds = event.currentTarget.getBoundingClientRect();
    const x = (event.clientX - bounds.left) / bounds.width - 0.5;
    const y = (event.clientY - bounds.top) / bounds.height - 0.5;
    rawTiltX.set(-y * 2);
    rawTiltY.set(x * 2);
  };

  const resetStageTilt = () => {
    rawTiltX.set(0);
    rawTiltY.set(0);
  };

  return (
    <div className="flex flex-col items-center w-full">
      <motion.div
        className="relative aspect-square w-full max-w-[320px] md:max-w-[440px]"
        style={{ rotateX: tiltX, rotateY: tiltY, transformStyle: 'preserve-3d' }}
        onPointerMove={handleStagePointerMove}
        onPointerLeave={resetStageTilt}
      >
        <svg className="pointer-events-none absolute inset-0 h-full w-full overflow-visible" viewBox="0 0 440 440" aria-hidden="true">
          <circle cx="220" cy="220" r="204" fill="none" stroke="rgba(70,255,185,0.12)" strokeWidth="1" />
          <motion.g
            animate={shouldReduceMotion ? { rotate: 0 } : { rotate: 360 }}
            transition={{ duration: 45, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'linear' }}
            style={{ transformOrigin: '220px 220px' }}
          >
            <circle cx="220" cy="220" r="204" fill="none" stroke="rgba(70,255,185,0.22)" strokeWidth="1" strokeDasharray="178 1104" />
            <circle cx="220" cy="220" r="198" fill="none" stroke="rgba(94,242,177,0.18)" strokeWidth="1.5" strokeDasharray="82 1162" strokeDashoffset="190" />
            <circle cx="220" cy="16" r="2.5" fill="#5ef2b1" />
          </motion.g>

          <motion.g
            animate={shouldReduceMotion ? { rotate: 0 } : { rotate: -360 }}
            transition={{ duration: 60, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'linear' }}
            style={{ transformOrigin: '220px 220px' }}
          >
            <circle cx="220" cy="220" r="87" fill="none" stroke="rgba(255,255,255,0.11)" strokeWidth="1" strokeDasharray="3 7" />
            <path d="M 158 159 A 87 87 0 0 1 192 137" fill="none" stroke="rgba(94,242,177,0.3)" strokeWidth="2" strokeLinecap="round" />
          </motion.g>

          <circle cx="220" cy="220" r="170" fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="1.5" />
          <circle cx="220" cy="220" r="170" fill="none" stroke="rgba(94,242,177,0.18)" strokeWidth="3" strokeDasharray="2 16" strokeLinecap="round" />

          {orbitPoints.map((point, index) => (
            <line
              key={`spoke-${steps[index].id}`}
              x1="220"
              y1="220"
              x2={point.x}
              y2={point.y}
              stroke={activeIndex === index ? 'rgba(94,242,177,0.7)' : 'rgba(255,255,255,0.15)'}
              strokeWidth={activeIndex === index ? '1.6' : '1'}
              strokeDasharray={activeIndex === index ? '4 5' : undefined}
            />
          ))}

          <motion.g
            animate={shouldReduceMotion ? { rotate: 0 } : { rotate: 360 }}
            transition={{ duration: 60, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'linear' }}
            style={{ transformOrigin: '220px 220px' }}
          >
            {orbitPoints.map((point, index) => {
              const midpointAngle = point.angle + Math.PI / 6;
              const midpointX = 220 + Math.cos(midpointAngle) * 170;
              const midpointY = 220 + Math.sin(midpointAngle) * 170;
              const tangent = ((midpointAngle + Math.PI / 2) * 180) / Math.PI;
              return (
                <g key={`arrow-${steps[index].id}`} transform={`translate(${midpointX} ${midpointY}) rotate(${tangent})`}>
                  <path d="M -4 -5 L 2 0 L -4 5" fill="none" stroke="rgba(190,255,225,0.9)" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
                </g>
              );
            })}
          </motion.g>

          {!shouldReduceMotion && (
            <motion.circle
              r="4.5"
              fill="#ffffff"
              style={{ filter: 'drop-shadow(0 0 5px rgba(80,255,185,0.9)) drop-shadow(0 0 13px rgba(80,255,185,0.55))' }}
              initial={{ cx: orbitRoute[0].x, cy: orbitRoute[0].y }}
              animate={{ cx: orbitRoute.map((point) => point.x), cy: orbitRoute.map((point) => point.y) }}
              transition={{ duration: steps.length * 2.3, repeat: Infinity, ease: 'linear' }}
            />
          )}

          <motion.circle
            key={`center-pulse-${activeIndex}`}
            cx="220"
            cy="220"
            fill="none"
            stroke="rgba(94,242,177,0.75)"
            strokeWidth="2"
            initial={{ r: 62, opacity: shouldReduceMotion ? 0 : 0.45 }}
            animate={shouldReduceMotion ? { r: 62, opacity: 0 } : { r: [62, 82], opacity: [0.42, 0] }}
            transition={{ duration: 0.85, repeat: shouldReduceMotion ? 0 : 1, ease: 'easeOut' }}
          />

          {!shouldReduceMotion && (
            <motion.circle
              key={`data-to-center-${activeIndex}`}
              r="3.5"
              fill="#ffffff"
              style={{ filter: 'drop-shadow(0 0 6px rgba(94,242,177,0.95))' }}
              initial={{ cx: activePoint.x, cy: activePoint.y, opacity: 0 }}
              animate={{ cx: [activePoint.x, 220], cy: [activePoint.y, 220], opacity: [0, 1, 0] }}
              transition={{ duration: 0.7, ease: 'easeInOut' }}
            />
          )}

          {activeIndex === steps.length - 1 && !shouldReduceMotion && (
            <motion.circle
              key={`completion-${progressRun}`}
              cx="220"
              cy="220"
              fill="none"
              stroke="#8dffd0"
              strokeWidth="3"
              initial={{ r: 80, opacity: 0.75 }}
              animate={{ r: [80, 205], opacity: [0.65, 0] }}
              transition={{ duration: 0.8, ease: 'easeOut' }}
            />
          )}
        </svg>

        <motion.div
          animate={shouldReduceMotion ? { boxShadow: '0 0 24px rgba(94,242,177,0.14)' } : {
            boxShadow: ['0 0 22px rgba(94,242,177,0.12)', '0 0 34px rgba(94,242,177,0.24)', '0 0 22px rgba(94,242,177,0.12)']
          }}
          transition={{ duration: 3.5, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'easeInOut' }}
          className="absolute left-1/2 top-1/2 z-10 flex h-24 w-24 -translate-x-1/2 -translate-y-1/2 flex-col items-center justify-center rounded-full border border-[#b8f5d9]/80 bg-white/[0.94] p-2 text-center backdrop-blur-xl md:h-32 md:w-32"
        >
          <span className="text-base font-bold tracking-wide text-[#0a2d2b] md:text-lg">بيّنة AI</span>
          <span className="mt-0.5 text-[10px] text-[#1b5f59] md:text-xs">محرك التحقق</span>
        </motion.div>

        <div className="absolute inset-0 z-20" role="tablist" aria-label="مراحل محرك التحقق">
          {steps.map((step, index) => {
            const angle = (index * (360 / steps.length) - 90) * (Math.PI / 180);
            const x = Math.cos(angle) * orbitRadius;
            const y = Math.sin(angle) * orbitRadius;
            const isActive = activeIndex === index;

          return (
              <motion.button
                key={step.id}
                type="button"
                role="tab"
                aria-label={`${String(index + 1).padStart(2, '0')} ${step.label}`}
                aria-selected={isActive}
                aria-controls="hero-step-detail"
                tabIndex={isActive ? 0 : -1}
                onClick={() => selectStep(index)}
                onKeyDown={(event) => {
                  const direction = event.key === 'ArrowLeft' || event.key === 'ArrowDown'
                    ? 1
                    : event.key === 'ArrowRight' || event.key === 'ArrowUp'
                      ? -1
                      : 0;
                  if (!direction) return;
                  event.preventDefault();
                  const nextIndex = (index + direction + steps.length) % steps.length;
                  selectStep(nextIndex);
                  document.getElementById(`hero-step-${nextIndex}`)?.focus();
                }}
                id={`hero-step-${index}`}
                initial={false}
                whileTap={shouldReduceMotion ? undefined : { scale: 0.97 }}
                onPointerMove={(event) => {
                  if (shouldReduceMotion || event.pointerType !== 'mouse') return;
                  const bounds = event.currentTarget.getBoundingClientRect();
                  const offsetX = ((event.clientX - bounds.left) / bounds.width - 0.5) * 6;
                  const offsetY = ((event.clientY - bounds.top) / bounds.height - 0.5) * 6;
                  const magneticNode = event.currentTarget.querySelector('[data-magnetic-node]');
                  if (magneticNode instanceof HTMLElement) magneticNode.style.translate = `${offsetX}px ${offsetY}px`;
                }}
                onPointerLeave={(event) => {
                  const magneticNode = event.currentTarget.querySelector('[data-magnetic-node]');
                  if (magneticNode instanceof HTMLElement) magneticNode.style.translate = '0px 0px';
                }}
                className="group absolute flex -translate-x-1/2 -translate-y-1/2 flex-col items-center bg-transparent p-0 text-center focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#86ffd0]/80"
                style={{ left: `calc(50% + ${x}px)`, top: `calc(50% + ${y}px)` }}
              >
                <motion.span data-magnetic-node whileHover={shouldReduceMotion ? undefined : { scale: 1.06, y: -3 }} className={`relative flex h-11 w-11 items-center justify-center rounded-full border transition-[translate,background-color,border-color,box-shadow] duration-200 ease-out motion-reduce:transition-none md:h-14 md:w-14 ${isActive
                  ? 'border-[#6effbd] bg-gradient-to-br from-[#18d9a0] to-[#00ae7b] text-white shadow-[0_0_0_1px_rgba(100,255,195,0.65),0_0_21px_rgba(40,255,170,0.35),0_0_38px_rgba(40,255,170,0.15)]'
                  : 'border-[#d7f5e6]/55 bg-white text-[#0b493f] shadow-[0_5px_18px_rgba(0,35,26,0.16)] group-hover:border-[#7dffd0] group-hover:shadow-[0_0_18px_rgba(94,242,177,0.32)]'
                }`}>
                  {!shouldReduceMotion && isActive && (
                    <motion.span
                      aria-hidden="true"
                      className="absolute inset-0 rounded-full border border-[#aaffd4]"
                      animate={{ scale: [1, 1.38], opacity: [0.45, 0] }}
                      transition={{ duration: 1.35, repeat: Infinity, ease: 'easeOut' }}
                    />
                  )}
                  <span className="relative z-10">
                    {step.icon}
                  </span>
                  <span className={`absolute -right-1.5 -top-2 flex h-5 min-w-5 items-center justify-center rounded-full border px-1 font-mono text-[9px] font-bold transition-colors md:-right-2 md:h-[22px] md:min-w-[22px] md:text-[10px] ${isActive ? 'border-[#aaffd4] bg-[#80ffd0] text-[#064b37]' : 'border-[#ccefe0] bg-[#e8faf1] text-[#0b493f]'}`}>
                    {String(index + 1).padStart(2, '0')}
                  </span>
                </motion.span>
                <span className={`mt-1.5 whitespace-nowrap font-bold transition-all duration-300 motion-reduce:transition-none ${isActive ? 'text-white text-sm drop-shadow-md md:text-base' : 'text-white/75 text-[10px] group-hover:text-white md:text-xs'}`}>
                  {step.label}
                </span>
              </motion.button>
            );
          })}
        </div>
      </motion.div>

      <div id="hero-step-detail" role="tabpanel" aria-labelledby={`hero-step-${activeIndex}`} className="mt-7 w-full max-w-md overflow-hidden rounded-3xl border border-[#50ffb9]/55 bg-gradient-to-br from-[rgba(0,75,55,0.88)] to-[rgba(0,45,38,0.88)] p-5 text-white shadow-[0_12px_32px_rgba(0,20,15,0.2)] backdrop-blur-[18px] md:mt-8">
        <div className="relative h-2 rounded-full bg-white/[0.16]" aria-label={`تقدم المرحلة ${String(activeIndex + 1).padStart(2, '0')}`}>
          <motion.div
            key={progressRun}
            data-testid="hero-step-progress-fill"
            initial={{ width: '0%' }}
            animate={{ width: '100%' }}
            transition={{ duration: shouldReduceMotion ? 0.25 : 2.3, ease: 'linear' }}
            className="absolute right-0 top-0 h-full rounded-full bg-gradient-to-l from-[#35f0a5] to-[#7bffd0] shadow-[0_0_12px_rgba(94,242,177,0.65)]"
          >
            <span className="absolute -left-1.5 top-1/2 h-3 w-3 -translate-y-1/2 rounded-full border border-white bg-[#aaffd4] shadow-[0_0_10px_rgba(94,242,177,0.9)]" />
          </motion.div>
        </div>
        <AnimatePresence mode="wait" initial={false}>
          <motion.div
            key={activeIndex}
            initial={shouldReduceMotion ? false : { opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={shouldReduceMotion ? undefined : { opacity: 0, y: -6 }}
            transition={{ duration: shouldReduceMotion ? 0.15 : 0.32, ease: 'easeOut' }}
            aria-live="polite"
            className="mt-4 flex min-h-[108px] flex-col justify-center"
          >
            <div className="mb-3 flex items-center justify-between gap-4">
              <div className="flex min-w-0 items-center gap-3">
                <motion.span
                  animate={shouldReduceMotion ? { scale: 1 } : { scale: [1, 1.04, 1] }}
                  transition={{ duration: 2.2, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'easeInOut' }}
                  className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-[#78ffc3]/35 bg-white/[0.08] text-[#aaffd4]"
                >
                  {steps[activeIndex].icon}
                </motion.span>
                <div className="min-w-0">
                  <p className="text-sm font-bold text-white md:text-base">{steps[activeIndex].label}</p>
                  <p dir="ltr" className="text-right font-mono text-[10px] text-white/55">{String(activeIndex + 1).padStart(2, '0')} / 06</p>
                </div>
              </div>
              <span className="shrink-0 text-[10px] font-semibold text-[#aaffd4]/80">جاري التحقق</span>
            </div>
            <p className="min-h-[48px] text-center text-sm leading-relaxed text-white/85 md:text-base">
              {steps[activeIndex].desc}
            </p>
          </motion.div>
        </AnimatePresence>
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
  const [activeIndex, setActiveIndex] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
  const sectionRef = useRef<HTMLDivElement | null>(null);
  const pauseUntil = useRef(0);
  const shouldReduceMotion = useReducedMotion() ?? false;
  const steps = [
    { title: 'الفهم الذكي قبل التحقق', desc: 'لا تتعامل بيّنة مع المحتوى ككتلة نصية فقط، بل تفهم السياق وتحدد الادعاءات التي تحتاج إلى تحقق.', icon: <Layout className="h-8 w-8" /> },
    { title: 'المصادر أولًا', desc: 'تبحث بيّنة في المصادر المعتمدة والمرتبطة بنوع المحتوى والادعاء، بعيدًا عن التخمين.', icon: <Database className="h-8 w-8" /> },
    { title: 'الدليل ظاهر', desc: 'لا تكتفي بيّنة بالنتيجة، بل تعرض الدليل والمصدر والمرجع والرابط ليتمكن المستخدم من مراجعتها.', icon: <BookOpen className="h-8 w-8" /> },
    { title: 'معالجة متعددة الوسائط', desc: 'يمكن التحقق من: النص، الصورة، الفيديو، الرابط.', icon: <Link2 className="h-8 w-8" /> },
    { title: 'الأمانة العلمية', desc: 'إذا لم تجد بيّنة دليلًا كافيًا، لا تنشئ يقينًا من الفراغ، بل توضّح حدود ما تم التوصل إليه.', icon: <ShieldCheck className="h-8 w-8" /> }
  ];

  useEffect(() => {
    const section = sectionRef.current;
    if (!section) return;
    const observer = new IntersectionObserver(([entry]) => setIsVisible(entry.isIntersecting), { threshold: 0.2 });
    observer.observe(section);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!isVisible || shouldReduceMotion) return;
    const interval = window.setInterval(() => {
      if (document.hidden || Date.now() < pauseUntil.current) return;
      setActiveIndex((current) => (current + 1) % steps.length);
    }, 2600);
    return () => window.clearInterval(interval);
  }, [isVisible, shouldReduceMotion, steps.length]);

  const selectStep = (index: number) => {
    pauseUntil.current = Date.now() + 6000;
    setActiveIndex(index);
  };

  return (
    <div ref={sectionRef} className="relative">
      <div className="relative grid grid-cols-1 gap-3 md:gap-4 lg:grid-cols-[minmax(0,1fr)_48px_minmax(0,1fr)_48px_minmax(0,1fr)_48px_minmax(0,1fr)_48px_minmax(0,1fr)] lg:gap-2" role="list" aria-label="أسباب تميّز بيّنة">
        {steps.map((step, index) => {
          const isActive = activeIndex === index;
          return (
            <React.Fragment key={step.title}>
              <motion.button
                type="button"
                aria-pressed={isActive}
                onClick={() => selectStep(index)}
                onKeyDown={(event) => {
                  const direction = event.key === 'ArrowLeft' ? 1 : event.key === 'ArrowRight' ? -1 : 0;
                  if (!direction) return;
                  event.preventDefault();
                  const nextIndex = (index + direction + steps.length) % steps.length;
                  selectStep(nextIndex);
                  document.getElementById(`why-bayyinah-${nextIndex}`)?.focus();
                }}
                id={`why-bayyinah-${index}`}
                initial={shouldReduceMotion ? false : { opacity: 0, y: 12 }}
                whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.2 }}
                transition={{ duration: shouldReduceMotion ? 0 : 0.4, delay: shouldReduceMotion ? 0 : index * 0.09 }}
                whileHover={shouldReduceMotion ? undefined : { y: -4 }}
                whileTap={shouldReduceMotion ? undefined : { scale: 0.99 }}
                className={`relative z-10 flex min-h-[270px] w-full flex-col items-start overflow-hidden rounded-[25px] border p-6 text-right text-white shadow-[0_14px_35px_rgba(0,100,70,0.12)] transition-[border-color,box-shadow,opacity] duration-300 motion-reduce:transition-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-700/50 lg:min-h-[300px] ${isActive ? 'border-[#89ffd0]/75 opacity-100 shadow-[0_16px_40px_rgba(0,130,90,.18),0_0_28px_rgba(70,240,165,.16)]' : 'border-[#5affbe]/35 opacity-90 hover:opacity-100'}`}
                style={{ background: 'linear-gradient(145deg, #079669 0%, #007a59 48%, #006348 100%)' }}
              >
                <span className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-l from-transparent via-white/30 to-transparent" />
                <span className="flex w-full items-center justify-between">
                  <span className={`flex h-8 w-8 items-center justify-center rounded-full border font-mono text-xs font-bold transition-colors ${isActive ? 'border-white/70 bg-[#baffdf] text-[#00563d] shadow-[0_0_15px_rgba(154,255,210,.35)]' : 'border-white/40 bg-white/80 text-[#006348]'}`}>0{index + 1}</span>
                  <motion.span animate={isActive && !shouldReduceMotion ? { y: [0, -2, 0] } : { y: 0 }} transition={{ duration: 1.2, repeat: isActive && !shouldReduceMotion ? Infinity : 0, ease: 'easeInOut' }} className={`relative flex h-[74px] w-[74px] items-center justify-center rounded-full border text-white backdrop-blur-md transition-all duration-300 ${isActive ? 'border-[#aaffd7]/70 bg-white/20 shadow-[0_0_0_7px_rgba(80,255,185,.07),0_0_0_14px_rgba(80,255,185,.035),0_0_25px_rgba(70,240,165,.24)]' : 'border-[#aaffd7]/30 bg-[#005e45]/35'}`}>
                    {isActive && !shouldReduceMotion && <motion.span aria-hidden="true" className="absolute inset-0 rounded-full border border-[#bdffe2]" animate={{ scale: [1, 1.35], opacity: [0.35, 0] }} transition={{ duration: 2.1, repeat: Infinity, ease: 'easeOut' }} />}
                    {step.icon}
                  </motion.span>
                </span>
                <span className="mt-5 block min-h-[52px] text-base font-bold leading-relaxed sm:text-lg">{step.title}</span>
                {isActive && <span className="mt-3 h-1 w-full overflow-hidden rounded-full bg-white/15"><motion.span key={`why-progress-${index}`} className="block h-full rounded-full bg-gradient-to-l from-[#9affd2] to-[#40e99c]" initial={{ width: '0%' }} animate={{ width: '100%' }} transition={{ duration: shouldReduceMotion ? 0 : 2.6, ease: 'linear' }} /></span>}
                <p className="mt-3 text-sm leading-[1.8] text-white/85">{step.desc}</p>
              </motion.button>
              {index < steps.length - 1 && (
                <div className="relative flex h-8 items-center justify-center lg:h-full" aria-hidden="true">
                  <span className="absolute inset-y-0 w-px bg-emerald-800/15 lg:inset-y-1/2 lg:h-px lg:w-full lg:-translate-y-1/2" />
                  {activeIndex === index && !shouldReduceMotion && <motion.span className="absolute top-0 h-full w-px origin-top bg-gradient-to-b from-[#8affca] to-[#20b779] lg:inset-y-1/2 lg:h-px lg:w-full lg:origin-right lg:-translate-y-1/2 lg:bg-gradient-to-l" initial={{ scaleY: 0, scaleX: 0 }} animate={{ scaleY: 1, scaleX: 1 }} transition={{ duration: 2.3, ease: 'linear' }} />}
                  {activeIndex === index && !shouldReduceMotion && <motion.span className="absolute top-0 h-2 w-2 rounded-full bg-white shadow-[0_0_7px_rgba(255,255,255,.9),0_0_16px_rgba(70,255,180,.75)] lg:hidden" animate={{ y: [0, 24] }} transition={{ duration: 2.3, ease: 'linear' }} />}
                  {activeIndex === index && !shouldReduceMotion && <motion.span className="absolute right-0 top-1/2 hidden h-2 w-2 -translate-y-1/2 rounded-full bg-white shadow-[0_0_7px_rgba(255,255,255,.9),0_0_16px_rgba(70,255,180,.75)] lg:block" animate={{ x: [0, -38] }} transition={{ duration: 2.3, ease: 'linear' }} />}
                  <span className="relative z-10 flex h-7 w-7 items-center justify-center rounded-full border border-emerald-600/25 bg-white text-emerald-800 shadow-[0_0_16px_rgba(40,220,145,.12)]">
                    <ArrowDown className="h-4 w-4 lg:hidden" />
                    <ArrowLeft className="hidden h-4 w-4 lg:block" />
                  </span>
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

// 4. How It Works Timeline
const HowItWorks = () => {
  const [activeIndex, setActiveIndex] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
  const sectionRef = useRef<HTMLDivElement | null>(null);
  const pauseUntil = useRef(0);
  const hasStarted = useRef(false);
  const shouldReduceMotion = useReducedMotion() ?? false;
  const steps = [
    { num: '01', title: 'يفهم المحتوى', short: 'الفهم', desc: 'تستقبل بيّنة النص أو الصورة أو الفيديو وتقوم بتحليل البنية الأساسية للمحتوى باستخدام الذكاء الاصطناعي.', icon: <FileText className="h-5 w-5" /> },
    { num: '02', title: 'يستخرج الادعاء', short: 'الاستخراج', desc: 'تستخرج الادعاءات الرئيسية وتتجاهل الحشو، ليتم التركيز على ما يتطلب التحقق المرجعي.', icon: <Layers className="h-5 w-5" /> },
    { num: '03', title: 'يبحث في المصادر', short: 'البحث', desc: '', icon: <Search className="h-5 w-5" /> },
    { num: '04', title: 'يجمع الأدلة', short: 'الجمع', desc: 'جمع الأدلة المتوافقة والمتعارضة من المصادر المعتمدة لبناء قاعدة حكم متوازنة.', icon: <Database className="h-5 w-5" /> },
    { num: '05', title: 'يتحقق من المصدر', short: 'التحقق', desc: 'مقارنة الادعاء مع الدليل المستخرج والتأكد من عدم وجود اختلافات في سياق النقل.', icon: <ShieldCheck className="h-5 w-5" /> },
    { num: '06', title: 'تحدد حالة النتيجة', short: 'النتيجة', desc: '', icon: <CheckCircle className="h-5 w-5" /> },
    { num: '07', title: 'تعرض الدليل', short: 'الدليل', desc: '', icon: <BookOpen className="h-5 w-5" /> }
  ];
  const visualSymbols = [[FileText, ImageIcon, FileVideo, Link2], [FileText, Layers, Search], [Search, Database, Database], [FileText, BookOpen, Database], [ShieldCheck, Database, CheckCircle], [FileText, CheckCircle, AlertCircle], [BookOpen, Link2, Database]];
  const progressValues = [14, 28, 42, 57, 71, 85, 100];

  useEffect(() => {
    const section = sectionRef.current;
    if (!section) return;
    const observer = new IntersectionObserver(([entry]) => setIsVisible(entry.isIntersecting), { threshold: 0.18 });
    observer.observe(section);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!isVisible || shouldReduceMotion) return;
    const firstDelay = hasStarted.current ? 2900 : 1200;
    const pauseRemaining = Math.max(0, pauseUntil.current - Date.now());
    let timeout = 0;
    const advance = () => {
      if (document.hidden) {
        timeout = window.setTimeout(advance, 1000);
        return;
      }
      hasStarted.current = true;
      setActiveIndex((current) => (current + 1) % steps.length);
    };
    timeout = window.setTimeout(advance, Math.max(firstDelay, pauseRemaining, activeIndex === steps.length - 1 ? 3900 : 0));
    return () => window.clearTimeout(timeout);
  }, [activeIndex, isVisible, shouldReduceMotion, steps.length]);

  const selectStep = (index: number) => {
    pauseUntil.current = Date.now() + 7000;
    hasStarted.current = true;
    setActiveIndex(index);
  };

  return (
    <div ref={sectionRef} className="mt-12 w-full md:mt-14">
      <div className="relative mx-auto mb-10 max-w-6xl md:mb-12">
        <svg className="pointer-events-none absolute inset-x-0 top-[27px] hidden h-6 w-full overflow-visible lg:block" viewBox="0 0 1000 48" preserveAspectRatio="none" aria-hidden="true">
          <path d="M928 24 H72" stroke="rgba(180,255,220,.28)" strokeWidth="1.5" />
          <motion.path d="M928 24 H72" stroke="rgba(111,255,194,.65)" strokeWidth="2" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: progressValues[activeIndex] / 100 }} transition={{ duration: shouldReduceMotion ? 0 : 0.65, ease: 'easeInOut' }} />
          {!shouldReduceMotion && activeIndex < steps.length - 1 && <motion.circle key={`timeline-dot-${activeIndex}`} r="5" fill="#e5fff3" style={{ filter: 'drop-shadow(0 0 5px rgba(255,255,255,.8)) drop-shadow(0 0 12px rgba(70,255,180,.75))' }} initial={{ cx: 928 - activeIndex * (856 / 7), cy: 24 }} animate={{ cx: 928 - (activeIndex + 1) * (856 / 7), cy: 24 }} transition={{ duration: 2.9, ease: 'linear' }} />}
        </svg>
        <svg className="pointer-events-none absolute bottom-0 left-1/2 h-full w-10 -translate-x-1/2 lg:hidden" viewBox="0 0 40 700" preserveAspectRatio="none" aria-hidden="true">
          <path d="M20 30 V670" stroke="rgba(180,255,220,.28)" strokeWidth="1.5" />
          <motion.path d="M20 30 V670" stroke="rgba(111,255,194,.65)" strokeWidth="2" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: progressValues[activeIndex] / 100 }} transition={{ duration: shouldReduceMotion ? 0 : 0.65, ease: 'easeInOut' }} />
          {!shouldReduceMotion && activeIndex < steps.length - 1 && <motion.circle key={`mobile-timeline-dot-${activeIndex}`} cx="20" r="5" fill="#e5fff3" style={{ filter: 'drop-shadow(0 0 5px rgba(255,255,255,.8)) drop-shadow(0 0 12px rgba(70,255,180,.75))' }} initial={{ cy: 30 + activeIndex * (640 / 7) }} animate={{ cy: 30 + (activeIndex + 1) * (640 / 7) }} transition={{ duration: 2.9, ease: 'linear' }} />}
        </svg>
        <div className="relative grid grid-cols-1 gap-1 lg:grid-cols-7" role="list" aria-label="مراحل عمل بيّنة">
          {steps.map((step, index) => {
            const isActive = activeIndex === index;
            const isPast = activeIndex > index;
            return (
              <motion.button
                key={step.num}
                id={`how-step-${index}`}
                type="button"
                aria-current={isActive ? 'step' : undefined}
                aria-pressed={isActive}
                onClick={() => selectStep(index)}
                onKeyDown={(event) => {
                  const direction = event.key === 'ArrowLeft' || event.key === 'ArrowDown' ? 1 : event.key === 'ArrowRight' || event.key === 'ArrowUp' ? -1 : 0;
                  if (!direction) return;
                  event.preventDefault();
                  const nextIndex = (index + direction + steps.length) % steps.length;
                  selectStep(nextIndex);
                  document.getElementById(`how-step-${nextIndex}`)?.focus();
                }}
                initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }}
                whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.2 }}
                transition={{ duration: shouldReduceMotion ? 0 : 0.35, delay: shouldReduceMotion ? 0 : 0.2 + index * 0.07 }}
                whileHover={shouldReduceMotion ? undefined : { y: -3 }}
                className={`group relative z-10 flex min-h-[96px] flex-row items-center gap-3 rounded-xl px-3 py-2 text-right text-white transition-[opacity] duration-300 motion-reduce:transition-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#aaffd4]/70 lg:min-h-[116px] lg:flex-col lg:justify-start lg:gap-2 lg:px-1 lg:pt-2 ${isActive ? 'opacity-100' : 'opacity-65 hover:opacity-100'}`}
              >
                <motion.span animate={isActive || (activeIndex === steps.length - 1 && !shouldReduceMotion) ? { scale: [1, 1.08, 1] } : { scale: 1 }} transition={{ duration: activeIndex === steps.length - 1 ? 0.55 : 2.1, delay: activeIndex === steps.length - 1 ? index * 0.1 : 0, repeat: isActive && activeIndex !== steps.length - 1 && !shouldReduceMotion ? Infinity : 0, ease: 'easeInOut' }} className={`relative flex h-12 w-12 shrink-0 items-center justify-center rounded-full border transition-all duration-300 lg:h-14 lg:w-14 ${isActive ? 'scale-[1.08] border-[#b7ffdf] bg-gradient-to-br from-[#20c987] to-[#087c59] text-white shadow-[0_0_0_8px_rgba(80,255,185,.08),0_0_0_16px_rgba(80,255,185,.04),0_0_26px_rgba(70,240,165,.3)]' : isPast ? 'border-[#8fffc9]/55 bg-[#086348]/60 text-[#b6ffde]' : 'border-[#82ffc1]/35 bg-[#004b39]/30 text-[#b6ffde] group-hover:border-[#b7ffdf]/70'}`}>
                  {isActive && !shouldReduceMotion && <motion.span aria-hidden="true" className="absolute inset-0 rounded-full border border-[#b7ffdf]" animate={{ scale: [1, 1.35], opacity: [0.35, 0] }} transition={{ duration: 2.1, repeat: Infinity, ease: 'easeOut' }} />}
                  {step.icon}
                </motion.span>
                <span className="min-w-0 text-right lg:text-center"><span className={`block font-mono text-xs ${isActive ? 'text-[#c4ffe4]' : 'text-white/55'}`}>{step.num}</span><span className={`mt-1 block text-sm font-semibold leading-tight lg:text-xs xl:text-sm ${isActive ? 'text-white' : 'text-white/80'}`}>{step.short}</span></span>
              </motion.button>
            );
          })}
        </div>
      </div>

      <div className="relative min-h-[330px] overflow-hidden rounded-[24px] border border-[#b4ffdc]/25 bg-gradient-to-br from-white/[0.11] to-white/[0.045] p-5 shadow-[0_20px_60px_rgba(0,50,35,.16)] backdrop-blur-[18px] sm:p-8 lg:min-h-[310px] lg:p-10">
        <div className="grid min-h-[270px] grid-cols-1 items-center gap-7 md:grid-cols-[minmax(0,1.1fr)_minmax(250px,.9fr)] md:gap-10">
          <AnimatePresence mode="wait" initial={false}>
            <motion.div key={`details-${activeIndex}`} initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={shouldReduceMotion ? undefined : { opacity: 0, y: -6 }} transition={{ duration: shouldReduceMotion ? 0 : 0.42, ease: 'easeOut' }} aria-live="polite" className="order-1 flex min-h-[220px] flex-col justify-center md:order-2">
              <span className="w-fit rounded-full border border-[#aaffd4]/35 bg-white/[0.09] px-3 py-1 font-mono text-sm font-bold text-[#baffdf]">{steps[activeIndex].num}</span>
              <h3 className="mt-4 text-xl font-bold text-white sm:text-2xl">{steps[activeIndex].title}</h3>
              {activeIndex === 2 ? (
                <div className="mt-4 flex flex-wrap gap-2"><span className="rounded-lg border border-[#aaffd4]/25 bg-white/[0.08] px-3 py-2 text-sm text-white/85">بحث دلالي (Semantic)</span><span className="rounded-lg border border-[#aaffd4]/25 bg-white/[0.08] px-3 py-2 text-sm text-white/85">بحث نصي (Full Text)</span></div>
              ) : activeIndex === 5 ? (
                <div className="mt-4 flex flex-wrap gap-2"><span className="rounded-lg border border-[#aaffd4]/30 bg-[#35dc98]/15 px-3 py-2 text-sm text-white">ثابت بحسب المصدر</span><span className="rounded-lg border border-white/15 bg-white/[0.08] px-3 py-2 text-sm text-white/85">لم يثبت بهذا اللفظ</span><span className="rounded-lg border border-white/15 bg-white/[0.08] px-3 py-2 text-sm text-white/85">لم نجد دليلًا كافيًا</span></div>
              ) : activeIndex === 6 ? (
                <div className="mt-4 flex flex-wrap items-center gap-2 text-sm font-semibold text-[#c4ffe4]"><span>المصدر</span><ArrowLeft className="h-4 w-4" /><span>المرجع</span><ArrowLeft className="h-4 w-4" /><span>الدليل</span><ArrowLeft className="h-4 w-4" /><span>النتيجة</span></div>
              ) : <p className="mt-3 max-w-2xl text-sm leading-[1.9] text-white/80 sm:text-base">{steps[activeIndex].desc}</p>}
              <div className="mt-7"><div className="mb-2 flex items-center justify-between text-xs text-white/70"><span>تقدم المراحل</span><span dir="ltr" className="font-mono text-[#baffdf]">{progressValues[activeIndex]}%</span></div><div className="h-2 overflow-hidden rounded-full bg-white/[0.14]"><motion.div className="h-full rounded-full bg-gradient-to-l from-[#40e99c] to-[#9affd2] shadow-[0_0_14px_rgba(84,243,176,.32)]" animate={{ width: `${progressValues[activeIndex]}%` }} transition={{ duration: shouldReduceMotion ? 0 : 0.65, ease: 'easeInOut' }} /></div></div>
            </motion.div>
          </AnimatePresence>

          <AnimatePresence mode="wait" initial={false}>
            <motion.div key={`visual-${activeIndex}`} initial={shouldReduceMotion ? false : { opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} exit={shouldReduceMotion ? undefined : { opacity: 0, scale: 0.97 }} transition={{ duration: shouldReduceMotion ? 0 : 0.45, ease: 'easeOut' }} aria-hidden="true" className="relative order-2 mx-auto flex h-[190px] w-full max-w-[320px] items-center justify-center md:order-1 md:h-[220px]">
              <div className="absolute h-36 w-36 rounded-full border border-[#aaffd4]/15 md:h-44 md:w-44" /><div className="absolute h-28 w-28 rounded-full border border-dashed border-[#aaffd4]/25 md:h-36 md:w-36" />
              {!shouldReduceMotion && <motion.span className="absolute h-2 w-2 rounded-full bg-[#caffea] shadow-[0_0_12px_rgba(154,255,210,.85)]" animate={{ offsetDistance: ['0%', '100%'] }} transition={{ duration: 14 + activeIndex, repeat: Infinity, ease: 'linear' }} style={{ offsetPath: 'ellipse(74px 74px at 50% 50%)' }} />}
              <div className="relative z-10 flex h-[76px] w-[76px] items-center justify-center rounded-[22px] border border-[#aaffd4]/35 bg-white/[0.13] text-[#c5ffe5] shadow-[0_12px_36px_rgba(0,32,23,.2)] backdrop-blur-lg">{steps[activeIndex].icon}</div>
              {visualSymbols[activeIndex].map((Symbol, index) => {
                const positions = ['right-3 top-6', 'bottom-5 right-10', 'bottom-5 left-10', 'left-3 top-6'];
                return <motion.span key={`${activeIndex}-${index}`} animate={shouldReduceMotion ? { y: 0 } : { y: [0, index % 2 === 0 ? -4 : 4, 0] }} transition={{ duration: 3 + index * 0.4, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'easeInOut' }} className={`absolute ${positions[index]} flex h-10 w-10 items-center justify-center rounded-xl border border-[#aaffd4]/25 bg-[#00543d]/75 text-[#baffdf] shadow-lg backdrop-blur-md`}><Symbol className="h-5 w-5" /></motion.span>;
              })}
            </motion.div>
          </AnimatePresence>
        </div>
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
        style={{ background: 'radial-gradient(circle at 10% 20%, rgba(55,255,170,0.2), transparent 30%), radial-gradient(circle at 90% 75%, rgba(35,210,140,0.14), transparent 35%), linear-gradient(135deg, #056444 0%, #005339 45%, #003e2c 100%)' }}
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
      <section className="relative isolate overflow-hidden border-t border-emerald-900/[0.06] py-20 md:py-24" style={{ background: 'radial-gradient(circle at 10% 20%, rgba(40,220,145,.08), transparent 30%), radial-gradient(circle at 90% 80%, rgba(40,220,145,.07), transparent 30%), linear-gradient(180deg, #ffffff 0%, #fbfefc 48%, #f3fbf6 100%)' }}>
        <div aria-hidden="true" className="pointer-events-none absolute inset-0 overflow-hidden">
          <span className="absolute -right-32 top-[26%] h-[430px] w-[430px] rounded-full border border-emerald-900/[0.045]" />
          <span className="absolute -right-16 top-[33%] h-[300px] w-[300px] rounded-full border border-emerald-900/[0.035]" />
          <span className="absolute -left-40 bottom-[-180px] h-[520px] w-[520px] rounded-full border border-emerald-900/[0.04]" />
          <span className="absolute left-[14%] top-[32%] h-1.5 w-1.5 rounded-full bg-emerald-600/10" />
          <span className="absolute right-[24%] bottom-[18%] h-1 w-1 rounded-full bg-emerald-600/10" />
        </div>
        <div className="relative z-10 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <motion.header initial={{ opacity: 0, y: 12 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.35 }} transition={{ duration: 0.45 }} className="mb-12 text-center md:mb-14">
            <h2 className="text-3xl font-extrabold text-[#123d34] md:text-5xl">لماذا <span className="bg-gradient-to-l from-[#18895e] to-[#37bc83] bg-clip-text text-transparent">بيّنة؟</span></h2>
            <p className="mt-4 text-base font-light text-[#53665c] sm:text-xl">لأن التحقق لا يبدأ من الإجابة... بل من الدليل.</p>
          </motion.header>
          <WhyBayyinah />
        </div>
      </section>

      {/* 4. HOW IT WORKS (Rule 42) */}
      <section id="how-it-works" className="relative isolate overflow-hidden py-20 text-white md:py-24" style={{ background: 'radial-gradient(circle at 15% 20%, rgba(65,255,185,.15), transparent 30%), radial-gradient(circle at 85% 75%, rgba(60,220,160,.12), transparent 32%), linear-gradient(135deg, #087455 0%, #006649 45%, #00543d 100%)' }}>
        <div aria-hidden="true" className="pointer-events-none absolute inset-0 overflow-hidden">
          <span className="absolute -right-52 -top-52 h-[620px] w-[620px] rounded-full border border-emerald-100/[0.09]" />
          <span className="absolute -right-28 -top-28 h-[420px] w-[420px] rounded-full border border-emerald-100/[0.07]" />
          <span className="absolute -bottom-64 -left-44 h-[680px] w-[680px] rounded-full border border-emerald-100/[0.08]" />
          <motion.span animate={{ y: [0, -8, 0], opacity: [0.12, 0.22, 0.12] }} transition={{ duration: 19, repeat: Infinity, ease: 'easeInOut' }} className="absolute right-[18%] top-[18%] h-1.5 w-1.5 rounded-full bg-[#baffdf]" />
          <motion.span animate={{ y: [0, 11, 0], opacity: [0.08, 0.18, 0.08] }} transition={{ duration: 23, repeat: Infinity, ease: 'easeInOut' }} className="absolute bottom-[22%] left-[17%] h-1 w-1 rounded-full bg-[#baffdf]" />
          <motion.span animate={{ x: [0, 9, 0], opacity: [0.08, 0.16, 0.08] }} transition={{ duration: 17, repeat: Infinity, ease: 'easeInOut' }} className="absolute left-[43%] top-[13%] h-1 w-1 rounded-full bg-[#baffdf]" />
        </div>
        <div className="relative z-10 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <motion.header initial={{ opacity: 0, y: 12 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.35 }} transition={{ duration: 0.4 }} className="mx-auto max-w-3xl text-center">
            <h2 className="text-3xl font-extrabold text-white sm:text-4xl md:text-5xl">كيف تعمل <span className="bg-gradient-to-l from-[#7dffc8] to-[#31e995] bg-clip-text text-transparent">بيّنة؟</span></h2>
            <p className="mt-4 text-base font-light text-white/80 sm:text-xl">من المحتوى المتداول إلى سلسلة دليل واضحة.</p>
          </motion.header>
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
