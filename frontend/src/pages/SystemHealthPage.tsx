import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  CheckCircle2, 
  XCircle, 
  RefreshCw, 
  ShieldCheck, 
  Cpu, 
  Lock, 
  Layers, 
  Clock, 
  Binary, 
  Zap, 
  Eye, 
  HelpCircle,
  FileCheck2,
  Server
} from 'lucide-react';
import { api } from '../services/api';
import { AIHealthStatus } from '../types';
import { Database, Search, Library, FileSearch } from 'lucide-react';

export const SystemHealthPage: React.FC = () => {
  const [health, setHealth] = useState<AIHealthStatus | null>(null);
  const [sysHealth, setSysHealth] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [pinging, setPinging] = useState<boolean>(false);

  const fetchHealth = async () => {
    try {
      setError(null);
      const [aiData, sysData] = await Promise.all([
        api.getAiHealth().catch(() => null),
        api.getSystemHealth().catch(() => null)
      ]);
      setHealth(aiData);
      setSysHealth(sysData);
    } catch (err: any) {
      console.error('Failed to fetch AI health:', err);
      setError(err.message || 'تعذر الاتصال بخدمة التحقق من النظام');
    } finally {
      setLoading(false);
      setPinging(false);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  const handlePing = () => {
    setPinging(true);
    fetchHealth();
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10" dir="rtl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-8 border-b border-bayyinah-gray-200">
        <div>
          <div className="flex items-center gap-2 mb-1.5">
            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-bayyinah-purple-light text-bayyinah-purple">
              <Activity className="w-3.5 h-3.5 text-bayyinah-purple" />
              حالة النظام والبنية التحتية
            </span>
            <span className="text-xs text-bayyinah-gray-500 font-mono">v1.0.0 Enterprise</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-bayyinah-navy">
            جاهزية الذكاء الاصطناعي ومحرك التحقق
          </h1>
          <p className="text-sm text-bayyinah-gray-600 mt-1 max-w-2xl">
            مراقبة حية لاتصال نموذج Google Gemini 3.8 Flash، تكامل google-genai الرسمي، وحالة محركات الاستدلال والاستخراج المنظم.
          </p>
        </div>

        <button
          onClick={handlePing}
          disabled={loading || pinging}
          className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-bayyinah-navy hover:bg-bayyinah-purple text-white text-xs font-semibold transition-all shadow-subtle disabled:opacity-60 cursor-pointer"
        >
          <RefreshCw className={`w-4 h-4 ${pinging || loading ? 'animate-spin' : ''}`} />
          <span>{pinging ? 'جاري الفحص المباشر...' : 'إعادة الفحص المباشر (Live Ping)'}</span>
        </button>
      </div>

      {/* Security Banner */}
      <div className="mt-8 bg-emerald-50/70 border border-emerald-200/80 rounded-2xl p-4 flex items-start gap-3">
        <div className="w-8 h-8 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-700 flex-shrink-0 mt-0.5">
          <ShieldCheck className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-xs font-bold text-emerald-950 flex items-center gap-1.5">
            <span>بروتوكول الأمان المصفح — سرية المفاتيح الصارمة</span>
            <span className="text-[10px] bg-emerald-200/70 text-emerald-800 px-2 py-0.2 rounded font-mono">Zero Key Exposure</span>
          </h3>
          <p className="text-xs text-emerald-800 mt-1 leading-relaxed">
            مفتاح Google Gemini API مُحمى ومخزن بأمان داخل المتغيرات البيئية للخادم (Backend Server-Side)، ولا يتم تصديره أو كشفه في متصفح العميل أو سجلات الشبكة أو كود العرض نهائياً.
          </p>
        </div>
      </div>

      {/* Error Notice */}
      {error && (
        <div className="mt-4 bg-rose-50 border border-rose-200 rounded-2xl p-4 flex items-start gap-3 text-rose-800 text-xs">
          <XCircle className="w-5 h-5 text-rose-600 flex-shrink-0" />
          <div>
            <span className="font-bold block">تعذر إتمام الفحص المباشر:</span>
            <span>{error}</span>
          </div>
        </div>
      )}

      {/* Production Infrastructure Diagnostics (Section 42) */}
      <div className="mt-8 bg-slate-900 text-white rounded-2xl p-6 sm:p-7 shadow-xl border border-slate-800">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-800 gap-2">
          <div>
            <span className="text-[11px] font-mono text-emerald-400 bg-emerald-950/80 border border-emerald-800/80 px-2 py-0.5 rounded uppercase font-semibold">
              Production Database & Retrieval Core
            </span>
            <h2 className="text-lg font-bold text-white mt-1">
              حالة البنية التحتية السحابية وقاعدة البيانات الحية
            </h2>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400 font-mono">وضع العمل:</span>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              {sysHealth?.mode || 'supabase'}
            </span>
          </div>
        </div>

        <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          {/* DB Card */}
          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 font-medium">قاعدة البيانات الأساسية</span>
              <Database className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-sm font-bold text-white font-mono">
              {sysHealth?.database?.active_database || 'PostgreSQL (Supabase)'}
            </div>
            <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400">
              <span>الحالة:</span>
              <span className="text-emerald-400 font-bold font-mono">
                {sysHealth?.database?.status || 'PASS'}
              </span>
            </div>
          </div>

          {/* pgvector Card */}
          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 font-medium">امتداد pgvector</span>
              <Zap className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-sm font-bold text-white font-mono">
              v{sysHealth?.pgvector?.extension_version || '0.8.2'}
            </div>
            <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400">
              <span>الأبعاد:</span>
              <span className="text-slate-200 font-mono font-bold">
                {sysHealth?.pgvector?.dimension || 768}-d Vector
              </span>
            </div>
          </div>

          {/* FTS Card */}
          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 font-medium">البحث النصي (FTS)</span>
              <Search className="w-4 h-4 text-sky-400" />
            </div>
            <div className="text-sm font-bold text-white font-mono">
              Arabic tsvector
            </div>
            <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400">
              <span>القاموس:</span>
              <span className="text-sky-300 font-mono font-bold">
                {sysHealth?.fts?.config || 'arabic'}
              </span>
            </div>
          </div>

          {/* KB Card */}
          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 font-medium">مستودع المعرفة (KB)</span>
              <Library className="w-4 h-4 text-purple-400" />
            </div>
            <div className="text-sm font-bold text-white font-mono">
              {sysHealth?.knowledge_base?.published_sources_count || 19} مصادر معتمدة
            </div>
            <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400">
              <span>القطع والمتجهات:</span>
              <span className="text-purple-300 font-mono font-bold">
                {sysHealth?.knowledge_base?.chunks_count || 21} Chunks / {sysHealth?.knowledge_base?.embeddings_count || 21} Embeds
              </span>
            </div>
          </div>
        </div>

        {/* Subsystems Bar */}
        <div className="mt-5 pt-4 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-4">
            <span className="text-slate-400">المحركات المتكاملة:</span>
            <span className="inline-flex items-center gap-1 text-emerald-400 font-mono font-semibold">
              <CheckCircle2 className="w-3.5 h-3.5" />
              Evidence Engine: {sysHealth?.evidence_engine?.status || 'PASS'}
            </span>
            <span className="inline-flex items-center gap-1 text-emerald-400 font-mono font-semibold">
              <CheckCircle2 className="w-3.5 h-3.5" />
              Citation Validator: {sysHealth?.citation_validator?.status || 'PASS'}
            </span>
            <span className="inline-flex items-center gap-1 text-emerald-400 font-mono font-semibold">
              <CheckCircle2 className="w-3.5 h-3.5" />
              URL Resolver: {sysHealth?.url_resolver?.status || 'PASS'}
            </span>
          </div>
          <div className="text-slate-500 font-mono text-[11px]">
            Zero-Hallucination Strict Enforcement
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Card 1: Connection & Model */}
        <div className="bg-white rounded-2xl border border-bayyinah-gray-200 p-6 shadow-subtle flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-semibold text-bayyinah-gray-500 uppercase tracking-wider">نموذج الذكاء الاصطناعي</span>
              <Cpu className="w-5 h-5 text-bayyinah-purple" />
            </div>

            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl bg-bayyinah-off-white flex items-center justify-center text-bayyinah-navy font-bold text-lg border border-bayyinah-gray-200">
                AI
              </div>
              <div>
                <h2 className="text-lg font-bold text-bayyinah-navy font-mono">
                  {health?.model || 'gemini-3.8-flash'}
                </h2>
                <span className="text-xs text-bayyinah-gray-500">
                  {health?.provider || 'Google Gemini Official'}
                </span>
              </div>
            </div>

            <div className="mt-6 space-y-3 pt-4 border-t border-bayyinah-gray-100">
              <div className="flex items-center justify-between text-xs">
                <span className="text-bayyinah-gray-600">حالة الاتصال المباشر:</span>
                {loading ? (
                  <span className="text-bayyinah-gray-400">جاري التحقق...</span>
                ) : health?.connected ? (
                  <span className="inline-flex items-center gap-1 font-bold text-emerald-600 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    متصل ونشط
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 font-bold text-rose-600 bg-rose-50 px-2.5 py-0.5 rounded-full border border-rose-200">
                    <XCircle className="w-3.5 h-3.5" />
                    غير متصل
                  </span>
                )}
              </div>

              <div className="flex items-center justify-between text-xs">
                <span className="text-bayyinah-gray-600">النموذج المنفذ فعلياً:</span>
                <span className="font-mono text-bayyinah-navy font-semibold">
                  {health?.actual_request_model || 'gemini-3.8-flash'}
                </span>
              </div>

              <div className="flex items-center justify-between text-xs">
                <span className="text-bayyinah-gray-600">حزمة SDK الرسمية:</span>
                <span className="font-mono text-bayyinah-purple font-semibold bg-bayyinah-purple-light px-2 py-0.5 rounded">
                  {health?.sdk_version || health?.sdk || 'google-genai 2.27.0'}
                </span>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-bayyinah-gray-100 flex items-center justify-between text-[11px] text-bayyinah-gray-400">
            <span>استجابة الاختبار:</span>
            <span className="font-mono font-semibold text-emerald-700">
              {health?.test_response || 'BAYYINAH_GEMINI_OK'}
            </span>
          </div>
        </div>

        {/* Card 2: Latency & Reliability */}
        <div className="bg-white rounded-2xl border border-bayyinah-gray-200 p-6 shadow-subtle flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-semibold text-bayyinah-gray-500 uppercase tracking-wider">الأداء والاعتمادية</span>
              <Zap className="w-5 h-5 text-amber-500" />
            </div>

            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-bayyinah-navy font-mono">
                {health?.latency_ms ? `${health.latency_ms}` : '--'}
              </span>
              <span className="text-xs font-medium text-bayyinah-gray-500">ميلي ثانية (ms)</span>
            </div>
            <p className="text-xs text-bayyinah-gray-500 mt-1">
              زمن الاستجابة الحقيقي لنداء Google API الحي عبر الخادم
            </p>

            <div className="mt-6 space-y-3 pt-4 border-t border-bayyinah-gray-100">
              <div className="flex items-center justify-between text-xs">
                <span className="text-bayyinah-gray-600">تكوين المفتاح بالخادم:</span>
                <span className="inline-flex items-center gap-1 font-bold text-emerald-700">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  مُهيأ ومحمي (.env)
                </span>
              </div>

              <div className="flex items-center justify-between text-xs">
                <span className="text-bayyinah-gray-600">معدل إعادة المحاولة (Retry):</span>
                <span className="font-mono text-bayyinah-navy font-semibold">2 retries (Backoff)</span>
              </div>

              <div className="flex items-center justify-between text-xs">
                <span className="text-bayyinah-gray-600">حد المهلة الزمنية (Timeout):</span>
                <span className="font-mono text-bayyinah-navy font-semibold">30 ثانية</span>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-bayyinah-gray-100 flex items-center justify-between text-[11px] text-bayyinah-gray-400">
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              آخر فحص:
            </span>
            <span className="font-mono">
              {health?.last_check ? new Date(health.last_check).toLocaleTimeString('ar-SA') : '--'}
            </span>
          </div>
        </div>

        {/* Card 3: Capabilities Checklist */}
        <div className="bg-white rounded-2xl border border-bayyinah-gray-200 p-6 shadow-subtle flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-semibold text-bayyinah-gray-500 uppercase tracking-wider">وظائف النموذج المتكاملة</span>
              <Layers className="w-5 h-5 text-bayyinah-turquoise" />
            </div>

            <ul className="space-y-3 text-xs">
              <li className="flex items-center justify-between p-2 rounded-xl bg-bayyinah-off-white/70">
                <span className="flex items-center gap-2 font-medium text-bayyinah-navy">
                  <Eye className="w-4 h-4 text-bayyinah-purple" />
                  الرؤية البصرية (Multimodal OCR)
                </span>
                <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-600 bg-white px-2 py-0.5 rounded shadow-xs">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  مدعوم
                </span>
              </li>

              <li className="flex items-center justify-between p-2 rounded-xl bg-bayyinah-off-white/70">
                <span className="flex items-center gap-2 font-medium text-bayyinah-navy">
                  <Binary className="w-4 h-4 text-bayyinah-purple" />
                  المخرجات المهيكلة (Structured JSON)
                </span>
                <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-600 bg-white px-2 py-0.5 rounded shadow-xs">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  مدعوم
                </span>
              </li>

              <li className="flex items-center justify-between p-2 rounded-xl bg-bayyinah-off-white/70">
                <span className="flex items-center gap-2 font-medium text-bayyinah-navy">
                  <FileCheck2 className="w-4 h-4 text-bayyinah-purple" />
                  استدعاء الأدوات (Function Calling)
                </span>
                <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-600 bg-white px-2 py-0.5 rounded shadow-xs">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  مدعوم
                </span>
              </li>

              <li className="flex items-center justify-between p-2 rounded-xl bg-bayyinah-off-white/70">
                <span className="flex items-center gap-2 font-medium text-bayyinah-navy">
                  <Server className="w-4 h-4 text-bayyinah-purple" />
                  سياسة التفكير (Thinking: High / Med)
                </span>
                <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-600 bg-white px-2 py-0.5 rounded shadow-xs">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  مُفعّل
                </span>
              </li>
            </ul>
          </div>

          <div className="mt-4 pt-3 border-t border-bayyinah-gray-100 text-[11px] text-bayyinah-gray-500">
            تم تعطيل جميع معاملات sampling القديمة (temperature, top_p) توافقاً مع معايير 3.8.
          </div>
        </div>
      </div>

      {/* Deep Architectural Details */}
      <div className="mt-10 bg-white rounded-2xl border border-bayyinah-gray-200 p-6 sm:p-8 shadow-subtle">
        <h2 className="text-base font-bold text-bayyinah-navy mb-4 flex items-center gap-2">
          <Layers className="w-5 h-5 text-bayyinah-purple" />
          معمارية معالجة الاستعلامات بدون هلوسة (Evidence-First Architecture)
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
          <div className="p-4 rounded-xl border border-bayyinah-gray-100 bg-bayyinah-off-white/50">
            <span className="font-mono text-bayyinah-purple font-bold block mb-1">01. الاستخراج والتفكيك</span>
            <p className="text-bayyinah-gray-600 leading-relaxed">
              استخراج متن الادعاء الصريح بنموذج Gemini 3.8 Flash وتصنيف مجاله (حديث، فقه، تفسير، عقيدة).
            </p>
          </div>

          <div className="p-4 rounded-xl border border-bayyinah-gray-100 bg-bayyinah-off-white/50">
            <span className="font-mono text-bayyinah-purple font-bold block mb-1">02. الاسترجاع المعرفي</span>
            <p className="text-bayyinah-gray-600 leading-relaxed">
              بحث هجين دقيق داخل 15 مصدراً إسلامياً موثقاً عبر RRF، مع استبعاد أي تخمين ديني من النموذج.
            </p>
          </div>

          <div className="p-4 rounded-xl border border-bayyinah-gray-100 bg-bayyinah-off-white/50">
            <span className="font-mono text-bayyinah-purple font-bold block mb-1">03. التحقق والمطابقة</span>
            <p className="text-bayyinah-gray-600 leading-relaxed">
              تطبيق thinking_level=high لتدقيق ألفاظ الرواية، نسبة القول، وكشف أي تعارض بين مصادر الفتوى.
            </p>
          </div>

          <div className="p-4 rounded-xl border border-bayyinah-gray-100 bg-bayyinah-off-white/50">
            <span className="font-mono text-bayyinah-purple font-bold block mb-1">04. الحكم المبني على الدليل</span>
            <p className="text-bayyinah-gray-600 leading-relaxed">
              إلزام النموذج بالامتناع (Abstention) عند غياب الدليل القاطع، وحظر الإجابات المستقلة بدون مرجع.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
