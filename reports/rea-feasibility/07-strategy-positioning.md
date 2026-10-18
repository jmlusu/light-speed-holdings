# REA Feasibility — Phase 1: Strategy & Positioning

**Date:** 2026-10-17
**Author:** Chief Strategy Officer (dual hat: CEO Advisor to Jack Mlusu)
**Scope:** Strategic fit, portfolio placement, governance posture, positioning narrative, and GO/NO-GO recommendation for adopting "Reverse Engineer Anything" (REA, `morluto/rea`) as an internal capability and client service line.
**Inputs:** `reports/rea-feasibility/00-rea-capabilities.md` (shared facts, cited as §N/SN); `docs/venture-studio/02-sector-positioning.md`; `docs/venture-studio/03-operating-model.md`; `docs/Pharos/positioning.md`; `company-registry.yaml` (verified directly); `AGENTS.md` governance sections.
**Status:** Strategy deliverable — docs only. No registry, code, or brand changes.

---

## 1. Strategic Fit

**Where we stated we are:** *Agentic AI-Native Enterprise Transformation for Africa*; three intellectual territories — AI Company Building, Agentic AI Use Cases, AI Governance & Policy (`docs/venture-studio/02-sector-positioning.md` §1, `docs/Pharos/positioning.md`). Do-not-position-as list: AI Expert, AI Consultant, Generative AI Specialist, AI Engineer.

**What REA actually is:** a local MCP server + CLI that lets AI agents investigate software artifacts (binaries, APKs, JS/Electron, .NET, captures, firmware…) through existing engines, returning findings wrapped in a canonical **Evidence record** with stated coverage limitations and reproducible snapshots (§1, §4). It is not a decompiler; it is an *agent-to-analysis-engine harness with an evidence discipline*.

That last framing is the whole strategic argument: REA is a textbook instance of "AI agents performing meaningful technical work under governance and evidence" — our own core claim. The fit question is not "are we an RE firm?" (we are not) but "does governed agentic analysis extend our category, or dilute it?"

### Fit-score table

| # | Consideration | Fit | Rationale |
|---|---------------|-----|-----------|
| 1 | Core identity — AI Company Builder / agentic AI engineering | **Core-adjacent** | REA is agentic AI applied to a new work domain, with Evidence records + coverage caveats mirroring our honesty-badge/evidence discipline (§4; ADR-020 claim rules). It extends the proof laboratory rather than changing the category. |
| 2 | Intellectual territory — Agentic AI Use Cases | **Core-adjacent** | "Where should agents be deployed to create measurable value?" — software assurance/analysis is a legitimate, high-value answer with a named tool ecosystem to cite. |
| 3 | Intellectual territory — AI Governance & Policy | **Core-adjacent** | Dual-use governance of agentic reverse engineering is squarely inside our third territory. The hard questions (authorization, data egress, model-provider policy) are governance questions we already own language for (Four Reservations, 5-tier HITL). |
| 4 | Portfolio A/B/C archetypes (`03-operating-model.md` §2.2) | **Adjacent** | A consulting service line is not one of the three venture archetypes. Recurring RE-evidence workflows would eventually map to **B (B2B AI Workflow)** or **C (Sovereign Data — in-country/on-prem analysis of regulated targets)**, not A. |
| 5 | Sector matrix priorities (Finance/Gov/Donor P1) | **Adjacent** | Finance (payment-app fraud, mobile-money fraud tooling), Government (sovereign software assurance), and regulated fintechs are plausible first buyers — but "reverse engineering" is not a listed high-value play in `02-sector-positioning.md` §2. It would be a *new* sector-adjacent offer, not an existing thesis. |
| 6 | Four Reservations / Trust-by-Engineering | **Adjacent (conditional)** | Reservation 4 (AI skepticism) is answered naturally: reproducible snapshots, immutable evidence, stated coverage — audit-grade by construction. Reservation 2 (data protection) is *cut against* by default: analysis results flow to the agent's model provider (§3/S2) — client binaries reaching a third-party LLM is a policy decision we must answer before selling. |
| 7 | Malawi/SADC market demand now | **Stretch** | Local software-shop market sells custom builds + "AI services lines" (`02-sector-positioning.md` §3); no visible local RE-services competitor — but also no visible local demand signal. Demand must be validated (15–20 buyer calls per studio cadence), not assumed. Region-level cybersecurity policy instruments should be re-verified before citing in any client-facing doc. |
| 8 | Recurring-product potential | **Adjacent** | REA's snapshots + Evidence records are naturally productizable (monitored dependency/app-binary attestations, "what changed between versions" feeds) — but this is a *future* shape behind validation gates, not a day-one revenue line. |
| 9 | Revenue timing / near-term contribution | **Stretch** | First 90 days produce proof and pipeline, not material revenue. Budget accordingly; this is a capability bet, not a forecastable Q4 line. |
| 10 | Brand/positioning dilution risk | **Adjacent (manageable)** | "We reverse-engineer anything" reads as hacker-for-hire and conflicts with the do-not-position-as list if framed as technical stunt work. Framed as *governed software assurance*, it reinforces rather than dilutes the category. See §6. |

