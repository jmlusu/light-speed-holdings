# REA Adoption — Consolidated Phase-1 Feasibility Study

**To:** Jack Mlusu, Human CEO
**From:** Chief of Staff (Agentic Research Lead, Pharos)
**Date:** 2026-10-17
**Subject:** Decision memo — adopting `github.com/morluto/rea` (npm `rea-agents`, MIT) across Lightspeed Holdings
**Corpus:** Nine Phase-1 stream reports (`00`–`08`), `reports/rea-feasibility/`
**Status:** Consolidated synthesis. All figures trace to the stream files; nothing outside the corpus is asserted as verified.

---

## Evidence legend

| Label | Meaning |
|-------|---------|
| **[V]** | Verified against a primary source recorded in `00-rea-capabilities.md` (S1–S17; checked 2026-10-17) or in a named repo document |
| **[D]** | **DIRECTIONAL** — reasoned internal estimate, not yet validated with a real prospect or measured run |
| **[U]** | **UNVERIFIED** — flagged in the corpus as not established from available evidence; must not be relied on for a decision |
| **[S]** | Synthesis inference by this memo (derived from two or more streams; labeled at point of use) |

This memo follows AGENTS.md §15 (Evidence, Honesty and Execution Integrity Policy): what each stream found, what is inferred, and what remains unknown are kept distinct.

---

## 1. Executive summary

**Recommendation: adopt REA as an internal analysis engine under a conditional pilot — as a governed consulting service line, not a product and not a new venture.** Three independent streams reached compatible verdicts:

- **Security (CISO, `02`):** "**SAFE TO PROCEED — WITH CONDITIONS (conditional pilot approval)**" — blocked on P0 supply-chain controls (SC1 pin, SC2 internal mirror + lockfile/SHA-512, SC4 postinstall audit, SC7 no auto-update).
- **Technical (CAIO, `03`):** "**Architecture A — REA as an MCP tool inside the agent runtime**," recommended over a standalone workstation, gated on five time-boxed spikes (≈8–10 working days) including a Windows-11 Ghidra P0 reality check.
- **Strategy (CSO, `07`):** REA positions Lightspeed as an *Agentic AI-Native enterprise* partner with an evidence discipline — but "**New venture: not yet, not now**"; stage the offering (Now → Day 90 consulting service line) and require Portfolio scorecards green two consecutive quarters before any portfolio move (`docs/venture-studio/03-operating-model.md` §5).

**Why it is attractive.** REA and Ghidra are $0 (MIT) [V], the offering reuses the existing ~90-agent governed hierarchy and executor stack [V, `08`], and the delivery model is *local-first*: binaries never leave sovereign infrastructure — which both satisfies Malawi's Data Protection Act 2024 (Act No. 3 of 2024, MACRA as DPA) and differentiates against cloud REaaS competitors whose artifact-upload model is impractical under cross-border rules [D, `04` §3].

**Why it is gated.** REA is explicitly **not a sandbox** (`02`; `03` §1.1). Three hard gates govern go/no-go: (G-A) Windows 11 free native Ghidra support is **experimental, P0, read-only** (`00` §5 / S9) [U/V]; (G-B) evidence artifacts (hundreds of MB; ~334 MB raw) must never enter model context wholesale (`00` §4 / S7) [V]; (G-C) sending results to a model provider is an AGENTS.md §9.2 policy decision, mitigated by summary-only export (`03` §6) [V].

**Money.** Year-1 pilot ask: **$13,399 (≈MWK 24.1M @1,800)** — mostly internal analyst opportunity cost, not new cash [D, `05` §5]. Base-case unit margins 80.1%–88.3% clear the 55% floor; conservative cases for two of three archetypes (50.8%, 49.5%) fall below it and must be fixed by pricing or scope discipline before the pilot (`05` §3.2–3.3). Break-even: **≈2 engagements/year base, ≈3 conservative** (`05` §4.3) — achievable inside the Year-1 pilot itself.

**What we are buying:** ~8–10 days of spikes + P0 security controls, then a pilot of up to 5 engagements, to prove or disprove an evidence-producing, audit-ready reverse-engineering service line for Malawi and SADC.

---

## 2. Cross-stream reconciliation

The nine streams were written independently against the shared facts brief (`00`). Where they differ in emphasis, they reconcile as follows.

### 2.1 Verdicts are consistent, not additive

