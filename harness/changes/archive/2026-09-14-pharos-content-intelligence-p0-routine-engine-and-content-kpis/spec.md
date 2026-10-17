# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first (ADRs/plans authored during the Eden review, then
  approved by Human CEO before this change was opened)
- Questions asked this round: 1 (which codebase/branch is the Python truth —
  resolved to `feature/cleanup-dummy-tasks`; worktree at
  `C:\Users\jmlus\light-speed-holdings-p0`)

## Goal And Evidence

- Real problem or user request: LightSpeed's Pharos engine must produce 50
  thought-leadership articles/yr at a weekly 3-post cadence (Mon Agentic
  Enterprise Brief / Wed Build Log / Fri AI Policy & Governance Africa)
  toward 2,000+ newsletter subscribers for an institutional SADC audience.
  The Eden.so review (docs/eden-review-plan.md, ADR-020) concluded: don't buy
  Eden — build a governed content-intelligence loop on infrastructure the
  company already owns (daemon scheduler, message-bus, memory, graph), and
  start with a P0 routine engine + content KPIs.
- Current behavior: Pharos cadence is manual/blank-page; nothing on the daemon
  fires recurring research/draft tasks; no content-performance KPIs are
  collected beyond the generic marketing collector.
- Source of evidence: `docs/eden-review-plan.md`, `docs/adr/020-pharos-content-intelligence.md`
  (copied into this worktree), `docs/Pharos/*` (README, roadmap,
  content-calendar, positioning).

## User Scenarios And Success

- Primary user/system scenario: the executor daemon (idle loop, sub-minute
  poll) fires a configured Pharos routine when due; each fire enqueues a
  **fresh** MessageBus Task (idempotent via `routine_run` task tags);
  `AgentLoop` runs the routine's agent; the run is observable in the task
  store, KPI snapshot, and routine store `last_run` state. `config/company/routines.yaml`
  declares Mon/Wed/Fri Pharos routines today.
- Success criteria: passing gates below; a `routine:` scheduler runs inside
  the daemon loop; no duplicate task enqueue after crash/restart (mark-before-send);
  a Pharos content KPI collector reports published-this-period, drafts-in-pipeline,
  and subscriber count vs the 2,000 target.
- Acceptance criteria:
  1. `RoutineScheduler.run_due()` enqueues at most one task per due routine per
     fire, with `routine_run:{id}-{UTC date}` in the task's tags.
  2. A routine with an un-firable future date produces no task.
  3. Disabled routines are skipped; unknown days/times never raise.
  4. `content_writer` (valid registry id on this branch; Pharos agents exist
     only on `research/swot-baseline`, out of scope here) is the P0 receiver.
  5. Collectors feed `collect_all_kpis` without breaking the existing marketing
     KPI shape.

## Non-Goals

- P1/P2 features: deep-research routines, CEO voice profile, Boost
  reverse-engineer fan-out, publishing rails (bought, not built), Whisper,
  Pharos Content Intelligence MCP server (`src/ai_company/mcp/server.py`).
- Eden MCP consumption behind a feature flag; SADC regional verification pass.
- No schema change to `CompanyRegistry`; no new top-level CLI.
- No new agent registry entries.

## Constraints

- One active ECL change at a time; `INDEX.json` is script-derived (never
  hand-edit). Harness scripts: `scripts/harness-change.ps1`,
  `scripts/lint-ecl.ps1`.
- Daemon loop is the existing scheduler host (`kpi_snapshot` cadence pattern);
  extend, don't fork.
- Sub-agent idempotency: `mark_run` BEFORE `send_task` (crash-safety ordering,
  mirrors `Scheduler.create_pending_tasks`).
- Receiver id must exist in `company-registry.yaml` on this branch.
- Canonical tool vocabulary (AGENTS.md §8): only the 7 canonical tools in
  agent cards.

## Assumptions

- UTC day/time semantics for firings (daemon already UTC; Malawi is UTC+2).
- Default model tier for routine tasks is the bus/executor default; per-routine
  `budget_tokens` is metadata at P0, enforced in later phases.
- `config/company/routines.yaml` is the single source of routine definitions
  for P0 (mirrors scheduler/cycle file convention).

## Open Questions

- None blocking P0. (Pharos-specific agents arrive on a future branch; P0 uses
  `content_writer`.)

## Resolved Clarifications

- Python codebase lives on `feature/cleanup-dummy-tasks` (+ `phase-c-api-v1`);
  `research/swot-baseline` is the website/research branch — confirmed by the
  Human CEO; P0 implements in the worktree on `feature/cleanup-dummy-tasks`.
- The `scheduler.cycles` key in `config/company/scheduler.yaml` is not consumed
  by `Scheduler`/`KPISnapshotScheduler`; P0 introduces its own routine store and
  a `routine:` scheduler in the daemon, keeping the legacy cycle file untouched.
