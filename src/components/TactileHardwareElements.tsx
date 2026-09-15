import React from 'react';

interface TactileRockerSwitchProps {
  isOn: boolean;
  onToggle: () => void;
  labelLeft?: string;
  labelRight?: string;
  size?: 'sm' | 'md' | 'lg';
  isLight?: boolean;
}

export const TactileRockerSwitch: React.FC<TactileRockerSwitchProps> = ({
  isOn,
  onToggle,
  labelLeft = 'OFF',
  labelRight = 'ON',
  size = 'md',
  isLight = false,
}) => {
  const isSm = size === 'sm';
  return (
    <button
      type="button"
      onClick={onToggle}
      className={`relative inline-flex items-center rounded-full transition-all duration-300 cursor-pointer select-none p-1 ${
        isSm ? 'w-16 h-7' : 'w-20 h-9'
      } ${
        isLight ? 'hardware-well-light' : 'hardware-well-dark'
      }`}
      title={`Toggle: ${isOn ? labelRight : labelLeft}`}
    >
      {/* Debossed Labels */}
      <div className="absolute inset-0 flex items-center justify-between px-2 text-[9px] font-mono font-black pointer-events-none tracking-tighter">
        <span className={`transition-opacity duration-200 ${
          !isOn ? (isLight ? 'text-slate-900 font-bold opacity-100' : 'text-zinc-200 font-bold opacity-100') : 'opacity-35 text-zinc-500'
        }`}>
          {labelLeft}
        </span>
        <span className={`transition-opacity duration-200 ${
          isOn ? (isLight ? 'text-orange-600 font-bold opacity-100' : 'text-orange-400 font-bold opacity-100') : 'opacity-35 text-zinc-500'
        }`}>
          {labelRight}
        </span>
      </div>

      {/* Floating Rocker Pill Thumb */}
      <div
        className={`relative z-10 rounded-full transition-transform duration-300 ease-out flex items-center justify-center shadow-md ${
          isSm ? 'w-6 h-5' : 'w-8 h-7'
        } ${
          isLight
            ? 'bg-gradient-to-b from-white via-slate-100 to-slate-200 border border-white/90 shadow-slate-900/20'
            : 'bg-gradient-to-b from-zinc-200 via-zinc-400 to-zinc-600 border border-white/40 shadow-black/80'
        } ${
          isOn
            ? isSm ? 'translate-x-8' : 'translate-x-10'
            : 'translate-x-0'
        }`}
      >
        {/* Subtle Pill Center Slit / Pip */}
        <div className={`w-0.5 h-3 rounded-full transition-colors ${
          isOn
            ? 'bg-orange-500 shadow-[0_0_4px_rgba(230,57,70,0.9)]'
            : isLight ? 'bg-slate-400' : 'bg-zinc-600'
        }`} />
      </div>
    </button>
  );
};

interface TactileRotaryKnobProps {
  value: number; // 0 to 100
  onChange?: (val: number) => void;
  size?: number;
  label?: string;
  minLabel?: string;
  maxLabel?: string;
  isLight?: boolean;
}

export const TactileRotaryKnob: React.FC<TactileRotaryKnobProps> = ({
  value,
  onChange,
  size = 64,
  label,
  minLabel = 'MIN',
  maxLabel = 'MAX',
  isLight = false,
}) => {
  // Map 0-100 value to -135deg to +135deg rotation
  const rotationDeg = -135 + (value / 100) * 270;

  return (
    <div className="flex flex-col items-center select-none">
      {/* Outer Halo Lighting & Housing */}
      <div
        className={`relative rounded-full flex items-center justify-center transition-all ${
          isLight ? 'master-rotary-housing-light' : 'master-rotary-housing-dark'
        }`}
        style={{ width: size, height: size }}
      >
        {/* Optical Glow Halo Ring */}
        <div
          className="absolute inset-[-4px] rounded-full pointer-events-none opacity-40 transition-opacity"
          style={{
            background: isLight
              ? `radial-gradient(circle, rgba(230,57,70,0.2) 0%, transparent 70%)`
              : `radial-gradient(circle, rgba(230,57,70,0.35) 0%, transparent 70%)`
          }}
        />

        {/* Rotary Dial Top Face with Conic Brushed Texture */}
        <div
          className={`w-[82%] h-[82%] rounded-full relative transition-transform duration-200 cursor-pointer flex items-center justify-center ${
            isLight ? 'analog-rotary-dial-light' : 'analog-rotary-dial-dark'
          }`}
          style={{ transform: `rotate(${rotationDeg}deg)` }}
          onClick={() => {
            if (onChange) {
              const next = (value + 20) % 120;
              onChange(next > 100 ? 0 : next);
            }
          }}
        >
          {/* Vertical Precision Pointer Notch Slit */}
          <div className="absolute top-1.5 w-1 h-3 rounded-full bg-orange-500 shadow-[0_0_6px_rgba(230,57,70,1)]" />

          {/* Center Concave Bevel */}
          <div className={`w-3.5 h-3.5 rounded-full ${
            isLight
              ? 'bg-gradient-to-b from-slate-300 to-slate-100 shadow-inner'
              : 'bg-gradient-to-b from-zinc-900 to-zinc-800 shadow-inner'
          }`} />
        </div>
      </div>

      {/* Min/Max Ticks & Label */}
      {(minLabel || maxLabel || label) && (
        <div className="flex items-center justify-between w-full mt-1.5 px-1 text-[8px] font-mono tracking-wider text-zinc-500 font-bold">
          <span>{minLabel}</span>
          {label && <span className="text-orange-500 font-bold">{label}</span>}
          <span>{maxLabel}</span>
        </div>
      )}
    </div>
  );
};

