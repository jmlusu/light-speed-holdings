---
title: "ECL changes dedup - remove stale duplicate parking copies"
slug: "ecl-changes-dedup-remove-stale-duplicate-parking-copies"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "approved"
spec_review: "approved"
plan_review: "approved"
modules: []
files:
  - "harness/changes/INDEX.json"
  - "harness/changes/parking/*"
  - "knowledge/technology/bug-fixes/BUG-81c94142a.md"
tags: ["ecl", "harness", "dedup", "index"]
validation_status: "pass"
created_at: "2026-10-12"
updated_at: "2026-10-12"
session_id: "156963b8-f898-4dcb-9bbe-3890595189f2"
owner_agent: "jmlus"
claimed_at: "2026-10-12"
---

# Summary

## Outcome

Deduplicated `harness/changes/parking/` so every change id exists exactly once in `INDEX.json`. Removed 7 proven-stale parking directories (6 indexed + 1 `.gitkeep`-only), removed the bare `parts-2-5` stub that duplicated the `-parts-2-5-2` indexed copy, renamed `-parts-2-5-2` onto the canonical bare name, and added a historical epilogue to `BUG-81c94142a.md`. INDEX regenerated under PS 5.1: **59 → 52 entries** (46 archive + 6 parking), zero duplicate ids, zero duplicate slugs. The pre-execution estimate of 51 was off by one: the bare `parts-2-5` stub *was* indexed (both stub and `-2` carried `summary.md`), so the slug appeared twice pre-rename and once post-rename — net −7 parking entries, matching 59−7=52.

## Decisions

- User approved (2026-10-12): delete the 4 id-collision parking copies + the 2 hand-suffixed `-2` parking copies, PLUS two further same-slug duplicates found during investigation: `2026-09-25-...-v2-0` (proven stale snapshot) and `2026-09-22-narrative-...` (superseded intake skeleton).
- Evidence rules: archive copies are authoritative in every confirmed pair; parking copies hold no unique files (the one "unique" file in `v2-0-2` is byte-identical to the archive copy of `v2-implementation-p2`).
- External references checked: `docs/STATUS.md` references the archive ls-mem path (stays valid) and the parts-2-5 slug (stays valid after rename); no external refs to any deleted dir.
- Count reconciliation (2026-10-12): 13 parking dirs pre-state → 6 post-state; 6 indexed deletions + 1 indexed bare-stub deletion = 7 indexed removals; `ls-mem-phase-2-architecture` was `.gitkeep`-only (never indexed); rename preserves the `-2` entry under the bare slug. Spec/plan "51" predictions corrected to 52.

## Validation

- `lint-ecl.ps1` PASS (ps-antipattern 0 failures, ECL lint passed).
- `check-index-freshness.ps1` PASS (byte-fresh under Windows PowerShell 5.1, regenerated 52 entries).
- `validate-drift.ps1` PASS (87 files checked, all claims verified). Initial run in a venv-less worktree produced a false-negative JSON capture (`uv run` stdout noise); fixed by `uv sync --extra dev`, then clean PASS.
- Full non-e2e pytest with isolated basetemp: **2584 passed, 2 skipped, 0 failed** (290s, rc=0). The 5 previously observed `test_ecl_change_lifecycle` failures did not reproduce.
- Git-status before/after snapshot: exactly one drift (`src/data/generated/agent-registry.public.json`, a known generated side-effect of the suite) — restored per ECL §4 archive hygiene; no other files touched by the test run.
- INDEX audit (post-reindex): total 52 = archive 46 + parking 6; **zero duplicate ids, zero duplicate slugs**; remaining 6 parking ids enumerated and expected.

## Next Step

- STATUS.md handoff (ECL §7), then `harness-change.ps1 close completed` (which reindexes to 53 entries including this archived change), re-run lint-ecl + freshness, commit, push, open PR flagging the 2 user-approved scope additions and referencing `BUG-81c94142a`.
