"""Cost analytics — daily/weekly/monthly aggregation and budget forecasting.

Replaces the file-based ``CostTracker`` JSONL log with efficient SQLite
queries and adds multi-dimensional cost breakdown and forecasting.
"""

from __future__ import annotations

import json
import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from ai_company.data.database import Database

logger = logging.getLogger(__name__)

# Default daily ceiling for cache-read tokens (50M). Cache reads are the
# dominant prompt-side cost driver on long Desktop sessions; the cap turns
# that into a single, checkable number per UTC day.
DEFAULT_CACHE_READ_CAP = 50_000_000


@dataclass(frozen=True)
class CacheBudgetStatus:
    """Outcome of the daily cache-read token budget check.

    ``level`` is one of ``"ok"``, ``"warn"`` and ``"compact"`` (log-only
    stages) or ``"block"`` (the task must pause). ``reason`` is a short
    human string naming the percentage and numbers, or ``None`` when ``ok``.
    """

    level: str
    used: int
    cap: int
    reason: str | None

    @property
    def allowed(self) -> bool:
        """False only at the ``block`` stage."""
        return self.level != "block"


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
        files_read: int = 0,
        source: str = "ai-company-cli",
        session_id: str = "",
        event_id: str = "",
        cache_read: int = 0,
        cache_write: int = 0,
        cost_source: str = "computed",
        shadow_cost_usd: float = 0.0,
        metadata: dict[str, Any] | None = None,
        timestamp: str | None = None,
    ) -> int:
        """Record a single LLM usage event.

        ``shadow_cost_usd`` is the list-price economic burn (tokens x
        ``SHADOW_COSTS`` rates, see
        :meth:`CostTracker._calculate_shadow_cost`); it is persisted in
        ``cost_records.shadow_cost_usd`` so it survives without JSON.

        Returns the row ID of the inserted record, or 0 if ``event_id``
        was already present (idempotent insert-or-ignore).
        """
        ts = timestamp or datetime.now(timezone.utc).isoformat()
        if event_id:
            existing = self._db.fetchone(
                "SELECT id FROM cost_records WHERE event_id = ? LIMIT 1", (event_id,)
            )
            if existing is not None:
                return 0
        # Insert; concurrent duplicate event_id inserts race the SELECT above.
        # Catch the UNIQUE violation so the loser is a no-op (returns 0),
        # same as the SELECT-hit path. NULL event_ids (empty here) never
        # conflict under SQLite UNIQUE semantics, so only swallow when a
        # real event_id was supplied; otherwise re-raise.
        try:
            cursor = self._db.execute(
                """INSERT INTO cost_records
                   (timestamp, model, provider, agent_name, task_id,
                    prompt_tokens, completion_tokens, cost_usd, iteration,
                    files_read, source, session_id, event_id,
                    cache_read, cache_write, cost_source, shadow_cost_usd, metadata)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    ts,
                    model,
                    provider,
                    agent_name,
                    task_id,
                    prompt_tokens,
                    completion_tokens,
                    cost_usd,
                    iteration,
                    files_read,
                    source,
                    session_id,
                    event_id or None,
                    cache_read,
                    cache_write,
                    cost_source,
                    shadow_cost_usd,
                    json.dumps(metadata or {}, default=str),
                ),
            )
            self._db.commit()
        except sqlite3.IntegrityError:
            if event_id:
                self._db.rollback()
                return 0
            raise
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

    # ── Cache-read budget (OpenCode usage DB) ─────────────────────────

    def check_cache_budget(
        self, day: str | None = None, cap: int | None = None
    ) -> CacheBudgetStatus:
        """Report cache-read token pressure for *day* against *cap*.

        The number comes from the OpenCode usage DB via
        :func:`ai_company.llm.opencode_usage.cache_read_tokens_for_day` —
        never from ``self._db`` (``cost_records`` holds per-call spend, not
        the Desktop session cache counters).

        Thresholds are evaluated highest first so every stage is reachable:
        ``>= cap`` blocks, ``>= 85%`` is ``compact``, ``>= 70%`` is ``warn``,
        everything else is ``ok``. ``compact``/``warn`` are log-only.
        """
        target_day = day or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        effective_cap = DEFAULT_CACHE_READ_CAP if cap is None else int(cap)
        if effective_cap <= 0:
            # A non-positive cap carries no budget; never block on it.
            return CacheBudgetStatus(level="ok", used=0, cap=0, reason=None)
        # Lazily imported: ``ai_company.llm`` imports ``cost_tracker``, which
        # imports this module — a module-level import would close that cycle.
        from ai_company.llm.opencode_usage import cache_read_tokens_for_day

        used = int(cache_read_tokens_for_day(target_day))
        pct = used * 100 / effective_cap
        detail = f"cache-read {pct:.1f}% of cap ({used:,}/{effective_cap:,} tokens)"
        if used >= effective_cap:
            return CacheBudgetStatus(
                level="block",
                used=used,
                cap=effective_cap,
                reason=f"{detail} — daily cap reached, task paused",
            )
        if used >= effective_cap * 85 // 100:
            return CacheBudgetStatus(
                level="compact",
                used=used,
                cap=effective_cap,
                reason=f"{detail} — compaction advised",
            )
        if used >= effective_cap * 70 // 100:
            return CacheBudgetStatus(level="warn", used=used, cap=effective_cap, reason=detail)
        return CacheBudgetStatus(level="ok", used=used, cap=effective_cap, reason=None)

    def get_runaway_sessions(self, threshold: int = DEFAULT_CACHE_READ_CAP) -> list[dict[str, Any]]:
        """Return Desktop sessions whose cache-read tokens exceed *threshold*.

        DB work is delegated to
        :func:`ai_company.llm.opencode_usage.sessions_exceeding_cache_read`;
        results are ordered by cache-read tokens descending.
        """
        from ai_company.llm.opencode_usage import sessions_exceeding_cache_read

        return sessions_exceeding_cache_read(int(threshold))

    def suspension_report(self, threshold: int = DEFAULT_CACHE_READ_CAP) -> str:
        """Plain-text report of sessions over the cache-read *threshold*.

        Values are read by key (never positional), so a legacy session row
        without suspension columns still renders. A zero-cost session prints
        ``cost: $0.0000`` and its separator like any other — no row is ever
        dropped from the report.
        """
        sessions = self.get_runaway_sessions(threshold)
        separator = "-" * 66
        lines = [
            f"Cache-read suspension report (threshold: {int(threshold):,} tokens)",
            f"Sessions exceeding threshold: {len(sessions)}",
            separator,
        ]
        if not sessions:
            lines.append("No session exceeds the cache-read threshold.")
            return "\n".join(lines)
        for rec in sessions:
            raw_cost = rec.get("cost")
            cost_value = float(raw_cost) if raw_cost is not None else 0.0
            lines.extend(
                [
                    f"session: {rec.get('session_id') or 'unknown'}",
                    f"  cache_read: {int(rec.get('tokens_cache_read') or 0):,}",
                    f"  cost: ${cost_value:.4f}",
                    f"  agent: {rec.get('agent') or 'unknown'}"
                    f"  model: {rec.get('model') or 'unknown'}",
                    f"  created: {rec.get('time_created')}"
                    f"  suspended: {rec.get('time_suspended')}"
                    f"  resume_attempts: {rec.get('resume_attempts')}"
                    f"  idle_outcome: {rec.get('idle_outcome')}",
                    separator,
                ]
            )
        return "\n".join(lines)

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
            "by_model": {
                r["model"]: {
                    "cost_usd": round(r["cost_usd"], 6),
                    "prompt_tokens": r["prompt_tokens"],
                    "completion_tokens": r["completion_tokens"],
                    "calls": r["calls"],
                }
                for r in rows
            },
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

    def breakdown_by_source(self, days: int = 30) -> list[dict[str, Any]]:
        """Cost breakdown by source over the last *days* days."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        return self._db.fetchall(
            """SELECT source,
                      SUM(cost_usd) as cost_usd,
                      SUM(prompt_tokens) as prompt_tokens,
                      SUM(completion_tokens) as completion_tokens,
                      COUNT(*) as calls
               FROM cost_records
               WHERE timestamp >= ?
               GROUP BY source
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

        Idempotent: records that already exist in the database are skipped
        so re-running the backfill never double-counts LLM spend. Records
        with a non-empty ``event_id`` are deduplicated on ``event_id``
        alone (unique index); records without one fall back to the
        composite (timestamp, model, provider, agent, task, tokens, cost)
        match among event-less rows only.

        All unified fields (``files_read``, ``source``, ``session_id``,
        ``event_id``, ``cache_read``, ``cache_write``, ``cost_source``,
        ``shadow_cost_usd``) are preserved through the import. Records
        without a stored shadow value import as ``0.0``; the v7 backfill
        recomputes them via ``CostTracker._calculate_shadow_cost``.

        Returns the number of records imported.
        """
        path = Path(jsonl_path)
        if not path.exists():
            logger.warning("Legacy cost log not found: %s", path)
            return 0

        def _int(value: Any, fallback: int) -> int:
            if value is None:
                return fallback
            try:
                return int(value)
            except (TypeError, ValueError):
                return fallback

        count = 0
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    if not isinstance(rec, dict):
                        continue
                    timestamp = rec.get("timestamp")
                    cost_usd = rec.get("cost_usd", 0.0)
                    if cost_usd is None:
                        cost_usd = 0.0
                    shadow_raw = rec.get("shadow_cost_usd", 0.0)
                    if shadow_raw is None or shadow_raw == "":
                        shadow_cost_usd = 0.0
                    else:
                        try:
                            shadow_cost_usd = float(shadow_raw)
                        except (TypeError, ValueError):
                            shadow_cost_usd = 0.0
                    model = rec.get("model") or ""
                    provider = rec.get("provider") or ""
                    agent_name = rec.get("agent_name") or ""
                    task_id = rec.get("task_id") or ""
                    prompt_tokens = _int(rec.get("prompt_tokens", 0) or 0, 0)
                    completion_tokens = _int(rec.get("completion_tokens", 0) or 0, 0)
                    event_id = str(rec.get("event_id") or "")
                    raw_metadata = rec.get("metadata", {})
                    if isinstance(raw_metadata, str):
                        try:
                            parsed = json.loads(raw_metadata) if raw_metadata else {}
                            metadata: dict[str, Any] = parsed if isinstance(parsed, dict) else {}
                        except json.JSONDecodeError:
                            metadata = {}
                    elif isinstance(raw_metadata, dict):
                        metadata = raw_metadata
                    else:
                        metadata = {}
                    if self._record_exists(
                        timestamp=timestamp,
                        model=model,
                        provider=provider,
                        agent_name=agent_name,
                        task_id=task_id,
                        cost_usd=cost_usd,
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                        event_id=event_id,
                    ):
                        continue
                    row_id = self.record_usage(
                        model=model,
                        provider=provider,
                        agent_name=agent_name,
                        task_id=task_id,
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                        cost_usd=cost_usd,
                        iteration=_int(rec.get("iteration") or 1, 1),
                        files_read=_int(rec.get("files_read") or 0, 0),
                        source=str(rec.get("source") or "ai-company-cli"),
                        session_id=str(rec.get("session_id") or ""),
                        event_id=event_id,
                        cache_read=_int(rec.get("cache_read") or 0, 0),
                        cache_write=_int(rec.get("cache_write") or 0, 0),
                        cost_source=str(rec.get("cost_source") or "computed"),
                        shadow_cost_usd=shadow_cost_usd,
                        metadata=metadata,
                        timestamp=timestamp,
                    )
                    if row_id:
                        count += 1
                except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                    continue

        logger.info("Imported %d cost records from %s", count, path)
        return count

    def _record_exists(
        self,
        *,
        timestamp: str | None,
        model: str,
        provider: str,
        agent_name: str,
        task_id: str,
        cost_usd: float,
        prompt_tokens: int,
        completion_tokens: int,
        event_id: str = "",
    ) -> bool:
        """Return True if an identical cost record already exists."""
        if event_id:
            rows = self._db.fetchall(
                "SELECT 1 FROM cost_records WHERE event_id = ? LIMIT 1",
                (event_id,),
            )
            return bool(rows)
        rows = self._db.fetchall(
            """SELECT 1 FROM cost_records
               WHERE timestamp = ? AND model = ? AND provider = ?
                 AND agent_name = ? AND task_id = ?
                 AND cost_usd = ? AND prompt_tokens = ? AND completion_tokens = ?
                 AND (event_id IS NULL OR event_id = '')
               LIMIT 1""",
            (
                timestamp,
                model,
                provider,
                agent_name,
                task_id,
                cost_usd,
                prompt_tokens,
                completion_tokens,
            ),
        )
        return bool(rows)

    # ── Stats ─────────────────────────────────────────────────────────

    def total_records(self) -> int:
        """Total number of cost records."""
        return self._db.table_count("cost_records")

    def total_cost(self) -> float:
        """Total cost across all records."""
        row = self._db.fetchone("SELECT COALESCE(SUM(cost_usd), 0) as total FROM cost_records")
        return row["total"] if row else 0.0

    # ── Export ────────────────────────────────────────────────────────

    def export_to_jsonl(self, jsonl_path: str | Path) -> Path:
        """Export all cost records to the legacy ``cost_log.jsonl`` format.

        Preserves all unified fields (``files_read``, ``source``,
        ``session_id``, ``event_id``, ``cache_read``, ``cache_write``,
        ``cost_source``, ``shadow_cost_usd``) so a round trip through
        :meth:`import_from_jsonl` is lossless for everything the SQLite
        schema can store.

        Returns the path of the written file.
        """
        path = Path(jsonl_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        rows = self._db.fetchall("SELECT * FROM cost_records ORDER BY timestamp ASC")

        with open(path, "w", encoding="utf-8") as f:
            for row in rows:
                raw_meta = row.get("metadata")
                if isinstance(raw_meta, str) and raw_meta:
                    try:
                        parsed = json.loads(raw_meta)
                        metadata: dict[str, Any] = parsed if isinstance(parsed, dict) else {}
                    except json.JSONDecodeError:
                        metadata = {}
                elif isinstance(raw_meta, dict):
                    metadata = raw_meta
                else:
                    metadata = {}
                record = {
                    "timestamp": row["timestamp"],
                    "model": row["model"],
                    "provider": row["provider"],
                    "agent_name": row["agent_name"],
                    "task_id": row["task_id"],
                    "prompt_tokens": row["prompt_tokens"],
                    "completion_tokens": row["completion_tokens"],
                    "cost_usd": row["cost_usd"],
                    "iteration": row.get("iteration") or 1,
                    "files_read": row.get("files_read") or 0,
                    "source": row.get("source") or "ai-company-cli",
                    "session_id": row.get("session_id") or "",
                    "event_id": row.get("event_id") or "",
                    "cache_read": row.get("cache_read") or 0,
                    "cache_write": row.get("cache_write") or 0,
                    "cost_source": row.get("cost_source") or "computed",
                    "shadow_cost_usd": row.get("shadow_cost_usd") or 0.0,
                    "metadata": metadata,
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
