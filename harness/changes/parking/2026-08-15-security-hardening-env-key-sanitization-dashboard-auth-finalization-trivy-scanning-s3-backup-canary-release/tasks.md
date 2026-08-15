# Tasks

## Format

- `- [ ] T### [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.

## Implementation

### P0 — Security

- [ ] T002 `.env`: ensure all secret values are placeholders; add
      `DASHBOARD_AUTH_MODE=api_key`, `DASHBOARD_HOST=0.0.0.0`,
      `DASHBOARD_RUN_KEY`, `DASHBOARD_APPROVE_KEY`, `DASHBOARD_ADMIN_KEY`.
      Validate: `grep -E "sk-[a-zA-Z0-9]|AKIA|ghp_" .env` returns nothing.
- [ ] T003 `.gitignore`: verify `.env` is ignored. Validate:
      `git check-ignore .env` succeeds.
- [ ] T004 `.env.example`: add `DASHBOARD_AUTH_MODE` + `DASHBOARD_HOST`
      documented as optional. Validate: file parses as valid KEY=VALUE pairs.
- [ ] T005 `.env.staging.example`: sync RBAC keys + DASHBOARD_AUTH_MODE.
      Validate: diff against `.env.example` keys (only staging-specific values
      differ).
- [ ] T006 `dev_setup.py`: add `OPTIONAL_ENV_VARS` so bootstrap discovery
      skips non-required RBAC/auth vars. Validate: existing dev_bootstrap
      tests still pass.
- [ ] T007 Create `docs/DASHBOARD_KEY_ROTATION.md` + link from AGENTS.md.
      Validate: file exists, AGENTS.md contains a link.

### P1 — Infrastructure

- [ ] T008 `docker-compose.yml`: add DASHBOARD_AUTH_MODE + 4 dashboard keys
      to `dashboard` and `worker` env blocks. Validate:
      `docker compose config` (if Docker available) or YAML lint.
- [ ] T009 `docker-compose.staging.yml`: same as T008 for staging.
      Validate: `docker compose -f docker-compose.staging.yml config`
      renders without error.

### P2 — Production Readiness

- [ ] T010 `release.yml`: add Trivy scan job after `docker` job. Validate:
      workflow YAML is valid (`actionlint` or schema check).
- [ ] T011 `scripts/backup.ps1`: add S3 upload params + logic. Validate:
      `pwsh -File scripts/backup.ps1 -DryRun` runs without error.
- [ ] T012 `release.yml`: add canary release step after image push. Validate:
      workflow YAML is valid.

## Validation

- [ ] T013 `pwsh scripts/lint-ecl.ps1` → PASS
- [ ] T014 `pwsh -NoProfile -File scripts/harness-change.ps1 validate` → PASS
- [ ] T015 `uv run ruff check src/ && uv run mypy src/ && uv run pytest` → PASS
- [ ] T016 `pre-commit run --all-files` → PASS
- [ ] T017 `uv run bandit -c pyproject.toml -r src/` → PASS
- [ ] T018 `git status --porcelain` → no `.env` staged

## Deferred Tasks

- None.
