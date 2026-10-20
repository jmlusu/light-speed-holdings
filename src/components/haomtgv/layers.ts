import { Brain, Bot, GitBranch, HardDrive, Wrench, ShieldCheck, TrendingUp, type LucideIcon } from 'lucide-react';

export interface HaomtgvLayer {
  id: string;
  letter: string;
  title: string;
  heroDescription: string;
  Icon: LucideIcon;
}

export const HAOMTGV_LAYERS: HaomtgvLayer[] = [
  {
    id: 'human',
    letter: 'H',
    title: 'Human',
    heroDescription: 'People set intent and hold final authority.',
    Icon: Brain,
  },
  {
    id: 'agents',
    letter: 'A',
    title: 'Agents',
    heroDescription: 'Specialized AI roles with explicit scopes.',
    Icon: Bot,
  },
  {
    id: 'orchestration',
    letter: 'O',
    title: 'Orchestration',
    heroDescription: 'Deterministic routing of tasks and decisions.',
    Icon: GitBranch,
  },
  {
    id: 'memory',
    letter: 'M',
    title: 'Memory',
    heroDescription: 'Persistent contextual state across long-running work.',
    Icon: HardDrive,
  },
  {
    id: 'tools',
    letter: 'T',
    title: 'Tools',
    heroDescription: 'Isolated execution environments for APIs and actions.',
    Icon: Wrench,
  },
  {
    id: 'governance',
    letter: 'G',
    title: 'Governance',
    heroDescription: 'Five-tier approval woven through every layer.',
    Icon: ShieldCheck,
  },
  {
    id: 'value',
    letter: 'V',
    title: 'Value',
    heroDescription: 'Measured business outcomes fed back into strategy.',
    Icon: TrendingUp,
  },
];
