# Design: Task Pipeline — Pagination, Filters, Sorting, Dummy Data Cleanup

**Author:** Software Architect
**Date:** 2026-07-22
**Status:** Ready for Implementation
**Owner:** dashboard-owner

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Trade-off Analysis: Server-Side vs Client-Side](#2-trade-off-analysis)
3. [Backend Changes](#3-backend-changes)
4. [Frontend Changes](#4-frontend-changes)
5. [Dummy Data Cleanup](#5-dummy-data-cleanup)
6. [File Change List](#6-file-change-list)
7. [New Test Cases](#7-new-test-cases)
8. [Implementation Sequence](#8-implementation-sequence)

---

## 1. Executive Summary

This design replaces the current "load everything, filter in browser" pattern on the `/tasks` page with server-side pagination, filtering, and sorting. At ~1600 tasks (and growing), transferring the full payload on every 15-second poll is wasteful and blocks the UI from rendering quickly. Server-side pagination reduces the default response from ~1600 task objects to 20 per request, an **80x reduction** in JSON payload size.

Key decisions:
- **Server-side** pagination, filtering, sorting (all done server)
- **Top-level pagination** (one paginator across the entire pipeline, not per-column)
- **Client-side column slicing** of the paginated result for Kanban rendering
- **New `GET /api/tasks/paginated`** endpoint (additive, non-breaking)
- Dummy data cleanup via a dedicated **CLI subcommand + validation guard**

---

## 2. Trade-off Analysis

| Dimension | Server-Side (Chosen) | Client-Side |
|---|---|---|
| **Payload size** | ~20–100 tasks per request (~5–25 KB) | All ~1600 tasks (~400 KB) every 15s |
| **Browser memory** | Constant, bounded | Grows linearly with task count |
| **Render time** | Fast — Alpine.js renders 20 DOM nodes | Slow — 1600 `<template x-for>` iterations |
| **Filter/sort latency** | Single HTTP round-trip (~50ms) | Instant (in-memory) — but blocks main thread |
| **Backend complexity** | Moderate — new query function + response model | None — current code works |
| **Backend load** | One FileStore read per request (atomic, cached) | Same — one read, but bigger payload |
| **WebSocket updates** | Need to re-fetch on update (or optimistic patch) | Already have full dataset in memory |
| **Column counts** | Server returns `total_counts` alongside page | Computed client-side for free |
| **Future scaling** | Handles 10K+ tasks without degradation | Breaks at ~5K tasks |
| **Backward compat** | New endpoint; old `/api/tasks` preserved | Existing endpoint unchanged |

**Why server-side wins:** The inbox is a flat JSON file read through an atomic `FileStore`. There's no SQL index — so the "query" is a Python list comprehension over ~1600 dicts. At this scale, both approaches take <5ms for the filter/sort step. The differentiator is **payload size and render cost**. Sending 1600 tasks every 15 seconds wastes bandwidth and forces Alpine.js to diff a large array. With server-side pagination, we send 20 tasks and Alpine.js only re-renders 20 DOM nodes.

**Risk:** WebSocket `task_update` events deliver the full updated task. The client must decide whether to re-fetch (simple, always correct) or patch locally (faster, but may drift if filters changed). We choose **re-fetch** for correctness, since the 15-second poll already provides a safety net.

---

## 3. Backend Changes

### 3.1 New Response Model: `PaginatedTasks`

Add to `src/ai_company/dashboard/models.py`:

```python
class PaginatedTasks(BaseModel):
    """Server-side paginated task response."""
    items: list[TaskItem]
    total: int                          # Total matching tasks (before pagination)
    page: int                           # Current page (1-indexed)
    page_size: int                      # Requested page size
    total_pages: int                    # ceil(total / page_size)
    counts_by_status: dict[str, int]    # {"pending": 42, "in_progress": 15, ...}
```

### 3.2 New Query Parameters

Add to `GET /api/tasks/paginated`:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | int | 1 | 1-indexed page number |
| `page_size` | int | 20 | Results per page (validated: 10, 20, 50, 100) |
| `status` | str | "" | Comma-separated status filter (e.g. `"pending,in_progress"`) |
| `priority` | str | "" | Comma-separated priority filter (e.g. `"high,critical"`) |
| `department` | str | "" | Filter by receiver agent's department |
| `agent` | str | "" | Filter by sender_id or receiver_id (substring match) |
| `sort_by` | str | "created_at" | Sort field: `created_at`, `priority`, `status`, `receiver_id` |
| `sort_dir` | str | "desc" | Sort direction: `asc` or `desc` |

### 3.3 New Endpoint Implementation

Add to `src/ai_company/dashboard/api.py`:

```python
import math
from fastapi import Query


def _apply_priority_sort_key(task: dict, reverse: bool) -> tuple:
    """Sort key that orders priority: critical > high > medium > low."""
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    order = priority_order.get(task.get("priority", "medium"), 2)
    return (order, task.get("created_at", ""))


def _apply_status_sort_key(task: dict) -> tuple:
    """Sort key that orders status: escalated > failed > pending > in_progress > completed."""
    status_order = {
        "escalated": 0, "failed": 1, "pending": 2,
        "in_progress": 3, "completed": 4,
    }
    return (status_order.get(task.get("status", ""), 5),)


@router.get("/tasks/paginated", response_model=PaginatedTasks, tags=["tasks"])
def list_tasks_paginated(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=10, le=100),
    status: str = "",
    priority: str = "",
    department: str = "",
    agent: str = "",
    sort_by: str = "created_at",
    sort_dir: str = "desc",
) -> PaginatedTasks:
    """List tasks with server-side pagination, filtering, and sorting.

    Returns a page of tasks plus metadata (total, counts, total_pages).
    The counts_by_status field always reflects the filtered (but un-paginated)
    result set, so Kanban column headers stay accurate.
    """
    # Page size must be one of the allowed values
    if page_size not in (10, 20, 50, 100):
        page_size = 20

    tasks = _read_all_tasks()

    # ── Filter: status (comma-separated) ──
    if status:
        allowed_statuses = {s.strip() for s in status.split(",") if s.strip()}
        tasks = [t for t in tasks if t.get("status") in allowed_statuses]

    # ── Filter: priority (comma-separated) ──
    if priority:
        allowed_priorities = {p.strip() for p in priority.split(",") if p.strip()}
        tasks = [t for t in tasks if t.get("priority") in allowed_priorities]

    # ── Filter: department (via agent registry lookup) ──
    if department:
        registry = _load_registry()
        dept_agent_names = {
            a["name"] for a in registry
            if (a.get("department") or "").lower() == department.lower()
            or (a.get("department") or "").replace(" ", "_").lower() == department.lower()
        }
        tasks = [t for t in tasks if t.get("receiver_id") in dept_agent_names
                 or t.get("sender_id") in dept_agent_names]

    # ── Filter: agent (substring match on sender_id or receiver_id) ──
    if agent:
        agent_lower = agent.lower()
        tasks = [t for t in tasks
                 if agent_lower in t.get("receiver_id", "").lower()
                 or agent_lower in t.get("sender_id", "").lower()]

    # ── Counts by status (before pagination) ──
    counts: dict[str, int] = {}
    for t in tasks:
        s = t.get("status", "pending")
        counts[s] = counts.get(s, 0) + 1

    # ── Sort ──
    valid_sort_fields = {"created_at", "priority", "status", "receiver_id"}
    if sort_by not in valid_sort_fields:
        sort_by = "created_at"
    if sort_dir not in ("asc", "desc"):
        sort_dir = "desc"

    reverse = sort_dir == "desc"

    if sort_by == "priority":
        tasks.sort(key=lambda t: _apply_priority_sort_key(t, reverse), reverse=reverse)
    elif sort_by == "status":
        tasks.sort(key=_apply_status_sort_key, reverse=reverse)
    elif sort_by == "created_at":
        tasks.sort(key=lambda t: t.get("created_at", "") or "", reverse=reverse)
    elif sort_by == "receiver_id":
        tasks.sort(key=lambda t: t.get("receiver_id", ""), reverse=reverse)

    # ── Paginate ──
    total = len(tasks)
    total_pages = max(1, math.ceil(total / page_size))
    start = (page - 1) * page_size
    end = start + page_size
    page_items = tasks[start:end]

    return PaginatedTasks(
        items=[TaskItem(**t) for t in page_items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        counts_by_status=counts,
    )
```

### 3.4 Non-Breaking Backward Compatibility

The existing `GET /api/tasks` endpoint is **preserved unchanged**. Other consumers (KPI collectors, mobile API, cost tracker) that call it will continue to work. The new `GET /api/tasks/paginated` is purely additive.

---

## 4. Frontend Changes

### 4.1 Alpine.js State Additions

Add to the `dashboard()` function in `app.js`:

```javascript
// ── Task Pipeline Pagination ──────────────────────
taskPage: 1,
taskPageSize: 20,
taskSortBy: 'created_at',
taskSortDir: 'desc',
taskFilters: {
  status: [],        // e.g. ['pending', 'in_progress']
  priority: [],      // e.g. ['high', 'critical']
  department: '',
  agent: '',
},
taskPagination: {
  total: 0,
  total_pages: 1,
  counts_by_status: {},
},
```

### 4.2 New Data Loading Method

Replace the direct `/api/tasks` fetch in `loadPageData` for the `/tasks` path with a paginated fetch:

```javascript
async loadTasksPage() {
  const params = new URLSearchParams();
  params.set('page', this.taskPage);
  params.set('page_size', this.taskPageSize);
  params.set('sort_by', this.taskSortBy);
  params.set('sort_dir', this.taskSortDir);

  if (this.taskFilters.status.length > 0) {
    params.set('status', this.taskFilters.status.join(','));
  }
  if (this.taskFilters.priority.length > 0) {
    params.set('priority', this.taskFilters.priority.join(','));
  }
  if (this.taskFilters.department) {
    params.set('department', this.taskFilters.department);
  }
  if (this.taskFilters.agent) {
    params.set('agent', this.taskFilters.agent);
  }

  const data = await this.fetchJSON(`/api/tasks/paginated?${params}`);
  if (data) {
    this.tasks = data.items;
    this.taskPagination = {
      total: data.total,
      total_pages: data.total_pages,
      counts_by_status: data.counts_by_status,
    };
  }
},
```

### 4.3 Updated `loadPageData` for `/tasks` Path

```javascript
// In loadPageData():
} else if (path === '/tasks') {
  const agentsData = await this.fetchJSON('/api/agents');
  if (agentsData) this.agents = agentsData;
  await this.loadTasksPage();
}
```

### 4.4 Updated `kanbanTasks` Computed

The existing `kanbanTasks` computed property already filters `this.tasks` by status. Since the backend now returns a paginated subset, the Kanban columns will show only the tasks in the current page. However, we need the **total counts per column** for the header badges. Use `taskPagination.counts_by_status` instead:

```javascript
get kanbanTasks() {
  return {
    pending: this.tasks.filter(t => t.status === 'pending'),
    in_progress: this.tasks.filter(t => t.status === 'in_progress'),
    completed: this.tasks.filter(t => t.status === 'completed'),
    failed: this.tasks.filter(t => t.status === 'failed'),
    escalated: this.tasks.filter(t => t.status === 'escalated'),
  };
},

// New: total counts for column badges (from server-side aggregation)
get kanbanCounts() {
  const c = this.taskPagination.counts_by_status || {};
  return {
    pending: c.pending || 0,
    in_progress: c.in_progress || 0,
    completed: c.completed || 0,
    failed: c.failed || 0,
    escalated: c.escalated || 0,
  };
},
```

### 4.5 New Action Methods

```javascript
goToPage(page) {
  if (page < 1 || page > this.taskPagination.total_pages) return;
  this.taskPage = page;
  this.loadTasksPage();
},

nextPage() { this.goToPage(this.taskPage + 1); },
prevPage() { this.goToPage(this.taskPage - 1); },

setPageSize(size) {
  this.taskPageSize = size;
  this.taskPage = 1;  // Reset to first page
  this.loadTasksPage();
},

setSortBy(field) {
  if (this.taskSortBy === field) {
    this.taskSortDir = this.taskSortDir === 'asc' ? 'desc' : 'asc';
  } else {
    this.taskSortBy = field;
    this.taskSortDir = field === 'created_at' ? 'desc' : 'asc';
  }
  this.taskPage = 1;
  this.loadTasksPage();
},

toggleFilter(type, value) {
  const arr = this.taskFilters[type];
  const idx = arr.indexOf(value);
  if (idx >= 0) {
    arr.splice(idx, 1);
  } else {
    arr.push(value);
  }
  this.taskPage = 1;
  this.loadTasksPage();
},

clearAllFilters() {
  this.taskFilters = { status: [], priority: [], department: '', agent: '' };
  this.taskSortBy = 'created_at';
  this.taskSortDir = 'desc';
  this.taskPage = 1;
  this.loadTasksPage();
},

hasActiveFilters() {
  return this.taskFilters.status.length > 0
      || this.taskFilters.priority.length > 0
      || this.taskFilters.department !== ''
      || this.taskFilters.agent !== '';
},
```

### 4.6 WebSocket Update Handling

Update the `task_update` handler in `handleWSMessage` to re-fetch the current page instead of trying to patch a potentially-filtered local state:

```javascript
case 'task_update':
  if (msg.payload) {
    const event = msg.event || 'updated';
    if (event === 'deleted') {
      this.tasks = this.tasks.filter(t => t.id !== updatedTask.id);
      this.taskPagination.total = Math.max(0, this.taskPagination.total - 1);
    } else {
      // Re-fetch the current page for correctness
      this.loadTasksPage();
    }
  }
  break;
```

### 4.7 HTML: Filter Bar (above Kanban board)

Insert between the header row and the Kanban grid in `tasks.html`:

```html
<!-- ═══ FILTER & SORT BAR ═══ -->
<div class="bg-surface-900/60 rounded-xl border border-surface-700/50 p-4 mb-6">
  <div class="flex flex-wrap items-center gap-3">

    <!-- Priority Filter Chips -->
    <div class="flex items-center gap-1.5">
      <span class="text-xs text-surface-500 font-medium mr-1">Priority:</span>
      <template x-for="p in ['low', 'medium', 'high', 'critical']" :key="p">
        <button @click="toggleFilter('priority', p)"
                :class="taskFilters.priority.includes(p)
                  ? priorityClass(p) + ' ring-1 ring-white/20'
                  : 'bg-surface-800 text-surface-500 border border-surface-700 hover:border-surface-600'"
                class="px-2.5 py-1 rounded-md text-[11px] font-medium transition-all"
                x-text="p"></button>
      </template>
    </div>

    <!-- Department Filter -->
    <div class="flex items-center gap-1.5">
      <span class="text-xs text-surface-500 font-medium">Dept:</span>
      <select x-model="taskFilters.department"
              @change="taskPage = 1; loadTasksPage()"
              class="bg-surface-800 border border-surface-700 rounded-md px-2 py-1 text-xs text-surface-300 focus:ring-1 focus:ring-brand-500">
        <option value="">All</option>
        <template x-for="d in uniqueDepartments" :key="d">
          <option :value="d" x-text="d"></option>
        </template>
      </select>
    </div>

    <!-- Agent Search -->
    <div class="flex items-center gap-1.5">
      <span class="text-xs text-surface-500 font-medium">Agent:</span>
      <input type="text" x-model.debounce.300ms="taskFilters.agent"
             @input="taskPage = 1; loadTasksPage()"
             placeholder="Search agent..."
             class="bg-surface-800 border border-surface-700 rounded-md px-2 py-1 text-xs text-surface-300 placeholder-surface-600 focus:ring-1 focus:ring-brand-500 w-32">
    </div>

    <!-- Sort Dropdown -->
    <div class="flex items-center gap-1.5 ml-auto">
      <span class="text-xs text-surface-500 font-medium">Sort:</span>
      <select @change="setSortBy($event.target.value)"
              class="bg-surface-800 border border-surface-700 rounded-md px-2 py-1 text-xs text-surface-300">
        <option value="created_at" :selected="taskSortBy === 'created_at'">Date</option>
        <option value="priority" :selected="taskSortBy === 'priority'">Priority</option>
        <option value="status" :selected="taskSortBy === 'status'">Status</option>
        <option value="receiver_id" :selected="taskSortBy === 'receiver_id'">Agent</option>
      </select>
      <button @click="taskSortDir = taskSortDir === 'asc' ? 'desc' : 'asc'; loadTasksPage()"
              class="text-surface-400 hover:text-surface-200 transition-colors p-1"
              :title="taskSortDir === 'asc' ? 'Ascending' : 'Descending'">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                x-bind:d="taskSortDir === 'asc' ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'"/>
        </svg>
      </button>
    </div>

    <!-- Clear Filters -->
    <button x-show="hasActiveFilters()"
            @click="clearAllFilters()"
            class="text-xs text-red-400 hover:text-red-300 font-medium transition-colors">
      Clear all
    </button>
  </div>
</div>
```

### 4.8 HTML: Pagination Controls (below Kanban board)

Insert after the Failed/Escalated row:

```html
<!-- ═══ PAGINATION ═══ -->
<div class="flex items-center justify-between bg-surface-900/60 rounded-xl border border-surface-700/50 px-4 py-3 mb-6">
  <!-- Left: Page info -->
  <div class="text-xs text-surface-500">
    Showing <span class="text-surface-300 font-medium"
                 x-text="Math.min((taskPage - 1) * taskPageSize + 1, taskPagination.total)"></span>
    – <span class="text-surface-300 font-medium"
            x-text="Math.min(taskPage * taskPageSize, taskPagination.total)"></span>
    of <span class="text-surface-300 font-medium" x-text="taskPagination.total"></span> tasks
  </div>

  <!-- Center: Page navigation -->
  <div class="flex items-center gap-1">
    <button @click="prevPage()" :disabled="taskPage <= 1"
            class="px-2.5 py-1 rounded-md text-xs font-medium transition-colors
                   bg-surface-800 text-surface-400 hover:text-surface-200 hover:bg-surface-700
                   disabled:opacity-30 disabled:cursor-not-allowed">
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
    </button>

    <template x-for="pageNum in paginationRange()" :key="pageNum">
      <button @click="goToPage(pageNum)"
              :class="pageNum === taskPage
                ? 'bg-brand-600 text-white'
                : 'bg-surface-800 text-surface-400 hover:text-surface-200 hover:bg-surface-700'"
              class="w-7 h-7 rounded-md text-xs font-medium transition-colors"
              x-text="pageNum"></button>
    </template>

    <button @click="nextPage()" :disabled="taskPage >= taskPagination.total_pages"
            class="px-2.5 py-1 rounded-md text-xs font-medium transition-colors
                   bg-surface-800 text-surface-400 hover:text-surface-200 hover:bg-surface-700
                   disabled:opacity-30 disabled:cursor-not-allowed">
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
    </button>
  </div>

  <!-- Right: Page size selector -->
  <div class="flex items-center gap-1.5">
    <span class="text-xs text-surface-500">Per page:</span>
    <template x-for="size in [10, 20, 50, 100]" :key="size">
      <button @click="setPageSize(size)"
              :class="size === taskPageSize
                ? 'bg-brand-600 text-white'
                : 'bg-surface-800 text-surface-500 hover:text-surface-300'"
              class="w-7 h-7 rounded text-[10px] font-medium transition-colors"
              x-text="size"></button>
    </template>
  </div>
</div>
```

### 4.9 Pagination Range Helper

Add to `app.js`:

```javascript
paginationRange() {
  const total = this.taskPagination.total_pages;
  const current = this.taskPage;
  const range = [];
  const delta = 2;  // Show 2 pages on each side of current

  for (let i = Math.max(1, current - delta); i <= Math.min(total, current + delta); i++) {
    range.push(i);
  }

  // Add ellipsis indicators (handled as special page numbers)
  if (range[0] > 1) range.unshift(1);
  if (range[range.length - 1] < total) range.push(total);

  // Deduplicate
  return [...new Set(range)];
},
```

### 4.10 Kanban Column Badge Update

Replace the badge counts in column headers. Change from:
```html
<span class="text-xs text-surface-500 ml-auto font-mono"
      x-text="kanbanTasks.pending.length"></span>
```
To:
```html
<span class="text-xs text-surface-500 ml-auto font-mono"
      x-text="kanbanCounts.pending"></span>
```

This ensures the column header shows the **total** count across all pages, not just the current page's count.

---

## 5. Dummy Data Cleanup

### 5.1 Identification Criteria

A task is considered **dummy/placeholder** if it matches ANY of these rules:

1. **Short ID pattern**: `id` matches regex `^t\d+$` (e.g., `t1`, `t2`, `t3`)
2. **Trivial instruction**: `instruction` is 5 or fewer characters (e.g., `"do x"`, `"test"`)
3. **Single-letter agents**: Either `sender_id` or `receiver_id` is a single character (e.g., `"a"`, `"b"`)
4. **Missing required fields**: `sender_id` or `receiver_id` is empty
5. **Test-instruction patterns**: `instruction` matches common test patterns like `/^test\b/i`, `/^do [a-z]$/i`

### 5.2 Cleanup Script: `ai-company scripts/cleanup-dummy-tasks`

Add a CLI subcommand to the Typer app in `src/ai_company/cli/main.py`:

```python
# In src/ai_company/cli/main.py, add subcommand:

@cli_app.command()
def cleanup_tasks(
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be deleted without deleting"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show details of each dummy task"),
) -> None:
    """Remove dummy/placeholder tasks from inbox.json.

    Identifies tasks with trivial instructions, single-letter agent IDs,
    or test-pattern IDs and removes them. Use --dry-run to preview first.
    """
    from ai_company.orchestrator.message_bus import MessageBus

    bus = MessageBus(".opencode/inbox.json")
    all_tasks = bus.get_all_tasks()

    import re

    def is_dummy(task) -> bool:
        # Rule 1: Short ID pattern (t1, t2, etc.)
        if re.match(r'^t\d+$', task.id):
            return True
        # Rule 2: Trivial instruction (<=5 chars)
        if len(task.instruction.strip()) <= 5:
            return True
        # Rule 3: Single-letter agent IDs
        if len(task.sender_id.strip()) == 1 or len(task.receiver_id.strip()) == 1:
            return True
        # Rule 4: Missing agent IDs
        if not task.sender_id.strip() or not task.receiver_id.strip():
            return True
        # Rule 5: Test instruction patterns
        if re.match(r'^test\b', task.instruction, re.IGNORECASE):
            return True
        if re.match(r'^do [a-z]$', task.instruction, re.IGNORECASE):
            return True
        return False

    dummies = [t for t in all_tasks if is_dummy(t)]
    real = [t for t in all_tasks if not is_dummy(t)]

    typer.echo(f"Found {len(dummies)} dummy tasks out of {len(all_tasks)} total.")

    if verbose:
        for t in dummies:
            typer.echo(f"  - {t.id[:8]} | {t.sender_id[:20]} -> {t.receiver_id[:20]} | {t.instruction[:50]}")

    if dry_run:
        typer.echo(f"\n[dry-run] Would remove {len(dummies)} tasks, keep {len(real)}.")
    else:
        if not dummies:
            typer.echo("Nothing to clean up.")
            return
        confirm = typer.confirm(f"Remove {len(dummies)} dummy tasks?")
        if confirm:
            for t in dummies:
                bus.delete_task(t.id)
            typer.echo(f"Removed {len(dummies)} dummy tasks. {len(real)} tasks remaining.")
        else:
            typer.echo("Aborted.")
```

### 5.3 Validation Guard: Prevent Future Dummy Data

Add validation to `POST /api/tasks` in `api.py` to reject trivial tasks at creation time:

```python
import re

_TRIVIAL_INSTRUCTION_RE = re.compile(r'^(do [a-z]|test|.{0,5})$', re.IGNORECASE)

@router.post("/tasks", response_model=TaskItem, status_code=201, tags=["tasks"])
def create_task(assign: TaskAssign, background_tasks: BackgroundTasks) -> TaskItem:
    # ... existing code ...

    # Validate: reject trivial instructions
    if len(assign.instruction.strip()) <= 5:
        raise HTTPException(
            status_code=400,
            detail="Instruction too short. Please provide a meaningful task description.",
        )
    if _TRIVIAL_INSTRUCTION_RE.match(assign.instruction.strip()):
        raise HTTPException(
            status_code=400,
            detail="Instruction appears to be a placeholder. Please provide a meaningful task description.",
        )

    # ... rest of existing code ...
```

### 5.4 One-Time Cleanup on Startup (Optional)

Add a startup hook in `app.py` that logs a warning if dummy tasks are detected:

```python
# In create_app(), after configure_state_store():

@app.on_event("startup")
async def _warn_dummy_tasks():
    """Log a warning if dummy tasks are detected in the inbox."""
    from ai_company.dashboard.api import _read_all_tasks
    import re
    tasks = _read_all_tasks()
    dummies = [
        t for t in tasks
        if re.match(r'^t\d+$', t.get("id", ""))
        or len(t.get("instruction", "").strip()) <= 5
        or len(t.get("sender_id", "").strip()) == 1
        or len(t.get("receiver_id", "").strip()) == 1
    ]
    if dummies:
        logger.warning(
            "Detected %d dummy tasks in inbox. Run `ai-company cleanup-tasks` to remove them.",
            len(dummies),
        )
```

---

## 6. File Change List

| File | Change Type | Description |
|---|---|---|
| `src/ai_company/dashboard/models.py` | **Modify** | Add `PaginatedTasks` response model |
| `src/ai_company/dashboard/api.py` | **Modify** | Add `GET /api/tasks/paginated` endpoint, sort helper functions, dummy task validation on `POST /api/tasks` |
| `src/ai_company/dashboard/static/js/app.js` | **Modify** | Add pagination state, `loadTasksPage()`, filter/sort methods, `paginationRange()`, update `loadPageData`, update WS handler |
| `src/ai_company/dashboard/templates/tasks.html` | **Modify** | Add filter bar HTML, pagination controls HTML, update Kanban column badges |
| `src/ai_company/cli/main.py` | **Modify** | Add `cleanup-tasks` subcommand |
| `src/ai_company/dashboard/app.py` | **Modify** | Add startup warning for dummy tasks (optional) |
| `tests/unit/test_dashboard_pagination.py` | **New** | Unit tests for pagination, filtering, sorting |
| `tests/integration/test_tasks_paginated_api.py` | **New** | Integration tests for the new endpoint |
| `tests/unit/test_cleanup_tasks.py` | **New** | Unit tests for the cleanup CLI command |
| `tests/unit/test_dashboard.py` | **Modify** | Update existing task tests to verify backward compatibility |

---

## 7. New Test Cases

### 7.1 Unit Tests: `tests/unit/test_dashboard_pagination.py`

```python
"""Tests for the paginated tasks endpoint."""

class TestPaginatedTasks:
    """Server-side pagination, filtering, sorting."""

    def test_default_pagination(self, client):
        """Default returns page 1 with 20 items."""

    def test_page_size_10(self, client):
        """page_size=10 returns 10 items."""

    def test_page_size_100(self, client):
        """page_size=100 returns up to 100 items."""

    def test_invalid_page_size_falls_back_to_20(self, client):
        """page_size=15 (not allowed) falls back to 20."""

    def test_page_beyond_total_returns_empty(self, client):
        """Page > total_pages returns empty items list."""

    def test_total_pages_calculation(self, client):
        """total_pages = ceil(total / page_size)."""

    def test_filter_by_status_single(self, client):
        """status=pending returns only pending tasks."""

    def test_filter_by_status_multiple(self, client):
        """status=pending,in_progress returns both."""

    def test_filter_by_priority(self, client):
        """priority=high,critical returns only those."""

    def test_filter_by_department(self, client):
        """department=Engineering returns tasks for Engineering agents."""

    def test_filter_by_agent(self, client):
        """agent=lead returns tasks where sender or receiver contains 'lead'."""

    def test_combined_filters(self, client):
        """All filters combine with AND logic."""

    def test_sort_by_created_at_desc(self, client):
        """Default sort: newest first."""

    def test_sort_by_created_at_asc(self, client):
        """sort_dir=asc returns oldest first."""

    def test_sort_by_priority(self, client):
        """sort_by=priority orders critical > high > medium > low."""

    def test_sort_by_status(self, client):
        """sort_by=status orders escalated > failed > pending > in_progress > completed."""

    def test_sort_by_receiver_id(self, client):
        """sort_by=receiver_id orders alphabetically."""

    def test_counts_by_status_reflects_filters(self, client):
        """counts_by_status counts only filtered tasks (before pagination)."""

    def test_empty_result(self, client):
        """No matching tasks returns empty items, total=0."""

    def test_backward_compatibility(self, client):
        """GET /api/tasks still works unchanged."""
```

### 7.2 Integration Tests: `tests/integration/test_tasks_paginated_api.py`

```python
"""End-to-end integration tests for the paginated tasks API."""

class TestPaginatedTasksE2E:
    def test_create_then_paginate(self, client):
        """Create 30 tasks, paginate at page_size=10, verify 3 pages."""

    def test_filter_after_create(self, client):
        """Create tasks with mixed statuses, filter by status."""

    def test_sort_after_create(self, client):
        """Create tasks with different priorities, sort by priority."""

    def test_websocket_update_triggers_re_fetch(self, client):
        """After PATCH /api/tasks/{id}, paginated endpoint reflects change."""

    def test_delete_task_updates_total(self, client):
        """After DELETE, total and total_pages decrease correctly."""

    def test_department_filter_with_real_registry(self, client):
        """Filter by department matches against real agent registry."""
```

### 7.3 Unit Tests: `tests/unit/test_cleanup_tasks.py`

```python
"""Tests for the dummy task cleanup CLI command."""

class TestCleanupDetection:
    def test_short_id_pattern(self):
        """'t1', 't2', 't100' are detected as dummy."""

    def test_trivial_instruction(self):
        """'do x', 'test', 'hi' are detected as dummy."""

    def test_single_letter_agent(self):
        """sender_id='a' or receiver_id='b' detected as dummy."""

    def test_real_task_not_flagged(self):
        """UUID IDs with meaningful instructions are NOT flagged."""

    def test_mixed_real_and_dummy(self):
        """Correctly separates real from dummy tasks."""

class TestCleanupCommand:
    def test_dry_run_does_not_delete(self):
        """--dry-run shows candidates but doesn't modify inbox."""

    def test_cleanup_removes_dummies(self):
        """After cleanup, only real tasks remain."""
```

### 7.4 Backward Compatibility Tests (add to existing `test_dashboard.py`)

```python
class TestBackwardCompatibility:
    def test_old_tasks_endpoint_unchanged(self, setup_dashboard_data):
        """GET /api/tasks still returns list[TaskItem] with same shape."""

    def test_new_paginated_endpoint_coexists(self, setup_dashboard_data):
        """Both endpoints return consistent data for the same task set."""

    def test_create_task_validation(self, setup_dashboard_data):
        """POST /api/tasks rejects trivial instructions (<=5 chars)."""

    def test_create_task_valid_instruction(self, setup_dashboard_data):
        """POST /api/tasks accepts meaningful instructions."""
```

---

## 8. Implementation Sequence

| Step | Task | Dependencies | Estimated Effort |
|---|---|---|---|
| 1 | Add `PaginatedTasks` model to `models.py` | None | 10 min |
| 2 | Add sort helper functions + `/api/tasks/paginated` endpoint to `api.py` | Step 1 | 45 min |
| 3 | Add instruction validation to `POST /api/tasks` | Step 2 | 15 min |
| 4 | Add unit tests for new endpoint (`test_dashboard_pagination.py`) | Steps 1-3 | 45 min |
| 5 | Add integration tests (`test_tasks_paginated_api.py`) | Steps 1-3 | 30 min |
| 6 | Update `app.js` with pagination state + methods | Steps 1-3 | 45 min |
| 7 | Update `tasks.html` with filter bar + pagination controls | Step 6 | 45 min |
| 8 | Update Kanban column badges to use `kanbanCounts` | Step 6 | 10 min |
| 9 | Add `cleanup-tasks` CLI command | Step 3 | 30 min |
| 10 | Add cleanup unit tests | Step 9 | 20 min |
| 11 | Update existing `test_dashboard.py` backward compat tests | Steps 1-3 | 15 min |
| 12 | Add startup dummy-task warning to `app.py` | Step 9 | 10 min |
| 13 | Run full test suite: `ruff check src/ && mypy src/ && pytest` | All | 5 min |

**Total estimated effort: ~5.5 hours**

---

## Appendix A: API Response Examples

### `GET /api/tasks/paginated?page=1&page_size=10&status=pending&sort_by=priority&sort_dir=desc`

```json
{
  "items": [
    {
      "id": "a1b2c3d4-...",
      "sender_id": "human-ceo",
      "receiver_id": "lead-engineering",
      "instruction": "Build the new API endpoint for task pagination",
      "status": "pending",
      "priority": "critical",
      "created_at": "2026-07-22T10:30:00Z",
      "completed_at": null,
      "result": null
    }
  ],
  "total": 42,
  "page": 1,
  "page_size": 10,
  "total_pages": 5,
  "counts_by_status": {
    "pending": 42,
    "in_progress": 15,
    "completed": 1200,
    "failed": 8,
    "escalated": 3
  }
}
```

## Appendix B: Priority Sort Order

The priority sort uses a numeric mapping:

| Priority | Sort Value | Direction: desc (default) | Direction: asc |
|---|---|---|---|
| critical | 0 | First | Last |
| high | 1 | | |
| medium | 2 | | |
| low | 3 | Last | First |

Ties are broken by `created_at` descending (most recent first).

## Appendix C: Status Sort Order

| Status | Sort Value | Direction: desc | Direction: asc |
|---|---|---|---|
| escalated | 0 | First | Last |
| failed | 1 | | |
| pending | 2 | | |
| in_progress | 3 | | |
| completed | 4 | Last | First |
