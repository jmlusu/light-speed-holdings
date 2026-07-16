# AI Company Builder — Engineering Standards

> **Authority Level**: Layer 4 — derived from [02-ARCHITECTURE.md](02-ARCHITECTURE.md)
> **Last Updated**: 2026-07-16

---

## 1 Purpose

This document defines the engineering standards that govern all development work in AI Company Builder. These standards ensure consistency, quality, and maintainability across the codebase.

---

## 2 Scope

This document covers:

- Python version and language features
- Dependency management
- Logging standards
- Error handling patterns
- Type annotations
- Dependency injection
- Validation patterns
- Performance guidelines
- Scalability considerations
- Maintainability practices
- Configuration management

---

## 3 Python Standards

### 3.1 Version

| Standard | Value |
|----------|-------|
| Python version | 3.12+ |
| Minimum version | 3.12 (declared in `pyproject.toml`) |
| Target version | 3.12 (for ruff, black) |
| Syntax features | Use modern Python: `match/case`, `type` aliases, `X \| Y` unions |

### 3.2 Language Features

| Feature | Usage |
|---------|-------|
| `match/case` | Use for complex pattern matching instead of chained `if/elif` |
| `type` aliases | Use `type AgentID = str` for domain-specific string types |
| `X \| Y` unions | Use instead of `Union[X, Y]` or `Optional[X]` |
| `dataclass` | Use for simple data containers without validation |
| `Pydantic BaseModel` | Use for all domain models requiring validation |
| Walrus operator `:=` | Use sparingly, only when it improves readability |
| f-strings | Use for all string formatting |
| `pathlib.Path` | Use instead of `os.path` |

### 3.3 Import Order

```
1. Standard library
2. Third-party packages
3. Local packages (relative imports)
```

Separate each group with a blank line. Use absolute imports (`from ai_company.models import ...`).

---

## 4 Dependency Management

### 4.1 File

All dependencies are declared in `pyproject.toml`:

```toml
[project]
dependencies = [
    "jinja2",
    "pyyaml",
    "pydantic>=2.8",
    "typer",
    "rich",
    "networkx",
    "python-dotenv",
]

[project.optional-dependencies]
dev = [
    "pytest",
    "pytest-cov",
    "ruff",
    "black",
    "mypy",
    "types-PyYAML",
]
```

### 4.2 Rules

| Rule | Rationale |
|------|-----------|
| Pin minimum versions for critical deps | `pydantic>=2.8` ensures API compatibility |
| Never pin patch versions | Let pip resolve to latest compatible |
| New deps require security review | Supply chain security (see [13-SECURITY-STANDARDS.md](13-SECURITY-STANDARDS.md)) |
| Dev deps are separate | Production images don't need test tools |
| No dependencies in source code | Dependencies are managed at project level only |

### 4.3 Adding a Dependency

1. Check if existing deps already cover the need
2. Verify license compatibility (prefer MIT, BSD, Apache 2.0)
3. Check for known vulnerabilities (`pip audit`)
4. Add to `pyproject.toml` under appropriate section
5. Run `pip install -e ".[dev]"` to install
6. Run `ruff check src/ && mypy src/ && pytest` to verify no regressions

---

## 5 Logging Standards

### 5.1 Framework

Use Python's built-in `logging` module. Configure via `logging.basicConfig()` at application entry point.

### 5.2 Log Levels

| Level | When to Use | Example |
|-------|------------|---------|
| `DEBUG` | Detailed diagnostic information | `"Loaded 19 config files in 0.23s"` |
| `INFO` | Normal operational events | `"Company bootstrap complete: 31 agents generated"` |
| `WARNING` | Unexpected but recoverable | `"Config file routing.yaml missing, using defaults"` |
| `ERROR` | Operation failed | `"Failed to generate agent: lead-backend"` |
| `CRITICAL` | System-level failure | `"Cannot load CompanyRegistry: config files corrupt"` |

