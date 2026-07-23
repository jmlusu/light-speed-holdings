# MessageBus Deep Dive — Execution Plan (R1–R5)

> **Owner:** Chief of Staff (orchestrator)
> **Date:** 2026-07-23
> **Status:** READY FOR EXECUTION
> **Closes:** GAP-011 (full), GAP-020 (supplement)

---

## Executive Summary

The CTO's MessageBus Deep Dive identified 5 concrete recommendations (R1–R5) to harden the central nervous system of the AI company. This plan provides a complete delegation map, execution sequence, risk assessment, and verification checklist for each recommendation. **All work is delegated to specialist agents — the Chief of Staff orchestrates but does not write code.**

---

## 1. Delegation Map

### R1: Migrate KPI Collectors + Mobile API to MessageBus (GAP-011)

| Aspect | Detail |
|--------|--------|
| **Agent(s)** | `lead-backend` (primary), `qa-automation-engineer` (verification) |
| **Effort** | 3–4 hours |
| **Dependencies** | None (can start immediately) |
| **Summary** | Replace all 10 direct `inbox.json` file reads with `MessageBus.get_all_tasks()` calls |

**Task Prompt for `lead-backend`:**

```
MIGRATE KPI COLLECTORS + MOBILE API TO MESSAGEBUS (GAP-011 CLOSURE)

You must eliminate every direct read of `.opencode/inbox.json` and route all task data through the MessageBus.

## Files to Modify (10 total)

### 1. KPICollector Base Class — `src/ai_company/dashboard/kpis/base.py`
- Add optional `message_bus: MessageBus | None = None` parameter to `__init__`
- Add a `_get_tasks()` helper that returns `self._message_bus.get_all_tasks()` as raw dicts when a bus is injected, falling back to `self._load_json(".opencode/inbox.json")` for backward compatibility
- Import `from ai_company.orchestrator.message_bus import MessageBus`

### 2. Seven KPI Collectors (each in `src/ai_company/dashboard/kpis/`)
Replace `self._load_json(".opencode/inbox.json")` with `self._get_tasks()` in each:

- `engineering.py` line 17: `tasks: list[dict] = self._load_json(".opencode/inbox.json")` → `tasks: list[dict] = self._get_tasks()`
- `sales.py` line 19: `tasks = self._load_json(".opencode/inbox.json")` → `tasks = self._get_tasks()`
- `hr.py` — does NOT read inbox.json (only reads agent-registry.json and departments.yaml). No change needed.
- `finance.py` — does NOT read inbox.json. No change needed.
- `legal.py` line 19: `tasks = self._load_json(".opencode/inbox.json")` → `tasks = self._get_tasks()`
- `marketing.py` line 19: `tasks = self._load_json(".opencode/inbox.json")` → `tasks = self._get_tasks()`
- `customer_success.py` line 19: `tasks = self._load_json(".opencode/inbox.json")` → `tasks = self._get_tasks()`

### 3. Mobile API — `src/ai_company/dashboard/mobile_api.py`
Replace `_load_json(".opencode/inbox.json")` with `MessageBus.get_all_tasks()` at these call sites:
- Line 193 (`mobile_dashboard`): `tasks = _load_json(".opencode/inbox.json")` → `tasks = _get_bus().get_all_tasks_raw()`
- Line 256 (`mobile_tasks`): `tasks = _load_json(".opencode/inbox.json")` → `tasks = _get_bus().get_all_tasks_raw()`
- Line 404 (`_delegate_task`): `tasks = _load_json(".opencode/inbox.json")` → use bus
- Line 540 (`compact_kpis`): `tasks = _load_json(".opencode/inbox.json")` → use bus
- Line 778 (`mobile_sync`): `tasks = _load_json(".opencode/inbox.json")` → use bus

Add a `_get_bus()` helper at the top of mobile_api.py:
```python
from ai_company.orchestrator.message_bus import MessageBus
_bus: MessageBus | None = None

def _get_bus() -> MessageBus:
    global _bus
    if _bus is None:
        _bus = MessageBus()
    return _bus
