# CEO DIRECTIVE: CORPORATE BLUEPRINT ADOPTION & STRATEGIC GOVERNANCE

**Document ID:** DIR-CEO-2026-001
**Classification:** Board-Level — Confidential
**Effective Date:** August 20, 2026
**Status:** ACTIVE — Single Source of Truth
**Owner:** Human CEO, Light Speed Holdings, Inc.
**Approved By:** Human CEO (sole authority per Company Constitution §39–57)

---

## 1. FORMAL ADOPTION OF THE CORPORATE BLUEPRINT

### 1.1 Directive

Effective immediately, the following documents collectively constitute **The Corporate Blueprint** — the single governing source of truth for strategy, architecture, operations, and culture at Light Speed Holdings, Inc. All prior strategic documents, informal understandings, and ad hoc decisions are superseded.

| Component Document | Role in Blueprint | Authority |
|-------------------|-------------------|-----------|
| `docs/MISSION_AND_VISION.md` | Mission, Vision, Values, Strategic Pillars, Cultural DNA | **Foundational** — All decisions trace here |
| `docs/COMPANY-CONSTITUTION.md` | Principles, Decision Order, Escalation, Company Values | **Constitutional** — Governance framework |
| `docs/ORGANIZATION.md` | Org structure, roles, decision authority, communication patterns | **Structural** — Operating model |
| `config/company/malawi_offers.yaml` | Bifurcated Service Matrix (5 offers), pricing, risk, governance state | **Commercial** — Go-to-market & delivery |
| `docs/legal/client-onboarding-policy.md` | 4-Gate governance (G1–G4), offer-specific blocking rules | **Risk/Legal** — Client engagement gatekeeper |
| `docs/sop/sales-sop.md` | Pipeline, BANT, pricing tiers, escalation, KPIs | **Operational** — Revenue engine |
| `docs/PRODUCT-ROADMAP.md` | Phase 3–5 execution plan, milestones, risk assessments | **Execution** — Product delivery timeline |

### 1.2 Binding Effect

- **No agent, executive, or specialist may operate outside the Blueprint** without written CEO exception logged in the audit trail.
- **All new hires (human or AI) receive the Blueprint as Day 1 onboarding material.**
- **Quarterly Blueprint Refresh** (Section 4.3) is the only sanctioned amendment path.

---

## 2. STRATEGIC PRIORITIES: 90-DAY RECRUITMENT ROADMAP

Based on the Phase 3–5 Product Roadmap and Malawi Service Portfolio, I rank the 90-day recruitment/hiring priorities by **Strategic Impact × Execution Risk**:

### 2.1 Priority Matrix (Accelerate / Execute / Defer)

| Rank | Role / Capability | Strategic Impact | Execution Risk | Decision | Rationale |
|------|-------------------|------------------|----------------|----------|-----------|
| **1** | **Platform Licensing Sales Lead** (Offer E) | **Critical** — $USD, high-margin, software exists | **Low** — Product ready, devrel agents exist | **ACCELERATE** — Hire/activate Week 1–2. This is our 2026 breakout revenue line. |
| **2** | **BPA/Chatbot Delivery Lead** (Offer B) | **Critical** — NGO USD revenue, WhatsApp demand | **High** — Governance BLOCKED (G1–G4 + liability cap) | **EXECUTE WITH GATES** — Unblock G4 (Security Review) & Liability Cap ratification in parallel. Do not sell until unblocked. |
| **3** | **Data & Reporting Delivery Lead** (Offer C) | **High** — 10x consulting undercut, NGO stickiness | **High** — Donor data = Tier-1 sensitive, cross-border LLM consent | **EXECUTE WITH GATES** — Requires explicit donor data waiver workflow. Build compliance automation first. |
| **4** | **Marketing & Sales Module (Phase 3.1)** | **High** — Pipeline engine for all offers | **Medium** — Scope creep risk across 5 depts | **EXECUTE** — Strict sprint boundaries. Deferrable items marked "Could" stay deferred. |
| **5** | **Financial Analyst Specialist Agent** (Phase 4) | **Medium-High** — Cost tracking, ROI, budget enforcement | **Medium** — Tool permissions, model routing | **EXECUTE** — Sprint 4.1 (Weeks 9–12). Enables autonomous cost governance. |
| **6** | **DevOps Specialist Agent** (Phase 4) | **Medium** — CI/CD, infra provisioning automation | **Low** — Well-defined patterns | **EXECUTE** — Sprint 4.1. Reduces human ops burden. |
| **7** | **Compliance Officer Specialist Agent** (Phase 4) | **High** — Unblocks Offer B & C governance | **Medium** — Policy check, risk scan tools | **ACCELERATE** — Pull forward to Sprint 3.2 if possible. Directly unblocks revenue. |
| **8** | **Data Scientist Specialist Agent** (Phase 4) | **Medium** — Analytics, modeling for all depts | **Medium** — Cross-dept data dependencies | **EXECUTE** — Sprint 4.1. Depends on Phase 3 data models. |
| **9** | **Autonomous Coordination (Phase 5)** | **Strategic** — Self-governing AI company vision | **High** — Escalation storms, budget overruns, HITL overload | **DEFER TO PHASE 5** — Do not start until Phase 3–4 stable. Budget for Week 17+. |
| **10** | **Digital Presence (Offer A) & Marketing (Offer D)** | **Low-Medium** — Cash flow, brand | **Low** — Commodity, approved governance | **MAINTAIN** — Run as cash cows. No new hiring. Optimize margins. |

