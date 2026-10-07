# Solutions - DRAFT awaiting CEO/Pharos sign-off

> **Status:** DRAFT - awaiting CEO/Pharos sign-off.
> **Section:** Directive "WEBSITE TRANSFORMATION & REPOSITORY CONSOLIDATION DIRECTIVE.md" §16 (Solutions), §10 (status labels), §23-§24 (claims & honesty), §34 (CTA system).
> **Sources:** `src/data/registries/solution-registry.json` (8 families: slug, title, eyebrow, description, capabilities, useCases, cta - reproduced verbatim), `src/data/registries/use-case-registry.json` (status labels), `src/data/registries/claims-registry.json`, `src/data/registries/sector-registry.json`, `src/data/siteContent.ts` (solution proof labels), `src/data/registries/cta-registry.json` (canonical CTA labels).

**Page framing (§16):** Solutions answer "What can LightSpeed build or change?". Each solution links to **Use Cases** (`/use-cases`), **Sectors** (`/sectors`), **Insights** (`/insights`) and a **CTA**. Status labels come from the claims/use-case registries; where no registry evidence exists, a `<!-- TODO: needs fact -->` is used instead of a guess.

---

## 1. AI & Agentic Systems

<!-- src: solution-registry.json slug: ai-agentic-systems -->

**Eyebrow:** AI OPERATING MODEL
**Status:** PROVEN IN-HOUSE
<!-- src: claims-registry claim.agent-count, claim.five-tier-approval, claim.immutable-audit-trails (PROVEN_IN_HOUSE); use-case-registry uc-meta, fow-01 (PROVEN IN-HOUSE) -->

**Description:** Build governed multi-agent orchestration platforms where AI agents execute specialized roles across departments, with human CEO oversight, immutable audit trails, and deterministic routing.
<!-- src: solution-registry.json description (verbatim) -->

**Capabilities:**

- Multi-Agent Orchestration (90 agents, 20 departments)
- 5-Tier Human-in-the-Loop Approval Matrix
- Immutable SHA-256 Sealed Audit Trails
- Agent Registry & Role Definitions
- Model Routing (Local/Open-Weight -> Premium)
- Memory & Context Persistence

<!-- src: solution-registry.json capabilities (verbatim) -->

**Use cases:** AI Company Builder Platform Deployment; Enterprise Agent Workforce Automation; Solo Founder AI Operating Model (FOW-01); Consulting Firm Delivery Backbone (FOW-03); Non-Profit Full Capability with Minimal Staff (FOW-04).
<!-- src: solution-registry.json useCases (verbatim) -->

**Links:** Use Cases `/use-cases` | Sectors `/sectors` | Insights `/insights`
**CTA:** EXPLORE AI COMPANY BUILDER -> `/ai-company-builder`
<!-- src: solution-registry cta "Explore AI Company Builder" = canonical (cta-registry contextual; Directive §34) -->

---

## 2. Intelligent Automation

<!-- src: solution-registry.json slug: intelligent-automation -->

**Eyebrow:** WORKFLOW AUTOMATION
**Status:** PILOT
<!-- src: use-case-registry ws-02 (PILOT), uc-vsla-pilot (PILOT); per-capability note: Mobile-Money Integration is FIELDABLE (claims-registry claim.mobile-money-integration FIELDABLE) -->

**Description:** WhatsApp-native assistants, automated document pipelines, and intelligent form workflows that connect teams to tools without app downloads - running on infrastructure people already use.
<!-- src: solution-registry.json description (verbatim) -->

**Capabilities:**

- WhatsApp-Native Conversational Agents
- Document & Report Generation Pipelines
- Form & Survey Automation (Kobo/Google Forms -> Dashboard)
- Internal Tool & Dashboard Development
- Mobile-Money Integration (Airtel Money, TNM Mpamba) [FIELDABLE]
- Offline-First Operation on Local Infrastructure

<!-- src: solution-registry.json capabilities (verbatim); claim.mobile-money-integration (FIELDABLE: Airtel Money, TNM Mpamba, PayChangu) -->

**Use cases:** WhatsApp Customer Chatbot (B1); AI Document/Report Generator (B2); Form + Survey Automation (B3); Internal Tool / Dashboard (B4); Agricultural Cooperative Coordination (ws-02); VSLA/SACCO Mobile Money Workflows.
<!-- src: solution-registry.json useCases (verbatim) -->
<!-- TODO: needs fact - B1-B4 bundle use cases are not in use-case-registry.json; add or assign status labels before publication -->

