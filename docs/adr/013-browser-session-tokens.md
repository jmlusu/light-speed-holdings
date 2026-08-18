# ADR-013: Browser Session Tokens for the Dashboard

**Status:** Accepted
**Date:** 2026-08-14
**Deciders:** Human operator (via wayfinder grilling ticket #63)
**Technical Domain:** Dashboard Security

## Context

ADR-012 introduced role-gated dashboard auth: in `api_key` mode every request
must present a role key (`DASHBOARD_RUN_KEY` / `DASHBOARD_APPROVE_KEY` /
`DASHBOARD_ADMIN_KEY`), and the WebSocket handshake requires `?api_key=`
resolving to at least `run` because browsers cannot set custom headers on a
WebSocket handshake. Two consequences followed:

1. **The browser UI is dead in `api_key` mode.** The auth middleware 401s every
   HTTP request — including the page routes and GET endpoints — and nothing ever
   injects the `window.DASHBOARD_API_KEY` that `app.js` reads when building the
   WebSocket URL (`static/js/app.js`). The live dashboard effectively only works
   in loopback `open` mode.
2. **Injecting a static env key into the page was not acceptable.** A long-lived
   role key would sit in served HTML/JS — viewable in page source, cacheable,
   and revocable only by hand-rotation — defeating the point of the RBAC keys.

Production deployments bind non-loopback interfaces (`docker-compose.yml`
publishes `8420:8420` on all interfaces), so the browser is not always on
loopback. A key-delivery mechanism was required.

## Decision

Introduce short-lived, IP-bound, session-scoped browser tokens minted by an
unauthenticated bootstrap endpoint, with page/bootstrap carve-outs in the
fail-closed middleware. The **network boundary** (loopback / VPN / reverse
proxy) is the authentication layer; the app's key checks become defense-in-depth.

### 1. Bootstrap token endpoint

- `GET /api/v1/bootstrap-token` mints a token scoped to the `approve` role (the
  dashboard UI's approve/reject and escalation-resolve actions require
  `approve`, ADR-012) and bound to the requesting client IP.
- Tokens live in an in-memory store on the dashboard process (single process; a
  restart invalidates them and clients re-mint transparently).
- The endpoint is unauthenticated — anyone who can reach the port can mint a
  token. This is the accepted consequence of trusting the network boundary (see
  Consequences).
- `open` auth mode is unchanged: loopback-only (ADR-012), no token needed.

### 2. RBAC resolution

- Token validation plugs into the existing role resolution. `role_for_key` /
  `require_ws_role` first check the static env keys, then the session-token
  store: a valid, unexpired, IP-matching token resolves to its role.
- No change to the `require_role` interface, honoring ADR-012's stated
  extension point.

### 3. Middleware carve-out

- The fail-closed middleware exempts the page routes, static assets, and the
  bootstrap endpoint.
- Everything else — `/api/*`, `/ws/*`, `/metrics` — stays key-gated (session
  token or static role key).
- Page/static content holds no secret data; all data loads via the keyed API.

### 4. Frontend

- `app.js` fetches the bootstrap token on page load and holds it **in memory
  only** (re-fetched on each load; nothing persists across tabs or restarts).
- The token is sent as `X-API-Key` on REST calls and as `?api_key=` on the
  WebSocket handshake (replacing the never-populated `window.DASHBOARD_API_KEY`).
- On REST `401` or WebSocket close `1008` the client transparently re-mints and
  retries, covering expiry mid-session.

### 5. Configuration

- `DASHBOARD_SESSION_TTL` — token lifetime in seconds (default `3600`).
- The minted role is fixed at `approve` (charting decision Q5); no role switch.

## Consequences

- **Positive:** the production browser works on non-loopback interfaces;
  long-lived role keys never reach the browser; exposed tokens expire (default
  1h) and are bound to the client IP; the browser credential stays below
  `admin`.
- **Negative / risk:** anyone who can reach the dashboard port can mint an
  `approve`-scoped token, and the middleware no longer 401s page loads — the
  security posture now *depends* on the network boundary. This is explicit and
  accepted: operators must not expose the port without a boundary (loopback /
  VPN / authenticated reverse proxy). The rate limiter still applies to the
  bootstrap endpoint. Existing tests asserting every endpoint requires a key
  are updated to the carve-out reality.
- **Neutral:** no schema changes; single-process in-memory store; a dashboard
  restart invalidates browser tokens and clients recover by re-minting.

## Links

- ADR-012 (dashboard RBAC + loopback-only `open` mode) — the interface this
  extends; nothing superseded.
- Wayfinder ticket #63 — the grilling session whose decision this ADR records.
- Implementation ticket: #77 (Implement browser session tokens for the dashboard).
