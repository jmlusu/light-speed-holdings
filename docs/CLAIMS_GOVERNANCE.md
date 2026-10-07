# Claims & Evidence Governance

**Version:** 1.0
**Status:** ACTIVE — Mandatory for All Public Content
**Created:** 2026-10-04
**Owner:** Legal Owner / CISO / Content Architect

---

## Purpose

This document establishes the mandatory governance framework for all public claims made by LightSpeed Holdings. It implements Directive §23: "Every public claim must be classified... If a claim cannot be verified: DO NOT PUBLISH IT."

**Scope:** All public-facing content — website, presentations, proposals, social media, press, Pharos insights, sales materials.

---

## Claim Classification System

### Required Status Values (Directive §23)

| Status | Label | Definition | Publish? |
|--------|-------|------------|----------|
| `VERIFIED` | **VERIFIED** | Independently confirmed by third party (auditor, client, regulator) | ✅ Yes |
| `PROVEN_IN_HOUSE` | **PROVEN IN-HOUSE** | Running in LightSpeed operations, validated by internal systems/tests | ✅ Yes |
| `PILOT` | **PILOT** | Active pilot with real users, composing evidence, no signed engagement | ✅ Yes |
| `DEMONSTRATION` | **DEMONSTRATION** | Working demo/prototype, no live users | ✅ Yes |
| `FIELDABLE` | **FIELDABLE** | Ready for deployment, awaiting client, technically complete | ✅ Yes |
| `FUTURE` | **FUTURE** | Roadmap target, no evidence yet, honestly stated | ✅ Yes |
| `HISTORICAL` | **HISTORICAL** | Was true, no longer current (archived for reference) | ⚠️ Context only |
| `UNVERIFIED_DO_NOT_PUBLISH` | **UNVERIFIED — DO NOT PUBLISH** | Cannot be verified, lacks evidence | ❌ **NO** |

### Visual Badge Mapping (Design System)

| Status | Border | Background | Text | Icon |
|--------|--------|------------|------|------|
| VERIFIED | `cyan/40` | `cyan/10` | `cyan` | ✓ Shield |
| PROVEN_IN_HOUSE | `cyan/40` | `cyan/10` | `cyan` | ✓ Check |
| PILOT | `red/40` | `red/10` | `red` | ⚠ Triangle |
| DEMONSTRATION | `grey-light-text/40` | `grey-light-text/10` | `grey-light-text` | 👁 Eye |
| FIELDABLE | `grey-light-text/40` | `grey-light-text/10` | `grey-light-text` | 📦 Box |
| FUTURE | `grey-dark/40` | `grey-dark/10` | `grey-dark` | → Arrow |
| HISTORICAL | `grey-dark/40` | `grey-dark/10` | `grey-dark` | 📜 Scroll |

---

## Mandatory Claim Categories

Every claim about the following **must** carry a status badge and evidence reference:

| Category | Examples | Evidence Required |
|----------|----------|-------------------|
| **Clients** | "Client X uses our platform" | Signed contract, deployed instance, client reference (with permission) |
| **Deployments** | "Deployed in 14 departments" | Registry entry, audit log, infrastructure records |
| **Partnerships** | "Partnership with Org Y" | Signed MOU, joint press release, shared repo |
| **Government** | "Approved by Ministry Z" | Official letter, gazette notice, registry listing |
| **Universities** | "Collaboration with University A" | Signed research agreement, joint publication, student placement |
| **Regulators** | "Endorsed by Regulator B" | Formal letter, sandbox acceptance, regulatory filing |
| **Outcomes** | "40% reduction in reporting time" | Before/after metrics, client attestation, audit trail |
| **Financial Savings** | "Saved $X annually" | Financial model, client verification, cost accounting |
| **User Counts** | "1,200 cooperative members" | Platform analytics, admin records, third-party verification |
| **Performance** | "99.8% uptime" | Monitoring dashboard, SLA reports, incident logs |
| **Cost Savings** | "22% inference cost reduction" | Token accounting, model routing logs, before/after comparison |
| **Agent Counts** | "90 agents" | `company-registry.yaml` (canonical source) |
| **Department Counts** | "20 departments" | `company-registry.yaml` (canonical source) |

---

## Evidence Standards

### Evidence Hierarchy (Strongest → Weakest)

1. **Third-Party Verification** — Independent audit, client testimonial (with permission), regulator letter
2. **System-Generated** — Automated logs, registry data, monitoring dashboards, test results
3. **Internal Audit** — Structured review by Legal Owner / CISO / Security Compliance Lead
4. **Documented Process** — SOP, workflow execution record, approval chain
5. **Expert Attestation** — Signed statement by relevant agent owner (with role/date)
6. **Roadmap/Plan** — Documented in registry with `FUTURE` status only

### Minimum Evidence per Status

| Status | Minimum Evidence |
|--------|------------------|
| VERIFIED | Third-party doc + system record |
| PROVEN_IN_HOUSE | System record + internal audit sign-off |
| PILOT | Pilot agreement + active user metrics + composing evidence log |
| DEMONSTRATION | Demo environment access + test script + recorded walkthrough |
| FIELDABLE | Technical completion checklist + deployment runbook + staging environment |
| FUTURE | Roadmap entry in registry + owner assignment + target quarter |

