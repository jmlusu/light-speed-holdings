/**
 * Use Cases Registry — Canonical Source of Truth
 *
 * Source: Directive §10-11 + useCaseCatalogData.ts
 * Directive §22 — Single source for all use cases
 *
 * Status: LIVE | PROVEN_IN_HOUSE | PILOT | DEMONSTRATION | FIELDABLE | FUTURE
 * Filters: BY PROBLEM, BY SOLUTION, BY SECTOR, BY STATUS
 */

export type UseCaseStatus = 'LIVE' | 'PROVEN_IN_HOUSE' | 'PILOT' | 'DEMONSTRATION' | 'FIELDABLE' | 'FUTURE';

export type ProblemCategory =
  | 'Cost'
  | 'Operational Latency'
  | 'Compliance'
  | 'Reporting'
  | 'Customer Experience'
  | 'Decision Intelligence'
  | 'Growth'
  | 'Administration'
  | 'Research'
  | 'Knowledge Work'
  | 'Market Intelligence';

export type SolutionCategory =
  | 'Strategy'
  | 'Agentic Automation'
  | 'Data & Intelligence'
  | 'Digital Transformation'
  | 'AI Governance'
  | 'Research & Policy';

export interface UseCase {
  slug: string;
  title: string;
  problem: string;
  workflow: string;
  agentsInvolved: string[];     // Agent IDs from company-registry.yaml
  inputs: string[];
  orchestration: string;
  tools: string[];
  humanApproval: string;
  output: string;
  businessValue: string;
  sector: string[];             // Sector IDs from sectors registry
  solution: string[];           // Solution slugs from solutions registry
  status: UseCaseStatus;
  evidence?: string;            // Link to evidence/case study
  featured?: boolean;
  thumbnail?: string;           // Media asset reference
  problemCategory: ProblemCategory[];
  solutionCategory: SolutionCategory[];
}