### 2.2 Immediate Actions (Week 1–2)

1. **Activate Platform Licensing Sales Lead** — Assign to `head-of-developer-relations` + `growth-product-manager` with CFO pricing authority.
2. **Ratify `service_level_liability_cap`** — CLO to finalize ToS Services Annex override; Board Chair to countersign. Target: **August 25, 2026**.
3. **Unblock Offer B Security Review** — CISO to complete threat model for WhatsApp data flows; Data Privacy Officer to draft cross-border LLM consent waiver. Target: **September 5, 2026**.
4. **Freeze non-revenue hiring** — All Phase 4 specialist agents proceed per roadmap; no new human roles without CEO sign-off.

---

## 3. DECISION RIGHTS MATRIX

Clarifying authority boundaries per Constitution §39–57 and escalation chains. **If unsure, escalate.**

| Decision Category | Decision Owner | Escalation Path | Notes |
|------------------|----------------|-----------------|-------|
| **Client Acceptance / Rejection** | `sales_lead` (≤$10K) → `cfo` + `ceo` (>$10K) | CEO final | Pricing exceptions **always** require CFO + CEO. Offer B/C require full G1–G4 gate pass. |
| **Pricing Deviations** | `cfo` (within tier bands) → `ceo` (outside bands) | CEO final | No public pricing commitment without CFO + CEO. Malawi MWK/USD mixed-currency requires CFO hedging sign-off. |
| **Technical Architecture Changes** | `cto` + `chief_of_staff` (dept-level) → `ceo` (cross-cutting) | CEO final | Changes to: MessageBus schema, ModelRouter tiers, AgentRegistry structure, Zero-Cloud Boundary. |
| **Data Sovereignty Interpretations** | `data_privacy_officer` + `ciso` → `clo` → `ceo` | CEO final | Malawi Data Protection Act 2017, GDPR, cross-border LLM transfer. **Zero tolerance for ambiguity** — document every interpretation. |
| **Governance Gate Overrides (G1–G4)** | **CEO ONLY** | N/A | No agent may bypass gates. Any gate failure = security incident per `client-onboarding-policy.md` §5. |
| **Budget Allocation (>$100)** | `cfo` | CEO >$10K | First $500K guardrails in Section 7. |
| **Agent Hiring / Firing / Permission Changes** | `human_ceo` only | N/A | Per Constitution §56–57. CTO reviews config for security; Lead Engineer generates files. |
| **MSA/NDA Terms (Governing Law: Malawi)** | `clo` drafts → `ceo` approves | CEO final | All client contracts governed by Malawi law. No jurisdiction shopping. |
| **Strategic Pivots / New Offers** | `ceo` + `board_chair` | Board ratification | Requires written proposal, impact assessment, 7-day review (Constitution §86–91). |

### 3.1 Decision Log Requirement

