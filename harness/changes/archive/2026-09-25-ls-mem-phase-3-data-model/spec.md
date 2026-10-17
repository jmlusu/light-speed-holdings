# Spec

## Intake Review

- Intake type: Structured Change (retrospective)
- Input shape: plan-first (handoff §8 defines the deliverable)
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: Handoff §8 mandates
  `docs/architecture/LS-MEM-DATA-MODEL.md` — a versioned schema for the 13
  minimum memory types — as the Phase 3 deliverable before engine
  implementation.
- Current behavior: No Phase 3 ECL change existed; work proceeded without a
  tracked change record (process bypass flagged in reviewer consensus).
- Source of evidence: `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md` §8 and
  §34 (step 4 "Data Model"); Phase 2 archive "Next" note.

## User Scenarios And Success

- Primary user/system scenario: Engine implementers read the data model doc
  and implement DDL that satisfies every handoff §8 concept; auditors trace
  schema decisions to ADR-019/025 and the threat model.
- Success criteria: Doc exists; 13/13 types; minimum record fields preserved;
  schema versioned with forward-only migrations.
- Acceptance criteria: lint-ecl pass; cross-refs resolve; doc approved via
  this retrospective review.

## Non-Goals

- Implementing the schema in code (separate "Implementation" change).
- Replacing the JSON MemoryStore (forbidden by ADR-025, Phases 2–4).

## Constraints

- CEO-locked decisions from Phase 2 carry forward unchanged.
- Restricted classification never plaintext; redaction `[REDACTED_SECRET]`.

## Assumptions

- Handoff §8's example JSON is a floor, not a ceiling — "Do not hard-code
  this exact implementation if a better schema is justified, but preserve the
  underlying concepts."

## Open Questions

- None.

## Resolved Clarifications

- Retrospective record: no new clarification rounds needed; all inputs were
  already approved upstream (Phase 1, Phase 2, ADR-019, ADR-025).
