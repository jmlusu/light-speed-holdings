# Onboarding Stack → SOP Mapping

**Ticket**: #24 — "Map the onboarding stack to the SOP's 8 steps"
**Branch**: `research/onboarding-stack-map`
**Generated**: 2026-08-12

---

## Executive Summary

This document traces each of the 8 steps in `docs/sop-hr-onboarding.md` to the current implementation in the AI Company Builder codebase. It identifies which steps are automated, which are manual, and where gaps exist.

---

## SOP Step-by-Step Mapping

| SOP Step | Current Implementation | Gap? | Details |
|----------|------------------------|------|---------|
| **1. Identify Staffing Need** | Manual (human writes request) | ✅ Yes | No automated intake form or ticketing system. Department heads must manually document: work needed, why existing agents can't handle it, tools/permissions required. |
| **2. Define Agent Role** | `HRService.onboard()` creates roster entry | ⚠️ Partial | `HRService.onboard()` (src/ai_company/services/hr.py:38) creates entry in `roster.yaml` with id, role, department, seniority, reports_to, status="onboarding". Also delegates 3 onboarding tasks via MessageBus to `hr-specialist`. **Gap**: Does not write to `company-registry.yaml` (source of truth for generation). CLI `ai-company hr onboard` (src/ai_company/cli/hr.py:54) writes directly to `hr/roster.yaml` with status="active" — bypasses service layer and onboarding tasks. |
| **3. Security Review** | Manual (CTO reviews config) | ✅ Yes | No automated security validation pipeline. CTO must manually review: least-privilege permissions, no unnecessary tool access, valid reporting hierarchy, no role conflicts. **Gap**: No `security-review` CLI command or automated policy check. |
| **4. Validate and Generate** | `ai-company generate` CLI | ✅ Implemented | `generate` command (src/ai_company/cli/main.py:304) → `sync_registry()` (registry/sync.py) → `AgentGenerator.generate_all()` (generator.py:203). Validates YAML structure, syncs to `company/agent-registry.json`, generates `.opencode/agents/*.md` with OpenCode v2 `permission:` blocks. Dry-run via `ai-company generate --dry-run` not implemented (SOP mentions it). |
| **5. Run Tests** | `pytest && ruff check src/ && mypy src/` | ✅ Implemented | Documented in SOP and `AGENTS.md`. Run via `uv run pytest && uv run ruff check src/ && uv run mypy src/`. Pre-commit hooks enforce on commit. Test fixtures use `_anchor_data_root` (conftest pattern) to isolate `DASHBOARD_DATA_DIR` per test. |
| **6. Human Approval** | `ai-company orchestrator approval pending` | ✅ Implemented | `ApprovalGate` (src/ai_company/orchestrator/approval.py) persists requests to `orchestrator/approvals.yaml`. CLI `approval pending/approve/reject` (src/ai_company/cli/orchestrator.py:248). `HITLGate` (src/ai_company/executor/hitl_gate.py) wraps for tool-execution approvals. **Gap**: No dedicated "agent onboarding approval" request type — uses generic `tool:` actions. |
| **7. Verify Deployment** | `ai-company agents list` | ✅ Implemented | `agents list` (src/ai_company/cli/agents.py:16) loads unified registry via `load_registry()` and displays executives, board, specialists with role, type, department, reports_to. |
| **8. Update Documentation** | Manual (ORGANIZATION.md, departments.yaml, RACI) | ✅ Yes | No automation. Must manually update: `docs/ORGANIZATION.md`, `company/departments.yaml` (if department changed), relevant RACI matrices. **Gap**: No `docs sync` command or post-generation hook. |

---

## Component Deep Dive

### HR Service Layer (`src/ai_company/services/hr.py`)

| Method | Purpose | Data Store | MessageBus Integration |
|--------|---------|------------|------------------------|
| `onboard(agent_id, role, department, seniority, reports_to)` | Creates roster entry with `status="onboarding"`, delegates 3 tasks to `hr-specialist` | `hr/roster.yaml` (via `BaseService._save_data`) | Creates 3 tasks: access/permissions setup, spec card generation, reporting assignment |
| `activate(agent_id)` | Sets `status="active"`, records `activated_at` | `hr/roster.yaml` | Records event to memory |
| `deactivate(agent_id, reason)` | Sets `status="inactive"`, records `deactivated_at`, creates handoff task to `chief-of-staff` if reason provided | `hr/roster.yaml` | Creates handoff task on reason |

**Key Insight**: The service layer uses `hr/roster.yaml` as its data root, but the **generator reads from `company-registry.yaml`**. These are disconnected — onboarding an agent via HR service does not automatically make it generatable.

### CLI: `ai-company hr onboard` (`src/ai_company/cli/hr.py:54`)