| Stream | Verdict | Conditions |
|--------|---------|------------|
| `02` Security | SAFE TO PROCEED — WITH CONDITIONS | P0: SC1, SC2, SC4, SC7; deny-egress default; T1–T3 threat actors |
| `03` Technical | Architecture A recommended | 5 spikes ≈8–10 days; Gates G-A/G-B/G-C; HITL tiers 2–3 |
| `01` Legal | Permissible with contract architecture | Anti-circumvention scope clause, client indemnity, Malawi seat |
| `04` Market | Service line viable, not a market bill | Positioning; beachhead sequence; sell evidence + residency |
| `05` Financial | Pilot clears economics | Fix sub-floor conservative margins; validate prices with 2–3 prospects |
| `06` Commercial | 6 fixed-scope offerings ready | Gates G1–G4; attestation prerequisite; no public pricing w/o CFO+CEO |
| `07` Strategy | Staged evolution; venture NO | Portfolio scorecard rules |
| `08` Internal | Immediate low-risk internal use | Public accessibility ≠ authorization boundary |

**No stream recommends adoption without conditions; no stream recommends rejection.** [S] The conditions are compatible: the security P0s (`02` SC1–SC7), the technical spikes (`03`), and the legal contract clauses (`01` §contract) can run in parallel within the first 30 days (§4).

### 2.2 Architecture: A is the product path, C is the proof path

`03` §1.4 compares three architectures — A (MCP tool inside the agent runtime), B (worker-side `rea analyze --json` + managed evidence store), C (standalone analyst workstation). Effort estimates: MVP A ≈10–11 person-days, B ≈19–25, C ≈2–3.5 [D]. Reconciliation across `03` and `07`: **C is the validation vehicle** (get to a first reference deliverable with minimal build), **A is the productized delivery architecture** (HITL, evidence store, summary-only export already exist in the runtime), **B stays on the shelf** unless A's MCP registration fails in Spike 2 [S]. The strategy stream (`07`) never requires A in Day 1–90 — it requires *priced packages and buyer conversations*, which C can produce.

### 2.3 Scope reconciliation: what we do, and what we explicitly do not

- **Do not:** generic "AI cybersecurity," a pure pentest shop, or a SaaS product (`04` §4.3).
- **Do not:** cardholder data, telecom network elements/spectrum equipment, E2EE messaging internals, or auth/authorization components of third-party production systems (`01` contract clause 2) — these exclusions also remove PCI DSS and most telecom-network regulatory exposure by contract (`01` §7).
- **Do not:** launch a new venture before Day 90 (`07`).
- **Do:** an "Agentic AI-Native Enterprise Transformation for Africa" territory, of which REaaS is the first evidence-producing service line (`07`; `04` §4.3 positioning statement).

### 2.4 Evidence handling is the single cross-cutting invariant

Every stream touches the same control: **raw evidence stays local; only human-reviewed, size-bounded summaries reach models** (`00` §4 / S7; `03` §1.1 tool_summarizer + `raw_result` never leaves; `02` C-REPORT/C-SNAP; `06` evidence client-side by default). This invariant satisfies Malawi DPA cross-border expectations (`04` §3) [D], the internal audit-evidence separation rule (AGENTS.md §9.3), and the §9.2 transmission ban simultaneously. [S]

---

## 3. Consolidated risk register (R1–R10)