**Fit summary:** Strong on identity, territories, and governance narrative (3× core-adjacent); medium on portfolio/market mechanics (adjacent); weak on near-term demand and revenue (2× stretch). The stretches are validation problems, not identity problems — which is exactly what the studio's Discovery→Validation gates exist to resolve (`03-operating-model.md` §3).

---

## 2. Build-vs-Partner-vs-Adopt

**Reframe:** REA is MIT-licensed and free (§2/S3). "Build vs buy" does not apply to the software — nobody should build another agent-to-Ghidra harness. The real question is where *service capability* comes from.

| Option | What it means | Pros | Cons |
|--------|---------------|------|------|
| **(a) Adopt REA as tool + build service capability** | Pin `rea-agents`, wire into our agent stack, build our own engagement playbooks: scoping, authorization, evidence packs, sector packaging, HITL review, pricing. Human RE expertise added on the delivery path (hire or contract). | Full margin control; capability compounds inside the studio engine (shared HITL/audit/evidence stack, `03-operating-model.md` §2.1); differentiates on *delivery discipline* not RE tricks; MIT license, zero licence cost for the harness itself. | We start with zero RE specialists on roster (verified, §4); build takes time; we own version-pinning/supply-chain upkeep of a fast-moving repo (6.5.0, multiple releases/week, 1,207 open issues — §5). |
| **(b) Partner with an existing RE/security firm** | Resell or co-deliver: they do depth analysis, we wrap governance/orchestration/evidence layer; or subcontract surge capacity. | Instant depth; lower hiring risk; validates demand cheaply. | Margin share on the core work; our differentiation collapses to "project manager for someone else's analysts"; partner dependency becomes the new bus factor; knowledge doesn't compound in the studio. |
| **(c) Don't play** | Shelve REA after feasibility. | Zero risk, zero effort; keeps us in listed lanes only. | Forecloses a genuine core-adjacent adjacency where our evidence+governance stack is unusually well matched; cedes the "governed agentic analysis" narrative to whoever takes it first. |

**Recommendation: (a) — adopt REA and build service capability — with (b) as a bridging mechanism, not a posture.**

Reasoning:
1. The scarce asset is not the tool (free, MIT) and not raw RE technique (a one-person-with-Ghidra competitor owns that). The scarce asset in Malawi/SADC is *trusted, auditable, governed delivery of analysis work for regulated institutions*. That is precisely our existing stack: HITL, ApprovalGate, audit trails, honesty badges, MWK/mobile-money-aware GTM.
2. Partnering as the primary posture (b) gives away the compounding. Under the studio model, shared-core-before-differentiation is an operating decision (`03-operating-model.md` §5) — a partner-delivered service that never touches our orchestration/governance core teaches the studio nothing.
3. But (a) without a human RE lead is a house of cards (§4). So (a) *includes* hiring/contracting one RE specialist and/or a bench arrangement — partner capacity in a supporting role, capability in-house as the spine.
4. (c) is only right if validation fails — i.e., if the 15–20 buyer-discovery calls in the Validation window come back empty. That is the built-in exit, not a decision needed today.

