# Sprint 1 Backlog -- AI Company Builder

**Sprint Goal**: Harden the codebase for production use and create foundational documentation.
**Duration**: 2 weeks
**Total Story Points**: 34 (Track A: 8 | Track B: 18 | Track C: 8)

---

## Validation Summary

| Claim | Verdict | Evidence |
|-------|---------|----------|
| HITL gate gap at agent_loop.py:204 | **CONFIRMED** | Line 204 calls runner.run_plan(plan=plan) without passing hitl_gate, task_id, or agent_id. ToolRunner supports HITL but AgentLoop never wires it up. |
| EntityBase needs extra="ignore" at models.py:80 | **CONFIRMED** | EntityBase(BaseModel) has no model_config. Extra fields cause ValidationError for all 12+ subclasses. |
| JSON parsing duplication in client.py and agent_loop.py | **CONFIRMED** | LLMClient._parse_response() (lines 123-167) and AgentLoop._parse_agent_response() (lines 304-352) are identical 3-strategy implementations. |
| print() to logging needed | **CONFIRMED** | 97 matches total. ~40 bare print() calls in executor/loop.py, orchestrator/briefing.py, orchestrator/message_bus.py, generator.py. CLI console.print() calls are appropriate Rich output. |

---

## Track A: Documentation (No Code Dependencies)

### A1. Department SOPs -- Remaining 6 of 10

**Priority**: 2 | **Points**: 4 | **Owner**: content-creator agent

| SOP | Status | File |
|-----|--------|------|
| Engineering | TODO | docs/sop-engineering.md |
| Marketing | TODO | docs/sop-marketing.md |
| Sales | TODO | docs/sop-sales.md |
| Customer Success | TODO | docs/sop-customer-success.md |
| Legal | TODO | docs/sop-legal.md |
| Operations | TODO | docs/sop-operations.md |
| HR Onboarding | DONE | docs/sop-hr-onboarding.md |
| Budget Approval | DONE | docs/sop-budget-approval.md |
| Incident Response | DONE | docs/sop-incident-response.md |
| Deployment | DONE | docs/sop-deployment.md |

**Acceptance Criteria**:
- [ ] Each SOP follows the format of existing SOPs (sop-hr-onboarding.md as template)
- [ ] Each SOP has: Purpose, Scope, Steps, Roles, Escalation, Metrics
- [ ] SOPs reference actual CLI commands where applicable (e.g., `ai-company workflow start <id>`)
- [ ] Reviewed by at least one department executive agent for accuracy

**Dependencies**: None

**Risk**: Content may drift from actual CLI capabilities. Mitigation: cross-reference `ai-company --help` output.

---

### A2. Terms of Service

**Priority**: 3 | **Points**: 2 | **Owner**: content-creator agent

**Acceptance Criteria**:
- [ ] Standard ToS covering: usage terms, IP ownership, liability limitations, termination
- [ ] References the AI nature of the tool (agent-generated content, automated decisions)
- [ ] Stored at docs/TERMS-OF-SERVICE.md
- [ ] Compatible with the project licensing intent

**Dependencies**: None

**Risk**: Legal review needed before public-facing use. Mitigation: mark as DRAFT until reviewed.

---

### A3. Privacy Policy

**Priority**: 3 | **Points**: 2 | **Owner**: content-creator agent

**Acceptance Criteria**:
- [ ] Covers: data collection (API keys via .env), local-only processing, no telemetry
- [ ] Clarifies that all data stays on user's machine
- [ ] Stored at docs/PRIVACY-POLICY.md
- [ ] Compatible with the project licensing intent

**Dependencies**: None

**Risk**: Must accurately reflect actual data flow. Mitigation: verify no external telemetry exists in source.

---

## Track B: Code Hardening

### B1. Fix HITL Gate Gap in AgentLoop

**Priority**: 1 (highest) | **Points**: 5 | **Owner**: lead-backend agent

**Problem**: `AgentLoop.run()` calls `self.runner.run_plan(plan=plan)` at line 204 without passing hitl_gate, task_id, or agent_id. This means ToolRunner.DANGEROUS_TOOLS (write, execute, code_interpreter) execute without human approval.

