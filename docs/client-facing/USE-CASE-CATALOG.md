---
title: "LightSpeed Holdings — Use Case Catalog"
subtitle: "Master content source for the client-facing website"
status: "Draft v1 — for website incorporation"
owner: "thought-leadership-author"
date: "2026-09-10"
sources:
  - "results/use-case-fact-pack.md"
  - "results/use-case-messaging-brief.md"
  - "docs/superpowers/specs/2026-09-06-lightspeed-website-design.md"
honesty_classification: >
  Nothing in this document has been delivered to paying clients. All offers are
  fieldable in 2026, in pilot, or in active development. Every proof point carries
  an explicit honesty-ladder badge. No fabricated metrics, testimonials, or client
  logos appear anywhere in this document.
---

# Positioning

LightSpeed Holdings Limited™ is an AI-native company builder headquartered in Lilongwe, Malawi. The company operates a governed 144-agent, 20-department orchestration platform — the same system it sells to clients — making it both builder and proof of its own product. The leading positioning line is: **"The AI-native company builder for Southern Africa."** Five offer families (digital presence, business automation, data and analytics, digital marketing, and platform licensing) serve enterprise, government, donor, SME, and diaspora clients across Malawi and the SADC region. The tagline is **"ASPIRE. ACT. ACHIEVE."** Nothing has been delivered to paying clients yet — all offers are fieldable in 2026 or in pilot; every proof point is honesty-badged. This catalog is the master content source for the client-facing website.

---

# The Method

The AI Company Builder is the platform LightSpeed Holdings uses to run itself. It is a governed, multi-agent orchestration engine where 143 AI agents and one human CEO operate across 20 departments — content, compliance, finance, engineering, sales, Pharos thought leadership, and more. Every task follows a delivery pipeline: brief → inbox task → assigned agent(s) → human review → deliverable.

Governance is not a feature bolted on later. It is the architecture:

- **5-tier human-in-the-loop (HITL) approvals.** Agents execute; the human CEO owns the outcome. No client-facing deliverable ships without human sign-off. Approval gates block executor threads for up to 30 minutes per request.
- **4 governance gates (G1–G4).** Every client engagement must clear contract (G1), data-processing agreement (G2), compliance review (G3), and security assessment (G4) before work begins.
- **Immutable audit trails.** Every action generates an append-only JSONL audit event — correlated, queryable, and never overwritten. Every approval is gated; every escalation is documented.
- **Risk-classified agent tiers.** A 5×5 likelihood × impact risk matrix maps to 4 risk levels (low, medium, high, critical), each with a defined review cadence from quarterly to daily. Twenty-five distinct actions are risk-gated in the approval matrix.
- **Board-level governance cadence.** Weekly standup → bi-weekly product review → monthly management board review → quarterly strategy session → annual refresh.
- **Ethics Board review.** Tier 3+ deliverables require AI Ethics Board review before delivery.

Sovereignty is foundational. The platform is designed for offline-first operation, runs on local infrastructure, integrates with Malawi payment rails (Airtel Money, TNM Mpamba, PayChangu), and complies with the Malawi Data Protection Act 2017/2024 and GDPR from day one — not retrofitted. Data stays on your infrastructure. Where LLM providers are used, the most privacy-preserving option is selected and every cross-border data flow is documented in the governance gate process. Nine LLM providers are configured, including free local models via Ollama for budget-constrained deployments.

This is the "proven in-house" rung of the honesty ladder: the company runs on this platform daily, and the architecture is openly documented.

---

# The Four Reservations — Trust-by-Engineering

Decision-makers in the environments we serve hold four repeatable reservations
about AI. LightSpeed's answer is not marketing language — it is an engineering
discipline, honesty-badged, and built into every offer.

**The four reservations:**

1. **Low-bandwidth / resource-constrained** — "This won't work on our devices, our
   connectivity, or our electricity reality."
2. **Data protection** — "Where does our data go? Does it leave our country?"
3. **Technology debt** — "Won't this rip out what we have, or become a system we
   must maintain forever?"
4. **Skepticism of AI** — "We tried AI before and it failed. Why is this
   different, and how do we trust it?"

**How we answer them:**

