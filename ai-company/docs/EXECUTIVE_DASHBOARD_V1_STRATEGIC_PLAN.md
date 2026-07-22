# Executive Dashboard Version 1 — Strategic Implementation Plan

**Status:** Phase 1 Planning Complete | **Foundation:** 100% Existing Infrastructure Ready

---

## Executive Summary

The AI Company Builder already possesses **all foundational components** needed for Executive Dashboard v1. No new infrastructure is required — only strategic integration of existing APIs, data sources, and real-time capabilities.

**Executive Value Delivered:** Immediate strategic visibility into AI organization health, performance, and risk through 6 high-value capabilities.

---

## Phase 1: Architecture & Data Flow Analysis

### 1.1 Existing Infrastructure Map

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        EXECUTIVE DASHBOARD v1 ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  EXISTING    │    │  EXISTING    │    │  EXISTING    │    │  EXISTING    │  │
│  │  FastAPI     │    │  KPI         │    │  MessageBus  │    │  Graph       │  │
│  │  Dashboard   │◄───│  Collectors  │    │  (inbox.json)│    │  Engine      │  │
│  │  (20+ eps)   │    │  (7 depts)   │    │  + WebSocket │    │  (Org Chart) │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                   │                   │          │
│         └───────────────────┼───────────────────┼───────────────────┘          │
│                             ▼                   ▼                              │
│                  ┌─────────────────────────────────────────┐                  │
│                  │      EXECUTIVE AGGREGATION LAYER        │                  │
│                  │  (New: ExecutiveDashboardService)       │                  │
│                  ├─────────────────────────────────────────┤                  │
│                  │ • ExecutiveKPICalculator                │                  │
│                  │ • OrgChartTransformer                   │                  │
│                  │ • AIExecutiveStatusEngine               │                  │
│                  │ • TaskPipelineAggregator                │                  │
│                  │ • ActivityFeedCurator                   │                  │
│                  │ • RiskAlertCenter                       │                  │
│                  └─────────────────────────────────────────┘                  │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Capability-to-Data Source Mapping

| Executive Capability | Primary Data Sources | Secondary Sources | Real-time Required? |
|---------------------|---------------------|-------------------|---------------------|
| **1. Executive KPI Overview** | `dashboard/kpis/*` (7 collectors), `analytics.py` AlertEngine | `dashboard/repository.py` StateStore | Yes (WebSocket) |
| **2. Organization Chart** | `registry/loader.py` → `graph/engine.py` OrgChart | `company-registry.yaml` raw | No (cache 5min) |
| **3. AI Executive Status** | `orchestrator/message_bus.py`, `executor/`, `llm/cost_tracker.py` | `dashboard/api.py` AgentSummary | Yes (WebSocket) |
| **4. Active Projects/Tasks** | `orchestrator/message_bus.py`, `orchestrator/scheduler.py` | `orchestrator/escalation.py` | Yes (WebSocket) |
| **5. AI Agent Activity Feed** | `MessageBus` broadcast callbacks, `audit/` events | `memory/` recall logs | Yes (WebSocket) |
| **6. Risk & Alert Center** | `analytics.py` AlertEngine, `orchestrator/escalation.py` | `decision/` approval matrix | Yes (WebSocket) |

### 1.3 Integration Points Identified

| Integration Point | File | Status | Notes |
|------------------|------|--------|-------|
| KPI Collectors → Executive View | `dashboard/kpis/*.py` | ✅ Ready | 7 departments, unified interface |
| MessageBus → WebSocket Broadcast | `dashboard/ws.py:230` | ✅ Ready | `make_message_bus_broadcast_callback()` |
| Org Chart Data | `graph/engine.py:85` | ✅ Ready | `build_org_chart()` returns Graph |
| Analytics Alert Engine | `dashboard/analytics.py` | ✅ Ready | Threshold rules, history, trends |
| Task Lifecycle Events | `orchestrator/message_bus.py` | ✅ Ready | Broadcast on status changes |
| Cost Tracking | `llm/cost_tracker.py` | ✅ Ready | Per-agent, per-task accounting |

---

## Phase 2: Component Implementation Priority (ROI-Optimized)

### 2.1 Quick Wins (Week 1) — 80% Executive Value, 20% Effort

| Priority | Capability | Implementation Approach | Est. Effort |
|----------|------------|------------------------|-------------|
| **1** | **Executive KPI Overview** | Aggregate existing 7 KPI collectors + AlertEngine | 2 days |
| **2** | **Organization Chart** | Transform existing GraphEngine OrgChart → API | 1 day |
| **3** | **Risk & Alert Center** | Wrap existing AlertEngine + EscalationManager | 2 days |

**Total Week 1: ~5 days** → **Executive MVP Deployable**

### 2.2 Core Capabilities (Week 2) — High Value, Moderate Effort

