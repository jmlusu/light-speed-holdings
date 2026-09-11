import React from 'react';
import { ArrowRight, CheckCircle2, GitMerge, Clock, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { AcousticVentGrille } from './TactileHardwareElements';

interface CoreCapability {
  id: string;
  title: string;
  shortTitle: string;
  eyebrow: string;
  tagline: string;
  desc: string;
  metrics: string;
  inputContract: string;
  outputContract: string;
  upstreamSource: string;
  downstreamTarget: string;
  governance: string;
  deliverables: string[];
}

interface OfferingDetailCardProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
  offering: CoreCapability;
  activePillar: number;
  totalPillars: number;
  onSelectPillar: (idx: number) => void;
}

export const OfferingDetailCard: React.FC<OfferingDetailCardProps> = ({
  theme,
  onRequestBriefing,
  offering: active,
  activePillar,
  totalPillars,
  onSelectPillar
}) => {
  const isLight = theme === 'light';
  return (
    <div className={`p-6 sm:p-10 rounded-3xl transition-all duration-300 relative overflow-hidden shadow-2xl ${
      isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
    }`}>
      {/* Hardware Hex Corner Screws */}
      <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
      <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
      <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
      <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

      {/* Corner Badge */}
      <div className="absolute top-0 right-0 py-1.5 px-4 rounded-bl-2xl bg-orange-500 text-white text-[10px] font-mono font-bold tracking-wider shadow-md">
        {active.governance}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">

        {/* Left Column: Core Description & Contracts */}
        <div className="lg:col-span-7 space-y-6">
          <div>
            <span className="text-xs font-mono font-bold tracking-wider text-orange-500 block mb-1">
              {active.eyebrow}
            </span>
            <h3 className={`text-2xl sm:text-3xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              {active.title}
            </h3>
            <div className={`text-sm font-semibold mt-1 ${isLight ? 'text-slate-800' : 'text-orange-400'}`}>
              {active.tagline}
            </div>
          </div>

          <p className={`text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            {active.desc}
          </p>

          {/* Inter-Offering Data Contracts Box */}
          <div className={`p-4 rounded-2xl space-y-3 ${
            isLight ? 'hardware-well-light' : 'hardware-well-dark'
          }`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <GitMerge className="w-4 h-4 text-orange-500" />
                <span className={`text-xs font-mono font-bold ${isLight ? 'text-slate-900' : 'text-zinc-200'}`}>
                  Structured Inter-Offering Contracts
                </span>
              </div>
              <AcousticVentGrille variant="cluster" isLight={isLight} />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div className={`p-3 rounded-xl border ${isLight ? 'bg-white/90 border-slate-300' : 'bg-zinc-950/80 border-white/10'}`}>
                <span className={`text-[10px] font-mono font-bold block mb-1 ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>
                  Input Contract (Feeds In)
                </span>
                <p className={`text-justify font-medium leading-tight ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                  {active.inputContract}
                </p>
              </div>

              <div className={`p-3 rounded-xl border ${isLight ? 'bg-white/90 border-slate-300' : 'bg-zinc-950/80 border-white/10'}`}>
                <span className={`text-[10px] font-mono font-bold block mb-1 text-emerald-500`}>
                  Output Contract (Generates)
                </span>
                <p className={`text-justify font-medium leading-tight ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                  {active.outputContract}
                </p>
              </div>
            </div>

            {/* Upstream & Downstream Flow Lineage Grid */}
            <div className={`pt-3 border-t grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs ${
              isLight ? 'border-slate-200' : 'border-white/10'
            }`}>
              {/* Upstream Source Card */}
              <div className={`p-3 rounded-xl border flex flex-col justify-between space-y-1.5 ${
                isLight ? 'bg-orange-50/70 border-orange-200/80' : 'bg-orange-950/30 border-orange-500/20'
              }`}>
                <div className="flex items-center gap-1.5">
                  <span className="p-1 rounded-md bg-orange-500/15 text-orange-500">
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  </span>
                  <span className="font-bold font-mono text-[10px] tracking-wider text-orange-500">
                    Upstream Source
                  </span>
                </div>
                <p className={`text-justify text-[11px] sm:text-xs leading-relaxed font-medium break-words ${
                  isLight ? 'text-slate-800' : 'text-zinc-300'
                }`}>
                  {active.upstreamSource}
                </p>
              </div>

              {/* Downstream Target Card */}
              <div className={`p-3 rounded-xl border flex flex-col justify-between space-y-1.5 ${
                isLight ? 'bg-emerald-50/70 border-emerald-200/80' : 'bg-emerald-950/30 border-emerald-500/20'
              }`}>
                <div className="flex items-center gap-1.5">
                  <span className="p-1 rounded-md bg-emerald-500/15 text-emerald-500">
                    <ArrowDownRight className="w-3.5 h-3.5" />
                  </span>
                  <span className="font-bold font-mono text-[10px] tracking-wider text-emerald-500">
                    Downstream Target
                  </span>
                </div>
                <p className={`text-justify text-[11px] sm:text-xs leading-relaxed font-medium break-words ${
                  isLight ? 'text-slate-800' : 'text-zinc-300'
                }`}>
                  {active.downstreamTarget}
                </p>
              </div>
            </div>
          </div>

          {/* Deliverables List */}
          <div>
            <div className={`text-xs font-mono font-bold mb-3 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Production Deliverables & Specifications:
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {active.deliverables.map((item, dIdx) => (
                <div
                  key={dIdx}
                  className={`flex items-center gap-2.5 p-3 rounded-xl border text-xs font-medium transition-colors ${
                    isLight ? 'bg-slate-50 border-slate-300 text-slate-800 hover:bg-slate-100' : 'border-white/15 bg-white/[0.04] text-zinc-300 hover:bg-white/[0.08]'
                  }`}
                >
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                  <span className="leading-snug">{item}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Institutional Benchmarks & Engagement Model */}
        <div className="lg:col-span-5 space-y-5">
          <div className={`p-6 rounded-2xl ${
            isLight ? 'hardware-well-light' : 'hardware-well-dark'
          }`}>
            <span className={`text-xs font-mono block mb-1 font-bold ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Verified Institutional Benchmark
            </span>
            <div className="text-xl sm:text-2xl font-black font-mono text-emerald-500">
              {active.metrics}
            </div>
            <div className={`text-xs font-medium mt-2 leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
              Backed by audited telemetry in live production deployments across SADC commercial banking, national revenue authorities, and transport corridors.
            </div>
          </div>

          {/* Interconnected Suite Nav */}
          <div className={`p-5 rounded-2xl space-y-3 ${
            isLight ? 'hardware-well-light' : 'hardware-well-dark'
          }`}>
            <div className="flex items-center justify-between text-xs font-mono font-bold">
              <span className={isLight ? 'text-slate-900' : 'text-zinc-200'}>Integrated Suite Position</span>
              <span className="text-orange-500">Step {activePillar + 1} of {totalPillars}</span>
            </div>

            <div className="grid grid-cols-4 gap-1.5">
              {Array.from({ length: totalPillars }).map((_, cIdx) => (
                <button
                  key={cIdx}
                  onClick={() => onSelectPillar(cIdx)}
                  className={`h-2.5 rounded-full transition-all ${
                    activePillar === cIdx
                      ? 'bg-orange-500 shadow-[0_0_6px_rgba(249,115,22,0.8)]'
                      : isLight ? 'bg-slate-300 hover:bg-slate-400' : 'bg-zinc-800 hover:bg-zinc-700'
                  }`}
                  title={`Switch to Offering 0${cIdx + 1}`}
                />
              ))}
            </div>

            <div className="flex items-center justify-between pt-2">
              <button
                onClick={() => onSelectPillar((activePillar + totalPillars - 1) % totalPillars)}
                className={`text-xs font-mono font-semibold hover:text-orange-500 cursor-pointer ${
                  isLight ? 'text-slate-600' : 'text-zinc-400'
                }`}
              >
                Prev Offering
              </button>
              <button
                onClick={() => onSelectPillar((activePillar + 1) % totalPillars)}
                className="text-xs font-mono font-bold text-orange-500 hover:text-orange-400 cursor-pointer flex items-center gap-1"
              >
                <span>Next Offering</span>
                <ArrowRight className="w-3 h-3" />
              </button>
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-orange-500/10 border border-orange-500/30 space-y-3 relative overflow-hidden">
            <div className="text-xs font-mono tracking-wider text-orange-500 font-bold flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5" />
              <span>Commercial Engagement Protocol</span>
            </div>
            <div className={`text-sm font-bold ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
              2-Week Advisory Sprint to 90-Day Co-Built Pilot
            </div>
            <p className={`text-justify text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
              We embed with your executive team, audit current bottlenecks, define system requirements, and deliver production code with zero data leakage.
            </p>
            <button
              onClick={() => onRequestBriefing(`Inquiry regarding ${active.title}: ${active.tagline}`)}
              className="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-bold text-xs tracking-wider flex items-center justify-center gap-2 cursor-pointer transition-all shadow-md shadow-orange-500/20 active:scale-98"
            >
              <span>Engage {active.shortTitle} Practice</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};
