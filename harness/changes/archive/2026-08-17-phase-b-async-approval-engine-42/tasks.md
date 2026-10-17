# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.

## Implementation

- [x] T002 [P] Create ADR-017 documenting the async approval engine decision → `docs/adr/017-async-approval-engine.md`
- [x] T003 [P] Create `SuspendedState` model and `SuspendStore` class → `src/ai_company/orchestrator/suspend_store.py`
- [x] T004 [P] Create `ApprovalNotifier` class with WebSocket + webhook support → `src/ai_company/orchestrator/notifier.py`
- [x] T005 [P] Create default webhook config → `company/config/webhooks.yaml`
- [x] T006 Modify `AgentLoop.run()` to accept `resumed_state` parameter and restore conversation history → `src/ai_company/executor/agent_loop.py`
- [x] T007 Wire `SuspendStore` into executor `_park_task()` and `_resume_approved_task()` → `src/ai_company/executor/loop.py`
- [x] T008 Wire `ApprovalNotifier` into executor `_park_task()` for push notifications → `src/ai_company/executor/loop.py`
- [x] T009 Add `sweep_suspended_states()` to daemon governance cadence → `src/ai_company/executor/daemon.py`
- [x] T010 Write tests for `SuspendStore` (save/load/delete/sweep) → `tests/unit/test_suspend_store.py`
- [x] T011 Write tests for `ApprovalNotifier` (WebSocket + webhook) → `tests/unit/test_approval_notifier.py`
- [x] T012 Write integration test: park → suspend → resume → verify conversation continuity → `tests/unit/test_hitl_nonblocking.py` (extend)

## Validation

- [x] T013 Run `uv run ruff check src/` — lint clean
- [x] T014 Run `uv run mypy src/` — type clean
- [x] T015 Run `uv run pytest tests/unit/test_suspend_store.py tests/unit/test_approval_notifier.py -v` — new tests pass (28/28)
- [x] T016 Run `uv run pytest` — full suite passes (1743 passed, 1 pre-existing doc failure unrelated to this change)
- [x] T017 Run `.\scripts\lint-ecl.ps1` — ECL structure valid

## Deferred Tasks

- None.
