Now I have the full directive. Let me provide a comprehensive Board Risk assessment.

---

# LIGHTSPEED HOLDINGS — BOARD RISK COMMITTEE ASSESSMENT
**Website Transformation & Repository Consolidation Directive**
**Version:** 1.0 | **Priority:** CRITICAL | **Date:** 2026-10-04

---

## EXECUTIVE SUMMARY

This directive represents a **business-critical transformation** of LightSpeed's public digital presence. While the strategic intent is sound (coherent brand, Africa-first positioning, evidence-governed claims), the execution approach carries **material risks** across reputational, operational, legal, technical, and strategic dimensions. The "two-track" approach (Track A: launch, Track B: architectural hardening) is pragmatic but introduces specific dependency risks that must be explicitly governed.

---

## 1. TOP 5 RISKS BY CATEGORY

| # | Risk | Category | Likelihood | Impact | Risk Score |
|---|------|----------|------------|--------|------------|
| **R1** | **Misrepresentation of capabilities / "AI-washing" claims** | Reputational / Legal | **HIGH** | **CRITICAL** | 🔴 20 |
| **R2** | **Track B technical debt undermines Track A launch stability** | Operational / Technical | **HIGH** | **HIGH** | 🟠 16 |
| **R3** | **Athena/internal control plane exposure via public site** | Legal / Security / Reputational | **MEDIUM** | **CRITICAL** | 🔴 15 |
| **R4** | **Over-promising "open/local-first AI economics" without verified cost models** | Strategic / Reputational | **HIGH** | **HIGH** | 🟠 16 |
| **R5** | **Phase 0 audit reveals unseparable legacy dependencies → launch delay** | Operational / Technical | **MEDIUM** | **HIGH** | 🟠 12 |

---

## 2. CLAIMS/EVIDENCE GOVERNANCE (SECTION 23) — ADEQUACY ASSESSMENT

### Current State
Section 23 establishes a **classification framework** (VERIFIED, PROVEN IN-HOUSE, PILOT, DEMONSTRATION, FIELDABLE, FUTURE, HISTORICAL, UNVERIFIED) and mandates traceability to source. It explicitly bans publishing unverified claims and prohibits silent conversion of "planned" → "current."

### Gaps & Residual Risk

| Gap | Risk | Mitigation Needed |
|-----|------|-------------------|
| **No enforcement mechanism** — Classification is advisory; no technical gate prevents publishing UNVERIFIED claims | HIGH | Implement **content pipeline gate**: CMS/registry must require classification + source reference before publish |
| **No audit trail** — No immutable log of claim classification changes | MEDIUM | Append-only claim ledger (hash-linked) in `data/claims/` |
| **Subjective boundaries** — "PROVEN IN-HOUSE" vs "DEMONSTRATION" vs "FIELDABLE" lacks objective criteria | MEDIUM | Publish **CLAIM_CRITERIA.md** with concrete thresholds (e.g., "FIELDABLE = deployed in ≥1 non-LightSpeed environment with documented outcome") |
| **No expiry/review cycle** — Claims can stale without trigger | MEDIUM | Quarterly claim review cadence; auto-flag claims >180 days unreviewed |
| **No legal review hook** — High-risk claims (financial savings, regulatory, partnerships) need legal sign-off | HIGH | Mandatory legal review for claims tagged `financial`, `regulatory`, `partnership` |

### Verdict
**Section 23 is necessary but insufficient.** It provides taxonomy without enforcement. **Recommendation:** Elevate to a **technical governance control** in Phase 1 (canonicalize data) — build the claim registry with mandatory classification + source reference + review date as required fields. No content publishes without passing the gate.

---

## 3. TWO-TRACK APPROACH — TRACK B DEBT UNDERMINING TRACK A

### The Core Tension
- **Track A** (Launch): "Get the public website coherent, fast, credible" — deadline-driven, MVP scope
- **Track B** (Architectural Hardening): "Continue deeper repository cleanup without blocking launch" — open-ended, refactor-heavy

