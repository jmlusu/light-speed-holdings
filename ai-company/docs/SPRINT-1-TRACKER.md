# Sprint 1 Tracker

**Created:** 2026-07-19
**Owner:** Chief of Staff
**Status:** IN PROGRESS

---

## Executive Summary

Sprint 1 runs 3 parallel tracks. Code inspection complete — all gaps confirmed.

| Track | Owner | Status | Blocked By |
|-------|-------|--------|------------|
| A: Documentation | content_creator | 🟡 Pending | None |
| B: Code Hardening | lead-backend | 🟡 Pending | None |
| C: Audit Trail | TBD (after Track B) | 🔴 Blocked | Track B |

---

## Track A: Documentation

### Current State

| SOP | File | Status |
|-----|------|--------|
| Budget Approval (Finance) | `docs/sop-budget-approval.md` | ✅ Exists |
| Deployment (Engineering) | `docs/sop-deployment.md` | ✅ Exists |
| HR Onboarding | `docs/sop-hr-onboarding.md` | ✅ Exists |
| Incident Response (Engineering) | `docs/sop-incident-response.md` | ✅ Exists |
| Engineering (comprehensive) | `docs/sop/engineering-sop.md` | ✅ Exists |
| Terms of Service | — | ❌ Missing |
| Privacy Policy | — | ❌ Missing |
| Marketing | — | ❌ Missing |
| Sales | — | ❌ Missing |
| Customer Success | — | ❌ Missing |
| Legal | — | ❌ Missing |
| Operations | — | ❌ Missing |

### Task Checklist

| # | Task | SOP ID | Owner | Status |
|---|------|--------|-------|--------|
| A1 | Create Marketing SOP | SOP-MKT-001 | content_creator | ⬜ Pending |
| A2 | Create Sales SOP | SOP-SALES-001 | content_creator | ⬜ Pending |
| A3 | Create Customer Success SOP | SOP-CS-001 | content_creator | ⬜ Pending |
| A4 | Create Legal SOP | SOP-LEGAL-001 | content_creator | ⬜ Pending |
| A5 | Create Operations SOP | SOP-OPS-001 | content_creator | ⬜ Pending |
| A6 | Create Terms of Service | — | content_creator | ⬜ Pending |
| A7 | Create Privacy Policy | — | content_creator | ⬜ Pending |

**Dependencies:** None. All SOPs follow the established template pattern (see existing SOPs for frontmatter format, section structure, and CLI command references).

---

## Track B: Code Hardening

### Current State (Verified)

| Issue | File | Line(s) | Confirmed |
|-------|------|---------|-----------|
| HITL gate missing | `executor/agent_loop.py` | 204 | ✅ `self.runner.run_plan(plan=plan)` — no `hitl_gate`, `task_id`, or `agent_id` |
| EntityBase missing extra="ignore" | `models/models.py` | 80 | ✅ No `model_config` on class |
| Duplicate JSON parser | `llm/client.py` + `executor/agent_loop.py` | 123-167, 304-352 | ✅ Near-identical `_parse_response()` / `_parse_agent_response()` |
| print() in executor | `executor/loop.py` | 86,87,93,101,133,155,160,186,274 | ✅ 9 occurrences of `print()` |

### Task Checklist

| # | Task | File(s) | Owner | Status |
|---|------|---------|-------|--------|
| B1 | Fix HITL gate gap — pass `hitl_gate`, `task_id`, `agent_id` to `run_plan()` | `executor/agent_loop.py` | lead-backend | ⬜ Pending |
| B2 | Add `model_config = ConfigDict(extra="ignore")` to `EntityBase` | `models/models.py` | lead-backend | ⬜ Pending |
| B3 | Extract `parse_llm_json()` to `utils.py`, update both callers | `utils.py`, `llm/client.py`, `executor/agent_loop.py` | lead-backend | ⬜ Pending |
| B4 | Replace `print()` with `logging` in executor | `executor/loop.py` | lead-backend | ⬜ Pending |
| B5 | Run full verification: `pytest && ruff check src/ && mypy src/` | — | lead-backend | ⬜ Pending |

### B1 Details: HITL Gate Fix

**Current (line 204):**
```python
step_results = self.runner.run_plan(plan=plan)
```

