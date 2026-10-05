# Homepage - DRAFT awaiting CEO/Pharos sign-off

> **Status:** DRAFT - awaiting CEO/Pharos sign-off.
> **Section:** Directive "WEBSITE TRANSFORMATION & REPOSITORY CONSOLIDATION DIRECTIVE.md" §17 (Homepage), §9 (IA), §34 (CTA system), §23-§24 (claims & honesty).
> **Sources:** `src/data/siteContent.ts`, `src/data/homeImmersiveCopy.ts`, `src/data/registries/claims-registry.json`, `src/data/registries/metrics-registry.json`, `src/data/registries/sector-registry.json`, `src/data/registries/solution-registry.json`, `src/data/registries/use-case-registry.json`, `src/data/registries/cta-registry.json`, `src/data/registries/faq-registry.json`.

**Rules applied:** every claim carries an HTML source comment and, where relevant, one of the six status labels (LIVE / PROVEN IN-HOUSE / PILOT / DEMONSTRATION / FIELDABLE / FUTURE). No clients, partnerships, testimonials, or metrics were invented. Preferred phrasing: "AI executes. Humans decide."

---

## 01 — HERO

<!-- src: Directive §17 "01 — HERO"; cta-registry primary/secondary; siteContent.ts company.heroHeadline -->

**Eyebrow:** LIGHTSPEED HOLDINGS // AI-NATIVE COMPANY BUILDER
<!-- src: homeImmersiveCopy.ts heroEyebrow -->

**Headline:** Build, Govern & Scale Your AI Workforce
<!-- src: Directive §17 "01 — HERO" -->
<!-- §24 note: Directive §17 drafts "Autonomous AI Workforce". This draft proposes "AI Workforce" to avoid implying AI runs the company without humans (§24). CEO/Pharos to choose. -->

**Subheadline:** Agentic AI systems built and operated from Malawi. 90 roles - 89 AI agents + 1 Human CEO across 20 departments, under five-tier human approval. AI executes. Humans decide.
<!-- src: homeImmersiveCopy.ts heroLead; claims-registry claim.agent-count (PROVEN IN-HOUSE); faq-registry faq-05 -->

**Alternate subheadline (existing site):** LightSpeed Holdings helps organisations design, build and govern AI-native businesses, intelligent workflows and agentic systems - in Malawi, across SADC, and beyond.
<!-- src: siteContent.ts company.heroSubline -->

**Primary CTA:** START A CONVERSATION -> `/contact`
<!-- src: cta-registry primary; Directive §34 -->

**Secondary CTA:** REQUEST AN AI READINESS ASSESSMENT -> `/contact`
<!-- src: cta-registry secondary; Directive §34 -->

**Hero reassurance line:** Every claim is labeled. Every number is auditable.
<!-- src: homeImmersiveCopy.ts scrimHint -->

---

## 02 — ORIENTATION

<!-- src: Directive §17 "02 — ORIENTATION"; faq-registry faq-01 -->

**Section label:** WHAT LIGHTSPEED IS

LightSpeed Holdings Limited is an AI-native company builder and operating company based in Lilongwe, Malawi. We design, build and govern AI-native businesses, intelligent workflows and agentic systems for organisations across Malawi, SADC and Africa.

- **Tagline:** ASPIRE. ACT. ACHIEVE.
- **North star:** We build AI-native companies.
- **Positioning:** The AI-native company builder for Southern Africa.
- **Capability cycle:** Strategy -> Build -> Govern -> Research & Policy.

<!-- src: siteContent.ts company (legalName, tagline, northStar); capabilities.ts CAPABILITIES; Directive §15 capability families -->

---

## 03 — VISITOR PATHS

<!-- src: Directive §17 "03 — VISITOR PATHS" -->

Four self-selection cards. Labels are the visitor's own words, not ours.

