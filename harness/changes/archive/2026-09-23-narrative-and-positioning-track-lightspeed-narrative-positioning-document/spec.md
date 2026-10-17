# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: requirement-first
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: The public site lacked a single canonical narrative and had no provenance chain for quantitative claims.
- Current behavior: Positioning language and site numbers lived in scattered, partially contradictory sources; stash conflicts held stale 144-agent metadata.
- Source of evidence: `company-registry.yaml` (152 agents), `research/site-claims-index.yaml`, commit `2dbaaa9b`, validation scripts.

## User Scenarios And Success

- Primary user/system scenario: Marketing/agent teams pull one narrative source of truth; validators prove no claim drift before ship.
- Success criteria: One narrative doc; every claim ID classified; validators green; build green.
- Acceptance criteria: validate-drift, doc_drift, lint-ecl pass; conflicts resolved; `bun run build` succeeds.

## Non-Goals

- LLM integration for Ask LightSpeed.
- Launching Content Architecture Council agent cards.
- Phase 1 dynamic IA / conversion mechanics (next change).

## Constraints

- No invented numbers; honesty badges mandatory.
- Brand palette and 152-agent count are fixed canonical facts.

## Assumptions

- Updated-upstream conflict side is authoritative over stashed snapshots.

## Open Questions

- None remaining.

## Resolved Clarifications

- 3 unmapped LCA role titles: zero repo occurrences — removal is a no-op; closed 2026-09-23.
- Content Architecture Council launch: stays registry-only — closed 2026-09-23.