| Reservation | Answer (summary) |
|-------------|-----------------|
| Low-bandwidth | Offline-first architecture, local models via Ollama, WhatsApp-native, PWA with offline queues. Traffic quota-first on weak links. We test where you operate because we operate there. |
| Data protection | Sovereign in-country processing; every cross-border LLM flow documented in G1–G4 governance gates; DPA 2017/2024 + GDPR from day one; no client data used to train models. |
| Technology debt | 90-day pilot API connectors — no rip-and-replace, no lock-in. Our own engineering debt is tracked, linted, and budgeted. Agent cost is variable, visible, and optimisable. |
| Skepticism | 5-tier human-in-the-loop approvals, immutable audit trails, risk-classified tiers, circuit breakers, red-team and eval gates. Honesty badges on every claim — we never fabricate proof. |

Full doctrine, evidence mapping, and capability DNA framing:
`docs/RESERVATIONS-STRATEGY.md`
Operating skill: `.agents/skills/reservations-playbook/`
Portfolio demo probe script: `results/reservations-demo-script.md`

---

# Services

LightSpeed Holdings offers five families of service, each mapped to specific deliverables, target clients, and an honesty badge. Pricing is anchored in dual currency (MWK for local clients, ~USD for international) and is to be validated with prospects before publishing.

---

## Offer A — Digital Presence

Every business in Malawi deserves a digital front door. LightSpeed builds mobile-first websites, e-commerce stores, and brand identities — with Airtel Money, TNM Mpamba, and PayChangu checkout built in from day one. From MWK 150,000 (~$85) for a Google Business listing to a full online store with 20 products, we design for the way Malawi actually transacts.

**Honesty badge:** Fieldable in 2026 — governance approved, ready for deployment, not yet in client hands.

| Deliverable | Description | Price (MWK) | Price (~USD) | Turnaround |
|-------------|-------------|-------------|--------------|------------|
| **A1 — Business Website** | Up to 5 pages, mobile-first, contact form, WhatsApp button, hosting setup, 30 days support | MWK 800,000 | ~$450 | 5–10 days |
| **A2 — E-commerce / Online Store** | Product catalog, Airtel Money / Mpamba checkout, order notifications, 20 products | MWK 1,800,000 | ~$1,000 | 10–15 days |
| **A3 — Brand Identity** | Logo, color system, fonts, social media kit, letterhead | MWK 500,000 | ~$280 | 3–5 days |
| **A4 — Google Business + Listings** | Map listing, business info management, review setup | MWK 150,000 | ~$85 | 2–3 days |

**Target clients:** Local SMEs, schools, clinics, hotels/lodges, agri-businesses, churches, real estate.

**Governance:** Low-risk commodity service. Minimal PII; standard gates suffice.

**Pricing note:** Pricing is to be validated with 2–3 real prospects before publishing. 50% upfront / 50% on delivery for all one-off projects. All prices exclude ad spend, hosting, domain, and payment gateway fees.

---

## Offer B — Business Process Automation

Your customers are already on WhatsApp. LightSpeed builds WhatsApp-native assistants that handle FAQs, take orders, process bookings, and hand off to a human when the conversation gets complex. Integrated with Airtel Money and TNM Mpamba for instant mobile-money checkout — no app download required. Offer B also includes document and report generators, form automation, and internal dashboards for cooperatives, clinics, and schools.

**Honesty badge:** In active development — delivery awaits completion of the G1–G4 security review and liability cap ratification. Sales opening when governance gates clear. Offer B is currently blocked.

| Deliverable | Description | Price (MWK) | Price (~USD) | Turnaround |
|-------------|-------------|-------------|--------------|------------|
| **B1 — WhatsApp Customer Chatbot** | FAQ + order/service automation, handoff to human, analytics dashboard | MWK 1,500,000 | ~$850 | 7–14 days |
| **B2 — AI Document/Report Generator** | Template-driven report generation (donor reports, payroll letters, certificates) | MWK 1,200,000 | ~$680 | 7–14 days |
| **B3 — Form + Survey Automation** | Kobo/Google-Forms-to-spreadsheet pipeline, auto-alerts, summary dashboards | MWK 900,000 | ~$500 | 5–10 days |
| **B4 — Internal Tool / Dashboard** | Custom web dashboard for stock, sales, students, patients, or members | MWK 2,500,000 | ~$1,400 | 10–20 days |

**Target clients:** SMEs, clinics, schools, cooperatives, transport companies.