export const useCasesRegistry: UseCase[] = [
  {
    slug: 'compliance-automation',
    title: 'Compliance Automation',
    problem: 'Regulatory reporting across multiple departments is manual, error-prone, and lacks audit trails.',
    workflow: 'Regulatory change → Agent classification → Data extraction → Report generation → Human review → Submission → Audit log',
    agentsInvolved: ['compliance-specialist', 'risk-classifier', 'document-generator', 'audit-trail-agent', 'approval-gate'],
    inputs: ['Regulatory frameworks', 'Transaction data', 'Departmental records'],
    orchestration: 'MessageBus routes tasks through compliance-specialist → risk-classifier → document-generator with approval-gate at each stage',
    tools: ['Regulatory API', 'Database connectors', 'Document templates', 'SHA-256 audit logger'],
    humanApproval: 'Tier 3 (Dual: Compliance Lead + CISO) for report submission; Tier 4 (Executive) for regulatory filings',
    output: 'Regulatory reports with immutable audit trails',
    businessValue: 'Audit-ready evidence for every data point',
    sector: ['financial-services', 'government'],
    solution: ['ai-company-builder', 'enterprise-deployment', 'ai-governance-policy'],
    status: 'FIELDABLE',
    evidence: 'Governed multi-agent compliance automation proven in-house: 5-tier approval gating, full audit trails',
    featured: true,
    thumbnail: 'use-cases/compliance-automation.webp',
    problemCategory: ['Compliance', 'Reporting', 'Operational Latency'],
    solutionCategory: ['Agentic Automation', 'AI Governance'],
  },
  {
    slug: 'agricultural-coordination',
    title: 'Agricultural Cooperative Coordination',
    problem: 'Smallholder farmers and cooperatives lack coordination tools for supply chain, mobile-money payments, and market access.',
    workflow: 'Farmer input → Weather/soil advisory → Supply chain tracking → Mobile-money settlement → Cooperative dashboard',
    agentsInvolved: ['weather-advisor', 'soil-analyst', 'supply-chain-tracker', 'mobile-money-coordinator', 'cooperative-dashboard'],
    inputs: ['Weather data', 'Soil sensors', 'Farmer mobile inputs', 'Market prices', 'Mobile-money APIs'],
    orchestration: 'WhatsApp-native interface → Agent cluster processes → Mobile-money integration → Dashboard updates',
    tools: ['WhatsApp Business API', 'Airtel Money API', 'TNM Mpamba API', 'Weather API', 'Market data feeds'],
    humanApproval: 'Tier 2 (Lead) for payment release; Tier 3 (Dual) for cooperative-level decisions',
    output: 'Coordinated supply chain with transparent payments',
    businessValue: 'Pilot serving 1,200 cooperative members across Malawi and Mozambique',
    sector: ['agriculture', 'fintech'],
    solution: ['business-automation', 'digital-presence', 'enterprise-deployment'],
    status: 'PILOT',
    evidence: 'WhatsApp-native coordination platform for agricultural cooperatives in Malawi/Mozambique, 1,200 members in pilot',
    featured: true,
    thumbnail: 'use-cases/agricultural-coordination.webp',
    problemCategory: ['Operational Latency', 'Customer Experience', 'Market Intelligence'],
    solutionCategory: ['Agentic Automation', 'Digital Transformation'],
  },
  {
    slug: 'donor-reporting',
    title: 'Donor Reporting Automation',
    problem: 'NGOs spend weeks manually cleaning Kobo/DHIS2 data and writing narrative reports against donor templates.',
    workflow: 'Raw data ingestion → Cleaning/validation → Template mapping → Narrative generation → Human review → Dashboard publish',
    agentsInvolved: ['data-cleaner', 'template-mapper', 'narrative-generator', 'dashboard-builder', 'approval-gate'],
    inputs: ['KoboToolbox exports', 'DHIS2 data', 'Donor templates', 'Program indicators'],
    orchestration: 'Data pipeline → Agent processing → Review gate → Multi-format output (PDF, Excel, Web dashboard)',
    tools: ['Kobo API', 'DHIS2 API', 'Pandas/Polars', 'Jinja2 templates', 'Recharts dashboards'],
    humanApproval: 'Tier 2 (Lead) for data validation; Tier 3 (Dual: Program Lead + Finance) for donor submission',
    output: 'Donor-ready quarterly/annual reports + interactive dashboards',
    businessValue: 'Reporting time reduced from weeks to hours; donor compliance improved',
    sector: ['development', 'healthcare'],
    solution: ['data-intelligence', 'business-automation', 'enterprise-deployment'],
    status: 'PILOT',
    evidence: 'Automated donor reporting pipeline in pilot with development organisations; Kobo/DHIS2 integration',
    featured: true,
    thumbnail: 'use-cases/donor-reporting.webp',
    problemCategory: ['Reporting', 'Operational Latency', 'Administration'],
    solutionCategory: ['Data & Intelligence', 'Agentic Automation'],
  },
  {
    slug: 'data-cleaning',
    title: 'Data Cleaning & Analysis',
    problem: 'Raw field data is messy, incomplete, and requires significant manual cleaning before analysis.',
    workflow: 'Raw data → Schema validation → Anomaly detection → Imputation → Enrichment → Analysis report',
    agentsInvolved: ['data-validator', 'anomaly-detector', 'imputation-engine', 'enrichment-agent', 'analyst'],
    inputs: ['CSV/Excel exports', 'API data', 'Survey responses', 'Sensor logs'],
    orchestration: 'Parallel validation → Consensus cleaning → Human spot-check → Enriched output',
    tools: ['Pandas/Polars', 'Great Expectations', 'Custom validation rules', 'External enrichment APIs'],
    humanApproval: 'Tier 1 (Auto) for standard cleaning; Tier 2 (Lead) for imputation decisions',
    output: 'Clean dataset + insights report (Excel/PDF)',
    businessValue: 'Hours instead of days for data preparation; reproducible cleaning pipeline',
    sector: ['development', 'healthcare', 'agriculture', 'education'],
    solution: ['data-intelligence', 'business-automation'],
    status: 'FIELDABLE',
    evidence: 'Data cleaning pipelines proven in-house; used across LightSpeed engagements',
    featured: false,
    thumbnail: 'use-cases/data-cleaning.webp',
    problemCategory: ['Operational Latency', 'Knowledge Work', 'Administration'],
    solutionCategory: ['Data & Intelligence', 'Agentic Automation'],
  },
  {
    slug: 'sme-operations',
    title: 'SME Operations (Company-in-a-Box)',
    problem: 'Malawian SMEs cannot afford full teams but need Marketing, Sales, Compliance, Finance, HR capabilities.',
    workflow: 'Business context → Agent role assignment → Daily operations → Dashboard → Human oversight',
    agentsInvolved: ['marketing-agent', 'sales-agent', 'compliance-agent', 'finance-agent', 'hr-agent', 'ceo-dashboard'],
    inputs: ['Business data', 'Sales records', 'Inventory', 'Customer interactions', 'Financial transactions'],
    orchestration: 'Lightweight agent set per function → Shared memory → CEO dashboard for oversight',
    tools: ['Local inference (Ollama)', 'WhatsApp Business', 'Mobile-money APIs', 'Accounting software APIs'],
    humanApproval: 'Tier 1 (Auto) for daily ops; Tier 2 (Lead) for exceptions; Tier 4 (Executive) for strategy',
    output: 'Functional coverage across 5 departments at fraction of headcount cost',
    businessValue: 'Live at J&S StopOver Bar: inventory, sales, cash reconciliation, procurement, profitability monitoring',
    sector: ['smes'],
    solution: ['ai-company-builder', 'platform-licensing', 'business-automation'],
    status: 'FIELDABLE',
    evidence: 'J&S StopOver Bar live proof: non-tech SME running agentic decision support in Malawi market',
    featured: true,
    thumbnail: 'use-cases/sme-operations.webp',
    problemCategory: ['Cost', 'Operational Latency', 'Administration', 'Growth'],
    solutionCategory: ['Agentic Automation', 'Strategy', 'Digital Transformation'],
  },
  {
    slug: 'customer-service',
    title: 'Customer Service Automation',
    problem: 'High-volume customer inquiries overwhelm small teams; 24/7 coverage unaffordable.',
    workflow: 'Inquiry → Intent classification → FAQ resolution → Escalation to human → Resolution logging',
    agentsInvolved: ['intent-classifier', 'faq-responder', 'escalation-router', 'resolution-logger'],
    inputs: ['WhatsApp messages', 'Email', 'Chat history', 'Knowledge base'],
    orchestration: 'WhatsApp-native → Auto-resolve 80% → Human handoff for complex → Full conversation log',
    tools: ['WhatsApp Business API', 'Vector search (knowledge base)', 'Ticketing system', 'Analytics'],
    humanApproval: 'Tier 1 (Auto) for FAQ; Tier 2 (Lead) for escalation routing',
    output: '24/7 customer response with human escalation path',
    businessValue: '80% auto-resolution; 90% faster response times',
    sector: ['smes', 'technology', 'healthcare'],
    solution: ['business-automation', 'digital-presence'],
    status: 'FIELDABLE',
    evidence: 'WhatsApp-native assistants proven in-house; customer service flows fieldable 2026',
    featured: false,
    thumbnail: 'use-cases/customer-service.webp',
    problemCategory: ['Customer Experience', 'Operational Latency', 'Cost'],
    solutionCategory: ['Agentic Automation', 'Digital Transformation'],
  },
  {
    slug: 'market-intelligence',
    title: 'Market Intelligence & Competitive Analysis',
    problem: 'Organizations lack systematic market monitoring, competitor tracking, and opportunity identification.',
    workflow: 'Source monitoring → Entity extraction → Signal classification → Trend analysis → Alert generation → Briefing',
    agentsInvolved: ['source-monitor', 'entity-extractor', 'signal-classifier', 'trend-analyst', 'briefing-generator'],
    inputs: ['News APIs', 'Regulatory gazettes', 'Tender portals', 'Social media', 'Company filings'],
    orchestration: 'Continuous monitoring → Batch analysis → Daily/weekly briefings → Dashboard',
    tools: ['News APIs', 'Web scraping', 'NLP pipelines', 'Vector databases', 'Alerting'],
    humanApproval: 'Tier 1 (Auto) for monitoring; Tier 2 (Lead) for strategic alerts',
    output: 'Automated market intelligence briefings and dashboards',
    businessValue: 'Continuous situational awareness without dedicated analyst team',
    sector: ['financial-services', 'technology', 'government', 'development'],
    solution: ['research-applied-ai', 'data-intelligence', 'ai-company-builder'],
    status: 'FIELDABLE',
    evidence: 'Market intelligence agents proven in-house; used for SADC opportunity tracking',
    featured: false,
    thumbnail: 'use-cases/market-intelligence.webp',
    problemCategory: ['Market Intelligence', 'Decision Intelligence', 'Growth'],
    solutionCategory: ['Research & Policy', 'Data & Intelligence'],
  },
  {
    slug: 'research-synthesis',
    title: 'Research Synthesis & Literature Review',
    problem: 'Research teams spend weeks manually reviewing papers, extracting findings, and synthesizing across sources.',
    workflow: 'Query formulation → Multi-source search → Deduplication → Extraction → Synthesis → Citation mapping → Report',
    agentsInvolved: ['query-formulator', 'search-agent', 'deduplicator', 'extractor', 'synthesizer', 'citation-mapper'],
    inputs: ['Research questions', 'arXiv/PubMed/CrossRef', 'Internal documents', 'Grey literature'],
    orchestration: 'PRISMA-aligned pipeline → Human validation → Evidence-bounded output',
    tools: ['arXiv API', 'OpenAlex', 'CrossRef', 'Semantic Scholar', 'Zotero', 'Citation verification'],
    humanApproval: 'Tier 2 (Lead) for inclusion decisions; Tier 3 (Dual) for conclusion validation',
    output: 'Systematic review draft with claim-to-source mapping and audit trail',
    businessValue: 'Weeks → days for literature reviews; reproducible, auditable process',
    sector: ['research', 'education', 'healthcare', 'government'],
    solution: ['research-applied-ai', 'data-intelligence'],
    status: 'FIELDABLE',
    evidence: 'Research synthesis pipelines proven in-house (k-dense-literature-review skill)',
    featured: false,
    thumbnail: 'use-cases/research-synthesis.webp',
    problemCategory: ['Research', 'Knowledge Work', 'Operational Latency'],
    solutionCategory: ['Research & Policy', 'Data & Intelligence'],
  },
  {
    slug: 'regulatory-monitoring',
    title: 'Regulatory Monitoring & Compliance Tracking',
    problem: 'Organizations miss regulatory changes, deadlines, and compliance requirements across jurisdictions.',
    workflow: 'Gazette monitoring → Change detection → Impact assessment → Obligation mapping → Alert → Tracking',
    agentsInvolved: ['gazette-monitor', 'change-detector', 'impact-assessor', 'obligation-mapper', 'alert-generator'],
    inputs: ['Government gazettes', 'Regulator websites', 'Legal databases', 'Industry associations'],
    orchestration: 'Continuous monitoring → Structured change log → Compliance calendar → Dashboard',
    tools: ['Gazette APIs', 'Web monitoring', 'Legal NLP', 'Calendar integration', 'Dashboard'],
    humanApproval: 'Tier 2 (Lead) for impact assessment; Tier 3 (Dual: Legal + Compliance) for obligation confirmation',
    output: 'Real-time regulatory change tracking with compliance obligations',
    businessValue: 'Zero missed deadlines; proactive compliance posture',
    sector: ['financial-services', 'healthcare', 'government', 'regulators'],
    solution: ['ai-governance-policy', 'enterprise-deployment', 'data-intelligence'],
    status: 'FIELDABLE',
    evidence: 'Regulatory monitoring agents proven in-house; SADC framework tracking',
    featured: false,
    thumbnail: 'use-cases/regulatory-monitoring.webp',
    problemCategory: ['Compliance', 'Reporting'],
    solutionCategory: ['AI Governance', 'Agentic Automation'],
  },
  {
    slug: 'university-research-support',
    title: 'University Research Administration',
    problem: 'Universities struggle with grant administration, ethics compliance, student tracking, and research output reporting.',
    workflow: 'Grant intake → Ethics workflow → Student/project tracking → Output collection → Report generation → Audit',
    agentsInvolved: ['grant-administrator', 'ethics-coordinator', 'student-tracker', 'output-collector', 'report-generator'],
    inputs: ['Grant agreements', 'Ethics applications', 'Student records', 'Publication data', 'Funding reports'],
    orchestration: 'Integrated workflow across research office → Ethics committee → Departments → VC office',
    tools: ['Grant management APIs', 'Ethics workflow engine', 'Student IS integration', 'ORCID/CrossRef'],
    humanApproval: 'Tier 2 (Lead) for ethics; Tier 3 (Dual: DVC Research + Finance) for grant reporting',
    output: 'Automated research administration with full audit trails',
    businessValue: 'Reduced administrative burden; improved compliance; faster reporting',
    sector: ['education', 'research'],
    solution: ['enterprise-deployment', 'business-automation', 'ai-governance-policy'],
    status: 'FUTURE',
    evidence: 'Roadmap target — capacity building programs with MUBAS/UNIMA in development',
    featured: false,
    thumbnail: 'use-cases/university-research.webp',
    problemCategory: ['Administration', 'Compliance', 'Reporting'],
    solutionCategory: ['Digital Transformation', 'AI Governance'],
  },
  {
    slug: 'policy-analysis',
    title: 'Policy Analysis & Legislative Summarization',
    problem: 'Policy teams need rapid analysis of legislation, regulatory proposals, and stakeholder positions.',
    workflow: 'Document ingestion → Clause extraction → Impact modeling → Stakeholder mapping → Comparative analysis → Briefing',
    agentsInvolved: ['document-ingester', 'clause-extractor', 'impact-modeler', 'stakeholder-mapper', 'comparative-analyst'],
    inputs: ['Bills', 'Regulatory proposals', 'Hansard transcripts', 'Stakeholder submissions', 'Comparative law'],
    orchestration: 'Parallel analysis → Synthesis → Human validation → Policy brief',
    tools: ['Legal NLP', 'Document comparison', 'Stakeholder databases', 'Impact modeling'],
    humanApproval: 'Tier 2 (Lead) for analysis; Tier 3 (Dual: Policy Lead + Legal) for recommendations',
    output: 'Evidence-based policy briefs with stakeholder impact analysis',
    businessValue: 'Days → hours for legislative analysis; comprehensive stakeholder view',
    sector: ['government', 'regulators', 'development'],
    solution: ['research-applied-ai', 'ai-governance-policy', 'data-intelligence'],
    status: 'FIELDABLE',
    evidence: 'Policy analysis agents proven in-house; National AI Strategy consultation submission',
    featured: false,
    thumbnail: 'use-cases/policy-analysis.webp',
    problemCategory: ['Decision Intelligence', 'Compliance', 'Research'],
    solutionCategory: ['Research & Policy', 'AI Governance'],
  },
  {
    slug: 'executive-ai-readiness',
    title: 'Executive AI Readiness Assessment',
    problem: 'Leadership teams need structured assessment of AI readiness across data, infrastructure, talent, and governance.',
    workflow: 'Stakeholder interviews → Data audit → Infrastructure review → Talent assessment → Governance gap analysis → Roadmap',
    agentsInvolved: ['interviewer', 'data-auditor', 'infra-reviewer', 'talent-assessor', 'governance-analyst', 'roadmap-builder'],
    inputs: ['Leadership interviews', 'Data catalog', 'Infrastructure inventory', 'Org charts', 'Current policies'],
    orchestration: 'Parallel assessments → Synthesis → Executive presentation → Actionable roadmap',
    tools: ['Assessment frameworks', 'Maturity models', 'Gap analysis templates', 'Roadmap generators'],
    humanApproval: 'Tier 4 (Executive) for findings; Tier 5 (CEO) for strategic recommendations',
    output: 'AI Readiness Report with prioritized roadmap and investment case',
    businessValue: 'Clear path from current state to AI-native operating model',
    sector: ['financial-services', 'government', 'smes', 'technology', 'healthcare'],
    solution: ['boardroom-briefing', 'ai-company-builder', 'research-applied-ai'],
    status: 'FIELDABLE',
    evidence: 'AI Readiness Assessment framework proven in-house; delivered to SADC institutions',
    featured: true,
    thumbnail: 'use-cases/executive-readiness.webp',
    problemCategory: ['Decision Intelligence', 'Research'],
    solutionCategory: ['Strategy', 'Research & Policy'],
  },
  {
    slug: 'audit-trail-generation',
    title: 'Immutable Audit Trail Generation',
    problem: 'Organizations need tamper-proof records of all agent actions for compliance, security, and accountability.',
    workflow: 'Action → SHA-256 seal → Append-only JSONL → Merkle tree → Verification API → Retention policy',
    agentsInvolved: ['audit-logger', 'merkle-builder', 'verification-api', 'retention-manager'],
    inputs: ['Agent prompts', 'Tool invocations', 'Outputs', 'Approvals', 'Escalations'],
    orchestration: 'Every executor step → Automatic logging → Cryptographic sealing → Queryable audit store',
    tools: ['SHA-256', 'Merkle trees', 'Append-only storage', 'Verification API', 'Retention scheduler'],
    humanApproval: 'Tier 1 (Auto) for logging; Tier 3 (Dual) for audit access; Tier 5 (CEO) for retention policy',
    output: 'Cryptographically sealed, queryable audit trail for every agent action',
    businessValue: 'Full accountability; survives regulatory scrutiny; enables forensic analysis',
    sector: ['financial-services', 'government', 'healthcare', 'regulators'],
    solution: ['ai-company-builder', 'ai-governance-policy', 'enterprise-deployment'],
    status: 'PROVEN_IN_HOUSE',
    evidence: 'SHA-256 sealed audit trails run daily in LightSpeed operations; zero tampering incidents',
    featured: true,
    thumbnail: 'use-cases/audit-trail.webp',
    problemCategory: ['Compliance', 'Decision Intelligence'],
    solutionCategory: ['AI Governance', 'Agentic Automation'],
  },
];

export function getUseCaseBySlug(slug: string): UseCase | undefined {
  return useCasesRegistry.find(uc => uc.slug === slug);
}

export function getUseCasesByStatus(status: UseCaseStatus): UseCase[] {
  return useCasesRegistry.filter(uc => uc.status === status);
}

export function getUseCasesBySector(sectorId: string): UseCase[] {
  return useCasesRegistry.filter(uc => uc.sector.includes(sectorId));
}

export function getUseCasesBySolution(solutionSlug: string): UseCase[] {
  return useCasesRegistry.filter(uc => uc.solution.includes(solutionSlug));
}

export function getUseCasesByProblemCategory(category: ProblemCategory): UseCase[] {
  return useCasesRegistry.filter(uc => uc.problemCategory.includes(category));
}

export function getUseCasesBySolutionCategory(category: SolutionCategory): UseCase[] {
  return useCasesRegistry.filter(uc => uc.solutionCategory.includes(category));
}

export function getFeaturedUseCases(): UseCase[] {
  return useCasesRegistry.filter(uc => uc.featured);
}

export default useCasesRegistry;