```

### 4. CLI Executor — `src/ai_company/cli/executor.py`
Replace direct file reads with MessageBus calls:
- Line 128 (`run_task`): `tasks = json.loads(inbox_path.read_text(...))` → `bus.get_all_tasks_raw()`
- Line 197 (`status`): `tasks = json.loads(inbox_path.read_text(...))` → `bus.get_all_tasks_raw()`
- Line 302 (`dlq_retry`): `tasks = json.loads(inbox_path.read_text(...))` → `bus.get_all_tasks_raw()`

For `dlq_retry` specifically, replace the direct file append with `bus.send_task(Task(**restored))`.

### 5. Dead Letter Detector — `src/ai_company/executor/dead_letter.py`
- Line 118 (`detect_stale_tasks`): Replace `json.loads(inbox_path.read_text(...))` with a `MessageBus` parameter
- Change signature: `def detect_stale_tasks(bus: MessageBus, dlq: DeadLetterQueue, ...)`
- Use `bus.get_all_tasks_raw()` and `bus._mutate_tasks()` for removal
- Update all callers in `executor/loop.py` line 273

## Verification
After all changes:
1. Run `grep -r "_load_json.*inbox" src/ai_company/dashboard/ src/ai_company/cli/ src/ai_company/executor/dead_letter.py` — must return ZERO matches
2. Run `grep -r "inbox.json" src/ai_company/cli/ src/ai_company/executor/dead_letter.py --include="*.py"` — must return ZERO direct file reads
3. Run `ruff check src/ai_company/dashboard/ src/ai_company/cli/executor.py src/ai_company/executor/dead_letter.py`
4. Run `mypy src/ai_company/dashboard/ src/ai_company/cli/executor.py src/ai_company/executor/dead_letter.py`
5. Run `pytest tests/unit/test_message_bus_broadcast.py tests/integration/test_full_pipeline.py -v`
```

**Task Prompt for `qa-automation-engineer`:**

```
Write integration tests to verify GAP-011 closure:

1. Test that KPI collectors with injected MessageBus return the same data as file-based reads
2. Test that mobile_api endpoints read tasks through MessageBus (mock MessageBus, verify it is called)
3. Test that CLI `status`, `run_task`, and `dlq_retry` commands use MessageBus
4. Test that `detect_stale_tasks` uses MessageBus (not raw file reads)

File: `tests/integration/test_gap011_messagebus_migration.py`
```

---

### R2: Implement Priority-Based Task Ordering

| Aspect | Detail |
|--------|--------|
| **Agent(s)** | `lead-backend` (primary) |
| **Effort** | 1–2 hours |
| **Dependencies** | None |
| **Summary** | Sort pending tasks by priority before returning |

**Task Prompt for `lead-backend`:**

```
IMPLEMENT PRIORITY-BASED TASK ORDERING (R2)

Modify the MessageBus to return pending tasks sorted by priority (critical > high > medium > low).

## File to Modify: `src/ai_company/orchestrator/message_bus.py`

### Changes:

1. Add a priority sort order constant:
```python
PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}
```

2. Modify `get_pending_tasks()` (line 160-167):
```python
def get_pending_tasks(self) -> List[Task]:
    tasks = self._load_tasks()
    pending = [Task(**t) for t in tasks if t.get("status") == "pending"]
    pending.sort(key=lambda t: PRIORITY_ORDER.get(t.priority.value, 99))
    return pending
```

3. Modify `claim_next_pending()` (line 169-195):
Update the `_updater` lambda to iterate in priority order instead of insertion order:
```python
def _updater(tasks: List[dict]) -> List[dict]:
    nonlocal claimed
    # Sort pending tasks by priority
    pending_indices = [
        (i, PRIORITY_ORDER.get(t.get("priority", "medium"), 99))
        for i, t in enumerate(tasks)
        if t.get("status") == "pending"
    ]
    pending_indices.sort(key=lambda x: x[1])
    if pending_indices:
        idx = pending_indices[0][0]
        tasks[idx]["status"] = "in_progress"
        tasks[idx]["updated_at"] = now
        claimed = Task(**tasks[idx])
    return tasks
```

4. Also apply to `count_by_status()` — no change needed there since it only counts.

## Verification
1. Write unit test: Create 4 tasks with different priorities, verify `get_pending_tasks()` returns them in order: critical, high, medium, low
2. Write unit test: Verify `claim_next_pending()` claims the highest priority task first
3. Run `ruff check src/ai_company/orchestrator/message_bus.py`
4. Run `mypy src/ai_company/orchestrator/message_bus.py`
5. Run `pytest tests/unit/test_message_bus*.py -v`
```

---

### R3: Automatic Task-Level Retry with Exponential Backoff

