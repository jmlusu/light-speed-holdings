# Dashboard Feature Design Specifications

> **Version**: v0.5.1 Draft
> **Date**: 2026-08-18
> **Author**: Product Designer (Dashboard)
> **Status**: Design decisions — ready for prototype review

---

## Executive Summary

Eight dashboard features designed for the J.A.R.V.I.S. theme, built on the existing stack: FastAPI + Jinja2 + Alpine.js + Tailwind + Chart.js + WebSocket. Each feature is specified with wireframe, data contracts, component patterns, and integration points.

---

## Feature #31: CEO Dashboard Hero

**Status**: Prototype exists (`ceo-hero-prototype.js`), needs integration into index.html
**Priority**: **v0.5.1 — CRITICAL** (default landing page)

### Wireframe Description

The CEO Hero replaces the current KPI card grid as the top section of `/` (index.html). Three switchable variants exist in the prototype; the recommended default is **Variant B (Horizontal Split)**.

```
┌─────────────────────────────────────────────────────────────────────┐
│  ORG HEALTH                                          Variant: B  ◀▶ │
│  ┌──────────────┐  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐            │
│  │              │  │Tasks │ │Agent │ │Cost  │ │Error │            │
│  │   [GAUGE]    │  │ 72%  │ │ 85%  │ │ 68%  │ │ 91%  │            │
│  │   score: 82  │  │sparkl│ │sparkl│ │sparkl│ │sparkl│            │
│  │   band: 🟢   │  └──────┘ └──────┘ └──────┘ └──────┘            │
│  └──────────────┘                                                  │
│                                                                     │
│  ┌─ Recent Alerts ──────────────────────────────────────────────┐  │
│  │ 🔴 2 pending approvals    ⚡ 1 escalation    📋 5 in-progress │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

**Variant A (Gauge Hero)**: Large radial gauge centered, 4 KPI cards below.
**Variant D (Drill-down)**: Click gauge → expands to component breakdown with sub-gauges.

### Data Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/org-health` | GET | Composite score, band, components (exists) |
| `/api/v1/dashboard` | GET | KPI snapshot (exists) |
| `/api/v1/kpis/history/org_health?limit=24` | GET | Trend data for gauge sparkline |
| `/ws/v1/dashboard` | WS | Live org_health_update topic |

**Org Health Response Shape** (already implemented):
```json
{
  "score": 82,
  "band": "green",
  "components": [
    {"name": "task_success_rate", "value": 72.0, "weight": 0.30},
    {"name": "agent_utilization", "value": 85.0, "weight": 0.25},
    {"name": "cost_efficiency", "value": 68.0, "weight": 0.25},
    {"name": "error_rate", "value": 91.0, "weight": 0.20}
  ],
  "collected_at": "2026-01-15T10:30:00Z"
}
```

### Alpine.js Component Pattern

```javascript
// Integrates into existing dashboard() component in app.js
// New data properties:
orgHealth: null,
orgHealthLoading: true,
heroVariant: 'B',  // default
heroExpanded: null,

// New methods:
async loadOrgHealth() { ... },     // GET /api/v1/org-health
setHeroVariant(v) { ... },         // Toggle A/B/D
expandComponent(name) { ... },     // Drill-down toggle
```

**Integration into `app.js`**:
```javascript
// In init(), after loadPageData():
this.loadOrgHealth();

// In the WS message handler, add topic listener:
// Subscribe to 'org_health' topic
```

### Integration Points

1. **`templates/index.html`**: Replace KPI card grid with hero component at top
2. **`app.js`**: Add `orgHealth` state + `loadOrgHealth()` method
3. **`ceo-hero-prototype.js`**: Merge into app.js or load as separate module
4. **`ws.py`**: Already has `broadcast_org_health` — wire into periodic KPI broadcast
5. **`static/css/control-plane-theme.css`**: Add `.hero-gauge` class for the gauge container

### CSS Additions

```css
/* Hero gauge sizing */
.hero-gauge-container { width: 256px; height: 160px; }
.hero-gauge-container-sm { width: 192px; height: 128px; }

/* KPI sparkline cards */
.hero-kpi-card { min-width: 120px; }
.hero-sparkline { height: 32px; }
```

