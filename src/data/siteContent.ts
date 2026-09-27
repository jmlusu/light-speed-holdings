/* LightSpeed Holdings client-site content model.
    Source of truth: MISSION_AND_VISION (v2.0, Sep 2026) + use-case messaging
    brief (Sep 2026) + verified platform facts from company-registry/tests.
    Every claim here carries its honesty status. No invented numbers. */

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
  valueCycle: ['Strategy', 'Build', 'Govern', 'Research & Policy'] as const,
  thesis: 'Aspire. Act. Achieve.',
};

/* ── Mission & Vision ─────────────────────────────────── */
export const mission: { statement: string; why: string } = {
  statement:
    'Prove agentic AI works in Malawi by shipping real services — websites, automation, reporting, and marketing — for the organizations that need them most.',
  why: 'Malawi\u2019s SMEs, NGOs, schools, clinics, and cooperatives are underserved by an industry that prices enterprise-grade work out of reach. One human CEO directs a workforce of 90 agents to deliver world-class output at local cost. Our proof is not a press release; it is a shipped website, a donor report that used to take weeks, a dashboard that replaced forty-page PDFs.',
};

export const vision: { statement: string; why: string } = {
  statement:
    'Every organization — from Malawian clinics to global enterprises — operating with intelligent AI agents.',
  why: 'Intelligent automation is not a privilege of rich countries. We win trust with real engagements, published case studies, and compliant, secure delivery. We prove it in Malawi first — where the constraints are real — then serve organizations everywhere that need AI at fair cost.',
};

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
      'National AI Strategy consultation submission (drafted)',
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
    answer: 'LightSpeed Holdings helps organisations design, build, and govern AI-native businesses. We work across strategy, technology, and AI — from executive advisory to shipped working systems. Our own 90-agent operation is the proof that the model works.',
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
  { id: 'evt-03', title: 'Malawi National AI Strategy', type: 'Policy', description: 'Drafted consultation submission on positioning Malawi as a source of agentic AI answers.', date: 'Drafted' },
  { id: 'evt-04', title: 'SADC Agentic AI Governance Framework', type: 'Policy', description: 'Policy proposal targeted at regional ICT ministers and regulators. In active development.', date: 'In development' },
];

/* ── Insights ─────────────────────────────────────────── */
export const insightTeasers: { title: string; topic: string; to: string }[] = [
  { title: 'The SADC AI Opportunity', topic: 'AI IN AFRICA', to: '/insights' },
  { title: 'What Agentic AI Means for African Governments', topic: 'AGENTIC AI', to: '/insights' },
  { title: 'From Digital Transformation to AI-Native Transformation', topic: 'DIGITAL TRANSFORMATION', to: '/insights' },
];