| Aspect | Detail |
|--------|--------|
| **Agent(s)** | `lead-backend` (primary), `qa-automation-engineer` (testing) |
| **Effort** | 2–3 hours |
| **Dependencies** | None |
| **Summary** | Add retry_count, max_retries, next_retry_at to Task model; implement auto-retry on failure |

**Task Prompt for `lead-backend`:**

```
IMPLEMENT AUTOMATIC RETRY WITH EXPONENTIAL BACKOFF (R3)

Add task-level retry capability so failed tasks are automatically re-enqueued up to N times with exponential backoff.

## Step 1: Modify Task Model — `src/ai_company/models/models.py`

Add these fields to the `Task` class (after the `acknowledged_by` field, line 444):
```python
# Retry fields
retry_count: int = 0
max_retries: int = 3
next_retry_at: str = ""  # ISO timestamp
```

## Step 2: Modify MessageBus — `src/ai_company/orchestrator/message_bus.py`

Add a new method:
```python
def retry_task(self, task_id: str, delay_seconds: float) -> Task | None:
    """Schedule a failed task for retry after *delay_seconds*.

    Increments retry_count, computes next_retry_at, and sets status back to pending.
    Returns the updated Task or None if not found or max retries exceeded.
    """
    import time as _time
    from datetime import datetime as _dt

    def _updater(tasks: List[dict]) -> List[dict]:
        for i, t in enumerate(tasks):
            if t.get("id") == task_id:
                retry_count = t.get("retry_count", 0) + 1
                max_retries = t.get("max_retries", 3)
                if retry_count > max_retries:
                    logger.warning(
                        "Task %s exceeded max retries (%d) — not retrying.",
                        task_id, max_retries,
                    )
                    return tasks
                next_retry = _dt.now() + _dt.timedelta(seconds=delay_seconds)
                tasks[i]["retry_count"] = retry_count
                tasks[i]["next_retry_at"] = next_retry.isoformat()
                tasks[i]["status"] = "pending"
                tasks[i]["updated_at"] = _dt.now().isoformat()
                logger.info(
                    "Task %s scheduled for retry %d/%d at %s",
                    task_id, retry_count, max_retries, next_retry.isoformat(),
                )
                break
        return tasks

    updated = self._mutate_tasks(_updater)
    for t in updated:
        if t.get("id") == task_id:
            return Task(**t)
    return None

def get_retryable_tasks(self) -> List[Task]:
    """Return tasks whose next_retry_at has passed and status is pending."""
    from datetime import datetime as _dt
    now = _dt.now()
    tasks = self._load_tasks()
    result = []
    for t in tasks:
        if t.get("status") != "pending":
            continue
        next_retry = t.get("next_retry_at", "")
        if not next_retry:
            continue
        try:
            retry_time = _dt.fromisoformat(next_retry)
            if retry_time <= now:
                result.append(Task(**t))
        except (ValueError, TypeError):
            continue
    return result
```

## Step 3: Modify Executor Loop — `src/ai_company/executor/loop.py`

In the `_process_task` method (line 350), after the task fails (around line 434-446), add retry logic:

```python
# After failure, attempt auto-retry
if isinstance(self.bus, MessageBus):  # Only for JSON backend
    task = self.bus.get_task_by_id(task.id)
    if task and task.retry_count < task.max_retries:
        import math
        delay = 30 * (2 ** task.retry_count)  # 30s, 60s, 120s, ...
        self.bus.retry_task(task.id, delay_seconds=delay)
        logger.info("Task %s scheduled for retry in %.0fs", task.id, delay)
        return
```

Also, in `_detect_stale_tasks` (line 260), add retry logic for stale tasks:
```python
# If stale task has retries left, retry instead of DLQ
if task.get("retry_count", 0) < task.get("max_retries", 3):
    bus.retry_task(task_id, delay_seconds=60)
    # Remove from stale list (don't DLQ)
```

## Verification
1. Unit test: Create a task, fail it, verify retry_count incremented, status back to pending, next_retry_at set
2. Unit test: Create a task with max_retries=0, fail it, verify NO retry
3. Unit test: Verify exponential backoff: 30s, 60s, 120s
4. Unit test: Verify get_retryable_tasks() returns only tasks past their retry time
5. Run `ruff check src/ai_company/models/models.py src/ai_company/orchestrator/message_bus.py src/ai_company/executor/loop.py`
6. Run `mypy src/ai_company/models/models.py src/ai_company/orchestrator/message_bus.py src/ai_company/executor/loop.py`
7. Run `pytest tests/unit/test_message_bus*.py tests/integration/test_full_pipeline.py -v`
```

