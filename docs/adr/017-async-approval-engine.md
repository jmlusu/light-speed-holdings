# ADR-017: Async Approval Engine — Suspend-to-Disk + Push Notifications

**Status:** Accepted
**Date:** 2026-08-17
**Deciders:** CTO, COO, Human CEO
**Technical Domain:** Executor / HITL

## Context

Requirement T9 (issue #42) demands async pauses with state suspended to disk
(30-day hold) and an asynchronous notification flow. Today:

1. **State is lost on park.** When `ToolRunner` raises `HITLParked`, the executor
   catches it and transitions the task to `WAITING_APPROVAL`. On resume, the
   agent loop re-runs from scratch with `preapproved=True` — the full
   `conversation_history`, accumulated `ToolCallRecord`s, iteration count, and
   cost data are discarded. A task that completed 8 iterations of work re-does
   all 8 after resume, wasting LLM tokens and time.

2. **No outbound notification.** Approvers must poll via CLI
   (`ai-company orchestrator approval pending`) or dashboard. The WebSocket
   `_broadcast_approval_alert` fires only when the dashboard endpoint is
   queried, not when the executor parks a task. There is no webhook for
   external systems (Slack, email, mobile push).

3. **No retention policy for suspended state.** If we did persist state, there
   is no cleanup mechanism. The daemon's governance cadence handles approval
   expiry and archival, but nothing manages workflow state files.

The blockers for this decision (#34 event-bus, #37 RBAC) are both resolved:
the JSON MessageBus is kept (ADR-010) and dashboard RBAC is in place (ADR-012).

## Decision

Implement a file-based suspend store and outbound notification surface.

### 1. SuspendStore — Persist agent loop state on park

- New module `src/ai_company/orchestrator/suspend_store.py`.
- `SuspendedState` Pydantic model captures: `task_id`, `conversation_history`
  (list of strings — the full LLM context), `iterations_completed`,
  `tool_results` (list of dicts), `total_prompt_tokens`,
  `total_completion_tokens`, `total_cost_usd`, `parked_at` (UTC), `agent_name`,
  `priority`.
- `SuspendStore` class backed by `FileStore` (atomic writes, same pattern as
  `ApprovalGate`):
  - `save(task_id, state)` → `.opencode/suspended_states/{task_id}.json`
  - `load(task_id) → SuspendedState | None`
  - `delete(task_id)` — remove after successful resume
  - `sweep_expired(retain_days=30)` — daemon governance cleanup
- Serialized state capped at 1 MB; if exceeded, oldest iterations truncated
  from the front of `conversation_history`.

### 2. ApprovalNotifier — Push notifications on park/resolve

- New module `src/ai_company/orchestrator/notifier.py`.
- `ApprovalNotifier` class:
  - `notify_parked(request_id, task_id, agent_id, tool, description, tier)`:
    fires WebSocket broadcast via sync→async bridge + optional webhook POST.
  - `notify_resolved(request_id, task_id, decision)`: fires resolution
    broadcast.
- WebSocket: uses existing `dashboard.ws.broadcast_alert` with
  `category="approval"`. Fires from the executor via the sync→async bridge
  (same pattern as `make_message_bus_broadcast_callback`).
- Webhook: HTTP POST to URLs listed in `company/config/webhooks.yaml`.
  Config structure:
  ```yaml
  webhooks:
    - url: "https://example.com/hook"
      secret: ""          # HMAC-SHA256 signing secret (optional)
      events: ["parked"]  # filter: parked, resolved, all
  ```
  Fire-and-forget with best-effort logging; never blocks the executor.
- Webhook payload includes: `event`, `request_id`, `task_id`, `agent_id`,
  `tool`, `description`, `tier`, `timestamp`. Signed with HMAC-SHA256 when
  `secret` is configured.

### 3. AgentLoop integration

- `AgentLoop.run()` gains `resumed_state: SuspendedState | None` kwarg.
- When provided, initializes `conversation_history` from the persisted state
  and starts the iteration loop from `iterations_completed + 1`.
- Tool results from prior iterations are already embedded in the conversation
  history strings, so no separate replay is needed.

### 4. Executor wiring

- `_park_task()`: after catching `HITLParked`, calls
  `SuspendStore.save(task_id, state)` with the loop result data, then
  calls `ApprovalNotifier.notify_parked()`.
- `_resume_approved_task()`: calls `SuspendStore.load(task_id)`, passes
  state to `AgentLoop.run(resumed_state=...)`, calls
  `SuspendStore.delete(task_id)` on success.
- Both suspend store and notifier are instantiated in `Executor.__init__()`.

### 5. Daemon governance sweep

- `_sweep_suspended_states()` added to the daemon's governance cadence.
- Calls `SuspendStore.sweep_expired(retain_days=30)` to remove stale files.

## Consequences

- **Positive:** Tasks resume from where they left off (no wasted LLM tokens);
  humans get immediate push notifications; external systems can integrate via
  webhooks; 30-day retention prevents unbounded disk usage; all existing
  approval patterns preserved.
- **Negative / risk:** Serialized conversation history may be large for
  long-running tasks (mitigated by 1 MB cap); webhook delivery is
  best-effort (failures logged, not retried); resumed loops may produce
  different LLM responses (by design — non-deterministic).
- **Neutral:** No new external dependencies; FileStore atomic writes ensure
  crash safety; existing `pending_approvals.json` index and
  `approvals.yaml` SSOT unchanged.

## Links

- Issue #42: "Decide the persisted async approval engine"
- Requirement T9: async pauses with state suspended to disk
- ADR-010: JSON MessageBus (kept)
- ADR-012: Dashboard RBAC (notification endpoints gated by `approve` role)
- Evidence: `tests/unit/test_suspend_store.py`, `tests/unit/test_approval_notifier.py`
