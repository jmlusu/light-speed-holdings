# Tasks: Documentation Drift Prevention

## Phase 1: Source-of-Truth Registry

- [ ] T001 [P1] [knowledge-manager] Draft `docs/source-of-truth.yaml` with 5-10 critical claims
- [ ] T002 [P1] [registry-owner] Verify source file locations, extractors, and expected values
- [ ] T003 [P1] [technical-documentation-lead] Audit active docs to identify all claims that need tracking

## Phase 2: Automated Validation

- [ ] T004 [P1] [fullstack-engineer] Build `scripts/validate-drift.ps1` that reads the manifest
- [ ] T005 [P1] [qa-automation-engineer] Write `tests/docs/test_doc_drift.py`
- [ ] T006 [P1] [devops-lead] Add drift validation to `.pre-commit-config.yaml`
- [ ] T007 [P2] [fullstack-engineer] Build path-pattern scanner (catches `Path(__file__).parent.parent` anti-pattern)

## Phase 3: Process & Ownership

- [ ] T008 [P2] [compliance-officer] Update `CONTRIBUTING.md` with ownership model
- [ ] T009 [P2] [sop-owner] Create drift prevention SOP in `docs/DRIFT-PREVENTION.md`

## Verification

- [ ] T010 [P1] [qa-automation-engineer] Run full validation suite: validate-drift.ps1 + pytest + ruff + mypy
