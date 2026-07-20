# Engineering Standard Operating Procedure

**Document ID:** SOP-ENG-001
**Department:** Engineering / Technology
**Owner:** Chief Technology Officer (CTO)
**Classification:** Internal
**Last Updated:** July 2026

---

## 1. Purpose

This Standard Operating Procedure establishes the authoritative process for software development, code review, deployment, and incident response within Light Speed Holdings' AI Company Builder project. It defines how engineering agents and human contributors collaborate to produce reliable, secure, and maintainable software.

## 2. Scope

This SOP applies to all software engineering activities including:

- Feature development for the AI Company Builder CLI and runtime
- Generator and template modifications (`company-registry.yaml` to `.opencode/agents/`)
- Orchestrator and executor changes (`MessageBus`, `AgentLoop`, `CostTracker`, `HITLGate`)
- LLM provider integrations and model routing (`ModelRouter`, `LLMClient`)
- Dashboard and API changes (FastAPI CEO Dashboard)
- Doctor checks and health monitoring
- Tests, CI pipelines, and deployment automation
- Infrastructure configuration (Docker, Makefile, pyproject.toml)

## 3. Roles and Responsibilities

| Role | Agent/Person | Responsibilities |
|------|-------------|-----------------|
| CTO | `cto` (executive) | Architectural decisions, code review approval, release sign-off |
| Lead Developer | `lead_dev` | Sprint planning, technical design, code review, mentoring |
| Development Agents | Specialists | Feature implementation, bug fixes, test writing |
| Chief of Staff | `chief_of_staff` | Cross-department coordination, resource allocation |
| Human Operator | CEO / Founder | Final approval on architectural changes, production deployments |

## 4. Development Workflow

### 4.1 Task Intake

All engineering work originates as a Task in the `MessageBus`:

```
.opencode/inbox.json
```

Tasks arrive with a status of `pending` and one of the following priorities:

| Priority | Response SLA | Description |
|----------|-------------|-------------|
| `critical` | 30 minutes | Production outage, security vulnerability |
| `high` | 4 hours | Blocking bug, customer-reported issue |
| `medium` | 24 hours | Feature work, enhancements |
| `low` | 1 week | Tech debt, minor improvements |

### 4.2 Development Branch Workflow

1. **Create a feature branch** from `main`:
   ```
   git checkout -b feature/<ticket-id>-<short-description>
   ```

2. **Write or update tests first** (TDD encouraged):
   - Unit tests in `tests/unit/`
   - Integration tests in `tests/integration/`
   - All new functions must have corresponding pytest tests

3. **Implement the change**:
   - Follow PEP 8 (enforced by `ruff check src/`)
   - Line length limit: 100 characters
   - Use Python 3.12+ syntax and features
   - Type annotations required on all public functions

4. **Run the verification suite** before committing:
   ```bash
   ruff check src/          # Lint
   mypy src/                # Type check
   pytest                   # Tests
   ```

5. **Commit with a conventional message**:
   ```
   feat(executor): add parallel tool execution support
   fix(cost_tracker): correct daily budget reset at midnight
   docs(sop): update engineering procedures
   ```

### 4.3 Code Review Process

Every change requires at least one review before merge:

1. **Open a Pull Request** with a clear description of what changed and why
2. **Automated checks must pass**:
   - `ruff check src/` (linting)
   - `mypy src/` (type checking)
   - `pytest` (test suite)
3. **Human review required** for:
   - Changes to `executor/` (agent loop, HITL gate, tool runner)
   - Changes to `orchestrator/` (message bus, approval gate, escalation)
   - Changes to `llm/` (cost tracker, model router, provider chain)
   - Any change affecting agent permissions or security boundaries
4. **CTO approval required** for:
   - Architectural changes (new modules, major refactors)
   - Changes to `company-registry.yaml` or the Jinja2 template
   - Database schema changes or migration scripts
   - Changes to budget/financial logic in `CostTracker`

### 4.4 Review Checklist

Reviewers must verify:

- [ ] Code follows PEP 8 and project conventions
- [ ] Type annotations are present on all public APIs
- [ ] Tests cover new code paths (aim for 80%+ coverage)
- [ ] No secrets or API keys in source code
- [ ] No path traversal vulnerabilities in `ToolRunner._safe_path()`
- [ ] HITL gate is invoked for dangerous tools (`write`, `execute`, `code_interpreter`)
- [ ] Cost tracking records are emitted for LLM calls
- [ ] Error messages are descriptive and actionable
- [ ] Documentation is updated if public APIs changed

## 5. Deployment Process

### 5.1 Pre-Deployment Verification

Before any production deployment:

1. Run the full verification suite:
   ```bash
   ruff check src/ && mypy src/ && pytest
   ```

2. Regenerate agents from the registry to verify template integrity:
   ```bash
   ai-company generate
   ```

3. Verify the CLI is functional:
   ```bash
   ai-company --help
   ai-company doctor run
   ```

4. Verify Docker build succeeds:
   ```bash
   docker compose build
   ```

### 5.2 Deployment Steps

1. Merge the approved PR to `main`
2. Tag the release:
   ```
   git tag -a v<semver> -m "Release v<semver>"
   ```
3. Build and push the Docker image:
   ```bash
   docker compose build && docker compose push
   ```
4. Run the `doctor` command on the target environment:
   ```bash
   ai-company doctor run
   ```
