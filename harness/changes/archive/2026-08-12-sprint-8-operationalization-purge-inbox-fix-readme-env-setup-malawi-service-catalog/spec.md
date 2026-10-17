# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first (user approved the operationalization plan and said "start executing")
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: User wants to operationalize the 127-agent company and start
  providing services/products in Malawi. Review found the system is a simulation that has never
  run a real task.
- Current behavior: `.opencode/inbox.json` holds 177 junk test tasks (103× "do something",
  48× "Run migration", 25× "Do the thing"); `orchestrator/cost_tracker.json` shows $0.00 spent /
  0 LLM calls; `.opencode/audit.jsonl` has 0 events; no `.env` exists (`.env.example` only has
  placeholders); README says "27 agents / 24 CLI commands" (actual 127 agents / 30 commands);
  no service offering or pricing is defined anywhere.
- Source of evidence: inbox/cost/audit inspection 2026-08-12; grep for "27 agents"/"24 CLI";
  `Test-Path .env` = False.

## User Scenarios And Success

- Primary user/system scenario: CEO opens an empty, clean task queue, sees accurate agent
  counts in the README, has a place to put real API keys, and has a service catalog + pricing
  to take offers to the Malawi market.
- Success criteria:
  1. `inbox.json` contains zero junk tasks; SQLite mirror is consistent (0 junk rows).
  2. README accurately describes 127 agents and 30 CLI commands.
  3. `.env` exists (gitignored) with placeholder keys ready for real values.
  4. `docs/service-catalog-malawi.md` defines offers, pricing (MWK + USD), payment rails, delivery model.
- Acceptance criteria:
  - `MessageBus().get_all_tasks()` returns `[]` after purge.
  - `git status` shows inbox changes un-tracked (gitignored) and `.env` un-tracked.
  - `pwsh scripts/lint-ecl.ps1` passes.
  - `ruff`, `mypy`, `pytest` gates green.

## Non-Goals

- No LLM provider key provisioning (user must supply real keys).
- No dashboard UI changes in this sprint.
- No new source modules.
- No changes to archived harness changes or CHANGELOG history.

## Constraints

- `.opencode/inbox*.json`, `.env`, `data/*.db` are gitignored — purge must not break the
  MessageBus contract (JSON list at `<data root>/.opencode/inbox.json`).
- API keys must never be written to tracked files.
- ECL active-change rules apply; archive through `harness-change.ps1`.

## Assumptions

- The 177 inbox tasks are all test/junk data (verified by instruction-name grouping).
- User will fill real API keys into `.env` themselves.
- English is the primary business language; Chichewa can be added to the catalog later.

## Open Questions

- None blocking. (Real API-key values, pricing decisions, and final offer selection remain with the user.)

## Resolved Clarifications

- User approved starting with the fastest unblocks: purge inbox, fix README, draft service catalog.
