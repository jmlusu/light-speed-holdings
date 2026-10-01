---
title: "2026-09-25-mimo-incorporation-model-provider-and-agent-cli"
slug: "2026-09-25-mimo-incorporation-model-provider-and-agent-cli"
status: "in_progress"
location: "active"
phase: "validate"
intake_status: "approved"
spec_review: "approved"
plan_review: "approved"
modules:
  - "llm"
  - "dashboard"
  - "governance"
files:
  - "company/models.yaml"
  - "src/ai_company/llm/cost_tracker.py"
  - "src/ai_company/dashboard/monitoring.py"
  - "docs/APPROVED-VENDORS.md"
  - "docs/adr/025-mimo-provider-and-mimocode-cli.md"
  - ".mimocode/mimocode.jsonc"
tags:
  - "llm-provider"
  - "mimo"
  - "mimocode"
validation_status: "pass"
created_at: "2026-09-25"
updated_at: "2026-09-25"
session_id: "4c15e9f2-18de-4c95-8055-688553cf74b5"
owner_agent: "jmlus"
claimed_at: "2026-09-25"
---

# Summary

## Outcome

Xiaomi MiMo landed as the fleet's 10th LLM provider (Track A) and MiMo Code as a
second coding CLI (Track B), shipped as PR #364 on `feat/mimo-integration`
(7 commits from `origin/main` `ad1c242`). MiMo enters `standard` and `premium`
tiers last, so primary routing is unchanged and MiMo only earns traffic on
failover. CI green on all checks for PR #364.

## Decisions

- Tier placement: `mimo/mimo-v2.5` last in `standard`, `mimo/mimo-v2.5-pro` last
  in `premium`, `fast` untouched — zero primary-routing change.
- Provider wiring is config-only (config falls through to
  `OpenAICompatibleProvider`, `https://api.xiaomimimo.com/v1`, key
  `MIMO_API_KEY`); no changes to `providers/*`, `model_router.py`,
  `circuit_breaker.py`, or `token_bucket.py`.
- Track B credential path chosen by CEO: issue `MIMO_API_KEY` (paid API), not
  `mimo auth login`; `.mimocode/mimocode.jsonc` wires it as
  `"apiKey": "{env:MIMO_API_KEY}"` on a custom `@ai-sdk/openai-compatible`
  provider, default model `custom/mimo-v2.5`.
- Vendor allow-listed in `docs/APPROVED-VENDORS.md`, window ends 2026-12-24;
  MiMo Code built-in skills carry a stop-and-report note under the third-party
  transmission ban.
- Explicitly not touched: `FALLBACK_REQUIRED_ENV_VARS`, `security.py`
  `placeholder_keys` (all `.env.example` values empty), `doctor/checks.py`
  `check_llm_providers`, hand-edits to `.opencode/agents/*`,
  `company-registry.yaml`.

## Validation

- Pass: `ruff check src tests`, `mypy src/` (224 files), `validate-drift` (87
  files), `lint-ecl`, agent regen content-identical, archify regenerate +
  validate x4, `uv-audit`, version sync (0.6.0), pytest `not e2e`
  (2461 passed, cov 79.6% >= 72).
- Pass: PR #364 CI — all checks green including Test (ubuntu) + Test (windows),
  Generated Files Drift, Graph Build + Health, Archify, CI Gate.
- Pass: Track B probe — with a dummy key `mimo run --pure` selects
  `mimo-v2.5` and fails only at auth; unset key resolves to `""` and the config
  still parses. With the real key it reaches upstream and reports
  `Insufficient account balance`, i.e. wiring verified end-to-end up to account
  credit.
- Not ours (recorded): local perf p95 failures in
  `tests/performance/test_dashboard_performance.py` (cold-start timing; both
  files reverted to base reproduce them, and CI Test jobs pass) and local
  `graphify diagnose multigraph` exit -1 (fails identically on pristine
  `ad1c242`; CI graph job passes).

## Next Step

- Only human review + merge of PR #364 remains (tasks T012), then close this
  change via `scripts/harness-change.ps1 close`.
- Done since first draft: `MIMO_API_KEY` added to GitHub Actions secrets
  (2026-09-26); real `mimo run` generation deferred by CEO — the Xiaomi account
  has no balance and the wiring is already verified up to upstream auth.
