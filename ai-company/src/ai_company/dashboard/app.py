"""FastAPI application for the CEO dashboard.

Security hardening (GAP-010):
- CORS origins are configurable via ``DASHBOARD_CORS_ORIGINS`` env var
  (comma-separated; defaults to a localhost-only allowlist). The wildcard
  ``*`` is rejected and never used as a default.
- Write endpoints (POST / DELETE) require an ``X-API-Key`` header when
  ``DASHBOARD_API_KEY`` env var is set.
- Simple in-memory rate limiter protects all endpoints (100 req/min default,
  configurable via ``DASHBOARD_RATE_LIMIT``).

Frontend:
- Jinja2 templates served from ``src/ai_company/dashboard/templates/``
- Static assets (CSS, JS) served from ``src/ai_company/dashboard/static/``
- Page routes render templates with tab navigation context
"""

from __future__ import annotations

import logging
import os
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ai_company.logging_config import setup_logging

# Configure structured logging on import
setup_logging()

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
# Legacy static dir (backward compat)
LEGACY_STATIC_DIR = Path(__file__).resolve().parents[3] / "static"

# ---------------------------------------------------------------------------
# Rate limiter (simple in-memory, sliding window per IP)
# ---------------------------------------------------------------------------

class _RateLimiter:
    """Per-IP sliding-window rate limiter.  No external dependencies."""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        cutoff = now - self.window_seconds
        # Prune old entries
        self._hits[key] = [t for t in self._hits[key] if t > cutoff]
        if len(self._hits[key]) >= self.max_requests:
            return False
        self._hits[key].append(now)
        return True


# ---------------------------------------------------------------------------
# API key helper
# ---------------------------------------------------------------------------


def _get_api_key() -> str:
    """Read the API key from the environment (never cached)."""
    return os.environ.get("DASHBOARD_API_KEY", "")


def _check_api_key(request: Request) -> bool:
    """Return True if the request is authorised.

    * If ``DASHBOARD_API_KEY`` is not set → all requests pass (open mode).
    * For safe methods (GET, HEAD, OPTIONS) → always pass.
    * For mutating methods → require ``X-API-Key`` header matching the secret.
    """
    api_key = _get_api_key()
    if not api_key:
        return True
    if request.method in ("GET", "HEAD", "OPTIONS"):
        return True
    return request.headers.get("X-API-Key") == api_key


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
    ]
    return {"tabs": tabs, "active_tab": active_tab}


def create_app() -> FastAPI:
    app = FastAPI(title="Light Speed Holdings — CEO Dashboard", version="0.2.0")

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
        logger.warning(
            "DASHBOARD_CORS_ORIGINS contained '*'; ignoring wildcard for security."
        )
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

    @app.middleware("http")
    async def _rate_limit_middleware(request: Request, call_next: Any) -> Response:  # type: ignore[no-untyped-def]
        client_ip = request.client.host if request.client else "unknown"
        if not _limiter.is_allowed(client_ip):
            return Response(
                content='{"detail":"Rate limit exceeded"}',
                status_code=429,
                media_type="application/json",
            )
        return await call_next(request)

    # ── API-key guard for write endpoints (GAP-010) ──────────────────────
    @app.middleware("http")
    async def _api_key_middleware(request: Request, call_next: Any) -> Response:  # type: ignore[no-untyped-def]
        if not _check_api_key(request):
            return Response(
                content='{"detail":"Invalid or missing API key"}',
                status_code=401,
                media_type="application/json",
            )
        return await call_next(request)

    # ── Routers ─────────────────────────────────────────────────────
    app.include_router(router)
    app.include_router(ws_router)
    if _has_mobile:
        app.include_router(mobile_router)  # /api/mobile/*
    if _has_monitoring:
        app.include_router(monitoring_router)  # /metrics, /health, /ready

    # ── Health check ───────────────────────────────────────────────
    @app.get("/health", tags=["ops"])
    def health_check() -> dict[str, str]:
        return {"status": "ok", "service": "ceo-dashboard"}

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
