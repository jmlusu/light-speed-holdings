# AI Company Builder — Testing Standards

> **Authority Level**: Layer 9 — derived from [03-ENGINEERING-STANDARDS.md](03-ENGINEERING-STANDARDS.md)
> **Immutable Rule Reference**: IR-3 (All new code must have corresponding tests)
> **Last Updated**: 2026-07-16

---

## 1 Purpose

This document defines the testing standards for AI Company Builder. Tests are not optional — they are a mandatory part of every change. The test suite is the safety net that allows confident refactoring and feature development.

---

## 2 Scope

This document covers:

- pytest configuration and usage
- Unit testing standards
- Integration testing standards
- Fixture standards
- Mocking standards
- Coverage requirements
- Regression testing
- Generator testing
- CLI testing
- Prompt testing
- Memory testing

---

## 3 pytest Configuration

### 3.1 Setup

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

### 3.2 Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_decision.py

# Run specific test
pytest tests/unit/test_decision.py::test_evaluate_action

# Run with coverage
pytest --cov=ai_company --cov-report=term-missing

# Run matching tests
pytest -k "decision"
```

### 3.3 Test Discovery

pytest automatically discovers tests in:

- `tests/` directory
- Files matching `test_*.py`
- Functions matching `test_*()`
- Classes matching `Test*`

---

## 4 Unit Testing

### 4.1 Structure

```python
"""Tests for the decision engine."""

import pytest
from ai_company.decision.engine import DecisionEngine
from ai_company.models import CompanyRegistry