### Specific Risk Vectors

| Vector | How Track B Undermines Track A | Likelihood |
|--------|--------------------------------|------------|
| **Shared dependencies** | Track B refactors `packages/design-system`, `packages/content-model`, `packages/shared-types` → breaking changes cascade to Track A pages | HIGH |
| **Route conflicts** | Track B moves Athena to `apps/athena/`, restructures `apps/control-plane/` → public routes (`/ai-company-builder`, `/use-cases`) break if they import internal components | HIGH |
| **Data registry divergence** | Track A canonicalizes registries (Phase 1); Track B reorganizes `data/` structure → dual sources of truth emerge | MEDIUM |
| **CI/CD pipeline contention** | Both tracks need build/deploy; Track B experiments may break Track A's deploy pipeline | MEDIUM |
| **Team capacity split** | Same engineers context-switching → Track A quality slips, Track B stalls | HIGH |

### Mitigation: **Explicit Interface Contracts**
1. **Freeze public-facing interfaces** for Track A launch: `packages/design-system`, `packages/content-model`, `data/agents`, `data/use-cases`, `data/sectors`, `data/solutions` — **no breaking changes** until Track A ships
2. **Separate build pipelines**: Track A gets dedicated `vercel-preview` / `netlify-preview` branch; Track B works on `main` behind feature flags
3. **Registry ownership**: Track A owns public registries until launch; Track B proposes changes via PR to Track A's registry owners
4. **Hard cutoff**: Track B architectural changes **merge to main only after Track A launch** (or behind `/internal` routes)

---

## 4. DATA SOVEREIGNTY, PRIVACY, REGULATORY RISKS — PUBLIC AGENT REGISTRY

### Exposure Surface
The directive (Section 24, 28) contemplates exposing a **public agent registry** — 89 AI agents + 1 Human CEO across 20 departments with capabilities, tools, workflows.

| Risk | Detail | Regulatory Trigger |
|------|--------|-------------------|
| **Capability leakage** | Agent tool lists (API integrations, data access, external services) reveal internal architecture, vendor relationships, data flows | Competitive intelligence; potential NDA breach with vendors |
| **Prompt/instruction exposure** | If agent prompts or system instructions are in registry, they expose IP, operational logic, potential jailbreak vectors | Trade secrets; security |
| **Personal data in agent metadata** | Agent ownership, contact points, performance metrics could constitute personal data (GDPR/POPIA) | POPIA (South Africa), GDPR (if EU visitors) |
| **Client inference** | Sector/use-case mapping + agent capabilities could allow reconstruction of client engagements | Client confidentiality |
| **Cross-border data transfer** | Public website accessible globally → agent registry data leaves Malawi/SADC | Data sovereignty laws (Malawi Data Protection Act 2024, SADC Model Law) |

### Mitigation
1. **Registry tiering**: Public registry = **capability summaries only** (name, department, high-level purpose, status). Full tool configs, prompts, internal metrics → **internal only**
2. **Data Processing Addendum**: Publish DPA for website visitors; explicit consent for analytics
3. **Geo-fencing consideration**: If Malawi Data Protection Act requires local storage, ensure registry CDN edge nodes in SADC
4. **Legal review**: Pre-launch privacy impact assessment (PIA) for public registry
5. **Robots.txt / noindex**: Consider restricting registry pages from search indexing if sensitivity warrants

---

## 5. PHASE 0 AUDIT — CRITICAL LEGACY DEPENDENCIES

### Scenario
Phase 0 audit (Section 36) discovers legacy components that **cannot be cleanly separated** from public website:
- Shared React component library used by both public pages and Athena/control-plane
- Runtime config that injects internal feature flags into public build
- Auth/session middleware shared across apps
- Database connections pooled across public + internal

