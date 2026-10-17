# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation. (Done 2026-10-07 — spec/plan written from authorized T5 pull-up; user decisions 1–3 + proceed order recorded; `plan_review: approved`.)

## Implementation

- [x] T002 Census + single-source list in `summary.md` (registry 90 = 89 AI + 1 human CEO; 19 exec / 64 spec / 7 board; 20-dept table; mirrors + artifacts verified). Validation: counts recomputed from files, not copied.
- [x] T003 `docs/source-of-truth.yaml` stale-comment fix (line 23). Validation: `test_doc_drift.py` green, manifest `current_value` untouched.
- [x] T004 `docs/NARRATIVE-AND-POSITIONING.md` reconciliation (§§5e/5f/§7/§9). Validation: no "has 19"/"say 152" remains outside history.
- [x] T005 Live-count fixes: `docs/EXECUTIVE-STRATEGY-EXPANSION.md:8`, `docs/marketing/warmup-content-pack/linkedin-post.md:60`, `docs/Pharos/linkedin-intro-post.md:94-99`. Validation: targeted grep shows 90/20 only.
- [x] T006 Triage record: `docs/MASTER_SPEC.md:105-115`, `post-11/video-script.md:13,22` confirmed intentional (no edit). Validation: rationale in spec assumptions. (Addendum: MASTER_SPEC guard list fenced in backticks so the intentional examples pass the `validate-architecture.ps1` quote-guard; no wording change.)

## Validation

- [x] T007 Full gates: `ruff check src/`, `mypy src/`, generator (90/0 errors), `sync-registry --verify`, `validate-drift.ps1`, `validate-architecture.ps1`, doc drift/count tests, full non-e2e `pytest`, `lint-ecl.ps1`. Validation: all green, results in `summary.md validation_results`.
- [ ] T008 ECL close (`close completed`) + resolution comment on #421 with PR link + T6-#422 unblock note. Validation: archive exists, issue updated.

## Deferred Tasks

- Remote GitHub README sync (152/151 stale) + site-copy "140+" sweep — follow-up, out of local-repo scope.
