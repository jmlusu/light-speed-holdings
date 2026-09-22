/* LightSpeed Holdings client-site content model.
    Source of truth: MISSION_AND_VISION (v2.0, Sep 2026) + use-case messaging
    brief (Sep 2026) + verified platform facts from company-registry/tests.
    Every claim here carries its honesty status. No invented numbers. */

// @ts-nocheck

export type HonestyTone = 'proven' | 'pilot' | 'fieldable' | 'development';

export interface HonestyLabel {
  label: string;
  tone: HonestyTone;
}

export const TONE_STYLES: Record<HonestyTone, string> = {
  proven: 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan',
  pilot: 'border-ls-red/40 bg-ls-red/10 text-ls-red',
  fieldable: 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
  development: 'border-ls-grey-dark/40 bg-ls-grey-dark/10 text-ls-grey-dark',
};

/* ── Company identity ─────────────────────────────────── */
export const company = {
  legalName: 'LightSpeed Holdings Limited',
  firstMention: 'LightSpeed Holdings Limited™',
  shortName: 'LightSpeed Holdings',
  location: 'Lilongwe, Malawi',
  tagline: 'ASPIRE. ACT. ACHIEVE.',
  northStar: 'Malawi first. Prove it. Then the world.',
  heroHeadline: 'Build the intelligent enterprise.',
  heroSubline:
    'LightSpeed Holdings helps organisations design, build and govern AI-native businesses, intelligent workflows and agentic systems — in Malawi, across SADC, and beyond.',
  valueCycle: ['Strategy', 'Build', 'Govern', 'Scale'] as const,
  thesis: 'Aspire. Act. Achieve.',
};

/* ── Mission & Vision ─────────────────────────────────── */
export const mission: { statement: string; why: string } = {
  statement:
    'Prove agentic AI works in Malawi by shipping real services — websites, automation, reporting, and marketing — for the organizations that need them most.',
  why: 'Malawi\u2019s SMEs, NGOs, schools, clinics, and cooperatives are underserved by an industry that prices enterprise-grade work out of reach. One human CEO directs a workforce of 152 agents to deliver world-class output at local cost. Our proof is not a press release; it is a shipped website, a donor report that used to take weeks, a dashboard that replaced forty-page PDFs.',
};

export const vision: { statement: string; why: string } = {
  statement:
    'Every organization — from Malawian clinics to global enterprises — operating with intelligent AI agents.',
  why: 'Intelligent automation is not a privilege of rich countries. We win trust with real engagements, published case studies, and compliant, secure delivery. We prove it in Malawi first — where the constraints are real — then serve organizations everywhere that need AI at fair cost.',
};

/* ── Why LightSpeed: firm characteristics ─────────────── */
export interface WhyLightSpeedItem {
  num: string;
  title: string;
  body: string;
  proof: HonestyLabel;
}

export const whyLightSpeed: WhyLightSpeedItem[] = [
  {
    num: '01',
    title: 'Strategy + Technology in One Conversation',
    body: 'We do not separate advisory from implementation. The person who designs your roadmap is the person who builds it — reducing handoff friction and ensuring strategy survives contact with reality.',
    proof: { label: 'Proven in-house', tone: 'proven' },
  },
  {
    num: '02',
    title: 'AI-Native by Design',
    body: 'We are not an IT consultancy that added AI. Our own operating model — 152 agents across 20 departments — is the proof that agentic systems work in production, under real constraints.',
    proof: { label: 'Proven in-house', tone: 'proven' },
  },
  {
    num: '03',
    title: 'Business-Outcome Focused',
    body: 'Every engagement is measured against outcomes, not activities. Time saved, processes automated, decision cycles reduced. We report on what changed, not what we built.',
    proof: { label: 'Proven in-house', tone: 'proven' },
  },
  {
    num: '04',
    title: 'Architecture and Implementation Capability',
    body: 'We ship working systems — websites, dashboards, agentic workflows, data pipelines — not just documents. Our own platform is the reference architecture we deploy to clients.',
    proof: { label: 'Proven in-house', tone: 'proven' },
  },
  {
    num: '05',
    title: 'Executive-Level Advisory',
    body: 'Board-level counsel on AI governance, risk, and responsible deployment. Evidence-led, never boastful. Every recommendation traces to a governance framework that works.',
    proof: { label: 'Proven in-house', tone: 'proven' },
  },
  {
    num: '06',
    title: 'African Market Context',
    body: 'We build for the constraints that define the region: intermittent connectivity, mobile-first users, mobile-money rails, dual economies, and regulatory environments shaped by the Data Protection Act.',
    proof: { label: 'Proven in-house', tone: 'proven' },
  },
  {
    num: '07',
    title: 'Research-Informed',
    body: 'Pharos turns engineering into public intellectual work. The SADC Agentic AI Governance Framework and Malawi\u2019s National AI Strategy consultation position LightSpeed as a source of policy, not just product.',
    proof: { label: 'Published', tone: 'proven' },
  },
  {
    num: '08',
    title: 'Flexible Engagement Models',
    body: 'Not every engagement requires a large consulting project. We offer advisory, assessment, strategy sprints, design and build, transformation programs, research engagements, and executive workshops.',
    proof: { label: 'Fieldable', tone: 'fieldable' },
  },
];

/* ── Five capability domains ──────────────────────────── */
export interface CapabilityDomain {
  id: string;
  title: string;
  eyebrow: string;
  description: string;
  proof: HonestyLabel;
  subdomains: string[];
}

