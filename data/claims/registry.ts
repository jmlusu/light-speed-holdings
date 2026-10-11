/**
 * Claims Registry — Canonical Source of Truth
 *
 * Source: Directive §23 + siteContent.ts + all registries
 * Directive §22 — Single source for all claims
 *
 * Every public claim MUST be registered here with status and evidence.
 * If a claim cannot be verified: DO NOT PUBLISH IT.
 */

export type ClaimStatus =
  | 'VERIFIED'
  | 'PROVEN_IN_HOUSE'
  | 'PILOT'
  | 'DEMONSTRATION'
  | 'FIELDABLE'
  | 'FUTURE'
  | 'HISTORICAL'
  | 'UNVERIFIED_DO_NOT_PUBLISH';

export type ClaimCategory =
  | 'Clients'
  | 'Deployments'
  | 'Partnerships'
  | 'Government'
  | 'Universities'
  | 'Regulators'
  | 'Outcomes'
  | 'Financial'
  | 'Users'
  | 'Performance'
  | 'Costs'
  | 'Agents'
  | 'Departments';

export interface EvidenceRef {
  type: 'registry' | 'test' | 'audit' | 'contract' | 'client-attestation' | 'monitoring' | 'document' | 'code';
  ref: string;           // File path, system name, or document ID
  path?: string;         // Specific path within ref (e.g., JSONPath, section)
  accessible: boolean;   // Whether evidence is accessible for audit
}

export interface ClaimRegistryEntry {
  id: string;                    // CLM-XXXX
  claim: string;                 // Exact published text
  status: ClaimStatus;
  category: ClaimCategory;
  evidence: EvidenceRef[];
  verifiedBy: string;            // Agent/role who verified
  verifiedAt: string;            // ISO date
  expiresAt?: string;            // If time-sensitive
  publishedOn: string[];         // Routes/documents where used
  lastReviewed: string;          // ISO date
  reviewCycle: 'quarterly' | 'annual' | 'per-release';
  notes?: string;
}

