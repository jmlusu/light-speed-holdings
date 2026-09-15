import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { Reveal } from '../components/Reveal';
import { solutions, GOVERNANCE_SOLUTION } from '../data/siteContent';

interface SolutionsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /solutions hub. Lists the five detailed solution domains plus the
 * AI Governance & Policy domain (anchored under /technology#governance).
 * Every card carries its honesty status — we never blur proven vs. planned.
 */
export const SolutionsPage: React.FC<SolutionsPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="WHAT WE DO"
        title="Solutions Built for the Work to Be Done"
        lead="Six domains cover the arc from strategy to shipped system: agentic AI, digital transformation, data & intelligence, intelligent automation, strategy & advisory, and the governance layer that makes deployment safe. Every claim on this page carries its honesty status."
      />

      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 pb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {solutions.map((sol, idx) => (
            <Reveal key={sol.slug} delay={idx * 0.06}>
              <Link
                to={`/solutions/${sol.slug}`}
                className={`relative rounded-3xl p-6 sm:p-7 border transition-all h-full flex flex-col justify-between group ${
                  isLight
                    ? 'bg-white/95 border-slate-300 shadow-md hover:shadow-xl hover:-translate-y-0.5'
                    : 'bg-zinc-950/80 border-white/15 shadow-xl hover:shadow-2xl hover:-translate-y-0.5'
                }`}
              >
                <div className="space-y-4">
                  <div className="flex items-start justify-between gap-3">
                    <span className={`font-mono text-[10px] font-bold tracking-widest text-ls-red`}>
                      {sol.eyebrow}
                    </span>
                    <HonestyBadge label={sol.proof} />
                  </div>
                  <h3 className={`text-xl font-bold tracking-tight font-display ${
                    isLight ? 'text-slate-900' : 'text-zinc-100'
                  }`}>
                    {sol.title}
                  </h3>
                  <p className={`text-xs sm:text-sm leading-relaxed ${
                    isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
                  }`}>
                    {sol.oneLiner}
                  </p>
                </div>
                <div className={`pt-5 mt-5 border-t flex items-center justify-between ${
                  isLight ? 'border-slate-200' : 'border-white/10'
                }`}>
                  <span className={`text-[11px] font-mono font-bold tracking-widest group-hover:text-ls-red transition-colors ${
                    isLight ? 'text-slate-500' : 'text-zinc-400'
                  }`}>
                    EXPLORE
                  </span>
                  <ArrowRight className="w-4 h-4 text-ls-red" aria-hidden="true" />
                </div>
              </Link>
            </Reveal>
          ))}

          {/* Governance & Policy domain card (anchored at /technology#governance) */}
          <Reveal delay={solutions.length * 0.06}>
            <Link
              to={GOVERNANCE_SOLUTION.to}
              className={`relative rounded-3xl p-6 sm:p-7 border transition-all h-full flex flex-col justify-between group ${
                isLight
                  ? 'bg-white/95 border-slate-300 shadow-md hover:shadow-xl hover:-translate-y-0.5'
                  : 'bg-zinc-950/80 border-white/15 shadow-xl hover:shadow-2xl hover:-translate-y-0.5'
              }`}
            >
              <div className="space-y-4">
                <div className="flex items-start justify-between gap-3">
                  <span className="font-mono text-[10px] font-bold tracking-widest text-ls-red">
                    {GOVERNANCE_SOLUTION.eyebrow}
                  </span>
                  <HonestyBadge label={GOVERNANCE_SOLUTION.proof} />
                </div>
                <h3 className={`text-xl font-bold tracking-tight font-display ${
                  isLight ? 'text-slate-900' : 'text-zinc-100'
                }`}>
                  {GOVERNANCE_SOLUTION.title}
                </h3>
                <p className={`text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
                }`}>
                  {GOVERNANCE_SOLUTION.oneLiner}
                </p>
              </div>
              <div className={`pt-5 mt-5 border-t flex items-center justify-between ${
                isLight ? 'border-slate-200' : 'border-white/10'
              }`}>
                <span className={`text-[11px] font-mono font-bold tracking-widest group-hover:text-ls-red transition-colors ${
                  isLight ? 'text-slate-500' : 'text-zinc-400'
                }`}>
                  EXPLORE
                </span>
                <ArrowRight className="w-4 h-4 text-ls-red" aria-hidden="true" />
              </div>
            </Link>
          </Reveal>
        </div>
      </section>

      {/* Engagement model strip */}
      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full py-16 sm:py-20 border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <SectionHeading
          theme={theme}
          eyebrow="HOW WE WORK"
          title="One Human CEO. A Governed Agent Workforce."
          lead="Strategy — Build — Govern — Scale. Every engagement passes four gates (G1 discovery → G2 architecture → G3 build → G4 handover) that map to a five-tier human-approval matrix. What ships is yours: sites, data, dashboards, and agents, with 30 days of support included."
        />
        <Reveal>
          <div className={`max-w-3xl mx-auto rounded-3xl p-6 sm:p-8 border ${
            isLight ? 'bg-white/95 border-slate-300 shadow-md' : 'bg-zinc-950/80 border-white/15 shadow-xl'
          }`}>
            <ul className={`grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-3 text-sm leading-relaxed ${
              isLight ? 'text-slate-700' : 'text-zinc-300'
            }`}>
              <li className="flex items-start gap-2">
                <span className="text-ls-red font-mono font-black" aria-hidden="true">01</span>
                G1 DISCOVERY — a governed, 5-tier-approved conversation, not a product demo.
              </li>
              <li className="flex items-start gap-2">
                <span className="text-ls-red font-mono font-black" aria-hidden="true">02</span>
                G2 ARCHITECTURE — target design, cost, and honesty on what we will and won't build.
              </li>
              <li className="flex items-start gap-2">
                <span className="text-ls-red font-mono font-black" aria-hidden="true">03</span>
                G3 BUILD — 90-day pilot window, delivered against named outcomes.
              </li>
              <li className="flex items-start gap-2">
                <span className="text-ls-red font-mono font-black" aria-hidden="true">04</span>
                G4 HANDOVER — everything yours, documented, supported for 30 days.
              </li>
            </ul>
          </div>
        </Reveal>
      </section>

      <CtaBand theme={theme} />
    </>
  );
};

export default SolutionsPage;
