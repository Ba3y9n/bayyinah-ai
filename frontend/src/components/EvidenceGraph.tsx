import React, { useState } from 'react';
import { 
  Network, 
  ArrowRight, 
  BookOpen, 
  Search, 
  FileText, 
  CheckCircle2, 
  AlertTriangle,
  Info,
  ExternalLink,
  ChevronRight,
  Database
} from 'lucide-react';
import { EvidenceGraphResponse, EvidenceGraphNode } from '../types';

interface EvidenceGraphProps {
  graphData?: EvidenceGraphResponse;
  fallbackClaim?: string;
  fallbackStatus?: string;
}

export const EvidenceGraph: React.FC<EvidenceGraphProps> = ({
  graphData,
  fallbackClaim,
  fallbackStatus
}) => {
  const [selectedNode, setSelectedNode] = useState<EvidenceGraphNode | null>(null);

  if (!graphData || !graphData.nodes || graphData.nodes.length === 0) {
    return (
      <div className="bg-slate-50 border border-slate-200 rounded-2xl p-6 text-center text-xs text-slate-500">
        <Network className="w-8 h-8 text-slate-400 mx-auto mb-2" />
        <p>لا توجد بيانات شبكة أدلة متاحة لهذه الجلسة.</p>
      </div>
    );
  }

  const getNodeBadgeColor = (type: string) => {
    switch (type) {
      case 'INPUT':
        return 'bg-blue-50 text-blue-800 border-blue-200';
      case 'CLAIM':
        return 'bg-amber-50 text-amber-800 border-amber-200';
      case 'SOURCE':
        return 'bg-emerald-50 text-emerald-800 border-emerald-200';
      case 'EVIDENCE':
        return 'bg-purple-50 text-purple-800 border-purple-200';
      case 'RESULT':
        return 'bg-emerald-100 text-emerald-900 border-emerald-300 font-bold';
      default:
        return 'bg-slate-100 text-slate-800 border-slate-200';
    }
  };

  const getNodeTypeLabel = (type: string) => {
    switch (type) {
      case 'INPUT': return 'مدخل';
      case 'CLAIM': return 'ادعاء';
      case 'SOURCE': return 'مصدر';
      case 'EVIDENCE': return 'دليل';
      case 'RESULT': return 'نتيجة';
      default: return type;
    }
  };

  return (
    <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-xs space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-xl bg-bayyinah-purple-light/60 flex items-center justify-center text-bayyinah-purple">
            <Network className="w-5 h-5" />
          </div>
          <div>
            <h4 className="text-sm font-bold text-bayyinah-navy">شبكة الأدلة والاستدلال (Evidence Graph)</h4>
            <span className="text-[11px] text-slate-500">
              رسم بياني يربط المدخل بالادعاء والمصادر المعتمدة ومقتطفات الأدلة والنتيجة
            </span>
          </div>
        </div>
        <span className="text-[11px] font-mono bg-slate-50 text-slate-600 px-3 py-1 rounded-full border border-slate-200">
          {graphData.nodes.length} عقد • {graphData.edges.length} علاقات
        </span>
      </div>

      {/* Visual Pipeline Layout */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-start">
        {/* Step 1: Input & Claim */}
        <div className="space-y-3">
          <span className="text-[11px] font-bold text-slate-400 block uppercase tracking-wide">
            1. المدخل والادعاء
          </span>
          {graphData.nodes.filter(n => n.type === 'INPUT' || n.type === 'CLAIM').map(node => (
            <button
              key={node.id}
              onClick={() => setSelectedNode(node)}
              className={`w-full text-right p-3.5 rounded-2xl border transition-all text-xs space-y-1.5 ${
                selectedNode?.id === node.id 
                  ? 'border-bayyinah-purple ring-2 ring-bayyinah-purple/20 bg-purple-50/30' 
                  : 'border-slate-200 hover:border-bayyinah-purple/40 bg-slate-50/70'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className={`text-[10px] px-2 py-0.5 rounded-full border ${getNodeBadgeColor(node.type)}`}>
                  {getNodeTypeLabel(node.type)}
                </span>
              </div>
              <p className="font-semibold text-bayyinah-navy line-clamp-2">
                {node.metadata?.text || node.metadata?.claim || node.label}
              </p>
            </button>
          ))}
        </div>

        {/* Step 2: Sources */}
        <div className="space-y-3">
          <span className="text-[11px] font-bold text-slate-400 block uppercase tracking-wide">
            2. المصادر المعتمدة
          </span>
          {graphData.nodes.filter(n => n.type === 'SOURCE').map(node => (
            <button
              key={node.id}
              onClick={() => setSelectedNode(node)}
              className={`w-full text-right p-3.5 rounded-2xl border transition-all text-xs space-y-1.5 ${
                selectedNode?.id === node.id 
                  ? 'border-emerald-600 ring-2 ring-emerald-600/20 bg-emerald-50/30' 
                  : 'border-slate-200 hover:border-emerald-600/40 bg-slate-50/70'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className={`text-[10px] px-2 py-0.5 rounded-full border ${getNodeBadgeColor(node.type)}`}>
                  {getNodeTypeLabel(node.type)}
                </span>
                <BookOpen className="w-3.5 h-3.5 text-emerald-700" />
              </div>
              <p className="font-semibold text-bayyinah-navy truncate">
                {node.label}
              </p>
            </button>
          ))}
        </div>

        {/* Step 3: Evidence Chunks */}
        <div className="space-y-3">
          <span className="text-[11px] font-bold text-slate-400 block uppercase tracking-wide">
            3. مقتطفات الأدلة
          </span>
          {graphData.nodes.filter(n => n.type === 'EVIDENCE').map(node => (
            <button
              key={node.id}
              onClick={() => setSelectedNode(node)}
              className={`w-full text-right p-3.5 rounded-2xl border transition-all text-xs space-y-1.5 ${
                selectedNode?.id === node.id 
                  ? 'border-purple-600 ring-2 ring-purple-600/20 bg-purple-50/30' 
                  : 'border-slate-200 hover:border-purple-600/40 bg-slate-50/70'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className={`text-[10px] px-2 py-0.5 rounded-full border ${getNodeBadgeColor(node.type)}`}>
                  {getNodeTypeLabel(node.type)}
                </span>
                {node.metadata?.score && (
                  <span className="text-[10px] font-mono font-semibold text-purple-700">
                    {Math.round(node.metadata.score * 100)}% تطابق
                  </span>
                )}
              </div>
              <p className="font-semibold text-bayyinah-navy text-[11px] line-clamp-2">
                {node.metadata?.excerpt || node.label}
              </p>
            </button>
          ))}
        </div>

        {/* Step 4: Result */}
        <div className="space-y-3">
          <span className="text-[11px] font-bold text-slate-400 block uppercase tracking-wide">
            4. النتيجة المعتمدة
          </span>
          {graphData.nodes.filter(n => n.type === 'RESULT').map(node => (
            <button
              key={node.id}
              onClick={() => setSelectedNode(node)}
              className={`w-full text-right p-4 rounded-2xl border transition-all text-xs space-y-2 ${
                selectedNode?.id === node.id 
                  ? 'border-emerald-700 ring-2 ring-emerald-700/20 bg-emerald-50' 
                  : 'border-emerald-300 bg-emerald-50/70'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-800 text-white font-bold">
                  الحكم النهائي
                </span>
                <CheckCircle2 className="w-4 h-4 text-emerald-800" />
              </div>
              <p className="font-bold text-emerald-950 text-sm">
                {node.label}
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* Node Inspector Drawer */}
      {selectedNode && (
        <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 text-xs space-y-2 animate-fadeIn">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200">
            <span className="font-bold text-slate-800 flex items-center gap-1.5">
              <Info className="w-4 h-4 text-bayyinah-purple" />
              تفاصيل العقدة: [{selectedNode.label}]
            </span>
            <button
              onClick={() => setSelectedNode(null)}
              className="text-slate-400 hover:text-slate-700"
            >
              إغلاق
            </button>
          </div>
          <div className="space-y-1 text-slate-700 leading-relaxed">
            {selectedNode.metadata?.claim && (
              <p><strong>الادعاء: </strong>{selectedNode.metadata.claim}</p>
            )}
            {selectedNode.metadata?.excerpt && (
              <p><strong>نص الدليل: </strong>«{selectedNode.metadata.excerpt}»</p>
            )}
            {selectedNode.metadata?.reference && (
              <p><strong>التخريج: </strong>{selectedNode.metadata.reference}</p>
            )}
            {selectedNode.metadata?.grade && (
              <p><strong>الحكم والدرجة: </strong>{selectedNode.metadata.grade}</p>
            )}
            {selectedNode.metadata?.url && (
              <a
                href={selectedNode.metadata.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-bayyinah-purple hover:underline inline-flex items-center gap-1 pt-1"
              >
                <span>رابط المصدر</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
