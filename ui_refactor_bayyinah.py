import re

with open('frontend/src/pages/HomePage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. HeroOrbit Refactor
hero_orbit_new = """
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
        className="relative w-[340px] h-[340px] md:w-[480px] md:h-[480px] flex items-center justify-center"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {/* Center Element */}
        <div className="absolute z-30 w-24 h-24 md:w-32 md:h-32 rounded-full bg-white flex flex-col items-center justify-center text-center p-2 shadow-[0_0_40px_rgba(53,185,154,0.3)]">
          <span className="text-bayyinah-dark-text font-bold text-base md:text-lg tracking-wide">بيّنة AI</span>
          <span className="text-[10px] md:text-xs text-bayyinah-soft-emerald mt-0.5">محرك التحقق</span>
        </div>

        {/* Orbit Nodes */}
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
                  ${isActive ? 'bg-bayyinah-emerald text-white border-bayyinah-emerald shadow-[0_0_30px_rgba(53,185,154,0.9)] scale-115' : 'bg-white text-bayyinah-dark-text hover:bg-bayyinah-emerald/10 border-gray-100 shadow-sm'}`}
                whileHover={{ scale: 1.15 }}
                whileTap={{ scale: 0.95 }}
              >
                {step.icon}
              </motion.button>
              <div className={`mt-1.5 font-bold transition-all duration-300 ${isActive ? 'text-bayyinah-dark-text text-base drop-shadow-md' : 'text-bayyinah-dark-text/70 text-xs'}`}>
                {step.label}
              </div>
            </div>
          );
        })}
      </div>
      
      {/* Box below orbit for active description */}
      <div className="mt-8 p-6 bg-white rounded-2xl shadow-elevated border border-gray-100 max-w-md w-full text-center z-40 transition-all duration-300 transform min-h-[100px] flex flex-col justify-center">
        <p className="text-lg font-bold text-bayyinah-emerald mb-2">{steps[activeIndex].label}</p>
        <p className="text-base text-bayyinah-dark-text/80">{steps[activeIndex].desc}</p>
      </div>
    </div>
  );
};
"""
content = re.sub(r'const HeroOrbit = \(\) => \{.*?\};\n\n// 2\. CountUp', hero_orbit_new + '\n// 2. CountUp', content, flags=re.DOTALL)

# 2. WhyBayyinah Refactor
why_bayyinah_new = """
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
"""
content = re.sub(r'const WhyBayyinah = \(\) => \{.*?\};\n\n// 4\. How It Works Timeline', why_bayyinah_new + '\n// 4. How It Works Timeline', content, flags=re.DOTALL)


# 3. Main Hero section layout refactor
old_hero = r"""      \{/\* 1\. HERO SECTION \*/\}
      <section className="relative min-h-\[90vh\] flex items-center pt-20 overflow-hidden">
        \{/\* Background Image Layer exactly as Dawr reference \*/\}
        <div className="absolute inset-0 z-0 bg-bayyinah-deep-emerald">
          <img 
            src="/hero-bg\.jpg" 
            alt="Islamic Skyline" 
            className="w-full h-full object-cover object-center mix-blend-overlay opacity-60"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-bayyinah-deep-emerald/90 via-bayyinah-deep-emerald/60 to-transparent"></div>
        </div>
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full flex flex-col-reverse lg:flex-row items-center gap-12 lg:gap-8">
          
          \{/\* Right Content \(RTL\) - Typography \*/\}
          <div className="flex-1 flex flex-col items-start text-right">
            <motion\.div
              initial=\{\{ opacity: 0, y: -10 \}\}
              animate=\{\{ opacity: 1, y: 0 \}\}
              className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md border border-white/20 text-bayyinah-soft-emerald px-4 py-1\.5 rounded-full text-xs font-semibold mb-6 shadow-sm"
            >
              <ShieldCheck className="w-4 h-4 text-bayyinah-soft-emerald" />
              
            </motion\.div>

            <motion\.h1 
              initial=\{\{ opacity: 0, y: 30 \}\}
              animate=\{\{ opacity: 1, y: 0 \}\}
              transition=\{\{ duration: 0\.6 \}\}
              className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 text-bayyinah-dark-text leading-\[1\.2\] drop-shadow-md"
            >
              تحقّق قبل<br/>أن تنشر\.
            </motion\.h1>
            
            <motion\.p 
              initial=\{\{ opacity: 0, y: 30 \}\}
              animate=\{\{ opacity: 1, y: 0 \}\}
              transition=\{\{ duration: 0\.6, delay: 0\.2 \}\}
              className="text-lg md:text-2xl text-bayyinah-dark-text/90 max-w-xl mb-6 leading-relaxed font-light drop-shadow-sm"
            >
              بيّنة تساعدك على التحقق من الادعاءات الإسلامية بالرجوع إلى المصادر المعتمدة وإظهار الدليل\.
            </motion\.p>

            <motion\.p
              initial=\{\{ opacity: 0 \}\}
              animate=\{\{ opacity: 1 \}\}
              transition=\{\{ delay: 0\.3 \}\}
              className="text-sm text-bayyinah-soft-emerald/90 max-w-lg mb-8 font-medium bg-white/5 border border-white/10 p-3\.5 rounded-2xl"
            >
              «بيّنة لا تطلب منك أن تثق بالذكاء الاصطناعي؛ بل تمكّنك من رؤية المصدر بنفسك\.»
            </motion\.p>
            
            <motion\.div 
              initial=\{\{ opacity: 0, y: 30 \}\}
              animate=\{\{ opacity: 1, y: 0 \}\}
              transition=\{\{ duration: 0\.6, delay: 0\.4 \}\}
              className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto"
            >
              <button 
                onClick=\{onStartVerification\}
                className="bg-bayyinah-emerald hover:bg-bayyinah-soft-emerald text-bayyinah-dark-text px-8 py-4 rounded-xl font-bold text-lg transition-colors flex items-center justify-center gap-2 shadow-\[0_0_20px_rgba\(53,185,154,0\.4\)\] border border-white/10 cursor-pointer"
              >
                ابدأ التحقق
                <ArrowLeft className="w-5 h-5" />
              </button>
              <button 
                onClick=\{\(\) => setActiveTab\('judge-demo'\)\}
                className="bg-transparent border border-white/30 hover:border-white hover:bg-white/10 text-bayyinah-dark-text px-8 py-4 rounded-xl font-medium text-lg transition-colors cursor-pointer flex items-center justify-center gap-2"
              >
                <span>عرض الحكّام \(Demo\)</span>
                <ArrowLeft className="w-5 h-5" />
              </button>
            </motion\.div>

            <div className="mt-8 text-xs text-bayyinah-dark-text/60 flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-bayyinah-soft-emerald shrink-0" />
              <span>بيّنة نظام ذكاء اصطناعي للتحقق والمساعدة، وليست جهة إفتاء\.</span>
            </div>
          </div>

          \{/\* Left Content \(RTL\) - Interactive Orbit \*/\}
          <motion\.div 
            initial=\{\{ opacity: 0, scale: 0\.9 \}\}
            animate=\{\{ opacity: 1, scale: 1 \}\}
            transition=\{\{ duration: 0\.8, delay: 0\.3 \}\}
            className="flex-1 w-full flex justify-center lg:justify-end"
          >
            <HeroOrbit />
          </motion\.div>

        </div>
      </section>"""

new_hero = """      {/* 1. HERO SECTION */}
      <section className="relative min-h-[90vh] flex flex-col items-center pt-32 pb-16 overflow-hidden bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full flex flex-col items-center justify-center gap-12 text-center">
          
          {/* Top Content - Typography */}
          <div className="flex flex-col items-center max-w-3xl">
            <motion.h1 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 text-bayyinah-dark-text leading-[1.2] drop-shadow-sm"
            >
              تحقّق قبل أن تنشر.
            </motion.h1>
            
            <motion.p 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-lg md:text-2xl text-bayyinah-dark-text/80 max-w-2xl mb-8 leading-relaxed font-light"
            >
              بيّنة تساعدك على التحقق من الادعاءات الإسلامية بالرجوع إلى المصادر المعتمدة وإظهار الدليل.
            </motion.p>
            
            <motion.div 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="flex justify-center mb-4"
            >
              <button 
                onClick={onStartVerification}
                className="bg-bayyinah-emerald hover:bg-bayyinah-soft-emerald text-white px-10 py-4 rounded-xl font-bold text-xl transition-colors flex items-center justify-center gap-3 shadow-[0_0_20px_rgba(8,127,104,0.3)] cursor-pointer"
              >
                ابدأ التحقق
                <ArrowLeft className="w-6 h-6" />
              </button>
            </motion.div>
          </div>

          {/* Bottom Content - Interactive Orbit */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="w-full flex justify-center mt-4"
          >
            <HeroOrbit />
          </motion.div>
        </div>
      </section>"""

content = re.sub(old_hero, new_hero, content)

# 4. Remove links from Statistics section
stats_old = r'<a[^>]*>.*?</a>'
# We need to be careful not to remove other links.
# The links are specific to the Stats block
content = content.replace('''              <a 
                href="https://dawa.center" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="mt-6 text-xs text-bayyinah-emerald hover:underline font-bold flex items-center gap-1"
              >
                <span>دراسة توثيق المحتوى الرقمي 2025</span>
                <ArrowLeft className="w-3.5 h-3.5" />
              </a>''', '')

content = content.replace('''              <a 
                href="https://islamic-content.com" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="mt-6 text-xs text-bayyinah-emerald hover:underline font-bold flex items-center gap-1"
              >
                <span>دراسة عينة المنصات الرقمية 2025</span>
                <ArrowLeft className="w-3.5 h-3.5" />
              </a>''', '')

content = content.replace('''              <a 
                href="https://shamela.ws" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="mt-6 text-xs text-bayyinah-emerald hover:underline font-bold flex items-center gap-1"
              >
                <span>كشف الخفاء ومزيل الإلباس</span>
                <ArrowLeft className="w-3.5 h-3.5" />
              </a>''', '')

# 5. Fix RESTUCTURED BOX section (What do these numbers mean?)
# Make it have arrows pointing left between boxes
boxes_old = r"""            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
              <div className="group bg-white p-5 rounded-2xl border border-gray-100 hover:border-bayyinah-emerald/40 hover:shadow-subtle hover:-translate-y-1 transition-all duration-300">
                <span className="text-bayyinah-emerald font-bold mb-2 block text-lg">01</span>
                <h4 className="text-bayyinah-dark-text font-bold text-sm leading-relaxed">هل تم توثيقه؟</h4>
              </div>
              <div className="group bg-white p-5 rounded-2xl border border-gray-100 hover:border-bayyinah-emerald/40 hover:shadow-subtle hover:-translate-y-1 transition-all duration-300">
                <span className="text-bayyinah-emerald font-bold mb-2 block text-lg">02</span>
                <h4 className="text-bayyinah-dark-text font-bold text-sm leading-relaxed">ما مصدره؟</h4>
              </div>
              <div className="group bg-white p-5 rounded-2xl border border-gray-100 hover:border-bayyinah-emerald/40 hover:shadow-subtle hover:-translate-y-1 transition-all duration-300">
                <span className="text-bayyinah-emerald font-bold mb-2 block text-lg">03</span>
                <h4 className="text-bayyinah-dark-text font-bold text-sm leading-relaxed">هل النص مطابق؟</h4>
              </div>
              <div className="group bg-white p-5 rounded-2xl border border-gray-100 hover:border-bayyinah-emerald/40 hover:shadow-subtle hover:-translate-y-1 transition-all duration-300">
                <span className="text-bayyinah-emerald font-bold mb-2 block text-lg">04</span>
                <h4 className="text-bayyinah-dark-text font-bold text-sm leading-relaxed">ما درجة ثبوته؟</h4>
              </div>
              <div className="group bg-white p-5 rounded-2xl border border-gray-100 hover:border-bayyinah-emerald/40 hover:shadow-subtle hover:-translate-y-1 transition-all duration-300">
                <span className="text-bayyinah-emerald font-bold mb-2 block text-lg">05</span>
                <h4 className="text-bayyinah-dark-text font-bold text-sm leading-relaxed">هل توجد مصادر أخرى؟</h4>
              </div>
            </div>"""

boxes_new = """            <div className="flex flex-col lg:flex-row items-center justify-between gap-2 lg:gap-4 mt-8">
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
            </div>"""
content = content.replace(boxes_old, boxes_new)

# 6. Mission and Vision interactive
mission_old = r'className="relative"'
mission_new = r'className="relative bg-white p-10 rounded-3xl border border-gray-100 shadow-sm hover:shadow-elevated transition-all duration-300 hover:border-bayyinah-emerald/30"'
content = content.replace(mission_old, mission_new, 1) # Only first match

vision_old = r'className="bg-white p-10 rounded-3xl border border-gray-100 shadow-sm relative overflow-hidden flex flex-col justify-between"'
vision_new = r'className="bg-white p-10 rounded-3xl border border-gray-100 shadow-sm hover:shadow-elevated transition-all duration-300 hover:border-bayyinah-emerald/30 relative overflow-hidden flex flex-col justify-between"'
content = content.replace(vision_old, vision_new)

# 7. CTA Section - Change background to 10% green, remove lines, fix text color to dark
cta_old = r"""      \{/\* 6\. IMMERSIVE CTA \*/\}
      <section className="relative py-32 bg-bayyinah-deep-emerald text-bayyinah-dark-text overflow-hidden">
        \{/\* Background Visuals \*/\}
        <div className="absolute inset-0 z-0 opacity-10">
          <div className="absolute right-0 top-1/2 w-full h-px bg-gradient-to-l from-white to-transparent transform -translate-y-1/2"></div>
          <div className="absolute right-1/4 top-0 w-px h-full bg-gradient-to-b from-white to-transparent"></div>
        </div>

        <div className="max-w-4xl mx-auto px-4 text-center relative z-10">
          <motion\.h2 
            initial=\{\{ opacity: 0, scale: 0\.95 \}\}
            whileInView=\{\{ opacity: 1, scale: 1 \}\}
            viewport=\{\{ once: true \}\}
            className="text-4xl md:text-6xl font-bold mb-6 text-bayyinah-dark-text"
          >
            قبل أن تشارك\.\.\. <span className="text-bayyinah-gold">تحقّق\.</span>
          </motion\.h2>
          <motion\.p 
            initial=\{\{ opacity: 0 \}\}
            whileInView=\{\{ opacity: 1 \}\}
            viewport=\{\{ once: true \}\}
            transition=\{\{ delay: 0\.2 \}\}
            className="text-xl md:text-2xl text-bayyinah-dark-text/70 mb-12 font-light leading-relaxed max-w-2xl mx-auto"
          >
            أرسل المحتوى الذي تريد التحقق منه، ودع بيّنة تقودك من الادعاء إلى المصدر والدليل\.
          </motion\.p>
          <motion\.button 
            initial=\{\{ opacity: 0, y: 20 \}\}
            whileInView=\{\{ opacity: 1, y: 0 \}\}
            viewport=\{\{ once: true \}\}
            transition=\{\{ delay: 0\.4 \}\}
            onClick=\{onStartVerification\}
            className="bg-white hover:bg-bayyinah-ivory text-bayyinah-deep-emerald px-12 py-5 rounded-2xl font-bold text-xl transition-all shadow-\[0_0_40px_rgba\(255,255,255,0\.15\)\] hover:shadow-\[0_0_60px_rgba\(255,255,255,0\.25\)\] flex items-center gap-3 mx-auto"
          >
            ابدأ التحقق
            <ArrowLeft className="w-6 h-6" />
          </motion\.button>
        </div>
      </section>"""

cta_new = """      {/* 6. IMMERSIVE CTA */}
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
      </section>"""

content = re.sub(cta_old, cta_new, content)

with open('frontend/src/pages/HomePage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("HomePage.tsx updated successfully.")

