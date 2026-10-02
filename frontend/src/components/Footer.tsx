import React from 'react';
import { ShieldCheck, ExternalLink, Github, FileText } from 'lucide-react';
import { NavTab } from './Navbar';

interface FooterProps {
  setActiveTab: (tab: NavTab) => void;
}

export const Footer: React.FC<FooterProps> = ({ setActiveTab }) => {
  return (
    <footer className="bg-bayyinah-navy text-white mt-24 border-t border-bayyinah-purple/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10">
          {/* Brand Col */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-bayyinah-navy-light flex items-center justify-center border border-bayyinah-turquoise/40">
                <ShieldCheck className="w-6 h-6 text-bayyinah-turquoise" />
              </div>
              <div>
                <span className="text-xl font-bold text-white tracking-wide">بيّنة AI</span>
                <span className="text-xs text-bayyinah-turquoise block font-medium">تحقّق قبل أن تنشر.</span>
              </div>
            </div>

            <p className="text-sm text-bayyinah-off-white/80 leading-relaxed max-w-lg">
              منصة ذكية للتحقق من المحتوى الإسلامي الرقمي عبر استخراج الادعاءات واسترجاع الأدلة الموثقة من مصادرها المعتمدة، لتمكين صانعي المحتوى والمعرفين بالإسلام من النشر بموثوقية وأمانة علمية.
            </p>

            {/* Core Principle Quote */}
            <div className="bg-white/5 border border-white/10 rounded-xl p-3 text-xs text-bayyinah-off-white/90">
              <span className="font-semibold text-bayyinah-turquoise">المبدأ الأساسي: </span>
              «بيّنة لا تطلب منك أن تثق بالذكاء الاصطناعي؛ بل تمكّنك من رؤية المصدر بنفسك.»
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-3">
            <h4 className="text-sm font-semibold text-bayyinah-turquoise">روابط المنصة</h4>
            <ul className="space-y-2 text-xs text-bayyinah-off-white/70">
              <li>
                <button onClick={() => setActiveTab('home')} className="hover:text-white transition-colors">
                  التحقق من المحتوى
                </button>
              </li>
              <li>
                <button onClick={() => setActiveTab('sources')} className="hover:text-white transition-colors">
                  سجل المصادر والتراخيص
                </button>
              </li>
              <li>
                <button onClick={() => setActiveTab('how-it-works')} className="hover:text-white transition-colors">
                  كيف تعمل بيّنة؟ (AI Pipeline)
                </button>
              </li>
              <li>
                <button onClick={() => setActiveTab('evaluation')} className="hover:text-white transition-colors">
                  لوحة التقييم المعياري (30 حالة)
                </button>
              </li>
              <li>
                <button onClick={() => setActiveTab('demo')} className="hover:text-white transition-colors">
                  وضع العرض والحكام (Judge Mode)
                </button>
              </li>
              <li>
                <button onClick={() => setActiveTab('about')} className="hover:text-white transition-colors">
                  عن المشروع
                </button>
              </li>
            </ul>
          </div>

          {/* Safety & Disclosure */}
          <div className="space-y-3">
            <h4 className="text-sm font-semibold text-bayyinah-turquoise">الوثائق والسياسات</h4>
            <ul className="space-y-2 text-xs text-bayyinah-off-white/70">
              <li className="flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-bayyinah-turquoise" />
                <span>سياسة البيانات (DATA_POLICY.md)</span>
              </li>
              <li className="flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-bayyinah-turquoise" />
                <span>الإفصاح عن الذكاء الاصطناعي (AI_DISCLOSURE.md)</span>
              </li>
              <li className="flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-bayyinah-turquoise" />
                <span>سجل التراخيص (SOURCES_AND_LICENSES.md)</span>
              </li>
            </ul>
            <div className="flex items-center gap-1.5 text-[11px] text-bayyinah-turquoise/80 pt-2">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>مبني على RAG الموجه بالأدلة فقط</span>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-6 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-bayyinah-off-white/60">
          <div>
            جميع الحقوق محفوظة لمنصة <strong className="text-white">بيّنة AI</strong> © {new Date().getFullYear()} — المسار الرابع: أدوات المعرفة والتحقق لتمكين المعرفين بالإسلام.
          </div>
          <div className="flex items-center gap-4">
            <span className="text-[11px]">MIT Software License</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