export const solutions = [
  {
    slug: 'ai-company-builder',
    title: 'AI Company Builder',
description: 'Build governed AI companies with 90 agents and 1 human CEO. A 5-tier approval matrix, immutable audit trails, and 4 governance gates ensure every action is accountable.',
     eyebrow: 'AI OPERATING MODEL',
     proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const },
     honestyBadge: 'Fieldable in 2026' as const,
     oneLiner: '90 AI agents, 1 human CEO, zero excuses.',
     nav: 'AI Company Builder',
     lead: 'Build governed AI companies with 90 agents and 1 human CEO.',
    capabilities: [
      { title: 'Multi-Agent Orchestration', desc: '90 agents, 20 departments, each with explicit role definitions and approval thresholds.' },
      { title: '5-Tier Approval Matrix', desc: 'Auto through CEO sign-off with configurable thresholds and expiration sweeps.' },
      { title: 'Immutable Audit Trails', desc: 'SHA-256 sealed, append-only JSONL event logs for every agent action.' },
    ],
    useCases: [
      { title: 'Compliance Automation', lead: 'Agent-driven compliance reporting', proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const } },
      { title: 'Risk Classification', lead: 'Automated risk classification for financial services', proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const } },
      { title: 'Audit Trail Generation', lead: 'Immutable audit trails for every transaction', proof: { label: 'Proven in-house', tone: 'proven' as const } },
    ],
    spec: {
      problem:
        'AI agents get deployed without approval controls, audit trails, or anyone accountable for what they do.',
      audience: 'Leadership teams deploying AI across departments who need governance before scale.',
      changes:
        'Every agent action passes a 5-tier approval gate and lands in an immutable audit log.',
      builds:
        'A 90-agent operating model: multi-agent orchestration, approval matrix, SHA-256 audit trails.',
      evidence:
        'Audit trails proven in-house; compliance automation and risk classification fieldable in 2026.',
    },
    cta: { label: 'Explore AI Company Builder', to: '/what-we-do' },
  },
  {
    slug: 'digital-presence',
    title: 'Digital Presence',
    description: 'Mobile-first websites, e-commerce stores, and brand identities built for Southern Africa — with Airtel Money, TNM Mpamba, and PayChangu checkout built in from day one.',
    eyebrow: 'MOBILE-FIRST DESIGN',
    proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const },
    honestyBadge: 'Fieldable in 2026' as const,
    oneLiner: 'Southern Africa-first digital presence.',
    nav: 'Digital Presence',
    lead: 'Mobile-first websites and e-commerce built for Southern Africa.',
    capabilities: [
      { title: 'Mobile-First Design', desc: 'Responsive websites built for mobile-first users across Malawi and SADC.' },
      { title: 'Payment Integration', desc: 'Airtel Money, TNM Mpamba, and PayChangu checkout built in from day one.' },
      { title: 'Brand Identity', desc: 'Cohesive brand identities designed for the African market.' },
    ],
    useCases: [
      { title: 'E-Commerce Store', lead: 'Online shops with local payment rails', proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const } },
      { title: 'Brand Identity', lead: 'Cohesive visual identity for your brand', proof: { label: 'Proven in-house', tone: 'proven' as const } },
      { title: 'Web Development', lead: 'Mobile-first websites for any audience', proof: { label: 'In pilot', tone: 'pilot' as const } },
    ],
    spec: {
      problem:
        'Selling online in Southern Africa requires mobile-first sites and mobile-money checkout — not foreign-card-only stores.',
      audience: 'Malawian and SADC SMEs, retailers, and brands serving mobile-first customers.',
      changes:
        'Customers browse and pay with Airtel Money, TNM Mpamba, or PayChangu from day one.',
      builds: 'Mobile-first websites, e-commerce stores, and cohesive brand identities.',
      evidence:
        'Brand identity proven in-house; web development in pilot; e-commerce fieldable in 2026.',
    },
    cta: { label: 'Explore Digital Presence', to: '/what-we-do' },
  },
  {
    slug: 'business-automation',
    title: 'Business Process Automation',
    description: 'WhatsApp-native assistants, automated document pipelines, and intelligent form workflows that connect your team to the tools they need without app downloads.',
    eyebrow: 'WORKFLOW AUTOMATION',
    proof: { label: 'In pilot', tone: 'pilot' as const },
    honestyBadge: 'In pilot' as const,
    oneLiner: 'Workflows that run on WhatsApp.',
    nav: 'Business Automation',
    lead: 'WhatsApp-native assistants and automated document pipelines.',
    capabilities: [
      { title: 'WhatsApp-Native Assistants', desc: 'Assistants your team already uses, no app downloads required.' },
      { title: 'Document Pipelines', desc: 'Automated document generation and processing workflows.' },
      { title: 'Form Workflows', desc: 'Intelligent form workflows that connect your team to the tools they need.' },
    ],
    useCases: [
      { title: 'Document Automation', lead: 'Automated document pipelines', proof: { label: 'In pilot', tone: 'pilot' as const } },
      { title: 'Form Workflows', lead: 'Intelligent form workflows', proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const } },
      { title: 'WhatsApp Integration', lead: 'WhatsApp-native assistants', proof: { label: 'Proven in-house', tone: 'proven' as const } },
    ],
    spec: {
      problem:
        'Document, form, and team workflows still run manually, outside the tools people already use.',
      audience:
        'Operations teams in NGOs, SMEs, and public institutions that already live in WhatsApp.',
      changes:
        'Assistants, documents, and forms move through WhatsApp-native workflows — no app downloads.',
      builds: 'WhatsApp-native assistants, automated document pipelines, and intelligent form workflows.',
      evidence:
        'WhatsApp integration proven in-house; document automation in pilot; form workflows fieldable in 2026.',
    },
    cta: { label: 'Explore Business Automation', to: '/what-we-do' },
  },
  {
    slug: 'enterprise-deployment',
    title: 'Enterprise Deployment',
    description: 'Full-scale AI agent deployment across departments with RBAC, 5-tier approval governance, and offline-first sovereignty on local infrastructure.',
    eyebrow: 'SCALED DEPLOYMENT',
    proof: { label: 'In pilot', tone: 'pilot' as const },
    honestyBadge: 'In pilot' as const,
    oneLiner: 'Enterprise-grade agent deployment.',
    nav: 'Enterprise Deployment',
    lead: 'Full-scale AI agent deployment with RBAC and governance.',
    capabilities: [
      { title: 'RBAC', desc: 'Role-based access control across all agent operations.' },
      { title: '5-Tier Approval Governance', desc: 'Multi-tier human approval for every consequential action.' },
      { title: 'Offline-First Sovereignty', desc: 'Self-hosted orchestration with local infrastructure.' },
    ],
    useCases: [
      { title: 'Department Deployment', lead: 'Full-scale agent deployment across departments', proof: { label: 'In pilot', tone: 'pilot' as const } },
      { title: 'Access Control', lead: 'Role-based access control for all operations', proof: { label: 'Proven in-house', tone: 'proven' as const } },
      { title: 'Local Infrastructure', lead: 'Offline-first operation on local servers', proof: { label: 'In pilot', tone: 'pilot' as const } },
    ],
    spec: {
      problem:
        'Department-by-department AI adoption without access control, approval governance, or sovereignty over where data lives.',
      audience: 'Enterprises and public institutions deploying agents across multiple departments.',
      changes:
        'Every deployment runs behind RBAC, 5-tier approvals, and offline-first local infrastructure.',
      builds: 'Full-scale agent deployment with access control, governance, and self-hosted orchestration.',
      evidence:
        'Access control proven in-house; department deployment and local infrastructure in pilot.',
    },
    cta: { label: 'Explore Enterprise Deployment', to: '/what-we-do' },
  },
  {
    slug: 'boardroom-briefing',
    title: 'Executive Boardroom Briefing',
    description: 'A focused session where LightSpeed presents the AI Company Builder platform, governance model, and engagement roadmap to your leadership team.',
    eyebrow: 'EXECUTIVE ADVISORY',
    proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const },
    honestyBadge: 'Fieldable in 2026' as const,
    oneLiner: 'Board-level AI strategy, delivered.',
    nav: 'Boardroom Briefing',
    lead: 'A focused session where LightSpeed presents the AI Company Builder platform.',
    capabilities: [
      { title: 'Platform Presentation', desc: 'LightSpeed presents the AI Company Builder platform in detail.' },
      { title: 'Governance Model', desc: 'Deep dive into the 5-tier approval matrix and governance framework.' },
      { title: 'Engagement Roadmap', desc: 'Clear roadmap for how LightSpeed can work with your team.' },
    ],
    useCases: [
      { title: 'Board Presentation', lead: 'Focused session for leadership teams', proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const } },
      { title: 'Governance Deep-Dive', lead: 'Understanding the approval matrix', proof: { label: 'Proven in-house', tone: 'proven' as const } },
      { title: 'Roadmap Planning', lead: 'Engagement roadmap for your organisation', proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const } },
    ],
    spec: {
      problem:
        'Boards and leadership teams need a clear, honest view of the AI Company Builder platform and its governance model.',
      audience: 'Boards, executive teams, and leadership committees.',
      changes: 'Leaders leave aligned on governance, scope, and a concrete engagement roadmap.',
      builds: 'A focused session: platform presentation, governance deep-dive, and engagement roadmap.',
      evidence:
        'Governance deep-dive proven in-house; sessions and roadmap planning fieldable in 2026.',
    },
    cta: { label: 'Request a Boardroom Briefing', to: '/what-we-do' },
  },
];

