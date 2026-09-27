import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { SectionHeading } from '../site/SectionHeading';
import { HonestyBadge } from '../site/HonestyBadge';
import { Reveal } from '../Reveal';
import { solutions } from '../../data/siteContent';
import { HomeSection } from './HomeSection';
import { ScrimPanel } from './ScrimPanel';

interface BuilderSectionProps {
  theme: 'light' | 'dark';
}

const SPOTLIGHT_RUNGS = ['Human Leadership', 'Agent Workforce', 'Intelligent Workflows', 'Decision Intelligence'];

/** Chapter 02 — AI Company Builder spotlight + the six-domain solutions grid. */
export const BuilderSection: React.FC<BuilderSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="builder" label="AI Company Builder and solutions" theme={theme} scrim={false}>
      <Reveal>
        <div className={`relative overflow-hidden rounded-3xl p-8 sm:p-10 flex flex-col lg:flex-row lg:items-center gap-8 border shadow-xl ${
          isLight ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy' : 'bg-ls-navy border-ls-white/15 text-ls-white'
        }`}>
          <div className="flex-1 space-y-4">
            <span className="font-body text-[10px] font-bold tracking-widest text-ls-red uppercase">WHAT WE BUILD // AI COMPANY BUILDER</span>
            <h2 className="text-2xl sm:text-4xl font-black tracking-tight font-display">Your Governed AI Workforce</h2>
            <p className={`text-sm sm:text-base leading-relaxed max-w-xl ${
              isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
            }`}>
              The orchestration engine that runs LightSpeed — 90 agents, 20 departments — licensed to run on your infrastructure. Human direction, audited execution.
            </p>
            <Link
              to="/ai-company-builder"
              className="ripple-on inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:bg-ls-red/90"
            >
              Explore AI Company Builder
              <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
            </Link>
          </div>
          <ul className={`lg:w-80 grid grid-cols-2 lg:grid-cols-1 gap-2.5 text-xs font-bold ${
            isLight ? 'text-ls-navy' : 'text-ls-white'
          }`}>
            {SPOTLIGHT_RUNGS.map((rung) => (
              <li key={rung} className="flex items-center gap-2.5 px-3.5 py-2.5 rounded-2xl border border-ls-cyan/25 bg-ls-cyan/5">
                <span className="w-2 h-2 shrink-0 rounded-full bg-ls-cyan shadow-[0_0_6px_rgba(0,191,255,0.8)]" aria-hidden="true" />
                {rung}
              </li>
            ))}
          </ul>
        </div>
      </Reveal>

      {/* Solutions — nested inside chapter 02, its own scrim panel. */}
      <ScrimPanel theme={theme} className="mt-20 sm:mt-24">
        <SectionHeading
          theme={theme}
          eyebrow="SOLUTIONS"
          title="Six Domains, One Governed Stack"
          lead="From strategy to shipped system — each solution carries its own honesty status."
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {solutions.map((sol, idx) => (
            <Reveal key={sol.slug} delay={(idx % 3) * 0.06}>
              <Link to="/contact" className={`ripple-on rounded-3xl p-6 border transition-all h-full flex flex-col justify-between group ${
                isLight ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl hover:-translate-y-0.5' : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl hover:-translate-y-0.5'
              }`}>
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-3">
                    <span className="font-body text-[10px] font-bold tracking-widest text-ls-red">{sol.eyebrow}</span>
                    <HonestyBadge label={sol.proof} />
                  </div>
                  <h3 className={`font-display font-bold text-base tracking-tight ${
                    isLight ? 'text-ls-navy' : 'text-ls-white'
                  }`}>
                    {sol.title}
                  </h3>
                  <p className={`text-xs leading-relaxed ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}>
                    {sol.oneLiner}
                  </p>
                </div>
                <div className={`pt-4 mt-4 border-t flex items-center justify-between ${isLight ? 'border-ls-grey-dark' : 'border-ls-white/10'}`}>
                  <span className={`text-[10px] font-body font-bold tracking-widest group-hover:text-ls-red transition-colors ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>EXPLORE</span>
                  <ArrowRight className="w-3.5 h-3.5 text-ls-red" aria-hidden="true" />
                </div>
              </Link>
            </Reveal>
          ))}
        </div>
        <div className="mt-8 text-center">
          <Link
            to="/what-we-do"
            className={`font-body text-xs font-bold tracking-widest hover:underline ${isLight ? 'text-ls-navy' : 'text-ls-cyan'}`}
          >
            VIEW ALL CAPABILITIES &amp; CATALOG →
          </Link>
        </div>
      </ScrimPanel>
    </HomeSection>
  );
};

export default BuilderSection;