| ID | Risk | Source streams | Impact | Mitigation / owner | Gate |
|----|------|----------------|--------|--------------------|------|
| **R1** | **Supply-chain concentration** — single maintainer ≈53% of commits (1,790 ≈2,956, bus factor ≈1), weekly releases, npm delivery, 1,207 open issues; `npx -y rea-agents@latest` is forbidden | `02` §4.1 | Critical | SC1 pin version P0, SC2 internal mirror + lockfile + SHA-512 P0, SC4 postinstall audit P0, SC7 no auto-update P0; internal fork option (`04` §6.1) | Pilot start |
| **R2** | **Unauthorized evidence exfiltration to model providers** — violates AGENTS.md §9.2 | `00` §4/S7; `03` §6; `02` | Critical | Summary-only export; `raw_result` never reaches any provider; deny-egress-by-default firewall (SC/§3.4 of `02`) | Spike 3 |
| **R3** | **Prompt injection / malicious content in binaries** — REA is *not* a sandbox; PI1–PI8 vectors; actors T1–T3 | `02` §2; `03` §1.1 | High | Tier-2 HITL before analyze (`HITLGates.require_approval_from_tier = 2`), Tier-3 two-person before export; no shell (shlex sandbox) | Spike 2 |
| **R4** | **Authorization / anti-circumvention exposure** — DMCA §1201, EU InfoSoc Art. 6 + Software Directive Arts. 6/8, UK CDPA Part VII ss. 296ZA/296ZB (correction); Malawi copyright §85(1)(c) interop exception [U per `01`] | `01` §1, correction 1 | High | Signed lawful-access attestation (`06` hard prerequisite); authorized-target clause (`01` clause 1); scope exclusions (clause 2) | Gate L2 |
| **R5** | **Data-sovereignty / cross-border transfer** — Malawi Data Protection Act 2024 (Act No. 3 of 2024), MACRA as DPA; cloud REaaS competitors require artifact upload | `04` §3; `01` §6.5 (Malawi seat) | High | Local-first by architecture; evidence client-side by default; Malawi governing law/seat | Gate L2/L3 |
| **R6** | **Output ownership & AI-authorship uncertainty** — 17 U.S.C. §102(a)–(b), *Thaler v. Perlmutter*; Malawi position unestablished [U] | `01` §4 | Medium | Client owns findings, Lightspeed retains methods (`06` §4.4); output-warranty disclaimer + IP allocation clause with AI-authorship caveat (`01` clause 4) | Gate L2 |
| **R7** | **Human-hour overrun** — largest financial sensitivity: +25% hours = **−$108,000** Year-2 contribution | `05` §4.4 | High | Hard SOW + change-order clause; capped review rounds; liability cap = 100% of fees | Pilot |
| **R8** | **Conservative-case margins below the 55% floor** — Legacy 50.8%, Teardown 49.5% | `05` §3.2–3.3 | Medium | Reprice or tighten scope before external rate card; validate with 2–3 real prospects first (`05` §2 [D]) | Pre-rate-card |
| **R9** | **Windows-native Ghidra path fails** — free native support is *experimental / P0 / read-only* | `00` §5/S9; `03` §4 | Medium | Spike 1 reality check (`rea doctor` clean); fallback = Linux analysis hosts (`04` §6.1), Windows phase-2 | Spike 1 |
| **R10** | **Market entry & commoditization** — cloud players (Binarly, Finite State, NowSecure PTaaS), Big-4 entry; open-source virality (~297k stars) | `04` §6.1 | Medium–High | Defensibility = residency + audit-grade Evidence records + governed 90-agent hierarchy + regulatory familiarity; be specialist subcontractor to Big-4, not head-on | Day 90 |

**Residual risk posture:** with R1, R2, R3 closed by P0 controls and spikes, and R4–R6 closed by contract, remaining exposure is commercial (R7, R8, R10) — which is precisely what the pilot exists to measure. [S]

---

## 4. Phased roadmap — Days 1–90 (T-Now / T-Client tranches, L1–L3 legal gates)

### 4.1 Control tranches

| Tranche | Definition | May begin when |
|---------|------------|----------------|
| **T-Now** | Work with no client data: internal binaries, open-source verification, spikes, controls, docs, pricing research | Immediately |
| **T-Client** | Any engagement involving client-supplied binaries or client data | After Gates **G1–G4** (`06`: contract → DPA/classification → compliance → CISO review, mirroring `client_intake.py` POL-CL-001) |

### 4.2 Legal gate ladder (L1 → L3) [S, mapped to `01` + `06`]

| Gate | Scope | Required before |
|------|-------|-----------------|
| **L1** | Own/OSS binaries, internal use-case audits (`08`) | T-Now work (nothing beyond standard AGENTS.md §9 policy) |
| **L2** | Third-party client binaries under MSA: lawful-access attestation + four contract clauses (`01` clause 1–4), Malawi governing law/seat, scope exclusions, indemnity carve-out, IP/output allocation | First client engagement (G1/G2) |
| **L3** | Regulated-sector work (finance, telecom) — MACRA licensing verification, RBM IT-examination fit, DPA 2024 classification; **cardholder data and telecom network elements remain contractually excluded** (`01` clause 2) | Any L3 prospect; G3 compliance sign-off |

### 4.3 Schedule

**Days 1–14 — Spikes + P0 security (T-Now).**
- Spike 1: Windows 11 Ghidra reality check — `rea doctor` clean, read-only analyze on Windows 11; fallback documented to Linux host [G-A] (`03` §7).
- Spike 2: MCP registration + HITL interception in the existing runtime (`PROTOCOL_VERSION "2025-06-18"`, `src/ai_company/mcp/server.py`; MCP surface marked **UNVERIFIED → spike**) (`03` §1.1).
- In parallel: deploy SC1 pin, SC2 mirror/lockfile/SHA-512, SC4 postinstall audit, SC7 no-auto-update (`02` P0 list); deny-egress-by-default egress rule (`02` §3.4).

