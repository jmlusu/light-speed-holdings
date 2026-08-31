# Org Health Dashboard Enhancement — Design Spec

**Date:** 2026-08-31
**Status:** Approved
**Approach:** Hybrid (expand composite + metric cards grid)

---

## 1. Problem

The CEO Dashboard's Org Health section shows a single composite score (50 AMBER) from only 4 weighted components. With 135 agents across 15+ departments and 57 skills, the organization has far more signal available. The current view is too thin to drive meaningful decisions.

## 2. Goal

Expand Org Health from a single gauge into a rich health real-estate with:
- 8 weighted components (up from 4) feeding the composite score
- A gauge + metric cards grid layout
- Category-level groupings for drill-down
- Trend sparklines per component

## 3. Metric Components

### 3.1 Existing Components (rebalanced weights)

| Component | Weight | Formula | Source |
|-----------|--------|---------|--------|
| `task_success_rate` | 0.25 | `(completed / total) * 100` | task history (30d) |
| `agent_utilization` | 0.20 | `(active / registered) * 100` | task history (30d) |
| `cost_efficiency` | 0.15 | `100 - (spend/budget * 100) + 50` | cost data |
| `error_rate` | 0.15 | `100 - (errors / total * 100)` | task history (30d) |

### 3.2 New Components

| Component | Weight | Formula | Source |
|-----------|--------|---------|--------|
| `task_throughput` | 0.10 | `tasks_completed_per_day`, normalized 0-100 vs 30d target | task history |
| `escalation_rate` | 0.05 | `100 - (escalated / total * 100)` | task history |
| `security_posture` | 0.05 | Composite: audit trail health + compliance score | audit JSONL |
| `strategic_alignment` | 0.05 | `% tasks mapped to active goals` | task metadata + OKR config |

### 3.3 Weight Verification

Sum: 0.25 + 0.20 + 0.15 + 0.15 + 0.10 + 0.05 + 0.05 + 0.05 = **1.00** ✓

### 3.4 Score Bands (unchanged)

- GREEN: 80-100
- AMBER: 50-79
- RED: 0-49

## 4. Frontend Layout

### 4.1 Section Structure

```
┌─────────────────────────────────────────────────────────┐
│  ORG HEALTH                          [61 pending] [0↑] │
│                                                         │
│  ┌───────────────┐  ┌──────┐ ┌──────┐ ┌──────┐ ┌─────┐│
│  │               │  │Task  │ │Agent │ │Cost  │ │Error││
│  │   50 AMBER    │  │Succ. │ │Util. │ │Eff.  │ │Rate ││
│  │   (gauge)     │  │ 85   │ │ 72   │ │ 60   │ │ 90  ││
│  │               │  │  ●   │ │  ●   │ │  ●   │ │  ●  ││
│  └───────────────┘  └──────┘ └──────┘ └──────┘ └─────┘│
│                                                         │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                   │
│  │Throu.│ │Escal.│ │Secur.│ │Strat.│  ← NEW ROW       │
│  │  78  │ │  92  │ │  88  │ │  65  │                   │
│  │  ●   │ │  ●   │ │  ●   │ │  ●   │                   │
│  └──────┘ └──────┘ └──────┘ └──────┘                   │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Card Design

Each metric card shows:
- **Name** (abbreviated)
- **Score** (0-100, large number)
- **Color dot** (green/amber/red based on band thresholds)
- **Mini sparkline** (last 7 values from trend data)
- **Click behavior:** Expands to show detail panel with formula, weight, trend chart, raw values

### 4.3 Responsive Behavior

- Desktop: Gauge left (256px), cards grid right (2 rows x 4 cols)
- Tablet: Gauge top, cards below (2 rows x 4 cols, smaller)
- Mobile: Gauge top, cards stack (1 col x 8 rows)

### 4.4 Styling

Reuse existing glass-morphism from `style.css`:
- `.hero-section` background/border
- Card background: `rgba(255, 255, 255, 0.05)`
- Card border: `1px solid rgba(255, 255, 255, 0.1)`
- Hover: border glow effect

## 5. API Design

### 5.1 Modified Endpoint

**`GET /api/v1/org-health`** — response gains 4 new entries in `components[]`:

```json
{
  "score": 50,
  "band": "amber",
  "components": [
    { "name": "task_success_rate", "weight": 0.25, "value": 85, "sub_score": 85 },
    { "name": "agent_utilization", "weight": 0.20, "value": 72, "sub_score": 72 },
    { "name": "cost_efficiency", "weight": 0.15, "value": 60, "sub_score": 60 },
    { "name": "error_rate", "weight": 0.15, "value": 90, "sub_score": 90 },
    { "name": "task_throughput", "weight": 0.10, "value": 78, "sub_score": 78 },
    { "name": "escalation_rate", "weight": 0.05, "value": 92, "sub_score": 92 },
    { "name": "security_posture", "weight": 0.05, "value": 88, "sub_score": 88 },
    { "name": "strategic_alignment", "weight": 0.05, "value": 65, "sub_score": 65 }
  ],
  "trend": [...],
  "staleness": { ... }
}
```

### 5.2 New Endpoint

**`GET /api/v1/org-health/categories`** — groups components into categories:

```json
{
  "operational": {
    "score": 82,
    "components": ["task_success_rate", "task_throughput", "escalation_rate"]
  },
  "financial": {
    "score": 60,
    "components": ["cost_efficiency"]
  },
  "security": {
    "score": 88,
    "components": ["security_posture"]
  },
  "strategic": {
    "score": 65,
    "components": ["strategic_alignment"]
  },
  "workforce": {
    "score": 72,
    "components": ["agent_utilization", "error_rate"]
  }
}
```

## 6. Backend Changes

### 6.1 Files to Modify

| File | Change |
|------|--------|
| `config/org_health.yaml` | Add 4 new component definitions, rebalance weights |
| `src/ai_company/dashboard/org_health.py` | Add 4 new `_score_*` methods, wire into `compute()` |
| `src/ai_company/dashboard/api.py` | Add `/categories` endpoint, update `/org-health` response |
| `src/ai_company/dashboard/kpis/org_health.py` | Include new components in KPI collector output |

### 6.2 New Scorer Methods

```python
def _score_task_throughput(self, database) -> float | None:
    """Tasks completed per day, normalized to 0-100 vs target."""
    # Count completed tasks in 30d window
    # Normalize: (actual_per_day / target_per_day) * 100, capped at 100

