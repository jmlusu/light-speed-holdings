"""Agent behavior monitoring — detect anomalous patterns in agent actions."""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

# Default anomaly thresholds (per hour)
DEFAULT_THRESHOLDS: dict[str, int] = {
    "tool_calls_per_hour": 100,
    "memory_access_per_hour": 50,
    "delegation_attempts_per_hour": 20,
    "failed_tool_calls_per_hour": 10,
    "unique_files_accessed_per_hour": 30,
    "llm_calls_per_hour": 50,
    "total_tokens_per_hour": 500000,
}

# Maximum delegation depth before an anomaly is flagged.
MAX_DELEGATION_DEPTH = 5


@dataclass
class AgentAction:
    """Record of a single agent action."""
    agent_id: str
    action_type: str
    timestamp: float = field(default_factory=time.time)
    details: dict[str, Any] = field(default_factory=dict)
    success: bool = True


@dataclass
class AnomalyReport:
    """Report of detected anomalous behavior."""
    agent_id: str
    action_type: str
    count: int
    threshold: int
    window_start: float
    window_end: float
    severity: str  # "warning" or "critical"
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "action_type": self.action_type,
            "count": self.count,
            "threshold": self.threshold,
            "window_start": self.window_start,
            "window_end": self.window_end,
            "severity": self.severity,
            "description": self.description,
        }


