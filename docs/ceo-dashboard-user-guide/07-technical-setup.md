## Technical Setup

This section covers installation, configuration, authentication, and startup procedures for the CEO Dashboard.

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.12+ | Check with `python --version` |
| uv | Latest | Package manager; install from [astral.sh/uv](https://astral.sh/uv) |
| Node.js | Not required | Frontend assets are served statically by FastAPI |
| Git | Any recent | For cloning the repository |
| OS | Windows, macOS, or Linux | PowerShell used in examples below |

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/light-speed-holdings/ai-company-builder.git
cd ai-company-builder

# 2. Install all dependencies (creates .venv if absent)
uv sync --extra dev

# 3. Install pre-commit hooks (ruff, mypy, bandit)
pre-commit install
```

After installation, verify the CLI is available:

```bash
uv run ai-company dashboard --help
```

### Configuration

#### Environment Variables

The dashboard reads configuration from environment variables. Copy `.env.example` to `.env` and fill in actual values:

```bash
cp .env.example .env   # then edit .env with your values
```

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DASHBOARD_PORT` | Port the dashboard listens on | `8420` | No |
| `DASHBOARD_HOST` | Bind address | `127.0.0.1` | No |
| `DASHBOARD_AUTH_MODE` | Auth mode: `api_key` or `open` | `api_key` | No |
| `DASHBOARD_CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:8420` | No |
| `DASHBOARD_RATE_LIMIT` | Max requests per minute per client | `100` | No |
| `DASHBOARD_ADMIN_KEY` | Admin role key (full access) | — | Yes (api_key mode) |
| `DASHBOARD_APPROVE_KEY` | Approve role key (approve/reject) | — | Recommended |
| `DASHBOARD_RUN_KEY` | Run role key (execute tasks, read KPIs) | — | Recommended |
| `DASHBOARD_API_KEY` | Legacy single-key alias for admin | — | Yes (if RBAC keys unset) |
| `OPENCODE_API_KEY` | Primary LLM provider key | — | Yes |
| `GEMINI_API_KEY` | Fallback LLM provider key | — | Recommended |

**Notes:**

- `DASHBOARD_API_KEY` is a legacy alias for `DASHBOARD_ADMIN_KEY`. If both are set, the RBAC key takes precedence.
- Keys are hierarchical: `admin` implies `approve` implies `run`.
- `DASHBOARD_AUTH_MODE=open` is restricted to loopback hosts only (`127.0.0.1` / `::1`). The server refuses to start if `open` mode is used with a non-loopback host.

#### Configuration Files

| File | Purpose |
|------|---------|
| `config/org_health.yaml` | Health score bands (green/amber/red thresholds) and component weights. Weights must sum to 1.0. |
| `config/company/kpis.yaml` | Company-level KPI definitions, targets, and computed values. |
| `.env` | Runtime secrets (never commit to git). |
| `.opencode/inbox.json` | Task queue / fallback data store when SQLite is empty. |

### Authentication Setup

#### Generating RBAC Keys

Generate cryptographically secure keys for each role:

```bash
uv run python -c "import secrets; [print(secrets.token_urlsafe(32)) for _ in range(4)]"
```

This produces 4 keys. Assign them in `.env`:

```
DASHBOARD_ADMIN_KEY=<key1>
DASHBOARD_APPROVE_KEY=<key2>
DASHBOARD_RUN_KEY=<key3>
DASHBOARD_API_KEY=<key4>       # legacy alias, can mirror admin key
```

#### Role Permissions

| Role | Key Variable | Capabilities |
|------|-------------|--------------|
| `admin` | `DASHBOARD_ADMIN_KEY` | All endpoints, full access |
| `approve` | `DASHBOARD_APPROVE_KEY` | Approve/reject tasks and escalations |
| `run` | `DASHBOARD_RUN_KEY` | Execute tasks, read KPIs |
| `admin` (legacy) | `DASHBOARD_API_KEY` | Same as admin; for backward compatibility |

#### Key Rotation Schedule

| Trigger | Action |
|---------|--------|
| Every 90 days | Rotate all 4 keys on schedule |
| Suspected compromise | Rotate immediately |
| Team member with access departs | Rotate immediately |
| Security incident | Rotate immediately |

Full rotation procedure is documented in [docs/DASHBOARD_KEY_ROTATION.md](../../docs/DASHBOARD_KEY_ROTATION.md). Summary: generate new keys → update `.env` → update staging/production secrets → verify health endpoints → revoke old keys → record in CHANGELOG.md.

#### Session Tokens

Session tokens (ADR-013) are minted on-demand via the bootstrap endpoint. They are:

- **Short-lived** — expire after a configurable window
- **IP-bound** — tied to the client IP that requested them
- **In-memory** — not persisted; lost on server restart

Session tokens do not need rotation — only the static environment keys do.

### Starting the Dashboard

```bash
# Start with default settings (port 8420, opens browser)
uv run ai-company dashboard

# Start on a custom port
uv run ai-company dashboard --port 8421

# Start without auto-opening the browser
uv run ai-company dashboard --no-open

# Bind to all interfaces (requires api_key auth mode)
uv run ai-company dashboard --host 0.0.0.0
```

The server prints the startup URL:

```
Starting CEO dashboard at http://127.0.0.1:8420
Press Ctrl+C to stop.
```

#### Verifying Startup

Open a browser to `http://localhost:8420`. The dashboard loads with KPI cards, task kanban, agent status, and charts.

Alternatively, verify via the health endpoint:

```bash
curl -H "X-API-Key: $DASHBOARD_ADMIN_KEY" http://localhost:8420/health
```

Expected response: `{"status":"ok"}` with HTTP 200.

If using browser session tokens (ADR-013), call the bootstrap endpoint first to mint a session, then include the session token in subsequent requests.

#### Staging Environment

For running alongside production or testing configuration changes:

```bash
docker compose -f docker-compose.staging.yml up --build
```

Staging runs on host port **8421** (maps to container 8420). The production dashboard runs on **8420**.

---

## Troubleshooting

### Known Issues

The following issues are tracked and documented in `knowledge/technology/dashboard-known-issues.md`.

| ID | Symptom | Likely Cause | Workaround | Status |
|----|---------|-------------|------------|--------|
| DASH-001 | Dashboard scrolls to top on auto-refresh (every 10 s) | Alpine.js reactivity triggers full DOM re-render on data update | Avoid scrolling during refresh cycles; use keyboard navigation to return to position | Open — Sprint 4 |
| DASH-002 | WebSocket indicator flickers between green (live) and red (offline) | Connection drops and reconnects; basic reconnect logic without exponential backoff | Click "Reconnect" in the header when offline; flicker is visual only, data recovers | Open — Sprint 4 |
| DASH-003 | No loading spinners or indicators appear during data fetch | No loading state tracking in the Alpine.js data model | Wait for data to appear; if empty state persists, refresh the page | Open — Sprint 4 |
| DASH-004 | Failed API calls produce no visible error — data simply doesn't update | `fetchJSON()` catches errors but only logs to browser console | Open browser DevTools console (F12) to see error messages; refresh page | Open — Sprint 4 |
| DASH-005 | Multiple toast notifications overlap each other in the corner | Rapid-fire updates generate multiple toasts before prior ones dismiss | Wait for auto-dismiss; refresh page to clear | Open — Sprint 4 |
| DASH-006 | Kanban card drag is interrupted mid-drag by a data refresh | Auto-refresh fires while user is interacting with the board | Complete drag operations quickly (before next 10 s refresh); refresh page if card misplaces | Open — Sprint 4 |
| DASH-007 | Charts briefly flicker (disappear/reappear) on data update | Chart.js redraws the canvas on data change | Visual only; no data loss. Charts stabilize within a second. | Open — Sprint 4 |
| DASH-008 | No way to manually refresh a single section (KPIs, tasks, agents) | No per-section refresh controls in the UI | Refresh the entire page (F5 or Ctrl+R) | Open — Sprint 4 |

### Authentication Problems

| Symptom | What to Check |
|---------|---------------|
| **"Cannot connect to dashboard"** | Confirm the server is running (`uv run ai-company dashboard`). Check `DASHBOARD_PORT` matches the URL you're opening. Verify `DASHBOARD_HOST` is set to `127.0.0.1` for local access. |
| **401 Unauthorized** | The `X-API-Key` header is missing or the key value is empty/placeholder. Verify `.env` contains actual generated keys, not `your_admin_key_here`. Check for whitespace or newline characters at the end of the key value. |
| **403 Forbidden** | The key you provided belongs to a lower-privilege role. For example, a `run` key cannot access admin-only endpoints. Use the correct key for the endpoint's required role. |
| **Session expired / repeated 401s** | Session tokens (ADR-013) are IP-bound and short-lived. Your IP may have changed (VPN, Wi-Fi switch), or the token expired. Call the bootstrap endpoint again to mint a new session. |
| **Browser shows "open" mode error** | `DASHBOARD_AUTH_MODE=open` only works on loopback (`127.0.0.1`). If deploying on a network, use `api_key` mode and set RBAC keys. |
| **WebSocket connection fails** | For WebSocket URLs, pass the API key as a query parameter (`?api_key=...`). Check that `DASHBOARD_CORS_ORIGINS` includes your origin. |

### Data Issues

| Symptom | What to Check |
|---------|---------------|
| **"No data showing" / blank dashboard** | Check that the SQLite database exists and has records, or that `.opencode/inbox.json` contains task data. Run `uv run python scripts/compute_company_kpis.py` to verify KPI computation. |
| **KPIs show "n/a" or null** | Some KPIs (KPI-001, KPI-002, KPI-005) have no data source yet — this is expected. KPI-003 and KPI-004 compute from `.opencode/inbox.json`. Verify inbox.json is populated. |
| **Stale data / "last updated" timestamp is old** | The dashboard polls every 10 seconds. If data hasn't changed, the timestamp is correct. If you suspect a data pipeline issue, run `python scripts/compute_company_kpis.py --write` to refresh computed values. |
| **Health score is missing** | Health score requires at least one task in the database. Check that `config/org_health.yaml` weights sum to 1.0. Verify SQLite is accessible. |
| **Charts show no data** | Confirm the relevant data source (inbox.json or SQLite) has records. Check the browser console (F12) for API errors logged by `fetchJSON()`. |

### Performance Issues

| Symptom | What to Check |
|---------|---------------|
| **Dashboard loads slowly** | Check network latency to the server. On first load, static assets (Tailwind CSS, Chart.js) must download. Subsequent loads use browser cache. Verify SQLite database is not excessively large. |
| **High memory usage after extended sessions** | WebSocket reconnections may accumulate event listeners. Refresh the page periodically during long sessions. Restart the server if memory grows unbounded. |
| **API requests are slow** | Check `DASHBOARD_RATE_LIMIT` — if set too low, legitimate requests may be throttled. Verify the SQLite database is not locked by a concurrent process. Check LLM provider latency if KPI computation involves AI calls. |
| **Server won't start — port in use** | Another process is using port 8420. Either stop the other process or start the dashboard on a different port: `uv run ai-company dashboard --port 8421`. |

### Getting Help

| Channel | Use For |
|---------|---------|
| **GitHub Issues** | Bug reports, feature requests. Include the issue ID (e.g., DASH-001) if referencing a known issue. |
| **Browser Console (F12)** | First step for any UI issue. API errors, WebSocket failures, and JS exceptions are logged here. |
| **Server Logs (terminal)** | First step for backend issues. uvicorn logs all requests and errors to stdout. |
| **Dashboard "Report Issue" Button** | In-dashboard feedback form (footer). Automatically collects browser info, connection status, and recent errors. |
| **Support Knowledge Base** | `knowledge/technology/dashboard-known-issues.md` — full details on all tracked issues with root cause analysis. |

When reporting an issue, include:

1. Steps to reproduce
2. Expected vs. actual behavior
3. Browser console output (F12 → Console tab)
4. Server terminal output
5. `curl` output from `http://localhost:8420/health` (if server is running)
6. Environment: OS, Python version, dashboard port