| Visitor says | Card headline | Destination | CTA label |
|---|---|---|---|
| I have a business problem. | Start with the problem, not the technology. | `/use-cases` | EXPLORE USE CASES |
| I want an AI operating model. | See the 90-role operating model in full. | `/ai-company-builder` | EXPLORE AI COMPANY BUILDER |
| I want to explore AI use cases. | What LightSpeed can actually do - each with a status label. | `/use-cases` | EXPLORE USE CASES |
| I want executive advice. | A focused session for your leadership team. | `/contact` | START A CONVERSATION |

<!-- src: Directive §17 visitor path wording; §34 canonical CTA labels; §10 (Use Cases answers "What can LightSpeed actually do?") -->
<!-- TODO: needs fact - confirm 4th card destination (/contact vs /what-we-do) with CEO -->

---

## 04 — H-A-O-M-T-G-V

<!-- src: Directive §17 "04 — H-A-O-M-T-G-V"; faq-registry faq-06 (PROVEN IN-HOUSE) -->

**Section label:** THE LIGHTSPEED OPERATING FRAMEWORK

**Lead:** Seven letters describe how the company runs. The human layer stays above the system; value is the business outcome.

| Letter | Layer | What it means |
|---|---|---|
| H | HUMAN | Operational intent and final decision authority. |
| A | AGENTS | 90 specialized operating roles: 89 AI agents + 1 Human CEO. |
| O | ORCHESTRATION | Deterministic routing of data, tasks and decisions across workflows. |
| M | MEMORY | Persistent contextual data storage across long-running tasks. |
| T | TOOLS | Isolated execution environments for API integrations and actions. |
| G | GOVERNANCE | Five-tier approval controls and immutable logging. |
| V | VALUE | Measurable reductions in cost and operational latency. |

**Caption:** Status: PROVEN IN-HOUSE - this is LightSpeed's own architecture, running LightSpeed.
<!-- src: claims-registry claim.agent-count, claim.five-tier-approval, claim.immutable-audit-trails (all PROVEN_IN_HOUSE) -->

---

## 05 — AI COMPANY BUILDER

<!-- src: Directive §17 "05 — AI COMPANY BUILDER"; Directive §14; siteContent.ts solutions[0] -->

**Section label:** FLAGSHIP PLATFORM

**Headline:** Build. Govern. Scale.

**Body:** A governed multi-agent orchestration platform where 90 AI agents and 1 human CEO work across 20 departments. Work flows from brief to inbox task to assigned agents to human review to deliverable - no client-facing deliverable ships without human sign-off. The platform enforces 5-tier human-in-the-loop approvals, 4 governance gates (Contract, DPA, Compliance, Security), and immutable SHA-256 sealed audit trails for every action.
<!-- src: faq-registry faq-02 -->

**Status:** FIELDABLE - governance layers (5-tier approval, 4 gates, SHA-256 audit trails) PROVEN IN-HOUSE.
<!-- src: siteContent.ts solutions[0].proof "Fieldable in 2026"; claims-registry claim.five-tier-approval / claim.four-governance-gates / claim.immutable-audit-trails (PROVEN_IN_HOUSE) -->

**CTA:** EXPLORE AI COMPANY BUILDER -> `/ai-company-builder`
<!-- src: cta-registry contextual; Directive §34 -->

---

## 06 — 90-ROLE WORKFORCE

<!-- src: Directive §17 "06 — 90-ROLE WORKFORCE"; claims-registry claim.agent-count; metrics-registry -->

**Section label:** THE WORKFORCE

**Headline:** 89 AI agents + 1 Human CEO across 20 departments.

**Body:** LightSpeed's operating model contains 90 roles. The Human CEO agent acts at the explicit direction of the actual Human CEO - vision, final decisions, budgets, culture and accountability stay human. Every figure on this site is read from `company-registry.yaml`, never from marketing copy.

| Figure | Value | Classification |
|---|---|---|
| Total roles | 90 | PROVEN IN-HOUSE |
| AI agents | 89 | PROVEN IN-HOUSE |
| Human CEO | 1 | PROVEN IN-HOUSE |
| Departments | 20 | PROVEN IN-HOUSE |
| Approval tiers | 5 (Auto -> Lead -> Executive -> CEO -> Board) | PROVEN IN-HOUSE |
| Governance gates | 4 (Contract, DPA, Compliance, Security) | PROVEN IN-HOUSE |

