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
  FileText
} from 'lucide-react';
import { DemoCase, VerificationResponse } from '../types';

interface JudgeDemoPageProps {
  onStartVerification: (text?: string, imageBase64?: string, isDemo?: boolean, demoId?: string) => void;
}

export const JudgeDemoPage: React.FC<JudgeDemoPageProps> = ({ onStartVerification }) => {
  const [presentationMode, setPresentationMode] = useState(false);

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

  const handleRunCase = (c: any) => {
    onStartVerification(c.input, c.image_sample_url, true, c.id);
  };

  return (
    <div className={`max-w-5xl mx-auto px-4 py-10 space-y-10 ${presentationMode ? 'bg-white p-6 rounded-3xl shadow-xl' : ''}`}>
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-6 border-b border-bayyinah-gray-200">
        <div>
          <div className="inline-flex items-center gap-2 bg-bayyinah-purple-light text-bayyinah-purple px-3 py-1 rounded-full text-xs font-semibold mb-2">
            <Award className="w-3.5 h-3.5" />
            <span>مسار التحكيم والعرض المباشر (Judge Mode)</span>
          </div>
          <h1 className="text-2xl md:text-4xl font-extrabold text-bayyinah-navy">
            منصة العرض السريع للحكام (Demo Walkthrough)
          </h1>
          <p className="text-xs md:text-sm text-bayyinah-gray-600 mt-1">
            5 سيناريوهات متكاملة تم إعدادها لتجربة مسار التحقق الحقيقي من البداية حتى إصدار النتيجة وسلسلة الأدلة.
          </p>
        </div>

        {/* Presentation Mode Toggle */}
        <button
          onClick={() => setPresentationMode(!presentationMode)}
          className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold transition-all shadow-subtle ${
            presentationMode
              ? 'bg-bayyinah-purple text-white shadow-glow-purple'
              : 'bg-white text-bayyinah-navy border border-bayyinah-gray-200 hover:bg-bayyinah-off-white'
          }`}
        >
          <SlidersHorizontal className="w-4 h-4" />
          <span>{presentationMode ? 'إيقاف وضع العرض' : 'تفعيل وضع العرض (Presentation Mode)'}</span>
        </button>
      </div>

      {/* Principle Quote Banner */}
      <div className="bg-gradient-to-r from-bayyinah-navy to-bayyinah-navy-light text-white rounded-3xl p-6 md:p-8 flex items-center justify-between gap-6 shadow-xl border border-bayyinah-turquoise/30">
        <div className="space-y-1">
          <span className="text-xs text-bayyinah-turquoise font-bold uppercase tracking-wider">الرسالة الأساسية</span>
          <p className="text-sm md:text-base font-semibold leading-relaxed">
            «بيّنة لا تطلب منك أن تثق بالذكاء الاصطناعي؛ بل تمكّنك من رؤية المصدر بنفسك.»
          </p>
        </div>
        <div className="hidden sm:block flex-shrink-0 text-bayyinah-turquoise text-2xl font-black">
          Track 4
        </div>
      </div>

      {/* 5 Judge Test Cards */}
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

              {!presentationMode && (
                <div className="text-[11px] text-bayyinah-gray-500 pt-1 flex items-center gap-2">
                  <strong className="text-bayyinah-navy">الهدف من الفحص: </strong>
                  <span>{item.why}</span>
                </div>
              )}
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
    </div>
  );
};
