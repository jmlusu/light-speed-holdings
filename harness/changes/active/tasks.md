# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Confirm scope with CEO (both tracks, Xiaomi vendor, 10-agent roster,
  fresh worktree) and record it in `harness/changes/active/spec.md` — validation:
  no `[NEEDS CLARIFICATION]` markers in `spec.md`.

## Implementation

- [x] T002 Add MiMo to `company/models.yaml` (last in `standard`/`premium`) and
  `src/ai_company/llm/cost_tracker.py` `MODEL_COSTS` — validation:
  `uv run pytest tests/unit/test_mimo_provider.py`.
- [x] T003 Thread `MIMO_API_KEY` through `.env.example`, `.env.staging.example`,
  `docker-compose{,.staging}.yml`, `.github/workflows/{autonomous,repo-audit}.yml`,
  `AGENTS.md`, `src/ai_company/dashboard/monitoring.py` — validation: grep test in
  `tests/unit/test_mimo_provider.py`.
- [x] T004 Update count surfaces (`docs/source-of-truth.yaml`
  `provider_count: 10`, `README.md`, `docs/ux/DEVELOPER-EXPERIENCE.md`,
  `docs/client-facing/USE-CASE-CATALOG.md`, `docs/MODEL-ROUTING-POLICY.md`) —
  validation: `pwsh scripts/validate-drift.ps1`.
- [x] T005 Record governance: `docs/APPROVED-VENDORS.md` MiMo row +
  `docs/adr/025-mimo-provider-and-mimocode-cli.md` — validation:
  `pwsh scripts/lint-ecl.ps1`.
- [x] T006 Scaffold MiMo Code: tracked `.mimocode/mimocode.jsonc` and `.gitignore`
  rules for `.mimocode/*` + root `/mimocode.json(c)` — validation:
  `git check-ignore -v`.
- [x] T007 Wire Track B custom provider (`@ai-sdk/openai-compatible`,
  `https://api.xiaomimimo.com/v1`, `"apiKey": "{env:MIMO_API_KEY}"`, default
  `custom/mimo-v2.5`) in `.mimocode/mimocode.jsonc` — validation:
  `mimo debug config` resolves the model; probe `mimo run --pure` reaches auth.

## Validation

- [x] T008 Run the local gate set (ruff, mypy, validate-drift, lint-ecl,
  archify, uv-audit, agent regen, pytest `not e2e` cov >= 72) and restore
  test-pollution files afterwards — validation: gates green, `git status` clean.
- [x] T009 Push `feat/mimo-integration` and open PR — validation: PR #364, all
  CI checks pass.
- [ ] T010 Top up the Xiaomi MiMo account and confirm a real `mimo run` output —
  validation: `mimo run --pure` returns model text instead of
  `Insufficient account balance`. Blocked on account credit (CEO).
- [ ] T011 Add `MIMO_API_KEY` to GitHub Actions secrets — validation:
  `gh secret list` shows `MIMO_API_KEY`. Blocked on CEO approval to transmit the
  secret to GitHub.
- [ ] T012 Human review and merge of PR #364 — validation: branch merged into
  `main`.

## Deferred Tasks

- None.
