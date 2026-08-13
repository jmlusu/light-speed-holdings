# Tasks

## Format

- `- [ ] T00X [P] Action with target path and validation note`
- `[P]` means parallel-safe.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation (both approved).

## Implementation

- [x] T002 [P] Purge 177 junk tasks: back up `.opencode/inbox.json`, delete via `MessageBus.delete_task()`, `reconcile_mirror()`, verify `get_all_tasks() == []` and SQLite task rows clean.
- [x] T003 Update `README.md` — 127 agents / 18 departments, 30 CLI commands; remove stale "27 agents"/"24 CLI" strings.
- [x] T004 Create `.env` from `.env.example` (gitignored, real keys for OpenCode + Gemini, budget caps in `config/company/guardrails.yaml`).
- [x] T005 Draft `docs/service-catalog-malawi.md` — offers, MWK+USD pricing, payment rails, delivery model, compliance checklist.

## Validation

- [x] T006 Run gates: `pwsh scripts/lint-ecl.ps1`, `uv run ruff check src/`, `uv run mypy src/`, `uv run pytest`.
- [x] T007 Grep verify: no "27 agents"/"24 CLI" in README; `git check-ignore .env` exits 0.

## Deferred Tasks

- Point test suites at a temp inbox (test isolation) — follow-up sprint.
- Dashboard: Org Health score, agent onboarding flow, company-KPIs UI wiring.
