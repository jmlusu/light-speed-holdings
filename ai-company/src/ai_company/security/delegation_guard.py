"""Delegation depth limits and cycle detection for agent delegation."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

# Configuration constants
MAX_DELEGATION_DEPTH = 3
MAX_CONCURRENT_DELEGATIONS = 5
MAX_TOTAL_DELEGATIONS = 20


class DelegationGuard:
    """Enforce delegation depth limits and detect cycles.

    Tracks delegation chains per task to prevent:
    1. Infinite loops (A→B→C→A)
    2. Excessive depth (A→B→C→D→E)
    3. Resource exhaustion from too many concurrent delegations
    """

    def __init__(
        self,
        max_depth: int = MAX_DELEGATION_DEPTH,
        max_concurrent: int = MAX_CONCURRENT_DELEGATIONS,
        max_total: int = MAX_TOTAL_DELEGATIONS,
    ) -> None:
        self._max_depth = max_depth
        self._max_concurrent = max_concurrent
        self._max_total = max_total
        # Per-task delegation history: task_id -> list of delegated agent IDs
        self._task_chains: dict[str, list[str]] = {}
        # Per-task delegation count: task_id -> count
        self._task_counts: dict[str, int] = {}

    @property
    def max_depth(self) -> int:
        return self._max_depth

    def check_delegation(
        self,
        task_id: str,
        receiver: str,
        delegation_depth: int = 0,
        delegation_history: list[str] | None = None,
    ) -> tuple[bool, str]:
        """Check if a delegation is allowed.

        Args:
            task_id: The parent task ID.
            receiver: The agent ID being delegated to.
            delegation_depth: Current depth in the delegation chain.
            delegation_history: List of agent IDs already in the chain.

        Returns:
            (is_allowed, reason) tuple.
        """
        # Check depth limit
        if delegation_depth >= self._max_depth:
            reason = (
                f"Delegation depth {delegation_depth} exceeds maximum "
                f"({self._max_depth}). Task {task_id} chain: {delegation_history or []}"
            )
            logger.warning("Delegation blocked (depth): %s", reason)
            return False, reason

        # Check cycle detection
        if delegation_history and receiver in delegation_history:
            reason = (
                f"Delegation cycle detected: '{receiver}' already in chain. "
                f"Task {task_id} chain: {delegation_history}"
            )
            logger.warning("Delegation blocked (cycle): %s", reason)
            return False, reason

        # Check total delegation count for this task
        current_count = self._task_counts.get(task_id, 0)
        if current_count >= self._max_total:
            reason = (
                f"Total delegations ({current_count}) for task {task_id} "
                f"exceeds maximum ({self._max_total})"
            )
            logger.warning("Delegation blocked (count): %s", reason)
            return False, reason

        return True, ""

    def record_delegation(
        self,
        task_id: str,
        receiver: str,
    ) -> None:
        """Record a delegation for tracking purposes."""
        if task_id not in self._task_chains:
            self._task_chains[task_id] = []
        self._task_chains[task_id].append(receiver)
        self._task_counts[task_id] = self._task_counts.get(task_id, 0) + 1

    def get_chain(self, task_id: str) -> list[str]:
        """Return the delegation chain for a task."""
        return self._task_chains.get(task_id, [])

    def get_depth(self, task_id: str) -> int:
        """Return the current delegation depth for a task."""
        return len(self._task_chains.get(task_id, []))

    def reset(self, task_id: str) -> None:
        """Clear delegation tracking for a task (on completion/failure)."""
        self._task_chains.pop(task_id, None)
        self._task_counts.pop(task_id, None)


# Module-level singleton
_default_guard: DelegationGuard | None = None


def get_delegation_guard() -> DelegationGuard:
    """Return the module-level singleton."""
    global _default_guard
    if _default_guard is None:
        _default_guard = DelegationGuard()
    return _default_guard


def check_delegation_allowed(
    task_id: str,
    receiver: str,
    delegation_depth: int = 0,
    delegation_history: list[str] | None = None,
) -> tuple[bool, str]:
    """Quick delegation check using the module-level singleton."""
    return get_delegation_guard().check_delegation(
        task_id, receiver, delegation_depth, delegation_history
    )