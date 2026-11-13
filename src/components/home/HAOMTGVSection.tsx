import React from 'react';
import { Link } from 'react-router-dom';
import { Brain, Bot, GitBranch, HardDrive, Wrench, ShieldCheck, TrendingUp, type LucideIcon } from 'lucide-react';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';
import { HomeSection } from './HomeSection';
import { HAOMTGVVisualization } from './HAOMTGVVisualization';

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
 * H-A-O-M-T-G-V operating philosophy. Not a linear pipeline - a control model
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

/** Chapter 01 - the H-A-O-M-T-G-V operating philosophy. */
export const HAOMTGVSection: React.FC<HAOMTGVSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <section
      id="haomtgv"
      aria-label="H-A-O-M-T-G-V operating philosophy"
      tabIndex={-1}
      className={`relative w-full py-[100px] px-6 lg:px-12 scroll-mt-28 overflow-hidden transition-colors duration-300 ${
        isLight ? 'bg-[#F7F8F9] text-ls-navy' : 'bg-[#070A40] text-white'
      }`}
    >
      {/* Background Brand and Hero Visual */}
      <div className="absolute inset-0 z-0 pointer-events-none select-none overflow-hidden">
        <img
          src="/brand/digital/LightSpeed brand and hero visual.jpeg"
          alt="LightSpeed brand and hero visual"
          className="w-full h-full object-cover object-center transition-all duration-700 opacity-75 dark:opacity-85 filter saturate-110 brightness-100"
          loading="lazy"
        />
        {/* Atmosphere Scrim Overlay (Lightened for enhanced image clarity) */}
        <div
          className={`absolute inset-0 transition-colors duration-500 ${
            isLight
              ? 'bg-gradient-to-b from-[#F7F8F9]/65 via-[#F7F8F9]/35 to-[#F7F8F9]/65'
              : 'bg-gradient-to-b from-[#070A40]/70 via-[#070A40]/45 to-[#070A40]/70'
          }`}
        />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto w-full">
        <SectionHeading
          theme={theme}
          eyebrow="OPERATING PHILOSOPHY"
          title="H-A-O-M-T-G-V"
          lead="How LightSpeed thinks about AI-native operations: Human authority through Agents, Orchestration, Memory, and Tools, with Governance as an integral control layer and Value as the only score that counts. Not a linear pipeline; a working model."
        />
        <div className="mt-12 mb-12">
          <HAOMTGVVisualization theme={theme} />
        </div>

        <p className={`mt-6 text-xs leading-relaxed ${isLight ? 'text-slate-600 font-medium' : 'text-[#9CA3AF]'}`}>
          Human direction is not a checkpoint at the end. It is present at every layer. Governance (G) is how that authority stays enforceable when agents act at scale.
        </p>
        <div className="mt-4">
          <Link
            to="/haomtgv"
            className="inline-flex items-center gap-1.5 font-body text-[11px] font-bold tracking-widest uppercase text-[#00BFFF] transition-colors hover:text-[#DC3641]"
          >
            Explore the full framework →
          </Link>
        </div>
      </div>
    </section>
  );
};

export default HAOMTGVSection;
