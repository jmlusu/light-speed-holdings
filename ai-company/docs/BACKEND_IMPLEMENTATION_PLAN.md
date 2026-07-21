# Backend Implementation Plan — 7 Tasks / 24 Hours

> Generated: 2026-07-21
> Codebase state: ~85% complete, 962 passing tests
> Runtime: Python 3.12+, Typer CLI, Pydantic v2, FastAPI dashboard

---

## Dependency Graph

```
Task 2 (briefing.py mypy) ──┐
Task 1 (peripheral I/O)  ───┤── can run in parallel
Task 7 (token counting)  ───┘
                              │
Task 5 (structured logging) ──┼── standalone, but other tasks should adopt it
                              │
Task 3 (memory consolidation) ─┼── depends on Task 2 pattern (typed access)
Task 4 (cycle daemon)     ─────┘── depends on Task 1 (clean I/O layer)
                              │
Task 6 (CLI type hints)   ──────  last — purely cosmetic, runs over all modules
```

**Recommended execution order:**
1. **Phase 1 (parallel, 5h):** Tasks 2, 7, 5 (small, independent)
2. **Phase 2 (parallel, 8h):** Tasks 1, 3 (medium, build on Phase 1)
3. **Phase 3 (4h):** Task 4 (daemon, depends on clean I/O)
4. **Phase 4 (4h):** Task 6 (CLI polish, runs last over everything)
5. **Buffer (3h):** Integration testing, edge cases

---

## Task 1: Fix Peripheral File I/O (4h)

### Problem

Multiple dashboard modules bypass the `MessageBus` abstraction and read `inbox.json` as raw JSON dicts. This creates:
- No type safety (raw dicts vs typed `Task` objects)
- No file locking (reads race with executor writes)
- No correlation ID propagation
- KPI collector base class uses raw `open()` instead of `StateStore`

### Scope Audit — What Actually Needs Fixing

| File | Lines | Current I/O | Required Fix |
|------|-------|-------------|--------------|
| `dashboard/kpis/base.py` | 42-73 | Raw `open()` / `json.load()` / `yaml.safe_load()` | Route through `StateStore` |
| `dashboard/kpis/engineering.py` | 17 | `self._load_json(".opencode/inbox.json")` | Use `MessageBus.get_all_tasks()` for typed access |
| `dashboard/kpis/customer_success.py` | 19 | `self._load_json(".opencode/inbox.json")` | Same |
| `dashboard/kpis/sales.py` | 19 | `self._load_json(".opencode/inbox.json")` | Same |
| `dashboard/kpis/marketing.py` | 19 | `self._load_json(".opencode/inbox.json")` | Same |
| `dashboard/kpis/legal.py` | 19 | `self._load_json(".opencode/inbox.json")` | Same |
| `dashboard/mobile_api.py` | 193,256,404,408,540,778 | `_load_json(".opencode/inbox.json")` (already through StateStore) | Use `MessageBus` for typed `Task` access |
| `dashboard/monitoring.py` | 370 | `_get_store().read_json(...)` (already through StateStore) | Use `MessageBus.count_by_status()` |

### Step-by-Step

#### Step 1.1: Add `_get_message_bus()` helper to `KPICollector` base (1h)

**File:** `src/ai_company/dashboard/kpis/base.py`

```python
# Add imports
from ai_company.orchestrator.message_bus import MessageBus

class KPICollector(ABC):
    department: str = ""

    def __init__(self, project_root: Path | None = None) -> None:
        self.root: Path = project_root or Path(__file__).resolve().parents[3]
        self._bus: MessageBus | None = None

    @property
    def bus(self) -> MessageBus:
        """Lazy-initialized MessageBus for typed task access."""
        if self._bus is None:
            self._bus = MessageBus()
        return self._bus
```

