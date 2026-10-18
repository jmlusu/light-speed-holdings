# REA Reverse-Engineering Services — BD Pitch One-Pager & Internal Playbook

**Date:** 2026-10-17
**Owner:** head-of-business-development (reports-to: chief_of_staff)
**Status:** DRAFT — PART A must not be distributed until CFO + CEO ratify the indicative bands (per CEO directive: no public pricing without CFO + CEO)
**Sources:** `reports/rea-feasibility/06-client-offerings.md` (R1–R6 catalog, gates), `04-market-landscape.md` (sectors, positioning), `05-financial-model.md` (DIRECTIONAL price bands), `01-legal-compliance.md` (authorization, clean-room), `FEASIBILITY-STUDY.md` (verdict)

---

# PART A — FOR CLIENT DISTRIBUTION

*Draft body copy for the client-facing one-pager. Distribution requires CFO + CEO sign-off on the indicative bands.*

---

## Software answers, with evidence — not speculation

**Lightspeed's reverse-engineering service analyzes the software artifacts you own or are authorized to inspect — and hands you findings you can take to a board, an auditor, or a regulator.**

Every engagement runs on sovereign infrastructure. Your binaries, exports, and firmware images do not get uploaded to offshore scanning services. Every finding ships with a reproducible evidence record: what was analyzed, how, and with which tool versions — so any conclusion can be independently checked.

### The problem this solves, in your sector

- **Financial services & fintech:** The payment SDK or mobile-money app you are about to renew — or acquire — is a black box. Marketing claims say "bank-grade encryption" and "works offline." Before you sign a multi-year contract or close a deal, you need claims tested against the actual binary, not the sales deck.
- **Telecom & infrastructure operators:** The controller, metering stack, or protocol gateway from 2012 is out of support. The vendor is gone or unresponsive. Your engineers need the protocol behavior recovered before the last spare part dies — and the work has to satisfy MACRA and Data Protection Act 2024 expectations.
- **NGOs, agriculture & climate programs:** Donor-funded apps claim offline-first operation, then silently lose field data when the network drops. MRV and carbon-registry exports live in opaque formats that fail verifier scrutiny. You need the data formats decoded and the provenance chain documented — before the auditor does it for you.

### How an engagement works

1. **Scoped authorization.** We start with a signed authorization record covering exactly which artifacts we may analyze — ownership, license, or written permission from the rights-holder. Scope is frozen before any analysis begins.
2. **Human-governed analysis.** Our analysis agents do the bulk extraction; a senior reverse-engineering analyst reviews every finding against the evidence, line by line. Nothing ships as an agent-only conclusion.
3. **Defensible delivery.** You receive a findings report where every claim cites its evidence, a sector-specific artifact (format specification, risk scorecard, protocol documentation), and the full audit trail — authorization, methodology, tool versions.

### What you receive

| Deliverable component | What it gives you |
|---|---|
| Findings report | Every finding with evidence reference and confidence level |
| Sector artifact | Format spec, offline-readiness scorecard, or protocol documentation (engagement-dependent) |
| Evidence appendix | Tool versions, methodology, sample records — re-checkable by your auditors |
| Authorization & audit trail | Signed scope record and governance gates — defensible to boards and regulators |

### Engagement integrity — our standing commitments

> **We analyze only what you are authorized to have us analyze.** A signed authorization record covering every target artifact is a hard precondition — not fine print. We decline work where lawful access cannot be evidenced.
>
> **Your artifacts stay local by default.** Analysis runs on sovereign infrastructure; evidence stays client-side unless you explicitly authorize otherwise. This aligns with Malawi's Data Protection Act 2024 and cross-border transfer rules.
>
> **A human expert signs every report.** Agents accelerate the work; a named analyst owns the conclusions.

### Indicative engagement ranges

*Confirmed in scoping. Final scope and price are set after a paid discovery engagement.*

| Engagement tier | Typical scope | Indicative investment |
|---|---|---|
| **Format & data rescue** | One legacy/proprietary format or export chain — specification, field dictionary, migration runbook | USD 2,500 – 15,000 |
| **Readiness & compliance assessment** | Offline-readiness or MRV data-integrity audit of one application or registry export chain | USD 4,000 – 15,000 |
| **Vendor / product analysis** | Binary-level claims verification or legacy firmware/protocol recovery — **available under scoped legal review** | USD 8,000 – 50,000 |

*Ranges are indicative, sized to artifact count and depth. USD for donor/international clients; MWK terms available for local engagements with standard validity.*

### Next step

**Book a 30-minute scoping call.** Bring the artifact that is driving the question — a sample export, an app build name, a device model — and we will tell you within the call whether the engagement is viable, which tier it fits, and what authorization we would need. If it is not a fit, we will say so.

