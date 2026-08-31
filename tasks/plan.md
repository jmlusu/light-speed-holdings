# Implementation Plan: Org Health Dashboard Enhancement

## Overview

Expand the CEO Dashboard's Org Health section from a single composite gauge (4 components) into a rich health real-estate with 8 weighted components, a gauge + metric cards grid layout, category groupings, and trend sparklines. Uses existing agents from the company registry.

## Architecture Decisions

- **Hybrid approach:** Expand composite formula (8 components) + add metric cards grid around the gauge
- **Reuse existing patterns:** New scorers follow the same `_score_*` method pattern in `OrgHealthCalculator`
- **Graceful degradation:** New scorers return `None` on failure (excluded from composite), same as existing
- **Config-driven:** All component weights and definitions in `config/org_health.yaml`
- **No new agents:** Use 8 existing agents from company-registry.yaml

## Task List

### Phase 1: Backend Config & Scoring Foundation

- [ ] **Task 1:** Update `config/org_health.yaml` — rebalance existing weights, add 4 new component definitions (task_throughput, escalation_rate, security_posture, strategic_alignment)
  - Files: `config/org_health.yaml`
  - Verification: YAML parses, weights sum to 1.0

- [ ] **Task 2:** Add `_score_task_throughput()` method to `OrgHealthCalculator` — tasks completed per day normalized to 0-100 vs 30d target
  - Files: `src/ai_company/dashboard/org_health.py`
  - Verification: Unit test with mock task data

- [ ] **Task 3:** Add `_score_escalation_rate()` method — `100 - (escalated / total * 100)`, reuses `_window_tasks()`
  - Files: `src/ai_company/dashboard/org_health.py`
  - Verification: Unit test with mock task data

- [ ] **Task 4:** Add `_score_security_posture()` method — composite of audit trail health + compliance indicators from audit JSONL
  - Files: `src/ai_company/dashboard/org_health.py`
  - Verification: Unit test with mock audit data

- [ ] **Task 5:** Add `_score_strategic_alignment()` method — % tasks mapped to active goals, falls back to department coverage heuristic
  - Files: `src/ai_company/dashboard/org_health.py`
  - Verification: Unit test with mock data

- [ ] **Task 6:** Wire new scorers into `_scorers()` dict and update `_default_config()` with new components
  - Files: `src/ai_company/dashboard/org_health.py`
  - Verification: `OrgHealthCalculator().compute()` returns 8 components

### Checkpoint: Backend Scoring
- [ ] All existing tests pass
- [ ] New scorer unit tests pass
- [ ] `python -c "from ai_company.dashboard.org_health import OrgHealthCalculator; r = OrgHealthCalculator().compute(); assert len(r.components) == 8"` succeeds

### Phase 2: API Layer

- [ ] **Task 7:** Add `GET /api/v1/org-health/categories` endpoint — groups components into operational/financial/security/strategic/workforce categories
  - Files: `src/ai_company/dashboard/api.py`
  - Verification: Endpoint returns valid JSON with 5 categories

- [ ] **Task 8:** Update `OrgHealthKPICollector.collect()` to include new component KPIs
  - Files: `src/ai_company/dashboard/kpis/org_health.py`
  - Verification: KPI snapshot includes all 8 component entries

### Checkpoint: API Layer
- [ ] `curl http://localhost:8420/api/v1/org-health` shows 8 components
- [ ] `curl http://localhost:8420/api/v1/org-health/categories` returns 5 categories
- [ ] Existing API tests pass

### Phase 3: Frontend Layout

- [ ] **Task 9:** Expand `index.html` Org Health section — add 2-row metric cards grid (4 cards per row) next to the gauge
  - Files: `src/ai_company/dashboard/templates/index.html`
  - Verification: 8 cards render with correct component names and scores

- [ ] **Task 10:** Add CSS styles for metric cards — `.metric-card`, `.card-grid`, `.card-sparkline`, responsive breakpoints
  - Files: `src/ai_company/dashboard/static/css/style.css`
  - Verification: Cards display correctly at desktop/tablet/mobile widths

- [ ] **Task 11:** Add JS methods — `renderMetricCards()`, `renderCardSparkline()`, card click-to-expand handlers
  - Files: `src/ai_company/dashboard/static/js/app.js`
  - Verification: Cards show sparklines, clicking expands detail panel

### Checkpoint: Frontend Layout
- [ ] Dashboard loads without JS errors
- [ ] 8 metric cards render around the gauge
- [ ] Sparklines display for each component
- [ ] Click-to-expand shows detail panel

### Phase 4: Analytics Integration

- [ ] **Task 12:** Wire anomaly detection for new components — extend `detect_anomalies()` to cover all 8 components
  - Files: `src/ai_company/dashboard/org_health.py`
  - Verification: Anomalies detected for new component score changes

- [ ] **Task 13:** Add category-level trend data to `/org-health/categories` response
  - Files: `src/ai_company/dashboard/api.py`
  - Verification: Categories endpoint includes trend data per category

### Checkpoint: Complete
- [ ] All tests pass (`uv run pytest`)
- [ ] Lint clean (`uv run ruff check src/ && uv run mypy src/`)
- [ ] Dashboard renders full Org Health section with 8 components
- [ ] All acceptance criteria met

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Composite becomes noisy with 8 components | Medium | Lower weights for new components (0.05-0.10); they add signal without destabilizing |
| Security scorer needs audit data that may be sparse | Low | Returns `None` (excluded from composite) when data unavailable |
| Strategic alignment needs OKR config | Low | Optional config; scorer falls back to department coverage heuristic |
| Frontend performance with 8 sparklines | Low | Sparklines are tiny (7 points); use `requestAnimationFrame` batching |
| Weight rebalance changes existing composite score | Medium | Rebalancing is proportional; existing component ratios preserved |

## Open Questions

- None — all design decisions approved in spec review.
