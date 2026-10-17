# CTO Technical Ratification — Marketing Site / CEO Dashboard Application Boundary

**Date:** October 10, 2026
**From:** Chief Technology Officer
**To:** Chief Strategy Officer, Chief of Staff, Engineering (lead_backend, lead_frontend, solution_architect, vp_engineering)
**Ratifies:** `docs/organization/app-naming-and-port-assignments.md` (CSO directive v1.0, 2026-10-10)
**Status:** RATIFIED — with mandatory enforcement conditions (§6)

---

## 1. Verdict

The CSO directive is **technically sound and hereby ratified**. The two-application split it
describes already exists in the codebase and matches the declared port assignments. No
architectural contradiction was found.

Ratification is **conditional**: the directive's "enforced standards" (§4 of the directive) are
currently *documented but not machine-enforced*. Until §7 actions land, compliance depends on
human discipline. The enforcement gaps are listed as required engineering work.

---

## 2. Ratified Application Boundary

| Aspect | CEO Dashboard (internal) | Marketing Site (external) |
|---|---|---|
| **Runtime** | Python 3.12 / FastAPI / uvicorn | Node.js / Vite 7 / React 18 SPA |
| **Process launcher** | `uv run ai-company dashboard` or Docker `CMD` | PM2 (`ecosystem.config.cjs`), or `npm run dev/preview` |
| **Source root** | `src/ai_company/dashboard/`, `src/ai_company/cli/dashboard.py` | repo-root `src/`, `vite.config.ts`, `package.json` |
| **Dev port** | **8421** (staging/CI; local dev passes `--port 8421`) | **1441** (`vite.config.ts` → `server.port`) |
| **Prod port** | **8420** (`Dockerfile EXPOSE 8420`, compose `8420:8420`) | **443** on Vercel (`lightspeedholdings.vercel.app`) |
| **Preview port** | n/a | **1440** (`vite.config.ts` → `preview.port`) |
| **Health check** | `GET /health` → JSON `{"status": "ok"\|"degraded"}`, auth-exempt | `GET /` → HTTP 200 (SPA HTML); no `/health` exists |
| **Deploy target** | Docker image → internal infra (prod 8420, staging host 8421→8420) | Static `dist/` → Vercel; PM2 for local dev/preview |
| **Owner** | CTO / Engineering | Chief Marketing Officer |
| **CORS role** | Server; allowlists the Marketing Site origins as *clients* | Client; origin `http://localhost:1440`/`:1441` |

**Ratified rules:**

1. Ports **1440/1441** are bound only by the Marketing Site; **8420/8421** only by the Dashboard.
2. Never serve one application on the other's port; never probe one app's health contract against the other.
3. CORS allowlist entries are permitted *origins*, not port assignments — they do not imply either app may bind the other's port.
4. Port assignments are fixed; repointing requires CSO + CTO authorization and a change to this document, `AGENTS.md` §12/§13, and `docs/organization/app-naming-and-port-assignments.md`.

---

## 3. Evidence (verified 2026-10-10)

| Claim | Source |
|---|---|
| Vite dev port 1441 | `vite.config.ts:48` (`server.port: 1441`) |
| Vite preview port 1440 | `vite.config.ts:52` (`preview.port: 1440`) |
| PM2 dev app → 1441 | `ecosystem.config.cjs` app `vite-dev`, `args: "dev"`, `port: 1441` |
| PM2 preview app → 1440 | `ecosystem.config.cjs` app `vite-preview`, `args: "preview"`, `port: 1440` |
| Dashboard CLI default 8420 | `src/ai_company/cli/dashboard.py:23` (`typer.Option(8420)`) |
| Dashboard prod bind 8420 | `Dockerfile:52` (`EXPOSE 8420`), `Dockerfile:59` (`CMD ... --port 8420`) |
| Dashboard prod health probe | `Dockerfile:55-56` (`HEALTHCHECK ... curl -f http://localhost:8420/health`) |
| Compose prod mapping | `docker-compose.yml` `8420:8420`, healthcheck `:8420/health` |
| Compose staging mapping | `docker-compose.staging.yml` `${STAGING_DASHBOARD_PORT:-8421}:8420` |
| CI dashboard health gate | `.github/workflows/ci.yml` (e2e job starts dashboard on 8421, polls `/health`) |
| `/health` auth-exempt | `src/ai_company/dashboard/app.py:236-239` (ADR-012 / GAP-011) |
| `/health` JSON contract | `src/ai_company/dashboard/monitoring.py:703-704`, status `"ok"`/`"degraded"` at `:797` |
| CORS allows Marketing Site origins | `src/ai_company/dashboard/app.py:459-468` |
| Marketing Site health probe (local) | `scripts/dev/health-check.ps1` (polls `:1441/` and `:1440/` for HTTP 200) |
| Vite build gate wired to config | `.github/workflows/site-principles-gate.yml` (triggers on `vite.config.ts`, `package.json`) |
| Prior port work shipped | commit `272ff91a` "feat(ports): assign Vite dev=1441 / preview=1440 with CORS parity (#426)" |

