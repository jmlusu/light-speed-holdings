import React, { useState } from 'react';
import { HeroSection } from '../components/HeroSection';
import { StrategyChasmSection } from '../components/StrategyChasmSection';
import { Reveal } from '../components/Reveal';
import { StatCounter } from '../components/StatCounter';

interface HomePageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

/**
 * Verified operating metrics — sourced from company-registry (agent configs),
 * the automated test suite (regression tests), onboarded departments, and the
 * ApprovalGate governance layer (human approval tiers). No other data claims.
 */
interface ProofStat {
  value: number;
  label: string;
  format?: 'plain' | 'comma';
  suffix?: string;
}

const PROOF_STATS: ProofStat[] = [
  { value: 144, label: 'Verified Agent Configurations', format: 'comma' },
  { value: 2373, label: 'Automated Regression Tests', format: 'comma' },
  { value: 20, label: 'Departments Onboarded' },
  { value: 5, label: 'Human Approval Gates', suffix: '-Tier' },
];

export const HomePage: React.FC<HomePageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  // Pillar selection is page-local now: the cross-section linkage to
  // CoreOfferings moved to the Capabilities page.
  const [activePillar, setActivePillar] = useState(0);

  return (
    <div>
      <HeroSection
        theme={theme}
        onRequestBriefing={onRequestBriefing}
        activePillar={activePillar}
        onSelectPillar={setActivePillar}
      />

      <StrategyChasmSection theme={theme} />

      {/* Proof Band: verified operating metrics + executive briefing CTA */}
      <Reveal delay={0.05}>
      <section
        id="proof"
        aria-label="Verified operating metrics"
        className="px-4 sm:px-8 pb-24 sm:pb-28 max-w-7xl mx-auto w-full"
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
            {/* Eyebrow Badge + 4 Stat Cells */}
            <div className="flex-1 space-y-6">
              <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
                <span className="w-2 h-2 rounded-full bg-ls-red shadow-sm shadow-ls-red/80 animate-pulse" />
                <span>PROOF // VERIFIED OPERATING METRICS</span>
              </div>

              <div className="grid grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-6">
                {PROOF_STATS.map((stat, sIdx) => (
                  <div key={sIdx} className="min-w-0">
                    <span
                      className={`block text-xl sm:text-2xl font-black font-mono tracking-tight ${
                        sIdx % 2 === 0 ? 'text-ls-red' : 'text-ls-cyan'
                      }`}
                    >
                      <StatCounter to={stat.value} format={stat.format} suffix={stat.suffix} />
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
      </Reveal>
    </div>
  );
};

export default HomePage;
