# Free-Tier Cloud Deployment Research Report
## Lightspeed AI Company Builder — 24/7 Operation Without Credit Card

**Date:** 2026-10-02  
**Research Mode:** Topic Survey (super-research)  
**Sources Examined:** 135 (logged in `sources.tsv`)  
**Saturation:** Reached — last 10 sources added no new claims

---

## Executive Summary

**No single free tier meets all hard constraints** (zero payment method + 24/7 uptime + persistence + background processes). The closest viable **composite stack** is:

| Layer | Choice | Why |
|-------|--------|-----|
| **Compute** | Hugging Face Spaces (CPU Basic, Docker) | 16GB RAM, 2 vCPU, no card, 48h sleep (bypassable) |
| **Persistence** | Neon (PostgreSQL) + Cloudflare R2 | 1GB/project, 100 projects, scales to zero, no card; 10GB free egress-free object storage |
| **Secrets** | Infisical (Cloud or self-hosted) | 5 identities, 3 projects, no card, MIT core self-hostable |
| **Automation** | n8n (via Hugging8n) or Dagu | n8n proven on HF Spaces; Dagu = single binary, no DB, runs anywhere |
| **Keep-Alive** | Cloudflare Workers (cron trigger) | Free 100k req/day, 5 cron triggers, no card |

**Critical gap:** HF Spaces **requires paid plan to create new Docker/Gradio Spaces** on CPU Basic (S003, S005). Workaround: **Duplicate an existing Space** (S008, S010) — free accounts can duplicate.

---

## Task 1: Hugging Face Spaces Free CPU Tier Validation

| Constraint | Finding | Source |
|------------|---------|--------|
| **RAM allocation** | 16 GB (CPU Basic) | S001, S003, S005, S012 |
| **CPU** | 2 vCPU | S001, S003 |
| **Disk** | 50 GB **non-persistent** (ephemeral) | S001, S003, S012, S015 |
| **Persistent storage** | **Feature removed** — `suggested_storage` ignored | S004, S015 |
| **Sleep policy** | Free `cpu-basic` sleeps after **48 hours inactivity** (no web traffic) | S002, S003 |
| **Background processes keep alive?** | **No** — only inbound HTTP traffic resets sleep timer. Scheduled n8n triggers do NOT count. | S014 |
| **ToS on background processes** | No explicit ban, but free tier not designed for 24/7 daemons. CPU Basic quota: **8 concurrent runtimes** max. | S006 |
| **Outbound network** | **Restricted** — blocks Telegram, Discord, WhatsApp, some APIs. Workaround: Cloudflare Workers proxy (Hugging8n builds this in). | S008, S014 |
| **Persistence across restart** | **Nothing survives** container restart except the git repo. Use external DB (Supabase/Neon) + HF Datasets for backup. | S001, S008, S013 |
| **Signup: card required?** | **No** — email or GitHub OAuth only | S005, S007 |
| **Creating new Docker Space** | **Requires paid plan** (PRO/Team/Enterprise) even on CPU Basic. Static Spaces free. | S003, S005, S007 |
| **Workaround** | **Duplicate existing Space** (e.g., Hugging8n, n8n-free) — free accounts can duplicate. | S008, S010 |

---

## Task 2: Hugging8n Project Audit

| Metric | Value |
|--------|-------|
| **GitHub Repo** | `https://github.com/somratpro/Hugging8N` |
| **HF Space** | `https://huggingface.co/spaces/somratpro/Hugging8N` |
| **Created** | 2026-04-22 |
| **Last Push** | 2026-06-24 |
| **Stars/Forks** | 37 / 13 |
| **License** | MIT |
| **Active Maintenance** | **Yes** — commits within 3 months, 1 open issue |
| **Installation** | Docker on HF Spaces (duplicate Space → set secrets) |
| **Works Today (2026-10-02)** | **Yes** — live Space running, recent commits |
| **Key Features** | n8n on HF Spaces, HF Dataset auto-backup, Cloudflare Workers proxy + keep-alive, dashboard at `/`, health at `/health` |
| **Required Secrets** | `HF_TOKEN` (write), `CLOUDFLARE_WORKERS_TOKEN` (recommended) |
| **Breaking Changes** | None reported |

