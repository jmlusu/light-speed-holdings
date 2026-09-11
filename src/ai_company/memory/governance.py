"""Memory knowledge governance — policies for capture, retention, staleness,
conflict resolution, and curator pinning.

Implements the rules decided in ticket #229 (Knowledge Quality Governance).
The system keeps *fully automatic* capture (no human review gate): the
engine may veto content that violates the constitutional screen, warn on
probable noise, retire stale/contradicted entries, and honor explicit pins
from a curator.

Policy is expressed as data-first objects so defaults can be overridden from
config without changing code.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

# Minimum content length (chars) to count as knowledge rather than noise.
MIN_KNOWLEDGE_LENGTH = 40

# Retention TTL (days) per memory type. Semantic/procedural knowledge is
# long-lived by design: it is retired by contradiction or supersession, not
# by clock. Episodic task records are short-lived because they are digested
# into knowledge by consolidation.
DEFAULT_RETENTION_TTL_DAYS: dict[str, int] = {
    "episodic": 90,
    "semantic": 3650,
    "procedural": 3650,
    "relational": 730,
    "temporal": 365,
    "aggregate": 10950,
}

# Default staleness window (days): a memory not recalled in this long is
# flagged for review/supersession.
DEFAULT_STALENESS_DAYS = 180

# Constitutional screen — content matching these never enters memory.
# Expressed as lower-cased substrings; deliberately small, explicit, and
# human-reviewable. Aligns with ai_development_constitution/.
CONSTITUTIONAL_BLOCKLIST: list[str] = [
    "bypass safety",
    "ignore safety",
    "exfiltrate",
    "prompt injection: achieve",
    "extract secrets from",
]

# Probable noise markers — content carrying these (from auto-extraction
# heuristics) is captured but flagged; it still qualifies as knowledge.
NOISE_MARKERS: list[str] = [
    "unknown error",
    "no output",
    "command not found",
]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _parsed_days(entry: Any) -> float:
    """Return entry age in days, treating broken timestamps as 0."""
    try:
        created = datetime.fromisoformat(str(entry.created_at))
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        return (_utcnow() - created).total_seconds() / 86400.0
    except (ValueError, TypeError):
        return 0.0


@dataclass
class MemoryGovernance:
    """Configuration + policy predicates for the memory store.

    The store calls these at capture/retention time. Defaults match the
    ticket #229 decision; override fields to customise per deployment.
    """

    retention_ttl_days: dict[str, int] = field(
        default_factory=lambda: dict(DEFAULT_RETENTION_TTL_DAYS)
    )
    staleness_days: int = DEFAULT_STALENESS_DAYS
    constitutional_blocklist: list[str] = field(
        default_factory=lambda: list(CONSTITUTIONAL_BLOCKLIST)
    )
    noise_markers: list[str] = field(default_factory=lambda: list(NOISE_MARKERS))
    min_knowledge_length: int = MIN_KNOWLEDGE_LENGTH

    # -- Capture ----------------------------------------------------------

    def is_constitutionally_blocked(self, content: str) -> bool:
        """True if content violates the constitutional screen (hard veto)."""
        lowered = content.lower()
        return any(pattern in lowered for pattern in self.constitutional_blocklist)

    def is_probable_noise(self, content: str) -> bool:
        """True if content looks like extraction noise (soft warning)."""
        lowered = content.lower()
        return any(marker in lowered for marker in self.noise_markers)

    def is_knowledge_worthy(self, content: str) -> bool:
        """True if content is long/structured enough to count as knowledge."""
        text = " ".join(content.split())
        return len(text) >= self.min_knowledge_length

    def capture_decision(self, content: str, memory_type: str) -> dict[str, Any]:
        """Return a capture decision for ``content``.

        Returns a dict with ``allowed`` (bool), ``reason`` (str), and
        ``flagged`` (bool, noise warning only). A hard veto on constitutional
        violations; otherwise capture always proceeds (automatic capture).
        """
        if self.is_constitutionally_blocked(content):
            return {"allowed": False, "reason": "constitutional_block", "flagged": False}
        return {
            "allowed": True,
            "reason": "capture",
            "flagged": self.is_probable_noise(content) or not self.is_knowledge_worthy(content),
        }

    # -- Retention / staleness --------------------------------------------

    def ttl_days_for(self, memory_type: str) -> int:
        return self.retention_ttl_days.get(memory_type, 365)

    def is_expired(self, entry: Any, memory_type: str) -> bool:
        """True if the entry exceeds its type's TTL."""
        return _parsed_days(entry) > self.ttl_days_for(memory_type)

    def is_stale(self, entry: Any) -> bool:
        """True if the entry has not been recalled within the staleness window."""
        if getattr(entry, "access_count", 0) > 0:
            return False
        return _parsed_days(entry) >= self.staleness_days

    def mark_stale_flag(self, entry: Any) -> None:
        """Tag an entry as stale for review (idempotent)."""
        entry.metadata.setdefault("status", "stale")

    # -- Conflict resolution ----------------------------------------------

    def resolve_conflict(self, existing: Any, new: Any) -> dict[str, str]:
        """Decide between an existing entry and a newer, contradicting one.

        ``new`` wins by default (newest statement of fact); the loser is
        marked ``superseded`` in metadata and excluded from recall ranking.
        """
        if existing.metadata.get("status") == "pinned":
            return {"winner": "existing", "loser_status": "active"}
        return {"winner": "new", "loser_status": "superseded"}

    def mark_superseded(self, entry: Any) -> None:
        entry.metadata["status"] = "superseded"

    # -- Pinning (curator override, NOT a human review gate) --------------

    @staticmethod
    def is_pinned(entry: Any) -> bool:
        return entry.metadata.get("status") == "pinned" or entry.metadata.get("pinned") is True


GOOD_PATTERN = re.compile(r"\b(completed|fixed|resolved|solved|verified)\b")


def screen_capture(
    governance: MemoryGovernance | None,
    content: str,
    memory_type: str,
) -> dict[str, Any]:
    """Module-level capture screen usable from integration code.

    Falls back to the default governance when none is supplied.
    """
    gov = governance or MemoryGovernance()
    return gov.capture_decision(content, memory_type)
