# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation. User-approved scope (delete both extra same-slug duplicates) recorded in spec Resolved Clarifications.

## Implementation

- [x] T002 Create ECL change (this dir) via `harness-change.ps1 new` on worktree `wt-ecl-dedup` / branch `chore/ecl-changes-dedup`.
- [x] T003 `git rm -r` the seven proven-stale parking dirs (2026-09-22-narrative, 2026-09-23-narrative, 2026-09-24-v2-0, 2026-09-24-v2-0-2, 2026-09-25-v2-0, 2026-09-24-ls-mem-phase-2-architecture, 2026-10-03-customer-journey).
- [x] T004 `git rm -r` bare `2026-09-24-ai-venture-studio-execution-plan-parts-2-5` stub; `git mv` `-parts-2-5-2` onto canonical bare name.
- [x] T005 Add epilogue note to `knowledge/technology/bug-fixes/BUG-81c94142a.md`.
- [x] T006 `harness-change.ps1 reindex` under PS 5.1; confirm 52 entries, zero duplicate ids/slugs.

## Validation

- [x] T007 `lint-ecl.ps1`, `check-index-freshness.ps1`, `validate-drift.ps1` all PASS.
- [x] T008 Full non-e2e pytest with isolated basetemp + git-status before/after snapshot (ECL section 4).
- [ ] T009 Post-merge: delete remote branch, prune local leftovers (AGENTS section 17). Inherently outside this change's control — executed by the merger.

## Deferred Tasks

- Deferred (post-merge, executed by the merger): T009 delete the remote branch and prune local leftovers after squash-merge (AGENTS section 17).
- Optional follow-up: script-level duplicate-id guard in `Get-IndexEntries` (out of scope per spec Non-Goals).
