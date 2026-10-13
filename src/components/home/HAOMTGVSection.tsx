import React from 'react';
import { Brain, Bot, GitBranch, HardDrive, Wrench, ShieldCheck, TrendingUp, type LucideIcon } from 'lucide-react';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';
import { HomeSection } from './HomeSection';

interface HAOMTGVSectionProps {
  theme: 'light' | 'dark';
}

interface Pillar {
  id: string;
  letter: string;
  title: string;
  description: string;
  Icon: LucideIcon;
}

/**
 * H-A-O-M-T-G-V operating philosophy. Not a linear pipeline — a control model
 * where human authority runs through every layer and governance is an
 * integral control layer (G), not a final checkpoint.
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
    description: 'Specialized AI roles with explicit scopes, tools, and approval thresholds — not a single general-purpose bot.',
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
    description: 'Persistent contextual state across long-running work — so agents recall before they act, not from a blank slate.',
    Icon: HardDrive,
  },
  {
    id: 'tools',
    letter: 'T',
    title: 'Tools',
    description: 'Isolated execution environments for APIs, data, and actions — the only way agents touch the outside world.',
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
    description: 'Measured business outcomes — cost, latency, quality, and adoption — fed back into strategy, not vanity metrics.',
    Icon: TrendingUp,
  },
];

/** Chapter 01 — the H-A-O-M-T-G-V operating philosophy. */
export const HAOMTGVSection: React.FC<HAOMTGVSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="haomtgv" label="H-A-O-M-T-G-V operating philosophy" theme={theme}>
      <SectionHeading
        theme={theme}
        eyebrow="OPERATING PHILOSOPHY"
        title="H-A-O-M-T-G-V"
        lead="How LightSpeed thinks about AI-native operations: Human authority through Agents, Orchestration, Memory, and Tools — with Governance as an integral control layer and Value as the only score that counts. Not a linear pipeline; a working model."
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {PILLARS.map((pillar, idx) => (
          <Reveal key={pillar.id} delay={idx * 0.04}>
            <article
              className={`h-full rounded-3xl p-5 border flex flex-col gap-3 ${
                isLight
                  ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
                  : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
              } ${pillar.id === 'governance' ? 'ring-1 ring-ls-red/30' : ''}`}
            >
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-3">
                  <span
                    aria-hidden="true"
                    className="flex w-10 h-10 items-center justify-center rounded-full border border-ls-red/40 bg-ls-red/10 font-display font-black text-ls-red text-lg"
                  >
                    {pillar.letter}
                  </span>
                  <h3 className="font-display font-bold text-base tracking-tight">{pillar.title}</h3>
                </div>
                <pillar.Icon className="w-4 h-4 text-ls-cyan" aria-hidden="true" />
              </div>
              <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                {pillar.description}
              </p>
            </article>
          </Reveal>
        ))}
      </div>
      <p className={`mt-6 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
        Human direction is not a checkpoint at the end — it is present at every layer. Governance (G) is how that authority stays enforceable when agents act at scale.
      </p>
    </HomeSection>
  );
};

export default HAOMTGVSection;