---

## 3. Portfolio Placement

**Today:** a **consulting offer** — a new service line under existing consulting (one-off engagements: authorized analysis, software/asset due diligence, evidence-backed findings reports), not a product, not a venture.

**Evolution path (stage-gated, not committed):**

| Stage | Shape | Archetype fit | Gate to advance |
|-------|-------|---------------|-----------------|
| Now → Day 90 | Consulting service line (pilot engagements) | none yet — service line, not a venture | Discovery exit: written thesis + named owner (`03-operating-model.md` §3) |
| Validation | Repeatable engagement playbook + priced packages | — | 15–20 buyer calls; ≥N design-partner LOIs or paid-pilot intent |
| Build | Productize the *workflow* (intake → governed analysis → evidence pack → review) as recurring revenue: monitored binary/app attestation, version-diff monitoring for fintechs/telcos | **Portfolio B** (repeatable multi-step process; pulls workflow engine + durable state + connectors) | PoC on real data shape; ATC baseline; HITL gates live |
| Scale option | Sovereign/on-prem analysis for government & regulated clients (client binaries never leave in-country) | **Portfolio C** (sovereign data, local models, residency controls — maps to Finance/Government P1 sectors) | Scorecard green per Part 5 |

**New company/venture candidate?** **Not yet — and by rule not now.** Ventures are stage-gated spin-outs, and Portfolio D criteria explicitly require A–C scorecards green for two consecutive quarters (`03-operating-model.md` §5). REA-based work should initially run as a service line inside the operating company; it becomes a venture candidate only after Validation, and then only as a **B- or C-shaped** entity (it is not a consumer play — it does not belong to any "Portfolio D / Consumer Platforms" framing). Recommendation: record it in the studio Discovery backlog; do not open a venture track in this phase.

---

## 4. Capability Moat vs House of Cards

### What actually differentiates us (vs. a one-person with Ghidra)

| Claimed differentiator | Evidence it's real | Honest caveat |
|------------------------|--------------------|---------------|
| **AI orchestration at scale** — 90-agent hierarchy, MessageBus, 5-tier HITL, immutable audit (`02-sector-positioning.md` §3) | Internal proof stack exists and is tested (2,373 regression tests, 90 agent configs — ADR-020/033 discipline) | Orchestration is our strength, but REA itself already ships session isolation + evidence plumbing (§3) — a client can get "agents + Ghidra" without us. Our value-add must be the *governed engagement*, not the wiring. |
| **Evidence discipline** — honesty badges, no fabricated metrics, snapshots keyed by bytes+params+provider (§4/S6) | REA's Evidence record and our ADR-020 claim rules converge on the same principle | A one-person RE contractor also produces evidence; ours is institutionalized and auditable, theirs is personal reputation. That difference matters to banks/regulators, not to hobbyists — price accordingly. |
| **Regional trust & access** — Malawi-first, MWK pricing, mobile-money/WhatsApp-native, DPA 2017/2024 rigour (`02-sector-positioning.md` §5) | Stated wedge; no local RE-services competitor visible in competitive baseline (§3 of sector doc) | Trust is necessary, not sufficient: a bank buying software assurance buys analyst credibility first. |
| **Sector knowledge** — Finance/Government P1 priorities, regulated delivery experience | Stated in sector matrix | Not yet RE-specific. Sector knowledge + RE depth must be combined on the delivery team. |
| **Governance layer** — ApprovalGate, authorization scoping, walk-away rules (§5 below) | Exists (ApprovalGate is live per AGENTS.md §9.1) | Governance only counts if enforced at engagement intake — needs a new acceptance gate (§5). |

### Honest weaknesses (the house-of-cards side)

