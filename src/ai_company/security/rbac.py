"""Role-based access control (RBAC) for dashboard endpoints.

Permission model
----------------

Every dashboard request carries an ``X-API-Key`` header. In ``api_key``
auth mode the key maps to a role via the environment:

    DASHBOARD_ADMIN_KEY    -> ``admin``   (all permissions)
    DASHBOARD_APPROVE_KEY  -> ``approve`` (approvals + escalations)
    DASHBOARD_RUN_KEY      -> ``run``     (task mutations)

The legacy single-key ``DASHBOARD_API_KEY`` is accepted as the admin key
for backward compatibility.

Roles are hierarchical: ``admin`` implies ``approve`` implies ``run``.
A dependency produced by :func:`require_role` rejects requests whose role
sits below the minimum required (403).

In ``open`` auth mode every request is treated as ``admin``. That mode is
only permitted on loopback bindings; see ``app.py``/``cli/dashboard.py``
(ADR-012).
"""

from __future__ import annotations

import os
from enum import Enum
from typing import Any, Callable

from fastapi import Header, HTTPException, Request, status

__all__ = ["Role", "role_for_key", "require_role", "require_ws_role", "client_ip_for"]


class Role(str, Enum):
    """Granular dashboard roles, ordered from least to most privileged."""

    RUN = "run"
    APPROVE = "approve"
    ADMIN = "admin"


_RANK = {
    Role.RUN: 0,
    Role.APPROVE: 1,
    Role.ADMIN: 2,
}


def _configured_keys() -> dict[Role, str]:
    """Return the mapping role -> API key from the environment.

    ``DASHBOARD_API_KEY`` remains a valid alias for the admin key so
    existing single-key deployments keep working unchanged.
    """
    admin_key = os.environ.get("DASHBOARD_ADMIN_KEY", "") or os.environ.get("DASHBOARD_API_KEY", "")
    return {
        Role.RUN: os.environ.get("DASHBOARD_RUN_KEY", ""),
        Role.APPROVE: os.environ.get("DASHBOARD_APPROVE_KEY", ""),
        Role.ADMIN: admin_key,
    }


def role_for_key(api_key: str) -> Role | None:
    """Map an API key to its role, or ``None`` when the key is unknown."""
    if not api_key:
        return None
    for role, expected in _configured_keys().items():
        if expected and api_key == expected:
            return role
    return None


def client_ip_for(request_or_websocket: Any) -> str:
    """Extract the peer IP from a FastAPI ``Request`` or ``WebSocket``.

    Used to bind session tokens to the client that minted them (ADR-013).
    Returns ``""`` when the peer address is unknown (e.g. some test harnesses).
    """
    client = getattr(request_or_websocket, "client", None)
    return client.host if client else ""


def _resolve_role(x_api_key: str | None, client_ip: str = "") -> Role:
    """Authenticate the request and return its role.

    ``open`` auth mode short-circuits to ``admin`` (explicit opt-in for
    localhost dev, enforced to be loopback-only by the server/CLI).

    Role resolution order (ADR-012 / ADR-013):
    1. Static env keys (``DASHBOARD_*_KEY``) — backward compatible.
    2. A bootstrap session token (IP-bound, TTL) resolving to ``approve``.
    """
    if os.environ.get("DASHBOARD_AUTH_MODE", "api_key") == "open":
        return Role.ADMIN
    role = role_for_key(x_api_key or "")
    if role is None:
        # ADR-013: a browser session token resolves to its minted role.
        from ai_company.dashboard.sessions import resolve_session_token

        role = resolve_session_token(x_api_key or "", client_ip)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return role


def require_role(minimum: str | Role) -> Callable[..., Role]:
    """Build a FastAPI dependency that requires at least ``minimum`` role.

    Example::

        @router.post("/tasks")
        def create_task(
            ...,
            _: Role = Depends(require_role("run")),
        ) -> TaskItem: ...
    """
    min_role = Role(minimum)

    def dependency(
        x_api_key: str | None = Header(default=None, alias="X-API-Key"),
        request: Request | None = None,
    ) -> Role:
        role = _resolve_role(x_api_key, client_ip_for(request))
        if _RANK[role] < _RANK[min_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Insufficient permissions: requires role '{min_role.value}' "
                    f"(got '{role.value}')"
                ),
            )
        return role

    return dependency


def require_ws_role(minimum: str | Role, api_key: str | None, client_ip: str = "") -> Role:
    """Resolve the role for a WebSocket handshake supplied via query param.

    Browsers cannot set custom headers on a WebSocket handshake, so the
    ``X-API-Key``-based :func:`require_role` cannot be used directly; the key
    is instead carried as ``?api_key=``.  ``open`` auth mode short-circuits
    to ``admin`` exactly like :func:`require_role` (loopback-only, ADR-012).

    Raises ``HTTPException`` (401 unknown/missing key, 403 below *minimum*);
    WebSocket callers should translate that into a close (e.g. code 1008).
    """
    min_role = Role(minimum)
    role = _resolve_role(api_key, client_ip)
    if _RANK[role] < _RANK[min_role]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"Insufficient permissions: requires role '{min_role.value}' (got '{role.value}')"
            ),
        )
    return role
