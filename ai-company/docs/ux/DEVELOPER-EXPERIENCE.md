# Developer Experience Design

> Onboarding, configuration, testing, debugging, and common task recipes.

---

## 1. Design Principles

| Principle | Description |
|-----------|-------------|
| **Zero to productive in 10 minutes** | First task done, tests passing, CLI working |
| **Convention over configuration** | Sensible defaults, explicit overrides |
| **Fast feedback loops** | < 5s for lint, < 30s for tests |
| **Reproducible** | Same results on any machine |
| **Observable** | Every action has a visible result |

---

## 2. Onboarding Flow

### 2.1 First-Time Setup (< 10 minutes)

```bash
# 1. Clone and enter project
cd ai-company

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS/Linux

# 3. Install with dev dependencies
pip install -e ".[dev]"

# 4. Bootstrap the company
ai-company company run

# 5. Verify everything works
ai-company doctor run

# 6. Run tests
pytest

# 7. Start the dashboard
ai-company dashboard
```

**Expected result:**
- 27 agent files generated in `.opencode/agents/`
- Dashboard opens at http://localhost:8420
- All tests pass
- `ai-company doctor run` shows all green

### 2.2 Onboarding Checklist

| Step | Command | Expected Output |
|------|---------|-----------------|
| Install deps | `pip install -e ".[dev]"` | No errors |
| Bootstrap | `ai-company company run` | "27 agents ready" |
| Health check | `ai-company doctor run` | All PASS |
| Lint | `ruff check src/` | No errors |
| Type check | `mypy src/` | No errors |
| Tests | `pytest` | All pass |
| Dashboard | `ai-company dashboard` | Opens browser |

### 2.3 First Contribution

1. Read `AGENTS.md` for project context
2. Read `docs/ARCHITECTURE.md` for module layout
3. Pick an issue from the backlog
4. Create a feature branch
5. Write tests first (TDD)
6. Implement the change
7. Run `ruff check src/ && mypy src/ && pytest`
8. Submit PR

---

## 3. Configuration Experience

### 3.1 Configuration Files

All configuration lives in `company/`:

| File | Purpose | Format |
|------|---------|--------|
| `agent-registry.json` | Agent definitions (single source of truth) | JSON |
| `models.yaml` | LLM provider routing | YAML |
| `departments.yaml` | Department structure | YAML |
| `config/kpis.yaml` | Department KPI definitions | YAML |
| `workflows.yaml` | Workflow definitions | YAML |

### 3.2 Adding a New Agent

**Before (manual):**
1. Edit `company/agent-registry.json`
2. Add entry with id, name, role, type, department, reportsTo, tools, permissions
3. Run `ai-company generate`
4. Verify with `ai-company agents list`

**After (with validation):**
```bash
$ ai-company agents create \
    --id backend-dev-2 \
    --name "Backend Developer 2" \
    --role "Backend Developer" \
    --type specialist \
    --department engineering \
    --reports-to lead-engineer \
    --tools python,git,docker \
    --permissions read,edit,bash

✓ Agent 'backend-dev-2' created in registry
  Run: ai-company generate
```

### 3.3 Configuration Validation

```bash
$ ai-company doctor run

System Health
┌────────────────────────┬──────┬──────────────────────────────────┐
│ Check                  │Status│ Message                          │
├────────────────────────┼──────┼──────────────────────────────────┤
│ Registry exists        │ PASS │ Found 27 agents                  │
│ Registry valid JSON    │ PASS │ Valid JSON                       │
│ All agents have IDs    │ PASS │ All agents have unique IDs       │
│ ReportsTo chain valid  │ PASS │ No circular references           │
│ Models config exists   │ PASS │ 3 tiers configured               │
│ Departments config     │ PASS │ 7 departments defined            │
│ KPI config exists      │ PASS │ 28 KPIs across 7 departments     │
│ Templates directory    │ PASS │ 12 Jinja2 templates found        │
│ .opencode/ directory   │ PASS │ Exists                           │
│ inbox.json exists      │ PASS │ Valid JSON array                 │
└────────────────────────┴──────┴──────────────────────────────────┘

All 10 checks passed!
```