- Keep existing `_load_json()` and `_load_yaml()` methods for non-inbox files (they're used for approvals, escalations, etc. which are NOT managed by MessageBus).
- Add a new method:

```python
    def _get_all_tasks_raw(self) -> list[dict[str, Any]]:
        """Return all inbox tasks as raw dicts (for KPI aggregation).

        Uses MessageBus for atomic reads instead of direct file I/O.
        """
        from ai_company.models.task import Task as TaskModel
        tasks = self.bus.get_all_tasks()
        return [t.model_dump() for t in tasks]
```

#### Step 1.2: Update each KPI collector to use `_get_all_tasks_raw()` (1.5h)

**Files:** `engineering.py`, `customer_success.py`, `sales.py`, `marketing.py`, `legal.py`

Pattern change for each:
```python
# BEFORE:
tasks = self._load_json(".opencode/inbox.json")

# AFTER:
tasks = self._get_all_tasks_raw()
```

This is a mechanical find-and-replace in 5 files. Each file has exactly one line to change.

#### Step 1.3: Update `mobile_api.py` to use `MessageBus` (1h)

**File:** `src/ai_company/dashboard/mobile_api.py`

Add a module-level lazy bus helper:
```python
from ai_company.orchestrator.message_bus import MessageBus

_bus: MessageBus | None = None

def _get_bus() -> MessageBus:
    global _bus
    if _bus is None:
        _bus = MessageBus()
    return _bus
```

Replace 6 calls to `_load_json(".opencode/inbox.json")` at lines 193, 256, 404, 408, 540, 778:

| Line | Current | Replacement |
|------|---------|-------------|
| 193 | `tasks = _load_json(".opencode/inbox.json")` | `tasks = [t.model_dump() for t in _get_bus().get_all_tasks()]` |
| 256 | `tasks = _load_json(".opencode/inbox.json")` | `tasks = [t.model_dump() for t in _get_bus().get_all_tasks()]` |
| 404 | `tasks = _load_json(".opencode/inbox.json")` | `tasks = [t.model_dump() for t in _get_bus().get_all_tasks()]` |
| 408 | `_save_json(".opencode/inbox.json", tasks)` | Use `_get_bus().update_task_status()` for individual task mutations |
| 540 | `tasks = _load_json(".opencode/inbox.json")` | `tasks = [t.model_dump() for t in _get_bus().get_all_tasks()]` |
| 778 | `tasks = _load_json(".opencode/inbox.json")` | `tasks = [t.model_dump() for t in _get_bus().get_all_tasks()]` |

**Special case — `_delegate_task()` (lines 401-410):** This function reads the entire inbox, modifies a task's `receiver_id`, and writes the entire inbox back. Replace with:
```python
def _delegate_task(task_id: str, delegate_to: str) -> dict[str, Any]:
    bus = _get_bus()
    task = bus.get_task_by_id(task_id)
    if task is None:
        # Try prefix match
        all_tasks = bus.get_all_tasks()
        task = next((t for t in all_tasks if t.id[:8] == task_id), None)
    if task is None:
        return {"type": "delegate", "target_id": task_id, "ok": False, "error": "Task not found"}
    # MessageBus doesn't have a "reassign" method — use update_task_status
    # We need to add a reassign method OR store metadata
    # Safest: add `result` with delegation metadata
    bus.update_task_status(task.id, task.status.value, result=f"delegated_to:{delegate_to}")
    return {"type": "delegate", "target_id": task_id, "ok": True, "delegated_to": delegate_to}
```

**Decision point:** `MessageBus` lacks a `reassign_task()` method. Add one to `message_bus.py`:
```python
def reassign_task(self, task_id: str, new_receiver_id: str) -> Task | None:
    """Change the receiver of a task (delegation/reassignment)."""
    def _updater(tasks: List[dict]) -> List[dict]:
        for i, t in enumerate(tasks):
            if t.get("id") == task_id:
                tasks[i]["receiver_id"] = new_receiver_id
                tasks[i]["updated_at"] = datetime.now().isoformat()
        return tasks
    updated = self._mutate_tasks(_updater)
    for t in updated:
        if t.get("id") == task_id:
            return Task(**t)
    return None
```

#### Step 1.4: Update `monitoring.py` (0.5h)

**File:** `src/ai_company/dashboard/monitoring.py`

Line 370 already uses `_get_store().read_json(...)` — this is fine for raw access. But replace with `MessageBus.count_by_status()` for consistency:

```python
def _append_task_status_breakdown(lines: list[str]) -> None:
    try:
        bus = MessageBus()
        status_counts = bus.count_by_status()
        # ... emit Prometheus metrics from status_counts dict
```

Remove the raw JSON iteration loop and replace with the pre-computed dict from `count_by_status()`.

### Files Modified
- `src/ai_company/dashboard/kpis/base.py`
- `src/ai_company/dashboard/kpis/engineering.py`
- `src/ai_company/dashboard/kpis/customer_success.py`
- `src/ai_company/dashboard/kpis/sales.py`
- `src/ai_company/dashboard/kpis/marketing.py`
- `src/ai_company/dashboard/kpis/legal.py`
- `src/ai_company/dashboard/mobile_api.py`
- `src/ai_company/dashboard/monitoring.py`
- `src/ai_company/orchestrator/message_bus.py` (add `reassign_task`)

### Risk Areas
- `MessageBus()` constructor creates the `.opencode/inbox.json` file if missing — ensure tests mock or use tmp dirs
- `_delegate_task` semantic changes: old code mutated receiver_id in-place and wrote back; new code uses `reassign_task` with proper locking
- KPI collectors currently accept raw dicts everywhere — switching to `model_dump()` is backward-compatible since the dict shape is identical

---

## Task 2: Fix mypy Errors in `briefing.py` (1h)

### Problem

`briefing.py` lines 40-43 treat `Task` Pydantic objects as raw dicts:

```python
for task_dict in self.bus.get_inbox("all"):   # Returns List[Task], not dicts
    if task_dict.get("status") == "pending":   # Task has .status, not .get()
        receiver = task_dict["receiver_id"]     # Task has .receiver_id attribute
        pending_tasks.setdefault(receiver, []).append(task_dict)
```

Additionally, `get_inbox("all")` filters for `receiver_id == "all"` — which returns nothing. There is no "all" agent.

### Step-by-Step

**File:** `src/ai_company/orchestrator/briefing.py`

#### Step 2.1: Replace `get_inbox("all")` with `get_all_tasks()` (0.5h)

```python
# BEFORE (line 40):
for task_dict in self.bus.get_inbox("all"):

# AFTER:
for task in self.bus.get_all_tasks():
```

#### Step 2.2: Fix attribute access patterns (0.5h)

```python
# BEFORE (lines 41-43):
    if task_dict.get("status") == "pending":
        receiver = task_dict["receiver_id"]
        pending_tasks.setdefault(receiver, []).append(task_dict)

# AFTER:
    if task.status.value == "pending":
        pending_tasks.setdefault(task.receiver_id, []).append(task)
```

Also fix downstream usages that treat tasks as dicts:

| Line | Before | After |
|------|--------|-------|
| 65 | `task["id"]` | `task.id` |
| 66 | `task["sender_id"]` | `task.sender_id` |
| 67 | `task["id"]` | `task.id` |
| 68 | `task["sender_id"]` | `task.sender_id` |
| 69 | `task["instruction"]` | `task.instruction` |

The complete fixed `generate()` method:
```python
def generate(self) -> tuple[int, int]:
    """Generate briefing. Returns (active_agents, pending_task_count)."""
    agents = self._load_registry()
    pending_tasks: dict[str, list[Task]] = {}

    for task in self.bus.get_all_tasks():
        if task.status.value == "pending":
            pending_tasks.setdefault(task.receiver_id, []).append(task)

    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "# Daily Executive Briefing",
        f"**Date:** {today}\n",
    ]

    active_agents = 0
    for agent_id, tasks in pending_tasks.items():
        if agent_id not in agents:
            continue
        agent = agents[agent_id]
        active_agents += 1
        dept = agent.get("department", "N/A")
        reports_to = agent.get("reportsTo", "N/A")
        lines.append(f"## Action Required: {agent['role']} (`{agent_id}`)")
        lines.append(f"**Department:** {dept} | **Reports To:** {reports_to}\n")
        lines.append("**OpenCode Execution Prompt:**\n```text")
        lines.append(
            f"You are the {agent['role']}. You have {len(tasks)} pending task(s) in your inbox.\n"
        )
        for task in tasks:
            sender_name = agents.get(task.sender_id, {}).get("role", task.sender_id)
            lines.append(f"TASK ID: {task.id}")
            lines.append(f"FROM: {sender_name}")
            lines.append(f"INSTRUCTION: {task.instruction}\n")
        lines.append("Please execute these tasks using your available tools.")
        lines.append("```\n---\n")
    # ... rest unchanged
```

### Files Modified
- `src/ai_company/orchestrator/briefing.py`

### Risk Areas
- Minimal — this is a straightforward type correction
- Add `from ai_company.models.task import Task` import (already available via message_bus)

---

## Task 3: Memory Consolidation + Semantic Search + TTL (7h)

### Problem

The memory subsystem has building blocks but lacks:
- A periodic consolidation daemon that runs `consolidate_all()` automatically
- CLI commands for TTL/pruning
- Wired-up semantic search in the CLI `search` command
- Expiration metadata on memory entries

### Step-by-Step

#### Step 3.1: Add TTL/expiration support to `MemoryEntry` (1h)

**File:** `src/ai_company/memory/engine.py`

Add to `MemoryEntry.__init__()`:
```python
def __init__(
    self,
    memory_type: str,
    content: str,
    metadata: dict[str, Any] | None = None,
    agent_id: str = "",
    tags: list[str] | None = None,
    ttl_days: int | None = None,  # NEW
) -> None:
    # ... existing init ...
    self.ttl_days = ttl_days
    self.expires_at: str | None = None
    if ttl_days is not None:
        from datetime import timedelta
        self.expires_at = (datetime.now() + timedelta(days=ttl_days)).isoformat()
```

Update `to_dict()` to include `ttl_days` and `expires_at`.

Add a property:
```python
@property
def is_expired(self) -> bool:
    """Return True if this entry has passed its TTL."""
    if self.expires_at is None:
        return False
    try:
        return datetime.now() > datetime.fromisoformat(self.expires_at)
    except (ValueError, TypeError):
        return False
```

#### Step 3.2: Integrate TTL into `MemoryStore.prune()` (0.5h)

**File:** `src/ai_company/memory/engine.py`

Update `prune()` to also filter expired entries:
```python
def prune(
    self,
    max_age_days: int | None = None,
    max_entries_per_type: int | None = None,
    include_expired: bool = True,  # NEW
) -> int:
    # ... existing age-based and cap logic ...

    # NEW: Remove expired entries (those with TTL set that have passed)
    if include_expired:
        for mem_type, entries in self._stores.items():
            before = len(entries)
            survivors = [e for e in entries if not e.is_expired]
            expired_count = before - len(survivors)
            if expired_count > 0:
                pruned += expired_count
                self._stores[mem_type] = survivors
                self._save(mem_type)

    return pruned
```

#### Step 3.3: Create periodic consolidation scheduler (2h)

**New file:** `src/ai_company/memory/consolidation.py`

```python
"""Periodic memory consolidation daemon.

Runs consolidation, deduplication, and TTL pruning on a configurable
interval. Can be run as a standalone daemon or invoked by the scheduler.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Any, Callable

from ai_company.memory.engine import MemoryStore

logger = logging.getLogger(__name__)


class ConsolidationConfig:
    """Configuration for the consolidation daemon."""

    def __init__(
        self,
        interval_minutes: int = 60,
        max_age_days: int | None = 90,
        max_entries_per_type: int | None = 500,
        enable_dedup: bool = True,
        enable_aggregate: bool = True,
    ) -> None:
        self.interval_minutes = interval_minutes
        self.max_age_days = max_age_days
        self.max_entries_per_type = max_entries_per_type
        self.enable_dedup = enable_dedup
        self.enable_aggregate = enable_aggregate


class MemoryConsolidator:
    """Periodic memory consolidation process.

    Performs:
    1. TTL-based expiration (prune expired entries)
    2. Age-based pruning (remove entries older than max_age_days)
    3. Per-type cap enforcement (keep most-accessed/recent)
    4. Deduplication of near-identical semantic memories
    5. Aggregate rollup generation

    Args:
        store: The MemoryStore instance to consolidate.
        config: Consolidation configuration.
    """

    def __init__(
        self,
        store: MemoryStore,
        config: ConsolidationConfig | None = None,
    ) -> None:
        self.store = store
        self.config = config or ConsolidationConfig()
        self._last_run: str | None = None
        self._run_count: int = 0

    def run_once(self) -> dict[str, Any]:
        """Run a single consolidation pass.

        Returns:
            Summary dict with keys: pruned, deduplicated, aggregates_created, timestamp.
        """
        logger.info("Starting memory consolidation pass #%d", self._run_count + 1)

        # 1. Prune by TTL and age
        pruned = self.store.prune(
            max_age_days=self.config.max_age_days,
            max_entries_per_type=self.config.max_entries_per_type,
        )

        # 2. Deduplicate + aggregate
        dedup_result = {}
        if self.config.enable_dedup or self.config.enable_aggregate:
            dedup_result = self.store.consolidate_all()

        self._run_count += 1
        self._last_run = datetime.now().isoformat()

        summary = {
            "pruned": pruned,
            "semantic_duplicates_removed": dedup_result.get("semantic_duplicates_removed", 0),
            "aggregates_created": dedup_result.get("aggregates_created", 0),
            "types_processed": dedup_result.get("types_processed", 0),
            "timestamp": self._last_run,
            "total_memories": self.store.count(),
        }

        logger.info(
            "Consolidation complete: pruned=%d, deduped=%d, aggregates=%d, total=%d",
            summary["pruned"],
            summary["semantic_duplicates_removed"],
            summary["aggregates_created"],
            summary["total_memories"],
        )

        return summary

    def run_forever(
        self,
        max_cycles: int | None = None,
        *,
        sleep: Callable[[float], None] = time.sleep,
    ) -> int:
        """Run consolidation on a periodic interval.

        Args:
            max_cycles: Stop after N cycles. None = run until interrupted.
            sleep: Injectable sleep callable for testing.

        Returns:
            Number of cycles executed.
        """
        cycles = 0
        interval_seconds = self.config.interval_minutes * 60

        try:
            while True:
                if max_cycles is not None and cycles >= max_cycles:
                    break
                self.run_once()
                cycles += 1
                if max_cycles is not None and cycles >= max_cycles:
                    break
                sleep(interval_seconds)
        except KeyboardInterrupt:
            logger.info("Consolidation daemon interrupted after %d cycles", cycles)

        return cycles
```

#### Step 3.4: Add CLI commands for memory consolidation and TTL (1.5h)

**File:** `src/ai_company/cli/memory.py`

Add new commands:
```python
@app.command()
def prune(
    max_age_days: int = typer.Option(90, help="Remove entries older than N days"),
    max_per_type: int = typer.Option(500, help="Max entries per memory type"),
    dry_run: bool = typer.Option(False, help="Show what would be pruned without deleting"),
) -> None:
    """Prune old and expired memories."""
    from ai_company.memory.engine import MemoryStore

    store = MemoryStore()
    before = store.stats()
    if dry_run:
        console.print("[yellow]Dry run — no changes[/yellow]")
        console.print(f"Current counts: {before}")
        return

    pruned = store.prune(max_age_days=max_age_days, max_entries_per_type=max_per_type)
    after = store.stats()
    console.print(f"[green]Pruned {pruned} memories[/green]")
    console.print(f"Before: {before}")
    console.print(f"After:  {after}")


@app.command()
def consolidate_all() -> None:
    """Run full consolidation: dedup + aggregates + pruning."""
    from ai_company.memory.engine import MemoryStore

    store = MemoryStore()
    summary = store.consolidate_all()
    pruned = store.prune(max_age_days=90, max_entries_per_type=500)
    console.print("[green]Consolidation complete[/green]")
    for k, v in summary.items():
        console.print(f"  {k}: {v}")
    console.print(f"  pruned: {pruned}")


@app.command()
def daemon(
    interval: int = typer.Option(60, help="Consolidation interval in minutes"),
    max_cycles: int = typer.Option(None, help="Stop after N cycles"),
) -> None:
    """Run the memory consolidation daemon."""
    from ai_company.memory.consolidation import ConsolidationConfig, MemoryConsolidator
    from ai_company.memory.engine import MemoryStore

    store = MemoryStore()
    config = ConsolidationConfig(interval_minutes=interval)
    consolidator = MemoryConsolidator(store, config)

    typer.echo(f"Starting memory consolidation daemon (interval={interval}m)")
    typer.echo("Press Ctrl+C to stop.")
    cycles = consolidator.run_forever(max_cycles=max_cycles)
    typer.echo(f"Stopped after {cycles} cycle(s).")


@app.command()
def search_semantic(
    query: str = typer.Option(..., help="Semantic search query"),
    memory_type: str = typer.Option("all", help="Memory type to search"),
    top_k: int = typer.Option(10, help="Max results"),
) -> None:
    """Semantic search using vector embeddings."""
    from ai_company.memory.integration import init_memory, semantic_search

    init_memory()
    results = semantic_search(query, top_k=top_k)

    if not results:
        console.print("No semantic matches found (vector store may not be initialized).")
        return

    table = Table(title=f"Semantic Search: '{query}'")
    table.add_column("Type", style="cyan")
    table.add_column("Similarity", justify="right", style="green")
    table.add_column("Content")
    table.add_column("Agent")

    for r in results:
        content_preview = r["content"][:60] + "..." if len(r["content"]) > 60 else r["content"]
        table.add_row(
            r["type"],
            f"{r.get('similarity', 0):.3f}",
            content_preview,
            r.get("agent_id", ""),
        )
    console.print(table)
```

#### Step 3.5: Add TTL parameter to `store` CLI command (1h)

**File:** `src/ai_company/cli/memory.py`

Update the `add` command to accept `--ttl-days`:
```python
@app.command()
def add(
    memory_type: str = typer.Option(..., help="Memory type"),
    content: str = typer.Option(..., help="Memory content"),
    agent_id: str = typer.Option("", help="Agent ID"),
    tags: str = typer.Option("", help="Comma-separated tags"),
    ttl_days: int = typer.Option(None, help="Time-to-live in days (optional)"),
) -> None:
    """Add a new memory entry with optional TTL."""
    store = MemoryStore()
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    entry = store.store(
        memory_type, content,
        agent_id=agent_id, tags=tag_list, ttl_days=ttl_days,
    )
    console.print(f"[green]Stored {memory_type} memory:[/green] {entry.id}")
    if entry.expires_at:
        console.print(f"  Expires: {entry.expires_at}")
```

#### Step 3.6: Add tests (1h)

**New file:** `tests/test_memory_consolidation.py`

Test cases:
- `test_consolidation_removes_expired_entries` — entries with TTL in the past are pruned
- `test_consolidation_preserves_fresh_entries` — entries within TTL survive
- `test_consolidation_deduplicates_semantic` — near-identical entries reduced to one
- `test_consolidation_run_once_returns_summary` — verify summary dict keys
- `test_consolidation_run_forever_max_cycles` — verify cycle count

**Modified file:** `tests/test_memory_engine.py` (add TTL tests):
- `test_memory_entry_ttl` — entry with `ttl_days=1` has `expires_at` set
- `test_memory_entry_is_expired` — mock `datetime.now` to test expiration
- `test_prune_removes_expired` — prune with expired entries

### Files Modified/Created
- `src/ai_company/memory/engine.py` (TTL on MemoryEntry, prune expired)
- `src/ai_company/memory/consolidation.py` (NEW)
- `src/ai_company/cli/memory.py` (add `prune`, `consolidate-all`, `daemon`, `search-semantic` commands)
- `tests/test_memory_consolidation.py` (NEW)
- `tests/test_memory_engine.py` (add TTL tests)

### Risk Areas
- TTL expiration uses `datetime.now()` — entries created in the same second could expire immediately if `ttl_days=0`; add guard: `if ttl_days is not None and ttl_days > 0`
- `consolidate_all()` can be slow for large stores — add timing logs
- The `daemon` command blocks forever — ensure it handles SIGTERM gracefully (already handles `KeyboardInterrupt`)
- Semantic search requires `sentence-transformers` — the `search-semantic` CLI command should warn when unavailable

---

## Task 4: Scheduled Cycle Daemon (4h)

### Problem

The executor has `Executor.start()` for continuous polling and `Scheduler.run_forever()` for scheduled task creation, but there is no proper daemon mode with:
- PID file management for single-instance enforcement
- Graceful shutdown (SIGTERM/SIGINT handling)
- Structured logging to file
- Health check endpoint or heartbeat file
- Proper integration of scheduler + executor in one process

### Step-by-Step

#### Step 4.1: Create the daemon module (2h)

**New file:** `src/ai_company/executor/daemon.py`

```python
"""Scheduled-cycle daemon — runs executor + scheduler as a background process.

Provides:
- PID file management (prevents duplicate instances)
- Graceful shutdown on SIGTERM/SIGINT
- Structured JSON logging to file
- Heartbeat file for health monitoring
- Configurable cycle interval and max cycles

Usage:
    from ai_company.executor.daemon import CycleDaemon
    daemon = CycleDaemon()
    daemon.start()  # blocks until stopped
"""

from __future__ import annotations

import atexit
import json
import logging
import os
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger(__name__)

_DEFAULT_PID_FILE = ".opencode/daemon.pid"
_DEFAULT_HEARTBEAT_FILE = ".opencode/daemon.heartbeat"
_DEFAULT_LOG_FILE = "logs/daemon.jsonl"


class CycleDaemon:
    """Manages the lifecycle of a scheduled-cycle daemon process.

    Integrates Scheduler (for creating due tasks) and optionally Executor
    (for processing them) into a single long-running process.

    Args:
        interval_seconds: Seconds between cycles.
        max_cycles: Stop after N cycles (None = unlimited).
        pid_file: Path to the PID file for single-instance enforcement.
        heartbeat_file: Path to the heartbeat file (updated each cycle).
        log_file: Path for structured JSON log output.
        run_executor: If True, also run executor.tick() each cycle.
    """

    def __init__(
        self,
        interval_seconds: float = 60.0,
        max_cycles: int | None = None,
        pid_file: str = _DEFAULT_PID_FILE,
        heartbeat_file: str = _DEFAULT_HEARTBEAT_FILE,
        log_file: str | None = _DEFAULT_LOG_FILE,
        run_executor: bool = True,
    ) -> None:
        self.interval_seconds = interval_seconds
        self.max_cycles = max_cycles
        self.pid_file = Path(pid_file)
        self.heartbeat_file = Path(heartbeat_file)
        self.log_file = Path(log_file) if log_file else None
        self.run_executor = run_executor
        self._running = False
        self._cycles_completed = 0

    def start(self) -> int:
        """Start the daemon. Blocks until stopped.

        Returns:
            Number of cycles completed.
        """
        # Write PID file
        self.pid_file.parent.mkdir(parents=True, exist_ok=True)
        self.pid_file.write_text(str(os.getpid()), encoding="utf-8")
        atexit.register(self._cleanup_pid)

        # Register signal handlers
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

        self._running = True
        logger.info(
            "Daemon started (pid=%d, interval=%.1fs, max_cycles=%s)",
            os.getpid(),
            self.interval_seconds,
            self.max_cycles or "unlimited",
        )

        # Lazy-import heavy components
        from ai_company.orchestrator.message_bus import MessageBus
        from ai_company.orchestrator.scheduler import Scheduler

        bus = MessageBus()
        scheduler = Scheduler()

        executor = None
        if self.run_executor:
            from ai_company.executor.loop import Executor
            executor = Executor(poll_interval=self.interval_seconds)

        while self._running:
            if self.max_cycles is not None and self._cycles_completed >= self.max_cycles:
                break

            cycle_start = time.monotonic()

            try:
                # 1. Create due scheduled tasks
                created = scheduler.create_pending_tasks(bus)
                if created:
                    logger.info("Scheduler created %d task(s)", len(created))

                # 2. Process pending tasks (if executor enabled)
                if executor is not None:
                    processed = executor.tick()
                    if processed > 0:
                        logger.info("Executor processed %d task(s)", processed)

                # 3. Update heartbeat
                self._write_heartbeat()

                self._cycles_completed += 1
            except Exception:
                logger.exception("Error in daemon cycle #%d", self._cycles_completed + 1)

            if self.max_cycles is not None and self._cycles_completed >= self.max_cycles:
                break

            # Sleep for remainder of interval
            elapsed = time.monotonic() - cycle_start
            sleep_time = max(0, self.interval_seconds - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)

        self._cleanup_pid()
        logger.info("Daemon stopped after %d cycle(s)", self._cycles_completed)
        return self._cycles_completed

    def stop(self) -> None:
        """Signal the daemon to stop after the current cycle."""
        self._running = False

    def _handle_signal(self, signum: int, frame: Any) -> None:
        """Handle SIGTERM/SIGINT for graceful shutdown."""
        logger.info("Received signal %d, stopping daemon...", signum)
        self._running = False

    def _write_heartbeat(self) -> None:
        """Write a heartbeat file for health monitoring."""
        self.heartbeat_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "pid": os.getpid(),
            "cycles": self._cycles_completed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": 0,  # computed from start time
        }
        self.heartbeat_file.write_text(json.dumps(data), encoding="utf-8")

    def _cleanup_pid(self) -> None:
        """Remove the PID file."""
        try:
            if self.pid_file.exists():
                self.pid_file.unlink()
        except OSError:
            pass

    @staticmethod
    def is_already_running(pid_file: str = _DEFAULT_PID_FILE) -> bool:
        """Check if another daemon instance is already running."""
        path = Path(pid_file)
        if not path.exists():
            return False
        try:
            pid = int(path.read_text(encoding="utf-8").strip())
            # Check if process is alive
            os.kill(pid, 0)
            return True
        except (ValueError, OSError):
            # PID file stale or process dead
            path.unlink(missing_ok=True)
            return False
```

#### Step 4.2: Add daemon CLI command (1h)

**File:** `src/ai_company/cli/executor.py`

Add a `daemon` command:
```python
@app.command()
def daemon(
    interval: float = typer.Option(60.0, help="Seconds between cycles"),
    max_cycles: int = typer.Option(None, help="Stop after N cycles"),
    no_executor: bool = typer.Option(False, help="Only run scheduler, skip task execution"),
    pid_file: str = typer.Option(".opencode/daemon.pid", help="PID file path"),
) -> None:
    """Run the scheduled-cycle daemon with PID management and graceful shutdown."""
    from ai_company.executor.daemon import CycleDaemon

    if CycleDaemon.is_already_running(pid_file):
        typer.echo("Daemon is already running. Use 'executor daemon-stop' to stop it.")
        raise typer.Exit(1)

    daemon = CycleDaemon(
        interval_seconds=interval,
        max_cycles=max_cycles,
        pid_file=pid_file,
        run_executor=not no_executor,
    )
    typer.echo(f"Starting daemon (interval={interval}s, executor={'on' if not no_executor else 'off'})")
    typer.echo("Press Ctrl+C or send SIGTERM to stop.")
    cycles = daemon.start()
    typer.echo(f"Daemon completed {cycles} cycle(s).")


@app.command()
def daemon_stop(
    pid_file: str = typer.Option(".opencode/daemon.pid", help="PID file path"),
) -> None:
    """Stop a running daemon by sending SIGTERM."""
    import signal as sig

    path = Path(pid_file)
    if not path.exists():
        typer.echo("No daemon PID file found.")
        raise typer.Exit(1)

    try:
        pid = int(path.read_text(encoding="utf-8").strip())
        os.kill(pid, sig.SIGTERM)
        typer.echo(f"Sent SIGTERM to daemon process {pid}.")
    except (ValueError, OSError) as exc:
        typer.echo(f"Failed to stop daemon: {exc}")
        raise typer.Exit(1)


@app.command()
def daemon_status(
    pid_file: str = typer.Option(".opencode/daemon.pid", help="PID file path"),
    heartbeat_file: str = typer.Option(".opencode/daemon.heartbeat", help="Heartbeat file"),
) -> None:
    """Show daemon status from PID and heartbeat files."""
    from ai_company.executor.daemon import CycleDaemon

    if not CycleDaemon.is_already_running(pid_file):
        typer.echo("Daemon is NOT running.")
        return

    path = Path(pid_file)
    pid = path.read_text(encoding="utf-8").strip()
    typer.echo(f"Daemon is running (PID: {pid})")

    hb_path = Path(heartbeat_file)
    if hb_path.exists():
        try:
            hb = json.loads(hb_path.read_text(encoding="utf-8"))
            typer.echo(f"  Cycles: {hb.get('cycles', '?')}")
            typer.echo(f"  Last heartbeat: {hb.get('timestamp', '?')}")
        except (json.JSONDecodeError, OSError):
            typer.echo("  Heartbeat file unreadable")
```

#### Step 4.3: Add signal handling to Scheduler.run_forever (0.5h)

**File:** `src/ai_company/orchestrator/scheduler.py`

The existing `run_forever()` already handles `KeyboardInterrupt`. No changes needed.

#### Step 4.4: Add tests (0.5h)

**New file:** `tests/test_daemon.py`

Test cases:
- `test_daemon_is_already_running` — PID file with live process returns True
- `test_daemon_stale_pid_file` — stale PID file is cleaned up
- `test_daemon_start_stop` — start daemon with `max_cycles=2`, verify cycles completed
- `test_daemon_heartbeat_written` — verify heartbeat file created and updated

### Files Modified/Created
- `src/ai_company/executor/daemon.py` (NEW)
- `src/ai_company/cli/executor.py` (add `daemon`, `daemon-stop`, `daemon-status`)
- `tests/test_daemon.py` (NEW)

### Risk Areas
- PID files can become stale if process crashes — `is_already_running()` handles this by checking process liveness
- Signal handling in Windows is limited (no SIGTERM) — `signal.SIGTERM` raises `NotImplementedError` on Windows; wrap in try/except and fall back to `signal.SIGINT`
- Daemon + Executor in same process shares state — ensure no double-logging or conflicting file locks
- `atexit` handler for PID cleanup runs on normal exit but NOT on `kill -9` — the stale PID detection covers this

---

## Task 5: Structured Logging with Correlation IDs (3h)

### Problem

The `logging_config.py` already has:
- `JSONFormatter` that emits `correlation_id` on every log line
- `get_correlation_id()` / `set_correlation_id()` / `new_correlation_id()`
- `HumanFormatter` with color support

But adoption is minimal — most modules use `logger.info()` without passing structured `extra` fields like `task_id`, `agent_id`, or `correlation_id`.

### Step-by-Step

#### Step 5.1: Add structured logging helper (0.5h)

**File:** `src/ai_company/logging_config.py`

Add a convenience context manager and decorator:

```python
from contextlib import contextmanager

@contextmanager
def correlation_scope(cid: str | None = None):
    """Context manager that sets a correlation ID for the scope."""
    new_id = cid or new_correlation_id()
    old_id = _correlation_id.get()
    _correlation_id.set(new_id)
    try:
        yield new_id
    finally:
        _correlation_id.set(old_id)


def task_logger(task_id: str, agent_id: str = "") -> logging.LoggerAdapter:
    """Get a logger pre-bound with task_id and agent_id as extra fields."""
    logger = logging.getLogger("ai_company")
    return logging.LoggerAdapter(logger, {"task_id": task_id, "agent_id": agent_id})
```

#### Step 5.2: Add `extra` fields to key log calls in executor (1h)

**File:** `src/ai_company/executor/loop.py`

Update the highest-value log calls to include structured context:

```python
# In _process_task():
logger.info(
    "Processing task %s for agent %s",
    task.id[:8],
    task.receiver_id,
    extra={"task_id": task.id, "agent_id": task.receiver_id, "correlation_id": task.correlation_id},
)

# In _complete_task():
logger.info(
    "Task %s -> %s",
    task.id[:8],
    status.value,
    extra={"task_id": task.id, "agent_id": task.receiver_id, "new_status": status.value},
)

# In _resume_parked_tasks():
logger.info(
    "HITL resolved for task %s: %s",
    task_id,
    "approved" if decision else "rejected",
    extra={"task_id": task_id, "hitl_decision": "approved" if decision else "rejected"},
)
```

#### Step 5.3: Add correlation IDs to MessageBus operations (0.5h)

**File:** `src/ai_company/orchestrator/message_bus.py`

Update `send_task()` and `update_task_status()`:

```python
# In send_task():
logger.info(
    "Task %s sent from [%s] to [%s] (correlation=%s).",
    task.id,
    task.sender_id,
    task.receiver_id,
    task.correlation_id,
    extra={
        "task_id": task.id,
        "sender_id": task.sender_id,
        "receiver_id": task.receiver_id,
        "correlation_id": task.correlation_id,
        "event": "task_created",
    },
)
```

#### Step 5.4: Add correlation ID propagation in CLI commands (0.5h)

**File:** `src/ai_company/cli/main.py`

Update the `_init_logging` callback to set a root correlation ID:

```python
def _init_logging() -> None:
    """Configure structured logging once, on first CLI invocation."""
    from ai_company.logging_config import new_correlation_id, setup_logging

    setup_logging()
    cid = new_correlation_id()
    logging.getLogger("ai_company").info(
        "CLI invocation started",
        extra={"correlation_id": cid, "event": "cli_start"},
    )
```

#### Step 5.5: Add structured logging to KPI collectors (0.5h)

**File:** `src/ai_company/dashboard/kpis/base.py`

Update `_load_json()` and `_load_yaml()` to include file path in structured logs:

```python
def _load_json(self, rel_path: str | Path) -> Any:
    path = self.root / rel_path
    if not path.exists():
        logger.debug("JSON file not found, returning empty: %s", path, extra={"file_path": str(path)})
        return []
    # ... rest unchanged
```

### Files Modified
- `src/ai_company/logging_config.py` (add `correlation_scope`, `task_logger`)
- `src/ai_company/executor/loop.py` (structured extra fields on key log calls)
- `src/ai_company/orchestrator/message_bus.py` (structured extra fields)
- `src/ai_company/cli/main.py` (root correlation ID)
- `src/ai_company/dashboard/kpis/base.py` (file path in logs)

### Risk Areas
- `logging.LoggerAdapter` does not propagate `extra` to child loggers by default — test that JSONFormatter picks up the extra fields
- Adding `extra` dicts to hot-path logging calls has negligible performance cost (dict creation is fast)
- Existing tests that check log output may need updating if they assert on exact log message strings

---

## Task 6: CLI Type Hints + Docstrings (4h)

### Problem

Most CLI module functions lack:
- Return type annotations (many already have `-> None` from Typer patterns)
- Docstrings on public command functions
- Type hints on local variables

### Files to Update

All 21 CLI modules under `src/ai_company/cli/`:

| File | Functions Needing Docstrings | Functions Needing Type Hints |
|------|-----------------------------|------------------------------|
| `agents.py` | `list_agents` | — (already typed) |
| `board.py` | all commands | local vars |
| `company.py` | all commands | local vars |
| `customer_success.py` | all commands | — |
| `dashboard.py` | `dashboard`, `kpi_list`, `kpi_show` | `_open_browser` return |
| `decision.py` | all commands | — |
| `departments.py` | all commands | — |
| `doctor.py` | all commands | — |
| `executives.py` | all commands | — |
| `executor.py` | `start`, `tick`, `run_task`, `cycle`, `status`, `dlq_*` | — |
| `graph.py` | all commands | — |
| `hr.py` | all commands | — |
| `legal.py` | all commands | — |
| `main.py` | `sop`, `raci`, `generate`, `status` | — |
| `marketing.py` | all commands | — |
| `memory.py` | `list`, `add`, `search`, `consolidate` | — |
| `models.py` | all commands | — |
| `orchestrator.py` | `tick`, `briefing`, `scheduler_*`, `escalation_*`, `approval_*`, `postmortem_*` | — |
| `sales.py` | all commands | — |
| `specialists.py` | all commands | — |
| `workflows.py` | all commands | — |

### Step-by-Step

#### Step 6.1: Audit existing type hints (0.5h)

Run mypy baseline:
```bash
cd ai-company && mypy src/ai_company/cli/ --ignore-missing-imports 2>&1 | head -50
```

Catalog the existing mypy errors to prioritize fixes.

#### Step 6.2: Add docstrings to all public CLI functions (2.5h)

Pattern for each function:
```python
@app.command()
def my_command(
    arg: str = typer.Argument(..., help="Description"),
    option: str = typer.Option("default", help="Description"),
) -> None:
    """One-line summary of what this command does.

    Longer description if needed. Explain the primary use case.
    """
    ...
```

Priority order:
1. `executor.py` — 10 commands, most complex
2. `orchestrator.py` — 15+ commands across sub-apps
3. `memory.py` — 4 commands (adding new ones in Task 3)
4. `main.py` — 4 commands (public entry point)
5. All other modules — 1-3 commands each

#### Step 6.3: Add return type annotations and local variable types (1h)

Most Typer commands already have `-> None`. Focus on:
- Helper functions like `_open_browser(port: int) -> None`
- Functions that return data: `scheduler_add()` etc.
- Local variable annotations where complex:

```python
# BEFORE:
tasks = json.loads(inbox_path.read_text(encoding="utf-8"))
status_counts = {}
for t in tasks:
    s = t.get("status", "unknown")
    status_counts[s] = status_counts.get(s, 0) + 1

# AFTER:
tasks: list[dict[str, Any]] = json.loads(inbox_path.read_text(encoding="utf-8"))
status_counts: dict[str, int] = {}
for t in tasks:
    s: str = t.get("status", "unknown")
    status_counts[s] = status_counts.get(s, 0) + 1
```

### Files Modified
- `src/ai_company/cli/agents.py`
- `src/ai_company/cli/board.py`
- `src/ai_company/cli/company.py`
- `src/ai_company/cli/customer_success.py`
- `src/ai_company/cli/dashboard.py`
- `src/ai_company/cli/decision.py`
- `src/ai_company/cli/departments.py`
- `src/ai_company/cli/doctor.py`
- `src/ai_company/cli/executives.py`
- `src/ai_company/cli/executor.py`
- `src/ai_company/cli/graph.py`
- `src/ai_company/cli/hr.py`
- `src/ai_company/cli/legal.py`
- `src/ai_company/cli/main.py`
- `src/ai_company/cli/marketing.py`
- `src/ai_company/cli/memory.py`
- `src/ai_company/cli/models.py`
- `src/ai_company/cli/orchestrator.py`
- `src/ai_company/cli/sales.py`
- `src/ai_company/cli/specialists.py`
- `src/ai_company/cli/workflows.py`

### Risk Areas
- Typer auto-generates `--help` from docstrings — ensure docstrings don't have trailing whitespace or odd formatting
- Some CLI functions have complex Typer Option patterns with `Optional[str]` — these need `from __future__ import annotations` at the top (already present in most files)
- No runtime risk — purely cosmetic changes

---

## Task 7: Token Counting Integration (2h)

### Problem

The `LLMClient.execute_task()` method does NOT integrate with `CostTracker` for automatic token counting. While `AgentLoop` passes `CostTracker` through its constructor and calls `record_usage()`, the standalone `LLMClient` (used by CLI commands and tests) does not track costs.

Looking at the code flow:
1. `AgentLoop.__init__` takes `cost_tracker: CostTracker`
2. `AgentLoop.run()` calls `self.llm.execute_task()` → gets raw response → calls `self.cost_tracker.record_usage()` if available
3. But `LLMClient.execute_task()` itself never records usage

### Step-by-Step

#### Step 7.1: Add optional `CostTracker` to `LLMClient` (0.5h)

**File:** `src/ai_company/llm/client.py`

```python
from ai_company.llm.cost_tracker import CostTracker

class LLMClient:
    def __init__(
        self,
        config_path: str = "company/models.yaml",
        registry_path: str = "company/agent-registry.json",
        cost_tracker: CostTracker | None = None,  # NEW
    ) -> None:
        self.router = ModelRouter(config_path=config_path, registry_path=registry_path)
        self._providers: dict[str, LLMProvider] = {}
        self._circuit_breakers: dict[str, CircuitBreaker] = {}
        self._cost_tracker = cost_tracker  # NEW
        self._init_providers()
```

#### Step 7.2: Record usage after each successful LLM call (1h)

**File:** `src/ai_company/llm/client.py`

In `execute_task()`, after a successful parse:
```python
# After parsed = self._parse_response(response.content)
if parsed is not None:
    # NEW: Record token usage and cost
    if self._cost_tracker is not None:
        # Extract token counts from response if available
        prompt_tokens = getattr(response, "prompt_tokens", 0) or 0
        completion_tokens = getattr(response, "completion_tokens", 0) or 0
        self._cost_tracker.record_usage(
            model=model,
            provider=provider_id,
            agent_name=agent_name,
            task_id="",  # Task ID not available at this level
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )
    return parsed
```

Check the `ChatResponse` model to see if token counts are available:

**File:** `src/ai_company/llm/providers/base.py` (need to check)

```python
# If ChatResponse doesn't have token fields, we need to add them:
@dataclass
class ChatResponse:
    content: str
    model: str = ""
    provider: str = ""
    prompt_tokens: int = 0      # NEW
    completion_tokens: int = 0  # NEW
    total_tokens: int = 0       # NEW
```

Check provider implementations to extract token counts from API responses.

#### Step 7.3: Wire token counts from provider responses (0.5h)

**File:** `src/ai_company/llm/providers/openai_compatible.py`

Ensure `chat()` returns token counts in the `ChatResponse`:
```python
# In OpenAICompatibleProvider.chat():
# The OpenAI API response includes usage:
# {"prompt_tokens": N, "completion_tokens": N, "total_tokens": N}
response = client.chat.completions.create(...)
usage = response.usage
return ChatResponse(
    content=response.choices[0].message.content or "",
    model=response.model,
    prompt_tokens=usage.prompt_tokens if usage else 0,
    completion_tokens=usage.completion_tokens if usage else 0,
    total_tokens=usage.total_tokens if usage else 0,
)
```

**File:** `src/ai_company/llm/providers/ollama.py`

Ollama API also returns `eval_count` (output tokens) and `prompt_eval_count` (input tokens):
```python
# In OllamaProvider.chat():
return ChatResponse(
    content=response.get("response", ""),
    model=model,
    prompt_tokens=response.get("prompt_eval_count", 0),
    completion_tokens=response.get("eval_count", 0),
    total_tokens=response.get("prompt_eval_count", 0) + response.get("eval_count", 0),
)
```

#### Step 7.4: Update `AgentLoop` to use integrated tracking (0h)

**File:** `src/ai_company/executor/agent_loop.py`

The `AgentLoop` already has its own cost tracking. With the new `LLMClient` integration, we need to avoid double-counting. Two options:

**Option A (Recommended):** Keep `AgentLoop` as the authoritative cost tracker. Pass `cost_tracker=None` to `LLMClient` from `AgentLoop`. Only non-loop callers (CLI `run_task`, tests) pass a tracker.

**Option B:** Remove cost tracking from `AgentLoop` and let `LLMClient` handle it exclusively.

Go with Option A — minimal change, no risk of double-counting:
```python
# In AgentLoop.__init__():
self.llm = LLMClient(
    cost_tracker=None,  # AgentLoop handles cost tracking itself
)
```

This is already the default since `cost_tracker` defaults to `None` in the updated `LLMClient.__init__`.

#### Step 7.5: Add tests (0h)

**New file:** `tests/test_cost_tracker_integration.py`

```python
def test_llm_client_records_usage():
    tracker = CostTracker(results_dir=tmp_dir)
    llm = LLMClient(cost_tracker=tracker)
    # Mock provider to return response with token counts
    # Verify tracker.record_usage() was called
```

### Files Modified
- `src/ai_company/llm/client.py` (add `cost_tracker` param, record usage)
- `src/ai_company/llm/providers/base.py` (add token fields to `ChatResponse`)
- `src/ai_company/llm/providers/openai_compatible.py` (extract usage from API)
- `src/ai_company/llm/providers/ollama.py` (extract usage from API)
- `tests/test_cost_tracker_integration.py` (NEW)

### Risk Areas
- **Double-counting:** `AgentLoop` already tracks costs — ensure `LLMClient` defaults to `cost_tracker=None` to avoid double-recording
- **Missing token counts:** Some providers may not return usage data (e.g., streaming responses) — use `or 0` guards
- **ChatResponse change:** Adding fields to `ChatResponse` dataclass could break existing code that constructs it positionally — use keyword-only args
- `getattr(response, "prompt_tokens", 0)` is defensive against providers that don't set these fields yet

---

## Integration Testing Checklist

After all 7 tasks are complete:

```bash
# 1. Full test suite
cd ai-company && pytest

# 2. Type checking
mypy src/ai_company/ --ignore-missing-imports

# 3. Linting
ruff check src/ai_company/

# 4. CLI smoke tests
ai-company --help
ai-company agents list
ai-company memory list
ai-company memory search --query "test"
ai-company memory prune --dry-run
ai-company memory consolidate-all
ai-company executor cycle --max-cycles 1
ai-company executor daemon-status

# 5. Dashboard startup (verify I/O changes don't break)
ai-company dashboard --port 9420 --no-open &
curl http://localhost:9420/health
curl http://localhost:9420/metrics
kill %1

# 6. Briefing generation
ai-company orchestrator briefing

# 7. Pre-commit hooks
pre-commit run --all-files
```

---

## Summary Table

| Task | Hours | Files Modified | Files Created | Key Risk |
|------|-------|---------------|---------------|----------|
| 1. Peripheral I/O | 4h | 9 | 0 | Race conditions in delegate_task |
| 2. Briefing mypy | 1h | 1 | 0 | Minimal |
| 3. Memory consolidation | 7h | 3 | 2 | TTL edge cases, semantic search fallback |
| 4. Cycle daemon | 4h | 2 | 2 | Signal handling on Windows |
| 5. Structured logging | 3h | 5 | 0 | LoggerAdapter extra propagation |
| 6. CLI type hints | 4h | 21 | 0 | None (cosmetic) |
| 7. Token counting | 2h | 4 | 1 | Double-counting with AgentLoop |
| **Total** | **25h** | **45** | **5** | |