**Governance:** BLOCKED. WhatsApp customer data and cross-border LLM transfer require G1–G4 completion and liability cap ratification before any client engagement. B1 also requires a recurring hosting commitment (MWK 100,000/mo, ~$56/mo).

**Pricing note:** Pricing is to be validated with prospects. All prices exclude ad spend, hosting, domain, and payment gateway fees.

---

## Offer C — Data, Analytics & Donor Reporting

NGOs and development programmes spend weeks turning Kobo and DHIS2 data into donor-ready reports. LightSpeed automates that pipeline: clean the data, generate narrative reports against donor templates, and build interactive dashboards your field team can access on a phone. All hosted in-region, all compliant with Malawi's Data Protection Act.

**Honesty badge:** In active development — delivery awaits donor-data cross-border consent workflow completion and liability cap ratification. Sales opening when governance gates clear. Offer C is currently blocked.

| Deliverable | Description | Price (MWK) | Price (~USD) | Turnaround |
|-------------|-------------|-------------|--------------|------------|
| **C1 — Data Cleaning & Analysis** | Clean dataset + insights report (Excel/PDF) | MWK 700,000 | ~$400 | 3–7 days |
| **C2 — Donor/Project Reports** | Narrative + data-visualized quarterly/annual reports compliant with donor templates | MWK 1,000,000 | ~$550 | 5–10 days |
| **C3 — Interactive Dashboard** | Live web dashboard for program KPIs (mobile-friendly, NGO-grade) | MWK 2,000,000 | ~$1,100 | 10–15 days |
| **C4 — Survey Design + Analysis** | Questionnaire design, data collection setup, analysis, recommendations | MWK 1,300,000 | ~$720 | 7–14 days |

**Target clients:** NGOs, development programmes, UN agencies, cooperatives, research organizations.

**Governance:** BLOCKED. Donor data is treated as Tier-1 sensitive — requires explicit consent for cross-border transfer to LLM provider APIs. Professional liability cap required before any client engagement. The donor data waiver workflow is in active development.

**Pricing note:** International NGOs expect USD quotes and pay in USD. Quote at the USD figure directly with terms (50% upfront, 50% on delivery).

---

## Offer D — Digital Marketing

Reach Malawian customers where they already are — Facebook, WhatsApp, Google — with localised content, community management, and ad campaigns. LightSpeed handles the content calendar, the posting, and the optimisation so you can run the business.

**Honesty badge:** Fieldable in 2026 — governance approved, low-risk commodity service, ready for deployment, not yet in client hands.

| Deliverable | Description | Price (MWK) | Price (~USD) | Turnaround |
|-------------|-------------|-------------|--------------|------------|
| **D1 — Social Media Management** | Content calendar, 12 posts/month , community management | MWK 350,000/mo | ~$200/mo | Ongoing retainer |
| **D2 — Content Pack** | 10 blog articles + 20 social captions | MWK 600,000 | ~$340 | 5–10 days |
| **D3 — Google/Facebook Ads Setup** | Campaign setup, pixel, tracking, 2-week optimization | MWK 700,000 | ~$400 | 3–5 days |

**Target clients:** SMEs, local businesses, lodges, clinics, cooperatives.

**Governance:** Low-risk commodity service. Minimal PII; standard gates suffice. Ad spend is excluded from all pricing.

---

## Offer E — Platform Licensing

The same 144-agent orchestration engine that runs LightSpeed Holdings can run on your infrastructure. License the AI Company Builder, get one-on-one onboarding, and operate your own governed AI workforce — self-hosted, provider-agnostic, and extensible. For agencies: white-label agent teams for your clients.

**Honesty badge:** Fieldable in 2026 — proven in-house (our own company runs on this platform daily), ready for external licensing.

| Deliverable | Description | Price (MWK) | Price (~USD) | Turnaround |
|-------------|-------------|-------------|--------------|------------|
| **E1 — AI Company Builder License** | One-on-one onboarding, your own governed AI company running on your laptop/VPS | MWK 3,500,000 | ~$2,000 | 1–2 weeks setup |
| **E2 — Agent Setup for Agencies** | White-label: we stand up agent teams for your agency's clients | Contact for quote | — | — |

**Target clients:** Tech-savvy founders, local agencies, diaspora entrepreneurs, developers.

**Governance:** No client data handling; product license only. No G1–G4 blocking. E2 (agency setup) is in active development with no public pricing.