1. **No reverse-engineering specialist on the roster — verified.** `company-registry.yaml` Security department contains: CISO (executive; CISO of record is the Human CEO per AGENTS.md §9.2), `security_compliance_lead`, `ai_security_specialist`, `incident_response_lead`, `devsecops_lead`, `security_architect`, plus approval-gate/risk specialists. The only `red_team_engineer` sits in **AI Research** and is scoped to *agent* adversarial testing (prompt injection, jailbreaks, goal misalignment — registry lines 2003–2045), not binary/software reverse engineering. **There is no RE, malware-analysis, disassembly, or threat-intel role anywhere in the registry.** Until one exists (hire/contract), we are a delivery harness, not an analysis authority — client findings would carry no named expert signature.
2. **Bus factor of REA itself:** primary author holds ~53% of top-contribution commits; 6 months old; multiple releases per week with documented breaking surface (`migration-6.2.md`, fail-closed IDA tool renames) and 1,207 open issues (§5). Mitigation: **pin versions**, treat upgrades as change-managed events, keep CLI JSON interfaces as our abstraction seam so we can swap engines.
3. **Windows-only estate vs. Linux-shaped coverage:** our development/runtime estate is Windows 11/PowerShell 5.1 (AGENTS.md §12, environment). Windows Ghidra analysis is **experimental P0 read-only** (§2/S9); several target classes (firmware, packet captures, signal recordings, recorded crashes) are **Linux-only** (§1). Also Node ≥22.19/24.11/26+ is a hard prerequisite. We need at least one validated Linux analysis node before selling breadth.
4. **No commercial engine licences:** IDA Pro / Hopper / JEB are user-obtained; REA grants no tool licence, and cracked copies are explicitly unauthorized (§2/S2). Free stack = Ghidra (Apache-2.0) + Kuna (Apache-2.0). Fine for an MVP tier; premium depth tiers cost money and procurement time.
5. **Data egress by default:** analysis runs locally, but results flow to the agent's model provider (§3/S2). Our stack routes through third-party LLM providers (AGENTS.md §11 keys). Shipping client binaries/decompiled code to a third-party model violates the spirit of Four Reservations #2 unless we stand up a local/sovereign model path or contract it explicitly.
6. **Price competition:** a one-person with Ghidra undercuts us on price for pure analysis. We must never sell "decompilation hours"; we sell governed assurance with evidence, authorization discipline, and audit-grade reporting — and we must be honest that depth-of-technique is not our day-one differentiator.
7. **No ethics/dual-use policy on file:** grep across `docs/` for "ethics review / dual-use / export control" returns no matches. ApprovalGate bounds *operations*, not *engagement acceptance*. §5 fixes this as a condition.

**Verdict:** The moat is real but **conditional and thin today**: governance + evidence + regional trust + sector knowledge, stacked on top of a tool we did not build and skills we do not yet staff. Without the RE specialist and the data-egress answer, this is a house of cards with good branding. With both, it is a defensible, category-consistent offer that a lone RE contractor structurally cannot replicate for regulated buyers.

---

## 5. Risk Appetite & Governance