<!-- src: claims-registry claim.agent-count, claim.department-count, claim.five-tier-approval, claim.four-governance-gates, claim.canonical-registry-numbers (all PROVEN_IN_HOUSE); metrics-registry -->
<!-- §23 note: historical counts 89/90/127/143/144/152 are not equivalent - use only the canonical 90 = 89 + 1 (claim.historical-agent-counts, HISTORICAL). -->

---

## 07 — OPEN / OPEN-WEIGHT AI

<!-- src: Directive §17 "07 — OPEN / OPEN-WEIGHT AI"; faq-registry faq-13, faq-14 -->

**Section label:** AFRICA-FIRST AI ECONOMICS

**Headline:** The least expensive model that can reliably do the job.

**Body:** Open-source and open-weight AI is a cornerstone of our operating philosophy - designed for African cost realities, constrained infrastructure, intermittent connectivity, data sovereignty and local deployment. Local Ollama models handle routine classification, extraction, summarisation, embeddings and repetitive workflows at near-zero marginal cost. Commercial APIs are routed only when they provide a material quality, latency or capability advantage. LightSpeed itself operates this way daily.

**Supporting facts:**

- 9 LLM providers configured, including free local Ollama models. [PROVEN IN-HOUSE]
<!-- src: claims-registry claim.9-llm-providers -->
- Routing order: open/local first -> open-weight -> local inference -> self-hosted/low-cost -> commercial models when materially better -> governed routing -> humans decide.
<!-- src: faq-registry faq-12 -->
- Local-first operation with a Zero-Cloud Boundary option for state, health and financial data. [PROVEN IN-HOUSE]
<!-- src: claims-registry claim.sovereign-offline-first -->
- Engineered for low-bandwidth environments; WhatsApp-native workflows run on 2G/3G. [PROVEN IN-HOUSE]
<!-- src: faq-registry faq-16 -->

---

## 08 — USE CASES

<!-- src: Directive §17 "08 — USE CASES"; Directive §10 ("Proof" replaced by "Use Cases") -->

**Section label:** USE CASES - WHAT LIGHTSPEED CAN ACTUALLY DO

**Lead:** Selected examples. Every use case carries one of six status labels: LIVE, PROVEN IN-HOUSE, PILOT, DEMONSTRATION, FIELDABLE, FUTURE. Nothing here implies a paying client unless it is verified as one.

**Featured examples:**

| Use case | Sector | Status |
|---|---|---|
| J&S StopOver Bar - agentic decision support for a real, non-tech SME in Malawi | SMEs & Private Enterprise | LIVE |
| LightSpeed Holdings - the platform is its own first customer | Technology & Digital Businesses | PROVEN IN-HOUSE |
| Malawi Central Bank Compliance Automation - regulatory reporting across 14 departments with full audit trails, 40% reduction in reporting time | Financial Services | PROVEN IN-HOUSE |
| SADC Agricultural Cooperative Digital Platform - WhatsApp-native coordination with mobile-money, serving 1,200 cooperative members | Agriculture & Agritech | PILOT |
| University of Malawi Student Management System - 3 departments onboarded, 5,000 records processed | Education & Academia | PILOT |

<!-- src: use-case-registry.json (uc-js-bar, uc-meta, ws-01, ws-02, ws-03); claims-registry claim.js-stopover-bar-live (LIVE), claim.compliance-automation-40-percent (PROVEN_IN_HOUSE), claim.agricultural-cooperative-pilot (PILOT), claim.university-malawi-student-management (PILOT) -->
<!-- §23 note: "regional financial institution" / "University of Malawi" appear as named in the claims ledger; treat the 40% figure as PROVEN IN-HOUSE, not a client testimonial. -->

**CTA:** EXPLORE USE CASES -> `/use-cases`
<!-- src: cta-registry contextual; Directive §34 -->

