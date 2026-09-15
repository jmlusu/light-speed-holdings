# Feature Completeness: Executive KPIs, Org Chart, Alerting

## Goal
Deliver the three remaining "business readiness" pillars the CEO needs: consolidated executive KPIs, a rich interactive org chart, and an in-house alerting system that escalates across channels.

## Current State

| Feature | Status | Gap |
|---------|--------|-----|
| Executive KPIs | Partial — 7 department collectors exist, company-level aggregation is formula-driven | No unified "scorecard" endpoint with health indicators, trends, targets |
| Org Chart | Basic tree from registry via `/api/v1/org-chart` | No capacity, succession risk, performance rating, span-of-control |
| Alerting | Threshold rules in `analytics.py` (7 default rules) | No multi-channel delivery (email, WS, SMS), no escalation tiers, no runbook links |

---

## Phase 1: Executive KPI Scorecard (Week 1-2)

### Task FK-001: Unified Executive KPI Endpoint
**Owner**: `dashboard-owner` | **Reports to**: CTO | **Effort**: 3 days

**Endpoint**: `GET /api/v1/ceo-dashboard`

**Current**: `/api/v1/ceo-dashboard` exists (`api.py:514`) but returns raw KPI shapes without executive-level synthesis.

**Target Response Shape**:
```json
{
  "collected_at": "2026-08-31T10:00:00Z",
  "period_days": 30,
  "executive_summary": {
    "health_score": 82,
    "health_trend": "improving",
    "critical_items": 2,
    "active_escalations": 3,
    "pending_approvals": 5
  },
  "kpis": [
    {
      "id": "task_throughput",
      "label": "Task Throughput",
      "value": 142,
      "unit": "tasks/week",
      "target": 150,
      "status": "on_track",
      "gap": -8,
      "trend": "up",
      "department": "engineering",
      "source": "real_telemetry"
    },
    {
      "id": "agent_utilization",
      "label": "Agent Utilization",
      "value": 73.2,
      "unit": "%",
      "target": 80,
      "status": "attention",
      "gap": -6.8,
      "trend": "stable",
      "department": "operations",
      "source": "real_telemetry"
    }
  ],
  "department_health": {
    "engineering": { "score": 85, "trend": "up" },
    "operations": { "score": 72, "trend": "stable" },
    "finance": { "score": 91, "trend": "up" }
  },
  "risk_indicators": [
    { "severity": "warning", "message": "LLM costs trending +15% WoW", "action": "Review agent budgets" },
    { "severity": "critical", "message": "3 escalations unresolved >24h", "action": "Escalate to VP" }
  ]
}
```

**Implementation Steps**:
1. Create `dashboard/kpis/executive_scorecard.py` with `ExecutiveScorecardCollector`
2. Implement `_compute_health_score()` — weighted average across 7 department health scores
3. Implement `_compute_trends()` — period-over-period comparison using `analytics.py` history
4. Implement `_generate_risk_indicators()` — threshold-based rules (cost >budget 90%, escalations >24h, etc.)
5. Wire into `api.py` as `GET /api/v1/ceo-dashboard` (replace existing stub)
6. Add unit tests: 7 department collectors return mock data → scorecard produces correct health score, trends, risks
7. Add integration test: full KPI collection → scorecard → validate shape

**Verification**:
- `pytest tests/unit/test_company_kpis.py -v` (existing 7 tests pass)
- `pytest tests/unit/test_executive_scorecard.py -v` (new)
- Manual: `ai-company dashboard` → CEO Hero section shows health score + trend

---

### Task FK-002: Executive KPI Target Definitions
**Owner**: `business-intelligence-engineer` (reports to CDO) | **Effort**: 2 days

**File**: `company/config/kpis.yaml` (extend existing)

**Additions**:
```yaml
executive_targets:
  task_throughput:
    target: 150
    unit: "tasks/week"
    direction: "higher_is_better"
    critical_below: 100
    warning_below: 130

  agent_utilization:
    target: 80
    unit: "%"
    direction: "higher_is_better"
    critical_below: 60
    warning_below: 70

  cost_efficiency:
    target: 5.00
    unit: "USD/task"
    direction: "lower_is_better"
    critical_above: 10.00
    warning_above: 7.50

  build_success_rate:
    target: 99
    unit: "%"
    direction: "higher_is_better"
    critical_below: 95
    warning_below: 98

  escalation_resolution_time:
    target: 4
    unit: "hours"
    direction: "lower_is_better"
    critical_above: 24
    warning_above: 8

  approval_turnaround:
    target: 2
    unit: "hours"
    direction: "lower_is_better"
    critical_above: 8
    warning_above: 4
```

