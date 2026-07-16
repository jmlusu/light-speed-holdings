# AI Company Builder — Coding Standards

> **Authority Level**: Layer 5 — derived from [03-ENGINEERING-STANDARDS.md](03-ENGINEERING-STANDARDS.md)
> **Last Updated**: 2026-07-16

---

## 1 Purpose

This document defines the coding standards for all Python code in AI Company Builder. These standards are enforced by ruff, black, mypy, and code review. Every line of code should be readable, maintainable, and consistent.

---

## 2 Scope

This document covers:

- PEP 8 compliance
- SOLID principles
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- YAGNI (You Aren't Gonna Need It)
- Composition over inheritance
- Code organization
- Naming conventions
- Function design
- Class design
- Package organization
- Examples and anti-patterns

---

## 3 PEP 8 Compliance

### 3.1 Tooling

| Tool | Config | Purpose |
|------|--------|---------|
| ruff | `pyproject.toml` line-length = 100 | Linting |
| black | `pyproject.toml` line-length = 100 | Formatting |
| mypy | `mypy src/` | Type checking |

### 3.2 Line Length

Maximum line length is **100 characters**. This applies to:

- Code lines
- Docstring lines
- Comment lines
- Import lines

### 3.3 Whitespace

```python
# Correct
x = 1
if x == 1:
    do_something()

# Incorrect
x=1
if x==1:
    do_something()
```

### 3.4 Blank Lines

```python
# Two blank lines before top-level definitions
def function_one():
    pass


def function_two():
    pass


# One blank line before method definitions inside a class
class MyClass:
    def method_one(self):
        pass

    def method_two(self):
        pass
```

---

## 4 SOLID Principles

### 4.1 Single Responsibility Principle

Each module, class, and function should have one reason to change.

```python
# Good: One responsibility
class DecisionEngine:
    """Evaluates actions against governance rules."""

    def evaluate_action(self, action: str) -> dict:
        ...

# Bad: Multiple responsibilities
class DecisionAndWorkflowEngine:
    """Evaluates actions AND manages workflows."""

    def evaluate_action(self, action: str) -> dict:
        ...

    def start_workflow(self, workflow_id: str) -> None:
        ...
```

### 4.2 Open/Closed Principle

Open for extension, closed for modification.

```python
# Good: Extensible via configuration
_TEMPLATE_MAP: dict[str, str] = {
    "executive": "executive.md.j2",
    "department": "department.md.j2",
}
# Adding new type = adding to dict, not modifying code

# Bad: Requires modifying code to extend
def generate_agent(agent_type: str):
    if agent_type == "executive":
        ...
    elif agent_type == "department":
        ...
    # Adding new type = modifying function
```

### 4.3 Liskov Substitution Principle

All models inherit from `pydantic.BaseModel`. Any model can be used wherever a BaseModel is expected.

### 4.4 Interface Segregation

Keep interfaces small and focused:

```python
# Good: Small, focused interface
class MemoryStore:
    def store(self, entry: MemoryEntry) -> None: ...
    def recall(self, query: str) -> list[MemoryEntry]: ...

# Bad: Bloated interface
class MemoryStore:
    def store(self, entry: MemoryEntry) -> None: ...
    def recall(self, query: str) -> list[MemoryEntry]: ...
    def export_to_json(self) -> str: ...
    def import_from_json(self, data: str) -> None: ...
    def generate_report(self) -> str: ...
    def send_email_notification(self, email: str) -> None: ...
```

### 4.5 Dependency Inversion

Depend on abstractions, not concretions:

```python
# Good: Depends on model interface
def create_engine(registry: CompanyRegistry) -> DecisionEngine:
    return DecisionEngine(registry)

# Bad: Depends on concrete file system
def create_engine(config_path: str) -> DecisionEngine:
    raw = load_from_disk(config_path)
    return DecisionEngine(raw)
```

---

## 5 DRY (Don't Repeat Yourself)

### 5.1 Principle

Every piece of knowledge should have a single, unambiguous representation within the system.

### 5.2 Application

```python
# Good: Shared validation logic
def validate_agent_id(agent_id: str) -> bool:
    """Validate that agent_id follows naming convention."""
    return bool(re.match(r"^[a-z][a-z0-9_]*$", agent_id))

# Used in multiple places
validate_agent_id(executive.id)
validate_agent_id(department.id)
validate_agent_id(specialist.id)

# Bad: Duplicated validation
if re.match(r"^[a-z][a-z0-9_]*$", executive.id):
    ...
if re.match(r"^[a-z][a-z0-9_]*$", department.id):  # Duplicate!
    ...
```

---

## 6 KISS (Keep It Simple, Stupid)

### 6.1 Principle

Every piece of code should be as simple as possible, but no simpler.

### 6.2 Application

```python
# Good: Simple, readable
def count_agents(registry: CompanyRegistry) -> int:
    """Count total agents in the company."""
    return (
        len(registry.executives)
        + len(registry.departments)
        + len(registry.specialists)
        + len(registry.board)
    )

# Bad: Over-engineered
def count_agents(registry: CompanyRegistry) -> int:
    """Count total agents using reduce with lambda composition."""
    from functools import reduce
    return reduce(
        lambda acc, field: acc + len(getattr(registry, field)),
        ["executives", "departments", "specialists", "board"],
        0,
    )
```

---

## 7 YAGNI (You Aren't Gonna Need It)

### 7.1 Principle

Don't write code for features that don't exist yet. Every line of code is a liability.

### 7.2 Application

```python
# Good: Only what's needed now
class MemoryStore:
    def store(self, entry: MemoryEntry) -> None:
        """Store a memory entry."""
        self._store[entry.type].append(entry)

# Bad: Building for hypothetical future
class MemoryStore:
    def store(self, entry: MemoryEntry) -> None:
        """Store a memory entry."""
        self._store[entry.type].append(entry)

    def store_batch(self, entries: list[MemoryEntry]) -> None:
        """Store multiple entries. (not needed yet)"""
        for entry in entries:
            self.store(entry)

    def store_async(self, entry: MemoryEntry) -> None:
        """Store asynchronously. (not needed yet)"""
        ...

    def store_with_retry(self, entry: MemoryEntry, retries: int = 3) -> None:
        """Store with retry logic. (not needed yet)"""
        ...
```

---

## 8 Composition Over Inheritance

### 8.1 Principle

Prefer composing small, focused functions and objects over creating deep inheritance hierarchies.

### 8.2 Application

```python
# Good: Composition
class DecisionEngine:
    def __init__(self, registry: CompanyRegistry) -> None:
        self.registry = registry
        self.approval_matrix = registry.approval_matrix
        self.risk_matrix = registry.risk_matrix

    def evaluate_action(self, action: str) -> dict:
        rules = self._find_rules(action)
        risk = self._assess_risk(action)
        return {"rules": rules, "risk": risk}

# Bad: Inheritance
class BaseEngine:
    def __init__(self, registry):
        self.registry = registry

class DecisionEngine(BaseEngine):
    def evaluate(self):
        ...

class WorkflowEngine(BaseEngine):
    def execute(self):
        ...

# Now DecisionEngine and WorkflowEngine are coupled through BaseEngine
```

---

## 9 Naming Conventions

### 9.1 General Rules

| Element | Convention | Example |
|---------|-----------|---------|
| Module | `snake_case` | `decision_engine.py` |
| Class | `PascalCase` | `DecisionEngine` |
| Function | `snake_case` | `evaluate_action()` |
| Method | `snake_case` | `engine.evaluate_action()` |
| Variable | `snake_case` | `risk_level` |
| Constant | `UPPER_SNAKE_CASE` | `TEMPLATE_MAP` |
| Private | `_leading_underscore` | `_find_rules()` |
| Type alias | `PascalCase` | `AgentID = str` |
| Boolean | `is_/has_/can_` prefix | `is_valid`, `has_permission` |

### 9.2 Domain-Specific Naming

| Domain | Prefix/Pattern | Example |
|--------|---------------|---------|
| Agent IDs | `snake_case` | `chief_of_staff`, `lead_backend` |
| Config files | `snake_case.yaml` | `approval_matrix.yaml` |
| Templates | `snake_case.md.j2` | `executive.md.j2` |
| CLI commands | `kebab-case` | `ai-company company run` |
| Test files | `test_*.py` | `test_decision.py` |
| Test functions | `test_*` | `test_evaluate_action()` |

### 9.3 Anti-Patterns

```python
# Bad: Abbreviations
def calc_reg():
    ...

# Good: Full names
def calculate_regulatory_compliance():
    ...

# Bad: Hungarian notation
strName = "test"
iCount = 5

# Good: Pythonic names
name = "test"
count = 5

# Bad: Single letter (except loop variables)
def f(x):
    ...

# Good: Descriptive names
def evaluate_risk_level(action_description: str) -> RiskLevel:
    ...
```

---

## 10 Function Design

### 10.1 Rules

| Rule | Guideline |
|------|-----------|
| Max length | 50 lines |
| Max parameters | 5 (use dataclass/Pydantic for more) |
| Max return values | Use dataclass/Pydantic for >2 returns |
| Side effects | Document in docstring |
| Pure functions | Preferred when possible |

### 10.2 Function Structure

```python
def evaluate_action(
    self,
    action_description: str,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate an action against the approval matrix.

    Args:
        action_description: Natural language description of the action.
        context: Optional additional context for evaluation.

    Returns:
        Dictionary with evaluation results including matching_rules,
        risk_level, and requires_approval.

    Raises:
        DecisionError: If evaluation cannot be completed.
    """
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

### 10.3 Anti-Patterns

```python
# Bad: Too many parameters
def create_agent(id, name, role, dept, reports_to, tools, perms, meta, extra):
    ...

# Good: Use dataclass/Pydantic
def create_agent(config: AgentConfig) -> Agent:
    ...

# Bad: God function (200 lines)
def do_everything():
    ...

# Good: Small, focused functions
def load_config() -> CompanyRegistry: ...
def generate_agents(registry: CompanyRegistry) -> list[Path]: ...
def validate_output(paths: list[Path]) -> bool: ...
```

---

## 11 Class Design

### 11.1 Rules

| Rule | Guideline |
|------|-----------|
| Max length | 200 lines |
| Max methods | 10 |
| Max instance variables | 7 |
| Inheritance depth | 1 (Pydantic BaseModel only) |
| Responsibilities | Single responsibility |

### 11.2 Class Structure

```python
class DecisionEngine:
    """Evaluates organizational actions against governance rules."""

    def __init__(self, registry: CompanyRegistry) -> None:
        """Initialize with company configuration."""
        self.registry = registry
        self.approval_matrix = registry.approval_matrix
        self.risk_matrix = registry.risk_matrix
        self.decision_tree = registry.decision_tree

    def evaluate_action(self, action: str) -> dict[str, Any]:
        """Evaluate an action against the approval matrix."""
        ...

    def navigate_tree(self, start_node: str) -> list[str]:
        """Navigate the decision tree from a starting node."""
        ...

    def list_actions(self) -> list[str]:
        """List all configurable actions."""
        ...

    def _find_matching_rules(self, action: str) -> list[ApprovalEntry]:
        """Find rules matching the given action. (private)"""
        ...

    def _assess_risk(self, action: str, context: dict | None = None) -> RiskLevel:
        """Assess risk level. (private)"""
        ...
```

### 11.3 Anti-Patterns

```python
# Bad: God class
class EverythingEngine:
    def manage_decisions(self): ...
    def manage_workflows(self): ...
    def manage_memory(self): ...
    def manage_graphs(self): ...
    def generate_reports(self): ...
    def send_emails(self): ...
    # 500+ lines, 20+ methods

# Good: Focused classes
class DecisionEngine:
    """Only decision-related logic."""

class WorkflowEngine:
    """Only workflow-related logic."""
```

---

## 12 Package Organization

### 12.1 Module Structure

```
package/
├── __init__.py       # Public API exports
├── engine.py         # Core logic
├── models.py         # Data models (if package-specific)
├── exceptions.py     # Package-specific exceptions
└── _internal.py      # Private implementation details (optional)
```

### 12.2 `__init__.py` Rules

```python
# __init__.py should re-export public API
from ai_company.decision.engine import DecisionEngine

__all__ = ["DecisionEngine"]
```

### 12.3 Import Order

```python
# 1. Standard library
import json
import logging
from pathlib import Path

# 2. Third-party
from pydantic import BaseModel

# 3. Local
from ai_company.models import CompanyRegistry
```

---

## 13 Examples

### 13.1 Complete Module Example

```python
"""Workflow engine for executing organizational processes.

This module provides the WorkflowEngine class which manages
workflow execution, step tracking, and SLA monitoring.
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from ai_company.models import CompanyRegistry, Workflow, WorkflowStep

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """Manages workflow execution and tracking."""

    def __init__(self, registry: CompanyRegistry) -> None:
        self.registry = registry
        self._instances: dict[str, WorkflowInstance] = {}

    def list_workflows(self) -> list[dict[str, Any]]:
        """List all available workflows."""
        return [
            {"id": wf.id, "name": wf.name, "steps": len(wf.steps)}
            for wf in self.registry.workflows
        ]

    def start(self, workflow_id: str) -> str:
        """Start a new workflow instance."""
        workflow = self._get_workflow(workflow_id)
        instance_id = str(uuid.uuid4())[:8]
        self._instances[instance_id] = WorkflowInstance(
            workflow=workflow,
            instance_id=instance_id,
        )
        logger.info("Started workflow %s (instance: %s)", workflow_id, instance_id)
        return instance_id
```

### 13.2 Anti-Pattern Example

```python
# DON'T DO THIS
import os, sys, json, yaml, logging  # Multiple imports on one line

def do_stuff(x,y,z):  # No spaces after commas
    try:
        f=open("config.yaml")  # No spaces around =
        data=yaml.load(f)
        for i in data:  # Shadowing built-in
            if i==x:  # Comparison with = instead of ==
                return True
    except:  # Bare except
        pass  # Silent failure
    return None  # Explicit None return (unnecessary)
```

---

## 14 Best Practices

1. **Write code for humans first, computers second.** Readability is the primary goal.
2. **One concept per line.** Don't chain multiple operations on one line.
3. **Use descriptive names.** A variable name should explain its purpose.
4. **Keep related code together.** Functions that work together should be near each other.
5. **Delete dead code.** Don't comment it out — git remembers.
6. **Prefer explicit over implicit.** Don't rely on implicit behaviors.
7. **Match existing patterns.** Look at neighboring code before writing new code.

---

## 15 Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|-----------------|
| `from module import *` | Pollutes namespace, hides dependencies | Import specific names |
| Mutable default arguments | Shared state across calls | Use `None` default, create in function |
| Shadowing built-ins | Breaks expected behavior | Use descriptive names |
| Bare `except:` | Catches SystemExit, KeyboardInterrupt | Catch specific exceptions |
| Not using `with` for file I/O | Resource leaks | Always use context managers |
| Deeply nested code | Hard to read | Extract functions, use early returns |
| Magic numbers | Unclear meaning | Use named constants |

---

## 16 Future Enhancements

- Pre-commit hooks for ruff, black, mypy
- Code complexity limits (cyclomatic complexity < 10)
- Automated import sorting (isort via ruff)
- Module length limits enforced in CI
- Function complexity limits enforced in CI

---

## 17 References

| Document | Relationship |
|----------|-------------|
| [00-CONSTITUTION.md](00-CONSTITUTION.md) | Supreme authority |
| [03-ENGINEERING-STANDARDS.md](03-ENGINEERING-STANDARDS.md) | Parent engineering standards |
| [08-TESTING-STANDARDS.md](08-TESTING-STANDARDS.md) | Testing these coding standards |
| [09-CODE-REVIEW.md](09-CODE-REVIEW.md) | Reviewing for these standards |
| [pyproject.toml](../../pyproject.toml) | ruff, black, mypy configuration |
