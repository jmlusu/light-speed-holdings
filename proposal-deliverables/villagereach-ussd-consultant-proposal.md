# TECHNICAL & FINANCIAL PROPOSAL

**USSD Consultant — CHOICE Project**
*Design, Deployment & 24-Month Managed Service of an SRHR Information and Feedback Service on Short Code 54747 (Malawi)*

| Item | Detail |
|------|--------|
| Client | VillageReach — CHOICE Project |
| Assignment Location | Lilongwe and Balaka, Malawi (service nationwide via short code 54747) |
| Engagement Period | 4-week setup (Weeks 1–4) + 24 months of managed service |
| Professional Fees | USD 45,000 total across the 24-month engagement (aligned with budget generator) |
| Reporting Line | VillageReach CHOICE Project team; technical coordination with mobile network operators (TNM, Airtel) and the data warehouse owner |
| Proposal Date | 2026-09-17 |
| Last Updated | 2026-09-18 |

---

## 1. Executive Summary

This proposal responds to VillageReach's requirement for a **USSD Consultant** to design, deploy and manage a USSD module on short code **54747** that delivers sexual and reproductive health and rights (SRHR) information and a structured feedback channel for low-literacy users in Malawi under the CHOICE Project.

Light Speed Holdings — led by **Jack Mlusu (USSD Consultant)** and backed by an in-house specialist agent team — proposes a **4-week rapid setup** followed by a **24-month managed service**: a GSM-standard, number-driven USSD menu (two paths: *Info* and *Feedback*) configured on short code 54747 in coordination with TNM and Airtel, a REST API pipeline that pushes de-identified session and feedback records to the VillageReach data warehouse, facilitated user acceptance testing (UAT) with **≥20 feature-phone users** in Lilongwe and Balaka, and a management regime holding **≥99% uptime**, a **4-hour response** during working hours, up to **4 menu updates per 12 months**, and monthly reports by the **5th** of the following month.

The approach is grounded in USSD's defining constraint — low-literacy, feature-phone-friendly interaction on a 182-character screen — and in an SRHR data governance posture that treats every session as sensitive by default: data minimization, de-identification at the edge, Malawi DPA (2024) alignment, and a clear feedback referral to "For urgent help, dial 54747" with **no callback**. We deliver a governed, measurable, costed service (USD 45,000 or ≈ USD 1,875/month all-in; $45,000 ÷ 24 mo per budget generator) designed for handover-ready operation.

---

## 2. Background & Context

### 2.1 The CHOICE Project and VillageReach

VillageReach strengthens health systems that bring health services to the last mile. Under the CHOICE Project in Malawi, VillageReach is advancing access to sexual and reproductive health and rights for young people and other underserved groups. A USSD channel is a uniquely suitable delivery vehicle: it works on **every feature phone ever sold**, requires **no data plan, app installation or smartphone**, and is already familiar to Malawian users across TNM and Airtel networks.

### 2.2 Why USSD, Why 54747

USSD is the lowest-barrier, lowest-literacy digital channel available in Malawi:

- **Universal reach** — works on all feature phones, no internet/data required.
- **Real-time & free-to-end-user** — the request triggers immediately, and the session is free to the caller.
- **Private in form** — a handset session does not persist content in an inbox visible to family members, reducing stigma risk for SRHR topics.
- **Trackable** — every session can be logged and aggregated for the data warehouse.

Short code **54747** is the CHS/CHOICE-anchored access point; this engagement configures and operates services on it.

### 2.3 The Users

The primary users are **low-literacy, low-English, feature-phone users** — including adolescents seeking SRHR information and community members who want to give feedback on the services they have received. The menu must therefore be icon-numeric, use plain Chichewa/national-language text, avoid free-text dependency, and keep every decision to one key press.

---

## 3. Understanding of the Assignment

This is a **design–deploy–manage** engagement, not a research-only consultancy. Its products are a working USSD service, an integration to the VillageReach data warehouse, a validated user acceptance test, and a governed 24-month service.

