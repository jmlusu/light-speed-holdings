# AI Company Builder — Project Structure

> **Authority Level**: Layer 6 — derived from [02-ARCHITECTURE.md](02-ARCHITECTURE.md)
> **Last Updated**: 2026-07-16

---

## 1 Purpose

This document provides the complete reference for the AI Company Builder repository structure. Every directory, every package, every module has a defined purpose. This document is the authoritative map of the codebase.

---

## 2 Scope

This document covers:

- Complete folder tree with purpose annotations
- Package responsibilities
- Module responsibilities
- Naming standards
- Generated vs. manual code distinction
- Extensibility rules

---

## 3 Complete Folder Tree

```
ai-company/                              # Project root
│
├── .ai-company/                         # CONSTITUTION & GOVERNANCE
│   ├── constitution/                    # 16 governance documents
│   │   ├── 00-CONSTITUTION.md           # Supreme authority
│   │   ├── 01-MISSION.md               # Vision & strategy
│   │   ├── 02-ARCHITECTURE.md           # Architecture guide
│   │   ├── 03-ENGINEERING-STANDARDS.md  # Engineering practices
│   │   ├── 04-CODING-STANDARDS.md       # Code conventions
│   │   ├── 05-PROJECT-STRUCTURE.md      # This document
│   │   ├── 06-GENERATOR-STANDARDS.md    # Generator rules
│   │   ├── 07-PROMPT-STANDARDS.md       # Prompt templates
│   │   ├── 08-TESTING-STANDARDS.md      # Testing practices
│   │   ├── 09-CODE-REVIEW.md            # Review checklists
│   │   ├── 10-DEFINITION-OF-DONE.md     # Completion criteria
│   │   ├── 11-GIT-STANDARDS.md          # Git workflow
│   │   ├── 12-DOCUMENTATION-STANDARDS.md # Documentation rules
│   │   ├── 13-SECURITY-STANDARDS.md     # Security practices
│   │   ├── 14-DESIGN-PRINCIPLES.md      # Design philosophy
│   │   ├── 15-AI-COMPANY-VISION.md      # 10-year vision
│   │   └── bootstrap.md                 # Session startup guide
│   ├── state/                           # Live project state
│   │   ├── PROJECT_STATUS.md
│   │   ├── CURRENT_SPRINT.md
│   │   ├── ROADMAP.md
│   │   ├── CHANGELOG.md
│   │   ├── TECH_DEBT.md
│   │   ├── DECISIONS.md
│   │   ├── NEXT_ACTIONS.md
│   │   ├── RELEASE_PLAN.md
│   │   ├── MILESTONES.md
│   │   └── RISKS.md
│   ├── templates/                       # (empty — generator output target)
│   ├── examples/                        # (empty — populated with examples)
│   ├── diagrams/                        # (empty — Mermaid diagram sources)
│   └── reviews/                         # (empty — code review records)
│
├── .opencode/                           # GENERATED OUTPUT (do not edit)
│   ├── agents/                          # 31 generated agent .md files
│   │   ├── ceo.md                       # (generated from config)
│   │   ├── cto.md                       # (generated from config)
│   │   ├── lead_backend.md              # (generated from config)
│   │   └── ...                          # (31 total)
│   ├── inbox.json                       # Task queue
│   └── daily_briefing.md                # Generated briefing
│
├── config/                              # YAML CONFIGURATION (SOURCE OF TRUTH)
│   ├── company/                         # Company-level config (8 files)
│   │   ├── company.yaml                 # Company identity & structure
│   │   ├── vision.yaml                  # Vision & goals
│   │   ├── strategy.yaml                # Strategic pillars & KPIs
│   │   ├── culture.yaml                 # Values & communication
│   │   ├── governance.yaml              # Decision rights & escalation
│   │   ├── policies.yaml                # Organizational policies
│   │   ├── kpis.yaml                    # Performance metrics
│   │   └── budget.yaml                  # Financial allocation
│   ├── board/                           # Board governance (4 files)
│   │   ├── board.yaml                   # Board members
│   │   ├── committees.yaml              # Committee structure
│   │   ├── meetings.yaml                # Meeting schedule
│   │   └── voting.yaml                  # Voting rules
│   ├── executives/                      # Executive hierarchy (1 file)
│   │   └── executives.yaml              # 12 executive roles
│   ├── departments/                     # Department structure (1 file)
│   │   └── departments.yaml             # 12 departments
│   ├── agents/                          # Specialist agents (1 file)
│   │   └── specialists.yaml             # 17 specialist roles
│   ├── decision/                        # Decision framework (3 files)
│   │   ├── approval_matrix.yaml         # Who approves what
│   │   ├── risk_matrix.yaml             # Risk level definitions
│   │   └── decision_tree.yaml           # Decision navigation
│   ├── workflows/                       # Process definitions (1 file)
│   │   └── workflows.yaml               # 9 workflow definitions
│   └── routing.yaml                     # LLM model routing
│
├── templates/                           # JINJA2 TEMPLATES (7 active)
│   ├── base.md.j2                       # Base template (block inheritance)
│   ├── executive.md.j2                  # Executive agent (extends base)
│   ├── department.md.j2                 # Department agent (extends base)
│   ├── specialist_v2.md.j2             # Specialist agent (extends base)
│   ├── board_v2.md.j2                  # Board member (extends base)
│   ├── workflow.md.j2                   # Workflow definition (standalone)
│   ├── config.md.j2                     # Config generator (standalone)
│   ├── agents/                          # Legacy agent templates
│   ├── agent.md.j2                      # Legacy single agent template
│   ├── board.md.j2                      # Legacy board template
│   └── specialist.md.j2                 # Legacy specialist template
│
├── src/ai_company/                      # PYTHON SOURCE (APPLICATION CODE)
│   ├── __init__.py                      # Package init
│   │
│   ├── cli/                             # CLI LAYER (22 subcommands)
│   │   ├── __init__.py
│   │   ├── main.py                      # Typer app entry, registers all subcommands
│   │   ├── company.py                   # company run/status (BootstrapEngine CLI)
│   │   ├── decision.py                  # decision evaluate/matrix/tree
│   │   ├── graph.py                     # graph list/show/path
│   │   ├── workflows.py                 # workflows list/run/status/advance
│   │   ├── memory.py                    # memory list/add/search/consolidate
│   │   ├── agents.py                    # agent management
│   │   ├── board.py                     # board of directors
│   │   ├── departments.py               # department management
│   │   ├── executives.py                # executive management
│   │   ├── specialists.py               # specialist management
│   │   ├── orchestrator.py              # autonomous coordination
│   │   ├── doctor.py                    # system diagnostics
│   │   ├── dashboard.py                 # CEO dashboard
│   │   ├── executor.py                  # autonomous execution
│   │   ├── models.py                    # LLM model selection
│   │   ├── marketing.py                 # marketing operations
│   │   ├── sales.py                     # sales operations
│   │   ├── customer_success.py          # customer success
│   │   ├── legal.py                     # legal operations
│   │   └── hr.py                        # HR operations
│   │
│   ├── models/                          # DOMAIN MODELS (17+ Pydantic)
│   │   ├── __init__.py                  # Public API re-exports
│   │   ├── models.py                    # All domain models (~560 lines)
│   │   └── task.py                      # Task re-exports (backward compat)
│   │
│   ├── config/                          # CONFIGURATION LAYER
│   │   └── __init__.py                  # load_config() → CompanyRegistry
│   │
│   ├── registry/                        # REGISTRY SYSTEM (4 modules)
│   │   ├── __init__.py                  # load_registry() entry point
│   │   ├── loader.py                    # YAML file loading (FILE_MAP)
│   │   ├── parser.py                    # Raw dicts → typed models
│   │   ├── resolver.py                  # Cross-reference validation
│   │   └── validator.py                 # Structural validation (7 checks)
│   │
│   ├── builder/                         # BOOTSTRAP ENGINE
│   │   └── __init__.py                  # BootstrapEngine (dirs, agents, configs)
│   │
│   ├── decision/                        # DECISION ENGINE
│   │   └── engine.py                    # DecisionEngine (approvals, risk, trees)
│   │
│   ├── workflow/                        # WORKFLOW ENGINE
│   │   └── engine.py                    # WorkflowEngine + WorkflowInstance
│   │
│   ├── memory/                          # MEMORY ENGINE
│   │   └── engine.py                    # MemoryEntry + MemoryStore (6 types)
│   │
│   ├── graph/                           # GRAPH ENGINE
│   │   └── engine.py                    # Graph + GraphEngine (4 types, BFS)
│   │
│   ├── orchestrator/                    # TASK ORCHESTRATION
│   │   ├── message_bus.py               # JSON-based task queue
│   │   ├── briefing.py                  # Daily executive briefings
│   │   ├── scheduler.py                 # Task scheduling
│   │   ├── escalation.py                # Escalation rules
│   │   └── approval.py                  # Human approval gates
│   │
│   ├── llm/                             # LLM PROVIDERS
│   │   ├── client.py                    # LLM client
│   │   └── providers/                   # Provider implementations
│   │       ├── base.py                  # Base provider interface
│   │       ├── openai_compatible.py     # OpenAI-compatible provider
│   │       └── ollama.py                # Ollama provider
│   │
│   ├── executor/                        # TASK EXECUTION
│   │   ├── loop.py                      # Main execution loop
│   │   ├── tool_runner.py               # Tool execution
│   │   ├── hitl_gate.py                 # Human-in-the-loop gates
│   │   └── context.py                   # Execution context
│   │
│   ├── doctor/                          # SYSTEM DIAGNOSTICS
│   │   ├── doctor.py                    # Doctor commands
│   │   ├── checks.py                    # Health checks
│   │   └── report.py                    # Diagnostic reports
│   │
│   ├── dashboard/                       # CEO DASHBOARD
│   │   └── api.py                       # FastAPI endpoints
│   │
│   ├── generator.py                     # AGENT FILE GENERATION
│   ├── model_router.py                  # LLM MODEL ROUTING
│   ├── utils.py                         # SHARED UTILITIES
│   ├── builder.py                       # Legacy builder
│   ├── cli.py                           # Legacy CLI
│   ├── config.py                        # Legacy config
│   ├── generator/                       # Legacy generator package
│   ├── graph.py                         # Legacy graph
│   ├── registry.py                      # Legacy registry
│   ├── templates/                       # Legacy templates
│   └── validator.py                     # Legacy validator
│
├── tests/                               # TEST SUITE (175 tests)
│   ├── unit/                            # Unit tests
│   │   ├── test_models.py               # 16 model tests
│   │   ├── test_registry.py             # 18 registry tests
│   │   ├── test_bootstrap.py            # 7 bootstrap tests
│   │   ├── test_decision.py             # 11 decision tests
│   │   ├── test_workflow.py             # 12 workflow tests
│   │   ├── test_memory.py               # 11 memory tests
│   │   ├── test_graph.py                # 14 graph tests
│   │   ├── test_generator.py            # 5 generator tests
│   │   ├── test_dashboard.py            # Dashboard tests
│   │   ├── test_executor.py             # Executor tests
│   │   ├── test_llm.py                  # LLM tests
│   │   ├── test_model_router.py         # Router tests
│   │   └── test_orchestrator.py         # Orchestrator tests
│   └── integration/                     # Integration tests
│
├── harness/                             # ECL CHANGE LIFECYCLE
│   ├── changes/                         # Change tracking
│   │   ├── active/                      # Currently active change
│   │   ├── archive/                     # Completed changes
│   │   ├── parking/                     # Parked changes
│   │   └── INDEX.json                   # Generated index
│   ├── evolution/                       # Auto-evolution tracking
│   │   └── pending.md                   # Pending evolution items
│   └── templates/                       # Change templates
│
├── scripts/                             # POWERSHELL SCRIPTS
│   ├── harness-change.ps1               # Change lifecycle management
│   ├── harness-evolve.ps1               # Auto-evolution checker
│   └── lint-ecl.ps1                     # ECL structure validator
│
├── docs/                                # DOCUMENTATION
│   ├── ARCHITECTURE.md                  # Quick-reference architecture
│   ├── STATUS.md                        # Current project status
│   ├── ECL.md                           # Change lifecycle guide
│   ├── COMPANY-CONSTITUTION.md          # Legacy constitution
│   ├── DECISION-FRAMEWORK.md            # Decision framework
│   ├── ORGANIZATION.md                  # Organization chart
│   └── standards/                       # Standards documents
│       └── AGENT-SPECIFICATION.md       # Agent format spec
│
├── .github/workflows/                   # CI/CD
│   └── ci.yml                           # ruff, mypy, pytest, harness lint
│
├── AGENTS.md                            # Agent operating guide
├── pyproject.toml                       # Project metadata & dependencies
├── company-registry.yaml                # Legacy registry
├── *.py                                 # Legacy setup scripts
│
├── agents/                              # LEGACY (ignore)
├── board/                               # LEGACY (ignore)
├── company/                             # LEGACY (ignore)
├── departments/                         # LEGACY (ignore)
├── executives/                          # LEGACY (ignore)
├── specialists/                         # LEGACY (ignore)
├── generated/                           # LEGACY (ignore)
├── knowledge/                           # Knowledge base
├── logs/                                # Application logs
├── memory/                              # Memory storage
├── projects/                            # Project tracking
├── prompts/                             # Prompt templates
├── reports/                             # Generated reports
├── tools/                               # Tool definitions
├── workflows/                           # Workflow definitions
└── static/                              # Static assets
```