---

## Feature #43: Agent Onboarding Studio

**Status**: Backend service + API exist. No frontend tab yet.
**Priority**: **v0.5.1 — HIGH** (new Onboarding tab)

### Wireframe Description

New navigation tab "Onboarding" between "Approvals" and "Command Center". Shows requests grouped by state with real-time status.

```
┌─────────────────────────────────────────────────────────────────────┐
│  Agent Onboarding Studio                                           │
│                                                                     │
│  ┌─ Filters ───────────────────────────────────────────────────┐   │
│  │ [All] [Pending] [Generating] [Testing] [Active] [Archived]  │   │
│  │ Agent: [__________] Department: [All ▼]                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─ Pending Approval (2) ──────────────────────────────────────┐  │
│  │ ┌─────────────────────────────────────────────────────────┐  │  │
│  │ │ 🔵 financial-analyst              finance    Tier 2     │  │  │
│  │ │    Tools: read, edit, grep         Created: 2m ago      │  │  │
│  │ │    [Approve] [Reject]              Expires: 58m         │  │  │
│  │ └─────────────────────────────────────────────────────────┘  │  │
│  │ ┌─────────────────────────────────────────────────────────┐  │  │
│  │ │ 🔵 security-auditor               legal      Tier 3     │  │  │
│  │ │    Tools: read, grep, bash         Created: 15m ago     │  │  │
│  │ │    [Approve] [Reject]              Expires: 45m         │  │  │
│  │ └─────────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─ Generating (1) ────────────────────────────────────────────┐  │
│  │ ┌─────────────────────────────────────────────────────────┐  │  │
│  │ │ 🟡 content-writer                 marketing  Tier 1     │  │  │
│  │ │    Step 2/4: Generating agent card                     │  │  │
│  │ │    [████████░░░░░░░░░░] 50%                            │  │  │
│  │ └─────────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─ Active (5) ────────────────────────────────────────────────┐  │
│  │ compact list with agent name + activation date              │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/onboarding` | GET | List all requests (exists) |
| `/api/v1/onboarding?state=pending_approval` | GET | Filtered by state (exists) |
| `/api/v1/onboarding/{request_id}` | GET | Single request detail (exists) |
| `/ws/v1/dashboard?topics=onboarding` | WS | Real-time lifecycle events |

**Onboarding Request Shape** (from OnboardingService):
```json
{
  "id": "req_abc123",
  "agent_id": "financial-analyst",
  "role": "Financial Analyst",
  "department": "finance",
  "tools": ["read", "edit", "grep"],
  "state": "pending_approval",
  "approval_request_id": "apr_xyz",
  "created_at": "2026-01-15T10:00:00Z",
  "updated_at": "2026-01-15T10:02:00Z"
}
```

### Alpine.js Component Pattern

```javascript
// New top-level function for onboarding page
function onboardingStudio() {
  return {
    requests: [],
    loading: true,
    stateFilter: '',
    agentFilter: '',
    deptFilter: '',
    expandedRequest: null,

    get filteredRequests() {
      return this.requests.filter(r => {
        if (this.stateFilter && r.state !== this.stateFilter) return false;
        if (this.agentFilter && !r.agent_id.includes(this.agentFilter)) return false;
        return true;
      });
    },

    get groupedByState() {
      const groups = {};
      for (const r of this.filteredRequests) {
        (groups[r.state] = groups[r.state] || []).push(r);
      }
      return groups;
    },

    async loadRequests() { ... },
    async approveRequest(id) { ... },
    async rejectRequest(id) { ... },
    connectOnboardingWS() {
      // Subscribe to 'onboarding' topic
      // Handle onboarding_update events
    },
  }
}
```

### Integration Points

1. **`app.py`**: Add page route `GET /onboarding` + tab context entry
2. **`templates/onboarding.html`**: New template extending base.html
3. **`app.js`**: Add `onboardingStudio()` function or separate JS file
4. **`static/js/onboarding.js`**: Component logic + WS subscription
5. **OnboardingService**: Already broadcasts via `broadcast_onboarding_update`
6. **Approval integration**: Approve/reject buttons call existing `/api/v1/approvals/{id}/approve|reject`

