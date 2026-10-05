import React from 'react';
import { NavTab } from './Navbar';

interface FooterProps {
  setActiveTab: (tab: NavTab) => void;
}

export const Footer: React.FC<FooterProps> = ({ setActiveTab }) => {
  return (
    <footer className="bg-bayyinah-ivory border-t border-gray-100 py-16 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">
          
          {/* Brand & Slogan */}
          <div className="lg:col-span-2 flex flex-col gap-4">
            <img src="/bayyinah-logo.png" alt="بيّنة AI" className="h-10 w-auto object-contain object-right" />
            <span className="text-bayyinah-deep-emerald font-bold text-lg">تحقّق قبل أن تنشر.</span>
            <p className="text-bayyinah-secondary-text text-sm leading-relaxed max-w-sm mt-1">
              أدوات المعرفة والتحقق لتمكين المعرّفين بالإسلام. الذكاء الاصطناعي يساعدك في الوصول إلى الدليل، والمصدر هو الذي يُتبع.
            </p>
          </div>

          {/* Quick Links */}
          <div className="flex flex-col gap-3">
            <h4 className="text-bayyinah-dark-text font-bold mb-2 text-sm">التنقل الرئيسي</h4>
            <nav className="flex flex-col gap-2.5">
              <button onClick={() => setActiveTab('home')} className="text-right text-xs text-bayyinah-secondary-text hover:text-bayyinah-emerald transition-colors w-fit cursor-pointer">الرئيسية</button>
              <button onClick={() => setActiveTab('verify')} className="text-right text-xs text-bayyinah-secondary-text hover:text-bayyinah-emerald transition-colors w-fit cursor-pointer">التحقق</button>
              <button onClick={() => setActiveTab('judge-demo')} className="text-right text-xs text-bayyinah-secondary-text hover:text-bayyinah-emerald transition-colors w-fit cursor-pointer">عرض الحكّام (Demo)</button>
              <button onClick={() => setActiveTab('sources')} className="text-right text-xs text-bayyinah-secondary-text hover:text-bayyinah-emerald transition-colors w-fit cursor-pointer">المصادر المعتمدة</button>
              <button onClick={() => setActiveTab('knowledge-domains')} className="text-right text-xs text-bayyinah-secondary-text hover:text-bayyinah-emerald transition-colors w-fit cursor-pointer">طبقة البحث والتحقق</button>
              <button onClick={() => setActiveTab('health')} className="text-right text-xs text-bayyinah-secondary-text hover:text-bayyinah-emerald transition-colors w-fit cursor-pointer">حالة النظام</button>
            </nav>
          </div>

          {/* Developers Team (Section 55) */}
          <div className="flex flex-col gap-3">
            <h4 className="text-bayyinah-dark-text font-bold mb-2 text-sm">فريق التطوير</h4>
            <div className="flex flex-col gap-2 text-xs text-bayyinah-secondary-text">
              <span className="font-semibold text-bayyinah-dark-text">بيان المطيري</span>
              <span className="font-semibold text-bayyinah-dark-text">يزيد المطيري</span>
              <span className="font-semibold text-bayyinah-dark-text">محمد السلامة</span>
            </div>
          </div>

        </div>

        <div className="pt-8 border-t border-gray-200 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-bayyinah-secondary-text">
          <p>© {new Date().getFullYear()} بيّنة AI | Bayyinah AI. جميع الحقوق محفوظة.</p>
          <p>المشروع يخدم التحقق من المحتوى الإسلامي بالرجوع إلى أمهات المصادر المعتمدة.</p>
        </div>
      </div>
    </footer>
  );
};
