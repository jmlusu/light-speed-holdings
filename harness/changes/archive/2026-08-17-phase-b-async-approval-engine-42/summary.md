---
title: "Phase B: Async Approval Engine (#42)"
slug: "phase-b-async-approval-engine-42"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "complete"
spec_review: "approved"
plan_review: "approved"
modules:
  - "ai_company.orchestrator.suspend_store"
  - "ai_company.orchestrator.notifier"
  - "ai_company.executor.loop"
  - "ai_company.executor.agent_loop"
  - "ai_company.executor.daemon"
files:
  - "src/ai_company/orchestrator/suspend_store.py"
  - "src/ai_company/orchestrator/notifier.py"
  - "company/config/webhooks.yaml"
  - "src/ai_company/executor/agent_loop.py"
  - "src/ai_company/executor/loop.py"
  - "src/ai_company/executor/daemon.py"
  - "docs/adr/017-async-approval-engine.md"
  - "tests/unit/test_suspend_store.py"
  - "tests/unit/test_approval_notifier.py"
tags:
  - "hitl"
  - "approval"
  - "async"
  - "suspend-to-disk"
  - "webhook"
  - "phase-b"
  - "issue-42"
validation_status: "pass"
created_at: "2026-08-17"
updated_at: "2026-08-17"
---

# Summary

## Outcome

Implement async approval engine: persist agent loop state to disk when tasks are parked for HITL, resume from persisted state instead of re-running from scratch, and push approval notifications via WebSocket + optional outbound webhook. 30-day hold for suspended state.

## Decisions

- **ADR-017**: File-based suspend store (not Temporal) — single-machine constraint
- Conversation history serialized as JSON strings in `.opencode/suspended_states/{task_id}.json`
- WebSocket broadcast fires immediately on park (sync→async bridge from executor)
- Optional webhook POST to configurable URL in `company/config/webhooks.yaml`
- 30-day retention with daemon governance sweep
- `SuspendedState` model: conversation_history, iterations_completed, tool_results, cost accumulators
- `AgentLoop.run()` accepts `resumed_state` kwarg for state restoration
- Agent loop snapshots state before `run_plan()` so HITLParked can capture it

## Validation

- ruff check src/: PASS (0 errors)
- mypy src/: PASS (0 errors, 155 files)
- pytest tests/unit/test_suspend_store.py: 17/17 PASSED
- pytest tests/unit/test_approval_notifier.py: 11/11 PASSED
- pytest (full suite): 1743 passed, 1 pre-existing doc failure (unrelated)
- lint-ecl.ps1: PASS

## Next Step

- Close as completed, update docs/STATUS.md.
