import {
  Brain,
  Bot,
  GitBranch,
  HardDrive,
  Wrench,
  ShieldCheck,
  TrendingUp,
  type LucideIcon,
} from 'lucide-react';

export interface HaomtgvLayer {
  id: string;
  letter: string;
  title: string;
  description: string;
  heroDescription: string;
  Icon: LucideIcon;
}

export const HAOMTGV_LAYERS: HaomtgvLayer[] = [
  {
    id: 'human',
    letter: 'H',
    title: 'Human',
    description:
      'People set intent, own outcomes, and hold final decision authority. Agents propose; humans decide what ships.',
    heroDescription: 'People set intent and hold final decision authority.',
    Icon: Brain,
  },
  {
    id: 'agents',
    letter: 'A',
    title: 'Agents',
    description:
      'Specialized AI roles with explicit scopes, tools, and approval thresholds. Not a single general-purpose bot.',
    heroDescription: 'Specialized roles with explicit scopes and limits.',
    Icon: Bot,
  },
  {
    id: 'orchestration',
    letter: 'O',
    title: 'Orchestration',
    description:
      'Deterministic routing of tasks, data, and decisions across workflows so multi-step work stays auditable end to end.',
    heroDescription: 'Deterministic routing keeps every step auditable.',
    Icon: GitBranch,
  },
  {
    id: 'memory',
    letter: 'M',
    title: 'Memory',
    description:
      'Persistent contextual state across long-running work, so agents recall before they act, not from a blank slate.',
    heroDescription: 'Persistent context: agents recall before they act.',
    Icon: HardDrive,
  },
  {
    id: 'tools',
    letter: 'T',
    title: 'Tools',
    description:
      'Isolated execution environments for APIs, data, and actions: the only way agents touch the outside world.',
    heroDescription: 'Isolated execution for APIs, data, and real actions.',
    Icon: Wrench,
  },
  {
    id: 'governance',
    letter: 'G',
    title: 'Governance',
    description:
      'A control layer woven through the model: five-tier human approval, append-only audit receipts, and risk-classified actions.',
    heroDescription: 'Five-tier human approval over every risky action.',
    Icon: ShieldCheck,
  },
  {
    id: 'value',
    letter: 'V',
    title: 'Value',
    description:
      'Measured business outcomes (cost, latency, quality, and adoption) fed back into strategy, not vanity metrics.',
    heroDescription: 'Outcomes measured in cost, latency, quality, adoption.',
    Icon: TrendingUp,
  },
];