**Acceptance Criteria**:
- [ ] `AgentLoop.__init__()` accepts an optional `hitl_gate: HITLGate | None = None` parameter
- [ ] `AgentLoop.run()` passes hitl_gate, task_id, and agent_name to `self.runner.run_plan()`
- [ ] When hitl_gate is None, dangerous tools still execute (backward compatibility)
- [ ] New test in tests/unit/test_agent_loop.py: mock HITLGate, verify request_and_wait() is called for dangerous tools
- [ ] New test: verify denied HITL returns "denied" status in ToolCallRecord
- [ ] `ruff check src/ && mypy src/ && pytest` passes

**File Changes**:
- src/ai_company/executor/agent_loop.py -- add hitl_gate param, wire through to run_plan()
- tests/unit/test_agent_loop.py -- add HITL integration tests

**Dependencies**: None (Track B can start immediately)

**Risk**: Import cycle if hitl_gate imports from agent_loop. Mitigation: hitl_gate is already a standalone module; AgentLoop just needs to accept it as a parameter.

---

### B2. Add extra="ignore" to EntityBase

**Priority**: 1 (highest) | **Points**: 2 | **Owner**: lead-backend agent

**Problem**: EntityBase(BaseModel) at models.py:80 has no model_config. When YAML/JSON configs contain extra fields not defined in the model, Pydantic raises ValidationError. This affects all 12+ subclasses: Company, Policy, KPI, Agent, Task, Risk, DecisionRecord, BoardMember, Committee, BoardMeeting, Project, Workflow, Integration, Tool.

**Acceptance Criteria**:
- [ ] EntityBase gains `model_config = {"extra": "ignore"}`
- [ ] Existing tests still pass (no regressions)
- [ ] New test: create a Company with extra fields, verify no ValidationError
- [ ] New test: verify extra fields are silently dropped (not stored in model)
- [ ] `ruff check src/ && mypy src/ && pytest` passes

**File Changes**:
- src/ai_company/models/models.py -- add one line to EntityBase
- tests/unit/test_models.py -- add extra-field tolerance tests

**Dependencies**: None (can be done in parallel with B1)

**Risk**: Minimal. extra="ignore" is the standard Pydantic pattern for flexible schemas.

---

### B3. Extract parse_llm_json() Shared Utility

**Priority**: 2 | **Points**: 5 | **Owner**: lead-backend agent

**Problem**: Identical JSON parsing logic exists in two places:
- `LLMClient._parse_response()` -- src/ai_company/llm/client.py:123-167
- `AgentLoop._parse_agent_response()` -- src/ai_company/executor/agent_loop.py:304-352

Both implement the same 3-strategy approach: direct parse, markdown code block extraction, brace-depth scan.

**Acceptance Criteria**:
- [ ] New function `parse_llm_json(content: str) -> dict[str, Any] | None` in src/ai_company/utils.py
- [ ] `LLMClient._parse_response()` delegates to parse_llm_json()
- [ ] `AgentLoop._parse_agent_response()` delegates to parse_llm_json()
- [ ] Both callers maintain their existing public signatures (no breaking changes)
- [ ] Unit tests for parse_llm_json() cover: valid JSON, markdown-wrapped, brace-wrapped, malformed input, empty string
- [ ] `ruff check src/ && mypy src/ && pytest` passes

**File Changes**:
- src/ai_company/utils.py -- add parse_llm_json() function (file is currently empty)
- src/ai_company/llm/client.py -- replace _parse_response body with delegation
- src/ai_company/executor/agent_loop.py -- replace _parse_agent_response body with delegation
- tests/unit/test_utils.py -- new test file for the utility

**Dependencies**: None (can be done in parallel with B1, B2)

**Risk**: Low. The function is a pure utility with no side effects.

---

### B4. Replace print() with logging

**Priority**: 3 | **Points**: 3 | **Owner**: lead-backend agent

**Problem**: 40+ bare print() calls in non-CLI modules should use Python's logging module for proper log levels, configurability, and production readiness.

**Scope** (bare print() only, NOT console.print()):
- src/ai_company/executor/loop.py -- 10 calls
- src/ai_company/orchestrator/briefing.py -- 1 call
- src/ai_company/orchestrator/message_bus.py -- 1 call
- src/ai_company/generator.py -- 4 calls

