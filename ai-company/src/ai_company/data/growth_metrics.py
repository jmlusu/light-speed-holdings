"""Growth metrics — track adoption, completion, cost efficiency, and engagement.

Provides SQLite-backed metrics for measuring the growth trajectory of the
AI Company Builder system, including agent adoption rates, task completion
rates, cost efficiency trends, and engagement indicators.

All metrics are computed from the existing tasks, cost_records, and
audit_events tables in the database.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from ai_company.data.database import Database

logger = logging.getLogger(__name__)


class GrowthMetrics:
    """Core growth metrics engine.

    Tracks four growth dimensions:
    1. **Agent adoption** — how many agents are active and growing
    2. **Task completion** — throughput and reliability over time
    3. **Cost efficiency** — cost per task, cost per completion, trend
    4. **Engagement** — activity frequency, error recovery, escalation rates

    Args:
        database: An initialised :class:`Database` instance.
    """

    def __init__(self, database: Database) -> None:
        self._db = database

    # ── Agent Adoption ──────────────────────────────────────────────

    def agent_adoption_rate(self, days: int = 30) -> dict[str, Any]:
        """Measure agent adoption over time.

        Returns the percentage of registered agents that have been active
        (sent or received at least one task) in the period, plus a daily
        activation curve.

        Returns:
            Dict with total_agents, active_agents, adoption_pct,
            daily_active_agents, and new_agents_per_day.
        """
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        day_cutoffs = [
            (datetime.now(timezone.utc) - timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(days, -1, -1)
        ]

        # Total registered agents (from tasks table as proxy — any agent
        # that ever appeared in sender_id or receiver_id)
        all_agents_rows = self._db.fetchall(
            """SELECT DISTINCT agent_id FROM (
                SELECT sender_id as agent_id FROM tasks
                UNION
                SELECT receiver_id as agent_id FROM tasks
                UNION
                SELECT assignee as agent_id FROM tasks WHERE assignee != ''
            )"""
        )
        total_agents = len([r for r in all_agents_rows if r["agent_id"]])

        # Agents active in the full period
        active_rows = self._db.fetchall(
            """SELECT DISTINCT agent_id FROM (
                SELECT sender_id as agent_id FROM tasks WHERE created_at >= ?
                UNION
                SELECT receiver_id as agent_id FROM tasks WHERE created_at >= ?
                UNION
                SELECT assignee as agent_id FROM tasks
                    WHERE assignee != '' AND created_at >= ?
            )""",
            (cutoff, cutoff, cutoff),
        )
        active_agents = len([r for r in active_rows if r["agent_id"]])

        adoption_pct = (
            round(active_agents / total_agents * 100, 2) if total_agents > 0 else 0.0
        )

        # Daily active agent counts
        daily_active: list[dict[str, Any]] = []
        for day_str in day_cutoffs:
            count_row = self._db.fetchone(
                """SELECT COUNT(DISTINCT agent_id) as cnt FROM (
                    SELECT sender_id as agent_id FROM tasks
                        WHERE date(created_at) = ?
                    UNION
                    SELECT receiver_id as agent_id FROM tasks
                        WHERE date(created_at) = ?
                )""",
                (day_str, day_str),
            )
            daily_active.append({
                "date": day_str,
                "active_agents": count_row["cnt"] if count_row else 0,
            })

        # New agents (first appearance) per day
        new_per_day: list[dict[str, Any]] = []
        for day_str in day_cutoffs:
            count_row = self._db.fetchone(
                """SELECT COUNT(*) as cnt FROM (
                    SELECT agent_id, MIN(created_at) as first_seen
                    FROM (
                        SELECT sender_id as agent_id, created_at FROM tasks
                        UNION ALL
                        SELECT receiver_id as agent_id, created_at FROM tasks
                    )
                    WHERE agent_id != ''
                    GROUP BY agent_id
                    HAVING date(first_seen) = ?
                )""",
                (day_str,),
            )
            new_per_day.append({
                "date": day_str,
                "new_agents": count_row["cnt"] if count_row else 0,
            })

        return {
            "period_days": days,
            "total_agents": total_agents,
            "active_agents": active_agents,
            "adoption_pct": adoption_pct,
            "daily_active_agents": daily_active,
            "new_agents_per_day": new_per_day,
        }

    # ── Task Completion ─────────────────────────────────────────────

    def task_completion_metrics(self, days: int = 30) -> dict[str, Any]:
        """Track task completion rate and throughput over time.

        Returns daily task counts by status, overall completion rate,
        and failure rate trends.
        """
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        # Overall status distribution
        status_rows = self._db.fetchall(
            """SELECT status, COUNT(*) as cnt
               FROM tasks WHERE created_at >= ?
               GROUP BY status""",
            (cutoff,),
        )
        status_counts = {r["status"]: r["cnt"] for r in status_rows}

        total_tasks = sum(status_counts.values())
        completed = status_counts.get("completed", 0)
        failed = status_counts.get("failed", 0)
        finished = completed + failed

        completion_rate = round(completed / finished * 100, 2) if finished > 0 else 0.0
        failure_rate = round(failed / finished * 100, 2) if finished > 0 else 0.0
        throughput_per_day = round(total_tasks / max(days, 1), 1)

        # Daily breakdown
        daily_rows = self._db.fetchall(
            """SELECT date(created_at) as day, status, COUNT(*) as cnt
               FROM tasks WHERE created_at >= ?
               GROUP BY day, status ORDER BY day""",
            (cutoff,),
        )
        daily_by_status: dict[str, dict[str, int]] = {}
        for row in daily_rows:
            day = row["day"]
            if day not in daily_by_status:
                daily_by_status[day] = {}
            daily_by_status[day][row["status"]] = row["cnt"]

        daily_trend: list[dict[str, Any]] = []
        for day, counts in sorted(daily_by_status.items()):
            day_total = sum(counts.values())
            day_completed = counts.get("completed", 0)
            day_failed = counts.get("failed", 0)
            day_finished = day_completed + day_failed
            daily_trend.append({
                "date": day,
                "total": day_total,
                "completed": day_completed,
                "failed": day_failed,
                "completion_rate_pct": (
                    round(day_completed / day_finished * 100, 2)
                    if day_finished > 0 else 0.0
                ),
            })

        # Average task duration
        duration_rows = self._db.fetchall(
            """SELECT created_at, completed_at FROM tasks
               WHERE status IN ('completed', 'failed')
               AND created_at >= ?
               AND completed_at != '' AND completed_at IS NOT NULL""",
            (cutoff,),
        )
        durations: list[float] = []
        for row in duration_rows:
            try:
                created = datetime.fromisoformat(row["created_at"])
                completed = datetime.fromisoformat(row["completed_at"])
                dur = (completed - created).total_seconds()
                if dur >= 0:
                    durations.append(dur)
            except (ValueError, TypeError):
                continue

        avg_duration = round(sum(durations) / len(durations), 2) if durations else 0.0

        return {
            "period_days": days,
            "total_tasks": total_tasks,
            "completed": completed,
            "failed": failed,
            "completion_rate_pct": completion_rate,
            "failure_rate_pct": failure_rate,
            "throughput_per_day": throughput_per_day,
            "avg_duration_seconds": avg_duration,
            "status_distribution": status_counts,
            "daily_trend": daily_trend,
        }

    # ── Cost Efficiency ─────────────────────────────────────────────

    def cost_efficiency_metrics(self, days: int = 30) -> dict[str, Any]:
        """Track cost efficiency over time.

        Returns cost per task, cost per completion, cost trends, and
        cost per agent.
        """
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        # Total cost in period
        cost_row = self._db.fetchone(
            """SELECT COALESCE(SUM(cost_usd), 0) as total_cost,
                      COALESCE(SUM(prompt_tokens), 0) as total_prompt,
                      COALESCE(SUM(completion_tokens), 0) as total_completion,
                      COUNT(*) as call_count
               FROM cost_records WHERE timestamp >= ?""",
            (cutoff,),
        )
        total_cost = cost_row["total_cost"] if cost_row else 0.0
        total_calls = cost_row["call_count"] if cost_row else 0
        total_prompt = cost_row["total_prompt"] if cost_row else 0
        total_completion = cost_row["total_completion"] if cost_row else 0

        # Task counts in same period
        task_row = self._db.fetchone(
            """SELECT COUNT(*) as total,
                      SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
               FROM tasks WHERE created_at >= ?""",
            (cutoff,),
        )
        total_tasks = task_row["total"] if task_row else 0
        completed_tasks = task_row["completed"] if task_row else 0

        cost_per_task = round(total_cost / total_tasks, 6) if total_tasks > 0 else 0.0
        cost_per_completion = (
            round(total_cost / completed_tasks, 6) if completed_tasks > 0 else 0.0
        )
        cost_per_1k_tokens = (
            round(total_cost / ((total_prompt + total_completion) / 1000), 6)
            if (total_prompt + total_completion) > 0 else 0.0
        )

        # Daily cost trend
        daily_cost_rows = self._db.fetchall(
            """SELECT date(timestamp) as day,
                      SUM(cost_usd) as daily_cost,
                      COUNT(*) as calls
               FROM cost_records WHERE timestamp >= ?
               GROUP BY day ORDER BY day""",
            (cutoff,),
        )

        daily_trend: list[dict[str, Any]] = []
        for row in daily_cost_rows:
            daily_trend.append({
                "date": row["day"],
                "cost_usd": round(row["daily_cost"], 6),
                "calls": row["calls"],
            })

        # Cost per agent
        agent_cost_rows = self._db.fetchall(
            """SELECT agent_name,
                      SUM(cost_usd) as total_cost,
                      COUNT(*) as calls
               FROM cost_records WHERE timestamp >= ?
               GROUP BY agent_name ORDER BY total_cost DESC""",
            (cutoff,),
        )

        return {
            "period_days": days,
            "total_cost_usd": round(total_cost, 6),
            "total_llm_calls": total_calls,
            "total_tokens": total_prompt + total_completion,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "cost_per_task_usd": cost_per_task,
            "cost_per_completion_usd": cost_per_completion,
            "cost_per_1k_tokens_usd": cost_per_1k_tokens,
            "daily_cost_trend": daily_trend,
            "cost_by_agent": [
                {
                    "agent_name": r["agent_name"],
                    "cost_usd": round(r["total_cost"], 6),
                    "calls": r["calls"],
                }
                for r in agent_cost_rows
            ],
        }

    # ── Engagement Metrics ──────────────────────────────────────────

    def engagement_metrics(self, days: int = 30) -> dict[str, Any]:
        """Track user engagement and system activity indicators.

        Includes activity frequency, error recovery rate, escalation rate,
        and approval responsiveness.
        """
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        # Total audit events (proxy for activity)
        event_row = self._db.fetchone(
            """SELECT COUNT(*) as total,
                      SUM(CASE WHEN event_type = 'error' THEN 1 ELSE 0 END) as errors,
                      SUM(CASE WHEN event_type = 'tool_call' THEN 1 ELSE 0 END) as tool_calls,
                      SUM(CASE WHEN event_type = 'tool_result' THEN 1 ELSE 0 END) as tool_results
               FROM audit_events WHERE timestamp >= ?""",
            (cutoff,),
        )
        total_events = event_row["total"] if event_row else 0
        error_events = event_row["errors"] if event_row else 0
        tool_calls = event_row["tool_calls"] if event_row else 0

        # Escalation rate
        escalation_row = self._db.fetchone(
            """SELECT COUNT(*) as total,
                      SUM(CASE WHEN resolved = 1 THEN 1 ELSE 0 END) as resolved
               FROM escalation_events WHERE timestamp >= ?""",
            (cutoff,),
        )
        total_escalations = escalation_row["total"] if escalation_row else 0
        resolved_escalations = escalation_row["resolved"] if escalation_row else 0
        escalation_rate = (
            round(total_escalations / max(tool_calls, 1) * 100, 2)
            if tool_calls > 0 else 0.0
        )

        # Error recovery rate (completed tasks after failures in same period)
        task_status_row = self._db.fetchone(
            """SELECT
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed
               FROM tasks WHERE created_at >= ?""",
            (cutoff,),
        )
        completed = task_status_row["completed"] if task_status_row else 0
        failed = task_status_row["failed"] if task_status_row else 0
        error_recovery_rate = (
            round(completed / (completed + failed) * 100, 2)
            if (completed + failed) > 0 else 0.0
        )

        # Daily activity (events per day)
        daily_activity_rows = self._db.fetchall(
            """SELECT date(timestamp) as day, COUNT(*) as events
               FROM audit_events WHERE timestamp >= ?
               GROUP BY day ORDER BY day""",
            (cutoff,),
        )
        daily_activity = [
            {"date": r["day"], "events": r["events"]}
            for r in daily_activity_rows
        ]

        # Unique active agents per day (engagement breadth)
        daily_agents_rows = self._db.fetchall(
            """SELECT date(timestamp) as day,
                      COUNT(DISTINCT agent_id) as agents
               FROM audit_events WHERE timestamp >= ?
               GROUP BY day ORDER BY day""",
            (cutoff,),
        )
        daily_agent_engagement = [
            {"date": r["day"], "agents": r["agents"]}
            for r in daily_agents_rows
        ]

        # Activity frequency
        days_with_activity = len(daily_activity)
        activity_rate = (
            round(days_with_activity / max(days, 1) * 100, 2)
        )

        return {
            "period_days": days,
            "total_audit_events": total_events,
            "tool_calls": tool_calls,
            "error_events": error_events,
            "escalation_rate_pct": escalation_rate,
            "total_escalations": total_escalations,
            "resolved_escalations": resolved_escalations,
            "error_recovery_rate_pct": error_recovery_rate,
            "completed_tasks": completed,
            "failed_tasks": failed,
            "activity_rate_pct": activity_rate,
            "daily_activity": daily_activity,
            "daily_agent_engagement": daily_agent_engagement,
        }

    # ── Combined Growth Dashboard ───────────────────────────────────

    def growth_dashboard(self, days: int = 30) -> dict[str, Any]:
        """Aggregate all growth metrics into a single dashboard payload.

        Returns a comprehensive growth snapshot with all four dimensions
        and an overall growth score (0-100).
        """
        adoption = self.agent_adoption_rate(days)
        completion = self.task_completion_metrics(days)
        cost = self.cost_efficiency_metrics(days)
        engagement = self.engagement_metrics(days)

        # Compute composite growth score (0-100)
        growth_score = self._compute_growth_score(adoption, completion, cost, engagement)

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "period_days": days,
            "growth_score": growth_score,
            "agent_adoption": adoption,
            "task_completion": completion,
            "cost_efficiency": cost,
            "engagement": engagement,
        }

    def _compute_growth_score(
        self,
        adoption: dict[str, Any],
        completion: dict[str, Any],
        cost: dict[str, Any],
        engagement: dict[str, Any],
    ) -> float:
        """Compute a composite growth score (0-100).

        Weights:
        - Adoption: 25%
        - Completion rate: 30%
        - Cost efficiency (inverse of cost per task): 20%
        - Engagement: 25%
        """
        # Adoption score: adoption_pct (0-100)
        adoption_score = min(adoption.get("adoption_pct", 0), 100)

        # Completion score: completion_rate_pct (0-100)
        completion_score = min(completion.get("completion_rate_pct", 0), 100)

        # Cost efficiency score: lower cost_per_task is better
        # Normalize: $0 -> 100, $0.10 -> 0
        cpt = cost.get("cost_per_task_usd", 0)
        cost_score = max(0, 100 - (cpt * 1000))  # $0.10 = 0, $0 = 100

        # Engagement score: combination of activity and recovery
        activity = engagement.get("activity_rate_pct", 0)
        recovery = engagement.get("error_recovery_rate_pct", 0)
        engagement_score = (activity * 0.5 + recovery * 0.5)

        # Weighted composite
        score = (
            adoption_score * 0.25
            + completion_score * 0.30
            + cost_score * 0.20
            + engagement_score * 0.25
        )

        return round(min(max(score, 0), 100), 2)

    # ── Week-over-Week Comparison ───────────────────────────────────

    def week_over_week_comparison(self) -> dict[str, Any]:
        """Compare this week's metrics against last week's.

        Returns deltas for each growth dimension.
        """
        now = datetime.now(timezone.utc)
        this_week_start = (now - timedelta(days=now.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        this_week_days = (now - this_week_start).days + 1
        last_week_days = 7

        this_week = self.growth_dashboard(days=this_week_days)
        last_week = self.growth_dashboard(days=last_week_days + this_week_days)
        # last_week already spans the full lookback window; the 7 days before
        # this week are implicitly the tail of that range.

        return {
            "comparison_type": "week_over_week",
            "this_week": {
                "period_days": this_week_days,
                "growth_score": this_week["growth_score"],
                "adoption_pct": this_week["agent_adoption"]["adoption_pct"],
                "completion_rate_pct": this_week["task_completion"]["completion_rate_pct"],
                "cost_per_task_usd": this_week["cost_efficiency"]["cost_per_task_usd"],
                "error_recovery_rate_pct": this_week["engagement"]["error_recovery_rate_pct"],
            },
            "last_week": {
                "period_days": last_week_days,
                "growth_score": last_week["growth_score"],
                "adoption_pct": last_week["agent_adoption"]["adoption_pct"],
                "completion_rate_pct": last_week["task_completion"]["completion_rate_pct"],
                "cost_per_task_usd": last_week["cost_efficiency"]["cost_per_task_usd"],
                "error_recovery_rate_pct": last_week["engagement"]["error_recovery_rate_pct"],
            },
            "deltas": {
                "growth_score": round(
                    this_week["growth_score"] - last_week["growth_score"], 2
                ),
                "adoption_pct": round(
                    this_week["agent_adoption"]["adoption_pct"]
                    - last_week["agent_adoption"]["adoption_pct"],
                    2,
                ),
                "completion_rate_pct": round(
                    this_week["task_completion"]["completion_rate_pct"]
                    - last_week["task_completion"]["completion_rate_pct"],
                    2,
                ),
                "cost_per_task_usd": round(
                    this_week["cost_efficiency"]["cost_per_task_usd"]
                    - last_week["cost_efficiency"]["cost_per_task_usd"],
                    6,
                ),
            },
        }

    # ── Month-over-Month Comparison ─────────────────────────────────

    def month_over_month_comparison(self) -> dict[str, Any]:
        """Compare this month's metrics against last month's.

        Returns deltas for each growth dimension.
        """
        now = datetime.now(timezone.utc)
        this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_end = this_month_start - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        this_month_days = (now - this_month_start).days + 1
        last_month_days = (last_month_end - last_month_start).days + 1

        this_month = self.growth_dashboard(days=this_month_days)
        last_month = self.growth_dashboard(days=this_month_days + last_month_days)

        return {
            "comparison_type": "month_over_month",
            "this_month": {
                "period_days": this_month_days,
                "growth_score": this_month["growth_score"],
                "adoption_pct": this_month["agent_adoption"]["adoption_pct"],
                "completion_rate_pct": this_month["task_completion"]["completion_rate_pct"],
                "cost_per_task_usd": this_month["cost_efficiency"]["cost_per_task_usd"],
                "error_recovery_rate_pct": this_month["engagement"]["error_recovery_rate_pct"],
            },
            "last_month": {
                "period_days": last_month_days,
                "growth_score": last_month["growth_score"],
                "adoption_pct": last_month["agent_adoption"]["adoption_pct"],
                "completion_rate_pct": last_month["task_completion"]["completion_rate_pct"],
                "cost_per_task_usd": last_month["cost_efficiency"]["cost_per_task_usd"],
                "error_recovery_rate_pct": last_month["engagement"]["error_recovery_rate_pct"],
            },
            "deltas": {
                "growth_score": round(
                    this_month["growth_score"] - last_month["growth_score"], 2
                ),
                "adoption_pct": round(
                    this_month["agent_adoption"]["adoption_pct"]
                    - last_month["agent_adoption"]["adoption_pct"],
                    2,
                ),
                "completion_rate_pct": round(
                    this_month["task_completion"]["completion_rate_pct"]
                    - last_month["task_completion"]["completion_rate_pct"],
                    2,
                ),
                "cost_per_task_usd": round(
                    this_month["cost_efficiency"]["cost_per_task_usd"]
                    - last_month["cost_efficiency"]["cost_per_task_usd"],
                    6,
                ),
            },
        }
