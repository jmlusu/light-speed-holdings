# CEO Dashboard User Guide — Light Speed Holdings

**Version:** 1.0 — Draft
**Last Updated:** 2026-08-26
**Document Owner:** Chief of Staff

---

## Document Purpose

This guide provides comprehensive, role-aware instructions for every person who interacts with the CEO Dashboard — from first-time onboarding through daily operational workflows. It is designed to be the single authoritative reference for navigating the dashboard, understanding its data, and performing actions within your authorized role.

---

## Target Audience

This guide is written for four primary audiences:

- **CEO and executive leadership** — who need high-level visibility into organizational health, strategic goal progress, and financial performance without wading into technical configuration.
- **COO and operations managers** — who use the dashboard daily to monitor task throughput, manage escalations, and coordinate across departments.
- **Technical administrators** — who are responsible for initial setup, authentication configuration, deployment, and ongoing maintenance of the dashboard infrastructure.
- **New users** — anyone joining the organization who needs to get oriented quickly and start using the dashboard with confidence.

---

## Table of Contents

| Section | Title | Description |
|---------|-------|-------------|
| 1 | **Getting Started** | How to access the dashboard, initial login, and your first look around. |
| 2 | **Dashboard Overview** | The layout, navigation, JARVIS theme, and how all the pages connect. |
| 3 | **The Command Center** | Your real-time headquarters — org health gauges, alerts, and the briefing panel. |
| 4 | **Managing Tasks** | The Kanban board: creating, assigning, dragging, and tracking tasks through completion. |
| 5 | **Working with Agents** | Viewing the agent roster, checking agent status, understanding roles and capabilities. |
| 6 | **KPIs and Analytics** | Reading charts, selecting time ranges, switching department views, and interpreting trends. |
| 7 | **Finance and Costs** | Financial metrics, cost breakdowns, trend analysis, and budget monitoring. |
| 8 | **Escalations** | How escalations surface, the resolution workflow, and your role in clearing them. |
| 9 | **Org Chart** | Visualizing the organizational hierarchy and understanding reporting lines. |
| 10 | **Mission Control** | Strategic overview, goal tracking, and how operational work ladders up to company objectives. |
| 11 | **Onboarding Wizard** | Step-by-step setup for new users: preferences, notification config, and orientation. |
| 12 | **Real-Time Features** | How WebSocket updates work, what topics are available, and keeping your view live. |
| 13 | **Mobile and PWA** | Installing the dashboard on your phone, offline capabilities, and the action queue. |
| 14 | **Security and Access** | RBAC roles (admin, approve, run), what each role can do, and key rotation. |
| 15 | **Common Workflows** | Step-by-step walkthroughs for the most frequent operational tasks. |
| 16 | **Troubleshooting** | What to do when something looks wrong, stale, or unresponsive. |
| 17 | **Glossary** | Definitions of every term, abbreviation, and metric name used in this guide. |
| 18 | **Appendix** | Keyboard shortcuts, environment variables, and quick-reference cards. |

---

## Executive Summary

The CEO Dashboard is the operational nerve center of Light Speed Holdings. It is a web-based application that aggregates real-time data from every layer of the company — agent activity, task throughput, financial performance, KPI trends, and strategic goal progress — and presents it in a single, unified interface. Built on a FastAPI backend with an Alpine.js and Tailwind CSS frontend, the dashboard uses a distinctive dark "JARVIS" theme inspired by modern command-center interfaces. It runs locally or on a server, accessible through any modern browser on desktop or mobile.

The dashboard exists because Light Speed Holdings operates a complex hierarchy of AI agents across multiple departments, and keeping the full picture in your head is no longer feasible. Without centralized visibility, bottlenecks go unnoticed, escalations sit unresolved, and costs drift without accountability. The CEO Dashboard solves this by pulling together task management, agent monitoring, financial tracking, KPI analytics, and escalation management into one place — updated in real time through a persistent WebSocket connection. It replaces fragmented CLI commands and manual log-diving with a living, breathing view of the entire organization.

For executives, the Command Center and Mission Control pages provide an at-a-glance health check: an organizational health score, alert feeds, goal progress, and strategic summaries. For operations managers, the Tasks and Escalations pages are where daily work happens — triaging incoming work, resolving blocked items, and keeping the pipeline moving. For technical administrators, the Onboarding Wizard and security configuration ensure the dashboard is deployed correctly, authenticated properly, and accessible to the right people with the right permissions. Every page is designed to answer the question "What do I need to know right now?" without requiring you to dig.

To get started, open the dashboard in your browser at the URL provided by your technical administrator (by default, `http://localhost:8420`). If this is your first time, the Onboarding Wizard will guide you through initial setup. From there, the Command Center is your home base — bookmark it, and return to it throughout the day. Use the left-hand navigation to move between pages as your role requires. The dashboard updates automatically, so the numbers you see are always current. If you want a deeper dive into any specific area, navigate to the corresponding section of this guide using the table of contents above.

---

## How to Use This Guide

Not every section of this guide is relevant to every reader. The matrix below maps each role to the sections most useful to them.

| Section | CEO | COO | Tech Admin | New User |
|---------|:---:|:---:|:----------:|:--------:|
| 1 — Getting Started | | | ● | ● |
| 2 — Dashboard Overview | ● | ● | ● | ● |
| 3 — Command Center | ● | ● | | |
| 4 — Managing Tasks | | ● | | ● |
| 5 — Working with Agents | | ● | ● | |
| 6 — KPIs and Analytics | ● | ● | | |
| 7 — Finance and Costs | ● | | | |
| 8 — Escalations | | ● | | |
| 9 — Org Chart | ● | ● | | ● |
| 10 — Mission Control | ● | | | |
| 11 — Onboarding Wizard | | | ● | ● |
| 12 — Real-Time Features | | ● | ● | |
| 13 — Mobile and PWA | ● | ● | ● | ● |
| 14 — Security and Access | | | ● | ● |
| 15 — Common Workflows | ● | ● | ● | ● |
| 16 — Troubleshooting | | | ● | ● |
| 17 — Glossary | ● | ● | ● | ● |
| 18 — Appendix | | ● | ● | |

**How to read this matrix:**
- **●** = recommended reading for this role.
- Empty cell = this section exists but is not a priority for this role.
- Everyone should read Sections 2 and 15 regardless of role.

---

## Guide Conventions

This guide uses the following visual conventions and notation throughout:

### Callout Boxes

- **Tip** — A shortcut, best practice, or optional enhancement that improves your experience.
- **Warning** — An action that could cause data loss, disrupt other users, or produce unintended consequences. Read carefully before proceeding.
- **Note** — Additional context or clarification that supplements the surrounding text.

### Keyboard Shortcuts

Keyboard shortcuts are displayed in this format: **Ctrl + K** — meaning press and hold the first key, press the second key, then release both.

### Navigation Paths

When this guide tells you to navigate somewhere, the path is shown with right-pointing arrows: **Dashboard → Tasks → Create Task** means click "Dashboard" in the navigation bar, then click "Tasks" in the sidebar, then click the "Create Task" button.

### Button and Menu References

Interactive elements like buttons, tabs, and dropdown menus are shown in **bold** to distinguish them from surrounding text.

### Icons

- 🟢 Green — Healthy, nominal, or completed state.
- 🟡 Yellow — Warning, degraded, or attention needed.
- 🔴 Red — Critical, failed, or requires immediate action.
- ⚡ Lightning — Real-time or live-updating element.
- 📊 Chart — Analytics or visualization content.

### Data Values

Metric values, percentages, and scores appear exactly as they would on the dashboard — for example, "Org Health Score: 82" — so you can cross-reference what you read here with what you see on screen.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 — Draft | 2026-08-26 | Chief of Staff | Initial outline and executive summary. |

> This is a living document. As dashboard features evolve, this guide will be updated to reflect new capabilities, changed workflows, and revised screenshots. The "Last Updated" date at the top of this file is the authoritative version stamp.

---

*End of outline and executive summary. Proceed to [Section 1 — Getting Started](01-getting-started.md) for onboarding instructions, or jump to any section using the table of contents above.*


---

# Section Separator

---

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


---

# Section Separator

---

# Understanding Your KPIs

**Version:** 1.0 — Draft
**Last Updated:** 2026-08-26
**Document Owner:** Chief of Staff

---

## Understanding Your KPIs

This section explains every metric on the KPIs page — what it measures, what "good" looks like, and what to do when numbers move. You do not need to understand the underlying data collection to use this page effectively. Think of it as your organizational vital signs monitor: each metric tells you something specific about the health of one part of the company, and together they paint the full picture.

---

### The Org Health Score

Your **Org Health Score** is a single number between 0 and 100 that summarizes the overall operational condition of the company. Think of it like a credit score for your organization — one composite number that aggregates multiple signals into a quick, actionable read.

The score is composed of four weighted components, each drawn from live operational data:

| Component | Weight | What It Measures |
|-----------|--------|------------------|
| **Task Success Rate** | 30% | The percentage of tasks completed successfully out of all tasks in the 30-day window. This is the single largest signal — if work is getting done reliably, the organization is healthy. |
| **Agent Utilization** | 25% | The percentage of registered agents that have been active (sent or received at least one task) in the last 30 days. Low utilization means resources are idle; very high utilization may signal capacity strain. |
| **Cost Efficiency** | 25% | How well actual spending aligns with budget. This is inverted so that higher scores mean lower budget consumption relative to plan — staying under budget scores well, going over scores poorly. |
| **Error Rate** | 20% | The inverse of the failure rate across all agent operations. Fewer failed, errored, or cancelled tasks means a higher score. This catches systemic reliability issues before they compound. |

#### How to Read the Score

The score maps to three color bands that give you an instant read:

| Band | Score Range | What It Means | Recommended Action |
|------|-------------|---------------|-------------------|
| 🟢 **Green** | 80 – 100 | The organization is operating well. Tasks are completing, agents are active, costs are managed, and errors are rare. | **Monitor.** Continue your regular review cadence. Look for optimization opportunities, not fire drills. |
| 🟡 **Amber** | 50 – 79 | Something needs attention. One or more components are underperforming. The organization is functional but degraded. | **Investigate.** Open the department view for the declining component. Identify which metric is pulling the score down and delegate a corrective action to the responsible department head. |
| 🔴 **Red** | 0 – 49 | The organization is in a critical state. Multiple components are failing or data is severely degraded. Immediate intervention is required. | **Escalate.** Treat this as an incident. Review the component breakdown, check the Escalations page for blocked items, and convene the relevant department heads. Do not wait for the next scheduled review. |

> 💡 **Tip**: The Org Health Score appears on both the **Command Center** and the **KPIs** page. On the Command Center, it displays as a large gauge with the four component cards beneath it. On the KPIs page, it appears as the first entry in the department breakdown with a trend sparkline.

[Chart: Org Health Score trend over 30 days — a line chart showing the composite score plotted daily, with green/amber/red background bands]

The four component scores also appear individually beneath the composite gauge, so you can immediately see which area is pulling the score up or down. If the composite is in amber but Task Success Rate is in the green while Cost Efficiency is in the red, you know the problem is financial, not operational.

> 📝 **Note**: If a component has no data available — for example, if no tasks have been recorded in the 30-day window — that component is excluded from the composite calculation. The score reflects only the components for which data exists. A score built from fewer components may be less representative, so check the component breakdown when interpreting a score with missing data.

---

### KPI Dashboard Overview

The **KPIs** page organizes all departmental and company-level metrics in a single scrollable view. Here is how the page is structured:

**Department Tabs.** Across the top of the page, you see tabs for each department: Engineering, Finance, HR, Marketing, Sales, Customer Success, Legal, and Org Health. Click a tab to filter the view to that department's metrics only. The **All Departments** tab (shown by default) displays a summary row for every department.

[Screenshot: KPIs page with department tabs across the top and summary cards below — KPIs Page]

