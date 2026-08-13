# Phase 4 Plan — Specialist Agents

**Status:** Planned
**Date:** 2026-07-17
**Owner:** CTO, CAIO

## Summary

Phase 4 implements specialist agent subagents that operate within each department. These agents have specific skills, tool access, and reporting hierarchies. This phase moves from a flat agent list to a true hierarchical organization with delegation chains.

## Objectives

1. Implement subagent spawning and management
2. Add department-specific specialist agents (Financial Analyst, DevOps Engineer, etc.)
3. Implement agent-to-agent delegation via MessageBus
4. Add agent capability matching for task routing
5. Implement agent performance tracking

## New Specialist Agents

### Engineering Department

| Agent | Role | Tools | Tier |
|-------|------|-------|------|
| `devops-engineer` | CI/CD, infrastructure, deployments | bash, docker, kubernetes | standard |
| `security-analyst` | Security reviews, vulnerability scanning | bash, grep, read | premium |
| `qa-engineer` | Testing, quality assurance | python, pytest, bash | standard |
| `data-analyst` | Data analysis, reporting | python, sql, pandas | standard |

### Finance Department

| Agent | Role | Tools | Tier |
|-------|------|-------|------|
| `financial-analyst` | Financial modeling, forecasting | python, excel, read | premium |
| `cost-optimizer` | LLM cost optimization, routing tuning | python, read, write | standard |
| `accountant` | Bookkeeping, reconciliation | python, excel | standard |

### Marketing Department

| Agent | Role | Tools | Tier |
|-------|------|-------|------|
| `seo-specialist` | SEO optimization, keyword research | read, write, websearch | standard |
| `social-media-manager` | Social media content, scheduling | read, write | fast |
| `copywriter` | Long-form content, blog posts | read, write | standard |

### Sales Department

| Agent | Role | Tools | Tier |
|-------|------|-------|------|
| `sales-analyst` | Pipeline analysis, forecasting | python, read | standard |
| `proposal-writer` | RFP responses, proposals | read, write | standard |

### Operations Department

| Agent | Role | Tools | Tier |
|-------|------|-------|------|
| `process-optimizer` | Process analysis, automation | python, read, write | standard |
| `vendor-manager` | Vendor evaluation, contract tracking | read, write | standard |

## Architecture

```
CEO (Human)
  └── Chief of Staff
        ├── CTO
        │     ├── Lead Engineer
        │     │     ├── Backend Engineer
        │     │     ├── Frontend Engineer
        │     │     └── DevOps Engineer (NEW)
        │     ├── Security Analyst (NEW)
        │     └── QA Engineer (NEW)
        ├── CFO
        │     └── Financial Analyst (NEW)
        ├── COO
        │     ├── HR Lead
        │     ├── Ops Lead
        │     │     └── Process Optimizer (NEW)
        │     └── Vendor Manager (NEW)
        ├── CMO
        │     ├── Content Creator
        │     ├── SEO Specialist (NEW)
        │     └── Social Media Manager (NEW)
        ├── Head of Sales
        │     ├── Sales Rep
        │     └── Sales Analyst (NEW)
        ├── Head of Customer Success
        │     └── Support Engineer
        └── General Counsel
              └── Compliance Officer
```

## Subagent Spawning

### Agent Registry Extension

```json
{
  "id": "devops-engineer",
  "name": "DevOps Engineer",
  "role": "DevOps Engineer",
  "type": "Specialist",
  "department": "engineering",
  "reportsTo": "lead-engineer",
  "tools": ["bash", "docker", "kubernetes"],
  "permissions": ["read", "edit", "execute"],
  "model_tier": "standard",
  "max_concurrent_tasks": 3,
  "capabilities": ["ci_cd", "infrastructure", "deployment", "monitoring"]
}
```

### Task Routing

Tasks are routed to agents based on:
1. **Explicit assignment**: Task specifies `receiver_id`
2. **Capability matching**: Task requirements matched to agent capabilities
3. **Load balancing**: Distribute across available agents in a department
4. **Escalation**: Unmatched tasks escalate to department executive

### Agent-to-Agent Delegation

```
Human CEO → Chief of Staff
  → CTO → Lead Engineer
    → DevOps Engineer (runs deployment)
    → reports back to Lead Engineer
  → Lead Engineer reports back to CTO
  → CTO reports back to Chief of Staff
```

Delegation chain is tracked via the MessageBus task hierarchy.

## Implementation Plan

| Sprint | Deliverables | Duration |
|--------|-------------|----------|
| Sprint 4.1 | Subagent spawning, capability matching | 2 weeks |
| Sprint 4.2 | Engineering specialists (devops, security, QA) | 2 weeks |
| Sprint 4.3 | Business specialists (finance, marketing, sales) | 2 weeks |
| Sprint 4.4 | Operations specialists + delegation chains | 2 weeks |

## Dependencies

- Phase 3 complete (department CLIs, cost management)
- `company/agent-registry.json` updated with new specialist entries
- `company/departments.yaml` updated with new agent assignments
- Task routing logic in MessageBus extended for capability matching

## Success Criteria

- [ ] 15+ new specialist agents defined in registry
- [ ] Subagent spawning works from CLI
- [ ] Task routing matches capabilities to tasks
- [ ] Agent-to-agent delegation chains tracked
- [ ] Dashboard shows agent utilization and performance
- [ ] All new agents have unit tests
- [ ] Performance benchmarks for task routing (<10ms)

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Delegation chains too deep | Medium | Medium | Max 4 levels enforced |
| Capability matching too loose | Medium | High | Start with explicit assignment, add matching later |
| Agent performance tracking overhead | Low | Low | Use existing KPI collector infrastructure |

---

*Phase 4 adds specialist agents. Phase 5 enables autonomous coordination and scheduling.*
