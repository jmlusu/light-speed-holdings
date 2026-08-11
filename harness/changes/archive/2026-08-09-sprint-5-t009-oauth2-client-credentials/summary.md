---
title: "Sprint 5 - T009 OAuth2 client credentials"
slug: "sprint-5-t009-oauth2-client-credentials"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "approved"
spec_review: "approved"
plan_review: "approved"
modules: ["llm"]
files:
  - "src/ai_company/llm/oauth2.py"
  - "src/ai_company/llm/providers/openai_compatible.py"
  - "src/ai_company/llm/client.py"
  - "src/ai_company/model_router.py"
  - "tests/unit/test_oauth2.py"
tags:
  - "sprint-5"
  - "t009"
  - "oauth2"
  - "auth"
  - "security"
validation_status: "pass"
created_at: "2026-08-09"
updated_at: "2026-08-09"
---

# Summary

## Outcome

T009 OAuth2 client-credentials flow — implemented. New `OAuth2TokenManager` (client-credentials grant, in-memory token cache with TTL, fail-closed on missing credentials/token-fetch failure) wired into `OpenAICompatibleProvider` (per-request bearer token) and `LLMClient._init_providers` (opt-in per provider via `company/models.yaml`). `ProviderConfig` extended with an `oauth2` block. 11 new tests.

## Decisions

- OAuth2 is opt-in per provider via a `oauth2:` block in `company/models.yaml`.
- Secrets read from env vars only; token cache held in memory with TTL.
- Fail-closed: missing credentials or token-fetch failure makes the provider unavailable and routing falls through.

## Validation

- ruff check src/ — clean
- mypy src/ — clean (4 source files)
- pytest — 1778 passed, 53 deselected, 0 failures (baseline 1745 + 11 OAuth2 + 22 from parallel commits)
- CLI help verified (`ai-company llm --help`)

## Next Step

- Close change: update STATUS.md, archive, run lint-ecl.ps1.