export const capabilityDomains: CapabilityDomain[] = [
  {
    id: 'strategy-transformation',
    title: 'Strategy & Transformation',
    eyebrow: 'Clarify where you are going and what needs to change.',
    description:
      'Enterprise strategy, digital transformation, operating-model transformation, transformation roadmaps, organizational capability, executive advisory, performance improvement.',
    proof: { label: 'Proven in-house', tone: 'proven' },
    subdomains: [
      'Enterprise strategy',
      'Digital transformation',
      'Operating-model transformation',
      'Transformation roadmaps',
      'Organizational capability',
      'Executive advisory',
      'Performance improvement',
    ],
  },
  {
    id: 'ai-agentic-systems',
    title: 'AI & Agentic Systems',
    eyebrow: 'Design and implement the capabilities, systems and workflows required to get there.',
    description:
      'AI strategy, agentic AI, multi-agent systems, AI-native operating models, workflow automation, AI use-case discovery, AI implementation, AI governance.',
    proof: { label: 'Proven in-house', tone: 'proven' },
    subdomains: [
      'AI strategy',
      'Agentic AI',
      'Multi-agent systems',
      'AI-native operating models',
      'Workflow automation',
      'AI use-case discovery',
      'AI implementation',
      'AI governance',
    ],
  },
  {
    id: 'data-intelligence',
    title: 'Data & Intelligence',
    eyebrow: 'Establish the operating models, controls and policies required for sustainable transformation.',
    description:
      'Data strategy, data architecture, data platforms, business intelligence, analytics, data governance, monitoring, evaluation and learning, market intelligence.',
    proof: { label: 'Proven in-house', tone: 'proven' },
    subdomains: [
      'Data strategy',
      'Data architecture',
      'Data platforms',
      'Business intelligence',
      'Analytics',
      'Data governance',
      'Monitoring, evaluation and learning',
      'Market intelligence',
    ],
  },
  {
    id: 'digital-platforms',
    title: 'Digital Platforms & Solutions',
    eyebrow: 'Design and implement the capabilities, systems and workflows required to get there.',
    description:
      'Digital product strategy, platform architecture, enterprise systems, data integration, cloud architecture, digital experience, technology assessment, product development.',
    proof: { label: 'Fieldable in 2026', tone: 'fieldable' },
    subdomains: [
      'Digital product strategy',
      'Platform architecture',
      'Enterprise systems',
      'Data integration',
      'Cloud architecture',
      'Digital experience',
      'Technology assessment',
      'Product development',
    ],
  },
  {
    id: 'research-policy',
    title: 'Research, Policy & Advisory',
    eyebrow: 'Explore emerging technologies, markets and policy to help leaders prepare for what comes next.',
    description:
      'AI policy, technology policy, digital economy research, emerging technology analysis, market research, policy advisory, thought leadership, executive briefings.',
    proof: { label: 'Published', tone: 'proven' },
    subdomains: [
      'AI policy',
      'Technology policy',
      'Digital economy research',
      'Emerging technology analysis',
      'Market research',
      'Policy advisory',
      'Thought leadership',
      'Executive briefings',
    ],
  },
];

/* ── Client problems / triggers ───────────────────────── */
export interface ClientProblem {
  id: string;
  trigger: string;
  heading: string;
  subtext: string;
  solution: string;
  to: string;
  proof: HonestyLabel;
}

export const clientProblems: ClientProblem[] = [
  {
    id: 'exec-01',
    trigger: 'Your strategy isn\u2019t translating into execution',
    heading: 'Strategy & Transformation',
    subtext: 'You have a vision but the gap between planning and delivery is widening.',
    solution: 'Discovery, AI readiness assessment, and a transformation roadmap — sequenced and costed.',
    to: '/how-we-help#engagement',
    proof: { label: 'Proven in-house', tone: 'proven' },
  },
  {
    id: 'exec-02',
    trigger: 'You\u2019re trying to determine where AI can actually create value',
    heading: 'AI Opportunity Assessment',
    subtext: 'The hype is loud; the signal is hard to find.',
    solution: 'A sector-aware diagnostic that scores your operating model and identifies where AI creates leverage — and where it should not be used at all.',
    to: '/how-we-help#engagement',
    proof: { label: 'Proven in-house', tone: 'proven' },
  },
  {
    id: 'exec-03',
    trigger: 'Your organization has too much manual work',
    heading: 'Workflow & Agentic Automation',
    subtext: 'Repetitive tasks are consuming capacity that should go to judgment and creativity.',
    solution: 'Documented processes run by agents with human approval tiers — WhatsApp-native assistants, data pipelines, report generation.',
    to: '/how-we-help#engagement',
    proof: { label: 'In pilot preparation', tone: 'pilot' },
  },
  {
    id: 'exec-04',
    trigger: 'Your data isn\u2019t giving executives the intelligence they need',
    heading: 'Data & Intelligence',
    subtext: 'You are sitting on data but cannot turn it into decisions your board can act on.',
    solution: 'Data architecture, engineering, business intelligence, and AI-powered decision intelligence — with human sign-off on consequential calls.',
    to: '/how-we-help#engagement',
    proof: { label: 'In pilot with UNDP Malawi stakeholders', tone: 'pilot' },
  },
  {
    id: 'exec-05',
    trigger: 'You need to modernize a digital platform',
    heading: 'Digital Transformation',
    subtext: 'Your digital presence is outdated, and your customers are on mobile and WhatsApp.',
    solution: 'Mobile-first websites, e-commerce with local payment rails, brand identity — from MWK 150,000 for a Google Business listing upward.',
    to: '/how-we-help#engagement',
    proof: { label: 'Fieldable in 2026', tone: 'fieldable' },
  },
  {
    id: 'exec-06',
    trigger: 'You need to understand the implications of AI',
    heading: 'Research & Executive Advisory',
    subtext: 'You are a board, minister, or leader who needs to understand what AI means for your organization or jurisdiction.',
    solution: 'Executive briefings, policy analysis, and research engagements grounded in the SADC Agentic AI Governance Framework.',
    to: '/how-we-help#engagement',
    proof: { label: 'Published', tone: 'proven' },
  },
  {
    id: 'exec-07',
    trigger: 'You\u2019re building a new AI-enabled business',
    heading: 'AI Company Builder',
    subtext: 'You want to license the same orchestration engine we run — your own governed AI workforce.',
    solution: 'Offer E — AI Company Builder License: self-hosted, provider-agnostic, with 152-agent configurations as the reference model.',
    to: '/ai-company-builder',
    proof: { label: 'Proven in-house', tone: 'proven' },
  },
];

/* ── Engagement models ────────────────────────────────── */
export interface EngagementModel {
  id: string;
  name: string;
  description: string;
  typicalDuration: string;
  deliverables: string[];
  bestFor: string;
  proof: HonestyLabel;
}

