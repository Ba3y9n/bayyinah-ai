import React from 'react';
import { CheckCircle2, AlertTriangle, HelpCircle, XCircle, UserCheck, AlertOctagon } from 'lucide-react';
import { VerificationStatusType, StatusSlug } from '../types';

interface ResultBadgeProps {
  status: VerificationStatusType | string;
  statusSlug?: StatusSlug | string;
  size?: 'sm' | 'md' | 'lg';
  showIcon?: boolean;
}

export const ResultBadge: React.FC<ResultBadgeProps> = ({
  status,
  statusSlug,
  size = 'md',
  showIcon = true
}) => {
  // Determine color theme based on status
  let bgClass = 'bg-bayyinah-off-white text-bayyinah-navy border-bayyinah-gray-300';
  let icon = <HelpCircle className="w-4 h-4" />;
  let dotClass = 'bg-bayyinah-purple';

  if (status.includes('ثابت') || statusSlug === 'verified_authentic') {
    bgClass = 'bg-emerald-50 text-emerald-800 border-emerald-200';
    icon = <CheckCircle2 className="w-4 h-4 text-emerald-600" />;
    dotClass = 'bg-emerald-500';
  } else if (status.includes('موضوع') || status.includes('مكذوب') || statusSlug === 'fabricated_per_source') {
    bgClass = 'bg-rose-50 text-rose-800 border-rose-200';
    icon = <XCircle className="w-4 h-4 text-rose-600" />;
    dotClass = 'bg-rose-500';
  } else if (status.includes('ضعيف') || statusSlug === 'weak_per_source') {
    bgClass = 'bg-amber-50 text-amber-800 border-amber-200';
    icon = <AlertTriangle className="w-4 h-4 text-amber-600" />;
    dotClass = 'bg-amber-500';
  } else if (status.includes('لم يثبت') || statusSlug === 'unverified_wording') {
    bgClass = 'bg-orange-50 text-orange-800 border-orange-200';
    icon = <AlertOctagon className="w-4 h-4 text-orange-600" />;
    dotClass = 'bg-orange-500';
  } else if (status.includes('اختلاف') || statusSlug === 'scholarly_disagreement') {
    bgClass = 'bg-indigo-50 text-indigo-800 border-indigo-200';
    icon = <HelpCircle className="w-4 h-4 text-indigo-600" />;
    dotClass = 'bg-indigo-500';
  } else if (status.includes('مختص') || statusSlug === 'needs_specialist') {
    bgClass = 'bg-purple-50 text-purple-800 border-purple-200';
    icon = <UserCheck className="w-4 h-4 text-purple-600" />;
    dotClass = 'bg-purple-500';
  } else if (status.includes('كافي') || statusSlug === 'insufficient_evidence') {
    bgClass = 'bg-slate-100 text-slate-700 border-slate-300';
    icon = <HelpCircle className="w-4 h-4 text-slate-500" />;
    dotClass = 'bg-slate-400';
  }

  const sizeClasses = {
    sm: 'text-xs px-2.5 py-1 gap-1.5',
    md: 'text-sm px-3.5 py-1.5 gap-2',
    lg: 'text-base px-5 py-2.5 gap-2.5 font-semibold'
  };

  return (
    <span className={`inline-flex items-center rounded-full border font-medium ${sizeClasses[size]} ${bgClass} transition-colors`}>
      {showIcon && <span className="flex-shrink-0">{icon}</span>}
      <span>{status}</span>
    </span>
  );
};