---

# PART B — INTERNAL ONLY — BD PLAYBOOK

*Not for distribution. Working reference for BD conversations.*

## B1. Package pitchability

| Package | Risk class | Legal gate | BD posture |
|---|---|---|---|
| **R1** Format Rescue — Legacy/Proprietary Interoperability | Low | No (elevates to Medium if third-party commercial binary must be inspected) | **PITCHABLE NOW** — lead offering; attach to Offer C (Data & Reporting) |
| **R5** Offline-Readiness & Low-Bandwidth App Assessment | Medium | No (legal gate if third-party commercial product) | **PITCHABLE NOW** — NGO/agriculture beachhead; pairs with "offline-first, sovereign by design" positioning |
| **R6** MRV / Climate Data-Format Audit | Low–Medium | No (unless third-party platform binaries in scope) | **PITCHABLE NOW** — climate/natural-resources differentiator; no local competitor offers this |
| **R2** Vendor Due-Diligence Audit | Medium–High | **Yes if third-party vendor binary in scope** | **CONDITIONAL** — pitch only to clients who can evidence license/authorization to inspect the vendor binary; CLO confirms per engagement |
| **R3** Competitor Product Teardown & Benchmarking | High | **Yes — mandatory every time** | **GATED** — say "available under scoped legal review" only if asked; do not lead with it; cap at one concurrent R3 per analyst pod until CLO playbook exists |
| **R4** Firmware & Protocol Analysis | High | **Yes — mandatory** | **GATED** — same posture as R3; requires engagement lead with hardware background; extra CISO review if device touches subscriber/payment data |

**Default pitch set for outbound: R1, R5, R6.** R2 only when the buyer already holds inspection rights (procurement shortlist under contract review is the natural case). R3/R4 are inbound/relationship plays after trust is established.

## B2. Sector ICP cards

### Financial services (beachhead #2)
- **Buyer:** Head of Digital Payments / CISO / Head of IT at commercial bank or mobile-money operator; secondary: Head of Procurement during vendor renewal
- **Trigger event:** RBM IT-examination notice; fraud incident traced to third-party payment SDK; vendor contract up for renewal or M&A target under diligence
- **Opener:** "When the next RBM exam or SDK incident hits, can you show evidence of what your payment vendor's app actually does with customer data — or only what the contract says it does?"
- **First package to offer:** R2 (conditional — client must hold license/authorization) or R1 if the pain is their own legacy export chain

### Telecom (beachhead #3)
- **Buyer:** Network Operations Director / CTO office at TNM, Airtel Malawi; secondary: MACRA compliance desk (regulator-adjacent proof play)
- **Trigger event:** end-of-support notice on network element or protocol stack; MACRA enforcement action; DPA 2024 audit of subscriber-data handling
- **Opener:** "When the 2012 controller's vendor support ends, does your team have the protocol spec — or does the equipment keep running on tribal knowledge until it doesn't?"
- **First package to offer:** R4 (gated — lead only the discovery conversation, not the engagement); bridge with R1 on any associated export formats

### NGOs / donor-funded projects (beachhead #4)
- **Buyer:** IT Director / MEAL Director on a World Bank, FCDO, or UN-funded project; secondary: local prime implementing NGO
- **Trigger event:** donor audit requirement naming software due diligence; vendor DD clause in grant agreement; field teams reporting data loss on offline apps
- **Opener:** "Your grant says the app works offline for 2G field sites. Has anyone verified that against the actual build — or are you trusting the vendor's claim at the next donor review?"
- **First package to offer:** R5

### Agriculture / natural resources
- **Buyer:** Ops Director / CTO of agri-tech platform; GIS/ exploration lead at mining or forestry operator
- **Trigger event:** farm-management system vendor sunsetting; sensor data-format dispute with partner; IP concern over proprietary crop/soil model exposure
- **Opener:** "Ten years of cooperative member records sit in one vendor's export format. If that vendor disappears next quarter, what happens to the data?"
- **First package to offer:** R1

### Climate / MRV
- **Buyer:** MRV Lead / carbon-registry operations at climate-finance program
- **Trigger event:** verifier challenge on data provenance; registry platform migration; donor audit of the emission-data chain
- **Opener:** "When your verifier asks how the emission numbers trace back to raw measurements, can you show the provenance chain — or is it a spreadsheet export nobody can open?"
- **First package to offer:** R6

## B3. Discovery questions (use in scoping call, in order)