---

### R4: Add File Locking to Dead-Letter Queue

| Aspect | Detail |
|--------|--------|
| **Agent(s)** | `lead-backend` (primary) |
| **Effort** | 1–2 hours |
| **Dependencies** | None |
| **Summary** | Refactor DeadLetterQueue to use FileStore for all persistence |

**Task Prompt for `lead-backend`:**

```
ADD FILE LOCKING TO DEAD-LETTER QUEUE (R4)

Refactor DeadLetterQueue to use FileStore for all persistence, eliminating race conditions from raw Path.read_text()/write_text().

## File to Modify: `src/ai_company/executor/dead_letter.py`

### Changes:

1. Add FileStore import:
```python
from ai_company.store.file_store import FileStore
```

2. Modify `DeadLetterQueue.__init__`:
```python
def __init__(self, dlq_path: str = DEFAULT_DLQ_PATH) -> None:
    self.dlq_path = Path(dlq_path)
    self.dlq_path.parent.mkdir(parents=True, exist_ok=True)
    self._store = FileStore(self.dlq_path.parent, backup=True)
    self._dlq_name = self.dlq_path.name
    if not self._store.exists(self._dlq_name):
        self._save_entries([])
```

3. Replace `_load_entries` (line 35-39):
```python
def _load_entries(self) -> list[dict[str, Any]]:
    data = self._store.read_json(self._dlq_name)
    if data is None:
        return []
    if not isinstance(data, list):
        logger.warning("Corrupt DLQ data — returning empty list.")
        return []
    return data
```

4. Replace `_save_entries` (line 41-44):
```python
def _save_entries(self, entries: list[dict[str, Any]]) -> None:
    self._store.write_json(self._dlq_name, entries)
```

5. In `detect_stale_tasks` function (line 104-163):
- Replace `json.loads(inbox_path.read_text(...))` with `MessageBus` parameter
- Replace `inbox_path.write_text(...)` with `MessageBus._mutate_tasks()`
- Update signature: `def detect_stale_tasks(bus: MessageBus, dlq: DeadLetterQueue, ...)`
- Update caller in `executor/loop.py` line 273

## Verification
1. Run existing tests: `pytest tests/unit/test_dead_letter.py -v`
2. Write new test: concurrent access test (2 threads writing DLQ simultaneously)
3. Run `ruff check src/ai_company/executor/dead_letter.py`
4. Run `mypy src/ai_company/executor/dead_letter.py`
```

---

### R5: Migrate Backend from JSON to SQLite (Strategic)

| Aspect | Detail |
|--------|--------|
| **Agent(s)** | `data-engineer` (primary), `lead-backend` (review) |
| **Effort** | 4–6 hours |
| **Dependencies** | R1, R2, R3 must be stable first (R5 is strategic, not urgent) |
| **Summary** | Create SqliteTaskStore implementing same interface as MessageBus |

**Task Prompt for `data-engineer`:**

```
IMPLEMENT SQLITE TASK STORE BACKEND (R5 — STRATEGIC)

Create a new SQLite-backed task store that implements the same interface as MessageBus, enabling indexed queries, concurrent reads, and better crash recovery.

## Context
The project already has a `src/ai_company/data/task_store.py` with a `TaskStore` class that uses SQLite. This recommendation asks you to:

1. Audit the existing `TaskStore` for completeness against `MessageBus` interface
2. Add any missing methods
3. Add a transparent migration path from JSON to SQLite
4. Write comprehensive tests

## Files to Create/Modify

### 1. New: `src/ai_company/store/sqlite_store.py`
Create a clean SQLite task store with WAL mode:
```python
import sqlite3
from pathlib import Path
from typing import Any

