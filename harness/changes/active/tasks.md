# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation (spec approved; plan approved; see `reviews/review.md`).

## Implementation

- [x] T002 Refresh competitive-landscape.md baseline v2 → v3 (§8 November 2026 Delta added, header updated, per-player deltas updated, §7 monthly checklist advanced to 2026-12-16, source URLs stamped, honesty tags applied).
- [x] T003 Update scoreboard-v1.md decision entry 7 (T5 #447 Nov refresh baseline v3, §8 reference).
- [x] T004 Correct Gap 5 false claim in social-media-positioning-status.md ("No competitive landscape document exists") — note: this follows the competitive-landscape.md refresh but is a separate change.

## Validation

- [x] T005 Run `pwsh scripts/maintenance/lint-ecl.ps1`; `ruff check src/ && mypy src/ && pytest` passes.
- [x] T006 Section 8 content cross-checked against source URLs; honesty tags present and correct per ADR-020/033.
- [x] T007 No unrelated file modifications: data/orchestrator/cost_tracker.json, open-design submodule, src/data/generated/agent-registry.public.json left as-is.

## Deferred Tasks

- None in this change. The Gap 5 correction in `docs/marketing/social-media-positioning-status.md` is tracked separately and was not part of this refresh.
