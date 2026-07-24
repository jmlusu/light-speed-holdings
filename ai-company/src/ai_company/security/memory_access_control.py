"""Memory access controls — restrict agent access to sensitive memory types."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

# Access matrix: memory_tag -> list of allowed agent IDs
DEFAULT_ACCESS_MATRIX: dict[str, list[str]] = {
    # Financial memories — only CFO, financial analysts, and CEO
    "financial": ["cfo", "financial_analyst", "human_ceo", "chief_financial_officer"],
    "budget": ["cfo", "financial_analyst", "human_ceo"],
    "revenue": ["cfo", "financial_analyst", "human_ceo", "sales_owner", "sales"],
    "expense": ["cfo", "financial_analyst", "human_ceo"],

    # HR memories — only HR lead and CEO
    "hr": ["hr_lead", "human_ceo", "chro"],
    "personnel": ["hr_lead", "human_ceo", "chro"],
    "hiring": ["hr_lead", "human_ceo", "recruiter", "chro"],
    "compensation": ["hr_lead", "human_ceo", "cfo", "chro"],

    # Security memories — only CISO and security team
    "security": ["ciso", "ai_security_specialist", "human_ceo"],
    "secrets": ["ciso", "ai_security_specialist"],
    "credentials": ["ciso", "ai_security_specialist"],
    "encryption": ["ciso", "ai_security_specialist", "security_architect"],

    # Legal memories — only legal team and CEO
    "legal": ["legal_lead", "human_ceo", "clo"],
    "compliance": ["legal_lead", "human_ceo", "compliance_officer", "clo"],
    "contract": ["legal_lead", "human_ceo", "clo"],

    # Strategic memories — only C-suite
    "strategy": ["human_ceo", "cto", "cfo", "coo", "cmo", "cso"],
    "merger": ["human_ceo", "cso", "cfo"],
    "acquisition": ["human_ceo", "cso", "cfo"],
}


class MemoryAccessControl:
    """Control which agents can access which memory types based on tags.

    The access matrix maps memory tags to lists of allowed agent IDs.
    When a memory entry has tags that appear in the access matrix, only
    agents in the allowed list can access that entry.
    Tags not in the access matrix are considered unrestricted.
    """

    def __init__(
        self,
        access_matrix: dict[str, list[str]] | None = None,
    ) -> None:
        self._access_matrix = access_matrix or DEFAULT_ACCESS_MATRIX.copy()

    @property
    def access_matrix(self) -> dict[str, list[str]]:
        return self._access_matrix

    def set_access(self, tag: str, allowed_agents: list[str]) -> None:
        """Set access control for a memory tag."""
        self._access_matrix[tag] = allowed_agents

    def remove_access(self, tag: str) -> None:
        """Remove access control for a memory tag (makes it unrestricted)."""
        self._access_matrix.pop(tag, None)

    def can_access(self, agent_id: str, memory_tags: list[str]) -> bool:
        """Check if an agent can access memory with the given tags.

        Returns True if the agent is allowed for ALL restricted tags.
        If a tag is not in the access matrix, it's unrestricted.
        """
        for tag in memory_tags:
            if tag in self._access_matrix:
                if agent_id not in self._access_matrix[tag]:
                    return False
        return True

    def filter_memories(
        self,
        agent_id: str,
        memories: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Filter a list of memory entries based on access permissions.

        Returns only entries the agent is allowed to access.
        """
        return [
            m for m in memories
            if self.can_access(agent_id, m.get("tags", []))
        ]

    def get_allowed_tags(self, agent_id: str) -> list[str]:
        """Return all memory tags this agent is allowed to access."""
        allowed = []
        for tag, agents in self._access_matrix.items():
            if agent_id in agents:
                allowed.append(tag)
        return sorted(allowed)

    def get_restricted_tags(self) -> list[str]:
        """Return all tags that have access restrictions."""
        return list(self._access_matrix.keys())


# Module-level singleton
_default_mac: MemoryAccessControl | None = None


def get_memory_access_control() -> MemoryAccessControl:
    """Return the module-level singleton."""
    global _default_mac
    if _default_mac is None:
        _default_mac = MemoryAccessControl()
    return _default_mac


def check_memory_access(agent_id: str, memory_tags: list[str]) -> bool:
    """Quick access check using the module-level singleton."""
    return get_memory_access_control().can_access(agent_id, memory_tags)


def filter_memories_by_access(
    agent_id: str,
    memories: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Quick filter using the module-level singleton."""
    return get_memory_access_control().filter_memories(agent_id, memories)