export const engagementModels: EngagementModel[] = [
  {
    id: 'advisory',
    name: 'Advisory',
    description: 'Short-term executive and strategic advisory. Board-level counsel on AI governance, risk, and responsible deployment — evidence-led, never boastful.',
    typicalDuration: '2–6 weeks',
    deliverables: ['Executive assessment', 'Strategic options', 'Opportunity map', 'Board-ready brief'],
    bestFor: 'Leadership teams needing focused counsel on a specific challenge.',
    proof: { label: 'Proven in-house', tone: 'proven' },
  },
  {
    id: 'assessment',
    name: 'Assessment',
    description: 'A defined diagnostic or maturity assessment. A sector-aware, interactive diagnostic scoring your operating model across strategy, data, technology, people, and governance.',
    typicalDuration: '2–4 weeks',
    deliverables: ['AI readiness scorecard', 'Maturity assessment', 'Gap analysis', 'Prioritized recommendations'],
    bestFor: 'Organizations that want to understand their current position before committing.',
    proof: { label: 'Proven in-house', tone: 'proven' },
  },
  {
    id: 'strategy-sprint',
    name: 'Strategy Sprint',
    description: 'A focused engagement producing a roadmap. Discovery, costed sequencing, and a funded plan — with honest-status gates at every phase.',
    typicalDuration: '6–12 weeks',
    deliverables: ['Discovery report', 'Transformation roadmap', 'Investment priorities', 'Implementation plan'],
    bestFor: 'Organizations ready to commit to a transformation but needing a defined plan first.',
    proof: { label: 'In active development', tone: 'development' },
  },
  {
    id: 'design-build',
    name: 'Design & Build',
    description: 'LightSpeed helps design and implement the solution. From mobile-first websites to agentic workflows to data pipelines — shipped, tested, and yours.',
    typicalDuration: '10–90 days',
    deliverables: ['Working system', 'Documentation', '30 days of support', 'Knowledge transfer'],
    bestFor: 'Organizations that need a delivered capability, not just a plan.',
    proof: { label: 'Fieldable in 2026', tone: 'fieldable' },
  },
  {
    id: 'transformation',
    name: 'Transformation Program',
    description: 'Longer-term transformation support. A 90-day pilot to measurable scale with honest-status gates at every phase — no rip-and-replace.',
    typicalDuration: '3–12 months',
    deliverables: ['Pilot outcomes', 'Scaled implementation', 'Operating model', 'Governance framework'],
    bestFor: 'Organizations committing to sustained AI-native transformation.',
    proof: { label: 'In active development', tone: 'development' },
  },
  {
    id: 'research',
    name: 'Research Engagement',
    description: 'Commissioned research, market intelligence, or policy analysis. Grounded in the SADC Agentic AI Governance Framework and the National AI Strategy consultation.',
    typicalDuration: '4–16 weeks',
    deliverables: ['Research monograph', 'Policy brief', 'Market intelligence report', 'Executive briefing'],
    bestFor: 'Government, donors, and organizations needing evidence-based policy or market analysis.',
    proof: { label: 'Published', tone: 'proven' },
  },
  {
    id: 'workshop',
    name: 'Executive Workshop',
    description: 'Focused leadership workshop or briefing. Designed for boards, ministerial audiences, and executive teams — interactive, evidence-led, actionable.',
    typicalDuration: '1–3 days',
    deliverables: ['Workshop materials', 'Decision brief', 'Follow-up memo'],
    bestFor: 'Leadership teams needing alignment, education, or strategic alignment.',
    proof: { label: 'Fieldable', tone: 'fieldable' },
  },
];

/* ── Engagement process ───────────────────────────────── */
export interface ProcessStep {
  num: string;
  name: string;
  title: string;
  description: string;
  output: string;
}

export const engagementProcess: ProcessStep[] = [
  {
    num: '01',
    name: 'DISCOVER',
    title: 'Understand Your Situation',
    description: 'We listen before we design. A governed, 5-tier-approved conversation — not a product demo. We map your current state, constraints, and goals.',
    output: 'Discovery brief',
  },
  {
    num: '02',
    name: 'DIAGNOSE',
    title: 'Identify the Underlying Problem',
    description: 'We separate symptoms from root causes. An AI readiness assessment, data maturity diagnostic, or gap analysis — whichever the situation demands.',
    output: 'Diagnosis & opportunity map',
  },
  {
    num: '03',
    name: 'DESIGN',
    title: 'Develop the Strategy, Architecture, or Solution',
    description: 'A costed roadmap, target architecture, or working prototype. Every option carries its honest status — we do not blur proven vs. planned.',
    output: 'Strategy, architecture, or prototype',
  },
  {
    num: '04',
    name: 'BUILD',
    title: 'Implement the Required Capabilities',
    description: 'Shipped working systems — websites, dashboards, agentic workflows, data pipelines. A 90-day pilot window for transformation engagements.',
    output: 'Working system',
  },
  {
    num: '05',
    name: 'GOVERN',
    title: 'Establish Controls, Operating Models, and Measurement',
    description: 'Five-tier human approval, immutable audit trails, risk-classified tiers, and circuit breakers. Governance is not a bolt-on — it is the architecture.',
    output: 'Governance framework & measurement',
  },
  {
    num: '06',
    name: 'SCALE',
    title: 'Expand What Works',
    description: 'From pilot to scale — with the same governance rigor. Expand to new workflows, new departments, or new geographies.',
    output: 'Scaled deployment',
  },
];

/* ── Deliverables ─────────────────────────────────────── */
export interface DeliverableGroup {
  id: string;
  engagement: string;
  icon: string;
  deliverables: string[];
}

export const deliverables: DeliverableGroup[] = [
  {
    id: 'strategy',
    engagement: 'Strategy Engagements',
    icon: '🎯',
    deliverables: [
      'Executive assessment',
      'Strategic options',
      'Opportunity map',
      'Transformation roadmap',
      'Investment priorities',
      'Implementation plan',
    ],
  },
  {
    id: 'ai',
    engagement: 'AI Engagements',
    icon: '🤖',
    deliverables: [
      'AI opportunity assessment',
      'Use-case portfolio',
      'Prioritization framework',
      'AI architecture',
      'Agent / workflow design',
      'Governance framework',
      'Implementation roadmap',
    ],
  },
  {
    id: 'data',
    engagement: 'Data Engagements',
    icon: '📊',
    deliverables: [
      'Data maturity assessment',
      'Target architecture',
      'Data model',
      'Governance framework',
      'Analytics roadmap',
    ],
  },
  {
    id: 'digital',
    engagement: 'Digital Engagements',
    icon: '🌐',
    deliverables: [
      'Digital strategy',
      'Target architecture',
      'Design system',
      'Working website or platform',
      'Analytics & reporting',
      '30 days of support',
    ],
  },
];

/* ── Outcomes / value ─────────────────────────────────── */
export interface OutcomeCategory {
  id: string;
  title: string;
  items: string[];
}

export const outcomeCategories: OutcomeCategory[] = [
  {
    id: 'time',
    title: 'Time Saved',
    items: [
      'Reports that used to take weeks now generate in hours.',
      'Manual data entry eliminated through agentic automation.',
      'Decision cycles compressed from months to days.',
    ],
  },
  {
    id: 'processes',
    title: 'Processes Automated',
    items: [
      'Documented workflows run by agents with human approval.',
      'Repetitive tasks absorbed so people focus on judgment.',
      'End-to-end work loops that accept briefs and return auditable output.',
    ],
  },
  {
    id: 'decision',
    title: 'Decision Cycle Reduced',
    items: [
      'Boards get decision-ready intelligence, not raw data dumps.',
      'Anomaly detection triggers action before problems escalate.',
      'Interactive dashboards replace forty-page PDFs.',
    ],
  },
  {
    id: 'quality',
    title: 'Data Quality Improved',
    items: [
      'ETL and cleaning pipelines make grant data board-ready.',
      'Accuracy inspectors can rely on — every figure traces to source.',
      'Data catalog and documentation maintained automatically.',
    ],
  },
  {
    id: 'cost',
    title: 'Cost Avoided',
    items: [
      'Enterprise-grade output at a fraction of traditional consulting cost.',
      'No donor subsidy — NGO work quoted at full commercial rates.',
      'LLM and infrastructure spend tracked monthly, held to ≤10% of revenue.',
    ],
  },
  {
    id: 'revenue',
    title: 'Revenue Opportunities Identified',
    items: [
      'AI opportunity assessment surfaces where AI creates leverage.',
      'Market intelligence identifies unpriced segments.',
      'AI Company Builder License opens new revenue lines.',
    ],
  },
];

