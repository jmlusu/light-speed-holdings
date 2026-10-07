# What We Do - DRAFT awaiting CEO/Pharos sign-off

> **Status:** DRAFT - awaiting CEO/Pharos sign-off.
> **Section:** Directive "WEBSITE TRANSFORMATION & REPOSITORY CONSOLIDATION DIRECTIVE.md" §15 (What We Do), §16 (link boundary to Solutions), §23-§24 (claims & honesty), §34 (CTA).
> **Sources:** `src/data/capabilities.ts` (four capability families, verbatim descriptions), `src/data/registries/solution-registry.json`, `src/data/registries/claims-registry.json`, `src/data/registries/faq-registry.json`, `src/data/siteContent.ts` (capability cycle), `src/data/ctas.ts`.

**Positioning rule (§15):** this page explains the LightSpeed **engagement model** - how we move an organization from problem to measured outcome. It is NOT a giant service catalog: per-family detail lives on `/solutions` (§16), evidence lives on `/use-cases` (§10). The page shows the method; it does not restate all 8 solution offerings.

---

## HERO

**Eyebrow:** LIGHTSPEED HOLDINGS // ENGAGEMENT MODEL

**Headline:** Strategy. Build. Govern. Research & Policy.
<!-- src: capabilities.ts CAPABILITIES titles; siteContent.ts capability cycle (Strategy -> Build -> Govern -> Research & Policy) -->

**Subheadline:** We help organizations move from a real problem to a governed, measured AI capability - not from a pitch deck to a pilot that never ships.
<!-- src: Directive §15 (engagement model framing); §24 (no inflated promises) -->

**Primary CTA:** START A CONVERSATION -> `/contact`
**Secondary CTA:** REQUEST AN AI READINESS ASSESSMENT -> `/contact`
<!-- src: cta-registry primary/secondary; Directive §34 -->

---

## THE ENGAGEMENT MODEL (how work actually flows)

<!-- src: Directive §15 (PROBLEM -> MEASURE chain, verbatim) -->

```
PROBLEM
   ↓
DESIGN
   ↓
BUILD
   ↓
DEPLOY
   ↓
GOVERN
   ↓
MEASURE
```

| Stage | What happens | What you get |
|---|---|---|
| PROBLEM | Start with your business problem, not the technology. Diagnose whether AI can help at all - we will say no when it cannot. | Honest read: help, partly, or not yet. [PROVEN IN-HOUSE process] |
| DESIGN | AI strategy, AI readiness, data architecture, agentic workflow design. Baseline captured during the AI Readiness Assessment. | Operating model, roadmap, success metrics agreed up front. |
| BUILD | AI implementation - AI-native workflows, applications, agentic systems, data products, automation. | Working capability, delivered in stages (Foundation 14-21 days, Pilot 6-10 weeks, Scale 3-6 months). |
| DEPLOY | Staged rollout onto your infrastructure or ours; offline-first and Zero-Cloud Boundary options for sensitive data. | Capability in production use, with local-first economics. |
| GOVERN | Five-tier approval, four governance gates, SHA-256 audit trails, RBAC - governance from day one, not bolted on. | [PROVEN IN-HOUSE] controls that make deployment safe. |
| MEASURE | Outcomes measured against the assessment baseline and reported - never asserted in marketing copy. | Evidence: what changed, what it cost, what to do next. |

<!-- src: faq-registry faq-18 (stage duration + governance from day one), faq-28 (research and policy built into engagements), faq-19 (honest "no" on engagement), claims-registry claim.five-tier-approval / claim.four-governance-gates / claim.immutable-audit-trails (PROVEN_IN_HOUSE) -->
<!-- §23 note: stage durations are commitments from faq-registry, not invented ranges. Measurement values are TBD until Phase 0 validation - see value-metric TODO below. -->

---

## CORE CAPABILITY FAMILIES

<!-- src: Directive §15 core capability families; capabilities.ts descriptions (verbatim) -->

### 1. STRATEGY

Turn organizational priorities into executable strategies, operating models, roadmaps, and AI opportunities.
<!-- src: capabilities.ts title/description verbatim -->

**Covers:** AI strategy - AI readiness assessments - digital transformation direction - executive advisory.
<!-- src: Directive §15 "Include" list; solution family "Strategy & Executive Advisory" (solution-registry) -->

### 2. BUILD

