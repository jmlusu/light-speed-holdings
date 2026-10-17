/**
 * Sectors Registry — Canonical Source of Truth
 *
 * Source: Directive §12 + sector-registry.ts
 * Directive §22 — Single source for all sectors
 *
 * 10 Canonical Sectors with evidence-based status
 */

export type SectorStatusTone = 'proven' | 'pilot' | 'fieldable' | 'development';

export interface SectorStatus {
  label: string;
  tone: SectorStatusTone;
}

export interface Sector {
  id: string;
  title: string;
  description: string;
  status: SectorStatus;
  evidence: string;
  region: string[];
  relevantSolutions: string[];
  useCases: string[];
  keyMetrics?: string[];
  iconName?: string;
}

export const sectorsRegistry: Sector[] = [
  {
    id: 'financial-services',
    title: 'Financial Services',
    description: 'Risk classification, audit trails, and regulatory reporting for banks, microfinance, SACCOs, and mobile-money providers.',
    status: { label: 'PROVEN EXPERIENCE', tone: 'proven' },
    evidence: 'Governed multi-agent compliance automation for a regional financial institution: regulatory reporting across 14 departments with full audit trails, cutting reporting time by 40%.',
    region: ['Malawi', 'SADC'],
    relevantSolutions: ['ai-company-builder', 'enterprise-deployment', 'business-automation', 'ai-governance-policy', 'data-intelligence'],
    useCases: ['compliance-automation', 'risk-classification', 'audit-trail-generation', 'market-intelligence', 'regulatory-monitoring'],
    keyMetrics: ['40% reporting time reduction', '14 departments automated', 'Zero audit findings'],
    iconName: 'Building2',
  },
  {
    id: 'healthcare',
    title: 'Healthcare & Public Health',
    description: 'Data pipelines, reporting automation, clinical decision support, and supply chain monitoring for clinics and health systems.',
    status: { label: 'FUTURE OPPORTUNITY', tone: 'development' },
    evidence: 'Offline-first, sovereignty-first architecture designed for clinical data — but LightSpeed has no healthcare deployment yet. Listed honestly as a roadmap target.',
    region: ['Malawi', 'SADC'],
    relevantSolutions: ['enterprise-deployment', 'business-automation', 'data-intelligence', 'ai-governance-policy'],
    useCases: ['donor-reporting', 'data-cleaning', 'supply-chain-monitoring', 'clinical-decision-support'],
    keyMetrics: [],
    iconName: 'Activity',
  },
  {
    id: 'agriculture',
    title: 'Agriculture & Agritech',
    description: 'Supply-chain intelligence, mobile-money coordination, climate-data pipelines, and farmer advisory for rural economies.',
    status: { label: 'CURRENT CAPABILITY', tone: 'pilot' },
    evidence: 'WhatsApp-native coordination platform for agricultural cooperatives across Malawi and Mozambique, with mobile-money payments and supply chain tracking — serving 1,200 members in pilot.',
    region: ['Malawi', 'Mozambique', 'SADC'],
    relevantSolutions: ['digital-presence', 'business-automation', 'enterprise-deployment', 'data-intelligence', 'platform-licensing'],
    useCases: ['agricultural-coordination', 'market-intelligence', 'mobile-money-coordination', 'farmer-advisory'],
    keyMetrics: ['1,200 cooperative members in pilot', 'Malawi + Mozambique coverage', 'Mobile-money integration'],
    iconName: 'Sprout',
  },
  {
    id: 'education',
    title: 'Education & Academia',
    description: 'Student management, credential verification, research administration, and data-driven policy for schools and universities.',
    status: { label: 'CURRENT CAPABILITY', tone: 'pilot' },
    evidence: 'Agent-driven student management at the University of Malawi — 3 departments onboarded, 5,000 records processed with immutable audit trails.',
    region: ['Malawi', 'SADC'],
    relevantSolutions: ['ai-company-builder', 'enterprise-deployment', 'business-automation', 'data-intelligence', 'research-applied-ai'],
    useCases: ['student-management', 'credential-verification', 'university-research-support', 'policy-analysis'],
    keyMetrics: ['3 departments onboarded', '5,000 records processed', 'Immutable audit trails'],
    iconName: 'GraduationCap',
  },
  {
    id: 'government',
    title: 'Government & Public Sector',
    description: 'Digital services, compliance automation, citizen engagement, and data-driven policy for ministries and agencies.',
    status: { label: 'CURRENT CAPABILITY', tone: 'pilot' },
    evidence: "Advisory work on Malawi's National AI Strategy consultation. Policy-level engagement so far — no ministerial production deployment claimed.",
    region: ['Malawi', 'SADC'],
    relevantSolutions: ['ai-company-builder', 'enterprise-deployment', 'boardroom-briefing', 'ai-governance-policy', 'data-intelligence'],
    useCases: ['compliance-automation', 'citizen-engagement', 'policy-analysis', 'regulatory-monitoring', 'legislative-summarization'],
    keyMetrics: ['National AI Strategy consultation', 'Policy-level engagement'],
    iconName: 'Landmark',
  },
  {
    id: 'regulators',
    title: 'Regulators & Standards Institutions',
    description: 'Regulatory monitoring, sandbox frameworks, compliance tracking, and standards development for AI governance.',
    status: { label: 'FUTURE OPPORTUNITY', tone: 'development' },
    evidence: 'SADC Agentic AI Governance Framework in development; engagement with MACRA, CRASA, central banks, and regional development banks. Aligned with AU Continental AI Strategy.',
    region: ['Malawi', 'SADC', 'Africa'],
    relevantSolutions: ['ai-governance-policy', 'boardroom-briefing', 'research-applied-ai', 'enterprise-deployment'],
    useCases: ['regulatory-monitoring', 'sandbox-frameworks', 'standards-development', 'policy-analysis'],
    keyMetrics: ['SADC Framework in development', 'MACRA/CRASA engagement', 'AU Continental AI Strategy alignment'],
    iconName: 'Gavel',
  },
  {
    id: 'research',
    title: 'Research & Universities',
    description: 'Applied AI research, literature synthesis, grant administration, and sovereign talent pipeline development.',
    status: { label: 'FUTURE OPPORTUNITY', tone: 'development' },
    evidence: 'Capacity building programs with Malawian universities (MUBAS, UNIMA) in development. Pharos research program active. No formal university partnerships signed yet.',
    region: ['Malawi', 'SADC'],
    relevantSolutions: ['research-applied-ai', 'boardroom-briefing', 'data-intelligence', 'platform-licensing'],
    useCases: ['research-synthesis', 'university-research-support', 'grant-administration', 'talent-pipeline'],
    keyMetrics: ['Pharos research active', 'MUBAS/UNIMA discussions'],
    iconName: 'Microscope',
  },
  {
    id: 'smes',
    title: 'SMEs & Private Enterprise',
    description: 'Company-in-a-Box lightweight agent sets for Marketing, Sales, Compliance, Finance, HR — demonstrated live at J&S StopOver Bar.',
    status: { label: 'FIELDABLE', tone: 'fieldable' },
    evidence: 'J&S StopOver Bar provides live proof-of-concept: inventory, sales, cash reconciliation, procurement, profitability monitoring via agentic decision support.',
    region: ['Malawi', 'SADC'],
    relevantSolutions: ['ai-company-builder', 'platform-licensing', 'business-automation', 'digital-presence', 'data-intelligence'],
    useCases: ['sme-operations', 'customer-service', 'digital-presence', 'market-intelligence', 'inventory-management'],
    keyMetrics: ['Live at J&S StopOver Bar', '5 departments covered', 'Non-tech SME in Malawi market'],
    iconName: 'Store',
  },
  {
    id: 'development',
    title: 'Development & Nonprofit Organizations',
    description: 'Donor reporting automation, Kobo/DHIS2 pipelines, program dashboards, and field coordination for NGOs and INGOs.',
    status: { label: 'PILOT', tone: 'pilot' },
    evidence: 'Kobo/DHIS2 donor reporting pipeline in pilot with development organisations. NGO-grade dashboards in development. No signed engagement with named INGO yet.',
    region: ['Malawi', 'SADC', 'Africa'],
    relevantSolutions: ['data-intelligence', 'business-automation', 'enterprise-deployment', 'platform-licensing', 'ai-governance-policy'],
    useCases: ['donor-reporting', 'data-cleaning', 'program-dashboards', 'field-coordination', 'grant-administration'],
    keyMetrics: ['Kobo/DHIS2 integration in pilot', 'NGO-grade dashboards in development'],
    iconName: 'Heart',
  },
  {
    id: 'technology',
    title: 'Technology & Digital Businesses',
    description: 'Platform licensing, self-hosted AI Company Builder, agent white-label for agencies, and developer tooling.',
    status: { label: 'FIELDABLE', tone: 'fieldable' },
    evidence: 'Platform Licensing (E1) fieldable 2026: AI Company Builder self-hosted on laptop/VPS with onboarding. LightSpeed runs on same platform internally (proven in-house).',
    region: ['Malawi', 'SADC', 'Global'],
    relevantSolutions: ['platform-licensing', 'ai-company-builder', 'research-applied-ai', 'data-intelligence'],
    useCases: ['self-hosted-deployment', 'agency-white-label', 'developer-tooling', 'model-routing', 'local-inference'],
    keyMetrics: ['E1 license fieldable 2026', 'Self-hosted on laptop/VPS', 'Internal dogfooding proven'],
    iconName: 'Cpu',
  },
];

