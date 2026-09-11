import React from 'react';
import { ArrowRight } from 'lucide-react';
import { AcousticVentGrille } from './TactileHardwareElements';

interface PillarNavigationCardProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
  activePillar: number;
  onSelectPillar: (idx: number) => void;
}

const PILLARS = [
  { num: '01', title: 'Strategy', desc: 'Operating model redesign & capital allocation', tag: 'Executive', idx: 0 },
  { num: '02', title: 'Intelligence', desc: 'Private data systems & knowledge graphs', tag: 'Data', idx: 1 },
  { num: '03', title: 'AI-Native Systems', desc: 'Multi-agent orchestration & structured workflows', tag: 'Autonomous', idx: 2 },
  { num: '04', title: 'Execution', desc: 'Legacy core integration & instant settlement', tag: 'Production', idx: 3 }
];

export const PillarNavigationCard: React.FC<PillarNavigationCardProps> = ({
  theme,
  onRequestBriefing,
  activePillar,
  onSelectPillar
}) => {
  const isLight = theme === 'light';
  return (
    <div className={`p-6 sm:p-7 rounded-3xl max-w-md w-full transition-all duration-300 relative overflow-hidden ${
      isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
    }`}>
      {/* Hardware Hex Corner Fasteners */}
      <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
      <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
      <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
      <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

      {/* Chassis Header Strip with Micro Acoustic Vent */}
      <div className={`flex items-center justify-between pb-3.5 border-b ${isLight ? 'border-black/10' : 'border-white/10'}`}>
        <div className="flex items-center gap-2 pl-2">
          <div className="w-2.5 h-2.5 rounded-full bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.9)]" />
          <span className={`font-mono text-xs font-bold tracking-wider ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
            OPERATING MODEL
          </span>
        </div>
        <div className="flex items-center gap-2.5 pr-2">
          <AcousticVentGrille variant="strip" isLight={isLight} />
          <span className="text-[10px] font-mono text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20 font-bold">
            LIVE CORE
          </span>
        </div>
      </div>

      {/* The 4 Connected Pillars (Tactile Hardware Stepped Array) */}
      <div className="space-y-2 pt-4">
        {PILLARS.map((p) => (
          <button
            key={p.num}
            onClick={() => {
              onSelectPillar(p.idx);
              const el = document.getElementById('capabilities');
              if (el) el.scrollIntoView({ behavior: 'smooth' });
            }}
            className={`w-full text-left p-3 rounded-2xl transition-all cursor-pointer group ${
              activePillar === p.idx
                ? isLight ? 'tactile-btn-active-light border-orange-500/50' : 'tactile-btn-active-dark border-orange-500/50'
                : isLight
                  ? 'tactile-concave-btn-light'
                  : 'tactile-concave-btn-dark'
            }`}
          >
            <div className="flex items-center justify-between text-xs mb-1">
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full transition-all ${
                  activePillar === p.idx ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                }`} />
                <span className="font-mono font-bold text-orange-500">{p.num}</span>
                <span className={`font-bold font-display group-hover:text-orange-500 transition-colors ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>{p.title}</span>
              </div>
              <span className={`text-[10px] font-mono font-semibold ${activePillar === p.idx ? 'text-orange-500' : 'text-zinc-500'}`}>{p.tag}</span>
            </div>
            <p className="text-justify text-xs leading-snug pl-6 text-zinc-500 font-medium">
              {p.desc}
            </p>
          </button>
        ))}
      </div>

      {/* Card Footer */}
      <div className={`pt-4 mt-3 border-t flex items-center justify-between text-xs px-2 ${isLight ? 'border-black/10' : 'border-white/10'}`}>
        <span className="font-mono text-[10px] font-semibold text-zinc-500">SADC & International</span>
        <button
          onClick={() => onRequestBriefing()}
          className="font-mono text-[11px] font-bold text-orange-500 hover:text-orange-400 flex items-center gap-1 cursor-pointer"
        >
          <span>Partner Briefing</span>
          <ArrowRight className="w-3 h-3" />
        </button>
      </div>

    </div>
  );
};
