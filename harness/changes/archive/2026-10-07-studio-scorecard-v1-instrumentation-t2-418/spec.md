# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first (T1 signed metric sheet + plan-mode review, user-approved 2026-10-07)
- Questions asked this round: 3 (scope cut, tracker home, dashboard surface — all answered)

## Goal And Evidence

- Real problem or user request: T2 #418 (Wayfinder map #416) — instrument the Studio Scorecard v1 without breaking prod: collectors + Studio Scorecard page + 30-day baseline behind SoT drift gates.
- Current behavior: T1 definitions exist (`docs/venture-studio/scoreboard-v1.md`, signed 2026-10-07) but no collectors emit `venture_id`/`model_id`/`cost_usd`, no studio tracker exists, no scorecard UI exists; `Task` model has no studio fields.
- Source of evidence: `docs/venture-studio/05-kpi-scorecard.md` (blueprint four + instrumentation plan steps 1–6), `docs/venture-studio/scoreboard-v1.md` (signed v1 sheet), ADR-033 (governed evidence, no fake metrics), `src/ai_company/dashboard/kpis/` (collector pattern), `src/ai_company/models/models.py` (`Task` shape).

## User Scenarios And Success

- Primary user/system scenario: CEO/COO open the Studio Scorecard and see the blueprint four (ATC, Velocity, Correction Ratio, Capital Efficiency) computed from live internal task telemetry, plus per-venture portfolio cards and a risk strip — with `no_data` honesty states wherever data does not yet exist.
- Success criteria: (1) task events carry `venture_id`/`model_id`/`cost_usd`/latency additively; (2) `company/studio_tracker.yaml` holds gate timestamps; (3) `StudioScorecardCollector` reports all four metrics with `data_quality` flags; (4) `GET /api/v1/studio-scorecard` + dashboard page render live-or-`no_data` (never fabricated); (5) 30-day baseline runs measurement-only; (6) `validate-drift` green.
- Acceptance criteria: same as success criteria; ECL closed with `validation_status: pass`; resolution comment posted on #418.

## Non-Goals

- Changing Org Health weights or formulas (explicit T1 non-goal).
- Paging alerts on studio metrics (baseline is measurement-only; symptom alerts deferred).
- Backfilling history or inventing revenue/cost-avoidance figures (ADR-020/033).
- Touching the T4 #420 competitive-landscape work or any other map ticket (T3, T5, T6).

## Constraints

- Additive-only instrumentation: optional `Task` fields with safe defaults; collectors never raise; SQLite-first with MessageBus/file fallback (`kpis/base.py` contract).
- ADR-020/033 honesty: every public/internal number evidenced, qualified, or `no_data`; capital figures need ratified CFO inputs.
- SoT drift gates: no duplicated metric hard-codes in components; `docs/source-of-truth.yaml` + `validate-drift.ps1` green.
- ECL one-active-max; this change owns the slot until closed.

## Assumptions

- `venture_id` values: `studio-core` default + ventures A/B/C (Portfolio A Enterprise Agent / B B2B Workflow / C Sovereign Data per scoreboard-v1).
- Agent-action volume for the correction denominator comes from the audit/tool-call trail already written by `ToolRunner` (`log_tool_call`).

## Open Questions

- None — all clarifications resolved (see below).

## Resolved Clarifications

- Scope: full four metrics in this one ECL (user-approved 2026-10-07).
- Tracker home: `company/studio_tracker.yaml`, COO-owned.
- Surface: new `GET /api/v1/studio-scorecard` endpoint + dedicated dashboard page/section.
- ATC denominator: `tasks_entered` = end-to-end agentic tasks (completion/failure/escalation); forced human completion = failure; scheduled Tier-gate HITL = governance, not failure (T1 decision 1).
- Velocity clock: any external customer wait pauses with logged reason + dates (T1 v1 deviation).
