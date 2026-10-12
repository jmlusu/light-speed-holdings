# Deployment — Canonical Reference

> Single entry point for how LightSpeed Holdings is deployed. Detailed
> guides live in the sources below; this file states the canonical
> environments, ports, and commands so they agree in one place.

## 1 Environments

| Environment | How | Dashboard | Notes |
|-------------|-----|-----------|-------|
| Local dev | `.\scripts\dev\dev.ps1` / `uv run ai-company dashboard` | localhost:8420 | `.env` from `.env.example` (gitignored) |
| Staging (Docker) | `docker compose -f docker-compose.staging.yml up --build` | host **8421** → container **8420** | Profiles: `worker`, `monitoring` (Prometheus) |
| Production (Docker) | `docker compose up` / `Dockerfile` | container **8420** | RBAC keys required (fail-closed without them) |
| Frontend (Vite SPA) | Vercel (`vercel.json`, `.vercelignore`) | — | `npm run build`; see Brand Deployment Guide |

## 2 Key Commands

```powershell
# Staging lifecycle
docker compose -f docker-compose.staging.yml up --build
docker compose -f docker-compose.staging.yml --profile worker up
docker compose -f docker-compose.staging.yml --profile monitoring up

# Backups (outside the repo: ~/.lightspeed/backups)
.\scripts\deploy\backup.ps1
.\scripts\deploy\backup.ps1 -RetentionDays 14

# Release (PyPI trusted publishing, no stored tokens)
gh workflow run Release -f version=0.x.y

# Health
uv run python scripts/health_check.py          # ruff + mypy + pytest + generator + CLI + lint-ecl
curl http://localhost:8420/health              # production
curl http://localhost:8421/health              # staging
```

## 3 Detailed Sources

| Document | Covers |
|----------|--------|
| [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md) | Local setup, Dockerfile, Compose, CI/CD, security |
| [BRAND_DEPLOYMENT_GUIDE.md](BRAND_DEPLOYMENT_GUIDE.md) | Brand/static asset deployment |
| [OCI-FREE-TIER-DEPLOYMENT.md](OCI-FREE-TIER-DEPLOYMENT.md) | Oracle Cloud free-tier target |
| [directives/RUNBOOK-LightspeedAI-Deployment-2026-10-03.md](directives/RUNBOOK-LightspeedAI-Deployment-2026-10-03.md) | Point-in-time deployment runbook (2026-10-03) |
| [DEVELOPMENT.md](DEVELOPMENT.md) §11 | Release process (trusted publishing) |
| AGENTS.md §11 | Key rotation procedure (dashboard RBAC, LLM providers) |

## 4 Deployment Hygiene (from the 2026-10-06 sanitization)

- Backups land **outside** the repo (`~/.lightspeed/backups`); `backups/` no longer exists in-tree.
- `open-design/` is a declared git submodule (`.gitmodules`); fresh clones resolve it with `git submodule update --init`.
- `models/` (24 GB local weights) is gitignored and regenerable via `scripts/build/download_models.py` — never commit weights.
- `static/brand/` and `public/brand/` are generated mirrors of `brand/` — deploy reads them, humans edit `brand/` and run `scripts/build/sync-brand.ps1 -Verify`.

## 5 Vercel Preview Failure Runbook

A preview deploy can fail **before it builds** (observed 2026-10-12: `errorCode: git_info_fail`).
These failures expose **no build logs** — `/v6/deployments/<id>/events` returns 400/empty and the
dashboard shows a dead "Preparing" state. They are transient; the fix is a redeploy, not a code change.

**Identify.** The GitHub commit status uses context `Vercel`; its `target_url` is
`https://vercel.com/<team-slug>/<project>/<short-id>`. The API requires the full id:
`dpl_<short-id>` (the bare short id 404s).

**Auth.** Local: `VERCEL_ACCESS_TOKEN` from `.env`. CI: GitHub secret `VERCEL_API_KEY`.
Team scope: `teamId=team_ktnrLZHZZA1CPEC8XTRYNXt1` (slug `jmlusu-8288s-projects`) — the
deployments endpoints return 404 without it.

**Manual redeploy:**

