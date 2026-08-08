# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: Complete Sprint 4 quality & completeness deliverables to harden the AI Company Builder for production readiness
- Current behavior:
  - GAP-019: Agent spec validation missing (only open architecture gap)
  - Daemon mode code exists but unverified end-to-end
  - OAuth2/API key rotation not implemented (fail-open for network deploys)
  - Token counting estimated, not actual (cost accuracy issue)
  - CLI modules lack comprehensive type hints and docstrings
  - CLI command tests incomplete (26 commands)
  - Dashboard rate limiting tests missing
  - Approval escalation tests missing
- Source of evidence: Architecture review, test coverage reports, CLI audit

## User Scenarios And Success

- Primary user/system scenario:
  1. Developers run `ai-company agents validate` to catch spec issues early
  2. Operators run `ai-company executor start --daemon` for autonomous operation
  3. Network deployments use OAuth2/API keys with automatic rotation (fail-closed)
  4. Cost tracking uses actual token counts, not estimates
  5. CLI help shows complete type hints and docstrings
  6. All 26 CLI commands have test coverage
  7. Dashboard enforces rate limits with 429 responses
  8. Approval workflows handle escalation, timeout, expiry correctly

- Success criteria: All 8 tasks complete, verification gates pass, no regressions
- Acceptance criteria:
  - GAP-019: AgentContext.validate() method added, CLI command integrated, generator integration
  - Daemon: PID file management, status, stop, graceful shutdown all verified
  - OAuth2: Fail-closed authentication, key rotation implemented
  - Token counting: Integrated with LLM client for actual usage
  - Type hints: All CLI modules fully annotated with docstrings
  - Tests: 100% CLI command coverage, rate limiting tests, approval escalation tests

## Non-Goals

- Dashboard UI redesign
- New agent types or registry changes
- Database schema migrations
- Multi-tenant support

## Constraints

- Must maintain 1,526+ test baseline (no regressions)
- Ruff and mypy must remain clean
- Changes must be incremental and verifiable
- ECL change tracking required for all modifications

## Assumptions

- Existing daemon mode code in src/ai_company/executor/main.py is functional but untested
- LLM client abstraction supports token counting hooks
- OAuth2 library (authlib) available for integration
- pytest test infrastructure supports CLI command testing

## Open Questions

- None - all tasks defined with clear acceptance criteria

## Resolved Clarifications

- Delegation assignments confirmed per user directive
- Verification gates defined and agreed
- ECL change active throughout sprint
