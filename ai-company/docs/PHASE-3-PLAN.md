# Phase 3 Plan — Growth Functions

**Status:** Planned
**Date:** 2026-07-17
**Owner:** CTO, Lead Engineer

## Summary

Phase 3 implements growth function CLI commands (marketing, sales, customer success, legal, HR), cost management dashboard, and department-specific workflows. This phase makes the AI Company operational for business functions beyond engineering.

## Objectives

1. Implement full CLI commands for all 7 departments
2. Add cost management and budget tracking to the dashboard
3. Implement marketing campaign lifecycle management
4. Implement sales pipeline management
5. Add HR onboarding and workforce management
6. Add legal contract management
7. Add customer success ticket management

## Department CLI Commands

### Marketing (`ai-company marketing`)

| Command | Description | Priority |
|---------|-------------|----------|
| `list-campaigns` | List all marketing campaigns | P0 |
| `create-campaign` | Create a new campaign | P0 |
| `launch` | Launch a campaign | P0 |
| `metrics` | View campaign metrics | P0 |
| `pause` | Pause a running campaign | P1 |
| `archive` | Archive a completed campaign | P2 |

### Sales (`ai-company sales`)

| Command | Description | Priority |
|---------|-------------|----------|
| `list-leads` | List sales pipeline | P0 |
| `add-lead` | Add a new lead | P0 |
| `update-stage` | Move lead to next stage | P0 |
| `pipeline` | View pipeline summary | P0 |
| `forecast` | View revenue forecast | P1 |
| `close` | Mark deal as won/lost | P0 |

### HR (`ai-company hr`)

| Command | Description | Priority |
|---------|-------------|----------|
| `list-agents` | Agent workforce roster | P0 |
| `onboard` | Onboard a new agent | P0 |
| `offboard` | Offboard an agent | P0 |
| `performance` | View agent performance | P1 |
| `roster` | View department roster | P0 |

### Legal (`ai-company legal`)

| Command | Description | Priority |
|---------|-------------|----------|
| `list-contracts` | Contract management | P0 |
| `add-contract` | Register a new contract | P0 |
| `review` | Request contract review | P0 |
| `renewals` | View upcoming renewals | P1 |

### Customer Success (`ai-company customer-success`)

| Command | Description | Priority |
|---------|-------------|----------|
| `list-tickets` | Support tickets | P0 |
| `create-ticket` | Create a support ticket | P0 |
| `resolve` | Mark ticket resolved | P0 |
| `health` | Customer health scores | P1 |
| `nps` | View NPS scores | P2 |

## Cost Management Dashboard

### New API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/costs/daily` | GET | Daily cost summary |
| `/api/costs/by-agent` | GET | Cost breakdown by agent |
| `/api/costs/by-model` | GET | Cost breakdown by model |
| `/api/costs/trend` | GET | 7-day and 30-day trends |
| `/api/budget` | GET | Budget utilization status |
| `/api/budget` | POST | Update budget limits |

### Dashboard Views

- **Cost overview**: Daily spend, budget utilization, cost per agent
- **Model distribution**: Spend by LLM model (pie chart)
- **Trend analysis**: 7-day and 30-day cost trends (line chart)
- **Budget alerts**: Visual warnings when approaching budget limits

## Department Workflows

Each department gets workflow definitions in `company/workflows.yaml`:

1. **Marketing campaign lifecycle**: plan → create → review → launch → measure → archive
2. **Sales pipeline**: prospect → qualify → demo → propose → negotiate → close
3. **HR onboarding**: identify → define → review → generate → verify → approve → deploy
4. **Legal contract**: request → draft → review → negotiate → execute → monitor
5. **Customer success**: onboard → monitor → intervene → expand → renew

## Implementation Plan

| Sprint | Deliverables | Duration |
|--------|-------------|----------|
| Sprint 3.1 | Marketing CLI + campaign workflows | 2 weeks |
| Sprint 3.2 | Sales CLI + pipeline management | 2 weeks |
| Sprint 3.3 | HR + Legal + CS CLI commands | 2 weeks |
| Sprint 3.4 | Cost management dashboard + budget API | 2 weeks |

## Dependencies

- Phase 2 complete (orchestrator, executor, dashboard)
- `company/workflows.yaml` updated with department workflows
- `company/config/kpis.yaml` updated with department KPIs
- Dashboard API extended with cost management endpoints

## Success Criteria

- [ ] All 5 department CLIs functional with CRUD operations
- [ ] Cost management dashboard showing real-time spend
- [ ] Budget utilization visible in dashboard
- [ ] 5 new workflow definitions operational
- [ ] All new commands have unit tests
- [ ] All new API endpoints documented in API-REFERENCE.md

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Department workflows too complex | Medium | Medium | Start with minimal viable workflows, iterate |
| Cost tracking accuracy | Low | High | Validate against provider billing APIs |
| Dashboard performance with cost data | Low | Medium | Use JSONL streaming for cost log reads |

---

*Phase 3 adds business function capabilities. Phase 4 adds specialist agent subagents.*