---

## 09 — SOLUTIONS

<!-- src: Directive §17 "09 — SOLUTIONS"; Directive §16; solution-registry.json -->

**Section label:** SOLUTIONS - WHAT LIGHTSPEED CAN BUILD OR CHANGE

Eight solution families:

1. AI & Agentic Systems
2. Intelligent Automation
3. Data & Decision Intelligence
4. Digital Transformation
5. Strategy & Executive Advisory
6. AI Governance & Policy
7. Research & Applied AI
8. AI Company Builder Deployment

<!-- src: Directive §16 "Recommended families"; solution-registry.json solutions[] (8 entries, slugs match) -->

**CTA:** EXPLORE SOLUTIONS -> `/solutions`
<!-- src: cta-registry contextual; Directive §34 -->

---

## 10 — SECTORS

<!-- src: Directive §17 "10 — SECTORS"; Directive §12; sector-registry.json -->

**Section label:** SECTORS - MARKETS AND INSTITUTIONS SERVED OR TARGETED

A sector exists here because it is a strategic target. Each carries an explicit honesty badge.

| Sector | Badge |
|---|---|
| Financial Services | PROVEN IN-HOUSE |
| Healthcare & Public Health | FUTURE |
| Agriculture & Agritech | PILOT |
| Education & Academia | PILOT |
| Government & Public Sector | CURRENT CAPABILITY |
| Regulators & Standards Institutions | DEMONSTRATION |
| Research & Universities | DEMONSTRATION |
| SMEs & Private Enterprise | FIELDABLE |
| Development & Nonprofit Organizations | PILOT |
| Technology & Digital Businesses | PROVEN IN-HOUSE |

<!-- src: sector-registry.json honestyBadge per sector; Directive §12 list of 10 -->
<!-- §12 note: no formal university or regulator partnerships are claimed; academia/research/regulators are strategic targets. -->

---

## 11 — PHAROS

<!-- src: Directive §17 "11 — PHAROS"; Directive §13 -->

**Section label:** INSIGHTS FROM PHAROS

**Body:** Pharos is LightSpeed's in-house thought-leadership team - not a generic blog. It turns our engineering, research, experimentation and field observations into public work on agentic AI, AI company building, African AI, open/open-weight AI, AI governance and policy, digital transformation, data architecture, SADC and Malawi technology, sovereign AI and resource-constrained deployment.

**Featured teasers:**

- The SADC AI Opportunity -> `/insights/sadc-ai-opportunity`
- What Agentic AI Means for African Governments -> `/insights/agentic-ai-african-governments`
- From Digital Transformation to AI-Native Transformation -> `/insights/digital-to-ai-native-transformation`

<!-- src: siteContent.ts insightTeasers; Directive §13 topic list -->
<!-- IA note: nav label stays INSIGHTS; section visibly labeled "Insights from Pharos" (Directive §13). -->

**CTA:** READ PHAROS INSIGHTS -> `/insights`
<!-- src: cta-registry contextual; Directive §34 -->

---

## 12 — GOVERNANCE

<!-- src: Directive §17 "12 — GOVERNANCE"; siteContent.ts trustEvidence, GOVERNANCE_SOLUTION -->

**Section label:** TRUST, HUMAN CONTROL AND AUDITABILITY

**Headline:** No client-facing deliverable ships without human sign-off.

**Lead:** The governance layer that makes deployment safe - all PROVEN IN-HOUSE.

