---
title: "Documentation Drift Prevention System"
slug: "doc-drift-prevention"
status: "active"
location: "active"
phase: "plan"
intake_status: "done"
spec_review: "pending"
plan_review: "pending"
modules:
  - "docs/source-of-truth.yaml"
  - "scripts/validate-drift.ps1"
  - "tests/docs/test_doc_drift.py"
  - ".pre-commit-config.yaml"
  - "CONTRIBUTING.md"
tags:
  - "documentation"
  - "governance"
  - "quality"
  - "automation"
validation_status: "pending"
created_at: "2026-09-04"
updated_at: "2026-09-04"
owner_agent: "chief-of-staff"
---

# Summary

## Outcome

Establish an org-wide system to prevent documentation drift when upstream sources change. Three layers:

1. **Source-of-Truth Manifest** (`docs/source-of-truth.yaml`) — Maps factual claims to authoritative sources
2. **Automated Validation** (`scripts/validate-drift.ps1` + `tests/docs/test_doc_drift.py`) — Fails on drift
3. **Process & Ownership** (updated `CONTRIBUTING.md`) — Clear responsibility model

## Decisions

- Source-of-truth manifest is YAML, not code — readable by humans and agents
- Validation runs at three speeds: pre-commit (fast), CI (thorough), weekly (catch-all)
- Archived/ADR docs are exempt from drift checks — they record historical state
- `company-registry.yaml` and `company/departments.yaml` are the canonical sources

## Validation

- `scripts/validate-drift.ps1` exits non-zero on drift
- `pytest tests/docs/test_doc_drift.py` passes
- Pre-commit hook runs validation automatically
- `ruff check src/ && mypy src/` pass

## Next Step

Execute Phase 1: knowledge-manager drafts source-of-truth.yaml, registry-owner verifies sources, technical-documentation-lead audits active docs.
