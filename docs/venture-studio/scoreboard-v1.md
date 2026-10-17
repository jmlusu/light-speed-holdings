# Studio Scoreboard v1 — Metric Sheet (T1 #417)

**Source:** `docs/venture-studio/05-kpi-scorecard.md` (blueprint four, board one-pager, instrumentation plan)
**Map:** #416 T1 — frontier, `ready-for-human`
**Status:** v1 definitions only — no collectors, no dashboard code (T2 #418)
**Sign-off:** Jack Mlusu only

---

## Header

Studio · reporting period · CEO: Jack Mlusu

## Row 1 — Blueprint four (big numbers)

| ATC | Velocity to MVP | Correction Ratio | Capital Efficiency |
|-----|-----------------|------------------|--------------------|
| e.g. 92% | 54 d | 12 / 1k | 3.4x |

| Metric | v1 formula | Target / bands |
|--------|-----------|----------------|
| **ATC Rate** | `without_manual / entered * 100` | >90% green · 80–90% watch · <80% block scale |
| **Velocity to MVP** | `date(deploy) - date(thesis_approved)` | <60d green · 60–90d retro · >90d pause intake |
| **Correction Ratio** | `(overrides + forced + rework) / actions * 1000` | 30d baseline, no target; then per-archetype |
| **Capital Efficiency** | `realized_value / capital_consumed` | 3–5x green · 2–3x review · <2x kill/re-thesis |

## v1 decisions

1. **ATC denominator:** `tasks_entered` = end-to-end agentic tasks entering the success pipeline (completion / failure / escalation). Forced human completion = failure. Scheduled Tier-gate HITL approvals = governance, not failure. Document rule in collector so ATC can't be gamed.
2. **Required events:** every task event emits `venture_id` (A/B/C or `studio-core`), `model_id`, `cost_usd` (+ latency). Gate timestamps `thesis_approved`, `deploy` in studio tracker (owner: COO). No phase advance without recorded gate review.
3. **Velocity clock (v1 deviation):** any external customer wait pauses the clock; each pause logged with reason + dates. Internal delay always counts. Relaxes the strict pre-agreed-only rule for v1.
4. **CFO rollup:** CFO-owned section, MWK/USD dual display; `realized_value` = contracted ARR + verified cost-avoidance only. Dashboard rollup deferred to T2.
5. **30-day baseline:** measurement-only from instrumentation start, split by archetype A/B/C; rolling targets set after.
6. **T4 #420 competitive landscape refresh:** Oct 2026 delta vs. baseline v1 (2026-09-16); 4 local moves verified (TNM data centre, TNM+Huawei 2027 plan, Seed Co AI upgrade, SpaceAI new entrant), 4 international moves verified (BCG index, Deloitte, Accenture, Polsia pricing); wedge-table verdicts NO flips — category "empty locally" holds; position LightSpeed as only governed human-led agentic org with Malawi-first ops, transparent MWK pricing, HITL audit trails, RBAC; monitor unconfirmed/re-check list (18 items) next cycle 2026-11-16.

## Row 2 — Portfolio

One card per venture (A Enterprise Agent / B B2B Workflow / C Sovereign Data): stage, sector, ATC, velocity, status.

## Row 3 — Risk strip

Red Org Health components · open EXPIRED approvals · cost overrun vs budget · policy/compliance exceptions.

**Cadence:** weekly ops (ATC, corrections, cost) · monthly board pack (all four + portfolio) · gate reviews use full scorecard.

## Honesty rules (ADR-020/033)

Evidenced, qualified, or removed. No invented revenue. Capital efficiency needs ratified approval before external use. Never cite Org Health green as ATC proof without the ATC collector running.

**Non-goals:** collectors, Studio Scorecard UI, Org Health weight changes.

---

**Approved:** Jack Mlusu, date: 2026-10-07
