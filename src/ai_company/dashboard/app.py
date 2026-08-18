"""FastAPI application for the CEO dashboard.

Security hardening (GAP-010):
- CORS origins are configurable via ``DASHBOARD_CORS_ORIGINS`` env var
  (comma-separated; defaults to a localhost-only allowlist). The wildcard
  ``*`` is rejected and never used as a default.
- Auth is fail-closed by default (``DASHBOARD_AUTH_MODE`` defaults to
  ``api_key``): write endpoints (POST / PUT / PATCH / DELETE) require an
  ``X-API-Key`` header matching ``DASHBOARD_API_KEY``, and are rejected when
  no key is configured. Set ``DASHBOARD_AUTH_MODE=open`` only for
  localhost-only development.
- Simple in-memory rate limiter protects all endpoints (100 req/min default,
  configurable via ``DASHBOARD_RATE_LIMIT``).
- Response security headers (T018 / ticket #11): CSP, HSTS,
  X-Content-Type-Options, X-Frame-Options, Referrer-Policy,
  Permissions-Policy are applied to every response via middleware.
  ``security_headers()`` returns the default policy set.

Frontend:
- Jinja2 templates served from ``src/ai_company/dashboard/templates/``
- Static assets (CSS, JS) served from ``src/ai_company/dashboard/static/``
- Page routes render templates with tab navigation context
"""

from __future__ import annotations

import ipaddress
import logging
import os
import time
from collections import defaultdict
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, cast

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ai_company.logging_config import setup_logging
from ai_company.paths import get_data_root, get_project_root
from ai_company.version import get_version

load_dotenv()

# Configure structured logging on import
setup_logging()
logger = logging.getLogger(__name__)


def security_headers() -> dict[str, str]:
    """Return the hardened response-security headers for the dashboard.

    T018 (ticket #11): CSP, HSTS, and clickjacking/type-confusion guards.

    The default CSP is pragmatic for the current CDN-based frontend
    (Tailwind + Alpine + Chart.js from ``cdn.tailwindcss.com`` and
    ``cdn.jsdelivr.net``, plus the inline ``tailwind.config`` script in
    ``base.html``).  It still blocks objects, frames, form-targeting and
    base-URI attacks, and restricts connect/font/img to first-party or
    data: sources.  ``'unsafe-eval'`` is required by Alpine.js v3, which
    compiles ``x-data``/``x-text`` expressions with ``new Function()``;
    without it the dashboard's dynamic KPIs, tasks table, and WebSocket
    indicator never render.  Tighten it by setting ``DASHBOARD_CSP``.

    HSTS max-age is configurable via ``DASHBOARD_HSTS_MAX_AGE``
    (default 31536000 = 1 year; set ``0`` to disable).
    """
    csp = os.environ.get(
        "DASHBOARD_CSP",
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com "
        "https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "img-src 'self' data:; font-src 'self' data:; "
        "connect-src 'self' ws: wss:; frame-ancestors 'none'; "
        "base-uri 'self'; form-action 'self'; object-src 'none'",
    )
    hsts_max_age = int(os.environ.get("DASHBOARD_HSTS_MAX_AGE", "31536000"))
    headers = {
        "Content-Security-Policy": csp,
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }
    if hsts_max_age > 0:
        headers["Strict-Transport-Security"] = f"max-age={hsts_max_age}; includeSubDomains"
    return headers


from ai_company.dashboard.api import router  # noqa: E402
from ai_company.dashboard.ws import router as ws_router  # noqa: E402

try:
    from ai_company.dashboard.mobile_api import router as mobile_router  # noqa: E402

    _has_mobile = True
except ImportError:
    _has_mobile = False

try:
    from ai_company.dashboard.monitoring import router as monitoring_router  # noqa: E402

    _has_monitoring = True
except ImportError:
    _has_monitoring = False

logger = logging.getLogger(__name__)