### Tab Navigation Addition

```python
# In _tab_context() in app.py:
{
    "id": "onboarding",
    "label": "Onboarding",
    "href": "/onboarding",
    "icon": '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">...</svg>',
},
```

---

## Feature #44: Kanban + Task Decomposition UX

**Status**: Kanban board exists in tasks.html. Drag-and-drop implemented. Missing: task decomposition view.
**Priority**: **v0.5.1 — MEDIUM** (enhance existing)

### Wireframe Description

Enhance existing Kanban with:
1. Click task card → slide-out detail panel with decomposition
2. "Decompose" button on high-priority tasks → breaks into subtasks
3. Visual dependency lines between parent/child tasks

```
Existing Kanban (already implemented):
┌──────────┐  ┌──────────────┐  ┌───────────┐
│ Pending  │  │ In Progress  │  │ Completed │
│ ┌──────┐ │  │ ┌──────────┐ │  │ ┌───────┐ │
│ │task 1│◄┼──┼─┤task 3    │ │  │ │task 5 │ │
│ │      │ │  │ │          │ │  │ │       │ │
│ └──────┘ │  │ └──────────┘ │  │ └───────┘ │
│ ┌──────┐ │  │              │  │           │
│ │task 2│ │  │              │  │           │
│ └──────┘ │  │              │  │           │
└──────────┘  └──────────────┘  └───────────┘

NEW — Task Detail Slide-out Panel:
┌──────────────────────────────────────────┐
│ Task: abc123                   [×]      │
│ ─────────────────────────────────────── │
│ Instruction: Analyze Q4 financial data  │
│ Assigned to: financial-analyst          │
│ Priority: high   Status: in_progress    │
│ Created: 2h ago                         │
│                                          │
│ ── Decomposition ─────────────────────  │
│ Parent task breaks into:                 │
│  ┌─────────────────────────────────┐   │
│  │ 1. Pull Q4 revenue data        │ ✓  │
│  │ 2. Calculate margins           │ ◉  │
│  │ 3. Generate summary report     │ ○  │
│  │ 4. Send to CEO for review      │ ○  │
│  └─────────────────────────────────┘   │
│                                          │
│ [Decompose] [Reassign] [Escalate]      │
└──────────────────────────────────────────┘
```

### Data Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/tasks/paginated` | GET | Kanban data (exists) |
| `/api/v1/tasks/{task_id}` | GET | Task detail (NEW) |
| `/api/v1/tasks/{task_id}/decompose` | POST | AI decomposition (NEW) |
| `/api/v1/tasks/{task_id}/subtasks` | GET | Child tasks (NEW) |
| `PATCH /api/v1/tasks/{task_id}` | PATCH | Status update (exists) |

**Task Decomposition Response** (NEW):
```json
{
  "parent_id": "abc123",
  "subtasks": [
    {"id": "sub_1", "instruction": "Pull Q4 revenue data", "status": "completed"},
    {"id": "sub_2", "instruction": "Calculate margins", "status": "in_progress"},
    {"id": "sub_3", "instruction": "Generate summary report", "status": "pending"},
    {"id": "sub_4", "instruction": "Send to CEO for review", "status": "pending"}
  ],
  "progress_pct": 37.5
}
```

### Alpine.js Component Pattern

```javascript
// Additions to existing dashboard() in app.js:

// New state:
selectedTask: null,
taskDetailOpen: false,
taskDecomposition: null,
taskDecomposing: false,

// New methods:
async openTaskDetail(task) {
  this.selectedTask = task;
  this.taskDetailOpen = true;
  this.taskDecomposition = null;
  // Fetch decomposition if available
},
async decomposeTask(taskId) {
  this.taskDecomposing = true;
  // POST /api/v1/tasks/{taskId}/decompose
},
async closeTaskDetail() {
  this.taskDetailOpen = false;
  this.selectedTask = null;
},
```

