---
title: "T5 canonical org truth 90-20"
slug: "t5-canonical-org-truth-90-20"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "completed"
spec_review: "approved"
plan_review: "approved"
modules: ["registry", "docs"]
files: ["company-registry.yaml", "company/departments.yaml", "docs/source-of-truth.yaml", "docs/NARRATIVE-AND-POSITIONING.md", "docs/EXECUTIVE-STRATEGY-EXPANSION.md", "docs/marketing/warmup-content-pack/linkedin-post.md", "docs/Pharos/linkedin-intro-post.md"]
tags: ["wayfinder", "t5-421", "org-truth", "drift"]
validation_status: "pass"
created_at: "2026-10-07"
updated_at: "2026-10-07"
session_id: "b531f8ad-1fd9-4ce6-8146-cddac27d4752"
owner_agent: "jmlus"
claimed_at: "2026-10-07"
validation_results:
  - "ruff check src/: PASS (all checks passed)"
  - "mypy src/: PASS (no issues, 226 files)"
  - "generator: PASS (90 agent cards, 0 errors; side-effect CRLF churn restored)"
  - "sync-registry --verify: PASS (90 agents in sync)"
  - "pytest tests/docs/: PASS (33 passed / 1 skipped)"
  - "validate-drift.ps1: PASS (87 files, no drift)"
  - "validate-architecture.ps1: PASS (incl. type census 19/64/7=90; MASTER_SPEC guard fenced in backticks)"
  - "lint-ecl.ps1: PASS"
  - "pytest full non-e2e: PASS (2521 passed / 2 skipped / 67 deselected, isolated --basetemp)"
---

# Summary

## Outcome

T5 #421 in progress — canonical org truth reconciliation (docs + comment only; data layer already 90/20).

## Single-Source Census (computed 2026-10-07, not copied)

- **Registry (`company-registry.yaml`): 90 agents = 89 AI + 1 human CEO**; types 19 executive / 64 specialist / 7 board; **20 departments**.
- Per-department: Technology 13, Marketing 9, AI Research 7, Security 7, Board 7, Operations 6, Pharos 6, Executive 5, Product 5, People 4, Data 3, Legal 3, Sales 3, QA 3, Finance 2, Strategy 2, Customer Success 2, IT 1, Business Development 1, Consulting 1.
- Mirrors: `company/departments.yaml` 20 entries incl. `pharos`; `company/agent-registry.json` 90; `.opencode/agents/*.md` 90.
- SoT manifest (`docs/source-of-truth.yaml`): `department_count` 20, `agent_count` 90 — values correct, only the line-23 comment is stale.

## Decisions

- ECL slot handling: prior BLOCKER (T2 #418 occupied slot) cleared — T2 archived by its owner before this change opened; slot verified free (active/ held only `.gitkeep`); change created via `scripts/maintenance/harness-change.ps1 new` (note: ECL.md path `scripts/harness-change.ps1` is stale; actual script lives under `scripts/maintenance/`).
- Issue-body gap resolved: "Fix departments.yaml 19->20" needs no data fix (already 20) — reconciliation is comment/prose only.
- User decisions (2026-10-07): (1) NARRATIVE via ECL — yes; (2) history left as history with footnotes; (3) local-repo scope only, remote README + site copy are follow-ups.
- Triaged no-change: `MASTER_SPEC.md:105-115` guard block, `post-11/video-script.md:13,22` 152→90 story beats (intentional history per ADR-025).

## Validation

- All gates green 2026-10-07; see `validation_results` front matter. `git status` before/after full suite shows only this change's 6 files + harness records (concurrent-session files untouched).

## Next Step

- Close `completed`; comment resolution on #421 with PR link; unblock note for T6 #422.