Every decision at **CFO level and above** must be logged in `audit/decisions.jsonl` with:
- Decision ID, timestamp, owner
- Options considered, rationale
- Escalation trail (if any)
- Blueprint section referenced

---

## 4. GOVERNANCE CADENCE

### 4.1 Board-Level Review Schedule

| Cadence | Forum | Participants | Agenda | Output |
|---------|-------|--------------|--------|--------|
| **Weekly** | CEO + Chief of Staff Standup | CEO, CoS | Tactical: blockers, escalations, gate status, cash position | Action items, escalation resolutions |
| **Bi-Weekly** | Product Roadmap Review | CEO, CoS, CPO, CTO | Phase 3–5 milestone tracking, risk burn-down | Sprint adjustments, resource reallocation |
| **Monthly** | **Monthly Business Review (MBR)** | CEO, CoS, CFO, CTO, CLO, CMO, CSO, Board Chair | Revenue vs. target, pipeline health, governance gate status, compliance, capital deployment | MBR memo to Board; go/no-go on offers |
| **Quarterly** | **Quarterly Strategy Pivot Review** | CEO, Board (all 7 committees) | Strategic pillar progress, market shifts, competitive landscape, Blueprint amendment proposals | Strategy pivot decisions; Blueprint amendments ratified |
| **Annually** | **Annual Blueprint Refresh** | CEO, Board, all executives | Full Blueprint re-validation: mission relevance, org design, service matrix, pricing, risk appetite | Blueprint vNext published; Constitution amendments if needed |

### 4.2 Governance Artifacts

| Artifact | Owner | Cadence | Location |
|----------|-------|---------|----------|
| MBR Memo | CoS | Monthly | `board/mbr/YYYY-MM.md` |
| Quarterly Strategy Memo | CSO | Quarterly | `board/strategy/quarterly-YYYY-QN.md` |
| Annual Blueprint Refresh | CEO | Annual | `docs/BLUEPRINT-vN.md` (archived versions retained) |
| Governance Gate Status Dashboard | `data_privacy_officer` + `ciso` | Real-time | CEO Dashboard `/governance` panel |

### 4.3 Escalation SLAs (Per Constitution §73)

- **P0 (Business-critical / irreversible):** Acknowledged ≤15 min, CEO decision ≤2 hrs
- **P1 (Cross-department / revenue-impacting):** Acknowledged ≤1 hr, CoS resolution ≤4 hrs
- **P2 (Department-level):** Acknowledged ≤4 hrs, Executive resolution ≤24 hrs
- **P3 (Task-level):** Specialist resolution per SOP SLA

---

## 5. CULTURE & VALUES: BEHAVIORAL EXPECTATIONS

Translating **"Offline-First, Localization-Heavy, Infrastructure-Resilient"** into 5 non-negotiable behavioral expectations for **every hire (human or AI)**:

### 5.1 The Five Behaviors

| # | Behavior | Blueprint Anchor | What "Good" Looks Like | What "Bad" Looks Like |
|---|----------|------------------|------------------------|------------------------|
| **1** | **Default to Local-First Execution** | Offline-First / Zero-Cloud Boundary | Agent runs fully on-prem; data never leaves client boundary without explicit consent; LLM routing prefers local/edge. | Shipping cloud-dependent features without local fallback; assuming connectivity. |
| **2** | **Build for the Hardest Jurisdiction First** | Localization-Heavy / Malawi DPA 2017 | Every feature designed for Malawi data sovereignty, GDPR, cross-border consent from Day 1. | "We'll add compliance later" — retrofitting costs 10x. |
| **3** | **Resilience Over Convenience** | Infrastructure-Resilient | Idempotent builds, deterministic deployments, self-healing retries, chaos-tested failure modes. | Happy-path only; manual runbooks; single points of failure. |
| **4** | **Evidence Over Opinion, Always** | Constitution §12–16 | Decisions logged with data; assumptions explicit and time-boxed for validation. | HiPPO-driven; undocumented "tribal knowledge"; unvalidated hypotheses in production. |
| **5** | **Own the Outcome, Not the Output** | Constitution §37–38 | Specialist owns client success metric, not just task completion; escalates early when outcome at risk. | "I shipped the code" without verifying it solved the customer problem. |

### 5.2 Hiring & Promotion Filter

