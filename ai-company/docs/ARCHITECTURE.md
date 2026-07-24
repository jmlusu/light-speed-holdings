# Architecture

## 1 Module Hierarchy

```
src/ai_company/
├── cli/                        # Typer CLI commands (24 subcommands)
│   ├── main.py                 # App entry point, registers all subcommands
│   ├── company.py              # Bootstrap engine CLI (company run/status)
│   ├── decision.py             # Decision engine CLI (evaluate/matrix/tree)
│   ├── graph.py                # Graph engine CLI (list/show/path)
│   ├── workflows.py            # Workflow engine CLI (list/run/status/advance)
│   ├── memory.py               # Memory engine CLI (list/add/search/consolidate)
│   ├── agents.py               # Agent management
│   ├── board.py                # Board of directors
│   ├── departments.py          # Department management
│   ├── executives.py           # Executive management
│   ├── specialists.py          # Specialist agent management
│   ├── orchestrator.py         # Autonomous coordination (postmortem sub-app)
│   ├── doctor.py               # System diagnostics
│   ├── dashboard.py            # CEO dashboard (kpi sub-app)
│   ├── executor.py             # Autonomous task execution
│   ├── models.py               # LLM model selection
│   ├── marketing.py            # Marketing operations
│   ├── sales.py                # Sales operations
│   ├── customer_success.py     # Customer success operations
│   ├── legal.py                # Legal operations
│   └── hr.py                   # HR operations
├── executor/                   # Task execution pipeline
│   ├── loop.py                 # Executor — polls inbox, runs AgentLoop, DLQ, memory
│   ├── agent_loop.py           # AgentLoop — ReAct pattern, multi-turn LLM↔tool
│   ├── tool_runner.py          # Tool execution with HITL gates
│   ├── hitl_gate.py            # Human-in-the-loop approval gates
│   ├── context.py              # Agent spec parsing, prompt building
│   ├── prompts.py              # System/user prompt templates
│   └── dead_letter.py          # Dead-letter queue for stale tasks (GAP-017)
├── llm/                        # LLM abstraction layer
│   ├── client.py               # LLMClient — multi-provider, retry, JSON parse
│   ├── cost_tracker.py         # CostTracker — JSONL logging, budgets, per-model pricing
│   ├── circuit_breaker.py      # CircuitBreaker — fail-fast after N errors
│   ├── json_parser.py          # parse_llm_json() — shared 3-strategy parser
│   └── providers/              # Provider implementations (base, openai, ollama, etc.)
├── orchestrator/               # Task orchestration
│   ├── message_bus.py          # JSON-based task queue (.opencode/inbox.json)
│   ├── briefing.py             # Daily executive briefings
│   ├── scheduler.py            # Task scheduling for autonomous cycles
│   ├── escalation.py           # Escalation rules and postmortem tracking
│   ├── approval.py             # Approval gate (request/approve/reject/expiry)
│   ├── approval_prompts.py     # HITL approval prompt templates
│   └── tier_rules.py           # 5-tier action classification (418 lines)
├── models/                     # Pydantic domain models (17+)
│   ├── models.py               # All domain models (Company, Executive, etc.)
│   ├── task.py                 # Task re-exports (backward compat)
│   ├── company.py              # Company config models
│   ├── board.py                # Board member models
│   ├── executive.py            # Executive models
│   ├── department.py           # Department models
│   ├── agent.py                # Agent models
│   ├── workflow.py             # Workflow models
│   ├── project.py              # Project models
│   └── meeting.py              # Meeting models
├── registry/                   # Config registry system
│   ├── __init__.py             # load_registry() entry point
│   ├── loader.py               # YAML file loading (19 config files)
│   ├── parser.py               # Raw dicts → typed models
│   ├── resolver.py             # Cross-reference resolution
│   └── validator.py            # Structural validation
├── config/                     # Config loader
│   └── __init__.py             # load_config() function
├── builder/                    # Bootstrap engine
│   └── __init__.py             # BootstrapEngine — full company generation
├── decision/                   # Decision engine
│   └── engine.py               # DecisionEngine — approvals, risk, trees
├── workflow/                   # Workflow engine
│   └── engine.py               # WorkflowEngine — 9 workflows, step tracking, SLA
├── memory/                     # Memory engine
│   ├── engine.py               # MemoryStore — 6 types, persistence
│   └── integration.py          # Executor integration (recall context before tasks)
├── graph/                      # Graph engine
│   └── engine.py               # GraphEngine — 4 graph types, BFS pathfinding
├── audit/                      # Audit trail package
│   ├── __init__.py             # Public API: AuditEvent, AuditWriter, AuditReader
│   ├── events.py               # AuditEvent model, AuditEventType enum
│   ├── writer.py               # AuditWriter — JSONL append
│   ├── reader.py               # AuditReader — query/filter by task, agent, type
│   └── integration.py          # Executor hooks: log_tool_call, log_task_status, log_hitl_decision
├── dashboard/                  # CEO dashboard
│   ├── app.py                  # FastAPI app with CORS, middleware
│   ├── api.py                  # REST endpoints (tasks, KPIs, costs, approvals)
│   ├── ws.py                   # WebSocket endpoint (ping/pong, broadcast stubs)
│   ├── kpi_collector.py        # KPI collection orchestrator
│   ├── analytics.py            # History tracking, trends, alerts, summaries
│   ├── retention.py            # Data retention policies
│   ├── models.py               # Dashboard-specific Pydantic models
│   └── kpis/                   # Per-department KPI collectors
│       ├── __init__.py         # collect_all_kpis() — iterates all 7 collectors
│       ├── base.py             # KPICollector base class
│       ├── engineering.py      # Engineering KPIs
│       ├── finance.py          # Finance KPIs
│       ├── hr.py               # HR KPIs
│       ├── legal.py            # Legal KPIs
│       ├── marketing.py        # Marketing KPIs
│       ├── sales.py            # Sales KPIs
│       └── customer_success.py # Customer Success KPIs
├── doctor/                     # System diagnostics
│   ├── doctor.py               # Diagnostic runner
│   ├── checks.py               # Individual check functions
│   └── report.py               # Report generation
├── generator.py                # Agent .md file generation from templates
├── model_router.py             # LLM model selection by agent/context
├── config.py                   # Config utilities
├── builder.py                  # Legacy builder (use builder/ package)
├── registry.py                 # Legacy registry (use registry/ package)
├── graph.py                    # Legacy graph (use graph/ package)
└── utils.py                    # Shared utilities (currently empty)
```

