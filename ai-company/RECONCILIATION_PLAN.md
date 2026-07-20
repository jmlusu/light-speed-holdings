# AI Company Builder Documentation Reconciliation Plan

## Executive Summary

The AI Company Builder has successfully resolved 13 of 20 architecture gaps, with 3 critical gaps (014, 015, 019) remaining open and 4 partially completed (005, 011, 018, 020). The AGENTS.md narrative is now misaligned with the source code reality — this document reconciles the narrative with verified source state and provides a focused integration hardening plan.

## Current State Verification

### Source-Verified Resolved Gaps (13/20)
✅ **GAP-001**: Executor routes all inbox I/O through MessageBus (`loop.py:182,228,270,355,397` use `self.bus.*`)
✅ **GAP-002**: File locking implemented (`store/file_store.py` atomic writes + platform locking)  
✅ **GAP-003**: Tier rules integrated (`tool_runner.py:361` calls `classify_tool_action()`)
✅ **GAP-004**: Non-blocking HITL gate (`hitl_gate.py:72` returns `Future`; executor auto-parks)
✅ **GAP-006**: WebSocket broadcast wired (`dashboard/api.py:111,129,144` call `broadcast_*`)
✅ **GAP-007**: Scheduler integrated (`loop.py:149` `scheduler.create_pending_tasks(self.bus)`)
✅ **GAP-008**: Escalation events persisted (`escalation.py:117,140` persist+restore events)
✅ **GAP-009**: CostTracker accumulators rebuilt (`cost_tracker.py:110,294` `_rebuild_accumulators()`)
✅ **GAP-010**: Dashboard auth/CORS hardened (`app.py:94,182,207` API-key + configurable CORS)
✅ **GAP-012**: AgentLoop priority forwarding (`agent_loop.py` forwards priority to router)
✅ **GAP-013**: KPI collectors wired (`dashboard/kpis/__init__.py` `ALL_COLLECTORS` contains 7 depts)
✅ **GAP-016**: Shell injection protection (`tool_runner.py:466` `shlex.split()`; no `shell=True`)
✅ **GAP-017**: Dead-letter queue implemented (`dead_letter.py` + `loop.py:174` stale detection)

### Partially Completed (4 gaps)
🟡 **GAP-005**: Memory integration wired; `consolidate()` not in executor loop
🟡 **GAP-011**: Dashboard write path uses MessageBus; KPI/mobile_API still read directly
🟡 **GAP-018**: Structured logging incomplete; 11 `print()` calls remain
🟡 **GAP-020**: Integration tests exist; full pipeline happy-path test pending

### Open (3 critical gaps)
🔴 **GAP-014**: BriefingGenerator uses private MessageBus method (`briefing.py:40` still calls `_load_tasks()`)
🔴 **GAP-015**: LLM retry provider cycling bug (`client.py:103-125` restarts chain from index 0 each attempt)
🔴 **GAP-019**: No AgentContext.validate() and no validation CLI command

## Integration-Focused Reconciliation Plan

### Phase 1: MessageBus Hardening (P0 - Critical, 2 hours)

**Priority**: Highest — resolves race conditions between executor and dashboard

**Tasks**:
1. **Dashboard KPI collectors**: Fix `mobile_api.py` and all 7 department KPI collectors to use MessageBus
   - Files: `dashboard/kpis/*`, `mobile_api.py`, `dashboard/ws.py`
   - Replace `.opencode/inbox.json` reads with `bus.get_inbox()`
   - Ensure `bus.get_all_tasks()` for dashboard aggregation

2. **Add public MessageBus.get_all_tasks()** (✅ already done)
   - Already implemented in `message_bus.py:130`
   - Used in `_read_all_tasks()` ✅ 
   - Requires wiring in dashboard KPI collectors

**Files Modified**:
- `src/ai_company/orchestrator/message_bus.py:130` (added)
- `src/ai_company/dashboard/api.py:62` (updated to use public method)
- `src/ai_company/orchestrator/briefing.py:40` (partially updated)
- All 7 KPI collector files and mobile_api.py

### Phase 2: Validation Framework (P0 - Critical, 3 hours)

**Priority**: High — prevents specification drift and improves code quality

**Tasks**:
1. **Add AgentContext.validate()** (GAP-019)
   - Files: `executor/context.py:31-100` (parse_agent_spec), `models/`
   - Implement schema validation using Pydantic models
   - Add validation warnings for missing critical fields (mission, responsibilities)
   - Integrate validation into generator pipeline

2. **Add validation CLI command** (GAP-019)
   - CLI: `ai-company agents validate`
   - Validates all `.opencode/agents/*.md` against schema
   - Reports warnings/errors with actionable remediation
   - Integrates with existing CLI structure in `src/ai_company/cli/`

3. **Complete structured logging** (GAP-018)
   - Replace 11 remaining `print()` calls in non-CLI modules
   - Add correlation IDs for end-to-end tracing
   - Use structured JSON format with consistent field names
   - Implement in: executor, agent_loop, tool_runner, hitl_gate

### Phase 3: Performance & Hardening (P1 - High, 6 hours)

**Priority**: Medium-high — race conditions and performance issues

**Tasks**:
1. **Memory consolidation** (GAP-005)
   - Add `memory.consolidate()` calls in executor loop
   - Prevent memory growth beyond bounds
   - Implement age-based pruning of old memories