class SqliteTaskStore:
    """SQLite-backed task store with WAL mode for concurrent reads."""
    
    def __init__(self, db_path: str = ".opencode/tasks.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.db_path))
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA busy_timeout=5000")
        self._conn.row_factory = sqlite3.Row
        self._init_schema()
    
    def _init_schema(self):
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                assignee TEXT,
                sender_id TEXT,
                receiver_id TEXT,
                instruction TEXT,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                dependencies TEXT DEFAULT '[]',
                due_date TEXT,
                tags TEXT DEFAULT '[]',
                created_at TEXT,
                updated_at TEXT,
                completed_at TEXT,
                result TEXT,
                requires_approval INTEGER DEFAULT 0,
                approved_by TEXT,
                correlation_id TEXT,
                parent_task_id TEXT,
                acknowledged_by TEXT,
                retry_count INTEGER DEFAULT 0,
                max_retries INTEGER DEFAULT 3,
                next_retry_at TEXT,
                raw_json TEXT
            )
        """)
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_status ON tasks(status)")
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_priority ON tasks(priority)")
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_receiver ON tasks(receiver_id)")
        self._conn.commit()
    
    # ... implement send_task, get_pending_tasks, claim_next_pending, etc.
```

### 2. Modify: `src/ai_company/orchestrator/message_bus.py`
Add backend abstraction:
```python
class MessageBusBackend:
    """Protocol for task persistence backends."""
    def send_task(self, task: Task) -> None: ...
    def get_pending_tasks(self) -> List[Task]: ...
    def claim_next_pending(self) -> Task | None: ...
    def get_task_by_id(self, task_id: str) -> Task | None: ...
    def update_task_status(self, task_id: str, status: str, *, result: str = "") -> Task | None: ...
    def get_all_tasks(self) -> List[Task]: ...
```

### 3. New: `tests/test_sqlite_store.py`
Comprehensive test suite:
- Test schema creation
- Test CRUD operations
- Test priority ordering
- Test concurrent reads (WAL mode)
- Test migration from JSON
- Test retry fields

### 4. Migration: `src/ai_company/data/migration.py`
```python
def migrate_json_to_sqlite(json_path: str, db_path: str) -> int:
    """Migrate tasks from inbox.json to SQLite. Returns count migrated."""
```

## Verification
1. Run existing MessageBus tests with SQLite backend: `TASK_STORE_BACKEND=sqlite pytest tests/`
2. Run new SQLite-specific tests: `pytest tests/test_sqlite_store.py -v`
3. Run `ruff check src/ai_company/store/sqlite_store.py src/ai_company/data/migration.py`
4. Run `mypy src/ai_company/store/sqlite_store.py src/ai_company/data/migration.py`
5. Verify WAL mode: `sqlite3 .opencode/tasks.db "PRAGMA journal_mode;"` should return `wal`
```

---

## 2. Execution Sequence

### Phase 1: Independent Work (Days 1–2) — Can Run in Parallel

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 1 (Parallel)                           │
│                                                                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│  │   R1    │    │   R2    │    │   R3    │    │   R4    │     │
│  │ KPI+API │    │Priority │    │ Retry   │    │  DLQ    │     │
│  │  Lead   │    │  Lead   │    │  Lead   │    │  Lead   │     │
│  │Backend  │    │Backend  │    │Backend  │    │Backend  │     │
│  └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘     │
│       │              │              │              │            │
│       └──────────────┴──────────────┴──────────────┘            │
│                          │                                      │
│                    Phase 1 Complete                             │
│                    (All 4 merged to main)                       │
└─────────────────────────────────────────────────────────────────┘
```

| Recommendation | Start | End | Critical Path? |
|---------------|-------|-----|----------------|
| R1 (KPI+API migration) | Day 1 AM | Day 1 PM | Yes — blocks GAP-011 closure |
| R2 (Priority ordering) | Day 1 AM | Day 1 PM | No |
| R3 (Retry with backoff) | Day 1 AM | Day 2 AM | No |
| R4 (DLQ file locking) | Day 1 AM | Day 1 PM | No |

### Phase 2: Integration Testing (Day 2) — After Phase 1

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 2 (Sequential)                         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐       │
│  │          QA Automation Engineer                     │       │
│  │   - GAP-011 verification tests                      │       │
│  │   - GAP-020 supplementary tests                     │       │
│  │   - R2 priority ordering tests                      │       │
│  │   - R3 retry behavior tests                         │       │
│  │   - R4 DLQ concurrency tests                        │       │
│  └─────────────────────────────────────────────────────┘       │
│                          │                                      │
│                    Phase 2 Complete                             │
└─────────────────────────────────────────────────────────────────┘
```

### Phase 3: Strategic — SQLite Backend (Days 3–5) — After Phase 2 Stable

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 3 (After Phase 2)                      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐       │
│  │              Data Engineer                          │       │
│  │   - SqliteTaskStore implementation                  │       │
│  │   - JSON→SQLite migration                           │       │
│  │   - Backend abstraction in MessageBus               │       │
│  │   - Comprehensive test suite                        │       │
│  └─────────────────────────────────────────────────────┘       │
│                          │                                      │
│  ┌─────────────────────────────────────────────────────┐       │
│  │         Lead Backend (review)                       │       │
│  │   - Code review of SQLite store                     │       │
│  │   - Integration with executor loop                  │       │
│  │   - Feature flag testing                            │       │
│  └─────────────────────────────────────────────────────┘       │
│                          │                                      │
│                    Phase 3 Complete                             │
│                    ALL RECOMMENDATIONS DONE                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Risk Assessment

### R1: KPI + API Migration

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Broadcast callback not wired in KPI collectors | Medium | Medium | KPI collectors are read-only; broadcast not needed for reads |
| Breaking mobile API endpoints | Medium | High | Test all 8 mobile endpoints after migration |
| Performance regression from MessageBus overhead | Low | Low | MessageBus.get_all_tasks() is O(n) same as file read |
| Backward compatibility with existing tests | Low | Medium | Add fallback: if no bus injected, use file read |

**Rollback:** Revert the 10 files to pre-migration state. No data changes involved.

### R2: Priority Ordering

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Sort breaks insertion-order assumptions | Low | Medium | Only affects pending tasks; completed tasks unaffected |
| Performance impact from sorting | Very Low | Low | Sorting 1000 tasks is <1ms |
| Starvation of low-priority tasks | Low | Medium | Document that critical tasks always come first |

**Rollback:** Remove the sort from `get_pending_tasks()` and `claim_next_pending()`.

### R3: Retry with Backoff

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Infinite retry loops | Low | High | Default max_retries=3, hard cap at 10 |
| Retry storms overwhelming LLM providers | Medium | High | Exponential backoff + max retries cap |
| Stale retry tasks accumulating | Low | Medium | Retryable tasks checked on each tick |
| Task model backward compatibility | Low | Medium | New fields have defaults; existing JSON still works |

**Rollback:** Remove retry fields from Task model; remove retry logic from executor.

### R4: DLQ File Locking

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| FileStore locking overhead | Very Low | Low | FileStore already used by MessageBus; proven pattern |
| Deadlock from lock contention | Very Low | High | FileStore uses timeout-based locks |
| Breaking existing DLQ tests | Low | Medium | DLQ API unchanged; only internals changed |

**Rollback:** Revert `dead_letter.py` to raw file I/O.

### R5: SQLite Backend

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| SQLite corruption | Low | High | WAL mode + backup on every write |
| Migration data loss | Medium | Critical | Run migration in transaction; verify row count |
| Performance regression for small datasets | Low | Low | SQLite is faster than JSON for queries |
| Breaking existing executor | Medium | High | Feature flag `TASK_STORE_BACKEND`; fallback to JSON |

**Rollback:** Set `TASK_STORE_BACKEND=json`; fall back to MessageBus.

---

## 4. Verification Checklist

### R1 Verification

| # | Check | Command | Expected |
|---|-------|---------|----------|
| 1 | No direct inbox.json reads in dashboard | `grep -r "inbox.json" src/ai_company/dashboard/ --include="*.py"` | Only in repository.py allowlist |
| 2 | No direct inbox.json reads in CLI | `grep -r "inbox.json" src/ai_company/cli/executor.py` | Zero matches |
| 3 | No direct inbox.json reads in DLQ | `grep -r "inbox.json" src/ai_company/executor/dead_letter.py` | Zero matches |
| 4 | Linter clean | `ruff check src/ai_company/dashboard/ src/ai_company/cli/executor.py src/ai_company/executor/dead_letter.py` | Zero errors |
| 5 | Type checker clean | `mypy src/ai_company/dashboard/ src/ai_company/cli/executor.py src/ai_company/executor/dead_letter.py` | Zero errors |
| 6 | All tests pass | `pytest tests/unit/test_message_bus_broadcast.py tests/integration/test_full_pipeline.py -v` | All pass |
| 7 | Mobile API works | `pytest tests/integration/test_dashboard_api.py -v` | All pass |

### R2 Verification

| # | Check | Command | Expected |
|---|-------|---------|----------|
| 1 | Priority ordering test | `pytest tests/ -k "priority" -v` | All pass |
| 2 | Critical tasks first | Unit test: 4 tasks → order is critical, high, medium, low | Pass |
| 3 | Claim priority | Unit test: claim_next_pending returns highest priority | Pass |
| 4 | Linter clean | `ruff check src/ai_company/orchestrator/message_bus.py` | Zero errors |

### R3 Verification

| # | Check | Command | Expected |
|---|-------|---------|----------|
| 1 | Retry fields in Task | `python -c "from ai_company.models.task import Task; t=Task(id='x'); print(t.retry_count, t.max_retries)"` | `0 3` |
| 2 | Retry on failure | Unit test: fail task → retry_count=1, status=pending | Pass |
| 3 | Max retries exceeded | Unit test: fail task 3 times → no retry | Pass |
| 4 | Backoff calculation | Unit test: verify 30s, 60s, 120s delays | Pass |
| 5 | Linter clean | `ruff check src/ai_company/orchestrator/message_bus.py src/ai_company/executor/loop.py` | Zero errors |

### R4 Verification

| # | Check | Command | Expected |
|---|-------|---------|----------|
| 1 | DLQ uses FileStore | `grep -r "Path.read_text\|Path.write_text" src/ai_company/executor/dead_letter.py` | Zero matches |
| 2 | Existing DLQ tests pass | `pytest tests/unit/test_dead_letter.py -v` | All pass |
| 3 | Concurrent write test | Unit test: 2 threads writing DLQ → no corruption | Pass |
| 4 | Linter clean | `ruff check src/ai_company/executor/dead_letter.py` | Zero errors |

### R5 Verification

| # | Check | Command | Expected |
|---|-------|---------|----------|
| 1 | SQLite schema created | `sqlite3 .opencode/tasks.db ".tables"` | `tasks` |
| 2 | WAL mode active | `sqlite3 .opencode/tasks.db "PRAGMA journal_mode;"` | `wal` |
| 3 | Migration works | Unit test: import 10 tasks → count=10 | Pass |
| 4 | All tests pass with SQLite | `TASK_STORE_BACKEND=sqlite pytest tests/ -v` | All pass |
| 5 | All tests pass with JSON | `TASK_STORE_BACKEND=json pytest tests/ -v` | All pass |

---

## 5. GAP-011 Closure Plan

### Current State (from ARCHITECTURE-GAPS.md)

> GAP-011: Dashboard API Reads Files Directly, Bypasses MessageBus
> Status: 🟡 Partial
> Evidence: write path fixed (`api.py:313` `get_bus().send_task()`); `mobile_api.py` + `kpis/*` still read `inbox.json` (read-only)

### Exact Steps to Close GAP-011

#### Step 1: Grep for All Direct Reads

```powershell
cd C:\Users\jmlus\light-speed-holdings\ai-company
rg -n "inbox\.json" src/ --include "*.py" | grep -v "__pycache__"
```

Expected matches (before fix):
- `src/ai_company/dashboard/kpis/engineering.py:17`
- `src/ai_company/dashboard/kpis/sales.py:19`
- `src/ai_company/dashboard/kpis/legal.py:19`
- `src/ai_company/dashboard/kpis/marketing.py:19`
- `src/ai_company/dashboard/kpis/customer_success.py:19`
- `src/ai_company/dashboard/mobile_api.py:193,256,404,540,778`
- `src/ai_company/cli/executor.py:128,197,302`
- `src/ai_company/executor/dead_letter.py:118`
- `src/ai_company/dashboard/repository.py:39` (allowlist — this is correct)

#### Step 2: Migrate Each Collector

For each KPI collector that reads `inbox.json`:
1. Add `message_bus` parameter to `__init__`
2. Add `_get_tasks()` helper to base class
3. Replace `self._load_json(".opencode/inbox.json")` with `self._get_tasks()`
4. Verify collector returns same data structure

#### Step 3: Migrate Mobile API

For each mobile_api.py endpoint that reads `inbox.json`:
1. Add `_get_bus()` helper
2. Replace `_load_json(".opencode/inbox.json")` with `_get_bus().get_all_tasks_raw()`
3. For write operations (delegate_task), use `bus.send_task()` or `bus.update_task()`

#### Step 4: Migrate CLI Executor

For each CLI command that reads `inbox.json`:
1. Create `MessageBus` instance
2. Replace `json.loads(inbox_path.read_text(...))` with `bus.get_all_tasks_raw()`
3. For `dlq_retry`, use `bus.send_task()` instead of file append

#### Step 5: Migrate Dead Letter Detector

1. Change `detect_stale_tasks` to accept `MessageBus` parameter
2. Use `bus.get_all_tasks_raw()` and `bus._mutate_tasks()` for removal
3. Update caller in `executor/loop.py`

#### Step 6: Verify Broadcast Callbacks

After migration, verify that broadcast callbacks still fire:
1. KPI collectors are read-only — no broadcast needed
2. Mobile API endpoints that modify state should trigger broadcasts
3. Test: `pytest tests/unit/test_message_bus_broadcast.py -v`

#### Step 7: Final Grep Verification

```powershell
rg -n "inbox\.json" src/ --include "*.py" | grep -v "__pycache__" | grep -v "repository.py"
```

Expected result: **ZERO matches** (all direct reads eliminated)

---

## 6. GAP-020 Closure Plan

### Current State

> GAP-020: No Integration Tests for End-to-End Pipeline
> Status: ✅ Resolved (10 tests in `tests/integration/test_full_pipeline.py`)

### Supplementary Tests Needed

The existing 10 tests cover:
- Happy path task lifecycle
- Failure handling
- Multiple tasks
- Memory storage
- Consolidation scheduler
- Empty inbox
- Audit trail
- Tool execution
- Max iterations
- Status transitions

**Missing scenarios for full MessageBus pipeline coverage:**

#### New Test File: `tests/integration/test_messagebus_pipeline.py`

```python
"""Full MessageBus pipeline integration tests (GAP-020 supplement).