class TestDecisionEngine:
    """Tests for DecisionEngine class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.registry = create_test_registry()
        self.engine = DecisionEngine(self.registry)

    def test_evaluate_action_returns_dict(self):
        """evaluate_action should return a dictionary."""
        result = self.engine.evaluate_action("test action")
        assert isinstance(result, dict)

    def test_evaluate_action_includes_risk_level(self):
        """evaluate_action should include risk_level in result."""
        result = self.engine.evaluate_action("test action")
        assert "risk_level" in result
```

### 4.2 Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Test file | `test_<module>.py` | `test_decision.py` |
| Test class | `Test<ClassName>` | `TestDecisionEngine` |
| Test function | `test_<what>` | `test_evaluate_action` |
| Test fixture | `create_<thing>` or `<thing>_fixture` | `create_test_registry` |

### 4.3 Assertions

```python
# Good: Specific assertions
assert result["risk_level"] == "medium"
assert len(matching_rules) == 3
assert isinstance(result, dict)

# Bad: Vague assertions
assert result  # Too vague
assert result is not None  # Doesn't verify content
```

---

## 5 Integration Testing

### 5.1 Location

Integration tests go in `tests/integration/`.

### 5.2 What to Integration Test

| Component | Integration Test |
|-----------|-----------------|
| Registry → Generator | Load config → Generate agents → Verify output |
| CLI → Engine | CLI command → Engine method → Verify side effect |
| Config → Registry → Engine | Full pipeline from YAML to result |

### 5.3 Example

```python
"""Integration test: Config → Registry → Generator pipeline."""

from pathlib import Path
from ai_company.config import load_config
from ai_company.generator import AgentGenerator


def test_full_generation_pipeline(tmp_path):
    """Test complete config → generation pipeline."""
    registry = load_config()
    generator = AgentGenerator(registry, output_dir=tmp_path)

    generator.generate_all()

    agent_files = list(tmp_path.glob("*.md"))
    assert len(agent_files) > 0
    assert all(f.read_text().strip() for f in agent_files)
```

---

## 6 Fixtures

### 6.1 conftest.py

Shared fixtures go in `tests/conftest.py`:

```python
"""Shared test fixtures."""

import pytest
from ai_company.models import CompanyRegistry, Executive, Department


@pytest.fixture
def sample_executive():
    """Create a sample executive for testing."""
    return Executive(
        id="test_exec",
        name="Test Executive",
        role="Test Role",
        department="Engineering",
        seniority="executive",
    )


@pytest.fixture
def sample_registry():
    """Create a minimal CompanyRegistry for testing."""
    return CompanyRegistry(
        company={"name": "Test Company", "id": "test-co"},
        executives=[],
        departments=[],
        specialists=[],
        board=[],
        workflows=[],
    )
```

### 6.2 Fixture Rules

| Rule | Rationale |
|------|-----------|
| Use `@pytest.fixture` | Proper lifecycle management |
| Use `setup_method` for class tests | Fresh instance per test |
| Scope fixtures appropriately | Don't share state between tests |
| Use `tmp_path` for file I/O tests | Automatic cleanup |
| Name fixtures descriptively | `create_test_registry` not `fixture1` |

---

## 7 Mocking

### 7.1 When to Mock

| Scenario | Mock? | Reason |
|----------|-------|--------|
| External API calls (LLM) | Yes | Don't depend on external services |
| File system (for unit tests) | Yes | Isolate from I/O |
| Time-dependent logic | Yes | Deterministic tests |
| Database (future) | Yes | Isolate from persistence |

### 7.2 Mocking Tools

```python
from unittest.mock import MagicMock, patch, Mock

# Mock an external API
with patch("ai_company.llm.client.openai") as mock_openai:
    mock_openai.ChatCompletion.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="test response"))]
    )
    result = client.generate("test prompt")

# Mock file system
def test_memory_store(tmp_path):
    store = MemoryStore(base_path=tmp_path)
    store.store(MemoryEntry(type="episodic", content="test"))
    assert store.count("episodic") == 1
```

### 7.3 Mocking Rules

| Rule | Rationale |
|------|-----------|
| Mock at the boundary | Don't mock internal functions |
| Don't over-mock | Test real behavior when possible |
| Verify mock calls | Assert mocks were called correctly |
| Use `tmp_path` over mocking file I/O | Prefer real I/O with temp files |

---

## 8 Coverage Requirements

### 8.1 Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Line coverage | >80% | `pytest --cov=ai_company` |
| Branch coverage | >70% | `pytest --cov=ai_company --cov-branch` |
| New code coverage | 100% | PR review |

### 8.2 Coverage Configuration

```bash
# Generate coverage report
pytest --cov=ai_company --cov-report=term-missing --cov-report=html

# View HTML report
open htmlcov/index.html
```

### 8.3 Coverage Rules

| Rule | Rationale |
|------|-----------|
| New code must have 100% coverage | Quality gate |
| Coverage gaps must be documented | Known risk areas |
| Don't chase 100% overall | Diminishing returns |

---

## 9 Regression Testing

### 9.1 Principle

Every bug fix must include a test that reproduces the bug. This test prevents the bug from recurring.

### 9.2 Pattern

```python
def test_bug_fix_issue_123():
    """Regression test: Issue #123 — division by zero in risk calculation.

    Before the fix, calculate_risk() raised ZeroDivisionError when
    the risk matrix had no entries. After the fix, it returns a
    default risk level.
    """
    from ai_company.decision.engine import DecisionEngine

    engine = DecisionEngine(empty_registry)
    result = engine.calculate_risk("test action")
    assert result is not None  # Should not raise
```

---

## 10 Generator Testing

### 10.1 What to Test

| Aspect | Test |
|--------|------|
| Template rendering | Verify output for known input |
| Template inheritance | Verify base template blocks are overridden |
| File generation | Verify files are created |
| Idempotency | Verify re-running produces same output |
| Error handling | Verify graceful handling of bad input |

### 10.2 Example

```python
def test_generate_executive_agent(tmp_path):
    """Test executive agent generation."""
    from ai_company.generator import AgentGenerator

    registry = create_test_registry()
    generator = AgentGenerator(registry, output_dir=tmp_path)

    generator.generate_agent(registry.executives[0])

    output_file = tmp_path / f"{registry.executives[0].id}.md"
    assert output_file.exists()
    content = output_file.read_text()
    assert "Identity" in content
    assert "Mission" in content
```

---

## 11 CLI Testing

### 11.1 Tool

Use `typer.testing.CliRunner` for CLI testing:

```python
from typer.testing import CliRunner
from ai_company.cli.main import app

runner = CliRunner()


def test_help_command():
    """Test that --help works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "AI Company Builder" in result.output


def test_company_status():
    """Test company status command."""
    result = runner.invoke(app, ["company", "status"])
    assert result.exit_code == 0
```

### 11.2 CLI Test Rules

| Rule | Rationale |
|------|-----------|
| Test all commands | Every CLI entry point must be tested |
| Test error cases | Invalid arguments, missing files, etc. |
| Test output format | Verify rich output renders correctly |
| Use `tmp_path` for file operations | Don't pollute real directories |

---

## 12 Prompt Testing

### 12.1 Principle

Agent prompts must be tested to verify agents behave as expected.

### 12.2 What to Test

| Aspect | Test |
|--------|------|
| Prompt completeness | All required sections present |
| Prompt format | Follows the standard template |
| Agent behavior | Agent responds within defined scope |
| Restriction enforcement | Agent doesn't violate restrictions |

### 12.3 Current State

Prompt testing is manual. Automated prompt testing is a future enhancement.

---

## 13 Memory Testing

### 13.1 What to Test

| Aspect | Test |
|--------|------|
| Store/retrieve | Store entry, recall by query |
| Type filtering | Recall only specific types |
| Persistence | Write to disk, read back |
| Consolidation | Merge related memories |
| Count/stats | Verify accurate counts |

### 13.2 Example

```python
def test_memory_store_and_recall(tmp_path):
    """Test memory storage and retrieval."""
    from ai_company.memory.engine import MemoryStore, MemoryEntry

    store = MemoryStore(base_path=tmp_path)
    entry = MemoryEntry(
        type="episodic",
        content="Test memory content",
        agent_id="test_agent",
    )
    store.store(entry)

    results = store.recall("test")
    assert len(results) == 1
    assert results[0].content == "Test memory content"