### 5.3 Format

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Generated %d agents from registry", len(agents))
logger.error("Failed to load config: %s", exc_info=True)
```

### 5.4 Rules

| Rule | Rationale |
|------|-----------|
| Use module-level loggers | `logging.getLogger(__name__)` for traceability |
| Never log secrets or keys | Security |
| Use lazy formatting | `logger.info("Count: %d", count)` not `logger.info(f"Count: {count}")` |
| Log exceptions with `exc_info=True` | Full stack traces for debugging |
| Don't use `print()` for operational output | Use `logging` or CLI output (rich) |

---

## 6 Error Handling

### 6.1 Exception Hierarchy

```python
class AIBaseError(Exception):
    """Base exception for all AI Company Builder errors."""

class ConfigError(AIBaseError):
    """Configuration loading or validation failed."""

class RegistryError(AIBaseError):
    """Registry parsing or resolution failed."""

class GenerationError(AIBaseError):
    """Agent generation failed."""

class DecisionError(AIBaseError):
    """Decision evaluation failed."""

class WorkflowError(AIBaseError):
    """Workflow execution failed."""
```

### 6.2 Error Handling Patterns

**Pattern 1: Fail Fast**

```python
def load_config(path: Path) -> CompanyRegistry:
    if not path.exists():
        raise ConfigError(f"Config not found: {path}")
    # ... proceed with confidence
```

**Pattern 2: Catch and Re-raise with Context**

```python
try:
    raw = yaml.safe_load(f)
except yaml.YAMLError as e:
    raise ConfigError(f"Invalid YAML in {path}: {e}") from e
```

**Pattern 3: Log and Continue**

```python
for agent in registry.specialists:
    try:
        generate_agent(agent)
    except GenerationError as e:
        logger.error("Failed to generate %s: %s", agent.id, e)
        continue  # Don't fail entire generation for one agent