---

## 4. PM2 Ecosystem Review

Reviewed `ecosystem.config.cjs` (both processes).

| # | Finding | Severity | Action |
|---|---|---|---|
| F1 | **PM2 `port` is metadata, not enforcement.** PM2 does not bind, reserve, or verify ports — Vite binds whatever `vite.config.ts` (or a `--port` override) dictates. The `port: 1441` / `port: 1440` fields only mirror intent for `pm2 status` display. Parity with `vite.config.ts` is correct today but unverified by any check. | High | G-1 (static guard), G-3 (runtime guard) |
| F2 | **Hardcoded absolute Windows path** in `script:` (`C:\Users\jmlus\light-speed-holdings\node_modules\.bin\vite.exe`). Breaks any other checkout, CI, Linux host, or container. | High | G-4 (portable `script` + `cwd: __dirname`) |
| F3 | No readiness/health integration in PM2 config (no `wait-ready`, no restart backoff tuning). Readiness is handled out-of-band by `scripts/dev/health-check.ps1`. | Low | G-5 (identity-aware probe) |
| F4 | Both apps correctly use one `cwd` (repo root) and separate `args`, so dev and preview cannot collide with each other. | OK | none |

**Verdict on PM2:** structurally correct (two apps, right ports, right args), but F1/F2 mean it is
*documentation of intent* rather than a control. G-1 and G-4 close this.

---

## 5. Health-Check Separation (ratified contracts)

| | Dashboard | Marketing Site |
|---|---|---|
| Endpoint | `GET /health` | `GET /` (root document) |
| Success signal | HTTP 200 + JSON containing `status: "ok"` | HTTP 200 + HTML |
| Auth | Exempt from API-key middleware (ADR-012) | n/a (static) |
| Consumers | Docker `HEALTHCHECK`, staging compose, CI e2e job, ops dashboards | `scripts/dev/health-check.ps1`, local dev |

**Rules:**

- A probe against **8420/8421** must assert a JSON `status` field — an HTML response there means the
  Marketing Site is cross-serving on a dashboard port (fail the check).
- A probe against **1440/1441** must assert HTML (Vite/SPA signature) — a JSON `status` response there
  means the Dashboard is cross-serving on a Marketing Site port (fail the check).
- Never point the Docker `HEALTHCHECK` or CI dashboard gate at 1440/1441, or the Vite readiness poll at 8420/8421.

---

## 6. Enforcement: Current State vs Gaps

**Exists today:**

- Documentation: `AGENTS.md` §12/§13, `docs/organization/app-naming-and-port-assignments.md`, `README.md` §1-2 (in flight).
- CI: dashboard e2e health gate on 8421 (`.github/workflows/ci.yml`); Vite build gate on config change (`site-principles-gate.yml`).
- Prod: Docker `EXPOSE 8420` + `HEALTHCHECK :8420/health` + `CMD --port 8420`; compose port mappings.
- Startup guard (one only): `DASHBOARD_AUTH_MODE=open` refuses non-loopback hosts — `src/ai_company/cli/dashboard.py:44-50`.
- CORS unit coverage: `tests/unit/test_dashboard_security.py`.

**Missing (these are the conditional obligations of this ratification):**

- No test asserts the four ports across `vite.config.ts`, `ecosystem.config.cjs`, the dashboard CLI default, and compose files.
- No runtime refusal when the Dashboard is asked to bind 1440/1441, or Vite is asked to bind 8420/8421 (including via `--port` CLI override).
- No CI check on frontend-only changes that could retarget ports without running Python tests.
- No port-binding *identity* audit (which process actually owns each port).
- PM2 non-portability (F2).

