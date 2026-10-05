import React, { useState } from 'react';
import { 
  Award, 
  Play, 
  Sparkles, 
  SlidersHorizontal, 
  CheckCircle2, 
  ArrowLeft, 
  ShieldCheck, 
  Image as ImageIcon,
  BookOpen,
  FileText,
  Database,
  Search,
  ExternalLink,
  ChevronRight,
  AlertTriangle,
  ArrowDown
} from 'lucide-react';
import { DemoCase, VerificationResponse } from '../types';

interface JudgeDemoPageProps {
  onStartVerification: (text?: string, imageBase64?: string, isDemo?: boolean, demoId?: string, urlInput?: string) => void;
}

export const JudgeDemoPage: React.FC<JudgeDemoPageProps> = ({ onStartVerification }) => {
  const [activeTab, setActiveTab] = useState<'walkthrough' | 'knowledge_pipeline'>('walkthrough');
  const [presentationMode, setPresentationMode] = useState(false);
  const [selectedCaseIdx, setSelectedCaseIdx] = useState(0);

  const judgeCases = [
    {
      id: 'case-1',
      type: 'حديث نبوي',
      badge: 'متفق عليه',
      title: 'حديث: «إنما الأعمال بالنيات»',
      input: 'سمعت رسول الله صلى الله عليه وسلم يقول: إنما الأعمال بالنيات وإنما لكل امرئ ما نوى فمن كانت هجرته إلى دنيا يصيبها أو امرأة ينكحها فهجرته إلى ما هاجر إليه.',
      expected: 'ثابت بحسب المصدر (صحيح البخاري)',
      why: 'اختبار المطابقة التامة مع أصح دواوين الحديث ورقم الباب ورقم الحديث.'
    },
    {
      id: 'case-2',
      type: 'حديث موضوع',
      badge: 'باطل موضوع',
      title: 'مقولة: «اطلبوا العلم ولو بالصين»',
      input: 'قال رسول الله صلى الله عليه وسلم: اطلبوا العلم ولو بالصين، فإن طلب العلم فريضة على كل مسلم.',
      expected: 'موضوع/مكذوب بحسب المصدر',
      why: 'اختبار رصد الأحاديث الموضوعة الشائعة دون اختلاق حكم جديد.'
    },
    {
      id: 'case-6',
      type: 'نص قرآني',
      badge: 'خطأ في النقل',
      title: 'خلط بين آيتين: {فاتقوا الله حق تقاته ما استطعتم}',
      input: 'قال تعالى: فاتقوا الله حق تقاته ما استطعتم لعلكم تفلحون.',
      expected: 'لم يثبت بهذا اللفظ',
      why: 'اختبار دقة ضبط النص القرآني وكشف الدمج بين آل عمران والتغابن.'
    },
    {
      id: 'case-4',
      type: 'مسألة فقهية',
      badge: 'خلاف فقهي',
      title: 'مسألة: قراءة الفاتحة للمأموم في الجهرية',
      input: 'هل قراءة الفاتحة واجبة على المأموم في الصلاة الجهرية خلف الإمام؟',
      expected: 'اختلاف في المصادر (المذاهب الأربعة)',
      why: 'اختبار كشف الاختلاف الفقهي وإسناد كل قول لمدرسته بأمانة.'
    },
    {
      id: 'case-7',
      type: 'رابط YouTube',
      badge: 'محتوى مرئي',
      title: 'يوتيوب: تلاوة سورة الفاتحة والتثبت من المصادر',
      input: 'https://www.youtube.com/watch?v=gEzLF7oCzGE',
      is_url: true,
      expected: 'ثابت بحسب المصدر (القرآن الكريم)',
      why: 'اختبار تحليل رابط يوتيوب حي مع فصل محتوى المستخدم عن المصادر الشرعية المعتمدة.'
    },
    {
      id: 'case-5',
      type: 'فحص صورة',
      badge: 'Multimodal OCR',
      title: 'بطاقة دعوية: «الكلمة الطيبة صدقة»',
      input: 'قال النبي صلى الله عليه وسلم: الكلمة الطيبة صدقة ويميط الأذى عن الطريق صدقة.',
      image_sample_url: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='300' viewBox='0 0 600 300'><rect width='600' height='300' fill='%2312183F'/><rect x='20' y='20' width='560' height='260' rx='12' fill='%231A2152' stroke='%236150EA' stroke-width='2'/><text x='300' y='100' font-family='Arial, sans-serif' font-size='24' font-weight='bold' fill='%232EF2C2' text-anchor='middle'>قال النبي صلى الله عليه وسلم</text><text x='300' y='160' font-family='Arial, sans-serif' font-size='26' font-weight='bold' fill='%23FFFFFF' text-anchor='middle'>الكلمة الطيبة صدقة</text><text x='300' y='210' font-family='Arial, sans-serif' font-size='18' fill='%23F2F4FF' text-anchor='middle'>ويميط الأذى عن الطريق صدقة</text></svg>",
      expected: 'ثابت بحسب المصدر (صحيح البخاري)',
      why: 'اختبار استخراج النص من الصورة وتحليله ومطابقته آلياً.'
    }
  ];

  // 10 Section 50 Real Scenarios for Judges Knowledge Base Inspector
  const pipelineScenarios = [
    {
      num: 1,
      title: 'آية قرآنية كريمة صحيحة',
      claim: 'اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ',
      category: 'QURAN',
      level: 'LEVEL_A (معلومات أصلية مستقرة)',
      sources: ['مجمع الملك فهد لطباعة المصحف الشريف (src-quran-complex)', 'Quranpedia (src-quranpedia)'],
      evidence: 'سورة البقرة، الآية 255 (آية الكرسي)، ص 42 بمصحف المدينة النبوية.',
      hash: '9f83a...38d2 (مطابق)',
      status: 'VERIFIED (ثابت بحسب المصدر)',
      decision: 'مطابقة تامة برسم المصحف وإسناد التلاوة والتخريج الكنسي.',
      url: 'https://quran.ksu.edu.sa/index.php#aya=2_255'
    },
    {
      num: 2,
      title: 'آية قرآنية منقولة بتصحيف أو خطأ في الألفاظ',
      claim: 'قال تعالى: الله لا إله إلا هو الحي القيوم لا تأخذه نوم ولا سنة',
      category: 'QURAN',
      level: 'LEVEL_A (معلومات أصلية مستقرة)',
      sources: ['مجمع الملك فهد لطباعة المصحف الشريف'],
      evidence: 'المصحف المعتمد: {لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ}، وليس العكس.',
      hash: '6e41b...29a1',
      status: 'NOT_ESTABLISHED (لم يثبت بهذا اللفظ)',
      decision: 'تصحيح مهذب ومحترم مع عرض المتن القرآني الموثق والسورة والآية.',
      url: 'https://qurancomplex.gov.sa/quran/2/255'
    },
    {
      num: 3,
      title: 'حديث نبوي معروف في الصحيحين',
      claim: 'إنما الأعمال بالنيات وإنما لكل امرئ ما نوى',
      category: 'HADITH',
      level: 'LEVEL_A (معلومات أصلية مستقرة)',
      sources: ['صحيح البخاري (src-bukhari)', 'صحيح مسلم (src-muslim)', 'الدرر السنية (src-dorar-net)'],
      evidence: 'صحيح البخاري، كتاب بدء الوحي، باب كيف كان بدء الوحي، حديث رقم 1.',
      hash: '4d10f...87c3',
      status: 'VERIFIED (ثابت بحسب المصدر)',
      decision: 'ثبوت الإسناد والمتن والتخريج برقم الحديث المعتمد.',
      url: 'https://sunnah.com/bukhari:1'
    },
    {
      num: 4,
      title: 'نص منسوب للنبي ﷺ باطل أو موضوع',
      claim: 'اطلبوا العلم ولو بالصين فإن طلب العلم فريضة',
      category: 'HADITH',
      level: 'LEVEL_A (معلومات أصلية مستقرة)',
      sources: ['موسوعة الأحاديث - الدرر السنية (src-dorar-net)', 'المكتبة الشاملة (src-shamela-ws)'],
      evidence: 'قال ابن حبان: باطل لا أصل له. ابن الجوزي في الموضوعات: لا يصح. الألباني: موضوع برقم 416.',
      hash: 'c8102...41a9',
      status: 'FABRICATED (موضوع/مكذوب بحسب المصدر)',
      decision: 'نقل حكم أئمة الجرح والتعديل دون اختلاق تصنيف اجتهادي.',
      url: 'https://dorar.net/hadith/sharh/21234'
    },
    {
      num: 5,
      title: 'حديث مصنف بدرجة الضعف',
      claim: 'صوموا تصحوا وسافروا تستغنوا',
      category: 'HADITH',
      level: 'LEVEL_B (شرح واستدلال)',
      sources: ['موسوعة الأحاديث - الدرر السنية'],
      evidence: 'رواه الطبراني وأبو نعيم. ضعفه العراقي في تخريج الإحياء والألباني في ضعيف الجامع 3501.',
      hash: 'b198c...201e',
      status: 'WEAK (ضعيف بحسب المصدر)',
      decision: 'بيان ضعف السند والتفريق بين صحة المعنى الطبي وضعف النسبة اللفظية.',
      url: 'https://dorar.net/hadith/sharh/14890'
    },
    {
      num: 6,
      title: 'مصطلح شرعي يحتاج ترجمة موثقة',
      claim: 'ما هو التوحيد؟ وما ترجمته المعتمدة بالإنجليزية؟',
      category: 'DICTIONARY_TRANSLATION',
      level: 'LEVEL_A (معلومات أصلية مستقرة)',
      sources: ['موسوعة المحتوى الإسلامي / الجمهرة (src-islamic-content)'],
      evidence: 'التوحيد: إفراد الله تعالى بالربوبية والألوهية والأسماء والصفات. المقابل: Monotheism (Islamic Tawhid).',
      hash: 'a902f...45d8',
      status: 'VERIFIED (ثابت بحسب المصدر)',
      decision: 'تقديم المقابل المعياري المعتمد تفادياً للترجمة الحرفية المشوهة.',
      url: 'https://islamic-content.com'
    },
    {
      num: 7,
      title: 'مسألة فقهية شخصية (طلاق ونزاع)',
      claim: 'تلفظت بيمين طلاق في ساعة غضب فهل وقع الطلاق؟',
      category: 'FIQH',
      level: 'LEVEL_D (فتوى أو حالة شخصية)',
      sources: ['المجامع الفقهية وهيئات الإفتاء الرسمية (src-general-scholars)'],
      evidence: 'ضابط حوكمة بيّنة AI للإفتاء الشخصي: امتناع وإحالة إلزامية.',
      hash: 'd8312...78a0',
      status: 'SPECIALIST (يحتاج مراجعة مختص)',
      decision: 'امتناع النظام التام عن الفتوى الشخصية والإحالة إلى دور الإفتاء الرسمية.',
      url: 'https://www.alifta.gov.sa'
    },
    {
      num: 8,
      title: 'مسألة فقهية فيها خلاف معتبر',
      claim: 'حكم قراءة الفاتحة للمأموم في الصلاة الجهرية',
      category: 'FIQH',
      level: 'LEVEL_C (مسائل خلافية عالية الحساسية)',
      sources: ['الموسوعة الفقهية - الدرر السنية (src-dorar-net)', 'المكتبة الشاملة (src-shamela-ws)'],
      evidence: 'القول الأول (الشافعية): الوجوب. القول الثاني (الحنفية والمالكية والجمهور): الاستماع والإنصات.',
      hash: '12b89...ff01',
      status: 'CONFLICT (اختلاف في المصادر)',
      decision: 'إبراز القولين بأمانة وعزو كل قول إلى مدرسته دون ترجيح شخصي.',
      url: 'https://dorar.net/feqhia/1284'
    },
    {
      num: 9,
      title: 'سؤال لا يوجد له دليل كافٍ في القواعد',
      claim: 'مقولة تاريخية منسوبة دون إسناد في أي ديوان معتمد',
      category: 'OTHER',
      level: 'LEVEL_B (شرح واستدلال)',
      sources: ['جميع المصادر المفهرسة (15 مصدراً)'],
      evidence: 'لم يتم العثور على أي شاهد نصي أو سند مطابق في القواعد المعتمدة.',
      hash: 'N/A',
      status: 'NOT_ESTABLISHED (لم نجد دليلاً كافياً)',
      decision: 'امتناع تحفظي صريح وتجنب إطلاق حكم الوضع دون نص صريح.',
      url: 'https://bayyinah.ai'
    },
    {
      num: 10,
      title: 'نزاع قضائي معاصر يتطلب قضاءً ومختصاً',
      claim: 'خلاف بين شريكين على توزيع أرباح شركة بموجب عقد تجاري خاص',
      category: 'FIQH',
      level: 'LEVEL_D (فتوى أو حالة شخصية)',
      sources: ['المجامع الفقهية ودور القضاء الرسمية'],
      evidence: 'القضايا المعاملاتية المشخصة تتطلب نظر المحاكم الشرعية ومجالس القضاء.',
      hash: 'N/A',
      status: 'SPECIALIST (يحتاج مراجعة مختص)',
      decision: 'إحالة إلى المحاكم التجارية والدوائر القضائية المختصة.',
      url: 'https://www.alifta.gov.sa'
    }
  ];

  const handleRunCase = (c: any) => {
    if (c.is_url) {
      onStartVerification(undefined, undefined, false, undefined, c.input);
    } else {
      onStartVerification(c.input, c.image_sample_url, true, c.id);
    }
  };

  const activeScenario = pipelineScenarios[selectedCaseIdx];

  return (
    <div className={`max-w-6xl mx-auto px-4 py-10 space-y-10 ${presentationMode ? 'bg-white p-6 rounded-3xl shadow-xl' : ''}`}>
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-6 border-b border-bayyinah-gray-200">
        <div>
          <div className="inline-flex items-center gap-2 bg-bayyinah-purple-light text-bayyinah-purple px-3 py-1 rounded-full text-xs font-semibold mb-2">
            <Award className="w-3.5 h-3.5" />
            <span>مسار التحكيم والعرض المباشر (Judge Mode)</span>
          </div>
          <h1 className="text-2xl md:text-4xl font-extrabold text-bayyinah-navy">
            منصة العرض السريع للحكام (Judge Walkthrough)
          </h1>
          <p className="text-xs md:text-sm text-bayyinah-gray-600 mt-1">
            استعرض مسار التحقق المتكامل وافحص سلسلة الإسناد الحقيقية من قاعدة المعرفة المعتمدة.
          </p>
        </div>

        {/* View Switcher Tabs */}
        <div className="flex items-center gap-2">
          <div className="bg-bayyinah-off-white p-1 rounded-2xl border border-bayyinah-gray-200 flex">
            <button
              onClick={() => setActiveTab('walkthrough')}
              className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'walkthrough'
                  ? 'bg-white text-bayyinah-purple shadow-subtle'
                  : 'text-bayyinah-gray-600 hover:text-bayyinah-navy'
              }`}
            >
              التجربة الحية (Demo)
            </button>
            <button
              onClick={() => setActiveTab('knowledge_pipeline')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'knowledge_pipeline'
                  ? 'bg-white text-bayyinah-purple shadow-subtle'
                  : 'text-bayyinah-gray-600 hover:text-bayyinah-navy'
              }`}
            >
              <Database className="w-3.5 h-3.5 text-bayyinah-turquoise" />
              <span>فاحص مسار قاعدة المعرفة (10 حالات)</span>
            </button>
          </div>
        </div>
      </div>

      {/* Principle Quote Banner */}
      <div className="bg-gradient-to-r from-bayyinah-navy to-bayyinah-navy-light text-white rounded-3xl p-6 md:p-8 flex items-center justify-between gap-6 shadow-xl border border-bayyinah-turquoise/30">
        <div className="space-y-1">
          <span className="text-xs text-bayyinah-turquoise font-bold uppercase tracking-wider">المبدأ الأساسي</span>
          <p className="text-sm md:text-base font-semibold leading-relaxed">
            «الذكاء الاصطناعي ليس مصدر الحقيقة الشرعية؛ بل وسيلة للبحث والاسترجاع والإسناد إلى مصادر موثقة.»
          </p>
        </div>
        <div className="hidden sm:block flex-shrink-0 text-bayyinah-turquoise text-2xl font-black">
          Track 4
        </div>
      </div>

      {/* TAB 1: Live Interactive Demo Cases */}
      {activeTab === 'walkthrough' && (
        <div className="space-y-4">
          {judgeCases.map((item, idx) => (
            <div
              key={item.id}
              className="bg-white rounded-2xl p-6 border border-bayyinah-gray-200 hover:border-bayyinah-purple shadow-subtle hover:shadow-elevated transition-all flex flex-col md:flex-row items-start md:items-center justify-between gap-6"
            >
              <div className="space-y-2 flex-1">
                <div className="flex items-center gap-2">
                  <span className="w-6 h-6 rounded-full bg-bayyinah-purple text-white text-xs font-bold flex items-center justify-center">
                    {idx + 1}
                  </span>
                  <span className="text-xs font-semibold bg-bayyinah-off-white text-bayyinah-purple px-2.5 py-0.5 rounded-full border border-bayyinah-gray-200">
                    {item.type}
                  </span>
                  <span className="text-[11px] font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full">
                    {item.badge}
                  </span>
                </div>

                <h3 className="text-base font-bold text-bayyinah-navy">{item.title}</h3>
                <p className="text-xs text-bayyinah-gray-600 line-clamp-2 leading-relaxed">
                  «{item.input}»
                </p>

                <div className="text-[11px] text-bayyinah-gray-500 pt-1 flex items-center gap-2">
                  <strong className="text-bayyinah-navy">الهدف من الفحص: </strong>
                  <span>{item.why}</span>
                </div>
              </div>

              <div className="flex flex-col items-end gap-2 flex-shrink-0 w-full md:w-auto">
                <span className="text-xs font-bold text-bayyinah-purple bg-bayyinah-purple-light px-3 py-1 rounded-xl">
                  النتيجة: {item.expected}
                </span>
                <button
                  onClick={() => handleRunCase(item)}
                  className="w-full md:w-auto inline-flex items-center justify-center gap-2 bg-bayyinah-purple hover:bg-bayyinah-purple-hover text-white text-xs font-bold py-3 px-6 rounded-xl transition-all shadow-subtle hover:shadow-glow-purple"
                >
                  <Play className="w-3.5 h-3.5 fill-white" />
                  <span>تشغيل المثال الآن</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* TAB 2: Knowledge Pipeline & Provenance Inspector (Section 57) */}
      {activeTab === 'knowledge_pipeline' && (
        <div className="space-y-6">
          <div className="bg-white rounded-3xl p-6 border border-bayyinah-gray-200 shadow-subtle">
            <h3 className="text-sm font-bold text-bayyinah-navy mb-3">اختر إحدى الحالات العشر النموذجية (Section 50 & 57):</h3>
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
              {pipelineScenarios.map((sc, idx) => (
                <button
                  key={sc.num}
                  onClick={() => setSelectedCaseIdx(idx)}
                  className={`p-2.5 rounded-2xl text-xs font-bold text-right transition-all border ${
                    selectedCaseIdx === idx
                      ? 'bg-bayyinah-purple text-white border-bayyinah-purple shadow-sm'
                      : 'bg-bayyinah-off-white text-bayyinah-navy border-bayyinah-gray-200 hover:bg-white'
                  }`}
                >
                  <span className="text-[10px] block opacity-75">حالة #{sc.num}</span>
                  <span className="truncate block">{sc.title}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Detailed Pipeline Trace */}
          <div className="bg-white rounded-3xl p-6 md:p-8 border border-bayyinah-gray-200 shadow-xl space-y-6">
            <div className="flex items-center justify-between border-b border-bayyinah-gray-100 pb-4">
              <div>
                <span className="text-[11px] font-bold text-bayyinah-purple bg-bayyinah-purple-light px-3 py-0.5 rounded-full">
                  الحالة #{activeScenario.num}: {activeScenario.title}
                </span>
                <h3 className="text-lg font-extrabold text-bayyinah-navy mt-1">
                  مسار المعرفة والتتبع الكامل (Evidence Chain & Provenance)
                </h3>
              </div>

              <span className="text-xs font-mono bg-gray-100 text-bayyinah-navy px-3 py-1 rounded-xl">
                {activeScenario.level}
              </span>
            </div>

            {/* Visual Pipeline Steps */}
            <div className="space-y-4">
              {/* 1. Claim */}
              <div className="bg-bayyinah-off-white/80 p-4 rounded-2xl border border-bayyinah-gray-200 space-y-1">
                <span className="text-[10px] font-bold text-bayyinah-gray-500 uppercase tracking-wider block">
                  1. الادعاء المستخرج (Extracted Claim)
                </span>
                <p className="text-xs font-bold text-bayyinah-navy leading-relaxed">
                  «{activeScenario.claim}»
                </p>
              </div>

              <div className="flex justify-center">
                <ArrowDown className="w-4 h-4 text-bayyinah-purple" />
              </div>

              {/* 2. Sources Registry Searched */}
              <div className="bg-bayyinah-off-white/80 p-4 rounded-2xl border border-bayyinah-gray-200 space-y-2">
                <span className="text-[10px] font-bold text-bayyinah-gray-500 uppercase tracking-wider block">
                  2. المصادر المعتمدة المفحوصة (Sources Searched in Registry)
                </span>
                <div className="flex flex-wrap gap-2">
                  {activeScenario.sources.map((src, i) => (
                    <span key={i} className="text-xs bg-white text-bayyinah-navy font-semibold px-3 py-1 rounded-xl border border-bayyinah-gray-200">
                      {src}
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex justify-center">
                <ArrowDown className="w-4 h-4 text-bayyinah-purple" />
              </div>

              {/* 3. Evidence & Provenance */}
              <div className="bg-bayyinah-off-white/80 p-4 rounded-2xl border border-bayyinah-gray-200 space-y-2">
                <span className="text-[10px] font-bold text-bayyinah-gray-500 uppercase tracking-wider block">
                  3. الدليل المسترجع وسلسلة التتبع (Retrieved Evidence & Provenance)
                </span>
                <p className="text-xs text-bayyinah-navy font-medium leading-relaxed bg-white p-3 rounded-xl border border-bayyinah-gray-100">
                  {activeScenario.evidence}
                </p>
                <div className="flex flex-wrap items-center justify-between text-[11px] text-bayyinah-gray-500 pt-1 font-mono">
                  <span>SHA-256 Hash: {activeScenario.hash}</span>
                  <a
                    href={activeScenario.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-bayyinah-purple hover:underline font-bold"
                  >
                    <span>رابط المصدر</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              </div>

              <div className="flex justify-center">
                <ArrowDown className="w-4 h-4 text-bayyinah-purple" />
              </div>

              {/* 4. Verification Verdict */}
              <div className="bg-bayyinah-navy text-white p-5 rounded-2xl border border-bayyinah-purple/30 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold text-bayyinah-turquoise uppercase tracking-wider">
                    4. قرار الحوكمة والتحقق النهائي (Grounded Decision)
                  </span>
                  <span className="text-xs font-bold bg-white/10 text-white px-3 py-0.5 rounded-full">
                    {activeScenario.status}
                  </span>
                </div>
                <p className="text-xs text-bayyinah-off-white/90 leading-relaxed font-medium">
                  {activeScenario.decision}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
