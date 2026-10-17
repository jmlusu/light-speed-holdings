"""Reliability primitives for the hardening layer.

Timeouts, bulkheads, circuit breakers, and the shared hardening config
(``company/config/hardening.yaml``). See ``docs/HARDENING-PATTERN-CATALOG.md``
for the pattern contracts these implement (wayfinder map #167).
"""

from ai_company.reliability.breaker import ComponentBreaker
from ai_company.reliability.config import get_hardening_value, load_hardening_config
from ai_company.reliability.timeout import Bulkhead, call_with_timeout

__all__ = [
    "Bulkhead",
    "ComponentBreaker",
    "call_with_timeout",
    "get_hardening_value",
    "load_hardening_config",
]