### Integration Points

1. **`templates/tasks.html`**: Add slide-out panel markup + decompose button
2. **`app.js`**: Add task detail state + decomposition methods
3. **`api.py`**: Add 3 new endpoints (detail, decompose, subtasks)
4. **`models.py`**: Add `TaskDecomposition` response model
5. **Task card**: Add `@click="openTaskDetail(task)"` to existing cards
6. **Executor**: Hook decomposition into AgentLoop for AI-powered breakdown

---

## Feature #45: Health and Anomaly Monitor

**Status**: OrgHealth scoring exists. No real-time anomaly view.
**Priority**: **v0.5.1 — HIGH** (new Health tab or section in KPIs)

### Wireframe Description

Integrated into the KPIs tab as a "Health Monitor" section, or standalone page. Real-time metrics with anomaly detection alerts.

```
┌─────────────────────────────────────────────────────────────────────┐
│  System Health Monitor                    Auto-refresh: 10s  🔄   │
│                                                                     │
│  ┌─ Live Metrics ──────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  Task Success    Agent Util    Cost Eff.    Error Rate     │   │
│  │  ┌─────┐        ┌─────┐      ┌─────┐      ┌─────┐         │   │
│  │  │ 72% │ ▲+3   │ 85% │ ▼-2  │ 68% │ ─    │ 91% │ ▲+1     │   │
│  │  │spark│        │spark│      │spark│      │spark│         │   │
│  │  └─────┘        └─────┘      └─────┘      └─────┘         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─ Anomaly Detection ────────────────────────────────────────┐   │
│  │  ⚠️  2026-01-15 10:32  Error rate spike: 15% → 22% (+47%) │   │
│  │  📊  2026-01-15 10:28  Agent utilization drop: 85% → 72%  │   │
│  │  ✅  2026-01-15 10:20  Cost efficiency normalized           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─ Trend Chart (24h) ────────────────────────────────────────┐   │
│  │  [Line chart: org-health score over time]                   │   │
│  │  ───────────●────●────●────●────●────●────●────────        │   │
│  │       ●──────●────●────●────●────●────●────●               │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/org-health` | GET | Current composite score (exists) |
| `/api/v1/org-health/trend` | GET | Historical scores (NEW) |
| `/api/v1/org-health/anomalies` | GET | Detected anomalies (NEW) |
| `/api/v1/kpis/history/{dept}` | GET | Per-department trends (exists) |
| `/ws/v1/dashboard?topics=org_health` | WS | Real-time score updates |

**Anomaly Detection Model** (NEW — server-side):
```python
class Anomaly(BaseModel):
    timestamp: str
    component: str          # "task_success_rate" | "agent_utilization" | etc.
    previous_value: float
    current_value: float
    change_pct: float       # percent change
    severity: str           # "info" | "warning" | "critical"
    message: str
```

### Alpine.js Component Pattern

```javascript
// healthMonitor() — standalone or integrated into dashboard()
function healthMonitor() {
  return {
    orgHealth: null,
    trend: [],
    anomalies: [],
    loading: true,
    autoRefresh: true,
    _refreshTimer: null,

    async loadHealth() { ... },
    async loadTrend() { ... },
    async loadAnomalies() { ... },

    get changeFromPrevious() {
      // Calculate delta from previous score
    },

    connectHealthWS() {
      // Subscribe to 'org_health' topic
      // Handle org_health_update events
    },
  }
}
```

### Integration Points

1. **`api.py`**: Add `/org-health/trend` and `/org-health/anomalies` endpoints
2. **`org_health.py`**: Add `compute_trend()` and `detect_anomalies()` methods
3. **`templates/kpis.html`**: Add health monitor section at top
4. **`static/js/health.js`**: Standalone component or extend app.js
5. **`ws.py`**: Wire periodic org-health broadcast (every 60s)
6. **Anomaly logic**: Z-score or moving average deviation detection on component scores

---

## Feature #46: Revenue Attribution Model

**Status**: Cost tracking exists in `/api/v1/costs`. No revenue attribution.
**Priority**: **v0.5.2 — DEFERRED** (requires revenue data model)