---

## 7. Required Engineering Actions

Priority: **P0** = ratification blocker; **P1** = next sprint; **P2** = hardening.

| ID | Priority | Action | File(s) |
|---|---|---|---|
| **G-1** | P0 | Add static port-assignment guard test: assert `server.port==1441`, `preview.port==1440`; `vite-dev→1441`, `vite-preview→1440`; dashboard CLI default `==8420`; compose `8420:8420` and staging default `8421`; and `dashboard_ports ∩ vite_ports == ∅`. Runs in the existing pytest gate. | **new** `tests/unit/test_port_assignments.py`; consumed by `.github/workflows/ci.yml` (existing `uv run pytest`) |
| **G-2** | P0 | Runtime fail-fast in dashboard CLI: refuse `--port 1440` / `--port 1441` with a message naming the Marketing Site, exiting non-zero. Follows the existing ADR-012 guard pattern already in the same function. | `src/ai_company/cli/dashboard.py` (adjacent to lines 44-50) |
| **G-3** | P0 | Runtime fail-fast in Vite: a small inline plugin asserting the resolved `server.port` / `preview.port` are not 8420/8421, throwing with a message naming the CEO Dashboard. Use `configResolved` so a `vite --port 8420` CLI override is also caught. | `vite.config.ts` (plugins array, line 17) |
| **G-4** | P1 | PM2 portability: replace the absolute `.exe` path with a repo-relative `script: "node_modules/vite/bin/vite.js"` + `cwd: __dirname`; keep `port` fields and add a comment that they are declarative metadata (parity enforced by G-1). | `ecosystem.config.cjs` |
| **G-5** | P1 | Port-binding identity audit: script that maps listeners on 1440/1441 to a `node`/vite process and 8420/8421 to a `python`/uvicorn process, and performs the §5 contract probes (HTML vs JSON `status`). Also remove the unused hardcoded `$ProjectRoot` path. | **new** `scripts/dev/verify-port-bindings.ps1`; cleanup `scripts/dev/health-check.ps1:4` |
| **G-6** | P1 | Frontend-only CI guard: add a port-assertion step so a PR touching only `vite.config.ts` cannot retarget ports without Python CI running. | `.github/workflows/site-principles-gate.yml` (already triggers on `vite.config.ts`) |
| **G-7** | P2 | Prod residual-risk note: Marketing Site production is Vercel (port 443), so cross-serving on 8420/8421 is structurally impossible in production; the only exposure is local/dev/staging. Record this as accepted residual in the directive checklist. | `docs/organization/app-naming-and-port-assignments.md` (§5 checklist) |

**Change control:** G-1…G-6 span more than two files and touch architecture-adjacent guards, so per
`docs/ECL.md` they must ship as a **single ECL change** (open via the harness script; `harness/changes/active/`
is currently empty). Do not hand-edit `harness/changes/INDEX.json`.

---

## 8. Change-Control Notes

- **This ratification changes no code.** It is a document only.
- A concurrent session holds **uncommitted work** in this exact area (`ecosystem.config.cjs`,
  `src/ai_company/dashboard/app.py`, `tests/unit/test_dashboard_security.py`,
  `scripts/dev/health-check.ps1`, `README.md`, `AGENTS.md`, plus the untracked
  `docs/organization/` directory). Whoever implements §7 must re-read `git status` and `git diff`
  first, build on those edits, and must not revert them.
- `AGENTS.md` §12/§13 already encodes this boundary in executable agent guidance; this document is
  the engineering-facing ratification of the same decision. If they ever diverge, `AGENTS.md` §12/§13
  and this document must be updated together.

---

## 9. Sign-Off

Ratified by the Chief Technology Officer on 2026-10-10. §7 P0 items (G-1, G-2, G-3) are required
before the directive may be marked fully enforced; P1/P2 items are scheduled engineering work.

**Related, pending elsewhere:** `harness/evolution/pending.md` holds an unprocessed evolution
trigger (reindex, 6+ archived candidates) — outside this ratification's scope, awaiting a decision
from the Chief of Staff on whether to process it.

---

## Revision History

| Date | Version | Author | Change |
|---|---|---|---|
| 2026-10-10 | 1.0 | Chief Technology Officer | Initial ratification of CSO directive v1.0 |