```

---

## 14 Test Organization

### 14.1 Current Structure

```
tests/
├── unit/
│   ├── test_models.py          # 16 tests
│   ├── test_registry.py        # 18 tests
│   ├── test_bootstrap.py       # 7 tests
│   ├── test_decision.py        # 11 tests
│   ├── test_workflow.py        # 12 tests
│   ├── test_memory.py          # 11 tests
│   ├── test_graph.py           # 14 tests
│   ├── test_generator.py       # 5 tests
│   ├── test_dashboard.py       # Dashboard tests
│   ├── test_executor.py        # Executor tests
│   ├── test_llm.py             # LLM tests
│   ├── test_model_router.py    # Router tests
│   └── test_orchestrator.py    # Orchestrator tests
└── integration/
```

### 14.2 Organization Rules

| Rule | Rationale |
|------|-----------|
| One test file per source module | Easy to find tests |
| Mirror source structure | Predictable organization |
| Group related tests | Readability |
| Keep tests independent | No test depends on another |

---

## 15 Examples

### 15.1 Complete Test File

```python
"""Tests for the memory engine."""

import pytest
from pathlib import Path

from ai_company.memory.engine import MemoryStore, MemoryEntry


class TestMemoryStore:
    """Tests for MemoryStore class."""

    def test_store_and_retrieve(self, tmp_path):
        """Store an entry and retrieve it."""
        store = MemoryStore(base_path=tmp_path)
        entry = MemoryEntry(type="episodic", content="test content")

        store.store(entry)
        results = store.recall("test")

        assert len(results) == 1
        assert results[0].content == "test content"

    def test_count_by_type(self, tmp_path):
        """Count entries by type."""
        store = MemoryStore(base_path=tmp_path)
        store.store(MemoryEntry(type="episodic", content="one"))
        store.store(MemoryEntry(type="semantic", content="two"))
        store.store(MemoryEntry(type="episodic", content="three"))

        assert store.count("episodic") == 2
        assert store.count("semantic") == 1
        assert store.count("procedural") == 0

    def test_empty_store_returns_no_results(self, tmp_path):
        """Empty store returns no results."""
        store = MemoryStore(base_path=tmp_path)
        results = store.recall("anything")
        assert results == []
```

---

## 16 Best Practices

1. **Write tests first**: Test-driven development catches issues early.
2. **Test one thing per test**: Each test should verify one behavior.
3. **Use descriptive test names**: `test_evaluate_action_with_high_risk` not `test_1`.
4. **Keep tests independent**: No test should depend on another test's state.
5. **Use fixtures for setup**: Don't repeat setup code across tests.
6. **Test edge cases**: Empty inputs, large inputs, invalid inputs.
7. **Test error paths**: Verify exceptions are raised correctly.

---

## 17 Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|-----------------|
| Testing implementation details | Tests break on refactoring | Test public API behavior |
| Shared mutable state between tests | Non-deterministic failures | Use fixtures, create fresh instances |
| Not testing error paths | Errors go undetected | Test both success and failure |
| Mocking too much | Tests don't verify real behavior | Mock only external boundaries |
| Tests that depend on execution order | Non-deterministic failures | Each test is self-contained |
| Not running tests in CI | Regressions go undetected | CI runs full test suite |

---

## 18 Future Enhancements

- Test coverage reporting in CI
- Performance testing framework
- Property-based testing with Hypothesis
- Mutation testing
- Prompt testing automation
- Contract testing for API boundaries

---

## 19 References

| Document | Relationship |
|----------|-------------|
| [00-CONSTITUTION.md](00-CONSTITUTION.md) | IR-3 (All new code must have tests) |
| [03-ENGINEERING-STANDARDS.md](03-ENGINEERING-STANDARDS.md) | Engineering standards |
| [04-CODING-STANDARDS.md](04-CODING-STANDARDS.md) | Code standards for tests |
| [10-DEFINITION-OF-DONE.md](10-DEFINITION-OF-DONE.md) | Tests must pass for completion |
| [pyproject.toml](../../pyproject.toml) | pytest configuration |
| [tests/](../../tests/) | Test suite |
