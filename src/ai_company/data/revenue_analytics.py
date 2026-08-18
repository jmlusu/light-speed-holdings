"""Revenue analytics — pairing costs with revenue for ROI calculations.

Extends CostAnalytics with revenue attribution by linking
revenue_transactions to tasks via linked_task_id, and cost_records
via task_id.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from ai_company.data.database import Database
from ai_company.models.models import RevenueAttribution, RevenueSummary

logger = logging.getLogger(__name__)


class RevenueAnalytics:
    """LLM cost + revenue analytics backed by SQLite.

    Provides:
      - Revenue attribution per agent/department
      - ROI calculations
      - Revenue trend analysis
      - Cost vs revenue comparison
    """

    def __init__(self, database: Database) -> None:
        self._db = database

    def _per_agent_costs(self, start_date: str, end_date: str) -> dict[str, float]:
        """Get total cost per agent for a date range."""
        rows = self._db.fetchall(
            """SELECT agent_name, COALESCE(SUM(cost_usd), 0) as total_cost
               FROM cost_records
               WHERE date(timestamp) >= ? AND date(timestamp) < ?
               GROUP BY agent_name""",
            (start_date, end_date),
        )
        return {r["agent_name"]: r["total_cost"] for r in rows}

    def _per_task_revenue(self, start_date: str, end_date: str) -> dict[str, float]:
        """Get total revenue per linked_task_id for a date range."""
        rows = self._db.fetchall(
            """SELECT linked_task_id, COALESCE(SUM(amount), 0) as total_revenue
               FROM revenue_transactions
               WHERE date(timestamp) >= ? AND date(timestamp) < ?
               AND linked_task_id != '' AND status = 'completed'
               GROUP BY linked_task_id""",
            (start_date, end_date),
        )
        return {r["linked_task_id"]: r["total_revenue"] for r in rows}

    def _agent_for_task(self, task_id: str) -> str | None:
        """Look up which agent was assigned to a task."""
        row = self._db.fetchone(
            "SELECT assignee FROM tasks WHERE id = ?",
            (task_id,),
        )
        return row["assignee"] if row and row["assignee"] else None

    def _agent_department(self, agent_name: str) -> str:
        """Look up the department for an agent from the agent registry."""
        from ai_company.registry import load_registry
        registry = load_registry()
        # Check specialists
        for agent in registry.specialists:
            if agent.id == agent_name and agent.department:
                return agent.department
        # Check executives
        for exec_ in registry.executives:
            if exec_.id == agent_name and exec_.department:
                return exec_.department
        return "unknown"

    def _tasks_completed_by_agent(self, start_date: str, end_date: str) -> dict[str, int]:
        """Count completed tasks per agent for a date range."""
        rows = self._db.fetchall(
            """SELECT assignee, COUNT(*) as completed
               FROM tasks
               WHERE status = 'completed'
               AND date(created_at) >= ? AND date(created_at) < ?
               AND assignee != ''
               GROUP BY assignee""",
            (start_date, end_date),
        )
        return {r["assignee"]: r["completed"] for r in rows}

    def get_revenue_attribution(self, period_days: int = 30) -> RevenueSummary:
        """Compute revenue attribution and ROI for all agents/departments."""
        today = datetime.now(timezone.utc)
        end_date = today.strftime("%Y-%m-%d")
        start_dt = today - timedelta(days=period_days)
        start_date = start_dt.strftime("%Y-%m-%d")

        costs = self._per_agent_costs(start_date, end_date)
        revenue_by_task = self._per_task_revenue(start_date, end_date)
        tasks_by_agent = self._tasks_completed_by_agent(start_date, end_date)

        # Map revenue to agents via task assignments
        agent_revenue: dict[str, float] = {}
        agent_tasks: dict[str, int] = {}

        for task_id, revenue in revenue_by_task.items():
            agent = self._agent_for_task(task_id)
            if agent:
                agent_revenue[agent] = agent_revenue.get(agent, 0) + revenue
                agent_tasks[agent] = agent_tasks.get(agent, 0) + 1

        # Build attribution list
        attributions: list[RevenueAttribution] = []
        for agent_id in sorted(set(list(costs.keys()) + list(agent_revenue.keys()) + list(tasks_by_agent.keys()))):
            cost = costs.get(agent_id, 0.0)
            revenue = agent_revenue.get(agent_id, 0.0)
            tasks = int(tasks_by_agent.get(agent_id, 0))
            roi = revenue / cost if cost > 0 else 0.0
            revenue_per_task = revenue / tasks if tasks > 0 else 0.0

            department = self._agent_department(agent_id)

            attributions.append(RevenueAttribution(
                agent_id=agent_id,
                department=department,
                tasks_completed=tasks,
                revenue_attributed=round(revenue, 2),
                cost_incurred=round(cost, 6),
                roi=round(roi, 2),
                revenue_per_task=round(revenue_per_task, 2),
            ))

        # Group by department
        dept_revenue: dict[str, dict[str, float]] = {}
        for attr in attributions:
            dept = attr.department
            if dept not in dept_revenue:
                dept_revenue[dept] = {"revenue": 0, "cost": 0, "tasks": 0}
            dept_revenue[dept]["revenue"] += attr.revenue_attributed
            dept_revenue[dept]["cost"] += attr.cost_incurred
            dept_revenue[dept]["tasks"] += attr.tasks_completed

        by_department = [
            RevenueAttribution(
                agent_id=f"{dept}__department_total",
                department=dept,
                tasks_completed=int(data["tasks"]),
                revenue_attributed=round(data["revenue"], 2),
                cost_incurred=round(data["cost"], 6),
                roi=round(data["revenue"] / data["cost"], 2) if data["cost"] > 0 else 0.0,
                revenue_per_task=round(data["revenue"] / data["tasks"], 2) if data["tasks"] > 0 else 0.0,
            )
            for dept, data in sorted(dept_revenue.items())
        ]

        total_revenue = sum(a.revenue_attributed for a in attributions)
        total_cost = sum(a.cost_incurred for a in attributions)

        return RevenueSummary(
            total_revenue=round(total_revenue, 2),
            total_cost=round(total_cost, 6),
            overall_roi=round(total_revenue / total_cost, 2) if total_cost > 0 else 0.0,
            by_department=by_department,
            by_agent=attributions,
            period_days=period_days,
        )

    def get_revenue_trend(self, period_days: int = 30) -> list[dict[str, Any]]:
        """Get daily revenue trend data."""
        today = datetime.now(timezone.utc)
        start_dt = today - timedelta(days=period_days)
        start_date = start_dt.strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")

        rows = self._db.fetchall(
            """SELECT date(timestamp) as day,
                     COALESCE(SUM(amount), 0) as revenue,
                     COALESCE(SUM(CASE WHEN currency = 'USD' THEN amount
                                  ELSE amount * exchange_rate END), 0) as revenue_usd
               FROM revenue_transactions
               WHERE date(timestamp) >= ? AND date(timestamp) <= ?
               AND status = 'completed'
               GROUP BY day
               ORDER BY day""",
            (start_date, end_date),
        )

        return [
            {
                "date": r["day"],
                "revenue": r["revenue"],
                "revenue_usd": r["revenue_usd"],
            }
            for r in rows
        ]
