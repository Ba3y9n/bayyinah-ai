import React, { useRef, useState } from 'react';
import { Download, Share2, Copy, Check, ExternalLink, ShieldCheck } from 'lucide-react';
import { toPng } from 'html-to-image';
import { ShareCardData } from '../types';
import { ResultBadge } from './ResultBadge';

interface ShareCardProps {
  data: ShareCardData;
}

export const ShareCard: React.FC<ShareCardProps> = ({ data }) => {
  const cardRef = useRef<HTMLDivElement>(null);
  const [copied, setCopied] = useState(false);
  const [downloading, setDownloading] = useState(false);

  const handleCopyText = () => {
    const text = `🔍 بطاقة تحقق بيّنة AI
📌 الادعاء: ${data.claim}
🏷️ النتيجة: ${data.status}
📖 الدليل: ${data.evidence_excerpt}
📚 المصدر: ${data.source_name} (${data.reference})
🔗 الرابط: ${data.source_url}
—
بيّنة AI: ${data.slogan}`;

    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  const handleDownloadImage = async () => {
    if (!cardRef.current) return;
    try {
      setDownloading(true);
      const dataUrl = await toPng(cardRef.current, {
        cacheBust: true,
        quality: 0.95,
        pixelRatio: 2
      });
      const link = document.createElement('a');
      link.download = `bayyinah-verification-${Date.now()}.png`;
      link.href = dataUrl;
      link.click();
    } catch (err) {
      console.error('Failed to generate image:', err);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* Visual Rendered Card for Export & Sharing */}
      <div
        ref={cardRef}
        className="w-full bg-bayyinah-navy text-white rounded-3xl p-6 md:p-8 shadow-xl border border-bayyinah-purple/30 relative overflow-hidden font-sans"
        dir="rtl"
      >
        {/* Ambient background decoration */}
        <div className="absolute -left-20 -top-20 w-64 h-64 rounded-full bg-bayyinah-purple/20 blur-3xl pointer-events-none" />
        <div className="absolute -right-20 -bottom-20 w-64 h-64 rounded-full bg-bayyinah-turquoise/15 blur-3xl pointer-events-none" />

        {/* Header: Brand & Slogan */}
        <div className="flex items-center justify-between pb-5 border-b border-white/10 relative z-10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-bayyinah-purple to-bayyinah-navy-light flex items-center justify-center border border-bayyinah-turquoise/40">
              <ShieldCheck className="w-6 h-6 text-bayyinah-turquoise" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-lg font-bold text-white tracking-wide">بيّنة AI</span>
                <span className="text-[10px] font-semibold bg-bayyinah-turquoise/15 text-bayyinah-turquoise px-2 py-0.5 rounded-full border border-bayyinah-turquoise/30">
                  توثيق معرفي
                </span>
              </div>
              <span className="text-xs text-bayyinah-off-white/70 block mt-0.5">تحقّق قبل أن تنشر.</span>
            </div>
          </div>

          <div className="text-left" dir="ltr">
            <span className="text-[11px] text-white/50">{data.verified_at}</span>
          </div>
        </div>

        {/* Verification Status Banner */}
        <div className="my-5 relative z-10">
          <div className="inline-block">
            <ResultBadge status={data.status} statusSlug={data.status_slug} size="lg" />
          </div>
        </div>

        {/* Extracted Claim */}
        <div className="bg-white/5 border border-white/10 rounded-2xl p-4 mb-4 relative z-10">
          <span className="text-[11px] font-semibold text-bayyinah-turquoise block mb-1">الادعاء الذي تم فحصه:</span>
          <p className="text-sm md:text-base font-medium text-white/95 leading-relaxed">
            «{data.claim}»
          </p>
        </div>

        {/* Retrieved Evidence Excerpt */}
        <div className="bg-white/5 border border-white/10 rounded-2xl p-4 mb-4 relative z-10">
          <span className="text-[11px] font-semibold text-bayyinah-off-white/70 block mb-1">الدليل المسترجع من المصدر:</span>
          <p className="text-xs md:text-sm text-bayyinah-off-white/90 leading-relaxed italic">
            {data.evidence_excerpt}
          </p>
        </div>

        {/* Source & Reference Meta */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-3 border-t border-white/10 text-xs text-white/80 relative z-10">
          <div>
            <span className="text-white/50 block text-[11px]">المصدر المعتمد:</span>
            <span className="font-semibold text-bayyinah-turquoise">{data.source_name}</span>
          </div>
          <div>
            <span className="text-white/50 block text-[11px]">المرجع الموثق:</span>
            <span className="font-medium text-white/90 truncate block">{data.reference}</span>
          </div>
        </div>

        {/* Footer Link & Verification Pledge */}
        <div className="mt-5 pt-3 border-t border-white/10 flex items-center justify-between text-[11px] text-white/60 relative z-10">
          <div className="flex items-center gap-1.5 text-bayyinah-turquoise/90">
            <ExternalLink className="w-3.5 h-3.5" />
            <span>{data.source_url}</span>
          </div>
          <span className="font-semibold text-bayyinah-off-white/80">Bayyinah AI Platform</span>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-wrap items-center gap-3">
        <button
          onClick={handleDownloadImage}
          disabled={downloading}
          className="flex-1 min-w-[160px] inline-flex items-center justify-center gap-2 bg-bayyinah-purple hover:bg-bayyinah-purple-hover text-white text-sm font-medium py-3 px-5 rounded-xl transition-all shadow-subtle disabled:opacity-50"
        >
          <Download className="w-4 h-4" />
          <span>{downloading ? 'جاري إنشاء البطاقة...' : 'تحميل بطاقة بيّنة (PNG)'}</span>
        </button>

        <button
          onClick={handleCopyText}
          className="inline-flex items-center justify-center gap-2 bg-white hover:bg-bayyinah-off-white text-bayyinah-navy border border-bayyinah-gray-300 text-sm font-medium py-3 px-5 rounded-xl transition-all shadow-subtle"
        >
          {copied ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4" />}
          <span>{copied ? 'تم نسخ بيانات البطاقة' : 'نسخ نص البطاقة'}</span>
        </button>
      </div>
    </div>
  );
};
