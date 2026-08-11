# Dashboard UX Design

> Information architecture, navigation, key user flows, and wireframes for the CEO Dashboard.

---

## 1. Design Principles

| Principle | Description |
|-----------|-------------|
| **Glanceable** | The most critical numbers are visible in < 3 seconds |
| **Progressive disclosure** | Summary first, details on demand |
| **Action-oriented** | Every data point connects to a next action |
| **Real-time** | WebSocket-powered live updates; never stale |
| **Role-adaptive** | Different views for CEO, Manager, Operator, Developer |

---

## 2. Information Architecture

```
CEO Dashboard
|
+-- Dashboard (Home)
|   +-- KPI Cards (5 primary metrics)
|   +-- Task Status Bars (horizontal bar chart)
|   +-- Department Load (agent count per dept)
|   +-- Recent Tasks (last 8, table)
|
+-- Org Chart
|   +-- Hierarchical tree view
|   +-- Agent detail modal (click any node)
|
+-- Tasks
|   +-- Assign new task (form)
|   +-- Task list (filterable by status)
|   +-- Task detail (click row)
|
+-- Approvals & Escalations
|   +-- Pending approvals (approve/reject)
|   +-- Open escalations (resolve)
|
+-- Models
|   +-- Model tier overview (3 cards)
|   +-- Per-agent routing table
|
+-- Departments (Phase 3)
|   +-- Department selector
|   +-- Department KPIs
|   +-- Department agents
|   +-- Department budget
|
+-- Memory (Phase 3)
|   +-- Memory entries
|   +-- Search
|   +-- Consolidation status
```

---

## 3. Navigation Structure

### Primary Navigation (Top Tab Bar)

| Tab | Icon | Badge | Description |
|-----|------|-------|-------------|
| Dashboard | Home | — | KPI summary, charts, recent tasks |
| Org Chart | Tree | — | Agent hierarchy visualization |
| Tasks | List | `pending_tasks` count | Task queue management |
| Approvals | Shield | `pending_approvals` count | Approval queue + escalations |
| Models | Cpu | — | Model routing and tier info |
| Departments | Building | — | Per-department KPIs and agents |

### Navigation Rules

1. **Badges update in real-time** via WebSocket
2. **Active tab** indicated by brand-colored bottom border
3. **Keyboard navigation**: `1`-`6` to switch tabs, `Tab`/`Shift+Tab` within
4. **URL hash sync**: `#dashboard`, `#org`, `#tasks`, `#approvals`, `#models`, `#departments`

---

## 4. Key User Flows

### Flow 1: CEO Checking Company Health

```
1. CEO opens dashboard
   |
2. Sees Dashboard tab (default)
   |-- 5 KPI cards: Pending | Completed | Escalations | Approvals | Agents
   |-- Color-coded: green (good), amber (attention), red (urgent)
   |
3. Glances at task status bars
   |-- Horizontal bars: pending, in_progress, completed, failed, escalated
   |-- Proportional width shows relative volume
   |
4. Checks escalation count (red badge if > 0)
   |-- Clicks "Approvals" tab
   |-- Reviews escalation cards
   |-- Clicks "Resolve" on handled items
   |
5. Checks department load
   |-- Sees which departments are busiest
   |-- Clicks "Departments" tab for details (Phase 3)
   |
6. Done in < 2 minutes
```

**Decision points:**
- Escalations > 0 → Go to Approvals tab
- Any department > 80% load → Investigate
- Failed tasks > 0 → Check task detail

---

### Flow 2: Manager Reviewing Department KPIs

```
1. Manager opens dashboard
   |
2. Navigates to "Departments" tab (Phase 3)
   |
3. Selects department from dropdown
   |
4. Sees department KPIs:
   +----------------------------------+
   | Engineering KPIs                 |
   |----------------------------------|
   | Deployment Frequency  8/10/week  |
   | Cycle Time            1.5 days   |
   | Bug Escape Rate       2%         |
   +----------------------------------+
   |
5. Compares to targets (green = on track, red = below)
   |
6. Views department agents
   |-- Sees who's assigned
   |-- Checks their task load
```

---

### Flow 3: Operator Handling Escalations

```
1. Operator sees badge on "Approvals" tab
   |
2. Clicks to view
   |-- Pending Approvals section
   |-- Open Escalations section
   |
3. For each approval card:
   |-- Reviews agent, action, description
   |-- Reviews risk score (visual bar)
   |-- Reviews time remaining
   |
4. Decision:
   +-- Approve → Click "Approve" → Add notes (optional) → Confirm
   +-- Reject → Click "Reject" → Add reason → Confirm
   |
5. For escalations:
   |-- Reviews escalation rule and reason
   |-- Clicks "Resolve" when handled
   |
6. Dashboard updates in real-time (WebSocket)
```

---

### Flow 4: Developer Monitoring Agent Performance

