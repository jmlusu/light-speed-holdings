# Page-by-Page Guide

This chapter walks you through every page of the CEO Dashboard — what it shows, how to interact with it, and how it behaves in real time. Each section is self-contained so you can jump directly to the page you need.

---

## Navigation Overview

Every page shares the same navigation framework defined in the base layout:

- **Top Header Bar** — Displays the company name, dashboard uptime counter, WebSocket connection status (green pulsing dot = *Live*, red = *Offline*), and the number of connected clients.
- **Tab Navigation** — A horizontal row of tabs below the header. The active tab is highlighted with a cyan underline. Tabs that have pending items (e.g., escalation count) show a red badge.
- **Command Bar (Ctrl+K)** — A global search and command palette available on every page. Type to search agents, tasks, pages, or run quick actions. Press `↑`/`↓` to navigate results, `Enter` to execute, `Esc` to close.
- **Toast Notifications** — Appear in the bottom-right corner for general alerts. Escalation notifications appear as a separate stack in the top-right corner with *Resolve* / *Dismiss* buttons.
- **Offline Indicator** — A full-width amber banner at the very top of the viewport appears when you lose connectivity. Actions taken while offline are queued and sync automatically when reconnected.

[Screenshot: Annotated base layout showing the header bar, tab navigation, command bar overlay, and toast notification positions]

---

## Dashboard (Home)

### Purpose

The landing page provides an at-a-glance organizational health score with a drill-down gauge, summary alerts, key charts, and a snapshot of recent tasks.

### How to Access

| Method | Detail |
|--------|--------|
| Sidebar tab | **Dashboard** (first tab, grid icon) |
| URL path | `/` |
| Command Bar | Type "dashboard" or "home" |

### Key Elements

1. **Org Health Gauge** — A large, circular gauge rendered on a `<canvas>` element displays the composite organizational health score (0–100). The band label (e.g., GREEN, AMBER, RED) appears inside the gauge. The gauge is clickable.
2. **Component Breakdown (expandable)** — Click the gauge to expand a 2×2 grid of component cards (e.g., Engineering, Sales, Finance, Operations). Each card shows the component's current score, a color-coded status dot, and a mini sparkline chart. Click any component card to see a detail panel with the current score, sub-score, weight in the composite, and a larger sparkline.
3. **Alerts Bar** — A horizontal row below the gauge showing counts of pending approvals (amber), open escalations (red), and in-progress tasks (blue).
4. **Charts Row** — Two side-by-side Chart.js visualizations:
   - *Tasks by Status* — A doughnut/bar chart showing the distribution of pending, in-progress, completed, failed, and escalated tasks.
   - *Department Load* — A bar chart showing the number of agents per department.
5. **Cost Breakdown** — A compact panel showing total spent (USD), average cost per task, the top 5 agents by cost (with horizontal bar indicators), and a cost trend sparkline.
6. **Recent Tasks Table** — The 10 most recent tasks with columns for receiver, instruction (truncated), priority badge, status badge, and creation time. A "View all →" link navigates to the Tasks page.

[Screenshot: Full dashboard home page showing the Org Health gauge in the center, alerts bar, two charts side by side, cost breakdown, and recent tasks table]

### Interactions

| Action | How |
|--------|-----|
| Drill into org health | Click the gauge → component grid appears → click any component card → detail panel with score breakdown |
| Collapse drill-down | Click the component card again or click the `×` button in the detail panel |
| Navigate to Tasks | Click "View all →" in the Recent Tasks table header |
| Navigate to any page | Use the tab bar or press `Ctrl+K` / `⌘K` to open the Command Bar |

### Real-Time Updates

| WebSocket Message | Effect on This Page |
|-------------------|---------------------|
| `kpi_update` | Updates the task counts in the alerts bar and refreshes the charts. The org health gauge re-renders if the score changes. Scroll position is preserved across updates. |
| `task_update` | Locally merges the updated task into the Recent Tasks table (no full reload). |
| `alert` | Triggers a toast notification in the bottom-right corner. |

### Mobile Behavior

On mobile viewports (PWA or narrow browser), the page stacks vertically: the gauge shrinks to a smaller size, the component grid becomes a single column, charts stack one above the other, and the cost breakdown wraps. The Recent Tasks table becomes scrollable horizontally. Touch-friendly tap targets replace hover effects.

### Tips

- The gauge auto-refreshes via WebSocket. If you see stale data, check the top-right status indicator — a red "Offline" badge means the connection dropped and polling is the fallback.
- The sparkline charts inside component cards show the last several data points. They update without a full page refresh.
- The Org Health score is a weighted composite of multiple departmental sub-scores. The weight of each component is visible when you drill into the detail panel.

---

## Command Center

### Purpose

The Command Center is a real-time strategic overview page with a dramatic "arc reactor" visual, executive briefing, AI workforce roster, and model telemetry — designed as a war-room style command dashboard.

### How to Access

