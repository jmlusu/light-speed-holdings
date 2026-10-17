# AI Company Builder — Design Principles

> **Authority Level**: Layer 2 — derived from [00-CONSTITUTION.md](00-CONSTITUTION.md)
> **Last Updated**: 2026-07-16

---

## 1 Purpose

This document defines the foundational design principles that guide every architectural decision, code structure, and system design in AI Company Builder. These principles are not aspirational — they are enforced through code review, testing, and CI.

---

## 2 Scope

This document governs:

- System architecture decisions
- Module design and boundaries
- API design and contracts
- Data model design
- Configuration schema design
- Template structure
- Test architecture

---

## 3 Domain-Driven Design (DDD)

### 3.1 Principle

The codebase is organized around the business domain of AI company management, not technical layers. The domain model is the heart of the system.

### 3.2 Application

| Domain Concept | Code Location | Model |
|----------------|---------------|-------|
| Organization | `models/models.py` | `Company`, `CompanyStructure` |
| People | `models/models.py` | `Executive`, `Department`, `Agent`, `BoardMember` |
| Work | `workflow/engine.py` | `Workflow`, `WorkflowStep`, `WorkflowInstance` |
| Decisions | `decision/engine.py` | `ApprovalEntry`, `RiskLevel`, `DecisionNode` |
| Knowledge | `memory/engine.py` | `MemoryEntry`, `MemoryStore` |
| Relationships | `graph/engine.py` | `Graph`, `GraphNode`, `GraphEdge` |
| Configuration | `registry/` | `CompanyRegistry` (parsed from 19 YAML files) |

### 3.3 Bounded Contexts

Each engine operates within a bounded context:

```
Configuration Context:  config/ → registry/ → CompanyRegistry
Generation Context:     CompanyRegistry → generator/ → .opencode/agents/*.md
Decision Context:       CompanyRegistry → decision/engine.py → Action/Risk
Workflow Context:       CompanyRegistry → workflow/engine.py → Step/Task
Memory Context:         memory/engine.py → MemoryStore (6 types)
Graph Context:          graph/engine.py → Graph (4 types)
Bootstrap Context:      CompanyRegistry → builder/ → Full company scaffold
```

Cross-context communication happens through the `CompanyRegistry` model — the shared domain object.

### 3.4 Tradeoffs

- **Chosen**: Monolithic domain model in `models/models.py` for simplicity
- **Deferred**: Splitting into separate domain packages when the model exceeds ~30 types
- **Risk**: `models/models.py` grows unwieldy. Mitigation: current 17+ types are manageable; monitor file length

---

## 4 Clean Architecture

### 4.1 Principle

Dependencies point inward. The domain model has no dependencies on infrastructure. Engines depend on the domain model, not on CLI or I/O.

### 4.2 Layer Structure

```
┌─────────────────────────────────────┐
│           CLI Layer (I/O)           │  typer, rich, click
├─────────────────────────────────────┤
│          Engine Layer               │  DecisionEngine, WorkflowEngine, etc.
├─────────────────────────────────────┤
│         Domain Model                │  Pydantic models (no deps)
├─────────────────────────────────────┤
│      Configuration Layer            │  YAML parsing, registry loading
└─────────────────────────────────────┘
```

### 4.3 Dependency Rules

| Layer | May Depend On | May NOT Depend On |
|-------|--------------|-------------------|
| CLI | Engines, Domain, Config | Infrastructure, External APIs |
| Engines | Domain, Config | CLI, Infrastructure |
| Domain | Nothing (pure Pydantic) | CLI, Engines, Config, Infrastructure |
| Config | Domain | CLI, Engines, Infrastructure |

### 4.4 Current Compliance

| Module | Follows Clean Arch? | Notes |
|--------|-------------------|-------|
| `models/models.py` | Yes | Pure Pydantic, no external deps |
| `decision/engine.py` | Yes | Depends only on models |
| `workflow/engine.py` | Yes | Depends only on models |
| `memory/engine.py` | Partially | File I/O for persistence |
| `graph/engine.py` | Yes | Depends only on models |
| `registry/` | Yes | Parses YAML → models |
| `cli/*.py` | Yes | Depends on engines + registry |
| `llm/client.py` | Violates | Has import ordering issues |

### 4.5 Tradeoffs

- **Chosen**: Simple layering over strict hexagonal architecture
- **Accepted**: `memory/engine.py` does file I/O directly (acceptable for current scale)
- **Deferred**: Ports-and-adapters pattern for memory/graph persistence when multiple storage backends are needed

---

## 5 Hexagonal Architecture (Ports and Adapters)