## 2 Naming Conventions

Agent naming follows a strict convention using hyphens (kebab-case) throughout.

### Convention Summary

| Layer | Convention | Example | Notes |
|-------|-----------|---------|-------|
| Registry IDs (`company-registry.yaml`) | **hyphens** | `board-chair`, `financial-analyst` | Canonical format per CEO Directive |
| Generated filenames (`.opencode/agents/`) | **hyphens** | `board-chair.md`, `financial-analyst.md` | Must match registry IDs |
| Config file references (`config/**/*.yaml`) | **hyphens** | `board-chair`, `financial-analyst` | Must match generated filenames |
| OpenCode `@agent-name` resolution | **hyphens** | `@board-chair` | Looks for `board-chair.md` |

### Why Hyphens?

- **All layers use hyphens** per CEO Directive (2026-07-24). Underscores are deprecated.
- **Generated files** use hyphens because OpenCode resolves `@agent-name` by looking for `agent-name.md` in `.opencode/agents/`.
- **Config references** must use hyphens to match the filenames that OpenCode will actually find.

### The Conversion Rule

```
Registry ID:  board_chair
              ↓  (underscores → hyphens)
Filename:     board-chair.md
Config ref:   board-chair
```

### Validation

Run `ai-company validate` to check all config references resolve to generated agent files. The validator:

1. Loads the registry and generates all agent filenames
2. Scans every YAML config for agent references
3. Checks each reference resolves to an existing `.opencode/agents/*.md` file
4. Reports mismatches with file path and line number

## 3 Data Flow

```
config/*.yaml (19 files)
        │
        ▼
  RegistryLoader (registry/loader.py)
        │
        ▼
  RegistryParser (registry/parser.py)
        │
        ▼
  CompanyRegistry (models/models.py)
        │
        ├──► BootstrapEngine (builder/)
        │       ├──► .opencode/agents/*.md   (agent files via 12 Jinja2 templates)
        │       ├──► .opencode/config/*.yaml  (derived configs)
        │       └──► .opencode/{dirs}/        (memory, knowledge, etc.)
        │
        ├──► Executor (executor/loop.py)
        │       │
        │       ├──► MessageBus.get_pending_tasks()
        │       ├──► detect_stale_tasks() → DeadLetterQueue
        │       ├──► MemoryEngine.recall() → context injection
        │       ├──► AgentLoop.run()
        │       │       ├──► LLMClient.chat() → CostTracker.record_usage()
        │       │       ├──► ToolRunner.run_plan()
        │       │       │       └──► HITLGate (for dangerous tools)
        │       │       └──► Iteration loop (max 10)
        │       ├──► AuditWriter.log_task_status()
        │       └──► MemoryEngine.store() (episodic memory)
        │
        ├──► DecisionEngine (decision/)
        │       ├──► Approval evaluation
        │       ├──► Risk assessment
        │       └──► Decision tree navigation
        │
        ├──► WorkflowEngine (workflow/)
        │       ├──► Workflow execution
        │       ├──► Step tracking
        │       └──► SLA monitoring
        │
        └──► GraphEngine (graph/)
                ├──► Org chart
                ├──► Decision graph
                ├──► Workflow graph
                └──► Knowledge graph
```

