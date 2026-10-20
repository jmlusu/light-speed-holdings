---
title: "Lint the deck tooling in CI: cover scripts/presentation/ in the ruff job"
slug: "lint-the-deck-tooling-in-ci-cover-scripts-presentation-in-the-ruff-job"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "completed"
spec_review: "approved"
plan_review: "approved"
modules: ["scripts/presentation", ".github/workflows"]
files:
  - ".github/workflows/ci.yml"
  - "scripts/presentation/verify-deck.py"
  - "CHANGELOG.md"
  - "docs/STATUS.md"
tags: ["ci", "lint", "presentation"]
validation_status: "pass"
created_at: "2026-10-20"
updated_at: "2026-10-20"
session_id: "9d2a7e13-5c48-4b0e-8f61-1a9c4e7b2d55"
owner_agent: "jmlus"
claimed_at: "2026-10-20"
---

# Summary

## Outcome

The `Lint (ruff)` job covered `src/` and `tests/` only, so the scripts that generate, verify and render the AI Venture Studio client deck were policed solely by the local pre-commit hook - which `--no-verify` can bypass. That is the exact situation the server-side gate exists to prevent, as the workflow's own comment says.

The job now also covers `scripts/presentation/`, with a comment recording why the directory is included. Two pre-existing ruff findings in `scripts/presentation/verify-deck.py` (unsorted import block, no newline at end of file) and the file's format drift were fixed so the widened scope is green on the first run.

The `verify-deck.py` change is import ordering, a trailing newline and the line wrapping of two long expressions. Its checks and their output are unchanged.

Eleven ruff findings remain in `scripts/maintenance/`. They belong to other owners' files, some under active work elsewhere, so the scope stops at the directory this work owns; widening it to all of `scripts/` is recorded as a deferred task.

## Decisions

- Scope the widening to `scripts/presentation/` rather than all of `scripts/`. The remaining findings sit in throwaway and debug scripts owned elsewhere, and touching them would collide with other work.
- Fix the two pre-existing findings rather than exclude the file. It is inside the directory this change owns, nobody is editing it, and an exclusion would leave the scope fragile.
- Do not add `ruff format --check` to CI. The repository has known format drift under `src/` (see `docs/STATUS.md`), so a format gate would fail on unrelated files. Formatting is enforced by the pre-commit hook on the files it touches.

## Validation

- `uv run ruff check src/ tests/ scripts/presentation/` (the new CI command): **All checks passed!**
- `uv run ruff format --check scripts/presentation/`: **5 files already formatted**.
- `uv run pytest tests/presentation -q`: **10 passed**.
- `uv run pytest tests/performance -q`: **28 passed**.
- Full non-e2e pytest suite (`uv run pytest --basetemp=<isolated> -q`): **2666 passed / 2 skipped / 67 deselected / 0 failed** (rc=0, 5m24s). The known side-effect file `src/data/generated/agent-registry.public.json` was restored; the before/after `git status` snapshot showed no other change.
- `pwsh scripts/maintenance/lint-ecl.ps1`: **ECL lint passed**.
- `pwsh scripts/maintenance/check-index-freshness.ps1` under Windows PowerShell 5.1: **PASS**.
- CI on the PR: the `Lint (ruff)` job green with the widened scope, plus all other required checks.

## Next Step

- Merge the PR, then confirm the parked HAOMTGV change is back in `harness/changes/active/`.
- Deferred: the eleven ruff findings in `scripts/maintenance/`, and a decision on whether the CI lint scope should eventually cover all of `scripts/`.
