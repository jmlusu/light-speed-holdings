# Content Architecture

**Version:** 1.0
**Status:** ACTIVE
**Created:** 2026-10-04
**Owner:** Content Architect / Technical Documentation Lead

---

## Purpose

This document defines the canonical content architecture for the LightSpeed Holdings public website. It establishes single-source registries for all content types, eliminating duplicate competing registries and ensuring every page consumes from the same authoritative data.

**Directive Reference:** §22 — "Create canonical registries for: company, metrics, capabilities, solutions, useCases, sectors, insights, faqs, claims, governance, media, ctas. No duplicate competing registries. No page should maintain its own independent version of: agent count, department count, sector definitions, use cases, proof/evidence, CTA labels, company positioning."

---

## Registry Overview

| Registry | Location | Source of Truth | Consumers |
|----------|----------|-----------------|-----------|
| Company Identity | `data/company/` | `brand/tokens/brand-tokens.json` + CEO directives | All pages |
| Metrics | `data/metrics/` | `company-registry.yaml` + test suite + orchestration | Home, AI Company Builder, Proof/Use Cases |
| Capabilities | `data/capabilities/` | `company-registry.yaml` + directive §15 | What We Do, Solutions, AI Company Builder |
| Solutions | `data/solutions/` | Directive §16 + siteContent.ts | Solutions, Home, Use Cases, Sectors |
| Use Cases | `data/use-cases/` | Directive §10-11 + useCaseCatalogData.ts | Use Cases, Home, Solutions, Sectors, Sectors |
| Sectors | `data/sectors/` | Directive §12 + sector-registry.ts | Sectors, Home, Solutions, Use Cases |
| Insights | `data/insights/` | Directive §13 + siteContent.ts | Insights, Home, Solutions |
| FAQs | `data/faqs/` | Directive §18 + siteContent.ts | FAQ, Home, AI Company Builder, Use Cases, About |
| Claims | `data/claims/` | Directive §23 + siteContent.ts | All pages (validation) |
| Governance | `data/governance/` | Directive §24 + siteContent.ts | AI Company Builder, Use Cases, About |
| Media | `data/media/` | Directive §19-20 + public/assets/ | All pages |
| CTAs | `data/ctas/` | Directive §34 + siteContent.ts | All pages |

---

## Registry Schema Definitions

### 1. Company Identity (`data/company/registry.ts`)

```typescript
export interface CompanyIdentity {
  legalName: string;           // "LightSpeed Holdings Limited"
  shortName: string;           // "LightSpeed Holdings"
  trademarkDomain: string;     // "LightSpeed Holdings Limited™"
  tagline: string;             // "ASPIRE. ACT. ACHIEVE."
  positioning: string;         // "The AI-native company builder for Southern Africa."
  geographicProgression: string[];  // ["Malawi", "SADC", "Africa"]
  northStar: string;           // "We build AI-native companies."
  heroHeadline: string;
  heroSubline: string;
  valueCycle: string[];        // Capability titles
  thesis: string;              // "Aspire. Act. Achieve."
  foundedYear: number;
  location: string;            // "Lilongwe, Malawi"
}
```

**Canonical Values (Directive §2):**
- Total roles: **90** (89 AI agents + 1 Human CEO)
- Departments: **20**
- Governance: **5-tier human approval**
- Never describe Human CEO as autonomous AI agent
- Never describe LightSpeed as operating without human authority

---

### 2. Metrics (`data/metrics/registry.ts`)

```typescript
export interface PlatformMetric {
  id: string;
  label: string;
  value: string | number;
  source: string;              // e.g., "company-registry.yaml", "pytest test suite"
  category: 'agents' | 'departments' | 'tests' | 'governance' | 'cost' | 'uptime';
  honestyTier: 'verified' | 'proven-in-house' | 'fieldable' | 'pilot' | 'development';
}
```

**Canonical Metrics (Directive §37):**
| ID | Label | Value | Source |
|----|-------|-------|--------|
| `agent-count` | Canonical AI Agents | 90 | company-registry.yaml |
| `ai-agent-count` | AI Agents | 89 | company-registry.yaml |
| `human-ceo-count` | Human CEO | 1 | company-registry.yaml |
| `department-count` | Departments Modeled | 20 | company-registry.yaml |
| `test-count` | Automated Regression Tests | [live count] | pytest test suite |
| `approval-tiers` | Human Approval Gates | 5-Tier | ApprovalGate matrix |
| `model-tiers` | Model Tiers Configured | 3 | llm/platform config |

