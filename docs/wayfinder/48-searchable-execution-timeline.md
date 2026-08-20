# F9: Searchable Execution Timeline

**Issue**: [#48](https://github.com/user/light-speed-holdings/issues/48)
**Status**: Design
**Date**: 2026-08-19

## Goal

Build a searchable, filterable timeline of agent execution events that lets operators answer questions like "What did agent X do with tool Y in the last hour?" in under 200ms.

---

## 1 Indexed Fields

The following fields from `AuditEvent` are indexed for search and filtering:

| Field | Index Type | Rationale |
|-------|-----------|-----------|
| `timestamp` | B-tree (range queries) | Primary timeline ordering; "last N hours" filters |
| `event_type` | B-tree (equality) | Filter by task_completed, error, hitl_approved, etc. |
| `agent_id` | B-tree (equality) | "What did CEO do?" |
| `task_id` | B-tree (equality) | Follow a task's full execution trace |
| `tool` | B-tree (equality) | "All bash calls", "grep usage", etc. |
| `severity` | B-tree (equality) | "Only errors", "warnings and above" |
| `task_id, event_type` | Composite | Task lifecycle queries (created -> completed/failed) |
| `agent_id, event_type` | Composite | Agent-specific event type breakdowns |
| `timestamp, event_type` | Composite | Time-bounded event type histograms |
| `task_id, event_type, severity` | Composite | Task error investigation |
| `task_id, tool, args, result, metadata` | **FTS5** | Full-text search across all event payloads |

**Composite index design**: These cover the top-5 query patterns identified from the dashboard's existing polling behavior (`command-center.js` lines 163-208) and the `AuditStore` query methods.

---

## 2 Storage Schema

### 2.1 Existing Tables (already in `database.py`)

```sql
-- Core audit events table (schema v1)
CREATE TABLE IF NOT EXISTS audit_events (
    event_id        TEXT PRIMARY KEY,
    timestamp       TEXT NOT NULL,
    event_type      TEXT NOT NULL,
    agent_id        TEXT NOT NULL,
    task_id         TEXT NOT NULL DEFAULT '',
    tool            TEXT,
    args            TEXT NOT NULL DEFAULT '{}',
    result          TEXT NOT NULL DEFAULT '{}',
    metadata        TEXT NOT NULL DEFAULT '{}',
    severity        TEXT NOT NULL DEFAULT 'info'
);

-- B-tree indexes (schema v1 + v5)
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_agent ON audit_events(agent_id);
CREATE INDEX IF NOT EXISTS idx_audit_task ON audit_events(task_id);
CREATE INDEX IF NOT EXISTS idx_audit_type ON audit_events(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_severity ON audit_events(severity);
CREATE INDEX IF NOT EXISTS idx_audit_agent_type ON audit_events(agent_id, event_type);
CREATE INDEX IF NOT EXISTS idx_audit_task_type ON audit_events(task_id, event_type);
CREATE INDEX IF NOT EXISTS idx_audit_ts_type ON audit_events(timestamp, event_type);
CREATE INDEX IF NOT EXISTS idx_audit_task_status ON audit_events(task_id, event_type, severity);
```

### 2.2 FTS5 Virtual Table (schema v5, already exists)

```sql
-- Full-text search over event payloads
CREATE VIRTUAL TABLE IF NOT EXISTS audit_events_fts USING fts5(
    task_id, tool, args, result, metadata,
    content='audit_events',
    content_rowid='rowid'
);

-- Triggers keep FTS in sync on INSERT/UPDATE/DELETE
CREATE TRIGGER IF NOT EXISTS audit_events_ai AFTER INSERT ON audit_events BEGIN
    INSERT INTO audit_events_fts(rowid, task_id, tool, args, result, metadata)
    VALUES (new.rowid, new.task_id, new.tool, new.args, new.result, new.metadata);
END;

CREATE TRIGGER IF NOT EXISTS audit_events_ad AFTER DELETE ON audit_events BEGIN
    INSERT INTO audit_events_fts(audit_events_fts, rowid, task_id, tool, args, result, metadata)
    VALUES('delete', old.rowid, old.task_id, old.tool, old.args, old.result, old.metadata);
END;

CREATE TRIGGER IF NOT EXISTS audit_events_au AFTER UPDATE ON audit_events BEGIN
    INSERT INTO audit_events_fts(audit_events_fts, rowid, task_id, tool, args, result, metadata)
    VALUES('delete', old.rowid, old.task_id, old.tool, old.args, old.result, old.metadata);
    INSERT INTO audit_events_fts(rowid, task_id, tool, args, result, metadata)
    VALUES (new.rowid, new.task_id, new.tool, new.args, new.result, new.metadata);
END;
```

### 2.3 Schema Status

All indexes and FTS5 tables already exist in the current schema (v5). No new DDL is needed. The `SearchIndex` class in `data/search.py` already performs FTS5 queries on `audit_events_fts`.

---

## 3 API Design

### 3.1 Search Endpoint

```
GET /api/v1/timeline/search
```

**Query Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | `""` | Full-text search query (FTS5 syntax) |
| `agent_id` | string | `""` | Filter by agent |
| `event_type` | string | `""` | Filter by event type |
| `task_id` | string | `""` | Filter by task |
| `tool` | string | `""` | Filter by tool name |
| `severity` | string | `""` | Filter by severity |
| `from` | string | `""` | ISO 8601 start time |
| `to` | string | `""` | ISO 8601 end time |
| `limit` | int | `50` | Max results (1-200) |
| `cursor` | string | `""` | Pagination cursor (event_id) |

**Response** (200 OK):

```json
{
  "events": [
    {
      "event_id": "uuid",
      "timestamp": "2026-08-19T12:00:00Z",
      "event_type": "tool_call",
      "agent_id": "cto",
      "task_id": "task-abc",
      "tool": "bash",
      "severity": "info",
      "args_summary": "git status",
      "result_summary": "On branch main...",
      "metadata": {}
    }
  ],
  "total_count": 127,
  "cursor": "next-event-id",
  "query_ms": 12
}
```

**Implementation** (`data/audit_store.py` already has `get_timeline()` and `search_events()`):

```python
# Existing pattern from AuditStore.get_timeline()
async def search_events(
    self,
    agent_id: str | None = None,
    event_type: str | None = None,
    task_id: str | None = None,
    from_time: str | None = None,
    to_time: str | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
```

The new endpoint wraps this existing method and adds FTS5 query support from `SearchIndex._search_audit_events()`.

### 3.2 Timeline Endpoint (paginated)

```
GET /api/v1/timeline
```

Returns events in reverse-chronological order with cursor-based pagination. Uses the same parameters as search but defaults to no FTS query.

### 3.3 Task Trace Endpoint

```
GET /api/v1/timeline/task/{task_id}
```

Returns all events for a specific task in chronological order. Useful for following a task's full lifecycle from creation through completion/failure.

### 3.4 Agent Activity Endpoint

```
GET /api/v1/timeline/agent/{agent_id}
```

Returns recent events for a specific agent. Supports `event_type` and `from`/`to` filters.

### 3.5 Stats Endpoint

```
GET /api/v1/timeline/stats
```

Returns aggregated counts by event_type, agent, and severity for a given time range. Used by the timeline chart.

```json
{
  "by_event_type": {"tool_call": 45, "task_completed": 12, "error": 3},
  "by_agent": {"cto": 20, "software-architect": 15},
  "by_severity": {"info": 50, "warning": 5, "error": 3},
  "time_range": {"from": "2026-08-19T00:00:00Z", "to": "2026-08-19T12:00:00Z"}
}
```

---

## 4 UI Design

### 4.1 Component Structure

The timeline lives in a new panel on the command-center page, following the existing Alpine.js patterns from `command-center.js`:

```
command-center.html
  └─ #timeline-panel (Alpine component)
       ├─ Search bar (input + filter chips)
       ├─ Filter bar (dropdowns for agent, event_type, severity, time range)
       ├─ Timeline list (scrollable, infinite-scroll via cursor)
       ├─ Event detail drawer (click to expand)
       └─ Stats chart (Chart.js bar chart, top of panel)
```

### 4.2 Alpine.js Data Shape

```javascript
function timelinePanel() {
  return {
    // Search state
    query: '',
    filters: {
      agent_id: '',
      event_type: '',
      task_id: '',
      tool: '',
      severity: '',
      from: '',
      to: '',
    },

    // Results
    events: [],
    totalCount: 0,
    cursor: '',
    loading: false,
    queryMs: 0,

    // Detail drawer
    selectedEvent: null,
    showDetail: false,

    // Stats
    stats: null,

    // Polling
    _pollTimer: null,

    async init() {
      await this.fetchTimeline();
      this.fetchStats();
      this._pollTimer = setInterval(() => this.fetchTimeline(), 10000);
    },

    async fetchTimeline() {
      this.loading = true;
      const params = new URLSearchParams();
      if (this.query) params.set('q', this.query);
      Object.entries(this.filters).forEach(([k, v]) => {
        if (v) params.set(k, v);
      });
      params.set('limit', '50');
      if (this.cursor) params.set('cursor', this.cursor);

      const res = await fetch(`/api/v1/timeline/search?${params}`);
      const data = await res.json();
      this.events = data.events;
      this.totalCount = data.total_count;
      this.cursor = data.cursor;
      this.queryMs = data.query_ms;
      this.loading = false;
    },

    async loadMore() {
      // Append next page using cursor
      const params = new URLSearchParams(/* same filters */);
      params.set('cursor', this.cursor);
      const res = await fetch(`/api/v1/timeline/search?${params}`);
      const data = await res.json();
      this.events.push(...data.events);
      this.cursor = data.cursor;
    },

    async fetchStats() {
      const res = await fetch('/api/v1/timeline/stats');
      this.stats = await res.json();
    },

    selectEvent(event) {
      this.selectedEvent = event;
      this.showDetail = true;
    },

    clearFilters() {
      this.query = '';
      Object.keys(this.filters).forEach(k => this.filters[k] = '');
      this.fetchTimeline();
    },
  };
}
```

### 4.3 HTML Layout (simplified)

```html
<div x-data="timelinePanel()" class="cc-timeline-panel">
  <!-- Search bar -->
  <div class="flex items-center gap-2 mb-4">
    <input type="text" x-model="query"
           @keydown.enter="fetchTimeline()"
           placeholder="Search events..."
           class="cc-input" />
    <button @click="fetchTimeline()" class="cc-btn">Search</button>
  </div>

  <!-- Filter chips -->
  <div class="flex flex-wrap gap-2 mb-4">
    <select x-model="filters.event_type" @change="fetchTimeline()" class="cc-select">
      <option value="">All types</option>
      <option value="tool_call">Tool Call</option>
      <option value="task_completed">Task Completed</option>
      <option value="error">Error</option>
      <!-- ... -->
    </select>
    <select x-model="filters.severity" @change="fetchTimeline()" class="cc-select">
      <option value="">All severity</option>
      <option value="info">Info</option>
      <option value="warning">Warning</option>
      <option value="error">Error</option>
    </select>
    <!-- agent_id, tool, time range selects -->
  </div>

  <!-- Query stats -->
  <div class="text-xs text-jarvis-muted mb-2">
    <span x-text="totalCount"></span> events
    <span x-show="queryMs > 0">in <span x-text="queryMs"></span>ms</span>
  </div>

  <!-- Event list -->
  <div class="cc-timeline-list overflow-y-auto" style="max-height: 400px">
    <template x-for="event in events" :key="event.event_id">
      <div @click="selectEvent(event)"
           class="cc-timeline-item p-3 border-b border-jarvis-border cursor-pointer hover:bg-jarvis-surface">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full" :class="severityDot(event.severity)"></span>
          <span class="text-xs font-mono text-jarvis-muted" x-text="formatTime(event.timestamp)"></span>
          <span class="text-sm font-medium" x-text="event.event_type"></span>
          <span class="text-xs text-jarvis-muted" x-text="event.agent_id"></span>
        </div>
        <div class="text-xs text-jarvis-muted mt-1" x-text="event.args_summary"></div>
      </div>
    </template>
  </div>

  <!-- Load more -->
  <button x-show="cursor" @click="loadMore()" class="cc-btn-outline mt-2 w-full">
    Load more
  </button>

  <!-- Detail drawer -->
  <div x-show="showDetail" class="cc-detail-drawer p-4 border-t border-jarvis-border">
    <h3 class="font-medium" x-text="selectedEvent?.event_type"></h3>
    <pre class="text-xs mt-2 overflow-x-auto" x-text="JSON.stringify(selectedEvent, null, 2)"></pre>
    <button @click="showDetail = false" class="cc-btn-outline mt-2">Close</button>
  </div>
</div>
```

### 4.4 Stats Chart

Uses Chart.js (already loaded) for a bar chart showing event counts by type over the selected time range:

```javascript
// In timelinePanel stats rendering
renderStatsChart() {
  const ctx = document.getElementById('timeline-stats-chart');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(this.stats.by_event_type),
      datasets: [{
        data: Object.values(this.stats.by_event_type),
        backgroundColor: '#00d4ff', // jarvis-cyan
      }],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, ticks: { color: '#94a3b8' } } },
    },
  });
}
```

---

## 5 Retention Policy

### 5.1 Strategy

Audit events are append-only. Without pruning, the `audit_events` table grows unboundedly. The retention policy balances query performance against storage cost.

| Tier | Retention | Action |
|------|-----------|--------|
| **Hot** (0-7 days) | Full detail | All columns, FTS indexed |
| **Warm** (7-30 days) | Compact | Strip `args`/`result` JSON to summaries; keep indexes |
| **Cold** (30-90 days) | Archive | Move to separate SQLite file; query via federation |
| **Purge** (90+ days) | Delete | Drop rows; vacuum table |

### 5.2 Implementation

The `AuditStore` already has a `prune_old_events()` method. Extend it with tiered compaction:

```python
async def compact_events(self, older_than_days: int = 7) -> int:
    """Compact warm-tier events: strip args/result to summaries."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=older_than_days)).isoformat()
    # Update args/result to stripped versions for events older than cutoff
    count = self._db.execute(
        """UPDATE audit_events
           SET args = json_object('summary', substr(args, 1, 200)),
               result = json_object('summary', substr(result, 1, 200))
           WHERE timestamp < ? AND length(args) > 200""",
        (cutoff,),
    )
    self._db.commit()
    return count
```

### 5.3 Scheduled Runs

The compaction job runs via the existing daemon loop (`orchestrator/daemon.py`) on a daily schedule:

```python
# In daemon loop
if datetime.now().hour == 3:  # 3 AM UTC daily
    await audit_store.compact_events(older_than_days=7)
    await audit_store.archive_events(older_than_days=30)
    await audit_store.prune_old_events(older_than_days=90)
```

### 5.4 Storage Estimates

| Events/day | 7-day hot | 30-day warm | 90-day total |
|-----------|-----------|-------------|--------------|
| 1,000 | 7K rows | 30K rows | 90K rows |
| 10,000 | 70K rows | 300K rows | 900K rows |
| 100,000 | 700K rows | 3M rows | 9M rows |

At ~500 bytes/row average, 100K events/day = ~50MB/day raw. Compacted warm tier reduces to ~100 bytes/row = ~3MB/day. 90-day total at 100K/day = ~5GB with compaction.

---

## 6 WebSocket Integration

### 6.1 Topic: `timeline`

New WebSocket topic for real-time event streaming. Follows the existing `ConnectionManager` pattern from `ws.py`:

```python
# In ws.py ConnectionManager
async def broadcast_timeline_event(self, event: dict[str, Any]) -> None:
    """Push new audit events to timeline subscribers."""
    await self.broadcast("timeline", {
        "type": "timeline_event",
        "data": event,
    })
```

### 6.2 Client Subscription

```javascript
// In timelinePanel init()
async initWebSocket() {
  const ws = new WebSocket(`ws://${window.location.host}/ws`);
  ws.onmessage = (msg) => {
    const data = JSON.parse(msg.data);
    if (data.type === 'timeline_event') {
      // Prepend new event to top of list
      this.events.unshift(data.data);
      this.totalCount++;
    }
  };
  // Subscribe to timeline topic
  ws.send(JSON.stringify({ action: 'subscribe', topic: 'timeline' }));
}
```

### 6.3 Event Hook

The audit writer (`audit/writer.py`) already calls `AuditStore.append()`. Add a post-write hook:

```python
# In AuditStore.append() or AuditWriter
async def _emit_to_websocket(self, event: AuditEvent) -> None:
    """Push event to WebSocket timeline subscribers."""
    from ai_company.dashboard.ws import ws_manager
    await ws_manager.broadcast_timeline_event(event.model_dump())
