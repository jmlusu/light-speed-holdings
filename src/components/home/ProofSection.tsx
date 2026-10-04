import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { Reveal } from '../Reveal';
import { HomeSection } from './HomeSection';
import { liveTestCount, metrics } from '../../data/metrics';

interface ProofSectionProps {
  theme: 'light' | 'dark';
}

const PROOF_STATS = [
  { value: metrics.agentCount, label: 'Agent Configurations', format: 'comma' },
  { value: liveTestCount, label: 'Automated Regression Tests', format: 'comma' },
  { value: metrics.departments, label: 'Departments Onboarded' },
  { value: 5, label: 'Human Approval Gates', suffix: '-Tier' },
];

/** Chapter 05 — verified operating metrics on its own solid panel (no scrim). */
export const ProofSection: React.FC<ProofSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="proof" label="Verified operating metrics" theme={theme} scrim={false}>
      <Reveal delay={0.05}>
        <div className={`relative overflow-hidden rounded-3xl p-6 sm:p-8 border shadow-xl ${
          isLight ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy' : 'bg-ls-navy border-ls-white/15 text-ls-white'
        }`}>
          <div className="flex flex-col xl:flex-row xl:items-center gap-8 xl:gap-12">
            <div className="flex-1 space-y-6">
              <h2 className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-body text-[11px] tracking-widest">
                <span className="w-2 h-2 rounded-full bg-ls-red shadow-sm shadow-ls-red/80" aria-hidden="true" />
                <span>PROOF // VERIFIED OPERATING METRICS</span>
              </h2>
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-6">
                {PROOF_STATS.map((stat, sIdx) => (
                  <div key={sIdx} className="min-w-0">
                      <span className="block text-xl sm:text-2xl font-black font-body tracking-tight">
                        {stat.format === 'comma' ? stat.value.toLocaleString('en-US') : stat.value}
                        {stat.suffix}
                      </span>
                    <span className={`block mt-1 text-[10px] font-body font-bold tracking-widest uppercase ${
                      isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                    }`}>
                      {stat.label}
                    </span>
                  </div>
                ))}
              </div>
            </div>
            <div className={`shrink-0 w-full xl:w-auto xl:border-l xl:pl-12 flex flex-col items-start gap-3 ${
              isLight ? 'xl:border-ls-grey-dark/30' : 'xl:border-ls-white/10'
            }`}>
              <Link
                to="/proof"
                className="ripple-on w-full xl:w-auto inline-flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:bg-ls-red/90"
              >
                See the Evidence
                <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
              </Link>
              <span className={`text-[10px] font-body tracking-widest font-bold ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
                SHIPPED ENGAGEMENTS &amp; POLICY
              </span>
            </div>
          </div>
        </div>
      </Reveal>
    </HomeSection>
  );
};

export default ProofSection;
