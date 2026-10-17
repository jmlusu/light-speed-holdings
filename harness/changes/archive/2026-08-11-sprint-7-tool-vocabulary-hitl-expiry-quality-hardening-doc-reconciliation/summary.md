---
title: "Sprint 7 - Tool vocabulary, HITL expiry, quality hardening, doc reconciliation"
slug: "sprint-7-tool-vocabulary-hitl-expiry-quality-hardening-doc-reconciliation"
status: "completed"
location: "archive"
phase: "implement"
intake_status: "approved"
spec_review: "approved"
plan_review: "approved"
modules:
  - "executor"
  - "orchestrator"
  - "registry"
  - "llm"
  - "docs"
files:
  - "src/ai_company/executor/tool_runner.py"
  - "src/ai_company/executor/prompts.py"
  - "src/ai_company/executor/hitl_gate.py"
  - "src/ai_company/orchestrator/tier_rules.py"
  - "src/ai_company/orchestrator/approval.py"
  - "src/ai_company/executor/daemon.py"
  - "src/ai_company/data/governance.py"
  - "pyproject.toml"
  - ".github/workflows/ci.yml"
tags:
  - "sprint-7"
  - "tool-vocabulary"
  - "hitl"
  - "quality"
  - "docs"
validation_status: "unknown"
created_at: "2026-08-11"
updated_at: "2026-08-11"
---

# Summary

## Outcome

Sprint 7: close the outstanding code-review and audit-fix follow-ups identified in
`docs/CODE_REVIEW_2026-08-10.md` and `docs/AUDIT-FIXES-2026-08-10.md`, plus CI and doc
reconciliation. In progress.

## Decisions

- Approved plan (human CEO, 2026-08-11): execute the 7-item task list via parallel
  subagents with disjoint file ownership, then integrate and gate locally before push.
- Canonical runtime tool vocabulary = `read`, `edit`, `grep`, `list`, `bash`, `webfetch`,
  `task`; `code_interpreter` is removed; legacy aliases (`write`/`execute`/`delegate`,
  `web_search`) retained as backward-compatible aliases only.
- HITL expiry: `ApprovalGate` gains a sweep that transitions expired PENDING requests to
  `EXPIRED`; wired into the daemon/governance cadence.
- Version story: `pyproject.toml` is the canonical version source; bump to `0.4.0` and tag
  `v0.4.0` at release (historical `v0.3.0` tag was lost in the recovery reset).

## Validation

- Pending final gates (ruff, mypy with `warn_return_any`, pytest, coverage >= 80%, ECL lint,
  generated-files drift check). Baseline before change: 1805/1858 tests, ruff/mypy clean.

## Next Step

- Run implement phase via delegated subagents; then integrate, gate, commit, push, monitor CI.