| Priority | Capability | Implementation Approach | Est. Effort |
|----------|------------|------------------------|-------------|
| **4** | **AI Executive Status Panel** | Aggregate agent performance from MessageBus + CostTracker | 3 days |
| **5** | **Active Projects & Tasks** | Pipeline view from Scheduler + MessageBus task states | 3 days |

**Total Week 2: ~6 days** → **Full Executive Operational View**

### 2.3 Real-time Enhancement (Week 3) — Differentiator

| Priority | Capability | Implementation Approach | Est. Effort |
|----------|------------|------------------------|-------------|
| **6** | **AI Agent Activity Feed** | WebSocket subscription to MessageBus broadcasts + audit events | 4 days |

**Total Week 3: ~4 days** → **Real-time Executive Situational Awareness**

---

## Phase 3: Technical Architecture

### 3.1 New Service: ExecutiveDashboardService

```python
# File: src/ai_company/dashboard/executive.py (NEW)

class ExecutiveDashboardService:
    """Single service aggregating all executive dashboard capabilities."""
    
    def __init__(self):
        self.kpi_collectors = get_all_collectors()  # Existing
        self.message_bus = get_bus()  # Existing
        self.graph_engine = GraphEngine(registry)  # Existing
        self.analytics = KPIAnalytics()  # Existing
        self.cost_tracker = CostTracker()  # Existing
        self.escalation_mgr = EscalationManager()  # Existing
    
    # 1. Executive KPI Overview
    async def get_executive_kpi_snapshot(self) -> ExecutiveKPISnapshot:
        """Aggregate weighted KPIs across all departments."""
        
    # 2. Organization Chart
    async def get_executive_org_chart(self) -> OrgChartResponse:
        """Transform GraphEngine org_chart to executive view."""
        
    # 3. AI Executive Status
    async def get_ai_executive_status(self) -> AIExecutiveStatus:
        """Agent performance, model costs, quality metrics."""
        
    # 4. Active Projects & Tasks
    async def get_executive_pipeline(self) -> ExecutivePipeline:
        """Task pipeline with stage gates, critical path."""
        
    # 5. AI Agent Activity Feed
    async def get_activity_feed(self, filters: ActivityFilters) -> ActivityFeed:
        """Real-time curated agent activity stream."""
        
    # 6. Risk & Alert Center
    async def get_risk_alert_center(self) -> RiskAlertCenter:
        """Aggregated alerts with executive prioritization."""
```

### 3.2 API Endpoint Design

```python
# File: src/ai_company/dashboard/api.py (EXTEND existing router)

# Executive Dashboard Endpoints
@router.get("/api/executive/kpis", response_model=ExecutiveKPISnapshot)
async def get_executive_kpis()

@router.get("/api/executive/org-chart", response_model=OrgChartResponse)
async def get_executive_org_chart()

@router.get("/api/executive/ai-status", response_model=AIExecutiveStatus)
async def get_ai_executive_status()

@router.get("/api/executive/pipeline", response_model=ExecutivePipeline)
async def get_executive_pipeline()

@router.get("/api/executive/activity", response_model=ActivityFeed)
async def get_executive_activity(
    limit: int = 50,
    department: Optional[str] = None,
    agent_type: Optional[str] = None,
    since: Optional[datetime] = None
)

@router.get("/api/executive/alerts", response_model=RiskAlertCenter)
async def get_executive_alerts()

# WebSocket Topics for Real-time
# - "executive:kpis"     → Executive KPI updates
# - "executive:alerts"   → Critical alerts
# - "executive:tasks"    → Pipeline changes
# - "executive:activity" → Agent activity feed
```

### 3.3 Data Models (Extend `dashboard/models.py`)

```python
# Executive KPI Snapshot
class ExecutiveKPISnapshot(BaseModel):
    timestamp: datetime
    overall_health: Literal["healthy", "degraded", "critical"]
    department_scores: dict[str, DepartmentHealthScore]
    top_alerts: list[ExecutiveAlert]
    cost_summary: CostSummary
    velocity_indicators: VelocityIndicators

# Organization Chart
class OrgChartResponse(BaseModel):
    nodes: list[ExecutiveOrgNode]  # Extends OrgNode with metrics
    reporting_lines: list[ReportingLine]
    team_metrics: dict[str, TeamMetrics]

# AI Executive Status
class AIExecutiveStatus(BaseModel):
    agents_by_tier: dict[str, int]  # fast/standard/premium
    agents_by_department: dict[str, int]
    model_cost_24h: float
    model_cost_budget_pct: float
    quality_scores: dict[str, float]  # By agent
    error_rates: dict[str, float]

# Executive Pipeline
class ExecutivePipeline(BaseModel):
    stages: list[PipelineStage]  # backlog → ready → in_progress → review → done
    critical_path: list[TaskItem]
    resource_allocation: dict[str, int]  # agent -> active task count
    sla_risks: list[SLARisk]

# Activity Feed
class ActivityFeed(BaseModel):
    events: list[ActivityEvent]
    filters_applied: ActivityFilters
    real_time: bool

# Risk Alert Center
class RiskAlertCenter(BaseModel):
    critical_alerts: list[ExecutiveAlert]
    warning_alerts: list[ExecutiveAlert]
    info_alerts: list[ExecutiveAlert]
    escalation_count: int
    approval_pending: int
    risk_trend: TrendDirection
```