Tests the complete message bus pipeline including:
1. Create → Process → Complete
2. Create → Fail → Retry → Complete
3. Create → HITL Park → Approve → Complete
4. Stale Task → DLQ → Retry
5. Priority ordering under load
6. Concurrent task processing
7. Broadcast events through full lifecycle
"""
```

#### Test Scenarios

| # | Scenario | Steps | Assertion |
|---|----------|-------|-----------|
| 1 | Happy path | Create task → tick → complete | Status=completed, result set |
| 2 | Failure + retry | Create task → fail (mock) → retry → complete | retry_count=1, eventually completed |
| 3 | Max retries exceeded | Create task → fail 3 times | Status=failed, no more retries |
| 4 | HITL park + approve | Create task → HITL gate → approve → complete | Status transitions correct |
| 5 | Stale task → DLQ | Create task → set old timestamp → tick | Task in DLQ, inbox empty |
| 6 | Priority ordering | Create 4 tasks (different priorities) → tick | Processed in priority order |
| 7 | Concurrent claims | 2 executors claim simultaneously | Only 1 gets the task |
| 8 | Broadcast events | Create → process → complete | All events emitted |
| 9 | DLQ retry flow | DLQ task → retry_task → re-enqueue → process | Task completed |
| 10 | Full lifecycle with SQLite | TASK_STORE_BACKEND=sqlite → all above | Same results |

#### How to Run

```powershell
cd C:\Users\jmlus\light-speed-holdings\ai-company

# Run new tests
pytest tests/integration/test_messagebus_pipeline.py -v

# Run all integration tests
pytest tests/integration/ -v

# Run with SQLite backend
$env:TASK_STORE_BACKEND="sqlite"; pytest tests/integration/ -v

# Run with JSON backend
$env:TASK_STORE_BACKEND="json"; pytest tests/integration/ -v

# Run full test suite
pytest --tb=short -q
```

---

## 7. Summary

| Rec | Description | Agent | Effort | Phase | Status |
|-----|-------------|-------|--------|-------|--------|
| R1 | KPI+API migration | lead-backend | 3–4h | 1 | ⏳ Pending |
| R2 | Priority ordering | lead-backend | 1–2h | 1 | ⏳ Pending |
| R3 | Retry with backoff | lead-backend | 2–3h | 1 | ⏳ Pending |
| R4 | DLQ file locking | lead-backend | 1–2h | 1 | ⏳ Pending |
| R5 | SQLite backend | data-engineer | 4–6h | 3 | ⏳ Pending |
| GAP-011 | Full closure | lead-backend + QA | Included in R1 | 1–2 | ⏳ Pending |
| GAP-020 | Supplementary tests | qa-automation-engineer | 2–3h | 2 | ⏳ Pending |

**Total estimated effort:** 14–20 hours across all agents
**Critical path:** R1 → GAP-011 closure
**Parallelization:** R1, R2, R3, R4 can all run simultaneously in Phase 1