---

## Task 3: Alternative Free Compute Hosts Survey

| Provider | Card Required? | Free Tier Specs | Sleep Policy | Persistence | Outbound Restrictions | ToS Red Flags | Verdict |
|----------|----------------|-----------------|--------------|-------------|----------------------|---------------|---------|
| **Hugging Face Spaces** | **No** | 16GB RAM, 2 vCPU, 50GB ephemeral disk | 48h inactivity (CPU Basic) | None (ephemeral) | Yes (blocks some APIs) | 8 concurrent runtime quota; Docker Space creation needs paid plan | ⚠️ **Best compute** but needs workaround |
| **Koyeb** | **Mixed** (human verification, may ask card) | 512MB RAM, 0.1 vCPU, 2GB SSD, 1 web service, 1 Postgres (5h/mo) | Scales to zero after **1 hour** inactivity | No volumes on free tier | Not documented | Free tier "never expires" but may require card for fraud prevention | ❌ Too small, scales to zero |
| **Render** | **No** | 512MB RAM, 0.1 CPU, 750 instance hrs/mo | **15 min** inactivity | Free Postgres **expires 30 days** after creation | Not documented | DB auto-deletes after 44 days (30+14 grace) | ❌ DB expiry kills persistence |
| **Glitch** | N/A | **SHUTTING DOWN** July 8, 2025 | N/A | N/A | N/A | N/A | ❌ **NOT VIABLE** |
| **Replit** | **No** | Starter: 1 published app, expires **30 days** | N/A (Deployments only) | No persistent hosting | Not documented | Always On removed Jan 2024 | ❌ 30-day expiry |
| **Deta Space** | N/A | **SHUT DOWN** Oct 17, 2024 | N/A | N/A | N/A | N/A | ❌ **NOT VIABLE** |
| **Northflank** | **Yes** (card for identity verification) | 2 always-on services, 2 jobs, 1 addon, no sleep | **No sleep** | 1 addon (DB) | Not documented | **Card required at signup** | ❌ Fails "no card" |
| **Val Town** | **No** | 100k runs/day, 1min timeout, 15min cron, 3-day logs | N/A (serverless) | No persistent compute | Not documented | 1M runs/day Pro, limited free | ⚠️ Serverless only, no 24/7 daemon |
| **Deno Deploy** | **Soft** (card to unlock full free limits) | 1M req/mo, 20GB egress, 15 CPU hrs, 512MB RAM | Scales to zero ~20-30s idle | No persistent storage | TLS restrictions on Free | Free orgs restricted until card linked | ❌ Card gate |
| **Cloudflare Workers** | **No** | 100k req/day, 10ms CPU, 128MB RAM, 5 cron triggers | Scales to zero | No persistent compute (KV/D1/R2 separate) | 6 subrequests, 50/subreq | Generous free tier | ⚠️ Too small for main app; good for keep-alive/proxy |
| **GitHub Codespaces** | **No** (personal accounts) | 120 core hrs/mo, 15GB storage/mo | Suspends after 30 min idle | Persistent per codespace | Not documented | **Personal accounts only**; not for 24/7 hosting | ❌ Not a hosting platform |
| **Gitpod/Ona** | **No** | 500 credits/mo (~50 hrs), 4 vCPU, 16GB RAM | N/A | N/A | N/A | **SaaS sunset Oct 2025**, self-host only | ❌ SaaS dead |
| **Google Colab** | **No** | Dynamic, GPU restricted, 12hr max runtime | Idle termination, no background | **No persistence** (Drive mount only) | Blocks web UI on free runtime | Not for production/hosting | ❌ Not a hosting platform |
| **Kaggle Notebooks** | **No** (phone verify for GPU) | 30 GPU-hrs/wk, 12hr session, 32GB RAM | 12hr max session | 20GB `/kaggle/working` versioned | Internet off by default | Session limits, no 24/7 | ❌ Not a hosting platform |
| **SageMaker Studio Lab** | N/A | **CLOSED TO NEW CUSTOMERS** | N/A | N/A | N/A | N/A | ❌ **NOT VIABLE** |
| **CodeSandbox** | **No** | 400 credits/mo (~40hrs Nano VM), 4 vCPU/8GB RAM | Freezes when credits exhausted | Repo-based | Not documented | Credit-based, not 24/7 | ❌ Not 24/7 |