### 5.1 Principle

Core business logic defines ports (interfaces). Infrastructure implements adapters. This allows swapping implementations without changing business logic.

### 5.2 Current Application

| Port (Interface) | Adapter (Implementation) | Swappable? |
|-------------------|-------------------------|------------|
| YAML Config | `registry/loader.py` | Yes — could load from DB, API |
| Agent Generation | `generator.py` + Jinja2 | Yes — could generate other formats |
| Memory Storage | JSON file in `memory/engine.py` | Partially — needs interface extraction |
| Graph Storage | In-memory in `graph/engine.py` | Yes — could persist to Neo4j |
| LLM Providers | `llm/providers/` | Yes — OpenAI, Ollama already |

### 5.3 Tradeoffs

- **Chosen**: Pragmatic hexagonal — ports where it matters (LLM, storage), simple functions elsewhere
- **Deferred**: Full port/adapter extraction for memory and graph until multiple backends are needed
- **Risk**: Tight coupling in `memory/engine.py`. Mitigation: JSON persistence is acceptable for v1

---

## 6 Infrastructure as Code (IaC)

### 6.1 Principle

The entire AI organization is defined as code. Configuration IS the infrastructure. There is no distinction between "configuring" a company and "building" one.

### 6.2 Application

| IaC Concept | AI Company Builder Implementation |
|-------------|-----------------------------------|
| Source of truth | 19 YAML config files in `config/` |
| Template engine | 7 Jinja2 templates in `templates/` |
| Code generation | `generator.py` → `.opencode/agents/*.md` |
| State management | JSON files in `.opencode/` |
| Idempotent operations | Bootstrap regenerates from config |
| Version control | Git tracks all config + code changes |
| Testing | pytest validates generation + engines |

### 6.3 Configuration First

Every organizational decision starts with configuration:

```
Want a new agent?     → Edit config/agents/specialists.yaml
Want a new workflow?   → Edit config/workflows/workflows.yaml
Want a new policy?     → Edit config/company/policies.yaml
Want a new board seat?  → Edit config/board/board.yaml
Want a new department?  → Edit config/departments/departments.yaml
```

Then regenerate. Never edit generated output.

---

## 7 Plugin Architecture

### 7.1 Principle

The system should be extensible through well-defined interfaces. New engines, new agent types, new templates, and new CLI commands should be addable without modifying existing code.

### 7.2 Extension Points

| Extension Point | Mechanism | Current Status |
|-----------------|-----------|----------------|
| Agent types | `_TEMPLATE_MAP` in `generator.py` | Working — 5 types |
| CLI commands | Typer subcommand registration in `cli/main.py` | Working — 22 commands |
| Memory types | `MemoryStore._stores` dict keys | Working — 6 types |
| Graph types | `GraphEngine._builders` dict | Working — 4 types |
| LLM providers | `llm/providers/` directory | Working — 2 providers |
| Decision rules | `DecisionEngine.evaluate_action()` | Working — matrix + tree |
| Workflow steps | `WorkflowInstance.steps` list | Working — 9 workflows |

### 7.3 Tradeoffs

- **Chosen**: Dictionary-based dispatch over formal plugin interfaces
- **Accepted**: Adding new types requires editing source code (acceptable for current scale)
- **Deferred**: Dynamic plugin loading from external packages when third-party extensions are needed

---

## 8 Composition Over Inheritance

### 8.1 Principle

Prefer composing small, focused functions and objects over creating deep inheritance hierarchies.

### 8.2 Application

| Pattern Used | Example |
|-------------|---------|
| Function composition | `load_config()` = `load_raw()` → `parse()` → `resolve()` → `validate()` |
| Object composition | `CompanyRegistry` composes Executive, Department, Agent, etc. |
| Engine composition | CLI commands compose registry loading + engine methods |
| Template inheritance | Jinja2 templates extend `base.md.j2` |

### 8.3 Anti-Patterns Avoided

- No deep class hierarchies (all models inherit from Pydantic `BaseModel`)
- No God objects (engines are focused: decision, workflow, memory, graph)
- No circular imports (clean dependency direction)

---

## 9 Declarative Design

### 9.1 Principle

Declare WHAT should exist, not HOW to create it. The system figures out the HOW.

### 9.2 Application

| Declarative | Imperative (Avoided) |
|-------------|---------------------|
| `config/agents/specialists.yaml` defines agents | Manually writing `.md` agent files |
| `config/workflows/workflows.yaml` defines workflows | Hardcoding workflow logic |
| `config/decision/approval_matrix.yaml` defines rules | Writing if/else chains for approvals |
| `templates/specialist_v2.md.j2` defines agent format | Manually formatting each agent |