| Method | Detail |
|--------|--------|
| Sidebar tab | **Command Center** (monitor icon) |
| URL path | `/command-center` |
| Command Bar | Type "command center" |

### Key Elements

The Command Center has **three switchable layout variants** accessible via the variant switcher at the bottom of the page or keyboard shortcuts:

| Variant | Name | Layout |
|---------|------|--------|
| **A** | *The Bridge* | Three-column layout: Briefing (left) / Company Core (center) / Workforce + Telemetry (right) |
| **B** | *The War Room* | **(Default)** Full-width Company Core hero on top, three-column bottom row: Briefing / Workforce / Activity Stream + Telemetry |
| **C** | *The Cockpit* | Two-column: dominant Company Core (left) / stacked Briefing + Workforce + Activity (right) |

**Common panels across all variants:**

1. **Company Core (Arc Reactor)** — A large animated visualization with concentric rings, animated SVG connection lines to agent nodes on the outer ring, and animated data packets traveling along the connections. The center displays the system health percentage. The ring color shifts based on health: green (≥80%), amber (50–79%), red (<50%).
2. **Executive Briefing** — A prioritized list of items requiring attention. Each item has a priority indicator (high = red, medium = amber, low = muted) with a title and source label. Shows "All clear" when empty.
3. **AI Workforce** — A scrollable list of all registered agents. Each row shows a status dot (online/thinking/executing/etc.), the agent name and role, and the model being used. Status dots are color-coded: green = online, blue = thinking/executing, amber = waiting/delegating, red = escalated/blocked.
4. **Activity Stream** (Variants B and C only) — A timeline of recent events with colored dots, source labels, event text, and relative timestamps. Updates every 5 seconds.
5. **Model Telemetry** — Read-only panel showing each LLM model's request count, success rate (with a colored progress bar), and average latency in milliseconds.
6. **Key Metrics** — Summary stat cards showing: Total Agents, Active Tasks, Pending Approvals, Open Escalations, and (in Variant B) Completed Tasks.

[Screenshot: Command Center in "The War Room" variant (B) showing the arc reactor hero, briefing panel, workforce list, activity stream, and model telemetry]

### Interactions

| Action | How |
|--------|-----|
| Switch layout variant | Click `←` / `→` arrows in the variant switcher at the bottom, or press `Ctrl+1` (Bridge), `Ctrl+2` (War Room), `Ctrl+3` (Cockpit) |
| Toggle command bar | Press `Ctrl+K` / `⌘K` |
| Scroll workforce list | Scroll within the AI Workforce panel (independent scroll) |
| Close command bar | Press `Esc` |

### Real-Time Updates

| WebSocket Message | Effect on This Page |
|-------------------|---------------------|
| `kpi_update` | Refreshes metrics cards, system health percentage, and arc reactor ring color. |
| `task_update` | Updates active/completed task counts in the metrics. |
| `escalation` | Updates escalation count (red when > 0). |
| `connected` | Updates the connected client count. |

Additionally, the **Activity Stream** polls the server every 5 seconds independently of WebSocket messages, and the main data refreshes every 15 seconds as a polling fallback.

### Mobile Behavior

On mobile, the multi-column layouts collapse to a single stacked column. The arc reactor shrinks to fit the viewport width. The variant switcher remains accessible at the bottom. Swipe-scrolling works in each panel independently.

### Tips

- Use `Ctrl+1`/`Ctrl+2`/`Ctrl+3` to rapidly switch between layout variants without reaching for the mouse.
- The arc reactor animation is CSS + SVG only — it has negligible performance cost even on lower-end devices.
- Variant B ("The War Room") is the default because it gives the most screen real estate to the Company Core health visualization while still showing all key panels.

---

## Tasks (Kanban Board)

### Purpose

The Tasks page provides a Kanban board view of the full task pipeline, with drag-and-drop, filtering, sorting, pagination, task assignment, decomposition, and a detail slide-out panel.

### How to Access

| Method | Detail |
|--------|--------|
| Sidebar tab | **Tasks** (clipboard icon) |
| URL path | `/tasks` |
| Command Bar | Type "tasks" or "kanban" |

### Key Elements

1. **Filter Bar** — A horizontal bar above the Kanban board with:
   - **Priority filter** — Toggle buttons for low, medium, high, critical (only one active at a time)
   - **Department filter** — Dropdown populated with all unique departments
   - **Agent filter** — Text input that searches by agent name (debounced 300ms)
   - **Sort** — Dropdown to sort by Date, Priority, Agent, or Status, with an ascending/descending toggle
   - **Clear** link to reset all filters
2. **Kanban Board** — Three primary columns with drag-and-drop:
   - **Pending** (amber dot) — Tasks awaiting execution
   - **In Progress** (blue pulsing dot) — Tasks currently being worked on
   - **Completed** (green dot) — Finished tasks (scrollable, max height 400px)
3. **Secondary Columns** — Below the main three:
   - **Failed** (red dot, red border) — Tasks that failed
   - **Escalated** (amber dot, amber border) — Tasks escalated for human review