---

## Claim Registration Process

### 1. Claim Submission
```markdown
# Claim Registration Form

**Claim ID:** CLM-XXXX (auto-generated)
**Claim Text:** Exact wording to be published
**Category:** [Clients|Deployments|Partnerships|Government|Universities|Regulators|Outcomes|Financial|Users|Performance|Costs|Agents|Departments]
**Proposed Status:** [VERIFIED|PROVEN_IN_HOUSE|PILOT|DEMONSTRATION|FIELDABLE|FUTURE]
**Evidence References:** [List of evidence IDs, files, system records]
**Owner:** [Agent/Role responsible]
**Target Publication:** [Page, document, channel]
**Expiry Date:** [If time-sensitive]
```

### 2. Verification Workflow
```
Submit → Legal Owner Review → Evidence Validation → Status Assignment → Registry Entry → Publish Approval
```

### 3. Registry Entry (`data/claims/registry.ts`)
```typescript
export interface ClaimRegistryEntry {
  id: string;                    // CLM-XXXX
  claim: string;                 // Exact published text
  status: ClaimStatus;           // From classification system
  category: ClaimCategory;       // From mandatory categories
  evidence: EvidenceRef[];       // References to evidence
  verifiedBy: string;            // Agent/role who verified
  verifiedAt: string;            // ISO date
  expiresAt?: string;            // If time-sensitive
  publishedOn: string[];         // Routes/documents where used
  lastReviewed: string;          // ISO date
  reviewCycle: 'quarterly' | 'annual' | 'per-release';
}
```

---

## Content-Specific Rules

### Website Pages
- **Every metric, outcome, client reference, partnership** → Must have claim ID + status badge
- **Agent/department counts** → Sourced from `company-registry.yaml` only
- **Use case status** → Uses Use Case status system (LIVE/PROVEN_IN_HOUSE/PILOT/DEMONSTRATION/FIELDABLE/FUTURE)
- **Sector experience** → Uses Sector status system (PROVEN/CURRENT/DEMONSTRATION/FUTURE)

### Pharos Insights
- **Research claims** → Citation to primary source (paper, dataset, official publication)
- **Market data** → Source attribution (World Bank, IMF, national stats office)
- **Forward-looking statements** → Explicitly labeled `FUTURE` or `ANALYSIS`
- **Opinion** → Clearly marked as Pharos perspective, not verified fact

### Sales/Proposals
- **Capability claims** → Mapped to Solutions/Use Cases registry with status
- **Timeline promises** → `FIELDABLE` or `FUTURE` only; never `VERIFIED` for future work
- **Pricing** → Current rate card only; no "discounted" without approval

### Social Media / Press
- **Same standards as website** — No lower bar for social
- **Quote cards** → Must reference claim ID in alt text/metadata
- **Metrics graphics** → Must include status badge in visual

---

## Prohibited Practices (Directive §23, §10, §18)

### NEVER Do These

| Prohibited | Correct Approach |
|------------|------------------|
| Fabricate client names/logos | Use "Regional financial institution" + sector + status |
| Invent testimonials | Use "Proven in-house" with system evidence |
| Claim unsigned partnerships | Use "In discussion" / `FUTURE` with roadmap reference |
| State government approval without letter | Use "Advisory engagement with Ministry X" + `PILOT`/`CURRENT` |
| Claim university partnership without agreement | Use "Capacity building program with MUBAS/UNIMA in development" + `FUTURE` |
| Imply regulator endorsement without letter | Use "SADC Agentic AI Governance Framework in development" + `FUTURE` |
| Convert "planned" → "current" silently | Explicit status change with evidence |
| Publish unverified financial claims | Only `PROVEN_IN_HOUSE` or `VERIFIED` with audit trail |
| Use "90 agents" without "89 AI + 1 Human CEO" clarification | Always: "90 roles: 89 AI agents + 1 Human CEO" |
| Use stale counts (127, 143, 144, 152) | Canonical: 90 (89 AI + 1 Human CEO) |

---

## Audit & Compliance

### Quarterly Claims Audit
**Owner:** Legal Owner + CISO
**Process:**
1. Export all claims from `data/claims/registry.ts`
2. Verify evidence still exists and is accessible
3. Check status still accurate (pilots may become FIELDABLE/VERIFIED)
4. Identify expired claims (expiry date passed)
5. Flag `UNVERIFIED_DO_NOT_PUBLISH` entries still in content
6. Report to CEO + Board

### Pre-Publication Gate
**Before any public content ships:**
- [ ] All claims have Claim IDs
- [ ] All claims have valid status (not UNVERIFIED)
- [ ] All evidence references resolve
- [ ] Status badges render correctly
- [ ] No prohibited language present
- [ ] CEO sign-off for `VERIFIED` client claims

### Continuous Monitoring
- **Automated:** CI check scans content for claim-like patterns without IDs
- **Manual:** Monthly spot-check of high-traffic pages
- **Incident:** Any external challenge → immediate review + correction

