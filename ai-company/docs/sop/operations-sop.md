# Operations Standard Operating Procedure

**Document ID:** SOP-OPS-001
**Department:** Operations
**Owner:** Chief Operating Officer (COO)
**Classification:** Internal
**Last Updated:** July 2026

---

## 1. Purpose

This Standard Operating Procedure establishes the processes for process optimization, metrics tracking, vendor management, and capacity planning within Light Speed Holdings' AI Company Builder. It ensures efficient, scalable operations that support the organization's growth while maintaining quality and cost control.

## 2. Scope

This SOP applies to all operational activities including:

- Process design, optimization, and automation
- Performance metrics collection and analysis
- Vendor and supplier management
- Capacity planning and resource allocation
- Infrastructure and environment management
- Quality assurance and process compliance
- Workflow orchestration via the `MessageBus` and `Scheduler`
- Escalation management and postmortem processes

## 3. Roles and Responsibilities

| Role | Agent/Person | Responsibilities |
|------|-------------|-----------------|
| COO | `coo` (executive) | Operational strategy, process ownership, resource allocation |
| Ops Lead | `ops_lead` (specialist) | Day-to-day operations, process execution, monitoring |
| HR Lead | `hr_lead` (specialist) | Agent onboarding, staffing, performance management |
| CTO | `cto` | Technical infrastructure, system reliability |
| Chief of Staff | `chief_of_staff` | Cross-department coordination, strategic alignment |
| CEO / Founder | Human operator | Strategic decisions, final approval on operational changes |

## 4. Process Management

### 4.1 Process Lifecycle

Every operational process follows a defined lifecycle:

```
Design -> Implement -> Monitor -> Optimize -> Archive
```

| Phase | Activities | Owner |
|-------|-----------|-------|
| Design | Define process, roles, SLAs, escalation paths | COO |
| Implement | Create workflows, configure tools, train agents | Ops Lead |
| Monitor | Track KPIs, collect feedback, identify issues | Ops Lead |
| Optimize | Analyze data, implement improvements, measure impact | COO |
| Archive | Document lessons learned, retire obsolete processes | Ops Lead |

### 4.2 Process Documentation

Every process must be documented with:

1. **Purpose**: Why this process exists
2. **Scope**: What it covers and what it does not
3. **Roles**: Who is involved and their responsibilities
4. **Steps**: Detailed workflow with decision points
5. **SLAs**: Response and resolution time targets
6. **Escalation**: What happens when things go wrong
7. **Metrics**: How success is measured
8. **Compliance**: Regulatory and policy requirements

### 4.3 Workflow Orchestration

Processes are orchestrated through the `MessageBus` (`src/ai_company/orchestrator/message_bus.py`):

```python
from ai_company.orchestrator.message_bus import MessageBus
from ai_company.models.task import Task, TaskPriority

bus = MessageBus()

# Create a task for the next process step
task = Task(
    id="ops-process-001",
    name="Quarterly vendor review",
    sender_id="coo",
    receiver_id="ops_lead",
    priority=TaskPriority.HIGH,
    instruction="Complete quarterly review of LLM vendor contracts",
)
bus.send_task(task)
```

### 4.4 Scheduled Operations

Recurring operations are managed via the `Scheduler` (`src/ai_company/orchestrator/scheduler.py`):

```python
from ai_company.orchestrator.scheduler import Scheduler

scheduler = Scheduler()

# Schedule a daily health check
scheduler.add_task(
    task_id="daily-health-check",
    name="Daily system health check",
    interval_minutes=1440,  # 24 hours
    task_template={
        "name": "Run doctor checks",
        "instruction": "ai-company doctor run",
        "priority": "medium",
    },
)
```

## 5. Metrics and Monitoring

### 5.1 Operational Metrics

| Metric | Description | Target | Collection |
|--------|-------------|--------|-----------|
| System uptime | Dashboard and API availability | 99.9% | Health check endpoint |
| Task throughput | Tasks completed per day | > 50 | MessageBus |
| Average task duration | Time from assignment to completion | < 30 min | Task timestamps |
| Escalation rate | % of tasks escalated | < 15% | EscalationManager |
| Agent utilization | % of agents with active tasks | > 70% | Dashboard |
| Error rate | % of tasks that fail | < 5% | TaskStatus.FAILED |

### 5.2 Dashboard KPIs

The CEO Dashboard (`src/ai_company/dashboard/`) provides real-time operational visibility:

- **KPI Collector** (`src/ai_company/dashboard/kpi_collector.py`): Aggregates metrics from all departments
- **WebSocket updates** (`src/ai_company/dashboard/ws.py`): Real-time metric streaming
- **Department KPIs**: `src/ai_company/dashboard/kpis/` per-department metrics

### 5.3 Health Checks

The `Doctor` system provides automated health monitoring:

```bash
ai-company doctor run
```

Checks include:
- System component availability
- LLM provider connectivity
- MessageBus inbox status
- CostTracker logging status
- HITL gate responsiveness
- Scheduler task execution

### 5.4 Reporting

| Report | Frequency | Owner | Audience |
|--------|-----------|-------|---------|
| Daily operations summary | Daily | Ops Lead | COO |
| Weekly KPI report | Weekly | Ops Lead | Executive team |
| Monthly business review | Monthly | COO | Board |
| Quarterly strategic review | Quarterly | COO + CEO | Board + investors |

## 6. Vendor Management

### 6.1 Vendor Categories

| Category | Vendors | Contract Type | Review Cycle |
|----------|---------|--------------|-------------|
| LLM Providers | OpenAI, Anthropic, DeepSeek | Usage-based | Monthly |
| Infrastructure | Ollama (self-hosted), Docker | Self-managed | Quarterly |
| Software | Python packages, dev tools | Open source / subscription | Semi-annual |
| Services | Consulting, support | SOW-based | Per engagement |

### 6.2 Vendor Evaluation

New vendors are evaluated using the following criteria:

| Criterion | Weight | Minimum Score |
|-----------|--------|--------------|
| Cost competitiveness | 25% | 7/10 |
| Reliability/uptime | 25% | 9/10 |
| Security/compliance | 20% | 8/10 |
| Integration ease | 15% | 7/10 |
| Support quality | 15% | 7/10 |

### 6.3 LLM Provider Management

The `ModelRouter` (`src/ai_company/model_router.py`) manages LLM provider relationships:

**Provider chain configuration:**

Each tier defines an ordered list of providers for automatic fallback:

```yaml
# company/models.yaml
tiers:
  standard:
    providers:
      - provider: openai
        model: gpt-4o-mini
      - provider: anthropic
        model: claude-3-5-haiku-20241022
      - provider: ollama
        model: llama3.1:8b
```

**Provider health monitoring:**

The `LLMClient` (`src/ai_company/llm/client.py`) implements automatic fallback:

1. Try the first provider in the tier
2. On failure, try the next provider in the chain
3. Log the failure and switch for subsequent calls
4. Report provider health to the dashboard

### 6.4 Vendor Review Cadence

| Vendor | Review | Focus | Owner |
|--------|--------|-------|-------|
| OpenAI | Monthly | Cost, uptime, model updates | CAIO |
| Anthropic | Monthly | Cost, uptime, model updates | CAIO |
| DeepSeek | Monthly | Cost, availability | CAIO |
| Ollama | Quarterly | Performance, model updates | CTO |

## 7. Capacity Planning

### 7.1 Resource Types

| Resource | Measurement | Scaling Method |
|----------|-------------|---------------|
| Agent capacity | Max concurrent tasks per agent | Add agents to registry |
| LLM throughput | Tokens per minute | Upgrade provider tier |
| Storage | GB used for logs and data | Archive old data |
| Dashboard connections | WebSocket connections | Horizontal scaling |
| MessageBus capacity | Tasks in inbox | Process or archive |

### 7.2 Capacity Thresholds

| Resource | Warning (80%) | Critical (95%) | Action |
|----------|--------------|----------------|--------|
| Agent task queue | 40 pending tasks | 48 pending tasks | Add agents, redistribute |
| Daily LLM budget | $40 of $50 | $47.50 of $50 | Review task priorities |
| Storage (logs) | 8 GB of 10 GB | 9.5 GB of 10 GB | Archive old logs |
| Dashboard memory | 800 MB of 1 GB | 950 MB of 1 GB | Restart, optimize |

### 7.3 Scaling Procedures

**Vertical scaling (more resources per agent):**

1. Update `LoopConfig.max_iterations` if agents are hitting iteration limits
2. Increase `LoopConfig.max_tokens` for tasks requiring longer outputs
3. Upgrade the model tier for agents needing more capability

**Horizontal scaling (more agents):**