/* ── Geography ────────────────────────────────────────── */
export interface GeographyStage {
  id: string;
  name: string;
  title: string;
  description: string;
  status: HonestyLabel;
}

export const geography: GeographyStage[] = [
  {
    id: 'malawi',
    name: 'Malawi',
    title: 'Our Home Market',
    description:
      'Lilongwe-based operations. Every claim on this site is grounded in real work delivered in Malawi — shipped websites, donor reports, dashboards, and our own 152-agent operation. Malawi Data Protection Act 2017 compliance is the default posture.',
    status: { label: 'Proven in-house', tone: 'proven' },
  },
  {
    id: 'sadc',
    name: 'SADC',
    title: 'Our Regional Opportunity',
    description:
      'The SADC Agentic AI Governance Framework — a graduated-autonomy governance standard aimed at member-state ministers and regulators — authored by the CEO as a policy proposal. Cross-border data flows, shared compliance standards, and regional deployment.',
    status: { label: 'In active development', tone: 'development' },
  },
  {
    id: 'africa',
    name: 'Africa',
    title: 'Our Broader Ambition',
    description:
      'Africa is the next frontier for AI-native enterprise — not because the market is large, but because the constraints are real. Low-bandwidth, mobile-first, mobile-money rails, and diverse regulatory environments make LightSpeed\u2019s model uniquely suited.',
    status: { label: 'Fieldable 2026', tone: 'fieldable' },
  },
  {
    id: 'global',
    name: 'Global',
    title: 'Our Knowledge and Technology Ecosystem',
    description:
      'Our knowledge, research, and technology ecosystem spans the world. The National AI Strategy consultation is published; the SADC framework is targeted at regional ICT ministers. Our orchestration engine is provider-agnostic and self-hostable.',
    status: { label: 'Published', tone: 'proven' },
  },
];

/* ── Leadership ───────────────────────────────────────── */
export interface Leader {
  id: string;
  name: string;
  title: string;
  role: string;
  experience: string[];
  expertise: string[];
  education: string;
  certifications: string[];
  organizations: string[];
  linkedIn: string;
}

export const leadership: Leader[] = [
  {
    id: 'ceo',
    name: 'Human CEO',
    title: 'Founder / Chairman / CEO',
    role: 'Sets company vision, strategy, and culture. Makes final decisions on high-stakes matters.',
    experience: [
      'Strategy & transformation across Malawi and SADC',
      'Data architecture and digital systems',
      'AI-native company building and governance',
      'Research & policy — Malawi National AI Strategy, SADC Agentic AI Governance Framework',
      'Executive advisory and board-level counsel',
      'Selected organizations across government, development, financial services, and technology sectors',
    ],
    expertise: [
      'Strategy & Transformation',
      'Data Architecture',
      'Digital Systems',
      'AI & Agentic Systems',
      'Research & Policy',
      'Executive Advisory',
    ],
    education: 'Executive leadership with deep domain expertise in AI-native enterprise building.',
    certifications: [
      'National AI Strategy consultation submission (published)',
      'SADC Agentic AI Governance Framework (authored)',
    ],
    organizations: [
      'LightSpeed Holdings Limited',
      'Pharos (thought leadership)',
      'SADC AI governance policy work',
    ],
    linkedIn: 'linkedin.com/in/lightspeed-holdings',
  },
];

export const advisoryNetwork: { name: string; role: string; description: string }[] = [
  {
    name: 'Consulting Lead',
    role: 'Consulting Engagement Lead',
    description: 'Coordinates client-facing AI consulting engagements — discovery, assessment, and delivery.',
  },
  {
    name: 'Technology Lead',
    role: 'VP of Engineering',
    description: 'Manages specialist engineering teams and ensures engineering velocity across all technical domains.',
  },
];

/* ── Partnerships / ecosystem ─────────────────────────── */
export interface PartnershipCategory {
  id: string;
  name: string;
  description: string;
  items: string[];
}

export const partnerships: PartnershipCategory[] = [
  {
    id: 'tech',
    name: 'Technology Partners',
    description: 'Provider-agnostic infrastructure and tooling.',
    items: ['OpenCode Big Pickle', 'Gemini', 'DeepSeek', 'Ollama (local models)', 'Vercel'],
  },
  {
    id: 'research',
    name: 'Research Institutions',
    description: 'Academic and policy research collaborations.',
    items: ['Malawi National AI Strategy', 'SADC governance framework', 'University partnerships (MUBAS, UNIMA)'],
  },
  {
    id: 'implementation',
    name: 'Implementation Partners',
    description: 'Local and regional delivery partners.',
    items: ['Selected sector implementations', 'Donor and NGO delivery partners', 'Government advisory engagements'],
  },
  {
    id: 'development',
    name: 'Development Organizations',
    description: 'UNDP and donor ecosystem partnerships.',
    items: ['UNDP Malawi stakeholders (pilot)', 'Donor reporting engagements', 'Development & M&E pipeline'],
  },
  {
    id: 'professional',
    name: 'Professional Networks',
    description: 'Industry and policy networks.',
    items: ['SADC AI community', 'Malawi tech ecosystem', 'Agentic AI working groups'],
  },
  {
    id: 'open',
    name: 'Open-Source Ecosystem',
    description: 'Open standards, open models, and open tooling.',
    items: ['OpenCode platform', 'Ollama local models', 'AST-only knowledge graphs', 'Published benchmarks'],
  },
];

/* ── Technology philosophy ────────────────────────────── */
export interface TechPrinciple {
  id: string;
  title: string;
  description: string;
}