**Links:** Use Cases `/use-cases` | Sectors `/sectors` | Insights `/insights`
**CTA:** EXPLORE USE CASES -> `/use-cases`
<!-- §34 note: registry cta "Explore Business Automation" is not a canonical label; canonicalized to EXPLORE USE CASES -->

---

## 3. Data & Decision Intelligence

<!-- src: solution-registry.json slug: data-decision-intelligence -->

**Eyebrow:** DATA & ANALYTICS
**Status:** PILOT
<!-- src: use-case-registry uc-health-pilot (PILOT), ws-02 (PILOT) -->
<!-- TODO: needs fact - C1-C4 bundle use cases are not in use-case-registry.json; confirm status labels before publication -->

**Description:** Automate donor-ready reports from Kobo and DHIS2 data in hours, not weeks. Clean data, generate narrative reports against donor templates, and build interactive dashboards accessible on mobile.
<!-- src: solution-registry.json description (verbatim) -->

**Capabilities:**

- Automated Data Cleaning & Analysis
- Donor/Project Report Generation (Compliant Templates)
- Interactive Program KPI Dashboards
- Survey Design, Collection & Analysis
- GDPR-Level Data Protection & Sovereignty
- Cross-Border Consent Workflows for LLM APIs

<!-- src: solution-registry.json capabilities (verbatim); claims-registry claim.data-protection-act-compliance (PROVEN_IN_HOUSE) -->

**Use cases:** Data Cleaning & Analysis (C1); Donor/Project Reports (C2); Interactive Dashboard (C3); Survey Design + Analysis (C4); Health/M&E Clinic Supply Chain Monitoring; Agricultural Cooperative Supply Chain Tracking.
<!-- src: solution-registry.json useCases (verbatim) -->

**Links:** Use Cases `/use-cases` | Sectors `/sectors` | Insights `/insights`
**CTA:** EXPLORE USE CASES -> `/use-cases`
<!-- §34 note: registry cta "Explore Data & Decision Intelligence" is not a canonical label; canonicalized to EXPLORE USE CASES -->

---

## 4. Digital Transformation

<!-- src: solution-registry.json slug: digital-transformation -->

**Eyebrow:** MOBILE-FIRST DESIGN
**Status:** FIELDABLE
<!-- src: sector-registry SMEs & Private Enterprise badge FIELDABLE; claims-registry claim.mobile-money-integration (FIELDABLE, PayChangu included) -->
<!-- TODO: needs fact - confirm FAMILY-level status with CEO: registry bundles A1-A4/D1-D3 have no use-case-registry entries yet -->

**Description:** Mobile-first websites, e-commerce stores, and brand identities built for Southern Africa - with Airtel Money, TNM Mpamba, and PayChangu checkout built in from day one.
<!-- src: solution-registry.json description (verbatim) -->

**Capabilities:**

- Mobile-First Responsive Web Development
- E-Commerce with Local Payment Rails
- Brand Identity & Design Systems
- Google Business & Listings Management
- Bilingual Content (Chichewa + English)
- Social Media Management & Ad Campaigns

<!-- src: solution-registry.json capabilities (verbatim) -->

**Use cases:** Business Website (A1); E-Commerce / Online Store (A2); Brand Identity (A3); Google Business + Listings (A4); Social Media Management (D1); Content Pack (D2); Google/Facebook Ads Setup (D3).
<!-- src: solution-registry.json useCases (verbatim) -->

**Links:** Use Cases `/use-cases` | Sectors `/sectors` | Insights `/insights`
**CTA:** START A CONVERSATION -> `/contact`
<!-- §34 note: registry cta "Explore Digital Presence" is not a canonical label; canonicalized to primary CTA -->

---

## 5. Strategy & Executive Advisory

<!-- src: solution-registry.json slug: strategy-executive-advisory -->