**Pricing note:** E1 is a one-off license fee plus a recurring support retainer of MWK 350,000/mo (~$200/mo). E2 pricing is to be determined.

---

### Enterprise Transformation Line

In addition to the five offer families, LightSpeed Holdings is developing an enterprise consultancy line for organizations that need more than a productized deliverable. These services are in active development — modules are being built, not yet production-ready. They are included here for completeness and to support the Method page narrative.

| Capability | Description | Status |
|------------|-------------|--------|
| **Strategy & Roadmap** | Structured discovery → roadmap generation; assessment templates, ROI modeling | In active development |
| **AI Design Sprint (5-day)** | 5-day concept-to-prototype engagement: kickoff → research → prototype → demo → backlog | In active development |
| **Forward-Deployed Engineers** | Embed AI agents within client teams as consulting capacity | In active development |
| **Venture Co-Build** | Build AI-native ventures from scratch; equity stakes + consulting | In active development |
| **Platform Licensing (Managed Hosting)** | Managed deployment with RBAC + client portals | In active development |
| **Industry Accelerators** | Per-vertical agent presets, prompt packs, KPI dashboards | In active development |
| **Client Portal / Self-Service** | Read-only client dashboard: project status, costs, deliverables | In active development |

---

# Industries

## SADC Industry Verticals

LightSpeed Holdings targets five industry verticals for the client-facing website. Each represents a sector where agentic AI has a specific, demonstrable application in Malawi and the broader SADC region.

---

### Agriculture & Agritech

Weather data, soil analysis, and mobile-money micro-loan risk assessments — agentic AI workflows that help smallholder farmers make better decisions and help agri-businesses manage supply chains. Designed for offline-first environments where connectivity is intermittent. The foundation is being built through a piloting initiative with the Ministry of Agriculture.

**Key use cases:**

- Agentic weather + soil advisory for smallholder farmers (modelled on Ulangizi-style chatbot patterns)
- Mobile-money micro-loan risk assessment for agricultural cooperatives
- Supply chain monitoring and procurement automation for agri-businesses

**Honesty status:** In pilot / Fieldable 2026.

---

### Public Health & M&E

Monitor clinic supply chains, auto-generate procurement requests on anomaly detection, and produce donor-ready M&E reports from Kobo and DHIS2 data. The pipeline from field collection to boardroom reporting is designed to move from weeks to hours. Health and M&E use cases are in pilot development, composing evidence and aligning with stakeholder credibility frameworks.

**Key use cases:**

- Clinic supply chain monitoring with Z-score anomaly detection and auto-procurement
- Donor-ready quarterly and annual M&E reports from Kobo/DHIS2 data
- Interactive program dashboards (mobile-friendly, NGO-grade)
- Citizen-query agents for public health information

**Honesty status:** In pilot (composing evidence). No confirmed partnership with any named health organization has been signed.

---

### Financial Inclusion (VSLA / SACCO / Mobile Money)

Agentic workflows over Airtel Money and TNM Mpamba rails, serving informal savings groups (VSLA/SACCO) and micro-finance institutions. Micro-loan risk assessment for smallholder farmers, automated savings tracking, and mobile-money reconciliation — built for the dual-economy reality of Southern Africa.

**Key use cases:**

- Agentic workflows over Airtel Money and TNM Mpamba rails
- Automated savings tracking for VSLA/SACCO groups
- Micro-loan risk assessment for smallholder farmers
- Mobile-money reconciliation and reporting

**Honesty status:** In pilot (use case in active development). This is a use case that development organizations working in financial inclusion are actively seeking; no signed engagement exists.

---

### SME & Services

A "Company-in-a-Box" lightweight agent set — Marketing, Sales, Compliance, Finance, HR — for Malawian SMEs that cannot afford a full team but need full capability. From the bar that runs AI-powered inventory and pricing to the lodge that automates bookings and guest communications.

**Key use cases:**

- AI-powered inventory, sales, and profitability monitoring (demonstrated at J&S StopOver Bar)
- Booking and guest communication automation for hospitality
- Lightweight agent sets for Marketing, Sales, Compliance, Finance, HR
- WhatsApp-native customer service for SMEs

**Honesty status:** Fieldable 2026. J&S StopOver Bar provides live proof-of-concept (see Proof section).

---

### Government / Public Sector