def _score_escalation_rate(self, database) -> float | None:
    """100 - (escalated / total * 100). Lower escalation = higher score."""
    # Reuse _read_all_tasks() data already fetched in compute()

def _score_security_posture(self, database) -> float | None:
    """Audit trail health + compliance indicators."""
    # Check: audit events exist, no critical severity events,
    # compliance-related tasks completed

def _score_strategic_alignment(self, database) -> float | None:
    """% of tasks mapped to active goals/OKRs."""
    # Optional OKR config from config/okr.yaml
    # Fall back to task metadata (department coverage) if no OKR config
```

### 6.3 Circuit Breakers

All new scorers follow the existing pattern:
- Return `None` on failure (excluded from composite)
- Log warnings but never crash the health endpoint
- Thread-pooled execution (existing `ThreadPoolExecutor` in `compute()`)

## 7. Frontend Changes

### 7.1 Files to Modify

| File | Change |
|------|--------|
| `src/ai_company/dashboard/templates/index.html` | Expand Org Health section with card grid |
| `src/ai_company/dashboard/static/js/app.js` | Add `renderMetricCards()`, `renderCardSparkline()`, card click handlers |
| `src/ai_company/dashboard/static/css/style.css` | Add `.metric-card`, `.card-grid`, `.card-sparkline` styles |

### 7.2 JavaScript Additions

```javascript
// New methods in Alpine.js component
renderMetricCards(components) {
  // Create card elements for each component
  // Attach sparkline canvases
  // Wire click handlers for expand/collapse
}

renderCardSparkline(canvasId, trendData) {
  // Reuse _renderSparkline() logic
  // Compact 60x30px sparkline
}

expandComponentDetail(componentName) {
  // Show detail panel with formula, weight, full trend chart
}
```

## 8. Agent Team

| Track | Agent | Responsibility | Skills |
|-------|-------|---------------|--------|
| 1. Backend Scoring | `data_engineer` | New scorer methods, config update | `tdd`, `code-review-and-quality` |
| 2. Ops Metrics | `orchestration_owner` | Throughput + escalation scorers | `observability-and-instrumentation` |
| 3. Security | `security_compliance_lead` | Security posture scorer | `security-and-hardening` |
| 4. Strategy | `chief_of_staff` | Strategic alignment scorer, OKR config | `domain-modeling` |
| 5. API | `dashboard_owner` | Wire scorers, new `/categories` endpoint | `api-endpoint-builder` |
| 6. Frontend | `frontend_architect` | Card grid, sparklines, responsive | — |
| 7. Design | `product_designer` | Card visuals, interaction patterns | `rayden-code` |
| 8. Analytics | `business_intelligence_engineer` | Trend charts, anomaly detection | `observability-and-instrumentation` |

## 9. Execution Order

1. **Parallel (Tracks 1-4):** Backend scorers + config
2. **Sequential (Track 5):** API wiring (depends on 1-4)
3. **Parallel (Tracks 6-7):** Frontend (depends on 5)
4. **Sequential (Track 8):** Analytics integration (depends on 6)

## 10. Verification

| Step | Command |
|------|---------|
| Config validation | `python -c "from ai_company.dashboard.org_health import OrgHealthCalculator; c = OrgHealthCalculator(); print('OK')"` |
| Scorer unit tests | `uv run pytest tests/dashboard/test_org_health.py -v` |
| API smoke test | `curl http://localhost:8420/api/v1/org-health \| python -m json.tool` |
| Categories endpoint | `curl http://localhost:8420/api/v1/org-health/categories \| python -m json.tool` |
| Frontend visual | Open dashboard, verify 8 cards render with sparklines |
| Lint | `uv run ruff check src/ && uv run mypy src/` |
| Full test suite | `uv run pytest` |

## 11. Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Composite becomes noisy with 8 components | Lower weights for new components (0.05-0.10); they add signal without destabilizing |
| Security scorer needs data that may not exist | Graceful fallback: returns None (excluded from composite) when audit data is sparse |
| Strategic alignment needs OKR config | Optional config file; scorer falls back to department coverage heuristic |
| Frontend performance with 8 sparklines | Use `requestAnimationFrame` batching; sparklines are tiny (7 points) |
