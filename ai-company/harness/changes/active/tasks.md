# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.

## Implementation

### P0 - Critical (Start Immediately)

- [x] T002 [P0] Add `AgentContext.validate()` method to `src/ai_company/executor/context.py` - validates mission, responsibilities, tools; logs warnings for missing critical fields
- [x] T003 [P0] Add `ai-company agents validate` CLI command in `src/ai_company/cli/agents.py` - accepts agent ID or --all flag, outputs validation results, exit code 1 on failures
- [x] T004 [P0] Integrate validation into generator output in `src/ai_company/generator.py` - run validation after generation, report issues in summary
- [x] T005 [P0] Verify `ai-company executor start --daemon` works end-to-end - daemon starts, creates PID file at `logs/executor-daemon.pid`, enters poll loop
- [x] T006 [P0] Test `executor status` command - reads PID file, checks process alive via psutil, reports status (running/stopped)
- [~] T007 [P0] Test `executor stop` command - sends terminate signal (psutil on Windows), but cleanup doesn't run due to Windows signal handling limitation
- [~] T008 [P0] Verify graceful shutdown - works on SIGTERM/SIGINT but not on psutil.terminate(); consolidation scheduler and message bus cleanup needs signal-triggered path

### P1 - High Priority (Parallel Tracks)

- [ ] T009 [P1] Add OAuth2 client credentials flow to `src/ai_company/llm/client.py` - fail-closed, token caching with TTL (DEFERRED to next sprint)
- [x] T010 [P1] Implement API key rotation in `src/ai_company/security/keys.py` - scheduled rotation, graceful transition, audit logging
- [x] T011 [P1] Add token counting hooks to LLM client in `src/ai_company/llm/client.py` - track prompt/completion/total tokens, per-request and cumulative
- [ ] T012 [P1] Expose token usage via `ai-company llm usage` CLI command - show usage by model, time period, agent (DEFERRED to next sprint)
- [x] T013 [P1] Add full type annotations to all CLI modules in `src/ai_company/cli/` - main.py, agents.py, executor.py, governance.py, dashboard.py, etc.
- [x] T014 [P1] Add comprehensive docstrings (Google/NumPy style) to all CLI modules - module, class, function level with params, returns, exceptions

### P2 - Medium Priority (Test Coverage)

- [x] T015 [P2] Create CLI command tests in `tests/cli/` for all 26 commands - help output, success cases, error cases, mock externals, verify exit codes
- [x] T016 [P2] Add dashboard rate limiting tests in `tests/dashboard/test_rate_limiting.py` - 429 response, CORS rejection, rate limit headers
- [x] T017 [P2] Add approval escalation tests in `tests/orchestrator/test_approval_escalation.py` - escalation flow, timeout handling, expiry behavior, manual override
- [x] T018 [P2] Dashboard security hardening in `src/ai_company/dashboard/` - CSP headers, HSTS, X-Frame-Options, input validation, secure WebSocket

## Validation

- [ ] T019 Run verification gates after each task: `ruff check src/ && mypy src/ && pytest`
- [ ] T020 Run CLI help checks after each task: `ai-company --help && ai-company executor --help && ai-company governance --help`
- [x] T021 Final sprint validation: all 1,526+ tests passing, ruff clean, mypy clean, no regressions

## Deferred Tasks

- T009 OAuth2 client credentials flow - fail-closed, token caching with TTL (P1)
- T012 `ai-company llm usage` CLI command - usage by model, time period, agent (P1)
