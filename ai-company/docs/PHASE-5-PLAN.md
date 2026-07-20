# Phase 5 Plan — Autonomous Coordination

**Status:** Planned
**Date:** 2026-07-17
**Owner:** CTO, COO

## Summary

Phase 5 enables fully autonomous operation: scheduled orchestration cycles, automated escalation handling, self-healing task queues, and human-in-the-loop safety gates for all critical operations. This phase transitions the AI Company from manually-triggered to autonomously-operating.

## Objectives

1. Implement scheduled orchestration via GitHub Actions (every 6 hours)
2. Add automated escalation handling and retry logic
3. Implement self-healing for failed tasks
4. Add cost budget enforcement with automatic throttling
5. Implement postmortem-driven learning
6. Add human approval gates for all critical operations

## Autonomous Scheduling

### GitHub Actions Workflow

```yaml
# .github/workflows/autonomous.yml
name: Autonomous Cycle
on:
  schedule:
    - cron: "0 */6 * * *"  # Every 6 hours
  workflow_dispatch:

jobs:
  orchestrator:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: ai-company orchestrator tick
        env:
          OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}

  executor:
    needs: orchestrator
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: ai-company executor tick
        env:
          OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}

  report:
    needs: executor
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: ai-company orchestrator briefing
```

### Cycle Flow

```
Every 6 hours:
  1. Orchestrator tick
     ├── Check due scheduled tasks
     ├── Process pending escalations
     ├── Review pending approvals
     └── Generate briefing if new day

  2. Executor tick
     ├── Process all pending tasks
     ├── Execute tool calls with HITL gates
     ├── Enforce budget limits
     └── Report completions/failures

  3. Report
     ├── Generate executive briefing
     ├── Update dashboard KPIs
     └── Send alerts for critical items
```

## Automated Escalation

### Escalation Rules

| Trigger | Condition | Escalate To | Timeout | Max Retries |
|---------|-----------|------------|---------|-------------|
| Task timeout | > 30 min without completion | Department executive | 30 min | 3 |
| Consecutive failures | 3 failures on same task | Chief of Staff | 1 hour | 2 |
| Budget exceeded | Daily/task budget hit limit | CFO | Immediate | 0 |
| HITL timeout | No human response in 30 min | Chief of Staff | 30 min | 1 |
| Security violation | Path traversal detected | CTO + CEO | Immediate | 0 |
| Provider outage | All providers in tier failing | CTO | 15 min | 5 |

### Retry Logic

```python
for attempt in range(max_retries):
    try:
        result = executor.run_task(task)
        if result.success:
            break
    except BudgetExceeded:
        escalate(task, "budget_exceeded")
        break
    except ProviderError:
        # Automatic fallback to next provider in tier
        continue
    except Exception as e:
        if attempt == max_retries - 1:
            escalate(task, "max_retries_exceeded")
```

## Self-Healing Task Queue

### Health Checks

| Check | Frequency | Action on Failure |
|-------|-----------|-------------------|
| Task queue integrity | Every cycle | Rebuild from logs |
| Agent file validity | Every cycle | Regenerate from registry |
| LLM provider health | Every cycle | Switch to fallback provider |
| Dashboard health | Every cycle | Restart service |
| Cost log integrity | Daily | Reconcile with provider billing |

### Recovery Procedures

1. **Corrupted task queue**: Rebuild from `orchestrator/escalation.yaml` and `orchestrator/approvals.yaml`
2. **Missing agent files**: Regenerate from `company/agent-registry.json`
3. **Provider failure**: Automatic fallback to next provider in tier
4. **Dashboard down**: Restart via systemd or Docker health check
5. **Cost log gap**: Mark affected period as "untracked" and continue

## Cost Budget Enforcement

### Throttling Rules

| Condition | Action | Duration |
|-----------|--------|----------|
| Daily budget > 80% | Route non-critical tasks to fast tier | Until midnight |
| Daily budget > 95% | Pause non-critical tasks | Until budget reset |
| Per-task budget exceeded | Terminate task immediately | Permanent |
| Cost anomaly detected | Alert CFO, pause affected agent | Until review |

### Budget Reset

Daily budgets reset at midnight UTC. The `CostTracker` tracks:
- Daily spend across all agents and models
- Per-task spend for each active task
- Per-agent spend for each agent
- Per-department spend for each department

## Postmortem-Driven Learning

### Automated Postmortem Triggers

| Trigger | Severity | Auto-create? |
|---------|----------|-------------|
| SEV-1 incident | Critical | Yes |
| SEV-2 incident | High | Yes |
| SEV-3 incident | Medium | Optional |
| Budget exceeded | High | Yes |
| Security violation | Critical | Yes |

### Learning Integration

Postmortems are reviewed by the CTO and used to:
1. **Update escalation rules**: Adjust timeouts and retry limits
2. **Improve agent configurations**: Adjust tools, permissions, model tiers
3. **Enhance HITL gates**: Add new dangerous operation patterns
4. **Refine budget thresholds**: Adjust daily and per-task limits

## Human-in-the-Loop Safety Gates

### Approval Matrix

| Action Type | Approval Required | Timeout |
|------------|-------------------|---------|
| Task creation (simple) | Auto-approve | N/A |
| Tool execution (read) | Auto-approve | N/A |
| Tool execution (write) | Single approval | 30 min |
| Tool execution (execute) | Dual approval | 30 min |
| Budget allocation | CFO approval | 24 hours |
| Agent creation | HR + CTO approval | 48 hours |
| Production deployment | CEO approval | 24 hours |
| Security changes | CTO + CEO approval | Immediate |

### Safety Boundaries

- Agents cannot modify their own permissions
- Agents cannot modify other agents' configurations
- Agents cannot access files outside their sandbox
- Agents cannot exceed budget limits
- Agents cannot bypass HITL gates

## Implementation Plan

| Sprint | Deliverables | Duration |
|--------|-------------|----------|
| Sprint 5.1 | GitHub Actions autonomous workflow | 2 weeks |
| Sprint 5.2 | Automated escalation + retry logic | 2 weeks |
| Sprint 5.3 | Self-healing + health checks | 2 weeks |
| Sprint 5.4 | Cost throttling + safety gates | 2 weeks |

## Dependencies

- Phase 4 complete (specialist agents, delegation chains)
- GitHub Actions secrets configured (API keys)
- Systemd timers configured for on-premise deployment
- All existing tests passing

## Success Criteria

- [ ] Orchestrator runs autonomously every 6 hours via GitHub Actions
- [ ] Executor processes all pending tasks automatically
- [ ] Escalations handled without human intervention (for routine cases)
- [ ] Budget enforcement stops runaway costs
- [ ] Postmortems generated automatically for SEV-1/SEV-2 incidents
- [ ] HITL gates block all dangerous operations
- [ ] Dashboard shows real-time autonomous operation status
- [ ] System recovers from common failures without human intervention

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Autonomous cycle costs too much | Medium | High | Aggressive budget throttling, fast tier for routine tasks |
| False positive escalations | Medium | Medium | Tune escalation thresholds based on production data |
| Postmortem quality too low | Low | Medium | Human review required for all postmortems |
| Safety gate too restrictive | Medium | Medium | Regular review and adjustment of approval matrix |

---

*Phase 5 enables autonomous operation. Future phases add multi-company support, marketplace, and enterprise features.*