```

### 6.3 Rules

| Rule | Rationale |
|------|-----------|
| Never catch bare `except:` | Catches `SystemExit`, `KeyboardInterrupt` |
| Always use specific exception types | Prevents masking unrelated errors |
| Include actionable error messages | `"Config not found: config/company/company.yaml"` not `"File not found"` |
| Use `raise ... from e` | Preserves exception chain for debugging |
| Validate at boundaries | Fail fast at config load, API boundaries |

---

## 7 Type Annotations

### 7.1 Standard

All public APIs must have complete type annotations. This is enforced by mypy.

```python
def evaluate_action(
    self,
    action_description: str,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate an action against the approval matrix."""
    ...
```

### 7.2 Rules

| Rule | Rationale |
|------|-----------|
| All function parameters must be typed | mypy enforcement |
| All return types must be declared | mypy enforcement |
| Use `dict[str, Any]` not `Dict[str, Any]` | Python 3.12+ syntax |
| Use `list[str]` not `List[str]` | Python 3.12+ syntax |
| Use `X \| None` not `Optional[X]` | Python 3.12+ syntax |
| Use `Any` only when type is truly dynamic | Prefer specific types |
| Use `type` aliases for domain types | `type AgentID = str` |

### 7.3 Model Types

```python
from pydantic import BaseModel, Field

class Agent(BaseModel):
    id: str
    name: str
    role: str
    department: str | None = None
    tools: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)
```

---

## 8 Dependency Injection

### 8.1 Current Approach

Dependencies are resolved through function parameters and factory functions:

```python
# Factory function
def load_config() -> CompanyRegistry:
    """Create CompanyRegistry from YAML files."""
    ...

# Function parameter injection
def create_engine(registry: CompanyRegistry) -> DecisionEngine:
    """Create engine with injected dependency."""
    ...
```

### 8.2 Rules

| Rule | Rationale |
|------|-----------|
| Pass dependencies as parameters | Explicit over implicit |
| Use factory functions for complex construction | Centralize creation logic |
| Don't use global state for dependencies | Testability |
| Prefer composition over DI containers | Simplicity (for current scale) |

### 8.3 Future

When the codebase grows beyond 30+ modules, consider:
- `dependency-injector` package
- Formal DI container
- Interface-based injection

---

## 9 Validation

### 9.1 Configuration Validation

All configuration is validated at load time:

```python
# registry/validator.py
def validate(registry: dict) -> dict:
    errors = []
    if not registry.get("company", {}).get("name"):
        errors.append("Company name is required")
    if not registry.get("executives"):
        errors.append("At least one executive is required")
    # ... more checks
    if errors:
        raise ConfigError("Validation failed: " + "; ".join(errors))
    return registry
```

### 9.2 Model Validation

Pydantic handles model-level validation:

```python
class Executive(BaseModel):
    id: str  # Required
    name: str  # Required
    seniority: str = ""  # Optional with default
    decision_rights: list[str] = Field(default_factory=list)
```

### 9.3 Input Validation

CLI commands validate inputs:

```python
@app.command()
def evaluate(action: str) -> None:
    if not action.strip():
        console.print("[red]Error: Action cannot be empty[/red]")
        raise typer.Exit(1)
```

### 9.4 Validation Rules

| Layer | What is Validated | When |
|-------|------------------|------|
| Config | Structure, required fields, types | Load time |
| Models | Field types, constraints, defaults | Construction time |
| CLI | User input format, ranges | Command execution |
| Engine | Business rules, preconditions | Method call time |

---

## 10 Performance

### 10.1 Guidelines

| Guideline | Target | Measurement |
|-----------|--------|-------------|
| Config load time | < 1 second | `time python -c "from ai_company.config import load_config; load_config()"` |
| Agent generation | < 5 seconds (all 31 agents) | `time python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` |
| Test suite | < 60 seconds | `time pytest` |
| CLI response | < 2 seconds | Manual timing |
| Memory usage | < 100MB | `psutil` monitoring |

### 10.2 Optimization Rules

| Rule | Rationale |
|------|-----------|
| Profile before optimizing | Don't guess at bottlenecks |
| Cache expensive computations | `functools.lru_cache` for repeated lookups |
| Lazy-load large data | Don't load everything at startup |
| Use generators for large datasets | Memory efficiency |
| Avoid premature optimization | Simplicity first |

---

## 11 Scalability

### 11.1 Current Scale

| Metric | Current | Limit |
|--------|---------|-------|
| Config files | 19 | ~100 before refactor |
| Models | 17+ | ~50 before package split |
| Agents | 31 | ~100 before optimization |
| CLI commands | 22 | ~50 before grouping |
| Tests | 175 | ~1000 before parallelization |

### 11.2 Scaling Strategy

| Scale Threshold | Action |
|----------------|--------|
| >50 models | Split `models.py` into domain packages |
| >100 agents | Add agent generation caching |
| >50 CLI commands | Group into CLI namespaces |
| >1000 tests | Enable pytest parallel execution |
| >100 config files | Add config file validation caching |

---

## 12 Maintainability

### 12.1 Code Organization Rules

| Rule | Rationale |
|------|-----------|
| Single Responsibility | Each module does one thing |
| Module length < 500 lines | Readability |
| Function length < 50 lines | Readability |
| Class length < 200 lines | Readability |
| No circular imports | Compilation and test speed |

### 12.2 Documentation Rules

| Rule | Rationale |
|------|-----------|
| All public functions have docstrings | API documentation |
| All modules have module docstrings | Context |
| Complex logic has inline comments | Explanation |
| README.md is always current | Onboarding |
| Architecture docs match code | Truth |

### 12.3 Refactoring Rules

| Rule | Rationale |
|------|-----------|
| Refactor only with tests passing | Safety net |
| Refactor one concern at a time | Isolation |
| Keep diffs small | Reviewability |
| Update docs with refactoring | Accuracy |

---

## 13 Configuration Management

### 13.1 Principles

1. Configuration is the source of truth
2. All configuration is validated at load time
3. Configuration changes are version-controlled
4. Generated configuration is derived, not authoritative
5. Environment-specific overrides use `.env` files

### 13.2 Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `AI_COMPANY_CONFIG_DIR` | Override config directory | `config/` |
| `AI_COMPANY_OUTPUT_DIR` | Override output directory | `.opencode/` |
| `OPENAI_API_KEY` | OpenAI API key | None |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |

### 13.3 Configuration Hierarchy

```
1. Hardcoded defaults (in code)
2. YAML config files (config/)
3. Environment variables (.env)
4. CLI arguments (highest priority)
```

---

## 14 Examples

### 14.1 Well-Engineered Module

```python
"""Decision engine for evaluating actions against governance rules."""

import logging
from typing import Any

from ai_company.models import (
    ApprovalEntry,
    CompanyRegistry,
    RiskLevel,
)

logger = logging.getLogger(__name__)


class DecisionEngine:
    """Evaluates organizational actions against approval matrix and risk rules."""

    def __init__(self, registry: CompanyRegistry) -> None:
        self.registry = registry
        self.approval_matrix = registry.approval_matrix
        self.risk_matrix = registry.risk_matrix

    def evaluate_action(
        self,
        action_description: str,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Evaluate an action against the approval matrix."""
        logger.debug("Evaluating action: %s", action_description)

        matching_rules = self._find_matching_rules(action_description)
        risk_level = self._assess_risk(action_description, context)

        return {
            "action": action_description,
            "matching_rules": len(matching_rules),
            "risk_level": risk_level.value,
            "requires_approval": risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL),
        }
