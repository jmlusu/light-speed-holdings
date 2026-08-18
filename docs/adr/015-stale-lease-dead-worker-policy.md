# ADR-015: Stale-Lease and Dead-Worker Claim Policy

## Status

Proposed — 2026-08-17

## Context

When an executor process dies while processing a task, the task's lease expires and the task is left `in_progress` in the inbox with no live owner. The stale detector (`detect_stale_tasks()`) currently moves such tasks to the dead-letter queue (DLQ) for manual operator intervention. Two related problems exist:

1. **No automatic recovery** — transient failures (OOM, network blip, executor restart) cause tasks to go to the DLQ even though a simple retry would succeed. Operators must manually run `dlq retry <task_id>`.

2. **Double-resume race** — two concurrent `ai-company executor tick` instances can both observe a `waiting_approval` task, both transition it to `pending`, and both attempt to claim it. The `claim_task` CAS prevents double-execution but the wasted agent loop run is an unnecessary cost.

The SSOT for task lifecycle state is `.opencode/inbox.json` via `MessageBus` (ADR-014 follow-up from #57).

## Decision

### 1. Auto-Retry Before DLQ

When the stale detector observes an `in_progress` task whose lease has expired:

- **If `retry_count < retry_budget`**: increment `retry_count`, set status to `pending`, re-enqueue via `send_task()`. Log at INFO: `"Task %s stale — auto-retrying (%d/%d)"`.
- **If `retry_count >= retry_budget`**: move to DLQ with enriched metadata. Log at WARNING: `"Task %s stale — retry budget exhausted, moved to DLQ"`.

**Retry budget**: `retry_budget` field on the task dict, defaulting to global constant `STALE_RETRY_MAX = 3`. Tasks can override via `retry_budget` in their metadata. `retry_count` starts at 0 and is incremented on each stale detection.

**Backoff**: immediate re-enqueue. The lease itself provides natural backoff — each re-claimed task gets a fresh 30-minute lease, so the minimum spacing between retries is ~30 minutes (the stale detection interval).

### 2. DLQ Entry Enrichment

DLQ entries inherit the full task dict including `retry_count` and `retry_budget`. A `dlq_reason` field is added to the entry with value `"stale_lease_exhausted"`. The `dlq_list` CLI output displays these fields.

### 3. Double-Resume CAS Gate

A new `resume_task(task_id, expected_status)` method on `MessageBus` provides a CAS-guarded transition from `waiting_approval` to `pending`. The `_resume_approved_task` path calls this instead of `update_task_status`, so two concurrent executors racing on the same parked task will have the second one skip (returns `None`).

### 4. No PID Guard for Tick Mode

`ai-company executor tick` remains unguarded at the process level. Concurrent tick instances are safe via file locks + CAS. The CAS gate from decision 3 handles the resume race. Users who want parallelism can run multiple ticks.

### 5. DLQ Expiry

DLQ entries are retained indefinitely. No automatic purge. Operators clear via `dlq_clear`. (Deferred — TTL expiry is a future enhancement if DLQ bloat becomes a concern.)

## Consequences

- Transient failures self-heal without operator intervention (common case).
- Poison tasks (fail repeatedly) are caught by the retry budget and land in the DLQ with full diagnostic metadata.
- Two concurrent executor instances cannot both resume the same parked task (the CAS gate eliminates wasted agent loops).
- Task schema gains two new optional fields (`retry_count`, `retry_budget`) — backward compatible (missing fields default to 0 and 3 respectively).
- The stale detector's logic grows from a simple move-to-DLQ to a budget-check-then-move-or-retry decision, but the code path is straightforward.
