/* Homepage copy & asset constants — Prompt 09 / Appendix A token palette.
 * Single source of truth for copy mapped to the redesigned home page sections.
 * All tokens referenced are verified against brand-tokens.json (navy #070A40, red #DC3641, cyan #00BFFF).
 */

export type PathwayCard = {
  id: string;
  title: string;
  intent: string;
  body: string;
  primaryLabel: string;
  primaryTo: string;
  secondaryLabels: { label: string; to: string }[];
  status?: string;
};

export type SolutionCard = {
  id: string;
  title: string;
  description: string;
  status: 'IN DEVELOPMENT' | 'PILOT' | 'PROTOTYPE' | 'IN-HOUSE' | 'EXPLORATION';
};

export type ArticleCard = {
  id: string;
  category: string;
  title: string;
  slug: string;
  excerpt: string;
  readTime: string;
};

export const pathwayCards: PathwayCard[] = [
  {
    id: 'business-leaders',
    title: 'Business Leaders',
    intent: 'I lead a team and need AI to deliver measurable outcomes',
    body: 'Start with the outcome you need. Each solution maps to real-world results — cost reduction, latency improvement, or adoption velocity — and links to the sectors where it applies.',
    primaryLabel: 'Explore Solutions',
    primaryTo: '/solutions',
    secondaryLabels: [
      { label: 'How we work', to: '/what-we-do' },
      { label: 'Case studies', to: '/case-studies' },
    ],
  },
  {
    id: 'partners',
    title: 'Partners',
    intent: 'I partner with LightSpeed to co-build AI capabilities',
    body: 'Review the use cases and evidence status, then start a conversation: an executive briefing, an AI readiness assessment, or a direct enquiry about co-development.',
    primaryLabel: 'View Solutions',
    primaryTo: '/solutions',
    secondaryLabels: [
      { label: 'Start a conversation', to: '/contact' },
      { label: 'Browse solutions', to: '/solutions' },
    ],
  },
  {
    id: 'researchers',
    title: 'Researchers',
    intent: 'I study AI-native operating models and frameworks',
    body: 'Walk the H-A-O-M-T-G-V operating model: the control layer, governance integration, and value measurement fed back into strategy, not vanity metrics.',
    primaryLabel: 'Explore the Framework',
    primaryTo: '/haomtgv',
    secondaryLabels: [
      { label: 'Memory and tools', to: '#memory-tools' },
      { label: 'Governance details', to: '#governance' },
    ],
  },
  {
    id: 'policy-makers',
    title: 'Policy Makers',
    intent: 'I shape policy for AI governance and adoption',
    body: 'Review our evidence-based approach to AI governance, including human authority through every layer, append-only audit receipts, and risk-classified actions.',
    primaryLabel: 'Understand Our Approach',
    primaryTo: '/haomtgv',
    secondaryLabels: [
      { label: 'Framework details', to: '/haomtgv' },
      { label: 'Contact us', to: '/contact' },
    ],
  },
];

export const solutionsGrid: SolutionCard[] = [
  {
    id: 'sol-1',
    title: 'Customer Intelligence',
    description: 'Real-time analysis of customer signals to surface actionable insights.',
    status: 'IN DEVELOPMENT',
  },
  {
    id: 'sol-2',
    title: 'Predictive Maintenance',
    description: 'AI-driven forecasting to reduce downtime and optimize maintenance schedules.',
    status: 'PILOT',
  },
  {
    id: 'sol-3',
    title: 'Supply Chain Orchestration',
    description: 'End-to-end visibility and automation of logistics and fulfillment.',
    status: 'PROTOTYPE',
  },
  {
    id: 'sol-4',
    title: 'Revenue Operations',
    description: 'Unified data layer for forecasting, pricing, and deal acceleration.',
    status: 'IN-HOUSE',
  },
  {
    id: 'sol-5',
    title: 'Risk Guard',
    description: 'Automated compliance monitoring and risk classification for regulated industries.',
    status: 'EXPLORATION',
  },
  {
    id: 'sol-6',
    title: 'Talent Match',
    description: 'AI-powered matching of talent to project roles based on skills and availability.',
    status: 'EXPLORATION',
  },
];

export const pharosTeaser: ArticleCard[] = [
  {
    id: 'art-1',
    category: 'STRATEGY',
    title: 'The H-A-O-M-T-G-V Operating Model in Practice',
    slug: 'haomtgv-in-practice',
    excerpt: 'How leading enterprises are implementing the control-layer framework for AI-native operations.',
    readTime: '6 min read',
  },
  {
    id: 'art-2',
    category: 'GOVERNANCE',
    title: 'Human Authority at Scale: Governance That Works',
    slug: 'human-authority-scale',
    excerpt: 'A control layer woven through the model: five-tier human approval, append-only audit receipts, and risk-classified actions.',
    readTime: '5 min read',
  },
  {
    id: 'art-3',
    category: 'WAVEFORM',
    title: 'Measuring What Matters: Value Over vanity Metrics',
    slug: 'measuring-value',
    excerpt: 'Cost, latency, quality, and adoption fed back into strategy — the only score that counts.',
    readTime: '4 min read',
  },
];