**Days 15–30 — Evidence pipeline + tiers (T-Now).**
- Spike 3: evidence volume → disk → `tool_summarizer` → context-safe summary; prove `raw_result` never leaves [G-B] (`03` §7).
- Spikes 4–5: model routing policy per evidence tier (three existing routing layers; hard rule = no raw evidence to providers) and a reference analysis run (`03` §6).
- Commission contract template review — legal budget line $2,000 (`05` §5).

**Days 31–60 — First deliverable + pricing validation (T-Now → L2 entry).**
- MVP: 1 working end-to-end teardown report (REA + Ghidra + local models) in **2–3 weeks** analyst time (`05` §5) [D].
- Pricing validation: 2–3 real prospects per `05` §2 before any external rate card; lock the three archetypes or reprice to clear the 55% floor (R8).
- Legal: execute the four-clause MSA; set up attestation workflow in `06`.

**Days 61–90 — Pilot engagements (T-Client, gates G1–G4).**
- Target: first closed engagement(s); Year-1 base plan = 3 (`05` §4.1).
- Productize only what is proven: report template (7 sections, §7 Authorization Record) + evidence appendix (tool version, methodology) (`06`).
- Strategy checkpoint: 15–20 buyer calls and design-partner LOIs per `07` validation criteria.

**Not in Days 1–90:** new-venture launch (forbidden, `07`); Portfolio B/C move (needs two consecutive green quarters); public rate card (needs CFO+CEO, `06`); IDA Pro spend (optional per-engagement only, `05` §5).

---

## 5. Final recommendation and NO-GO triggers

### 5.1 Recommendation

**Adopt REA — conditionally.** Approve:

1. **A 90-day conditional pilot** at a Year-1 budget of **$13,399 (≈MWK 24.1M)** — tooling $99, legal $2,000, compute headroom $500, analyst labor $9,000 (opportunity cost), QA $1,800 (`05` §5) [D].
2. **Architecture A** for productization; **Architecture C** as the Day-1 validation vehicle (`03` §1.4).
3. **Service-line posture only** — positioning per `04` §4.3; staged evolution per `07`; no new venture.
4. **The four contract clauses and gates G1–G4 as non-waivable** entry conditions for any client work (L2).
5. **P0 supply-chain controls (SC1/SC2/SC4/SC7) as the precondition for any execution of `rea`** — no exceptions, no `@latest`.

### 5.2 NO-GO triggers

Abort, pause, or hold the affected tranche if any of the following occurs:

| # | Trigger | Response |
|---|---------|----------|
| N1 | Spike 1 fails on Windows **and** no Linux analysis host is available | Hold Windows path; re-plan on Linux. If neither viable → **NO-GO** on technical adoption |
| N2 | P0 controls (SC1/SC2/SC4/SC7) cannot be implemented as specified | **NO-GO** until implemented — overrides `02` conditional approval |
| N3 | Spike 3 shows raw evidence cannot be kept out of model context (G-B breach) | **NO-GO** on any provider-touching workflow; restrict to fully offline local models or abort |
| N4 | Client will not sign the attestation or the four-clause MSA (incl. scope exclusions + indemnity carve-out) | **NO-GO** on that engagement (T-Client denied) |
| N5 | Any request to upload client artifacts to a cloud REaaS or to move evidence across borders contrary to DPA 2024 posture | **NO-GO**; report per AGENTS.md §9.2 escalation (CISO of record: CEO) |
| N6 | 2–3 prospect validations show no price clears the 55% floor | Pause rate card; re-scope archetypes before pilot close |
| N7 | Pilot closes 0 engagements after validation window | Strategy checkpoint with CEO — continue service line, or park per `07` portfolio rules |
| N8 | Supply-chain incident (malicious release, postinstall anomaly) | Immediate SC7-style freeze; incident response; CISO review |

---

## 6. Decision log (D1–D5)