1. Add new agent entries to `company-registry.yaml`
2. Assign appropriate tools and permissions
3. Configure model routing for the new agent
4. Regenerate agent files: `AgentGenerator().generate_all()`
5. Verify the new agent appears in `ai-company agents list`

## 8. Escalation Management

### 8.1 Escalation Rules

The `EscalationManager` (`src/ai_company/orchestrator/escalation.py`) defines automated escalation:

| Rule | Trigger | Escalate To | Timeout |
|------|---------|------------|---------|
| Task failure | 3 consecutive failures | Department executive | 30 min |
| Budget exceeded | CostTracker check fails | CFO | Immediate |
| HITL timeout | No human response in 30 min | Chief of Staff | 30 min |
| Security violation | Path traversal detected | CTO + CEO | Immediate |
| System outage | Health check fails | CTO | 15 min |

### 8.2 Postmortem Process

After SEV-1 or SEV-2 incidents:

1. **Create postmortem** using `PostmortemStore`:
   ```python
   from ai_company.orchestrator.escalation import PostmortemStore, Postmortem
   store = PostmortemStore()
   postmortem = Postmortem(
       incident_id="INC-<task_id>",
       title="Brief description of incident",
       severity="high",
       affected_agent="<agent_id>",
       department="<department>",
   )
   store.save(postmortem)
   ```

2. **Complete the postmortem** within 48 hours:
   - Root cause analysis
   - Impact assessment (tasks affected, downtime, cost)
   - Timeline of events
   - Resolution steps taken
   - Action items for prevention
   - Lessons learned

3. **Review** the postmortem with the executive team

4. **Implement** preventive measures and track completion

## 9. Quality Assurance

### 9.1 Process Compliance

| Check | Frequency | Method | Owner |
|-------|-----------|--------|-------|
| SOP adherence | Weekly | Spot check | Ops Lead |
| Documentation currency | Monthly | Review all SOPs | COO |
| Escalation SLA compliance | Per incident | Automated tracking | Ops Lead |
| Budget adherence | Daily | CostTracker reports | CFO |

### 9.2 Continuous Improvement

The operations team follows a continuous improvement cycle:

1. **Measure**: Collect metrics on process performance
2. **Analyze**: Identify bottlenecks, inefficiencies, and failures
3. **Improve**: Implement changes to address identified issues
4. **Verify**: Confirm the improvement achieved the desired result
5. **Standardize**: Update SOPs to reflect the improved process

## 10. Escalation Procedures

| Condition | Escalate To | SLA |
|-----------|------------|-----|
| Process failure affecting multiple departments | COO + CEO | 4 hours |
| Vendor contract dispute | Legal + CFO | 24 hours |
| System outage > 15 minutes | CTO + CEO | Immediate |
| Capacity threshold breached | COO | 4 hours |
| Regulatory compliance gap | Legal + Compliance Officer | 24 hours |
| Cross-team coordination needed | Chief of Staff | 8 hours |

## 11. Key Performance Indicators

| KPI | Target | Frequency | Owner |
|-----|--------|-----------|-------|
| System uptime | 99.9% | Monthly | CTO |
| Task throughput | > 50 tasks/day | Daily | Ops Lead |
| Average task duration | < 30 minutes | Weekly | Ops Lead |
| Escalation rate | < 15% | Monthly | COO |
| Process documentation coverage | 100% | Quarterly | COO |
| Vendor SLA compliance | > 99% | Monthly | Ops Lead |
| Postmortem completion rate | 100% within 48h | Per incident | COO |

## 12. Compliance Requirements

- All operational processes must be documented in SOPs
- Vendor contracts must be reviewed by Legal before execution
- Capacity planning reviews must be conducted quarterly
- Postmortems must be completed within 48 hours for SEV-1/SEV-2 incidents
- Metrics must be collected and reported on the defined cadence
- Escalation rules must be tested monthly

## 13. Related Documents

- `docs/ARCHITECTURE.md` - System architecture
- `docs/DEVOPS-PLAN.md` - DevOps and infrastructure
- `docs/raci-escalation.md` - RACI matrix for escalation
- `docs/raci-deployment.md` - RACI matrix for deployment
- `src/ai_company/orchestrator/message_bus.py` - Task orchestration
- `src/ai_company/orchestrator/scheduler.py` - Scheduled operations
- `src/ai_company/orchestrator/escalation.py` - Escalation management
- `src/ai_company/dashboard/` - CEO Dashboard

---

*This document is maintained by the Operations department. Updates require COO approval.*
