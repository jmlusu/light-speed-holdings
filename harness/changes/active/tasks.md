# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation. (Intake complete; spec + plan review done 2026-09-17)

## Implementation

- [x] T002 Append 7 Marketing specialists (`creative_director`, `presentation_designer`, `document_designer`, `diagram_designer`, `visual_storyteller`, `brand_advertising_designer`, `artifact_qa_reviewer`) to `company-registry.yaml` after `media_generation_owner`. (Done 2026-09-17)
- [x] T003 Run `uv run ai-company generate` to sync `company/agent-registry.json` and regenerate `.opencode/agents/*.md` + `docs/AGENT-REGISTRY-TABLE.md`. (Done 2026-09-17)
- [x] T004 Verify counts: `load_registry()` -> 20 exec / 125 spec / 7 board / 152 total; `.opencode/agents/*.md` = 152. (Done 2026-09-17: 152 registry entries; 152 agent cards; 152 agent-registry.json)
- [x] T005 Update `docs/source-of-truth.yaml` `agent_count` 145 -> 152 (+ comment update). (Done 2026-09-17)
- [x] T006 Sweep count-bearing docs: `README.md`, `docs/USER-GUIDE.md`, `docs/ORGANIZATION.md`, `docs/API-REFERENCE.md`, `docs/STATUS.md`, `CHANGELOG.md`, `research/site-claims-ledger.md`, `brand-strategy-validation-report.md`, `UX_VALIDATION_REPORT.md` (145/144 -> 152/151). (Pharos pillars + marketing/social/atomized/newsletter + framework + manifestos + whitepaper + articles + pillars also swept; only line-range refs excluded — see plan.md scope note)

## Validation

- [ ] T007 Run gates: `uv run ai-company sync-registry --verify`, `.\scripts\validate-drift.ps1`, `uv run pytest tests/docs/test_doc_drift.py`, `.\scripts\lint-ecl.ps1`, `uv run ruff check src/`, `uv run mypy src/`, `uv run pytest`.
- [ ] T008 Record `validation_results` in `summary.md`; update `docs/STATUS.md`; close change via harness.

## Deferred Tasks

- None.