Citizen-query agents, legislative summarisation, project monitoring, and compliance reporting — built for the governance-first standards that Malawi's DPA and SADC's digital transformation agenda demand. Every action is auditable. Every approval is gated.

**Key use cases:**

- Compliance monitoring and regulatory reporting for government agencies
- Contract review and legal document analysis at scale
- Citizen-query agents for public service information
- Legislative summarisation and policy analysis
- HR and personnel management automation

**Honesty status:** In active development. Governance framework mapped to Malawi DPA and SADC standards. National AI Strategy consultation submission published.

---

## Company Scenarios — Platform Use Cases

The following eight scenarios describe how the AI Company Builder platform can be deployed. These are platform use cases, not client deliverables — they illustrate the breadth of the orchestration framework and support the Method and Industries pages.

**FOW-01 — Startup Acceleration (Solo Founder + AI).** A solo founder operates with the functional coverage of a multi-person team: agents handle CTO, CFO, CMO, and CLO roles, with a CEO dashboard for real-time visibility. The founder sets vision; agents execute operations, legal, finance, marketing, and sales. Proven in-house — LightSpeed itself operates as a 1-human, 144-agent organisation.

**FOW-02 — Enterprise Automation (Augment Existing Teams).** Existing teams gain specialist AI agents for compliance scanning, data pipelines, and contract review — without the 6-month hiring cycle. The system adapts to an organization's structure via YAML configuration. In active development; enterprise deployment model designed for SADC regulatory environments.

**FOW-03 — Consulting Firm Scale (Delivery Backbone).** Consulting firms sell expertise but are constrained by headcount. Agents handle research, analysis, and report generation; humans focus on client relationships. In active development; framework validated in LightSpeed's own consulting operations.

**FOW-04 — Non-Profit Operations (Full Capability, Minimal Staff).** A small non-profit gets coverage across finance, HR, compliance, M&E, and donor communications. The audit trail provides the documentation grantmakers require. In active development; supports free local models (Ollama) for budget-constrained deployments.

**FOW-05 — Government Compliance (Authorisation-Aligned).** AI agents handle compliance monitoring, contract review, and regulatory reporting. The 5-tier approval matrix aligns with government authorisation levels. In active development; governance framework mapped to Malawi DPA and SADC standards.

**FOW-06 — E-Commerce (24/7 Customer Success).** Customer success, sales pipeline, and marketing analytics without shift-based human teams. AI agents maintain customer context across interactions and escalate high-value issues. In active development; WhatsApp-native interface designed for SADC mobile-first markets.

**FOW-07 — Healthcare Administration.** Billing compliance, patient scheduling, credentialing, and regulatory reporting — agents handle the administrative burden so clinical staff can focus on patients. Memory encryption and PII detection for sensitive data environments. In active development; designed for Malawi DPA and GDPR compliance.

**FOW-08 — Financial Services (Risk & Compliance).** Continuous compliance monitoring, risk analysis, and audit preparation. The 5-tier approval matrix maps directly to financial services authorisation levels. In active development; audit trail meets financial regulatory documentation requirements.

---

# Proof

Every proof point in this section carries an explicit honesty-ladder badge. No testimonials, no logo walls, no invented metrics.

---

## J&S StopOver Bar — Live SME Proof

**Honesty badge:** Live proof — not a paid client.

J&S StopOver Bar is a real, non-tech SME in Malawi running agentic decision support. The system monitors inventory levels, sales velocity, cash reconciliation, procurement needs, and profitability — demonstrating that AI-native operations work in the informal economy. This is the world's smallest AI-native bar: a genuinely African SME AI transformation case, built in-house and documented openly.

**What it monitors:** Inventory, sales, shortage detection, cash reconciliation, procurement triggers, and profitability tracking.

**Why it matters:** It is the most tangible proof that the AI Company Builder works outside a lab — on a real business, with real money, in a real Malawian market.

---

## Lightspeed Holdings — The Meta Case Study

**Honesty badge:** Proven in-house.

LightSpeed Holdings is its own first customer. The company runs on the same 144-agent, 20-department orchestration platform it offers to clients. Five-tier HITL approvals, immutable audit trails, RACI matrices, and governance controls mapped to regulatory requirements — all operating daily. The CEO directs strategy; 143 AI agents handle operations. This is not a demo; it is an operating company that builds the tooling it uses.