**Time Range Selector.** In the upper right, a dropdown lets you choose the analysis window: **Last 24 Hours**, **Last 7 Days**, **Last 30 Days**, or **Last 90 Days**. The selected range controls the trend charts and comparison values. The default is **Last 30 Days**, which aligns with the Org Health Score's rolling window.

**KPI Cards.** Each metric appears as a card showing the current value, the target value, the unit of measurement, and a status badge. Status badges use the following conventions:

| Badge | Meaning |
|-------|---------|
| 🟢 **On Track** | Current value meets or exceeds the target |
| 🟡 **Below Target** | Current value is below the target (for metrics where higher is better) |
| 🔴 **Above Target** | Current value exceeds the target (for metrics where lower is better, such as error rates) |
| ⚪ **No Data** | No data source is connected or no records exist yet |
| ℹ️ **Info** | No target is defined; the value is informational only |

**Trend Sparklines.** Each KPI card includes a small inline sparkline chart showing the metric's trajectory over the selected time range. A green upward arrow means the trend is improving; a red downward arrow means it is declining. The sparkline gives you a quick directional read without needing to open the full chart.

[Chart: Example KPI sparkline — a mini line chart showing Task Completion Rate trending upward from 88% to 95% over 30 days]

---

### Department KPI Deep-Dives

Each department collector gathers live metrics from the operational data layer. Below is what each department tracks, what "good" looks like, and what to watch for.

#### Engineering

Engineering tracks **task completion rate** (target: 95%), **failure rate** (target: 0%), **escalation rate** (target: below 5%), and **open escalations** (target: 0). It also monitors task volume across four states — pending, in progress, completed, and failed — plus scheduled tasks from the scheduler. A bonus signal is **SOP compliance**: whether the Engineering Standard Operating Procedure is current (updated within 90 days). When task completion is above 95% and failures are near zero, engineering output is healthy. Watch for a rising failure rate or an increase in open escalations — these are early signals of systemic issues, often related to agent configuration or tooling problems. If the escalation rate climbs above 5%, investigate whether agents are encountering a recurring blocker that should be resolved at the infrastructure level rather than escalated individually.

#### Finance

Finance tracks **budget utilization** (target: 90%), **cost per agent** (target: below $50/month), **estimated LLM spend**, **total budget**, **total spent**, **total revenue**, **overall ROI** (target: 1.0 or higher), and **revenue per task**. Budget utilization tells you how much of the allocated budget has been consumed — values above 90% signal that spending is approaching the limit and may require reallocation or cost reduction. Cost per agent divides total spend by the number of active agents, giving you a per-unit efficiency metric. The revenue and ROI metrics come from the RevenueAnalytics module when revenue attribution data is available. If cost per agent is climbing while output remains flat, you have an efficiency problem. If ROI drops below 1.0, the organization is spending more than it is generating — a critical signal for strategic review.

#### HR

HR tracks **total agents** (headcount), **agents by department** (a breakdown showing how many agents serve each department), **department coverage** (target: 100%), and **declared departments**. Department coverage measures what percentage of declared departments have at least one assigned agent. A coverage score below 100% means at least one department has no dedicated agent support — a gap that will surface as delayed responses or missed tasks in that department. The agents-by-department breakdown helps you spot concentration imbalances: if Engineering has eight agents while Customer Success has one, you may need to rebalance staffing. Watch for declining total agent count (attrition or decommissioning) without corresponding workload reduction.

#### Marketing

Marketing tracks **campaign generation rate** (target: 5 campaigns), **active campaigns**, **content quality score** (target: 8 out of 10), **marketing task completion** (target: 90%), **total marketing tasks**, and **content pieces produced**. Campaign generation rate counts the total campaigns created; active campaigns shows how many are currently in flight. Content quality score averages the quality ratings assigned to produced content — a score below 8 signals a quality drift that may require editorial review. Marketing task completion measures the percentage of tasks assigned to the CMO, content creator, content writer, or growth hacker that reached "completed" status. If task completion drops below 90%, check whether marketing agents are blocked on dependencies from other departments.

#### Sales

Sales tracks **pipeline value** (total dollar value of all deals), **total deals**, **win rate** (target: 25%), **new leads**, **sales task completion** (target: 85%), and **total sales tasks**. Win rate — the percentage of deals that reached "won" stage — is the most direct indicator of sales effectiveness. A win rate below 25% may indicate lead quality issues, pricing misalignment, or process friction. Pipeline value gives you the total revenue opportunity in the system; a declining pipeline with a stable win rate means fewer deals are entering the funnel, which is a leading indicator of future revenue contraction. New leads tracks the count of leads with "new" status, giving you a forward-looking view of pipeline generation.

#### Customer Success

Customer Success tracks **ticket resolution time** (target: below 4 hours), **open tickets** (target: 0), **resolved tickets**, **total tickets**, **customer satisfaction** (target: 9 out of 10), **CS task completion** (target: 90%), and **SOP compliance**. Ticket resolution time is computed from the timestamps on resolved tickets — it tells you how long, on average, it takes to close a support ticket. Open tickets is a direct backlog measure: the lower the better. Customer satisfaction is averaged from survey responses; a score below 9 signals growing dissatisfaction that should trigger a root-cause review. If resolution time is climbing while ticket volume is stable, the issue is likely agent capability or tooling, not capacity.

#### Legal

Legal tracks **contract review time** (target: below 2 hours), **pending contract reviews** (target: 0), **approved contracts**, **total contracts**, **compliance score** (target: 100%), **total compliance checks**, **legal task completion** (target: 90%), and **SOP compliance**. Compliance score is the percentage of compliance checks that returned "pass" — anything below 100% means there is an active compliance gap. Pending contract reviews above zero indicates a backlog in the contract approval pipeline. Contract review time measures how long, on average, it takes to move a contract from submission to decision. A rising review time with a stable contract volume may indicate the legal team is under-resourced or that contract complexity has increased.

---

### Company-Level KPIs

Beyond department-level metrics, the dashboard tracks five company-wide KPIs that ladder up to strategic goals. These appear in a dedicated **Company KPIs** section at the top of the KPIs page.

| KPI | Target | Current | Status |
|-----|--------|---------|--------|
| **Annual Recurring Revenue (ARR)** | $10,000,000 | n/a | ⚪ No Data |
| **Customer Satisfaction** | 95% | n/a | ⚪ No Data |
| **Agent Utilization Rate** | 80% | Computed | 🟢 or 🟡 |
| **Build Success Rate** | 99.5% | Computed | 🟢 or 🟡 |
| **Employee Net Promoter Score** | 75 | n/a | ⚪ No Data |

**ARR** and **Employee Net Promoter Score** currently show "n/a" because the data sources required to compute them — a revenue ledger and an employee survey, respectively — have not yet been connected to the dashboard. The targets are set as strategic goals; the current values will populate automatically once the data sources are in place.

**Customer Satisfaction** also shows "n/a" because the survey file exists but contains no records yet. Once customer satisfaction surveys are collected, this metric will compute automatically from the average score.

**Agent Utilization Rate** and **Build Success Rate** are computed at request time from the task data layer. They update as new tasks flow through the system. These two metrics are your most reliable company-level indicators right now because they draw from live operational data.

> 💡 **Tip**: A "n/a" (null) value means the data source is not yet connected or contains no records — it does not mean the metric is zero. The dashboard explicitly distinguishes "no data" from "zero" so you can tell the difference between a metric that is failing and one that simply has not been measured yet.

---

### Reading Trends

Every KPI card on the dashboard includes a trend indicator that compares the current value to a previous period. Here is how to interpret what you see.

**Direction arrows.** A green upward arrow (↑) means the metric is improving compared to the previous period. A red downward arrow (↓) means it is declining. A gray dash (—) means the value is unchanged. The direction is always computed relative to the metric's "higher is better" setting — for error rates, a decrease is shown as improving (green ↑), not declining.

**Sparklines vs. full charts.** Sparklines are the small inline line charts on each KPI card. They give you a quick visual sense of the trajectory — is the line trending up, flat, or volatile? For a deeper analysis, click any KPI card to open the full Chart.js visualization. Full charts show the exact values at each data point, allow you to hover for details, and display the target line as a dashed reference. You can also toggle between daily, weekly, and monthly aggregations on the full chart view.

[Chart: Full KPI detail chart — a line chart with daily granularity showing Task Completion Rate over 30 days, with a dashed target line at 95% and data point labels]

**Trend analysis in context.** A single data point is a snapshot; a trend is a story. When evaluating a metric, always ask: is this a one-time fluctuation or a sustained pattern? A dip in task completion rate that recovers within a day is noise. A decline over five consecutive days is a signal. The dashboard's trend indicators compare the latest snapshot against the previous one, but the sparkline and full chart give you the longer arc.

**Anomaly detection.** The system also runs statistical anomaly detection on Org Health component scores. When a component value deviates significantly from its historical pattern (measured by Z-score), an anomaly alert is generated. These appear in the Command Center alert feed and are labeled as either **warning** (unusual deviation) or **critical** (extreme deviation). An anomaly does not always mean something is wrong — it means something is different enough from the norm to warrant your attention.

---

### KPI Alerts

The dashboard includes a rule-based alert engine that monitors KPI values against thresholds you define. Alerts surface in the **Command Center** alert feed and, for critical alerts, trigger a notification.

**How alert rules work.** Each rule specifies a department, a KPI key, a comparison operator, a threshold value, and a severity level. When the latest KPI snapshot matches the rule condition, an alert fires. For example, a rule might state: "If the Engineering failure rate is greater than 5%, fire a warning alert." The engine evaluates all enabled rules against every KPI snapshot collection cycle.

| Operator | Meaning | Example |
|----------|---------|---------|
| `gt` | Greater than | Fire if failure_rate > 5 |
| `lt` | Less than | Fire if budget_utilization < 50 |
| `gte` | Greater than or equal to | Fire if open_escalations >= 10 |
| `lte` | Less than or equal to | Fire if customer_satisfaction <= 7 |
| `eq` | Equal to | Fire if agent_sync_status = 0 |

**Severity levels.** Alerts carry one of three severity levels:

| Level | Meaning | Where It Appears |
|-------|---------|------------------|
| ℹ️ **Info** | Informational — a metric changed in a noteworthy way but no action is required | KPIs page, analytics log |
| ⚠️ **Warning** | Attention needed — a metric is approaching or has crossed a threshold | Command Center alert feed |
| 🔴 **Critical** | Immediate action required — a metric has crossed a critical threshold | Command Center alert feed, notification push |

**Where alerts appear.** Active alerts display in the Command Center's real-time alert feed, which is a scrollable list sorted by severity (critical first) and then by time. Each alert shows the rule name, the affected department and KPI, the current value, the threshold that was breached, and the timestamp. You can acknowledge alerts from the feed, which marks them as reviewed but does not dismiss them — they remain visible until the underlying condition clears.

> 📝 **Note**: Alert rules are evaluated on each KPI snapshot collection cycle. The default collection interval is every 5 minutes. This means an alert may appear up to 5 minutes after the condition first occurs.

---

### Taking Action

The KPIs page is designed to help you make decisions quickly. Here is a decision framework for what to do when you see a metric that concerns you.

**When to dig deeper.** If a metric is in amber or trending downward but no alert has fired, this is your signal to investigate before it becomes a problem. Click the KPI card to open the full chart view. Check the sparkline for the pattern: is it a sudden drop (likely an incident) or a gradual decline (likely a process or capacity issue)? Then open the corresponding department tab to see the related metrics. For example, if the Org Health Score is declining, check which of the four components is pulling it down, then navigate to that department's tab for the underlying metrics.

**When to delegate.** If a department-level KPI is below target, the most effective response is usually to delegate corrective action to the department head. You do not need to solve the problem yourself — you need to ensure the right person is aware and acting. The dashboard gives you the evidence to have a specific, data-driven conversation: "Customer satisfaction has dropped from 9.2 to 8.4 over the last two weeks. What is happening in the support pipeline?" This is far more effective than a vague "how are things going?"

