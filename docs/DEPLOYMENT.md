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
**exits 0 to skip the build** (exit 1 — and any exit ≥ 1 — continues the build; this is
Vercel's contract, live-verified on `dpl_EzKiYqykZhC8dJSnc4T9DCgwq2ed`, 2026-10-13)
when no site-bundle file changed. Vercel records the merge
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

**`.vercelignore` coupling (critical):** Vercel runs `ignoreCommand` inside the
`.vercelignore`-filtered tree. `scripts/` is excluded, so the filter script must
be let back in with the full parent-chain pattern (gitignore cannot re-include a
file under an excluded directory — a bare `!/scripts/deploy/vercel-ignore-build.sh`
next to `/scripts/` is inert):

```
/scripts/*
!/scripts/deploy/
/scripts/deploy/*
!/scripts/deploy/vercel-ignore-build.sh
```

Without it every deployment fails at the ignore step with
`ENOENT ... exit code 127` (incidents `c9cecc05` and `2927304d`, 2026-10-12).
`scripts/test/check-vercelignore.py` asserts the script survives the rules —
never delete its `STATIC_REQUIRED` entry or the pattern above; if the script
moves, update `vercel.json`, `.vercelignore`, and the guard together.

**Exit-code contract (critical):** Vercel's Ignored Build Step uses the *opposite*
of Unix intuition: **0 skips, 1 builds**. PR #449 shipped the inverted mapping
(0=build, 1=skip); it never ran successfully before the ENOENT incidents masked
it, and the first live run (`dpl_EzKiYqykZhC8dJSnc4T9DCgwq2ed`, exit 0 with a
"building." message) was CANCELED. Fixed in PR #452. Never flip these exits
without re-reading this section and the script header.

**Force a production deploy** without a site change: redeploy the latest deployment
from the Vercel dashboard (Redeploy), or push a trivial site-file touch (e.g. a comment
in `vite.config.ts`). The retry workflow (§5) is unaffected — it only re-runs
deployments whose `readyState` is `ERROR`, and skipped builds never reach that state.

<!-- skip-filter verification marker 2026-10-13 -->

## Security headers

Every route gets the same header set from the catch-all rule (`"source": "/(.*)"`) in
[`vercel.json`](../vercel.json). [`src/__tests__/security-headers.test.ts`](../src/__tests__/security-headers.test.ts)
parses that file and fails on a missing header, a changed value, a duplicate header key or
CSP directive, or a CSP origin outside `'self'`, `data:`, and the Turnstile host.

| Header | Value | Enforcement status |
|--------|-------|--------------------|
| `X-Content-Type-Options` | `nosniff` | Enforced (browser honours) |
| `X-Frame-Options` | `SAMEORIGIN` | Enforced (browser honours) |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Enforced (browser honours) |
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains; preload` | Enforced (browser honours); `preload` has no effect until the domain is accepted onto the HSTS preload list, which has not been requested |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=(), payment=(), usb=(), browsing-topics=(), display-capture=(), hid=(), serial=(), bluetooth=(), idle-detection=(), accelerometer=(), gyroscope=(), magnetometer=()` | Enforced (browser honours) |
| `Cross-Origin-Opener-Policy` | `same-origin` | Enforced (browser honours) |
| `X-DNS-Prefetch-Control` | `off` | Enforced (browser honours) |
| `Content-Security-Policy-Report-Only` | `default-src 'self'; script-src 'self' https://challenges.cloudflare.com; frame-src https://challenges.cloudflare.com; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self' https://challenges.cloudflare.com; form-action 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'self'; upgrade-insecure-requests` | **Report-only — blocks nothing** |

### Why the CSP is `Report-Only`

The contact form depends on Cloudflare Turnstile. A wrong `script-src` breaks the widget
silently: the challenge never renders, the form cannot be submitted, and nothing in the
build or the type-checker notices. So the policy ships as
`Content-Security-Policy-Report-Only`, which reports violations (if a collector existed —
see below) but **does not block any resource or inline script**. The site's actual protection
today comes from the enforced headers above, not from this policy.

### How violations are observed (honest scope)

**No report collector exists.** The header has no `report-uri` and no `report-to` directive,
so no violation reports are sent anywhere or stored. Observation is entirely manual:

1. **Console scan** of `/`, `/contact`, `/use-cases`, and `/ai-company-builder` at 375, 1024,
   and 1440 px widths, looking for console messages containing `Content Security Policy`.
2. **Manual DevTools** inspection of the same routes (Console + Network), on production.

Two directives are inert in Report-Only mode: `frame-ancestors` and
`upgrade-insecure-requests`. Browsers ignore both when the policy is report-only, so a
violation of either is neither blocked nor reported. Framing is actually prevented by
`X-Frame-Options: SAMEORIGIN`.

### Known preview noise

On **preview** deployments only, Vercel's preview toolbar (`vercel.live`) violates
`script-src 'self'` and produces CSP console noise that production does not. It is
deliberately **not** allowlisted: widening `script-src` for a Vercel-injected preview-only
script would weaken the production policy. Disregard `vercel.live` reports when scanning
previews, and confirm the production scan is clean.

### Deferred

- **Enforcement flip** — switching `Content-Security-Policy-Report-Only` to an enforcing
  `Content-Security-Policy`. Target **2026-11-01**, contingent on a clean observation window
  on the four routes above (and on Turnstile still working in an enforcing policy).
- **`style-src-attr` narrowing** — the site sets React inline styles directly (99
  `style={{ ... }}` occurrences across 15 files under `src/`, plus Framer Motion writing to
  `element.style` at runtime), so `style-src` keeps `'unsafe-inline'`. Splitting
  `style-src-attr` (or migrating the inline styles) would let `style-src` drop it.
