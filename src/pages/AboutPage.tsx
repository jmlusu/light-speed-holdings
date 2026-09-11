import React from 'react';
import { Check, Globe2, Network, ShieldCheck } from 'lucide-react';
import { FaqSection } from '../components/FaqSection';

interface AboutPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

type EvidenceStatus = 'PROVEN IN-HOUSE' | 'IN PILOT';

interface AuthorityCard {
  icon: React.ComponentType<{ className?: string }>;
  eyebrow: string;
  title: string;
  status: EvidenceStatus;
  bullets: string[];
}

const AUTHORITY_CARDS: AuthorityCard[] = [
  {
    icon: Network,
    eyebrow: 'FLEET ARCHITECTURE',
    title: 'Structured Agent Fleet',
    status: 'PROVEN IN-HOUSE',
    bullets: [
      '144 agent configurations live in company-registry.yaml.',
      'Every agent is bound to the canonical 7-tool runtime.',
      'All approvals pass Title-IX-style governance gates.',
    ],
  },
  {
    icon: ShieldCheck,
    eyebrow: 'GOVERNANCE CONTROL',
    title: 'Regulatory-Grade Governance',
    status: 'PROVEN IN-HOUSE',
    bullets: [
      '5-tier human approval matrix (ApprovalGate) with expiry sweeps.',
      'Immutable SHA-256 audit trail on every agent action.',
      'X-API-Key RBAC on the control-plane dashboard.',
    ],
  },
  {
    icon: Globe2,
    eyebrow: 'REGIONAL POSITION',
    title: 'Malawi / SADC Regional Position',
    status: 'IN PILOT',
    bullets: [
      "Targeted at Malawi's National AI Strategy consultation.",
      'Engaged with the SADC Agentic AI Governance Framework.',
      'Speaker engagements underway across the region.',
    ],
  },
];

interface Pillar {
  term: string;
  sentence: string;
}

const PILLARS: Pillar[] = [
  {
    term: 'SME Operations',
    sentence: 'Agentic decision support for pricing, inventory, cash reconciliation, and procurement in non-tech businesses running on real constraints.',
  },
  {
    term: 'Health and M&E',
    sentence: 'Automated monitoring and evaluation, supply-chain anomaly detection, and donor reporting where accuracy is not optional.',
  },
  {
    term: 'Financial Inclusion',
    sentence: 'Agentic workflows over mobile-money rails and informal savings groups, designed for the infrastructure people actually use.',
  },
  {
    term: 'Public Services',
    sentence: 'Citizen-query agents, legislative summarization, and project monitoring that meet government accountability standards.',
  },
];

const STATUS_STYLES: Record<EvidenceStatus, string> = {
  'PROVEN IN-HOUSE': 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan',
  'IN PILOT': 'border-ls-red/40 bg-ls-red/10 text-ls-red',
};

/**
 * About route: establishes trust before the FAQ by leading with an
 * "Authority & Governance" band of honestly-labeled capability cards.
 */
