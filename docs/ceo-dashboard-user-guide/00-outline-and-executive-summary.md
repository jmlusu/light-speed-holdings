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