**Every candidate (human or agent spec) is evaluated against these 5 behaviors.** No exceptions.

- **Interview questions** must probe each behavior with concrete scenarios.
- **Performance reviews** weight behaviors 50%, technical delivery 50%.
- **Agent spec cards** must include `behavioral_expectations` field mapping to the 5.

---

## 6. EXTERNAL SIGNALING: MARKET NARRATIVE

The Blueprint shapes how we show up in the market. **Consistency is the strategy.**

### 6.1 Narrative Pillars (Derived from Blueprint)

| Pillar | Message | Proof Points | Channels |
|--------|---------|--------------|----------|
| **"AI Companies That Run Themselves — Governed by Humans"** | We don't sell agents; we sell self-governing AI organizations with human oversight at every critical decision. | 135-agent hierarchy, 5-tier HITL, Constitution decision order | Website hero, pitch decks, keynote |
| **"Offline-First. Sovereign by Design."** | Your data, your models, your jurisdiction. We deploy where you operate — not where we want you to. | Zero-Cloud Boundary, Malawi DPA 2017 compliance, local LLM support | Technical blog, security whitepaper, partner convos |
| **"10x the Consulting Model"** | We deliver NGO reporting, chatbot automation, data services at 1/10th the cost of traditional firms — with audit trails. | Offer B/C pricing, governance gates, SLA-backed delivery | Case studies, ROI calculators, NGO partner testimonials |
| **"Platform Licensing: The AI Company Builder in Your Hands"** | The same engine that runs us runs you. White-label, self-hosted, extensible. | Offer E, Phase 3–5 roadmap, developer experience | DevRel content, OSS components, hackathons |

### 6.2 Channel-Specific Guidance

| Channel | Blueprint Alignment | Guardrails |
|---------|---------------------|------------|
| **Website** | Live governance gate status for Offer B/C; transparent pricing tiers; Malawi DPA badge | No vaporware — only shipped features. Update quarterly with Blueprint Refresh. |
| **Pitch Decks** | Lead with Mission & Vision; anchor in Constitution principles; show org chart as differentiator | No revenue projections without CFO sign-off. No architecture claims without CTO validation. |
| **Thought Leadership** | CEO/CoS publish on: AI governance, data sovereignty, offline-first architecture | All content reviewed by CLO for compliance; CISO for security claims. |
| **Partner Conversations** | Position as infrastructure layer, not app competitor. "We power your AI agents." | No data sharing agreements without DPA. No joint go-to-market without CEO approval. |

---

## 7. CAPITAL ALLOCATION GUIDANCE: FIRST $500K OPERATIONAL SPEND

Guardrails for the first $500K across four pillars. **Any single line item >$25K requires CEO approval.** CFO tracks weekly; CoS reports at MBR.

### 7.1 Allocation Framework

| Pillar | Budget Range | Priority Investments | Guardrails |
|--------|--------------|---------------------|------------|
| **Hardware Lab** | **$75K–$125K** (15–25%) | • On-prem GPU cluster (2× H100 or 4× A100) for local LLM inference<br>• Edge devices for offline-first testing (Jetson Orin, RPi 5 clusters)<br>• Network simulation gear (latency, partition, bandwidth)<br>• Malawi-field-test kit (ruggedized laptops, solar backup) | **No cloud GPU spend** — this lab IS our offline-first proof. CapEx only; no recurring cloud bills. |
| **Talent** | **$200K–$250K** (40–50%) | • Platform Licensing Sales Lead (Offer E) — **Priority 1**<br>• BPA/Chatbot Delivery Lead (Offer B) — **Priority 2**<br>• Compliance Officer (human or agent) — **Priority 3**<br>• DevRel Engineer (Offer E enablement) | **No full-time hires without 90-day ROI model.** Contract-to-hire preferred. Agent specialists (Phase 4) funded from dev budget, not talent budget. |
| **Client Pilots** | **$100K–$150K** (20–30%) | • 3× Offer A pilots (digital presence) — cash flow, referenceable<br>• 1× Offer B pilot (NGO chatbot) — **only after G1–G4 + liability cap ratified**<br>• 1× Offer C pilot (NGO reporting) — **only after donor data waiver workflow live**<br>• Pilot success metrics: NPS ≥4.5, Time-to-Value <2 weeks, Zero governance violations | **Pilot budgets capped at $25K each.** Overrun = auto-escalation to CEO. No pilot without signed MSA + DPA. |
| **Compliance / Legal** | **$50K–$75K** (10–15%) | • Malawi legal counsel retainer (DPA 2017, corporate)<br>• GDPR / cross-border transfer legal opinion<br>• SOC 2 Type II readiness (audit prep, not full audit)<br>• Liability cap insurance rider (Offer B/C unblocking) | **Fixed-fee engagements only.** No open-ended hourly. CLO manages vendor; CEO approves retainer. |