**What it proves:** The platform is real, governed, and running in production — on our own operations.

---

## Pilots in Development

### Health / M&E — Clinic Supply Chain Monitoring

**Honesty badge:** In pilot (composing evidence).

Agentic workflows for monitoring clinic supply chains and auto-generating procurement requests on anomaly detection (dashboard Z-score triggers). This use case is in pilot development, composing evidence and aligning with sector credibility frameworks. No confirmed partnership with any named health organization has been signed.

---

### VSLA / SACCO / Mobile Money — Financial Inclusion

**Honesty badge:** In pilot (use case in active development).

Agentic workflows over mobile-money rails (Airtel Money, TNM Mpamba) for informal savings groups and micro-finance institutions. Micro-loan risk assessment for smallholder farmers. This is a use case that development organizations working in financial inclusion are actively seeking. No signed engagement exists.

---

### Ministry of Agriculture — Farmer Advisory

**Honesty badge:** In pilot.

Building the foundation for farmer advisory, citizen-query, and public-service agents in partnership with the Ministry of Agriculture. The capability is in pilot development.

---

### Citizen-Inquiry Lighthouse (Proposed)

**Honesty badge:** In pilot (proposed — not yet launched).

LightSpeed Holdings is prepared to pilot a high-visibility lighthouse use case — a citizen-inquiry or legislative-summary agent — with a non-commercial partner, as part of the National AI Strategy consultation. This use case is proposed, not yet launched.

---

# Policy

LightSpeed Holdings does not only build agentic AI — it shapes the policy that governs it. The policy track positions the company as a regional thought leader and provides tangible contributions to the governance conversation across Malawi and SADC.

---

## Citizen-Inquiry Lighthouse (Proposed)

**Honesty badge:** In pilot (proposed).

A proposed high-visibility lighthouse use case — a citizen-inquiry or legislative-summary agent — designed for deployment with a non-commercial partner. The purpose is to demonstrate governed agentic AI in a public-service context and generate a replicable model for the National AI Strategy.

---

## Governance Controls as National Template

**Honesty badge:** Proven in-house.

LightSpeed Holdings already operates the governance pattern it proposes as a national template: 5-tier approvals, immutable audit trails, RACI matrices, risk-classified agent tiers, and 4-gate client onboarding (G1–G4). This governance architecture is offered as a template for Malawi's Department of E-Government and MACRA, and as a reference model for SADC harmonisation.

---

## Capacity Building

**Honesty badge:** In active development.

Training and certification programmes in partnership with Malawian universities (MUBAS, UNIMA) to build a sovereign agentic-AI talent pipeline. The goal is to ensure that Malawi and the SADC region develop local expertise in governed AI deployment, rather than importing capability from abroad.

---

## National AI Strategy + SADC Framework

**Honesty badge:** Published (National AI Strategy) / In active development (SADC Framework).

The SADC Agentic AI Governance Framework is the region's first operational governance standard for autonomous agentic AI — authored by the CEO and submitted to SADC Member State digital ministers and telecom regulators (MACRA, CRASA), central banks, and regional development banks. The National AI Strategy consultation submission has been published, proposing lighthouse use cases and governance architecture for the Department of E-Government. Both are aligned to the AU Continental AI Strategy.

---

# Get in Touch

**Primary CTA:** Book a Discovery Call.

Whether you are an enterprise lead in Lilongwe, an NGO programme manager in Blantyre, a diaspora entrepreneur in Johannesburg, or a policymaker in Lusaka, the conversation starts with a discovery call. We will map your challenge to the right offer, the right governance posture, and the right price point — in MWK or USD.

**Secondary CTA:** Read the Malawi Agentic AI Monitor — the monthly thought-leadership publication tracking agentic AI deployment, governance, and policy across Malawi and SADC.

**Tertiary CTA:** See Our Research — the Pharos publications library, including the SADC Agentic AI Governance Framework, the National AI Strategy consultation submission, and the H-A-O-M-T-G-V framework documentation.

**Contact framing:**

- **Malawi clients:** Lilongwe office. Dual-currency pricing (MWK via Airtel Money, TNM Mpamba, or bank transfer; USD via bank transfer for international contracts).
- **SADC clients:** Regional coverage across Zambia, Zimbabwe, South Africa, and the broader SADC corridor. USD pricing standard; MWK available for Malawi-based engagements.