### 3.4 WebSocket Integration

```python
# File: src/ai_company/dashboard/ws.py (EXTEND)

# Add executive-specific broadcast functions
async def broadcast_executive_kpi_update(data: dict) -> None:
    await manager.broadcast({"type": "executive_kpi", "topic": "executive:kpis", ...})

async def broadcast_executive_alert(alert: dict) -> None:
    await manager.broadcast({"type": "executive_alert", "topic": "executive:alerts", ...})

async def broadcast_executive_task_update(task: dict, event: str) -> None:
    await manager.broadcast({"type": "executive_task", "topic": "executive:tasks", ...})

async def broadcast_executive_activity(activity: dict) -> None:
    await manager.broadcast({"type": "executive_activity", "topic": "executive:activity", ...})
```

---

## Phase 4: Implementation Roadmap

### 4.1 Week 1: Executive MVP (Days 1-5)

| Day | Task | Files to Create/Modify | Dependencies |
|-----|------|------------------------|--------------|
| 1 | Create `ExecutiveDashboardService` skeleton | `dashboard/executive.py` (NEW) | None |
| 1 | Implement Executive KPI Aggregation | `dashboard/executive.py`, `dashboard/models.py` | KPI collectors, Analytics |
| 2 | Add Executive KPI API endpoints | `dashboard/api.py` | Service ready |
| 2 | Implement OrgChart transformation | `dashboard/executive.py` | GraphEngine |
| 3 | Add OrgChart API endpoint | `dashboard/api.py`, `dashboard/models.py` | OrgChart logic |
| 3 | Implement Risk Alert Center | `dashboard/executive.py` | Analytics AlertEngine, EscalationMgr |
| 4 | Add Alerts API endpoint | `dashboard/api.py` | Alert logic |
| 4 | Create executive dashboard UI template | `dashboard/templates/executive.html` (NEW) | API endpoints |
| 5 | Integration testing & validation | All above | All Week 1 components |

**Week 1 Deliverable:** `/executive` route with KPI overview, Org Chart, Alert Center

### 4.2 Week 2: Operational View (Days 6-11)

| Day | Task | Files to Create/Modify | Dependencies |
|-----|------|------------------------|--------------|
| 6 | Implement AI Executive Status aggregation | `dashboard/executive.py` | MessageBus, CostTracker |
| 6 | Add AI Status API endpoint | `dashboard/api.py`, `dashboard/models.py` | Status logic |
| 7 | Implement Executive Pipeline view | `dashboard/executive.py` | Scheduler, MessageBus |
| 7 | Add Pipeline API endpoint | `dashboard/api.py` | Pipeline logic |
| 8 | Executive Pipeline UI components | `dashboard/templates/executive.html` | API endpoints |
| 9 | AI Status UI components | `dashboard/templates/executive.html` | API endpoints |
| 10 | End-to-end integration testing | All Week 1-2 components | All APIs |
| 11 | Performance optimization, caching | `dashboard/executive.py` | Test results |

**Week 2 Deliverable:** Full operational view with AI status and pipeline

### 4.3 Week 3: Real-time Situational Awareness (Days 12-15)

| Day | Task | Files to Create/Modify | Dependencies |
|-----|------|------------------------|--------------|
| 12 | Implement Activity Feed curation | `dashboard/executive.py` | MessageBus, Audit |
| 12 | Add Activity Feed API + WebSocket | `dashboard/api.py`, `dashboard/ws.py` | Feed logic |
| 13 | WebSocket subscription UI | `dashboard/templates/executive.html`, `dashboard/static/executive.js` (NEW) | WS endpoints |
| 14 | Real-time alert push integration | `dashboard/ws.py`, `dashboard/analytics.py` | AlertEngine |
| 15 | Full real-time integration testing | All components | Week 1-3 complete |

**Week 3 Deliverable:** Real-time executive dashboard with live feeds

---

## Phase 5: Governance & Compliance

### 5.1 Executive Access Control