**Verification**:
- `ai-company validate` — targets parse correctly
- `pytest tests/unit/test_kpi_collectors.py -v` — collectors respect targets

---

### Task FK-003: KPI History & Trend Computation
**Owner**: `observability-engineer` | **Effort**: 2 days

**File**: `dashboard/analytics.py` (extend existing `KPIHistoryStore`)

**Current**: History stored as NDJSON, basic `compute_trends()` exists but not wired to executive scorecard.

**Enhancements**:
- [ ] Add `compute_period_comparison(dept, kpi_key, current_period, previous_period)` → returns `{value, change, change_pct}`
- [ ] Add `compute_moving_average(dept, kpi_key, window_days=7)` → returns smoothed trend
- [ ] Add `detect_anomaly(dept, kpi_key, threshold_sigma=2)` → returns `True/False`
- [ ] Wire `ExecutiveScorecardCollector` to call `compute_trends()` for each KPI

**Verification**:
- `pytest tests/test_kpi_analytics.py -v` (existing 12 tests)
- Add 3 new tests for period comparison, moving average, anomaly detection

---

## Phase 2: Rich Org Chart (Week 3-4)

### Task FK-004: Enhanced Org Chart Data Structure
**Owner**: `graph-owner` (reports to CTO) | **Effort**: 3 days

**Current**: `/api/v1/org-chart` builds tree from `company-registry.yaml` with `reportsTo` relationships (`api.py:261-284`)

**Target Response Shape**:
```json
{
  "root": "human-ceo",
  "nodes": [
    {
      "id": "cto",
      "name": "Chief Technology Officer",
      "title": "CTO",
      "type": "executive",
      "department": "Technology",
      "tier": 2,
      "reports_to": "chief-of-staff",
      "direct_reports": ["vp-engineering", "lead-backend", "lead-frontend", "solution-architect", "devops-lead"],
      "metrics": {
        "capacity": 75,
        "active_tasks": 8,
        "completed_tasks": 23,
        "utilization_trend": "stable"
      },
      "risk": {
        "succession_risk": "medium",
        "bus_factor": 1,
        "last_review": "2026-07-15"
      },
      "skills": ["architecture", "system-design", "security"]
    }
  ],
  "edges": [
    { "from": "human-ceo", "to": "chief-of-staff", "type": "reports_to" },
    { "from": "chief-of-staff", "to": "cto", "type": "reports_to" }
  ],
  "summary": {
    "total_agents": 135,
    "executives": 18,
    "specialists": 117,
    "avg_span_of_control": 4.2,
    "max_depth": 5,
    "critical_roles": 12
  }
}
```

**Implementation Steps**:
1. Extend `graph/engine.py` `GraphEngine` to add `org_chart_with_metrics()` method
2. Query `MessageBus` inbox for task counts per agent (utilization)
3. Query `KPIHistoryStore` for agent performance trends
4. Compute `capacity` = active_tasks / (active_tasks + queued_tasks) * 100
5. Compute `succession_risk` based on: direct reports count, unique skills, tenure
6. Add to `api.py`: `GET /api/v1/org-chart?include_metrics=true`
7. Wire frontend: `command-center.html` SVG overlay shows capacity as color (green >80%, yellow 60-80%, red <60%)

**Verification**:
- `pytest tests/unit/test_graph.py -v` (existing 45 tests)
- Add 5 tests for metrics computation, succession risk, span-of-control
- Manual: `GET /api/v1/org-chart?include_metrics=true` → nodes have `metrics` and `risk` objects

---

### Task FK-005: Org Chart Interactive Features
**Owner**: `frontend-engineer` | **Effort**: 3 days

**File**: `dashboard/static/js/org-chart-interactive.js` (exists, ~200 lines)

