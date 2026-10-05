/* Capabilities registry — MASTER_SPEC §15.
 * Canonical source for the four operating-model capabilities.
 * Consumed by home OperatingModelSection; company.valueCycle derives from here. */

export interface Capability {
  id: string;
  title: string;
  description: string;
  icon: string;
}

export const CAPABILITIES: readonly Capability[] = [
  {
    id: 'strategy',
    title: 'Strategy',
    description: 'Turn organizational priorities into executable strategies, operating models, roadmaps, and AI opportunities.',
    icon: '🎯',
  },
  {
    id: 'build',
    title: 'Build',
    description: 'Design and build AI-native workflows, applications, agentic systems, data products, automation, and digital operating capabilities.',
    icon: '🔨',
  },
  {
    id: 'govern',
    title: 'Govern',
    description: 'Establish controls, architecture, policies, standards, risk management, security, data governance, and decision rights for responsible AI adoption.',
    icon: '🛡️',
  },
  {
    id: 'research-policy',
    title: 'Research & Policy',
    description: 'Develop evidence, research, market intelligence, policy analysis, and practical guidance for AI adoption in Malawi and Africa.',
    icon: '📊',
  },
];

export const capabilityTitles: readonly string[] = CAPABILITIES.map((c) => c.title);