4. **Task Cards** — Each card shows: truncated task ID (first 8 chars), priority badge (color-coded), instruction text (2-line clamp), assigned agent, and creation time. Failed/escalated cards also have a delete button.
5. **Assign Task Button** — Opens a modal with fields for: receiver agent (dropdown of all agents), instruction (textarea), and priority selector (low/medium/high/critical).
6. **Task Detail Slide-out Panel** — Clicking any card opens a slide-out panel from the right with:
   - Full task ID, instruction, status badge, priority badge, assigned agent, creation time
   - **Decomposition section** — A "Decompose" button that breaks the task into subtasks with a progress bar and subtask list showing individual statuses (pending, in-progress, completed)
   - **Action buttons** — "Reassign" and "Escalate"
7. **Pagination Controls** — Below the board:
   - Page size selector: 10, 20, 50, 100
   - Page info showing total tasks, current page, and total pages
   - First / Prev / Next / Last navigation buttons

[Screenshot: Full Kanban board showing all five columns with task cards, filter bar at the top, and pagination at the bottom]

### Interactions

| Action | How |
|--------|-----|
| Drag a task between columns | Click and hold a task card in Pending/In Progress, drag it to another column, release to drop. The task status updates automatically. |
| Assign a new task | Click "Assign Task" button (top right) → fill in the modal → click "Assign Task" to submit |
| View task details | Click any task card → slide-out panel opens from the right |
| Decompose a task | In the detail panel, click "Decompose" → subtask list appears with progress bar |
| Reassign a task | In the detail panel, click "Reassign" |
| Escalate a task | In the detail panel, click "Escalate" |
| Delete a task | Click the `×` button on any Pending, In Progress, Failed, or Escalated card |
| Filter by priority | Click a priority button in the filter bar (toggle on/off) |
| Filter by department | Select a department from the dropdown |
| Search by agent | Type in the Agent filter input |
| Change sort order | Select a sort field from the dropdown, click the arrow to toggle asc/desc |
| Clear all filters | Click "Clear" in the filter bar (only appears when filters are active) |
| Paginate | Click First/Prev/Next/Last or change the page size |

### Real-Time Updates

| WebSocket Message | Effect on This Page |
|-------------------|---------------------|
| `task_update` | Reloads the current paginated page to reflect any status changes, new tasks, or deletions. Scroll position is preserved. |

### Mobile Behavior

