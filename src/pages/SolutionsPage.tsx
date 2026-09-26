import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { Reveal } from '../components/Reveal';
import { solutions, GOVERNANCE_SOLUTION } from '../data/siteContent';
import type { HonestyLabel } from '../data/siteContent';

interface SolutionsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

interface SolutionCardData {
  eyebrow: string;
  title: string;
  proof: HonestyLabel;
  spec: {
    problem: string;
    audience: string;
    changes: string;
    builds: string;
    evidence: string;
  };
}

const SPEC_QUESTIONS: Array<{ key: keyof SolutionCardData['spec']; label: string }> = [
  { key: 'problem', label: 'THE PROBLEM' },
  { key: 'audience', label: "WHO IT'S FOR" },
  { key: 'changes', label: 'WHAT CHANGES' },
  { key: 'builds', label: 'WHAT WE BUILD' },
  { key: 'evidence', label: 'EVIDENCE' },
];

/**
 * One solution card answering all five MASTER_SPEC §10 questions:
 * problem, audience, changes, build, evidence — each with its honesty status.
 */
const SolutionCard: React.FC<{
  sol: SolutionCardData;
  theme: 'light' | 'dark';
  to: string;
}> = ({ sol, theme, to }) => {
  const isLight = theme === 'light';

  return (
    <Link
      to={to}
      className={`relative rounded-3xl p-6 sm:p-7 border transition-all h-full flex flex-col justify-between group ${
        isLight
          ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl hover:-translate-y-0.5'
          : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl hover:-translate-y-0.5'
      }`}
    >
      <div className="space-y-4">
        <div className="flex items-start justify-between gap-3">
          <span className="font-body text-[10px] font-bold tracking-widest text-ls-red">
            {sol.eyebrow}
          </span>
          <HonestyBadge label={sol.proof} />
        </div>
        <h3
          className={`text-xl font-bold tracking-tight font-display ${
            isLight ? 'text-ls-navy' : 'text-ls-white'
          }`}
        >
          {sol.title}
        </h3>
        <dl className="space-y-3">
          {SPEC_QUESTIONS.map(({ key, label }) => (
            <div key={key}>
              <dt
                className={`font-body text-[9px] font-bold tracking-widest ${
                  isLight ? 'text-ls-red' : 'text-ls-red'
                }`}
              >
                {label}
              </dt>
              <dd
                className={`text-xs leading-relaxed mt-0.5 ${
                  isLight ? 'text-ls-grey-dark font-medium' : 'text-ls-grey-light-text'
                }`}
              >
                {sol.spec[key]}
              </dd>
            </div>
          ))}
        </dl>
      </div>
      <div
        className={`pt-5 mt-5 border-t flex items-center justify-between ${
          isLight ? 'border-ls-grey-dark' : 'border-ls-white/10'
        }`}
      >
        <span
          className={`text-[11px] font-body font-bold tracking-widest group-hover:text-ls-red transition-colors ${
            isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
          }`}
        >
          DISCUSS THIS SOLUTION
        </span>
        <ArrowRight className="w-4 h-4 text-ls-red" aria-hidden="true" />
      </div>
    </Link>
  );
};

/**
 * /solutions hub. Lists the five detailed solution domains plus the
 * AI Governance & Policy domain (anchored under AI Company Builder).
 * Every card answers MASTER_SPEC §10's five questions with its honesty status.
 */
export const SolutionsPage: React.FC<SolutionsPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="WHAT WE DO"
        title="Solutions Built for the Work to Be Done"
        lead="Six domains cover the arc from strategy to shipped system: agentic AI, digital transformation, data & intelligence, intelligent automation, strategy & advisory, and the governance layer that makes deployment safe. Every card answers: what problem, who it's for, what changes, what we build, and what evidence exists — each claim carries its honesty status."
      />

      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 pb-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {solutions.map((sol, idx) => (
            <Reveal key={sol.slug} delay={idx * 0.06}>
              <SolutionCard sol={sol} theme={theme} to="/contact" />
            </Reveal>
          ))}

          {/* Governance & Policy domain card (anchored at AI Company Builder) */}
          <Reveal delay={solutions.length * 0.06}>
            <SolutionCard sol={GOVERNANCE_SOLUTION} theme={theme} to={GOVERNANCE_SOLUTION.to} />
          </Reveal>
        </div>
      </section>

      {/* Engagement model strip */}
      <section
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full py-16 sm:py-20 border-t ${
          isLight ? 'border-ls-grey-dark/80' : 'border-ls-grey-dark/80'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="HOW WE WORK"
          title="One Human CEO. A Governed Agent Workforce."
          lead="Strategy — Build — Govern — Scale. Every engagement passes four gates (G1 discovery → G2 architecture → G3 build → G4 handover) that map to a five-tier human-approval matrix. What ships is yours: sites, data, dashboards, and agents, with 30 days of support included."
        />
        <Reveal>
          <div
            className={`max-w-3xl mx-auto rounded-3xl p-6 sm:p-8 border ${
              isLight ? 'bg-ls-white/95 border-ls-grey-dark shadow-md' : 'bg-ls-navy/80 border-ls-white/15 shadow-xl'
            }`}
          >
            <ul
              className={`grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-3 text-sm leading-relaxed ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}
            >
              <li className="flex items-start gap-2">
                <span className="text-ls-red font-body font-black" aria-hidden="true">01</span>
                G1 DISCOVERY — a governed, 5-tier-approved conversation, not a product demo.
              </li>
              <li className="flex items-start gap-2">
                <span className="text-ls-red font-body font-black" aria-hidden="true">02</span>
                G2 ARCHITECTURE — target design, cost, and honesty on what we will and won't build.
              </li>
              <li className="flex items-start gap-2">
                <span className="text-ls-red font-body font-black" aria-hidden="true">03</span>
                G3 BUILD — 90-day pilot window, delivered against named outcomes.
              </li>
              <li className="flex items-start gap-2">
                <span className="text-ls-red font-body font-black" aria-hidden="true">04</span>
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