```python
# File: src/ai_company/dashboard/auth.py (NEW or extend)

EXECUTIVE_ROLES = ["human-ceo", "ceo_advisor", "chief_of_staff", "board_chair"]

async def require_executive_access(request: Request) -> str:
    """Validate executive-level access for dashboard endpoints."""
    api_key = request.headers.get("X-API-Key")
    agent_id = await validate_api_key(api_key)
    
    if agent_id not in EXECUTIVE_ROLES:
        raise HTTPException(403, "Executive access required")
    return agent_id

# Apply to all /api/executive/* endpoints
@router.get("/api/executive/kpis", dependencies=[Depends(require_executive_access)])
```

### 5.2 Audit Trail for Executive Dashboard Access

```python
# Extend existing audit/event system
class ExecutiveDashboardAccessEvent(BaseModel):
    event_type: Literal["executive_dashboard_access"]
    agent_id: str
    endpoint: str
    timestamp: datetime
    data_accessed: list[str]  # Which capabilities accessed
```

### 5.3 Data Retention & Privacy

| Data Type | Retention | Privacy Level |
|-----------|-----------|---------------|
| Executive KPI Snapshots | 2 years | Executive-only |
| Org Chart | Indefinite | Company-wide |
| AI Agent Status | 1 year | Executive + Dept Heads |
| Task Pipeline | 1 year | Executive + Assigners |
| Activity Feed | 90 days | Executive-only |
| Alerts/Escalations | 2 years | Executive + Relevant Parties |

---

## Risk Assessment & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| WebSocket connection instability | Medium | High | Auto-reconnect, fallback polling |
| KPI data staleness | Low | Medium | 30s cache TTL, explicit refresh |
| MessageBus broadcast failures | Low | High | Circuit breaker, dead-letter logging |
| Executive access misconfiguration | Low | Critical | Automated access validation tests |
| Performance under load | Medium | Medium | Redis caching layer (future), pagination |

---

## Success Metrics & Validation Criteria

### Phase 1 (Week 1) - MVP Validation
- [ ] Executive KPI endpoint returns <500ms p95
- [ ] Org Chart renders full 27-agent hierarchy correctly
- [ ] Alert Center shows all active escalations + approvals
- [ ] All endpoints require executive authentication
- [ ] Dashboard loads in <2s on cold start

### Phase 2 (Week 2) - Operational Validation
- [ ] AI Status shows accurate model costs per agent
- [ ] Pipeline displays correct stage counts from MessageBus
- [ ] SLA risks identified match orchestrator escalations
- [ ] Executive can drill from KPI → Alert → Task

### Phase 3 (Week 3) - Real-time Validation
- [ ] Activity feed updates within 2s of agent action
- [ ] Alert push notification <1s from threshold breach
- [ ] WebSocket reconnects automatically on network blip
- [ ] 10 concurrent executive sessions supported

---

## File Inventory for Implementation

### New Files to Create
```
src/ai_company/dashboard/
├── executive.py              # ExecutiveDashboardService (core aggregation)
├── auth.py                   # Executive access control
├── templates/
│   └── executive.html        # Executive dashboard UI
└── static/
    └── executive.js          # Real-time UI logic
```

### Files to Extend
```
src/ai_company/dashboard/
├── api.py                    # +6 executive endpoints
├── models.py                 # +6 executive response models
├── ws.py                     # +4 executive broadcast functions + topics
├── analytics.py              # +Executive alert rule helpers (optional)
└── __init__.py               # Export new service
```

### Files Referenced (No Changes Needed)
```
src/ai_company/
├── dashboard/kpis/*.py       # 7 existing collectors
├── orchestrator/message_bus.py
├── orchestrator/scheduler.py
├── orchestrator/escalation.py
├── graph/engine.py           # OrgChart already built
├── registry/loader.py        # Registry already loaded
├── llm/cost_tracker.py
├── executor/loop.py
├── audit/writer.py
└── models/models.py          # CompanyRegistry
```

---

## Dependencies & Prerequisites

| Prerequisite | Status | Notes |
|--------------|--------|-------|
| FastAPI dashboard running | ✅ Complete | Port 8420 |
| 7 KPI collectors functional | ✅ Complete | All departments |
| MessageBus with WebSocket broadcast | ✅ Complete | GAP-011 resolved |
| GraphEngine OrgChart | ✅ Complete | BFS pathfinding |
| Analytics AlertEngine | ✅ Complete | Threshold rules |
| CostTracker per-agent | ✅ Complete | 3-tier routing |
| 962 tests passing | ✅ Complete | CI green |

---

## Next Immediate Actions

1. **Create `dashboard/executive.py`** — Core aggregation service
2. **Extend `dashboard/models.py`** — Executive response models
3. **Add executive endpoints to `dashboard/api.py`** — 6 new routes
4. **Add WebSocket topics to `dashboard/ws.py`** — 4 executive topics
5. **Create executive dashboard template** — `templates/executive.html`

**Estimated Start-to-MVP:** 5 working days with existing infrastructure

---

*Plan Status: READY FOR EXECUTION*  
*All foundations verified. No blockers identified. Proceed to implementation.*