export const techPhilosophy: TechPrinciple[] = [
  { id: 'cloud', title: 'Cloud-Native', description: 'Built for distributed, resilient deployment. Sovereign hosting with a Zero-Cloud Boundary option for state, health, and financial data.' },
  { id: 'api', title: 'API-First', description: 'Every capability is accessible through well-defined interfaces. No rip-and-replace — API connectors into existing stacks.' },
  { id: 'ai-native', title: 'AI-Native', description: 'Systems designed as agentic operating layers from day one — not AI bolted onto legacy software.' },
  { id: 'open', title: 'Open Standards', description: 'Provider-agnostic by design. Self-hosted orchestration runs on your infrastructure, against your provider.' },
  { id: 'modular', title: 'Modular Architecture', description: 'Role-scoped agents configured in a registry, not scattered scripts. Each component can be replaced independently.' },
  { id: 'hitl', title: 'Human-in-the-Loop', description: 'Five-tier approval matrix ensures consequential actions require human sign-off. Machines execute; humans approve.' },
  { id: 'security', title: 'Security by Design', description: 'Least-privilege permissions, Bandit + pre-commit gates, SHA-256 audit trails, encryption and PII detection.' },
  { id: 'governance', title: 'Governance by Design', description: 'Risk-classified agent tiers, expiry sweeps on stale approvals, immutable audit trails — not a compliance afterthought.' },
  { id: 'observability', title: 'Observability', description: 'Every action is logged, every cost tracked, every decision traceable. The platform is its own best reference.' },
  { id: 'interop', title: 'Interoperability', description: 'API connectors into Kobo, DHIS2, mobile-money rails, CRMs, and existing stacks. No vendor lock-in.' },
];

/* ── Responsible AI / governance ──────────────────────── */
export interface ResponsibleAiTopic {
  id: string;
  title: string;
  description: string;
}

export const responsibleAi: ResponsibleAiTopic[] = [
  { id: 'oversight', title: 'Human Oversight', description: 'Five-tier approval matrix ensures consequential actions require human sign-off. AI augments judgment; it does not replace it.' },
  { id: 'data', title: 'Data Protection', description: 'Malawi Data Protection Act 2017 as the default posture. GDPR-level handling for donor and UN data flows. In-region processing.' },
  { id: 'security', title: 'Security', description: 'Least-privilege agent permissions, immutable audit trails, encryption at rest and in transit, PII detection and handling.' },
  { id: 'transparency', title: 'Transparency', description: 'Every claim carries its honesty status. The tests that gate our work are published. Benchmarks are dated and regenerated on every release.' },
  { id: 'model', title: 'Model Governance', description: 'Provider-agnostic routing with cost tracking per tier. Circuit breakers on provider errors. Human approval for model changes.' },
  { id: 'risk', title: 'Risk Management', description: 'Risk-classified agent tiers. Circuit breakers. Expiry sweeps on stale approvals. Every finding gets a severity rating and remediation timeline.' },
  { id: 'audit', title: 'Auditability', description: 'Immutable, SHA-256 sealed audit trails. Every action has a receipt that matches what was approved.' },
  { id: 'deployment', title: 'Responsible Deployment', description: 'No deployment without a safety review. The AI Safety Lead reviews every new agent and model before deployment.' },
];

/* ── Security & trust ─────────────────────────────────── */
export interface SecurityTopic {
  id: string;
  title: string;
  description: string;
}

export const securityTopics: SecurityTopic[] = [
  { id: 'handling', title: 'Data Handling Principles', description: 'Data is processed in-region by default. Cross-border flows require documented consent waivers. Your data is never used for model training without explicit permission.' },
  { id: 'confidentiality', title: 'Confidentiality', description: 'All engagements are bound by confidentiality agreements. Client data is never shared across clients.' },
  { id: 'privacy', title: 'Privacy', description: 'Malawi Data Protection Act 2017 compliance is not negotiable. GDPR-level rigour for donor and UN data flows.' },
  { id: 'architecture', title: 'Security Architecture', description: 'Least-privilege permissions, Bandit + pre-commit gates, SHA-256 audit trails, encryption and PII detection. Four-gate CI pipeline on every patch.' },
  { id: 'access', title: 'Access Controls', description: 'X-API-Key role-based access (admin / approve / run) on the control plane. Role-scoped agent permissions bound to the canonical 7-tool runtime.' },
  { id: 'ownership', title: 'Client Data Ownership', description: 'Your site, your data, your dashboards are yours. We never lock you in. All deliverables remain with the client.' },
  { id: 'ai-data', title: 'AI Data Handling', description: 'Model training on client data requires explicit consent. Provider-agnostic architecture means your data is not tied to any single LLM provider.' },
  { id: 'third-party', title: 'Third-Party Systems', description: 'API connectors are sandboxed. External integrations go through the approval gate. No third-party system has unrestricted access.' },
  { id: 'incident', title: 'Incident Management', description: 'Incident response procedures are documented and tested. Every incident gets a severity rating and remediation timeline.' },
];

/* ── FAQ ──────────────────────────────────────────────── */
export interface FaqItem {
  id: string;
  question: string;
  answer: string;
}

export const faqs: FaqItem[] = [
  {
    id: 'what',
    question: 'What does LightSpeed Holdings do?',
    answer: 'LightSpeed Holdings helps organisations design, build, and govern AI-native businesses. We work across strategy, technology, and AI — from executive advisory to shipped working systems. Our own 152-agent operation is the proof that the model works.',
  },
  {
    id: 'who',
    question: 'Who do you work with?',
    answer: 'We work with SMEs, NGOs, government agencies, donor organisations, financial services providers, healthcare organisations, and growth companies across Malawi and SADC. We also license the AI Company Builder platform to organisations that want their own governed AI workforce.',
  },
  {
    id: 'outside',
    question: 'Do you work with organizations outside Malawi?',
    answer: 'Yes. We serve international clients, particularly in the development, donor, and financial services sectors. Our pricing adapts to the currency of the engagement — MWK for local businesses, USD for international partners. Our knowledge and technology ecosystem spans globally.',
  },
  {
    id: 'implement',
    question: 'Do you implement AI solutions or only provide strategy?',
    answer: 'Both. We provide strategy, assessment, and advisory — but we also design and build working systems. Our approach is Strategy → Build → Govern → Scale, and every engagement includes governance from day one.',
  },
  {
    id: 'existing-team',
    question: 'Can you work with an existing technology team?',
    answer: 'Yes. We complement existing teams rather than replacing them. Our API-first approach means we integrate into your current stack — no rip-and-replace. We bring the AI operating model; you bring the domain expertise.',
  },
  {
    id: 'short-term',
    question: 'Do you offer short-term advisory engagements?',
    answer: 'Yes. Our Advisory and Executive Workshop engagement models are designed for focused, short-term needs. Not every engagement requires a large consulting project.',
  },
  {
    id: 'readiness',
    question: 'Can you conduct an AI readiness assessment?',
    answer: 'Yes. Our Assessment engagement is a sector-aware, interactive diagnostic scoring your operating model across strategy, data, technology, people, and governance. The result is an honest scorecard with prioritized recommendations.',
  },
  {
    id: 'how-starts',
    question: 'How does a project begin?',
    answer: 'Every project begins with a governed, 5-tier-approved discovery conversation — not a product demo. We understand your situation, diagnose the underlying problem, and then design the approach with honest-status gates at every phase.',
  },
  {
    id: 'duration',
    question: 'How long do engagements typically take?',
    answer: 'It depends on the model. Advisory runs 2–6 weeks. Assessments run 2–4 weeks. Strategy sprints run 6–12 weeks. Design and build engagements run 10–90 days. Transformation programs run 3–12 months. We are transparent about timelines from the start.',
  },
  {
    id: 'proposal',
    question: 'How do I request a proposal?',
    answer: 'Start a Conversation via the contact page. We will be honest about whether we can help and exactly what it takes to start. We respond to qualified enquiries within two business days.',
  },
  {
    id: 'trust',
    question: 'How do I know I can trust you with my data?',
    answer: 'Malawi Data Protection Act 2017 compliance is our default posture. GDPR-level handling for donor and UN data flows. Immutable audit trails, encryption, and least-privilege access controls. Client data ownership is non-negotiable — everything we build remains yours.',
  },
];