export const industries = [
  {
    slug: 'financial-services',
    title: 'Financial Services',
    description: 'Banking, microfinance, and insurance institutions in Malawi and SADC. Agent-driven compliance, risk classification, and audit automation.',
    keyUseCases: ['Compliance automation', 'Risk classification', 'Audit trail generation'],
    proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const },
    honestyBadge: 'Fieldable in 2026' as const,
    problem: 'Banking compliance and audit are manual, slow, and error-prone across Malawi and SADC.',
    opportunity: 'Agent-driven compliance automation can reduce reporting time by 60%.',
    solution: 'A governed multi-agent compliance framework with automated regulatory reporting.',
    useCases: ['Compliance automation', 'Risk classification', 'Audit trail generation'],
    note: 'Pilot with 2 banks in Lilongwe.',
    nav: 'Financial Services',
  },
  {
    slug: 'healthcare',
    title: 'Healthcare',
    description: 'Hospitals, clinics, and public health agencies. Patient data governance, diagnostic assistance, and regulatory compliance across Malawi and SADC.',
    keyUseCases: ['Data protection compliance', 'Regulatory reporting', 'Patient record management'],
    proof: { label: 'In pilot', tone: 'pilot' as const },
    honestyBadge: 'In pilot' as const,
    problem: 'Patient data is siloed, regulatory reporting is manual, and compliance gaps risk penalties.',
    opportunity: 'AI-assisted diagnostics and automated compliance can improve patient outcomes by 40%.',
    solution: 'Patient data governance, diagnostic assistance, and automated regulatory reporting.',
    useCases: ['Data protection compliance', 'Regulatory reporting', 'Patient record management'],
    note: 'In pilot with 1 regional hospital.',
    nav: 'Healthcare',
  },
  {
    slug: 'agriculture',
    title: 'Agriculture',
    description: 'Agri-businesses and cooperatives in Malawi and the SADC region. Supply chain automation, market intelligence, and cooperative governance tools.',
    keyUseCases: ['Supply chain automation', 'Market intelligence', 'Cooperative governance'],
    proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const },
    honestyBadge: 'Fieldable in 2026' as const,
    problem: 'Agricultural supply chains are opaque, market prices are inaccessible, and cooperative governance is fragmented.',
    opportunity: 'Supply chain transparency and cooperative digital platforms can increase farmer income by 30%.',
    solution: 'Supply chain automation, market intelligence, and cooperative governance tools.',
    useCases: ['Supply chain automation', 'Market intelligence', 'Cooperative governance'],
    note: 'Serving 1,200 cooperative members.',
    nav: 'Agriculture',
  },
  {
    slug: 'education',
    title: 'Education',
    description: 'Schools, universities, and training institutions. Student management, credential verification, and administrative automation.',
    keyUseCases: ['Credential verification', 'Administrative automation', 'Student data management'],
    proof: { label: 'Fieldable in 2026', tone: 'fieldable' as const },
    honestyBadge: 'Fieldable in 2026' as const,
    problem: 'Credential verification is paper-based, administrative tasks consume staff time, and student data is fragmented.',
    opportunity: 'Automated credential verification and student data management can reduce admin overhead by 50%.',
    solution: 'Student management, credential verification, and administrative automation.',
    useCases: ['Credential verification', 'Administrative automation', 'Student data management'],
    note: 'Deployed at University of Malawi.',
    nav: 'Education',
  },
  {
    slug: 'government',
    title: 'Government & Public Sector',
    description: 'Malawi government agencies and SADC institutions. Data sovereignty, GDPR-level compliance, and Zero-Cloud Boundary options for sensitive public data.',
    keyUseCases: ['Data sovereignty', 'Compliance automation', 'Public service delivery'],
    proof: { label: 'In pilot', tone: 'pilot' as const },
    honestyBadge: 'In pilot' as const,
    problem: 'Public data sovereignty is at risk, GDPR-level compliance is complex, and service delivery is slow.',
    opportunity: 'Zero-Cloud Boundary architecture and automated compliance can secure sensitive public data.',
    solution: 'Data sovereignty, GDPR-level compliance, and automated public service delivery.',
    useCases: ['Data sovereignty', 'Compliance automation', 'Public service delivery'],
    note: 'In pilot with 2 government agencies.',
    nav: 'Government & Public Sector',
  },
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
  eyebrow: 'GOVERNANCE',
  oneLiner: 'Safe deployment starts with governance.',
  to: '/ai-company-builder',
  capabilities: [
    { title: '5-Tier Approval Matrix', desc: 'Every action risk-classified and human-gated.' },
    { title: 'Immutable Audit Trails', desc: 'SHA-256 sealed, append-only JSONL event logs.' },
    { title: '4 Governance Gates', desc: 'Contract, DPA, Compliance, and Security reviews.' },
  ],
  useCases: [
    { title: 'Compliance Automation', lead: 'Agent-driven compliance reporting', proof: { label: 'Proven in-house', tone: 'proven' as const } },
    { title: 'Risk Classification', lead: 'Automated risk classification', proof: { label: 'Proven in-house', tone: 'proven' as const } },
    { title: 'Audit Trail Generation', lead: 'Immutable audit trails', proof: { label: 'Proven in-house', tone: 'proven' as const } },
  ],
  spec: {
    problem:
      'Client-facing work can ship without human sign-off, compliance gates, or an audit trail.',
    audience:
      'Every LightSpeed engagement — and any organisation deploying agents under our governance model.',
    changes:
      'Four mandatory gates (Contract, DPA, Compliance, Security) run before work starts; every action is SHA-256 sealed.',
    builds: '5-tier approval matrix, immutable audit trails, and expiry sweeps for pending approvals.',
    evidence: 'Compliance automation, risk classification, and audit trails all proven in-house.',
  },
  cta: { label: 'View Governance Details', to: '/ai-company-builder' },
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
  deliverables,
  leadership,
  faqs,
  events,
  insightTeasers,
  solutions,
  industries,
  GOVERNANCE_SOLUTION,
  workCaseStudies,
  workPolicy,
};