### 7.2 Spend Controls

1. **Weekly Cash Position Report** — CFO to CEO + CoS every Monday 09:00.
2. **Monthly Budget vs. Actual** — MBR agenda item. Variance >10% = explanation required.
3. **Quarterly Re-forecast** — QStrategy Review adjusts allocations for next quarter.
4. **Emergency Reserve** — $50K held in reserve; CEO-only release for: security incident, regulatory action, critical talent retention.

---

## 8. IMMEDIATE NEXT STEPS (CEO ACTION ITEMS)

| # | Action | Owner | Deadline | Evidence |
|---|--------|-------|----------|----------|
| 1 | Publish this Directive to all agents via MessageBus broadcast | CoS | **Aug 21, 2026** | Task ID in inbox |
| 2 | Ratify `service_level_liability_cap` in `malawi_offers.yaml` | CLO + Board Chair | **Aug 25, 2026** | YAML commit + Board minutes |
| 3 | Complete Offer B Security Review threat model | CISO | **Sep 5, 2026** | `legal/clients/<pilot>/security-review.md` |
| 4 | Draft donor data cross-border consent waiver (Offer C) | Data Privacy Officer | **Sep 5, 2026** | `legal/templates/donor-data-waiver.md` |
| 5 | Activate Platform Licensing Sales Lead | CMO + CPO | **Aug 22, 2026** | Agent spec card deployed |
| 6 | Freeze non-revenue hiring; communicate to HR | CEO | **Aug 21, 2026** | Slack + MessageBus broadcast |
| 7 | Schedule Q3 Quarterly Strategy Pivot Review | CoS | **Sep 15, 2026** | Calendar invite + pre-read |
| 8 | Wire Governance Gate Status to CEO Dashboard | CTO + Data Privacy Officer | **Aug 29, 2026** | Dashboard `/governance` panel live |

---

## 9. CLOSING

This Directive is **effective immediately** and **binding on all agents, executives, and human operators** within Light Speed Holdings.

The Corporate Blueprint is not a static document — it is our **operating contract with reality**. We will measure ourselves against it weekly, challenge it quarterly, and rebuild it annually. But between now and the next refresh, **it is the law**.

Every decision we make must trace to a Blueprint section. Every hire must embody the Five Behaviors. Every dollar must serve the Strategic Pillars. Every client engagement must pass the Four Gates.

**We build AI companies that run themselves — governed by humans. This is how we govern ourselves.**

---

**Signed:**

> **Human CEO**
> Light Speed Holdings, Inc.
> August 20, 2026

**Countersigned (Acknowledgement):**

> **Chief of Staff** — *Operational coordination authority confirmed*
>
> **Board Chair** — *Governance cadence ratified*

---

### Distribution

| Role | Channel | Acknowledgment Required |
|------|---------|------------------------|
| All Executives (CTO, CFO, CLO, CMO, CSO, COO, CAIO, CISO, CPO, CDO, CIO) | MessageBus `broadcast:executives` | Yes — reply "ACK DIR-CEO-2026-001" |
| All Department Heads | MessageBus `broadcast:dept-heads` | Yes |
| All Specialist Agents | Registry auto-distribution | Implicit (task execution) |
| Board of Directors | Secure email + board portal | Yes — formal minute |
| Human Operator (CEO) | This document | N/A (originator) |

---

### Version Control

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-08-20 | Human CEO | Initial adoption directive |

*Next review: Quarterly Strategy Pivot (September 15, 2026)*
*Next refresh: Annual Blueprint Refresh (Q1 2027)*
