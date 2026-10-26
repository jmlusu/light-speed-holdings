# Deck decisions — CEO record

**Date:** 2026-10-26
**Decision owner:** Jack Mlusu, Human CEO
**Supersedes the open items in:** `docs/deck-open-decisions.md`
**Authority for:** figures marked `verified` in `docs/claims.yaml` with
`record: docs/decisions/2026-10-26-deck-decisions.md D-xx`

## How this was recorded

The ten recommendations in `docs/deck-open-decisions.md` were put to the Human CEO
in an OpenCode session on 2026-10-26. The CEO answered:

- **"Accept all ten recommendations."**
- On item 5, asked which branch: **"$650K full plan."**

This file records what was accepted. It is a decision register, not a financial
model: each entry states the figure that may now appear on the deck, and where the
underlying fact lives in the repository.

---

## D-01 — Pricing

**Decided:** publish two products, retire the self-serve tier.

| Product | Price | Source of the price |
|---|---|---|
| Platform licence | `$2,000` one-off + `$200/mo` support retainer | `docs/client-facing/USE-CASE-CATALOG.md:169,176` |
| Consulting-firm licence | `$15K/yr` + `$250/mo` | `docs/ai-caas-pricing-model.md:41` |

`$49/mo`, `$149/mo` and `$299/mo` are **retired**. They were template artefacts with
no product behind them. No self-serve tier exists, so none is published.

## D-02 — Year-one revenue

**Decided:** report `$50-85K` gross revenue by month 12, and `$120K` only as an
**exit ARR run-rate**, never as revenue.

- Gross revenue: `docs/MISSION_AND_VISION.md:139,148` (MWK 90–150M).
- `$120K` is labelled `ARR run-rate` in `static/brand/templates/brief.json:149`; it is
  not a revenue figure.

## D-03 — LLM and infrastructure cost

**Decided:** publish `≤10%` of revenue as a **guardrail**, not as measured spend.

`docs/MISSION_AND_VISION.md:142` sets "LLM + infra ≤ 10% of revenue". The `~15%`
figure in template text is withdrawn. No actual spend figure is published: the cost
tracker records zero calls, so there is nothing to report.

## D-04 — Gross margin

**Decided:** `70%+` on the platform, `55-60%` floor on services.

The single unscoped `70%+` is withdrawn. `70%+` is scoped to platform revenue;
services carry a lower floor, consistent with the 55% modeled-margin floor in
`docs/ai-caas-pricing-model.md:102`.

## D-05 — The ask

**Decided:** ask `$650K`.

`$500K` is the first operational spend cap in
`docs/CEO-DIRECTIVE-BLUEPRINT-ADOPTION.md:168`, not a raise. The documented plan
arithmetic is: hardware 75–125K + talent 200–250K + pilots 100–150K + compliance
50–75K + reserve 50K = `$475–650K`. The CEO selected the top of that plan.

**Not decided by this record:** instrument (equity/SAFE/other) and runway. The deck
states that they are not yet set and does not imply either.

## D-06 — ATC >90%

**Decided:** retract as achieved; it may be described as a target only.

There is no denominator: every table in `data/ai_company.db` has 0 rows and the
hash-chained trail has zero terminal task events. The only computable rate (55.6%)
comes from a file explicitly marked synthetic.

## D-07 — Capital efficiency, velocity, correction ratio

**Decided:** retract `3–5×`, `3×`, `4.2×`, `<60d`, `<45d` and `8 per 1,000`.

All trace to template text or unratified trackers: `company/studio_tracker.yaml` has
`ratified: false`, `contracted_arr_usd: 0.0`, `capital_consumed_usd: 0.0`.

## D-08 — Market sizing

**Decided:** publish a capacity-derived SOM only; label TAM and SAM as pending a
cited report.

- SOM: `$44-85K`. Floor = `22` clients (midpoint of the `20-25` delivery cap,
  `docs/MISSION_AND_VISION.md:140`) at the `$2,000` average deal
  (`docs/client-facing/USE-CASE-CATALOG.md:169`) = `$44K`. Ceiling = the board's own
  `$85K` gross-revenue target for month 12 (`docs/MISSION_AND_VISION.md:139,148`).
- No per-deal figure above `$2,000` is assumed anywhere: the `~$3.4K` average deal
  that the open-decisions note said the top of the band needs is **not** published
  as an assumption.
- `$65B` TAM, `$12B` SAM and `$120M` SOM are withdrawn: no source exists in the repo.
- `results/pestel-lightspeed-2026.md`, cited by six documents, does not exist, so the
  "~1.6m MSMEs" figure is not used.

## D-09 — Team slide

**Decided:** name the founder only. The agent cabinet moves to the product slide as
proof that the org chart is generated, not as a leadership team.

No human advisor, contractor or director has consented to being named, so none is.
"Board of Directors / standing committees" is removed from the team slide: those are
registry entries, and presenting them as a board overstates the governance.

## D-10 — Paying clients

**Decided:** confirmed. No paying clients, no signed pilots, no revenue.

The honest formulation stands: one live unpaid deployment (J&S StopOver Bar, a
non-tech SME running inventory, procurement and pricing agents); three pilot-stage
workstreams, none contracted; zero revenue. `15+` pilot clients and `50+` enterprise
clients are withdrawn.