---

### 3. Capabilities (`data/capabilities/registry.ts`)

```typescript
export interface Capability {
  id: string;
  title: string;
  description: string;
  category: 'strategy' | 'build' | 'govern' | 'research-policy';
  honestyTier: 'verified' | 'proven-in-house' | 'fieldable' | 'pilot' | 'development';
  relatedSolutions: string[];  // Solution slugs
  relatedUseCases: string[];   // Use case slugs
}
```

**Canonical Capabilities (Directive §15):**
1. **Strategy** — AI strategy, AI readiness, digital transformation, data architecture
2. **Build** — Agentic workflow design, AI implementation, governance
3. **Govern** — Policy, research, institutional capacity building
4. **Research & Policy** — Applied AI research, AI governance, AI policy

---

### 4. Solutions (`data/solutions/registry.ts`)

```typescript
export interface Solution {
  slug: string;
  title: string;
  description: string;
  eyebrow: string;             // Category label
  oneLiner: string;
  lead: string;
  honestyBadge: 'Verified' | 'Proven in-house' | 'Fieldable in 2026' | 'In pilot' | 'In active development';
  capabilities: SolutionCapability[];
  useCases: SolutionUseCase[];
  spec: SolutionSpec;
  cta: { label: string; to: string };
}

export interface SolutionCapability {
  title: string;
  desc: string;
}

export interface SolutionUseCase {
  title: string;
  lead: string;
  proof: { label: string; tone: 'proven' | 'pilot' | 'fieldable' | 'development' };
}

export interface SolutionSpec {
  problem: string;
  audience: string;
  changes: string;
  builds: string;
  evidence: string;
}
```

**Canonical Solutions (Directive §16):**
1. **AI & Agentic Systems** — AI Company Builder deployment
2. **Intelligent Automation** — Business Process Automation (WhatsApp, docs, forms)
3. **Data & Decision Intelligence** — Data, Analytics & Donor Reporting
4. **Digital Transformation** — Digital Presence (websites, e-commerce, brand)
5. **Strategy & Executive Advisory** — Boardroom Briefing
6. **AI Governance & Policy** — The Governance Solution
7. **Research & Applied AI** — Pharos thought leadership
8. **AI Company Builder Deployment** — Platform Licensing (Enterprise Deployment)

---

### 5. Use Cases (`data/use-cases/registry.ts`)

```typescript
export type UseCaseStatus = 'LIVE' | 'PROVEN_IN_HOUSE' | 'PILOT' | 'DEMONSTRATION' | 'FIELDABLE' | 'FUTURE';

export interface UseCase {
  slug: string;
  title: string;
  problem: string;
  workflow: string;
  agentsInvolved: string[];     // Agent IDs from registry
  inputs: string[];
  orchestration: string;
  tools: string[];
  humanApproval: string;
  output: string;
  businessValue: string;
  sector: string[];             // Sector IDs
  solution: string[];           // Solution slugs
  status: UseCaseStatus;
  evidence?: string;            // Link to evidence/case study
  featured?: boolean;
  thumbnail?: string;           // Media asset reference
}
```

**Status Definitions (Directive §10):**
| Status | Meaning |
|--------|---------|
| LIVE | Deployed to paying client, measurable outcomes |
| PROVEN_IN_HOUSE | Running in LightSpeed operations, verified |
| PILOT | Active pilot with real users, composing evidence |
| DEMONSTRATION | Working demo, no live client |
| FIELDABLE | Ready for deployment, awaiting client |
| FUTURE | Roadmap target, no evidence yet |

**Filter Dimensions (Directive §11):**
- BY PROBLEM: Cost, Operational Latency, Compliance, Reporting, Customer Experience, Decision Intelligence, Growth, Administration, Research, Knowledge Work, Market Intelligence
- BY SOLUTION: Strategy, Agentic Automation, Data & Intelligence, Digital Transformation, AI Governance, Research & Policy
- BY SECTOR: All 10 canonical sectors
- BY STATUS: All 6 status values

---

### 6. Sectors (`data/sectors/registry.ts`)

