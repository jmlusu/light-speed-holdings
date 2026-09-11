import React from 'react';
import { RefreshCw, Activity } from 'lucide-react';

interface SynergyMatrixProps {
  theme: 'light' | 'dark';
  selectedSynergy: string;
  onSelectSynergy: (key: string) => void;
}

const synergyPairs: Record<string, {
  title: string;
  from: string;
  to: string;
  headline: string;
  mechanism: string;
  compoundImpact: string;
}> = {
  'strategy-intelligence': {
    title: 'Strategy and Intelligence',
    from: '01. Strategy',
    to: '02. Private Intelligence',
    headline: 'Policy-Governed Knowledge Systems',
    mechanism: 'Compliance rules and corporate mandates become data filters. The knowledge graph keeps confidential data within regulatory boundaries and blocks unauthorized access before indexing anything.',
    compoundImpact: 'Zero unauthorized data leakage across cross-border business units.'
  },
  'intelligence-systems': {
    title: 'Intelligence and Autonomous Systems',
    from: '02. Private Intelligence',
    to: '03. Autonomous Systems',
    headline: 'Verified AI Grounding',
    mechanism: 'The knowledge graph feeds verified document citations and entity links directly to AI agents. Every recommendation traces back to an actual source record. No made-up information.',
    compoundImpact: 'Zero made-up information with sub-200ms retrieval across millions of legacy records.'
  },
  'systems-execution': {
    title: 'Autonomous Systems and Execution',
    from: '03. Autonomous Systems',
    to: '04. Execution & Settlement',
    headline: 'Verified Autonomous Settlement',
    mechanism: 'Agent teams break complex transactions into individual API calls. High-value operations route through human approval gates before writing to banking or customs systems.',
    compoundImpact: 'Reconciliation times compressed from 72 hours to 14 minutes. Every write verified.'
  },
  'execution-strategy': {
    title: 'Execution and Strategy (Feedback Loop)',
    from: '04. Execution & Settlement',
    to: '01. Strategy',
    headline: 'Closed-Loop Performance Telemetry',
    mechanism: 'Live transaction data, revenue recovery, and error rates feed into executive dashboards. Leadership adjusts strategy based on current performance, not quarterly assumptions.',
    compoundImpact: 'Quarterly strategy cycles replaced by real-time operational adjustment.'
  }
};

export const SynergyMatrix: React.FC<SynergyMatrixProps> = ({
  theme,
  selectedSynergy,
  onSelectSynergy
}) => {
  const isLight = theme === 'light';
  return (
    <div className={`mt-12 p-8 sm:p-10 rounded-3xl border ${
      isLight ? 'bg-slate-50/80 border-slate-300' : 'bg-zinc-950/70 border-white/15'
    }`}>
      <div className="max-w-3xl mb-8 space-y-2">
        <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-500 font-mono text-[10px] tracking-widest">
          <RefreshCw className="w-3 h-3" />
          <span>THE CLOSED-LOOP MULTIPLIER EFFECT</span>
        </div>
        <h3 className={`text-2xl sm:text-3xl font-black tracking-tight font-display ${
          isLight ? 'text-slate-900' : 'text-white'
        }`}>
          How the Four Offerings Interconnect
        </h3>
        <p className={`text-justify text-xs sm:text-sm leading-relaxed ${
          isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
        }`}>
          Deploying any single offering creates value. Connecting all four multiplies it. Click any pair below to see the integration protocol:
        </p>
      </div>

      {/* Synergy Pair Selector Buttons */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        {Object.entries(synergyPairs).map(([key, pair]) => (
          <button
            key={key}
            onClick={() => onSelectSynergy(key)}
            className={`p-3.5 rounded-xl border text-left transition-all cursor-pointer ${
              selectedSynergy === key
                ? 'bg-orange-500 text-white border-orange-400 shadow-md shadow-orange-500/20'
                : isLight
                  ? 'bg-white hover:bg-slate-100 text-slate-800 border-slate-300'
                  : 'bg-zinc-900/80 hover:bg-zinc-900 text-zinc-300 border-white/15'
            }`}
          >
            <div className={`text-[10px] font-mono font-bold mb-1 ${
              selectedSynergy === key ? 'text-orange-100' : 'text-orange-500'
            }`}>
              {pair.title}
            </div>
            <div className="text-xs font-bold truncate">{pair.headline}</div>
          </button>
        ))}
      </div>

      {/* Active Synergy Detail Card */}
      {(() => {
        const pair = synergyPairs[selectedSynergy];
        if (!pair) return null;
        return (
          <div className={`p-6 rounded-2xl border transition-all ${
            isLight ? 'bg-white border-slate-300 shadow-sm' : 'bg-zinc-900/90 border-white/20'
          }`}>
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-orange-500/20 mb-4">
              <div className="flex items-center gap-3">
                <span className="px-3 py-1 rounded-lg bg-orange-500 text-white font-mono text-xs font-bold">
                  {pair.title}
                </span>
                <h4 className={`text-base font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                  {pair.headline}
                </h4>
              </div>
              <div className="flex items-center gap-2 text-xs font-mono font-semibold text-emerald-500">
                <Activity className="w-3.5 h-3.5" />
                <span>Real-time Integration Protocol</span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-start">
              <div className="md:col-span-7 space-y-2">
                <span className={`text-[11px] font-mono font-bold block ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>
                  Integration Mechanism & Technical Contract
                </span>
                <p className={`text-justify text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'}`}>
                  {pair.mechanism}
                </p>
              </div>

              <div className={`md:col-span-5 p-4 rounded-xl border ${
                isLight ? 'bg-emerald-50/70 border-emerald-200 text-emerald-950' : 'bg-emerald-950/20 border-emerald-500/30 text-emerald-200'
              }`}>
                <span className="text-[10px] font-mono font-bold text-emerald-600 dark:text-emerald-400 block mb-1">
                  Compound Institutional Impact
                </span>
                <p className="text-justify text-xs font-bold leading-relaxed">
                  {pair.compoundImpact}
                </p>
              </div>
            </div>
          </div>
        );
      })()}
    </div>
  );
};