---

## 4 Package Responsibilities

### 4.1 Core Packages

| Package | Responsibility | Public API |
|---------|---------------|-----------|
| `cli/` | User interface (22 commands) | `app` (Typer) |
| `models/` | Domain model definitions | All Pydantic models |
| `config/` | Configuration loading | `load_config()` |
| `registry/` | Registry parsing & validation | `load_registry()` |
| `builder/` | Full company bootstrap | `BootstrapEngine` |
| `decision/` | Decision evaluation | `DecisionEngine` |
| `workflow/` | Workflow execution | `WorkflowEngine` |
| `memory/` | Memory storage & recall | `MemoryStore` |
| `graph/` | Graph construction & analysis | `GraphEngine` |
| `orchestrator/` | Task orchestration | MessageBus, Scheduler |
| `llm/` | LLM provider abstraction | `LLMClient` |
| `executor/` | Task execution loop | `ExecutionLoop` |

### 4.2 Support Packages

| Package | Responsibility | Public API |
|---------|---------------|-----------|
| `doctor/` | System health checks | `run_checks()` |
| `dashboard/` | CEO web dashboard | FastAPI app |
| `generator/` | Agent generation (legacy) | `AgentGenerator` |

---

## 5 Naming Standards

### 5.1 Files

| Type | Convention | Example |
|------|-----------|---------|
| Python module | `snake_case.py` | `engine.py` |
| Python package | `snake_case/` | `decision/` |
| YAML config | `snake_case.yaml` | `approval_matrix.yaml` |
| Jinja2 template | `snake_case.md.j2` | `executive.md.j2` |
| Test file | `test_*.py` | `test_decision.py` |
| PowerShell script | `kebab-case.ps1` | `harness-change.ps1` |