LightSpeed Holdings Limited™ — Lilongwe, Malawi.

**ASPIRE. ACT. ACHIEVE.**

---

# Appendix A — Website Incorporation Map

This table maps each section of this document to the target page in the future client-facing website (`/website`), per the site design spec §4.

| Document Section | Target Page(s) | Site Spec Reference |
|------------------|-----------------|---------------------|
| **Positioning** | `/ (Home)` — Hero + Trust Strip | §4.2 items 1–2 |
| **The Method** | `/method` — H-A-O-M-T-G-V framework, HITL, audit trails, sovereignty | §4.1 nav item 2; §4.2 item 5 |
| **Offer A — Digital Presence** | `/services` — Offer A detail; `/ (Home)` Services Preview card | §4.1 nav item 3; §4.2 item 4 |
| **Offer B — Business Process Automation** | `/services` — Offer B detail; `/ (Home)` Services Preview card | §4.1 nav item 3; §4.2 item 4 |
| **Offer C — Data, Analytics & Donor Reporting** | `/services` — Offer C detail; `/ (Home)` Services Preview card | §4.1 nav item 3; §4.2 item 4 |
| **Offer D — Digital Marketing** | `/services` — Offer D detail | §4.1 nav item 3 |
| **Offer E — Platform Licensing** | `/services` — Offer E detail; `/method` cross-link | §4.1 nav item 3 |
| **Enterprise Transformation Line** | `/services` — Enterprise line | §4.1 nav item 3 |
| **Agriculture & Agritech** | `/industries` — detail page; `/ (Home)` Industry Tiles | §4.1 nav item 4; §4.2 item 6 |
| **Public Health & M&E** | `/industries` — detail page; `/ (Home)` Industry Tiles | §4.1 nav item 4; §4.2 item 6 |
| **Financial Inclusion (VSLA / SACCO)** | `/industries` — detail page; `/ (Home)` Industry Tiles | §4.1 nav item 4; §4.2 item 6 |
| **SME & Services** | `/industries` — detail page; `/ (Home)` Industry Tiles | §4.1 nav item 4; §4.2 item 6 |
| **Government / Public Sector** | `/industries` — detail page; `/ (Home)` Industry Tiles | §4.1 nav item 4; §4.2 item 6 |
| **Company Scenarios (FOW-01..08)** | `/method` — deep-dive; `/industries` cross-links | §4.1 nav item 2 |
| **J&S StopOver Bar** | `/proof` — Proof card; `/industries` SME tile cross-link | §4.1 nav item 5; §4.2 item 7 |
| **Lightspeed Holdings Meta Case** | `/proof` — Proof card; `/method` cross-link | §4.1 nav item 5 |
| **Pilots in Development** | `/proof` — Proof cards with honest badges | §4.1 nav item 5; §4.2 item 7 |
| **Policy** | `/proof` — Policy cards; `/industries` Gov tile cross-link | §4.1 nav item 5 |
| **Get in Touch / CTA** | `/get-in-touch` — Contact + Book a Discovery Call | §4.1 nav item 6 |
| **Footer (all pages)** | Footer — Lilongwe, Malawi; See Our Research; Social links; LightSpeed Holdings Limited™ | §4.1 footer |

---

# Appendix B — Source & Provenance List

Every factual claim in this document traces to one or more authoritative source files. This appendix provides the mapping by section. Inline file:line citations are deliberately omitted from body copy to keep it clean for website incorporation.

