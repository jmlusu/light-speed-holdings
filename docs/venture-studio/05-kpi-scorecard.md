# Part 5 — Core Performance Metrics (Studio Scorecard)

**Source:** `brand/ai_venture_studio_execution_plan.md` Part 5
**ECL:** AI Venture Studio Execution Plan Parts 2-5
**Owner:** CFO / Chief of Staff / CEO
**Date:** 2026-09-24
**Status:** Strategy deliverable (docs only)

---

## 1. North-star metrics (blueprint four)

| # | Metric | Definition | Target | Primary data source |
|---|--------|------------|--------|---------------------|
| 1 | **Agentic Task Completion (ATC) Rate** | % of end-to-end agentic tasks completed **without manual intervention** | **> 90%** | Task success pipeline (Engineering task completion / failure / escalation); correlate with Org Health Task Success Rate |
| 2 | **Velocity to MVP** | Days from **Phase 1 thesis approval** → **Phase 3 customer deployment** (Part 3 lifecycle) | **< 60 days** | Venture stage-gate timestamps (ECL / studio tracker) |
| 3 | **Manual Correction Ratio** | Human override / correction events **per 1,000 executed agent actions** | Track; reduce trend-wise (baseline first) | ApprovalGate override events ÷ agent action volume × 1000 |
| 4 | **Capital Efficiency per Spin-Out** | Output per capital unit vs traditional seed benchmark | **3–5×** capital efficiency | CFO: studio spend + venture cost tags vs delivered value / contracted ARR / avoided cost |

These four are the **studio board pack**. Department KPIs on the CEO dashboard remain the **operating vital signs**; this scorecard is the **venture studio rollup**.

---

## 2. Metric specifications

### 2.1 ATC Rate

```
ATC = tasks_completed_without_manual_intervention / tasks_entered * 100
```

| Band | ATC | Interpretation |
|------|-----|----------------|
| 🟢 On target | > 90% | Meets blueprint goal |
| 🟡 Watch | 80–90% | Automation gap; inspect top correction reasons |
| 🔄 Below | < 80% | Gate Block on scale phase; fix prompts/tools/HITL routing |

**Disambiguation:** “Manual intervention” includes forced human completion, not *scheduled* HITL approvals designed into Tier gates — those count as **governance**, not failure. Document the denominator rule in the collector so ATC is not gamed by adding approvals.

### 2.2 Velocity to MVP

```
Velocity_days = date(phase3_deploy) - date(phase1_thesis_approved)
```

| Band | Days | Action |
|------|------|--------|
| 🟢 | < 60 | At target |
| 🟡 | 60–90 | Retrospective; identify shared-stack bottleneck |
| 🔴 | > 90 | Pause new Discovery intake until cycle time recovers |

**Clock rules:** Pause only for external customer waits if pre-agreed; internal delay always counts.

### 2.3 Manual Correction Ratio

```
Correction_Ratio = (human_overrides + forced_completions + rejected_outputs_reworked)
                  / agent_actions * 1000
```

| Direction | Meaning |
|-----------|---------|
| Falling ratio + flat ATC | Better model/tool quality |
| Rising ratio + flat ATC | Humans papering over failures — investigate before celebrating ATC |
| Rising both | Systemic regression — amber on Org Health path |

**Baseline:** First 30 days after instrumentation = measurement only (no target). Then set rolling target by venture archetype (A/B/C from Part 3).

### 2.4 Capital Efficiency per Spin-Out

```
Capital_Efficiency = realized_value / studio_capital_consumed
```

Where `realized_value` is prioritized as: contracted ARR + verified cost-avoidance for design partners (honesty ladder per ADR-020/033 — **no invented revenue**).

| Band | Multiple vs traditional seed-equivalent output | Action |
|------|-----------------------------------------------|--------|
| 🟢 | 3–5× | Scale; institutional capitalization conversations |
| 🟡 | 2–3× | Cost or pricing review |
| 🔴 | < 2× | Kill or re-thesis at next gate |

---

## 3. Supporting metrics (not substitutes)

| Supporting metric | Why it matters | Maps to |
|-------------------|----------------|---------|
| Org Health Score (0–100) | Running-company vital signs | CEO dashboard: Task Success 30%, Utilization 25%, Cost Efficiency 25%, Error Rate 20% |
| Engineering task completion / failure / escalation | Feeds ATC and correction ratio | Dashboard Engineering tab (completion target 95%, escalation < 5%) |
| Cost per successful task (USD/MWK) | Router quality + cascade discipline | Part 4 cost tags |
| Design-partner count at Phase 3 | Validation quality | Part 3 exit gates (2–3 partners) |
| Time-in-pending HITL | Governance latency, not failure | ApprovalGate ageing / EXPIRED sweep |

---

## 4. Scorecard layout (board one-pager)

**Header:** Studio name · reporting period · CEO · CFO

**Row 1 — Blueprint four (big numbers):**

| ATC | Velocity to MVP | Correction Ratio | Capital Efficiency |
|-----|-----------------|------------------|--------------------|
| e.g. 92% | 54 d | 12 / 1k | 3.4× |

**Row 2 — Portfolio:** one card per venture (A/B/C) with stage, primary sector (Part 2), ATC, velocity, status.

**Row 3 — Risk strip:** red Org Health components, open EXPIRED approvals, cost overrun vs budget, policy/compliance exceptions.

**Cadence:** Weekly ops review (ATC, corrections, cost) · Monthly board pack (all four + portfolio) · Gate reviews use full scorecard (Part 3).

---

## 5. Instrumentation plan (implementation follow-up)

| Step | Work | Owner | Depends on |
|------|------|-------|------------|
| 1 | Define ATC denominator rule + correction taxonomy | Engineering + Chief of Staff | None |
| 2 | Emit `venture_id`, `model_id`, `cost` on task events | Platform | Part 4 cost tags |
| 3 | Stage-gate timestamps in studio tracker | COO | Part 3 lifecycle adopted |
| 4 | CFO rollup formula + MWK/USD dual display | CFO | Pricing model docs |
| 5 | Dashboard: Studio Scorecard page (or section) | Dashboard owner | Steps 1–4 |
| 6 | First 30-day correction baseline | Chief of Staff | Step 2 |

**This ECL does not implement** collectors or UI — it locks definitions so the next implementation ECL has a single spec.

---

## 6. Honesty & evidence rules

- Public or client-facing numbers follow **ADR-020 + ADR-033**: evidenced, qualified, or removed.
- Internal proof stack (90 agents, 2,373 tests, 5-tier) may be cited only when still true at publish time (SoT-linked constants).
- Capital efficiency and client financials require the ratified approval path before external use.
- Never present Org Health green as proof of venture ATC without the ATC collector running.

---

## 7. Deliverable checklist

- [x] Blueprint four fully specified with formulas and bands
- [x] Supporting metrics and Org Health relationship
- [x] Board one-pager layout and cadence
- [x] Instrumentation follow-ups without implementing them here
- [x] Honesty/evidence alignment with ADR-020/033

**Non-goals:** dashboard code, collector code, changing Org Health weights.
