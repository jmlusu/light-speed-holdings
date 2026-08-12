# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: requirement-first
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: Sprint 7 (commit 1b30d8f) implemented tool vocabulary sync, HITL expiry, quality hardening, and a documentation audit report. However, the doc reconciliation portion is incomplete — 8 doc issues remain across version drift, stale counts, SOP v1/v2 duplication, and missing feature docs.
- Current behavior: `docs/STATUS.md` line 79 says "6 resolved" in ARCHITECTURE-GAPS.md (should be 20); `USER-GUIDE.md` says "27 agents" (actual 127); `DEVELOPER-GUIDE.md` says "24 CLI commands" (actual 30); `API-REFERENCE.md` says "Version: 0.1.0" (actual 0.4.0); `CHANGELOG.md` missing 0.4.0 entry; `sop-deployment.md` and `sop-incident-response.md` (v1) both marked `status: active` alongside v2; several features (OAuth2, ML module, Security module, Governance CLI) have no user/dev docs.
- Source of evidence: `docs/archive/2026-08-11-pre-restructure/DOCUMENTATION_AUDIT_REPORT.md` section 3, `docs/STATUS.md`, `pyproject.toml`, `company-registry.yaml`, `src/ai_company/cli/main.py:31-73`

## User Scenarios And Success

- Primary user/system scenario: A developer runs `ai-company --help` and sees 30 commands; opens `docs/USER-GUIDE.md` and sees 127 agents; checks `docs/API-REFERENCE.md` and sees version 0.4.0; runs `ai-company generate` and all 127 agent specs pass validation.
- Success criteria: No version/test-count contradictions remain; all SOP v1 files marked superseded; all feature docs cover implemented features; `docs/STATUS.md` line 79 updated to "20 resolved".
- Acceptance criteria: 1) `grep 'version = ' pyproject.toml` == `grep 'Version:' API-REFERENCE.md` == 0.4.0; 2) `grep -c "^- id:" company-registry.yaml` == 127 in USER-GUIDE.md; 3) 30 CLI commands listed in DEVELOPER-GUIDE.md; 4) CHANGELOG.md has `## [0.4.0]` entry; 5) SOP v1 files have `status: superseded` in frontmatter; 6) STATUS.md reports 20 of 20 gaps resolved; 7) `uv run ruff check src/ tests/` and `uv run mypy src/` and `uv run pytest -q -m "not e2e"` all pass.

## Non-Goals

- Rewriting existing documentation prose — only correcting counts, versions, and status metadata.
- Implementing new features — all features referenced already exist in source.

## Constraints

- Documentation changes only; no source code changes expected.
- Must pass `scripts/lint-ecl.ps1` and CI gate.

## Assumptions

- The 127 agent count in `company-registry.yaml` is the canonical count.
- The 30 CLI commands in `main.py:_LAZY_SUB_APPS` (5 root + 25 lazy) is canonical.
- Version 0.4.0 in `pyproject.toml` is canonical (per STATUS.md).

## Open Questions

- None.

## Resolved Clarifications

- None.
