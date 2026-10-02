import React from 'react';
import { ShieldCheck, Search, BookOpen, HelpCircle, Info, Sparkles, BarChart3, Award } from 'lucide-react';

export type NavTab = 'home' | 'verify' | 'sources' | 'how-it-works' | 'about' | 'evaluation' | 'demo';

interface NavbarProps {
  activeTab: NavTab;
  setActiveTab: (tab: NavTab) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-bayyinah-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        {/* Brand Logo & Slogan */}
        <div 
          onClick={() => setActiveTab('home')}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-11 h-11 rounded-2xl bg-bayyinah-navy flex items-center justify-center border border-bayyinah-purple/30 group-hover:border-bayyinah-turquoise transition-all shadow-subtle">
            <ShieldCheck className="w-6 h-6 text-bayyinah-turquoise transition-transform group-hover:scale-105" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-bold text-bayyinah-navy tracking-tight">بيّنة AI</span>
              <span className="text-[11px] font-semibold bg-bayyinah-purple-light text-bayyinah-purple px-2 py-0.5 rounded-full">
                المسار الرابع
              </span>
            </div>
            <span className="text-xs text-bayyinah-gray-500 block font-normal">تحقّق قبل أن تنشر.</span>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="hidden lg:flex items-center gap-1 bg-bayyinah-off-white/80 p-1.5 rounded-2xl border border-bayyinah-gray-200">
          <button
            onClick={() => setActiveTab('home')}
            className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
              activeTab === 'home'
                ? 'bg-white text-bayyinah-purple shadow-subtle'
                : 'text-bayyinah-navy hover:text-bayyinah-purple hover:bg-white/50'
            }`}
          >
            الرئيسية
          </button>

          <button
            onClick={() => setActiveTab('sources')}
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
              activeTab === 'sources'
                ? 'bg-white text-bayyinah-purple shadow-subtle'
                : 'text-bayyinah-navy hover:text-bayyinah-purple hover:bg-white/50'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span>المصادر</span>
          </button>

          <button
            onClick={() => setActiveTab('how-it-works')}
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
              activeTab === 'how-it-works'
                ? 'bg-white text-bayyinah-purple shadow-subtle'
                : 'text-bayyinah-navy hover:text-bayyinah-purple hover:bg-white/50'
            }`}
          >
            <HelpCircle className="w-3.5 h-3.5" />
            <span>كيف تعمل؟</span>
          </button>

          <button
            onClick={() => setActiveTab('evaluation')}
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
              activeTab === 'evaluation'
                ? 'bg-white text-bayyinah-purple shadow-subtle'
                : 'text-bayyinah-navy hover:text-bayyinah-purple hover:bg-white/50'
            }`}
          >
            <BarChart3 className="w-3.5 h-3.5 text-emerald-600" />
            <span>تقييم المنصة (30)</span>
          </button>

          <button
            onClick={() => setActiveTab('demo')}
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
              activeTab === 'demo'
                ? 'bg-white text-bayyinah-purple shadow-subtle'
                : 'text-bayyinah-navy hover:text-bayyinah-purple hover:bg-white/50'
            }`}
          >
            <Award className="w-3.5 h-3.5 text-bayyinah-purple" />
            <span>وضع العرض والحكام</span>
          </button>

          <button
            onClick={() => setActiveTab('about')}
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
              activeTab === 'about'
                ? 'bg-white text-bayyinah-purple shadow-subtle'
                : 'text-bayyinah-navy hover:text-bayyinah-purple hover:bg-white/50'
            }`}
          >
            <Info className="w-3.5 h-3.5" />
            <span>عن بيّنة</span>
          </button>
        </nav>

        {/* Action Button */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveTab('demo')}
            className="hidden sm:inline-flex items-center gap-1.5 bg-bayyinah-purple-light text-bayyinah-purple hover:bg-bayyinah-purple hover:text-white text-xs font-bold py-2.5 px-4 rounded-xl transition-all"
          >
            <Award className="w-3.5 h-3.5" />
            <span>Demo الحكام</span>
          </button>

          <button
            onClick={() => setActiveTab('home')}
            className="bg-bayyinah-purple hover:bg-bayyinah-purple-hover text-white text-xs font-bold px-4 py-2.5 rounded-xl transition-all shadow-subtle flex items-center gap-1.5"
          >
            <Search className="w-3.5 h-3.5" />
            <span>تحقق جديد</span>
          </button>
        </div>
      </div>
    </header>
  );
};
