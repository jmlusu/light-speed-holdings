/**
 * Solutions Registry — Canonical Source of Truth
 *
 * Source: Directive §16 + siteContent.ts
 * Directive §22 — Single source for all solutions
 */

export type HonestyTier = 'verified' | 'proven-in-house' | 'fieldable' | 'pilot' | 'development';

export interface SolutionCapability {
  title: string;
  desc: string;
}

export interface SolutionUseCase {
  title: string;
  lead: string;
  proof: { label: string; tone: HonestyTier };
}

export interface SolutionSpec {
  problem: string;
  audience: string;
  changes: string;
  builds: string;
  evidence: string;
}

export interface Solution {
  slug: string;
  title: string;
  description: string;
  eyebrow: string;
  oneLiner: string;
  lead: string;
  honestyBadge: 'Verified' | 'Proven in-house' | 'Fieldable in 2026' | 'In pilot' | 'In active development';
  capabilities: SolutionCapability[];
  useCases: SolutionUseCase[];
  spec: SolutionSpec;
  cta: { label: string; to: string };
}

export const solutionsRegistry: Solution[] = [
  {
    slug: 'ai-company-builder',
    title: 'AI Company Builder',
    description: 'Build governed AI companies with 90 agents and 1 human CEO. A 5-tier approval matrix, immutable audit trails, and 4 governance gates ensure every action is accountable.',
    eyebrow: 'AI OPERATING MODEL',
    oneLiner: '90 AI agents, 1 human CEO, zero excuses.',
    lead: 'Build governed AI companies with 90 agents and 1 human CEO.',
    honestyBadge: 'Fieldable in 2026',
    capabilities: [
      { title: 'Multi-Agent Orchestration', desc: '90 agents, 20 departments, each with explicit role definitions and approval thresholds.' },
      { title: '5-Tier Approval Matrix', desc: 'Auto through CEO sign-off with configurable thresholds and expiration sweeps.' },
      { title: 'Immutable Audit Trails', desc: 'SHA-256 sealed, append-only JSONL event logs for every agent action.' },
    ],
    useCases: [
      { title: 'Compliance Automation', lead: 'Agent-driven compliance reporting', proof: { label: 'Fieldable in 2026', tone: 'fieldable' } },
      { title: 'Risk Classification', lead: 'Automated risk classification for financial services', proof: { label: 'Fieldable in 2026', tone: 'fieldable' } },
      { title: 'Audit Trail Generation', lead: 'Immutable audit trails for every transaction', proof: { label: 'Proven in-house', tone: 'proven-in-house' } },
    ],
    spec: {
      problem: 'AI agents get deployed without approval controls, audit trails, or anyone accountable for what they do.',
      audience: 'Leadership teams deploying AI across departments who need governance before scale.',
      changes: 'Every agent action passes a 5-tier approval gate and lands in an immutable audit log.',
      builds: 'A 90-agent operating model: multi-agent orchestration, approval matrix, SHA-256 audit trails.',
      evidence: 'Audit trails proven in-house; compliance automation and risk classification fieldable in 2026.',
    },
    cta: { label: 'Explore AI Company Builder', to: '/ai-company-builder' },
  },
  {
    slug: 'digital-presence',
    title: 'Digital Presence',
    description: 'Mobile-first websites, e-commerce stores, and brand identities built for Southern Africa — with Airtel Money, TNM Mpamba, and PayChangu checkout built in from day one.',
    eyebrow: 'MOBILE-FIRST DESIGN',
    oneLiner: 'Southern Africa-first digital presence.',
    lead: 'Mobile-first websites and e-commerce built for Southern Africa.',
    honestyBadge: 'Fieldable in 2026',
    capabilities: [
      { title: 'Mobile-First Design', desc: 'Responsive websites built for mobile-first users across Malawi and SADC.' },
      { title: 'Payment Integration', desc: 'Airtel Money, TNM Mpamba, and PayChangu checkout built in from day one.' },
      { title: 'Brand Identity', desc: 'Cohesive brand identities designed for the African market.' },
    ],
    useCases: [
      { title: 'E-Commerce Store', lead: 'Online shops with local payment rails', proof: { label: 'Fieldable in 2026', tone: 'fieldable' } },
      { title: 'Brand Identity', lead: 'Cohesive visual identity for your brand', proof: { label: 'Proven in-house', tone: 'proven-in-house' } },
      { title: 'Web Development', lead: 'Mobile-first websites for any audience', proof: { label: 'In pilot', tone: 'pilot' } },
    ],
    spec: {
      problem: 'Selling online in Southern Africa requires mobile-first sites and mobile-money checkout — not foreign-card-only stores.',
      audience: 'Malawian and SADC SMEs, retailers, and brands serving mobile-first customers.',
      changes: 'Customers browse and pay with Airtel Money, TNM Mpamba, or PayChangu from day one.',
      builds: 'Mobile-first websites, e-commerce stores, and cohesive brand identities.',
      evidence: 'Brand identity proven in-house; web development in pilot; e-commerce fieldable in 2026.',
    },
    cta: { label: 'Explore Digital Presence', to: '/solutions' },
  },
  {
    slug: 'business-automation',
    title: 'Business Process Automation',
    description: 'WhatsApp-native assistants, automated document pipelines, and intelligent form workflows that connect your team to the tools they need without app downloads.',
    eyebrow: 'WORKFLOW AUTOMATION',
    oneLiner: 'Workflows that run on WhatsApp.',
    lead: 'WhatsApp-native assistants and automated document pipelines.',
    honestyBadge: 'In pilot',
    capabilities: [
      { title: 'WhatsApp-Native Assistants', desc: 'Assistants your team already uses, no app downloads required.' },
      { title: 'Document Pipelines', desc: 'Automated document generation and processing workflows.' },
      { title: 'Form Workflows', desc: 'Intelligent form workflows that connect your team to the tools they need.' },
    ],
    useCases: [
      { title: 'Document Automation', lead: 'Automated document pipelines', proof: { label: 'In pilot', tone: 'pilot' } },
      { title: 'Form Workflows', lead: 'Intelligent form workflows', proof: { label: 'Fieldable in 2026', tone: 'fieldable' } },
      { title: 'WhatsApp Integration', lead: 'WhatsApp-native assistants', proof: { label: 'Proven in-house', tone: 'proven-in-house' } },
    ],
    spec: {
      problem: 'Document, form, and team workflows still run manually, outside the tools people already use.',
      audience: 'Operations teams in NGOs, SMEs, and public institutions that already live in WhatsApp.',
      changes: 'Assistants, documents, and forms move through WhatsApp-native workflows — no app downloads.',
      builds: 'WhatsApp-native assistants, automated document pipelines, and intelligent form workflows.',
      evidence: 'WhatsApp integration proven in-house; document automation in pilot; form workflows fieldable in 2026.',
    },
    cta: { label: 'Explore Business Automation', to: '/solutions' },
  },
  {
    slug: 'enterprise-deployment',
    title: 'Enterprise Deployment',
    description: 'Full-scale AI agent deployment across departments with RBAC, 5-tier approval governance, and offline-first sovereignty on local infrastructure.',
    eyebrow: 'SCALED DEPLOYMENT',
    oneLiner: 'Enterprise-grade agent deployment.',
    lead: 'Full-scale AI agent deployment with RBAC and governance.',
    honestyBadge: 'In pilot',
    capabilities: [
      { title: 'RBAC', desc: 'Role-based access control across all agent operations.' },
      { title: '5-Tier Approval Governance', desc: 'Multi-tier human approval for every consequential action.' },
      { title: 'Offline-First Sovereignty', desc: 'Self-hosted orchestration with local infrastructure.' },
    ],
    useCases: [
      { title: 'Department Deployment', lead: 'Full-scale agent deployment across departments', proof: { label: 'In pilot', tone: 'pilot' } },
      { title: 'Access Control', lead: 'Role-based access control for all operations', proof: { label: 'Proven in-house', tone: 'proven-in-house' } },
      { title: 'Local Infrastructure', lead: 'Offline-first operation on local servers', proof: { label: 'In pilot', tone: 'pilot' } },
    ],
    spec: {
      problem: 'Department-by-department AI adoption without access control, approval governance, or sovereignty over where data lives.',
      audience: 'Enterprises and public institutions deploying agents across multiple departments.',
      changes: 'Every deployment runs behind RBAC, 5-tier approvals, and offline-first local infrastructure.',
      builds: 'Full-scale agent deployment with access control, governance, and self-hosted orchestration.',
      evidence: 'Access control proven in-house; department deployment and local infrastructure in pilot.',
    },
    cta: { label: 'Explore Enterprise Deployment', to: '/solutions' },
  },
  {
    slug: 'boardroom-briefing',
    title: 'Executive Boardroom Briefing',
    description: 'A focused session where LightSpeed presents the AI Company Builder platform, governance model, and engagement roadmap to your leadership team.',
    eyebrow: 'EXECUTIVE ADVISORY',
    oneLiner: 'Board-level AI strategy, delivered.',
    lead: 'A focused session where LightSpeed presents the AI Company Builder platform.',
    honestyBadge: 'Fieldable in 2026',
    capabilities: [
      { title: 'Platform Presentation', desc: 'LightSpeed presents the AI Company Builder platform in detail.' },
      { title: 'Governance Model', desc: 'Deep dive into the 5-tier approval matrix and governance framework.' },
      { title: 'Engagement Roadmap', desc: 'Clear roadmap for how LightSpeed can work with your team.' },
    ],
    useCases: [
      { title: 'Board Presentation', lead: 'Focused session for leadership teams', proof: { label: 'Fieldable in 2026', tone: 'fieldable' } },
      { title: 'Governance Deep-Dive', lead: 'Understanding the approval matrix', proof: { label: 'Proven in-house', tone: 'proven-in-house' } },
      { title: 'Roadmap Planning', lead: 'Engagement roadmap for your organisation', proof: { label: 'Fieldable in 2026', tone: 'fieldable' } },
    ],
    spec: {
      problem: 'Boards and leadership teams need a clear, honest view of the AI Company Builder platform and its governance model.',
      audience: 'Boards, executive teams, and leadership committees.',
      changes: 'Leaders leave aligned on governance, scope, and a concrete engagement roadmap.',
      builds: 'A focused session: platform presentation, governance deep-dive, and engagement roadmap.',
      evidence: 'Governance deep-dive proven in-house; sessions and roadmap planning fieldable in 2026.',
    },
    cta: { label: 'Request a Boardroom Briefing', to: '/solutions' },
  },
  {
    slug: 'data-intelligence',
    title: 'Data, Analytics & Donor Reporting',
    description: 'Automate donor-ready reports from Kobo and DHIS2 data in hours, not weeks. Clean data, generate narrative reports against donor templates, build interactive dashboards.',
    eyebrow: 'DATA & INTELLIGENCE',
    oneLiner: 'Donor reports in hours, not weeks.',
    lead: 'Automated data pipelines for development organisations.',
    honestyBadge: 'In pilot',
    capabilities: [
      { title: 'Data Cleaning & Analysis', desc: 'Clean dataset + insights report (Excel/PDF).' },
      { title: 'Donor/Project Reports', desc: 'Narrative + data-visualized quarterly/annual reports compliant with donor templates.' },
      { title: 'Interactive Dashboards', desc: 'Live web dashboard for program KPIs (mobile-friendly, NGO-grade).' },
    ],
    useCases: [
      { title: 'Data Cleaning', lead: 'Clean dataset + insights report', proof: { label: 'In pilot', tone: 'pilot' } },
      { title: 'Donor Reporting', lead: 'Narrative reports compliant with donor templates', proof: { label: 'In pilot', tone: 'pilot' } },
      { title: 'Program Dashboards', lead: 'Live KPI dashboards for field teams', proof: { label: 'Fieldable in 2026', tone: 'fieldable' } },
    ],
    spec: {
      problem: 'NGOs and development programmes spend weeks turning Kobo and DHIS2 data into donor-ready reports.',
      audience: 'NGOs, INGOs, UN Agencies, Agricultural Cooperatives, Research Organizations.',
      changes: 'Data pipelines automate cleaning, narrative generation, and dashboard delivery.',
      builds: 'Automated data cleaning, donor reports, and interactive dashboards.',
      evidence: 'Data cleaning and donor reporting in pilot; dashboards fieldable in 2026.',
    },
    cta: { label: 'Explore Data & Intelligence', to: '/solutions' },
  },
  {
    slug: 'ai-governance-policy',
    title: 'AI Governance & Policy',
    description: 'The governance layer that makes deployment safe. 5-tier HITL approvals, immutable audit trails, 4 mandatory gates (Contract, DPA, Compliance, Security).',
    eyebrow: 'GOVERNANCE',
    oneLiner: 'Safe deployment starts with governance.',
    lead: 'The governance layer that makes deployment safe.',
    honestyBadge: 'Proven in-house',
    capabilities: [
      { title: '5-Tier Approval Matrix', desc: 'Every action risk-classified and human-gated.' },
      { title: 'Immutable Audit Trails', desc: 'SHA-256 sealed, append-only JSONL event logs.' },
      { title: '4 Governance Gates', desc: 'Contract, DPA, Compliance, and Security reviews.' },
    ],
    useCases: [
      { title: 'Compliance Automation', lead: 'Agent-driven compliance reporting', proof: { label: 'Proven in-house', tone: 'proven-in-house' } },
      { title: 'Risk Classification', lead: 'Automated risk classification', proof: { label: 'Proven in-house', tone: 'proven-in-house' } },
      { title: 'Audit Trail Generation', lead: 'Immutable audit trails', proof: { label: 'Proven in-house', tone: 'proven-in-house' } },
    ],
    spec: {
      problem: 'Client-facing work can ship without human sign-off, compliance gates, or an audit trail.',
      audience: 'Every LightSpeed engagement — and any organisation deploying agents under our governance model.',
      changes: 'Four mandatory gates (Contract, DPA, Compliance, Security) run before work starts; every action is SHA-256 sealed.',
      builds: '5-tier approval matrix, immutable audit trails, and expiry sweeps for pending approvals.',
      evidence: 'Compliance automation, risk classification, and audit trails all proven in-house.',
    },
    cta: { label: 'View Governance Details', to: '/ai-company-builder' },
  },
  {
    slug: 'research-applied-ai',
    title: 'Research & Applied AI',
    description: 'Pharos thought leadership: Agentic AI, African AI, Open-Weight AI, AI Economics, AI Governance, AI Policy, Sovereign AI, Resource-Constrained Deployment.',
    eyebrow: 'THOUGHT LEADERSHIP',
    oneLiner: 'Evidence-led AI research for Africa.',
    lead: 'Turning engineering into public intellectual work.',
    honestyBadge: 'Proven in-house',
    capabilities: [
      { title: 'Pharos Insights', desc: 'Monthly Malawi Agentic AI Monitor, white papers, policy briefs.' },
      { title: 'Open-Weight Research', desc: 'Model routing, local inference, cost optimization for African contexts.' },
      { title: 'Policy Research', desc: 'SADC governance frameworks, national AI strategy, regulatory alignment.' },
    ],
    useCases: [
      { title: 'Policy Briefs', lead: 'Evidence-based policy recommendations', proof: { label: 'Proven in-house', tone: 'proven-in-house' } },
      { title: 'Model Routing Studies', lead: 'Cost/quality optimization for resource-constrained environments', proof: { label: 'Fieldable in 2026', tone: 'fieldable' } },
      { title: 'African AI Economics', lead: 'API dependency vs local inference analysis', proof: { label: 'Proven in-house', tone: 'proven-in-house' } },
    ],
    spec: {
      problem: 'African leaders need evidence-led research on agentic AI, not vendor marketing.',
      audience: 'Governments, regulators, universities, development partners, SADC institutions.',
      changes: 'Pharos publishes research notes, field notes, policy notes, system maps, and data stories.',
      builds: 'Monthly Monitor, quarterly white papers, policy briefs, research notes.',
      evidence: 'Pharos research proven in-house; policy engagement fieldable in 2026.',
    },
    cta: { label: 'Read Pharos Insights', to: '/insights' },
  },
  {
    slug: 'platform-licensing',
    title: 'Platform Licensing',
    description: 'Run your own governed AI workforce self-hosted on your infrastructure. License the AI Company Builder, get onboarding, operate your own 90-agent company.',
    eyebrow: 'PLATFORM LICENSING',
    oneLiner: 'Your AI company, your infrastructure.',
    lead: 'Self-hosted AI Company Builder for tech-savvy teams.',
    honestyBadge: 'Fieldable in 2026',
    capabilities: [
      { title: 'AI Company Builder License', desc: 'One-on-one onboarding, your own governed AI company running on your laptop/VPS.' },
      { title: 'Agent Setup for Agencies', desc: 'White-label: we stand up agent teams for your agency\'s clients.' },
    ],
    useCases: [
      { title: 'Self-Hosted Deployment', lead: 'Run AI Company Builder on your infrastructure', proof: { label: 'Fieldable in 2026', tone: 'fieldable' } },
      { title: 'Agency White-Label', lead: 'Stand up agent teams for your clients', proof: { label: 'In development', tone: 'development' } },
    ],
    spec: {
      problem: 'Tech-savvy teams want full control over their AI workforce without vendor lock-in.',
      audience: 'Tech-savvy founders, local tech agencies, diaspora entrepreneurs, software developers.',
      changes: 'License includes full platform, onboarding, and support retainer.',
      builds: 'Self-hosted 90-agent orchestration platform with governance.',
      evidence: 'Platform runs LightSpeed internally (proven in-house); licensing fieldable in 2026.',
    },
    cta: { label: 'Explore Platform Licensing', to: '/solutions' },
  },
];

export function getSolutionBySlug(slug: string): Solution | undefined {
  return solutionsRegistry.find(s => s.slug === slug);
}

export function getSolutionsByHonestyBadge(badge: Solution['honestyBadge']): Solution[] {
  return solutionsRegistry.filter(s => s.honestyBadge === badge);
}

export default solutionsRegistry;