2. **LLM retry cycling** (GAP-015)
   - Fix `client.py:103-125` provider chain cycling
   - Implement round-robin retry across providers
   - Add provider rotation state tracking per request

3. **Integration test suite** (GAP-020)
   - Create full pipeline integration test with mocked LLM
   - Test happy path: MessageBus → Executor → AgentLoop → ToolRunner → Completion
   - Mock cost tracker, memory, audit for isolated testing
   - Add to `tests/integration/` as `test_pipeline_integration.py`

### Phase 4: Architecture Updates (Documentation)

**Task**: Update AGENTS.md narrative

**Changes Required**:
- Replace stale foundation narrative with current reality (13 gaps resolved)
- Update sprint status alignment with source verification
- Remove references to pre-fix GAP prose, trust verified Status matrix
- Add integration hardening plan and recommendations
- Include concise sprint roadmap based on this reconciliation

## Technical Implementation Details

### Critical Race Condition Resolution

**Problem**: Dashboard writes competing with executor reads/writes of `inbox.json`

**Solution**: MessageBus hardending
- Implement single source of truth via MessageBus methods
- Use FileStore atomic writes with platform locking
- Apply pattern: all dashboard API writes → MessageBus.send_task/update

**Files**:
- `src/ai_company/dashboard/api.py:176,286,512,635,936,1012,1105` (multiple read sites)
- `dashboard/kpis/__init__.py:collect_all_kpis()` 
- `mobile_api.py` (lookup in source)

### Performance Analysis

**Metrics Required**:
- MessageBus vs direct file I/O comparison
- Concurrent read/write contention scenarios
- Memory growth tracking with consolidation
- HitL approval latency measurements

**Tools**:
- Add performance benchmarks in test suite
- Include `pytest-benchmark` integration
- Add profiling in executor metrics

## Risk Mitigation

### High Risks (Immediate)
1. **Dashboard race conditions** → Break dashboard functionality
   - Mitigation: MessageBus hardending (P0)
   - Cutover: Reduce to single write path

2. **Specification drift** → Dashboard shows stale/missing data
   - Mitigation: Validation framework (P1)  
   - Prevention: Agent spec validation CLI

### Medium Risks (Sprint 2)
1. **Memory explosion** → Production degradation
   - Mitigation: Consolidation in executor loop (P2)

2. **Provider retry bugs** → LLM fallback failures
   - Mitigation: Fix provider cycling (P2)

### Low Risks (Sprint 3)
1. **Documentation debt** → Technical confusion
   - Mitigation: AGENTS.md reconciliation (P3)

2. **Test coverage gaps** → Undetected regressions
   - Mitigation: Integration test suite (P3)

## Sprint Prioritization

### Sprint 2 (2 weeks)
**MessageBus Hardening** (P0)
- Complete KPI collector MessageBus migration
- Fix BriefingGenerator (GAP-014) to use public API
- Add performance benchmarks

**Validation Framework** (P1)
- Implement AgentContext.validate()
- Add validation CLI command
- Complete structured logging

### Sprint 3 (2 weeks) 
**Performance & Hardening** (P1)
- Memory consolidation integration
- LLM retry provider cycling fix
- Add integration test suite

**Architecture Updates** (P3)
- Update AGENTS.md narrative
- Complete documentation alignment

### Sprint 4 (1 week)
**Final Polish** (P3)
- Code quality review
- Complete documentation updates
- Final system verification

## Verification Criteria

### Technical
- **All messages flows through MessageBus**: No direct `inbox.json` reads/writes (except FileStore)
- **100% test coverage**: `pytest` passes without skips/ignores
- **Clean linting**: `ruff check src/` and `mypy src/` produce zero warnings
- **Security**: No `shell=True` usage, all commands via shlex.split, allowlist enforced

### Operational
- **Dashboard API**: All endpoints use MessageBus for task operations
- **WebSocket broadcasts**: All lifecycle events published
- **Memory management**: Consolidation running automatically
- **Escalation persistence**: Events preserved across restarts

### Business
- **Agent specs**: 100% validated before generation
- **Compliance**: Dashboard auth/CORS properly configured
- **Cost controls**: Budget tracking resilient to restart
- **Documentation**: AGENTS.md aligned with source reality

## Success Metrics

| Metric | Target | Verification Method |
|--------|--------|-------------------|
| MessageBus adoption | 100% of inbox I/O | Git grep for `inbox.json` reads |  
| Test pass rate | 100% (no skips) | `pytest` command output |
| Lint clean | Zero warnings | `ruff check src/` |
| Type coverage | Zero errors | `mypy src/` |
| Dashboard API writes | All via MessageBus | Code review |

## Conclusion

This reconciliation plan resolves the narrative-source alignment issue by:

1. **Acknowledging reality**: 13/20 gaps resolved, focusing on remaining work
2. **Prioritizing integration**: MessageBus hardening eliminates race conditions
3. **Quality focus**: Validation framework prevents drift and improves robustness
4. **Performance hardening**: Memory and retry fixes ensure production stability
5. **Documentation alignment**: AGENTS.md accurately reflects current state

The plan addresses the core Fullstack Engineer mandate: "Build end-to-end features across frontend and backend" by ensuring the integration seams are solid, secure, and traceable — enabling reliable agent orchestration at enterprise scale.

**Immediate next step**: Implement MessageBus hardening in dashboard KPI collectors and mobile API (P0, 2 hours).