```typescript
export interface Sector {
  id: string;                    // Canonical slug
  title: string;
  description: string;
  status: SectorStatus;
  evidence: string;
  region: string[];
  relevantSolutions: string[];   // Solution slugs
  useCases: string[];            // Use case slugs
  keyMetrics?: string[];         // Metric IDs
}

export type SectorStatus =
  | { label: 'PROVEN EXPERIENCE'; tone: 'proven' }
  | { label: 'CURRENT CAPABILITY'; tone: 'pilot' }
  | { label: 'DEMONSTRATION'; tone: 'fieldable' }
  | { label: 'FUTURE OPPORTUNITY'; tone: 'development' };
```

**Canonical 10 Sectors (Directive §12):**
| ID | Title | Status | Evidence |
|----|-------|--------|----------|
| `financial-services` | Financial Services | PROVEN EXPERIENCE | Governed multi-agent compliance automation for regional financial institution: 14 departments, 40% reporting time reduction |
| `healthcare` | Healthcare & Public Health | FUTURE OPPORTUNITY | Offline-first architecture designed for clinical data; no healthcare deployment yet |
| `agriculture` | Agriculture & Agritech | CURRENT CAPABILITY | WhatsApp-native coordination for cooperatives in Malawi/Mozambique; 1,200 members in pilot |
| `education` | Education & Academia | CURRENT CAPABILITY | Agent-driven student management at University of Malawi; 3 depts, 5,000 records |
| `government` | Government & Public Sector | CURRENT CAPABILITY | Advisory on Malawi National AI Strategy; policy-level engagement |
| `regulators` | Regulators & Standards Institutions | FUTURE OPPORTUNITY | SADC Agentic AI Governance Framework in development; MACRA/CRASA engagement |
| `research` | Research & Universities | FUTURE OPPORTUNITY | Capacity building programs with MUBAS/UNIMA in development |
| `smes` | SMEs & Private Enterprise | FIELDABLE | J&S StopOver Bar live proof; Company-in-a-Box agent set |
| `development` | Development & Nonprofit Organizations | PILOT | Kobo/DHIS2 donor reporting pipeline in pilot; NGO-grade dashboards |
| `technology` | Technology & Digital Businesses | FIELDABLE | Platform Licensing (E1) fieldable 2026; AI Company Builder self-hosted |

**Distinction Rules (Directive §12):**
- Clearly distinguish: proven experience / current capability / pilot / demonstration / fieldable / future opportunity
- Academia, research, universities, regulators are strategic sectors
- Do NOT claim formal university/regulator partnerships unless verified

---

### 7. Insights (`data/insights/registry.ts`)

```typescript
export interface Insight {
  slug: string;
  title: string;
  topic: string;               // Pharos category
  excerpt: string;
  content: string;             // Markdown/MDX
  publishedAt: string;         // ISO date
  author: string;              // Pharos team member
  pharosFormat: 'BRIEF' | 'FIELD_NOTE' | 'RESEARCH_NOTE' | 'POLICY_NOTE' | 'SYSTEM_MAP' | 'DATA_STORY' | 'AI_ECONOMICS' | 'AFRICA_WATCH';
  relatedUseCases: string[];   // Use case slugs
  relatedSolutions: string[];  // Solution slugs
  relatedSectors: string[];    // Sector IDs
  tags: string[];
  featured?: boolean;
  thumbnail?: string;
}
```

**Pharos Categories (Directive §13):**
- Agentic AI, AI Company Building, African AI, Open/Open-Weight AI
- AI Economics, AI Governance, AI Policy, AI Regulation, AI Safety
- Digital Transformation, Data Architecture, AI Use Cases
- Research, Universities, Academia, SADC Technology, Malawi Technology
- Sovereign AI, Resource-Constrained AI Deployment

**Visual Formats (Directive §40):**
- PHAROS BRIEF, PHAROS FIELD NOTE, PHAROS RESEARCH NOTE
- PHAROS POLICY NOTE, PHAROS SYSTEM MAP, PHAROS DATA STORY
- PHAROS AI ECONOMICS, PHAROS AFRICA WATCH

---

### 8. FAQs (`data/faqs/registry.ts`)

```typescript
export interface FAQ {
  id: string;
  question: string;
  answer: string;
  category: 'general' | 'ai-company-builder' | 'use-cases' | 'governance' | 'models' | 'africa' | 'engagement' | 'pharos';
  tags: string[];
  honestyTier: 'verified' | 'proven-in-house' | 'fieldable' | 'pilot' | 'development';
}
```

