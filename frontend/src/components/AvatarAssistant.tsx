import React from 'react';

interface AvatarAssistantProps {
  state: 'idle' | 'thinking' | 'searching' | 'evidence_found' | 'explaining';
  size?: 'sm' | 'md' | 'lg';
  label?: string;
}

export const AvatarAssistant: React.FC<AvatarAssistantProps> = ({
  state = 'idle',
  size = 'md',
  label
}) => {
  const sizeMap = {
    sm: { container: 'w-8 h-8', svg: 32, dot: 'w-2 h-2' },
    md: { container: 'w-12 h-12', svg: 48, dot: 'w-3 h-3' },
    lg: { container: 'w-16 h-16', svg: 64, dot: 'w-4 h-4' }
  };

  const currentSize = sizeMap[size];

  // Colors & visual pulse based on state
  const getStateConfig = () => {
    switch (state) {
      case 'thinking':
        return {
          ringColor: 'stroke-bayyinah-purple',
          coreColor: 'fill-bayyinah-purple',
          glowClass: 'animate-pulse text-bayyinah-purple',
          text: 'يفكر في الاستفسار...'
        };
      case 'searching':
        return {
          ringColor: 'stroke-bayyinah-turquoise',
          coreColor: 'fill-bayyinah-turquoise',
          glowClass: 'animate-spin text-bayyinah-turquoise',
          text: 'يبحث في الأدلة المعتمدة...'
        };
      case 'evidence_found':
        return {
          ringColor: 'stroke-bayyinah-turquoise',
          coreColor: 'fill-bayyinah-turquoise',
          glowClass: 'text-bayyinah-turquoise',
          text: 'تم استرجاع الدليل'
        };
      case 'explaining':
        return {
          ringColor: 'stroke-bayyinah-purple',
          coreColor: 'fill-bayyinah-purple',
          glowClass: 'animate-bounce text-bayyinah-purple',
          text: 'يشرح النتيجة من الدليل...'
        };
      case 'idle':
      default:
        return {
          ringColor: 'stroke-bayyinah-navy',
          coreColor: 'fill-bayyinah-purple',
          glowClass: 'text-bayyinah-navy',
          text: 'مساعد بيّنة جاهز'
        };
    }
  };

  const config = getStateConfig();

  return (
    <div className="flex items-center gap-2.5">
      <div className={`relative ${currentSize.container} flex items-center justify-center flex-shrink-0`}>
        {/* Outer ambient glow */}
        <div 
          className={`absolute inset-0 rounded-full transition-all duration-500 ${
            state === 'searching' || state === 'evidence_found' 
              ? 'bg-bayyinah-turquoise/20 blur-md' 
              : state === 'thinking' || state === 'explaining' 
                ? 'bg-bayyinah-purple/20 blur-md' 
                : 'bg-bayyinah-navy/5'
          }`}
        />

        {/* Minimal Geometric Scientific SVG Avatar */}
        <svg 
          width={currentSize.svg} 
          height={currentSize.svg} 
          viewBox="0 0 48 48" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
          className={`relative z-10 transition-transform duration-300 ${state === 'searching' ? 'rotate-45' : ''}`}
        >
          {/* Base outer shield / circle */}
          <rect 
            x="4" 
            y="4" 
            width="40" 
            height="40" 
            rx="20" 
            fill="#12183F" 
          />
          
          {/* Dynamic Geometric Rings */}
          <circle 
            cx="24" 
            cy="24" 
            r="15" 
            stroke={state === 'searching' || state === 'evidence_found' ? '#2EF2C2' : '#6150EA'} 
            strokeWidth="2" 
            strokeDasharray={state === 'searching' ? '6 4' : 'none'}
            className={state === 'searching' ? 'animate-spin origin-center' : ''}
          />
          
          {/* Central node / core */}
          <circle 
            cx="24" 
            cy="24" 
            r="5" 
            fill={state === 'searching' || state === 'evidence_found' ? '#2EF2C2' : '#FFFFFF'} 
            className="transition-colors duration-300"
          />

          {/* Verification checkmark or nodes */}
          {state === 'evidence_found' && (
            <path 
              d="M19 24.5L22.5 28L29 20" 
              stroke="#12183F" 
              strokeWidth="2.5" 
              strokeLinecap="round" 
              strokeLinejoin="round" 
            />
          )}

          {/* Wave bars for explaining */}
          {state === 'explaining' && (
            <>
              <line x1="14" y1="24" x2="14" y2="24" stroke="#2EF2C2" strokeWidth="3" strokeLinecap="round" className="animate-pulse" />
              <line x1="34" y1="24" x2="34" y2="24" stroke="#2EF2C2" strokeWidth="3" strokeLinecap="round" className="animate-pulse" />
            </>
          )}
        </svg>
      </div>

      {label !== undefined && (
        <div className="flex flex-col">
          <span className="text-xs font-semibold text-bayyinah-navy">مساعد بيّنة</span>
          <span className="text-[11px] text-bayyinah-gray-500">{label || config.text}</span>
        </div>
      )}
    </div>
  );
};