```
1. Developer opens dashboard
   |
2. Clicks "Models" tab
   |-- Sees 3 tier cards: Fast | Standard | Premium
   |-- Each shows provider + model
   |
3. Reviews per-agent routing table
   |-- Agent name, provider, model, tier, reason
   |-- Identifies any overrides
   |
4. Clicks "Org Chart" tab
   |-- Explores agent hierarchy
   |-- Clicks agent to see details
   |-- Reviews model override if set
   |
5. Cross-references with task queue
   |-- Filters tasks by agent
   |-- Checks for failures or escalations
```

---

## 5. Wireframes (Text-Based)

### 5.1 Dashboard Tab (Home)

```
+------------------------------------------------------------------+
|  [LS] Light Speed Holdings    CEO Dashboard          Uptime: 2h  |
|                                              [Live]              |
+------------------------------------------------------------------+
| Dashboard | Org Chart | Tasks | Approvals | Models | Departments |
+------------------------------------------------------------------+
|                                                                    |
|  +----------+ +----------+ +----------+ +----------+ +----------+ |
|  | Pending  | |Completed | |Escalations| |Approvals | |  Agents  | |
|  |    12    | |    45    | |     3    | |     2    | |    27    | |
|  | (amber)  | | (green)  | |  (red)   | | (purple) | |  (blue)  | |
|  +----------+ +----------+ +----------+ +----------+ +----------+ |
|                                                                    |
|  +------------------------------+ +------------------------------+ |
|  | Tasks by Status              | | Department Load              | |
|  |                              | |                              | |
|  | Pending    [======    ] 12  | | Engineering  [========  ] 8  | |
|  | In Progress[==        ]  4  | | Marketing    [====      ] 4  | |
|  | Completed  [==========] 45  | | Sales        [======    ] 6  | |
|  | Failed     [          ]  0  | | Finance      [====      ] 4  | |
|  | Escalated  [=         ]  3  | | HR           [==        ] 2  | |
|  +------------------------------+ +------------------------------+ |
|                                                                    |
|  +--------------------------------------------------------------+ |
|  | Recent Tasks                                                  | |
|  | +----+------+----------------------+--------+--------+       | |
|  | | ID | From | Instruction          |Priority| Status |       | |
|  | +----+------+----------------------+--------+--------+       | |
|  | | a3 | cto  | Review PR #42        | high   |pending |       | |
|  | | b7 | cfo  | Budget report Q3     | med    |in_prog |       | |
|  | | c1 | cmo  | Draft blog post      | low    |done    |       | |
|  | +----+------+----------------------+--------+--------+       | |
|  +--------------------------------------------------------------+ |
+------------------------------------------------------------------+
```

### 5.2 Org Chart Tab

```
+------------------------------------------------------------------+
| Dashboard | Org Chart | Tasks | Approvals | Models | Departments |
+------------------------------------------------------------------+
|                                                                    |
|  Company Hierarchy                                                 |
|  +--------------------------------------------------------------+ |
|  |                                                              | |
|  |  chief-of-staff                                              | |
|  |  |-- cto                                                     | |
|  |  |   |-- lead-engineer                                       | |
|  |  |   |   |-- backend-engineer                                | |
|  |  |   |   |-- frontend-engineer                               | |
|  |  |   |-- lead-data-scientist                                 | |
|  |  |-- cfo                                                     | |
|  |  |   |-- financial-analyst                                   | |
|  |  |-- coo                                                     | |
|  |  |   |-- operations-manager                                  | |
|  |  |-- cmo                                                     | |
|  |  |   |-- content-writer                                      | |
|  |  |   |-- growth-marketer                                     | |
|  |  |-- chro                                                    | |
|  |  |   |-- hr-coordinator                                      | |
|  |  |-- general-counsel                                         | |
|  |      |-- legal-analyst                                       | |
|  +--------------------------------------------------------------+ |
|                                                                    |
|  [Click any agent to see details]                                 |
+------------------------------------------------------------------+

Agent Detail Modal (overlay):
+------------------------------------------+
|  Lead Engineer                    [X]     |
|  lead-engineer                          |
|                                          |
|  Type:       Specialist                 |
|  Department: engineering                |
|  Reports To: cto                        |
|  Direct Reports: backend-engineer,      |
|                  frontend-engineer       |
|  Model Override: (none — using tier)    |
|                                          |
|  Description:                           |
|  Leads the engineering team, reviews    |
|  code, and coordinates with the CTO.   |
+------------------------------------------+
```

### 5.3 Tasks Tab

```
+------------------------------------------------------------------+
| Dashboard | Org Chart | Tasks | Approvals | Models | Departments |
+------------------------------------------------------------------+
|                                                                    |
|  Assign New Task                                                   |
|  +--------------------------------------------------------------+ |
|  | Receiver: [lead-engineer        v]                          | |
|  | Instruction: [Review PR #42 for the auth module_______]     | |
|  | Priority: [medium v]                                        | |
|  | [Assign Task]                                                | |
|  +--------------------------------------------------------------+ |
|                                                                    |
|  Filters: [all] [pending] [in_progress] [completed] [failed]     |
|                                                                    |
|  +--------------------------------------------------------------+ |
|  | ID      | From     | To           | Instruction     | Pri | St| |
|  |---------|----------|--------------|-----------------|-----|---| |
|  | a3f2c1  | human-ceo| lead-engineer| Review PR #42   |high |pen| |
|  | b7d4e2  | cto      | cfo          | Budget report   |med  |pro| |
|  | c1a8f3  | cmo      | content-writer| Draft blog     |low  |com| |
|  +--------------------------------------------------------------+ |
+------------------------------------------------------------------+
```