class AgentBehaviorMonitor:
    """Monitor agent behavior for anomalies.

    Tracks action counts per agent per hour and compares against
    configurable thresholds. When a threshold is exceeded, an
    anomaly report is generated.
    """

    def __init__(
        self,
        thresholds: dict[str, int] | None = None,
        window_seconds: int = 3600,  # 1 hour
    ) -> None:
        self._thresholds = thresholds or DEFAULT_THRESHOLDS.copy()
        self._window_seconds = window_seconds
        self._max_actions_per_agent: int = 200
        # Action history: agent_id -> action_type -> list of timestamps
        self._history: dict[str, dict[str, list[float]]] = defaultdict(
            lambda: defaultdict(list)
        )
        # All recorded actions for auditing
        self._actions: list[AgentAction] = []

    @property
    def thresholds(self) -> dict[str, int]:
        return self._thresholds

    def set_threshold(self, action_type: str, max_count: int) -> None:
        """Set the threshold for an action type."""
        self._thresholds[action_type] = max_count

    def record_action(
        self,
        agent_id: str,
        action_type: str,
        details: dict[str, Any] | None = None,
        success: bool = True,
    ) -> AgentAction:
        """Record an agent action for monitoring.

        Returns the created :class:`AgentAction`.
        """
        now = time.time()
        action = AgentAction(
            agent_id=agent_id,
            action_type=action_type,
            timestamp=now,
            details=details or {},
            success=success,
        )
        self._actions.append(action)
        self._history[agent_id][action_type].append(now)

        # Prune old entries outside the window
        cutoff = now - self._window_seconds
        self._history[agent_id][action_type] = [
            t for t in self._history[agent_id][action_type]
            if t > cutoff
        ]

        # Enforce per-agent action limit (rotation)
        agent_actions = [
            a for a in self._actions if a.agent_id == agent_id
        ]
        if len(agent_actions) > self._max_actions_per_agent:
            # Remove oldest actions beyond the limit
            excess = len(agent_actions) - self._max_actions_per_agent
            ids_to_remove = {id(a) for a in agent_actions[:excess]}
            self._actions = [
                a for a in self._actions if id(a) not in ids_to_remove
            ]

        return action

    def check_anomaly(
        self,
        agent_id: str,
        action_type: str,
    ) -> AnomalyReport | None:
        """Check if a specific agent/action exceeds its threshold.

        Returns an AnomalyReport if threshold exceeded, None otherwise.
        """
        now = time.time()
        cutoff = now - self._window_seconds

        timestamps = [
            t for t in self._history[agent_id][action_type]
            if t > cutoff
        ]
        count = len(timestamps)
        threshold = self._thresholds.get(action_type, 100)

        if count > threshold:
            severity = "critical" if count > threshold * 2 else "warning"
            return AnomalyReport(
                agent_id=agent_id,
                action_type=action_type,
                count=count,
                threshold=threshold,
                window_start=cutoff,
                window_end=now,
                severity=severity,
                description=f"{count} {action_type} (threshold {threshold})",
            )
        return None

    def _check_failure_rate(self, agent_id: str) -> AnomalyReport | None:
        """Check if the agent's task failure rate is anomalous."""
        now = time.time()
        cutoff = now - self._window_seconds

        failures = sum(
            1 for a in self._actions
            if a.agent_id == agent_id
            and a.action_type == "task_completed"
            and not a.success
            and a.timestamp > cutoff
        )
        successes = sum(
            1 for a in self._actions
            if a.agent_id == agent_id
            and a.action_type == "task_completed"
            and a.success
            and a.timestamp > cutoff
        )
        total = failures + successes
        if total < 2:
            return None

        rate = failures / total
        if rate >= 0.8:
            return AnomalyReport(
                agent_id=agent_id,
                action_type="high_failure_rate",
                count=failures,
                threshold=total,
                window_start=cutoff,
                window_end=now,
                severity="critical",
                description=f"{failures} failures out of {total} ({rate:.0%})",
            )
        elif rate >= 0.5:
            return AnomalyReport(
                agent_id=agent_id,
                action_type="high_failure_rate",
                count=failures,
                threshold=total,
                window_start=cutoff,
                window_end=now,
                severity="warning",
                description=f"{failures} failures out of {total} ({rate:.0%})",
            )
        return None

    def _check_delegation_depth(self, agent_id: str) -> AnomalyReport | None:
        """Check if the agent has excessive delegations (depth > MAX)."""
        now = time.time()
        cutoff = now - self._window_seconds

        delegation_count = sum(
            1 for a in self._actions
            if a.agent_id == agent_id
            and a.action_type == "delegation"
            and a.timestamp > cutoff
        )
        if delegation_count > MAX_DELEGATION_DEPTH:
            return AnomalyReport(
                agent_id=agent_id,
                action_type="excessive_delegation",
                count=delegation_count,
                threshold=MAX_DELEGATION_DEPTH,
                window_start=cutoff,
                window_end=now,
                severity="warning",
                description=f"{delegation_count} delegations (max depth {MAX_DELEGATION_DEPTH})",
            )
        return None

    def check_anomalies(
        self,
        agent_id: str | None = None,
    ) -> list[AnomalyReport]:
        """Check all tracked agents/actions for anomalies.

        If agent_id is provided, only check that agent.
        Otherwise check all agents.
        """
        anomalies: list[AnomalyReport] = []

        agents = [agent_id] if agent_id else list(self._history.keys())

        for aid in agents:
            # Rate-based checks per action type
            for action_type in self._history[aid]:
                report = self.check_anomaly(aid, action_type)
                if report:
                    anomalies.append(report)
                    logger.warning(
                        "Agent behavior anomaly: %s %s count=%d threshold=%d",
                        aid, action_type, report.count, report.threshold,
                    )

            # Failure-rate check
            failure_report = self._check_failure_rate(aid)
            if failure_report:
                anomalies.append(failure_report)

            # Delegation depth check
            delegation_report = self._check_delegation_depth(aid)
            if delegation_report:
                anomalies.append(delegation_report)

        return anomalies

    def get_agent_summary(self, agent_id: str) -> dict[str, Any]:
        """Get action summary for an agent within the current window."""
        now = time.time()
        cutoff = now - self._window_seconds

        # Per action-type counts
        actions_summary: dict[str, int] = {}
        for action_type, timestamps in self._history.get(agent_id, {}).items():
            count = sum(1 for t in timestamps if t > cutoff)
            if count > 0:
                actions_summary[action_type] = count

        # Success / failure counts from full action log
        total_successes = sum(
            1 for a in self._actions
            if a.agent_id == agent_id and a.success
        )
        total_failures = sum(
            1 for a in self._actions
            if a.agent_id == agent_id and not a.success
        )
        total_completed = total_successes + total_failures
        failure_rate = (
            total_failures / total_completed if total_completed > 0 else 0.0
        )

        # Convenience type-specific counts
        tool_calls = actions_summary.get("tool_call", 0)
        llm_calls = actions_summary.get("llm_call", 0)
        delegations = actions_summary.get("delegation", 0)

        return {
            "agent_id": agent_id,
            "window_seconds": self._window_seconds,
            "actions": actions_summary,
            "total_actions": sum(actions_summary.values()),
            "total_successes": total_successes,
            "total_failures": total_failures,
            "failure_rate": failure_rate,
            "tool_calls": tool_calls,
            "llm_calls": llm_calls,
            "delegations": delegations,
        }

    def get_all_summaries(self) -> dict[str, dict[str, Any]]:
        """Get summaries for all tracked agents."""
        return {
            agent_id: self.get_agent_summary(agent_id)
            for agent_id in self._history
        }

    def get_recent_actions(
        self,
        agent_id: str | None = None,
        action_type: str | None = None,
        limit: int = 100,
    ) -> list[AgentAction]:
        """Get recent actions with optional filtering.

        Returns the most recent *limit* actions in chronological order
        (oldest first within the limit window).
        """
        actions = self._actions

        if agent_id:
            actions = [a for a in actions if a.agent_id == agent_id]
        if action_type:
            actions = [a for a in actions if a.action_type == action_type]

        return sorted(actions, key=lambda a: a.timestamp)[-limit:]

    def reset(self) -> None:
        """Clear all monitoring data."""
        self._history.clear()
        self._actions.clear()


# Module-level singleton
_default_monitor: AgentBehaviorMonitor | None = None


def get_agent_monitor() -> AgentBehaviorMonitor:
    """Return the module-level singleton."""
    global _default_monitor
    if _default_monitor is None:
        _default_monitor = AgentBehaviorMonitor()
    return _default_monitor


def reset_agent_monitor() -> None:
    """Reset the module-level singleton (used by tests)."""
    global _default_monitor
    _default_monitor = None


def record_agent_action(
    agent_id: str,
    action_type: str,
    details: dict[str, Any] | None = None,
    success: bool = True,
) -> None:
    """Quick action recording using the module-level singleton."""
    get_agent_monitor().record_action(agent_id, action_type, details, success)


def check_agent_anomalies(agent_id: str | None = None) -> list[AnomalyReport]:
    """Quick anomaly check using the module-level singleton."""
    return get_agent_monitor().check_anomalies(agent_id)