Design and build AI-native workflows, applications, agentic systems, data products, automation, and digital operating capabilities.
<!-- src: capabilities.ts title/description verbatim -->

**Covers:** agentic workflow design - AI implementation - data architecture - intelligent automation - AI company builder deployment.
<!-- src: Directive §15 "Include" list; solution families "AI & Agentic Systems", "Intelligent Automation", "Data & Decision Intelligence", "AI Company Builder Deployment" (solution-registry) -->

### 3. GOVERN

Establish controls, architecture, policies, standards, risk management, security, data governance, and decision rights for responsible AI adoption.
<!-- src: capabilities.ts title/description verbatim -->

**Covers:** governance - policy - AI governance & policy solution family - five-tier approval, four governance gates, SHA-256 audit trails as the reference implementation. [PROVEN IN-HOUSE]
<!-- src: Directive §15 "Include" list; claims-registry claim.five-tier-approval, claim.four-governance-gates, claim.immutable-audit-trails (PROVEN_IN_HOUSE) -->

### 4. RESEARCH & POLICY

Develop evidence, research, market intelligence, policy analysis, and practical guidance for AI adoption in Malawi, SADC, and Africa.
<!-- src: capabilities.ts title/description verbatim -->

**Covers:** research - institutional capacity building - Pharos thought leadership - applied AI research.
<!-- src: Directive §15 "Include" list; solution family "Research & Applied AI" (solution-registry); Directive §13 (Pharos) -->
<!-- §23 note: institutional capacity building is delivered as training, systems and applied research - NOT as formal university partnerships. No partnership is claimed or implied. (faq-registry faq-19; claims-registry claim.university-capacity-building is classified DEMONSTRATION and its ledger wording "in partnership with" must not be used publicly.) -->

---

## WHAT THIS IS NOT

<!-- src: Directive §15 "Do not make the page a giant service catalog"; claims-registry claim.no-paying-clients (VERIFIED) -->

- Not a price sheet - engagement costs are discussed after discovery, in Malawian Kwacha, and no public pricing page exists. [VERIFIED]
<!-- src: faq-registry faq-27; claims-registry claim.no-paying-clients -->
- Not a client roster - we do not have paying-client deployments yet, and this page claims none.
<!-- src: claims-registry claim.no-paying-clients (VERIFIED) -->
- Not the catalog - the 8 solution families with capabilities, use cases and links live on `/solutions`.
<!-- src: Directive §16; §15 catalog boundary -->
- Not the proof - labeled evidence lives on `/use-cases` (LIVE / PROVEN IN-HOUSE / PILOT / DEMONSTRATION / FIELDABLE / FUTURE).
<!-- src: Directive §10 status labels -->

---

## WHERE TO GO NEXT

<!-- src: Directive §15 (link out, do not duplicate), §34 CTA system -->

| If you want... | Go to | CTA label |
|---|---|---|
| The full 8 solution families | `/solutions` | EXPLORE SOLUTIONS |
| Labeled evidence of what works | `/use-cases` | EXPLORE USE CASES |
| The flagship platform in depth | `/ai-company-builder` | EXPLORE AI COMPANY BUILDER |
| A session for your leadership team | `/contact` | START A CONVERSATION |

<!-- src: cta-registry contextual + primary; Directive §34 labels canonicalized -->
<!-- §34 note: siteContent/legacy CTAs include "View Service Catalog" (/what-we-do) and "Executive Briefing" variants - canonicalized away per §34. -->

---

## DRAFT NOTES FOR CEO / PHAROS REVIEW

1. **Catalog boundary respected:** page states method + capability families and links out to `/solutions` for the 8 offerings, per §15.
2. **Institutional capacity building (§23 concern):** phrased as training/systems/research with an explicit no-partnership-claimed note. If CEO wants the MUBAS/UNIMA names shown, approved phrasing must be "in active development with Malawian universities" - never "partnership" (contra claims-registry ledger wording).
3. **Value metrics:** MEASURE stage shows no numbers pending Phase 0 validation (same TODO as homepage/ACB drafts).
4. **FAQ:** §35 places FAQ on Homepage, AI Company Builder, Use Cases and About - not on this page. If CEO wants the Quick Answer component here anyway, use `content/drafts/faq.md` Q1/Q18/Q19.
5. **Status labels:** PROVEN IN-HOUSE (governance reference implementation, honest-no process); no other claims made.
