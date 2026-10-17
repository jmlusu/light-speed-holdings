# Issue 5 (audit-export) — Promotion to `phase: implement` — Hand-off Document

## Promotion Summary
- **Issue**: Issue 5 — daily audit evidence export repointed from the 0-row tracked decoy `audit/audit.db` to the canonical hash-chained trail (`.opencode/audit` + rotated siblings)
- **Phase**: `implement` (confirmed in `harness/changes/archive/2026-10-04-audit-export-reads-canonical-jsonl-trail/summary.md` line 6)
- **Validation Status**: `pass` (confirmed in same summary.md line 27)
- **Archive Status**: `completed` (ECL `audit-export-reads-canonical-jsonl-trail` closed and archived at `harness/changes/archive/2026-10-04-audit-export-reads-canonical-jsonl-trail`)
- **Date**: 2026-10-04
- **Owner**: jmlus

## What Was Done
All tasks from the implementation plan were completed:

### Implementation Tasks (all ✅)
- **T003**: Promoted `ordered_audit_files()` in `src/ai_company/audit/integrity.py` with backward-compatible alias
- **T004**: Added `export_audit_trail()` to `src/ai_company/audit/export.py` with `get_audit_path()` default, rotation-aware read, UTC date filter, write-only-if-non-empty
- **T005**: Rewired `main()` in `export.py`: `--db` default `None`, `--all-tables` requires `--db`, exit 1 on missing source, docstring fix
- **T006**: Added `tests/unit/test_audit_export_trail.py` covering AC-1/2/3/4/5 with tmp trail fixtures (incl. synthetic `audit.1`)
- **T007**: Created `scripts/export-audit-evidence.ps1` (run export, append run log, `-Date`, `-Commit` with push+rebase fallback)
- **T008**: Reworked `.github/workflows/audit-export.yml` into daily freshness guard (bash-only, no `setup-uv`/`uv sync`, dropped `date`/`all-tables` inputs, `workflow_dispatch` guard re-run, `if: always()` artifact + deploy-key commit)
- **T009**: `git rm --cached audit/audit.db` and added `audit/` to `.gitignore`
- **T010**: Backfilled evidence: exported 2026-10-01 (46 lines), 2026-10-03 (84), 2026-10-04 (41); skipped 10-02; seeded `reports/evidence/audit-export-runs.jsonl`
- **T011**: Targeted tests passed: `uv run pytest tests/unit/test_audit_export_trail.py tests/unit/test_evidence_separation.py` (10/10 passed)
- **T012**: Full gates passed: `uv run ruff check src/` (clean), `uv run mypy src/` (265 files clean), `uv run pytest` (2624 passed), `pwsh scripts/lint-ecl.ps1` (ECL lint passed)
- **T013**: Manual AC verified: export produces non-empty JSONL for 2026-10-01/03/04, exit 0 on quiet day, exit 1 on missing source, trail renamed test
- **T014**: ECL recorded: `validation_status: pass`, `phase: implement`, close completed, `docs/STATUS.md` updated, `harness/evolution/pending.md` noted

### Key Decisions Recorded (D-a through D-f)
- **D-a**: Export runs locally (`scripts/export-audit-evidence.ps1` + Task Scheduler); CI workflow becomes a freshness guard only
- **D-b**: Untrack `audit/audit.db` and gitignore `audit/` only; `.lightspeed/memory/*` stays tracked
- **D-c**: Zero-row day → no file, exit 0; missing source → exit 1
- **D-d**: Run log `reports/evidence/audit-export-runs.jsonl` distinguishes quiet day from "didn't run"
- **D-e**: Backfill last 3 active days: 2026-10-01 (46), 2026-10-03 (84), 2026-10-04 (41); skip 10-02 (0)
- **D-f**: `harness/evolution/pending.md` (5 pending archives) → note only in STATUS handoff

### Artifacts Delivered
- `src/ai_company/audit/export.py` — new exporter, CLI rewire, docstring
- `src/ai_company/audit/integrity.py` — public `ordered_audit_files()`
- `tests/unit/test_audit_export_trail.py` — 10 tests, all passing
- `scripts/export-audit-evidence.ps1` — PowerShell local runner
- `.github/workflows/audit-export.yml` — guard rework
- `.gitignore` — `audit/` entry updated
- `reports/evidence/audit-2026-10-0{1,3,4}.jsonl` — generated evidence files
- `reports/evidence/audit-export-runs.jsonl` — append-only run marker
- `harness/changes/archive/2026-10-04-audit-export-reads-canonical-jsonl-trail/` — archived change set

## What Remains / Deferred
- **None** — all implementation, validation, and close-out tasks are complete
- The 5 pending archives in `harness/evolution/pending.md` are noted only for STATUS handoff context; no action required

## Next Steps
1. **No immediate actions required** — the change is fully implemented, validated, and archived at `phase: implement`
2. The ECL `audit-export-reads-canonical-jsonl-trail` is closed and can remain archived
3. If future audit evidence work is needed, reference the archived change set at `harness/changes/archive/2026-10-04-audit-export-reads-canonical-jsonl-trail/`
4. Monitor `harness/evolution/pending.md` for any resolution of the 5 pending archives (notified in STATUS.md per D-f)
5. The next Issue 5–related change should follow the same ECL lifecycle: `phase: validate` or `phase: implement` → full gate pass → `validation_status: pass` → close → archive
