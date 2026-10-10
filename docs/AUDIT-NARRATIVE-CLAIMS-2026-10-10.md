# Narrative Claims Audit — Clinic, NGO, Offer E Outcomes

**Date:** 2026-10-10
**Scope:** Audit external narrative claims against internal artifacts, then instrument the claimed outcomes (clinic, NGO, Offer E).
**Method:** Each outward-facing claim in `docs/NARRATIVE-AND-POSITIONING.md` was traced to the internal artifacts that would have to exist for it to be true (`docs/client-facing/USE-CASE-CATALOG.md`, `docs/legal/client-onboarding-policy.md`, `docs/MALAWI_FOCUS_ALIGNMENT.md`, `docs/Pharos/case-study-pipeline.md`, `src/data/siteContent.ts`). Verdicts use the evidence tiers in `docs/architecture/EVIDENCE_ARCHITECTURE.md` (T3 = human-approved case studies and outcome numbers; ADR-020 = no unqualified claims, no fabricated metrics).
**Instrumentation produced:** `company/narrative_outcomes.yaml` (metric definitions + claim gates for all three pillars), validated by `tests/unit/test_narrative_outcomes.py`.

---

## 1. Claim matrix

| ID | Claim (verbatim, abbreviated) | Claim source | Internal artifact evidence | Verdict |
|----|------------------------------|--------------|---------------------------|---------|
| CL-01 | "The Malawi clinic that now answers patients on WhatsApp" | `docs/NARRATIVE-AND-POSITIONING.md:29` | Health/M&E is "in pilot (composing evidence). No confirmed partnership with any named health organization has been signed" (`USE-CASE-CATALOG.md:229`, `:382`, `:518`); the WhatsApp patient channel is Offer B, **governance BLOCKED** (`client-onboarding-policy.md:36`, `:41`; `USE-CASE-CATALOG.md:116`, `:507`) | **UNSUPPORTED** — present-tense shipped claim; vehicle blocked, no signed partnership |
| CL-02 | "The NGO whose donor report lands on time instead of weeks later" | `docs/NARRATIVE-AND-POSITIONING.md:29` | Donor reporting is Offer C, **governance BLOCKED** pending liability-cap ratification (`client-onboarding-policy.md:37`, `:41`); the NGO lighthouse client is a *week 3–6 goal*, not a landed account (`MALAWI_FOCUS_ALIGNMENT.md:25`, `:144`) | **UNSUPPORTED** — vehicle blocked, client not landed |
| CL-03 | "The agency that licenses Offer E and builds for its own clients" | `docs/NARRATIVE-AND-POSITIONING.md:29` | Offer E is "Fieldable 2026 — proven in-house... ready for external licensing" with E2 "in active development with no public pricing" (`USE-CASE-CATALOG.md` Offer E section, `:510`); **no licensee recorded anywhere in the repo** | **UNSUPPORTED** — product readiness is not a licensee; zero licenses evidenced |
| CL-04 | "These are... shipped artifacts, measured in real time, and published with named metrics" | `docs/NARRATIVE-AND-POSITIONING.md:29` | Public evidence surface carries only ws-01..03 / oc-01..03 (compliance, agri coop, university) in `src/data/siteContent.ts` — no clinic, NGO, or Offer E entry; grep for the three claim sentences across README/site sources returns no match | **UNSUPPORTED** — no named metrics exist for any of the three pillars (baseline instrumentation now created; all `current: null`) |
| CL-05 | "LightSpeed Holdings serves Malawian clinics and health workers" (present tense) | `docs/NARRATIVE-AND-POSITIONING.md:153` (§8) | Same as CL-01; catalog honesty classification constrains claims to "fieldable 2026 or in pilot" (`NARRATIVE-AND-POSITIONING.md:92` citing `USE-CASE-CATALOG.md`) | **UNSUPPORTED as written** — serve relationship is pilot-stage, not signed |
| CL-06 | "Agentic AI is shipped into real clinic workflows... generating tangible impact data" | `docs/NARRATIVE-AND-POSITIONING.md:203` (§11) | Health/M&E workflow is described as a *composite* ("Monitor clinic supply chains...", `case-study-pipeline.md:30-34`), pilot per catalog | **UNSUPPORTED** — no clinic deployment, hence no impact data |
| CL-07 | "This is not a pilot; it is a running delivery engine" | `docs/NARRATIVE-AND-POSITIONING.md:27` | Directly contradicted by the document's own §3.9 honesty note (`:92`) and the catalog's fieldable/in-pilot classification | **MISLEADING framing** — overstates portfolio status |

**Aggregate:** all three named outcome pillars (CL-01..03) and every generalization built on them (CL-04..07) are unsupported by internal artifacts. The claims have **not** propagated to the public site or README (verified 2026-10-10), so the damage is contained to the internal canonical narrative.

## 2. Classifications

| Finding | Class |
|---------|-------|
| Publishing or reusing CL-01..CL-07 on any external surface as written | **BLOCKER** (would fail ADR-020 / T3 review; governance-blocked offers presented as delivered work) |
| Correcting `docs/NARRATIVE-AND-POSITIONING.md` | **REQUIRED DEPENDENCY** — the file is ECL-controlled ("Do not hand-edit... Edits must go through the ECL validate/close cycle", `NARRATIVE-AND-POSITIONING.md:225`); correction requires a harness change (`scripts/maintenance/harness-change.ps1 new`) |
| Reaching CL-01/CL-02 states at all | **REQUIRED DEPENDENCY** — three sources disagree on the Offer B/C gate: `docs/legal/client-onboarding-policy.md:36-41` and `client_intake.py:44` (`BLOCKED_OFFERS`) still block them, while `config/company/malawi_offers.yaml` shows `governance_state: approved` for all offers, `service_level_liability_cap.status: ratified` (2026-08-12), and `blocked_offers: []`. The policy's stated unblock condition is already met, yet the code gate is unchanged. A human/CLO decision must reconcile them before either pillar can move |

## 3. Out-of-scope findings (recorded only, not touched)

- `docs/architecture/EVIDENCE_ARCHITECTURE.md:7` baseline still names `workCaseStudies`, `workPolicy`, `honestyPolicy` — `src/data/siteContent.ts` now exports `proofCaseStudies`, `proofPolicy`, and has no `honestyPolicy`.
- ADR numbering: duplicate numbers `008`, `020`, `025`; missing `006`, `007`, `009`, `011` (`docs/adr/`).
- `docs/NARRATIVE-AND-POSITIONING.md` §9 list has duplicate/out-of-order item letters (c, d, c, d, e, f, h, i, j).

## 4. Instrumentation (the second half of the task)

`company/narrative_outcomes.yaml` instruments each claimed outcome the same way `company/studio_tracker.yaml` instruments venture gates:

- One entry per pillar: `clinic_whatsapp` (blocked), `ngo_donor_reporting` (blocked), `offer_e_licensing` (not_started).
- **Metrics** per pillar with `unit`, `owner`, `source`, and `formula`. Every `current` is `null` — per the CEO decision recorded in `config/company/kpis.yaml` (real sources only, no dummy values).
- **`claim_gate`**: the conditions that must all hold before the corresponding narrative claim may be restated as fact (signed partnership / ratified liability cap / recorded licensee / named metric with a non-null current / T3 human approval).
- **`governance_refs`**: file paths into the policy and catalog artifacts, checked for existence by the test.

**Verification:** `uv run pytest tests/unit/test_narrative_outcomes.py tests/docs/test_doc_drift.py` + `uv run ruff check tests/unit/test_narrative_outcomes.py` (mypy excludes `tests/`, see `pyproject.toml`).