1. What specific artifact or system is driving this question today — and what happened to put it on your desk this quarter?
2. Do you own it, hold a license to it, or would we need written authorization from a third party to analyze it?
3. What decision hangs on the answer: procurement, modernization, compliance response, board reporting, or something else?
4. If you do nothing for six months, what breaks or stays exposed?
5. Have you already asked the vendor for this information (interface spec, security posture, offline behavior)? What did they say — and what did that cost you in delay?
6. Are there hard deadlines attached: an RBM exam, MACRA interaction, donor audit date, contract signature, or board meeting?
7. Are there policy or regulatory constraints on where the artifact can be analyzed — does it have to stay on your infrastructure?
8. What would a "good enough" deliverable look like for whoever has to defend this internally — auditor, board, regulator, or engineering lead?
9. Who besides you has to sign off on engaging an external analysis firm, and what is their main reservation likely to be?
10. Which budget line would this come from — IT audit, compliance, innovation, or capex — and is that line already funded this cycle?

## B4. Objection handlers

**"Isn't reverse engineering illegal?"**
No — not when it is done with authorization, on artifacts you own or are licensed to inspect, and without circumventing protections you are not permitted to touch. Written authorization covering every target is our first deliverable and a hard precondition. We decline work where lawful access cannot be evidenced. That discipline is why our reports hold up with auditors and regulators.

**"We could do this ourselves — our engineers know the system."**
The tools are largely free; the cost is the analyst bench and the governance. A senior reverse engineer who has done this fifty times, plus a review process where every finding carries a re-checkable evidence record, is what you are buying — not access to a decompiler. Internal teams rarely have spare RE capacity, and they rarely have the review discipline that survives a board challenge.

**"AI output is unreliable — how do I know this isn't hallucinated?"**
You are right to ask, and it is why our process is built around it. Agents do the bulk extraction; a named senior analyst reviews every finding against the raw evidence before it ships. Every report includes an evidence appendix — tool versions, methodology, sample records — so your team or your auditors can re-derive any conclusion. We do not ship agent-only findings, and we will tell you when the evidence does not support a claim rather than dress up a guess.

**"Our binaries / data cannot leave our premises."**
Agreed, and it is the default. Analysis runs on sovereign infrastructure; evidence stays client-side unless you explicitly authorize otherwise. That is also our difference from offshore scanning platforms (NowSecure, Appknox, Binarly) that require uploading artifacts to their cloud — a non-starter under Malawi's Data Protection Act 2024 cross-border rules for many of our clients.

**"We don't have budget for this right now."**
The entry tiers are sized to sit inside an IT-audit or compliance line, not a new capex request — indicative USD 2,500–15,000 for format and readiness engagements, confirmed in a paid scoping session so you are not buying a blind project. If the decision on the table (vendor renewal, acquisition, donor audit) is worth more than the engagement fee, this is cheap insurance against it going wrong.

**"Why use a local firm instead of a global vendor?"**
Three reasons, in order of weight: (1) data residency — your artifacts do not get uploaded to an offshore SaaS scanner; (2) regional legal literacy — DPA 2024, MACRA, RBM examination expectations, and donor flow-downs are the context we work in daily; (3) cost and turnaround — the same governed evidence discipline without global-firm pricing or time-zone drag. Global firms compete on brand; we compete on locality and evidence quality.

**"What if your findings are wrong, or the vendor disputes them?"**
Every engagement starts with signed acceptance criteria and a scope freeze, and ships with the evidence appendix so disputes get settled against the record, not opinions. Our liability is capped at fees — standard for analysis work — but the reason disputes are rare is that we report what the evidence supports, including "inconclusive" when that is the honest answer.

**"Can you guarantee you will find X (the vulnerability, the hidden telemetry, the protocol field)?"**
No — and be wary of anyone who says yes. We guarantee process, evidence, and honest reporting: you will get what the analysis supports, with confidence levels attached, and a clear statement of what was out of scope or not observable. A clean result with evidence behind it is often the more valuable finding.

## B5. Qualification checklist (gate before proposal)

- [ ] **Authorization path confirmed** — client owns the artifact, holds a license, or can obtain written third-party authorization; no ambiguous lawful-access posture
- [ ] **Use case maps to a pitchable package** — R1/R5/R6 fit, or R2/R3/R4 only with legal-gate awareness and a named CLO handoff
- [ ] **Named economic buyer + decision deadline** — not "the team is interested"; a person with budget authority and a date
- [ ] **Data-handling posture compatible** — local analysis acceptable; no policy requiring the artifact stay on a specific air-gapped environment we cannot meet
- [ ] **Funded budget line exists** — audit, compliance, or IT line, current cycle
- [ ] **Scope fits the effort band** — artifact count and depth consistent with the tier; change-order discipline explained at proposal stage
- [ ] **No POL-CL-001 offer-block conflict** — intake service check passes
- [ ] **No "do not promise" violation** — see B7; walk away or re-scope if the buyer's expectation cannot be met honestly

