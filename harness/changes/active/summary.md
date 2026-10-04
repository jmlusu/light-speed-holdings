---
title: "Audit export reads canonical JSONL trail"
slug: "audit-export-reads-canonical-jsonl-trail"
status: "in_progress"
location: "active"
phase: "plan"
intake_status: "complete"
spec_review: "approved"
plan_review: "approved"
modules:
  - "audit.export"
  - "audit.integrity"
files:
  - "src/ai_company/audit/export.py"
  - "src/ai_company/audit/integrity.py"
  - "tests/unit/test_audit_export_trail.py"
  - "scripts/export-audit-evidence.ps1"
  - ".github/workflows/audit-export.yml"
  - ".gitignore"
  - "docs/adr/008-evidence-separation.md"
  - "docs/adr/008-evidence-separation-sequence.md"
  - "docs/runbooks/evidence-stores-dr.md"
tags:
  - "audit"
  - "evidence"
  - "issue-5"
validation_status: "unknown"
created_at: "2026-10-04"
updated_at: "2026-10-04"
session_id: "7611da92-f453-48cc-9baa-1915055b9926"
owner_agent: "jmlus"
claimed_at: "2026-10-04"
---

# Summary

## Outcome

Issue 5 fix in progress: daily audit evidence export repointed from the 0-row tracked decoy `audit/audit.db` to the canonical hash-chained trail (`get_audit_path()` → `<data root>/.opencode/audit` + rotated siblings), with a local export runner + run log and a CI freshness guard (CI can never export — the trail is gitignored).

## Decisions

- D-a: Export runs locally (`scripts/export-audit-evidence.ps1` + Task Scheduler); CI workflow becomes a freshness guard only.
- D-b: Untrack `audit/audit.db` and gitignore `audit/` only; `.lightspeed/memory/*` stays tracked.
- D-c: Zero-row day → no file, exit 0; missing source → exit 1.
- D-d: Run log `reports/evidence/audit-export-runs.jsonl` distinguishes quiet day from "didn't run".
- D-e: Backfill last 3 active days: 2026-10-01 (46), 2026-10-03 (84), 2026-10-04 (41); skip 10-02 (0).
- D-f: `harness/evolution/pending.md` (5 pending archives) → note only in STATUS handoff.

## Validation

- Pending (T011-T013: targeted tests, ruff/mypy/pytest/lint-ecl, manual AC run).

## Next Step

- T003: promote `ordered_audit_files()` in `src/ai_company/audit/integrity.py`, then T004/T005 exporter + CLI rewire. Set `phase: implement`.
