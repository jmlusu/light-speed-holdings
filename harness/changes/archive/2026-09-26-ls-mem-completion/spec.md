# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first
- Questions asked this round: 5 (CLI naming, `.opencode/tools/`, commit policy, global skill copy, ECL tracking) — all resolved in Resolved Clarifications.

## Goal And Evidence

- Real problem or user request: LS-MEM Phases 0-3 are implemented and committed (`621a26e`) but the system is not yet operable end-to-end: `ai-company memory` still maps to the legacy JSON CLI (so the ls-memory skill scripts fail), the audit chain has no persisted head (tail tampering undetectable), required docs (user guide, security verification report) are missing, and §34 steps 19-20 (independent security audit, human approval) are outstanding.
- Current behavior: `src/ai_company/cli/main.py:45` maps `memory` -> `ai_company.cli.memory` (legacy). `uv run ai-company memory remember ...` errors; skill scripts `.agents/skills/ls-memory/scripts/memory-*` fail. `AuditLogger.verify_chain()` recomputes hashes but never compares the final event hash against a persisted head.
- Source of evidence: `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md` §18, §27, §31-§34, §36; `harness/changes/archive/2026-09-25-ls-mem-implementation/summary.md` known-follow-ups.

## User Scenarios And Success

- Primary user/system scenario: operator/agent runs `ai-company memory remember/search/get/forget/status` and the ls-memory skill scripts end-to-end; verifier can detect audit-tail tampering; reviewer reads user guide + security verification report.
- Success criteria: CLI lifecycle works; legacy CLI reachable at `ai-company knowledge`; `verify_chain()` fails on last-event tampering; `docs/LS-MEM-USER-GUIDE.md` + `docs/security/LS-MEM-SECURITY-VERIFICATION.md` exist answering §27/§33; ruff/mypy/pytest green; independent security audit recorded.
- Acceptance criteria: handoff §31 items 17-20 satisfied; §34 step 19 audit performed; gates in §36 pass.

## Non-Goals

- No `.opencode/tools/` wrappers (skill scripts are the tool surface; deviation recorded in the security verification report).
- No global skill copy at `C:\Users\jmlus\.agents\skills\ls-memory`.
- No changes to `open-design/`, no `git push`.
- No executor/memory-engine behavior changes beyond the audit head.

## Constraints

- Single active ECL; unrelated parked change `2026-09-26-immersive-3d-homepage-rebuild-full-webgl-lusion-igloo-class` must remain parked (resumable).
- Dual skill path hash-identical (`tests/memory/test_dual_path_hash.py`).
- Commit only LS-MEM-scoped files at the end; user-approved plan = this document.

## Assumptions

- Legacy `memory` CLI has no runtime consumers beyond `main.py` (verified: only reference is `src/ai_company/cli/main.py:45`); `config/company/scheduler.yaml` command keys are not executed by code.
- Existing archived LS-MEM validation evidence (36 files, Phase 0-3) remains valid.

## Open Questions

- None.

## Resolved Clarifications

- Q1 CLI naming: LS-MEM takes `ai-company memory`; legacy JSON CLI moves to `ai-company knowledge`.
- Q2 `.opencode/tools/`: skip; satisfy AC via ls-memory skill scripts; note deviation in §33 report.
- Q3 Commit: yes, one commit at end, LS-MEM files only, no push.
- Q4 Global skill copy: no.
- Q5 ECL: open + archive this change.