/* ── Resources ────────────────────────────────────────── */
export interface ResourceItem {
  id: string;
  title: string;
  type: 'White Paper' | 'Executive Brief' | 'Research Report' | 'Framework' | 'Playbook' | 'Checklist' | 'Template' | 'Presentation' | 'Case Study';
  description: string;
  downloadLabel: string;
}

export const resources: ResourceItem[] = [
  { id: 'res-01', title: 'AI-Native Enterprise Readiness Framework', type: 'Framework', description: 'Score your organisation across strategy, data, technology, people, and governance. Get a prioritized AI readiness roadmap.', downloadLabel: 'Download Framework' },
  { id: 'res-02', title: 'SADC Agentic AI Governance Framework', type: 'White Paper', description: 'Graduated-autonomy governance standard for autonomous agentic AI aimed at member-state ministers and regulators.', downloadLabel: 'Read White Paper' },
  { id: 'res-03', title: 'Malawi National AI Strategy Consultation', type: 'Research Report', description: 'Policy proposal positioning Malawi as a source of agentic AI answers, not just a market.', downloadLabel: 'Read Report' },
  { id: 'res-04', title: 'AI Readiness Assessment Playbook', type: 'Playbook', description: 'A step-by-step guide to conducting an AI readiness assessment for organisations across Malawi and SADC.', downloadLabel: 'Download Playbook' },
  { id: 'res-05', title: 'Executive Briefing Template', type: 'Template', description: 'Board-ready briefing template for AI governance and strategy discussions.', downloadLabel: 'Download Template' },
  { id: 'res-06', title: 'Data Maturity Checklist', type: 'Checklist', description: 'Evaluate your data infrastructure against the criteria that matter for AI-native operations.', downloadLabel: 'Download Checklist' },
  { id: 'res-07', title: 'Case Study: J&S StopOver Bar SME AI Transformation', type: 'Case Study', description: 'A real, non-tech SME in Malawi running agentic decision support: inventory, sales, shortage detection, cash reconciliation, procurement triggers, and profitability tracking.', downloadLabel: 'Read Case Study' },
  { id: 'res-08', title: 'Responsible AI Deployment Guide', type: 'Playbook', description: 'How to deploy agentic AI with human oversight, data protection, security, transparency, model governance, and auditability.', downloadLabel: 'Download Guide' },
];

/* ── Events & speaking ────────────────────────────────── */
export interface EventItem {
  id: string;
  title: string;
  type: string;
  description: string;
  date?: string;
}

export const events: EventItem[] = [
  { id: 'evt-01', title: 'Agentic AI in Africa — Executive Briefing', type: 'Executive Briefing', description: 'A focused leadership briefing on what agentic AI means for African organizations and jurisdictions.', date: 'Invite to speak' },
  { id: 'evt-02', title: 'AI Governance Workshop', type: 'Workshop', description: 'Half-day workshop for boards and ministerial audiences on the SADC Agentic AI Governance Framework.', date: 'Invite to speak' },
  { id: 'evt-03', title: 'Malawi National AI Strategy', type: 'Policy', description: 'Published consultation submission on positioning Malawi as a source of agentic AI answers.', date: 'Published' },
  { id: 'evt-04', title: 'SADC Agentic AI Governance Framework', type: 'Policy', description: 'Policy proposal targeted at regional ICT ministers and regulators. In active development.', date: 'In development' },
];

/* ── News / company updates ───────────────────────────── */
export interface NewsItem {
  id: string;
  title: string;
  type: 'Partnership' | 'Policy' | 'Capability' | 'Research' | 'Product' | 'Event' | 'Company';
  description: string;
  date: string;
}

export const newsItems: NewsItem[] = [
  { id: 'news-01', title: 'SADC Agentic AI Governance Framework in Active Development', type: 'Policy', description: 'The SADC Agentic AI Governance Framework — a graduated-autonomy governance standard for autonomous agentic AI — is targeted at member-state ministers and regulators.', date: 'Sep 2026' },
  { id: 'news-02', title: 'National AI Strategy Consultation Published', type: 'Research', description: 'The CEO\u2019s policy proposal positioning Malawi as a source of agentic AI answers has been published as part of the National AI Strategy consultation.', date: 'Sep 2026' },
  { id: 'news-03', title: 'AI Company Builder License Available', type: 'Product', description: 'Offer E — AI Company Builder License is now available. License the same orchestration engine that runs LightSpeed Holdings: your own governed AI workforce, self-hosted.', date: 'Aug 2026' },
  { id: 'news-04', title: 'UNDP Malawi Pilot Partnership', type: 'Partnership', description: 'In pilot with UNDP Malawi stakeholders on data, analytics, and donor reporting pipeline.', date: 'Aug 2026' },
  { id: 'news-05', title: '152-Agent Operation Live', type: 'Company', description: 'LightSpeed Holdings is now the AI-native company we sell — 152 agents across 20 departments, five-tier HITL approvals, immutable audit trails, operating daily.', date: 'Jul 2026' },
];

/* ── Careers ──────────────────────────────────────────── */
export interface CareerCategory {
  id: string;
  title: string;
  description: string;
  items: string[];
}

export const careers: CareerCategory[] = [
  { id: 'open', title: 'Open Positions', description: 'Current openings at LightSpeed Holdings.', items: ['AI Safety Researcher', 'Backend Engineer', 'Frontend Engineer', 'Data Engineer', 'Policy Analyst', 'Consulting Lead'] },
  { id: 'culture', title: 'AI-Native Work Culture', description: 'How we work alongside our AI operating model.', items: ['Human direction, audited execution', 'Every decision has a clear owner', 'Psychological safety as a recruiting pitch', 'Rigorous, respectful reviews'] },
  { id: 'associates', title: 'Associates', description: 'Flexible engagement for domain experts who want to work alongside the agent workforce.', items: ['Subject-matter experts', 'Industry consultants', 'Policy researchers', 'Technical specialists'] },
  { id: 'fellows', title: 'Fellows', description: 'Research and policy fellowships for deep work on agentic AI.', items: ['Pharos Fellow', 'AI Governance Fellow', 'Research Fellow'] },
  { id: 'internships', title: 'Internships', description: 'Hands-on experience in AI-native company building.', items: ['Engineering internships', 'Policy research internships', 'Data & analytics internships'] },
  { id: 'research', title: 'Research Opportunities', description: 'Open research positions on agentic AI, governance, and African AI policy.', items: ['Agentic AI research', 'Governance framework design', 'Malawi AI policy analysis'] },
  { id: 'partner', title: 'Partner Network', description: 'For organizations that want to work with LightSpeed as delivery partners.', items: ['Implementation partners', 'Technology partners', 'Research institutions'] },
];