**Kill criteria (walk away / park):** no lawful-access path; buyer wants agent-only unreviewed findings; buyer wants forensic/legal-expert testimony we do not provide; buyer wants malware or offensive tooling; scope requires circumventing protections we are not authorized to touch; free-discovery expectation with no paid scoping path.

## B6. Legal handoff rules (R2 conditional, R3/R4 gated)

1. **Never start analysis before the CLO memo on R3 and R4.** The memo must cover: jurisdiction-specific reverse-engineering exceptions (interoperability, security research as applicable), terms-of-service exposure of the target, technical-protection-measures assessment, and an explicit go/no-go. Same for R2 whenever a third-party vendor binary is in scope.
2. **Freeze scope at S2 authorization.** Signed authorization record lists every target artifact; scope hash frozen; any new artifact is a change order and re-attestation, never an informal add.
3. **Clean-room procedure when output is delivered to clients** (per `01-legal-compliance.md` §3.2) — required whenever REA output becomes a client deliverable, not optional.
4. **Cap concurrent R3 engagements at one per analyst pod** until the CLO has a standard playbook (per `06-client-offerings.md` R3 notes).
5. **R4 additional gate:** CISO review for any device that handles subscriber or payment data, on top of the mandatory legal gate.
6. **Sector overlays apply before the CLO memo, not after:** financial services (GLBA Safeguards Rule if serving a covered US institution), telecom (MACRA licensing/equipment-authorization questions), NGOs (clause-by-clause prime-grant flow-down check), agriculture/climate (lowest overlay risk — personal-data exposure under DPA 2024 only).
7. **In outbound copy and calls, gated packages are never sold as delivered work.** The only permitted phrasing is "available under scoped legal review" — and only if the buyer asks about competitor teardown or firmware work. Do not lead with R3/R4; do not put their price bands in circulated materials until the CLO playbook and CFO+CEO ratification exist.

## B7. Do-not-promise list (standing — every conversation)

- Autonomous agent-only findings — every deliverable is human-reviewed
- Forensic or legal-expert testimony — we produce analysis reports, not expert-witness work
- Malware creation, offensive tooling, or attacking systems — out of scope, no exceptions
- Circumvention of access controls or technical protections beyond documented statutory carve-outs the client is authorized to rely on
- Guarantee of any specific finding — we guarantee process, evidence, and honest reporting
- Free discovery or scoping without a paid engagement path — unpaid scoping is the top pilot-margin killer (`05-financial-model.md` §6)
- Public rate cards or final pricing — indicative bands only until CFO + CEO ratification

## B8. Pitchable-now vs gated — quick reference

| Say this | Not this |
|---|---|
| "We analyze artifacts you own or are authorized to inspect, with a signed authorization record" | "Send us any binary and we'll take it apart" |
| "Every finding ships with a re-checkable evidence record, reviewed by a named analyst" | "Our AI will find everything" |
| "Analysis stays on sovereign infrastructure by default — aligned with DPA 2024" | "Upload to our portal and we'll scan it" |
| "Format rescue, offline-readiness, and MRV audits are available now" | "We do competitor teardown and firmware cracking" (never in outbound) |
| "Vendor/product analysis is available under scoped legal review" | Specific R3/R4 price bands or "we can start next week" on gated work |
| "Indicative investment ranges, confirmed in a paid scoping session" | "Our rate is $X" as a committed price |

---

## Sources

| Claim | Source |
|---|---|
| R1–R6 offering definitions, risk classes, legal gates, engagement SOP | `reports/rea-feasibility/06-client-offerings.md` |
| Sector demand, buyers, willingness to pay, beachhead sequence, positioning statement | `reports/rea-feasibility/04-market-landscape.md` |
| Indicative price bands (DIRECTIONAL), pilot economics, unpaid-scoping risk | `reports/rea-feasibility/05-financial-model.md` |
| Authorization precondition, clean-room procedure, sector overlays, DPA 2024 / MACRA / RBM context | `reports/rea-feasibility/01-legal-compliance.md` |
| Adoption verdict, evidence-handling invariant | `reports/rea-feasibility/FEASIBILITY-STUDY.md` |
| 4 governance gates (G1–G4), POL-CL-001 | `src/ai_company/services/client_intake.py`, `config/company/malawi_offers.yaml` |
| Do-not-position-as list | `reports/rea-feasibility/07-strategy-positioning.md` |
