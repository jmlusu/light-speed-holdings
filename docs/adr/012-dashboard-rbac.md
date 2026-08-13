# ADR-012: Dashboard RBAC + Loopback-Only `open` Auth Mode

**Status:** Accepted
**Date:** 2026-08-13
**Deciders:** CISO, Security & Compliance Lead
**Technical Domain:** Dashboard Security

## Context

Dashboard auth was all-or-nothing. In the default `api_key` mode a single
`DASHBOARD_API_KEY` was checked by middleware against every request; in the
explicit `open` mode every request passed regardless of configuration. Two
problems followed:

1. **No privilege separation.** Task mutations, approval decisions, escalation
   resolution, and mobile batch/sync actions all shared one key. A key that can
   dispatch tasks can also approve money or resolve audits, with no way to
   issue a read/run-only credential.
2. **`open` mode was not actually localhost-only.** It disabled auth entirely
   and nothing stopped an operator from binding it to `0.0.0.0` and exposing an
   unauthenticated CEO dashboard on a network interface.

## Decision

Introduce role-based access control and lock `open` mode to loopback.

### 1. RBAC with hierarchical roles

- New module `src/ai_company/security/rbac.py` defines `Role` (`run` →
  `approve` → `admin`, most-to-least privileged) and a `require_role(minimum)`
  FastAPI dependency.
- Roles map to environment-configured keys:

  | Role | Env var |
  |------|---------|
  | `run` (task mutations) | `DASHBOARD_RUN_KEY` |
  | `approve` (approvals, escalations) | `DASHBOARD_APPROVE_KEY` |
  | `admin` (all permissions) | `DASHBOARD_ADMIN_KEY` (falls back to `DASHBOARD_API_KEY`) |

- `admin` implies `approve` implies `run`. The middleware still rejects unknown
  keys with `401`; the per-endpoint dependency rejects an authenticated but
  under-privileged key with `403`.
- Applied to every dashboard write endpoint:
  - `api.py`: task create/update/delete → `run`; approval approve/reject and
    escalation resolve → `approve`.
  - `mobile_api.py`: batch actions, quick-approve, swipe, sync → `approve`;
    notification register/unregister/preferences and batch GET → `run`.

### 2. Loopback-only `open` mode

- `is_loopback_host()` in `dashboard/app.py` accepts `localhost` and any
  literal loopback address (`127.0.0.0/8`, `::1`).
- The CLI (`cli/dashboard.py`) refuses to start with `DASHBOARD_AUTH_MODE=open`
  when `--host` is not loopback.
- `create_app()` raises at startup when `open` mode is combined with a
  non-loopback `DASHBOARD_HOST` (covers direct `uvicorn` launches).

## Consequences

- **Positive:** least-privilege credentials for the dashboard; a leaked run key
  no longer grants approval authority; `open` mode cannot be accidentally
  exposed on a network interface; existing single-key deployments keep working
  unchanged (`DASHBOARD_API_KEY` = admin).
- **Negative / risk:** operators must distribute up to three keys; the CLI
  refuses a previously-accepted configuration (`open` + `0.0.0.0`), which
  requires updating any local dev scripts that relied on it (bind to
  `127.0.0.1` instead). Role keys are static environment config, not an
  identity/issuer system — fine for a single-operator CEO dashboard, but a
  future OAuth token identity (SPRINT-5 T009 groundwork) can supersede it
  without changing the `require_role` interface.
- **Neutral:** read endpoints keep the existing middleware-only key check;
  no new dependencies; no schema changes.

## Links

- ADR-011 superseded on disk (SQLite-first storage) — unrelated to this record.
- GAP-010: dashboard auth fail-closed + CORS lockdown (`docs/ARCHITECTURE-GAPS.md`)
- Evidence: `tests/unit/test_dashboard_rbac.py`
- Existing auth docs: `docs/DASHBOARD_ARCHITECTURE.md`, `docs/SECURITY_HARDENING.md`
