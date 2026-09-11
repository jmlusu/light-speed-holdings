# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: audit-first (carried from the 2026-08-10 code review and the audit-fix checklist)
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: Post-review cleanup of tool-vocabulary drift, CWD-dependent registry loading, duplicated template boilerplate, and runtime hardening gaps (circuit-breaker error taxonomy, task leasing, unbounded in-memory state).
- Current behavior:
  - Agent cards mix legacy tool names (`websearch`, `web_search`, `code_interpreter`) that do not match canonical OpenCode v2 permission keys.
  - Operating Principles are rendered byte-identical into all 127 agent cards (boilerplate duplication).
  - Registry loading resolves paths relative to the process CWD, breaking CLI use from other directories.
  - Circuit breaker counts every failure equally; cost/decision logs grow without bound in long-running processes.
- Source of evidence: `docs/CODE_REVIEW_2026-08-10.md`, audit checklist, `docs/ARCHITECTURE-GAPS.md`.

## User Scenarios And Success

- Primary user/system scenario:
  1. Operator runs `ai-company` from any working directory; registry loads deterministically from the package root.
  2. Generated agent cards advertise only canonical OpenCode permission keys that match the runtime executor tooling.
  3. LLM provider failures are classified so the circuit breaker trips only on retry-able failures; auth problems fail fast without blacklisting.
  4. Executor/store state stays bounded and safe under concurrent access.
- Success criteria: All gates green (ruff/mypy/pytest), no regression, tool vocabulary canonical across cards and registry, registry CWD-independent.
- Acceptance criteria:
  - Registry resolves project root deterministically (`AI_COMPANY_ROOT` override with package-root fallback).
  - Zero residual `websearch`/`code_interpreter` in the registry and generated cards.
  - Operating Principles live in one shared `operating-standards.md`; `parse_agent_spec()` still returns all 5 principles via fallback.
  - Provider failures carry a `ProviderErrorCategory`; breaker ignores `auth`.
  - Task model carries lease fields; in-memory cost/decision logs are bounded.

## Non-Goals

- Rewriting the executor tool runner vocabulary (`code_interpreter` removal / `web_search` implementation) — deferred follow-up.
- Changing Success Metrics / Escalation content per agent type.
- OAuth2, dashboard auth-default, HITL-expiry, or mypy-strict work from the code review — separate changes.

## Constraints

- Must maintain the existing test baseline; no regressions.
- Ruff and mypy must remain clean.
- Backward compatible with legacy agent cards that still carry inline Operating Principles.

## Assumptions

- OpenCode v2 permission keys (`read`, `edit`, `grep`, `list`, `bash`, `webfetch`, `task`) are the canonical vocabulary.
- Package-root discovery works when the package is installed or run from source.

## Open Questions

- None — scope fully specified by the audit checklist and code review.

## Resolved Clarifications

- Shared-standards dedup applies to Operating Principles only; per-type sections stay inline.
- `cli/executor.py` DLQ re-enqueue delegation landed with the concurrency commit because it depends on `DeadLetterQueue.retry_dlq_task`.