```bash
# 1. Confirm it failed
curl -sS -H "Authorization: Bearer $VERCEL_ACCESS_TOKEN" \
  "https://api.vercel.com/v6/deployments/dpl_<ID>?teamId=team_ktnrLZHZZA1CPEC8XTRYNXt1" \
  | jq '.readyState, .errorCode'

# 2. Redeploy — payload is exactly deploymentId + name (project slug)
curl -sS -X POST -H "Authorization: Bearer $VERCEL_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"deploymentId":"dpl_<ID>","name":"light-speed-holdings"}' \
  "https://api.vercel.com/v13/deployments?teamId=team_ktnrLZHZZA1CPEC8XTRYNXt1" | jq '.id'
```

Rejected payloads (HTTP 400): `target: "preview"`, `forceNew` — do not add them.

**CLI caveat.** `npx vercel inspect <url> --logs` hangs without `~/.vercel/auth.json`; run
`vercel login` once interactively, then inspect works. Prefer the REST API in scripts.

**Automation.** [`.github/workflows/vercel-retry.yml`](../.github/workflows/vercel-retry.yml)
watches `status` events and redeploys once per commit (marker context `vercel-retry` prevents
loops); no workflow action runs twice for the same SHA.

## 6 Website Deploy — Happy-Path Verification

After merging a website PR to `main`, verify in this order (failure handling is §5 above):

1. **Merge → status event.** The squash merge on `main` triggers the `Vercel` GitHub status,
   which starts the production deployment — **unless the merge only touched non-site files**
   (see §7; the build is skipped and production keeps serving the last site deploy). Its
   `target_url` carries the short id; the API needs the full `dpl_<short-id>`.
2. **Poll REST until `readyState` is `READY`** — the endpoint 404s without `teamId`:

   ```bash
   curl -sS -H "Authorization: Bearer $VERCEL_ACCESS_TOKEN" \
     "https://api.vercel.com/v6/deployments/dpl_<ID>?teamId=team_ktnrLZHZZA1CPEC8XTRYNXt1" \
     | jq -r '.readyState'
   ```

3. **Check the production alias** serves the deploy:

   ```bash
   curl -sI https://lightspeedholdings.vercel.app | head -1    # expect HTTP 200
   ```

   Then spot-check the shipped change in the browser (e.g. the footer FAQ link → `/#faq`).

Worked example (PR #445, 2026-10-12): squash merge `cab747b6` → 15 checks green → deploy
`gc9i4ijt2` `READY` → alias 200 → prod verify 6/6 PASS.

## 7 Website Deploy — Skip Filter (ignoreCommand)

We merge to `main` often (ship fast / fail fast). Most merges touch docs, harness, Python,
or tests — none of which change what production serves. `vercel.json` therefore sets
`ignoreCommand` to `bash scripts/deploy/vercel-ignore-build.sh`, which diffs the commit
against `VERCEL_GIT_PREVIOUS_SHA` (the last commit that actually produced a deploy) and
**exits 1 to skip the build** when no site-bundle file changed. Vercel records the merge
as a skipped deployment; the production alias keeps serving the previous deploy. The
filter applies to preview deployments on other branches too.

**Triggers a build** (site-bundle set): `index.html`, `vercel.json`, `.vercelignore`,
`package.json`, `package-lock.json`, `tsconfig*.json`, `vite.config.*`, `api/`
(Vercel Functions), `public/`, `brand/`, `packages/design-system/`, `src/` (minus
`src/ai_company/` and `src/__tests__/`), and `data/<dir>/registry.ts` (the aliased
site registries — mirrors the `.vercelignore` re-include rules).

**Never triggers:** Python (`src/ai_company/`), unit tests (`src/__tests__/` — CI's
site-principles gate still type-checks them), docs, harness, scripts, `.github/`.
Safe defaults: if `VERCEL_GIT_PREVIOUS_SHA` is missing or unknown, the build runs.

**Force a production deploy** without a site change: redeploy the latest deployment
from the Vercel dashboard (Redeploy), or push a trivial site-file touch (e.g. a comment
in `vite.config.ts`). The retry workflow (§5) is unaffected — it only re-runs
deployments whose `readyState` is `ERROR`, and skipped builds never reach that state.
