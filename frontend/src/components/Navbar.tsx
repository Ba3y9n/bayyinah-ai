import React, { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';

export type NavTab = 'home' | 'verify' | 'judge-demo' | 'sources' | 'knowledge-domains' | 'health';

interface NavbarProps {
  activeTab: NavTab;
  setActiveTab: (tab: NavTab) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const tabs = [
    { id: 'home', label: 'الرئيسية' },
    { id: 'verify', label: 'التحقق' },
    { id: 'sources', label: 'المصادر المعتمدة' },
    { id: 'knowledge-domains', label: 'طبقة البحث والتحقق' },
    { id: 'health', label: 'حالة النظام' },
  ];
  const visibleTabs = tabs.filter((tab) => tab.id !== 'knowledge-domains' && tab.id !== 'health');

  const handleTabClick = (tabId: string) => {
    setActiveTab(tabId as NavTab);
    setIsMobileMenuOpen(false);
  };

  return (
    <header 
      className={`fixed top-0 w-full z-50 transition-all duration-300 ${
        scrolled 
          ? 'bg-white/90 backdrop-blur-md shadow-sm border-b border-gray-100 py-3' 
          : 'bg-white/95 backdrop-blur-sm py-5'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between relative">
        {/* Brand Logo */}
        <div 
          onClick={() => handleTabClick('home')}
          className="flex items-center cursor-pointer group"
        >
          <img 
            src="/bayyinah-logo.png" 
            alt="بيّنة AI" 
            className="h-9 w-auto object-contain transition-transform duration-300 group-hover:scale-105" 
          />
        </div>

        {/* Desktop Navigation */}
        <nav className="hidden lg:flex flex-1 items-center justify-center gap-8">
          {visibleTabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => handleTabClick(tab.id)}
              aria-current={activeTab === tab.id ? 'page' : undefined}
              className={`relative py-2 text-[15px] font-medium transition-colors ${
                activeTab === tab.id
                  ? 'font-semibold text-[#005c43]'
                  : 'text-gray-700 hover:text-[#005c43]'
              }`}
            >
              {tab.label}
              {activeTab === tab.id && <span className="absolute inset-x-0 -bottom-1 h-0.5 rounded-full bg-[#c89418]" />}
            </button>
          ))}
        </nav>

        {/* Mobile Menu Toggle */}
        <button 
          className="lg:hidden p-2 text-bayyinah-dark-text"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        >
          {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="lg:hidden absolute top-full left-0 w-full bg-white border-b border-gray-100 shadow-lg flex flex-col py-4 px-6 gap-4">
          {visibleTabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => handleTabClick(tab.id)}
              aria-current={activeTab === tab.id ? 'page' : undefined}
              className={`border-r-2 py-2 pr-3 text-right text-[16px] transition-colors ${
                activeTab === tab.id
                  ? 'border-[#c89418] font-semibold text-[#005c43]'
                  : 'border-transparent text-bayyinah-dark-text'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      )}
    </header>
  );
};

