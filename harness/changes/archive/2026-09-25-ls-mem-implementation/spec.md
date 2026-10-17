# Spec

## Intake Review

- Intake type: Structured Change (retrospective)
- Input shape: plan-first (handoff §34 implementation sequence + Phase 3 data model + reviewer consensus)
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: Build the LS-MEM core system (handoff §34
  steps 5–16, 18) implementing the Phase 3 data model, and remediate all 7
  "FIX FIRST" blockers from the 4-reviewer consensus before Phase 4.
- Current behavior: Phase 0–3 docs complete; no engine code, no tests, no
  executor wiring recorded under ECL.
- Source of evidence: handoff §30 testing requirements, §31 acceptance
  criteria, §32 deliverables, §34 sequence; reviewer consensus memo
  (CoS/CTO/memory-owner/qa-lead, round 2).

## User Scenarios And Success

- Primary user/system scenario: Agents store/retrieve/search memories through
  the engine with classification-aware redaction; every external-transfer
  attempt passes the permission gateway (deny-by-default) with a hash-chained
  audit trail; executor injects quota-bounded context into sessions.
- Success criteria: mypy 0 errors; ruff clean; tests/memory green; gateway,
  audit, bridge, injector, CLI integration coverage; dual skill paths
  hash-identical; 7/7 consensus blockers closed.
- Acceptance criteria: all gates in the Validation Results table pass.

## Non-Goals

- Phase 4+ work (dashboard, Ollama default-on, external-provider integration).
- Replacing JSON MemoryStore (ADR-025 forbids Phases 2–4).
- Registering the lsmem CLI in `main.py` (recorded as follow-up).
- Fixing pre-existing unrelated test failures (dashboard/websocket/daemon).

## Constraints

- CEO-locked decisions from Phase 2 carry forward unchanged.
- Network deny-by-default; uncertain → BLOCK; Restricted never plaintext.
- No commits without explicit user instruction.

## Assumptions

- Reviewer claims verified against disk before acting; stale claims closed
  with evidence rather than "fixed".

## Open Questions

- None.

## Resolved Clarifications

- Typer 0.27 `Annotated` semantics: first positional of `Option(...)` is an
  option flag, not the default — default moves to the `= value` binding.
- `forget` = soft-delete (`ARCHIVED`), retrievable by ID for restore.
