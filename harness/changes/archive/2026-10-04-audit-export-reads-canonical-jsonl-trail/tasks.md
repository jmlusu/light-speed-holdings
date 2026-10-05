# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe.

## Setup / Intake

- [x] T001 Create active ECL change and record the 6 resolved decisions in `spec.md` / `plan.md`.
- [x] T002 Amend `docs/adr/008-evidence-separation.md`, `docs/adr/008-evidence-separation-sequence.md`, `docs/runbooks/evidence-stores-dr.md` (gate for `plan_review: approved`).

## Implementation

- [x] T003 Promote `_ordered_files()` → `ordered_audit_files(path)` in `src/ai_company/audit/integrity.py` with a backward-compatible alias; `verify_audit_chain` unchanged.
- [x] T004 Add `export_audit_trail()` to `src/ai_company/audit/export.py`: `get_audit_path()` default, `FileNotFoundError` on missing source, rotation-aware read, UTC date filter, raw passthrough, write-only-if-non-empty.
- [x] T005 Rewire `main()` in `export.py`: `--db` default `None`, `--all-tables` requires `--db`, exit 1 on missing source, updated module docstring.
- [x] T006 [P] Add `tests/unit/test_audit_export_trail.py` covering AC-1/2/3/4/5 with tmp trail fixtures (incl. synthetic `audit.1`).
- [x] T007 Create `scripts/export-audit-evidence.ps1` (run export, append run log, `-Date`, `-Commit` with push + rebase fallback).
- [x] T008 Rework `.github/workflows/audit-export.yml` into the freshness guard; drop `setup-uv`/`uv sync`, drop `date`/`all-tables` inputs, keep artifact + deploy-key commit steps.
- [x] T009 `git rm --cached audit/audit.db` and add `audit/` to `.gitignore`.
- [x] T010 Backfill evidence: export 2026-10-01 (46), 2026-10-03 (84), 2026-10-04 (41); skip 10-02; seed `reports/evidence/audit-export-runs.jsonl`.

## Validation

- [x] T011 Targeted tests: `uv run pytest tests/unit/test_audit_export_trail.py tests/unit/test_evidence_separation.py`.
- [x] T012 Full gates: `uv run ruff check src/`, `uv run mypy src/`, `uv run pytest`, `pwsh scripts/lint-ecl.ps1`.
- [x] T013 Manual AC run: AC-1/AC-2/AC-3/AC-4 exit codes and line counts; AC-6 `git status` snapshot; AC-7 non-empty tracked evidence; AC-8 guard dry-run via `workflow_dispatch`.
- [x] T014 ECL: record `validation_status: pass`, `phase: validate`, run `close completed`, update `docs/STATUS.md` handoff (note `harness/evolution/pending.md`).

## Deferred Tasks

- None. (Findings outside scope: issues 1-4, `audit_events` mirror stall, `correlation_id` schema — tracked as separate tickets.)