### Wireframe Description

New "Finance" tab (exists) enhanced with revenue attribution. Shows revenue per agent/department with ROI calculations.

```
┌─────────────────────────────────────────────────────────────────────┐
│  Revenue Attribution                                               │
│                                                                     │
│  ┌─ Summary Cards ────────────────────────────────────────────┐   │
│  │  Total Revenue    Total Cost     ROI        Tasks/Revenue │   │
│  │  $12,450          $3,200         3.9x       $1.24/task    │   │
│  │  ▲+8.2%           ▼-2.1%        ▲+0.3x                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─ By Department ────────────────────────────────────────────┐   │
│  │  [Horizontal bar chart]                                     │   │
│  │  Engineering  ████████████████████  $5,200  (42%)          │   │
│  │  Sales        ██████████████        $3,800  (31%)          │   │
│  │  Marketing    ████████              $2,100  (17%)          │   │
│  │  Finance      ████                  $1,350  (10%)          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─ Cost vs Revenue per Agent ───────────────────────────────┐   │
│  │  [Scatter plot: cost (x) vs revenue (y), bubble = tasks]   │   │
│  │                                                             │   │
│  │  financial-analyst     $120 cost   $800 revenue   ROI 6.7x │   │
│  │  senior-developer      $450 cost   $1,200 revenue ROI 2.7x │   │
│  │  content-writer        $80 cost    $300 revenue   ROI 3.8x │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/costs` | GET | Cost summary (exists) |
| `/api/v1/revenue/attribution` | GET | Revenue by agent/dept (NEW) |
| `/api/v1/revenue/roi` | GET | ROI calculations (NEW) |
| `/api/v1/revenue/trend` | GET | Revenue over time (NEW) |

**Revenue Attribution Model** (NEW):
```python
class RevenueAttribution(BaseModel):
    agent_id: str
    department: str
    tasks_completed: int
    revenue_attributed: float      # USD
    cost_incurred: float           # USD (LLM cost)
    roi: float                     # revenue / cost
    revenue_per_task: float

class RevenueSummary(BaseModel):
    total_revenue: float
    total_cost: float
    overall_roi: float
    by_department: list[RevenueAttribution]
    by_agent: list[RevenueAttribution]
    period_days: int
```

### Integration Points

1. **`api.py`**: Add revenue attribution endpoints
2. **`templates/finance.html`**: Replace stub with revenue dashboard
3. **Revenue data model**: Requires defining how revenue maps to tasks (manual input, task value, or external data source)
4. **Cost tracking**: Extend `_per_agent_costs_from_audit()` to pair with revenue
5. **Charts**: Chart.js horizontal bar (departments) + bubble chart (agent scatter)

---

## Feature #47: Interactive Org Chart

**Status**: Org chart API exists at `/api/v1/org-chart`. No visual renderer.
**Priority**: **v0.5.1 — HIGH** (new Org Chart tab or section in Agents)

### Wireframe Description

Visual tree rendering of the agent hierarchy. Click nodes for details, drag to reassign `reports_to`.

```
┌─────────────────────────────────────────────────────────────────────┐
│  Org Chart                          [Zoom: 100%] [Fit] [Reset]    │
│                                                                     │
│                    ┌──────────────┐                                │
│                    │  human-ceo   │                                │
│                    │  CEO         │                                │
│                    └──────┬───────┘                                │
│               ┌───────────┼───────────┐                            │
│               │           │           │                            │
│        ┌──────▼──────┐ ┌──▼───────┐ ┌─▼──────────┐               │
│        │ cto         │ │ cfo      │ │ coo        │               │
│        │ Technology  │ │ Finance  │ │ Operations │               │
│        └──────┬──────┘ └──┬───────┘ └─┬──────────┘               │
│          ┌────┼────┐      │       ┌───┼────┐                       │
│          │    │    │      │       │   │    │                       │
│       ┌──▼┐ ┌▼──┐ ┌▼──┐ ┌▼──┐ ┌─▼┐ ┌▼──┐ ┌▼──┐               │
│       │eng│ │eng│ │eng│ │fin│ │hr│ │ops│ │ops│               │
│       └───┘ └───┘ └───┘ └───┘ └──┘ └───┘ └───┘               │
│                                                                     │
│  ┌─ Selected: cto ────────────────────────────────────────────┐   │
│  │  Role: Chief Technology Officer                             │   │
│  │  Type: Executive   Department: engineering                  │   │
│  │  Reports to: human-ceo                                      │   │
│  │  Direct reports: 3 agents                                   │   │
│  │  Tasks completed: 42   Completion rate: 92%                 │   │
│  │  [View Details] [Reassign Reports]                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/org-chart` | GET | Hierarchical org data (exists) |
| `/api/v1/org-chart/flat` | GET | Flat list with positions (NEW) |
| `PATCH /api/v1/agents/{name}/reports-to` | PATCH | Reassign manager (NEW) |

