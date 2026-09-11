# Spec

> Recorded retroactively on 2026-08-26; the work shipped directly to main before this change was created. This spec documents what was done and why, for handoff continuity.

## Intake Review

- Intake type: Structured Change (recorded retroactively as small ops change)
- Input shape: mixed (CI failure triage → dependency remediation plan approved by user)
- Questions asked this round: 2 (merge vs close PR #155; leave vs document dirty files)

## Goal And Evidence

- Real problem or user request: "Monitoring & Alerts" workflow failing on Dashboard Health Check; Dependency Health job emitting vulnerable-dependency warnings.
- Current behavior: streak logic used a last-5-runs window causing false alerts; `uv.lock` held Jan 2024 fastapi/starlette carrying 15 advisories.
- Source of evidence: GitHub run logs (`32558034171`), `uv audit --frozen` output, advisory IDs PYSEC-2024-38 / GHSA-qf9m-vfgh-m389 + 13 starlette advisories.

## User Scenarios And Success

- Primary user/system scenario: scheduled monitoring runs stay green without stale-run false positives; dependency audit exits clean.
- Success criteria: monitoring workflow success with `[OK] No known vulnerabilities found`; no warning annotation.
- Acceptance criteria: CI green on all commits; audit exit 0.

## Non-Goals

- httpx2 migration (tracked as separate follow-up issue).
- Landing the concurrent session's in-progress workstream.
- Broad `uv lock --upgrade` of unrelated packages.

## Constraints

- Shared working tree with an active concurrent session — only surgical staging permitted.
- Lockfile atomicity: pyproject.toml changes must ship with uv.lock in the same commit (ECL §4).

## Assumptions

- fastapi/starlette major-version jumps are safe given no direct starlette imports and stable TestClient usage in tests (verified by grep before upgrade).

## Open Questions

- None remaining.

## Resolved Clarifications

- PR #155 disposition: merged (squash `44b3d85`) after verifying CLEAN/MERGEABLE + 11 green checks.
- Dirty working-tree files: left untouched per user decision.
