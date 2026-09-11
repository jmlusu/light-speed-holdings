import React from 'react';
import { Check } from 'lucide-react';

interface EngagementSectionProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const EngagementSection: React.FC<EngagementSectionProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  return (
    <section id="engagement" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
      isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
    }`}>
      <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
        <span className="text-xs font-mono font-bold tracking-widest text-orange-500">
          HOW WE ENGAGE
        </span>
        <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
          isLight ? 'text-slate-900' : 'text-white'
        }`}>
          Engagement Structures
        </h2>
        <p className={`text-justify text-sm sm:text-base leading-relaxed ${
          isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
        }`}>
          Three phases, each designed for board accountability and fast time-to-value.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        {/* Model 01 */}
        <div className={`p-8 rounded-3xl border flex flex-col justify-between space-y-6 ${
          isLight ? 'bg-white/95 border-slate-300 shadow-md text-slate-900' : 'bg-zinc-950/80 border-white/15 shadow-xl text-zinc-300'
        }`}>
          <div className="space-y-4">
            <span className={`text-xs font-mono font-bold block ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              PHASE 01 // 2 WEEKS
            </span>
            <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Advisory Architecture Sprint</h3>
            <p className={`text-justify text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
              A fast audit of your current operations, regulatory constraints, and data availability. You receive an executive blueprint with actionable business rules and an ROI model.
            </p>
            <ul className={`space-y-2 text-xs font-medium pt-2 ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
              <li className="flex items-center gap-2">
                <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                <span>Operations Bottleneck & Latency Audit</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                <span>Data Residency Blueprint</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                <span>Board-Level Investment Case</span>
              </li>
            </ul>
          </div>

          <button
            onClick={() => onRequestBriefing('Advisory Architecture Sprint (2 Weeks)')}
            className="w-full py-3 rounded-full border border-orange-500/50 text-orange-500 hover:bg-orange-500 hover:text-white font-bold text-xs tracking-wider transition-colors cursor-pointer"
          >
            Initiate Architecture Sprint
          </button>
        </div>

        {/* Model 02: Featured Co-Built Pilot */}
        <div className="p-8 rounded-3xl border-2 border-orange-500 bg-gradient-to-b from-orange-500/10 via-zinc-950 to-zinc-950 flex flex-col justify-between space-y-6 relative shadow-2xl shadow-orange-500/10">
          <div className="absolute -top-3 left-8 px-3 py-1 rounded-full bg-orange-500 text-white font-mono text-[10px] font-bold tracking-widest">
            MOST COMMON COMMENCEMENT
          </div>

          <div className="space-y-4">
            <span className="text-xs font-mono text-orange-400 font-bold block">
              PHASE 02 // 90 DAYS
            </span>
            <h3 className="text-xl font-bold tracking-tight text-white">Co-Built Pilot</h3>
            <p className="text-justify text-xs sm:text-sm text-zinc-300 leading-relaxed font-normal">
              We deploy a live AI pipeline alongside your internal team. You see real results against actual transaction volume before committing to a full rollout.
            </p>
            <ul className="space-y-2 text-xs text-zinc-200 font-medium pt-2">
              <li className="flex items-center gap-2">
                <Check className="w-3.5 h-3.5 text-orange-400 shrink-0" />
                <span>Production Core API Integration</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-3.5 h-3.5 text-orange-400 shrink-0" />
                <span>Human Approval Gates at Every Step</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-3.5 h-3.5 text-orange-400 shrink-0" />
                <span>Verified ROI Ledgers & SLA Guarantee</span>
              </li>
            </ul>
          </div>

          <button
            onClick={() => onRequestBriefing('Co-Engineered Pilot (90 Days)')}
            className="w-full py-3.5 rounded-full bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-bold text-xs tracking-widest transition-all cursor-pointer shadow-md shadow-orange-500/25"
          >
            Request Pilot Consultation
          </button>
        </div>

        {/* Model 03 */}
        <div className={`p-8 rounded-3xl border flex flex-col justify-between space-y-6 ${
          isLight ? 'bg-white/95 border-slate-300 shadow-md text-slate-900' : 'bg-zinc-950/80 border-white/15 shadow-xl text-zinc-300'
        }`}>
          <div className="space-y-4">
            <span className={`text-xs font-mono font-bold block ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              PHASE 03 // ENTERPRISE SCALE
            </span>
            <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Full Enterprise Deployment</h3>
            <p className={`text-justify text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
              Full transition to an AI-native operating model. Continuous agent teams, on-site inference clusters, and embedded transformation partners.
            </p>
            <ul className={`space-y-2 text-xs font-medium pt-2 ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
              <li className="flex items-center gap-2">
                <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                <span>Autonomous Multi-Agent Fleet</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                <span>Enterprise Air-Gapped Infrastructure</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                <span>24/7 Model Monitoring & Security Oversight</span>
              </li>
            </ul>
          </div>

          <button
            onClick={() => onRequestBriefing('Enterprise Deployment')}
            className="w-full py-3 rounded-full border border-orange-500/50 text-orange-500 hover:bg-orange-500 hover:text-white font-bold text-xs tracking-wider transition-colors cursor-pointer"
          >
            Consult On Enterprise Scope
          </button>
        </div>

      </div>
    </section>
  );
};
