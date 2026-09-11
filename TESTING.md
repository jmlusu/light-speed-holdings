# LightSpeed Holdings — Testing Strategy & OpenCode Automation Guidelines

This document defines the testing strategy, verification protocols, and automation standards for the **LightSpeed Holdings** platform. It covers testing for React 18 frontend components, Three.js spatial stages, OpenCode agent runtime integration points, and backend Python services.

---

## 1. Testing Philosophy & Architecture

The LightSpeed Holdings platform operates as a unified dual-stack architecture:
- **Presentation Layer**: React 18 + Vite + Tailwind CSS + Three.js spatial components.
- **Orchestration Layer**: Python 3.12 + FastAPI + Typer CLI (`ai-company`).
- **OpenCode Runtime & Governance**: Markdown agent definitions (`.opencode/agents/*.md`), JSON task queues (`.opencode/inbox.json`), and cryptographic Human-in-the-Loop approval gates (`.opencode/pending_approvals.json`).

Our testing strategy ensures **zero-regression automated verification** across both frontend UI states and OpenCode agent automation workflows.

```
+-----------------------------------------------------------------------------------+
|                            AUTOMATED TESTING SUITE                                |
+-----------------------------------------------------------------------------------+
|  FRONTEND VERIFICATION              |  OPENCODE INTEGRATION & SCHEMA              |
|  - TypeScript (`tsc --noEmit`)      |  - Agent Card Syntax (`.opencode/agents/`)  |
|  - Vite Production Build            |  - Canonical 7-Tool Permission Gates        |
|  - Accessibility & ARIA Audit       |  - JSON Task Queue (`inbox.json`) Sync      |
|  - Hardware Component Interactions  |  - Cryptographic HITL Approval Gates        |
+-----------------------------------------------------------------------------------+
|  BACKEND & ORCHESTRATOR             |  CONTINUOUS INTEGRATION (CI/CD)             |
|  - Python Unit/Integration Tests    |  - Pre-commit Git Hooks                     |
|  - Ruff Linter & Formatter          |  - OpenCode Agent Verification Loops        |
|  - Mypy Static Type Safety          |  - GitHub Actions Test Workflows            |
+-----------------------------------------------------------------------------------+
```

---

## 2. React Component Testing Strategy

### 2.1 Core Component Coverage

Every major React component in `src/components/` must be validated against visual layout, state transitions, theme switches, and user interactions:

| Component | Key Testing Verification Points |
|-----------|--------------------------------|
| `CorporateLanding.tsx` | Verifies 4 Core Offerings rendering, regional SADC proposition, publications, Executive Briefing form submission, and accessible FAQ accordion searching/filtering. |
| `InteractiveOperatingModel.tsx` | Validates 3D canvas stage mounting, node inspection interactions, and theme switching (`light` vs. `dark`). |
| `TransformationDiagnostic.tsx` | Tests multi-step questionnaire state, score calculation algorithms, and diagnostic summary generation. |
| `TemplatesArtifacts.tsx` | Verifies rendering of OpenCode agent YAML cards, Policy-as-Code schemas, SADC compliance blueprints, and template copy/download triggers. |
| `TactileHardwareElements.tsx` | Tests physical feedback states for `TactileRockerSwitch`, `TactileRotaryKnob`, and `AcousticVentGrille`. |
| `MissionControl.tsx` & `CommandCenter.tsx` | Tests Real-time system status feeds, active agent metrics, token spend charts, and view switches. |
| `AgentRoster.tsx` & `AgentModal.tsx` | Verifies filtering 144 agents across 20 departments, searching agent cards, and displaying OpenCode tool permission blocks. |
| `TaskKanban.tsx` & `TaskModal.tsx` | Validates task column transitions (`PENDING` -> `IN_PROGRESS` -> `COMPLETED`), filtering by priority, and task execution logs. |
| `ApprovalsEscalations.tsx` | Tests Human-in-the-Loop (HITL) approval request rendering, decision triggers (`APPROVE`, `REJECT`), and cryptographic signature validation. |

### 2.2 Accessibility & WCAG AA Compliance

All interactive components must adhere to WCAG AA accessibility standards:
- **ARIA Labeling**: Accordions, tabs, and modals must include proper `aria-expanded`, `aria-controls`, `aria-selected`, `role="region"`, and `role="tablist"` attributes.
- **Keyboard Navigation**: Interactive elements must support `Tab`, `Space`, and `Enter` keypresses with visible focus rings (`focus-visible:ring-2 focus-visible:ring-orange-500`).
- **Color Contrast**: Text elements must maintain a minimum contrast ratio of 4.5:1 for body text and 7:1 for headers against light/dark background chassis.

---

## 3. OpenCode Integration Testing

OpenCode compatibility is tested directly against file schemas, tool permissions, and task queues:

### 3.1 Agent Definition & YAML Schema Validation

Agent definitions generated from `company-registry.yaml` must pass structural parsing tests:
- **Location**: `.opencode/agents/*.md`
- **Required Metadata**: `description`, `mode: subagent`, `permission:` blocks, `reports_to`.
- **Validation Command**:
  ```bash
  uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"
  ```

### 3.2 Canonical 7-Tool Permission Gate

OpenCode v2 runtimes enforce a strict 7-tool primitive vocabulary:
`read`, `edit`, `grep`, `list`, `bash`, `webfetch`, `task`.

- **Alias Resolution**: The test suite confirms that legacy aliases (`write` -> `edit`, `execute` -> `bash`, `delegate` -> `task`) are correctly mapped by `ToolRunner`.
- **Unknown Tool Rejection**: Any attempt to register an unrecognized tool (e.g. `code_interpreter`) must trigger an immediate validation error.

### 3.3 Inbox Queue & Approval Gate Synchronization

- **Task Queue Integrity**: `.opencode/inbox.json` must validate against Pydantic models in `src/ai_company/models/models.py`.
- **HITL Approval Sweep**: The `ApprovalGate` execution loop must automatically sweep expired `PENDING` requests into `EXPIRED` status, ensuring state hygiene.

---

## 4. Execution & Verification Commands

### 4.1 Frontend Verification Commands

```bash
# 1. Type Safety Check (Zero Code Generation)
npm run lint

# 2. Production Build Verification
npm run build

# 3. Local Production Preview
npm run preview
```

### 4.2 Backend & Orchestrator Testing Commands

```bash
# 1. Run Complete Pytest Suite (1856+ Unit & Integration Tests)
uv run pytest

# 2. Run Tests with Coverage Report
uv run pytest --cov=ai_company

# 3. Python Code Style & Syntax Check
uv run ruff check src/

# 4. Mypy Static Type Analysis
uv run mypy src/

# 5. Run System Health Diagnostics
uv run ai-company doctor
```

### 4.3 All-in-One Quality Gate

```bash
# Execute full lint, typecheck, and test suite via Makefile
make all-checks
```

---

## 5. CI/CD & OpenCode Automated Workflows

The repository uses automated pre-commit hooks and GitHub Actions to enforce code quality on every commit:

1. **Pre-commit Hooks (`.pre-commit-config.yaml`)**:
   - Trailing whitespace removal & end-of-file fixer.
   - YAML syntax validation (`check-yaml`).
   - Ruff linting and formatting (`ruff check`, `ruff format`).
   - Mypy static type verification.
   - Bandit security analysis.

2. **OpenCode Agent Verification**:
   - OpenCode agents reading this repository follow instructions in `AGENTS.md`.
   - Verification tools (`lint_applet` and `compile_applet`) are executed after component or state modifications to ensure green build outputs.
