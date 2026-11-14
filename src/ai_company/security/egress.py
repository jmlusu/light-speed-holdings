"""Egress URL policy for webfetch/shell egress (F-07 / P2-T6, GO-8 support).

Rules (evaluated in code, not in the prompt):
1. Scheme must be ``https`` — exception: ``http`` allowed only for
   loopback / already-observed dev ranges (``localhost``,
   ``127.0.0.1``, ``172.30.96.x``).
2. URLs containing userinfo (``user:pass@host``) are rejected.
3. Query strings with token-like parameter *names* are rejected
   (values are never logged).
4. Cloud-metadata / private-IP / non-http targets are denied.
5. Schemes ``file:``, ``data:``, ``ftp:`` are denied.

Host *names* and parameter *names* may be logged; URLs and payload
values must never be persisted. The transmission register (host + tool +
payload class) is produced by callers using :func:`result_to_register_entry`.

TOCTOU note: the private-IP check here is a string/denylist check at
admission time. DNS-rebinding defence (resolve once, pin the IP,
re-validate every redirect hop) belongs to the fetcher itself and is
documented as a residual risk in the P0 runbook.
"""

from __future__ import annotations

import ipaddress
import logging
import re
from pathlib import Path
from urllib.parse import urlparse

import yaml

logger = logging.getLogger(__name__)
_security_logger = logging.getLogger("ai_company.security.egress")

# Parameter names that look like tokens; matched case-insensitively.
_TOKEN_PARAM_NAMES = frozenset({"key", "token", "secret", "api_key", "apikey", "auth", "session"})

# Explicitly denied hosts (cloud metadata).
_DENIED_HOSTS = frozenset({"169.254.169.254", "169.254.169.253", "metadata.google.internal"})

# Suspended under AGENTS.md §9.2 (absent from docs/APPROVED-VENDORS.md,
# verified 2026-11-08). Flagged — never deleted silently; see
# config/suspended_vendors.yaml. Lifting requires a signed
# docs/APPROVED-VENDORS.md row (forward fix, not a rollback).
_SUSPENDED_HOSTS: frozenset[str] = frozenset({"resend.com", "mcp.resend.com"})

# Loopback / dev ranges where plain http is tolerated.
_HTTP_ALLOWED_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})
_HTTP_ALLOWED_SUBNETS: list[ipaddress.IPv4Network | ipaddress.IPv6Network] = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("172.30.96.0/24"),
]

_ALLOWED_SCHEMES = frozenset({"http", "https"})
_DENIED_SCHEMES = frozenset({"file", "data", "ftp"})