**When to escalate.** Escalate when a KPI crosses into red territory, when multiple departments show simultaneous declines, or when an alert fires at critical severity. Escalation means the issue is beyond what a single department head can resolve — it may require cross-functional coordination, budget reallocation, or a strategic decision. Use the Escalations page to create a formal escalation record, which ensures the issue is tracked through resolution and does not fall through the cracks.

**When to celebrate.** Do not only use the KPIs page for problems. When a metric hits a new high, when a department sustains green performance over a full quarter, or when a previously red metric trends back to green — acknowledge it. The data is here to tell you what is working, not just what is broken. Positive signals are just as important for decision-making as negative ones: they tell you where to double down, which teams to learn from, and which practices to replicate.

---

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 — Draft | 2026-08-26 | CEO Advisor | Initial draft. Org Health Score explanation, KPI dashboard overview, all 8 department deep-dives, company-level KPIs, trend reading guide, alert system documentation, and decision framework. |

---

*End of Understanding Your KPIs. Proceed to [Section 4 — Managing Tasks](04-managing-tasks.md) for the Kanban board workflow, or return to the [Table of Contents](00-outline-and-executive-summary.md#table-of-contents).*


---

# Section Separator

---

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


---

# Section Separator

---

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


---

# Section Separator

---

# Health Monitoring & Diagnostics

This section explains how to monitor the health of the CEO Dashboard, interpret its diagnostic signals, and resolve issues when something goes wrong. Whether you are a technical administrator keeping the system operational or a COO who needs to know "is the dashboard healthy?", this chapter gives you the tools to answer that question quickly and act on what you find.

---

## Dashboard Health at a Glance

The dashboard exposes its health status in two ways: a visual status indicator you can see without navigating anywhere, and a structured health check you can query programmatically.

### Visual Status Indicators

The **top header bar** on every page shows two real-time health signals:

| Indicator | What It Means | Location |
|-----------|---------------|----------|
| **WebSocket status dot** (green pulsing = *Live*, red = *Offline*) | Whether the dashboard's real-time connection is active. A green dot means data is streaming; a red dot means the frontend has fallen back to polling or is stale. | Top-right of header bar |
| **Uptime counter** | How long the dashboard process has been running since the last restart. Resets to zero on every restart. | Top-right of header bar, next to the status dot |

[Screenshot: Header bar annotated with WebSocket status dot, uptime counter, and client count]

When the WebSocket connection drops, a full-width **amber banner** appears at the top of the viewport: "Connection lost — working in offline mode." Data continues to load via polling fallback, but real-time updates stop until the connection restores.

### The Org Health Score Gauge

The most important single health indicator is the **Org Health Score** gauge on the Dashboard home page. This circular gauge displays a composite score from 0 to 100 and labels it with a color band:

| Band | Score Range | Meaning | Action |
|------|-------------|---------|--------|
| 🟢 Green (healthy) | 80–100 | Organization is operating within normal parameters. | Monitor. No action needed. |
| 🟡 Amber (degraded) | 50–79 | One or more components are underperforming. Investigate. | Click the gauge to expand the component grid and identify which metric is dragging the score down. |
| 🔴 Red (critical) | 0–49 | Multiple components are failing or one is severely degraded. | Immediate investigation required. Follow the diagnostic workflows below. |

> 💡 **Tip**: Click the gauge to expand the 2x2 component grid. Each card shows the component name, its current score, a color-coded status dot, and a mini sparkline chart. Click any card to see the detailed score breakdown with its weight in the composite.

[Screenshot: Org Health Score gauge expanded to show four component cards with sparkline charts]

### Status Bar Summary

Below the gauge, the **Alerts Bar** provides a compact summary of pending items that require attention:

- **Pending approvals** (amber badge) — tasks waiting for human approval
- **Open escalations** (red badge) — issues raised to the CEO or COO
- **In-progress tasks** (blue badge) — tasks currently being worked by agents

A healthy dashboard shows a green gauge, a green WebSocket dot, and low or zero counts in the amber and red badges. If any of these shift to warning colors, proceed to the relevant section below.

---

## The Org Health Score — Deep Dive

The **Org Health Score** ([see Glossary](#glossary)) is not a single measurement. It is a weighted composite of four independent component scores, each measuring a different dimension of organizational performance. Understanding how these components work — and how their weights interact — is essential for interpreting the score correctly and making informed configuration changes.

### Component Breakdown

| Component | Weight | What It Measures | Data Source | Score Behavior |
|-----------|--------|-------------------|-------------|----------------|
| **Task Success Rate** | 0.30 | Ratio of completed tasks to total tasks in the last 30 days | Message Bus (`inbox.json`) via `_company_window_tasks()` | Higher completion rate = higher score. Returns `None` when no tasks exist in the window. |
| **Agent Utilization** | 0.25 | Active agents (those appearing in recent tasks) as a percentage of all registered agents | Agent registry + Message Bus task data | More agents working = higher score. Capped at 100. Returns `None` when no agents are registered. |
| **Cost Efficiency** | 0.25 | Budget utilization — how much of the allocated budget has been spent | Cost summary from the data layer | Lower spend relative to budget = higher score. Returns `None` when no budget is configured. |
| **Error Rate** | 0.20 | Inverse of the error/exception rate across agent operations | Task statuses in the Message Bus (failed, error, cancelled tasks) | Fewer errors = higher score. A 0% error rate scores 100; a 10% error rate scores 90. Returns `None` when no tasks exist. |

### How the Composite Score Is Calculated

The calculator at `ai_company/dashboard/org_health.py` performs these steps on each evaluation:

1. **Collect component values.** Each component scorer returns a value from 0 to 100, or `None` if no data is available.
2. **Filter to available data.** Components returning `None` are excluded from the composite — the score reflects only dimensions where data exists.
3. **Compute weighted average.** The remaining component values are multiplied by their respective weights, summed, and divided by the sum of the active weights. This ensures that a missing component does not artificially lower the score — its weight is redistributed proportionally across the remaining components.
4. **Clamp and round.** The result is clamped to 0–100 and rounded to the nearest integer.
5. **Map to band.** The integer score is compared against the configured band thresholds to determine the color label.

#### Example Calculation

Suppose all four components are available and return these values:

| Component | Weight | Value | Weighted Contribution |
|-----------|--------|-------|-----------------------|
| Task Success Rate | 0.30 | 85 | 25.5 |
| Agent Utilization | 0.25 | 60 | 15.0 |
| Cost Efficiency | 0.25 | 70 | 17.5 |
| Error Rate | 0.20 | 95 | 19.0 |

Composite = (25.5 + 15.0 + 17.5 + 19.0) / (0.30 + 0.25 + 0.25 + 0.20) = 77.0 / 1.00 = **77** → 🟡 Amber

Now suppose the Cost Efficiency component has no data (`None`):

| Component | Weight | Value | Weighted Contribution |
|-----------|--------|-------|-----------------------|
| Task Success Rate | 0.30 | 85 | 25.5 |
| Agent Utilization | 0.25 | 60 | 15.0 |
| Error Rate | 0.20 | 95 | 19.0 |

Composite = (25.5 + 15.0 + 19.0) / (0.30 + 0.25 + 0.20) = 59.5 / 0.75 = **79** → 🟡 Amber

The score *increased* because the lower-scoring Cost Efficiency component was removed, and the weights were redistributed proportionally.

> ⚠️ **Warning**: A rising Org Health Score is not always good news. If a component returns `None` because its data source is unavailable (e.g., the Message Bus is down and no tasks can be read), the score may rise while the organization is actually degraded. Always check the component breakdown, not just the composite number.

### Configuring Weights and Bands

The composite score behavior is defined in `config/org_health.yaml`. You can modify this file to adjust how the score responds to organizational changes.

#### Band Thresholds

```yaml
bands:
  green:
    min: 80
    max: 100
  amber:
    min: 50
    max: 79
  red:
    min: 0
    max: 49
```

To make the green band harder to achieve (e.g., only scores of 90+ are "healthy"), change `green.min` to `90` and `amber.max` to `89`. To create a wider amber zone, lower `amber.min` to `40` and raise `green.min` to `85`.

#### Component Weights

```yaml
components:
  - name: task_success_rate
    weight: 0.30
  - name: agent_utilization
    weight: 0.25
  - name: cost_efficiency
    weight: 0.25
  - name: error_rate
    weight: 0.20
```

> ⚠️ **Warning**: Weights **must** sum to 1.0. The calculator validates this at startup and logs a warning if the sum deviates by more than 0.01. If you add or remove a component, adjust the remaining weights to maintain a total of 1.0.

#### What Configuration Changes Mean

| Change | Effect on Score |
|--------|-----------------|
| Increase `task_success_rate` weight to 0.40 | Task completion becomes more influential. A drop in task completion will pull the score down faster. |
| Decrease `error_rate` weight to 0.10 | Errors matter less. The score is more resilient to error spikes but less sensitive to error recovery. |
| Raise `green.min` to 90 | The "healthy" bar is higher. The dashboard shows amber more often, flagging marginal performance earlier. |
| Lower `amber.min` to 30 | The red zone shrinks. Only severe degradation triggers a red alert, reducing alert fatigue. |

> 💡 **Tip**: Start with conservative weight changes (shift by 0.05 at a time) and observe the score over a few days before making further adjustments. The score is sensitive to weight redistribution because it uses a proportional recalculation.

### Historical Trend Interpretation

The Org Health Score is designed to be evaluated over time, not just as a point-in-time snapshot. The component breakdown includes mini sparkline charts that show recent history.

| Trend Pattern | What It Means | Likely Cause |
|---------------|---------------|--------------|
| Score consistently ≥ 80 (green) | Stable, healthy operations | All components performing within normal bounds |
| Score fluctuating between 50–79 (amber) | Intermittent issues or one struggling component | Check which component card shows the lowest value and most volatile sparkline |
| Score steadily declining over days | Progressive degradation — a component is getting worse | Identify the declining component and investigate its data source |
| Score suddenly drops from green to red | Acute failure — something broke | Check the Alert System for fired alerts, then follow the "High error rate" diagnostic workflow |
| Score rises after being low, but a component shows `None` | The score is masking a problem — a data source went offline | Check the `/health` endpoint for missing dependencies |

> 📝 **Note**: The `OrgHealthCalculator.detect_anomalies()` method can automatically flag unusual component score movements using Z-score analysis. Anomalies are classified as "warning" (Z-score > 2.0) or "critical" (Z-score > 3.0). This is useful for catching sudden shifts that might otherwise go unnoticed in a slowly declining trend.

---

## Health Endpoints Reference

The dashboard exposes three HTTP endpoints for health monitoring. These are intended for external monitoring systems, load balancers, CI pipelines, and manual diagnosis.

### GET `/health` — Deep Health Check

**Purpose**: Comprehensive status check covering dependencies, disk, memory, and task state.

**When to use**: Manual diagnosis, automated health monitoring, and as a liveness check that goes beyond "is the process running?"

**Expected response (200)**:

```json
{
  "status": "ok",
  "service": "ai-company-dashboard",
  "version": "1.0.0",
  "uptime_seconds": 3642.1,
  "checks": {
    "inbox": "ok",
    "registry": "ok",
    "agents": "ok (12 files)",
    "config": "ok",
    "llm_providers": "2 configured",
    "audit_log": "ok (45.3 KB)",
    "disk_space": "12.4 GB free / 47.6 GB (26%)",
    "process_memory": "84.2 MB RSS",
    "memory_store": "ok (128 entries)",
    "dead_letter_queue": "empty"
  },
  "metrics_summary": {
    "tasks_total": 156,
    "tasks_completed": 142,
    "tasks_failed": 8,
    "llm_cost_usd": 12.4567,
    "success_rate_pct": 91.0
  },
  "timestamp": "2026-08-26T14:30:00+00:00"
}
```

**What each check verifies**:

| Check | What It Confirms | "Missing" Means |
|-------|-------------------|-----------------|
| `inbox` | `.opencode/inbox.json` is readable | The Message Bus file is absent — tasks cannot be created or tracked |
| `registry` | `company/agent-registry.json` exists | No agent definitions are available — the dashboard cannot display agents |
| `agents` | `.opencode/agents/*.md` files exist (reports count) | Agent markdown files have not been generated — the `ai-company generate` step was not run |
| `config` | `company/models.yaml` exists | LLM model configuration is missing |
| `llm_providers` | Environment variables for LLM API keys are set | No LLM providers are configured — agents cannot call language models |
| `audit_log` | `.opencode/audit` is readable (reports size) | No audit trail exists — agent operations are not being logged |
| `disk_space` | Free disk space on the volume | N/A — always reports a value or "unavailable" |
| `process_memory` | Current RSS memory usage of the dashboard process | N/A — always reports a value or "unavailable" |
| `memory_store` | `memory/` directory exists and contains JSON files | The persistent memory store is absent |
| `dead_letter_queue` | `.opencode/dead_letter_queue.json` is readable | N/A — an empty queue is healthy |

**Overall status logic**: If any check returns "missing" or "error", the overall `status` field is `"degraded"` instead of `"ok"`. A `"degraded"` status means the dashboard is running but operating with reduced capability.

> 📝 **Note**: All file checks are anchored at the configured `StateStore` root directory, not the process working directory. This means the health check is accurate regardless of which directory you launched the dashboard from.

### GET `/ready` — Readiness Probe

**Purpose**: Lightweight readiness check for Kubernetes-style orchestration. Returns `200` when the dashboard can serve requests, or `503` when core dependencies are missing.

**When to use**: Automated dependency checks, load balancer health routing, and CI/CD deployment gates. This is the endpoint a container orchestrator should poll to decide whether to route traffic to this instance.

**What it checks (hard requirements only)**:

| Dependency | Why It's Hard | Failure Mode |
|------------|---------------|--------------|
| `company/agent-registry.json` | The dashboard cannot function without agent definitions | 503 with `"reason": "registry missing"` |
| `.opencode/agents/` directory | The dashboard serves agent data from this directory | 503 with `"reason": "agents directory missing"` |

**Expected response (200 — ready)**:

```json
{
  "status": "ready"
}
```

**Expected response (503 — not ready)**:

```json
{
  "status": "not ready",
  "reason": "registry missing"
}
```

> ⚠️ **Warning**: A 503 from `/ready` means the dashboard **cannot** serve its primary functions. Unlike `/health` which reports degraded states, `/ready` makes a binary decision: ready or not ready. If you see 503s in your load balancer logs, the agent registry or agents directory is missing — run `ai-company generate` to rebuild them.

### GET `/metrics` — Prometheus Exporter

**Purpose**: Expose operational metrics in Prometheus text exposition format for integration with external monitoring systems (Prometheus, Grafana, Datadog, etc.).

**When to use**: When you need to feed dashboard health data into an existing monitoring stack, build custom dashboards, or set up long-term alerting rules.

**Content type**: `text/plain; version=0.0.4; charset=utf-8`

**Metrics exported**:

| Metric Name | Type | Description |
|-------------|------|-------------|
| `process_start_time_seconds` | gauge | Unix timestamp when the process started |
| `ai_company_uptime_seconds` | gauge | Seconds since process start |
| `ai_company_process_rss_bytes` | gauge | Current resident set size in bytes (requires `psutil`) |
| `ai_company_process_vms_bytes` | gauge | Current virtual memory size in bytes (requires `psutil`) |
| `ai_company_process_open_fds` | gauge | Number of open file descriptors (requires `psutil`) |
| `ai_company_process_max_rss_bytes` | gauge | Peak resident set size in bytes (Linux/macOS) |
| `ai_company_cpu_user_seconds_total` | counter | Total user CPU time |
| `ai_company_cpu_system_seconds_total` | counter | Total system CPU time |
| `ai_company_llm_requests_total` | counter | Total LLM API requests |
| `ai_company_llm_errors_total` | counter | Total LLM API errors |
| `ai_company_llm_cost_usd_total` | gauge | Total LLM cost across all providers |
| `ai_company_llm_cost_anthropic_usd` | gauge | LLM cost from Anthropic |
| `ai_company_llm_cost_openai_usd` | gauge | LLM cost from OpenAI |
| `ai_company_llm_cost_deepseek_usd` | gauge | LLM cost from DeepSeek |
| `ai_company_llm_cost_other_usd` | gauge | LLM cost from other providers |
| `ai_company_task_success_rate_pct` | gauge | Live task success rate as a percentage |
| `ai_company_llm_error_rate_pct` | gauge | LLM error rate as a percentage |
| `ai_company_llm_avg_cost_per_request_usd` | gauge | Average cost per LLM request |
| `ai_company_circuit_breaker_trips_total` | counter | Total circuit breaker trip events |
| `ai_company_circuit_breaker_half_open_total` | counter | Total circuit breaker half-open transitions |
| `ai_company_tasks_by_status{status="..."}` | gauge | Task count per status (completed, failed, pending, etc.) |
| `ai_company_agent_tasks_total{agent="..."}` | counter | Total tasks per agent |
| `ai_company_agent_successes_total{agent="..."}` | counter | Successful tasks per agent |
| `ai_company_agent_failures_total{agent="..."}` | counter | Failed tasks per agent |
| `ai_company_llm_model_calls_total{model="..."}` | counter | LLM calls per model |
| `ai_company_llm_model_cost_usd{model="..."}` | gauge | LLM cost per model |
| `ai_company_llm_model_tokens_in_total{model="..."}` | counter | Input tokens per model |
| `ai_company_llm_model_tokens_out_total{model="..."}` | counter | Output tokens per model |

> 📝 **Note**: In-memory counters (LLM requests, errors, costs) reset when the dashboard process restarts. The audit-log-derived metrics (per-agent, per-model) are computed from the persistent audit trail and survive restarts.

---

## KPI Snapshot System

The dashboard periodically collects Key Performance Indicator snapshots across all departments and stores them for historical analysis. This system runs in the background as part of the executor daemon.

### How Periodic Collection Works

The **KPI Snapshot Scheduler** (`ai_company/dashboard/kpis/scheduler.py`) is a time-gated wrapper that the executor daemon calls on every poll tick:

1. The daemon polls at its configured interval (default: every few seconds).
2. On each tick, the scheduler checks whether enough time has elapsed since the last snapshot (default interval: **300 seconds / 5 minutes**).
3. If the interval has elapsed, the scheduler triggers a full collection run.
4. The collection run invokes **8 department-specific KPI collectors** in sequence.

The collectors are:

| Collector | Department |
|-----------|------------|
| `EngineeringKPICollector` | Engineering |
| `HRKPICollector` | HR |
| `FinanceKPICollector` | Finance |
| `MarketingKPICollector` | Marketing |
| `SalesKPICollector` | Sales |
| `CustomerSuccessKPICollector` | Customer Success |
| `LegalKPICollector` | Legal |
| `OrgHealthKPICollector` | Org Health (composite) |

### What Gets Stored

Each collector returns a dictionary of KPI values for its department. These are ingested into two storage layers:

1. **SQLite database** — via `KPIPipeline.ingest_snapshot()`. This is the primary data store for the dashboard's real-time KPI views and trend analysis.
2. **NDJSON history files** — via `KPIHistoryStore.store_snapshot()`. Each department gets a file at `dashboard/kpi_history/<department>_history.ndjson`, one JSON object per line per snapshot. This provides a durable, append-only history that survives database corruption.

Each stored KPI entry contains:

| Field | Description |
|-------|-------------|
| `timestamp` | ISO 8601 timestamp of the collection |
| `department` | Department identifier (e.g., `"engineering"`) |
| `kpi_key` | The specific KPI name (e.g., `"tasks_completed"`, `"failure_rate"`) |
| `current` | The numeric value at time of collection |
| `target` | The target value (if defined), otherwise `null` |
| `unit` | Unit of measurement (e.g., `"count"`, `"percent"`, `"usd"`) |
| `status` | Status indicator (`"ok"`, `"warning"`, `"critical"`) |

Non-numeric KPIs (such as agent-by-department breakdowns that return dictionaries) are automatically skipped during storage.

### Viewing Historical Snapshots

You can retrieve stored history through the `KPIHistoryStore` API:

| Operation | Method | Description |
|-----------|--------|-------------|
| Get all history for a department | `get_history(department)` | Returns all stored entries, oldest first |
| Filter by specific KPI | `get_history(department, kpi_key="failure_rate")` | Returns history for one KPI only |
| Filter by time range | `get_history(department, since="2026-08-25T00:00:00")` | Returns entries after the specified timestamp |
| Get the latest snapshot | `get_latest(department)` | Returns the most recent collection for a department |
| List departments with data | `list_departments()` | Returns department IDs that have stored history |
| Count stored entries | `count_entries(department)` | Returns the total number of stored KPI entries |

### Retention and Cleanup

KPI history files grow as new snapshots are appended. To manage storage:

- Use `clear(department)` to remove all history for a specific department.
- Use `clear()` to remove all history across all departments.
- The NDJSON files are located at `dashboard/kpi_history/` under the configured data directory.

> 💡 **Tip**: If you are running the dashboard in production, consider adding a periodic cleanup job that removes history files older than your retention window (e.g., 90 days). The `KPIHistoryStore` does not enforce automatic retention — it stores everything you give it.

---

## Alert System

The **Alert Engine** (`ai_company/dashboard/analytics.py`) evaluates threshold-based rules against live KPI snapshots and fires alerts when conditions are violated. Alerts are a critical part of the monitoring loop — they surface problems before they become crises.

### How Alert Rules Work

An alert rule defines a condition on a specific KPI. Each KPI snapshot is evaluated against all active rules. When a rule's condition is true, an alert fires.

Each rule has these properties:

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Human-readable name (e.g., "High failure rate") |
| `department` | string | Department this rule applies to, or `"*"` for all departments |
| `kpi_key` | string | The KPI to watch (e.g., `"failure_rate"`) |
| `operator` | string | Comparison: `gt` (>), `lt` (<), `gte` (>=), `lte` (<=), `eq` (=) |
| `threshold` | number | The numeric value to compare against |
| `severity` | string | `info`, `warning`, or `critical` |
| `enabled` | boolean | Whether this rule is active |

### Configuring Thresholds

Rules can be managed programmatically or loaded from a JSON file.

**Loading rules from a JSON file**:

```json
[
  {
    "name": "High failure rate",
    "department": "*",
    "kpi_key": "failure_rate",
    "operator": "gt",
    "threshold": 10.0,
    "severity": "warning",
    "enabled": true
  },
  {
    "name": "Critical task backlog",
    "department": "engineering",
    "kpi_key": "pending_tasks",
    "operator": "gt",
    "threshold": 50.0,
    "severity": "critical",
    "enabled": true
  }
]
```

**Example threshold scenarios**:

| Scenario | Rule |
|----------|------|
| Alert when any department's failure rate exceeds 10% | `kpi_key: "failure_rate"`, `operator: "gt"`, `threshold: 10.0`, `department: "*"` |
| Alert when Engineering's pending tasks drop below 5 (idle team) | `kpi_key: "pending_tasks"`, `operator: "lt"`, `threshold: 5.0`, `department: "engineering"` |
| Alert when total cost exceeds $100 | `kpi_key: "total_cost"`, `operator: "gt"`, `threshold: 100.0`, `department: "*"` |
| Info notification when a KPI exactly equals its target | `kpi_key: "tasks_completed"`, `operator: "eq"`, `threshold: 100.0`, `severity: "info"` |

### Where Alerts Appear

| Location | What You See |
|----------|-------------|
| **Toast notifications** (bottom-right) | Each fired alert triggers a toast with the severity icon, alert name, department, KPI, and current value vs threshold |
| **Alerts Bar** on Dashboard home | Aggregated count of active alerts by severity |
| **Escalation stack** (top-right) | Critical alerts that require human action appear here with *Resolve* / *Dismiss* buttons |

### Alert History

Fired alerts are logged with a timestamp, the rule name, the triggering KPI value, and the threshold it violated. The alert message follows this format:

```text
[SEVERITY] Rule Name: department.kpi_key = value (operator threshold)
```

Example:

```text
[WARNING] High failure rate: engineering.failure_rate = 12.5 (gt 10.0)
[CRITICAL] Critical task backlog: engineering.pending_tasks = 67 (gt 50.0)
```

---

## Diagnostic Workflows

When something goes wrong, these step-by-step procedures help you identify the root cause and restore normal operation. Each workflow starts with symptoms and narrows to a specific cause.

### Workflow 1: Dashboard Won't Start

**Symptoms**: The dashboard process fails to start, exits immediately, or shows an error in the console.

**Diagnostic tree**:

1. **Check if a process is already running on the dashboard port.**
   - If another instance is using port `8420` (production) or `8421` (staging), the new process will fail with an address-already-in-use error.
   - **Fix**: Stop the existing process or configure a different port.

2. **Check if the required environment variables are set.**
   - At minimum, you need `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` for LLM functionality.
   - The dashboard itself will start without LLM keys, but agent operations will fail.
   - **Fix**: Set the required keys in your `.env` file or export them in your shell.

3. **Check if `company/agent-registry.json` exists.**
   - The readiness probe (`/ready`) will return 503 if this file is missing.
   - **Fix**: Run `ai-company generate` to regenerate the registry and agent files.

4. **Check if the SQLite database is accessible.**
   - If the database file is locked by another process, the dashboard may fail to initialize the data layer.
   - **Fix**: Ensure no other dashboard instance is running. If the database is corrupted, check for WAL/SHM files and remove stale locks.

5. **Check the logs for the specific error.**
   - Look at the console output or log files for a Python traceback. The most common startup errors are `ImportError` (missing dependency), `FileNotFoundError` (missing data directory), and `PermissionError` (insufficient file access).

6. **Verify Python version and dependencies.**
   - The dashboard requires Python 3.12+. Run `python --version` to confirm.
   - Run `uv sync` or `pip install -e .` to ensure all dependencies are installed.

### Workflow 2: Data Looks Wrong

**Symptoms**: KPI values on the dashboard don't match what you expect, scores seem too high or too low, or charts show unexpected patterns.

**Verification steps**:

1. **Check the Org Health Score components.**
   - Click the gauge to expand the component grid. Identify which component has the unexpected value.
   - If a component shows `None` or "No data", its data source is unavailable — the score may be artificially inflated because that component is excluded from the composite.

2. **Verify the data source directly.**
   - **Task data**: Check `.opencode/inbox.json` for the raw task list. Count completed vs total tasks manually to verify the task success rate.
   - **Agent data**: Check `company/agent-registry.json` to confirm the expected number of registered agents.
   - **Cost data**: Check the cost summary in the data layer or audit log.

3. **Check the KPI snapshot timestamp.**
   - If the snapshot is stale (more than 5 minutes old), the KPI scheduler may not be running.
   - Check the daemon status at `GET /api/v1/daemon/status`. The `last_tick_at` field shows when the daemon last ran.

4. **Check for stale NDJSON history.**
   - If the history files at `dashboard/kpi_history/` haven't been updated recently, the snapshot scheduler's interval may have elapsed but the collection is failing silently.
   - Check the daemon logs for KPI collection errors.

5. **Compare the Prometheus `/metrics` endpoint.**
   - The `ai_company_task_success_rate_pct` gauge in `/metrics` is computed live from the Message Bus. If it disagrees with the Org Health Score's task success rate component, the data sources may be reading from different points in time.

### Workflow 3: Real-Time Updates Stopped

**Symptoms**: The WebSocket status dot in the header bar turns red, the "Connection lost" banner appears, and charts stop updating.

**WebSocket diagnosis**:

1. **Check if the WebSocket endpoint is reachable.**
   - The WebSocket connects to `ws://<host>:<port>/ws/v1`. If the dashboard is behind a reverse proxy, ensure the proxy supports WebSocket upgrades (HTTP `Upgrade: websocket` header).

2. **Check the browser console.**
   - Open your browser's developer tools (F12) and look at the Console tab for WebSocket errors. Common messages include:
     - `WebSocket connection to 'ws://...' failed` — the server is unreachable
     - `WebSocket closed with code 1006` — abnormal closure, usually a network issue
     - `WebSocket closed with code 1008` — policy violation, often a CORS or auth issue

3. **Verify the WebSocket topics.**
   - The dashboard subscribes to these topics: `kpis`, `tasks`, `escalations`, `approvals`, `daemon`, `org_health`.
   - If the connection is established but you're not receiving updates on a specific topic, the server-side publisher for that topic may not be producing messages.

4. **Check the dashboard process health.**
   - A healthy WebSocket requires the dashboard process to be alive and responsive. Call `GET /health` to verify the process is running and check the `uptime_seconds` field.

5. **Test the polling fallback.**
   - The dashboard is designed to fall back to HTTP polling when the WebSocket drops. If polling is also failing, the issue is likely network connectivity or the dashboard process itself — not WebSocket-specific.

6. **Restart the WebSocket connection.**
   - If the WebSocket is stuck, the frontend will automatically attempt reconnection with exponential backoff. You can force a reconnection by refreshing the page.

### Workflow 4: KPIs Not Updating

**Symptoms**: KPI charts on the dashboard show the same values over time, or the KPI history stops growing.

**Scheduler diagnosis**:

1. **Check if the daemon is running.**
   - Call `GET /api/v1/daemon/status`. The response shows:
     - `state`: Should be `"running"`. If `"not_running"`, the daemon has never been started. If `"stale (process dead)"`, the daemon process has crashed.
     - `ticks_completed`: Should be increasing. If it's stuck at a fixed number, the daemon loop is frozen.
     - `last_tick_at`: Should be recent. If it's old, the daemon is not polling.

2. **Check the KPI scheduler interval.**
   - The default snapshot interval is 300 seconds (5 minutes). If the scheduler is running but snapshots appear infrequent, this is expected behavior.
   - To force an immediate snapshot, the scheduler's `reset()` method resets the internal timer so the next `run_due()` call triggers immediately.

3. **Check the SQLite database.**
   - If the database is unavailable (returns `None` from `get_database()`), the snapshot scheduler skips collection silently with a debug-level log message.
   - Verify the database path is correct and the file is accessible.

4. **Check for collection errors in the logs.**
   - The scheduler wraps collection in a try/except and logs exceptions at the `exception` level. Look for messages starting with "KPI snapshot failed" in the daemon logs.

5. **Verify the collectors are returning data.**
   - Each of the 8 department collectors reads from different data sources. If a specific department's KPIs are not updating while others are, the issue is likely in that collector's data source (e.g., a missing or corrupted file that the collector reads).

### Workflow 5: High Error Rate

**Symptoms**: The Org Health Score has dropped, the Error Rate component shows a low value, or alerts fire for high failure rates.

**Investigation procedure**:

1. **Identify which component is driving the score down.**
   - Expand the Org Health Score component grid. Check the Error Rate card — if it's red or has a volatile sparkline, this is the primary contributor.

2. **Check the task status breakdown.**
   - In the `/health` endpoint response, review `metrics_summary.tasks_failed` vs `metrics_summary.tasks_total`.
   - On the Dashboard home page, check the "Tasks by Status" chart for the proportion of failed tasks.

3. **Examine the audit log.**
   - The audit trail at `.opencode/audit` records every task completion with success/failure metadata. Look for patterns:
     - Are failures concentrated in one agent? (Check `ai_company_agent_failures_total` in `/metrics`)
     - Are failures concentrated in one department? (Check the task status breakdown)
     - Did failures start at a specific time? (Check the audit log timestamps)

4. **Check LLM provider health.**
   - High LLM error rates often indicate provider-side issues. Check `ai_company_llm_errors_total` and `ai_company_llm_error_rate_pct` in `/metrics`.
   - If circuit breaker trips are increasing (`ai_company_circuit_breaker_trips_total`), the LLM provider is returning errors frequently enough to trigger the breaker.

5. **Check the dead letter queue.**
   - The `/health` endpoint reports `dead_letter_queue` status. If there are pending items in the dead letter queue, tasks are failing repeatedly and being quarantined.

6. **Review error patterns over time.**
   - Use the `compute_trends()` function or the KPI history API to compare the current error rate against historical values. A sudden spike suggests an acute issue (provider outage, configuration change); a gradual increase suggests a systemic problem (resource exhaustion, model degradation).

---

## Monitoring Integration

The `/metrics` endpoint provides a standard Prometheus text exposition format that integrates with the most common monitoring stacks.

### Prometheus Configuration

Add this scrape configuration to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: "ai-company-dashboard"
    scrape_interval: 30s
    static_configs:
      - targets: ["localhost:8420"]
    metrics_path: "/metrics"
```

### Grafana Dashboard Panels

The exported metrics support these common Grafana panel configurations:

| Panel | Query | Type |
|-------|-------|------|
| Dashboard Uptime | `ai_company_uptime_seconds` | Stat |
| LLM Cost Rate | `rate(ai_company_llm_cost_usd_total[5m])` | Time series |
| Task Success Rate | `ai_company_task_success_rate_pct` | Gauge (0–100) |
| LLM Error Rate | `ai_company_llm_error_rate_pct` | Gauge (0–100) with threshold bands |
| Cost by Provider | `ai_company_llm_cost_*_usd` (stacked) | Time series, stacked area |
| Agent Success vs Failure | `ai_company_agent_successes_total` vs `ai_company_agent_failures_total` | Bar chart |
| Process Memory | `ai_company_process_rss_bytes` | Time series |
| Circuit Breaker Events | `ai_company_circuit_breaker_trips_total` | Counter, rate over 5m |
| Tasks by Status | `ai_company_tasks_by_status` (per-label) | Pie or bar chart |

### Key Alert Rules for Prometheus

```yaml
# Alert when LLM error rate exceeds 15% for 5 minutes
- alert: HighLLMErrorRate
  expr: ai_company_llm_error_rate_pct > 15
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "LLM error rate is {{ $value }}%"

# Alert when dashboard is down
- alert: DashboardDown
  expr: up{job="ai-company-dashboard"} == 0
  for: 1m
  labels:
    severity: critical

# Alert when process memory exceeds 500MB
- alert: HighMemoryUsage
  expr: ai_company_process_rss_bytes > 524288000
  for: 10m
  labels:
    severity: warning
```

> 💡 **Tip**: Combine Prometheus metrics with the Org Health Score from the dashboard's API for a complete monitoring picture. Prometheus gives you infrastructure-level visibility; the Org Health Score gives you organizational-level visibility.

---

## Health Check Quick Reference Card

This one-page reference summarizes every health indicator, what it measures, its thresholds, and what to do when it signals a problem.

| Indicator | Where to Find It | Healthy | Warning | Critical | Action When Unhealthy |
|-----------|-------------------|---------|---------|----------|----------------------|
| **Org Health Score** | Dashboard home gauge | 🟢 ≥ 80 | 🟡 50–79 | 🔴 < 50 | Expand component grid → identify lowest component → follow diagnostic workflow |
| **WebSocket Status** | Header bar (top-right) | 🟢 Green pulsing | — | 🔴 Red | Check network, browser console, restart page |
| **`/health` status** | `GET /health` → `status` field | `"ok"` | `"degraded"` | — | Check `checks` object for "missing" entries → fix data sources |
| **`/ready` status** | `GET /ready` | `200 OK` | — | `503 Not Ready` | Run `ai-company generate` to rebuild registry/agents |
| **Task Success Rate** | Component card or `/metrics` → `ai_company_task_success_rate_pct` | ≥ 80% | 50–79% | < 50% | Check failed tasks in audit log → identify failing agent or LLM provider |
| **Agent Utilization** | Component card or compute from registry + task data | ≥ 70% | 30–69% | < 30% | Check if agents are blocked, tasks are available, registry is current |
| **Cost Efficiency** | Component card or cost summary | ≥ 70% | 40–69% | < 40% | Review LLM costs in `/metrics` → check for runaway agent loops |
| **Error Rate** | Component card or `/metrics` → `ai_company_llm_error_rate_pct` | ≤ 5% | 5–15% | > 15% | Check LLM provider status, circuit breaker trips, dead letter queue |
| **Daemon Status** | `GET /api/v1/daemon/status` → `state` | `"running"` | — | `"stale (process dead)"` or `"not_running"` | Restart the daemon process |
| **Disk Space** | `GET /health` → `checks.disk_space` | > 20% free | 10–20% free | < 10% free | Clean up old logs, audit files, or KPI history |
| **Process Memory** | `GET /health` → `checks.process_memory` | < 200 MB | 200–500 MB | > 500 MB | Check for memory leaks, restart the process |
| **Dead Letter Queue** | `GET /health` → `checks.dead_letter_queue` | `"empty"` | N pending > 0 | N pending > 10 | Review quarantined tasks, identify recurring failures |
| **LLM Providers** | `GET /health` → `checks.llm_providers` | ≥ 1 configured | — | `0 configured` | Set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` in `.env` |
| **Audit Log** | `GET /health` → `checks.audit_log` | `"ok (N KB)"` | `"error reading"` | `"missing"` | Check file permissions, verify `.opencode/audit` exists |
| **Alert Rules** | Dashboard Alerts Bar or toast notifications | 0 pending | 1–5 pending | > 5 pending or any critical | Review alerts, resolve escalations, adjust thresholds |

> 📝 **Note**: "Warning" thresholds in this table are approximate guidelines. The actual behavior depends on your configured band thresholds in `config/org_health.yaml` and your alert rules. Customize these to match your organization's risk tolerance.

---

*This section covers the complete health monitoring and diagnostics capability of the CEO Dashboard. For real-time data flow details, see [Section 12 — Real-Time Features](12-real-time-features.md). For troubleshooting other dashboard issues, see [Section 16 — Troubleshooting](16-troubleshooting.md).*

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-08-26 | Doctor Owner | Initial Health Monitoring & Diagnostics section. Covered org health score, health endpoints, KPI snapshot system, alert system, diagnostic workflows, monitoring integration, and quick reference card. |


---

# Section Separator

---

## Technical Setup

This section covers installation, configuration, authentication, and startup procedures for the CEO Dashboard.

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.12+ | Check with `python --version` |
| uv | Latest | Package manager; install from [astral.sh/uv](https://astral.sh/uv) |
| Node.js | Not required | Frontend assets are served statically by FastAPI |
| Git | Any recent | For cloning the repository |
| OS | Windows, macOS, or Linux | PowerShell used in examples below |

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/light-speed-holdings/ai-company-builder.git
cd ai-company-builder

# 2. Install all dependencies (creates .venv if absent)
uv sync --extra dev

# 3. Install pre-commit hooks (ruff, mypy, bandit)
pre-commit install
```

After installation, verify the CLI is available:

```bash
uv run ai-company dashboard --help
```

### Configuration

#### Environment Variables

The dashboard reads configuration from environment variables. Copy `.env.example` to `.env` and fill in actual values:

```bash
cp .env.example .env   # then edit .env with your values
```

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DASHBOARD_PORT` | Port the dashboard listens on | `8420` | No |
| `DASHBOARD_HOST` | Bind address | `127.0.0.1` | No |
| `DASHBOARD_AUTH_MODE` | Auth mode: `api_key` or `open` | `api_key` | No |
| `DASHBOARD_CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:8420` | No |
| `DASHBOARD_RATE_LIMIT` | Max requests per minute per client | `100` | No |
| `DASHBOARD_ADMIN_KEY` | Admin role key (full access) | — | Yes (api_key mode) |
| `DASHBOARD_APPROVE_KEY` | Approve role key (approve/reject) | — | Recommended |
| `DASHBOARD_RUN_KEY` | Run role key (execute tasks, read KPIs) | — | Recommended |
| `DASHBOARD_API_KEY` | Legacy single-key alias for admin | — | Yes (if RBAC keys unset) |
| `OPENCODE_API_KEY` | Primary LLM provider key | — | Yes |
| `GEMINI_API_KEY` | Fallback LLM provider key | — | Recommended |

**Notes:**

- `DASHBOARD_API_KEY` is a legacy alias for `DASHBOARD_ADMIN_KEY`. If both are set, the RBAC key takes precedence.
- Keys are hierarchical: `admin` implies `approve` implies `run`.
- `DASHBOARD_AUTH_MODE=open` is restricted to loopback hosts only (`127.0.0.1` / `::1`). The server refuses to start if `open` mode is used with a non-loopback host.

#### Configuration Files

| File | Purpose |
|------|---------|
| `config/org_health.yaml` | Health score bands (green/amber/red thresholds) and component weights. Weights must sum to 1.0. |
| `config/company/kpis.yaml` | Company-level KPI definitions, targets, and computed values. |
| `.env` | Runtime secrets (never commit to git). |
| `.opencode/inbox.json` | Task queue / fallback data store when SQLite is empty. |

### Authentication Setup

#### Generating RBAC Keys

Generate cryptographically secure keys for each role:

```bash
uv run python -c "import secrets; [print(secrets.token_urlsafe(32)) for _ in range(4)]"
```

This produces 4 keys. Assign them in `.env`:

```
DASHBOARD_ADMIN_KEY=<key1>
DASHBOARD_APPROVE_KEY=<key2>
DASHBOARD_RUN_KEY=<key3>
DASHBOARD_API_KEY=<key4>       # legacy alias, can mirror admin key
```

#### Role Permissions

| Role | Key Variable | Capabilities |
|------|-------------|--------------|
| `admin` | `DASHBOARD_ADMIN_KEY` | All endpoints, full access |
| `approve` | `DASHBOARD_APPROVE_KEY` | Approve/reject tasks and escalations |
| `run` | `DASHBOARD_RUN_KEY` | Execute tasks, read KPIs |
| `admin` (legacy) | `DASHBOARD_API_KEY` | Same as admin; for backward compatibility |

#### Key Rotation Schedule

| Trigger | Action |
|---------|--------|
| Every 90 days | Rotate all 4 keys on schedule |
| Suspected compromise | Rotate immediately |
| Team member with access departs | Rotate immediately |
| Security incident | Rotate immediately |

Full rotation procedure is documented in [docs/DASHBOARD_KEY_ROTATION.md](../../docs/DASHBOARD_KEY_ROTATION.md). Summary: generate new keys → update `.env` → update staging/production secrets → verify health endpoints → revoke old keys → record in CHANGELOG.md.

#### Session Tokens

Session tokens (ADR-013) are minted on-demand via the bootstrap endpoint. They are:

- **Short-lived** — expire after a configurable window
- **IP-bound** — tied to the client IP that requested them
- **In-memory** — not persisted; lost on server restart

Session tokens do not need rotation — only the static environment keys do.

### Starting the Dashboard

```bash
# Start with default settings (port 8420, opens browser)
uv run ai-company dashboard

# Start on a custom port
uv run ai-company dashboard --port 8421

# Start without auto-opening the browser
uv run ai-company dashboard --no-open

# Bind to all interfaces (requires api_key auth mode)
uv run ai-company dashboard --host 0.0.0.0
```

The server prints the startup URL:

```
Starting CEO dashboard at http://127.0.0.1:8420
Press Ctrl+C to stop.
```

#### Verifying Startup

Open a browser to `http://localhost:8420`. The dashboard loads with KPI cards, task kanban, agent status, and charts.

Alternatively, verify via the health endpoint:

```bash
curl -H "X-API-Key: $DASHBOARD_ADMIN_KEY" http://localhost:8420/health
```

Expected response: `{"status":"ok"}` with HTTP 200.

If using browser session tokens (ADR-013), call the bootstrap endpoint first to mint a session, then include the session token in subsequent requests.

#### Staging Environment

For running alongside production or testing configuration changes:

```bash
docker compose -f docker-compose.staging.yml up --build
```

Staging runs on host port **8421** (maps to container 8420). The production dashboard runs on **8420**.

---

## Troubleshooting

### Known Issues

The following issues are tracked and documented in `knowledge/technology/dashboard-known-issues.md`.

| ID | Symptom | Likely Cause | Workaround | Status |
|----|---------|-------------|------------|--------|
| DASH-001 | Dashboard scrolls to top on auto-refresh (every 10 s) | Alpine.js reactivity triggers full DOM re-render on data update | Avoid scrolling during refresh cycles; use keyboard navigation to return to position | Open — Sprint 4 |
| DASH-002 | WebSocket indicator flickers between green (live) and red (offline) | Connection drops and reconnects; basic reconnect logic without exponential backoff | Click "Reconnect" in the header when offline; flicker is visual only, data recovers | Open — Sprint 4 |
| DASH-003 | No loading spinners or indicators appear during data fetch | No loading state tracking in the Alpine.js data model | Wait for data to appear; if empty state persists, refresh the page | Open — Sprint 4 |
| DASH-004 | Failed API calls produce no visible error — data simply doesn't update | `fetchJSON()` catches errors but only logs to browser console | Open browser DevTools console (F12) to see error messages; refresh page | Open — Sprint 4 |
| DASH-005 | Multiple toast notifications overlap each other in the corner | Rapid-fire updates generate multiple toasts before prior ones dismiss | Wait for auto-dismiss; refresh page to clear | Open — Sprint 4 |
| DASH-006 | Kanban card drag is interrupted mid-drag by a data refresh | Auto-refresh fires while user is interacting with the board | Complete drag operations quickly (before next 10 s refresh); refresh page if card misplaces | Open — Sprint 4 |
| DASH-007 | Charts briefly flicker (disappear/reappear) on data update | Chart.js redraws the canvas on data change | Visual only; no data loss. Charts stabilize within a second. | Open — Sprint 4 |
| DASH-008 | No way to manually refresh a single section (KPIs, tasks, agents) | No per-section refresh controls in the UI | Refresh the entire page (F5 or Ctrl+R) | Open — Sprint 4 |

### Authentication Problems

| Symptom | What to Check |
|---------|---------------|
| **"Cannot connect to dashboard"** | Confirm the server is running (`uv run ai-company dashboard`). Check `DASHBOARD_PORT` matches the URL you're opening. Verify `DASHBOARD_HOST` is set to `127.0.0.1` for local access. |
| **401 Unauthorized** | The `X-API-Key` header is missing or the key value is empty/placeholder. Verify `.env` contains actual generated keys, not `your_admin_key_here`. Check for whitespace or newline characters at the end of the key value. |
| **403 Forbidden** | The key you provided belongs to a lower-privilege role. For example, a `run` key cannot access admin-only endpoints. Use the correct key for the endpoint's required role. |
| **Session expired / repeated 401s** | Session tokens (ADR-013) are IP-bound and short-lived. Your IP may have changed (VPN, Wi-Fi switch), or the token expired. Call the bootstrap endpoint again to mint a new session. |
| **Browser shows "open" mode error** | `DASHBOARD_AUTH_MODE=open` only works on loopback (`127.0.0.1`). If deploying on a network, use `api_key` mode and set RBAC keys. |
| **WebSocket connection fails** | For WebSocket URLs, pass the API key as a query parameter (`?api_key=...`). Check that `DASHBOARD_CORS_ORIGINS` includes your origin. |

### Data Issues

| Symptom | What to Check |
|---------|---------------|
| **"No data showing" / blank dashboard** | Check that the SQLite database exists and has records, or that `.opencode/inbox.json` contains task data. Run `uv run python scripts/compute_company_kpis.py` to verify KPI computation. |
| **KPIs show "n/a" or null** | Some KPIs (KPI-001, KPI-002, KPI-005) have no data source yet — this is expected. KPI-003 and KPI-004 compute from `.opencode/inbox.json`. Verify inbox.json is populated. |
| **Stale data / "last updated" timestamp is old** | The dashboard polls every 10 seconds. If data hasn't changed, the timestamp is correct. If you suspect a data pipeline issue, run `python scripts/compute_company_kpis.py --write` to refresh computed values. |
| **Health score is missing** | Health score requires at least one task in the database. Check that `config/org_health.yaml` weights sum to 1.0. Verify SQLite is accessible. |
| **Charts show no data** | Confirm the relevant data source (inbox.json or SQLite) has records. Check the browser console (F12) for API errors logged by `fetchJSON()`. |

### Performance Issues

| Symptom | What to Check |
|---------|---------------|
| **Dashboard loads slowly** | Check network latency to the server. On first load, static assets (Tailwind CSS, Chart.js) must download. Subsequent loads use browser cache. Verify SQLite database is not excessively large. |
| **High memory usage after extended sessions** | WebSocket reconnections may accumulate event listeners. Refresh the page periodically during long sessions. Restart the server if memory grows unbounded. |
| **API requests are slow** | Check `DASHBOARD_RATE_LIMIT` — if set too low, legitimate requests may be throttled. Verify the SQLite database is not locked by a concurrent process. Check LLM provider latency if KPI computation involves AI calls. |
| **Server won't start — port in use** | Another process is using port 8420. Either stop the other process or start the dashboard on a different port: `uv run ai-company dashboard --port 8421`. |

### Getting Help

| Channel | Use For |
|---------|---------|
| **GitHub Issues** | Bug reports, feature requests. Include the issue ID (e.g., DASH-001) if referencing a known issue. |
| **Browser Console (F12)** | First step for any UI issue. API errors, WebSocket failures, and JS exceptions are logged here. |
| **Server Logs (terminal)** | First step for backend issues. uvicorn logs all requests and errors to stdout. |
| **Dashboard "Report Issue" Button** | In-dashboard feedback form (footer). Automatically collects browser info, connection status, and recent errors. |
| **Support Knowledge Base** | `knowledge/technology/dashboard-known-issues.md` — full details on all tracked issues with root cause analysis. |

When reporting an issue, include:

1. Steps to reproduce
2. Expected vs. actual behavior
3. Browser console output (F12 → Console tab)
4. Server terminal output
5. `curl` output from `http://localhost:8420/health` (if server is running)
6. Environment: OS, Python version, dashboard port


---

# Section Separator

---

# Documentation Standards

> **Version**: v1.0
> **Date**: 2026-08-26
> **Author**: Technical Documentation Lead
> **Status**: Active — applies to all sections of the CEO Dashboard User Guide

---

## Table of Contents

1. [Voice and Tone](#1-voice-and-tone)
2. [Formatting Conventions](#2-formatting-conventions)
3. [Diagram Specifications](#3-diagram-specifications)
4. [Accessibility Requirements](#4-accessibility-requirements)
5. [Screenshot Placeholders](#5-screenshot-placeholders)
6. [Cross-Reference Conventions](#6-cross-reference-conventions)
7. [Version History](#7-version-history)
8. [Contributing to This Guide](#8-contributing-to-this-guide)
9. [Glossary Convention](#9-glossary-convention)

---

## 1. Voice and Tone

Write in a **professional but approachable** style. The CEO Dashboard User Guide is read by non-technical executives, operations leads, and technical stakeholders alike. Every sentence should be immediately understandable without requiring domain expertise.

### 1.1 Pronoun and Perspective Rules

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Second person for addressing the reader | "You can filter tasks by status." | "The user can filter tasks by status." |
| Active voice for all instructions | "Click **Approve** to confirm." | "The approval is confirmed by clicking **Approve**." |
| Present tense for UI descriptions | "The sidebar displays department names." | "The sidebar will display department names." |
| Past tense for completed actions | "You approved three tasks." | "You have approved three tasks." |

### 1.2 Tone Calibration

- **Instructions**: Direct and imperative. "Select **Settings**." not "You might want to consider selecting Settings."
- **Explanations**: Calm and factual. Avoid hedging ("should", "might", "could potentially").
- **Warnings**: Urgent but not alarmist. State the consequence, then the mitigation.
- **Tips**: Helpful and concise. Lead with the benefit.

### 1.3 Terminology Discipline

Use the canonical term on first mention in every section. Subsequent mentions may use abbreviations if defined. Never invent terminology — if a term is not in the [Glossary](#9-glossary-convention), add it there first.

---

## 2. Formatting Conventions

### 2.1 Heading Hierarchy

The guide follows a strict four-level heading hierarchy. Never skip a level.

| Level | Markdown | Usage | Example |
|-------|----------|-------|---------|
| 1 | `#` | Document title — one per file | `# CEO Dashboard User Guide` |
| 2 | `##` | Major sections | `## Getting Started` |
| 3 | `###` | Sub-sections within a major section | `### Navigating the Dashboard` |
| 4 | `####` | Detail areas within a sub-section | `#### Filtering by Department` |

> ⚠️ **Warning**: Heading level 5 (`#####`) is **prohibited**. If you find you need it, restructure the content into separate sub-sections.

### 2.2 Inline Formatting

| Element | Format | Example |
|---------|--------|---------|
| UI element names (buttons, menus, tabs, fields, links) | **Bold** | Click **Approve**. Select the **Tasks** tab. |
| Technical values (env vars, ports, commands, file paths, API routes) | `Code font` | Set `DASHBOARD_PORT` to `8420`. |
| Keys and keyboard shortcuts | `Code font` | Press `Ctrl + K` to open the command bar. |
| File names | `Code font` | Edit `company-registry.yaml`. |
| New terms (first use only) | **Bold**, then link to glossary | The **Org Health Score** ([see Glossary](#9-glossary-convention)). |
| Emphasis (sparingly) | *Italic* | This setting is *permanent* and cannot be undone. |

### 2.3 Blockquotes — Callouts

Use blockquotes with emoji prefixes for callouts. Always place a blank line after the callout opening.

#### Tips

```markdown
> 💡 **Tip**: You can pin frequently used filters to the sidebar for faster access.
```

> 💡 **Tip**: You can pin frequently used filters to the sidebar for faster access.

#### Warnings

```markdown
> ⚠️ **Warning**: Rejecting an approval request is irreversible. Confirm with your team before proceeding.
```

> ⚠️ **Warning**: Rejecting an approval request is irreversible. Confirm with your team before proceeding.

#### Notes

```markdown
> 📝 **Note**: The dashboard refreshes KPI data every 60 seconds by default. This interval is configurable via `KPI_REFRESH_INTERVAL`.
```

> 📝 **Note**: The dashboard refreshes KPI data every 60 seconds by default. This interval is configurable via `KPI_REFRESH_INTERVAL`.

### 2.4 Tables

- Every table **must** have a header row.
- Align columns for readability in source markdown (pipe alignment is optional but encouraged).
- Use tables for structured data: option lists, parameter references, state enumerations, and comparison matrices.
- Do not use tables for narrative text or multi-paragraph explanations.

### 2.5 Code Blocks

- Every fenced code block **must** specify a language.
- Use `bash` for shell commands, `python` for Python, `json` for JSON payloads, `yaml` for YAML config, `javascript` for frontend code.
- Include a one-line comment or label above non-trivial code blocks when context is needed.

```markdown
\`\`\`bash
ai-company dashboard start --port 8421
\`\`\`
```

### 2.6 Lists

- Use **numbered lists** for sequential steps or ranked items.
- Use **bullet lists** for unordered collections.
- Indent nested lists by two spaces.
- Keep list items to one sentence where possible. If an item requires explanation, follow it with a paragraph rather than nesting deeper.

---

## 3. Diagram Specifications

The CEO Dashboard User Guide requires the following diagrams. Each is specified here for a diagram author or tool to produce. Diagrams should use a dark-background palette consistent with the JARVIS theme (dark grays, neon cyan/green accents, muted borders).

### 3.1 Navigation Flow Diagram

**Purpose**: Show the user how the dashboard navigation is structured — from sidebar to pages to command bar.

**Components**:

```
┌──────────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│     Sidebar       │────▶│      Page Area       │────▶│   Command Bar    │
│                   │     │                      │     │   (Ctrl + K)     │
│  ├─ Dashboard     │     │  ┌────────────────┐  │     │                  │
│  ├─ Agents        │     │  │ Page Content   │  │     │  Search tasks    │
│  ├─ Tasks         │     │  │ (KPIs, tables, │  │     │  Jump to agent   │
│  ├─ Approvals     │     │  │  charts)       │  │     │  Open settings   │
│  ├─ Escalations   │     │  └────────────────┘  │     │                  │
│  ├─ KPIs          │     │                      │     └──────────────────┘
│  ├─ Costs         │     └─────────────────────┘
│  └─ Settings      │
└──────────────────┘
```

**Label each node** with its page name. Show directional arrows for navigation paths. Include the keyboard shortcut for the command bar.

### 3.2 KPI Hierarchy Diagram

**Purpose**: Show how the Org Health Score is composed from its four component metrics and their source data.

**Components**:

```
┌─────────────────────────────────────────────────────────────┐
│                   ORG HEALTH SCORE                          │
│                     (composite)                              │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────┐ ┌────────┐ │
│  │ Task Success  │ │Agent Utiliz. │ │Cost      │ │Error   │ │
│  │ Rate (30%)   │ │    (25%)     │ │Eff.(25%) │ │Rate    │ │
│  │              │ │              │ │          │ │ (20%)  │ │
│  │ ─ source ──▶ │ │ ─ source ──▶ │ │─ source▶ │ │─ src─▶ │ │
│  │ inbox.json   │ │ registry +   │ │ cost log │ │audit   │ │
│  │              │ │ task complet.│ │          │ │trail   │ │
│  └──────────────┘ └──────────────┘ └──────────┘ └────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Show**: the composite score at top, four component boxes with weights, and source data feeds beneath each component.

### 3.3 Authentication Flow Diagram

**Purpose**: Trace the full authentication lifecycle from login through API request authorization.

**Sequence**:

```
User ──▶ Dashboard Login Page ──▶ POST /api/v1/auth/login
         (credentials)              │
                                    ▼
                              Validate API Key
                              (X-API-Key header)
                                    │
                          ┌─────────┴──────────┐
                          │                    │
                       Valid               Invalid
                          │                    │
                          ▼                    ▼
                   Issue Session Token    401 Unauthorized
                   (JWT / cookie)
                          │
                          ▼
                   API Request + Token
                          │
                          ▼
                   RBAC Check
                   (admin / approve / run)
                          │
                   ┌──────┴──────┐
                   │             │
                Granted       Denied
                   │             │
                   ▼             ▼
              200 OK        403 Forbidden
```

**Show**: each step as a labeled box, decision points as diamonds or branching paths, and the three RBAC roles (admin, approve, run) as labels on the RBAC check node.

### 3.4 Task Lifecycle Diagram

**Purpose**: Map every task state and every valid transition between them.

**States and transitions**:

```
┌───────────┐     ┌───────────┐     ┌──────────────┐
│  Backlog   │────▶│   Ready   │────▶│ In Progress  │
└───────────┘     └───────────┘     └──────┬───────┘
                        ▲                    │
                        │              ┌─────┴─────┐
                        │              │           │
                   ┌────┴────┐    ┌────▼────┐ ┌───▼────┐
                   │ Reopened│    │ Review  │ │ Failed │
                   └─────────┘    └────┬────┘ └───┬────┘
                                       │           │
                                       ▼           ▼
                                  ┌─────────┐ ┌─────────┐
                                  │  Done   │ │ Escalated│
                                  └─────────┘ └────┬────┘
                                                    │
                                                    ▼
                                              ┌──────────┐
                                              │ Resolved │
                                              └──────────┘
```

**Label each transition arrow** with the action that triggers it (e.g., "assign", "submit for review", "approve", "reject", "escalate").

### 3.5 Escalation Flow Diagram

**Purpose**: Show the escalation lifecycle from trigger through resolution.

**Components**:

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Trigger      │────▶│  Escalation      │────▶│  Review Queue   │
│               │     │  Queue           │     │                 │
│ • Task fails  │     │  (.opencode/     │     │  Dashboard UI   │
│ • Timeout     │     │   escalations/)  │     │  /escalations   │
│ • Agent error │     │                  │     │                 │
│ • HITL block  │     │  Sorted by       │     │  CEO reviews    │
└──────────────┘     │  severity + time │     │  and decides    │
                      └──────────────────┘     └────────┬────────┘
                                                        │
                                                  ┌─────┴──────┐
                                                  │            │
                                                  ▼            ▼
                                            ┌──────────┐ ┌──────────┐
                                            │ Resolved │ │ Reassigned│
                                            └──────────┘ └──────────┘
```

**Show**: the three trigger categories, the queue mechanism, the review step, and the two resolution outcomes.

### 3.6 WebSocket Architecture Diagram

**Purpose**: Illustrate the real-time data flow between client and server via WebSocket.

**Components**:

```
┌──────────────────────┐                    ┌──────────────────────┐
│      CLIENT           │    WebSocket       │      SERVER          │
│   (Browser)           │◀══════════════════▶│   (FastAPI + ws.py)  │
│                       │   ws://host/ws/v1  │                      │
│  ┌─────────────────┐  │                    │  ┌────────────────┐  │
│  │ Alpine.js Store  │  │  subscribe        │  │ Topic Manager  │  │
│  │ (x-data)        │──┼───────────────────▶│  │                │  │
│  └─────────────────┘  │                    │  │ Topics:        │  │
│                       │  ◀────────────────┼──│  • kpi_update   │  │
│  ┌─────────────────┐  │  broadcast        │  │  • alert        │  │
│  │ Reactive UI      │  │                    │  │  • task_update  │  │
│  │ (auto-update)    │  │                    │  │  • escalation   │  │
│  └─────────────────┘  │                    │  │  • org_health   │  │
└──────────────────────┘                    └──────────────────────┘
```

**Show**: bidirectional data flow, the subscribe/unsubscribe model, all five topic names, and the reactive update loop on the client.

---

## 4. Accessibility Requirements

Every section of the CEO Dashboard User Guide must meet the following accessibility standards. These are non-negotiable.

### 4.1 Images and Diagrams

- Every image, diagram, and screenshot **must** include descriptive alt text.
- Alt text should describe the content and purpose of the image, not its appearance.
- Alt text format: `[Image: <description of what the image shows and why it matters>]`

**Example**:
```markdown
![Org Health Score dashboard showing a gauge at 82 with four component cards](path/to/image.png)
```
*Alt text: "The Org Health Score gauge displays 82 in the green band, with four component cards below showing Task Success Rate at 72%, Agent Utilization at 85%, Cost Efficiency at 68%, and Error Rate at 91%."*

### 4.2 Heading Hierarchy

- Heading levels must be **sequential** — never skip from `##` to `####`.
- Every section must have at least one `##` heading.
- Every `####` heading must have a parent `###` heading.

### 4.3 Color and Visual Indicators

- **Color is never the sole indicator** of meaning. Always pair color with text labels, icons, or symbols.
- When describing status bands (green, yellow, red), always include the text equivalent: "green band (healthy)".
- Dashboard tables must use both color badges **and** text status labels.

**Example**:
```markdown
> ⚠️ **Warning**: The status indicator shows both a colored badge and a text label.
> Never reference only the color — always include the text.
```

### 4.4 Tables

- All tables **must** have a header row.
- Tables must not be used for layout purposes — only for structured data.
- For complex tables, provide a brief introductory sentence explaining what the table contains.

### 4.5 Code Blocks

- Every fenced code block **must** specify a language for syntax highlighting.
- Screen readers and assistive technologies use the language hint to provide appropriate context.

---

## 5. Screenshot Placeholders

Screenshots are critical for a visual dashboard guide. Use the following convention to mark locations where screenshots should be added. This allows the document structure to be finalized before visual assets are produced.

### 5.1 Syntax

```markdown
[Screenshot: <description> — <page or feature>]
```

### 5.2 Rules

- The description should be specific enough that a screenshot author can capture the correct view.
- Place the placeholder on its own line, centered between the paragraphs it illustrates.
- After the screenshot is added, replace the placeholder with a standard markdown image reference.
- Never leave a placeholder in a published section without at least a TODO comment.

### 5.3 Examples

```markdown
[Screenshot: Full dashboard overview with Org Health Score gauge and four KPI cards — Dashboard Home]

[Screenshot: Task board filtered to "In Progress" status with three agent columns — Tasks Tab]

[Screenshot: Escalation detail panel showing trigger context and resolution options — Escalations Tab]

[Screenshot: Settings page with environment variable configuration fields — Settings Page]

[Screenshot: Command bar open with search results for "approval" — Command Bar (Ctrl+K)]
```

### 5.4 Screenshot Naming Convention

When screenshots are added, name them descriptively:

```
dashboard-home-overview.png
tasks-tab-filtered.png
escalation-detail-panel.png
settings-env-config.png
command-bar-search.png
```

Use lowercase, hyphen-separated names. Prefix with the page or feature name.

---

## 6. Cross-Reference Conventions

Cross-references link related content across sections of the guide. They improve navigability and reduce duplication.

### 6.1 Format

Use the standard markdown link format with an anchor target:

```markdown
[Section Name](#section-anchor)
```

### 6.2 Anchor Generation Rules

Anchors are derived from the section heading, lowercased, with spaces replaced by hyphens:

| Heading | Anchor |
|---------|--------|
| `## Getting Started` | `#getting-started` |
| `### Navigating the Dashboard` | `#navigating-the-dashboard` |
| `#### Filtering by Department` | `#filtering-by-department` |

### 6.3 Link Text

- Link text should be the **section name** — not "click here" or "see above".
- For links to other files in the guide, include the file name in parentheses:

```markdown
See [Diagram Specifications](08-documentation-standards.md#3-diagram-specifications) for details.
```

### 6.4 External Links

- Link to external documentation (FastAPI, Alpine.js, Chart.js, Tailwind) only when the reader needs to go deeper than the guide covers.
- Always use HTTPS URLs.
- Open external links in a new tab (if rendering supports it): `[FastAPI docs](https://fastapi.tiangolo.com/){:target="_blank"}`.

### 6.5 Rules

- Do not create circular references.
- Every cross-reference must resolve — never link to a section that does not exist yet.
- If a section is planned but not yet written, add a `TODO` comment instead of a broken link.

---

## 7. Version History

Track every substantive change to the User Guide in the version history table below. A "substantive change" is any edit that affects content, accuracy, or structure — not typo fixes or whitespace.

### 7.1 Format

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-08-26 | Technical Documentation Lead | Initial Documentation Standards appendix. Defined voice/tone, formatting, diagrams, accessibility, screenshots, cross-references, glossary convention, and contribution guide. |

### 7.2 Rules

- Version numbers follow [Semantic Versioning](https://semver.org/): `vMAJOR.MINOR.PATCH`.
  - **Major**: Breaking changes to section structure or removal of sections.
  - **Minor**: New sections, new diagrams, expanded content.
  - **Patch**: Corrections, clarifications, typo fixes.
- Date format: `YYYY-MM-DD`.
- Author: Use the role title or agent name — not a personal name.
- Changes: One sentence per change, beginning with a verb (Added, Updated, Removed, Fixed, Clarified).

---

## 8. Contributing to This Guide

This section describes how anyone — human or agent — can contribute to the CEO Dashboard User Guide.

### 8.1 How to Suggest an Edit

1. **Open a pull request** against the repository with your proposed change.
2. In the PR description, state:
   - Which section you are editing.
   - What the change is and why it is needed.
   - Whether the change affects other sections (cross-reference audit).
3. The Technical Documentation Lead reviews the PR for adherence to this standards document.

### 8.2 How to Add a New Section

1. **Check the Table of Contents** in the target file. Ensure the new section fits the existing structure.
2. **Follow the heading hierarchy** — do not create orphaned `###` or `####` headings.
3. **Add a version history entry** in both the new file's version table and any parent guide's version table.
4. **Update all cross-references** that may be affected.
5. **Run the ECL lint check** before submitting: `pwsh scripts/lint-ecl.ps1`.

### 8.3 How to Report an Error

1. **Open a GitHub issue** with the label `documentation`.
2. Include:
   - The file name and section heading.
   - The incorrect text (quote it exactly).
   - The correct information, with a source link if available.
3. For urgent accuracy issues (wrong port number, incorrect API endpoint, security-relevant error), tag the Technical Documentation Lead directly.

### 8.4 How to Add a Screenshot

1. Capture the screenshot using the JARVIS-themed dashboard (dark background, neon accents).
2. Follow the [screenshot naming convention](#54-screenshot-naming-convention).
3. Place images in the `docs/ceo-dashboard-user-guide/images/` directory.
4. Replace the corresponding `[Screenshot: ...]` placeholder with a standard markdown image reference.
5. Verify the alt text meets the [accessibility requirements](#41-images-and-diagrams).

### 8.5 Review Checklist

Before submitting a PR that modifies this guide, verify:

- [ ] Heading hierarchy is sequential (no skipped levels).
- [ ] All code blocks specify a language.
- [ ] All tables have header rows.
- [ ] Bold is used for UI elements, code font for technical values.
- [ ] Callouts use the correct emoji prefix (💡, ⚠️, 📝).
- [ ] Cross-references resolve to existing sections.
- [ ] Version history is updated.
- [ ] Screenshots have descriptive alt text.
- [ ] No color is used as a sole indicator.

---

## 9. Glossary Convention

The CEO Dashboard uses domain-specific terminology that must be consistent across all sections. This section defines the convention for how terms are managed.

### 9.1 Single Definition, Multiple References

- Every glossary term is defined **once**, in the Glossary section of the User Guide.
- All other sections reference the glossary definition by linking to it — they do **not** redefine the term.
- On first mention in a section, the term should be bolded and linked to the glossary.

**Example**:
```markdown
The **Org Health Score** ([see Glossary](#glossary)) is a weighted composite of four metrics.
```

### 9.2 Adding a New Term

1. Verify the term is not already defined in the Glossary.
2. Add the term in **alphabetical order** within the Glossary table.
3. Provide a one-sentence definition suitable for a non-technical reader.
4. Include the technical implementation detail in parentheses if relevant.
5. Update the Table of Contents if the Glossary section has moved.

### 9.3 Glossary Table Format

| Term | Definition |
|------|------------|
| **Approval Gate** | A human-in-the-loop checkpoint that requires explicit CEO approval before an agent action proceeds. Implemented via `orchestrator/approvals.yaml`. |
| **Command Bar** | A keyboard-activated search overlay (`Ctrl + K`) for quick navigation to pages, agents, and tasks. |
| **Escalation** | An issue that exceeds an agent's authority or capability and is routed to the CEO for resolution. Stored in `.opencode/inbox.json` with status `escalated`. |
| **JARVIS Theme** | The dashboard's dark visual theme — dark gray backgrounds with neon cyan and green accents. Defined in the Tailwind config and `style.css`. |
| **KPI** | Key Performance Indicator — a quantified metric used to measure department or organizational health. |
| **Org Health Score** | A composite score (0–100) aggregating task success rate, agent utilization, cost efficiency, and error rate into a single organizational health metric. Band: green (≥80), yellow (60–79), red (<60). |
| **RBAC** | Role-Based Access Control — the permission model for the dashboard. Three roles: `admin` (full access), `approve` (approve/reject tasks), `run` (execute tasks, read KPIs). |
| **Task** | A unit of work assigned to an agent, tracked through a lifecycle from backlog to done. Stored in `.opencode/inbox.json`. |
| **Topic** | A named WebSocket channel for real-time data push. Clients subscribe to topics (e.g., `kpi_update`, `alert`, `task_update`). |

### 9.4 Rules

- Definitions must be **stable** — do not change a term's meaning without updating every section that references it.
- Do not use acronyms in definitions without first spelling them out.
- If a term has both a business meaning and a technical meaning, lead with the business definition and add the technical detail second.
- When a term appears in a diagram label, use the bold form (e.g., **Org Health Score**) not the code form.

---

*This standards document is maintained by the Technical Documentation Lead. All sections of the CEO Dashboard User Guide must conform to the conventions defined here. When in doubt, refer to this appendix.*
