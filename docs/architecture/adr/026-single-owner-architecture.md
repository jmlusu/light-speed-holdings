# ADR-026: Single-Owner Architecture

**Status:** Accepted
**Date:** 2026-09-24
**ECL:** LightSpeed AI Company Builder + Web Experience Architecture v2.0
**Cross-refs:** [AI_WORKFORCE_90.md](../../AI_WORKFORCE_90.md) §6, [AGENT_CONSOLIDATION_152_TO_90.md](../../AGENT_CONSOLIDATION_152_TO_90.md) §4

## Context

Discovery found multiple structural dual-owner violations: two departments sharing one executive, parallel content/legal/DevOps/prompt roles, and dual IC ladders. Shared execution is workable; shared *accountability* is not — it creates unowned decisions and KPI ambiguity. The 152→90 trim closed most violations but left at least one structural open item (V1) and two bounded items (V9, V10).

## Decision

1. **Principle:** Every capability has exactly one accountable owner. Chain is mandatory end-to-end:

   **Capability → Owner → Decision Rights → Workflow → Execution → Measurement (KPIs) → Accountability (escalation_path + approval_level)**

2. **Shared execution allowed; shared accountability not allowed.** Dual mandates must be split into two capabilities or explicitly re-owned with a documented primary.

3. **BD executive:** `business_development` department executive = `head_of_business_development` (specialist under chief_of_staff), not `cso`. **`cso` remains Strategy executive only** — strategy owns M&A/partnership *strategy* input; BD owns pipeline execution under that strategy.

4. **Registry ownership schema (§9 in AI_WORKFORCE_90):** MANDATORY fields eventually include `decision_rights`, `kpis`, `approval_level`, `escalation_path` (currently 0/90 — gaps G3–G6). Enforcement is validator fail-fast work for a follow-on implementation ECL, not this docs-only change.

5. **Known violations disposition:**

   | ID | Status | Ruling |
   |----|--------|--------|
   | V1 cso dual exec (BD + strategy) | **Open → resolved by this ADR** | Split: BD exec = `head_of_business_development`; cso = strategy only |
   | V2–V8 (trim merges) | Closed at `e2bdb0c7` | Record only |
   | V9 qa_lead vs test_engineering_lead | Bounded open | Encode decision_rights when §9 backfilled: qa_lead = policy/gates; test_engineering_lead = automation/eval execution |
   | V10 fullstack → dual target | Bounded open | Intake rule: BE-heavy → lead_backend; UI-first → lead_frontend; disputes → vp_engineering |
   | V11 chief_of_staff 19 reports | Watch | Capacity risk, not dual ownership; offload program tracking to workflow_owner if SLA breaches |

## Alternatives

| Option | Why not |
|--------|---------|
| Leave cso as dual department executive | Violates single-owner principle; BD KPIs and strategy KPIs collide on one executive |
| Create a new `bd_executive` ID | Already exists as `head_of_business_development`; CREATE NEW forbidden without approval |
| Make ownership a doc convention only | Ambiguity returns on next registry edit; validator cannot enforce prose |
| Fix violations case-by-case without schema | Leaves decision_rights/escalation implicit forever (G3–G6) |

## Rationale

- Single owner is the accountability primitive for governance tiers (HITL approval levels map per-owner, not per-committee).
- Reusing `head_of_business_development` avoids a new roster ID and matches the REASSIGN pattern already used in the trim (business_developer → sales_owner, corporate_development_lead → head_of_business_development merges).
- Schema MANDATORY fields make the chain machine-checkable at registry load.

## Consequences

- `company/departments.yaml` must change `business_development.executive` from `cso` to `head_of_business_development` in the follow-on implementation ECL (docs-only here).
- `cso` direct scope narrows to Strategy (+ market_analyst); BD reports path stays chief_of_staff → head_of_business_development.
- When §9 backfill lands, validator fails load on missing `decision_rights`/`kpis`/`approval_level`/`escalation_path` (staged warn→fail).
- V9/V10 remain documented operational rules until schema fields exist.
