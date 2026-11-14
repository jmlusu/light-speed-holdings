"""Pre-persistence secret redaction for tool outputs (security F-05 / P0-T5).

Applies value-level redaction to text *before* it is persisted into the
trajectory store (``part.data`` / ``message.data``). This complements
:class:`PIIDetector` (which masks PII with partial visibility) with
full ``[REDACTED]`` replacement for credential-shaped values.

Design constraints (from the 2026-11-08 security plan):
- Pattern IDs are logged, never values, so a false-positive review can
  re-admit benign mentions without re-exposing real keys.
- Key names are preserved for debuggability: ``API_KEY=sk-...`` becomes
  ``API_KEY=[REDACTED]``.
- Historical rows are never rewritten by this filter; it only governs
  new writes. Historical exposure is retired by rotation (F-04) and
  retention purge (F-10).

Test values in the unit tests are synthetic; no real keys appear here.
"""

from __future__ import annotations

import json
import logging
import re

logger = logging.getLogger(__name__)
_security_logger = logging.getLogger("ai_company.security.redact")

REDACTED = "[REDACTED]"


def redact_part_data(data: str) -> tuple[str, list[str], bool]:
    """Redact one ``part.data`` / ``message.data`` value pre-persistence.

    JSON-carrying values are parsed, string nodes redacted recursively,
    re-serialized, and the result is re-parsed to prove the replacement
    did not break validity (parse-then-serialize, not blind regex-on-JSON).
    Non-JSON text goes through :func:`redact_secrets`. Returns
    ``(text, pattern_ids_hit, json_valid)`` — an empty/missing JSON
    payload falls back to regex-only (``json_valid=False``). Historical
    rows are never rewritten by this filter; new writes only.
    """
    if not data:
        return data, [], False
    candidate = data.lstrip()
    if candidate.startswith(("{", "[")):
        try:
            parsed = json.loads(data)
        except (json.JSONDecodeError, ValueError):
            redacted, hits = redact_secrets(data)
            return redacted, hits, False

        def _node(node: object, hits: list[str]) -> object:
            if isinstance(node, str):
                redacted_str, node_hits = redact_secrets(node)
                for h in node_hits:
                    if h not in hits:
                        hits.append(h)
                return redacted_str
            if isinstance(node, dict):
                return {k: _node(v, hits) for k, v in node.items()}
            if isinstance(node, list):
                return [_node(v, hits) for v in node]
            return node

        json_hits: list[str] = []
        redacted_obj = _node(parsed, json_hits)
        serialized = json.dumps(redacted_obj, ensure_ascii=False)
        try:
            json.loads(serialized)
            valid = True
        except (json.JSONDecodeError, ValueError):
            valid = False
        return serialized, json_hits, valid
    redacted, hits = redact_secrets(data)
    return redacted, hits, False


# Ordered (pattern_id, compiled_regex, preserve_group) rules.
# preserve_group is the capture group whose text is kept (e.g. the key
# name ``API_KEY=``) so the value alone is replaced.
_RULES: list[tuple[str, re.Pattern[str], int | None]] = [
    # PEM blocks first (they span many lines and contain look-alike lines).
    (
        "pem_private_key",
        re.compile(
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?"
            r"-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
        ),
        None,
    ),
    ("openai_sk", re.compile(r"sk-[A-Za-z0-9_-]{8,}"), None),
    ("sk_ant", re.compile(r"sk-ant-[A-Za-z0-9_-]{8,}"), None),
    ("google_api_key", re.compile(r"AIza[A-Za-z0-9_-]{30,}"), None),
    ("aws_access_key_id", re.compile(r"AKIA[A-Z0-9]{16}"), None),
    ("github_token", re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}"), None),
    ("slack_token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), None),
    ("bearer_token", re.compile(r"(Bearer\s+)\S{10,}"), 1),
    ("api_key_assign", re.compile(r"(?i)((?:api[_-]?key|apikey)\s*[:=]\s*)\S+"), 1),
    ("secret_assign", re.compile(r"(?i)((?:secret|password|passwd|pwd)\s*[:=]\s*)\S+"), 1),
    ("dsn_assign", re.compile(r"(?i)((?:dsn|connectionstring)\s*[:=]\s*)\S+"), 1),
]


def _apply_rule(text: str, pattern: re.Pattern[str], preserve: int | None) -> tuple[str, int]:
    """Apply one redaction rule; return (new_text, replacement_count)."""
    count = 0

    def _repl(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        if preserve is not None:
            return f"{match.group(preserve)}{REDACTED}"
        return REDACTED

    return pattern.sub(_repl, text), count


def redact_secrets(text: str) -> tuple[str, list[str]]:
    """Redact credential-shaped values from *text*.

    Returns ``(redacted_text, pattern_ids_hit)`` where ``pattern_ids_hit``
    lists the rule ids that fired (for audit logging; values are never
    returned). Empty input is returned unchanged.
    """
    if not text:
        return text, []
    redacted = text
    hits: list[str] = []
    for pattern_id, pattern, preserve in _RULES:
        redacted, n = _apply_rule(redacted, pattern, preserve)
        if n:
            hits.append(pattern_id)
    if hits:
        _security_logger.info(
            "Redacted %d secret pattern(s) pre-persistence: %s",
            len(hits),
            ",".join(hits),
        )
    return redacted, hits


def contains_secret_pattern(text: str) -> list[str]:
    """Return the ids of secret patterns present in *text* (no redaction)."""
    if not text:
        return []
    return [pattern_id for pattern_id, pattern, _ in _RULES if pattern.search(text)]
