import React from 'react';
import { EngagementSection } from '../components/EngagementSection';

interface EngagementPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

/**
 * Verified operating metrics powering the engagement proof strip — same
 * baseline the Home page cites: 144 registered agents, the enforced
 * regression suite, the 20 governed departments, and the ApprovalGate
 * five-tier human-approval matrix.
 */
const PROOF_STATS = [
  { value: '144', label: 'Agent Configurations in Production' },
  { value: '2,373', label: 'Regression Tests Enforced on Every Change' },
  { value: '20', label: 'Departments Under Agent Governance' },
  { value: '5-TIER', label: 'Human Approval Matrix with Audit Trail' },
];

export const EngagementPage: React.FC<EngagementPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      <section
        aria-labelledby="engagement-heading"
        className={`px-4 sm:px-8 pt-16 sm:pt-20 pb-2 max-w-7xl mx-auto w-full ${
          isLight ? 'text-slate-800' : 'text-zinc-100'
        }`}
      >
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
            <span className="w-2 h-2 rounded-full bg-ls-red shadow-sm shadow-ls-red/80 animate-pulse" />
            <span>ENGAGEMENT MODELS</span>
          </div>
          <h1
            id="engagement-heading"
            className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}
          >
            Engagement Structures for Board Accountability
          </h1>
          <p
            className={`max-w-2xl text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-slate-600' : 'text-zinc-400'
            }`}
          >
            Advisory sprints, co-built pilots, and full enterprise deployment — each phase designed for board accountability, traceable governance, and measurable outcomes within 90 days.
          </p>
        </div>
      </section>

      {/* Proof Strip: verified operating metrics + executive briefing CTA */}
      <section
        aria-label="Verified operating metrics"
        className="px-4 sm:px-8 py-16 sm:py-20 max-w-7xl mx-auto w-full"
      >
        <div
          className={`relative overflow-hidden rounded-3xl p-6 sm:p-8 ${
            isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
          }`}
        >
          {/* Hardware Hex Corner Fasteners */}
          <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
          <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
          <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
          <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

          <div className="flex flex-col xl:flex-row xl:items-center gap-8 xl:gap-12">
            {/* Eyebrow Badge + Stat Cells */}
            <div className="flex-1 space-y-6">
              <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
                <span className="w-2 h-2 rounded-full bg-ls-red shadow-sm shadow-ls-red/80 animate-pulse" />
                <span>PROOF // VERIFIED OPERATING METRICS</span>
              </div>

              <p className={`max-w-3xl text-sm sm:text-base leading-relaxed ${
                isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
              }`}>
                These are not projections or pilot snapshots. They are the operating baseline of a company that runs its own infrastructure on the same governance architecture it offers clients. An engagement with LightSpeed begins with that baseline — and gives your organization the same traceability, approval gates, and audit discipline we apply to ourselves.
              </p>

              <div className="grid grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-6">
                {PROOF_STATS.map((stat, sIdx) => (
                  <div key={sIdx} className="min-w-0">
                    <span
                      className={`block text-xl sm:text-2xl font-black font-mono tracking-tight ${
                        sIdx % 2 === 0 ? 'text-ls-red' : 'text-ls-cyan'
                      }`}
                    >
                      {stat.value}
                    </span>
                    <span
                      className={`block mt-1 text-[10px] font-mono font-bold tracking-widest uppercase ${
                        isLight ? 'text-slate-500' : 'text-zinc-500'
                      }`}
                    >
                      {stat.label}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* CTA */}
            <div
              className={`shrink-0 w-full xl:w-auto xl:border-l xl:pl-12 ${
                isLight ? 'xl:border-slate-300/70' : 'xl:border-white/10'
              }`}
            >
              <button
                onClick={() => onRequestBriefing()}
                className="w-full xl:w-auto inline-flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:brightness-110"
              >
                Request Your Executive Briefing
              </button>
            </div>
          </div>
        </div>
      </section>

      <EngagementSection theme={theme} onRequestBriefing={onRequestBriefing} />
    </>
  );
};

export default EngagementPage;