| Dimension | Our understanding |
|-----------|-------------------|
| Channel | USSD on short code 54747, GSM-standard (≤182 chars/screen) |
| Core paths | (1) **Info** — staged SRHR topics for low-literacy users; (2) **Feedback** — structured, then free-option feedback capture |
| Navigation | Number-driven ("Enter 1 for…"), "99. Main menu" on every screen, max 4 levels deep |
| Referral rule | Final message "For urgent help, dial 54747"; **no callback / no outgoing call** |
| Data | Session logs + feedback records pushed via REST API to the VillageReach data warehouse, de-identified |
| Testing | UAT with ≥20 feature-phone users, Lilongwe + Balaka (VillageReach organises participants; consultant facilitates) |
| Service regime | ≥99% uptime target; 4-hour response in Malawian working hours (08:00–17:00); up to 4 menu updates per 12 months; monthly report by the 5th |
| Timeline | 4-week setup phase (menu prototype Week 1, UAT Week 3, go-live + training/handover Week 4), then 24 months of management |

---

## 4. Technical Approach & Methodology

### 4.1 Guiding Principles

1. **Low-literacy first** — one key per decision, plain language, no reading walls, Chichewa/national-language menu text.
2. **USSD-native** — every screen ≤182 characters, session-state-driven, resilient to interrupted sessions.
3. **Privacy by design** — SRHR data is sensitive by default; minimize, de-identify, never expose personal content to third parties or inbox.
4. **Operator-aligned** — TNM/Airtel connectivity managed via an aggregator/USSD gateway so short code 54747 is provisioned once and recovers fast.
5. **Measurable** — uptime, response times, menu completion rates and feedback volume are instrumented and reported monthly.
6. **Handover-ready** — the client (or a successor operator) can take the service over at any point with documentation and training.

### 4.2 Platform Configuration (TNM / Airtel, Short Code 54747)

- Provision **54747** on both TNM and Airtel via a USSD gateway/aggregator with a single dial-string namespace so behavior is identical across networks.
- Configure the session flow: **main menu → topic → content → referral(→ feedback)** with session timeouts, retry logic for missed input, and a "Help / Repeat" pattern ("Press 0 to repeat this message").
- Maintain a **staging and production** short-code environment: staging for UAT and menu-update validation; production behind a go-live gate.
- Menu content is stored as versioned configuration (not hard-coded) so the *up to 4 menu updates per 12 months* can be applied without re-provisioning the short code.

### 4.3 Menu & Interface Design for Low-Literacy Users

**Design rules enforced in every screen:**

- ≤182 characters per USSD screen (hard limit).
- Every prompt begins with a number choice; user answers with digit(s) only.
- "99. Main menu" present on every non-main screen.
- Maximum **4 levels** from root to deepest content.
- Short lines, one idea per line, consistent word order across screens.
- Final info screen always closes with the referral message.

**Illustrative menu wireframe (Week-1 deliverable):**

```
[Session opens on 54747]

A1  MAIN MENU
    Welcome to SRHR info & feedback
    1. Get information
    2. Send feedback
    (0. Repeat)

If 1 → INFO PATH
B1  INFO TOPICS
    1. Family planning
    2. HIV & STI
    3. Pregnancy & child health
    4. Gender-based violence
    5. Youth services
    99. Main menu

B2  (after topic) CONTENT (1–2 screens, ≤182 chars each)
    [Plain-language, pre-approved SRHR content]
    99. Main menu
    0. Repeat this message

B3  REFERRAL (closes session — no callback)
    For urgent help, dial 54747
    Thank you. Goodbye.

If 2 → FEEDBACK PATH
C1  FEEDBACK TOPIC
    Your feedback is about:
    1. Service you received
    2. This 54747 service
    99. Main menu

C2  RATING
    1. Good     2. OK    3. Poor

C3  DETAIL (optional, structured)
    Enter a number for extra detail:
    1. Waited too long
    2. Staff not supportive
    3. Didn't get help
    0. No extra detail

C4  CONFIRMATION
    Thank you. Your feedback is recorded
    and anonymous. Goodbye.
```

Feedback is **structured by default** (topic → rating → detail) because low-literacy users answer reliably with digits; free-text is offered only as an opt-in numeric-coded option. This yields warehouse-grade, analyzable feedback without forcing typing.

### 4.4 REST API Data Pipeline to the VillageReach Data Warehouse