On mobile, the three-column Kanban board collapses to a **single-column layout** — columns stack vertically (Pending → In Progress → Completed). The Failed and Escalated columns also stack below. The filter bar wraps into multiple rows. Drag-and-drop is replaced by tap-to-select then tap-column-to-move (on touch devices, native HTML5 drag may not work — use the task detail panel's status change instead). The Assign Task modal and Task Detail panel are full-width overlays.

### Tips

- When the WebSocket connection is live, new tasks appear almost instantly without manual refresh.
- Use the Agent filter to quickly see all tasks assigned to a specific agent — useful during standup or review.
- The Decompose feature is powered by the workflow engine and creates actual subtask records in the system, not just a visual breakdown.
- Completed tasks are capped at 400px height with independent scrolling to keep the board manageable.

---

## Agents

### Purpose

The Agents page displays a searchable, filterable registry of all AI agents in the company, with a detail modal for each agent's full profile.

### How to Access

| Method | Detail |
|--------|--------|
| Sidebar tab | **Agents** (people icon) |
| URL path | `/agents` |
| Command Bar | Type "agents" |

### Key Elements

1. **Header** — Shows "Agent Registry" with a live count of registered agents.
2. **Search and Filter Bar** — Two controls in the top-right:
   - **Search input** — Free-text search across agent names and roles
   - **Department dropdown** — Filter by department (populated from unique departments across all agents)
3. **Agent Grid** — A responsive card grid (1 column on mobile, 2 on tablet, 3 on desktop). Each agent card shows:
   - A colored avatar badge with the agent's role initial (color varies by agent type: purple for Executive, blue for Department, green for Specialist, amber for Board)
   - Role name (prominent) and agent ID (monospace, muted)
   - Type badge (executive/specialist/department/etc.)
   - Department
   - Reports-to relationship
   - Number of direct reports (if any)
   - Description (2-line clamp)
4. **Agent Detail Modal** — Clicking any card opens a centered modal with:
   - Full agent profile: type, department, reports-to, direct reports (as chips), model override (if set, highlighted in amber), and full description

[Screenshot: Agent grid showing cards for different agent types with color-coded badges, and a detail modal overlay]

### Interactions

| Action | How |
|--------|-----|
| Search agents | Type in the search input — the grid filters in real time |
| Filter by department | Select a department from the dropdown |
| View agent details | Click any agent card → modal opens |
| Close modal | Click the `×` button, click outside the modal, or press `Esc` |

### Real-Time Updates

| WebSocket Message | Effect on This Page |
|-------------------|---------------------|
| `kpi_update` | The agent count in the header may update if agents were added or removed. |

Note: The Agents page does not have its own dedicated WebSocket subscription. Agent data is loaded once on page load. To see real-time agent status changes, check the Command Center's AI Workforce panel, which polls more frequently.

### Mobile Behavior

On mobile, the agent grid becomes a single column. Cards are full-width with all information visible. The search and filter bar stacks vertically. The detail modal becomes nearly full-screen.

### Tips

- Use the search box to quickly find a specific agent by name — faster than scrolling through a large registry.
- The model override badge (amber highlight) indicates agents that use a specific LLM model rather than the default.
- Agent type badges help you quickly identify the hierarchy: purple = executive, blue = department, green = specialist.

---

## KPIs

### Purpose

The KPIs page provides deep performance metrics across all departments with a system health monitor, anomaly detection, trend charts, and a full KPI comparison table.

### How to Access

| Method | Detail |
|--------|--------|
| Sidebar tab | **KPIs** (bar-chart icon) |
| URL path | `/kpis` |
| Command Bar | Type "KPIs" or "metrics" |

### Key Elements

This page has two major sections:

#### 1. System Health Monitor (top)

- **Header** — "System Health Monitor" with an auto-refresh toggle (ON/OFF) and a manual refresh button. A spinning indicator shows when live updates are active.
- **Component Metric Cards** — A row of cards (one per health component), each showing:
  - Component name (formatted from snake_case)
  - Current value as a large percentage number
  - Color-coded progress bar (green ≥ 80%, amber 50–79%, red < 50%)
  - Change indicator (up/down arrow with color)
- **Composite Score Display** — A horizontal bar showing the overall health score (large number) and band label (green/amber/red).
- **Anomaly Detection** — A list of detected anomalies, each with a severity icon, message text, and timestamp. Anomalies are color-coded by severity.
- **Org Health Trend Chart** — A line chart with time-range selector buttons: 6h, 24h, 7d. The chart shows the health score over time.

#### 2. Department KPIs (bottom)

- **Company KPIs vs Targets** — A grid of cards showing company-wide KPIs with current value, target value, gap, status badge (on_track/below_target/above_target), and a "live" or "config" source indicator. Below the cards, a grouped bar chart compares current vs target across all company KPIs.
- **Department Tabs** — A horizontal row of department tabs (one per department). Clicking a tab loads that department's KPIs.
- **KPI Summary Cards** — For the selected department, a grid of cards showing each KPI with its current value, unit, target bar, and status badge.
- **KPI Charts** — Two side-by-side charts:
  - *KPI Comparison* — Compares KPI values across departments
  - *KPI Targets vs Current* — Shows target vs actual for each KPI in the selected department
- **All Department KPIs Table** — A full-width table listing every KPI across all departments with columns for Department, KPI name, Target, Unit, and Frequency.

[Screenshot: KPIs page showing the health monitor at top with component cards, anomaly list, trend chart, and department KPI tabs below]

### Interactions

| Action | How |
|--------|-----|
| Toggle auto-refresh | Click "Auto-refresh: ON/OFF" in the health monitor header |
| Manual refresh | Click the refresh icon button |
| Change trend time range | Click 6h, 24h, or 7d buttons in the trend chart header |
| Switch department | Click a department tab in the Department KPIs section |
| Refresh KPIs | Click the "Refresh" button in the Department KPIs header |

### Real-Time Updates

| WebSocket Message | Effect on This Page |
|-------------------|---------------------|
| `kpi_update` | When the payload contains `departments` data (live KPI snapshots), the department KPI cards, charts, and health monitor update in place. Charts are coalesced to prevent double redraws per animation frame. |

When auto-refresh is ON, the health monitor polls independently and updates component cards, anomaly list, and trend data.

### Mobile Behavior

On mobile, the component metric cards stack to 2 columns, the KPI summary cards become a single column, and the two side-by-side charts stack vertically. The All KPIs table becomes horizontally scrollable. Department tabs are horizontally scrollable.

### Tips

- Toggle auto-refresh OFF if you want to study a snapshot without it changing while you analyze.
- The anomaly detection section only appears when anomalies are present — it's hidden otherwise to reduce visual noise.
- The "live" tag on company KPI cards means the value is computed from real data; "config" means it's a static configuration target.
- Use the 7d trend range to see weekly patterns in organizational health.

---

## Finance

### Purpose

The Finance page tracks revenue, costs, and profit margin with a payment recording form, revenue ledger, and project cost table.

### How to Access

| Method | Detail |
|--------|--------|
| Sidebar tab | **Finance** (dollar-sign icon) |
| URL path | `/finance` |
| Command Bar | Type "finance" or "revenue" |

### Key Elements

1. **Finance Summary Cards** — Four large metric cards in a row:
   - **Revenue (MWK)** — Total confirmed revenue in Malawian Kwacha (cyan)
   - **Revenue (USD)** — Converted at 1,800 MWK/USD (amber)
   - **Costs (USD)** — Combined delivery + LLM costs (red)
   - **Margin** — Contribution margin percentage (green if positive, red if negative)
2. **Revenue Ledger** — A table of all revenue transactions with columns for ID, Client, Service, Amount (currency + amount), Payment Method, Status (confirmed/pending/failed), and Date.
3. **Record Payment Button** — Opens an inline form with fields:
   - Client ID, Project ID, Offer ID, Service Name
   - Amount (number input)
   - Currency (MWK or USD)
   - Payment Method (Airtel Money, TNM Mpamba, Bank Transfer, PayChangu, Manual)
   - Installment Type (Upfront 50%, Delivery 50%, Full Payment)
   - Reference number, Linked Task ID
4. **Project Costs Table** — A table of all project cost entries with columns for ID, Project, Type, Amount (USD), Agent, Description, and Date.

[Screenshot: Finance page showing the four summary cards at top, revenue ledger table in the middle, and project costs table at the bottom]

### Interactions

| Action | How |
|--------|-----|
| Record a payment | Click "+ Record Payment" → fill in the form → click "Record Payment" |
| Toggle payment form | Click "+ Record Payment" again to collapse the form |
| View transaction details | Scroll through the Revenue Ledger table |
| View cost details | Scroll through the Project Costs table |

### Real-Time Updates

| WebSocket Message | Effect on This Page |
|-------------------|---------------------|
| (None specific) | The Finance page loads data once on init via REST API calls (`/api/v1/revenue/summary`, `/api/v1/revenue`, `/api/v1/project-costs`). To see new payments, click "Refresh" or reload the page. |

Note: The Finance page does not currently subscribe to WebSocket updates. Payment recording triggers an immediate local data reload after successful submission.

### Mobile Behavior

On mobile, the four summary cards become a 2×2 grid. Both tables become horizontally scrollable. The payment form fields stack vertically into a single-column layout.

### Tips

- The margin percentage is color-coded: green for positive (profitable), red for negative (loss).
- Payment methods reflect the Malawian fintech ecosystem: Airtel Money and TNM Mpamba are mobile money platforms, PayChangu is a local payment gateway.
- The exchange rate (1,800 MWK/USD) is hardcoded in the display — the actual conversion uses the rate from the database per transaction.

---

## Costs

### Purpose

The Costs page provides detailed LLM usage cost analysis with budget tracking, trend charts, per-agent cost breakdowns, and budget alerts.

### How to Access

| Method | Detail |
|--------|--------|
| Sidebar tab | **Costs** (dollar-sign icon) |
| URL path | `/costs` |
| Command Bar | Type "costs" or "budget" |

### Key Elements

1. **Period Selector** — Three toggle buttons at the top: **Daily**, **Weekly**, **Monthly**. Clicking one changes the time period for all data on the page.
2. **Cost Summary Cards** — Four cards:
   - **Total Cost** — Dollar amount for the selected period
   - **Budget Used** — Percentage with a color-coded progress bar (green < 70%, amber 70–90%, red > 90%)
   - **Avg Cost/Task** — Cost per task average (to 6 decimal places)
   - **Total Tasks** — Number of tasks in the period
3. **Cost Charts** — Two side-by-side Chart.js visualizations:
   - *Cost Trend* — Line chart showing cost over time for the selected period
   - *Cost by Agent* — Bar/doughnut chart breaking down costs by individual agent
4. **Budget Alerts** — A list of active alerts, each with severity-based styling:
   - Critical (red background/border) — Budget exceeded or critical threshold
   - Warning (amber) — Approaching budget limits
   - Info (blue) — Informational notices
5. **Cost per Agent Table** — A table with columns for Agent name, Tasks count, Total Cost, Average Cost per Task, and Model used.

[Screenshot: Costs page showing the period selector, four summary cards, cost trend and agent cost charts, budget alerts, and per-agent cost table]

### Interactions

| Action | How |
|--------|-----|
| Change time period | Click **Daily**, **Weekly**, or **Monthly** — all data on the page reloads for the new period |
| View cost trend | Read the Cost Trend line chart |
| Identify high-cost agents | Look at the Cost by Agent chart or the per-agent table sorted by total cost |

### Real-Time Updates

| WebSocket Message | Effect on This Page |
|-------------------|---------------------|
| (None specific) | Cost data is loaded on page init and when the period changes. To refresh, change the period or reload the page. |

### Mobile Behavior

On mobile, the summary cards stack to a single column, the two charts stack vertically, and the per-agent table becomes horizontally scrollable.

### Tips

- The budget progress bar changes color dynamically: green is healthy, amber means you're approaching limits, red means you've exceeded 90% of your budget.
- Switch between Daily/Weekly/Monthly to identify cost spikes on different time scales.
- The per-agent table shows which agents are the most expensive — useful for optimizing model assignments.

---

## Escalations

### Purpose

The Escalations page is the human-in-the-loop decision center, showing pending approval requests and open escalations side by side for quick triage.

### How to Access

| Method | Detail |
|--------|--------|
| Sidebar tab | **Approvals** (warning triangle icon) |
| URL path | `/escalations` |
| Command Bar | Type "escalations" or "approvals" |

### Key Elements

The page is a **two-column layout**:

#### Left Column: Pending Approvals

- **Header** — "Pending Approvals" with a count and refresh button
- **Empty State** — A green checkmark icon with "All caught up!" message when no approvals are pending
- **Approval Cards** — Each card shows:
  - Action name (what the agent wants to do)
  - Agent ID (who requested it)
  - Description (detailed explanation)
  - Risk level badge (low = green, medium = amber, high = red)
  - Cost estimate (in cyan)
  - Timestamp
  - **Edit button** — Opens an inline form to modify risk level and cost estimate before approving
  - **Approve button** (green) — Approves the request
  - **Reject button** (red) — Rejects the request

#### Right Column: Open Escalations

- **Header** — "Open Escalations" with a count and refresh button
- **Empty State** — Green checkmark with "All clear!" when no escalations exist
- **Escalation Cards** — Each card shows:
  - Rule ID that triggered the escalation
  - From agent → To agent flow (with an arrow icon)
  - Reason text
  - Timestamp
  - **Resolve button** — Marks the escalation as resolved

[Screenshot: Escalations page showing the two-column layout with pending approvals on the left and open escalations on the right]

### Interactions

| Action | How |
|--------|-----|
| Approve a request | Click the green "Approve" button on an approval card |
| Reject a request | Click the red "Reject" button on an approval card |
| Edit risk/cost before approving | Click "Edit" → modify risk level and cost estimate in the inline form → click "Save" → then Approve |
| Resolve an escalation | Click the "Resolve" button on an escalation card |
| Refresh data | Click the refresh icon in either column header |

### Real-Time Updates

| WebSocket Message | Effect on This Page |
|-------------------|---------------------|
| `escalation` | When a new escalation arrives via WebSocket, the escalation list auto-refreshes. Additionally, a dedicated escalation notification toast appears in the top-right corner with *Resolve* / *Dismiss* buttons — this works on **any** page, not just the Escalations page. |
| `alert` | Approval-related alerts trigger a toast notification. |

### Mobile Behavior

On mobile, the two-column layout stacks vertically: Pending Approvals on top, Open Escalations below. Cards become full-width. The inline edit form for risk/cost takes the full card width.

### Tips

- Escalation notifications arrive globally (top-right toasts) even when you're on a different page — you never miss a critical escalation.
- The Edit feature lets you adjust the risk assessment and cost estimate *before* approving, so you can correct agent miscalculations.
- When no approvals or escalations exist, the empty states are visually distinct (green checkmarks) so you know the system is healthy at a glance.

---

## Org Chart

### Purpose

The Org Chart page visualizes the company's organizational hierarchy as an interactive tree, with drag-and-drop reassignment and zoom controls.

### How to Access

| Method | Detail |
|--------|--------|
| Sidebar tab | **Org Chart** (sitemap icon) |
| URL path | `/org-chart` |
| Command Bar | Type "org chart" or "hierarchy" |

### Key Elements

1. **Header Controls** — Three controls in the top-right:
   - **Fit** button — Resets zoom to 100% to fit the tree to the viewport
   - **Reset** button — Sets zoom to 75% for a wider view
   - **Zoom percentage** — Displays current zoom level
2. **Org Tree Container** — A large scrollable area (full viewport height minus header) containing the hierarchical tree:
   - Each node is a card showing the type badge (3-letter abbreviation, color-coded by type: purple = Executive, blue = Department, green = Specialist, amber = Board), agent name, and role
   - Three levels of hierarchy are rendered: root → children → grandchildren
   - Nodes with children have expand/collapse behavior
   - Connector lines link parent and child nodes
3. **Node Selection Panel** — Clicking any node opens a fixed panel in the bottom-right corner showing:
   - Agent name and role
   - Type, Department, Reports To, Direct Reports count
   - **View Details** button — Opens the full agent detail modal
   - **Reassign** button — Opens the reassignment modal
4. **Reassignment Modal** — A centered modal that lets you change which manager an agent reports to. Shows the agent name, a dropdown of all available managers, and Cancel/Reassign buttons.

[Screenshot: Org chart showing a hierarchical tree with color-coded node cards, connector lines, and a selected node detail panel in the corner]

### Interactions

| Action | How |
|--------|-----|
| Select a node | Click any node card — detail panel appears in bottom-right |
| Drag to reassign | Drag a node card and drop it onto another node's card (drag-and-drop reassignment) |
| Reassign via modal | Select a node → click "Reassign" in the detail panel → choose a new manager from the dropdown → click "Reassign" |
| View full details | Select a node → click "View Details" in the detail panel |
| Zoom in/out | Use Fit/Reset buttons, or change the zoom percentage |
| Scroll the tree | Scroll within the tree container (it's independently scrollable) |
| Close detail panel | Click the `×` button in the panel |

### Real-Time Updates

| WebSocket Message | Effect on This Page |
|-------------------|---------------------|
| (None specific) | The org chart loads data on init via REST (`/api/v1/org-chart` and `/api/v1/agents`). After a reassignment, the tree reloads automatically. |

Note: The interactive org chart JS (`org-chart-interactive.js`) subscribes to `agents` and `tasks` topics for real-time node updates if that component is active.

### Mobile Behavior

On mobile, the tree container becomes horizontally and vertically scrollable. The detail panel moves to a bottom sheet that can be swiped closed. The reassignment modal becomes full-width. Pinch-to-zoom may work on touch devices for adjusting the tree scale.

### Tips

- Use drag-and-drop for quick visual reassignment — drag an agent onto their new manager's card.
- The Fit button is useful after zooming out to explore the tree — click it to snap back to a readable view.
- Node type badges use 3-letter abbreviations: "Exe" for Executive, "Dep" for Department, "Spe" for Specialist, "Boa" for Board.
- The tree supports three levels of hierarchy. Deeper nesting may require scrolling.

---

## Mission Control

### Purpose

Mission Control is the strategic operations hub, combining an Org Health hero visualization with a workflow pipeline engine for managing multi-step business processes.

### How to Access

| Method | Detail |
|--------|--------|
| Sidebar tab | **Mission Control** (lightning bolt icon) |
| URL path | `/mission-control` |
| Command Bar | Type "mission control" or "workflows" |

### Key Elements

The page has two major sections:

#### 1. Org Health Hero Prototype (top)

A switchable hero visualization with three layout variants (A, B, D):

| Variant | Description |
|---------|-------------|
| **A** | Centered gauge + 4 KPI component cards in a grid |
| **B** | Horizontal split: gauge (left) + 2×2 KPI cards (right) |
| **D** | Drill-down gauge (click to expand) + component breakdown |

Each variant shows the organizational health score as a large gauge with the score number and band label inside. Component cards include mini sparklines.

A floating **prototype switcher bar** at the bottom of the screen lets you cycle between variants using `←`/`→` buttons (this is a development/design tool).

#### 2. Workflow Pipeline UI (bottom)

- **Header** — "Mission Control" with a WebSocket connection status dot (green/amber) and instance count.
- **Start Workflow** — A dropdown to select a workflow template, and a "Start" button to launch a new instance.
- **Main Layout** — Two-column grid:
  - **Left Rail: Instance List** — A scrollable list of all workflow instances. Each card shows the workflow name, status badge (running/completed/cancelled), step progress (e.g., "3/5 steps"), and a short ID.
  - **Right Panel: Pipeline Detail** — When an instance is selected:
    - Header with workflow name, instance ID, and action buttons (Advance, Complete Step, Abort)
    - **Progress bar** — Cyan gradient showing completion percentage
    - **Step pipeline** — A vertical timeline of workflow steps, each with:
      - Status icon (checkmark = completed, lightning = in progress, number = pending, X = cancelled)
      - Step name (color-coded by status)
      - Owner, action label, SLA countdown
      - Result text (if completed)
    - **Detail footer** — Start time, completion time, workflow ID

[Screenshot: Mission Control showing the Org Health gauge hero at top and the workflow pipeline below with instance list on the left and step timeline on the right]

### Interactions

| Action | How |
|--------|-----|
| Switch hero variant | Click `←`/`→` in the floating switcher bar at the bottom |
| Start a new workflow | Select a workflow from the dropdown → click "Start" |
| Select an instance | Click any instance card in the left rail |
| Advance a step | Click "Advance" in the pipeline header (only for running instances) |
| Complete current step | Click "Complete Step" in the pipeline header |
| Abort an instance | Click "Abort" in the pipeline header |

### Real-Time Updates

| WebSocket Message | Effect on This Page |
|-------------------|---------------------|
| `workflows` topic | The instance list auto-refreshes every 5 seconds via polling. WebSocket messages on the `workflows` topic update the pipeline detail in real time. The connection status dot reflects the WS state. |

### Mobile Behavior

On mobile, the hero variant collapses to a single-column layout. The workflow pipeline's two-column grid becomes a single column: the instance list appears on top, and the pipeline detail appears below when an instance is selected. The floating variant switcher remains accessible.

### Tips

- The "Advance" button moves the workflow to the next step automatically; "Complete Step" marks the current step as done and moves to the next.
- "Abort" cancels the entire workflow — use this only when the process should not continue.
- The SLA countdown on each step shows the time remaining before the step's service level agreement expires.
- The Org Health hero variants (A/B/D) are prototypes for design exploration. Variant D is the most interactive with drill-down capability.

---

## Onboarding

### Purpose

The Onboarding page manages the full agent onboarding lifecycle — from initial request through code generation, testing, approval, and activation.

### How to Access

| Method | Detail |
|--------|--------|
| Sidebar tab | **Onboarding** (person-plus icon) |
| URL path | `/onboarding` |
| Command Bar | Type "onboarding" |

### Key Elements

1. **Header** — "Agent Onboarding Studio" with a description and Refresh button.
2. **Filter Bar** — A glass-styled panel with:
   - **State filter buttons** — All, Pending, Generating, Testing, Active (each shows a count in parentheses)
   - **Agent search input** — Text search with a magnifying glass icon
3. **Request Groups** — Requests are grouped by state, each group in a collapsible section:
   - **Group header** — State label (color-coded), state name, count
   - **Request cards** — Each card shows:
     - Agent ID (monospace)
     - Department
     - HITL Tier badge (T1–T4, color-coded)
     - Role and assigned tools
     - Creation timestamp
     - Approval expiration time (if in approval state, shown in amber)
     - Error message (if in error state, shown in red)
4. **Action Buttons** (per request):
   - **Approve** (green) — Available for requests in `approval` or `requested` state
   - **Reject** (red) — Opens a reject confirmation modal with optional reason textarea
5. **Progress Indicator** — For requests in `generating` or `testing` state, a horizontal progress bar with percentage.
6. **Reject Modal** — A centered modal with the agent ID, a reason textarea, and Cancel/Reject buttons.

[Screenshot: Onboarding page showing the filter bar at top, grouped request cards with state badges and action buttons, and a progress bar for in-progress items]

### Interactions

| Action | How |
|--------|-----|
| Filter by state | Click a state button (All/Pending/Generating/Testing/Active) |
| Search for an agent | Type in the agent search input |
| Approve a request | Click the green "Approve" button on a request card |
| Reject a request | Click the red "Reject" button → fill in optional reason → click "Reject" in the modal |
| Refresh data | Click the "Refresh" button in the header |
| View request details | Read the card — it shows agent ID, role, tools, department, tier, and timestamps |

### Real-Time Updates

| WebSocket Message | Effect on This Page |
|-------------------|---------------------|
| `onboarding` topic | The onboarding page subscribes to the `onboarding` WebSocket topic. State changes (e.g., a request moving from `generating` to `testing`) update the cards in real time without a manual refresh. |

### Mobile Behavior

On mobile, the filter bar wraps vertically. Request cards become full-width. The state group sections stack. The reject modal becomes full-width. Action buttons on each card remain accessible via horizontal scrolling if needed.

### Tips

- The HITL Tier badge (T1–T4) indicates the human-in-the-loop oversight level — lower tiers have more autonomy, higher tiers require more human approval.
- Requests in `approval` state have an expiration timer — if not approved in time, they may expire and need re-submission.
- The progress bar for `generating`/`testing` states shows real-time progress as the system builds and validates the agent.
- Use the state filter buttons to quickly triage: start with "Pending" to see what needs your attention, then check "Generating" and "Testing" for in-progress items.
- Error messages appear in red on the request card — check these if an onboarding request is stuck.

---

## Global Features (Cross-Page)

These features are available on **every page** of the dashboard:

### Command Bar (Ctrl+K / ⌘K)

The command bar is a universal search and navigation tool. Press `Ctrl+K` (Windows/Linux) or `⌘K` (Mac) from any page to open it. Type to search for agents, tasks, pages, or actions. Results are grouped by type. Use `↑`/`↓` to navigate, `Enter` to execute, `Esc` to close. The command bar supports voice input on compatible browsers (microphone button).

### Offline Support (PWA)

The dashboard is a Progressive Web App. When you lose connectivity:
- An amber banner appears at the top: "You are offline. Changes will sync when reconnected."
- Mutating actions (POST/PUT/PATCH/DELETE) are queued in IndexedDB
- The offline queue badge appears in the tab navigation bar showing the number of queued actions
- Click the badge to open the Offline Queue panel, which shows each queued action with its timestamp, URL, and retry/delete buttons
- When connectivity restores, queued actions replay automatically
- If a replayed action conflicts with the current server state, a **Conflict Resolution Modal** appears showing a side-by-side diff of your queued change vs. the server state, with options to "Keep Server State" or "Override with Queue"

### Escalation Notifications (Global)

Escalation notifications appear as a stack of toast-style cards in the **top-right corner** of the viewport, regardless of which page you're on. Each notification shows the escalation reason, the from→to agent flow, and *Resolve* / *Dismiss* buttons. These are pushed in real time via WebSocket.

### API Status Banner

When a background API request fails (network error, timeout, rate limit, auth error), a small amber banner appears in the **bottom-left corner** with a descriptive message. It auto-clears on the next successful request. This prevents silent failures from going unnoticed.

### Scroll Position Preservation

The dashboard preserves your scroll position across data updates. When WebSocket messages trigger a re-render (e.g., KPI update, task update), the page saves your scroll position, applies the update, and restores you to exactly where you were. This prevents the frustrating "auto-scroll to top" behavior common in real-time dashboards.