**Canonical FAQs (Directive §18 — all 28 required):**
1. What is LightSpeed Holdings?
2. What is the AI Company Builder?
3. How many agents does LightSpeed have? → "90 roles: 89 AI agents + 1 Human CEO"
4. What does the Human CEO do?
5. Does LightSpeed replace employees?
6. What is H-A-O-M-T-G-V?
7. How does human approval work?
8. What does five-tier governance mean?
9. How are actions audited?
10. What is the role of memory?
11. What tools can agents use?
12. What models does LightSpeed use?
13. Why does LightSpeed prioritize open and open-weight models?
14. Can LightSpeed operate without expensive API calls?
15. Can LightSpeed run locally?
16. Can LightSpeed operate in low-bandwidth environments?
17. How does LightSpeed approach data sovereignty?
18. What sectors does LightSpeed work with?
19. Does LightSpeed work with universities?
20. Does LightSpeed work with regulators?
21. What is Pharos?
22. What is a Use Case?
23. What does "Proven In-House" mean?
24. Is every Use Case a paying-client deployment?
25. How do we engage LightSpeed?
26. What does an AI Readiness Assessment involve?
27. What does LightSpeed cost?
28. How quickly can an engagement begin?

---

### 9. Claims & Evidence (`data/claims/registry.ts`)

```typescript
export type ClaimStatus =
  | 'VERIFIED'
  | 'PROVEN_IN_HOUSE'
  | 'PILOT'
  | 'DEMONSTRATION'
  | 'FIELDABLE'
  | 'FUTURE'
  | 'HISTORICAL'
  | 'UNVERIFIED_DO_NOT_PUBLISH';

export interface Claim {
  id: string;
  claim: string;
  status: ClaimStatus;
  evidence: string[];          // References to case studies, metrics, audits
  source: string;              // File, system, or document
  verifiedAt?: string;         // ISO date
  verifiedBy?: string;         // Agent/role
  expiresAt?: string;          // For time-sensitive claims
  relatedUseCases: string[];
  relatedSectors: string[];
}
```

**Governance Rules (Directive §23):**
- Every public claim must be classified with a status
- Claims about: clients, deployments, partnerships, government, universities, regulators, outcomes, financial savings, user counts, performance, cost savings — must be traceable to a source
- If a claim cannot be verified: **DO NOT PUBLISH IT**
- Do not silently convert "planned" into "current"

---

### 10. Governance (`data/governance/registry.ts`)

```typescript
export interface GovernanceFramework {
  hitlMatrix: HITLTier[];
  governanceGates: GovernanceGate[];
  auditTrail: AuditTrailSpec;
  approvalExpiry: ApprovalExpiryPolicy;
  riskMatrix: RiskLevel[];
  humanAuthority: HumanAuthorityStatement;
}

export interface HITLTier {
  tier: number;
  name: string;
  description: string;
  approverRole: string;
  maxAutoApproveMinutes: number;
  actions: string[];
}
```

**Canonical Governance (Directive §24):**
- 5-tier approval matrix
- 4 mandatory gates: Contract, DPA, Compliance, Security
- Immutable audit trails (SHA-256 sealed, append-only JSONL)
- Periodic expiry sweep for pending approvals
- **Human Authority:** "AI executes. Humans decide." / "Agents execute. The Human CEO owns operational intent and final decision authority."

---

### 11. Media (`data/media/registry.ts`)

```typescript
export type MediaType =
  | 'HERO_IMAGERY'
  | 'HAOMTGV_INFOGRAPHIC'
  | 'AI_COMPANY_BUILDER_ORG_CHART'
  | 'MODEL_ROUTING_INFOGRAPHIC'
  | 'AFRICA_AI_ECONOMICS'
  | 'USE_CASE_CARDS'
  | 'ARCHITECTURE_DIAGRAMS'
  | 'AFRICAN_MAPS'
  | 'RESEARCH_VISUALS'
  | 'HUMAN_LEADERSHIP'
  | 'MICRO_ILLUSTRATIONS';

export interface MediaAsset {
  id: string;
  type: MediaType;
  title: string;
  description: string;
  src: string;                 // Path in public/assets/
  alt: string;
  width: number;
  height: number;
  formats: ('webp' | 'avif' | 'svg' | 'png')[];
  placement: string[];         // Page routes where used
  attribution?: string;
}
```

**Media Types (Directive §19):** Types A-K as defined in directive.

**Placement Strategy (Directive §20):** Strategic distribution per page.

---

### 12. CTAs (`data/ctas/registry.ts`)