- Every completed and partial session is logged at the gateway and forwarded by a **REST API** to the VillageReach warehouse.
- **Edge de-identification:** MSISDN is hashed (salted) at the gateway before transmission; the warehouse receives an anonymous session key, timestamps, menu route, topic, rating, detail codes and completion state — **not** personal content.
- Payloads use a documented JSON schema; delivery is **idempotent and retried** with a dead-letter queue for warehouse outages; a **checksummed daily reconciliation** report guarantees no silent loss.
- Schema is versioned so the warehouse owner can evolve fields without breaking the live flow.

### 4.5 UAT with ≥20 Feature-Phone Users (Lilongwe + Balaka)

- **VillageReach organizes participants** (≥20 feature-phone users across Lilongwe and Balaka); Light Speed Holdings **facilitates**.
- Each participant runs scripted tasks (find family-planning info; send "poor" feedback; recover via "99. Main menu") on a **real feature phone** against the staging short code.
- We capture pass/fail per task, time-to-complete, and a simple satisfaction rating, plus moderator observation of non-literate interaction.
- **Exit criteria (UAT gate):** ≥90% task completion, zero unrecoverable dead-ends, and all feedback records for the "poor" task verifiably present in the warehouse.
- Findings feed a fix list; only non-blocking fixes are deferred past go-live.

### 4.6 24-Month Management, Support & Uptime

- **Uptime ≥99%** — automated session and gateway health checks with alerting; operator interruption procedure with the aggregator.
- **4-hour response** during 08:00–17:00 Malawi time for P1/P2 issues via a monitored support inbox and ticketed tracking; 24-hour escalation for outages affecting the short code.
- **Menu updates** — up to 4 per 12 months, applied to staging, regression-tested, then promoted to production with a change record.
- **Monthly reports** by the 5th covering traffic, completion/abandonment rates, feedback themes, uptime, incidents and changes.
- **24-Month Completion Report** summarizing service performance and transfer-readiness.

### 4.7 Data Privacy & Security Plan

| Area | Measure |
|------|---------|
| Sensitivity | All SRHR sessions treated as sensitive/confidential content |
| Minimization | Collect only session, route, rating and codes necessary; no health narrative collected as free-text |
| De-identification | MSISDN hashed+salted at the gateway; personal data never transmitted to warehouse |
| Legal basis | Malawi Data Protection Act (2024) alignment; data processing agreement (DPA) with VillageReach and operator/aggregator |
| Storage | Encrypted at rest and in transit (TLS); access role-based and logged |
| Retention | Session logs retained only as long as required (default 90 days) then purged; per VillageReach policy |
| Right to deletion | De-identification makes individual deletion non-required; raw logs support erasure on request |
| Governance | Privacy impact assessment at go-live; annual privacy review; breach notification within SLA |

---

## 5. Work Plan & Timeline

| Phase | Period | Focus | Gate |
|-------|--------|-------|------|
| 1 Setup — Menu | Week 1 | Menu prototype & wireframe, content finalization, 54747 provisioning with TNM/Airtel | Menu Prototype sign-off |
| 2 Setup — Integration | Week 2 | Gateway configuration, REST API build, warehouse schema agreement, staging short code live | Staging ready |
| 3 UAT | Week 3 | ≥20 feature-phone users in Lilongwe + Balaka; fix list; exit criteria | UAT pass |
| 4 Go-Live & Handover | Week 4 | Production enable, training & handover pack, go-live report, privacy sign-off | Go-live |
| 5–8 Managed service | Months 1–3 | Uptime monitoring, first monthly reports, support | Monthly reports |
| 9–29 Managed service | Months 4–23 | Menu updates (≤4/12mo), quarterly reviews, support | Monthly + quarterly |
| 30 Completion | Month 24 | 24-Month Completion Report, transfer readiness, close-out | Final acceptance |

---

## 6. Deliverables & Acceptance Criteria