| ID | Decision | Basis | Status |
|----|----------|-------|--------|
| **D1** | **Adopt REA under a conditional pilot** | `02` SAFE TO PROCEED — WITH CONDITIONS; `03` Architecture A; consistent across all streams | **Awaiting CEO approval** |
| **D2** | **Architecture: A (MCP-in-runtime) for productization; C for validation; B shelved** | `03` §1.4 effort comparison + HITL/evidence reuse | Proposed (spike-conditional) |
| **D3** | **Scope exclusions are non-negotiable** — cardholder data, telecom network elements/spectrum equipment, E2EE internals, third-party auth components | `01` contract clause 2; kills PCI DSS and most telecom overlay | Proposed |
| **D4** | **Not a new venture before Day 90** — consulting service line only; Portfolio move requires two consecutive green quarters | `07` (venture-gate rules, `docs/venture-studio/03-operating-model.md` §5) | Proposed |
| **D5** | **No external rate card until 2–3 prospect validations clear the 55% floor**; pilot ask $13,399 approved in parallel | `05` §2, §3; `06` pricing rule (CFO+CEO) | Proposed |

**Open questions requiring CEO or owner input:**
1. Approve the $13,399 Year-1 pilot ask (and the $2,000 legal line) — yes/no?
2. Confirm Linux analysis-host availability if Spike 1 (R9) fails on Windows — provision or defer?
3. Confirm that Tier-2 HITL before every client analyze is operationally acceptable for pilot speed (`03` §1.1).

---

## 7. Appendix — file index

All files: `reports/rea-feasibility/`.

| File | Lines | Stream | Author role | Core contribution |
|------|-------|--------|-------------|-------------------|
| `00-rea-capabilities.md` | 233 | Shared facts | Agentic Research Lead (Pharos) | Sources S1–S17, verified 2026-10-17; UNVERIFIED convention; evidence-record design (334 MB → ~10 KB) |
| `01-legal-compliance.md` | 209 | Legal / compliance | CLO (desk research, not formal legal advice) | Anti-circumvention, copyright/AI-authorship, 4 contract clauses, Malawi seat, GLBA/PCI DSS sector overlays |
| `02-security-threat-model.md` | 321 | Security | CISO / acting Red-Team Engineer | Assets A1–A8, actors T1–T3, PI1–PI8, controls SC1–SC7, P0/P1 control tables, verdict "SAFE TO PROCEED — WITH CONDITIONS" |
| `03-technical-feasibility.md` | 307 | Technical | CAIO | Architectures A/B/C, Gates G-A/G-X, HITL tiers, effort table, Windows 11 matrix, model routing, 5 spikes (≈8–10 days) |
| `04-market-landscape.md` | 217 | Market | Market stream (DIRECTIONAL) | Market sizing, pricing archetypes ($2,000–$15,000 [D]), DPA 2024/MACRA, positioning statement, beachheads, threat/defensibility tables |
| `05-financial-model.md` | 235 | Financial | Financial analyst (reports to CFO) | Cost base ($13,259 Y1 / $44,379 Y2), unit economics (3 archetypes × 3 scenarios), break-even ≈2–3 engagements, sensitivity, budget ask $13,399 |
| `06-client-offerings.md` | 293 | Commercial | Service owner | 6 fixed-scope offerings, gates G1–G4 (POL-CL-001), report template (7 sections), attestation prerequisite, pricing/payment rules |
| `07-strategy-positioning.md` | 183 | Strategy | CSO | Position *Agentic AI-Native Enterprise Transformation for Africa*; staged evolution Now→D90; venture "not yet, not now" |
| `08-internal-use-cases.md` | 143 | Internal adoption | CTO (internal-only) | Estate facts (Python ≥3.12 CLI, Vite/React SPA, ~90 agent cards, 12 workflows, 6 required checks); internal use cases; authorization boundary note |

**Corroborating repo documents cited by the corpus:** `AGENTS.md` (§9.1 HITL, §9.2 transmission ban, §9.3 audit evidence separation, §15), `docs/ai-caas-pricing-model.md` (bands, 55% floor, 50/50 terms), `docs/APPROVED-VENDORS.md`, `docs/SKILL_CURATION_POLICY.md`, `config/company/guardrails.yaml` ($0.50/task, $2/day caps), `docs/venture-studio/02-sector-positioning.md` (Four Reservations), `docs/venture-studio/03-operating-model.md` §5 (portfolio scorecards), `src/ai_company/audit/`, `src/ai_company/orchestrator/`, `src/ai_company/executor/hitl_gate.py`, `src/ai_company/services/client_intake.py`.

---

*Prepared as a consolidated synthesis of the Phase-1 corpus. Figures labeled [D] are directional; labeled [U] are explicitly unestablished. This memo does not add analysis beyond the corpus except where marked [S].*
