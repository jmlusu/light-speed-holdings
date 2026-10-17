# Hosting Contingency — No Always-On Host

**Status:** Active decision (2026-09-24)
**Context:** OCI free-tier path abandoned; team review (CTO, CFO, CISO, DevOps) selected **Sovereign split** as primary. This document is the **contingency** when no always-on Docker host exists (verified: local Docker Desktop only, 3h sleep, no remote context).

**Primary plan:** Keep Vercel for the public SPA + run `docker-compose` production on any always-on Docker host when one exists. Coolify optional. Do not start a new Proxmox buildout solely for this.

---

## Decision gate

| Situation | Action |
|-----------|--------|
| Always-on Docker host available | Follow primary plan (this file does not apply). |
| No always-on host; dashboard must be public for demos | **Render Hobby Free contingency** (below). |
| No always-on host; dashboard only used on this laptop | Run `docker compose --profile production up -d` locally; no Render. |

---

## What already works (no new hosting required)

| Surface | Where it runs today |
|---------|---------------------|
| SPA + `api/enquiry.ts` | Vercel (ADR-020 / ADR-022 edge runtime) |
| 6-hour orchestrator / executor cadence | `.github/workflows/autonomous.yml` (`cron: "0 */6 * * *"`) |
| Daily JSON / repo backup | `.github/workflows/disaster-recovery.yml` (03:00 UTC → artifact, 30 days) |
| Images | GHCR via existing release CI (multi-arch) |
| Staging dashboard | Local: `docker compose -f docker-compose.staging.yml --profile staging up -d` → host `:8421` |

Actions workers are ephemeral: `.opencode/inbox.json` is gitignored; `autonomous.yml` seeds tasks each run. That path does not depend on Render or any long-lived VM.

---

## Render Hobby Free — dashboard only

Use **only** when the FastAPI dashboard must be reachable off-laptop (demo, stakeholder link). Not the day-to-day system of record.

### Service

1. Render → **New Web Service** → deploy from GHCR image (same `Dockerfile`, target `runtime`).
2. Container port: **8420**.
3. Instance type: **Free** (expect sleep / cold start; no durable disk).

### Required environment (fail-closed)

| Variable | Value |
|----------|--------|
| `DASHBOARD_AUTH_MODE` | `api_key` (never open mode — ARCHITECTURE-GAPS / ADR-012) |
| `DASHBOARD_ADMIN_KEY` | From GitHub Actions / secrets manager (§11 rotation) |
| `DASHBOARD_RUN_KEY` | Same |
| `DASHBOARD_APPROVE_KEY` | Same |
| `DASHBOARD_API_KEY` | Legacy alias optional; prefer explicit role keys |
| `DASHBOARD_HOST` | `0.0.0.0` (container bind; auth still required) |
| `DASHBOARD_CORS_ORIGINS` | Pinned real origins only — not bare `localhost` for public URL |
| `AI_COMPANY_ENV` | `staging` or `production` as appropriate |
| Provider keys | Only what the demo needs; rotate per §11 |

Never commit `.env`. Prefer Render env vars + GitHub Environments secrets.

### State (JSON / ADR-005)

Free tier disk is **ephemeral**. Treat Render as non-authoritative for:

- `.opencode/` (inbox, memory, briefings)
- `company/`
- `logs/`
- `results/`

**Restore pattern (each cold start or deploy):**

1. Download latest `disaster-recovery.yml` artifact (or a mirrored copy you control).
2. Extract `.opencode/` + `company/` into the service workspace / volume if you enable a paid disk later.
3. Start dashboard.

If restore is not automated, **do not** rely on Render for approval state or agent memory — use it as a read-mostly health/KPI view only.

### Worker and Prometheus on free tier

| Component | Free-tier plan |
|-----------|----------------|
| Long-running worker / executor daemon | **Do not** put on Render free — no free workers, no always-on. Keep cadence in `autonomous.yml`. |
| Prometheus | **Skip** on Render free. Use `monitoring.yml` cron + dashboard `/health` checks. |
| Staging `:8421` | Stays local Compose (per AGENTS.md staging ports). |

### Upgrade triggers (pre-authorize before click)

| Need | Approx. cost | Note |
|------|----------------|------|
| Always-on dashboard, no cold start | ~$7/mo tier or paid instance | CTO/CFO review before first paid render |
| Durable disk without manual restore | Paid instance + disk | Replaces boot-time restore hack |
| Real workers + volumes on PaaS | ~$7–25/mo | CFO: auto-decline if >4 hrs/mo ops labor on self-host first |

Dual-approve gate still applies to anything **>$500** (AGENTS.md). Sub-$7/mo contingency spend is pre-decided by this plan when the gate path is chosen.

---

## Explicit non-choices (from team review)

| Option | Why rejected here |
|--------|-------------------|
| Fly.io | Org free posture requires card / tightened free tier — fails no-CC constraint. |
| Koyeb | No free workers / scale-to-zero / no durable volumes for this stack. |
| Supabase as “database host” | Stack persists JSON files (ADR-005); no Postgres to buy. |
| LocalStack | Local AWS emulator for dev/CI — not a production host. |
| GitHub Pages as primary | Static only; drops Vercel edge enquiry path. |
| GitHub Student Developer Pack | Student-licensed, time-boxed; model company infra as **$0** value. |
| New Proxmox just to replace OCI | CapEx negative ROI vs $0–50/mo; keep as upgrade path only. |

---

## §9.2 vendor note

Hosting **our services** on a PaaS is not skill third-party transmission. Any future **skill or integration** that POSTs local code, memory, prompts, or screenshots to that vendor’s API **does** require a row in [`APPROVED-VENDORS.md`](APPROVED-VENDORS.md) (CEO/CISO, ≤90-day window). Record **Vercel (existing)**; gate any new PaaS integration the same way.

---

## Rollout checklist (contingency only)

- [ ] Gate confirmed: no always-on host **and** public dashboard required
- [ ] Render service created from GHCR; healthcheck `/health` green
- [ ] Auth mode `api_key` + role keys set; smoke-test unauthorized → 401/403
- [ ] CORS pinned to real origins
- [ ] Restore-from-DR path documented **or** service accepted as read-mostly
- [ ] Worker left on Actions (`autonomous.yml`); not on Render free
- [ ] Prometheus left off free tier
- [ ] Upgrade trigger written on the service README / team note
- [ ] `.env` not committed; secrets in GH + Render only

---

## Rollback / exit

- Delete Render service — no state migration out if you treated disk as ephemeral.
- Authoritative JSON remains whatever was last backed up (DR artifact / local bind mounts).
- When an always-on Docker host appears, return to **Sovereign split** and decommission the contingency service.