**Org Chart Response** (already exists):
```json
[
  {
    "name": "cto",
    "role": "Chief Technology Officer",
    "type": "Executive",
    "department": "engineering",
    "children": [
      {"name": "senior-developer", "role": "...", "children": []}
    ]
  }
]
```

### Alpine.js Component Pattern

```javascript
// orgChart() — new component for org chart page
function orgChart() {
  return {
    tree: [],
    flatAgents: [],
    selectedNode: null,
    zoom: 100,
    loading: true,

    async loadOrgChart() {
      const res = await fetch('/api/v1/org-chart');
      this.tree = await res.json();
    },

    selectNode(node) {
      this.selectedNode = node;
    },

    async reassignReportsTo(agentName, newManager) {
      // PATCH /api/v1/agents/{agentName}/reports-to
    },

    fitToView() { ... },
    resetZoom() { ... },
  }
}
```

### Integration Points

1. **`api.py`**: Add `/org-chart/flat` endpoint and `PATCH /agents/{name}/reports-to`
2. **`templates/org-chart.html`**: New template (or section in agents.html)
3. **Rendering**: Use CSS flexbox/grid for tree layout (no D3 dependency), or lightweight SVG
4. **`app.py`**: Add page route + tab context
5. **Agent detail modal**: Reuse existing modal from agents.html
6. **Drag-and-drop**: HTML5 drag API for reassigning `reports_to`

### Tree Rendering Strategy

Pure CSS approach (no external libs):
```css
.org-tree { display: flex; flex-direction: column; align-items: center; }
.org-tree-children { display: flex; gap: 1rem; }
.org-tree-node { position: relative; }
.org-tree-connector { /* vertical/horizontal lines via ::before/::after */ }
```

---

## Feature #48: Searchable Execution Timeline

**Status**: Audit trail exists in JSONL format. No timeline UI.
**Priority**: **v0.5.2 — DEFERRED** (requires audit query optimization)

### Wireframe Description

Timeline view of all agent executions with search and filter. Drill-down into execution details.