5. Verify the CEO Dashboard health endpoint:
   ```
   GET /health -> {"status": "ok"}
   ```

### 5.3 Rollback Procedure

If a deployment introduces issues:

1. Revert the merge commit on `main`
2. Re-deploy the previous Docker image tag
3. Run `ai-company doctor run` to verify system health
4. Notify the Chief of Staff via the `MessageBus` with a `critical` priority task
5. Document the incident in a postmortem (see Section 7)

## 6. Incident Response

### 6.1 Incident Severity Levels

| Level | Definition | Response Time | Example |
|-------|-----------|--------------|---------|
| SEV-1 | Complete system outage | Immediate | MessageBus failure, all agents unresponsive |
| SEV-2 | Major feature degraded | 30 minutes | HITL gate timeout, cost tracker logging failure |
| SEV-3 | Minor issue | 4 hours | Dashboard display bug, non-critical CLI error |
| SEV-4 | Cosmetic / informational | 1 week | Typo in help text, minor formatting issue |

### 6.2 Incident Response Workflow

1. **Detect**: Automated monitoring (doctor checks) or human report
2. **Triage**: CTO assigns severity level and initiates response
3. **Contain**:
   - For SEV-1: Immediately halt affected agents via `MessageBus` task cancellation
   - For SEV-2: Disable affected feature flag or route around the issue
4. **Resolve**: Implement and deploy a fix following the standard deployment process
5. **Review**: Conduct a postmortem within 48 hours using the `PostmortemStore`:
   ```python
   from ai_company.orchestrator.escalation import PostmortemStore, Postmortem
   store = PostmortemStore()
   postmortem = Postmortem(
       incident_id="INC-<task_id>",
       title="Brief description",
       severity="high",
       affected_agent="<agent_id>",
       department="Engineering",
   )
   store.save(postmortem)
   ```

### 6.3 Escalation Path

The `EscalationManager` defines automated escalation rules:

- **Tool execution failure** (3 consecutive failures) -> Escalate to CTO
- **Budget exceeded** (`CostTracker.check_budget()` returns False) -> Escalate to CFO
- **HITL timeout** (30 minutes without human response) -> Escalate to Chief of Staff
- **Security violation** (path traversal in `ToolRunner`) -> Escalate to CTO + immediate halt

## 7. Quality Standards

### 7.1 Code Quality Metrics

| Metric | Target | Enforcement |
|--------|--------|-------------|
| Test coverage | 80%+ | `pytest --cov` |
| Lint violations | 0 | `ruff check src/` |
| Type errors | 0 | `mypy src/` |
| Maximum function length | 50 lines | Manual review |
| Maximum file length | 500 lines | Manual review |

### 7.2 Documentation Requirements

- All public functions must have docstrings (Google style)
- All modules must have a module-level docstring explaining purpose
- Architecture decisions are recorded in `docs/ARCHITECTURE.md`
- Changes to the agent template require updates to `docs/` and `AGENTS.md`

### 7.3 Security Requirements

- All file operations in `ToolRunner` are sandboxed to `PROJECT_ROOT`
- Path traversal is blocked by `ToolRunner._safe_path()`
- Dangerous tools (`write`, `execute`, `code_interpreter`) require HITL approval
- API keys must be stored in environment variables, never in source code
- The `AgentLoop` enforces daily and per-task budget caps via `CostTracker`

## 8. Escalation Procedures

| Condition | Escalate To | SLA |
|-----------|------------|-----|
| Architecture decision needed | CTO | 4 hours |
| Cross-team dependency | Chief of Staff | 8 hours |
| Budget approval needed (> $100) | CFO | 24 hours |
| Security vulnerability discovered | CTO + CEO | Immediate |
| Production outage lasting > 15 min | CTO + CEO | Immediate |
| Agent misbehavior or loop | Chief of Staff | 1 hour |

## 9. Key Performance Indicators

| KPI | Target | Frequency | Owner |
|-----|--------|-----------|-------|
| Deployment frequency | 2+ per week | Weekly | CTO |
| Mean time to recovery (MTTR) | < 1 hour | Per incident | CTO |
| Change failure rate | < 5% | Monthly | CTO |
| Test coverage | >= 80% | Per release | Lead Dev |
| Lint/type error count | 0 | Per commit | All engineers |
| Sprint velocity | >= 80% of committed | Biweekly | Lead Dev |

## 10. Compliance Requirements

- All code changes must be traceable to a Task in the `MessageBus`
- Cost tracking logs (`results/cost_log.jsonl`) must be retained for 90 days
- Postmortems must be completed within 48 hours of SEV-1/SEV-2 incidents
- HITL approval records in `orchestrator/approvals.yaml` must not be manually edited
- Escalation events must be logged in `orchestrator/escalation.yaml`

## 11. Related Documents

- `docs/ARCHITECTURE.md` - System architecture overview
- `docs/ECL.md` - Evolutionary Change Lifecycle
- `docs/MODEL-ROUTING-POLICY.md` - LLM routing and tier configuration
- `docs/DEVOPS-PLAN.md` - DevOps and infrastructure plan
- `docs/raci-deployment.md` - RACI matrix for deployment
- `docs/raci-escalation.md` - RACI matrix for escalation

---

*This document is maintained by the Engineering department. Updates require CTO approval.*
