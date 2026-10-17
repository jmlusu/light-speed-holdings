---
title: "Sprint 8 operationalization - purge inbox, fix README, env setup, Malawi service catalog"
slug: "sprint-8-operationalization-purge-inbox-fix-readme-env-setup-malawi-service-catalog"
status: "completed"
location: "archive"
phase: "implement"
intake_status: "accepted"
spec_review: "approved"
plan_review: "approved"
modules: [orchestrator, docs, config]
files:
  - ".opencode/inbox.json"
  - "README.md"
  - ".env"
  - "docs/service-catalog-malawi.md"
tags: [operationalization, malawi, inbox, docs, onboarding]
validation_status: "pass"
created_at: "2026-08-12"
updated_at: "2026-08-12"
---

# Summary

## Outcome

Sprint 8 kicks off operationalization. The company has never run a real task:
0 LLM calls, 0 audit events, 177 junk test tasks in the inbox, no `.env`
(real API keys), stale README (says 27 agents / 24 commands; actual 127 / 30),
and no defined service offering for the Malawi market.

This change: purges the junk inbox via MessageBus (keeps SQLite mirror
consistent), fixes the stale README, creates a `.env` scaffold for real keys,
and drafts a Malawi service catalog with pricing and delivery model.

## Decisions

- Inbox purge is the sanctioned path: back up `.opencode/inbox.json` to a
  timestamped file, delete every task through `MessageBus.delete_task()`, then
  call `reconcile_mirror()` so `data/ai_company.db` task rows heal.
- README is rewritten to reflect reality: 127 agents, 30 CLI commands, real
  current-state quick start; historical changelog entries are left untouched.
- `.env` is created from `.env.example` (gitignored) with placeholder keys and
  a clear TODO comment — real keys stay out of version control.
- Service catalog is a new business doc `docs/service-catalog-malawi.md`
  (offers, MWK + USD pricing, payment rails, delivery model). This is the
  market-facing definition of what the company sells.
- `.env` holds real keys for the active stack (OpenCode `big-pickle`
  standard/premium, Gemini flash fast/cheap) sourced from local auth config;
  Deepseek/Kimi are excluded from routing tiers (no African payment/registration
  path). Hard budget caps ($2.00/day, $0.50/task, auto-suspend) stay in
  `config/company/guardrails.yaml` and bind via `CostTracker`.
- No source code changes in this sprint unless a validation gate fails.
  Exception: three test files gained the canonical `_anchor_data_root` fixture
  so the suite can never re-pollute the real inbox.

## Validation

- Passed. `lint-ecl.ps1` clean, `ruff check src/` clean, `mypy src/` clean,
  full `pytest` green (1860 passed, 53 deselected), inbox + SQLite mirror empty
  after the run. `git check-ignore .env` exits 0; no stale "27 agents"/"24 CLI"
  strings in README (word-boundary check).

## Next Step

- All tasks T001-T007 complete. Park or close this change through the harness
  script (`pwsh scripts/lint-ecl.ps1` passes; run the harness close flow), or
  open a follow-up sprint for the deferred items (temp-inbox test isolation is
  already landed via fixtures; dashboard Org Health score, onboarding flow,
  company-KPIs UI wiring remain).
