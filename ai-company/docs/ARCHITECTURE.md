# Architecture

## 1 Module Hierarchy

```
src/ai_company/
├── cli/                        # Typer CLI commands (22 subcommands)
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
│   ├── orchestrator.py         # Autonomous coordination
│   ├── doctor.py               # System diagnostics
│   ├── dashboard.py            # CEO dashboard
│   ├── executor.py             # Autonomous task execution
│   ├── models.py               # LLM model selection
│   ├── marketing.py            # Marketing operations
│   ├── sales.py                # Sales operations
│   ├── customer_success.py     # Customer success operations
│   ├── legal.py                # Legal operations
│   └── hr.py                   # HR operations
├── models/                     # Pydantic domain models (17+)
│   ├── models.py               # All domain models (Company, Executive, etc.)
│   ├── task.py                 # Task re-exports (backward compat)
│   └── __init__.py             # Public API re-exports
├── config/                     # Config loader (19 YAML files → CompanyRegistry)
│   └── __init__.py             # load_config() function
├── registry/                   # Registry system
│   ├── __init__.py             # load_registry() entry point
│   ├── loader.py               # YAML file loading
│   ├── parser.py               # Raw dicts → typed models
│   ├── resolver.py             # Cross-reference resolution
│   └── validator.py            # Structural validation
├── builder/                    # Bootstrap engine
│   └── __init__.py             # BootstrapEngine — full company generation
├── decision/                   # Decision engine
│   └── engine.py               # DecisionEngine — approvals, risk, trees
├── workflow/                   # Workflow engine
│   └── engine.py               # WorkflowEngine — step tracking, SLA
├── memory/                     # Memory engine
│   └── engine.py               # MemoryStore — 6 types, persistence
├── graph/                      # Graph engine
│   └── engine.py               # GraphEngine — 4 graph types, pathfinding
├── orchestrator/               # Task orchestration
│   ├── message_bus.py          # JSON-based task queue
│   ├── briefing.py             # Daily executive briefings
│   ├── scheduler.py            # Task scheduling
│   ├── escalation.py           # Escalation rules
│   └── approval.py             # Human approval gates
├── llm/                        # LLM providers
│   ├── client.py               # LLM client
│   └── providers/              # OpenAI, Ollama providers
├── executor/                   # Task execution loop
│   ├── loop.py                 # Main execution loop
│   ├── tool_runner.py          # Tool execution
│   ├── hitl_gate.py            # Human-in-the-loop gates
│   └── context.py              # Execution context
├── doctor/                     # System diagnostics
├── dashboard/                  # CEO dashboard
├── generator.py                # Agent .md file generation
├── model_router.py             # LLM model selection by agent/context
└── utils.py                    # Shared utilities
```

## 2 Data Flow

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
        │       ├──► .opencode/agents/*.md   (agent files via templates)
        │       ├──► .opencode/config/*.yaml  (derived configs)
        │       └──► .opencode/{dirs}/        (memory, knowledge, etc.)
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
        ├──► MemoryEngine (memory/)
        │       ├──► 6-type memory store
        │       └──► Consolidation
        │
        └──► GraphEngine (graph/)
                ├──► Org chart
                ├──► Decision graph
                ├──► Workflow graph
                └──► Knowledge graph
```

## 3 Key Entry Points

| Entry Point | File | Purpose |
|-------------|------|---------|
| CLI | `cli/main.py:app` | Typer app, 22 subcommands |
| Config Loader | `config/__init__.py:load_config()` | YAML → CompanyRegistry |
| Registry | `registry/__init__.py:load_registry()` | Load + parse + resolve + validate |
| Bootstrap | `builder/__init__.py:BootstrapEngine` | Full company generation |
| Generator | `generator.py:AgentGenerator` | Registry → .md files |
| Decision | `decision/engine.py:DecisionEngine` | Approval/risk/tree evaluation |
| Workflow | `workflow/engine.py:WorkflowEngine` | Workflow execution engine |
| Memory | `memory/engine.py:MemoryStore` | 6-type memory persistence |
| Graph | `graph/engine.py:GraphEngine` | 4-type graph construction |

## 4 External Dependencies

| Package | Purpose |
|---------|---------|
| typer | CLI framework |
| pydantic | Data models (17+ types) |
| pyyaml | YAML config parsing |
| jinja2 | Template rendering (7 templates) |
| rich | CLI output formatting |
| networkx | Graph algorithms (optional) |
