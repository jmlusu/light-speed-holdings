# Plan

## Technical Approach

### 1. New module: `src/ai_company/llm/oauth2.py`

- `OAuth2Config` dataclass: `token_url`, `client_id`, `client_secret`, optional `scope`, `audience`, `cache_ttl_seconds`.
- `OAuth2TokenManager` class:
  - `get_access_token() -> str` — returns cached token if still valid (within a configurable safety margin), otherwise fetches a new one via the client-credentials grant (httpx `POST` with form data).
  - In-memory token cache keyed by provider config; TTL derived from `expires_in` in the token response, clamped to `cache_ttl_seconds`.
  - Fail-closed: raises `OAuth2Error` (subclass of `LLMProviderError`) if credentials are missing or the token endpoint returns non-2xx.
  - Thread-safe with a lock; concurrent callers share one refresh.

### 2. Provider wiring: `src/ai_company/llm/providers/openai_compatible.py`

- `OpenAICompatibleProvider.__init__` gains an optional `oauth2: OAuth2TokenManager | None = None`.
- When OAuth2 is set, the provider resolves its bearer token per request (no static key baked into the client) and uses `Authorization: Bearer <token>`.
- `is_available()` returns True when either a static API key or a configured OAuth2 manager with credentials is present.
- `chat()`/`chat_stream()` fetch the token before the request and attach it as an auth header.

### 3. Client wiring: `src/ai_company/llm/client.py`

- `_init_providers()` reads optional `oauth2` block from each provider config in `company/models.yaml`.
- Builds an `OAuth2TokenManager` and passes it to `OpenAICompatibleProvider`.
- Fallback: when no OAuth2 block is present, the existing `{PROVIDER}_API_KEY` bearer/x-api-key path is used unchanged.

### 4. Config model: `src/ai_company/model_router.py`

- `ProviderConfig` gains an optional `oauth2` dict field parsed from `models.yaml`.

## Impacted Modules And Files

- `src/ai_company/llm/oauth2.py` — new (token manager)
- `src/ai_company/llm/providers/openai_compatible.py` — auth wiring
- `src/ai_company/llm/client.py` — provider init wiring
- `src/ai_company/model_router.py` — ProviderConfig field
- `tests/unit/test_oauth2.py` — new (token manager + provider integration)
- `harness/changes/active/*` — ECL tracking

## Interfaces, Data, Permissions

- New public API: `OAuth2TokenManager.get_access_token()` and `OAuth2Error`.
- `company/models.yaml` provider entry example:

  ```yaml
  providers:
    enterprise-llm:
      backend: openai_compatible
      default_model: enterprise-model
      api_base: https://llm.example.com/v1
      oauth2:
        token_url: https://idp.example.com/oauth/token
        client_id_env: ENTERPRISE_LLM_CLIENT_ID
        client_secret_env: ENTERPRISE_LLM_CLIENT_SECRET
        scope: "llm:inference"
        cache_ttl_seconds: 300
  ```

- Secrets read from env vars only; never logged or persisted by the token manager.
- No filesystem writes; token cache is in-memory only.

## Spec Gaps Found From Planning

- None — the plan maps cleanly onto the deferred T009 acceptance criteria.

## Risks And Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| OAuth2 breaks existing auth | Low | High | Opt-in per provider; API-key path untouched when no oauth2 block present |
| Token endpoint latency adds per-call overhead | Medium | Low | In-memory cache + TTL; only one refresh per TTL window |
| Credentials leak via logs | Low | High | Secrets read from env, never logged; cache held in memory only |
| Token fetch failure blocks calls | Medium | Medium | Fail-closed provider unavailable → router falls through to next provider |

## Verification Plan

1. `ruff check src/` — clean
2. `mypy src/` — clean
3. `pytest` — full suite green (existing 1745+ plus new OAuth2 tests)
4. Manual: instantiate `OAuth2TokenManager` against a mocked token endpoint; confirm cache reuse and refresh.
