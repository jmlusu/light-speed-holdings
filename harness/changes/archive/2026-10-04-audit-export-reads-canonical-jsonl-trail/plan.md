# Plan

## Technical Approach

1. **Source resolution** — add `export_audit_trail(path=None, output_dir="reports/evidence", date=None) -> int` in `src/ai_company/audit/export.py`:
   - resolve `path or get_audit_path()`; missing → `raise FileNotFoundError` (CLI maps to exit 1, AC-3).
   - enumerate active + rotated files via `ordered_audit_files()` (oldest → newest).
   - stream lines, `json.loads`, filter `datetime.fromisoformat(ts).date().isoformat() == date` (offset-safe).
   - raw passthrough of original lines; collect first, **write only if count > 0** (AC-2).
2. **CLI** — `main()`: `--db` default `None` (JSONL trail mode; a value selects the legacy SQLite functions unchanged), `--all-tables` requires `--db`, exit 1 on missing source, exit 0 on success/quiet. Fix the module docstring still naming `audit/audit.db`.
3. **Rotation reuse** — promote `integrity._ordered_files()` → public `ordered_audit_files(path)` with a backward-compatible alias; `verify_audit_chain` keeps working; export reuses the same ordering (AC-5).
4. **Local runner** — new `scripts/export-audit-evidence.ps1`: runs the export for UTC today, appends `{"date","events","run_at"}` to `reports/evidence/audit-export-runs.jsonl`, optional `-Commit` (add+commit+push with rebase fallback, mirroring the workflow's push pattern); default no commit. Accepts `-Date` for backfill.
5. **CI guard** — rework `.github/workflows/audit-export.yml` into *Daily Audit Evidence Check*: `schedule` runs a bash-only freshness check (newest run-log `run_at` within 36h; if `events > 0` the matching `audit-<date>.jsonl` must exist and be non-empty, else `exit 1`); drop `setup-uv`/`uv sync`; `workflow_dispatch` re-runs the guard and drops the `date`/`all-tables` inputs (CI cannot export a gitignored trail); keep the artifact-upload and deploy-key commit steps under `if: always()`.
6. **Repo cleanup** — `git rm --cached audit/audit.db` and gitignore `audit/` (also silences the untracked `audit.db-shm`/`-wal` noise), AC-6.
7. **Docs/ADR** — amend `docs/adr/008-evidence-separation.md` (line 29 source, line 40 path, Implementation Plan row), `docs/adr/008-evidence-separation-sequence.md:48,148`, `docs/runbooks/evidence-stores-dr.md:82`.

## Impacted Modules And Files

- `src/ai_company/audit/export.py` — new exporter, CLI rewire, docstring.
- `src/ai_company/audit/integrity.py` — public `ordered_audit_files()`.
- `tests/unit/test_audit_export_trail.py` — new.
- `scripts/export-audit-evidence.ps1` — new.
- `.github/workflows/audit-export.yml` — guard rework.
- `.gitignore` — `audit/` entry.
- `audit/audit.db` — untracked (working copy retained).
- `reports/evidence/audit-2026-10-0{1,3,4}.jsonl`, `reports/evidence/audit-export-runs.jsonl` — generated evidence.
- `docs/adr/008-evidence-separation.md`, `docs/adr/008-evidence-separation-sequence.md`, `docs/runbooks/evidence-stores-dr.md`.

## Interfaces, Data, Permissions

- CLI: `python -m ai_company.audit.export [--date D] [--output DIR] [--db PATH] [--start-date/--end-date] [--all-tables]`; exit codes 0 / 1.
- Evidence naming unchanged: `reports/evidence/audit-<date>.jsonl`; new side file `reports/evidence/audit-export-runs.jsonl` (append-only run marker, tracked).
- CI needs no secrets for the guard; the deploy-key commit path is retained unchanged for `if: always()`.
- Local push from the scheduled task requires the developer's existing remote credentials.

## Spec Gaps Found From Planning

- CI cannot run the export at all (trail gitignored) — resolved by making `workflow_dispatch` a guard re-run rather than an exporter; backfill is local-only.
- Zero-row days leave no dated file, so an age-based guard alone cannot distinguish "quiet" from "never ran" — resolved by the run log (D-d).

## Risks And Mitigations

- Wrong date window (timezone/offset) → use `fromisoformat(...).date()`, assert per-line dates in tests (AC-1/AC-4).
- Silent regression on rotation → synthetic `audit.1` fixture test (AC-5).
- Back-compat break of legacy `--db` path → existing `test_evidence_separation.py` must stay green (T5 gate).
- CI false failure on quiet days → run log carries `events: 0`, guard only checks freshness then (AC-8).
- Untracking `audit/audit.db` while the legacy `--db` default points there → default becomes `None`, and an explicit missing path raises rather than warns.

## Verification Plan

- Targeted: `uv run pytest tests/unit/test_audit_export_trail.py tests/unit/test_evidence_separation.py`.
- Full: `uv run ruff check src/ && uv run mypy src/ && uv run pytest` and `pwsh scripts/lint-ecl.ps1`.
- Manual ACs: export 2026-10-04 (41 lines), 2026-10-01 (46), 2026-10-02 (no file, exit 0), trail renamed (exit 1), `git status` snapshot before/after.
- ECL: `plan_review: approved` before implementation; `validation_status: pass` at `phase: validate` before close.