**Required (matching pattern from `loop.py:167-172`):**
```python
step_results = self.runner.run_plan(
    plan=plan,
    hitl_gate=self.hitl,    # requires AgentLoop to accept/hold a HITLGate
    task_id=task_id,
    agent_id=resolved_name,
)
```

**Note:** `AgentLoop.__init__` does not currently accept a `hitl_gate` parameter. The constructor and `run()` method signature must be extended to accept and store the gate, OR the caller at `loop.py` must be updated to pass it when constructing `AgentLoop`.

### B2 Details: EntityBase Config

**Current (line 80):**
```python
class EntityBase(BaseModel):
    """Base for all named entities."""
    id: str = Field(..., min_length=1, description="Unique identifier")
    name: str = Field(default="", description="Human-readable name")
```

**Required:**
```python
from pydantic import ConfigDict

class EntityBase(BaseModel):
    """Base for all named entities."""
    model_config = ConfigDict(extra="ignore")
    id: str = Field(..., min_length=1, description="Unique identifier")
    name: str = Field(default="", description="Human-readable name")
```

### B3 Details: Shared parse_llm_json

**Source locations (near-identical code):**
- `llm/client.py:123-167` — `_parse_response(self, content: str)`
- `executor/agent_loop.py:304-352` — `_parse_agent_response(content: str)` (static)

**Target:** Extract to `src/ai_company/utils.py` as `parse_llm_json(content: str) -> dict[str, Any] | None`.

### B4 Details: Logging Migration

**All 9 print() occurrences in `executor/loop.py`:**

| Line | Current | Replacement |
|------|---------|-------------|
| 86 | `print(f"Executor started...")` | `logger.info(...)` |
| 87 | `print("Press Ctrl+C...")` | `logger.info(...)` |
| 93 | `print(f"  Processed {count}...")` | `logger.info(...)` |
| 101 | `print(f"\nExecutor stopped...")` | `logger.info(...)` |
| 133 | `print(f"\n[{task.id[:8]}] Processing...")` | `logger.info(...)` |
| 155 | `print(f"  LLM FAILED...")` | `logger.error(...)` |
| 160 | `print(f"  Provider error...")` | `logger.error(...)` |
| 186 | `print(f"  COMPLETED...")` | `logger.info(...)` |
| 274 | `print(f"  Delegated subtask...")` | `logger.info(...)` |

---

## Track C: Audit Trail Package

**Status:** 🔴 Blocked by Track B (B3 must complete first — shared utils extraction)

### Current State

- No `src/ai_company/audit/` directory exists
- No audit tests exist in `tests/unit/`

### Task Checklist

| # | Task | File(s) | Owner | Status |
|---|------|---------|-------|--------|
| C1 | Create `src/ai_company/audit/__init__.py` | — | TBD | ⬜ Blocked |
| C2 | Create `audit/events.py` — event dataclasses | — | TBD | ⬜ Blocked |
| C3 | Create `audit/writer.py` — append-only JSONL writer | — | TBD | ⬜ Blocked |
| C4 | Create `audit/reader.py` — query/filter reader | — | TBD | ⬜ Blocked |
| C5 | Write `tests/unit/test_audit.py` | — | TBD | ⬜ Blocked |
| C6 | Wire audit into executor loop (`executor/loop.py`) | — | TBD | ⬜ Blocked |
| C7 | Run full verification | — | TBD | ⬜ Blocked |

---

## Verification Gates

| Gate | Command | When |
|------|---------|------|
| After any source change | `cd ai-company && ruff check src/ && mypy src/ && pytest` | After each task |
| After Track B complete | `ruff check src/ && mypy src/ && pytest` | B5 |
| After Track C complete | `pytest tests/unit/test_audit.py -v` | C7 |
| After all tracks | Full `pytest` suite (248+ tests must pass) | Sprint close |

---

## Risk Log

| Risk | Impact | Mitigation |
|------|--------|------------|
| B1 HITL fix may change AgentLoop constructor signature | Callers may break | Grep for all `AgentLoop(` usages before changing |
| B3 shared util extraction touches 3 files | Merge conflicts if parallel edits | Do B3 as single atomic commit |
| Track C depends on Track B | Delay cascades | Track B is unblocked; start immediately |

---

## Revision History

| Date | Author | Changes |
|------|--------|---------|
| 2026-07-19 | Chief of Staff | Initial tracker — all gaps verified via code inspection |