interface AcousticVentGrilleProps {
  cols?: number;
  rows?: number;
  variant?: 'strip' | 'cluster';
  isLight?: boolean;
}

export const AcousticVentGrille: React.FC<AcousticVentGrilleProps> = () => {
  return null;
};

interface StatusLedPipProps {
  status?: 'emerald' | 'amber' | 'crimson' | 'dim' | 'off';
  label?: string;
  isLight?: boolean;
  pulse?: boolean;
}

export const StatusLedPip: React.FC<StatusLedPipProps> = ({
  status = 'emerald',
  label,
  isLight = false,
}) => {
  return (
    <div className="inline-flex items-center gap-2 select-none">
      <div className={isLight ? 'status-pip-container-light' : 'status-pip-container'}>
        {status === 'emerald' && <div className="pip-led-emerald" />}
        {status === 'amber' && <div className="pip-led-amber" />}
        {status === 'crimson' && <div className="pip-led-crimson" />}
        {(status === 'dim' || status === 'off') && <div className="pip-led-dim" />}
      </div>
      {label && (
        <span className={`text-[10px] font-mono tracking-wider font-semibold uppercase ${
          isLight ? 'text-slate-600' : 'text-zinc-400'
        }`}>
          {label}
        </span>
      )}
    </div>
  );
};

export const MachineScrewHead: React.FC<{ isLight?: boolean; className?: string }> = ({
  isLight = false,
  className = '',
}) => {
  return (
    <div
      className={`${isLight ? 'machine-screw-light' : 'machine-screw'} ${className}`}
      aria-hidden="true"
    />
  );
};

interface ChassisPanelProps {
  children: React.ReactNode;
  title?: string;
  telemetryTag?: string;
  statusLed?: 'emerald' | 'amber' | 'crimson' | 'dim';
  statusLabel?: string;
  isLight?: boolean;
  className?: string;
}

export const ChassisPanel: React.FC<ChassisPanelProps> = ({
  children,
  title,
  telemetryTag,
  statusLed,
  statusLabel,
  isLight = false,
  className = '',
}) => {
  return (
    <div className={`rounded-2xl p-6 relative overflow-hidden transition-colors ${
      isLight ? 'chassis-milled-light text-slate-900' : 'chassis-milled-dark text-zinc-100'
    } ${className}`}>
      {/* Corner Fastener Screws */}
      <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
      <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
      <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
      <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />

      {/* Header bar if title or telemetry exists */}
      {(title || telemetryTag || statusLed) && (
        <div className={`flex flex-wrap items-center justify-between gap-3 pb-3 mb-4 border-b px-2 ${
          isLight ? 'border-slate-200' : 'border-zinc-800'
        }`}>
          <div className="flex items-center gap-3">
            {statusLed && (
              <StatusLedPip status={statusLed} label={statusLabel} isLight={isLight} />
            )}
            {title && (
              <span className={`text-xs font-mono font-bold tracking-wider uppercase ${
                isLight ? 'text-slate-900' : 'text-zinc-100'
              }`}>
                {title}
              </span>
            )}
          </div>

          {telemetryTag && (
            <span className={`px-2 py-0.5 rounded font-mono text-[9px] tracking-wider uppercase ${
              isLight ? 'telemetry-tag-light' : 'telemetry-tag-dark'
            }`}>
              {telemetryTag}
            </span>
          )}
        </div>
      )}

      {/* Main Content Area */}
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
};
