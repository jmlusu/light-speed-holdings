# Org Health Enhancement — Task Checklist

## Phase 1: Backend Config & Scoring Foundation

- [ ] Task 1: Update `config/org_health.yaml` — rebalance weights, add 4 new components
- [ ] Task 2: Add `_score_task_throughput()` to `OrgHealthCalculator`
- [ ] Task 3: Add `_score_escalation_rate()` to `OrgHealthCalculator`
- [ ] Task 4: Add `_score_security_posture()` to `OrgHealthCalculator`
- [ ] Task 5: Add `_score_strategic_alignment()` to `OrgHealthCalculator`
- [ ] Task 6: Wire new scorers into `_scorers()` dict and update `_default_config()`

### Checkpoint: Backend Scoring
- [ ] All existing tests pass
- [ ] New scorer unit tests pass
- [ ] `OrgHealthCalculator().compute()` returns 8 components

## Phase 2: API Layer

- [ ] Task 7: Add `GET /api/v1/org-health/categories` endpoint
- [ ] Task 8: Update `OrgHealthKPICollector.collect()` for new components

### Checkpoint: API Layer
- [ ] `/api/v1/org-health` shows 8 components
- [ ] `/api/v1/org-health/categories` returns 5 categories
- [ ] Existing API tests pass

## Phase 3: Frontend Layout

- [ ] Task 9: Expand `index.html` with 2-row metric cards grid
- [ ] Task 10: Add CSS styles for metric cards
- [ ] Task 11: Add JS methods for card rendering and interaction

### Checkpoint: Frontend Layout
- [ ] Dashboard loads without JS errors
- [ ] 8 metric cards render around the gauge
- [ ] Sparklines display for each component
- [ ] Click-to-expand shows detail panel

## Phase 4: Analytics Integration

- [ ] Task 12: Extend anomaly detection for new components
- [ ] Task 13: Add category-level trend data to categories endpoint

### Checkpoint: Complete
- [ ] All tests pass
- [ ] Lint clean
- [ ] Dashboard renders full Org Health section
- [ ] All acceptance criteria met
