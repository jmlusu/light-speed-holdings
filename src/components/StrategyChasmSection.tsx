import React from 'react';
import { Reveal } from './Reveal';

interface StrategyChasmSectionProps {
  theme: 'light' | 'dark';
}

export const StrategyChasmSection: React.FC<StrategyChasmSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <section id="problem" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
      isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
    }`}>
      <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
        <span className="text-xs font-mono font-bold tracking-widest text-ls-red">
          THE STRATEGY-EXECUTION CHASM
        </span>
        <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
          isLight ? 'text-slate-900' : 'text-white'
        }`}>
          Why Most Transformations Stall
        </h2>
        <p className={`text-justify text-sm sm:text-base leading-relaxed ${
          isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
        }`}>
          Organizations fail for the same reasons. Strategy stays in slide decks. Data stays in silos. Execution takes months of manual handoffs.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        {/* Failure Trap 01 */}
        <Reveal delay={0}>
        <div className={`p-8 rounded-3xl border transition-all flex flex-col justify-between ${
          isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-lg' : 'bg-zinc-950/80 border-white/15 text-zinc-300 shadow-xl'
        }`}>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-2xl font-mono font-black text-ls-red">01</span>
              <span className="text-[10px] font-mono tracking-widest px-2.5 py-0.5 rounded-full border border-red-500/30 text-red-500 bg-red-500/10 font-bold">
                THE SLIDE TRAP
              </span>
            </div>
            <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Static Strategy Decks</h3>
            <p className="text-justify text-xs sm:text-sm leading-relaxed text-[var(--ink-primary)]">
              Most consultancies spend 6 months writing 200-page slide decks. By the time the presentation lands, market conditions have changed and the strategy is already out of date.
            </p>
          </div>
          <div className={`pt-6 border-t text-xs font-mono flex justify-between font-semibold ${isLight ? 'border-slate-200' : 'border-white/10'} text-[var(--ink-primary)]`}>
            <span>LATENCY: 6-9 MONTHS</span>
            <span className="text-red-500 font-bold">CODE SHIPPED: 0%</span>
          </div>
        </div>
        </Reveal>

        {/* Failure Trap 02 */}
        <Reveal delay={0.12}>
        <div className={`p-8 rounded-3xl border transition-all flex flex-col justify-between ${
          isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-lg' : 'bg-zinc-950/80 border-white/15 text-zinc-300 shadow-xl'
        }`}>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-2xl font-mono font-black text-ls-red">02</span>
              <span className="text-[10px] font-mono tracking-widest px-2.5 py-0.5 rounded-full border border-ls-cyan/30 text-ls-cyan bg-ls-cyan/10 font-bold">
                THE SILO TAX
              </span>
            </div>
            <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Fragmented Knowledge Pools</h3>
            <p className="text-justify text-xs sm:text-sm leading-relaxed text-[var(--ink-primary)]">
              Critical business data sits in legacy mainframes, paper bills-of-lading, and disconnected spreadsheets. Executives make multimillion-dollar decisions on information that is two weeks old.
            </p>
          </div>
          <div className={`pt-6 border-t text-xs font-mono flex justify-between font-semibold ${isLight ? 'border-slate-200' : 'border-white/10'} text-[var(--ink-primary)]`}>
            <span>TRUTH CONVERGENCE: POOR</span>
            <span className="text-ls-cyan font-bold">RISK: HIGH</span>
          </div>
        </div>
        </Reveal>

        {/* Failure Trap 03 */}
        <Reveal delay={0.24}>
        <div className={`p-8 rounded-3xl border transition-all flex flex-col justify-between ${
          isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-lg' : 'bg-zinc-950/80 border-white/15 text-zinc-300 shadow-xl'
        }`}>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-2xl font-mono font-black text-ls-red">03</span>
              <span className="text-[10px] font-mono tracking-widest px-2.5 py-0.5 rounded-full border border-ls-cyan/30 text-ls-cyan bg-ls-cyan/10 font-bold">
                THE TOY PLAYGROUND
              </span>
            </div>
            <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Ungoverned Ad-Hoc AI</h3>
            <p className="text-justify text-xs sm:text-sm leading-relaxed text-[var(--ink-primary)]">
              Companies subscribe to disconnected SaaS chatbots that generate text but cannot access production data, cannot run audited tools, and cannot take responsibility for outcomes.
            </p>
          </div>
          <div className={`pt-6 border-t text-xs font-mono flex justify-between font-semibold ${isLight ? 'border-slate-200' : 'border-white/10'} text-[var(--ink-primary)]`}>
            <span>BUSINESS IMPACT: 0%</span>
            <span className="text-ls-red font-bold">COMPLIANCE: UNVERIFIED</span>
          </div>
        </div>
        </Reveal>

      </div>
    </section>
  );
};
