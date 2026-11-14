"""Backwards-compat shim: ``redaction`` -> canonical :mod:`ai_company.security.redact`.

Canonical implementation lives in :mod:`ai_company.security.redact`
(CISO security/, F-05/P0-T5). This module exists so legacy
``lsmem.redaction``/``security.redaction`` import paths keep working and
future code does not create a competing redaction module (D-1 dedup).
"""

from __future__ import annotations

from ai_company.security.redact import (
    REDACTED,
    contains_secret_pattern,
    redact_part_data,
    redact_secrets,
)

__all__ = [
    "REDACTED",
    "contains_secret_pattern",
    "redact_part_data",
    "redact_secrets",
]
