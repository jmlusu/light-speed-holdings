"""API versioning layer for the CEO dashboard.

Provides:
- ``/api/version`` discovery endpoint
- Legacy ``/api/*`` → ``/api/v1/*`` redirects (308)
- ``API-Version: v1`` header injection on versioned responses
- ``Deprecation`` and ``Sunset`` headers on legacy redirects

The versioning strategy is URL-path based: all versioned endpoints live
under ``/api/v1/*``.  Legacy paths (``/api/<endpoint>``) are redirected
with a 308 Permanent Redirect, preserving the HTTP method and query
string.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Request, Response
from starlette.responses import RedirectResponse

# ── Constants ────────────────────────────────────────────────────────

CURRENT_VERSION = "v1"
SUNSET_DATE = (datetime.now(timezone.utc) + timedelta(days=365)).strftime(
    "%a, %d %b %Y 00:00:00 GMT"
)

# Endpoints that live under /api/* but should NOT redirect to /api/v1/*.
# These are either version-info or non-versioned paths.
_EXEMPT_PREFIXES: tuple[str, ...] = ("/api/version", "/api/v1")

# ── Version info router ─────────────────────────────────────────────

version_router = APIRouter(tags=["versioning"])


@version_router.get("/api/version")
def get_version_info() -> dict[str, Any]:
    """Return API version metadata for client discovery.

    This endpoint is intentionally NOT under ``/api/v1/`` and does NOT
    receive the ``API-Version`` header.
    """
    return {
        "current_version": CURRENT_VERSION,
        "latest_version": CURRENT_VERSION,
        "deprecated_versions": [],
        "sunset_date": datetime.now(timezone.utc).isoformat(),
    }


# ── Middleware ────────────────────────────────────────────────────────


def _is_versioned_path(path: str) -> bool:
    """Return True if *path* is under ``/api/v1/``."""
    return path.startswith("/api/v1/")


def _is_legacy_api_path(path: str) -> bool:
    """Return True if *path* is a legacy ``/api/*`` that should redirect.

    Exempts ``/api/version`` and anything already under ``/api/v1/``.
    """
    if not path.startswith("/api/"):
        return False
    if path.startswith("/api/v1"):
        return False
    for exempt in _EXEMPT_PREFIXES:
        if path.startswith(exempt):
            return False
    return True


def add_version_header_middleware(app: Any) -> None:
    """Register middleware that adds ``API-Version`` to versioned responses."""

    @app.middleware("http")
    async def _version_header_middleware(request: Request, call_next: Any) -> Response:  # type: ignore[no-untyped-def]
        response = await call_next(request)
        if _is_versioned_path(request.url.path):
            response.headers["API-Version"] = CURRENT_VERSION
        return response


def add_legacy_redirect_middleware(app: Any) -> None:
    """Register middleware that redirects ``/api/*`` → ``/api/v1/*``.

    Returns a 308 Permanent Redirect with deprecation headers. Query
    strings and POST bodies are preserved (308 keeps the method).
    """

    @app.middleware("http")
    async def _legacy_redirect_middleware(request: Request, call_next: Any) -> Response:  # type: ignore[no-untyped-def]
        path = request.url.path
        if _is_legacy_api_path(path):
            # Build the new path: /api/<x> → /api/v1/<x>
            new_path = "/api/v1" + path[len("/api"):]
            # Preserve query string
            qs = request.url.query
            if qs:
                new_path = f"{new_path}?{qs}"
            return RedirectResponse(
                url=new_path,
                status_code=308,
                headers={
                    "Deprecation": "true",
                    "Sunset": SUNSET_DATE,
                    "API-Version": CURRENT_VERSION,
                },
            )
        return await call_next(request)
