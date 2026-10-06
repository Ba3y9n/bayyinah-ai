import React, { useState } from 'react';
import { VerificationResponse, MultiClaimItem } from '../types';
import { ChevronDown, ChevronUp, FileText, CheckCircle, AlertCircle, FileArchive, Search, LayoutTemplate } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface PDFResultViewerProps {
  result: VerificationResponse;
}

export const PDFResultViewer: React.FC<PDFResultViewerProps> = ({ result }) => {
  const [expandedPages, setExpandedPages] = useState<number[]>([1]); // First page expanded by default
  const { multi_claims, media_metadata } = result;
  
  if (!multi_claims || multi_claims.length === 0) {
    return null;
  }
  
  const togglePage = (pageNum: number) => {
    setExpandedPages(prev => 
      prev.includes(pageNum) ? prev.filter(p => p !== pageNum) : [...prev, pageNum]
    );
  };
  
  // Group claims by page number
  const claimsByPage: Record<number, MultiClaimItem[]> = {};
  multi_claims.forEach(c => {
    const pNum = c.page_number || 1;
    if (!claimsByPage[pNum]) {
      claimsByPage[pNum] = [];
    }
    claimsByPage[pNum].push(c);
  });
  
  const totalPages = media_metadata?.total_pages || Object.keys(claimsByPage).length;
  const processedPages = Object.keys(claimsByPage).length;
  
  return (
    <div className="space-y-6" dir="rtl">
      {/* PDF Header Summary */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-bayyinah-ivory text-bayyinah-emerald rounded-xl shrink-0">
            <FileArchive className="w-8 h-8" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-bayyinah-deep-emerald mb-2">
              نتائج تحليل الوثيقة: {media_metadata?.original_filename || "ملف PDF"}
            </h2>
            <div className="flex flex-wrap gap-4 text-sm text-gray-600">
              <div className="flex items-center gap-1.5">
                <LayoutTemplate className="w-4 h-4 text-gray-400" />
                <span>إجمالي الصفحات: <span className="font-bold">{totalPages}</span></span>
              </div>
              <div className="flex items-center gap-1.5">
                <CheckCircle className="w-4 h-4 text-bayyinah-emerald" />
                <span>الصفحات المعالجة: <span className="font-bold">{processedPages}</span></span>
              </div>
              <div className="flex items-center gap-1.5">
                <Search className="w-4 h-4 text-bayyinah-deep-emerald" />
                <span>الادعاءات المكتشفة: <span className="font-bold">{multi_claims.length}</span></span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Pages Accordion */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-bayyinah-dark-text flex items-center gap-2">
          <FileText className="w-5 h-5 text-bayyinah-emerald" />
          التفاصيل صفحة بصفحة
        </h3>
        
        {Object.keys(claimsByPage).map((pNumStr) => {
          const pageNum = parseInt(pNumStr);
          const claims = claimsByPage[pageNum];
          const isExpanded = expandedPages.includes(pageNum);
          
          return (
            <div key={pageNum} className="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm">
              <button 
                onClick={() => togglePage(pageNum)}
                className="w-full flex items-center justify-between p-5 bg-gray-50 hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-bayyinah-ivory text-bayyinah-emerald flex items-center justify-center font-bold text-sm">
                    {pageNum}
                  </div>
                  <span className="font-bold text-bayyinah-dark-text">الصفحة {pageNum}</span>
                  <span className="text-xs bg-gray-200 text-gray-600 px-2 py-0.5 rounded-full">
                    {claims.length} ادعاء
                  </span>
                </div>
                {isExpanded ? <ChevronUp className="w-5 h-5 text-gray-500" /> : <ChevronDown className="w-5 h-5 text-gray-500" />}
              </button>
              
              <AnimatePresence>
                {isExpanded && (
                  <motion.div 
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="border-t border-gray-200 p-5 space-y-6"
                  >
                    {claims.map((claim, idx) => {
                      const vRes = claim.verification_result;
                      const hasResult = !!vRes;
                      
                      return (
                        <div key={idx} className="pb-6 border-b border-gray-100 last:border-0 last:pb-0">
                          <div className="mb-3">
                            <span className="text-xs font-bold text-gray-400 mb-1 block">الادعاء المكتشف</span>
                            <p className="text-gray-800 font-medium font-arabic">{claim.claim_text}</p>
                          </div>
                          
                          {hasResult ? (
                            <div className="bg-gray-50 p-4 rounded-xl space-y-3 border border-gray-100">
                              <div className="flex items-start gap-2">
                                <div className={`px-2.5 py-1 rounded-full text-xs font-bold shrink-0 ${vRes.status_slug === 'verified_authentic' ? 'bg-bayyinah-emerald text-white' : (vRes.status_slug?.includes('fabricated') ? 'bg-red-600 text-white' : 'bg-gray-700 text-white')}`}>
                                  {vRes.status_ar || 'نتيجة التحقق'}
                                </div>
                                <p className="text-sm text-gray-700">{vRes.reason || vRes.summary}</p>
                              </div>
                              
                              {vRes.evidence && vRes.evidence.length > 0 && (
                                <div className="mt-3 bg-white p-3 rounded-lg border border-gray-200">
                                  <span className="text-xs font-bold text-bayyinah-deep-emerald mb-1 block flex items-center gap-1">
                                    <Search className="w-3 h-3" /> الدليل المسترجع
                                  </span>
                                  <p className="text-sm text-gray-600 line-clamp-3">"{vRes.evidence[0].excerpt}"</p>
                                  <div className="mt-2 text-xs text-gray-400 flex items-center gap-1">
                                    المصدر: {vRes.evidence[0].source_name} 
                                    {vRes.evidence[0].url && <a href={vRes.evidence[0].url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline mx-1">رابط</a>}
                                  </div>
                                </div>
                              )}
                            </div>
                          ) : (
                            <div className="flex items-center gap-2 text-sm text-amber-600 bg-amber-50 p-3 rounded-lg">
                              <AlertCircle className="w-4 h-4" />
                              <span>لم يتم التحقق من هذا الادعاء أو جاري التحقق...</span>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          );
        })}
      </div>
    </div>
  );
};