**Eyebrow:** EXECUTIVE ADVISORY
**Status:** PROVEN IN-HOUSE
<!-- src: faq-registry faq-19, faq-28 (the discovery/readiness/research method is LightSpeed's own documented process); methodology proven internally, NOT as paid client work -->
<!-- TODO: needs fact - confirm family status label with CEO; no external engagements exist (claims-registry claim.no-paying-clients VERIFIED) -->

**Description:** Structured discovery, AI readiness assessments, boardroom briefings, and roadmap generation - helping leadership teams move from problem to governed AI deployment with clarity.
<!-- src: solution-registry.json description (verbatim) -->

**Capabilities:**

- AI Strategy & Roadmap Generation
- AI Design Sprint (5-Day Concept-to-Prototype)
- Executive Boardroom Briefing Sessions
- ROI Modeling & Assessment Templates
- Forward-Deployed Engineer Embedding
- Venture Co-Build (Equity + Consulting)

<!-- src: solution-registry.json capabilities (verbatim) -->

**Use cases:** Board Presentation & Platform Deep-Dive; Governance Model Deep-Dive; Engagement Roadmap Planning; AI Readiness Assessment; SADC AI Governance Framework Advisory; National AI Strategy Consultation.
<!-- src: solution-registry.json useCases (verbatim) -->

**Links:** Use Cases `/use-cases` | Sectors `/sectors` | Insights `/insights`
**CTA:** REQUEST AN AI READINESS ASSESSMENT -> `/contact`
<!-- §34 note: registry cta "Request a Boardroom Briefing" is not a canonical label; canonicalized to secondary CTA -->

---

## 6. AI Governance & Policy

<!-- src: solution-registry.json slug: ai-governance-policy -->

**Eyebrow:** GOVERNANCE & POLICY
**Status:** PROVEN IN-HOUSE
<!-- src: claims-registry claim.five-tier-approval, claim.four-governance-gates, claim.immutable-audit-trails, claim.rbac-key-rotation, claim.ai-ethics-board-review (all PROVEN_IN_HOUSE) -->

**Description:** Establish controls, architecture, policies, standards, risk management, and decision rights for responsible AI adoption - aligned with Malawi DPA, SADC frameworks, and AU Continental AI Strategy.
<!-- src: solution-registry.json description (verbatim) -->

**Capabilities:**

- 5-Tier Risk-Classified Approval Matrix
- 4 Governance Gates (Contract, DPA, Compliance, Security)
- Immutable Audit Trails with Expiry Sweeps
- RBAC with 90-Day Key Rotation
- AI Ethics Board Review (Tier 3+)
- SADC/AU Policy Framework Alignment

<!-- src: solution-registry.json capabilities (verbatim); claims-registry claim.rbac-key-rotation, claim.ai-ethics-board-review (PROVEN_IN_HOUSE); alignment claim = directional (claims-registry HISTORICAL caveat - SADC/AU framework work is DEMONSTRATION stage) -->
<!-- §23 note: "aligned with Malawi DPA, SADC frameworks, AU Continental AI Strategy" is registry wording; supporting framework artifacts are drafts/demonstrations - do not upgrade to LIVE without evidence -->

**Use cases:** Compliance Automation for Financial Services; Risk Classification & Audit Trail Generation; Government Compliance Monitoring (FOW-05); Data Protection & Sovereignty Implementation; Regulatory Reporting Automation; AI Ethics Board Review Workflows.
<!-- src: solution-registry.json useCases (verbatim); claim.compliance-automation-40-percent (PROVEN_IN-HOUSE) underpins the compliance entry -->

**Links:** Use Cases `/use-cases` | Sectors `/sectors` | Insights `/insights`
**CTA:** EXPLORE USE CASES -> `/use-cases`
<!-- §34 note: registry cta "View Governance Details" has no canonical target and no governance detail page in IA; canonicalized to EXPLORE USE CASES -->

---

## 7. Research & Applied AI

<!-- src: solution-registry.json slug: research-applied-ai -->

**Eyebrow:** RESEARCH & POLICY
**Status:** DEMONSTRATION
<!-- src: claims-registry claim.university-capacity-building (DEMONSTRATION); SADC framework work is a draft (companyData.ts task "SADC Agentic Governance Policy Framework Draft") -->
<!-- §23 note: registry capability "University Capacity Building & Certification" must NOT be presented as a university partnership (faq-registry faq-19) -->

**Description:** Develop evidence, research, market intelligence, policy analysis, and practical guidance for AI adoption in Malawi, SADC, and Africa - turning engineering observations into public intellectual work via Pharos.
<!-- src: solution-registry.json description (verbatim) -->

**Capabilities:**

- Applied AI Research & Experimentation
- African AI Economics & Open-Weight Model Research
- AI Governance & Policy Research
- SADC Technology & Digital Transformation Studies
- Sovereign AI & Resource-Constrained Deployment Research
- University Capacity Building & Certification
<!-- §23 note: phrase in public copy as training, systems and applied research with Malawian universities (MUBAS, UNIMA) "in active development" - never "in partnership with". No formal partnership is claimed (faq-19). -->

**Use cases:** Pharos Insight Publication (Agentic AI, African AI, AI Governance); SADC Agentic AI Governance Framework; National AI Strategy Consultation Submission; University Talent Pipeline Development; Model Comparison & Benchmarking on Local Infra; Open-Weight Model Routing Optimization.
<!-- src: solution-registry.json useCases (verbatim); published Pharos insights are LIVE (src/data/insights.ts) -->

**Links:** Use Cases `/use-cases` | Sectors `/sectors` | Insights `/insights`
**CTA:** READ PHAROS INSIGHTS -> `/insights`
<!-- src: solution-registry cta "Read Pharos Insights" = canonical (cta-registry contextual; Directive §34) -->

---

## 8. AI Company Builder Deployment

<!-- src: solution-registry.json slug: ai-company-builder-deployment -->

**Eyebrow:** PLATFORM LICENSING
**Status:** FIELDABLE
<!-- src: siteContent.ts solutions[0].proof "Fieldable in 2026"; use-case-registry/proofPolicy "AI Company Builder Platform Deployment" FIELDABLE -->

**Description:** License and deploy the same 90-agent orchestration engine that runs LightSpeed Holdings on your infrastructure - self-hosted, provider-agnostic, with one-on-one onboarding and support.
<!-- src: solution-registry.json description (verbatim) -->

**Capabilities:**

- AI Company Builder License (E1) - Self-Hosted on Your Laptop/VPS
- Agent Setup for Agencies (E2) - White-Label
- Provider-Agnostic Model Routing (9 LLM Providers + Ollama)
- RBAC & Client Portal Access
- Support Retainer (MWK 350,000/mo)
- Extensible Agent & Workflow Configuration

<!-- src: solution-registry.json capabilities (verbatim); claims-registry claim.9-llm-providers (PROVEN_IN_HOUSE) -->
<!-- §23/§34 note: MWK 350,000/mo appears in the canonical registry but faq-27 says costs are discussed after discovery. DECISION NEEDED: publish the figure or defer it to conversation (recommended: defer - FAQ Q27 is the canonical cost language). -->

**Use cases:** Solo Founder AI Workforce (FOW-01); Tech-Savvy Founder Self-Deployment; Local Tech Agency White-Label; Diaspora Entrepreneur Operations; Software Developer Agent Teams.
<!-- src: solution-registry.json useCases (verbatim); use-case-registry fow-01 (PROVEN IN-HOUSE) -->

**Links:** Use Cases `/use-cases` | Sectors `/sectors` | Insights `/insights`
**CTA:** EXPLORE AI COMPANY BUILDER -> `/ai-company-builder`
<!-- src: solution-registry cta "Explore AI Company Builder" = canonical (cta-registry contextual; Directive §34) -->

---

## PAGE-LEVEL STATUS SUMMARY

| # | Solution | Status | Evidence source |
|---|---|---|---|
| 1 | AI & Agentic Systems | PROVEN IN-HOUSE | claims-registry (agent-count, approvals, audit) + uc-meta/fow-01 |
| 2 | Intelligent Automation | PILOT | use-case-registry ws-02, uc-vsla-pilot (money rails FIELDABLE) |
| 3 | Data & Decision Intelligence | PILOT | use-case-registry uc-health-pilot, ws-02 (C1-C4 TODO) |
| 4 | Digital Transformation | FIELDABLE | sector-registry SMEs badge (A/D bundles TODO) |
| 5 | Strategy & Executive Advisory | PROVEN IN-HOUSE | faq-19/28 internal method (external work: none, TODO) |
| 6 | AI Governance & Policy | PROVEN IN-HOUSE | claims-registry governance set |
| 7 | Research & Applied AI | DEMONSTRATION | claims-registry university-capacity-building + SADC draft |
| 8 | AI Company Builder Deployment | FIELDABLE | siteContent "Fieldable in 2026" |

---

## DRAFT NOTES FOR CEO / PHAROS REVIEW

1. **CTA canonicalization (§34):** 4 of 8 registry CTA labels were non-canonical and were mapped to canonical labels ("Explore Business Automation" / "Explore Data & Decision Intelligence" / "Explore Digital Presence" / "Request a Boardroom Briefing" / "View Governance Details"). If CEO prefers keeping distinct per-solution labels, §34 and cta-registry must be amended first - flagging for decision.
2. **MWK 350,000/mo support retainer:** present in canonical solution-registry but in tension with faq-27 ("costs discussed after discovery"). Recommendation: remove from public capability line, keep in sales conversation. Decision needed.
3. **University wording (§23):** "University Capacity Building & Certification" kept from registry but flagged - public phrasing must avoid "partnership" (faq-19).
4. **Status gaps:** B1-B4, C1-C4, A1-A4, D1-D3 bundle use cases are referenced by the registry but absent from use-case-registry.json (16 entries). Marked `<!-- TODO: needs fact -->` rather than guessed.
5. **Registry wording retained verbatim** (descriptions, capabilities, use cases) so solutions.md can be diffed against solution-registry.json during QA.