### 5.2 Directories

| Type | Convention | Example |
|------|-----------|---------|
| Source package | `snake_case/` | `ai_company/` |
| Config category | `lowercase/` | `company/`, `board/` |
| Generated output | `lowercase/` | `agents/`, `config/` |
| Tests | `lowercase/` | `unit/`, `integration/` |

---

## 6 Generated vs. Manual Code

### 6.1 Generated (Do Not Edit)

| Location | Generator | Regenerate Command |
|----------|-----------|-------------------|
| `.opencode/agents/*.md` | `generator.py` | `python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` |
| `.opencode/config/*.yaml` | `builder/__init__.py` | `ai-company company run` |
| `harness/changes/INDEX.json` | `harness-change.ps1` | `.\scripts\harness-change.ps1 reindex` |

### 6.2 Manual (Edit Freely)

| Location | Purpose |
|----------|---------|
| `src/ai_company/` | Application source code |
| `config/` | YAML configuration |
| `templates/` | Jinja2 templates |
| `tests/` | Test suite |
| `docs/` | Documentation |
| `.ai-company/` | Governance documents |

### 6.3 Boundary Rule

**Never edit generated output. Always edit the source and regenerate.**

---

## 7 Extensibility Rules

### 7.1 Adding a New CLI Command

1. Create `src/ai_company/cli/new_command.py`
2. Define Typer app: `app = typer.Typer()`
3. Add commands: `@app.command()`
4. Register in `cli/main.py`: `app.add_typer(new_command.app, name="new-command")`
5. Add tests in `tests/unit/test_new_command.py`