**Enhancements**:
- [ ] **Click-to-drill**: Click node → slide-out panel with agent details, recent tasks, KPIs
- [ ] **Search**: Type-ahead search filtering nodes by name, department, skill
- [ ] **Filter by department**: Dropdown to show only Technology, Operations, etc.
- [ ] **Filter by capacity**: Show only agents with capacity <50% (bottlenecks)
- [ ] **Zoom/Pan**: Scroll-wheel zoom, drag to pan for large org charts
- [ ] **Expand/Collapse**: Click executive to collapse/expand their subtree
- [ ] **Export**: Download as PNG or SVG

**UI Components** (in `templates/org-chart.html`):
- Filter bar: search input, department dropdown, capacity slider
- Detail panel: slide-out from right with agent info
- Legend: color coding for capacity, type (executive/specialist), department

**Verification**:
- Playwright E2E: `tests/test_org_chart_e2e.py` (new)
  - Page loads, SVG renders
  - Click node → detail panel opens
  - Search filters nodes
  - Department filter works
  - Zoom/pan works on trackpad

---

### Task FK-006: Org Chart Data Validation
**Owner**: `registry-owner` (reports to CTO) | **Effort**: 1 day

**Checks**:
- [ ] Every agent has `reports_to` field (no orphan nodes except root)
- [ ] No circular references (A→B→C→A)
- [ ] Span of control ≤10 (per `vp_engineering` guidelines)
- [ ] Every executive has at least 1 direct report
- [ ] `direct_reports` list matches inverse of `reports_to` references
- [ ] Department assignments consistent with registry

**Wire into**: `ai-company validate` CLI command + CI gate

**Verification**:
- `ai-company validate` passes
- `pytest tests/unit/test_registry.py -v` (existing 89 tests)
- Add 3 tests for circular detection, orphan detection, span validation

---

## Phase 3: In-House Alerting System (Week 5-6)

### Task FK-007: Alert Engine Core
**Owner**: `dashboard-owner` | **Effort**: 3 days

**File**: `dashboard/alerting/` (new package)

**Architecture**:
```
dashboard/alerting/
├── __init__.py          # AlertEngine public API
├── engine.py            # AlertEngine — rule evaluation, state machine
├── rules.py             # AlertRule model, 12 default rules
├── channels.py          # ChannelRouter — WS, email, webhook
├── escalation.py        # TierRouter — 5-tier escalation matrix
└── state.py             # AlertStateStore — JSON persistence
```

**Alert Rule Model**:
```python
from pydantic import BaseModel
from enum import Enum

class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class AlertRule(BaseModel):
    id: str
    name: str
    description: str
    source: str                    # "kpi" | "escalation" | "approval" | "system"
    metric: str                    # e.g., "build_success_rate", "escalation_count"
    condition: str                 # "lt" | "gt" | "eq" | "gte" | "lte"
    threshold: float
    severity: Severity
    cooldown_minutes: int = 30     # Don't re-alert within this window
    escalation_tier: int = 1       # 1-5, starts here and escalates
    runbook_url: str | None = None
    enabled: bool = True
```

**Default Rules** (12):
1. `build_success_rate_lt_95` — CRITICAL
2. `escalation_count_gt_5` — WARNING
3. `escalation_age_gt_24h` — CRITICAL
4. `approval_pending_gt_10` — WARNING
5. `cost_daily_gt_budget_50pct` — WARNING
6. `cost_daily_gt_budget_90pct` — CRITICAL
7. `agent_utilization_lt_50` — WARNING
8. `agent_utilization_lt_30` — CRITICAL
9. `task_failure_rate_gt_10pct` — WARNING
10. `ws_connection_drop_rate_gt_5pct` — WARNING
11. `kpi_collection_failure` — CRITICAL
12. `system_health_score_lt_60` — CRITICAL

**AlertEngine API**:
```python
class AlertEngine:
    def evaluate_rules(self, kpi_snapshot: dict) -> list[Alert]:
        """Evaluate all enabled rules against current KPIs."""

    def acknowledge(self, alert_id: str, user: str) -> None:
        """User acknowledges alert, stops escalation."""

    def resolve(self, alert_id: str, resolution: str) -> None:
        """Alert resolved, close it."""

    def get_active_alerts(self) -> list[Alert]:
        """Return all unresolved alerts."""

    def get_alert_history(self, hours: int = 24) -> list[Alert]:
        """Return historical alerts."""
```

**Verification**:
- `pytest tests/unit/test_alert_engine.py -v` (new, 20+ tests)
- Unit test each rule against mock KPI snapshots
- Integration test: rule triggers → alert created → state persisted → cooldown respected