### Impact if Unresolved
| Consequence | Severity |
|-------------|----------|
| **Launch blocker** — Cannot deploy public site without internal systems | CRITICAL |
| **Security exposure** — Shared auth = credential leakage risk | CRITICAL |
| **Performance contamination** — Internal workloads degrade public site | HIGH |
| **Compliance failure** — Mixed data planes violate data sovereignty claims | HIGH |

### Contingency Plan (Must Be Defined in Phase 0 Output)
1. **Strangler Fig pattern**: Identify minimal "public-only" subset; build new independent deployment target (`apps/web/`) that **does not import** from internal apps — even if it duplicates some components temporarily
2. **Feature flag kill switches**: Every internal dependency in public build must have `ENABLE_INTERNAL_FEATURES=false` default
3. **Acceptable duplication**: Explicitly authorize **temporary code duplication** (design tokens, UI primitives) to achieve separation — repay in Track B
4. **Go/No-Go gate**: Phase 0 must produce a **"Separability Assessment"** with binary launch readiness decision

---

## 6. OPEN/LOCAL-FIRST AI ECONOMICS — OVER-PROMISING RISK

### Claims in Directive (Sections 4, 14, 22, 42)
- "Use the least expensive model that can reliably do the job"
- "Avoid unnecessary API costs"
- "Local inference / self-hosted / low-cost infrastructure"
- "Open model portability / provider independence"
- "Operate in low-bandwidth environments"

### Verification Gap
**No verified cost models, benchmarks, or latency data** are referenced in the directive. The claims are **architectural aspirations**, not measured outcomes.

| Claim | Evidence Required | Current Status |
|-------|-------------------|----------------|
| Local inference cost advantage | $/1K tokens (local GPU) vs API pricing at African cloud rates | **MISSING** |
| Low-bandwidth viability | Latency/token at 2G/3G; model size vs download time | **MISSING** |
| Provider independence | Successful swap: OpenAI → Llama-3.1-70B → Nemotron → same task quality | **MISSING** |
| "Least expensive model" routing accuracy | % tasks correctly routed; quality regression rate | **MISSING** |

### Risk
**Marketing claims precede engineering validation.** If a prospect requests proof (e.g., "show me the cost model for a 50-agent workflow in Lilongwe"), LightSpeed cannot produce it.

### Mitigation
1. **Phase 1 deliverable**: `AI_ECONOMICS_EVIDENCE.md` — benchmark suite with real measurements (local vs API, bandwidth profiles, model swap tests)
2. **Qualify claims linguistically**: "Designed for..." / "Architected to enable..." / "Targeting..." — not "Achieves..."
3. **FAQ transparency** (Q14, Q15, Q16): Explicitly state "We are publishing benchmarks in Q1 2027" or equivalent
4. **Internal dogfood first**: Run LightSpeed's own operations on local/open-weight stack; publish *those* numbers

---

## 7. ATHENA SEPARATION RISK — INADVERTENT EXPOSURE

### Directive Requirements (Section 27)
- Athena = separate application (`/athena` or `apps/athena/`)
- Own layout, routes, components, data, services, styling
- **No visual language contamination** of public site
- **No mixing** into public LightSpeed website architecture

### Exposure Vectors

| Vector | Mechanism | Likelihood |
|--------|-----------|------------|
| **Shared component imports** | Public page `import { Button } from '@/components/ui'` → pulls Athena-styled variant | HIGH |
| **Shared CSS/design tokens** | Global `:root` variables or Tailwind config leaks Athena colors/spacing | HIGH |
| **Route collision** | `/athena` catches sub-routes meant for public (`/athena/dashboard` vs `/ai-company-builder`) | MEDIUM |
| **Build output bleed** | `next build` or `vite build` bundles Athena chunks into public JS if not explicitly split | MEDIUM |
| **Auth/session leakage** | Shared auth middleware exposes Athena session cookies on public routes | HIGH |
| **API proxy misconfiguration** | Public site proxies `/api/athena/*` → internal endpoints reachable | CRITICAL |

### QA Gate (Section 37 Item 25)
> **"No accidental Athena exposure"** — but this is a **pass/fail test at end**, not a continuous guard.

