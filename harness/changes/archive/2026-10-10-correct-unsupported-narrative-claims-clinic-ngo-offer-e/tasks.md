# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation. (spec written; plan_review pending until wording approval)
- [x] T002 Create this ECL change via `harness-change.ps1 new` (done 2026-10-10; active slot was free).

## Wave 1 (parallel)

- [ ] T003 [P] `explore` sweep: verify every `file:line` citation in `docs/AUDIT-NARRATIVE-CLAIMS-2026-10-10.md` against live files; return correction list.
- [ ] T004 [P] `clo` briefing: Offer B/C gate conflict options + recommendation → save to `harness/changes/active/reviews/offer-bc-gate-briefing.md` (no code change).

## Wave 2

- [ ] T005 Apply citation corrections to `docs/AUDIT-NARRATIVE-CLAIMS-2026-10-10.md` (if T003 finds drift).
- [ ] T006 `thought-leadership-author`: draft corrected CEO-voice wording for CL-01..CL-07.
- [ ] T007 `chief-of-staff`: honesty cross-check of T006 draft vs `USE-CASE-CATALOG` + ADR-020.
- [ ] T008 STOP: present draft to user for approval; set `plan_review: approved` in `summary.md` front matter upon approval.
- [ ] T009 Apply approved wording to `docs/NARRATIVE-AND-POSITIONING.md`.

## Validation

- [ ] T010 `lint-ecl.ps1` → PASS; `harness-change.ps1 validate` → valid.
- [ ] T011 `uv run pytest tests/docs/ -q` → PASS.
- [ ] T012 Full non-e2e suite `uv run pytest tests/unit -q` → PASS; snapshot `git status` before/after (ECL §4).
- [ ] T013 Populate `summary.md` `validation_results`, `validation_status: pass`, phase `validate`.

## Close / Handoff

- [ ] T014 Update `docs/STATUS.md`; `harness-change.ps1 close completed`; re-run `lint-ecl.ps1`.
- [ ] T015 Final handoff: subagents that actually returned vs. done directly; briefing awaiting CEO decision.

## Deferred Tasks

- Offer B/C gate decision (CEO/CLO) — tracked in `reviews/offer-bc-gate-briefing.md`, intentionally not executed.
- `harness/evolution/pending.md` — ignored per user decision.
