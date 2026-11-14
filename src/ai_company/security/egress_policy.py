"""Backwards-compat shim: ``egress_policy`` -> canonical :mod:`ai_company.security.egress`.

Canonical implementation lives in :mod:`ai_company.security.egress`
(CISO security/, F-07/P2-T6). This module keeps legacy
``security.egress_policy`` import paths working and prevents a second
egress module from appearing (D-1 dedup).
"""

from __future__ import annotations

from ai_company.security.egress import (
    check_shell_egress,
    result_to_register_entry,
    validate_egress_url,
)

__all__ = [
    "check_shell_egress",
    "result_to_register_entry",
    "validate_egress_url",
]
