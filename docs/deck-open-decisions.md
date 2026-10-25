# Pitch deck — ten open decisions

**Status:** blocking. The deck is structurally finished (PR #522, 11 slides) but carries **no business figures**, because `docs/claims.yaml` has 29 claims and **zero** with `status: verified`.

**Date:** 2026-10-25
**Prepared by:** CFO, CTO, CSO, CLO, Head of BD, QA Lead, Board Risk (agent review), consolidated here.
**Owner of this document:** CEO. Each item below is a tick-box, not a discussion paper.

---

## How to use this

Every figure that could go on the deck is either contradictory in the repo or unattested. The deck cannot move from `INTERNAL DRAFT` to investor-ready until each item is answered, because `verify-deck.py` refuses any number that is not a `verified` claim in `docs/claims.yaml`.

Each item gives: what the repo currently says (with `file:line`), the recommended answer, and what it unblocks. Reply with the recommendation accepted or replaced.

---

## 1. Starter price

**Repo says:** three different answers for what looks like one product.

| Value | Source |
|---|---|
| `$49/mo` | `docs/claims.yaml:66` (`placeholder`, note "Pricing is a decision") |
| `$199/mo Professional`, `$49 Starter` | `docs/sop/sales-sop.md:206-207` |
| `~$2,000 one-off + ~$200/mo` (Offer E) | `docs/client-facing/USE-CASE-CATALOG.md:169,176`; `docs/service-catalog-malawi.md:80` |
| `$15K/yr + $250/mo` (Offer F, sold to consulting firms) | `docs/ai-caas-pricing-model.md:41` |

These are three different products. `$15K/yr` is a *firm* licence, not a self-serve tier. `$49/mo` is unsourced and unreconciled against two commercial docs.

**Recommend:** show `~$2,000 one-off + $200/mo` as the platform offer (two documents agree) and `$15K/yr + $250/mo` as the consulting-firm licence. Retire `$49/mo` unless a genuine self-serve tier exists.

**Unblocks:** the pricing line on Product & Business Model; `price-starter`, `price-pro`, `price-enterprise` in `claims.yaml`.

---

## 2. Year-one revenue

**Repo says:** two numbers that are actually different metrics.

- `$120K` — `docs/claims.yaml:144` (placeholder). Traced to `static/brand/templates/brief.json:122`, built as `$10K/mo` and labelled `ARR run-rate` at `:149`.
- `~$50–85K gross revenue by month 12` — `docs/MISSION_AND_VISION.md:139,148`, CEO-approved at `:218`.
- `$600K` Year 3 — `brief.json:124`.

`$120K` as *year-one revenue* is impossible at `$49/mo` (204 subscribers) and is a run-rate in its own source.

**Recommend:** report `$50–85K` year-one gross revenue, and if useful `$120K exit ARR run-rate` — labelled as a run-rate, not revenue.

**Unblocks:** the Financials content now folded into The Ask; `arr-120k`, `arr-600k`.

---

## 3. LLM/infra cost as share of revenue

**Repo says:** `~15%` (`claims.yaml:162`; `brief.json:67,128`) versus `≤10%` (`docs/MISSION_AND_VISION.md:142,163`; `docs/ai-caas-pricing-model.md:100`).

`≤10%` is a CFO-tracked monthly guardrail in two governing documents. `15%` appears only in template text. Actual measured spend: **no source**.

**Recommend:** `≤10%` as the guardrail. Do not publish an actual spend figure until the cost tracker records one (`cost_tracker.json` currently shows `total_spent 0.0, call_count 0`).

**Unblocks:** unit-economics line; `llm-cost-15`.

---

## 4. Gross margin

**Repo says:** `70%+` (`claims.yaml:156`; `brief.json:66`) versus `70% minimum` scoped to **enterprise tiers only** (`docs/EXECUTIVE-STRATEGY-EXPANSION.md:12`) versus `60–75% blended, reject below 55%` (`docs/ai-caas-pricing-model.md:27,102`).

`≥60%` is **not stated verbatim anywhere** in the repo.

**Recommend:** publish `70%+ platform / 55–60% services floor`, or `60–75% blended`. Not a single unscoped `70%+`.

**Unblocks:** unit-economics line; `gross-margin-70`.

---

## 5. The ask — and what `$500K` actually means

**Repo says:** `$500K` is a **spend cap**, not a raise.

- `docs/CEO-DIRECTIVE-BLUEPRINT-ADOPTION.md:168` — "CAPITAL ALLOCATION GUIDANCE: **FIRST $500K OPERATIONAL SPEND**", "Guardrails for the first $500K across four pillars" (`:170`).
- No instrument, valuation or dilution is recorded anywhere.
- "Raising $500K Seed" appears in `brief.json:139` and `generate-keynote.py:625,875` — template artefacts misquoting §7.

Arithmetic on §7's own ranges: hardware `75–125K` + talent `200–250K` + pilots `100–150K` + compliance `50–75K` + reserve `50K` = **`$475K–$650K`**. `$500K` funds only the floor of the stated plan.

**Recommend:** either ask `$650K` (top of the documented plan) or keep `$500K` and publish a scope-reduced plan. Add instrument and runway — the deck currently says "pending board decision", which is the weakest slide in the deck.

**Unblocks:** The Ask; `seed-ask`.

---

## 6. Attest or retract: ATC >90%

**Repo says:** nothing supports it. The collector is real; the data is empty.

- Formula `clean/terminal*100`, target 90.0 — `src/ai_company/dashboard/kpis/studio.py:176-185`, `:138`.
- Every table in `data/ai_company.db` has **0 rows**.
- The real hash-chained trail (`reports/evidence/audit-2026-10-0{1,3,4}.jsonl`) has 171 events, 6 task ids, and **zero** `task_completed`/`task_failed` — no denominator.
- The only computable rate is in `.opencode/audit.synthetic-2026-10-10.jsonl` — 10 completed / 8 failed = **55.6%**, explicitly synthetic.

**Recommend:** RETRACT as achieved; re-label as a target.

**Unblocks:** trust. A number that diligence disproves in an afternoon is worse than no number.

---

## 7. Attest or retract: capital efficiency (3.5x / 3x / 4.2x)

**Repo says:** three competing variants, all tracing to one phrase — "capital efficiency 3–5×" in `ai_venture_studio_client_presentation.md:19`.

Inputs are all zero or unratified: `company/studio_tracker.yaml` has `ratified: false`, `contracted_arr_usd: 0.0`, `capital_consumed_usd: 0.0`; `cost_tracker.json` shows `total_spent 0.0`; `revenue_transactions` has 0 rows.

**Recommend:** RETRACT all three variants. Same for `velocity-mvp-45d` (no source anywhere) and `correction-ratio 8 per 1,000` (spec says baseline-first; no target exists).

**Unblocks:** nothing on the deck. This is a claims-register cleanup.

---

## 8. Market sizing

**Repo says:** `$65B TAM / $12B SAM / $120M SOM` are all placeholders with no source. The binding constraint is not market size — it is delivery capacity: the board capped year one at 20–25 clients (`docs/MALAWI_FOCUS_ALIGNMENT.md:99,106`).

Inputs that **do** exist: 20–25 paid clients (`docs/MISSION_AND_VISION.md:149`), win rate >25% (`docs/sop/sales-sop.md:285`), average deal >`$2,000` (`:286`), Offer E price (`USE-CASE-CATALOG.md:169`).

Computable now: `22 × $2,000 = $44K` to `25 × $3,400 = $85K` — which lands at the *bottom* of the stated year-one band. The top of that band needs a `~$3.4K` average deal; that gap is worth knowing before it is asked about in a meeting.

TAM/SAM require external research the repo does not contain (CONGOMA NGO register, RBM bank register, ITU/World Bank ICT-spend data). One cited source is also **missing from the repo**: `results/pestel-lightspeed-2026.md` is referenced by at least six documents and does not exist, so the "~1.6m MSMEs" figure must not be used.

**Recommend:** show a capacity-derived SOM only (`$44–85K`), label TAM/SAM "pending external research". A defensible small number beats an unsourceable large one.

**Unblocks:** the market slide; `tam-65b`, `sam-12b`, `som-120m`.

---

## 9. Who may be named on the team slide

**Repo says:** one human (Jack Mlusu), seven agent executives, and a "Board of Directors" that never states it is composed of agents.

Board Risk and QA both flagged this as the deck's biggest credibility risk: a reader who works out these are registry entries re-reads everything else as inflated. The underlying capability is real and defensible — it just belongs on the product slide.

**Recommend:** name the founder plus any human advisors/contractors; move the agent cabinet to the product slide as proof ("the org chart we generate"); relabel or delete "Board of Directors / standing committees".

**Decision needed:** are there any human advisors, contractors or directors who consent to being named? If none, the slide says one person.

**Unblocks:** Team slide rewrite.

---

## 10. Is there a paying pilot or LOI?

**Repo says:** none. No LOI, MOU, signed agreement, invoice, deposit or paid pilot exists anywhere in the repository. Only blank templates (`docs/legal/msa-template.md`, `docs/sow-template.md`, `docs/templates/invoice.md`).

Soft, non-binding, citeable:
- **J&S StopOver Bar** — a real SME running agentic pricing support, explicitly unpaid (`content/pharos-2026-10-12/05-dual-economy-ai-pricing.ts:79`).
- Pilot-stage workstreams, none contracted: agriculture 1,200 members; University of Malawi 3 departments; donor reporting "no signed engagement with named INGO yet" (`data/sectors/registry.ts:132`).
- Prospect list only: four NGO contacts, every outcome blank, CONGOMA "not-contacted" (`docs/venture-studio/12-T3-call-scripts.md:110-118`).

**Recommend:** keep "no paying clients, no signed pilots, no revenue" — it is accurate. The strongest honest version is "one live unpaid production deployment (J&S StopOver Bar); three pilot-stage workstreams, none contracted; zero revenue".

**Decision needed:** confirm that wording, and confirm no commitment exists outside the repo that we should be citing.

---

## Already fixed — no decision required

Applied in PR #522 after a legal review of the deck:

| Was | Now | Why |
|---|---|---|
| Malawi DPA 2017 | DPA 2024 | Operative act is Act No. 3 of 2024, in force 3 June 2024 (`docs/marketing/newsletter/monitor-01.md:61`) |
| "SOC 2 readiness" | "SOC 2 planned, not certified" | SOC 2 is an unchecked task; no attestation exists |
| "GDPR opinion" | dropped from capability claims | Only artefact is a budget line to buy one (`CEO-DIRECTIVE-BLUEPRINT-ADOPTION.md:179`) |
| "Governance gates operating under audit" | "live with tamper-evident audit trail" | No external audit engagement exists |
| "Human approval gates ratified" | "enforced in code" | Tiers 0–4 enforced pre-execution in `src/ai_company/executor/tool_runner.py:18-19,463` |
| "agent registry in production" | "running this company internally" | Nothing is in production without a client |

Two shell documents were verified as genuinely backed by code and left alone: the five-tier approval matrix (`src/ai_company/orchestrator/tier_rules.py:1-10,29-35`) and the hash-chained audit trail (`src/ai_company/audit/integrity.py:1-6`).

---

## Needs engineering, not a decision

The KPI instrumentation is ~90% written — schema, collector, spec and an explicit `no_data` honesty contract in `studio.py`. What is missing is data production, roughly 2–3 engineering days plus a CFO signature:

1. executor persists terminal task status (including `manual_intervention`) to `tasks`
2. `venture_id` added to tasks and audit events (deferred at `studio.py:20-21`)
3. continuous audit trail
4. CFO ratifies `company/studio_tracker.yaml`
5. 30 baseline days (`instrumentation_start: 2026-10-07`, day 19 at time of writing)

Until then every KPI in `studio.py` correctly returns `no_data`.

---

## Repo contradictions found during this review — fix separately

These are published claims that contradict the deck. They are not deck issues, and they were not touched:

1. `data/faqs/registry.ts:251` — "LIVE: Paying client… (compliance automation for regional financial institution)". No client, value or date exists. **On a public site.**
2. `src/data/siteContent.ts:286-294` and `data/sectors/registry.ts:36-40` — "Malawi Central Bank Compliance Automation … **Deployed** … Q2 2026", badged "Proven in-house".
3. `data/metrics/registry.ts:96-104` — asserts **97.4%** task success rate at "proven-in-house", sourced to "orchestrator metrics", against an empty database.
4. `data/claims/registry.ts:113` — cites `reports/evidence/jss-bar/`, which does not exist.
5. `docs/legal/privacy-policy.md:295` — controller address still `[Company address]`.

Items 1–3 are the same failure the deck gate exists to prevent, in places the gate does not cover. Recommend the CMO and CTO treat them as a single corrective PR.
