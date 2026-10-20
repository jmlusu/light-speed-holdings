import React from 'react';
import { Brain, Bot, GitBranch, HardDrive, Wrench, ShieldCheck, TrendingUp, ArrowRight, type LucideIcon } from 'lucide-react';
import { Link } from 'react-router-dom';
import { SectionHeading } from '../components/site/SectionHeading';
import { Reveal } from '../components/Reveal';
import { RelatedLinks } from '../components/site/RelatedLinks';

interface HaomtgvPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

interface Pillar {
  id: string;
  letter: string;
  title: string;
  description: string;
  Icon: LucideIcon;
}

/**
 * Canonical 7-layer framework — text mirrors HAOMTGVSection.tsx:24.
 * Not a linear pipeline; a control model where human authority runs
 * through every layer and governance (G) is integral, not a checkpoint.
 */
const PILLARS: Pillar[] = [
  {
    id: 'human',
    letter: 'H',
    title: 'Human',
    description: 'People set intent, own outcomes, and hold final decision authority. Agents propose; humans decide what ships.',
    Icon: Brain,
  },
  {
    id: 'agents',
    letter: 'A',
    title: 'Agents',
    description: 'Specialized AI roles with explicit scopes, tools, and approval thresholds. Not a single general-purpose bot.',
    Icon: Bot,
  },
  {
    id: 'orchestration',
    letter: 'O',
    title: 'Orchestration',
    description: 'Deterministic routing of tasks, data, and decisions across workflows so multi-step work stays auditable end to end.',
    Icon: GitBranch,
  },
  {
    id: 'memory',
    letter: 'M',
    title: 'Memory',
    description: 'Persistent contextual state across long-running work, so agents recall before they act, not from a blank slate.',
    Icon: HardDrive,
  },
  {
    id: 'tools',
    letter: 'T',
    title: 'Tools',
    description: 'Isolated execution environments for APIs, data, and actions: the only way agents touch the outside world.',
    Icon: Wrench,
  },
  {
    id: 'governance',
    letter: 'G',
    title: 'Governance',
    description: 'A control layer woven through the model: five-tier human approval, append-only audit receipts, and risk-classified actions.',
    Icon: ShieldCheck,
  },
  {
    id: 'value',
    letter: 'V',
    title: 'Value',
    description: 'Measured business outcomes (cost, latency, quality, and adoption) fed back into strategy, not vanity metrics.',
    Icon: TrendingUp,
  },
];

const BRAND_BAR = ['#070A40', '#E63946', '#00BFFF'];

export const HaomtgvPage: React.FC<HaomtgvPageProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const cardBase = isLight
    ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl';

    {/*
     * AGENT TEAM NARRATIVE - HAOMTGVPage (7-Layer Framework)
     * Content fidelity governed by:
     *   - orchestration-owner | MessageBus task queue, agent coordination
     *   - governance-owner    | 5-tier approval matrix, H-A-O-M-T-G-V compliance
     *   - registry-owner      | canonical pillar data, company-registry.yaml mapping
     * Last audited: 2026-10-18
     */}
  return (
    <>
      {/* Hero */}
      <section
        className={`relative overflow-hidden border-b ${
          isLight ? 'bg-ls-navy text-ls-white' : 'bg-ls-navy text-ls-white'
        }`}
      >
        <div aria-hidden="true" className="absolute top-0 left-0 right-0 h-1 flex">
          {BRAND_BAR.map((color) => (
            <div key={color} className="flex-1" style={{ backgroundColor: color }} />
          ))}
        </div>
        <div className="max-w-4xl mx-auto px-6 py-20 sm:py-28 text-center space-y-6">
          <span className="text-xs font-body font-bold tracking-widest text-ls-red">
            OPERATING FRAMEWORK
          </span>
          <h1
            id="haomtgv-title"
            className="text-4xl sm:text-6xl font-black tracking-[0.2em] font-display text-ls-cyan"
          >
            H-A-O-M-T-G-V
          </h1>
          <p className="text-sm sm:text-lg leading-relaxed text-ls-grey-light-text max-w-2xl mx-auto">
            Human authority through Agents, Orchestration, Memory, and Tools —
            with Governance as an integral control layer and Value as the only
            score that counts. Not a linear pipeline; a working model.
          </p>
          <Link
            to="/ai-company-builder/#governance"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-ls-red text-ls-white font-bold text-sm tracking-wide hover:brightness-110 transition-all"
          >
            Explore the Framework
            <ArrowRight className="w-4 h-4" aria-hidden="true" />
          </Link>
        </div>
      </section>

      {/* 7-layer grid */}
      <section className={`py-16 sm:py-24 ${isLight ? 'bg-ls-white' : 'bg-ls-navy-dark'}`}>
        <div className="max-w-6xl mx-auto px-6">
          <SectionHeading
            theme={theme}
            eyebrow="THE SEVEN LAYERS"
            title="How the Model Works"
            lead="Each layer has a distinct role. Human direction is present at every layer — not saved for the end."
          />
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {PILLARS.map((pillar, idx) => (
              <Reveal key={pillar.id} delay={idx * 0.04}>
                <article
                  className={`h-full rounded-3xl p-5 border flex flex-col gap-3 transition-transform hover:-translate-y-1 duration-300 ${cardBase} ${
                    pillar.id === 'governance' ? 'ring-1 ring-ls-red/30' : ''
                  }`}
                >
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-3">
                      <span
                        aria-hidden="true"
                        className="flex w-10 h-10 items-center justify-center rounded-full border border-ls-red/40 bg-ls-red/10 font-display font-black text-ls-red text-lg"
                      >
                        {pillar.letter}
                      </span>
                      <h3 className="font-display font-bold text-base tracking-tight">
                        {pillar.title}
                      </h3>
                    </div>
                    <pillar.Icon className="w-4 h-4 text-ls-cyan" aria-hidden="true" />
                  </div>
                  <p
                    className={`text-xs leading-relaxed ${
                      isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                    }`}
                  >
                    {pillar.description}
                  </p>
                </article>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* Governance callout */}
      <section className={`py-16 ${isLight ? 'bg-ls-navy/5' : 'bg-ls-navy-dark'}`}>
        <div className="max-w-3xl mx-auto px-6 text-center space-y-4">
          <h2
            className={`text-xl sm:text-2xl font-black font-display ${
              isLight ? 'text-ls-navy' : 'text-ls-white'
            }`}
          >
            Governance Runs Through Every Layer
          </h2>
          <p
            className={`text-sm leading-relaxed ${
              isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
            }`}
          >
            Human direction is not a checkpoint at the end. It is present at
            every layer. Governance (G) is how that authority stays enforceable
            when agents act at scale.
          </p>
        </div>
      </section>

      {/* Brand color bar */}
      <div aria-hidden="true" className="h-1 flex">
        {BRAND_BAR.map((color) => (
          <div key={color} className="flex-1" style={{ backgroundColor: color }} />
        ))}
      </div>

      <RelatedLinks
        theme={theme}
        links={[
          { to: '/ai-company-builder', label: 'AI Company Builder' },
          { to: '/solutions', label: 'Solutions' },
          { to: '/insights', label: 'Insights' },
        ]}
      />
    </>
  );
};

export default HaomtgvPage;