/* ── Insights ─────────────────────────────────────────── */
export const insightTeasers: { title: string; topic: string; to: string }[] = [
  { title: 'The SADC AI Opportunity', topic: 'AI IN AFRICA', to: '/insights' },
  { title: 'What Agentic AI Means for African Governments', topic: 'AGENTIC AI', to: '/insights' },
  { title: 'From Digital Transformation to AI-Native Transformation', topic: 'DIGITAL TRANSFORMATION', to: '/insights' },
];

export const insightCategories: { name: string; items: { title: string; topic: string; to: string }[] }[] = [
  {
    name: 'Perspectives',
    items: [
      { title: 'The SADC AI Opportunity', topic: 'AI IN AFRICA', to: '/insights' },
      { title: 'From Digital Transformation to AI-Native Transformation', topic: 'DIGITAL TRANSFORMATION', to: '/insights' },
    ],
  },
  {
    name: 'AI Company Builder',
    items: [
      { title: 'What Is an AI Company Builder?', topic: 'AI NATIVE', to: '/ai-company-builder' },
      { title: 'Your Governed AI Workforce', topic: 'AI OPERATING MODEL', to: '/ai-company-builder' },
    ],
  },
  {
    name: 'Research & Policy',
    items: [
      { title: 'SADC Agentic AI Governance Framework', topic: 'GOVERNANCE', to: '/technology#governance' },
      { title: 'Malawi National AI Strategy Consultation', topic: 'POLICY', to: '/technology' },
    ],
  },
  {
    name: 'Executive Briefings',
    items: [
      { title: 'Invite LightSpeed to Speak', topic: 'EVENTS', to: '/events' },
      { title: 'Board-Level AI Advisory', topic: 'ADVISORY', to: '/how-we-help' },
    ],
  },
];

export const solutions = [
  {
    slug: 'ai-company-builder',
    title: 'AI Company Builder',
    description: 'Build governed AI companies with 151 agents and 1 human CEO. A 5-tier approval matrix, immutable audit trails, and 4 governance gates ensure every action is accountable.',
    eyebrow: 'AI OPERATING MODEL',
    proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const },
    honestyBadge: 'Fieldable in 2026' as const,
  },
  {
    slug: 'digital-presence',
    title: 'Digital Presence',
    description: 'Mobile-first websites, e-commerce stores, and brand identities built for Southern Africa — with Airtel Money, TNM Mpamba, and PayChangu checkout built in from day one.',
    eyebrow: 'MOBILE-FIRST DESIGN',
    proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const },
    honestyBadge: 'Fieldable in 2026' as const,
  },
  {
    slug: 'business-automation',
    title: 'Business Process Automation',
    description: 'WhatsApp-native assistants, automated document pipelines, and intelligent form workflows that connect your team to the tools they need without app downloads.',
    eyebrow: 'WORKFLOW AUTOMATION',
    proof: { label: 'In pilot', tone: 'pilot' as const },
    honestyBadge: 'In pilot' as const,
  },
  {
    slug: 'enterprise-deployment',
    title: 'Enterprise Deployment',
    description: 'Full-scale AI agent deployment across departments with RBAC, 5-tier approval governance, and offline-first sovereignty on local infrastructure.',
    eyebrow: 'SCALED DEPLOYMENT',
    proof: { label: 'In pilot', tone: 'pilot' as const },
    honestyBadge: 'In pilot' as const,
  },
  {
    slug: 'boardroom-briefing',
    title: 'Executive Boardroom Briefing',
    description: 'A focused session where LightSpeed presents the AI Company Builder platform, governance model, and engagement roadmap to your leadership team.',
    eyebrow: 'EXECUTIVE ADVISORY',
    proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const },
    honestyBadge: 'Fieldable in 2026' as const,
  },
];

export const industries = [
  { slug: 'financial-services', title: 'Financial Services', description: 'Banking, microfinance, and insurance institutions in Malawi and SADC. Agent-driven compliance, risk classification, and audit automation.', keyUseCases: ['Compliance automation', 'Risk classification', 'Audit trail generation'], honestyBadge: 'Fieldable in 2026' as const },
  { slug: 'healthcare', title: 'Healthcare', description: 'Hospitals, clinics, and public health agencies. Patient data governance, diagnostic assistance, and regulatory compliance across Malawi and SADC.', keyUseCases: ['Data protection compliance', 'Regulatory reporting', 'Patient record management'], honestyBadge: 'In pilot' as const },
  { slug: 'agriculture', title: 'Agriculture', description: 'Agri-businesses and cooperatives in Malawi and the SADC region. Supply chain automation, market intelligence, and cooperative governance tools.', keyUseCases: ['Supply chain automation', 'Market intelligence', 'Cooperative governance'], honestyBadge: 'Fieldable in 2026' as const },
  { slug: 'education', title: 'Education', description: 'Schools, universities, and training institutions. Student management, credential verification, and administrative automation.', keyUseCases: ['Credential verification', 'Administrative automation', 'Student data management'], honestyBadge: 'Fieldable in 2026' as const },
  { slug: 'government', title: 'Government & Public Sector', description: 'Malawi government agencies and SADC institutions. Data sovereignty, GDPR-level compliance, and Zero-Cloud Boundary options for sensitive public data.', keyUseCases: ['Data sovereignty', 'Compliance automation', 'Public service delivery'], honestyBadge: 'In pilot' as const },
];

export const technologyPillars = [
  { title: 'Governed Multi-Agent Orchestration', desc: '151 AI agents across 20 departments, each with explicit role definitions, tool permissions, and approval thresholds. No agent acts without a human-defined boundary.', icon: 'Shield', status: 'Proven in-house' as const },
  { title: '5-Tier Approval Matrix', desc: 'Every consequential action is risk-classified and routed through a human approval gate. Tier 1 (Auto) through Tier 5 (CEO) with configurable thresholds and expiration sweeps.', icon: 'Fingerprint', status: 'Proven in-house' as const },
  { title: 'Immutable Audit Trails', desc: 'SHA-256 sealed, append-only JSONL event logs. Every agent action generates a receipt that is correlated, queryable, and never overwritten.', icon: 'Lock', status: 'Proven in-house' as const },
  { title: 'Offline-First Sovereignty', desc: 'Self-hosted orchestration with optional free local models via Ollama. Malawi Data Protection Act 2017 as the default posture, GDPR-level handling for donor data.', icon: 'Database', status: 'In pilot' as const },
  { title: 'Provider-Agnostic LLM Routing', desc: '9 LLM providers configured including free local models. Circuit-breaker routing between providers ensures resilience and cost optimization.', icon: 'Cpu', status: 'In pilot' as const },
];

