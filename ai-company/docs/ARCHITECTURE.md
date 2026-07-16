# Architecture

## 1 Module Hierarchy

```
src/ai_company/
├── cli/                    # Typer CLI commands (one module per subcommand)
│   ├── main.py             # App entry point, registers all subcommands
│   ├── agents.py           # Agent management commands
│   ├── board.py            # Board of directors commands
│   ├── departments.py      # Department management
│   ├── executives.py       # Executive management
│   ├── specialists.py      # Specialist agent management
│   ├── orchestrator.py     # Autonomous coordination
│   ├── doctor.py           # System diagnostics
│   ├── workflows.py        # Workflow management
│   ├── memory.py           # Company memory
│   ├── marketing.py        # Marketing operations
│   ├── sales.py            # Sales operations
│   ├── customer_success.py # Customer success operations
│   ├── legal.py            # Legal operations
│   ├── hr.py               # HR operations
│   └── models.py           # LLM model selection CLI
├── models/                 # Pydantic domain models
│   ├── models.py           # Executive, Specialist, Department, Company
│   ├── task.py             # Task model with status/priority enums
│   └── ...                 # Board, Department, Workflow, etc.
├── orchestrator/           # Task orchestration subsystem
│   ├── message_bus.py      # JSON-based task queue
│   ├── briefing.py         # Daily executive briefings
│   ├── scheduler.py        # Task scheduling
│   ├── escalation.py       # Escalation rules
│   └── approval.py         # Human approval gates
├── doctor/                 # System diagnostics
│   ├── checks.py           # Health check implementations
│   ├── report.py           # Report generation
│   └── doctor.py           # Doctor orchestration
├── generator.py            # Registry → agent .md file generation
├── model_router.py         # LLM model selection by agent/context
├── config.py               # Project configuration
├── registry.py             # Agent registry loading
├── graph.py                # Org chart graph (networkx)
├── validator.py            # Validation utilities
└── utils.py                # Shared utilities
```

## 2 Data Flow

```
company-registry.yaml
        │
        ▼
  AgentGenerator (generator.py)
        │
        ├─► .opencode/agents/*.md   (OpenCode agent files)
        │
        └─► company/*.yaml          (derived YAML files)
```

## 3 Key Entry Points

| Entry Point | File | Purpose |
|-------------|------|---------|
| CLI | `src/ai_company/cli/main.py:app` | Typer app, all 17 subcommands |
| Generator | `src/ai_company/generator.py:AgentGenerator` | Registry → .md files |
| Task Queue | `src/ai_company/orchestrator/message_bus.py` | JSON task queue |
| Model Router | `src/ai_company/model_router.py:ModelRouter` | Agent → LLM model selection |

## 4 External Dependencies

| Package | Purpose |
|---------|---------|
| typer | CLI framework |
| pydantic | Data models |
| pyyaml | YAML registry parsing |
| jinja2 | Template rendering |
| networkx | Org chart graph |
| rich | CLI output formatting |
