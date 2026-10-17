"""ADR-013 browser session-token store for the dashboard.

Short-lived, IP-bound, in-memory tokens minted by the bootstrap endpoint.
A browser fetches a token (no long-lived key ever reaches the client JS)
and presents it as ``X-API-Key`` (REST) or ``?api_key=`` (WebSocket) on
subsequent requests. Tokens are bound to the minting client IP and expire
after :data:`DASHBOARD_SESSION_TTL` seconds (default 3600).

Lifetime notes
--------------
* Single-process store: a dashboard restart invalidates every token and
  clients transparently re-mint (see ``app.js``).
* Expiry is swept lazily (access) and can be purged on demand
  (:func:`purge_expired`), so stale tokens never accumulate indefinitely.
"""

from __future__ import annotations

import os
import secrets
import threading
import time
from dataclasses import dataclass
from typing import Optional

from ai_company.security.rbac import Role

__all__ = [
    "DEFAULT_TTL",
    "mint_bootstrap_token",
    "resolve_session_token",
    "revoke",
    "purge_expired",
    "clear",
    "store_size",
]


DEFAULT_TTL = 3600


def _ttl() -> int:
    """Token lifetime in seconds (``DASHBOARD_SESSION_TTL``, default 3600)."""
    raw = os.environ.get("DASHBOARD_SESSION_TTL", str(DEFAULT_TTL))
    try:
        return max(1, int(raw))
    except ValueError:
        return DEFAULT_TTL


@dataclass
class _Session:
    token: str
    role: Role
    client_ip: str
    expires_at: float


_store: dict[str, _Session] = {}
_lock = threading.Lock()


def _sweep_locked() -> int:
    now = time.time()
    dead = [t for t, s in _store.items() if s.expires_at <= now]
    for t in dead:
        _store.pop(t, None)
    return len(dead)


def purge_expired() -> int:
    """Remove expired tokens now. Returns the number evicted."""
    with _lock:
        return _sweep_locked()


def clear() -> None:
    """Drop every token (used for test isolation and shutdown)."""
    with _lock:
        _store.clear()


def store_size() -> int:
    """Live token count (for metrics/testing)."""
    with _lock:
        return len(_store)


def mint_bootstrap_token(client_ip: str) -> str:
    """Mint an ``approve``-scoped, IP-bound session token and return it."""
    token = secrets.token_urlsafe(32)
    with _lock:
        _sweep_locked()
        _store[token] = _Session(
            token=token,
            role=Role.APPROVE,
            client_ip=client_ip,
            expires_at=time.time() + _ttl(),
        )
    return token


def resolve_session_token(token: str, client_ip: str) -> Optional[Role]:
    """Resolve a session token to its role.

    Returns the role only when the token exists, has not expired, and is bound
    to *client_ip*; otherwise returns ``None``. Expired entries are evicted on
    access.
    """
    if not token:
        return None
    with _lock:
        _sweep_locked()
        session = _store.get(token)
        if session is None:
            return None
        if session.expires_at <= time.time():
            _store.pop(token, None)
            return None
        if session.client_ip != client_ip:
            return None
        return session.role


def revoke(token: str) -> bool:
    """Invalidate *token* immediately. Returns True if it existed."""
    with _lock:
        return _store.pop(token, None) is not None
