# Plan

## Technical Approach

Track A (config-only): append MiMo models last in `standard`/`premium` in
`company/models.yaml`, add `MODEL_COSTS` entries, add `MIMO_API_KEY` to the
monitoring provider list, thread the variable through env templates, compose,
workflows, and `AGENTS.md`, bump count claims to 10, record the vendor and the
decision in an ADR. Track B: commit `.mimocode/mimocode.jsonc` as a custom
`@ai-sdk/openai-compatible` provider keyed on `{env:MIMO_API_KEY}`, ignore all
other `.mimocode/` runtime state.

## Impacted Modules And Files

- `company/models.yaml`, `src/ai_company/llm/cost_tracker.py`,
  `src/ai_company/dashboard/monitoring.py`
- `.env.example`, `.env.staging.example`, `docker-compose.yml`,
  `docker-compose.staging.yml`, `.github/workflows/autonomous.yml`,
  `.github/workflows/repo-audit.yml`, `AGENTS.md`
- `docs/source-of-truth.yaml`, `README.md`, `docs/ux/DEVELOPER-EXPERIENCE.md`,
  `docs/client-facing/USE-CASE-CATALOG.md`, `docs/MODEL-ROUTING-POLICY.md`
- `docs/APPROVED-VENDORS.md`, `docs/adr/025-mimo-provider-and-mimocode-cli.md`
- `.mimocode/mimocode.jsonc`, `.gitignore`, `tests/unit/test_mimo_provider.py`

## Interfaces, Data, Permissions

- Provider contract: `provider: mimo`, `api_base:
  https://api.xiaomimimo.com/v1`, env var `MIMO_API_KEY`, models
  `mimo/mimo-v2.5` and `mimo/mimo-v2.5-pro` (SDK routing keys
  `mimo-v2.5` / `mimo-v2.5-pro`).
- Pricing per 1M tokens (cache-miss): `mimo-v2.5-pro` 0.435/0.87,
  `mimo-v2.5` 0.14/0.28.
- Track B: project config at `.mimocode/mimocode.jsonc`, default
  `custom/mimo-v2.5`, both models registered, no model cost/limit metadata
  invented.

## Spec Gaps Found From Planning

- None open. Credential path resolved (env token, not `mimo auth login`).

## Risks And Mitigations

- Routing displacement risk — mitigated by appending MiMo last in each tier.
- Committed secrets risk — mitigated by `.env` gitignore, empty example values,
  `detect-private-key` hook, and probes using dummy keys only.
- Divergent CLI config risk — mitigated by committing the project config and
  ignoring every other `.mimocode/` artifact.

## Verification Plan

1. `uv run ruff check src tests/ && uv run mypy src/`
2. `pwsh scripts/validate-drift.ps1` and `pwsh scripts/lint-ecl.ps1`
3. `uv run pytest -q -m "not e2e" --cov=src/ai_company --cov-fail-under=72`
4. Agent regen + archify regenerate (content-identical diff)
5. `uvx uv-audit`, version sync check
6. `mimo debug config` + `mimo run --pure` probe (dummy key, then real key)
7. Push, open PR, watch CI to green
