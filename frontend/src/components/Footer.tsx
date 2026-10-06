import React from 'react';
import { motion, useReducedMotion } from 'framer-motion';
import { NavTab } from './Navbar';

interface FooterProps {
  setActiveTab: (tab: NavTab) => void;
}

export const Footer: React.FC<FooterProps> = ({ setActiveTab }) => {
  const shouldReduceMotion = useReducedMotion() ?? false;

  return (
    <footer className="relative isolate mt-auto overflow-hidden border-t border-[#d6a72a]/25 py-16 text-white md:py-20" style={{ background: 'radial-gradient(circle at 50% 110%, rgba(75,190,115,.24), transparent 40%), radial-gradient(circle at 90% 70%, rgba(15,135,90,.15), transparent 35%), linear-gradient(135deg, #006347 0%, #004d39 45%, #003f30 100%)' }}>
      <svg className="pointer-events-none absolute inset-0 h-full w-full" viewBox="0 0 1440 520" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
        <defs>
          <pattern id="footer-geometry" width="34" height="34" patternUnits="userSpaceOnUse">
            <path d="M17 1 33 17 17 33 1 17Z M17 8 26 17 17 26 8 17Z" fill="none" stroke="rgba(225,187,85,.55)" strokeWidth=".7" />
          </pattern>
        </defs>
        <rect x="0" y="230" width="150" height="290" fill="url(#footer-geometry)" opacity=".09" />
        <rect x="1290" y="230" width="150" height="290" fill="url(#footer-geometry)" opacity=".09" />
        <motion.g animate={shouldReduceMotion ? { y: 0 } : { y: [0, -5, 0] }} transition={{ duration: 21, repeat: shouldReduceMotion ? 0 : Infinity, ease: 'easeInOut' }}>
          <path d="M0 402 C180 350 300 445 500 415 C720 382 815 350 1020 404 C1200 450 1330 410 1440 374 V520 H0Z" fill="rgba(10,112,76,.32)" />
          <path d="M0 430 C185 382 320 468 520 440 C760 406 875 380 1060 430 C1230 476 1335 438 1440 410 V520 H0Z" fill="rgba(0,48,37,.45)" />
          <path d="M0 402 C180 350 300 445 500 415 C720 382 815 350 1020 404 C1200 450 1330 410 1440 374" fill="none" stroke="rgba(225,187,85,.42)" strokeWidth="1.2" />
          <path d="M0 430 C185 382 320 468 520 440 C760 406 875 380 1060 430 C1230 476 1335 438 1440 410" fill="none" stroke="rgba(140,236,193,.2)" strokeWidth="1" />
        </motion.g>
        {!shouldReduceMotion && <motion.circle r="3.5" fill="#e1bb55" style={{ filter: 'drop-shadow(0 0 7px rgba(225,187,85,.35))' }} animate={{ cx: [140, 470, 850, 1280], cy: [402, 416, 390, 380] }} transition={{ duration: 19, repeat: Infinity, ease: 'linear' }} />}
        {shouldReduceMotion && <circle cx="140" cy="402" r="3.5" fill="#c89418" />}
      </svg>

      <div className="relative z-10 mx-auto max-w-[1500px] px-6 sm:px-8 lg:px-12">
        <div className="grid grid-cols-1 gap-10 md:grid-cols-2 md:gap-12 lg:grid-cols-[1.25fr_.8fr_.8fr] lg:gap-0">
          <motion.section initial={shouldReduceMotion ? false : { opacity: 0, y: 14 }} whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.2 }} transition={{ duration: shouldReduceMotion ? 0 : 0.5 }} className="flex flex-col items-start gap-4 md:col-span-2 lg:col-span-1 lg:pl-12">
            <motion.span whileHover={shouldReduceMotion ? undefined : { scale: 1.02 }} className="inline-flex rounded-[14px] bg-white/95 px-3 py-1.5 shadow-[0_8px_28px_rgba(0,0,0,.08)]">
              <img src="/bayyinah-logo.png" alt="بيّنة AI" className="h-[64px] w-[175px] object-contain object-right" />
            </motion.span>
            <h2 className="text-[26px] font-extrabold leading-relaxed text-white sm:text-[30px]">تحقّق قبل أن تنشر.</h2>
            <p className="mt-0.5 max-w-[520px] text-sm leading-[1.9] text-white/82 sm:text-base">
              أدوات المعرفة والتحقق لتمكين المعرّفين بالإسلام. الذكاء الاصطناعي يساعدك في الوصول إلى الدليل، والمصدر هو الذي يُتبع.
            </p>
          </motion.section>

          <motion.section initial={shouldReduceMotion ? false : { opacity: 0, y: 14 }} whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.2 }} transition={{ duration: shouldReduceMotion ? 0 : 0.5, delay: shouldReduceMotion ? 0 : 0.1 }} className="flex flex-col items-start gap-4 md:pr-8 lg:border-r lg:border-[#d6a72a]/30 lg:pr-8">
            <h2 className="text-xl font-bold text-[#e4bc58] sm:text-[22px]">التنقل الرئيسي</h2>
            <span className="h-0.5 w-[42px] rounded-full bg-gradient-to-l from-[#c99728] to-[#f1d67a]" />
            <nav aria-label="التنقل الرئيسي" className="flex flex-col items-start gap-3.5">
              {[
                { label: 'الرئيسية', tab: 'home' as NavTab },
                { label: 'التحقق', tab: 'verify' as NavTab },
                { label: 'المصادر المعتمدة', tab: 'sources' as NavTab }
              ].map((item) => (
                <motion.button key={item.tab} type="button" onClick={() => setActiveTab(item.tab)} whileHover={shouldReduceMotion ? undefined : { x: -3 }} className="text-right text-base text-white/88 transition-colors duration-200 hover:text-[#e8c76c] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#e6be50]/85 focus-visible:ring-offset-4 focus-visible:ring-offset-[#004d39]">
                  {item.label}
                </motion.button>
              ))}
            </nav>
          </motion.section>

          <motion.section initial={shouldReduceMotion ? false : { opacity: 0, y: 14 }} whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.2 }} transition={{ duration: shouldReduceMotion ? 0 : 0.5, delay: shouldReduceMotion ? 0 : 0.2 }} className="flex flex-col items-start gap-4 md:pr-8 lg:border-r lg:border-[#d6a72a]/30 lg:pr-8">
            <h2 className="text-xl font-bold text-[#e4bc58] sm:text-[22px]">فريق التطوير</h2>
            <span className="h-0.5 w-[42px] rounded-full bg-gradient-to-l from-[#c99728] to-[#f1d67a]" />
            <div className="flex flex-col gap-2.5 text-base leading-[1.9] text-white/88">
              <span>بيان المطيري</span>
              <span>يزيد المطيري</span>
              <span>محمد السلامة</span>
            </div>
          </motion.section>
        </div>

        <motion.div initial={shouldReduceMotion ? false : { opacity: 0, y: 10 }} whileInView={shouldReduceMotion ? undefined : { opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.2 }} transition={{ duration: shouldReduceMotion ? 0 : 0.45, delay: shouldReduceMotion ? 0 : 0.28 }} className="relative mt-12 flex justify-start border-t border-transparent pt-7 text-xs text-white/70 sm:text-sm">
          <span className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-l from-transparent via-[rgba(220,175,65,.65)] to-transparent" />
          <svg aria-hidden="true" className="pointer-events-none absolute left-1/2 top-[-5px] h-[10px] w-[10px] -translate-x-1/2" viewBox="0 0 10 10"><path d="M5 0 10 5 5 10 0 5Z" fill="#d6a72a" /></svg>
          <p>© {new Date().getFullYear()} بيّنة AI | Bayyinah AI. جميع الحقوق محفوظة.</p>
        </motion.div>
      </div>
    </footer>
  );
};
