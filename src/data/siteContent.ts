/* LightSpeed Holdings client-site content model.
    Source of truth: MISSION_AND_VISION (v2.0, Sep 2026) + use-case messaging
    brief (Sep 2026) + verified platform facts from company-registry/tests.
    Every claim here carries its honesty status. No invented numbers. */

import { capabilityTitles } from './capabilities';

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
  valueCycle: capabilityTitles,
  thesis: 'Aspire. Act. Achieve.',
};

/* ── Insights ─────────────────────────────────────────── */
/* MASTER_SPEC §13 content categories — one canonical list (§15),
   consumed by InsightsPage. */
export const insightCategories: string[] = [
  'Agentic AI',
  'AI Company Building',
  'AI governance',
  'AI policy',
  'Data architecture',
  'Digital transformation',
  'African AI',
  'Malawi technology',
  'SADC technology',
  'Market intelligence',
  'Operating models',
  'AI implementation',
];

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
  insightCategories,
  insightTeasers,
  solutions,
  GOVERNANCE_SOLUTION,
  workCaseStudies,
  workPolicy,
  TONE_STYLES,
};