```
┌─────────────────────────────────────────────────────────────────────┐
│  Execution Timeline                                                │
│                                                                     │
│  ┌─ Search & Filter ──────────────────────────────────────────┐   │
│  │ 🔍 [Search executions...           ]                       │   │
│  │ Agent: [All ▼] Status: [All ▼] Tool: [All ▼]              │   │
│  │ Time: [Last 24h ▼] Sort: [Newest ▼]                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─ Timeline ─────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  10:32:15 ─●── financial-analyst ── completed ── 4.2s     │   │
│  │            │  Task: Analyze Q4 financial data              │   │
│  │            │  Cost: $0.12  Tokens: 2,340                   │   │
│  │                                                             │   │
│  │  10:31:42 ─●── senior-developer ── failed ──── 12.8s      │   │
│  │            │  Task: Deploy microservice                    │   │
│  │            │  Error: Connection timeout                    │   │
│  │            │  [View Details] [Retry]                       │   │
│  │                                                             │   │
│  │  10:30:01 ─●── content-writer ─── completed ── 2.1s       │   │
│  │            │  Task: Generate blog post                     │   │
│  │            │  Cost: $0.03  Tokens: 890                     │   │
│  │                                                             │   │
│  │  10:28:55 ─●── hr-assistant ──── in_progress ── 8.3s     │   │
│  │            │  Task: Screen resumes                         │   │
│  │            │  [Running...]                                 │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─ Execution Detail (slide-out) ─────────────────────────────┐   │
│  │  Task: abc123                                               │   │
│  │  Agent: financial-analyst                                   │   │
│  │  Duration: 4.2s   Cost: $0.12                              │   │
│  │                                                             │   │
│  │  ── Tool Calls ──                                          │   │
│  │  1. read("data/q4_revenue.csv") — 0.8s                    │   │
│  │  2. grep("margin", "*.csv") — 1.2s                        │   │
│  │  3. edit("report.md", ...) — 2.1s                         │   │
│  │                                                             │   │
│  │  ── LLM Calls ──                                          │   │
│  │  1. gemini-2.5-flash — 1,200 tokens in / 890 out          │   │
│  │  2. gemini-2.5-flash — 1,140 tokens in / 450 out          │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/audit/timeline` | GET | Paginated timeline (NEW) |
| `/api/v1/audit/timeline?agent=X&status=Y` | GET | Filtered (NEW) |
| `/api/v1/audit/execution/{task_id}` | GET | Execution detail (NEW) |
| `/api/v1/audit/search?q=...` | GET | Full-text search (NEW) |

**Timeline Response** (NEW):
```python
class TimelineEntry(BaseModel):
    task_id: str
    agent_id: str
    instruction: str
    status: str                    # completed | failed | in_progress
    started_at: str
    completed_at: str | None
    duration_seconds: float
    cost_usd: float
    prompt_tokens: int
    completion_tokens: int
    tool_calls: list[ToolCallSummary]
    error: str | None

class ToolCallSummary(BaseModel):
    tool: str
    duration_seconds: float
    success: bool
```

### Alpine.js Component Pattern

```javascript
function executionTimeline() {
  return {
    entries: [],
    loading: true,
    search: '',
    agentFilter: '',
    statusFilter: '',
    toolFilter: '',
    timeRange: '24h',
    selectedEntry: null,
    detailOpen: false,

    async loadTimeline() { ... },
    async loadExecutionDetail(taskId) { ... },
    async searchExecutions() { ... },

    get filteredEntries() { ... },
  }
}
```

### Integration Points

1. **`api.py`**: Add audit timeline/search endpoints
2. **`audit/reader.py`**: Extend `AuditReader` with timeline query methods
3. **`templates/timeline.html`**: New template
4. **`static/js/timeline.js`**: Component logic
5. **SQLite optimization**: Add indexes on `timestamp`, `agent_id`, `event_type` in audit table
6. **Search**: Use SQLite FTS5 for full-text search on instruction field

---

## Feature #50: Command Bar & Voice Scope

**Status**: No existing implementation.
**Priority**: **v0.5.2 — DEFERRED** (polish feature)

### Wireframe Description

Global Cmd+K (Ctrl+K) command palette overlay. Fuzzy search across all entities. Optional voice input.

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ┌─ Command Bar ──────────────────────────────────────────────┐   │
│  │ 🔍 Type a command or search...              🎤 Voice       │   │
│  │                                                             │   │
│  │  ── Quick Actions ──                                      │   │
│  │  ⚡  Assign Task                    → /tasks?action=assign │   │
│  │  📊  View KPIs                      → /kpis                │   │
│  │  👥  View Agents                    → /agents              │   │
│  │  🔔  View Approvals                 → /escalations         │   │
│  │                                                             │   │
│  │  ── Search Results ──                                     │   │
│  │  🤖  financial-analyst               Agent                  │   │
│  │  📋  abc123 — Analyze Q4 data        Task (in_progress)    │   │
│  │  📊  engineering dept KPIs           Department              │   │
│  │                                                             │   │
│  │  ── Recent ──                                             │   │
│  │  📋  def456 — Deploy microservice    Task (failed)          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/search` | GET | Global search across entities (NEW) |
| `/api/v1/commands` | GET | Available quick commands (NEW) |

**Search Response** (NEW):
```python
class SearchResult(BaseModel):
    type: str           # "agent" | "task" | "kpi" | "department"
    id: str
    title: str
    subtitle: str
    url: str
    icon: str