- Directly writes to `hr/roster.yaml` with `status="active"` (skips "onboarding" state)
- No MessageBus task delegation
- Simpler but bypasses the service layer's workflow

### Registry System (`src/ai_company/registry/`)

| Module | Role |
|--------|------|
| `loader.py` | `RegistryLoader.load_all()` — reads `company-registry.yaml` (agents) + 14 config files from `config/`. Partitions agents by `type`: executives, specialists, board. |
| `validator.py` | `RegistryValidator.validate()` — structural checks: company name/id, executive hierarchy, department-executive links, specialist reports_to/department validity, board existence, workflow steps, budget > 0. |
| `sync.py` | `sync_registry()` — converts YAML registry to legacy `company/agent-registry.json` (camelCase keys, derived `permission` field). `verify_sync()` checks drift. |
| `parser.py` / `resolver.py` | Reference resolution and parsing utilities. |

### AgentGenerator (`src/ai_company/generator.py`)

| Method | Purpose |
|--------|---------|
| `generate_all(clean=True)` | Full generation: loads registry, renders templates per agent type, writes `.opencode/agents/{id}.md` (underscores→hyphens), writes shared `operating-standards.md`, validates output. |
| `generate_from_registry(registry)` | Generates from `CompanyRegistry` Pydantic model (executives→`executive.md.j2`, departments→`department.md.j2`, specialists→`specialist.md.j2`, board→`board.md.j2`). |
| `validate_generated()` | Checks all generated files for OpenCode v2 compliance: frontmatter, required fields (`description`, `mode`, `permission`), forbidden `tools` field, valid mode/permission values. |
| `validate_naming()` | Ensures filenames use hyphens, not underscores. |

**Tool Normalization**: `_TOOL_MAP` converts registry tool names to OpenCode v2 canonical keys (`execute`→`bash`, `write`/`edit`→`edit`, `web_search`/`websearch`→`webfetch`, `delegate`→`task`). Permission block built as `{tool: "allow"}`.

### Approval System

| Component | File | Purpose |
|-----------|------|---------|
| `ApprovalGate` | `src/ai_company/orchestrator/approval.py` | Persists `ApprovalRequest` to `orchestrator/approvals.yaml` via `FileStore`. Supports `request_approval`, `approve`, `reject`, `expire`, `sweep_expired` (HITL expiry sweep per Sprint 7). |
| `HITLGate` | `src/ai_company/executor/hitl_gate.py` | Wraps `ApprovalGate` for tool-execution approvals. `request_and_wait()` returns `Future[bool]` (blocking or callback). `request_and_park()` / `resume_approved()` for non-blocking executor tick loop. Background polling thread with configurable timeout. |
| CLI | `src/ai_company/cli/orchestrator.py` | `approval pending/approve/reject` subcommands. |

**ApprovalRequest Fields**: `id`, `task_id`, `agent_id`, `action` (e.g., `tool:execute`), `description`, `tier`, `required_approvers`, `approved_by_list`, `status` (PENDING/APPROVED/REJECTED/EXPIRED), `requested_at`, `responded_at`, `response_by`, `notes`, `expires_at`.

### Test Gates & Fixtures

| Gate | Command | Purpose |
|------|---------|---------|
| Unit/Integration Tests | `pytest` | Runs test suite. Fixtures use `_anchor_data_root` (autouse) to monkeypatch `DASHBOARD_DATA_DIR` → `tmp_path`, isolating MessageBus/AuditWriter per test. |
| Lint | `ruff check src/` | Fast linting + formatting. |
| Type Check | `mypy src/` | Static type analysis. |

**`_anchor_data_root` Fixture** (in multiple test files, e.g., `tests/unit/test_executor.py:23`):
```python
@pytest.fixture(autouse=True)
def _anchor_data_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))
```
Ensures default-constructed `MessageBus`/`AuditWriter` stay inside per-test tmp dir instead of real `.opencode`.

---

## Gap Analysis Summary

| # | Gap | Impact | Suggested Fix |
|---|-----|--------|---------------|
| 1 | No staffing need intake system | Step 1 fully manual | Add `ai-company hr request-staffing` CLI + YAML template |
| 2 | HR onboarding doesn't write to `company-registry.yaml` | Step 2 disconnected from generation | Extend `HRService.onboard()` to also append to `company-registry.yaml` (or add sync step) |
| 3 | CLI `hr onboard` bypasses service layer | Inconsistent state (active vs onboarding) | Deprecate CLI direct write; route through `HRService` |
| 4 | No automated security review | Step 3 fully manual | Add `security-review` command: validate permissions against least-privilege policy, check hierarchy, detect conflicts |
| 5 | No `--dry-run` for generate | SOP documents it but not implemented | Add `gen.generate_all(dry_run=True)` that validates without writing |
| 6 | No dedicated onboarding approval type | Step 6 uses generic tool approval | Add `action: "onboard:agent"` request type with custom description |
| 7 | No post-generation doc sync | Step 8 fully manual | Add `docs sync` command or generator hook to update `ORGANIZATION.md`, `departments.yaml`, RACI |
| 8 | Two roster sources (`hr/roster.yaml` vs `company-registry.yaml`) | Data divergence risk | Unify or add bidirectional sync |

