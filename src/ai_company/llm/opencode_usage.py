"""OpenCode Desktop usage reader.

Read-only importer for OpenCode Desktop sessions stored in
``~/.local/share/opencode/opencode.db``. Maps Desktop token usage to
canonical ``CostAnalytics`` records (source=opencode-desktop) so CLI
and Desktop reporting share one truthful store.

Only real sessions are ever read. No request bodies are logged, no
secrets are read (auth.json is never opened). Re-running is idempotent
via ``event_id`` dedup in the consumer.
"""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

logger = logging.getLogger(__name__)


def default_opencode_db_path() -> Path:
    """Return the default OpenCode Desktop SQLite path."""
    return Path.home() / ".local" / "share" / "opencode" / "opencode.db"


def _resolve_db_path(db_path: str | Path | None) -> Path:
    return Path(db_path) if db_path else default_opencode_db_path()


def _parse_model(model_json: Any) -> tuple[str, str]:
    """Parse Desktop ``model`` JSON (``{"id","providerID"}``) to (model, provider)."""
    if isinstance(model_json, dict):
        model = str(model_json.get("id") or "")
        provider = str(model_json.get("providerID") or "")
        return model, provider
    if isinstance(model_json, str):
        try:
            data = json.loads(model_json)
            if isinstance(data, dict):
                return (
                    str(data.get("id") or ""),
                    str(data.get("providerID") or ""),
                )
        except (json.JSONDecodeError, TypeError):
            pass
        return model_json, ""
    return "", ""


def _iso_from_ms(ms: Any) -> str:
    """Convert Desktop millisecond timestamp to UTC ISO string."""
    try:
        return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OverflowError):
        return datetime.now(timezone.utc).isoformat()


def _num(value: Any) -> int:
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def _recompute_cost(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
) -> tuple[float, str]:
    """Recompute cost via existing ``MODEL_COSTS``.

    Returns ``(cost_usd, cost_source)`` where ``cost_source`` is
    ``provider`` when ``model`` resolves to the free/known table with
    0.0 rates, else ``recomputed`` / ``recomputed-default``.
    """
    from ai_company.llm.cost_tracker import MODEL_COSTS, _cost_per_token

    if model in MODEL_COSTS:
        cost = prompt_tokens * _cost_per_token(
            model, "input"
        ) + completion_tokens * _cost_per_token(model, "output")
        return round(cost, 8), "recomputed"
    cost = prompt_tokens * _cost_per_token(model, "input") + completion_tokens * _cost_per_token(
        model, "output"
    )
    return round(cost, 8), "recomputed-default"


def normalize_session_row(
    *,
    session_id: str,
    agent: str,
    model_raw: Any,
    tokens_input: int,
    tokens_output: int,
    tokens_reasoning: int,
    tokens_cache_read: int,
    tokens_cache_write: int,
    raw_cost: float,
    time_created: Any,
) -> dict[str, Any] | None:
    """Normalize one Desktop session aggregate to a canonical record.

    ``prompt = input + cache_write`` (cache reads are cheap and kept
    separate), ``completion = output + reasoning``. Returns ``None``
    for zero-token / free sessions with no usage (APIError rows are
    never zero-filled).
    """
    prompt = _num(tokens_input) + _num(tokens_cache_write)
    completion = _num(tokens_output) + _num(tokens_reasoning)
    if prompt == 0 and completion == 0:
        return None
    model, provider = _parse_model(model_raw)
    if not model:
        return None
    if float(raw_cost or 0.0) > 0:
        cost = float(raw_cost)
        cost_source = "provider"
    else:
        cost, cost_source = _recompute_cost(model, prompt, completion)
    return {
        "model": model,
        "provider": provider or "opencode",
        "agent_name": (agent or "desktop") if agent else "desktop",
        "task_id": session_id,
        "prompt_tokens": prompt,
        "completion_tokens": completion,
        "cost_usd": cost,
        "iteration": 1,
        "files_read": 0,
        "source": "opencode-desktop",
        "session_id": session_id,
        "event_id": f"ses_{session_id}",
        "cache_read": _num(tokens_cache_read),
        "cache_write": _num(tokens_cache_write),
        "cost_source": cost_source,
        "metadata": {"raw_cost": float(raw_cost or 0.0)},
        "timestamp": _iso_from_ms(time_created),
    }


def iter_opencode_sessions(
    db_path: str | Path | None = None,
    project: str | None = None,
    since: str | None = None,
    limit: int = 500,
) -> Iterator[dict[str, Any]]:
    """Yield canonical records for Desktop sessions, read-only.

    Unions the legacy ``session`` table and ``session_v2`` (same
    shape, v2 adds extra columns). Uses ``mode=ro`` so the live
    Desktop WAL is never written or locked.
    """
    path = _resolve_db_path(db_path)
    if not path.exists():
        logger.warning("OpenCode DB not found: %s", path)
        return
    uri = f"file:{path.as_posix()}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True, timeout=5)
        conn.row_factory = sqlite3.Row
    except sqlite3.Error:
        logger.warning("Could not open OpenCode DB read-only: %s", path)
        return
    try:
        tables = {
            row["name"]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        }
        # ``limit`` is a global cap across both tables (and a negative
        # SQLite LIMIT means "no limit", so reject non-positive values).
        if int(limit) <= 0:
            return
        seen: set[str] = set()
        yielded = 0
        for table in ("session_v2", "session"):
            if table not in tables:
                continue
            cols = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
            if not {"tokens_input", "tokens_output"}.issubset(cols):
                continue
            query = f"""SELECT id, directory, agent, model,
                tokens_input, tokens_output, tokens_reasoning,
                tokens_cache_read, tokens_cache_write, cost,
                time_created, time_updated
                FROM {table}"""
            clauses: list[str] = []
            params: list[Any] = []
            if project:
                clauses.append("directory LIKE ?")
                params.append(f"%{project}%")
            if since:
                try:
                    since_ms = int(
                        datetime.fromisoformat(since).replace(tzinfo=timezone.utc).timestamp()
                        * 1000
                    )
                except (ValueError, TypeError):
                    since_ms = None
                if since_ms is not None:
                    clauses.append("time_created >= ?")
                    params.append(since_ms)
            if clauses:
                query += " WHERE " + " AND ".join(clauses)
            query += " ORDER BY time_created DESC LIMIT ?"
            params.append(int(limit) - yielded)
            for row in conn.execute(query, tuple(params)).fetchall():
                rec = normalize_session_row(
                    session_id=str(row["id"]),
                    agent=str(row["agent"] or ""),
                    model_raw=row["model"],
                    tokens_input=_num(row["tokens_input"]),
                    tokens_output=_num(row["tokens_output"]),
                    tokens_reasoning=_num(row["tokens_reasoning"]),
                    tokens_cache_read=_num(row["tokens_cache_read"]),
                    tokens_cache_write=_num(row["tokens_cache_write"]),
                    raw_cost=float(row["cost"] or 0.0),
                    time_created=row["time_created"],
                )
                if rec is not None and rec["event_id"] not in seen:
                    seen.add(rec["event_id"])
                    yielded += 1
                    yield rec
                    if yielded >= int(limit):
                        return
    finally:
        conn.close()


def count_opencode_sessions(
    db_path: str | Path | None = None,
    project: str | None = None,
) -> int:
    """Count candidate Desktop sessions without reading bodies (diagnostic)."""
    return sum(1 for _ in iter_opencode_sessions(db_path, project=project, limit=10000))