```

### 14.2 Anti-Pattern: Poor Engineering

```python
# DON'T DO THIS
def do_stuff(x, y, z):
    try:
        f = open("config.yaml")
        data = yaml.load(f)
        # ... 200 lines of logic ...
        return data
    except:
        pass
    # No type hints, no logging, bare except, no docstring,
    # file I/O in business logic, no validation
```

---

## 15 Best Practices

1. **Type everything**: If it can be typed, type it. mypy is your friend.
2. **Log meaningfully**: Logs should tell a story about what happened.
3. **Fail fast, fail loud**: Errors should be impossible to ignore.
4. **Validate at boundaries**: Don't let bad data propagate.
5. **Keep functions pure**: Side effects are harder to test.
6. **Document as you code**: Don't leave documentation for later.
7. **Review your own PR**: Before asking others, review your own changes.

---

## 16 Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|-----------------|
| Using `print()` for debugging | pollutes stdout, not configurable | Use `logging.debug()` |
| Catching bare `except:` | catches SystemExit, KeyboardInterrupt | Catch specific exceptions |
| Missing type annotations | mypy can't verify correctness | Add types to all public APIs |
| Hardcoding file paths | not portable, not testable | Use `pathlib.Path` and config |
| No docstrings | API is undocumented | Add docstrings to all public functions |
| Importing at module level unnecessarily | slow startup, circular deps | Import where needed |
| Using mutable defaults | shared state bugs | Use `Field(default_factory=list)` |

---

## 17 Future Enhancements

- Pre-commit hooks for linting and type checking
- Architecture fitness functions in CI
- Automated dependency updates (Dependabot)
- Performance benchmarks in CI
- Code complexity metrics (cyclomatic complexity limits)
- Automated API documentation generation

---

## 18 References

| Document | Relationship |
|----------|-------------|
| [00-CONSTITUTION.md](00-CONSTITUTION.md) | Supreme authority |
| [04-CODING-STANDARDS.md](04-CODING-STANDARDS.md) | Code-level implementation of these standards |
| [08-TESTING-STANDARDS.md](08-TESTING-STANDARDS.md) | Testing standards for this engineering |
| [13-SECURITY-STANDARDS.md](13-SECURITY-STANDARDS.md) | Security standards |
| [pyproject.toml](../../pyproject.toml) | Dependency declarations |
| [AGENTS.md](../../AGENTS.md) | Development commands |
