"""Injection quarantine flag (F-12 -> R6).

The trajectory store holds thousands of prompt-injection phrases
(``ignore prior`` 3,412, ``override instruction`` 2,162, ``system prompt``
2,077, ``jailbreak`` 317 …) in the same corpus the
``## Relevant Past Work`` recall loop reads from. This module provides the
**additive** quarantine control: classification of text against injection
patterns so rows can be *flagged* — never deleted — and excluded from
memory recall pending human review.

Design (from the fix plan):

- A ``quarantine`` sidecar keyed by ``(session_id, part_id)`` with
  ``reason, reviewer, reviewed_at``. Quarantined rows are **evidence**;
  rollback = clear the flag by review batch, never purge.
- The injector excludes quarantined rows via a ``NOT EXISTS`` anti-join;
  re-admission requires a named reviewer + date.
- Both columns and the tagging job mutate the live DB only in a
  maintenance window with a pre-change snapshot (fix plan §12). This
  module only *classifies* — it never writes to the store.

Patterns mirror the audit LIKE-probes, expressed as case-insensitive
regexes, loaded from ``config/quarantine_patterns.yaml`` with code
defaults as fallback.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)
_security_logger = logging.getLogger("ai_company.security.quarantine")

_DEFAULT_PATTERNS: tuple[tuple[str, str, str], ...] = (
    ("ignore_prior", r"ignore.{0,30}(prior|previous)", "Ignore-prior override"),
    ("override_instruction", r"override.{0,30}instruction", "Override-instruction"),
    ("system_prompt", r"system\s+prompt", "System-prompt reference"),
    ("jailbreak", r"jailbreak", "Jailbreak terminology"),
    (
        "disregard",
        r"disregard.{0,30}(instruction|prompt|rule|prior|previous)",
        "Disregard-instructions",
    ),
    ("ignore_all", r"ignore\s+all\b", "Ignore-all directive"),
    ("new_instructions", r"new\s+instructions?\b", "New-instructions injection"),
    ("you_are_now", r"you\s+are\s+now\s+(a|an|the)\b", "Role-swap injection"),
)


def _load_patterns(config_path: str | Path | None = None) -> list[tuple[str, re.Pattern[str], str]]:
    """Compile quarantine patterns from YAML, falling back to code defaults."""
    if config_path is None:
        candidate = Path("config/quarantine_patterns.yaml")
        if candidate.exists():
            config_path = candidate
    rules: list[tuple[str, str, str]] = [(pid, pat, desc) for pid, pat, desc in _DEFAULT_PATTERNS]
    if config_path is not None:
        try:
            with open(config_path, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
            entries = data.get("patterns", [])
            if entries:
                rules = [
                    (
                        str(e.get("id", f"pattern_{i}")),
                        str(e.get("regex", "")),
                        str(e.get("description", "")),
                    )
                    for i, e in enumerate(entries)
                    if e.get("regex")
                ]
            logger.info("Loaded quarantine patterns from %s (%d)", config_path, len(rules))
        except (yaml.YAMLError, OSError) as exc:
            logger.warning(
                "Failed to load quarantine patterns from %s: %s — using defaults",
                config_path,
                exc,
            )
    return [(pid, re.compile(pat, re.IGNORECASE), desc) for pid, pat, desc in rules]


_COMPILED = _load_patterns()

#: (id, compiled_regex, description) triples in config order.
QUARANTINE_PATTERNS: tuple[tuple[str, re.Pattern[str], str], ...] = tuple(_COMPILED)

#: All known pattern IDs (for reporting without importing config details).
QUARANTINE_PATTERN_IDS: tuple[str, ...] = tuple(pid for pid, _, _ in _COMPILED)


def classify_quarantine(text: str) -> list[str]:
    """Return the quarantine pattern IDs matching *text* (empty = clean)."""
    if not text:
        return []
    hits: list[str] = []
    for pid, pattern, _ in _COMPILED:
        if pattern.search(text):
            hits.append(pid)
    return hits


def is_quarantined(text: str) -> bool:
    """True when *text* matches any active quarantine pattern."""
    return bool(classify_quarantine(text))


def quarantine_flag(text: str) -> dict[str, object]:
    """Build the additive sidecar flag for one text/row (no DB writes).

    The caller persists ``flag`` into the ``quarantine`` sidecar table
    keyed by ``(session_id, part_id)`` during a maintenance window. An
    empty ``matched`` list means *no flag needed* — the row stays
    eligible for recall.
    """
    matched = classify_quarantine(text)
    return {
        "quarantined": 1 if matched else 0,
        "matched": matched,
        "reviewer": None,
        "reviewed_at": None,
    }


# Injector exclusion shape (documentation only — the injector itself lives
# in the executor/memory layer; this module never queries the store):
#   SELECT ... FROM part p
#   WHERE NOT EXISTS (SELECT 1 FROM quarantine q
#                     WHERE q.session_id = p.session_id
#                       AND q.part_id = p.id AND q.quarantined = 1)
