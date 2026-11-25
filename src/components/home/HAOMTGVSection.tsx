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
    description: 'Authority starts with a named person and stays there. Humans set intent, own outcomes, and sign off on anything irreversible; agents are delegates, never principals. Delegation is revocable by design. The human is the last line of code in the organization.',
    Icon: Brain,
  },
  {
    id: 'agents',
    letter: 'A',
    title: 'Agents',
    description: 'The machine side is a roster, not a single "AI." Every agent is a role-bounded persona with an explicit domain, a declared toolset, and a deterministic escalation path. When work exceeds scope, the agent escalates — it does not improvise.',
    Icon: Bot,
  },
  {
    id: 'orchestration',
    letter: 'O',
    title: 'Orchestration',
    description: 'Work does not happen off-script. Tasks move through a message bus with an owner, a lifecycle, and a failure path; the organization itself — departments, budgets, data classifications — is encoded as enforceable schema. "Is this allowed?" becomes a query, not a meeting.',
    Icon: GitBranch,
  },
  {
    id: 'memory',
    letter: 'M',
    title: 'Memory',
    description: 'Two obligations share this pillar. Inference runs on soil we control, with local fallbacks and a circuit breaker, so the company does not export its operations to a cloud it cannot govern. And the company remembers: decisions, context, and lessons are captured in structured memory so it does not relearn the same lesson on every new task. Sovereignty is a deployment property. Memory is an operating habit.',
    Icon: HardDrive,
  },
  {
    id: 'tools',
    letter: 'T',
    title: 'Tools',
    description: 'An agent\'s world is a closed set of primitives: read, edit, grep, list, bash, webfetch, task. No arbitrary code execution, no hidden gateways. The runtime refuses anything outside the list — which is what makes "what can this agent do?" a finite, reviewable question, and governance a property of execution rather than a policy document.',
    Icon: Wrench,
  },
  {
    id: 'governance',
    letter: 'G',
    title: 'Governance',
    description: 'Control happens before the action, not after the incident. Every proposal is checked against thresholds, budgets, and covenants before an external write event fires, with deterministic states — pending, approved, rejected, expired — and a sweep that clears stale approvals. Post-hoc review is archaeology, not governance.',
    Icon: ShieldCheck,
  },
  {
    id: 'value',
    letter: 'V',
    title: 'Value',
    description: 'Every prompt, tool call, human decision, and response is written to a cryptographic hash chain. Audit is a byproduct of running the company, not a quarterly exercise. Above the trail, cost, productivity, service delivery, and impact are measured against KPIs with honest status. Seven layers of control exist for one reason: value that is real, attributable, and provable to the people it serves — demonstrated, not merely promised.',
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
          lead="How LightSpeed thinks about AI-native operations. The seven callouts are: Humans authorize, Agents act, Orchestration orders, Memory persists, Tools stay sandboxed, Governance gates, Value verified. Not a linear pipeline; a working model."
        />
        <div className="mt-12 mb-12">
          <HAOMTGVVisualization theme={theme} />
        </div>

        <p className={`mt-6 text-xs leading-relaxed ${isLight ? 'text-slate-600 font-medium' : 'text-[#9CA3AF]'}`}>
          Human direction is not a checkpoint at the end. It is present at every layer. Governance gates high-impact moves and keeps that authority enforceable when agents act at scale.
        </p>
        <div className="mt-4">
          <Link
            to="/haomtgv"
            className="inline-flex items-center gap-1.5 font-body text-[11px] font-bold tracking-widest uppercase text-[#00BFFF] transition-colors hover:text-[#E63946]"
          >
            Explore the full framework →
          </Link>
        </div>
      </div>
    </section>
  );
};

export default HAOMTGVSection;
