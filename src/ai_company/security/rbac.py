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

Browser session tokens (ADR-013):
    When an ``X-API-Key`` does not match a static env key, the value is
    checked against the in-memory session-token store
    (:func:`~ai_company.dashboard.sessions.resolve_session_token`). A
    valid, unexpired, IP-bound token resolves to its minted role.
"""

from __future__ import annotations

import os
from enum import Enum
from typing import Callable

from fastapi import Header, HTTPException, Request, status

__all__ = [
    "Role",
    "role_for_key",
    "authenticate",
    "require_role",
    "require_ws_role",
    "verify_keys",
]


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
    """Map an API key to its role, or ``None`` when the key is unknown.

    Checks static env keys only. For session-token resolution (ADR-013),
    use :func:`_resolve_role` which chains env keys then session tokens.
    """
    if not api_key:
        return None
    for role, expected in _configured_keys().items():
        if expected and api_key == expected:
            return role
    return None


def _resolve_session_token(token: str, client_ip: str) -> Role | None:
    """Resolve a browser session token to its role (ADR-013).

    Returns the role when the token is valid, unexpired, and bound to
    *client_ip*; ``None`` otherwise.  Imports lazily to avoid a circular
    dependency at module level.
    """
    if not token:
        return None
    try:
        from ai_company.dashboard.sessions import resolve_session_token

        return resolve_session_token(token, client_ip)
    except ImportError:
        return None


def authenticate(x_api_key: str | None, client_ip: str = "unknown") -> Role | None:
    """Resolve a request's role without raising.

    ``open`` auth mode short-circuits to ``admin`` (explicit opt-in for
    localhost dev, enforced to be loopback-only by the server/CLI).

    Resolution order (ADR-013):
    1. Static env keys (``DASHBOARD_*_KEY``)
    2. In-memory session token (browser bootstrap token, IP-bound)

    Returns the resolved role, or ``None`` when the key/token is unknown.
    This is the single authentication primitive for the dashboard: the
    middleware guard (:func:`ai_company.dashboard.app._check_api_key`) and
    the dependency-injection path (:func:`_resolve_role`) both delegate so
    the env-mode check, key lookup, and fallback order live in one place.
    """
    if os.environ.get("DASHBOARD_AUTH_MODE", "api_key") == "open":
        return Role.ADMIN
    api_key = x_api_key or ""
    role = role_for_key(api_key)
    if role is None:
        role = _resolve_session_token(api_key, client_ip)
    return role


def _resolve_role(x_api_key: str | None, client_ip: str = "unknown") -> Role:
    """Authenticate the request and return its role.

    ``open`` auth mode short-circuits to ``admin`` (explicit opt-in for
    localhost dev, enforced to be loopback-only by the server/CLI).

    Resolution order (ADR-013):
    1. Static env keys (``DASHBOARD_*_KEY``)
    2. In-memory session token (browser bootstrap token, IP-bound)

    Raises ``HTTPException`` (401) when the request cannot be authenticated.
    """
    role = authenticate(x_api_key, client_ip)
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
        request: Request,
        x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    ) -> Role:
        client_ip = request.client.host if request.client else "unknown"
        role = _resolve_role(x_api_key, client_ip)
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


def require_ws_role(minimum: str | Role, api_key: str | None, client_ip: str = "unknown") -> Role:
    """Resolve the role for a WebSocket handshake supplied via query param.

    Browsers cannot set custom headers on a WebSocket handshake, so the
    ``X-API-Key``-based :func:`require_role` cannot be used directly; the key
    is instead carried as ``?api_key=``.  ``open`` auth mode short-circuits
    to ``admin`` exactly like :func:`require_role` (loopback-only, ADR-012).

    ADR-013: session tokens are also accepted (IP-bound, minted by the
    bootstrap endpoint).

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


def verify_keys() -> None:
    """Verify that all required dashboard RBAC keys are set and non-placeholder.

    Checks that DASHBOARD_ADMIN_KEY (or DASHBOARD_API_KEY), DASHBOARD_APPROVE_KEY,
    and DASHBOARD_RUN_KEY are configured with real values, not placeholders.

    Raises:
        RuntimeError: If any key is missing or still has a placeholder value.
    """
    import os

    placeholder_values = {
        "your_dashboard_api_key_here",
        "your_run_key_here",
        "your_approve_key_here",
        "your_admin_key_here",
    }

    required_keys = {
        "DASHBOARD_ADMIN_KEY": os.environ.get("DASHBOARD_ADMIN_KEY", ""),
        "DASHBOARD_APPROVE_KEY": os.environ.get("DASHBOARD_APPROVE_KEY", ""),
        "DASHBOARD_RUN_KEY": os.environ.get("DASHBOARD_RUN_KEY", ""),
    }

    # DASHBOARD_API_KEY is an alias for DASHBOARD_ADMIN_KEY
    dashboard_api_key = os.environ.get("DASHBOARD_API_KEY", "")
    if dashboard_api_key and not required_keys["DASHBOARD_ADMIN_KEY"]:
        required_keys["DASHBOARD_ADMIN_KEY"] = dashboard_api_key

    errors = []
    for key_name, value in required_keys.items():
        if not value:
            errors.append(f"{key_name} is not set")
        elif value in placeholder_values:
            errors.append(f"{key_name} still has placeholder value")

    if errors:
        raise RuntimeError("Dashboard RBAC verification failed:\n  " + "\n  ".join(errors))

    print("Dashboard RBAC keys verified: all set with non-placeholder values")
