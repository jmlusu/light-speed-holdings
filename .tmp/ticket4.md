## Question

Decide the Org Health score composition: components, sub-score formulas (0–100), weights, color bands/thresholds, and the `config/company/org-health.yaml` schema.

Proposed components (from telemetry inventory):
1. **Department KPI health** — avg on-track ratio across 7 department collectors (`collect_all_kpis()`)
2. **Task success rate** — completed / (completed + failed) over 30-day window (same as KPI-004)
3. **Agent utilization** — distinct active agents / registered agents (same as KPI-003)
4. **Escalation pressure** — open escalations count (inverse: fewer = better)
5. **Approval backlog** — pending approvals count (inverse)
6. **Budget utilization** — spent / budget (inverse: lower = better)

For each: define sub-score formula mapping raw metric to 0–100. Define weights (sum=1.0). Define color bands (green >= 80, amber 60-79, red < 60). Define config schema with defaults.

Config schema sketch:
```yaml
components:
  department_kpi_health:
    weight: 0.30
    formula: "avg(dept.on_track_ratio) * 100"
  task_success_rate:
    weight: 0.25
    formula: "completed / (completed + failed) * 100"
  agent_utilization:
    weight: 0.20
    formula: "active_agents / registered_agents * 100"
  escalation_pressure:
    weight: 0.10
    formula: "max(0, 100 - open_escalations * 10)"
  approval_backlog:
    weight: 0.10
    formula: "max(0, 100 - pending_approvals * 5)"
  budget_utilization:
    weight: 0.05
    formula: "max(0, 100 - (spent / budget * 100))"
bands:
  green: 80
  amber: 60
  red: 0
```

**Blocked by: Inventory dashboard telemetry sources for the Org Health score (#23)**