export const claimsRegistry: ClaimRegistryEntry[] = [
  // AGENTS & DEPARTMENTS
  {
    id: 'CLM-001',
    claim: 'LightSpeed\'s operating model contains 90 roles: 89 AI agents plus one Human CEO across 20 departments.',
    status: 'VERIFIED',
    category: 'Agents',
    evidence: [
      { type: 'registry', ref: 'company-registry.yaml', path: 'company.agents.length', accessible: true },
      { type: 'test', ref: 'tests/registry.test.ts', path: 'agent count assertion', accessible: true },
    ],
    verifiedBy: 'registry-owner',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/', '/ai-company-builder', '/what-we-do', '/use-cases', '/about', '/faq'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-002',
    claim: 'The AI Company Builder provides multi-agent orchestration, 5-tier approval matrix, immutable SHA-256 audit trails, 4 governance gates, and model routing.',
    status: 'FIELDABLE',
    category: 'Deployments',
    evidence: [
      { type: 'code', ref: 'src/ai_company/orchestrator/', accessible: true },
      { type: 'code', ref: 'src/ai_company/registry/', accessible: true },
      { type: 'code', ref: 'src/ai_company/security/rbac.ts', accessible: true },
      { type: 'document', ref: 'docs/WEBSITE_ARCHITECTURE.md', accessible: true },
    ],
    verifiedBy: 'cto',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/ai-company-builder', '/solutions', '/faq'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-003',
    claim: 'The Human CEO (Jack Mlusu) sets company vision, makes final decisions, and directs the AI agent workforce. The Human CEO is not an autonomous AI agent.',
    status: 'VERIFIED',
    category: 'Government', // Human CEO is a governance role
    evidence: [
      { type: 'registry', ref: 'company-registry.yaml', path: 'company.agents[human_ceo]', accessible: true },
      { type: 'document', ref: 'AGENTS.md', accessible: true },
    ],
    verifiedBy: 'human-ceo',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/ai-company-builder', '/faq', '/about'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'annual',
  },
  {
    id: 'CLM-004',
    claim: 'LightSpeed augments teams with AI agents; humans retain all decision authority. The J&S StopOver Bar demonstrates 1 human + 5 agents covering 5 functional roles.',
    status: 'PROVEN_IN_HOUSE',
    category: 'Outcomes',
    evidence: [
      { type: 'audit', ref: 'reports/evidence/jss-bar/', accessible: true },
      { type: 'monitoring', ref: 'orchestrator/metrics', accessible: true },
      { type: 'client-attestation', ref: 'J&S StopOver Bar owner', accessible: false }, // Private
    ],
    verifiedBy: 'consulting-lead',
    verifiedAt: '2026-09-15T00:00:00Z',
    publishedOn: ['/faq', '/use-cases', '/solutions'],
    lastReviewed: '2026-09-15T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-005',
    claim: 'H-A-O-M-T-G-V is LightSpeed\'s core framework: Human → Agents → Orchestration → Memory → Tools → Governance → Value.',
    status: 'VERIFIED',
    category: 'Deployments',
    evidence: [
      { type: 'document', ref: 'docs/WEBSITE_ARCHITECTURE.md', accessible: true },
      { type: 'code', ref: 'src/ai_company/orchestrator/message_bus.py', accessible: true },
      { type: 'code', ref: 'src/ai_company/memory/', accessible: true },
      { type: 'code', ref: 'src/ai_company/security/rbac.ts', accessible: true },
    ],
    verifiedBy: 'caio',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/', '/ai-company-builder', '/what-we-do', '/faq'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'annual',
  },
  // GOVERNANCE
  {
    id: 'CLM-006',
    claim: 'Every agent action passes through a 5-tier risk-classified approval matrix (Auto → Lead → Dual → Executive → CEO) with expiration sweeps.',
    status: 'PROVEN_IN_HOUSE',
    category: 'Government',
    evidence: [
      { type: 'code', ref: 'src/ai_company/orchestrator/approval.py', accessible: true },
      { type: 'code', ref: 'src/ai_company/orchestrator/tier_rules.py', accessible: true },
      { type: 'audit', ref: 'orchestrator/audit_events.jsonl', accessible: true },
    ],
    verifiedBy: 'security-compliance-lead',
    verifiedAt: '2026-09-20T00:00:00Z',
    publishedOn: ['/ai-company-builder', '/faq', '/solutions'],
    lastReviewed: '2026-09-20T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-007',
    claim: 'Four mandatory governance gates (Contract, DPA, Compliance, Security) run before any engagement; every action is SHA-256 sealed.',
    status: 'PROVEN_IN_HOUSE',
    category: 'Government',
    evidence: [
      { type: 'code', ref: 'src/ai_company/services/client_intake.py', accessible: true },
      { type: 'code', ref: 'src/ai_company/security/rbac.ts', accessible: true },
      { type: 'audit', ref: 'orchestrator/audit_events.jsonl', accessible: true },
    ],
    verifiedBy: 'ciso',
    verifiedAt: '2026-09-20T00:00:00Z',
    publishedOn: ['/ai-company-builder', '/faq', '/solutions'],
    lastReviewed: '2026-09-20T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-008',
    claim: 'Every agent action generates an append-only SHA-256 sealed JSONL audit log; Merkle trees provide tamper-evidence.',
    status: 'PROVEN_IN_HOUSE',
    category: 'Outcomes',
    evidence: [
      { type: 'code', ref: 'src/ai_company/store/report_store.py', accessible: true },
      { type: 'audit', ref: 'orchestrator/audit_events.jsonl', accessible: true },
      { type: 'test', ref: 'tests/audit.test.ts', accessible: true },
    ],
    verifiedBy: 'ciso',
    verifiedAt: '2026-09-20T00:00:00Z',
    publishedOn: ['/ai-company-builder', '/faq', '/use-cases'],
    lastReviewed: '2026-09-20T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  // MEMORY & TOOLS
  {
    id: 'CLM-009',
    claim: 'LightSpeed provides 6 persistent memory types (episodic, semantic, procedural, relational, temporal, aggregate) with recall-before-execute.',
    status: 'PROVEN_IN_HOUSE',
    category: 'Deployments',
    evidence: [
      { type: 'code', ref: 'src/ai_company/memory/', accessible: true },
      { type: 'code', ref: 'src/ai_company/lsmem/', accessible: true },
      { type: 'test', ref: 'tests/memory.test.ts', accessible: true },
    ],
    verifiedBy: 'memory-owner',
    verifiedAt: '2026-09-25T00:00:00Z',
    publishedOn: ['/ai-company-builder', '/faq'],
    lastReviewed: '2026-09-25T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-010',
    claim: 'Agents use a canonical 7-tool vocabulary (read, edit, grep, list, bash, webfetch, task) validated at runtime by ToolRunner.',
    status: 'PROVEN_IN_HOUSE',
    category: 'Deployments',
    evidence: [
      { type: 'registry', ref: 'company-registry.yaml', path: 'company.agents[].tools', accessible: true },
      { type: 'code', ref: 'src/ai_company/security/rbac.ts', accessible: true },
      { type: 'document', ref: 'AGENTS.md', accessible: true },
    ],
    verifiedBy: 'cto',
    verifiedAt: '2026-09-25T00:00:00Z',
    publishedOn: ['/ai-company-builder', '/faq'],
    lastReviewed: '2026-09-25T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  // MODELS
  {
    id: 'CLM-011',
    claim: 'LightSpeed uses 3 model tiers: Local/Free (Ollama), Open-Weight APIs (DeepSeek, Kimi, Gemini Flash), Premium (Gemini Pro, GPT-4o). 9 providers configured.',
    status: 'PROVEN_IN_HOUSE',
    category: 'Deployments',
    evidence: [
      { type: 'code', ref: 'src/ai_company/llm/', accessible: true },
      { type: 'monitoring', ref: 'data/companyData.ts (modelTiers)', accessible: true },
      { type: 'document', ref: 'docs/WEBSITE_ARCHITECTURE.md', accessible: true },
    ],
    verifiedBy: 'llm-platform-owner',
    verifiedAt: '2026-09-25T00:00:00Z',
    publishedOn: ['/ai-company-builder', '/faq', '/insights'],
    lastReviewed: '2026-09-25T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-012',
    claim: 'LightSpeed prioritizes open-weight/local-first models for cost sovereignty, data sovereignty, provider independence, offline capability, and regulatory compliance.',
    status: 'PROVEN_IN_HOUSE',
    category: 'Outcomes',
    evidence: [
      { type: 'monitoring', ref: 'data/companyData.ts (modelTiers)', accessible: true },
      { type: 'document', ref: 'docs/WEBSITE_ARCHITECTURE.md', accessible: true },
      { type: 'document', ref: 'directive §4', accessible: true },
    ],
    verifiedBy: 'caio',
    verifiedAt: '2026-09-25T00:00:00Z',
    publishedOn: ['/faq', '/insights', '/ai-company-builder'],
    lastReviewed: '2026-09-25T00:00:00Z',
    reviewCycle: 'annual',
  },
  {
    id: 'CLM-013',
    claim: 'LightSpeed internal operations route 70% of tasks to local/open-weight models, achieving $0.038 average cost per task.',
    status: 'PROVEN_IN_HOUSE',
    category: 'Costs',
    evidence: [
      { type: 'monitoring', ref: 'data/companyData.ts (llm_cost_per_task)', accessible: true },
      { type: 'code', ref: 'src/ai_company/llm/client.py', accessible: true },
    ],
    verifiedBy: 'cfo',
    verifiedAt: '2026-09-25T00:00:00Z',
    publishedOn: ['/faq', '/insights', '/ai-company-builder'],
    lastReviewed: '2026-09-25T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-014',
    claim: 'Platform Licensing (E1) enables self-hosted deployment on laptop/VPS with full 90-agent orchestration, governance, and audit trails.',
    status: 'FIELDABLE',
    category: 'Deployments',
    evidence: [
      { type: 'document', ref: 'src/data/useCaseCatalogData.ts (Offer E)', accessible: true },
      { type: 'code', ref: 'src/ai_company/cli/', accessible: true },
    ],
    verifiedBy: 'vp-engineering',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/faq', '/solutions'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  // AFRICA-FIRST
  {
    id: 'CLM-015',
    claim: 'LightSpeed operates from Lilongwe with intermittent connectivity; architecture supports local inference, offline MessageBus, WhatsApp on 2G/3G, USSD fallbacks.',
    status: 'PROVEN_IN_HOUSE',
    category: 'Outcomes',
    evidence: [
      { type: 'document', ref: 'directive §4', accessible: true },
      { type: 'code', ref: 'src/ai_company/llm/providers/ollama.py', accessible: true },
      { type: 'code', ref: 'src/ai_company/orchestrator/message_bus.py', accessible: true },
    ],
    verifiedBy: 'cto',
    verifiedAt: '2026-09-28T00:00:00Z',
    publishedOn: ['/faq', '/insights', '/about'],
    lastReviewed: '2026-09-28T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-016',
    claim: 'Zero-Cloud Boundary option keeps all inference, memory, and audit logs on client infrastructure; Malawi DPA/GDPR compliant; local encryption.',
    status: 'PROVEN_IN_HOUSE',
    category: 'Government',
    evidence: [
      { type: 'code', ref: 'src/ai_company/security/memory_encryption.py', accessible: true },
      { type: 'code', ref: 'src/ai_company/security/encryption_key_manager.py', accessible: true },
      { type: 'document', ref: 'directive §23', accessible: true },
    ],
    verifiedBy: 'ciso',
    verifiedAt: '2026-09-28T00:00:00Z',
    publishedOn: ['/faq', '/insights', '/solutions'],
    lastReviewed: '2026-09-28T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  // SECTORS
  {
    id: 'CLM-017',
    claim: 'LightSpeed targets 10 sectors: Financial Services (Proven), Agriculture (Pilot), Education (Pilot), Government (Pilot), SMEs (Fieldable), Development (Pilot), Technology (Fieldable), Healthcare (Future), Regulators (Future), Research (Future).',
    status: 'VERIFIED',
    category: 'Deployments',
    evidence: [
      { type: 'registry', ref: 'data/sectors/registry.ts', accessible: true },
      { type: 'document', ref: 'directive §12', accessible: true },
    ],
    verifiedBy: 'head-of-business-development',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/faq', '/sectors', '/solutions'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-018',
    claim: 'University capacity building programs with MUBAS/UNIMA in development; no formal partnerships signed. Pharos research active.',
    status: 'FUTURE',
    category: 'Universities',
    evidence: [
      { type: 'document', ref: 'directive §12', accessible: true },
      { type: 'registry', ref: 'data/sectors/registry.ts (research sector)', accessible: true },
    ],
    verifiedBy: 'community-ecosystem-builder',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/faq', '/sectors', '/insights'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-019',
    claim: 'SADC Agentic AI Governance Framework in development; submitted to MACRA, CRASA, central banks, digital ministers. Aligned with AU Continental AI Strategy.',
    status: 'FUTURE',
    category: 'Regulators',
    evidence: [
      { type: 'document', ref: 'directive §12, §13, §40', accessible: true },
      { type: 'registry', ref: 'data/sectors/registry.ts (regulators sector)', accessible: true },
      { type: 'document', ref: 'src/data/useCaseCatalogData.ts (CATALOG_POLICIES)', accessible: true },
    ],
    verifiedBy: 'agentic-policy-analyst',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/faq', '/sectors', '/insights'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  // PHAROS & USE CASES
  {
    id: 'CLM-020',
    claim: 'Pharos produces 8 formats (BRIEF, FIELD_NOTE, RESEARCH_NOTE, POLICY_NOTE, SYSTEM_MAP, DATA_STORY, AI_ECONOMICS, AFRICA_WATCH) across 19 topics.',
    status: 'PROVEN_IN_HOUSE',
    category: 'Deployments',
    evidence: [
      { type: 'registry', ref: 'data/insights/registry.ts', accessible: true },
      { type: 'document', ref: 'directive §13, §40', accessible: true },
    ],
    verifiedBy: 'thought-leadership-lead',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/faq', '/insights', '/about'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-021',
    claim: 'Use Cases have 6 status levels (LIVE, PROVEN_IN_HOUSE, PILOT, DEMONSTRATION, FIELDABLE, FUTURE) with explicit evidence requirements.',
    status: 'VERIFIED',
    category: 'Deployments',
    evidence: [
      { type: 'registry', ref: 'data/use-cases/registry.ts', accessible: true },
      { type: 'document', ref: 'directive §10, §11', accessible: true },
    ],
    verifiedBy: 'consulting-lead',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/faq', '/use-cases'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'annual',
  },
  {
    id: 'CLM-022',
    claim: '"Proven In-House" = running in LightSpeed operations, validated by internal systems/tests/audit. Highest evidence for non-client capabilities.',
    status: 'VERIFIED',
    category: 'Outcomes',
    evidence: [
      { type: 'document', ref: 'directive §10, §18', accessible: true },
      { type: 'registry', ref: 'data/use-cases/registry.ts', accessible: true },
    ],
    verifiedBy: 'consulting-lead',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/faq', '/use-cases'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'annual',
  },
  {
    id: 'CLM-023',
    claim: 'Most Use Cases are not paying-client deployments. Status system is explicit: LIVE=1, PROVEN_IN_HOUSE=multiple, PILOT=multiple, FIELDABLE=multiple, FUTURE=multiple.',
    status: 'VERIFIED',
    category: 'Outcomes',
    evidence: [
      { type: 'registry', ref: 'data/use-cases/registry.ts', accessible: true },
      { type: 'document', ref: 'directive §10', accessible: true },
    ],
    verifiedBy: 'consulting-lead',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/faq', '/use-cases'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  // ENGAGEMENT
  {
    id: 'CLM-024',
    claim: 'Three engagement entry points: AI Readiness Assessment (2 weeks), Boardroom Briefing (focused session), Start a Conversation (general inquiry). All clear 4 governance gates.',
    status: 'FIELDABLE',
    category: 'Deployments',
    evidence: [
      { type: 'document', ref: 'src/data/siteContent.ts (GOVERNANCE_SOLUTION)', accessible: true },
      { type: 'code', ref: 'src/ai_company/services/client_intake.py', accessible: true },
    ],
    verifiedBy: 'sales-owner',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/faq', '/contact', '/solutions'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-025',
    claim: 'AI Readiness Assessment: 2-week structured evaluation (interviews, data audit, infra review, talent assessment, governance gap analysis, roadmap). Fieldable 2026.',
    status: 'FIELDABLE',
    category: 'Deployments',
    evidence: [
      { type: 'document', ref: 'src/data/siteContent.ts (GOVERNANCE_SOLUTION)', accessible: true },
      { type: 'registry', ref: 'data/faqs/registry.ts (faq-26)', accessible: true },
    ],
    verifiedBy: 'consulting-lead',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/faq', '/contact', '/solutions'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-026',
    claim: 'Pricing: Digital Presence MWK 150K–1.8M; Business Automation MWK 900K–2.5M + hosting; Data Intelligence USD quoted; Platform Licensing MWK 3.5M + MWK 350K/mo.',
    status: 'FIELDABLE',
    category: 'Financial',
    evidence: [
      { type: 'document', ref: 'src/data/useCaseCatalogData.ts (OFFER_FAMILIES)', accessible: true },
      { type: 'registry', ref: 'data/faqs/registry.ts (faq-27)', accessible: true },
    ],
    verifiedBy: 'cfo',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/faq', '/contact', '/solutions'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'quarterly',
  },
  {
    id: 'CLM-027',
    claim: 'Fastest engagement: Boardroom Briefing → Governance Gates → Pilot (3–4 weeks). Platform Licensing: 1–2 weeks setup. No work starts until governance gates clear.',
    status: 'FIELDABLE',
    category: 'Deployments',
    evidence: [
      { type: 'document', ref: 'src/data/siteContent.ts (GOVERNANCE_SOLUTION)', accessible: true },
      { type: 'registry', ref: 'data/faqs/registry.ts (faq-28)', accessible: true },
    ],
    verifiedBy: 'sales-owner',
    verifiedAt: '2026-10-05T00:00:00Z',
    publishedOn: ['/faq', '/contact'],
    lastReviewed: '2026-10-05T00:00:00Z',
    reviewCycle: 'quarterly',
  },
];

export function getClaimById(id: string): ClaimRegistryEntry | undefined {
  return claimsRegistry.find(c => c.id === id);
}

export function getClaimsByStatus(status: ClaimStatus): ClaimRegistryEntry[] {
  return claimsRegistry.filter(c => c.status === status);
}

export function getClaimsByCategory(category: ClaimCategory): ClaimRegistryEntry[] {
  return claimsRegistry.filter(c => c.category === category);
}

export function getClaimsForRoute(route: string): ClaimRegistryEntry[] {
  return claimsRegistry.filter(c => c.publishedOn.includes(route));
}

export function validateClaimsForRoute(route: string): { valid: boolean; missing: string[]; unverified: string[] } {
  const routeClaims = getClaimsForRoute(route);
  const missing = routeClaims.filter(c => c.status === 'UNVERIFIED_DO_NOT_PUBLISH').map(c => c.id);
  const unverified = routeClaims.filter(c => c.status === 'FUTURE' || c.status === 'HISTORICAL').map(c => c.id);
  return {
    valid: missing.length === 0,
    missing,
    unverified,
  };
}

export default claimsRegistry;
