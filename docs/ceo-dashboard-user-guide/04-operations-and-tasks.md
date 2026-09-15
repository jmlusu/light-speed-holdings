# CEO Dashboard User Guide — Day-to-Day Operations & Task Management

**Version:** 1.0 — Draft
**Last Updated:** 2026-08-26
**Document Owner:** Chief Operating Officer

---

## Day-to-Day Operations

The CEO Dashboard is your operational nerve center. This section covers how you navigate it, build a daily routine around it, and stay on top of everything happening across the organization without drowning in noise.

---

### Dashboard Navigation

The dashboard uses a **horizontal tab bar** across the top of every page, just below the sticky header. Each tab is a distinct page with its own URL, data, and purpose. You can navigate by clicking tabs directly, using the command bar, or typing a URL.

#### Tab Bar Walkthrough

The navigation bar contains the following tabs, listed left to right:

| Tab | URL | What It's For |
|-----|-----|---------------|
| **Dashboard** | `/` | The default landing page. Displays KPI cards (pending tasks, completed tasks, escalated tasks, etc.), the Org Health Score, and summary metrics. This is your "at a glance" home. |
| **Agents** | `/agents` | Full roster of every agent in the company. View agent names, roles, departments, assigned models, and current status. Use this to check who's available and who's overloaded. |
| **Tasks** | `/tasks` | The Kanban task board. This is where you create, assign, track, and complete tasks. Cards are organized in columns by status. See [Kanban Board](#kanban-board) below for details. |
| **KPIs** | `/kpis` | Department and company-wide Key Performance Indicator charts. Select time ranges, switch department views, and compare trends. See [KPIs and Analytics](06-kpis-and-analytics.md) for the full walkthrough. |
| **Costs** | `/costs` | Financial metrics: LLM spend, cost per agent, budget utilization, and cost trends over time. |
| **Approvals** | `/escalations` | The dual-pane view for pending approvals (left) and open escalations (right). This is where human-in-the-loop decisions happen. See [Approval Workflow](#approval-workflow) and [Escalation Workflow](#escalation-workflow). |
| **Command Center** | `/command-center` | A cinematic, real-time headquarters view with the Executive Briefing panel, organizational health arcs, and live alert feeds. Designed for your morning check-in and periodic monitoring. |
| **Mission Control** | `/mission-control` | Strategic overview: goal tracking, how operational work ladders up to company objectives, and high-level progress indicators. |
| **Finance** | `/finance` | Extended financial views: budget breakdowns by department, revenue projections, and spend forecasting. |
| **Onboarding** | `/onboarding` | Setup wizard for new users: configure preferences, notification settings, and initial dashboard orientation. |
| **Org Chart** | `/org-chart` | Visual hierarchy of the organization. Shows reporting lines, department structure, and agent span-of-control. |

> **Tip:** The tab you have open determines what the URL bar shows. You can bookmark any tab's URL directly — for example, bookmark `http://localhost:8420/tasks` to land on the task board every time.

[Screenshot: Full navigation tab bar with all tabs visible, Command Center tab highlighted — Navigation Bar]

#### Keyboard Navigation with the Command Bar

The command bar is your shortcut to anything in the dashboard. Press `Ctrl + K` (or `Cmd + K` on macOS) from any page to open it.

**What the command bar does:**

1. **Page navigation** — Type the name of any page ("tasks", "escalations", "kpis") and press Enter to jump directly to it.
2. **Search tasks** — Type a task ID or partial instruction to find specific tasks.
3. **Search agents** — Type an agent name to find and navigate to their details.
4. **Quick actions** — Access common operations without navigating to a specific page.

**How to use it:**

1. Press `Ctrl + K`. The command bar opens as an overlay with a search input focused.
2. Type your query. Results appear in real time, grouped by category (pages, tasks, agents, actions).
3. Use the `↑` and `↓` arrow keys to navigate results. `Enter` executes the selected result. `Esc` closes the command bar.
4. Each result shows an icon indicating its type, a title, and a description. Results are ranked by relevance.

[Screenshot: Command bar open with search results showing pages and agents — Command Bar]

> **Tip:** You can open the command bar at any time, even if another modal or dropdown is open. It always appears on top. Build the habit of using `Ctrl + K` instead of clicking through tabs — it's faster, especially when you know what you're looking for.

#### URL-Based Routing

Every page has a stable URL. This means:

- You can share a link to a specific page with a colleague: "Check out `/escalations` — there are three T3 approvals waiting."
- Your browser's back and forward buttons work as expected.
- Refreshing the page reloads the same view you were on.

The URL updates automatically as you navigate. There is no single-page-app routing ambiguity — each URL maps to exactly one view.

---

### Your Daily Routine

The dashboard is designed for continuous monitoring, but your most productive pattern is a structured check-in cadence. Here's a recommended routine built around the dashboard's layout.

#### Morning Check-In (5–10 minutes)

Start your day at the **Command Center**.

1. **Open the Command Center** (`/command-center`). The Executive Briefing panel shows you what happened overnight — new escalations, failed tasks, SLA breaches, and anything that needs your attention. Items are ranked by priority (high/medium/low), so scan from the top.

2. **Check the escalation count.** If there are any open escalations (shown in the briefing or in the top-bar badge), navigate to **Approvals** (`/escalations`) immediately. Unresolved escalations are time-sensitive — they represent tasks that are blocked or have exceeded their SLA.

3. **Scan the KPIs.** Return to the **Dashboard** tab (`/`) or navigate to **KPIs** (`/kpis`). Look for:
   - Org Health Score — is it in the green (≥80), yellow (60–79), or red (<60) band?
   - Any department KPI that has dropped significantly since yesterday.
   - The pending tasks count — if it's climbing, agents may be blocked or overloaded.

4. **Check agent status.** Navigate to **Agents** (`/agents`). Scan for any agents that show error states or unusually low task completion rates.

> **Tip:** If your morning check-in reveals no escalations and all KPIs are green, you can skip directly to strategic work. The dashboard's real-time WebSocket updates will push alerts to you if something changes — you don't need to babysit it.

#### During the Day

As you work, the dashboard runs in the background. The key things to watch for:

- **Toast notifications** — These appear in the bottom-right corner of the screen. They're triggered by WebSocket events: new escalations, approval requests, and critical alerts. You'll hear/see them even if you're on a different tab.
- **Badge counts** — The **Approvals** tab shows a red badge with the count of pending approvals. If that number is climbing, clear the queue.
- **WebSocket status** — The top-right corner shows a "Live" indicator (green dot + text) when the WebSocket connection is active. If it shows "Offline" (red), you're seeing stale data — refresh the page.

#### End-of-Day Review (3–5 minutes)

Before signing off:

1. Navigate to **Tasks** (`/tasks`). Scan the Kanban board for any tasks stuck in **In Progress** for more than 24 hours — these may need reassignment or escalation.
2. Check **Approvals** (`/escalations`). Approve or reject anything pending. Pending approvals have SLA timers — if a Tier 2 request times out (60 minutes), it automatically escalates to Tier 3, creating more work.
3. Glance at **KPIs** (`/kpis`). Confirm no trends are moving in the wrong direction overnight.

> **Tip:** If you use the dashboard on mobile (see [Mobile Usage](#mobile-usepwa)), you can do a quick end-of-day check from your phone. The mobile PWA shows the same data with a touch-optimized layout.

---

## Task Management

Tasks are the fundamental unit of work in Light Speed Holdings. Every piece of work — from code changes to strategic analysis — flows through the task system as a tracked item with an owner, a status, and a lifecycle.

---

### Kanban Board

The **Tasks** page (`/tasks`) displays all active work on a Kanban board. The board is organized into columns that represent task statuses, and you interact with task cards by dragging them between columns or clicking to inspect details.

#### Column Meanings

The board uses three primary columns:

| Column | What It Means | What You Should See |
|--------|---------------|---------------------|
| **Pending** | Tasks that have been created and assigned but not yet started by an agent. These are in the queue, waiting for an agent to pick them up. | Tasks with amber dot indicator. The count badge shows how many are waiting. |
| **In Progress** | Tasks that an agent is actively working on. The agent has picked up the task and is executing it. | Tasks with a cyan/blue indicator. If a task has been here for a long time, it may be stuck. |
| **Done** | Tasks that have been completed successfully. These are archived and ready for review. | Tasks with a green indicator. Completed tasks appear here until they're pruned from the active view. |

On narrower screens (mobile or small browser windows), the columns stack vertically instead of displaying side by side.

[Screenshot: Kanban board with three columns — Pending (3 tasks), In Progress (2 tasks), Done (5 tasks) — Tasks Page]

#### Reading Task Cards

Each task card on the Kanban board displays the following information at a glance:

| Element | Description |
|---------|-------------|
| **Task ID** | The first 8 characters of the task's UUID (e.g., `a3f2c1b7`). Click to open the full detail view. |
| **Priority badge** | Color-coded label: `low` (gray), `medium` (amber), `high` (orange), `critical` (red). |
| **Instruction** | The task's instruction text — a one-line summary of what the agent should do. Truncated on the card; click to read the full text. |
| **Assigned agent** | The `receiver_id` — the agent responsible for executing this task. |
| **Timestamp** | When the task was created. |

> **Tip:** Task cards are clickable. Click any card to open a detail view with the full instruction, creation time, current status, and the ability to delete the task if needed.

#### Drag-and-Drop

To move a task between columns:

1. Click and hold the task card.
2. Drag it to the target column.
3. Release the mouse button.

The board updates the task's status immediately, and a WebSocket broadcast notifies all connected clients. The task moves to its new column on your screen and on anyone else's browser that has the dashboard open.

You can move tasks:
- **Pending → In Progress**: When you want to indicate an agent has started working.
- **In Progress → Done**: When the task is complete.
- **In Progress → Pending**: If you need to return a task to the queue (for example, if it was assigned to the wrong agent).

> **Tip:** Drag-and-drop is also supported on mobile. Touch and hold a card, then drag it to a new column. The mobile layout stacks columns vertically, so you scroll down to reach the target column.

#### Filtering and Sorting

The filter bar above the Kanban board lets you narrow the view:

| Filter | How It Works |
|--------|-------------|
| **Priority** | Click any priority button (`low`, `medium`, `high`, `critical`) to show only tasks at that priority. Click again to deselect. Multiple priorities can be selected. |
| **Department** | Use the dropdown to filter tasks by the department of the assigned agent. Defaults to "All". |
| **Agent** | Type an agent name in the text input. Results filter as you type (300ms debounce). |
| **Sort** | Choose how tasks are ordered within each column: by `Date` (created_at), `Priority`, `Agent` (receiver_id), or `Status`. Click the arrow icon next to the sort dropdown to toggle ascending/descending. |

When filters are active, a **Clear** link appears. Click it to reset all filters at once.

[Screenshot: Filter bar with Priority buttons, Department dropdown, Agent search, and Sort controls — Tasks Page Filter Bar]

> **Tip:** If you frequently check tasks for a specific agent, type their name in the Agent filter. The filter persists within your session — you can switch tabs and come back without losing your filter settings.

#### Creating Tasks

To create a new task:

1. Click the **Assign Task** button in the top-right corner of the Tasks page.
2. A modal appears with fields for:
   - **Receiver** — The agent who will execute this task (required).
   - **Instruction** — What the agent should do (required).
   - **Priority** — `low`, `medium`, `high`, or `critical` (defaults to `medium`).
   - **Sender** — Who is assigning this task (defaults to your operator ID).
3. Click **Assign** to create the task.

The new task appears in the **Pending** column immediately (via WebSocket push), and the assigned agent picks it up on its next execution cycle.

> **Tip:** Be specific in the instruction field. "Write unit tests for the auth module" is better than "fix tests." Agents execute instructions literally — vague instructions produce vague results.

#### Bulk Actions

The Kanban board supports bulk operations through multi-select:

1. Hold `Shift` and click multiple task cards to select them.
2. With multiple tasks selected, action buttons appear in the toolbar above the board.
3. Available bulk actions: **Bulk Delete** (remove selected tasks from the queue) and **Bulk Reprioritize** (change the priority of all selected tasks).

> **Tip:** Use bulk actions when you need to clean up stale tasks at the end of a sprint or reprioritize a batch of work after a strategy change.

---

### Task Lifecycle

Every task follows a defined lifecycle from creation to completion. Understanding the flow helps you know what to expect and where to intervene.

#### States and Transitions

| State | Meaning | Who Moves Tasks Here |
|-------|---------|---------------------|
| **Backlog** | Task exists but is not yet prioritized for execution. | Created by agents or operators; moved to Ready when prioritized. |
| **Ready** (Pending) | Task is assigned, prioritized, and waiting for an agent to pick it up. | Moved from Backlog by operators or automatically by the scheduler. |
| **In Progress** | An agent has claimed the task and is executing it. | Moved automatically when an agent picks up the task from the MessageBus queue. |
| **Review** | Task is complete but awaiting human review before being marked Done. | Moved by the agent when execution finishes; requires approval gate clearance. |
| **Done** | Task is complete and verified. | Moved by operators or automatically after approval. |
| **Failed** | Task execution failed (agent error, dependency failure, etc.). | Moved automatically when the executor encounters an error. |
| **Escalated** | Task requires human intervention beyond the agent's authority. | Moved automatically when the agent hits an approval gate or SLA breach. |
| **Reopened** | A Done or Failed task is being re-executed. | Moved by operators who need to re-run or fix a previous task. |

#### Lifecycle Flow

```
Backlog ──▶ Ready ──▶ In Progress ──▶ Review ──▶ Done
                                │         │
                                ▼         ▼
                            Failed    Reopened ──▶ In Progress
                                │
                                ▼
                           Escalated ──▶ (Human resolves) ──▶ In Progress or Done
```

#### Who Can Move Tasks Where

| Transition | Who Can Do It | How |
|-----------|--------------|-----|
| Any → In Progress | The assigned agent (automatically) | Agent picks up the task from `inbox.json` on its execution cycle. |
| In Progress → Done | Operator or agent (after approval gate) | Drag-and-drop on Kanban board, or approval gate auto-advances. |
| In Progress → Failed | System (automatic) | Executor detects an error during task execution. |
| In Progress → Escalated | System (automatic) | Agent hits an approval gate, SLA breach, or authority limit. |
| Any → Pending/Ready | Operator | Drag-and-drop on Kanban board. |
| Done/Failed → Reopened | Operator | Click the task and select **Reopen**. |
| Escalated → In Progress | Operator (after resolving escalation) | Resolve the escalation on the Approvals page, then reassign. |

> **Tip:** If you see a task stuck in **In Progress** for an unusual amount of time, check the agent's status on the **Agents** page. The agent may be blocked by an approval gate — navigate to **Approvals** to see if there's a pending request for that task.

---

### Escalation Workflow

Escalations are tasks or situations that exceed an agent's authority, capability, or time limit. They surface on the **Approvals** page (`/escalations`) in the right-hand pane.

#### What Triggers an Escalation

An escalation is created automatically when:

| Trigger | Description |
|---------|-------------|
| **SLA breach** | A task has been in a given state longer than its allowed time limit. |
| **Agent error** | The agent encountered an unrecoverable error during execution. |
| **Approval gate timeout** | A pending approval was not resolved within its tier's timeout window. |
| **Authority limit** | The agent attempted an action (like a `bash` command or `edit` to production files) that requires human approval, and the approval request expired. |
| **HITL block** | The agent is waiting for human-in-the-loop input and the wait exceeded the configured threshold. |

#### Severity Levels

Every escalation has a severity level that determines how urgently you should respond:

| Level | Badge | What It Means | Expected Response Time |
|-------|-------|---------------|----------------------|
| **Critical** | Red | Service is down, data loss is imminent, or a production system is affected. | Immediate — within minutes. |
| **High** | Orange | A significant task is blocked, SLA is breached, or an agent is unable to proceed. | Within 1 hour. |
| **Medium** | Yellow | A task is degraded but not blocked. Agent can continue with reduced functionality. | Within 4 hours. |
| **Low** | Gray | Informational. The agent logged a non-critical issue for awareness. | Next business day. |

#### How to Review Escalations

1. Navigate to **Approvals** (`/escalations`). The right-hand pane shows **Open Escalations**.
2. Each escalation card displays:
   - **Rule ID** — The trigger that caused the escalation (e.g., SLA breach, authority limit).
   - **From → To** — The agent that escalated and the agent/operator it was escalated to.
   - **Reason** — A human-readable explanation of why the escalation was triggered.
   - **Timestamp** — When the escalation occurred.
   - **Severity badge** — Red/orange/yellow/gray indicator.
3. Read the reason carefully. It tells you what went wrong and what the agent was trying to do.

#### Resolving an Escalation

1. Click the **Resolve** button on the escalation card.
2. The system marks the escalation as resolved and logs the resolution in the audit trail.
3. After resolving, decide what to do with the underlying task:
   - If the task should continue: Navigate to **Tasks**, find the task, and move it back to **Pending** or **In Progress**.
   - If the task should be abandoned: Delete it from the Tasks page.
   - If the task needs reassignment: Create a new task with a different agent as the receiver.

> **Tip:** The escalation count appears as a red badge on the **Approvals** tab in the navigation bar. If you see a number there, it needs attention — don't let escalations pile up. Each unresolved escalation blocks the affected agent from doing other work.

---

### Approval Workflow

Approvals are the human-in-the-loop gatekeepers of the system. When an agent wants to perform a high-risk action, it must wait for explicit human approval before proceeding. The approval system uses a 5-tier matrix where friction scales with risk.

#### The 5-Tier Approval Matrix

| Tier | Name | Gate Type | Who Can Approve | Timeout | Examples |
|------|------|-----------|-----------------|---------|----------|
| **0** | Auto | None | — | — | `read`, `list`, `grep`, `recall` — safe, read-only operations. |
| **1** | Notify | Log only | — | — | `store_memory`, routine status updates — logged but never blocked. |
| **2** | Single Approve | One human | Any operator | 60 minutes → escalates to Tier 3 | `edit` code, budget changes under $100, configuration updates. |
| **3** | Dual Approve | Two humans | Any 2 distinct operators | 30 minutes → escalates to CEO | `bash` execution, data deletion, spend over $500, production deploys. |
| **4** | CEO Only | CEO explicit | CEO only | 24 hours → board notification | Constitutional changes, new agent deployment, org restructure. |

#### How Approvals Appear in the Dashboard

Navigate to **Approvals** (`/escalations`). The left-hand pane shows **Pending Approvals**.

Each approval card displays:

| Element | Description |
|---------|-------------|
| **Action** | What the agent wants to do (e.g., `edit`, `bash`, `deploy_agent`). |
| **Agent** | The agent requesting approval. |
| **Description** | The full detail of what the action will affect. |
| **Risk level** | Low / medium / high — shown as a colored badge. |
| **Cost estimate** | Estimated LLM cost for the action. |
| **Tier badge** | `[T0]` through `[T4]` — indicates the approval tier. |
| **SLA timer** | Time remaining before the request expires and escalates. |
| **Timestamp** | When the approval was requested. |

[Screenshot: Pending Approvals pane with three approval cards showing different tiers — Approvals Page]

#### Approve/Reject Workflow

**To approve a request:**

1. Read the approval card carefully — check the action, agent, description, and risk level.
2. Optionally click **Edit** to adjust the risk level or cost estimate before deciding.
3. Click the green **Approve** button.
4. The request is marked as approved, and the agent is notified. The agent proceeds with the action.

**To reject a request:**

1. Click the red **Reject** button.
2. The request is marked as rejected, and the agent is notified with the rejection reason.
3. The agent will not perform the action.

**For Tier 3 (Dual Approve) requests:**

- Two different operators must approve the request.
- After the first approval, the card updates to show "1 of 2 approvals" — it stays in the queue until the second approver acts.
- The same operator cannot approve twice. If you try, the system rejects the duplicate signature.

**For Tier 4 (CEO Only) requests:**

- Only the CEO can approve. If you are not the CEO, you will see a lock icon and the request cannot be actioned by you.
- Tier 4 requests timeout after 24 hours. On timeout, the board is notified, but the request remains in the CEO's queue with an `[EXPIRED]` badge — it never auto-resolves.

#### What Happens After Approval

1. The approval request status changes from `pending` to `approved`.
2. The agent's execution loop detects the status change and proceeds with the action.
3. The action is executed and logged in the audit trail.
4. If the action was part of a task, the task advances in its lifecycle (e.g., from In Progress to Done).

If the request times out without action:

1. The status changes to `escalated`.
2. A new approval request is created at the next tier (e.g., Tier 2 → Tier 3).
3. The original request's `escalated_from` field points to the new request.
4. The agent's poll loop re-attaches to the new request and continues waiting.

> **Tip:** Check the Approvals page at least twice a day. Tier 2 requests time out in 60 minutes — if you miss them, they escalate to Tier 3, which requires two approvers and has a shorter 30-minute window. Clearing approvals promptly keeps the pipeline moving.

> **Tip:** You can adjust the risk level and cost estimate on any approval before deciding. This is useful when you have context the agent doesn't — for example, you know a code change is in a low-risk area even though the agent classified it as high risk.

---

### Real-Time Updates

The dashboard uses a persistent WebSocket connection to push live updates to your browser without requiring a page refresh. This is what makes the dashboard feel alive.

#### How WebSocket Updates Work

When the dashboard loads, the browser opens a WebSocket connection to `ws://host/ws/v1/dashboard`. This connection stays open for the duration of your session. The server pushes messages to you whenever something changes in the backend.

The top-right corner of every page shows the connection status:
- **Live** (green dot + text) — WebSocket is connected. You're seeing real-time data.
- **Offline** (red dot + text) — WebSocket is disconnected. Data may be stale. The dashboard falls back to polling every 15 seconds, but real-time events won't arrive.

If the connection drops, the dashboard automatically reconnects using exponential backoff (up to 30 seconds). A heartbeat ping/pong runs every 25 seconds to detect dead connections.

#### What the Update Topics Mean

The WebSocket broadcasts messages on named topics. Each topic corresponds to a specific type of data change:

| Topic | What It Pushes | Where You See It |
|-------|---------------|-----------------|
| **`kpis`** | Updated KPI snapshots from all department collectors. | KPI cards update in place. Numbers and charts change without a page refresh. |
| **`tasks`** | Task lifecycle events — creation, status change, assignment, completion, failure. | Kanban board columns update. Task cards appear, move, or disappear in real time. |
| **`escalations`** | New escalation events and resolution confirmations. | Escalation count badge updates. New escalation cards appear in the Approvals page. |
| **`approvals`** | New approval requests and approval/rejection decisions. | Approval cards appear or disappear. Pending count updates. |
| **`daemon`** | Background daemon status — task execution progress, health checks. | Command Center status indicators. |
| **`org_health`** | Organizational health score updates and component metric changes. | Org Health Score gauge on the Dashboard page. Component metric cards update. |

#### What You'll Notice in the UI

- **Live counters** — Numbers like "Pending Tasks: 12" update automatically. You never need to refresh to see the current count.
- **Badge updates** — The red badge on the **Approvals** tab increments when a new approval arrives and decrements when one is resolved.
- **Toast notifications** — Bottom-right popups for critical events: new escalations, approval requests, and alerts. These appear even if you're on a different page.
- **Escalation toasts** — Top-right stacked notifications for real-time escalation events. These are separate from the generic toast system and are specifically designed for escalation awareness.
- **Chart updates** — Charts on the KPIs page update in place using `chart.update('none')` — no flicker, no destroy/recreate.

> **Tip:** If you notice numbers aren't updating or the WebSocket indicator shows "Offline," press `Ctrl + K`, type "tasks" (or any page name), and press Enter. This forces a full page reload and re-establishes the WebSocket connection.

---

### Mobile Usage (PWA)

The CEO Dashboard is a Progressive Web App (PWA) that you can install on your phone or tablet for a native-app experience.

#### Installing the PWA

**On iOS (Safari):**

1. Open the dashboard URL in Safari.
2. Tap the **Share** button (square with arrow).
3. Scroll down and tap **Add to Home Screen**.
4. Name it "CEO Dashboard" and tap **Add**.

**On Android (Chrome):**

1. Open the dashboard URL in Chrome.
2. Tap the three-dot menu in the top-right.
3. Tap **Add to Home Screen** or **Install App**.
4. Confirm the installation.

**On Desktop (Chrome/Edge):**

1. Open the dashboard URL.
2. Click the install icon in the address bar (monitor with a plus sign).
3. Click **Install**.

The PWA installs as a standalone app with its own window, no browser chrome, and a custom icon on your home screen.

[Screenshot: Dashboard installed as PWA on iPhone showing the task board — Mobile PWA]

#### What Works on Mobile

The mobile layout adapts the desktop dashboard for touch interaction:

| Feature | Mobile Support |
|---------|---------------|
| **Kanban board** | Columns stack vertically. Drag-and-drop works with touch (tap, hold, drag). |
| **Approvals** | Full approve/reject/edit functionality. Cards are touch-friendly with larger tap targets. |
| **Escalations** | Full resolve functionality. Escalation cards display all details. |
| **KPIs** | Charts and metric cards render responsively. Swipe to scroll through department views. |
| **Command Bar** | Opens via `Ctrl + K` (or the on-screen menu button on mobile). |
| **Notifications** | Push notifications via the service worker (if permitted by the OS). |
| **Real-time updates** | WebSocket connection works on mobile browsers. Live updates arrive the same as on desktop. |

#### Offline Mode

The PWA includes a service worker that caches the dashboard's static assets (HTML, CSS, JavaScript). If you lose connectivity:

1. The dashboard continues to load from the local cache.
2. Data shown is from the last successful fetch — it may be stale.
3. Any actions you take (approving, creating tasks, resolving escalations) are added to an **offline action queue**.
4. The WebSocket indicator shows "Offline" and an amber pulsing dot appears in the navigation bar.

#### Sync Behavior

When connectivity is restored:

1. The offline action queue badge appears in the navigation bar showing the count of queued actions.
2. Actions are replayed against the server in order.
3. The system performs **conflict resolution** — if the data has changed since you went offline, you'll see a conflict notification explaining what changed and how your action was handled.
4. Once all queued actions sync successfully, the badge disappears and the WebSocket indicator returns to "Live."

> **Tip:** If you see the offline queue badge with a number, don't worry — your actions are saved and will sync automatically. You don't need to do anything. If you want to review what's queued, tap the badge to see the pending actions list.

> **Tip:** The PWA is especially useful for end-of-day checks when you're away from your desk. Install it on your phone so you can quickly approve pending requests or resolve escalations without opening a laptop.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 — Draft | 2026-08-26 | Chief Operating Officer | Initial draft of Day-to-Day Operations and Task Management sections. |

---

*End of operations and task management section. Continue to [Section 5 — Working with Agents](05-working-with-agents.md) for agent roster management, or return to the [Table of Contents](00-outline-and-executive-summary.md#table-of-contents).*
