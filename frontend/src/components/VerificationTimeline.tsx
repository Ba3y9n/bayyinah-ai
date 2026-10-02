import React, { useState } from 'react';
import { 
  CheckCircle2, 
  ChevronDown, 
  ChevronUp, 
  Search, 
  FileText, 
  Layers, 
  Cpu, 
  ShieldCheck, 
  Database,
  GitBranch,
  HelpCircle,
  Eye
} from 'lucide-react';
import { VerificationStepLog } from '../types';

interface VerificationTimelineProps {
  steps: VerificationStepLog[];
  defaultOpen?: boolean;
}

export const VerificationTimeline: React.FC<VerificationTimelineProps> = ({
  steps,
  defaultOpen = false
}) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const [activeStepData, setActiveStepData] = useState<number | null>(null);

  const getStepIcon = (stepNum: number) => {
    switch (stepNum) {
      case 1:
      case 2:
        return <Eye className="w-4 h-4 text-bayyinah-purple" />;
      case 3:
      case 4:
        return <FileText className="w-4 h-4 text-bayyinah-purple" />;
      case 5:
      case 6:
      case 7:
        return <Search className="w-4 h-4 text-bayyinah-turquoise-dark" />;
      case 8:
      case 9:
        return <Database className="w-4 h-4 text-bayyinah-turquoise-dark" />;
      case 10:
        return <ShieldCheck className="w-4 h-4 text-emerald-600" />;
      case 11:
      case 12:
        return <GitBranch className="w-4 h-4 text-bayyinah-purple" />;
      case 13:
      default:
        return <CheckCircle2 className="w-4 h-4 text-emerald-600" />;
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-bayyinah-gray-200 shadow-subtle overflow-hidden">
      {/* Header Accordion Toggle */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-5 text-right hover:bg-bayyinah-off-white/60 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-bayyinah-purple-light flex items-center justify-center text-bayyinah-purple">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-bayyinah-navy">كيف وصلنا للنتيجة؟</h3>
            <p className="text-xs text-bayyinah-gray-500 mt-0.5">
              مسار الشفافية وسلسلة التحقق الاستدلالية ({steps.length} خطوة موثقة)
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs font-medium text-bayyinah-purple">
          <span>{isOpen ? 'إخفاء التفاصيل' : 'عرض خطوات التحقق'}</span>
          {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </div>
      </button>

      {/* Steps Content */}
      {isOpen && (
        <div className="px-6 pb-6 pt-2 border-t border-bayyinah-gray-100">
          <div className="relative border-r-2 border-bayyinah-purple-light mr-3 space-y-6 pr-6 pt-3">
            {steps.map((step) => {
              const isExpanded = activeStepData === step.step_number;
              const hasData = step.data && Object.keys(step.data).length > 0;

              return (
                <div key={step.step_number} className="relative group">
                  {/* Step Dot / Node */}
                  <div className="absolute -right-[31px] top-0 w-6 h-6 rounded-full bg-white border-2 border-bayyinah-purple flex items-center justify-center shadow-xs">
                    <span className="text-[10px] font-bold text-bayyinah-purple">{step.step_number}</span>
                  </div>

                  {/* Step Content Card */}
                  <div className="bg-bayyinah-off-white/80 rounded-xl p-4 border border-bayyinah-gray-200/70 hover:border-bayyinah-purple/30 transition-all">
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-center gap-2">
                        {getStepIcon(step.step_number)}
                        <h4 className="text-sm font-semibold text-bayyinah-navy">{step.title}</h4>
                      </div>
                      <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">
                        <CheckCircle2 className="w-3 h-3" /> تم بنجاح
                      </span>
                    </div>

                    <p className="text-xs text-bayyinah-gray-600 mt-1.5 leading-relaxed">
                      {step.description}
                    </p>

                    {/* Step Extra Data Inspector */}
                    {hasData && (
                      <div className="mt-2.5">
                        <button
                          onClick={() => setActiveStepData(isExpanded ? null : step.step_number)}
                          className="text-[11px] font-medium text-bayyinah-purple hover:underline inline-flex items-center gap-1"
                        >
                          {isExpanded ? 'إخفاء مخرجات الخطوة' : 'عرض المخرجات البرمجية للخطوة'}
                        </button>

                        {isExpanded && (
                          <div className="mt-2 p-3 bg-bayyinah-navy rounded-lg text-bayyinah-off-white text-[11px] font-mono overflow-x-auto text-left" dir="ltr">
                            <pre>{JSON.stringify(step.data, null, 2)}</pre>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
