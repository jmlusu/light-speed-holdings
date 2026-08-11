# Plan

## Technical Approach

### P0 - Critical (Sequential, Start Immediately)

**GAP-019: Agent Spec Validation** (lead-backend)
1. Add `AgentContext.validate()` method to `src/ai_company/executor/context.py`
   - Check for required fields: mission, responsibilities, tools
   - Log warnings for missing critical fields
   - Return validation result with errors/warnings
2. Add `ai-company agents validate` CLI command in `src/ai_company/cli/agents.py`
   - Accept agent ID or --all flag
   - Output validation results in human-readable format
   - Exit code 1 on validation failures
3. Integrate validation into generator output in `src/ai_company/generator.py`
   - Run validation after agent generation
   - Report any issues in generation summary

**Daemon Mode Completion** (lead-backend)
1. Verify `ai-company executor start --daemon` works end-to-end
   - Test process forking, PID file creation at `.opencode/executor.pid`
   - Verify daemon detaches from terminal
2. Test `executor status` command
   - Reads PID file, checks process alive, reports status
3. Test `executor stop` command
   - Sends SIGTERM, waits for graceful shutdown
   - Verifies PID file cleanup
4. Verify graceful shutdown
   - Flushes pending tasks to disk
   - Stops consolidation scheduler
   - Closes message bus connections cleanly

### P1 - High Priority (Parallel Tracks)

**OAuth2 / API Key Rotation** (lead-backend)
1. Add OAuth2 client credentials flow to `src/ai_company/llm/client.py`
   - Fail-closed: reject requests if auth unavailable
   - Token caching with TTL
2. Implement API key rotation in `src/ai_company/security/keys.py`
   - Scheduled rotation (configurable interval)
   - Graceful transition (overlap period)
   - Audit logging for rotation events

**Token Counting Integration** (lead-backend)
1. Add token counting hooks to LLM client in `src/ai_company/llm/client.py`
   - Track prompt tokens, completion tokens, total tokens
   - Per-request and cumulative counters
2. Expose via `ai-company llm usage` CLI command
   - Show usage by model, time period, agent

**CLI Type Hints & Docstrings** (lead-backend)
1. Add full type annotations to all CLI modules in `src/ai_company/cli/`
   - main.py, agents.py, executor.py, governance.py, dashboard.py, etc.
2. Add comprehensive docstrings (Google/NumPy style)
   - Module-level, class-level, function-level
   - Parameter descriptions, return types, exceptions

### P2 - Medium Priority (Test Coverage)

**CLI Command Tests** (qa_engineer)
1. Create test files in `tests/cli/` for all 26 commands
   - Test help output, success cases, error cases
   - Mock external dependencies
   - Verify exit codes and output format

**Dashboard Rate Limiting Tests** (qa_engineer)
1. Add tests in `tests/dashboard/test_rate_limiting.py`
   - Test 429 response on limit exceeded
   - Test CORS rejection for unauthorized origins
   - Test rate limit headers (X-RateLimit-*)

**Approval Escalation Tests** (qa_engineer)
1. Add tests in `tests/orchestrator/test_approval_escalation.py`
   - Test escalation flow (user → manager → director → VP → C-level)
   - Test timeout handling at each tier
   - Test expiry behavior
   - Test manual override

**Dashboard Security Hardening** (lead-frontend)
1. Review and harden dashboard security in `src/ai_company/dashboard/`
   - CSP headers, HSTS, X-Frame-Options
   - Input validation on all endpoints
   - Secure WebSocket connections

## Impacted Modules And Files

- `src/ai_company/executor/context.py` - AgentContext.validate()
- `src/ai_company/cli/agents.py` - validate command
- `src/ai_company/generator.py` - validation integration
- `src/ai_company/executor/main.py` - daemon mode verification
- `src/ai_company/llm/client.py` - OAuth2, token counting
- `src/ai_company/security/keys.py` - API key rotation (new)
- `src/ai_company/cli/*.py` - type hints & docstrings
- `tests/cli/` - CLI command tests (new/expanded)
- `tests/dashboard/test_rate_limiting.py` - rate limiting tests (new)
- `tests/orchestrator/test_approval_escalation.py` - approval tests (new)
- `src/ai_company/dashboard/` - security hardening

## Interfaces, Data, Permissions

- New CLI command: `ai-company agents validate [AGENT_ID] [--all]`
- New CLI command: `ai-company llm usage [--model MODEL] [--since DATE]`
- New module: `src/ai_company/security/keys.py` for key rotation
- Extended: `AgentContext` with `validate()` method
- Extended: LLM client with token counting hooks
- Dashboard: Rate limit headers, CORS config

## Spec Gaps Found From Planning

- None - all tasks have clear implementation paths

## Risks And Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Daemon mode has hidden bugs | Medium | High | Incremental verification, extensive logging |
| OAuth2 breaks existing auth | Low | High | Feature flag, fallback to current method |
| Token counting changes LLM client interface | Medium | Medium | Backward-compatible hooks, optional |
| Type hints reveal mypy errors | Medium | Low | Fix incrementally, use `# type: ignore` sparingly |
| Test flakiness in daemon tests | Medium | Medium | Isolated test fixtures, proper cleanup |

## Verification Plan

After each task:
```bash
ruff check src/ && mypy src/ && pytest
ai-company --help && ai-company executor --help && ai-company governance --help
```

Sprint completion:
- All 8 tasks marked complete
- Verification gates pass
- No test regressions (1,526+ tests passing)
- ECL change summary.md updated with outcomes