| Section | Primary Sources | Notes |
|---------|----------------|-------|
| **Positioning** | `docs/superpowers/specs/2026-09-06-lightspeed-website-design.md:1-34` (positioning, tagline, honesty constraint); `docs/source-of-truth.yaml:35-47` (144 agents canonical); `docs/source-of-truth.yaml:19-33` (20 departments canonical); `docs/AGENT-REGISTRY-TABLE.md:4` | 144 agents / 20 departments = canonical counts |
| **The Method** | `docs/archive/2026-08-11-pre-restructure/reports/future-of-work-report.md:43-80` (HITL, audit trails, memory); `docs/legal/client-onboarding-policy.md:19-25` (G1–G4 gates); `config/decision/risk_matrix.yaml:1-30` (5×5 risk matrix); `config/decision/approval_matrix.yaml:1-270` (25+ risk-gated actions); `docs/CEO-DIRECTIVE-BLUEPRINT-ADOPTION.md:93-100` (governance cadence); `docs/source-of-truth.yaml:87-96` (9 LLM providers) | |
| **Offer A** | `docs/service-catalog-malawi.md:32-42` (deliverables, pricing, targets); `config/company/malawi_offers.yaml:15-16` (approval status); `docs/legal/client-onboarding-policy.md:35` (governance approval) | Fieldable 2026; governance approved |
| **Offer B** | `docs/service-catalog-malawi.md:44-53` (deliverables, pricing); `config/company/malawi_offers.yaml:25` (risk assessment); `docs/legal/client-onboarding-policy.md:36` (BLOCKED — WhatsApp data + cross-border LLM) | BLOCKED — do not sell |
| **Offer C** | `docs/service-catalog-malawi.md:55-66` (deliverables, pricing); `docs/legal/client-onboarding-policy.md:37` (BLOCKED — donor data + liability cap); `docs/legal/client-onboarding-policy.md:49` (Tier-1 sensitive data handling) | BLOCKED — do not sell |
| **Offer D** | `docs/service-catalog-malawi.md:68-74` (deliverables, pricing); `config/company/malawi_offers.yaml:43` (low-risk commodity); `docs/legal/client-onboarding-policy.md:38` (minimal PII) | Fieldable 2026; low-risk |
| **Offer E** | `docs/service-catalog-malawi.md:76-83` (deliverables, pricing); `config/company/malawi_offers.yaml:52` (product ready); `docs/legal/client-onboarding-policy.md:39` (no client data handling) | Fieldable 2026; proven in-house |
| **Enterprise Line** | `docs/DEEP-DIVE-WEBUILD-AI.md:56-66` (missing modules, effort estimates); `docs/DEEP-DIVE-WEBUILD-AI.md:18-20` (consulting model) | All in active development; modules not built |
| **Industries (5 verticals)** | `docs/superpowers/specs/2026-09-06-lightspeed-website-design.md:163` (5 verticals); `docs/Pharos/case-study-pipeline.md:49-59` (sector targeting) | Positioning only; no active client deployments |
| **Company Scenarios (FOW-01..08)** | `docs/archive/2026-08-11-pre-restructure/reports/future-of-work-report.md:86-194` (all 8 use cases) | UNVERIFIED projections in source excluded from body copy |
| **J&S StopOver Bar** | `docs/Pharos/case-study-pipeline.md:7-28` (live proof, non-client) | Not a paid client; live proof |
| **Meta Case Study** | `docs/Pharos/case-study-pipeline.md:43-46` (143 AI agents + CEO, governance mapped) | Proven in-house |
| **Health/M&E Pilot** | `docs/Pharos/case-study-pipeline.md:31-34` (composing evidence) | HIGH risk — no confirmed partnership signed |
| **VSLA/SACCO Pilot** | `docs/Pharos/case-study-pipeline.md:37-40` (COMESA/IDEA seeking) | HIGH risk — no signed engagement |
| **Ministry of Agriculture — Farmer Advisory** | `docs/superpowers/specs/2026-09-06-lightspeed-website-design.md:164` (piloting listed) | MEDIUM risk — piloting |
| **Citizen-Inquiry Lighthouse** | `docs/Pharos/policy-drafts/national-ai-strategy-comments.md:62-63` (proposed) | HIGH risk — proposed, not launched |
| **Governance as Template** | `docs/Pharos/policy-drafts/national-ai-strategy-comments.md:46-47` (operates in production) | Proven in-house |
| **Capacity Building** | `docs/Pharos/policy-drafts/national-ai-strategy-comments.md:64-65` (MUBAS/UNIMA) | In active development |
| **SADC Framework** | `docs/Pharos/policy-drafts/sadc-agentic-ai-governance-framework.md` | In active development |
| **National AI Strategy** | `docs/Pharos/policy-drafts/national-ai-strategy-comments.md` | Published |
| **Website IA** | `docs/superpowers/specs/2026-09-06-lightspeed-website-design.md:122-166` (IA, nav, home sequence) | §4.1–4.2 |

---

*End of Use Case Catalog. All claims trace to real repository files. UNVERIFIED projections have been excluded. No fabricated metrics, testimonials, or client logos appear in this document. All honesty badges enforce the site spec's honesty ladder. Pricing is to be validated with prospects before publishing.*
