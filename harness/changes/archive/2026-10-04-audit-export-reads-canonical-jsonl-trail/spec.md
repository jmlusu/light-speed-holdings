# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: mixed (issue report + approved plan)
- Questions asked this round: 6 (export runtime, cleanup scope, zero-row day, run-log marker, backfill scope, pending-evolution handling)

## Goal And Evidence

- Real problem or user request: Issue 5 — `reports/evidence/audit-2026-10-04.jsonl` is 0 bytes, so the daily audit evidence artifact carries no evidence (commit `fb402c03`).
- Current behavior: `src/ai_company/audit/export.py` reads `audit/audit.db`, a tracked SQLite file with the `audit_log`/`audit_meta` schema but **zero rows and no writer anywhere in the codebase** (added in `5ab90eda` / PR #412). It has no `WHERE` date filter (`--date` only renames the output), and `open(output, "w")` runs before any row is read, so every run writes a 0-byte file that CI commits.
- Source of evidence:
  - `src/ai_company/audit/export.py:22,81,151,226` (hardcoded source), `:55-60` (no date filter), `:62` (empty-file write).
  - Canonical trail `.opencode/audit`: 3,743,797 B, 6,394 rows, 0 malformed, 38 dates spanning 2026-08-25 → 2026-10-04; per-date counts 2026-10-01=46, 2026-10-02=0, 2026-10-03=84, 2026-10-04=41.
  - `src/ai_company/paths.py:78-89` `get_audit_path()` + comment documenting the ticket #59 decoy class.
  - `src/ai_company/audit/reader.py:23-28` `AuditReader` already defaults to `get_audit_path()`.
  - `.gitignore:62` gitignores `.opencode/audit` → GitHub Actions can never read the trail.

## User Scenarios And Success

- Primary user/system scenario: a scheduled local run exports the previous day's audit events to `reports/evidence/audit-<date>.jsonl`; a daily CI job confirms the export actually ran and produced a non-empty file.
- Success criteria: the dated evidence file contains the real events for that date; a quiet day produces no artifact and does not fail; a broken wiring (trail missing) fails loudly.
- Acceptance criteria:
  - AC-1: `uv run python -m ai_company.audit.export --date 2026-10-04` writes `reports/evidence/audit-2026-10-04.jsonl` with 41 lines, every line UTC-dated 2026-10-04.
  - AC-2: `--date 2026-10-02` writes no file, exits 0, logs "0 events".
  - AC-3: trail file missing → exit 1, error logged, no output file.
  - AC-4: `--date 2026-10-01` yields 46 lines (proves the date filter).
  - AC-5: events in a rotated file (`.opencode/audit.1`) for the target date are included.
  - AC-6: `git status` shows no `audit/` entries; `git ls-files audit/` empty.
  - AC-7: tracked `audit-2026-10-04.jsonl` no longer 0 bytes; 10-01 and 10-03 files present.
  - AC-8: CI fails when the newest run-log entry is >36h old, or its `events > 0` but the matching dated file is missing/empty; passes otherwise, including quiet days.
  - AC-9: `ruff check src/`, `mypy src/`, `pytest`, `pwsh scripts/lint-ecl.ps1` all pass.

## Non-Goals

- Issues 1-4 (SMTP/Resend switch, Vercel DNS delegation, general gitignored junk, local stashes) — reported as findings only.
- `AuditEvent.correlation_id` schema change (open `gh #409`/`#403`).
- `data/ai_company.db.audit_events` SQLite mirror stopped emitting after 2026-10-01 (`writer.py:209` swallows failures at debug) — needs its own ticket.
- Untracking `.lightspeed/memory/{memory.db,audit/audit.db}` — explicitly left tracked.
- `harness/evolution/pending.md` auto-evolve — noted in the STATUS handoff only.

## Constraints

- Evidence must be a faithful copy of the trail: raw line passthrough, no `AuditEvent` re-serialization (preserves `__seq`, `__prev_hash`, future `correlation_id`).
- Legacy SQLite export paths stay intact for explicit `--db` (keeps `tests/unit/test_evidence_separation.py:190-232` green).
- ECL lifecycle applies (>2 files): one active change, stage front matter, `validation_status: pass` + `phase: validate` before close.
- ADR-008 must be amended (it documents the broken SQLite source) before `plan_review: approved`.

## Assumptions

- Timestamps in the trail are ISO-8601 with offsets; UTC-date comparison uses `datetime.fromisoformat(ts).date()`, not a raw string prefix.
- Local machine timezone differs from UTC; the CI freshness window is 36h to tolerate the CAT/UTC boundary.
- Rotation (10 MB, keep 5) has not triggered yet (active file 3.74 MB) but must be handled now.

## Open Questions

- None.

## Resolved Clarifications

- Export runtime: local script + CI freshness guard (CI never exports — the trail is gitignored).
- Cleanup scope: untrack `audit/` only.
- Zero-row day: no file, exit 0; missing source → exit 1.
- Quiet-day marker: adopt `reports/evidence/audit-export-runs.jsonl` run log.
- Backfill: last 3 active days (2026-10-01, 2026-10-03, 2026-10-04); 10-02 skipped.
- `harness/evolution/pending.md`: note only.