```

### 6.4 Debouncing

To avoid flooding the WebSocket with rapid sequential events (e.g., a batch of tool calls), debounce at 200ms:

```python
import asyncio

class TimelineDebouncer:
    def __init__(self, delay: float = 0.2):
        self._buffer: list[dict] = []
        self._delay = delay
        self._task: asyncio.Task | None = None

    async def push(self, event: dict) -> None:
        self._buffer.append(event)
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._flush())

    async def _flush(self) -> None:
        await asyncio.sleep(self._delay)
        from ai_company.dashboard.ws import ws_manager
        for event in self._buffer:
            await ws_manager.broadcast_timeline_event(event)
        self._buffer.clear()
```

---

## 7 Performance Notes

- **FTS5 query latency**: <5ms for typical queries on 100K rows (SQLite FTS5 benchmarks)
- **B-tree range scan**: <2ms for timestamp-bounded queries with existing indexes
- **WebSocket push latency**: <50ms from event write to client render
- **Target p95**: All search queries under 200ms
- **Cache**: No caching layer needed; SQLite in-process is already faster than any cache roundtrip

---

## 8 Files to Modify

| File | Change |
|------|--------|
| `src/ai_company/dashboard/api.py` | Add `/timeline` router with search, task-trace, agent-activity, stats endpoints |
| `src/ai_company/dashboard/models.py` | Add `TimelineEvent`, `TimelineStats`, `TimelineResponse` Pydantic models |
| `src/ai_company/dashboard/ws.py` | Add `broadcast_timeline_event()` method, `timeline` topic |
| `src/ai_company/dashboard/static/js/command-center.js` | Add `timelinePanel()` Alpine component |
| `src/ai_company/dashboard/templates/command-center.html` | Add timeline panel HTML |
| `src/ai_company/data/audit_store.py` | Add `compact_events()`, `archive_events()`, WebSocket hook |
| `src/ai_company/audit/writer.py` | Add post-write hook to emit to WebSocket |

---

## 9 Verification

| Check | How |
|-------|-----|
| FTS5 search works | `python -c "from ai_company.data.search import SearchIndex; print(SearchIndex().search('bash'))"` |
| API endpoints respond | `curl http://localhost:8420/api/v1/timeline/search?q=test` |
| WebSocket pushes events | Open browser devtools, connect to `ws://localhost:8420/ws`, subscribe to `timeline` |
| Retention compaction | `python -c "from ai_company.data.audit_store import AuditStore; AuditStore().compact_events()"` |
| Stats aggregation | `curl http://localhost:8420/api/v1/timeline/stats?from=2026-08-01T00:00:00Z` |