## 4 Key Entry Points

| Entry Point | File | Purpose |
|-------------|------|---------|
| CLI | `cli/main.py:app` | Typer app, 24 subcommands |
| Config Loader | `config/__init__.py:load_config()` | YAML → CompanyRegistry |
| Registry | `registry/__init__.py:load_registry()` | Load + parse + resolve + validate |
| Bootstrap | `builder/__init__.py:BootstrapEngine` | Full company generation |
| Generator | `generator.py:AgentGenerator` | Registry → .md files |
| Executor | `executor/loop.py:Executor` | Task polling + AgentLoop execution |
| AgentLoop | `executor/agent_loop.py:AgentLoop` | ReAct pattern, multi-turn LLM↔tool |
| Decision | `decision/engine.py:DecisionEngine` | Approval/risk/tree evaluation |
| Workflow | `workflow/engine.py:WorkflowEngine` | Workflow execution engine |
| Memory | `memory/engine.py:MemoryStore` | 6-type memory persistence |
| Graph | `graph/engine.py:GraphEngine` | 4-type graph construction |
| Audit | `audit/writer.py:AuditWriter` | JSONL audit trail |
| Dashboard | `dashboard/app.py:app` | FastAPI REST API |
| KPIs | `dashboard/kpis/__init__.py:collect_all_kpis()` | 7-department KPI collection |

## 5 External Dependencies

| Package | Purpose |
|---------|---------|
| typer | CLI framework |
| pydantic | Data models (17+ types) |
| pyyaml | YAML config parsing |
| jinja2 | Template rendering (12 templates) |
| rich | CLI output formatting |
| fastapi | Dashboard REST API |
| uvicorn | ASGI server for dashboard |
| httpx | HTTP client for LLM providers |
| networkx | Graph algorithms (optional) |

## 6 Test Structure

```
tests/
├── unit/                          # 27 unit test files
│   ├── test_models.py             # Pydantic model tests
│   ├── test_executor.py           # Executor + AgentLoop tests
│   ├── test_agent_loop.py         # AgentLoop unit tests
│   ├── test_audit.py              # Audit trail tests
│   ├── test_memory.py             # Memory engine tests
│   ├── test_decision.py           # Decision engine tests
│   ├── test_workflow.py           # Workflow engine tests
│   ├── test_graph.py              # Graph engine tests
│   ├── test_dashboard.py          # Dashboard API tests
│   ├── test_dashboard_ws.py       # WebSocket tests
│   ├── test_dashboard_security.py # CORS + auth tests
│   ├── test_kpi_collectors.py     # KPI collector tests
│   ├── test_bootstrap.py          # BootstrapEngine tests
│   ├── test_generator.py          # Generator tests
│   ├── test_registry.py           # Registry system tests
│   ├── test_llm.py                # LLM client tests
│   ├── test_model_router.py       # Model routing tests
│   ├── test_orchestrator.py       # Orchestrator tests
│   ├── test_doctor.py             # Diagnostics tests
│   ├── test_dead_letter.py        # Dead-letter queue tests
│   ├── test_approval_prompts.py   # Approval prompt tests
│   └── test_security.py           # Security tests (collection error — skip)
├── integration/                   # Integration tests
│   └── test_pipeline.py           # Memory, graph, scheduler, KPI integration
├── test_audit_integration.py      # Audit integration tests
├── test_memory_integration.py     # Memory integration tests
├── test_kpi_analytics.py          # KPI analytics tests
├── test_scheduler_integration.py  # Scheduler integration tests
├── test_llm_streaming.py          # LLM streaming tests
└── test_release.py                # Release validation tests
```

**Total: 962 tests collected** (2 collection errors in test_security.py and test_ml.py — skip with `--ignore`)