### 5.4 Approvals & Escalations Tab

```
+------------------------------------------------------------------+
| Dashboard | Org Chart | Tasks | Approvals | Models | Departments |
+------------------------------------------------------------------+
|                                                                    |
|  +---------------------------+ +---------------------------+     |
|  | Pending Approvals         | | Open Escalations          |     |
|  |                           | |                           |     |
|  | +-----------------------+ | | +-----------------------+ |     |
|  | | [T2] apr-7b3e9f       | | | timeout-rule           | |     |
|  | | lead-backend          | | | lead-backend -> cto    | |     |
|  | | edit: routes.py       | | | Task stalled > 30min   | |     |
|  | | Risk: ██░░░░░░ 25/100 | | |                       | |     |
|  | | Expires: 47m          | | | [Resolve]              | |     |
|  | | [Approve] [Reject]    | | +-----------------------+ |     |
|  | +-----------------------+ | |                           |     |
|  |                           | | +-----------------------+ |     |
|  | +-----------------------+ | | budget-rule             | |     |
|  | | [T3] apr-9c1d2e       | | | financial-analyst ->  | |     |
|  | | devops-engineer       | | |   cfo                  | |     |
|  | | bash: docker compose  | | | Over budget threshold  | |     |
|  | | Risk: █████░░░ 55/100 | | |                       | |     |
|  | | Sigs: 0/2 needed      | | | [Resolve]              | |     |
|  | | Expires: 22m ⚠        | | +-----------------------+ |     |
|  | | [Approve] [Reject]    | |                           |     |
|  | +-----------------------+ | |                           |     |
|  +---------------------------+ +---------------------------+     |
+------------------------------------------------------------------+
```

### 5.5 Models Tab

```
+------------------------------------------------------------------+
| Dashboard | Org Chart | Tasks | Approvals | Models | Departments |
+------------------------------------------------------------------+
|                                                                    |
|  +------------------+ +------------------+ +------------------+   |
|  | [FAST]           | | [STANDARD]       | | [PREMIUM]        |   |
|  | Simple tasks     | | General work     | | Complex reasoning|   |
|  |                  | |                  | |                  |   |
|  | deepseek-chat    | | opencode/pickle  | | opencode/pickle  |   |
|  | ollama/llama3    | | openai/gpt-4o    | | anthropic/sonnet |   |
|  +------------------+ +------------------+ +------------------+   |
|                                                                    |
|  Per-Agent Routing                                                 |
|  +--------------------------------------------------------------+ |
|  | Agent          | Provider | Model       | Tier     | Reason  | |
|  |----------------|----------|-------------|----------|---------| |
|  | cto            | opencode | big-pickle  | PREMIUM  | exec    | |
|  | lead-engineer  | opencode | big-pickle  | PREMIUM  | override| |
|  | content-writer | deepseek | deepseek-chat| STANDARD | default | |
|  | backend-engineer| opencode| big-pickle  | STANDARD | default | |
|  +--------------------------------------------------------------+ |
+------------------------------------------------------------------+
```

---

## 6. Responsive Behavior

| Breakpoint | Layout |
|------------|--------|
| ≥ 1280px | 5-column KPI grid, side-by-side charts |
| ≥ 768px | 2-column KPI grid, stacked charts |
| < 768px | Single column, cards stack vertically |

---

## 7. Real-Time Updates

The dashboard uses WebSocket (`/ws/dashboard`) for live updates:

| Event | Update |
|-------|--------|
| KPI change | All 5 KPI cards update, charts re-render |
| New task | Recent tasks list prepends new row |
| Task completed | KPI card animates, task status updates |
| Approval requested | Badge increments, card appears |
| Approval resolved | Badge decrements, card removed |
| Escalation triggered | Badge increments, red highlight |
| Escalation resolved | Badge decrements, card removed |

---

## 8. Error States

| Scenario | Display |
|----------|---------|
| WebSocket disconnected | "Offline" badge in header, data freezes |
| API error | Toast notification: "Failed to load [resource]" |
| Empty state | Centered message with action hint |
| Rate limited | "Too many requests — please wait" toast |
| Unauthorized | Redirect to health check page |

---

## 9. Accessibility

- All charts include text alternatives
- KPI cards use `aria-label` with full metric name
- Tab navigation: keyboard accessible
- Color is never the sole indicator (text labels + icons accompany)
- Modal focus trap when agent detail is open
- `aria-live="polite"` region for KPI updates
- Screen reader announces: "Pending tasks: 12" not just "12"
