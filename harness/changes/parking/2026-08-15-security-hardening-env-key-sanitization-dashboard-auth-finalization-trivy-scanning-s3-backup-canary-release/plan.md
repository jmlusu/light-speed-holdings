# Plan

## Technical Approach

### P0 — Security: env key sanitization + docs
1. `.env` (local, gitignored): replace any provider/secret values with
   `your_*_api_key_here` placeholders and add the missing RBAC role keys
   (`DASHBOARD_RUN_KEY`, `DASHBOARD_APPROVE_KEY`, `DASHBOARD_ADMIN_KEY`) +
   `DASHBOARD_AUTH_MODE=api_key` so local dev matches the fail-closed default.
2. `.gitignore`: already covers `.env` / `.env.*` with negations for
   `.env.example` + `.env.staging.example`. Verify and leave as-is (no change).
3. `.env.example`: add `DASHBOARD_AUTH_MODE` and `DASHBOARD_HOST` as documented
   **optional** vars; keep RBAC keys; add comments clarifying optionality.
4. `dev_setup.py`: introduce `OPTIONAL_ENV_VARS` set so the env-var discovery
   in `_discover_required_env_vars()` does not flag optional RBAC/auth-mode vars
   as "missing" during bootstrap (keeps `FALLBACK_REQUIRED_ENV_VARS` unchanged so
   existing tests stay green).
5. `.env.staging.example`: sync to match `.env.example` (add RBAC keys +
   DASHBOARD_AUTH_MODE).
6. Docs: create `docs/DASHBOARD_KEY_ROTATION.md` + reference from AGENTS.md.

### P1 — Infrastructure: finalize dashboard auth + Docker consistency
1. `.env`: add `DASHBOARD_AUTH_MODE=api_key`, `DASHBOARD_HOST=0.0.0.0`
   (fail-closed default), and the three RBAC role keys (placeholders).
2. `docker-compose.yml` + `docker-compose.staging.yml`: add `DASHBOARD_AUTH_MODE`,
   `DASHBOARD_HOST`, `DASHBOARD_API_KEY`, `DASHBOARD_RUN_KEY`,
   `DASHBOARD_APPROVE_KEY`, `DASHBOARD_ADMIN_KEY` to each service `environment:`
   block using `${VAR:-}` fallback. Production keeps `api_key` mode +
   `DASHBOARD_HOST=0.0.0.0` (container binds to 0.0.0.0 but auth is enforced).
3. Verify staging compose renders: `docker compose -f
   docker-compose.staging.yml config`.

### P2 — Production readiness: Trivy + S3 backup + canary
1. `release.yml`: add `trivy-scan` job (runs `aquasec/trivy-action` against the
   pushed GHCR image) as a dependency of `github-release`.
2. `scripts/backup.ps1`: add optional `-BackupS3` / `-S3Bucket` / `-S3Region`
   params; when provided, `aws s3 cp` each archive to S3 after local rotation.
   Document in a new `## Cloud (S3) backup` section + param help.
3. `release.yml`: add `canary-deploy` job (after image build) that deploys the
   new image to 1 of N replica pods via a `--canary` flag on the dashboard
   entrypoint (or a separate canary service label), waits, then promotes. Use
   GitHub Actions environment + manual approval gate for the promote step.

## Impacted Modules And Files

- `.env` (local/gitignored — `.env` only, NOT committed)
- `.env.example`
- `.env.staging.example`
- `.gitignore` (verify only — no change expected)
- `docker-compose.yml`
- `docker-compose.staging.yml`
- `.github/workflows/release.yml`
- `scripts/backup.ps1`
- `src/ai_company/bootstrap/dev_setup.py`
- `docs/DASHBOARD_KEY_ROTATION.md` (new)
- `AGENTS.md` (link to rotation doc)

## Interfaces, Data, Permissions

- No API/interface changes. Dashboard auth mode already implemented (ADR-012);
  this change wires env vars through Docker and documents the procedure.
- Bandit already skips B105/B107 — placeholder strings in `.env.example` are fine.
- `detect-private-key` pre-commit hook: placeholders are not real keys, no impact.

## Spec Gaps Found From Planning

- None material. The `dev_setup.py` optional-var filtering is the one code
  change needed to keep bootstrap from over-requiring RBAC keys.

## Risks And Mitigations

| Risk | Mitigation |
|------|-----------|
| Adding RBAC keys to `.env.example` makes bootstrap require them | Filter via `OPTIONAL_ENV_VARS` in dev_setup.py |
| Docker compose with empty `${VAR:-}` keys crashes dashboard | Dashboard start fails closed (RBAC rejects unknown → 401); fail-safe |
| Trivy job adds time to release | Run only on tagged releases, not every CI run |
| S3 upload fails mid-backup | Upload after local archive succeeds; non-blocking if AWS CLI missing |
| Canary deploy leaves traffic split | Manual approval gate before promote; rollback = keep prior tag |

## Verification Plan

- `pwsh scripts/lint-ecl.ps1`
- `pwsh -NoProfile -File scripts/harness-change.ps1 validate`
- `uv run ruff check src/ && uv run mypy src/ && uv run pytest`
- `pre-commit run --all-files`
- `uv run bandit -c pyproject.toml -r src/`
- `docker compose -f docker-compose.staging.yml config` (if Docker available)
- `git status --porcelain` — confirm `.env` not in staged files