- **5-Tier Approval Matrix** - Risk-tiered human approval on every agent action: Auto -> Lead -> Executive -> CEO -> Board, with expiry sweeps so stale approvals never queue forever. [PROVEN IN-HOUSE]
<!-- src: claims-registry claim.five-tier-approval; siteContent.ts trustEvidence te-01 -->
- **SHA-256 Sealed Audit Trails** - Append-only JSONL records of prompts, tool invocations, outputs, approval decisions and escalations. Tamper-evident, never overwritten. [PROVEN IN-HOUSE]
<!-- src: claims-registry claim.immutable-audit-trails; siteContent.ts trustEvidence te-02 -->
- **Four Mandatory Governance Gates** - Contract, DPA, Compliance and Security reviews run before work begins. [PROVEN IN-HOUSE]
<!-- src: claims-registry claim.four-governance-gates; siteContent.ts trustEvidence te-03 -->
- **RBAC With 90-Day Key Rotation** - Admin, approve and run roles separated; API keys rotate every 90 days and on suspected compromise. [PROVEN IN-HOUSE]
<!-- src: claims-registry claim.rbac-key-rotation; siteContent.ts trustEvidence te-04 -->
- **Data Protection** - Malawi Data Protection Act 2017/2024 compliance as default posture; GDPR-level handling for donor and UN data flows. [PROVEN IN-HOUSE]
<!-- src: claims-registry claim.data-protection-act-compliance; siteContent.ts proofPolicy wp-01 -->
- **Sovereign, Offline-First Operation** - Zero-Cloud Boundary option for state, health and financial data. [PROVEN IN-HOUSE]
<!-- src: claims-registry claim.sovereign-offline-first; siteContent.ts trustEvidence te-06 -->

**Honesty statement:** We do not have paying-client deployments yet. Nothing on this site is presented as a client outcome unless the claims ledger verifies it.
<!-- src: claims-registry claim.no-paying-clients (VERIFIED); Directive §10 -->

---

## 13 — FAQ

<!-- src: Directive §17 "13 — FAQ"; Directive §35 FAQ placement -->

**Section label:** FREQUENTLY ASKED QUESTIONS

Home to the objection-removal set - placed after the value proposition, never above it (Directive §35). Answer set lives in `content/drafts/faq.md` (28 questions).

**Homepage subset (top 6, all from faq-registry.json):**

1. What is LightSpeed Holdings?
2. What is the AI Company Builder?
3. How many agents does LightSpeed have? - "LightSpeed's operating model contains 90 roles: 89 AI agents plus one Human CEO."
4. Does LightSpeed replace employees?
5. Is this proven with paying clients?
6. How do we start?

<!-- src: faq-registry faq-01, faq-02, faq-03, faq-05, faq-24, faq-25; Directive §18 Q1-Q5 -->

---

## 14 — FINAL CTA

<!-- src: Directive §17 "14 — FINAL CTA"; §34 CTA system; cta-registry -->

**Headline:** Tell us the problem. We will tell you plainly what it takes.

**Body:** Start a conversation or request an AI Readiness Assessment. We will tell you honestly whether we can help, and exactly what it takes to start. Qualified enquiries get a response within two business days.
<!-- src: faq-registry faq-25, faq-28 -->

**Primary CTA:** START A CONVERSATION -> `/contact`
**Secondary CTA:** REQUEST AN AI READINESS ASSESSMENT -> `/contact`

<!-- §34 note: CTA labels canonicalized. Do not alternate with "Book Briefing", "Executive Briefing", or "Contact Us". -->

---

## DRAFT NOTES FOR CEO / PHAROS REVIEW

1. **Headline choice (§24):** §17 suggests "Autonomous AI Workforce"; this draft uses "AI Workforce" so the hero cannot read as "AI runs the company without humans". Decision needed.
2. **"Proof" removed:** §10 retires "Proof" as an IA concept; section 08 is labeled USE CASES. Existing `homeImmersiveCopy.ts` still has a chapter `id: 'proof'` - needs renaming at implementation time.
3. **Visitor-path destinations (section 03):** card 4 target (`/contact` vs `/what-we-do`) needs confirmation.
4. **Homepage FAQ subset:** which 6 of the 28 questions lead the homepage is a recommendation - CEO/Pharos may re-sequence.
5. **Metrics shown:** none beyond the claims-ledger figures (90/89/1/20/5/4, 40%, 1,200 members, 5,000 records, 2,566 tests not used here). Dashboard KPIs (task success rate, CSAT, cost/task) were deliberately excluded - they come from demo dashboard data, not a validated public metric set.