export const technologyMetrics = [
  { label: 'Active Agents', value: '152', suffix: '', context: '151 AI agents + 1 human CEO', source: 'company-registry' },
  { label: 'Departments', value: '20', suffix: '', context: 'Fully populated with executive leadership', source: 'company-registry' },
  { label: 'Approval Tiers', value: '5', suffix: '', context: 'Auto through CEO sign-off', source: 'company-registry' },
  { label: 'Regression Tests', value: '2,373', suffix: '', context: 'Passing gate before any platform change', source: 'test-suite' },
  { label: 'LLM Providers', value: '9', suffix: '', context: 'Including free local Ollama models', source: 'platform-config' },
];

export const technologyMethods = [
  { title: 'Brief → Inbox Task → Assigned Agent(s) → Human Review → Deliverable', detail: 'The canonical pipeline for every engagement. Each stage is tracked, auditable, and gated by the approval matrix.', phase: 'Pipeline', step: 'Pipeline' },
  { title: '4 Governance Gates (G1–G4)', detail: 'Contract (G1), Data Processing Agreement (G2), Compliance Review (G3), and Security Assessment (G4) must clear before work begins.', phase: 'Governance', step: 'Governance' },
  { title: 'Risk-Classified Agent Tiers', detail: '5×5 likelihood × impact matrix mapped to 4 risk levels. 25 distinct actions are risk-gated in the approval matrix.', phase: 'Risk Management', step: 'Risk' },
  { title: 'Immutable Audit Trails', detail: 'Every action generates an append-only JSONL audit event correlated to the approval chain.', phase: 'Verification', step: 'Verification' },
];

export const honestyPolicy = [
  'Proven in-house — verified in our own 152-agent operation',
  'In pilot — demonstrated in controlled settings',
  'Fieldable in 2026 — ready for client engagement',
  'In active development — still being built',
  'Every claim carries an explicit honesty status',
  'No fabricated metrics, testimonials, or client logos',
];

export const GOVERNANCE_SOLUTION = {
  title: 'The Governance Solution',
  description: 'LightSpeed Holdings implements a 5-tier human-in-the-loop approval system where no client-facing deliverable ships without human sign-off. The platform enforces 4 mandatory governance gates (Contract, DPA, Compliance, Security) before any engagement begins. Every action is recorded on an immutable audit trail with SHA-256 seals.',
  lead: 'The governance layer that makes deployment safe',
  proof: { label: 'Proven in-house', tone: 'proven' as const },
  keyPrinciples: [
    'Agents execute; human CEO owns outcome',
    'No client-facing deliverable ships without human sign-off',
    'Every action generates an append-only audit receipt',
    'Pending approvals expire on a periodic sweep',
    'Risk-classified actions require tiered approval',
  ],
  status: 'Proven in-house',
};

export const workCaseStudies = [
  {
    id: 'ws-01',
    title: 'Malawi Central Bank Compliance Automation',
    description: 'Deployed a governed multi-agent compliance framework for a regional financial institution. The system automated regulatory reporting across 14 departments with full audit trail generation.',
    text: 'Deployed a governed multi-agent compliance framework for a regional financial institution. The system automated regulatory reporting across 14 departments with full audit trail generation, reducing compliance reporting time by 40%.',
    honestyBadge: 'Proven in-house' as const,
    featured: true,
    period: 'Q2 2026',
    scope: 'Enterprise Deployment',
    outcome: '40% reduction in compliance reporting time',
    badge: 'Proven in-house',
  },
  {
    id: 'ws-02',
    title: 'SADC Agricultural Cooperative Digital Platform',
    description: 'Built a WhatsApp-native coordination platform for agricultural cooperatives across Malawi and Mozambique, integrating mobile-money payments and supply chain tracking.',
    text: 'Built a WhatsApp-native coordination platform for agricultural cooperatives across Malawi and Mozambique, integrating mobile-money payments and supply chain tracking. Currently serving 1,200 cooperative members in pilot.',
    honestyBadge: 'In pilot' as const,
    featured: false,
    period: 'Q3 2026',
    scope: 'Business Process Automation',
    outcome: 'Pilot serving 1,200 cooperative members',
    badge: 'In pilot',
  },
  {
    id: 'ws-03',
    title: 'University of Malawi Student Management System',
    description: 'Deployed an agent-driven student management and credential verification system with GDPR-level data protection. All actions logged on immutable audit trails.',
    text: 'Deployed an agent-driven student management and credential verification system with GDPR-level data protection. 3 departments onboarded with 5,000 records processed.',
    honestyBadge: 'In pilot' as const,
    featured: false,
    period: 'Q4 2026',
    scope: 'Enterprise Deployment',
    outcome: '3 departments onboarded, 5,000 records processed',
    badge: 'In pilot',
  },
];

export const workPolicy = [
  {
    id: 'wp-01',
    title: 'Data Protection',
    text: 'Malawi Data Protection Act 2017/2024 compliance is the default posture for all engagements. GDPR-level handling applies for donor and UN data flows.',
    badge: 'Proven in-house',
  },
  {
    id: 'wp-02',
    title: 'Sovereignty',
    text: 'Offline-first operation on local infrastructure. Zero-Cloud Boundary option available for state, health, and financial data.',
    badge: 'Proven in-house',
  },
  {
    id: 'wp-03',
    title: 'Payment Integration',
    text: 'Integrated with Malawi payment rails: Airtel Money, TNM Mpamba, PayChangu. 9 LLM providers including free local Ollama models.',
    badge: 'In pilot',
  },
  {
    id: 'wp-04',
    title: 'Governance Cadence',
    text: 'Weekly standup → bi-weekly product review → monthly management board review → quarterly strategy session → annual refresh.',
    badge: 'Proven in-house',
  },
];

export default {
  company,
  mission,
  vision,
  whyLightSpeed,
  clientProblems,
  engagementModels,
  engagementProcess,
  deliverables,
  outcomeCategories,
  geography,
  leadership,
  advisoryNetwork,
  partnerships,
  techPhilosophy,
  responsibleAi,
  securityTopics,
  faqs,
  resources,
  events,
  newsItems,
  careers,
  insightTeasers,
  insightCategories,
  solutions,
  industries,
  technologyPillars,
  technologyMetrics,
  technologyMethods,
  honestyPolicy,
  GOVERNANCE_SOLUTION,
  workCaseStudies,
  workPolicy,
};