# ── Directory paths ──────────────────────────────────────────
DASHBOARD_PKG = Path(__file__).resolve().parent
TEMPLATES_DIR = DASHBOARD_PKG / "templates"
DASHBOARD_STATIC_DIR = DASHBOARD_PKG / "static"
# Legacy static dir (backward compat) — anchored to the project root rather
# than a fixed ``parents[3]`` so it resolves correctly from any CWD.
LEGACY_STATIC_DIR = get_project_root() / "static"

# ---------------------------------------------------------------------------
# Rate limiter (simple in-memory, sliding window per IP)
# ---------------------------------------------------------------------------


class _RateLimiter:
    """Per-IP sliding-window rate limiter.  No external dependencies."""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, key: str) -> tuple[bool, int]:
        """Return ``(allowed, remaining)`` for the given *key*.

        *remaining* is the number of requests the client may still make
        within the current window (0 when the limit is reached).
        """
        now = time.time()
        cutoff = now - self.window_seconds
        # Prune old entries
        self._hits[key] = [t for t in self._hits[key] if t > cutoff]
        if len(self._hits[key]) >= self.max_requests:
            return False, 0
        self._hits[key].append(now)
        remaining = self.max_requests - len(self._hits[key])
        return True, remaining


# ---------------------------------------------------------------------------
# API key helper
# ---------------------------------------------------------------------------


def _check_api_key(request: Request) -> bool:
    """Return True if the request is authorised.

    Auth is controlled by ``DASHBOARD_AUTH_MODE``:

    * ``api_key`` (default, fail-closed): **ALL** methods require an
      ``X-API-Key`` header matching any configured role key
      (``DASHBOARD_ADMIN_KEY`` / ``DASHBOARD_APPROVE_KEY`` /
      ``DASHBOARD_RUN_KEY``; ``DASHBOARD_API_KEY`` remains a valid admin
      alias). If no key is configured the request is rejected (fail-closed),
      so a misconfigured network deployment never silently exposes any
      endpoints. Role-key checks are enforced per-endpoint by
      :func:`~ai_company.security.rbac.require_role`.

    * ``open`` (explicit opt-in for localhost-only dev): all requests
      pass regardless of configuration. The server refuses to bind open
      mode to a non-loopback interface (see ``create_app`` / CLI).

    ADR-013: when the header does not match a static env key, the value is
    checked against the in-memory session-token store (browser bootstrap
    tokens).  Page routes, static assets, and the bootstrap endpoint are
    exempt from the API-key guard (middleware carve-out).
    """
    if os.environ.get("DASHBOARD_AUTH_MODE", "api_key") == "open":
        return True
    api_key = request.headers.get("X-API-Key", "")
    if not api_key:
        return False
    from ai_company.security.rbac import role_for_key

    if role_for_key(api_key) is not None:
        return True
    # ADR-013: fall back to session token (IP-bound)
    client_ip = request.client.host if request.client else "unknown"
    from ai_company.security.rbac import _resolve_session_token

    return _resolve_session_token(api_key, client_ip) is not None


# Paths that are exempt from the API-key guard (ADR-013 middleware carve-out).
_PAGE_PREFIXES = (
    "/",
    "/agents",
    "/tasks",
    "/kpis",
    "/costs",
    "/escalations",
    "/command-center",
    "/mission-control",
    "/onboarding",
    "/finance",
    "/org-chart",
)


def _is_exempt_from_auth(path: str) -> bool:
    """Return True for paths that bypass the API-key middleware (ADR-013)."""
    if path == "/api/v1/bootstrap-token":
        return True
    if path.startswith("/static") or path.startswith("/legacy"):
        return True
    if path == "/docs" or path == "/redoc" or path == "/openapi.json":
        return True
    return any(path == prefix or path.startswith(prefix + "/") for prefix in _PAGE_PREFIXES)


def is_loopback_host(host: str) -> bool:
    """Return True when ``host`` resolves to a loopback interface.

    Accepts ``localhost`` plus any literal loopback address (127.0.0.0/8,
    ``::1``). Used to enforce the ADR-012 rule that ``DASHBOARD_AUTH_MODE=open``
    may only bind to a loopback interface.
    """
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return host.lower() in {"localhost", "localhost.localdomain"}