```typescript
export type CTAVariant = 'primary' | 'secondary' | 'contextual';

export interface CTA {
  id: string;
  label: string;
  variant: CTAVariant;
  href: string;
  context?: string;            // Where this CTA appears
  trackingLabel?: string;      // Analytics label
}
```

**Canonical CTAs (Directive §34):**
| Variant | Label | Context |
|---------|-------|---------|
| Primary | START A CONVERSATION | Global primary |
| Secondary | REQUEST AN AI READINESS ASSESSMENT | Global secondary |
| Contextual | EXPLORE AI COMPANY BUILDER | AI Company Builder page |
| Contextual | EXPLORE USE CASES | Use Cases page |
| Contextual | EXPLORE SOLUTIONS | Solutions page |
| Contextual | READ PHAROS INSIGHTS | Insights page |

**Rule:** Do NOT randomly alternate labels. Canonicalize CTA labels.

---

## Data Flow Implementation

### Registry Generation Pipeline

```
Source (YAML/JSON/Markdown)
    ↓
Validation (Zod schemas in packages/content-model)
    ↓
TypeScript Module Generation (build script)
    ↓
Published as @lightspeed/data/* packages
    ↓
Consumed by apps/web components
```

### Build-Time Validation

```bash
# Validate all registries against schemas
npm run validate:content

# Generate TypeScript modules
npm run generate:registries

# Type-check
npm run lint
```

### Runtime Consumption

```typescript
// In any page component
import { solutionsRegistry } from '@lightspeed/data/solutions';
import { getSolutionBySlug } from '@lightspeed/data/solutions';
import { sectorsRegistry } from '@lightspeed/data/sectors';
import { useCasesRegistry } from '@lightspeed/data/use-cases';
import { faqsRegistry } from '@lightspeed/data/faqs';
import { ctasRegistry } from '@lightspeed/data/ctas';
```

---

## Migration from Current State

### Current Duplicates to Consolidate

| Current Location | Target Registry | Action |
|------------------|-----------------|--------|
| `src/data/siteContent.ts` (solutions, proof, governance, case studies) | `data/solutions/`, `data/use-cases/`, `data/governance/`, `data/claims/` | Split and migrate |
| `src/data/useCaseCatalogData.ts` (offers, industries, scenarios, proof points) | `data/solutions/`, `data/sectors/`, `data/use-cases/`, `data/claims/` | Split and migrate |
| `src/data/sector-registry.ts` + `src/data/sectors.ts` | `data/sectors/` | Consolidate + expand to 10 |
| `src/data/faqs.ts` | `data/faqs/` | Expand to 28 canonical FAQs |
| `src/data/ctas.ts` | `data/ctas/` | Canonicalize labels |
| `src/data/governance.ts` | `data/governance/` | Formalize structure |
| `src/data/insights.ts` | `data/insights/` | Add Pharos formats |
| `src/data/metrics.ts` | `data/metrics/` | Add honesty tiers |
| `src/data/capabilities.ts` | `data/capabilities/` | Formalize |
| `src/data/companyData.ts` | (Internal only) | Keep for dashboard; not public |
| `src/data/publicAgentRegistry.ts` | `data/agents/` | Public subset only |

---

## Validation Rules

1. **No orphaned content:** Every registry entry must be referenced by at least one page
2. **No duplicate facts:** Agent count, department count, sector definitions exist in exactly one registry
3. **Honesty tier required:** Every claim-bearing entry must have an honesty tier
4. **Cross-reference integrity:** Use case → sector/solution references must resolve
5. **Media asset references:** All media IDs must exist in media registry
6. **CTA label canonicalization:** Only approved CTA labels from registry

---

## Content Review Cadence

| Registry | Review Frequency | Owner |
|----------|------------------|-------|
| Company Identity | Quarterly | CEO |
| Metrics | Weekly (auto from systems) | Dashboard Owner |
| Capabilities | Quarterly | CPO |
| Solutions | Monthly | CPO / Sales Owner |
| Use Cases | Bi-weekly | Consulting Lead / Delivery |
| Sectors | Quarterly | Head of Business Development |
| Insights | Per publication | Thought Leadership Lead |
| FAQs | Monthly | Customer Success Owner |
| Claims | Per claim | Legal Owner / CISO |
| Governance | Quarterly | Security Compliance Lead |
| Media | Per asset | Creative Director |
| CTAs | Quarterly | CMO |

---

*This document is living. Update as content architecture evolves during implementation.*