---

## Evidence Storage

### Evidence Types & Locations

| Evidence Type | Storage | Access |
|---------------|---------|--------|
| Contracts/MOUs | `reports/evidence/contracts/` (encrypted) | Legal Owner only |
| Client Data | `reports/evidence/client-data/` (encrypted) | Legal Owner + CISO |
| System Logs | `orchestrator/`, `data/ai_company.db` | Dashboard Owner + Orchestration Owner |
| Test Results | `tests/`, CI artifacts | Test Engineering Lead |
| Audit Trails | `orchestrator/audit_events.jsonl` | Audit Owner + CISO |
| Registry Data | `company-registry.yaml`, `data/*.ts` | Registry Owner |
| Pilot Agreements | `reports/evidence/pilots/` (encrypted) | Consulting Lead + Legal Owner |
| Research Citations | `data/insights/` + bibliography | Thought Leadership Lead |

### Evidence Access Protocol (Directive §9.3)
- **Auditor's read set and write set must be disjoint**
- Evidence directories are **read-only** during audit
- Audit output goes to **separate directory** (`reports/repo-audit-<DATE>.md`)
- On violation: discard run, re-fetch from fresh source, re-run, report incident

---

## Claim Lifecycle

```
DRAFT → SUBMITTED → VERIFIED → PUBLISHED → MONITORED → EXPIRED/ARCHIVED
              ↓
         REJECTED (insufficient evidence) → REVISE or WITHDRAW
```

### Status Transitions
| From | To | Trigger | Approval |
|------|-----|---------|----------|
| DRAFT | SUBMITTED | Author submits | — |
| SUBMITTED | VERIFIED/PROVEN/PILOT/DEMO/FIELDABLE/FUTURE | Evidence validated | Legal Owner |
| SUBMITTED | REJECTED | Evidence insufficient | Legal Owner |
| PUBLISHED | EXPIRED | Expiry date reached | Auto |
| PUBLISHED | ARCHIVED | Superseded/withdrawn | Legal Owner |
| PILOT → FIELDABLE | Pilot completes successfully | Pilot lead + Legal Owner |
| FIELDABLE → VERIFIED | Client deployment confirmed | Legal Owner + Client |
| FUTURE → PILOT | Work begins | Pilot lead + Legal Owner |

---

## Integration with Content Architecture

### Registry Cross-References
```typescript
// data/claims/registry.ts
export const claimsRegistry: ClaimRegistryEntry[] = [
  {
    id: 'CLM-001',
    claim: '90 roles: 89 AI agents + 1 Human CEO across 20 departments',
    status: 'VERIFIED',
    category: 'Agents',
    evidence: [
      { type: 'registry', ref: 'company-registry.yaml', path: 'company.agents.length' },
      { type: 'test', ref: 'tests/registry.test.ts', path: 'agent count assertion' }
    ],
    verifiedBy: 'registry-owner',
    verifiedAt: '2026-10-01T00:00:00Z',
    publishedOn: ['/', '/ai-company-builder', '/what-we-do', '/use-cases', '/about', '/faq'],
    lastReviewed: '2026-10-01T00:00:00Z',
    reviewCycle: 'quarterly'
  },
  // ...
];
```

### Component Usage
```tsx
// In any component displaying a claim
import { getClaimById } from '@lightspeed/data/claims';
import { Badge } from '@lightspeed/design-system';

const claim = getClaimById('CLM-001');
<>
  <Text>{claim.claim}</Text>
  <Badge variant={claim.status.toLowerCase()}>{claim.status}</Badge>
</>
```

---

## Enforcement

### Violations & Consequences

| Violation | First Offense | Repeat |
|-----------|---------------|--------|
| Publish UNVERIFIED claim | Immediate takedown + root cause analysis | Role review |
| Missing claim ID on metric | Content blocked in CI | Mandatory training |
| Stale agent count | Auto-fail build | Architecture review |
| Fabricated client evidence | Immediate takedown + legal review | Termination risk |
| Silent "planned"→"current" | Public correction + process audit | Process overhaul |

### CI Gates
```yaml
# .github/workflows/claims-gate.yml
- name: Validate Claims
  run: |
    npx tsx scripts/validate-claims.ts
    # Checks:
    # 1. All metrics in content have claim IDs
    # 2. All claim IDs resolve to registry
    # 3. No UNVERIFIED claims in published content
    # 4. Agent/department counts match registry
    # 5. Status badges match registry
```

---

## Training & Onboarding

**Required for:** All content creators, Pharos authors, sales, marketing, leadership

**Curriculum:**
1. Claim classification system (30 min)
2. Evidence standards (30 min)
3. Registration workflow (20 min)
4. Prohibited practices (20 min)
5. Tooling: registry, components, CI gates (20 min)

**Certification:** Annual re-certification; tracked in HR system

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-10-04 | Initial governance framework per Directive §23 | Legal Owner / CISO |

---

*This document is mandatory. Non-compliance blocks publication. Update this document first when claim standards evolve.*
