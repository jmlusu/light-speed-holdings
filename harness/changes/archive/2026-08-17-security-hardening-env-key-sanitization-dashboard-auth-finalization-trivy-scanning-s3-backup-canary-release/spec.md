# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first (user provided explicit P0/P1/P2 directive)
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: Pre-flight hardening sweep across three priority
  tiers (P0 security, P1 infrastructure, P2 production readiness) before
  productionizing the dashboard and release pipeline.
- Current behavior: `.env` uses placeholder keys (already sanitized, but
  `.env.staging.example` and `.env.example` are inconsistent — `.env.example`
  omits the RBAC role keys that `.env.staging.example` also omits; docker-compose
  files do not pass through `DASHBOARD_*_KEY` env vars; release pipeline has no
  container image scanning or canary strategy; backup script has no cloud
  destination).
- Source of evidence: User directive listing 8 files + 3 priority tiers.

## User Scenarios And Success

- Primary user/system scenario: A developer or operator clones the repo, copies
  `.env.example` → `.env`, fills in keys, and runs docker-compose — the dashboard
  starts in fail-closed `api_key` mode with RBAC keys available. CI/CD scans
  images and rolls out canaries. Backups land in both local rotation and S3.
- Success criteria:
  - `.env` contains only placeholder values for real secret keys.
  - `.gitignore` excludes `.env` (and `.env.*`) while keeping `.env.example`.
  - `.env.example` documents every env var the dashboard and Docker stack need.
  - docker-compose `.yml` + `.staging.yml` pass through `DASHBOARD_AUTH_MODE`,
    `DASHBOARD_HOST`, and all four dashboard keys.
  - `release.yml` runs Trivy image scan; release pipeline supports canary.
  - `scripts/backup.ps1` accepts an S3 (or GCS) destination and uploads archives.
  - docs cover key rotation procedure.
- Acceptance criteria:
  - `ruff check src/ && mypy src/ && pytest` green locally.
  - `pre-commit run --all-files` green.
  - `pwsh scripts/lint-ecl.ps1` green.
  - `git status` shows no `.env` in staged files.

## Non-Goals

- Implementing OAuth2/OIDC identity provider (SPRINT-5 T009 groundwork exists).
- Removing the legacy `DASHBOARD_API_KEY` admin alias (keep backward compat).
- Changing test expectations in `test_dev_bootstrap.py` (bootstrap discovers
  required vars from `.env.example` keys — so adding optional keys there would
  make the bootstrap *require* them; we keep `.env.example` focused on truly
  required vars and document optional RBAC keys in AGENTS.md/docs).

## Constraints

- `.env` must never be committed (gitignored). Changes to `.env` stay local only.
- docker-compose uses `${VAR:-}` fallback to empty so missing keys don't crash
  the container but the dashboard stays fail-closed.
- Bandit skips B105 (`*_api_key` as string defaults) — consistent with existing
  config, so placeholder values in code/docs are fine.
- Trivy runs in CI on `ubuntu-latest`; `aquasec/trivy-action` is the standard
  GitHub Action.

## Assumptions

- The user's directive is the approved plan (plan_review: approved by user
  directive).
- AWS CLI is available in the CI runner for S3 upload (or the backup script uses
  `aws s3 cp`). For local dev, `--BackupS3` is optional.
- Docker is available for staging verification, but the staging environment may
  not be runnable in this sandbox; we verify config consistency via `docker
  compose config`.

## Open Questions

- None — all directives are explicit.

## Resolved Clarifications

- `.env.example` will document required *and* optional keys; bootstrap only
  enforces `.env.example` keys as "required" (so we keep `.env.example` to the
  truly required set and add RBAC docs separately to avoid breaking bootstrap
  expectations). However the task explicitly says "Update `.env.example` if
  needed with all required env vars" — we will add the RBAC keys as documented
  optional vars with clear comments that they are optional, and update
  `dev_setup.py`'s `FALLBACK_REQUIRED_ENV_VARS` + discovery so the bootstrap
  does not *require* optional RBAC keys.