---

## 4. Testing Workflow

### 4.1 Test Structure

```
ai-company/tests/
+-- unit/
|   +-- test_models.py
|   +-- test_message_bus.py
|   +-- test_decision_engine.py
|   +-- test_memory_engine.py
|   +-- test_executor.py
|   +-- test_dashboard.py
|   +-- test_cli.py
|   +-- test_security.py      # Note: skip with --ignore
+-- integration/
|   +-- test_full_pipeline.py
|   +-- test_orchestrator.py
|   +-- test_executor_flow.py
```

### 4.2 Running Tests

```bash
# All tests
pytest

# Single file
pytest tests/unit/test_models.py

# Single test
pytest tests/unit/test_models.py::test_task_creation

# With verbose output
pytest -v

# With coverage
pytest --cov=ai_company --cov-report=html

# Skip broken test file
pytest --ignore=tests/unit/test_security.py

# Run integration tests only
pytest tests/integration/
```

### 4.3 Writing Tests

**Pattern: Arrange → Act → Assert**

```python
def test_task_creation():
    """Test that a task can be created with required fields."""
    # Arrange
    task = Task(
        id="test-001",
        sender_id="human-ceo",
        receiver_id="lead-engineer",
        instruction="Review PR #42",
        priority=TaskPriority.HIGH,
    )

    # Act
    result = task.model_dump()

    # Assert
    assert result["id"] == "test-001"
    assert result["status"] == TaskStatus.PENDING
    assert result["priority"] == TaskPriority.HIGH
```

**Pattern: Fixtures for shared state**

```python
@pytest.fixture
def sample_task():
    return Task(
        id="fixture-001",
        sender_id="human-ceo",
        receiver_id="lead-engineer",
        instruction="Test instruction",
    )

def test_task_status(sample_task):
    assert sample_task.status == TaskStatus.PENDING
```

### 4.4 Test Commands

| Command | Purpose |
|---------|---------|
| `pytest` | Run all tests |
| `pytest -x` | Stop on first failure |
| `pytest -k "test_memory"` | Run tests matching pattern |
| `pytest --lf` | Run last failures |
| `pytest --co` | Collect only (list tests) |
| `ruff check src/` | Lint source |
| `mypy src/` | Type check |

---

## 5. Debugging Workflow

### 5.1 Debugging Layers

```
Layer 1: CLI Output
  └─ ai-company doctor run
  └─ ai-company status
  └─ ai-company orchestrator tick

Layer 2: Logs
  └─ Dashboard stdout logs
  └─ Python logging (LOG_LEVEL=DEBUG)

Layer 3: Data Files
  └─ .opencode/inbox.json (task queue)
  └─ orchestrator/approvals.yaml (approval state)
  └─ orchestrator/escalation.yaml (escalation events)
  └─ orchestrator/scheduler.yaml (scheduled tasks)

Layer 4: API Inspection
  └─ curl http://localhost:8420/api/dashboard
  └─ curl http://localhost:8420/api/agents
  └─ curl http://localhost:8420/api/tasks

Layer 5: Test Reproduction
  └─ Write a failing test that reproduces the bug
  └─ Fix the bug
  └─ Verify test passes
```

### 5.2 Debug Commands

