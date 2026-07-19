"""FastAPI application for the CEO dashboard.

Security hardening (GAP-010):
- CORS origins are configurable via ``DASHBOARD_CORS_ORIGINS`` env var
  (comma-separated; defaults to ``http://localhost:3000``).
- Write endpoints (POST / DELETE) require an ``X-API-Key`` header when
  ``DASHBOARD_API_KEY`` env var is set.
- Simple in-memory rate limiter protects all endpoints (100 req/min default,
  configurable via ``DASHBOARD_RATE_LIMIT``).
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

from ai_company.dashboard.api import router
from ai_company.dashboard.ws import router as ws_router

logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).resolve().parents[3] / "static"

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


def create_app() -> FastAPI:
    app = FastAPI(title="Light Speed Holdings — CEO Dashboard", version="0.1.0")

    # ── CORS (GAP-010: configurable origins) ─────────────────────────
    origins_raw = os.environ.get("DASHBOARD_CORS_ORIGINS", "http://localhost:3000")
    origins = [o.strip() for o in origins_raw.split(",") if o.strip()]
    # If the operator explicitly sets "*," keep the legacy wide-open behaviour
    # for backward compatibility in development.
    allow_wildcard = "*" in origins

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if allow_wildcard else origins,
        allow_credentials=not allow_wildcard,
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

    # ── Health check (before static mount so it isn't shadowed) ─────

    @app.get("/health", tags=["ops"])
    def health_check() -> dict[str, str]:
        return {"status": "ok", "service": "ceo-dashboard"}

    # ── Static files (catch-all, must be last) ──────────────────────
    if STATIC_DIR.is_dir():
        app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

    return app


app = create_app()