class SearchResponse(BaseModel):
    results: list[SearchResult]
    actions: list[SearchResult]   # quick commands
    recent: list[SearchResult]    # recently accessed
```

### Alpine.js Component Pattern

```javascript
// Integrated into base.html as a global overlay
function commandBar() {
  return {
    open: false,
    query: '',
    results: [],
    actions: [],
    recent: [],
    selectedIndex: 0,
    voiceActive: false,

    init() {
      // Global keyboard shortcut: Cmd+K / Ctrl+K
      document.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
          e.preventDefault();
          this.toggle();
        }
        if (e.key === 'Escape') this.close();
      });
    },

    toggle() { this.open = !this.open; if (this.open) this.$nextTick(() => this.$refs.searchInput.focus()); },
    close() { this.open = false; this.query = ''; },

    async search() {
      if (!this.query) { this.results = []; return; }
      const res = await fetch(`/api/v1/search?q=${encodeURIComponent(this.query)}`);
      const data = await res.json();
      this.results = data.results;
      this.actions = data.actions;
    },

    navigate(url) { window.location.href = url; },

    // Voice input via Web Speech API
    startVoice() {
      const recognition = new webkitSpeechRecognition();
      recognition.onresult = (e) => { this.query = e.results[0][0].transcript; this.search(); };
      recognition.start();
      this.voiceActive = true;
    },
  }
}
```

### Integration Points

1. **`base.html`**: Add command bar overlay markup (global, all pages)
2. **`static/js/command-bar.js`**: Component logic
3. **`api.py`**: Add `/search` and `/commands` endpoints
4. **Search index**: Build from agents + tasks + departments + KPIs
5. **Web Speech API**: Browser-native voice recognition (no backend needed)
6. **Keyboard navigation**: Arrow keys + Enter for result selection

---

## Priority Summary

| Feature | Version | Priority | Effort | Dependencies |
|---------|---------|----------|--------|-------------|
| #31 CEO Hero | v0.5.1 | CRITICAL | 1-2 days | Already prototyped |
| #43 Onboarding Studio | v0.5.1 | HIGH | 2-3 days | Backend exists |
| #44 Kanban Decomposition | v0.5.1 | MEDIUM | 2-3 days | Extend existing |
| #45 Health Monitor | v0.5.1 | HIGH | 2-3 days | OrgHealth exists |
| #47 Interactive Org Chart | v0.5.1 | HIGH | 3-4 days | API exists |
| #46 Revenue Attribution | v0.5.2 | DEFERRED | 4-5 days | Needs revenue model |
| #48 Execution Timeline | v0.5.2 | DEFERRED | 3-4 days | Audit query opt |
| #50 Command Bar | v0.5.2 | DEFERRED | 2-3 days | Search index |

---

## Implementation Order for v0.5.1

1. **CEO Hero (#31)** — Integrate existing prototype into index.html
2. **Org Chart (#47)** — New tab + visual tree renderer
3. **Onboarding Studio (#43)** — New tab + request management
4. **Health Monitor (#45)** — Extend KPIs tab with real-time health
5. **Kanban Decomposition (#44)** — Enhance existing tasks page

---

## Design System Notes

All new features use existing J.A.R.V.I.S. theme tokens:
- **Colors**: `jarvis-cyan`, `jarvis-amber`, `jarvis-red`, `jarvis-success`
- **Glass**: `.jarvis-glass` panels with blur + border glow
- **Typography**: `font-display` (Rajdhani) for headings, `font-mono` (JetBrains) for data
- **Animations**: Respect `prefers-reduced-motion`, use `jarvis-pulse-*` classes
- **Spacing**: `gap-4` grid, `p-4`/`p-5` panels, `text-sm` body text

No new CSS frameworks or JS libraries. All charts via Chart.js, all interactivity via Alpine.js.