### Mitigation: **Architectural Firewall**
1. **Separate repos or monorepo with strict boundaries**: `apps/web/` **cannot import** from `apps/athena/` or `apps/control-plane/` — enforce via ESLint rule (`no-restricted-paths`)
2. **Independent deployments**: Each app = separate Vercel/Netlify/Cloudflare project, separate domain/subdomain (`app.lightspeed.mw`, `athena.lightspeed.mw`, `www.lightspeed.mw`)
3. **Shared packages only**: `packages/design-system`, `packages/shared-types` — **versioned, published, consumed as deps** — not source imports
4. **Runtime header check**: Public site middleware asserts `X-App: web`; rejects requests with Athena cookies/headers
5. **Pre-deploy scan**: CI job greps public build output for `athena`, `control-plane`, `internal`, `secret`, `admin` — fails build if found

---

## CONSOLIDATED RISK REGISTER

| ID | Risk | Category | Likelihood | Impact | Score | Owner | Mitigation Status |
|----|------|----------|------------|--------|-------|-------|-------------------|
| **R1** | Misrepresentation / AI-washing claims | Reputational / Legal | HIGH | CRITICAL | 🔴 20 | CRO / Legal | ⚠️ Section 23 taxonomy only; needs technical gate |
| **R2** | Track B debt breaks Track A launch | Operational / Technical | HIGH | HIGH | 🟠 16 | CTO | ⚠️ Interface freeze + separate pipelines needed |
| **R3** | Athena/control-plane exposure | Legal / Security | MEDIUM | CRITICAL | 🔴 15 | CISO / CTO | ⚠️ Architectural firewall + CI scan needed |
| **R4** | Unverified "open/local-first" economics claims | Strategic / Reputational | HIGH | HIGH | 🟠 16 | CTO / CEO | ⚠️ Benchmark evidence pack required pre-launch |
| **R5** | Phase 0 reveals inseparable legacy deps | Operational / Technical | MEDIUM | HIGH | 🟠 12 | CTO | ⚠️ Strangler Fig + duplication authorization needed |
| **R6** | Public agent registry leaks IP/PII | Legal / Privacy | MEDIUM | HIGH | 🟠 12 | CISO / DPO | ⚠️ Tiered registry + PIA required |
| **R7** | Sector/use-case claims imply false client traction | Reputational / Legal | MEDIUM | HIGH | 🟠 12 | CRO / Legal | ⚠️ Claim criteria + legal review gate needed |
| **R8** | Launch deadline forces quality compromises | Reputational / Operational | HIGH | MEDIUM | 🟠 12 | PM / CTO | ⚠️ Definition of Done (Section 42) must be non-negotiable |
| **R9** | Design system fragmentation persists | Technical / Brand | MEDIUM | MEDIUM | 🟡 9 | Design Lead | ✅ Phase 2 addresses; needs token enforcement |
| **R10** | SEO/accessibility/performance deferred to Phase 6 | Strategic / Operational | MEDIUM | MEDIUM | 🟡 9 | PM | ⚠️ Move critical a11y/perf to Phase 3-4 |

---

## BOARD RECOMMENDATIONS

1. **Approve Phase 0 with explicit "Separability Assessment" deliverable** — no Track A start until legacy separation feasibility is proven
2. **Mandate Claim Governance as technical control** — not documentation; build the registry gate in Phase 1
3. **Fund Track A / Track B separation** — dedicated capacity, separate pipelines, interface freeze
4. **Commission AI Economics Evidence Pack** — internal dogfood benchmarks before public claims
5. **Engage DPO/Legal for Privacy Impact Assessment** on public agent registry before Phase 2
6. **Set hard launch gate**: All Section 42 Definition of Done items = **pass/fail**, not "substantially complete"

---

**Prepared by:** Risk Committee Chair
**Distribution:** Board Chair, CEO, CTO, CRO, CISO, Legal Counsel
**Next Review:** Phase 0 completion (est. 2 weeks)
