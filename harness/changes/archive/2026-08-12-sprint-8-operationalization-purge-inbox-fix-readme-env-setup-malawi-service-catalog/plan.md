# Plan

## Technical Approach

1. **Purge inbox (T002).** One-off Python script run via `uv run python`:
   - Instantiate `MessageBus(database=init_database(<data root>/data/ai_company.db))`
     so deletes mirror into SQLite (same wiring as `cli/executor.py::_resolve_database`).
   - Copy current `.opencode/inbox.json` to `.opencode/inbox.json.operational-purge-<ts>.bak`.
   - Delete all tasks via `bus.delete_task(task_id)`.
   - Call `bus.reconcile_mirror()` and print counts.
   - Verify `bus.get_all_tasks()` == `[]` and `bus.count_by_status()` is empty.
   - Use the same script to confirm SQLite `tasks` table is clean.
2. **README (T003).** Replace stale counts with current reality: 127 agents / 18 departments,
   30 CLI commands, root `company-registry.yaml` as source of truth, real quick start
   (`uv run ai-company --help`, `agents list`, `status`). Keep structure; do not touch CHANGELOG.
3. **`.env` scaffold (T004).** Copy `.env.example` → `.env` (gitignored), keeping placeholders
   but adding a `# TODO: set real values` header. Verify it is ignored (`git status`).
4. **Service catalog (T005).** New `docs/service-catalog-malawi.md`: market positioning,
   offer tiers (AI services studio, BPA/chatbots, data & donor reporting, platform license),
   per-offer deliverables + MWK/USD pricing anchors, payment rails (Airtel Money, Mpamba,
   PayChangu-style cards, bank), delivery model (inbox task → agent → CEO review → client),
   legal/compliance checklist (Registrar General, MRA TIN, Data Protection Act 2017).
5. **Validation (T006).** Run `pwsh scripts/lint-ecl.ps1`, `uv run ruff check src/`,
   `uv run mypy src/`, `uv run pytest`. Update `docs/STATUS.md` after close.

## Impacted Modules And Files

- `.opencode/inbox.json` (runtime state, gitignored)
- `README.md`
- `.env` (new, gitignored)
- `docs/service-catalog-malawi.md` (new)
- `harness/changes/active/*` (ECL docs)
- No `src/` changes expected.

## Interfaces, Data, Permissions

- MessageBus file contract unchanged (JSON list). SQLite write-through honored.
- No permission/tier rule changes.
- New `.env` must not be committed.

## Spec Gaps Found From Planning

- None.

## Risks And Mitigations

- Risk: purge misses SQLite mirror rows → Mitigation: delete via bus + `reconcile_mirror()`
  + SQLite row-count verification.
- Risk: tests re-pollute inbox → noted for follow-up (test isolation), out of scope here.
- Risk: README edits drift again → single source for counts is `company/agent-registry.json`
  (127 verified 2026-08-12).

## Verification Plan

- `bus.get_all_tasks()` returns `[]`; SQLite task row count == 0 (or only real rows).
- `grep '127' README.md` present; no "27 agents" or "24 CLI" strings remain.
- `Test-Path .env` True; `git check-ignore .env` exits 0.
- `docs/service-catalog-malawi.md` contains offers + MWK + USD + payment rails.
- `lint-ecl.ps1` + ruff + mypy + pytest all green.
