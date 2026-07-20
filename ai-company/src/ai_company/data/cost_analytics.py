"""Cost analytics — daily/weekly/monthly aggregation and budget forecasting.

Replaces the file-based ``CostTracker`` JSONL log with efficient SQLite
queries and adds multi-dimensional cost breakdown and forecasting.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from ai_company.data.database import Database

logger = logging.getLogger(__name__)


class CostAnalytics:
    """LLM cost analytics backed by SQLite.

    Provides:
      - Recording of individual LLM usage events.
      - Aggregation by day, week, month.
      - Breakdown by agent, task, model, provider, department.
      - Budget tracking and forecasting.

    Args:
        database: An initialised :class:`Database` instance.
        daily_budget_usd: Optional daily spend cap. ``None`` = unlimited.
        task_budget_usd: Optional per-task spend cap. ``None`` = unlimited.
    """

    def __init__(
        self,
        database: Database,
        daily_budget_usd: float | None = None,
        task_budget_usd: float | None = None,
    ) -> None:
        self._db = database
        self.daily_budget = daily_budget_usd
        self.task_budget = task_budget_usd

    # ── Recording ─────────────────────────────────────────────────────

    def record_usage(
        self,
        model: str,
        provider: str,
        agent_name: str,
        task_id: str,
        prompt_tokens: int,
        completion_tokens: int,
        cost_usd: float,
        iteration: int = 1,
        metadata: dict[str, Any] | None = None,
        timestamp: str | None = None,
    ) -> int:
        """Record a single LLM usage event.

        Returns the row ID of the inserted record.
        """
        ts = timestamp or datetime.now(timezone.utc).isoformat()
        cursor = self._db.execute(
            """INSERT INTO cost_records
               (timestamp, model, provider, agent_name, task_id,
                prompt_tokens, completion_tokens, cost_usd, iteration, metadata)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                ts, model, provider, agent_name, task_id,
                prompt_tokens, completion_tokens, cost_usd, iteration,
                json.dumps(metadata or {}, default=str),
            ),
        )
        self._db.commit()
        return cursor.lastrowid or 0

    def check_budget(self, task_id: str, proposed_cost: float = 0.0) -> tuple[bool, str]:
        """Check if a new LLM call would exceed budget limits.

        Returns ``(allowed, reason)``.
        """
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Daily budget check
        if self.daily_budget is not None:
            daily = self.get_daily_total(today)
            if daily + proposed_cost > self.daily_budget:
                return (
                    False,
                    f"Daily budget exceeded: ${daily:.4f} + "
                    f"${proposed_cost:.4f} > ${self.daily_budget:.2f}",
                )

        # Task budget check
        if self.task_budget is not None:
            task_total = self.get_task_total(task_id)
            if task_total + proposed_cost > self.task_budget:
                return (
                    False,
                    f"Task budget exceeded: ${task_total:.4f} + "
                    f"${proposed_cost:.4f} > ${self.task_budget:.2f}",
                )

        return True, "within budget"

    # ── Aggregation queries ───────────────────────────────────────────

    def get_daily_total(self, day: str | None = None) -> float:
        """Return total cost for a given day (or today)."""
        target = day or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        row = self._db.fetchone(
            "SELECT COALESCE(SUM(cost_usd), 0) as total FROM cost_records WHERE date(timestamp) = ?",
            (target,),
        )
        return row["total"] if row else 0.0

    def get_task_total(self, task_id: str) -> float:
        """Return total cost for a specific task."""
        row = self._db.fetchone(
            "SELECT COALESCE(SUM(cost_usd), 0) as total FROM cost_records WHERE task_id = ?",
            (task_id,),
        )
        return row["total"] if row else 0.0

    def get_agent_total(self, agent_name: str) -> float:
        """Return total cost for a specific agent."""
        row = self._db.fetchone(
            "SELECT COALESCE(SUM(cost_usd), 0) as total FROM cost_records WHERE agent_name = ?",
            (agent_name,),
        )
        return row["total"] if row else 0.0

    def daily_summary(self, day: str | None = None) -> dict[str, Any]:
        """Full summary for a given day."""
        target = day or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        rows = self._db.fetchall(
            """SELECT
                model,
                SUM(cost_usd) as cost_usd,
                SUM(prompt_tokens) as prompt_tokens,
                SUM(completion_tokens) as completion_tokens,
                COUNT(*) as calls
               FROM cost_records
               WHERE date(timestamp) = ?
               GROUP BY model""",
            (target,),
        )

        total_cost = sum(r["cost_usd"] for r in rows)
        total_prompt = sum(r["prompt_tokens"] for r in rows)
        total_completion = sum(r["completion_tokens"] for r in rows)
        total_calls = sum(r["calls"] for r in rows)

        return {
            "date": target,
            "total_cost_usd": round(total_cost, 6),
            "total_prompt_tokens": total_prompt,
            "total_completion_tokens": total_completion,
            "call_count": total_calls,
            "by_model": {r["model"]: {
                "cost_usd": round(r["cost_usd"], 6),
                "prompt_tokens": r["prompt_tokens"],
                "completion_tokens": r["completion_tokens"],
                "calls": r["calls"],
            } for r in rows},
        }

    def weekly_summary(self, week_start: str | None = None) -> dict[str, Any]:
        """Summary for a 7-day period starting at *week_start*."""
        if week_start:
            start = week_start
        else:
            today = datetime.now(timezone.utc)
            start = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")

        end_dt = datetime.fromisoformat(start) + timedelta(days=7)
        end = end_dt.strftime("%Y-%m-%d")

        rows = self._db.fetchall(
            """SELECT date(timestamp) as day,
                      SUM(cost_usd) as cost_usd,
                      SUM(prompt_tokens) as prompt_tokens,
                      SUM(completion_tokens) as completion_tokens,
                      COUNT(*) as calls
               FROM cost_records
               WHERE date(timestamp) >= ? AND date(timestamp) < ?
               GROUP BY day ORDER BY day""",
            (start, end),
        )

        return {
            "period_start": start,
            "period_end": end,
            "total_cost_usd": round(sum(r["cost_usd"] for r in rows), 6),
            "total_prompt_tokens": sum(r["prompt_tokens"] for r in rows),
            "total_completion_tokens": sum(r["completion_tokens"] for r in rows),
            "call_count": sum(r["calls"] for r in rows),
            "daily_breakdown": rows,
        }

    def monthly_summary(self, month: str | None = None) -> dict[str, Any]:
        """Summary for a calendar month. *month* is ``"YYYY-MM"``."""
        if month is None:
            month = datetime.now(timezone.utc).strftime("%Y-%m")

        start = f"{month}-01"
        # Compute end of month
        start_dt = datetime.fromisoformat(start)
        if start_dt.month == 12:
            end_dt = start_dt.replace(year=start_dt.year + 1, month=1)
        else:
            end_dt = start_dt.replace(month=start_dt.month + 1)
        end = end_dt.strftime("%Y-%m-%d")

        rows = self._db.fetchall(
            """SELECT date(timestamp) as day,
                      SUM(cost_usd) as cost_usd,
                      SUM(prompt_tokens) as prompt_tokens,
                      SUM(completion_tokens) as completion_tokens,
                      COUNT(*) as calls
               FROM cost_records
               WHERE date(timestamp) >= ? AND date(timestamp) < ?
               GROUP BY day ORDER BY day""",
            (start, end),
        )

        return {
            "month": month,
            "total_cost_usd": round(sum(r["cost_usd"] for r in rows), 6),
            "total_prompt_tokens": sum(r["prompt_tokens"] for r in rows),
            "total_completion_tokens": sum(r["completion_tokens"] for r in rows),
            "call_count": sum(r["calls"] for r in rows),
            "daily_breakdown": rows,
        }

    # ── Breakdowns ────────────────────────────────────────────────────

    def breakdown_by_agent(self, days: int = 30) -> list[dict[str, Any]]:
        """Cost breakdown by agent over the last *days* days."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        return self._db.fetchall(
            """SELECT agent_name,
                      SUM(cost_usd) as cost_usd,
                      SUM(prompt_tokens) as prompt_tokens,
                      SUM(completion_tokens) as completion_tokens,
                      COUNT(*) as calls
               FROM cost_records
               WHERE timestamp >= ?
               GROUP BY agent_name
               ORDER BY cost_usd DESC""",
            (cutoff,),
        )

    def breakdown_by_task(self, days: int = 30) -> list[dict[str, Any]]:
        """Cost breakdown by task over the last *days* days."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        return self._db.fetchall(
            """SELECT task_id,
                      SUM(cost_usd) as cost_usd,
                      SUM(prompt_tokens) as prompt_tokens,
                      SUM(completion_tokens) as completion_tokens,
                      COUNT(*) as calls,
                      MAX(iteration) as max_iteration
               FROM cost_records
               WHERE timestamp >= ?
               GROUP BY task_id
               ORDER BY cost_usd DESC""",
            (cutoff,),
        )

    def breakdown_by_model(self, days: int = 30) -> list[dict[str, Any]]:
        """Cost breakdown by model over the last *days* days."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        return self._db.fetchall(
            """SELECT model, provider,
                      SUM(cost_usd) as cost_usd,
                      SUM(prompt_tokens) as prompt_tokens,
                      SUM(completion_tokens) as completion_tokens,
                      COUNT(*) as calls
               FROM cost_records
               WHERE timestamp >= ?
               GROUP BY model, provider
               ORDER BY cost_usd DESC""",
            (cutoff,),
        )

    def breakdown_by_provider(self, days: int = 30) -> list[dict[str, Any]]:
        """Cost breakdown by provider over the last *days* days."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        return self._db.fetchall(
            """SELECT provider,
                      SUM(cost_usd) as cost_usd,
                      SUM(prompt_tokens) as prompt_tokens,
                      SUM(completion_tokens) as completion_tokens,
                      COUNT(*) as calls
               FROM cost_records
               WHERE timestamp >= ?
               GROUP BY provider
               ORDER BY cost_usd DESC""",
            (cutoff,),
        )

    # ── Forecasting ───────────────────────────────────────────────────

    def forecast_daily(
        self,
        *,
        lookback_days: int = 14,
        forecast_days: int = 7,
    ) -> dict[str, Any]:
        """Simple linear extrapolation of daily costs.

        Computes the average daily cost over *lookback_days* and projects
        it forward for *forecast_days*.
        """
        cutoff = (datetime.now(timezone.utc) - timedelta(days=lookback_days)).isoformat()
        rows = self._db.fetchall(
            """SELECT date(timestamp) as day, SUM(cost_usd) as daily_cost
               FROM cost_records
               WHERE timestamp >= ?
               GROUP BY day ORDER BY day""",
            (cutoff,),
        )

        if not rows:
            return {
                "lookback_days": lookback_days,
                "forecast_days": forecast_days,
                "avg_daily_cost": 0.0,
                "projected_total": 0.0,
                "data_points": 0,
            }

        avg_daily = sum(r["daily_cost"] for r in rows) / len(rows)

        return {
            "lookback_days": lookback_days,
            "forecast_days": forecast_days,
            "avg_daily_cost": round(avg_daily, 6),
            "projected_total": round(avg_daily * forecast_days, 6),
            "data_points": len(rows),
            "daily_data": [{"day": r["day"], "cost": round(r["daily_cost"], 6)} for r in rows],
        }

    def budget_status(self, task_id: str | None = None) -> dict[str, Any]:
        """Current budget utilization status."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        daily_cost = self.get_daily_total(today)

        # This month cost
        month = today[:7]
        monthly = self.monthly_summary(month)

        result: dict[str, Any] = {
            "daily_cost_usd": round(daily_cost, 6),
            "monthly_cost_usd": round(monthly["total_cost_usd"], 6),
        }

        if self.daily_budget is not None:
            result["daily_budget"] = self.daily_budget
            result["daily_remaining"] = round(self.daily_budget - daily_cost, 6)
            result["daily_utilization_pct"] = round(
                (daily_cost / self.daily_budget) * 100 if self.daily_budget > 0 else 0, 2
            )

        if task_id and self.task_budget is not None:
            task_cost = self.get_task_total(task_id)
            result["task_id"] = task_id
            result["task_budget"] = self.task_budget
            result["task_cost_usd"] = round(task_cost, 6)
            result["task_remaining"] = round(self.task_budget - task_cost, 6)

        return result

    # ── Migration ─────────────────────────────────────────────────────

    def import_from_jsonl(self, jsonl_path: str | Path) -> int:
        """Import usage records from the legacy ``cost_log.jsonl`` file.

        Returns the number of records imported.
        """
        path = Path(jsonl_path)
        if not path.exists():
            logger.warning("Legacy cost log not found: %s", path)
            return 0

        count = 0
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    self.record_usage(
                        model=rec.get("model", ""),
                        provider=rec.get("provider", ""),
                        agent_name=rec.get("agent_name", ""),
                        task_id=rec.get("task_id", ""),
                        prompt_tokens=rec.get("prompt_tokens", 0),
                        completion_tokens=rec.get("completion_tokens", 0),
                        cost_usd=rec.get("cost_usd", 0.0),
                        iteration=rec.get("iteration", 1),
                        metadata=rec.get("metadata", {}),
                        timestamp=rec.get("timestamp"),
                    )
                    count += 1
                except (json.JSONDecodeError, KeyError):
                    continue

        logger.info("Imported %d cost records from %s", count, path)
        return count

    # ── Stats ─────────────────────────────────────────────────────────

    def total_records(self) -> int:
        """Total number of cost records."""
        return self._db.table_count("cost_records")

    def total_cost(self) -> float:
        """Total cost across all records."""
        row = self._db.fetchone(
            "SELECT COALESCE(SUM(cost_usd), 0) as total FROM cost_records"
        )
        return row["total"] if row else 0.0

    # ── Export ────────────────────────────────────────────────────────

    def export_to_jsonl(self, jsonl_path: str | Path) -> Path:
        """Export all cost records to the legacy ``cost_log.jsonl`` format.

        Returns the path of the written file.
        """
        path = Path(jsonl_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        rows = self._db.fetchall(
            "SELECT * FROM cost_records ORDER BY timestamp ASC"
        )

        with open(path, "w", encoding="utf-8") as f:
            for row in rows:
                record = {
                    "timestamp": row["timestamp"],
                    "model": row["model"],
                    "provider": row["provider"],
                    "agent_name": row["agent_name"],
                    "task_id": row["task_id"],
                    "prompt_tokens": row["prompt_tokens"],
                    "completion_tokens": row["completion_tokens"],
                    "cost_usd": row["cost_usd"],
                    "iteration": row["iteration"],
                    "metadata": json.loads(row.get("metadata", "{}")),
                }
                f.write(json.dumps(record, default=str) + "\n")

        logger.info("Exported %d cost records to %s", len(rows), path)
        return path

    # ── Extended aggregation ──────────────────────────────────────────

    def daily_cost_trend(self, days: int = 30) -> list[dict[str, Any]]:
        """Return daily cost totals for trend analysis."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        return self._db.fetchall(
            """SELECT date(timestamp) as day,
                      SUM(cost_usd) as total_cost,
                      COUNT(*) as call_count,
                      COUNT(DISTINCT agent_name) as agent_count,
                      COUNT(DISTINCT model) as model_count
               FROM cost_records
               WHERE timestamp >= ?
               GROUP BY day
               ORDER BY day""",
            (cutoff,),
        )

    def agent_daily_costs(self, agent_name: str, days: int = 30) -> list[dict[str, Any]]:
        """Return daily cost breakdown for a specific agent."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        return self._db.fetchall(
            """SELECT date(timestamp) as day,
                      SUM(cost_usd) as total_cost,
                      SUM(prompt_tokens) as prompt_tokens,
                      SUM(completion_tokens) as completion_tokens,
                      COUNT(*) as calls
               FROM cost_records
               WHERE agent_name = ? AND timestamp >= ?
               GROUP BY day
               ORDER BY day""",
            (agent_name, cutoff),
        )