**The dual-use optics problem:** reverse engineering is lawful and legitimate (interop, audit, preservation, security research — REA's own responsible-use positioning, §2/S2), but in the Malawi market a service line advertised as "we take software apart" invites the wrong first impression: hacker-for-hire, espionage, or piracy tooling. That would directly damage the trust wedge we are building with banks, government, and donors. The service must therefore be *born governed*, and its public framing must lead with authorization and assurance (§6).

**How our governance bounds it:**

| Control | Mechanism | Status |
|---------|-----------|--------|
| **Engagement acceptance gate (new — required before first client work)** | Every RE engagement passes: (1) signed client authorization + scope statement; (2) lawful-purpose check; (3) data-egress classification (does client code touch a third-party model?); (4) CISO sign-off (Human CEO, per AGENTS.md §9.2) for any cross-border/sensitive target; (5) named human RE lead accountable for findings. Enforced through ApprovalGate PENDING→APPROVED flow; expired/unapproved = no work (AGENTS.md §9.1). | **To be established — condition of GO** |
| **5-tier HITL / audit** | Findings reports reviewed by human before delivery; immutable audit of analysis runs. | Exists — extend to RE engagement records. |
| **Third-party transmission ban** | AGENTS.md §9.2: no local data to non-allow-listed vendors. Client code to model providers falls under this — default to allow-listed provider with contractual no-training terms, or local model. | Exists — needs an RE-specific ruling in the acceptance gate. |
| **Version pinning / supply chain** | Pin `rea-agents`; upgrades via change-managed bump; official channels only (README warns of look-alike repos, §2/S2). Supply-chain posture of REA itself was NOT audited in Phase 1 (UNVERIFIED in shared brief) — audit before first external engagement. | New working rule. |

**Walk-away rules (non-negotiable):**
1. No signed authorization from the software's owner/mandated party (or their lawful agent) → no engagement.
2. Requests involving unauthorized access, credential theft, exploit development for attack, DRM/key bypass, or analysis of pirated/cracked software → decline (REA itself declares cracked keys unauthorized, §2/S2).
3. Offensive or espionage-flavored work for any state or non-state actor outside a licensed, reviewed scope → escalate to Human CEO; default decline.
4. Targets whose analysis would require shipping client-identifiable code to an unapproved model provider with no contractual protection → decline or re-scope to local analysis.
5. Any engagement whose public association would plausibly breach the brand's trust wedge (named-in-press harm) → CEO decision, recorded.

**Risk appetite statement:** We accept *reputational and delivery* risk on a small number of tightly governed pilots (bounded, authorized, evidence-disciplined). We do not accept *regulatory, licensing, or dual-use* risk — no gray-zone engagements, ever. Appetite expires automatically if conditions in §7 are unmet.

---

## 6. Positioning Narrative

### Three candidate positioning statements

**Tone 1 — Technical credibility**
> "We don't give you opinions about your software — we give you reproducible evidence. LightSpeed runs AI agents through proven reverse-engineering engines under a governed pipeline: every finding is snapshot-keyed, coverage-stated, and auditable, from binaries to apps to captures — software assurance that holds up to review."

**Tone 2 — Trust / safety-first**
> "Reverse engineering, done with permission and on the record. LightSpeed's governed analysis service works only inside signed scopes, under human review, with your code never used for model training — the disciplined way for regulated institutions in Malawi and SADC to understand what they deploy, acquire, or inherit."

**Tone 3 — Regional partner**
> "Malawi and SADC institutions are buying, inheriting, and integrating software they cannot inspect. LightSpeed brings AI-native software assurance to the region — locally delivered, evidence-backed, priced for this market — so banks, telcos, fintechs, and public institutions can verify rather than trust."

*(All three deliberately avoid "we reverse-engineer anything" stunt framing, which conflicts with the do-not-position-as list and the trust wedge.)*

### How Pharos (Human CEO thought leadership) should treat this topic

- **Territory:** file under **AI Governance & Policy** (primary) and **Agentic AI Use Cases** (secondary). Never under "security researcher" or personal technical expertise — Jack's platform is institutional design, not disassembly.
- **Frame:** the story is *"what happens when AI agents can take software apart — and why institutions need governed analysis, not just capable analysis."* This is a Four Reservations story (skepticism + data protection answers) in a new domain, which is exactly the repeatable rhetorical structure Pharos already owns.
- **Suggested flagship angle:** "Governed Reverse Engineering: authorization, evidence, and the AI agent" — a thought-leadership piece arguing that the barrier in African markets isn't analytical capability (open-source tools solved that) but *trust, evidence, and accountability*. Supports territory 3, feeds category claim.
- **Cadence discipline:** one flagship article + one LinkedIn series segment inside the existing calendar; no premature "we launch RE services" claims before Validation gates pass (ADR-020 honesty rules: no fabricated client metrics, no launched-offer claims).
- **Audience:** CFO/CIO/CISO circles in banking and telco, and AI-policy audiences — not the security-tooling community (we are not trying to win that crowd; single-engine tool maintainers own it, §6 of shared brief).

---

## 7. Recommendation

# GO-WITH-CONDITIONS

Proceed with Phase-2 technical/economic validation and stand up REA as an adopted internal capability with a consulting-first offer — **only** under the enumerated conditions below. This is a capability-and-validation bet, not a revenue commitment.

### Conditions (all must hold; breach = park)

1. **Human RE specialist on the delivery path before any client engagement.** Hire, contract, or partner-bench one named reverse-engineering lead who signs findings. No agent-only, unsupervised RE deliverables to clients. (Registry verification, §4: no such role exists today.)
2. **Engagement acceptance gate established and wired through ApprovalGate** — signed authorization, lawful scope, data-egress classification, CISO (Human CEO) sign-off for sensitive targets, walk-away rules (§5) enforced before any PENDING→APPROVED analysis work. No gate, no engagements.
3. **Data-protection answer in place before external targets are accepted** — client code/binaries do not reach third-party model providers without contractual no-training protection or a local/sovereign model path (Four Reservations #2; AGENTS.md §9.2 transmission ban).
4. **Toolchain hardening:** `rea-agents` version pinned; upgrades change-managed; supply-chain posture audited; at least one validated Linux analysis node alongside the Windows estate (Windows Ghidra is experimental P0; several targets are Linux-only); commercial engines kept licence-clean or excluded from tier-1 scope.
5. **Stage-gate discipline:** Discovery → Validation gates from `03-operating-model.md` §3 apply verbatim. **Empty buyer discovery (15–20 calls, no LOIs or paid-pilot intent) = park the offer (NO-GO by evidence, not by debate).** No new venture track opened until Validation exits green; portfolio B/C placement only at Build stage.

### 90-day strategic milestones (2026-10-17 → 2027-01-15)

| Window | Milestone | Owner | Exit evidence |
|--------|-----------|-------|---------------|
| **Days 1–30** | Write engagement-acceptance policy draft (§5 controls) + walk-away rules; get CEO/CISO approval | CSO + CISO (Human CEO) | Signed policy in repo; ApprovalGate wiring spec |
| **Days 1–30** | Pin `rea-agents`; spike results land from technical stream (Windows Ghidra P0 validation, Linux node decision, engine tiering) | CTO stream (tech feasibility doc) | Pinned version + spike report with pass/fail per target class |
| **Days 31–60** | RE capability secured: lead identified, offer accepted (hire/contract/bench MOU) | CSO + CHRO/People | Named RE lead on delivery plan |
| **Days 31–60** | Buyer discovery: 15–20 structured calls (banks, telcos, fintechs, gov, donors) against sector matrix | CSO + Sales | Call log + LOI/paid-pilot-intent count |
| **Days 31–60** | Positioning package: pick/lock tone from §6 three statements; Pharos flagship piece drafted | CSO + CMO/Pharos | Locked statement; drafted article in calendar |
| **Days 61–90** | One governed internal pilot (our own artifacts / authorized sandbox target) delivering a full evidence pack under the new acceptance gate | RE lead + Delivery | Reproducible evidence pack + audit record |
| **Days 61–90** | One external design-partner conversation advanced to paid-pilot intent (not required to close) | Sales | Written intent or documented decline reason |
| **Day 90** | **Gate review:** GO to service-line launch / park / re-scope — decision recorded in ECL/board track | CSO → CEO | Recorded gate decision with the §7 evidence attached |

### Final recommendation (restated)

**GO-WITH-CONDITIONS** — adopt REA (option a) with partner capacity as bridge, place it first as a governed consulting service line (portfolio B/C only after validation), and treat it as a thought-leadership and capability bet under strict engagement governance. The three conditions that make or break it: **(1) a named human RE specialist on every delivery, (2) an enforced engagement-acceptance gate covering authorization and data egress, and (3) stage-gated buyer validation that gives us explicit permission to walk away.**

---

*End of strategy stream (07). Downstream streams: cite this document; contradicting it requires a recorded gate decision, not an inline edit.*
