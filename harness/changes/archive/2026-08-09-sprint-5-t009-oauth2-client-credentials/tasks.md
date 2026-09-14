# Tasks

## Setup / Intake

- [x] T001 Review deferred T009 task from Sprint 4 archive.
- [x] T002 Write `spec.md` and `plan.md`; approve plan review.

## Implementation

- [x] T010 Create `src/ai_company/llm/oauth2.py` with `OAuth2Config` + `OAuth2TokenManager` (client-credentials grant, in-memory token cache, TTL-based refresh, fail-closed on missing credentials/token-fetch failure).
- [x] T011 Wire OAuth2 into `src/ai_company/llm/providers/openai_compatible.py` — per-request bearer token, `is_available()` honors OAuth2, backward-compatible when no OAuth2 config.
- [x] T012 Wire OAuth2 into `src/ai_company/llm/client.py` — build `OAuth2TokenManager` from provider `oauth2` block; keep API-key path unchanged.
- [x] T013 Extend `ProviderConfig` in `src/ai_company/model_router.py` with optional `oauth2` dict.

## Tests

- [x] T020 Add `tests/unit/test_oauth2.py` — token fetch, cache reuse, TTL refresh, fail-closed on missing credentials, provider integration (token attached to request), fallback to API key when unset.

## Validation

- [x] T030 Run gates: `ruff check src/` && `mypy src/` && `pytest` — ruff/mypy clean, 1778 passed / 53 deselected.
- [ ] T031 Update `docs/STATUS.md` and ECL summary; run `lint-ecl.ps1`.
