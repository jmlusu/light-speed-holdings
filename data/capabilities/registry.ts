/**
 * Capabilities Registry — Canonical Source of Truth
 *
 * Source: company-registry.yaml + Directive §15
 * Directive §22 — Single source for all capabilities
 */

export type CapabilityCategory = 'strategy' | 'build' | 'govern' | 'research-policy';
export type HonestyTier = 'verified' | 'proven-in-house' | 'fieldable' | 'pilot' | 'development';

export interface Capability {
  id: string;
  title: string;
  description: string;
  category: CapabilityCategory;
  honestyTier: HonestyTier;
  relatedSolutions: string[];  // Solution slugs
  relatedUseCases: string[];   // Use case slugs
  source: string;
}

export const capabilitiesRegistry: Capability[] = [
  // STRATEGY
  {
    id: 'ai-strategy',
    title: 'AI Strategy',
    description: 'Define organizational AI vision, identify high-impact use cases, and build roadmaps aligned with business objectives.',
    category: 'strategy',
    honestyTier: 'proven-in-house',
    relatedSolutions: ['ai-company-builder', 'boardroom-briefing'],
    relatedUseCases: ['executive-ai-readiness', 'strategic-roadmapping'],
    source: 'company-registry.yaml (CPO, CSO responsibilities)',
  },
  {
    id: 'ai-readiness',
    title: 'AI Readiness Assessment',
    description: 'Structured evaluation of data maturity, infrastructure, talent, and governance gaps to determine AI adoption readiness.',
    category: 'strategy',
    honestyTier: 'proven-in-house',
    relatedSolutions: ['boardroom-briefing', 'enterprise-deployment'],
    relatedUseCases: ['readiness-assessment', 'gap-analysis'],
    source: 'company-registry.yaml (CPO, Consulting Lead responsibilities)',
  },
  {
    id: 'digital-transformation',
    title: 'Digital Transformation',
    description: 'Guide organizations from legacy digital systems to AI-native operating models with phased migration strategies.',
    category: 'strategy',
    honestyTier: 'proven-in-house',
    relatedSolutions: ['digital-presence', 'enterprise-deployment'],
    relatedUseCases: ['legacy-migration', 'platform-modernization'],
    source: 'company-registry.yaml (CSO, CTO responsibilities)',
  },
  {
    id: 'data-architecture',
    title: 'Data Architecture',
    description: 'Design sovereign, compliant data pipelines and governance frameworks for AI workloads in African regulatory contexts.',
    category: 'strategy',
    honestyTier: 'proven-in-house',
    relatedSolutions: ['enterprise-deployment', 'business-automation'],
    relatedUseCases: ['data-sovereignty', 'pipeline-design'],
    source: 'company-registry.yaml (CDO responsibilities)',
  },

  // BUILD
  {
    id: 'agentic-workflow-design',
    title: 'Agentic Workflow Design',
    description: 'Design multi-agent workflows with explicit role definitions, approval thresholds, and orchestration logic.',
    category: 'build',
    honestyTier: 'proven-in-house',
    relatedSolutions: ['ai-company-builder', 'business-automation'],
    relatedUseCases: ['compliance-automation', 'document-pipeline', 'customer-service'],
    source: 'company-registry.yaml (CTO, Orchestration Owner responsibilities)',
  },
  {
    id: 'ai-implementation',
    title: 'AI Implementation',
    description: 'Deploy governed AI agents with RBAC, approval governance, and offline-first sovereignty on local infrastructure.',
    category: 'build',
    honestyTier: 'fieldable',
    relatedSolutions: ['ai-company-builder', 'enterprise-deployment', 'platform-licensing'],
    relatedUseCases: ['department-deployment', 'local-infrastructure', 'access-control'],
    source: 'company-registry.yaml (VP Engineering, Orchestration Owner responsibilities)',
  },
  {
    id: 'governance-implementation',
    title: 'Governance Implementation',
    description: 'Implement 5-tier approval matrix, immutable audit trails, and 4 governance gates (Contract, DPA, Compliance, Security).',
    category: 'build',
    honestyTier: 'proven-in-house',
    relatedSolutions: ['ai-company-builder', 'enterprise-deployment'],
    relatedUseCases: ['approval-matrix', 'audit-trail-generation', 'governance-gates'],
    source: 'company-registry.yaml (CISO, Security Compliance Lead responsibilities)',
  },

  // GOVERN
  {
    id: 'ai-policy',
    title: 'AI Policy',
    description: 'Develop organizational AI policies aligned with Malawi DPA, SADC frameworks, and AU Continental AI Strategy.',
    category: 'govern',
    honestyTier: 'fieldable',
    relatedSolutions: ['boardroom-briefing', 'ai-governance-policy'],
    relatedUseCases: ['policy-development', 'regulatory-alignment'],
    source: 'company-registry.yaml (CLO, Agentic Policy Analyst responsibilities)',
  },
  {
    id: 'ai-governance',
    title: 'AI Governance',
    description: 'Establish ongoing governance cadence: weekly standup → bi-weekly review → monthly board → quarterly strategy → annual refresh.',
    category: 'govern',
    honestyTier: 'proven-in-house',
    relatedSolutions: ['ai-company-builder', 'boardroom-briefing'],
    relatedUseCases: ['governance-cadence', 'board-reporting'],
    source: 'company-registry.yaml (Chief of Staff, CEO Advisor responsibilities)',
  },
  {
    id: 'institutional-capacity-building',
    title: 'Institutional Capacity Building',
    description: 'Build sovereign agentic-AI talent pipelines through university partnerships, training programs, and certification.',
    category: 'govern',
    honestyTier: 'future',
    relatedSolutions: ['boardroom-briefing', 'research-applied-ai'],
    relatedUseCases: ['university-partnerships', 'talent-certification'],
    source: 'Directive §12 (strategic sectors: academia, research, universities)',
  },

  // RESEARCH & POLICY
  {
    id: 'applied-ai-research',
    title: 'Applied AI Research',
    description: 'Conduct research on African AI deployment, open-weight model optimization, resource-constrained inference, and sovereign AI.',
    category: 'research-policy',
    honestyTier: 'proven-in-house',
    relatedSolutions: ['research-applied-ai', 'ai-governance-policy'],
    relatedUseCases: ['model-routing-optimization', 'african-ai-economics', 'local-inference'],
    source: 'company-registry.yaml (CAIO, ML Engineer, Pharos responsibilities)',
  },
  {
    id: 'ai-governance-research',
    title: 'AI Governance Research',
    description: 'Research approval matrices, risk assessment frameworks, audit trail standards, and regulatory alignment for agentic AI.',
    category: 'research-policy',
    honestyTier: 'fieldable',
    relatedSolutions: ['ai-governance-policy', 'boardroom-briefing'],
    relatedUseCases: ['sadc-framework', 'national-ai-strategy', 'approval-matrix-research'],
    source: 'Directive §13 (Pharos: AI Governance, AI Policy, AI Regulation)',
  },
  {
    id: 'african-ai-deployment-studies',
    title: 'African AI Deployment Studies',
    description: 'Study low-bandwidth, intermittent connectivity, data sovereignty, and local compute deployment patterns across SADC.',
    category: 'research-policy',
    honestyTier: 'fieldable',
    relatedSolutions: ['research-applied-ai', 'platform-licensing'],
    relatedUseCases: ['offline-first-deployment', 'low-bandwidth-optimization', 'data-sovereignty'],
    source: 'Directive §4 (Africa-first AI economics)',
  },
];

export function getCapabilityById(id: string): Capability | undefined {
  return capabilitiesRegistry.find(c => c.id === id);
}

export function getCapabilitiesByCategory(category: CapabilityCategory): Capability[] {
  return capabilitiesRegistry.filter(c => c.category === category);
}

export function getCapabilitiesByHonestyTier(tier: HonestyTier): Capability[] {
  return capabilitiesRegistry.filter(c => c.honestyTier === tier);
}

export default capabilitiesRegistry;