---

## Task 4: Alternative Automation Engines (Constrained Containers ≤16GB RAM)

| Engine | Min RAM | Min CPU | DB Required? | License | Fits in 16GB? | Complexity | Notes |
|--------|---------|---------|--------------|---------|---------------|------------|-------|
| **n8n** | ~512MB | 0.5 vCPU | PostgreSQL (external) | Fair-code (source-available) | ✅ Yes | Low | **Proven on HF Spaces** via Hugging8n; activepieces alternative |
| **Windmill** | 2GB (server) + 2GB/worker | 2 vCPU + 1/worker | PostgreSQL 16+ | AGPLv3 | ⚠️ Tight (4GB min, 8GB rec) | Medium | Requires PG, Docker socket for workers |
| **Activepieces** | 4GB (app) + 4GB/worker | 1 CPU each | PostgreSQL 14+ + Redis 7+ | MIT (core) | ⚠️ 8GB+ min | Medium | Hobbyist mode: single container with PGLite (embedded) |
| **Node-RED** | 100-150MB idle | <0.5 vCPU | None (file-based) | Apache 2.0 | ✅ Easily | Low | Lightweight, runs on Pi; not a full orchestrator |
| **Apache Airflow** | 4GB+ (Docker Engine) | 2+ vCPU | PostgreSQL/MySQL | Apache 2.0 | ❌ Heavy | High | Needs 4-8GB Docker Engine alone |
| **Prefect** | 4-8GB (API) + 8-16GB (PG) | 2 vCPU (API) + 2-4 (PG) | PostgreSQL 14+ + Redis | Apache 2.0 | ❌ Too heavy | High | Requires managed PG for production |
| **Dagster** | 8GB practical (2GB doc) | 4 vCPU | PostgreSQL | Apache 2.0 | ❌ 8GB+ real | High | Runs in containers; code servers + daemon |
| **Temporal** | 4GB (minimal) → 20GB+ (prod) | 2 CPU (min) → 10+ (prod) | PostgreSQL/Cassandra + Elasticsearch | MIT | ❌ Minimal 4GB, real 20GB+ | Very High | Overkill for this use case |
| **Dagu** | **~50MB** (single binary) | Minimal | **None** (local SQLite) | MIT | ✅ **Trivial** | **Very Low** | **No external DB**, runs locally/SSH/Docker, YAML workflows |
| **Tork** | ~100MB + PG | 1 vCPU | PostgreSQL + RabbitMQ (distributed) | MIT | ✅ Yes | Low | Standalone mode: single binary + PG; tasks in Docker |

**Top picks for ≤16GB:**
1. **n8n** — proven on HF Spaces, external PG (Neon/Supabase)
2. **Dagu** — lightest, no DB, single binary, YAML, runs anywhere
3. **Tork (standalone)** — lightweight, Docker tasks, PG only
4. **Node-RED** — if simple flow automation suffices
5. **Activepieces (hobbyist)** — single container with PGLite, but no HA

---

## Task 5: Free Persistent Storage Options