---

### Task FK-008: Multi-Channel Alert Delivery
**Owner**: `observability-engineer` | **Effort**: 2 days

**Channels** (in priority order):
1. **WebSocket** — real-time toast/banner in dashboard (immediate)
2. **Email** — executive digest (via local SMTP or API)
3. **Webhook** — external integrations (Slack, Teams, etc.)

**Implementation**:
```python
class ChannelRouter:
    def route(self, alert: Alert) -> None:
        """Route alert through configured channels based on severity."""

        # Always: WebSocket broadcast (immediate)
        if alert.severity in (Severity.WARNING, Severity.CRITICAL):
            broadcast_alert(alert)

        # Critical: email to CEO, CTO, COO
        if alert.severity == Severity.CRITICAL:
            self._send_email(
                recipients=["ceo@company.com", "cto@company.com", "coo@company.com"],
                subject=f"[CRITICAL] {alert.name}",
                body=self._format_email(alert)
            )

        # Critical: webhook (Slack/Teams)
        if alert.severity == Severity.CRITICAL and self._webhook_url:
            self._send_webhook(alert)
```

**Email Template**:
```html
<h2>🚨 Alert: {alert.name}</h2>
<p><strong>Severity:</strong> {alert.severity.value}</p>
<p><strong>Source:</strong> {alert.source}</p>
<p><strong>Condition:</strong> {alert.metric} {alert.condition} {alert.threshold}</p>
<p><strong>Current Value:</strong> {alert.current_value}</p>
<p><strong>Time:</strong> {alert.timestamp}</p>
{if alert.runbook_url}
<p><a href="{alert.runbook_url}">📖 View Runbook</a></p>
{endif}
```

**Verification**:
- `pytest tests/unit/test_alert_channels.py -v` (new, 10+ tests)
- Test: alert triggers → WS broadcast fires → email sent (mock SMTP)
- Test: webhook fires with correct JSON payload

---

### Task FK-009: 5-Tier Escalation Matrix
**Owner**: `orchestration-owner` (reports to COO) | **Effort**: 2 days

**Escalation Tiers** (from `CEO_DASHBOARD_ARCHITECTURE_ANALYSIS.md:413-418`):

| Tier | Recipients | SLA | Action |
|------|------------|-----|--------|
| 1 | Direct manager | 1 hour | Auto-assign |
| 2 | Department head | 2 hours | Email + WS |
| 3 | Executive (CTO/COO/CAIO) | 4 hours | Email + WS |
| 4 | Cross-department coordination | 8 hours | Email + WS + webhook |
| 5 | Human CEO | Immediate | Email + WS + webhook + SMS (future) |

**Escalation Logic**:
```python
class TierRouter:
    def escalate(self, alert: Alert) -> Alert:
        """Move alert to next tier if SLA breached."""
        current_tier = alert.current_tier
        if current_tier >= 5:
            return alert  # Already at max

        elapsed = datetime.now() - alert.created_at
        sla = self._get_sla_minutes(current_tier)

        if elapsed.total_seconds() / 60 > sla:
            alert.current_tier = current_tier + 1
            alert.escalated_at = datetime.now()
            self._notify_tier(alert)

        return alert
```

**Verification**:
- `pytest tests/unit/test_alert_escalation.py -v` (new, 15+ tests)
- Test: alert at tier 1, 2 hours pass → escalates to tier 2
- Test: alert acknowledged → escalation stops
- Test: alert at tier 5 → no further escalation

---

### Task FK-010: Alert Dashboard UI
**Owner**: `frontend-engineer` | **Effort**: 2 days

**Template**: `templates/alerts.html` (new)

**Components**:
1. **Alert Banner** (top of dashboard): Active critical/warning alerts
2. **Alert Center** (full page): List of all alerts with filters
3. **Alert Detail** (slide-out): Full alert info, runbook link, acknowledge/resolve buttons
4. **Alert History** (tab): Past alerts with resolution notes

**Alpine.js State**:
```javascript
alerts: {
  active: [],
  history: [],
  loading: false,
  filters: {
    severity: '',
    source: '',
    acknowledged: false
  },
  selected: null,
  detailOpen: false
}
```

**API Endpoints** (in `api.py`):
- `GET /api/v1/alerts` — list active alerts
- `GET /api/v1/alerts/history` — list historical alerts
- `POST /api/v1/alerts/{id}/acknowledge` — acknowledge
- `POST /api/v1/alerts/{id}/resolve` — resolve