### 7.2 Adding a New Engine

1. Create `src/ai_company/new_engine/__init__.py`
2. Implement engine class
3. Add CLI commands in `cli/new_engine.py`
4. Register in `cli/main.py`
5. Add tests in `tests/unit/test_new_engine.py`
6. Update this document

### 7.3 Adding a New Config File

1. Add YAML file to `config/<category>/`
2. Add model to `models/models.py`
3. Add loader entry to `registry/loader.py` (FILE_MAP)
4. Add parser logic to `registry/parser.py`
5. Add to CompanyRegistry if needed
6. Regenerate: `ai-company company run`

### 7.4 Adding a New Template

1. Create `templates/new_type.md.j2`
2. Extend `base.md.j2` if appropriate: `{% extends "base.md.j2" %}`
3. Add to `_TEMPLATE_MAP` in `generator.py`
4. Test generation
5. Update this document

---

## 8 Future Enhancements

- Automated structure validation (CI check that docs match code)
- Module dependency graph generation
- Dead code detection and removal
- Structure documentation auto-generation from source
- Package-level `__all__` enforcement

---

## 9 References

| Document | Relationship |
|----------|-------------|
| [00-CONSTITUTION.md](00-CONSTITUTION.md) | Supreme authority |
| [02-ARCHITECTURE.md](02-ARCHITECTURE.md) | Architecture guide |
| [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) | Quick-reference architecture |
| [03-ENGINEERING-STANDARDS.md](03-ENGINEERING-STANDARDS.md) | Engineering standards |