---

## Integration Flow Diagram

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  Department     │     │  HR Service      │     │  company-registry.  │
│  Head (Human)   │────▶│  .onboard()      │────▶│  yaml (SOURCE OF    │
│  "Need doc"     │     │  → hr/roster.yaml│     │  TRUTH)             │
└─────────────────┘     │  → MessageBus    │     └──────────┬──────────┘
                        │    tasks         │                │
                        └──────────────────┘                │
                                                           ▼
                        ┌──────────────────┐     ┌─────────────────────┐
                        │  CTO (Human)     │     │  Registry Loader    │
                        │  Security Review │────▶│  + Validator        │
                        └──────────────────┘     └──────────┬──────────┘
                                                           │
                        ┌──────────────────┐                │
                        │  Lead Engineer   │                ▼
                        │  ai-company      │────▶┌─────────────────────┐
                        │  generate        │     │  AgentGenerator     │
                        │  (--dry-run?)    │     │  → .opencode/agents/│
                        └──────────────────┘     │  → sync to JSON     │
                                                 └──────────┬──────────┘
                                                            │
                        ┌──────────────────┐                │
                        │  pytest/ruff/    │                ▼
                        │  mypy            │────▶┌─────────────────────┐
                        └──────────────────┘     │  Human Operator     │
                                                 │  approval pending   │
                                                 │  (ApprovalGate)     │
                                                 └──────────┬──────────┘
                                                            │
                        ┌──────────────────┐                │
                        │  ai-company      │                ▼
                        │  agents list     │────▶┌─────────────────────┐
                        └──────────────────┘     │  Verify Deployment  │
                                                 └──────────┬──────────┘
                                                            │
                        ┌──────────────────┐                │
                        │  Human: Update   │                ▼
                        │  ORGANIZATION.md,│────▶┌─────────────────────┐
                        │  departments.yaml│     │  Documentation      │
                        │  RACI            │     │  (MANUAL - GAP)     │
                        └──────────────────┘     └─────────────────────┘
```

---

## Files Referenced

| File | Purpose |
|------|---------|
| `docs/sop-hr-onboarding.md` | SOP definition (8 steps) |
| `src/ai_company/services/hr.py` | `HRService.onboard/activate/deactivate` |
| `src/ai_company/cli/hr.py` | `ai-company hr onboard/list/deactivate` |
| `src/ai_company/registry/loader.py` | `RegistryLoader.load_all()` |
| `src/ai_company/registry/validator.py` | `RegistryValidator.validate()` |
| `src/ai_company/registry/sync.py` | `sync_registry()`, `verify_sync()` |
| `src/ai_company/generator.py` | `AgentGenerator.generate_all/from_registry/validate_*` |
| `src/ai_company/orchestrator/approval.py` | `ApprovalGate`, `ApprovalRequest`, `ApprovalStatus` |
| `src/ai_company/executor/hitl_gate.py` | `HITLGate` (blocking/non-blocking approval) |
| `src/ai_company/cli/orchestrator.py` | `approval pending/approve/reject` |
| `src/ai_company/cli/agents.py` | `agents list/validate` |
| `src/ai_company/cli/main.py` | `generate`, `sync-registry` commands |
| `tests/unit/test_executor.py` | `_anchor_data_root` fixture pattern |
| `orchestrator/approvals.yaml` | Persisted approval requests |

---

## Recommendations

1. **Unify Data Model**: Make `HRService.onboard()` write to `company-registry.yaml` (append agent entry) so generation picks it up automatically.
2. **Add Security Review Automation**: Implement `ai-company security review <agent-id>` that checks permissions, hierarchy, conflicts.
3. **Implement `--dry-run`**: Add validation-only mode to `AgentGenerator.generate_all()`.
4. **Add Onboarding Approval Type**: Extend `ApprovalGate` with `action: "onboard:agent"` for Step 6.
5. **Post-Generation Doc Hook**: After successful generation, auto-update `ORGANIZATION.md` (agent list), `departments.yaml` (if new dept), and flag RACI updates.
6. **Deprecate CLI Direct Write**: Route `ai-company hr onboard` through `HRService` to ensure task delegation and consistent state.
7. **Add Staffing Request Intake**: `ai-company hr request-staffing` with template to formalize Step 1.

---

*End of ONBOARDING_STACK_MAP.md*