export const AboutPage: React.FC<AboutPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      {/* Page Intro */}
      <header className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-24 pb-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
          <span>ABOUT THE FIRM</span>
        </div>
        <h1 className={`mt-4 text-3xl sm:text-5xl font-black tracking-tight font-display ${
          isLight ? 'text-slate-900' : 'text-white'
        }`}>
          An Agentic AI Company That Ships
        </h1>
        <p className={`mt-4 max-w-2xl text-sm sm:text-base leading-relaxed ${
          isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
        }`}>
          Malawi-rooted and SADC-focused, we design, govern, and ship working agentic AI systems with human approval gates and a verifiable audit trail at every step. Our own company runs on the same infrastructure we offer clients — 144 agents across 20 departments, governed, auditable, and held to the same five-tier standards we build for you.
        </p>
      </header>

      {/* Mission & Vision */}
      <section
        aria-labelledby="mission-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full py-16 sm:py-20 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <div className="max-w-3xl mx-auto text-center space-y-3">
          <span className="text-xs font-mono font-bold tracking-widest text-ls-red">
            MISSION AND VISION
          </span>
          <h2
            id="mission-heading"
            className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}
          >
            Where AI Meets Accountability
          </h2>
        </div>

        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className={`rounded-3xl p-6 sm:p-8 space-y-4 border ${
            isLight ? 'bg-white/95 border-slate-300 shadow-md text-slate-900' : 'bg-zinc-950/80 border-white/15 shadow-xl text-zinc-300'
          }`}>
            <span className="text-xs font-mono font-bold tracking-widest text-ls-red">
              MISSION
            </span>
            <p className={`text-justify text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
            }`}>
              LightSpeed Holdings builds agentic AI systems where software performs meaningful organizational work and humans remain accountable for what matters. We design, govern, and ship operating infrastructure for autonomous AI — not prototypes, not slide decks. Our platform runs 144 agents across 20 departments, governed by five-tier human approval and immutable audit trails, because the only AI worth deploying is AI you can trace.
            </p>
          </div>

          <div className={`rounded-3xl p-6 sm:p-8 space-y-4 border ${
            isLight ? 'bg-white/95 border-slate-300 shadow-md text-slate-900' : 'bg-zinc-950/80 border-white/15 shadow-xl text-zinc-300'
          }`}>
            <span className="text-xs font-mono font-bold tracking-widest text-ls-cyan">
              VISION
            </span>
            <p className={`text-justify text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
            }`}>
              Malawi and the SADC region can lead in AI-native institutional design — not by importing solutions built elsewhere, but by building governed, evidence-based systems from the ground up. LightSpeed exists to prove that governance-first, offline-first, sovereign-by-design AI is not a constraint on capability. It is the architecture that earns trust, and trust is what scales.
            </p>
          </div>
        </div>

        <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          {PILLARS.map((pillar) => (
            <article
              key={pillar.term}
              className={`rounded-2xl border p-5 sm:p-6 ${
                isLight ? 'bg-white border-slate-200 text-slate-900' : 'bg-zinc-900/60 border-zinc-800 text-zinc-100'
              }`}
            >
              <h3 className="font-display font-bold text-sm sm:text-base tracking-tight">
                {pillar.term}
              </h3>
              <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${
                isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
              }`}>
                {pillar.sentence}
              </p>
            </article>
          ))}
        </div>

        <p className={`mt-12 text-center text-sm sm:text-base leading-relaxed ${
          isLight ? 'text-slate-600 font-medium' : 'text-zinc-400'
        }`}>
          The systems are running. The governance is in place.{' '}
          <span className="font-bold text-ls-cyan">The work continues.</span>
        </p>
      </section>

      {/* Authority & Governance Band */}
      <section
        aria-labelledby="authority-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full py-16 sm:py-20 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <div className="text-center max-w-3xl mx-auto mb-12 space-y-3">
          <span className="text-xs font-mono font-bold tracking-widest text-ls-red">
            AUTHORITY &amp; GOVERNANCE
          </span>
          <h2
            id="authority-heading"
            className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}
          >
            What We Can Prove Today
          </h2>
          <p className={`text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            Every claim carries its evidence status — proven in-house, or in pilot. We do not blur the two.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {AUTHORITY_CARDS.map((card) => {
            const Icon = card.icon;
            return (
              <article
                key={card.title}
                className={`relative overflow-hidden rounded-3xl p-6 sm:p-8 ${
                  isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
                }`}
              >
                {/* Hardware corner screws */}
                <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
                <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
                <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
                <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

                <div className="flex items-start justify-between gap-3">
                  <span className="font-mono text-[10px] font-bold tracking-widest text-ls-red">
                    {card.eyebrow}
                  </span>
                  <span className={`shrink-0 rounded-full border px-2.5 py-0.5 font-mono text-[9px] font-bold tracking-widest ${STATUS_STYLES[card.status]}`}>
                    {card.status}
                  </span>
                </div>

                <div className="mt-4 flex items-center gap-2.5">
                  <span aria-hidden="true">
                    <Icon className="w-5 h-5 text-ls-cyan" />
                  </span>
                  <h3 className={`text-xl font-bold tracking-tight font-display ${
                    isLight ? 'text-slate-900' : 'text-zinc-100'
                  }`}>
                    {card.title}
                  </h3>
                </div>

                <ul className="mt-4 space-y-2">
                  {card.bullets.map((bullet) => (
                    <li key={bullet} className="flex items-start gap-2 text-xs sm:text-sm leading-relaxed">
                      <Check className="mt-0.5 w-3.5 h-3.5 shrink-0 text-ls-red" aria-hidden="true" />
                      <span className={isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'}>
                        {bullet}
                      </span>
                    </li>
                  ))}
                </ul>
              </article>
            );
          })}
        </div>
      </section>

      <FaqSection theme={theme} />
    </>
  );
};

export default AboutPage;
