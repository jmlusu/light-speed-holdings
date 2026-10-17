# Quick Start Guide & Reference

This section gets you from zero to productive in under ten minutes. It covers first-time setup, a guided tour of what you see after login, the most common daily workflows, a glossary of every dashboard term, and answers to the questions people ask most.

---

## Quick Start Guide

### Prerequisites

Before you begin, make sure you have:

- **Python 3.12 or newer** installed on your machine
- **uv** package manager installed (`pip install uv` if you don't have it)
- Access to the Light Speed Holdings Git repository

### First-Time Setup

✅ **Step 1 — Clone the repository**

Open a terminal and clone the repo to your machine:

```bash
git clone https://github.com/light-speed-holdings/ai-company-builder.git
cd ai-company-builder
```

You should see the project files in your terminal's working directory.

---

✅ **Step 2 — Install dependencies**

Run the sync command to install all required packages and create a virtual environment:

```bash
uv sync --extra dev
```

This creates a `.venv` folder and installs everything the dashboard needs. It takes about one to two minutes on a fresh install.

---

✅ **Step 3 — Copy the environment template**

Copy the example environment file and open it in your text editor:

```bash
cp .env.example .env
```

The `.env` file holds your secret keys and configuration. It is gitignored, so it never gets committed to version control.

---

✅ **Step 4 — Configure your RBAC keys**

Open `.env` and set your role-based access keys. At minimum, fill in these three lines:

```
DASHBOARD_ADMIN_KEY=your_secret_admin_key_here
DASHBOARD_APPROVE_KEY=your_secret_approve_key_here
DASHBOARD_RUN_KEY=your_secret_run_key_here
```

> 💡 **Tip:** These keys control what you can do on the dashboard. The **admin** key gives full access. The **approve** key lets you approve tasks and resolve escalations. The **run** key is read-only for monitoring. Pick strong, unique values for each.

> ⚠️ **Warning:** Never commit your `.env` file to Git. It contains secrets.

---

✅ **Step 5 — Start the dashboard**

Launch the dashboard server with:

```bash
ai-company dashboard
```

Or, if your environment isn't activated yet:

```bash
uv run ai-company dashboard
```

You'll see log output confirming the server is running. The dashboard automatically opens in your default browser. If it doesn't, go to **http://localhost:8420** manually.

---

✅ **Step 6 — Authenticate with your role key**

When the dashboard loads, you'll be prompted to authenticate. Paste the value of the RBAC key that matches your role (admin, approve, or run) into the authentication field. The dashboard stores your session locally so you don't need to re-enter it every visit.

---

✅ **Step 7 — Verify the connection**

Look at the **top-right corner** of the header bar. You should see a **green pulsing dot** with the word **Live**. This means your browser has an active WebSocket connection to the server and you're receiving real-time updates.

> 💡 **Tip:** If the dot is red and says **Offline**, check that the server is still running in your terminal and that you're connected to the same network.

---

✅ **Step 8 — Bookmark the dashboard**

Press **Ctrl + D** (or **Cmd + D** on Mac) to bookmark the dashboard in your browser. The Command Center page at `http://localhost:8420` is your home base.

---

✅ **Step 9 — Explore the navigation tabs**

Across the top of the page, you'll see a row of tabs: **Dashboard**, **Agents**, **Tasks**, **KPIs**, **Costs**, **Approvals**, **Command Center**, **Mission Control**, **Onboarding**, **Finance**, and **Org Chart**. Click any tab to navigate. The active tab is highlighted with a cyan underline.

---

✅ **Step 10 — Try the command bar**

Press **Ctrl + K** to open the command bar. Type "tasks" or "agents" or any page name. Use the arrow keys to navigate results and press **Enter** to jump there. Press **Esc** to close it. This is the fastest way to get around.

---

### Your First Look

Now that you're logged in, here's what to do in your first two minutes:

1. **Check the Org Health Score.** On the Dashboard home page, you'll see a large circular gauge in the center. The number inside (0–100) is your organization's overall health. Green (80+) means everything is running smoothly. Amber (50–79) means some areas need attention. Red (below 50) means there are critical issues to address.

2. **Look at the alerts bar.** Directly below the gauge, three numbers tell you at a glance: pending approvals (amber), open escalations (red), and in-progress tasks (blue). If any of these are above zero, those are your first items to investigate.

3. **Open the Command Center.** Click the **Command Center** tab. This is your war-room view. The animated arc reactor in the center shows real-time system health. The Executive Briefing panel on the left lists anything requiring your attention. The AI Workforce panel on the right shows every agent and its current status.

4. **Check the sidebar navigation.** On desktop, your navigation lives in a horizontal tab bar below the header. On mobile, it collapses into a menu. Either way, every page is one click or tap away.

5. **Watch for live updates.** Leave the dashboard open for a few minutes. Numbers update automatically via WebSocket. New tasks appear, KPI values change, and alerts pop in — all without you refreshing the page.

---

## Common Workflows

These step-by-step routines cover the tasks you'll perform most often.

### Morning Check-In

A five-minute daily routine to understand the state of the organization.

✅ **Step 1 — Open the Dashboard home page.**

Check the **Org Health Score** gauge. Note whether it's green, amber, or red. If it dropped since yesterday, that's your first signal that something changed overnight.

✅ **Step 2 — Read the alerts bar.**

Look at the three alert counts below the gauge: pending approvals, open escalations, and in-progress tasks. If any are elevated, that's where you'll focus today.

✅ **Step 3 — Open the Command Center.**

Click the **Command Center** tab. Scan the **Executive Briefing** panel for high-priority items. These are pulled from across the system and ranked by urgency.

✅ **Step 4 — Check the AI Workforce panel.**

In the right-hand panel, scan the agent list. Red status dots mean an agent is blocked or escalated. Amber means it's waiting. Blue means it's actively working. Green means it's online and available.

✅ **Step 5 — Glance at the KPIs tab.**

Click the **KPIs** tab. The System Health Monitor at the top shows component scores across all departments. Any card in red needs attention. Check the anomaly detection section for anything unusual.

✅ **Step 6 — Review pending approvals.**

Click the **Approvals** tab. If there are pending approval cards, review and approve or reject them. Morning is the best time to clear the queue so agents aren't blocked.

✅ **Step 7 — Note any trends.**

On the KPIs page, click the **7d** button on the Org Health Trend chart. Look for any downward slope that's been building over the past week. This tells you whether today's issues are new or part of a pattern.

---

### Approving a Task

When an agent requests permission to perform an action, you'll see it as a pending approval.

✅ **Step 1 — Navigate to the Approvals page.**

Click the **Approvals** tab (or press **Ctrl + K** and type "approvals"). The left column shows all pending approval requests.

✅ **Step 2 — Read the approval card.**

Each card shows: the action name, which agent requested it, a description of what it wants to do, the risk level (low/medium/high), and an estimated cost. Read the description carefully.

✅ **Step 3 — Adjust risk or cost if needed (optional).**

Click the **Edit** button on the card. You can change the risk level and cost estimate before approving. Click **Save** when done. This is useful when the agent's estimate is off.

✅ **Step 4 — Approve or reject.**

Click the green **Approve** button to let the agent proceed. Click the red **Reject** button if the request shouldn't happen. Once you click, the card disappears from the list and the agent is notified.

> 💡 **Tip:** Escalation notifications appear as toast pop-ups in the top-right corner on *every* page, so you never miss a request even if you're on a different tab.

---

### Investigating an Escalation

When an agent encounters something it can't handle on its own, it escalates to a human. Here's how to investigate.

✅ **Step 1 — Notice the escalation notification.**

An amber toast notification appears in the top-right corner with the escalation reason and the from → to agent flow. Click **Resolve** directly from the toast, or click the **Approvals** tab to see all open escalations in the right column.

✅ **Step 2 — Read the escalation card.**

Each card shows the rule that triggered it, which agent escalated and to whom, the reason text, and when it happened. Read the reason carefully — it tells you what the agent was trying to do and why it couldn't proceed.

✅ **Step 3 — Check the Tasks tab for context.**

Click the **Tasks** tab and look at the **Escalated** column at the bottom of the Kanban board. Click the escalated task card to open the detail panel. The full instruction, assigned agent, and task history are there.

✅ **Step 4 — Decide on a resolution.**

Depending on the situation, you can: reassign the task to a different agent (click **Reassign** in the task detail panel), edit the task's priority, or decompose it into smaller subtasks by clicking **Decompose**.

✅ **Step 5 — Mark the escalation as resolved.**

Return to the **Approvals** tab and click the **Resolve** button on the escalation card. This clears it from the queue and signals to the system that human intervention is complete.

---

### Reviewing KPI Trends

KPIs tell you how each department is performing over time. Here's how to read them.

✅ **Step 1 — Navigate to the KPIs page.**

Click the **KPIs** tab. The System Health Monitor at the top shows a row of component metric cards, one per department. Each card shows the current score as a large percentage with a color-coded progress bar.

✅ **Step 2 — Read the component scores.**

Green (80% and above) means the department is healthy. Amber (50–79%) means there are gaps. Red (below 50%) means a critical issue. Look at the change indicator (up or down arrow) to see if the score is improving or declining.

✅ **Step 3 — Check the Org Health Trend chart.**

Below the component cards, the trend chart shows the composite health score over time. Use the **6h**, **24h**, or **7d** buttons to change the time window. A steady upward line means things are improving. A downward slope means you should investigate.

✅ **Step 4 — Explore a specific department.**

Scroll down to the **Department KPIs** section and click a department tab (for example, **Engineering** or **Sales**). You'll see KPI summary cards for that department, a comparison chart, and a targets-vs-actual chart. This tells you exactly where the department stands against its goals.

✅ **Step 5 — Check for anomalies.**

Between the component cards and the trend chart, look for the **Anomaly Detection** section (it only appears when anomalies are present). Each anomaly has a severity level and timestamp. Red anomalies are the most urgent.

---

### Checking Dashboard Health

A quick health verification you can run anytime.

✅ **Step 1 — Look at the connection indicator.**

In the top-right corner of the header bar, the WebSocket status dot should be **green and pulsing** with "Live" next to it. This means real-time updates are flowing.

✅ **Step 2 — Check the health endpoint.**

If you have terminal access, run:

```bash
curl http://localhost:8420/health
```

A healthy response returns a JSON object with `"status": "ok"`. This endpoint requires no authentication.

✅ **Step 3 — Verify KPI auto-refresh.**

Navigate to the **KPIs** tab and make sure **Auto-refresh: ON** is displayed in the System Health Monitor header. If it says OFF, click the toggle to turn it on. The spinning indicator confirms live updates are active.

✅ **Step 4 — Check the Command Center arc reactor.**

Open the **Command Center** tab. The arc reactor ring color tells you system health at a glance: green (80%+), amber (50–79%), or red (below 50%). The percentage in the center is the composite health score.

---

## Glossary

| Term | Definition |
|------|------------|
| **Approval Gate** | A security checkpoint that pauses agent actions until a human reviews and approves them. This prevents agents from taking high-risk actions without oversight. |
| **Command Bar** | A universal search and navigation tool available on every page. Open it with **Ctrl + K** to quickly jump to any page, search for agents or tasks, or run quick actions. |
| **Command Center** | The real-time strategic overview page. It shows an animated arc reactor visualization of system health, an executive briefing of priority items, the full AI workforce roster, and model performance telemetry. |
| **Daemon** | A background process that keeps the dashboard and its services running continuously. It handles scheduled tasks, periodic health checks, and maintenance operations without requiring manual intervention. |
| **Dashboard** | The CEO Dashboard itself — a web-based application that aggregates real-time data from across the company (agents, tasks, finances, KPIs, escalations) and displays it in a unified, interactive interface. |
| **Escalation** | When an agent encounters a situation it cannot resolve autonomously, it escalates the issue to a human for intervention. Escalations appear on the Approvals page and as toast notifications across the dashboard. |
| **HITL (Human-in-the-Loop)** | A workflow pattern where AI agents perform work autonomously but require human approval at key decision points. The approval tiers (T1 through T4) control how much oversight each agent receives. |
| **Inbox** | A JSON-based task queue (`.opencode/inbox.json`) where the orchestrator dispatches tasks to agents. Agents pick up work from the inbox and return results when complete. |
| **JARVIS Theme** | The dark, command-center-inspired visual design of the dashboard. It uses a dark background with cyan, amber, and red accents — inspired by the JARVIS interface from popular culture. |
| **Kanban** | A visual task-management board where work flows through columns representing stages: Pending, In Progress, Completed, Failed, and Escalated. Tasks are cards that you can drag between columns. |
| **KPI (Key Performance Indicator)** | A measurable value that shows how effectively a department or the organization is achieving its goals. Each KPI has a current value, a target, and a status (on track, below target, or above target). |
| **KPI Collector** | An automated component that gathers raw operational data and calculates KPI values for a specific department. There are collectors for Engineering, Sales, Marketing, Finance, HR, Legal, Operations, and Customer Success. |
| **MessageBus** | The internal communication system that routes tasks, events, and messages between the orchestrator, agents, and the dashboard. It powers real-time updates and task dispatching. |
| **Mission Control** | The strategic operations page combining an Org Health hero visualization with a workflow pipeline engine for managing multi-step business processes like onboarding, approvals, and delivery stages. |
| **Org Health Score** | A composite number (0–100) that summarizes the overall health of the organization. It is a weighted average of departmental sub-scores. Green means healthy (80+), amber means attention needed (50–79), and red means critical (below 50). |
| **PWA (Progressive Web App)** | A web application that can be installed on your phone or desktop like a native app. It works offline by queuing actions and syncing them when connectivity returns. |
| **RBAC (Role-Based Access Control)** | A security system that controls what each user can do based on their assigned role key. Admin keys get full access, approve keys can approve and resolve, and run keys are read-only. |
| **Service Worker** | A background script that the PWA uses to cache assets and handle offline functionality. It intercepts network requests and serves cached content when the server is unreachable. |
| **SLA (Service Level Agreement)** | A time commitment for how quickly a task or workflow step should be completed. The Mission Control pipeline shows a countdown timer for each step's SLA. |
| **Sprint** | A time-boxed period (typically one to two weeks) during which a team completes a set amount of work. Sprint data feeds into engineering and operations KPIs. |
| **WebSocket** | A persistent, two-way communication channel between your browser and the dashboard server. It enables real-time updates — KPI changes, new tasks, escalation alerts — to appear instantly without page refreshes. |
| **York** | The orchestration engine that coordinates agent workflows, manages task lifecycles, and enforces governance rules like approval gates and escalation policies. |

---

## Frequently Asked Questions

### How do I log in?

Open the dashboard in your browser at **http://localhost:8420**. You'll be prompted to authenticate. Paste the value of the RBAC key that matches your role (admin, approve, or run). Your session is stored locally, so you typically only need to do this once per browser.

---

### What do the green/amber/red colors mean?

These colors appear throughout the dashboard and always mean the same thing:

- 🟢 **Green** — Healthy, on track, or performing well. No action needed.
- 🟡 **Amber** — Warning or attention needed. Something is degraded or approaching a threshold.
- 🔴 **Red** — Critical issue requiring immediate attention. Something has failed or is well below target.

You'll see these colors on the Org Health Score gauge, KPI progress bars, escalation notifications, cost budget indicators, and agent status dots.

---

### Why are some KPIs showing null?

A null value means the KPI collector hasn't gathered data for that metric yet. This is normal for newly added KPIs or when a department hasn't produced enough operational data to calculate a meaningful value. The KPI will populate once sufficient data is available. If a KPI stays null for more than 24 hours, check the KPIs page for anomalies or contact your technical administrator.

---

### How do I approve a task?

Navigate to the **Approvals** tab. You'll see a "Pending Approvals" column on the left with approval cards. Each card describes what the agent wants to do, the risk level, and the estimated cost. Click the green **Approve** button to allow it, or the red **Reject** button to deny it. You can click **Edit** first to adjust the risk or cost estimate before approving.

---

### Can I use the dashboard on my phone?

Yes. The dashboard is a Progressive Web App (PWA). Open **http://localhost:8420** in your phone's browser, then use your browser's "Add to Home Screen" option to install it. The mobile layout automatically adapts — columns stack vertically, the Kanban board becomes single-column, and navigation collapses into a menu. You'll also get offline support: if your connection drops, actions are queued and sync automatically when you reconnect.

---

### What if the dashboard is slow?

Try these steps in order:

1. **Check the WebSocket indicator** in the top-right corner. If it's red (Offline), the real-time connection is down and the dashboard is falling back to polling, which is slower. Refreshing the page usually reconnects it.
2. **Close unused browser tabs.** Each open tab maintains its own WebSocket connection. Multiple tabs can compete for resources.
3. **Check system resources.** The dashboard is lightweight, but if your machine is running low on memory or CPU, performance may degrade.
4. **Verify the server is healthy.** Run `curl http://localhost:8420/health` from a terminal. If it returns `"status": "ok"`, the server is fine and the issue is likely on the browser side. Try clearing your browser cache.
5. **Check budget alerts on the Costs page.** If LLM costs are spiking, the system may be under heavy load from agent activity.

---

### How do I check if the system is healthy?

Three quick checks:

1. **The WebSocket status dot** in the top-right corner should be green and pulsing with "Live" next to it.
2. **The Org Health Score** on the Dashboard home page should be green (80 or above). If it's amber or red, click the gauge to drill into which department is dragging the score down.
3. **The health endpoint** responds to `curl http://localhost:8420/health` with `"status": "ok"`. This requires no authentication and works even if the dashboard UI has issues.

---

### What is the command bar?

The command bar is a universal search and navigation tool. Press **Ctrl + K** (or **Cmd + K** on Mac) from any page to open it. Type to search for agents, tasks, pages, or actions. Results appear as you type, grouped by type. Use the arrow keys to navigate and **Enter** to select. Press **Esc** to close it. It's the fastest way to get anywhere in the dashboard.

---

### How do I report a problem?

If something looks wrong on the dashboard:

1. **Check the connection status** first (green = connected, red = disconnected).
2. **Refresh the page** to rule out a stale session.
3. **Check the health endpoint** (`curl http://localhost:8420/health`) to see if the server is responding.
4. **Look at the API Status Banner** in the bottom-left corner. If a background request failed, an amber banner appears with the error description.
5. **Contact your technical administrator** with details about what you saw, which page it was on, and the time it happened. Include any error messages from the API Status Banner.

---

### Where can I learn more?

This user guide has additional sections covering every page in detail:

- **Page-by-Page Guide** — Deep dives into every dashboard page
- **Real-Time Features** — How WebSocket updates work
- **Mobile and PWA** — Installing and using the dashboard on your phone
- **Security and Access** — Understanding RBAC roles and key rotation
- **Troubleshooting** — Fixing common issues
- **Appendix** — Keyboard shortcuts and quick-reference cards

You can also press **Ctrl + K** and type "docs" to jump between guide sections while reading.

---

## Tips and Shortcuts

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl + K** | Open the command bar |
| **Esc** | Close the command bar, modals, or slide-out panels |
| **Tab** | Move focus to the next interactive element |
| **Shift + Tab** | Move focus to the previous element |
| **Ctrl + 1** | Switch to Command Center layout "The Bridge" |
| **Ctrl + 2** | Switch to Command Center layout "The War Room" (default) |
| **Ctrl + 3** | Switch to Command Center layout "The Cockpit" |
| **Ctrl + D** | Bookmark the current page in your browser |

### Hidden Features

- **Org Health drill-down:** Click the health gauge on the Dashboard home page to expand a 2x2 component grid. Click any component card to see its detailed score breakdown and weight in the composite.
- **Offline queue:** If you lose connectivity, an amber banner appears at the top. Click the badge in the tab bar to see queued actions that will sync when you reconnect.
- **Command bar voice input:** On compatible browsers, the command bar has a microphone button for voice input.
- **Scroll preservation:** When real-time updates arrive, the dashboard saves and restores your scroll position so you never lose your place.
- **Approval editing:** Before approving a task, click **Edit** to adjust the risk level and cost estimate — useful when the agent's calculation is off.
- **Task decomposition:** In the task detail panel, click **Decompose** to break a large task into smaller subtasks with their own progress tracking.

### Power-User Tricks

- **Morning routine in 60 seconds:** Open Dashboard → check Org Health gauge → check alerts bar → open Approvals → clear the queue → done.
- **Fastest navigation:** Press **Ctrl + K**, type the first three letters of any page name, press **Enter**. You're there.
- **Multi-tab workflow:** Keep the Dashboard home page open in one tab and the Approvals tab in another. Escalation notifications appear on both.
- **7-day trend check:** On the KPIs page, click the **7d** button on the Org Health Trend chart to see weekly patterns. A gradual downward slope is more concerning than a single-day dip.
- **Budget watch:** On the Costs page, switch between **Daily** / **Weekly** / **Monthly** to spot cost spikes at different time scales.

---

*Proceed to [Section 3 — Page-by-Page Guide](05-page-by-page-guide.md) for detailed instructions on every dashboard page, or jump to [Section 17 — Glossary](#glossary) for quick term definitions.*