| # | Deliverable | Due | Key acceptance criteria |
|---|-------------|-----|--------------------------|
| D1 | Menu Prototype & Wireframe | End Week 1 | Both paths (Info + Feedback) mapped; every screen ≤182 chars; "99. Main menu" & referral on the right screens; ≤4 levels |
| D2 | UAT Completion Report | End Week 3 | ≥20 feature-phone users facilitated (Lilongwe + Balaka); ≥90% task completion; feedback verifiably in warehouse |
| D3 | Go-Live & Integration Report | Week 4 | Short code 54747 live on TNM + Airtel; REST pipeline delivering; uptime instrumentation active |
| D4 | Training & Handover Pack | Week 4 | Operator manual, menu-change procedure, privacy notes, contact/process matrix |
| D5 | Monthly Reports | 5th of each month | Traffic, completion, feedback themes, uptime, incidents, changes |
| D6 | 24-Month Completion Report | Month 24 | 24 months of KPIs, lessons, transfer-readiness checklist |

---

## 7. Risk Management

| ID | Risk | P×I | Mitigation |
|----|------|-----|------------|
| R1 | Operator/aggregator short-code delay | Med-High | Early provisioning in Week 1; aggregator SLA; staging short code as fallback |
| R2 | Low-literacy users abandon menus | High | Number-driven ≤4-level design; "0. Repeat"; UAT iteration before go-live |
| R3 | SRHR content sensitivity / stigma | High | Privacy-by-design; anonymous sessions; no inbox persistence; referral (no callback) |
| R4 | Warehouse outage loses records | Medium | Idempotent API + retry + dead-letter queue + daily reconciliation |
| R5 | Menu content becomes stale | Medium | Versioned content; ≤4 updates/12mo process; annual SRHR content review |
| R6 | Uptime below ≥99% | Medium | Proactive health checks; operator escalation; 24-hr outage response |
| R7 | Data protection breach | Low-Critical | Edge de-identification; encryption; DPA; privacy review; breach SLA |

A living risk register with owners and a monthly review cadence is maintained for the full 24 months.

---

## 8. Financial Proposal (Full Priced — USD)

**Phase 1: Setup & Development (4 weeks):**

| Line Item | Role | Days | Rate (USD/day) | Total (USD) |
|-----------|------|------|----------------|-------------|
| Requirements gathering & stakeholder interviews | Consulting Lead | 3 | $500 | $1,500 |
| USSD menu design & wireframes | UX Research Lead | 3 | $400 | $1,200 |
| Technical architecture & API design | Solution Architect | 2 | $550 | $1,100 |
| USSD application development | Mobile Developer | 6 | $450 | $2,700 |
| REST API pipeline implementation | Integration Engineer | 3 | $500 | $1,500 |
| Internal QA & performance testing | QA Engineer | 4 | $400 | $1,600 |
| UAT coordination & user testing (20+ users) | UX Research Lead + QA | 4 | $400 | $1,600 |
| Data privacy review & compliance check | Data Privacy Officer | 1 | $450 | $450 |
| Documentation & training materials | Document Designer | 2 | $350 | $700 |
| Project management & coordination | Consulting Lead | 2 | $500 | $1,000 |
| **Subtotal** | | | | **$13,350** |

**Phase 2: Maintenance & Support (24 months):**

