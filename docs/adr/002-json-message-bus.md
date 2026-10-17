# ADR-002: Why JSON-backed MessageBus

**Status:** Accepted
**Date:** 2026-07-17
**Deciders:** CTO, Lead Engineer
**Technical Domain:** Task Orchestration

## Context

AI Company Builder needs a task queue system that:
- Persists tasks to disk (no in-memory-only queues)
- Is human-readable and editable (operators may need to inspect/modify tasks)
- Works without external infrastructure (no Redis, RabbitMQ, or PostgreSQL)
- Supports the full task lifecycle: pending, in_progress, completed, failed, escalated, cancelled
- Integrates with the orchestrator tick cycle, executor loop, and dashboard API
- Can be backed up with simple file copy

## Decision

We use a **JSON file** (`orchestrator/inbox.json`) as the backing store for the MessageBus.

## Options Considered

### 1. JSON file (chosen)

```python
class MessageBus:
    def __init__(self, inbox_path: str = "orchestrator/inbox.json"):
        self._path = inbox_path

    def send_task(self, task: Task) -> None:
        tasks = self._load()
        tasks.append(task.model_dump())
        self._save(tasks)
```

**Pros:**
- Zero infrastructure — works on any machine with Python
- Human-readable and hand-editable for debugging
- Simple backup (copy the file)
- Git-friendly — diffs show exactly what changed
- Pydantic models serialize/deserialize cleanly to JSON
- Fast enough for the expected throughput (<100 tasks/day)

**Cons:**
- No concurrent write safety without file locking
- Not suitable for distributed systems
- Full file read/write on every operation

### 2. SQLite

**Pros:**
- ACID transactions, concurrent access
- SQL queries for complex filtering
- Still zero infrastructure (file-based)

**Cons:**
- Not human-readable without tools
- Harder to debug (can't just `cat` the file)
- Requires schema migrations for model changes
- Adds a dependency on `sqlite3` (stdlib, but ORM complexity)

### 3. Redis

**Pros:**
- Excellent performance and concurrency
- Built-in pub/sub for real-time notifications
- Atomic operations

**Cons:**
- Requires running a Redis server
- Adds operational complexity
- Data not human-readable
- Overkill for expected throughput

### 4. PostgreSQL

**Pros:**
- Full ACID, concurrent access, rich querying
- JSON column type for flexible schemas
- Production-grade

**Cons:**
- Requires running a database server
- Connection management complexity
- Overkill for a single-machine CLI tool

## Consequences

### Positive

- **Simplicity**: No external dependencies or services to manage
- **Debuggability**: `cat orchestrator/inbox.json | python -m json.tool` for instant inspection
- **Portability**: The entire system state is a handful of JSON/YAML files
- **Testing**: Tests can use temporary JSON files without mocking databases
- **Backup**: `cp -r orchestrator/ /backup/` covers all operational state

### Negative

- **Concurrency**: Concurrent writes could corrupt the file (mitigated: single-process execution model)
- **Performance**: Full file read/write on each operation (mitigated: file is small, <1MB expected)
- **No querying**: Filtering is done in Python (mitigated: task count is small)

### Mitigations

- The orchestrator and executor run as single processes (no concurrent writes)
- File locking via `fcntl` (Unix) or `msvcrt` (Windows) if concurrency is ever needed
- Task list size is bounded by the cleanup/archival policy
- Future migration to SQLite is straightforward if throughput exceeds JSON capabilities

## Evidence

- Current `orchestrator/inbox.json` stores all tasks as a JSON array
- The orchestrator tick, executor tick, and dashboard API all read/write through MessageBus
- 466 tests pass using temporary JSON file fixtures
- File size after 1000 tasks is <500KB (well within acceptable range)

## References

- `src/ai_company/orchestrator/message_bus.py` — MessageBus implementation
- `orchestrator/inbox.json` — Runtime task queue file
- `docs/ARCHITECTURE.md` — Data flow diagram