def _load_policy_extras() -> tuple[set[str], set[str]]:
    """Load additive extras from config/egress_allowlist.yaml.

    Returns ``(extra_http_hosts, extra_suspended_hosts)``; code defaults
    always remain in effect (config is additive — same convention as
    ``config/tool_allowlist.yaml``).
    """
    candidate = Path("config/egress_allowlist.yaml")
    if not candidate.exists():
        return set(), set()
    try:
        with open(candidate, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except (yaml.YAMLError, OSError) as exc:
        logger.warning("Failed to load egress config %s: %s — code defaults only", candidate, exc)
        return set(), set()
    extra_http = {str(h).lower() for h in data.get("dev_http_hosts", []) or []}
    extra_suspended = {str(h).lower() for h in data.get("blocked_hosts", []) or []}
    return extra_http, extra_suspended


_EXTRA_HTTP_HOSTS, _EXTRA_SUSPENDED_HOSTS = _load_policy_extras()
if _EXTRA_HTTP_HOSTS:
    _HTTP_ALLOWED_HOSTS = frozenset(set(_HTTP_ALLOWED_HOSTS) | _EXTRA_HTTP_HOSTS)
if _EXTRA_SUSPENDED_HOSTS:
    _SUSPENDED_HOSTS = frozenset(set(_SUSPENDED_HOSTS) | _EXTRA_SUSPENDED_HOSTS)

_EGRESS_VERB_RE = re.compile(
    r"\b(invoke-webrequest|invoke-restmethod|invoke-expression|curl|wget|iwr|irm)\b",
    re.IGNORECASE,
)
_URL_RE = re.compile(r"https?://[^\s\"'\)\]<>]+", re.IGNORECASE)


def check_shell_egress(command: str) -> tuple[bool, str]:
    """Validate shell egress in *command* (IWR/IRM/curl/wget …).

    Every URL in the command is validated with :func:`validate_egress_url`;
    any failure denies the command. An egress verb with no verifiable URL
    is denied as unverifiable egress. Commands without egress verbs are
    allowed (``no_egress``) — path policy still applies separately.
    Returns ``(allowed, reason)`` in the same shape as the URL validator.
    """
    if not isinstance(command, str) or not command.strip():
        return True, "no_egress"
    if not _EGRESS_VERB_RE.search(command):
        return True, "no_egress"
    urls = _URL_RE.findall(command)
    if not urls:
        _security_logger.warning("Shell egress denied (no verifiable URL): %.120s", command)
        return False, "egress_unverifiable"
    for raw_url in urls:
        allowed, reason = validate_egress_url(raw_url)
        if not allowed:
            _security_logger.warning(
                "Shell egress denied (%s) for URL host %s",
                reason,
                (urlparse(raw_url).hostname or ""),
            )
            return False, reason
    return True, "allowed"


def _is_http_allowed_host(host: str) -> bool:
    if host in _HTTP_ALLOWED_HOSTS:
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return any(ip in net for net in _HTTP_ALLOWED_SUBNETS)


def _is_private_or_link_local(host: str) -> bool:
    if host in _DENIED_HOSTS:
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return bool(
        ip.is_private or ip.is_link_local or ip.is_reserved or ip.is_multicast or ip.is_unspecified
    )


def validate_egress_url(url: str) -> tuple[bool, str]:
    """Validate *url* against egress policy.

    Returns ``(allowed, reason)``; ``reason`` is a short machine token
    (e.g. ``"userinfo_url"``) suitable for audit logging without values.
    """
    if not isinstance(url, str) or not url:
        return False, "empty_url"
    parsed = urlparse(url)
    scheme = (parsed.scheme or "").lower()
    if scheme in _DENIED_SCHEMES:
        return False, f"denied_scheme:{scheme}"
    if scheme not in _ALLOWED_SCHEMES:
        return False, f"unsupported_scheme:{scheme}"
    if parsed.username or parsed.password:
        return False, "userinfo_url"
    host = (parsed.hostname or "").lower()
    if not host:
        return False, "missing_host"
    if host in _DENIED_HOSTS:
        return False, "denied_metadata_host"
    if host in _SUSPENDED_HOSTS or any(
        host.endswith("." + h) for h in _SUSPENDED_HOSTS if "." in h
    ):
        return False, "suspended_vendor_host"
    if scheme != "https" and not _is_http_allowed_host(host):
        return False, "third_party_http"
    if _is_private_or_link_local(host) and host not in _HTTP_ALLOWED_HOSTS:
        return False, "private_ip_egress"
    # Query-string token names (names only, never values).
    if parsed.query:
        from urllib.parse import parse_qsl

        for name, _value in parse_qsl(parsed.query, keep_blank_values=True):
            if name.lower() in _TOKEN_PARAM_NAMES:
                _security_logger.info(
                    "Egress query token param name: %s (host logged separately)", name
                )
                return False, f"query_token_param:{name.lower()}"
    return True, "allowed"


def result_to_register_entry(tool: str, url: str, allowed: bool, reason: str) -> dict[str, str]:
    """Build a transmission-register entry (host + tool + class, no values)."""
    host = ""
    try:
        host = (urlparse(url).hostname or "") if isinstance(url, str) else ""
    except ValueError:
        host = ""
    return {
        "tool": tool,
        "host": host.lower(),
        "allowed": "yes" if allowed else "no",
        "reason": reason,
    }