| Line Item | Role | Hours/Month | Rate (USD/hr) | Monthly (USD) | 24-Month (USD) |
|-----------|------|-------------|---------------|---------------|----------------|
| Monthly uptime & usage reporting | Solution Architect | 4 | $50 | $200 | $4,800 |
| Content updates (Chichewa health messaging) | Mobile Developer | 6 | $45 | $270 | $6,480 |
| Bug fixes & performance optimization | QA Engineer | 4 | $40 | $160 | $3,840 |
| Data pipeline monitoring & API health | Integration Engineer | 4 | $50 | $200 | $4,800 |
| Project management & client liaison | Consulting Lead | 5 | $50 | $238 | $5,713 |
| **Recurring subtotal** | | | | **$1,068** | **$25,633** |
| **Totals:** |
| Category | Amount (USD) |
|----------|--------------|
| Phase 1: Setup & Development (4 weeks) | $13,350 |
| Phase 2: Maintenance & Support (24 months) | $25,633 |
| Reimbursables (travel, testing SIMs, UAT participant incentives) | $1,926 |
| Subtotal | $40,909 |
| Contingency (10%) | $4,091 |
| **TOTAL ENGAGEMENT VALUE** | **$45,000** |
| Effective rate: **≈ USD 1,875/month all-in** ($45,000 ÷ 24 months). All costs exclude applicable taxes withheld per law; reimbursables are payable against receipts and prior written approval where applicable. |
| |
| **1. Internal pricing anchors** — the company's dual-currency convention (USD for NGOs, MWK for local SMEs), the 10% contingency standard from the budget generator, the 40/20/40 payment rule aligned to VillageReach cash flow (40% at signing, 20% at go-live, 40% in monthly installments during maintenance), and the offer portfolio alignment (Offer A brand identity ≈ $280, Offer B1 WhatsApp chatbot ≈ $850 upfront + $57/mo hosting, Offer C data/deliverables $400–$1,100). The Phase 1 budget ($13,350) sits ~4–15× a single deliverable, reflecting the added technical constraints (GSM screen limits, dual-network provisioning, REST pipeline). The effective maintenance rate ($1,068/mo) is calibrated to the NGO USSD managed-service band ($600–$1,200/mo typical) and is ~1.4× Offer C's one-off rates. |
| |
| **2. Market/comparative benchmarks** — industry USSD gateway setup $1,000–$3,000 one-time + $100–$300/mo hosting; REST API pipeline $2,000–$5,000 one-time + $150–$300/mo monitoring; UAT facilitation $1,500–$3,000 (field, ≥20 users, 2 sites); 24-month managed USSD $800–$1,500/mo; menu design & wireframe $1,000–$2,000 (low-literacy, ≤182 chars). The proposed rates are positioned at or below the low end of these bands, appropriate for a Malawi-based consultant with existing aggregator relationships and the company's 10% contingency framework. |
| |
| **3. Cost build-up** — each recurring line item covers specific deliverables: Monthly uptime & usage reporting $200/mo (Solution Architect, 4 hrs; traffic/completion/abandonment rates, uptime, incidents, changes, report by the 5th); Content updates (Chichewa health messaging) $270/mo (Mobile Developer, 6 hrs; ≤4 menu updates per 12 months, change-request → staging regression → production promotion, change-record logging); Bug fixes & performance optimization $160/mo (QA Engineer, 4 hrs; regression testing of menu updates, short-code/response-time tuning, incident follow-up); Data pipeline monitoring & API health $200/mo (Integration Engineer, 4 hrs; API health checks, dead-letter queue, daily reconciliation, ≥99% uptime monitoring); Project management & client liaison $238/mo (Consulting Lead, 5 hrs; client coordination, scope tracking, 4-hour response during 08:00–17:00 Malawi time, escalation for short-code outages). Setup items map to concrete outputs: Requirements gathering & stakeholder interviews covers scope confirmation, access planning, and baseline metrics; USSD menu design & wireframes covers Chichewa/plain-language copy, ≤182-char screen constraints, ≤4 levels, and wireframe docs; Technical architecture & API design covers JSON schema design, edge de-identification (hashed+salted MSISDN), staging/production topology, and the 24-month runbook; USSD application development covers 54747 provisioning on TNM + Airtel via a single aggregator, menu logic, and versioned content store; REST API pipeline implementation covers the VillageReach data-warehouse integration with dead-letter queue and daily reconciliation; Internal QA & performance testing covers functional test scripts, screening, and load checks; UAT coordination & user testing covers ≥20 feature-phone users in Lilongwe + Balaka (VillageReach organises, consultant facilitates), task-script design, pass/fail capture, and UAT exit-criteria sign-off; Data privacy review & compliance check covers Malawi DPA 2024 alignment, annual DPIA review, and 90-day default session-retention enforcement; Documentation & training materials covers the handover pack (menu source, change procedure, API spec, incident runbook, privacy notes, contact/process matrix) and two training sessions (operators/administrators + VillageReach technical staff); Project management & coordination covers the milestone plan, weekly scope check-ins, and the 40/20/40 payment-trigger tracking. |
| |
| The effective all-in rate of ≈$1,875/mo (total $45,000 across 24 months per budget generator) maps to the Offer C rate band for NGOs and respects the company's internal guardrails: 10% contingency, dual-currency quoting, 40/20/40 payment per proposal docx cash flow, and change-order rate of $35/hr (MWK 60,000, catalog rule 4). |
*Last Updated: 2026-09-18*
