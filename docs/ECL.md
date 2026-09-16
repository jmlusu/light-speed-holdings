# ECL — Change Lifecycle

## 1 Purpose

This document defines how changes are tracked, reviewed, and validated in the AI Company Builder project. It is the operating manual for AI agents working in this repository.

## 2 When To Create a Change

Create an ECL change when:

- Work spans more than two files.
- Work touches APIs, data models, permissions, or architecture.
- Work needs user confirmation or plan review.
- Work needs multi-step tests or regression checks.
- Work is likely to exceed 20 minutes.

Small, local fixes (copy, comments, formatting, single-file bug fixes with no interface/data/architecture impact) can skip ECL changes. Record validation in the final response.

## 3 Change Lifecycle

```text
new -> active/in_progress
active -> close completed -> archive/YYYY-MM-DD-slug
active -> close abandoned -> archive/YYYY-MM-DD-slug
active -> close blocked -> archive/YYYY-MM-DD-slug
active -> park -> parking/YYYY-MM-DD-slug
parking/YYYY-MM-DD-slug -> resume -> active
```

Rules:

- `active/` allows only one change at a time.
- Starting a new task must never overwrite an existing active task.
- `INDEX.json` is derived from `parking/*/summary.md` and `archive/*/summary.md`.
- Hooks and CI may validate, but must not auto-write docs or move changes.

## 4 Stage-Boundary Protocol

Before moving between stages (intake → spec → plan → implement → validate), update `summary.md` front matter fields. The `phase` field tracks current stage; valid values are `intake`, `spec`, `plan`, `implement`, `validate`. When entering `validate`, populate `validation_results` with an array of gate outcomes (e.g., `lint-ecl.ps1: PASS`, `ruff check src/: PASS`, `mypy src/: PASS`, `pytest: 1856 passed`).

Archive gates:

- `validation_status` must be exactly `pass` (not `passed`, `unknown`, or `fail`) before archiving. Changes without validation evidence must remain active or be parked.
- `phase` must be `validate` or `implement` before archiving. `done` is not a valid archive phase; changes archived at `phase: "plan"` indicate implementation was skipped.
- `spec_review` must be resolved (value `approved` or equivalent recorded in reviews/) before archiving. Leaving `spec_review: "pending"` in an archived change is a gap.
- The full non-e2e test suite must run to completion and be listed in `validation_results` at archive. Closing with "full suite as the Next Step" is invalid — the full suite is a prerequisite for close, not a follow-up task.
- Verification hint: when a live dashboard/daemon process or parallel AI sessions share the machine, run the full suite with an isolated `pytest --basetemp=<unique>` path and snapshot `git status` before/after the run to prove no concurrent-writer interference.
- Archive hygiene: git-restore known side-effect files before archive (`docs/AGENT-REGISTRY-TABLE.md`, `hr/onboarding_requests.yaml`, `orchestrator/approvals.yaml`). Test runs and scaffolding may leave these dirty; they must not be committed as part of a change.
- When a change is parked, its test failures should not be counted as baseline by other changes. Tag parked failures (e.g., `parked:<change-id>`) to keep baselines isolated.
- If `pyproject.toml` is in the changeset, `uv.lock` must also be updated in the same commit. Lockfile atomicity prevents `--frozen` workflow breakage.

## 5 Plan Review Gate

Before implementation starts, require an approved plan review. Record it as `plan_review: "approved"` in `summary.md` front matter. This gate prevents raw requirements from moving directly into coding.

If the plan references an ADR (Architecture Decision Record), verify the ADR file exists in `docs/adr/` before marking `plan_review` as approved. ADRs must be recorded before or alongside implementation, not after.

If the plan or spec contains undefined codenames, abbreviations, or domain terms, define them before plan review. Undefined terms cost a clarification round-trip at implementation time (e.g. "Path-of-RPG" / "FLORA" required CEO clarification mid-implement).

## 6 Context Loading Order

1. `AGENTS.md`
2. `docs/ECL.md` (this file)
3. If active exists: `harness/changes/active/summary.md` → `spec.md` → `plan.md` → `tasks.md` → `reviews/`
4. If no active exists and `harness/evolution/pending.md` exists: read it, mention as pending, ask whether to handle
5. If no active exists and no pending: `docs/STATUS.md`
6. Relevant source files for the task

## 7 STATUS Handoff

Before closing active work:

1. Update `docs/STATUS.md` from active change files (summary, spec, plan, tasks, reviews).
2. Run `.\scripts\harness-change.ps1 close completed` to archive and rebuild INDEX.
3. After close, update `docs/STATUS.md` with archive path.
4. Run `.\scripts\lint-ecl.ps1` to confirm consistency.

## 8 Failure Feedback

When a task fails, capture the failure as context in the active change's `summary.md` Validation section. If the failure represents a new constraint or regression, record it in `tasks.md` as a follow-up task.

## 9 Auto-Evolve

Every few closed changes, `harness-evolve check` may create `harness/evolution/pending.md`. Treat it as a maintenance reminder. Do not let it block unrelated work. When you start acting on pending evolution, finish with a proposal + `results.tsv` row + `mark-complete`.

### 9.1 Auto-Evolve Proposal Template

When generating `harness/evolution/proposals/YYYY-MM-DD-auto-evolve.md`, use this structure:

```markdown
---
title: "Auto-evolve proposal: <eligible archive count> eligible archives (<date range>)"
date: <YYYY-MM-DD>
trigger:
  reason: <close|manual>
  eligible_count: <N>
  threshold: <N>
  window: <N>
  excludes: ["auto-evolve-harness-", "auto-evolve"]
---

# Auto-evolve Proposal

## Candidate Archives

| # | Archive ID | Title | Validation | Key Decisions |
|---|------------|-------|------------|---------------|

## Evidence: Repeated Failures / Verification Gaps / User Corrections / Reusable Constraints

### Verification Gaps
### User Corrections
### Reusable Constraints (Rules to Clarify / Keep)

## Scoring & Recommendations

Scoring: archive evidence (0-40), project relevance (0-30), rule clarity impact (0-30). ≥80 = accept.

| # | Candidate Change | Evidence | Relevance | Clarity | Score | Recommendation |
|---|-----------------|----------|-----------|---------|-------|----------------|

## Accepted Candidates (Score ≥ 80 + Auditor Approval)

## Application Plan
```

## 10 Script Reference

| Command | Script | Purpose |
|---------|--------|---------|
| `.\scripts\harness-change.ps1 new "Title"` | harness-change.ps1 | Create new active change |
| `.\scripts\harness-change.ps1 status` | harness-change.ps1 | Show active change status |
| `.\scripts\harness-change.ps1 close completed` | harness-change.ps1 | Archive active change |
| `.\scripts\harness-change.ps1 park` | harness-change.ps1 | Park active change |
| `.\scripts\harness-change.ps1 resume <id>` | harness-change.ps1 | Resume parked change |
| `.\scripts\harness-change.ps1 reindex` | harness-change.ps1 | Rebuild INDEX.json |
| `.\scripts\harness-evolve.ps1 check` | harness-evolve.ps1 | Check auto-evolve threshold |
| `.\scripts\harness-evolve.ps1 mark-complete` | harness-evolve.ps1 | Mark evolution complete |
| `.\scripts\lint-ecl.ps1` | lint-ecl.ps1 | Validate ECL structure |

## 11 Rules

- `harness/changes/INDEX.json` is generated by script only. Never hand-edit.
- Active change files override `docs/STATUS.md` for the current task.
- Archive history is loaded selectively through STATUS paths or INDEX, never wholesale.