**WebSocket Topic**: `alerts` — broadcast on new alert, acknowledge, resolve

**Verification**:
- Playwright E2E: `tests/test_alert_ui_e2e.py` (new)
  - Alert banner shows when alert fires
  - Alert Center lists alerts
  - Click alert → detail panel opens
  - Acknowledge → alert moves to history
  - Resolve → alert closed

---

## Phase 4: Integration & Polish (Week 7-8)

### Task FK-011: Executive Scorecard → Alert Integration
**Owner**: `dashboard-owner` | **Effort**: 1 day

**Wire**: `ExecutiveScorecardCollector._generate_risk_indicators()` → `AlertEngine.evaluate_rules()`

**Flow**:
```
KPI Collection (every 30s)
    ↓
ExecutiveScorecardCollector.compute()
    ↓
Risk indicators generated
    ↓
AlertEngine.evaluate_rules(kpi_snapshot)
    ↓
New alerts → ChannelRouter.route()
    ↓
WS broadcast + email (if critical)
```

---

### Task FK-012: Org Chart → Alert Integration
**Owner**: `graph-owner` | **Effort**: 1 day

**Wire**: Org chart metrics → alert rules
- Agent capacity <30% → `agent_utilization_lt_30` alert
- Agent capacity <50% → `agent_utilization_lt_50` alert
- Succession risk "high" → new rule `critical_role_understaffed`

---

### Task FK-013: End-to-End Integration Tests
**Owner**: `qa-automation-engineer` | **Effort**: 2 days

**Test Scenarios**:
1. KPI drops below threshold → alert fires → WS broadcast → UI shows banner
2. Alert not acknowledged in 1h → escalates to tier 2
3. Alert acknowledged → escalation stops
4. Org chart capacity changes → utilization alert fires
5. Executive scorecard refreshes → health score updates
6. Multiple rapid alerts → toast queue handles correctly
7. Alert history persists across page reloads

---

### Task FK-014: Documentation & Runbooks
**Owner**: `technical-documentation-lead` | **Effort**: 2 days

**Documents**:
1. `docs/ALERTING-GUIDE.md` — How to configure alert rules, channels, escalation
2. `docs/ALERT-RUNBOOKS.md` — Runbook for each of the 12 default alerts
3. `docs/EXECUTIVE-KPI-GUIDE.md` — How KPIs are computed, targets, trends
4. `docs/ORG-CHART-GUIDE.md` — How to use interactive org chart features

---

## Success Metrics & KPIs

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Executive KPI accuracy | Manual | 99.9% | Cross-validation with collectors |
| Org chart render time | N/A | <500ms | Browser performance |
| Alert detection latency | N/A | <30s | Rule evaluation cycle |
| Alert escalation SLA compliance | N/A | 100% | Escalation log |
| Alert false positive rate | N/A | <5% | User feedback |
| Dashboard load time | ~3s | <2s | Lighthouse |
| User satisfaction (NPS) | Low | >50 | Quarterly survey |

---

## Dependencies & Blockers

| Task | Depends On | Blocks |
|------|------------|--------|
| FK-001 | None | FK-011 |
| FK-002 | None | FK-001 (targets) |
| FK-003 | None | FK-001 (trends) |
| FK-004 | None | FK-005, FK-012 |
| FK-005 | FK-004 | None |
| FK-006 | None | None (CI gate) |
| FK-007 | None | FK-008, FK-009, FK-011 |
| FK-008 | FK-007 | None |
| FK-009 | FK-007 | FK-011, FK-012 |
| FK-010 | FK-007 | None |
| FK-011 | FK-001, FK-007 | None |
| FK-012 | FK-004, FK-007 | None |
| FK-013 | All above | None |
| FK-014 | FK-010 | None |

---

## Definition of Done per Task

- [ ] Code implemented and reviewed (5-axis review)
- [ ] Unit tests added/updated (minimum 80% coverage for new code)
- [ ] Integration test added (where applicable)
- [ ] E2E test added (Playwright, where UI involved)
- [ ] Manual verification on staging
- [ ] Documentation updated
- [ ] Deployed to staging, verified by `qa-lead`
- [ ] `ruff check src/ && mypy src/ && pytest` all green
