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
