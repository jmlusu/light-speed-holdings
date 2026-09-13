# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: mixed (requirement-first draft + CEO plan/sign-off)
- Questions asked this round: 0 (resolved in prior session — see Resolved Clarifications)

## Goal And Evidence

- Real problem or user request: The CEO dashboard hardening plan (A1–A5 +
  C1–C5) had two remaining items. Agents persist run output under
  `results/<name>/loop_result.json` and `results/cost_log.jsonl`, but there is
  no single queryable abstraction over them (inconsistent timestamps, no
  head/tail query, no "open the actual report" path), and there is no way to
  follow a single task's full lifecycle from the dashboard.
- Current behavior: Reports are read by hand-walking the filesystem; the
  dashboard shows live snapshots but cannot open an agent-produced report or
  trace a task through its audit events.
- Source of evidence: Live `results/` data (1787 indexed report records), the
  CEO dashboard hardening plan, and the prior session's implementation + tests.

## User Scenarios And Success

- Primary user/system scenario 1: A user selects a task ID on a "Task Flow"
  page and sees its lifecycle timeline (created → claimed → in-progress →
  completed/failed/escalated/dead-letter) with timestamps and the audit events
  that touch it.
- Scenario 2: A user opens a "Reports" page and browses agent-produced reports
  newest-first, filters them, and opens/reads a report's content — backed by a
  queryable `ReportStore`.
- Success criteria: Both views are read-only, list real data, expose correct
  new/old ordering across mixed timestamp formats, and never crash on missing
  or malformed data.
- Acceptance criteria:
  - A1: `ReportStore(root)` lists all report folders/shards under `root`.
  - A2: `latest(n)` / `oldest(n)` return the correct records/order even when
    timestamps mix naive-UTC and `Z`-suffixed forms (epoch handled too).
  - A3: a report with a missing/unparseable timestamp never crashes a query —
    it is pushed to a sane end and documented.
  - A4: a missing root is an empty store (no exception at construction).
  - A5: `ruff check src/`, `mypy src/`, and the targeted store/dashboard
    suites pass with no regression.
  - B1: `GET /api/v1/tasks/{task_id}/flow` returns the task snapshot plus the
    chronological lifecycle timeline (404 for unknown task).
  - B2: `GET /api/v1/reports` lists real `results/*` reports newest-first with
    `limit`/`agent` filters and excludes root `cost_log.jsonl` by default;
    `GET /api/v1/reports/content` returns a report's documents (404 on
    path-traversal escape).
  - B3: `/task-flow` and `/reports` pages render and expose the views.

## Non-Goals

- No editing/mutation of tasks or reports from these views (strictly read-only).
- No new persistence format; no migration of existing `results/` files.
- No schema enforcement on report contents (free-form JSON stays free-form).
- No dashboard UI beyond the two approved pages; no dead-letter UI changes.

## Constraints

- Reuse existing `store/` patterns where sensible; this is a read-heavy layer
  that must not force writes into the guarded-write path.
- Path-served report content must be confined to the reports root (SECURITY).
- Use the canonical ECL/harness workflow; do not commit (per the whole
  hardening effort until the user says otherwise).

## Assumptions

- The CEO-approved recommended interpretation of the codenames is correct
  (see Resolved Clarifications).
- The `results/` root resolves to the dashboard store base dir (`.` →
  `./results`), matching real data.
- `x-show`/Alpine is the existing front-end convention (no Vue `v-if`).

## Open Questions

- None blocking. (Full-suite pytest run is a verification task, not a design
  question.)

## Resolved Clarifications

- C4 Q1 (is "Path-of-RPG" a task-lifecycle traceability view?): **A — Yes**
  (task journey timeline with audit-trace overlay).
- C4 Q2 (is "FLORA" a reports/outcomes viewer?): **A — Yes** (Reports page
  built on C5 `ReportStore`).
- C4 Q3 (dashboard UI scope): **B — both** a "Task Flow" page and a "Reports"
  page.
- C4 Q4 (ordering): **C5-first** — build `ReportStore` then layer C4 on it.
- C5 scope: confirmed as written (read-only queryable `ReportStore`).