**Acceptance Criteria**:
- [ ] All bare print() in scope replaced with logger.info() / logger.debug() / logger.warning() as appropriate
- [ ] Each module gets `logger = logging.getLogger(__name__)` at module level
- [ ] CLI modules (cli/*.py) keep console.print() -- those are user-facing output, not logging
- [ ] `ruff check src/ && mypy src/ && pytest` passes
- [ ] `ai-company --help` still works

**File Changes**:
- src/ai_company/executor/loop.py
- src/ai_company/orchestrator/briefing.py
- src/ai_company/orchestrator/message_bus.py
- src/ai_company/generator.py

**Dependencies**: None (can be done in parallel)

**Risk**: Low. Must ensure no logger calls replace user-facing CLI output.

---

### B5. Write Tests for B1-B4

**Priority**: 2 | **Points**: 3 | **Owner**: lead-backend agent

**Acceptance Criteria**:
- [ ] tests/unit/test_agent_loop.py -- HITL gate integration (covered in B1)
- [ ] tests/unit/test_models.py -- extra-field tolerance (covered in B2)
- [ ] tests/unit/test_utils.py -- parse_llm_json() unit tests (covered in B3)
- [ ] All tests pass with pytest
- [ ] Test coverage >= 80% for changed modules

**Dependencies**: B1, B2, B3 must be complete (this is the verification pass)

**Risk**: None. Tests are the safety net.

---

## Track C: Audit Trail Package

### C1. Create src/ai_company/audit/ Package

**Priority**: 2 | **Points**: 8 | **Owner**: lead-backend agent

**Problem**: No structured audit trail for agent actions. When things go wrong, there is no way to trace what happened, who approved what, or which tools were called.

**Acceptance Criteria**:

#### C1a. src/ai_company/audit/__init__.py
- [ ] Exports public API: AuditEvent, AuditWriter, AuditReader

#### C1b. src/ai_company/audit/events.py
- [ ] AuditEvent Pydantic model with fields:
  - event_id: str (UUID)
  - timestamp: str (ISO 8601)
  - event_type: AuditEventType enum
  - agent_id: str
  - task_id: str
  - tool: str (optional, for tool events)
  - args: dict[str, Any] (optional)
  - result: dict[str, Any] (optional)
  - metadata: dict[str, Any] (optional)
- [ ] AuditEventType enum: tool_call, tool_result, hitl_approved, hitl_denied, task_created, task_completed, error

#### C1c. src/ai_company/audit/writer.py
- [ ] AuditWriter class:
  - __init__(self, path: str | Path = ".opencode/audit.jsonl")
  - write(self, event: AuditEvent) -> None
  - write_batch(self, events: list[AuditEvent]) -> None
  - Thread-safe (file locking or append-only pattern)
  - Auto-creates parent directories

#### C1d. src/ai_company/audit/reader.py
- [ ] AuditReader class:
  - __init__(self, path: str | Path = ".opencode/audit.jsonl")
  - read_all(self) -> list[AuditEvent]
  - read_by_task(self, task_id: str) -> list[AuditEvent]
  - read_by_agent(self, agent_id: str) -> list[AuditEvent]
  - read_by_type(self, event_type: str) -> list[AuditEvent]
  - read_since(self, since: str) -> list[AuditEvent]

#### C1e. tests/unit/test_audit.py
- [ ] Test AuditEvent creation and validation
- [ ] Test AuditWriter.write() and AuditReader.read_all() round-trip
- [ ] Test filtering by task_id, agent_id, event_type
- [ ] Test thread-safety (concurrent writes)
- [ ] Test malformed JSONL line handling (graceful skip)
- [ ] `ruff check src/ && mypy src/ && pytest` passes

**File Changes**:
- src/ai_company/audit/__init__.py (new)
- src/ai_company/audit/events.py (new)
- src/ai_company/audit/writer.py (new)
- src/ai_company/audit/reader.py (new)
- tests/unit/test_audit.py (new)

**Dependencies**: Track B should be complete first (B1 wires HITL gate, B3 extracts shared utility). Audit events should be emitted from the same code paths we are hardening.

**Risk**: JSONL format is simple but not query-efficient at scale. For Sprint 1, JSONL is fine. If we need SQL-level queries later, we can add a SQLite backend.

**Integration Point**: After C1 is done, a follow-up task would wire AuditWriter into AgentLoop, ToolRunner, and HITLGate to emit events automatically. That is Sprint 2 scope.

---

## Dependency Graph

```
Track A (parallel)          Track B (parallel)           Track C
==================          ===================          ==================
A1 (SOPs)                   B1 (HITL gate) -----------> C1 (audit pkg)
A2 (ToS)                    B2 (EntityBase)
A3 (Privacy)                B3 (parse_llm_json)
                            B4 (print to logging)
                            B5 (tests) <-- B1+B2+B3
```

**Critical path**: B1 -> C1 -> (Sprint 2: wire audit into loop)

---

## Definition of Done

### Track A -- Documentation

| Criterion | Verification |
|-----------|--------------|
| All SOPs exist and follow template | `ls docs/sop-*.md` shows 10 files |
| SOPs reference actual CLI commands | Grep for `ai-company` in each SOP |
| ToS and Privacy Policy exist | `ls docs/TERMS-OF-SERVICE.md docs/PRIVACY-POLICY.md` |
| No broken internal links | grep for cross-references |

**What could go wrong**:
- SOPs drift from actual CLI capabilities -- cross-reference `ai-company --help`
- Legal docs are inaccurate -- mark as DRAFT until reviewed

### Track B -- Code Hardening

| Criterion | Verification |
|-----------|--------------|
| HITL gate wired into AgentLoop | grep for hitl_gate in agent_loop.py |
| EntityBase tolerates extra fields | `pytest tests/unit/test_models.py -k extra` |
| parse_llm_json shared and tested | `pytest tests/unit/test_utils.py -k parse` |
| No bare print() in non-CLI modules | grep for bare `print(` excluding cli/ and doctor/ |
| All existing tests still pass | `pytest` (248+ tests) |
| Lint and type check pass | `ruff check src/ && mypy src/` |

**What could go wrong**:
- HITL gate introduces import cycle -- verify with `mypy src/`
- extra="ignore" hides real config errors -- add strict-mode flag later
- parse_llm_json changes parsing behavior -- existing tests catch regressions

### Track C -- Audit Trail

| Criterion | Verification |
|-----------|--------------|
| Audit package imports cleanly | `python -c "from ai_company.audit import AuditEvent, AuditWriter, AuditReader"` |
| Round-trip write/read works | `pytest tests/unit/test_audit.py` |
| JSONL format is correct | `head -1 .opencode/audit.jsonl \| python -m json.tool` |
| Malformed lines are skipped | Test with corrupted JSONL line |

**What could go wrong**:
- File locking issues on Windows -- use append-only pattern, no complex locks
- Audit file grows unbounded -- add rotation in Sprint 2
- Performance impact from writing on every tool call -- batch writes in hot paths

---

## Blockers and Risks

### Blockers

| ID | Blocker | Impact | Mitigation |
|----|---------|--------|------------|
| BLK-1 | No existing audit/ package directory | C1 starts from zero | Clean slate, no conflicts |
| BLK-2 | utils.py is empty (no existing code to conflict with) | B3 is safe | Good -- clean insertion point |
| BLK-3 | No import cycles detected | B1 safe to proceed | HITLGate already standalone |
| BLK-4 | 248 existing tests must stay green | All tracks | Run pytest after every change |

### Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|------------|--------|------------|
| R1 | HITL gate blocks all dangerous tools by default | Medium | High | AgentLoop passes None gate by default for backward compat |
| R2 | extra="ignore" silently drops real config errors | Low | Medium | Add strict mode flag in Sprint 2 |
| R3 | parse_llm_json changes edge case behavior | Low | Medium | Comprehensive test suite before refactor |
| R4 | JSONL audit file grows unbounded | Medium | Low | Add rotation in Sprint 2 |
| R5 | SOP content does not match actual CLI | Medium | Low | Cross-reference ai-company --help output |
