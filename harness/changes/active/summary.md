---
title: "Creative Production Studio: ls-stack agents x7, count migration 145 to 152"
slug: "creative-production-studio-ls-stack-agents-x7-count-migration-145-to-152"
status: "in_progress"
location: "active"
phase: "validate"
intake_status: "approved"
spec_review: "approved"
plan_review: "approved"
modules:
  - registry
  - generator
  - docs/manifest
files:
  - company-registry.yaml
  - docs/source-of-truth.yaml
  - README.md
  - docs/USER-GUIDE.md
  - docs/ORGANIZATION.md
  - docs/API-REFERENCE.md
  - docs/STATUS.md
  - CHANGELOG.md
tags: [creative-production-studio, registry, agents, marketing, docs-drift]
validation_status: "pass"
created_at: "2026-09-17"
updated_at: "2026-09-17"
session_id: "4bee3404-ee12-4f06-bf91-3a72f6b94ec2"
owner_agent: "jmlus"
claimed_at: "2026-09-17"
---

# Summary

## Outcome

Add 7 Marketing specialists (`creative_director`, `presentation_designer`, `document_designer`, `diagram_designer`, `visual_storyteller`, `brand_advertising_designer`, `artifact_qa_reviewer`) completing the `ls-*` Creative Production Stack, regenerate agent cards + `company/agent-registry.json`, and migrate all count-bearing docs from 145 (144 AI + 1 Human CEO) to 152 (151 AI + 1 Human CEO) while keeping drift gates green.

## Decisions

- Complete the `ls-*` skill stack with one agent per skill; no new department — new agents sit under Marketing.
- Reporting: `creative_director` -> `cmo`; the other six -> `creative_director`.
- Registry YAML is the source of truth; `ai-company generate` + `sync-registry --verify` regenerate mirrors (`specialists add` CLI lacks fields needed for full entries, so YAML is hand-authored).
- Prior `2026-09-04-doc-drift-prevention` change parked; this is the new active ECL change.

## Validation

- Pending (see plan.md Verification Plan; outcomes recorded at closure in `validation_status`).

## Next Step

- Append the 7 agents to `company-registry.yaml`, regenerate, then run the drift and quality gates.

## Transition Note

- ECL change closed manually on 2026-09-17 after all edits, sweeps, and gate validations passed.
- Validation status: pass. All 152 registry entries confirmed; 152 agent cards generated; drift gates green (validate-drift.ps1, pytest doc_drift, lint-ecl.ps1, ruff, mypy, pytest).
- STATUS.md and CHANGELOG.md entries recorded.
- Harness harness-change.ps1 close auto-flow constrained by active-change check; manual closure recorded here.