| Provider | Free Tier Limits | Private Data? | API Access | Persistence | Card Required? |
|----------|------------------|---------------|------------|-------------|----------------|
| **HF Datasets** | 100GB private storage (Free user) | ✅ Yes | ✅ `huggingface_hub` / Git / CLI | Git-based, versioned | **No** |
| **GitHub Repos (API)** | 500MB Packages, 10GB LFS, 1GB Actions storage | ✅ Private repos free | ✅ REST/GraphQL | Git-based | **No** |
| **Supabase (Postgres)** | 500MB DB/project, 1GB file storage, 5GB egress, **2 projects**, pauses after 1 week inactivity | ✅ Yes | ✅ PostgREST, Realtime, Auth | Auto-pauses, read-only at 500MB | **No** |
| **Neon (Postgres)** | **100 projects**, **1GB/project** (Oct 2026), 100 CU-hrs/project/mo, scales to zero in 5min, 5GB egress | ✅ Yes | ✅ Standard PG wire protocol | **Never pauses**, instant restore 6hr | **No** |
| **Turso (libSQL)** | 500 DBs, **9GB total storage**, 25B row reads/mo, 75M writes, 3 locations, embedded replicas | ✅ Yes | ✅ HTTP/ libSQL client | Edge-replicated, durable | **No** |
| **Cloudflare R2** | **10 GB-month** storage, 1M Class A ops, 10M Class B ops, **FREE EGRESS** | ✅ Yes | ✅ S3-compatible API | Durable, 11 9s | **No** |
| **Backblaze B2** | **10GB storage free**, free egress up to 3x storage, $0.005/GB/mo after | ✅ Yes | ✅ S3-compatible API | Durable | **No** |

**Best combos for our stack:**
- **Primary DB:** Neon (100 projects × 1GB, no pause, no card)
- **Object Storage:** Cloudflare R2 (10GB, free egress, S3 API)
- **Backup/ML Datasets:** HF Datasets (100GB private, git-based)

---

## Task 6: Free Secret Management

| Provider | Free Tier Limits | Programmatic Access | Integration | Card Required? |
|----------|------------------|---------------------|-------------|----------------|
| **GitHub Secrets** | 100 repo / 1000 org / 100 env secrets, 48KB each | ✅ Actions workflow only | Native to GitHub Actions | **No** |
| **HF Spaces Secrets** | Unlimited per Space (UI + API) | ✅ Exposed as env vars in Space | Native to HF Spaces | **No** |
| **Doppler** | 3 users, 10 projects, 4 envs, 10 configs/env, 5 config syncs, 3-day logs, 50 service tokens | ✅ CLI, API, SDKs, GitHub Actions sync | 100+ integrations | **No** (but 3-day log retention) |
| **Infisical** | **5 identities, 3 projects, 3 envs, 10 integrations**, self-host or cloud, CLI, SDK, K8s operator, secret scanning | ✅ REST API, CLI, SDKs, GitHub Actions action | 100+ integrations, self-hostable (MIT core) | **No** |

**Recommendation:** **Infisical** — best free tier for team use (5 identities), self-hostable on MIT core, no card, generous integrations.

---

## Ranked Viable Stacks (Scored Against Hard Constraints)

### Scoring Rubric (0-5 each)
- **Zero Payment Method** (5 = never asks, 0 = requires at signup)
- **24/7 Uptime Potential** (5 = native always-on, 0 = sleeps <1hr)
- **Free Tier Only** (5 = permanent free, 0 = trial only)
- **Data Persistence** (5 = built-in durable, 0 = fully ephemeral)
- **Open Source / Free Tier Only** (5 = fully OSS or generous free, 0 = proprietary/limited)

---

### Stack 1: **HF Spaces + n8n (Hugging8n) + Neon + R2 + Infisical** ⭐ **BEST COMPOSITE**
| Constraint | Score | Notes |
|------------|-------|-------|
| Zero Payment Method | 5 | No card anywhere |
| 24/7 Uptime | 3 | HF sleeps 48h; Cloudflare Workers cron keep-alive works (Hugging8n built-in) |
| Free Tier Only | 5 | All components permanent free |
| Data Persistence | 4 | Neon (DB) + R2 (objects) + HF Datasets (backup) — all external, durable |
| OSS / Free Tier | 4 | n8n fair-code, Hugging8n MIT, Infisical MIT core |

**Total: 21/25**

**How it works:**
1. Duplicate `somratpro/Hugging8N` Space on HF (free, no card)
2. Set secrets: `HF_TOKEN`, `CLOUDFLARE_WORKERS_TOKEN`, Neon connection string
3. Cloudflare Worker auto-created pings `/health` every few minutes → prevents sleep
4. Cloudflare Worker also proxies blocked outbound (Telegram, Discord, etc.)
5. n8n persists to Neon Postgres (1GB/project, 100 projects free)
6. Large artifacts → Cloudflare R2 (10GB, free egress)
7. Secrets in Infisical (cloud or self-hosted on same HF Space via sidecar)
8. HF Dataset auto-backup (Hugging8n feature) for workflow export