```bash
# Enable debug logging
LOG_LEVEL=DEBUG ai-company orchestrator tick

# Inspect task queue
cat .opencode/inbox.json | python -m json.tool

# Inspect approval state
cat orchestrator/approvals.yaml

# Test specific API endpoint
curl http://localhost:8420/api/dashboard | python -m json.tool

# Check WebSocket connection
# Open browser DevTools → Console:
# const ws = new WebSocket('ws://localhost:8420/ws/dashboard');
# ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

### 5.3 Common Debug Scenarios

| Symptom | Diagnostic | Fix |
|---------|-----------|-----|
| Agent not executing | Check `inbox.json` for task status | Verify agent exists in registry |
| Approval stuck | Check `approvals.yaml` for status | `ai-company orchestrator approval pending` |
| Dashboard shows stale data | Check WebSocket connection | Refresh page, check server logs |
| Tests failing | Check test isolation | Use fixtures, avoid global state |
| Import errors | Check `pip install -e ".[dev]"` | Verify `.venv` is active |

---

## 6. Common Task Recipes

### 6.1 Add a New Department

```bash
# 1. Add department to company/departments.yaml
# 2. Add agents to company/agent-registry.json
# 3. Add KPIs to company/config/kpis.yaml
# 4. Regenerate
ai-company generate
# 5. Verify
ai-company departments list
ai-company dashboard kpi show <new-dept>
```

### 6.2 Create a New Workflow

```bash
# 1. Define workflow in company/workflows.yaml
# 2. Implement workflow steps in src/ai_company/workflow/engine.py
# 3. Add CLI commands if needed
# 4. Write tests
pytest tests/unit/test_workflow.py -v
# 5. Verify
ai-company workflows list
```

### 6.3 Debug a Failed Task

```bash
# 1. Check task status
ai-company orchestrator tick

# 2. Find the task in inbox.json
cat .opencode/inbox.json | python -m json.tool | grep -A 10 "<task-id>"

# 3. Check escalation events
ai-company orchestrator escalation pending

# 4. Check approval status
ai-company orchestrator approval pending

# 5. Check executor logs
# Look for error messages in stdout
```

### 6.4 Add a New LLM Provider

```bash
# 1. Add provider to company/models.yaml
# 2. Implement provider client in src/ai_company/llm/client.py
# 3. Add to circuit breaker in src/ai_company/llm/circuit_breaker.py
# 4. Write tests
# 5. Update docs/MODEL-ROUTING-POLICY.md
```

### 6.5 Deploy to Production

```bash
# 1. Run full test suite
pytest

# 2. Lint and type check
ruff check src/
mypy src/

# 3. Run diagnostics
ai-company doctor run

# 4. Generate production config
ai-company company run --config-dir config/prod

# 5. Start executor
ai-company executor start --poll-interval 5.0

# 6. Start dashboard
ai-company dashboard --host 0.0.0.0 --port 8420
```

---

## 7. Development Tools

### 7.1 Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    hooks:
      - id: mypy
        args: [--ignore-missing-imports]
```

### 7.2 IDE Integration

**VS Code settings.json:**
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.typeCheckingMode": "strict",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

### 7.3 Useful Aliases

```bash
# Add to .bashrc / .zshrc
alias ac="ai-company"
alias act="ai-company test"
alias acd="ai-company dashboard"
alias acdoc="ai-company doctor run"
alias acg="ai-company generate"
alias acl="ruff check src/"
alias act="mypy src/"
```

---

## 8. Performance Expectations

| Operation | Expected Time |
|-----------|---------------|
| `ruff check src/` | < 5s |
| `mypy src/` | < 10s |
| `pytest` (unit) | < 30s |
| `pytest` (all) | < 60s |
| `ai-company generate` | < 5s |
| `ai-company company run` | < 10s |
| `ai-company doctor run` | < 5s |
| Dashboard startup | < 3s |

---

## 9. Documentation Standards

| Doc Type | Location | Format |
|----------|----------|--------|
| Architecture | `docs/ARCHITECTURE.md` | Markdown |
| API Reference | `docs/API-REFERENCE.md` | Markdown |
| User Guide | `docs/USER-GUIDE.md` | Markdown |
| UX Design | `docs/ux/*.md` | Markdown |
| SOPs | `docs/sop-*.md` | Markdown with frontmatter |
| RACI | `docs/raci-*.md` | Markdown with frontmatter |
| Changelog | `CHANGELOG.md` | Keep a Changelog format |

### Doc Writing Rules

1. **One concept per section**
2. **Include working examples** (copy-pasteable)
3. **Test all code examples** before committing
4. **Use tables** for structured data
5. **Include "Gotchas"** sections for non-obvious behavior
