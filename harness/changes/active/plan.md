# Plan

## Technical Approach

- Wave 1 (parallel, read-only outside `active/`): create this change; `explore` subagent sweeps every citation in `docs/AUDIT-NARRATIVE-CLAIMS-2026-10-10.md`; `clo` subagent drafts the Offer B/C gate briefing (options + recommendation, no code change).
- Wave 2: fix any drifted audit citations (direct edit); `thought-leadership-author` drafts corrected wording for CL-01..CL-07; `chief-of-staff` honesty-cross-checks the draft against the catalog; stop for user approval; then set `plan_review: approved` and apply edits to `docs/NARRATIVE-AND-POSITIONING.md`.
- Wave 3: `qa-lead` runs validation gates; populate `validation_results`; update `docs/STATUS.md`; `harness-change.ps1 close completed`; re-run `lint-ecl.ps1`.
- Load skill `ecl-harness-engineer` for lifecycle mechanics; it is never passed as `subagent_type`.

## Impacted Modules And Files

- `docs/NARRATIVE-AND-POSITIONING.md` (edit — the only governed doc touched)
- `docs/AUDIT-NARRATIVE-CLAIMS-2026-10-10.md` (citation corrections, if sweep finds drift)
- `harness/changes/active/**` (spec/plan/tasks/summary + `reviews/offer-bc-gate-briefing.md`)
- `docs/STATUS.md` (handoff at close)
- Read-only: `USE-CASE-CATALOG.md`, `malawi_offers.yaml`, `client_intake.py`, `client-onboarding-policy.md`

## Interfaces, Data, Permissions

- No API/data-model/permission changes; no `src/` changes, so `ruff`/`mypy` not in scope.
- Subagent writes: only the main agent writes files; subagents return content (prevents write friction).

## Spec Gaps Found From Planning

- None; three intake questions were resolved by the user before build mode.

## Risks And Mitigations

- Wordings drift stronger than artifacts → chief-of-staff cross-check + user approval gate.
- Concurrent dirty working tree interferes with full-suite run → snapshot `git status` before/after (ECL §4 hint).
- A `task` call rejects a subagent name → do the piece directly and report honestly.

## Verification Plan

- `pwsh scripts/maintenance/lint-ecl.ps1` → PASS
- `uv run pytest tests/docs/ -q` → PASS (includes `test_doc_drift.py`)
- `uv run pytest tests/unit -q` full non-e2e suite → PASS at archive (ECL §4 requirement)
- `.\scripts\maintenance\harness-change.ps1 validate` → valid
- Manual: all 7 claims traceable to a verified artifact status after edit