export const sectorTierLegend = [
  { tier: { label: 'PROVEN EXPERIENCE', tone: 'proven' as SectorStatusTone }, desc: 'Delivered engagements with named, measurable outcomes.' },
  { tier: { label: 'CURRENT CAPABILITY', tone: 'pilot' as SectorStatusTone }, desc: 'Running pilots or capability we can deploy now.' },
  { tier: { label: 'DEMONSTRATION', tone: 'fieldable' as SectorStatusTone }, desc: 'Working demonstration without a live client engagement.' },
  { tier: { label: 'FUTURE OPPORTUNITY', tone: 'development' as SectorStatusTone }, desc: 'Roadmap target — no evidence yet, and we say so.' },
];

export function getSectorById(id: string): Sector | undefined {
  return sectorsRegistry.find(s => s.id === id);
}

export function getSectorsByStatus(tone: SectorStatusTone): Sector[] {
  return sectorsRegistry.filter(s => s.status.tone === tone);
}

export function getSectorsByRegion(region: string): Sector[] {
  return sectorsRegistry.filter(s => s.region.includes(region));
}

export function getSectorsBySolution(solutionSlug: string): Sector[] {
  return sectorsRegistry.filter(s => s.relevantSolutions.includes(solutionSlug));
}

export function getSolutionsBySector(sectorId: string): string[] {
  const sector = getSectorById(sectorId);
  return sector?.relevantSolutions ?? [];
}

export function getUseCasesBySector(sectorId: string): string[] {
  const sector = getSectorById(sectorId);
  return sector?.useCases ?? [];
}

export default sectorsRegistry;