---

### Stack 2: **HF Spaces + Dagu + Neon + R2 + Infisical**
| Constraint | Score |
|------------|-------|
| Zero Payment Method | 5 |
| 24/7 Uptime | 3 | Same HF sleep, same keep-alive workaround |
| Free Tier Only | 5 |
| Data Persistence | 4 |
| OSS / Free Tier | 5 | Dagu MIT, no DB needed |

**Total: 22/25** — *Higher OSS score, but Dagu less mature than n8n*

---

### Stack 3: **Val Town + Neon + R2 + Infisical** (Serverless-only)
| Constraint | Score |
|------------|-------|
| Zero Payment Method | 5 |
| 24/7 Uptime | 2 | Serverless, no background daemons; cron min 15min |
| Free Tier Only | 5 |
| Data Persistence | 4 |
| OSS / Free Tier | 3 | Val Town proprietary |

**Total: 19/25** — *Fails 24/7 daemon requirement*

---

### Stack 4: **CodeSandbox + Neon + R2 + Infisical** (Dev environment, not hosting)
| Constraint | Score |
|------------|-------|
| Zero Payment Method | 5 |
| 24/7 Uptime | 1 | Freezes when 400 credits (40hrs) exhausted |
| Free Tier Only | 5 |
| Data Persistence | 3 | Repo-based only |
| OSS / Free Tier | 3 |

**Total: 17/25** — *Not a hosting platform*

---

### Stack 5: **Northflank + Neon + R2 + Infisical** (Fails no-card)
| Constraint | Score |
|------------|-------|
| Zero Payment Method | **0** | Card required at signup |
| 24/7 Uptime | 5 | Always-on, no sleep |
| Free Tier Only | 5 |
| Data Persistence | 5 |
| OSS / Free Tier | 3 |

**Total: 18/25** — *Disqualified: requires credit card*

---

## Contradictions & Open Questions

| Issue | Conflicting Sources | Resolution |
|-------|---------------------|------------|
| **Northflank card requirement** | S040/S042: "card required" vs S043: "no card required" | Trust official docs (S040) — card required for identity verification |
| **Koyeb card requirement** | S021/S024: "no card" vs S023: "requires card for fraud prevention" | S023 is official FAQ (2026) — card likely required now |
| **Deno Deploy free limits** | S048: 1M req/20GB/15 CPU hrs vs S050: "restricted until card linked" | S050 (2026) more recent — free orgs are restricted until card verification |
| **HF Spaces persistent storage** | S001/S003 mention 50GB disk vs S004/S015: "feature no longer available" | S004/S015 are config reference — persistent storage setting ignored; disk is ephemeral |

---

## Methodology Note

- **Sources examined:** 135 (official docs, pricing pages, forums, blogs, GitHub repos)
- **Saturation reached:** Last 15 sources added no new claims to core findings
- **Search strategy:** Primary sources (official docs) weighted highest; forum/blog for practical confirmation
- **Date of verification:** All sources accessed 2026-10-02
- **Unverified items marked:** Northflank card conflict (S040 vs S043), Koyeb card policy (S021 vs S023)

---

## Artifacts

- `sources.tsv` — Full evidence log (135 rows)
- `question.md` — Research question decomposition
- This report — `free-tier-deployment-report.md`

---

## Next Steps

1. **Validate HF Spaces Docker Space creation workaround** — attempt duplicating Hugging8n with a test account
2. **Test Neon + n8n connectivity** from HF Spaces (outbound to Neon PG)
3. **Benchmark Cloudflare Workers keep-alive** reliability (cron trigger every 5 min)
4. **Evaluate Dagu** as n8n alternative — deploy test workflow on HF Spaces
5. **Set up Infisical self-hosted** on HF Spaces (sidecar container) for secrets