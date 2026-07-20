# Phase 2 Complete — Core Operations

**Status:** Complete
**Date:** 2026-07-17
**Owner:** CTO, Lead Engineer

## Summary

Phase 2 built the operational core: MessageBus, orchestrator (scheduler, escalation, approval, briefing), executor (ReAct loop, HITL gates, tool runner), decision engine, workflow engine, memory engine, graph engine, model router, and the FastAPI CEO dashboard with WebSocket support.

## What Was Built

### MessageBus

- **File**: `src/ai_company/orchestrator/message_bus.py`
- **Storage**: `orchestrator/inbox.json` (JSON-backed task queue)
- **Operations**: send_task, get_inbox, update_task_status, get_pending_tasks
- **See**: [ADR-002](adr/002-json-message-bus.md)

### Orchestrator

| Component | File | Purpose |
|-----------|------|---------|
| Scheduler | `orchestrator/scheduler.py` | Recurring task scheduling |
| Escalation | `orchestrator/escalation.py` | Automated escalation rules |
| Approval | `orchestrator/approval.py` | Human-in-the-loop approval gates |
| Briefing | `orchestrator/briefing.py` | Daily executive briefings |
| Postmortem | `orchestrator/escalation.py` | Incident postmortem tracking |

**Data files:**
- `orchestrator/scheduler.yaml` — Scheduled recurring tasks
- `orchestrator/approvals.yaml` — Pending approval requests
- `orchestrator/escalation.yaml` — Escalation events
- `orchestrator/postmortems/` — Incident postmortem records (YAML per incident)

### Executor

- **File**: `src/ai_company/executor/loop.py`
- **Pattern**: ReAct (Reason + Act) — see [ADR-003](adr/003-react-agent-loop.md)
- **Components**:
  - `loop.py` — Main execution loop with budget enforcement
  - `tool_runner.py` — Sandboxed tool execution
  - `hitl_gate.py` — Human-in-the-loop approval gates
  - `context.py` — Execution context management

### Decision Engine

- **File**: `src/ai_company/decision/engine.py`
- **Features**: Approval matrix, risk assessment, decision tree navigation
- **CLI**: `ai-company decision evaluate`, `ai-company decision matrix`, `ai-company decision tree`

### Workflow Engine

- **File**: `src/ai_company/workflow/engine.py`
- **Features**: 9 workflow definitions, step tracking, SLA monitoring
- **CLI**: `ai-company workflows list`

### Memory Engine

- **File**: `src/ai_company/memory/engine.py`
- **Types**: episodic, semantic, procedural, relational, temporal, aggregate
- **Storage**: `memory/*.json` (one file per memory type)
- **CLI**: `ai-company memory list`, `ai-company memory search`, `ai-company memory add`, `ai-company memory consolidate`

### Graph Engine

- **File**: `src/ai_company/graph/engine.py`
- **Types**: org_chart, decision, workflow, knowledge
- **Algorithm**: BFS pathfinding (NetworkX optional)
- **CLI**: `ai-company graph list`, `ai-company graph show`, `ai-company graph path`

### Model Router

- **File**: `src/ai_company/model_router.py`
- **Tiers**: fast, standard, premium (see [ADR-004](adr/004-multi-provider-llm.md))
- **Routing**: per-agent override → context rules → type+priority rules → fallback
- **CLI**: `ai-company models list`, `ai-company models tiers`

### LLM Client

- **File**: `src/ai_company/llm/client.py`
- **Providers**: OpenCode, OpenAI, Anthropic, DeepSeek, Ollama
- **Features**: Automatic fallback, cost tracking, streaming support

### CEO Dashboard

- **File**: `src/ai_company/dashboard/api.py`
- **Framework**: FastAPI with WebSocket support
- **Port**: localhost:8420 (auto-opens browser)
- **Endpoints**: 20+ REST API routes + WebSocket at `/ws/dashboard`
- **KPIs**: 28 department KPIs across 7 departments
- **See**: [API Reference](API-REFERENCE.md)

### CLI Commands (24 total)

| Category | Commands |
|----------|----------|
| Core | `company run`, `generate`, `status`, `doctor` |
| Agents | `agents list` |
| Orchestrator | `orchestrator tick`, `orchestrator briefing`, `orchestrator scheduler list/add/remove`, `orchestrator escalation list/add/remove/pending`, `orchestrator approval pending/approve/reject`, `orchestrator postmortem list/create/show/update/render` |
| Executor | `executor tick`, `executor start`, `executor run-task`, `executor status` |
| Decision | `decision evaluate`, `decision matrix`, `decision tree` |
| Graph | `graph list`, `graph show`, `graph path` |
| Memory | `memory list`, `memory add`, `memory search`, `memory consolidate` |
| Workflows | `workflows list` |
| Dashboard | `dashboard`, `dashboard kpi list`, `dashboard kpi show` |
| Models | `models list`, `models tiers` |
| Department | `marketing list-campaigns`, `sales list-leads`, `hr list-agents`, `legal list-contracts`, `customer-success list-tickets`, `board list` |
| Governance | `sop`, `raci` |

## What Was NOT Built (Deferred to Later Phases)

- Growth function CLI commands (marketing campaigns, sales pipeline, HR onboarding)
- Specialist agent subagents
- Autonomous scheduling (GitHub Actions)
- Cost management dashboard
- Postmortem rendering to markdown
- WebSocket subscribe/filter topics

## Test Coverage

- **466 unit tests** covering: models, registry, orchestrator, executor, dashboard, memory, graphs, workflows, decision engine, model routing, generation, audit trail
- All tests passing

## Architecture

```
+-----------------------------------------------------+
|                    CLI Layer                         |
|  Typer app -> 24 subcommands -> domain engines      |
+-----------------------------------------------------+
|                  Engine Layer                        |
|  Orchestrator | Executor | Decision | Workflow      |
|  Memory       | Graph    | Model Router             |
+-----------------------------------------------------+
|                  Model Layer                         |
|  57 Pydantic models -> CompanyRegistry              |
+-----------------------------------------------------+
|                Infrastructure                        |
|  Registry (19 YAMLs) | Templates (14 Jinja2)       |
|  Task Queue (JSON)    | LLM Providers (5)           |
+-----------------------------------------------------+
|                  Dashboard Layer                     |
|  FastAPI REST API | WebSocket | KPI Collectors      |
+-----------------------------------------------------+
```

## Key Metrics

| Metric | Value |
|--------|-------|
| CLI commands | 24 |
| Pydantic models | 57 |
| REST API endpoints | 20+ |
| KPI definitions | 28 |
| Workflow definitions | 9 |
| Memory types | 6 |
| Graph types | 4 |
| LLM providers | 5 |
| Unit tests | 466 |
| Lines of code | ~15,000 |

## Technical Decisions

- **ReAct pattern** for executor loop (see [ADR-003](adr/003-react-agent-loop.md))
- **Multi-provider LLM** with tier-based routing (see [ADR-004](adr/004-multi-provider-llm.md))

## Lessons Learned

1. **Dashboard first**: Building the dashboard early made it easy to visualize system state during development
2. **Budget enforcement is critical**: The CostTracker caught several runaway loops during testing
3. **HITL gates are non-negotiable**: Several dangerous tool calls were correctly intercepted
4. **Pydantic v2 is fast**: Model validation overhead is negligible even with 57 models

---

*Phase 2 delivered the operational core. Phase 3 adds growth function CLI commands and cost management.*
