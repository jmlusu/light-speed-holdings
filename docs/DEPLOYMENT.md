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
