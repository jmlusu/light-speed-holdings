# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first (carried from deferred Sprint 4 T009)
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: Network deployments need OAuth2 client-credentials authentication for LLM providers instead of static API keys, with fail-closed behavior and token caching.
- Current behavior:
  - Providers authenticate with static bearer API keys from env vars (`{PROVIDER}_API_KEY`) baked into the httpx client at construction time.
  - No OAuth2 client-credentials flow; no token caching or TTL handling; no fail-closed auth path.
  - `APIKeyManager` (Sprint 4 T010) handles key rotation but still relies on static key material.
- Source of evidence: Sprint 4 deferred task T009 (`harness/changes/archive/2026-08-08-sprint-4-quality-completeness/tasks.md`); plan.md spec gap "Network deployments use OAuth2/API keys with automatic rotation (fail-closed)".

## User Scenarios And Success

- Primary user/system scenario:
  1. Operator configures an OAuth2-protected LLM endpoint in `company/models.yaml` with a `token_url`, client id, and client secret.
  2. LLMClient resolves the provider and authenticates via the client-credentials grant.
  3. Access tokens are cached and reused until near expiry, then refreshed automatically.
  4. If credentials are missing or the token endpoint fails, the provider is unavailable (fail-closed) and routing falls through to the next provider.
- Success criteria: OAuth2 providers authenticate end-to-end; token cache respects TTL; fail-closed behavior verified; no regression to API-key providers.
- Acceptance criteria:
  - New `OAuth2TokenManager` with client-credentials grant, in-memory token cache, and TTL-based refresh.
  - `OpenAICompatibleProvider` accepts an OAuth2 config and attaches a live bearer token per request.
  - `LLMClient._init_providers()` wires OAuth2 config from `company/models.yaml` provider entries.
  - Fail-closed: no credentials or token fetch failure → provider reports unavailable / raises.
  - API-key auth path unchanged when OAuth2 is not configured (feature-flag fallback).

## Non-Goals

- Changing the API key rotation flow (T010) — out of scope.
- Adding an interactive browser/device authorization-code flow — client-credentials only.
- Token persistence to disk — in-memory cache with TTL is sufficient for this task.
- Modifying provider APIs other than `openai_compatible`/`ollama` entry points.

## Constraints

- Must maintain the existing test baseline (no regressions; 1745+ passing).
- Ruff and mypy must remain clean.
- Backward compatible: providers without an OAuth2 config keep using static API keys.
- No new runtime dependencies unless required (prefer httpx which is already a dependency).

## Assumptions

- OAuth2-protected providers expose a standard token endpoint (`grant_type=client_credentials`).
- The token endpoint responds with `access_token` and `expires_in` fields.
- httpx is available (already a core dependency).

## Open Questions

- None — behavior is fully specified by the deferred task and OAuth2 client-credentials standard.

## Resolved Clarifications

- T009 scope confirmed: OAuth2 client-credentials flow in `llm/client.py` + provider wiring + token caching with TTL + fail-closed.
- API-key providers remain the default; OAuth2 is opt-in per provider via `company/models.yaml`.