### 9.3 Benefits

- Configuration changes propagate automatically
- Regeneration produces consistent output
- Version control captures intent, not implementation
- Testing validates the declaration, not the process

---

## 10 AI-Native Design

### 10.1 Principle

The system is designed for AI agents as first-class citizens, not retrofitted with AI capabilities.

### 10.2 Application

| Design Choice | Rationale |
|---------------|-----------|
| Markdown agent files | AI-native format, human-readable, version-controllable |
| YAML configuration | Machine-parseable, human-readable, diffable |
| Structured memory types | AI agents need categorized recall, not flat storage |
| Knowledge graphs | AI agents benefit from relationship-aware context |
| Decision trees | AI agents need structured decision frameworks |
| Escalation rules | AI agents must know when to ask for help |

### 10.3 Tradeoffs

- **Chosen**: Markdown-based agent definitions (OpenCode-native format)
- **Accepted**: Not using formal agent frameworks (LangChain, AutoGen) — too heavy for current needs
- **Deferred**: Runtime agent communication protocol when agents need to talk to each other

---

## 11 Examples

### 11.1 Applying Design Principles to a New Feature

**Scenario**: Add a "Budget Tracker" engine.

| Principle | Application |
|-----------|-------------|
| DDD | Define `Budget`, `BudgetLine`, `BudgetPeriod` domain models |
| Clean Architecture | Engine depends on models, not CLI |
| IaC | Budget definitions in `config/company/budget.yaml` |
| Declarative | `budget.yaml` declares budgets, engine enforces them |
| Composition | `BudgetEngine` = `load_budget()` + `validate()` + `track()` |
| Plugin | Register in `cli/main.py` as new subcommand |
| AI-Native | Budget agent gets memory type for spending history |

### 11.2 Anti-Pattern Examples

| Anti-Pattern | Violation | Correct Approach |
|-------------|-----------|-----------------|
| Hardcoded budgets in engine | IaC, Declarative | Config in YAML |
| `BudgetEngine` inherits from `BaseEngine` | Composition | Compose small functions |
| Budget logic in CLI handler | Clean Architecture | Logic in engine, CLI delegates |
| No tests for budget engine | Quality Before Speed | Write tests first |
| Manual budget .md files | Generated Code is Disposable | Generate from config |

---

## 12 Best Practices

1. **Start with the domain model**: Define Pydantic models before writing engine logic.
2. **Config first**: Every organizational concept gets a YAML config file.
3. **Generate, don't manually create**: If it can be generated, generate it.
4. **One engine, one concern**: Each engine handles exactly one domain concept.
5. **Test at the boundary**: Test engines through their public API, not internals.
6. **Document decisions**: Every architectural choice gets an ADR in `state/DECISIONS.md`.
7. **Validate early**: Load config → validate → parse → use. Never skip validation.

---

## 13 Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|-----------------|
| Putting business logic in CLI handlers | Violates Clean Architecture | Put logic in engines |
| Hardcoding configuration values | Violates IaC | Put values in YAML config |
| Creating base classes for everything | Violates Composition | Compose small functions |
| Skipping validation on config load | Violates Fail Fast | Validate at load time |
| Editing generated files | Violates Source of Truth | Edit config, regenerate |
| Adding features without tests | Violates Quality Before Speed | Test first |
| Creating deep inheritance hierarchies | Violates Composition | Use flat composition |

---

## 14 Future Enhancements

- Formal port/adapter interfaces for all storage backends
- Plugin discovery mechanism for third-party extensions
- Architecture fitness functions in CI (automated principle compliance checks)
- Dependency injection container for engine wiring
- Event-driven architecture for engine communication
- Formal DDD aggregates with consistency boundaries

---

## 15 References

| Document | Relationship |
|----------|-------------|
| [00-CONSTITUTION.md](00-CONSTITUTION.md) | Supreme authority these principles implement |
| [02-ARCHITECTURE.md](02-ARCHITECTURE.md) | Concrete architecture shaped by these principles |
| [03-ENGINEERING-STANDARDS.md](03-ENGINEERING-STANDARDS.md) | Engineering practices derived from these principles |
| [04-CODING-STANDARDS.md](04-CODING-STANDARDS.md) | Code-level implementation of these principles |
| [05-PROJECT-STRUCTURE.md](05-PROJECT-STRUCTURE.md) | Directory structure reflecting these principles |
| [15-AI-COMPANY-VISION.md](15-AI-COMPANY-VISION.md) | Vision enabled by these principles |