def _tab_context(active_tab: str) -> dict[str, Any]:
    """Build the template context for tab navigation."""
    tabs = [
        {
            "id": "dashboard",
            "label": "Dashboard",
            "href": "/",
            "icon": '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>',
        },
        {
            "id": "agents",
            "label": "Agents",
            "href": "/agents",
            "icon": '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>',
        },
        {
            "id": "tasks",
            "label": "Tasks",
            "href": "/tasks",
            "icon": '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>',
        },
        {
            "id": "kpis",
            "label": "KPIs",
            "href": "/kpis",
            "icon": '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>',
        },
        {
            "id": "costs",
            "label": "Costs",
            "href": "/costs",
            "icon": '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
        },
        {
            "id": "escalations",
            "label": "Approvals",
            "href": "/escalations",
            "icon": '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>',
        },
        {
            "id": "command-center",
            "label": "Command Center",
            "href": "/command-center",
            "icon": '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>',
        },
        {
            "id": "mission-control",
            "label": "Mission Control",
            "href": "/mission-control",
            "icon": '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>',
        },
        {
            "id": "onboarding",
            "label": "Onboarding",
            "href": "/onboarding",
            "icon": '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/></svg>',
        },
        {
            "id": "finance",
            "label": "Finance",
            "href": "/finance",
            "icon": '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
        },
        {
            "id": "org-chart",
            "label": "Org Chart",
            "href": "/org-chart",
            "icon": '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>',
        },
    ]
    return {"tabs": tabs, "active_tab": active_tab}


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Lifespan handler for FastAPI dashboard app."""
    try:
        from ai_company.dashboard.repository import get_state_store  # noqa: E402
        from ai_company.data import init_database  # noqa: E402

        db_path = Path(get_state_store().base_dir) / "data" / "ai_company.db"
        db = init_database(db_path)
        logger.info("SQLite database initialised: %s", db.path)
    except Exception:  # noqa: BLE001 - non-critical startup hook
        logger.debug("Database initialisation skipped (non-critical)")
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=_lifespan,
        title="Light Speed Holdings — CEO Dashboard",
        description=(
            "REST API for the AI Company Builder CEO Dashboard.\n\n"
            "Provides endpoints for monitoring agents, managing tasks, "
            "approvals, escalations, KPIs, cost tracking, and mobile access."
        ),
        version=get_version(),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_tags=[
            {"name": "dashboard", "description": "Main dashboard overview and CEO aggregate view"},
            {
                "name": "agents",
                "description": "Agent listing, detail, org chart, and performance metrics",
            },
            {"name": "tasks", "description": "Task listing and creation via the MessageBus"},
            {
                "name": "approvals",
                "description": "Human-in-the-loop approval requests and decisions",
            },
            {"name": "escalations", "description": "Escalation events and resolution"},
            {
                "name": "kpis",
                "description": "Key Performance Indicators: live, summary, history, trends, and alerts",
            },
            {"name": "costs", "description": "Budget and LLM cost tracking across agents"},
            {
                "name": "models",
                "description": "Model routing tiers and per-agent model assignments",
            },
            {"name": "scheduler", "description": "Scheduled and recurring task listings"},
            {
                "name": "departments",
                "description": "Department listing and per-department dashboards",
            },
            {
                "name": "monitoring",
                "description": "Prometheus-compatible metrics and deep health checks",
            },
            {
                "name": "mobile",
                "description": "Mobile-optimized endpoints with compact payloads and batch actions",
            },
            {
                "name": "ops",
                "description": "Operational endpoints: health checks, readiness probes",
            },
        ],
    )

    # ── Auth-mode loopback restriction (ADR-012) ────────────────────────
    # ``open`` auth mode bypasses the API-key guard entirely, so it must
    # never bind to a non-loopback interface. The CLI validates its own
    # ``--host`` argument; this check additionally fails fast for direct
    # ``uvicorn`` launches where the bind host is supplied via
    # ``DASHBOARD_HOST``.
    if os.environ.get("DASHBOARD_AUTH_MODE", "api_key") == "open":
        bind_host = os.environ.get("DASHBOARD_HOST", "").strip()
        if bind_host and not is_loopback_host(bind_host):
            raise RuntimeError(
                "DASHBOARD_AUTH_MODE=open is only allowed on loopback hosts "
                f"(127.0.0.1 / ::1); DASHBOARD_HOST='{bind_host}'"
            )

    # ── Jinja2 templates ─────────────────────────────────────────────
    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

    # ── CORS (GAP-010: configurable, restricted allowlist) ───────────
    # Default to localhost-only origins; never default to "*".
    # Override via DASHBOARD_CORS_ORIGINS (comma-separated). The wildcard
    # "*" is explicitly rejected: it is incompatible with allow_credentials
    # and is a production risk.
    _DEFAULT_ORIGINS = [
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
    ]
    origins_raw = os.environ.get("DASHBOARD_CORS_ORIGINS", "")
    origins = [o.strip() for o in origins_raw.split(",") if o.strip()]
    if not origins:
        origins = _DEFAULT_ORIGINS
    # Guard against accidental wildcard that would expose the API.
    if "*" in origins:
        logger.warning("DASHBOARD_CORS_ORIGINS contained '*'; ignoring wildcard for security.")
        origins = [o for o in origins if o != "*"]
    if not origins:
        origins = _DEFAULT_ORIGINS

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Rate limiter middleware (GAP-010) ────────────────────────────────
    rate_limit = int(os.environ.get("DASHBOARD_RATE_LIMIT", "100"))
    _limiter = _RateLimiter(max_requests=rate_limit)
    app.state.limiter = _limiter  # exposed for test isolation (conftest resets between tests)

    @app.middleware("http")
    async def _rate_limit_middleware(request: Request, call_next: Any) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        allowed, remaining = _limiter.is_allowed(client_ip)
        if not allowed:
            return Response(
                content='{"detail":"Rate limit exceeded"}',
                status_code=429,
                media_type="application/json",
                headers={
                    "X-RateLimit-Limit": str(rate_limit),
                    "X-RateLimit-Remaining": "0",
                },
            )
        response = cast(Response, await call_next(request))
        response.headers["X-RateLimit-Limit"] = str(rate_limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response

    # ── API-key guard for write endpoints (GAP-010) ──────────────────────
    # ADR-013: page routes, static assets, and the bootstrap endpoint are
    # exempt from the API-key guard (middleware carve-out).
    @app.middleware("http")
    async def _api_key_middleware(request: Request, call_next: Any) -> Response:
        if _is_exempt_from_auth(request.url.path):
            return cast(Response, await call_next(request))
        if not _check_api_key(request):
            return Response(
                content='{"detail":"Invalid or missing API key"}',
                status_code=401,
                media_type="application/json",
            )
        return cast(Response, await call_next(request))

    # ── Security headers (T018 / ticket #11) ─────────────────────────────
    # Registered AFTER the auth + rate-limit middlewares so it runs
    # outermost: every response — including 401/429 short-circuits —
    # carries the hardened headers.  CSP/HSTS are env-configurable.
    app.state.allowed_ws_origins = set(origins)

    @app.middleware("http")
    async def _security_headers_middleware(request: Request, call_next: Any) -> Response:
        response = cast(Response, await call_next(request))
        for name, value in security_headers().items():
            response.headers[name] = value
        return response

    # ── Explicit StateStore configuration (Option B) ────────────────
    # Bind the dashboard state root from configuration rather than the
    # import-time cwd. Defaults to the deterministic project root; override
    # via DASHBOARD_DATA_DIR.
    from ai_company.dashboard.repository import (  # noqa: E402
        configure_state_store,
    )

    dashboard_data_dir = os.environ.get("DASHBOARD_DATA_DIR") or str(get_data_root())
    configure_state_store(dashboard_data_dir)

    # ── Routers ─────────────────────────────────────────────────────
    app.include_router(router)
    app.include_router(ws_router)
    if _has_mobile:
        app.include_router(mobile_router)  # /api/v1/mobile/*
    if _has_monitoring:
        app.include_router(monitoring_router)  # /metrics, /health, /ready

    # ── ADR-013: Bootstrap token endpoint ──────────────────────────
    # Unauthenticated: anyone who can reach the port can mint a token.
    # The network boundary (loopback / VPN / reverse proxy) is the auth.
    from ai_company.dashboard.sessions import mint_bootstrap_token

    @app.get("/api/v1/bootstrap-token")
    async def bootstrap_token(request: Request) -> dict[str, str]:
        client_ip = request.client.host if request.client else "unknown"
        token = mint_bootstrap_token(client_ip)
        return {"token": token}

    # ── Page routes (Jinja2 templates) ─────────────────────────────
    # These MUST be registered BEFORE the static file mounts.

    @app.get("/", response_class=Response)
    async def page_index(request: Request) -> Response:
        ctx = _tab_context("dashboard")
        return templates.TemplateResponse(request, "index.html", ctx)

    @app.get("/agents", response_class=Response)
    async def page_agents(request: Request) -> Response:
        ctx = _tab_context("agents")
        return templates.TemplateResponse(request, "agents.html", ctx)

    @app.get("/tasks", response_class=Response)
    async def page_tasks(request: Request) -> Response:
        ctx = _tab_context("tasks")
        return templates.TemplateResponse(request, "tasks.html", ctx)

    @app.get("/kpis", response_class=Response)
    async def page_kpis(request: Request) -> Response:
        ctx = _tab_context("kpis")
        return templates.TemplateResponse(request, "kpis.html", ctx)

    @app.get("/costs", response_class=Response)
    async def page_costs(request: Request) -> Response:
        ctx = _tab_context("costs")
        return templates.TemplateResponse(request, "costs.html", ctx)

    @app.get("/escalations", response_class=Response)
    async def page_escalations(request: Request) -> Response:
        ctx = _tab_context("escalations")
        return templates.TemplateResponse(request, "escalations.html", ctx)

    @app.get("/command-center", response_class=Response)
    async def page_command_center(request: Request) -> Response:
        ctx = _tab_context("command-center")
        return templates.TemplateResponse(request, "command-center.html", ctx)

    @app.get("/command-center-v2", response_class=Response)
    async def page_command_center_v2(request: Request) -> Response:
        ctx = _tab_context("command-center")
        return templates.TemplateResponse(request, "command-center-v2.html", ctx)

    @app.get("/mission-control", response_class=Response)
    async def page_mission_control(request: Request) -> Response:
        ctx = _tab_context("mission-control")
        return templates.TemplateResponse(request, "mission-control.html", ctx)

    @app.get("/finance", response_class=Response)
    async def page_finance(request: Request) -> Response:
        ctx = _tab_context("finance")
        return templates.TemplateResponse(request, "finance.html", ctx)

    @app.get("/onboarding", response_class=Response)
    async def page_onboarding(request: Request) -> Response:
        ctx = _tab_context("onboarding")
        return templates.TemplateResponse(request, "onboarding.html", ctx)

    @app.get("/org-chart", response_class=Response)
    async def page_org_chart(request: Request) -> Response:
        ctx = _tab_context("org-chart")
        return templates.TemplateResponse(request, "org-chart.html", ctx)

    # ── Static files ───────────────────────────────────────────────
    # Dashboard static assets (CSS, JS, images)
    if DASHBOARD_STATIC_DIR.is_dir():
        app.mount(
            "/static",
            StaticFiles(directory=str(DASHBOARD_STATIC_DIR)),
            name="dashboard-static",
        )

    # Legacy static dir (backward compat — serves old SPA if present)
    if LEGACY_STATIC_DIR.is_dir():
        app.mount(
            "/legacy",
            StaticFiles(directory=str(LEGACY_STATIC_DIR), html=True),
            name="legacy-static",
        )

    return app


app = create_app()
