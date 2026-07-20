"""Agent performance analytics — completion rates, execution times, error rates.

Combines data from tasks, audit events, and cost records to provide
a comprehensive view of agent performance.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from ai_company.data.database import Database

logger = logging.getLogger(__name__)


class AgentPerformanceAnalytics:
    """Agent performance analytics backed by SQLite.

    Aggregates data from the tasks, audit_events, and cost_records
    tables to produce per-agent performance metrics.

    Args:
        database: An initialised :class:`Database` instance.
    """

    def __init__(self, database: Database) -> None:
        self._db = database

    # ── Per-agent metrics ─────────────────────────────────────────────

    def agent_summary(self, agent_id: str, days: int = 30) -> dict[str, Any]:
        """Full performance summary for a single agent."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        # Task metrics (sent + received)
        tasks_sent = self._db.fetchall(
            """SELECT status, COUNT(*) as cnt
               FROM tasks
               WHERE sender_id = ? AND created_at >= ?
               GROUP BY status""",
            (agent_id, cutoff),
        )
        tasks_received = self._db.fetchall(
            """SELECT status, COUNT(*) as cnt
               FROM tasks
               WHERE (receiver_id = ? OR assignee = ?) AND created_at >= ?
               GROUP BY status""",
            (agent_id, agent_id, cutoff),
        )

        sent_counts = {r["status"]: r["cnt"] for r in tasks_sent}
        recv_counts = {r["status"]: r["cnt"] for r in tasks_received}

        total_sent = sum(sent_counts.values())
        total_recv = sum(recv_counts.values())
        completed_recv = recv_counts.get("completed", 0)
        failed_recv = recv_counts.get("failed", 0)
        total_finished = completed_recv + failed_recv

        completion_rate = (
            round(completed_recv / total_finished * 100, 2) if total_finished > 0 else 0
        )
        error_rate = (
            round(failed_recv / total_finished * 100, 2) if total_finished > 0 else 0
        )

        # Audit event metrics
        audit_counts = self._db.fetchall(
            """SELECT event_type, COUNT(*) as cnt
               FROM audit_events
               WHERE agent_id = ? AND timestamp >= ?
               GROUP BY event_type""",
            (agent_id, cutoff),
        )
        event_counts = {r["event_type"]: r["cnt"] for r in audit_counts}

        # Tool usage
        tool_counts = self._db.fetchall(
            """SELECT tool, COUNT(*) as cnt
               FROM audit_events
               WHERE agent_id = ? AND timestamp >= ? AND tool IS NOT NULL AND tool != ''
               GROUP BY tool
               ORDER BY cnt DESC""",
            (agent_id, cutoff),
        )

        # Cost metrics
        cost_data = self._db.fetchone(
            """SELECT
                COALESCE(SUM(cost_usd), 0) as total_cost,
                COALESCE(SUM(prompt_tokens), 0) as total_prompt,
                COALESCE(SUM(completion_tokens), 0) as total_completion,
                COUNT(*) as call_count
               FROM cost_records
               WHERE agent_name = ? AND timestamp >= ?""",
            (agent_id, cutoff),
        )

        # Error events from audit
        error_events = self._db.fetchone(
            """SELECT COUNT(*) as cnt
               FROM audit_events
               WHERE agent_id = ? AND timestamp >= ?
               AND (event_type = 'error' OR severity IN ('error', 'critical'))""",
            (agent_id, cutoff),
        )

        return {
            "agent_id": agent_id,
            "period_days": days,
            "tasks_sent": total_sent,
            "tasks_received": total_recv,
            "tasks_completed": completed_recv,
            "tasks_failed": failed_recv,
            "completion_rate_pct": completion_rate,
            "error_rate_pct": error_rate,
            "sent_by_status": sent_counts,
            "received_by_status": recv_counts,
            "audit_events": event_counts,
            "tool_usage": [{"tool": r["tool"], "calls": r["cnt"]} for r in tool_counts],
            "cost": {
                "total_usd": round(cost_data["total_cost"], 6) if cost_data else 0.0,
                "prompt_tokens": cost_data["total_prompt"] if cost_data else 0,
                "completion_tokens": cost_data["total_completion"] if cost_data else 0,
                "llm_calls": cost_data["call_count"] if cost_data else 0,
            },
            "error_events": error_events["cnt"] if error_events else 0,
        }

    # ── Cross-agent comparison ────────────────────────────────────────

    def leaderboard(self, days: int = 30) -> list[dict[str, Any]]:
        """Performance leaderboard for all agents, ranked by completion rate."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        # Get all agents that have sent or received tasks
        agent_rows = self._db.fetchall(
            """SELECT DISTINCT agent_id FROM (
                SELECT sender_id as agent_id FROM tasks WHERE created_at >= ?
                UNION
                SELECT receiver_id as agent_id FROM tasks WHERE created_at >= ?
                UNION
                SELECT assignee as agent_id FROM tasks WHERE assignee != '' AND created_at >= ?
            )""",
            (cutoff, cutoff, cutoff),
        )

        summaries = []
        for row in agent_rows:
            agent_id = row["agent_id"]
            if not agent_id:
                continue
            summary = self.agent_summary(agent_id, days)
            summaries.append(summary)

        # Sort by completion rate (descending), then by total tasks (descending)
        summaries.sort(key=lambda s: (s["completion_rate_pct"], s["tasks_completed"]), reverse=True)

        # Add rank
        for i, s in enumerate(summaries):
            s["rank"] = i + 1

        return summaries

    # ── Model usage distribution ──────────────────────────────────────

    def model_usage_distribution(self, days: int = 30) -> list[dict[str, Any]]:
        """Distribution of model usage across agents."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        return self._db.fetchall(
            """SELECT model, provider, agent_name,
                      COUNT(*) as calls,
                      SUM(prompt_tokens) as prompt_tokens,
                      SUM(completion_tokens) as completion_tokens,
                      SUM(cost_usd) as cost_usd
               FROM cost_records
               WHERE timestamp >= ?
               GROUP BY model, provider, agent_name
               ORDER BY cost_usd DESC""",
            (cutoff,),
        )

    # ── Execution time analysis ───────────────────────────────────────

    def task_duration_stats(self, days: int = 30) -> dict[str, Any]:
        """Aggregate task duration statistics.

        Estimates duration from created_at -> completed_at timestamps.
        """
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        rows = self._db.fetchall(
            """SELECT id, receiver_id, created_at, completed_at, status
               FROM tasks
               WHERE status IN ('completed', 'failed')
               AND created_at >= ?
               AND completed_at != ''
               AND completed_at IS NOT NULL""",
            (cutoff,),
        )

        if not rows:
            return {"count": 0, "avg_seconds": 0, "median_seconds": 0, "by_agent": {}}

        durations: list[float] = []
        by_agent: dict[str, list[float]] = {}

        for r in rows:
            try:
                created = datetime.fromisoformat(r["created_at"])
                completed = datetime.fromisoformat(r["completed_at"])
                duration = (completed - created).total_seconds()
                if duration >= 0:
                    durations.append(duration)
                    agent = r["receiver_id"]
                    by_agent.setdefault(agent, []).append(duration)
            except (ValueError, TypeError):
                continue

        if not durations:
            return {"count": 0, "avg_seconds": 0, "median_seconds": 0, "by_agent": {}}

        durations.sort()
        mid = len(durations) // 2
        median = durations[mid] if len(durations) % 2 else (durations[mid - 1] + durations[mid]) / 2

        agent_stats = {}
        for agent, durs in by_agent.items():
            durs_sorted = sorted(durs)
            m = len(durs_sorted) // 2
            med = durs_sorted[m] if len(durs_sorted) % 2 else (durs_sorted[m - 1] + durs_sorted[m]) / 2
            agent_stats[agent] = {
                "count": len(durs),
                "avg_seconds": round(sum(durs) / len(durs), 2),
                "median_seconds": round(med, 2),
                "min_seconds": round(min(durs), 2),
                "max_seconds": round(max(durs), 2),
            }

        return {
            "count": len(durations),
            "avg_seconds": round(sum(durations) / len(durations), 2),
            "median_seconds": round(median, 2),
            "min_seconds": round(min(durations), 2),
            "max_seconds": round(max(durations), 2),
            "by_agent": agent_stats,
        }

    # ── Error analysis ────────────────────────────────────────────────

    def error_analysis(self, days: int = 30) -> dict[str, Any]:
        """Detailed error analysis across agents."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        # Failed tasks by agent
        failed_tasks = self._db.fetchall(
            """SELECT receiver_id, COUNT(*) as cnt
               FROM tasks
               WHERE status = 'failed' AND created_at >= ?
               GROUP BY receiver_id
               ORDER BY cnt DESC""",
            (cutoff,),
        )

        # Error events by agent and type
        error_events = self._db.fetchall(
            """SELECT agent_id, event_type, COUNT(*) as cnt
               FROM audit_events
               WHERE agent_id != '' AND timestamp >= ?
               AND (event_type = 'error' OR severity IN ('error', 'critical'))
               GROUP BY agent_id, event_type
               ORDER BY cnt DESC""",
            (cutoff,),
        )

        # Error severity distribution
        severity_dist = self._db.fetchall(
            """SELECT severity, COUNT(*) as cnt
               FROM audit_events
               WHERE timestamp >= ?
               GROUP BY severity
               ORDER BY cnt DESC""",
            (cutoff,),
        )

        return {
            "period_days": days,
            "failed_tasks_by_agent": [
                {"agent_id": r["receiver_id"], "count": r["cnt"]}
                for r in failed_tasks
            ],
            "error_events_by_agent": [
                {"agent_id": r["agent_id"], "event_type": r["event_type"], "count": r["cnt"]}
                for r in error_events
            ],
            "severity_distribution": {r["severity"]: r["cnt"] for r in severity_dist},
        }

    # ── Full agent report ─────────────────────────────────────────────

    def full_report(self, days: int = 30) -> dict[str, Any]:
        """Complete performance report combining all analytics."""
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "period_days": days,
            "leaderboard": self.leaderboard(days),
            "task_durations": self.task_duration_stats(days),
            "model_usage": self.model_usage_distribution(days),
            "error_analysis": self.error_analysis(days),
        }
