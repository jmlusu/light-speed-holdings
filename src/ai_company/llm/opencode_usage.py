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
    """Convert Desktop millisecond timestamp to UTC ISO string.

    Falls back to *now* (UTC) when the stored value is missing or
    unparsable so a single corrupt row cannot abort the import — the
    fallback always logs a warning so skewed timestamps stay visible.
    """
    try:
        return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OverflowError):
        logger.warning("Invalid Desktop timestamp %r; falling back to now", ms)
        return datetime.now(timezone.utc).isoformat()


def _num(value: Any) -> int:
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def _float(value: Any) -> float:
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _parse_json(data: Any) -> dict[str, Any]:
    """Parse a Desktop ``data`` JSON blob into a dict (``{}`` on failure)."""
    if isinstance(data, dict):
        return dict(data)
    if isinstance(data, str):
        try:
            parsed = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _message_model(data: dict[str, Any]) -> tuple[str, str]:
    """Extract (model, provider) from a message ``data`` payload.

    Assistant messages carry flat ``modelID``/``providerID``; user and
    legacy payloads nest ``model: {id|modelID, providerID}``. Both shapes
    are accepted; missing pieces resolve to ``""``.
    """
    model = str(data.get("modelID") or "")
    provider = str(data.get("providerID") or "")
    nested = data.get("model")
    if isinstance(nested, dict):
        model = model or str(nested.get("id") or nested.get("modelID") or "")
        provider = provider or str(nested.get("providerID") or "")
    elif isinstance(nested, str) and not model:
        return _parse_model(nested)
    if not provider:
        provider = str(data.get("provider") or "")
    return model, provider


def normalize_message_row(
    *,
    message_id: str,
    session_id: str,
    session_agent: str,
    data: Any,
    files_read: int,
    time_created: Any,
) -> dict[str, Any] | None:
    """Normalize one Desktop message turn to a canonical record (P3).

    ``prompt = input + cache_write`` and ``completion = output +
    reasoning`` — the same split as :func:`normalize_session_row` so
    message-grain and session-grain totals reconcile. ``files_read`` is
    counted from ``part.tool == read`` rows for this message by the
    caller. Returns ``None`` for zero-token / free sessions with no usage
    (user turns and APIError rows are never zero-filled).
    """
    parsed = _parse_json(data)
    tokens_raw = parsed.get("tokens")
    tokens: dict[str, Any] = tokens_raw if isinstance(tokens_raw, dict) else {}
    cache_raw = tokens.get("cache")
    cache: dict[str, Any] = cache_raw if isinstance(cache_raw, dict) else {}
    prompt = _num(tokens.get("input")) + _num(cache.get("write"))
    completion = _num(tokens.get("output")) + _num(tokens.get("reasoning"))
    if prompt == 0 and completion == 0:
        return None
    model, provider = _message_model(parsed)
    if not model:
        return None
    raw_cost = _float(parsed.get("cost"))
    if raw_cost > 0:
        cost = raw_cost
        cost_source = "provider"
    else:
        cost, cost_source = _recompute_cost(model, prompt, completion)
    return {
        "model": model,
        "provider": provider or "opencode",
        "agent_name": (str(parsed.get("agent") or "") or session_agent or "desktop") or "desktop",
        "task_id": session_id,
        "prompt_tokens": prompt,
        "completion_tokens": completion,
        "cost_usd": cost,
        "iteration": 1,
        "files_read": max(0, int(files_read)),
        "source": "opencode-desktop",
        "session_id": session_id,
        "event_id": f"msg_{message_id}",
        "cache_read": _num(cache.get("read")),
        "cache_write": _num(cache.get("write")),
        "cost_source": cost_source,
        "metadata": {"raw_cost": raw_cost},
        "timestamp": _iso_from_ms(time_created),
    }


def _files_read_by_message(
    conn: sqlite3.Connection,
    part_table: str,
    message_ids: list[str],
) -> dict[str, int]:
    """Count ``part.tool == read`` rows per message id (P3).

    Returns ``{}`` when the count query cannot run (e.g. a test DB without
    ``json_extract``); callers then record ``files_read=0`` rather than
    fabricating a read count.
    """
    if not message_ids:
        return {}
    placeholders = ",".join("?" for _ in message_ids)
    try:
        if part_table == "session_part":
            sql = (
                f"SELECT message_id, COUNT(*) AS c FROM {part_table} "
                f"WHERE message_id IN ({placeholders}) AND type = 'tool' "
                f"AND json_extract(data, '$.tool') = 'read' GROUP BY message_id"
            )
        else:
            sql = (
                f"SELECT message_id, COUNT(*) AS c FROM {part_table} "
                f"WHERE message_id IN ({placeholders}) "
                f"AND json_extract(data, '$.type') = 'tool' "
                f"AND json_extract(data, '$.tool') = 'read' GROUP BY message_id"
            )
        rows = conn.execute(sql, tuple(message_ids)).fetchall()
        return {str(r["message_id"]): int(r["c"]) for r in rows}
    except sqlite3.Error:
        logger.warning("files_read count query failed on %s", part_table)
        return {}


def _recompute_cost(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
) -> tuple[float, str]:
    """Recompute cost via existing ``MODEL_COSTS``.

    Returns ``(cost_usd, cost_source)`` with explicit values:

    - ``recomputed`` — ``model`` is listed in ``MODEL_COSTS`` (including
      free-tier entries priced at 0.0, which yield ``0.0`` here).
    - ``recomputed-default`` — ``model`` is unknown and was priced from
      the ``_default`` entry.

    ``provider`` is never returned here; it is reserved for costs the
    Desktop store reports directly (``raw_cost > 0``) in
    :func:`normalize_session_row` / :func:`normalize_message_row`.
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


def _iter_message_records(
    conn: sqlite3.Connection,
    message_table: str,
    part_table: str,
    session_id: str,
    session_agent: str,
    since_ms: int | None,
) -> Iterator[dict[str, Any]]:
    """Yield message-grain records for one session (P3).

    One record per assistant message with non-zero tokens
    (``event_id=msg_<id>``). Zero-token turns are skipped, matching the
    session-grain rule that only real usage is imported.
    """
    query = f"SELECT id, time_created, data FROM {message_table} WHERE session_id = ?"
    params: list[Any] = [session_id]
    if since_ms is not None:
        query += " AND time_created >= ?"
        params.append(since_ms)
    query += " ORDER BY time_created ASC"
    try:
        rows = conn.execute(query, tuple(params)).fetchall()
    except sqlite3.Error:
        logger.warning("Message lookup failed on %s for %s", message_table, session_id)
        return
    message_ids = [str(r["id"]) for r in rows]
    files_by_message = _files_read_by_message(conn, part_table, message_ids)
    for row in rows:
        rec = normalize_message_row(
            message_id=str(row["id"]),
            session_id=session_id,
            session_agent=session_agent,
            data=row["data"],
            files_read=files_by_message.get(str(row["id"]), 0),
            time_created=row["time_created"],
        )
        if rec is not None:
            yield rec


def iter_opencode_sessions(
    db_path: str | Path | None = None,
    project: str | None = None,
    since: str | None = None,
    limit: int = 500,
    message_granular: bool = True,
) -> Iterator[dict[str, Any]]:
    """Yield canonical records for Desktop sessions, read-only.

    Unions the legacy ``session`` table and ``session_v2`` (same
    shape, v2 adds extra columns). Uses ``mode=ro`` so the live
    Desktop WAL is never written or locked.

    When ``message_granular`` is set and ``message``/``session_message``
    plus ``part``/``session_part`` tables are available (P3), yields one
    record per token-bearing message turn (``event_id=msg_<id>``). Falls
    back to one session-grain record (``event_id=ses_<id>``) per session
    when message data or the part lookup is unavailable, or when a
    session has no token-bearing messages.
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
        # P3: message-grain is only used when both the message data and
        # the part (files_read) lookup exist; otherwise session-grain is
        # the sole source and existing behaviour is unchanged.
        message_table: str | None = None
        part_table: str | None = None
        if message_granular:
            for candidate in ("message", "session_message"):
                if candidate not in tables:
                    continue
                cols = {
                    row["name"]
                    for row in conn.execute(f"PRAGMA table_info({candidate})").fetchall()
                }
                if {"id", "session_id", "data", "time_created"}.issubset(cols):
                    message_table = candidate
                    break
            for candidate in ("part", "session_part"):
                if candidate not in tables:
                    continue
                cols = {
                    row["name"]
                    for row in conn.execute(f"PRAGMA table_info({candidate})").fetchall()
                }
                if {"message_id", "data"}.issubset(cols):
                    part_table = candidate
                    break
        use_messages = message_table is not None and part_table is not None
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
            since_ms: int | None = None
            if since:
                try:
                    dt = datetime.fromisoformat(since)
                    # Naive inputs are treated as UTC; offset-aware inputs
                    # keep their offset (previously ``replace`` clobbered
                    # ``+02:00``-style offsets to UTC and shifted the bound).
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    since_ms = int(dt.timestamp() * 1000)
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
                session_id = str(row["id"])
                session_agent = str(row["agent"] or "")
                session_rec = normalize_session_row(
                    session_id=session_id,
                    agent=session_agent,
                    model_raw=row["model"],
                    tokens_input=_num(row["tokens_input"]),
                    tokens_output=_num(row["tokens_output"]),
                    tokens_reasoning=_num(row["tokens_reasoning"]),
                    tokens_cache_read=_num(row["tokens_cache_read"]),
                    tokens_cache_write=_num(row["tokens_cache_write"]),
                    raw_cost=float(row["cost"] or 0.0),
                    time_created=row["time_created"],
                )
                yielded_for_session = 0
                if use_messages:
                    assert message_table is not None and part_table is not None
                    for msg_rec in _iter_message_records(
                        conn,
                        message_table,
                        part_table,
                        session_id,
                        session_agent,
                        since_ms,
                    ):
                        if msg_rec["event_id"] not in seen:
                            seen.add(msg_rec["event_id"])
                            yielded += 1
                            yielded_for_session += 1
                            yield msg_rec
                            if yielded >= int(limit):
                                return
                # Session-grain is the sole source unless message-grain
                # yielded nothing for this session (no token-bearing
                # messages), so usage is never silently dropped.
                if (
                    session_rec is not None
                    and session_rec["event_id"] not in seen
                    and (not use_messages or yielded_for_session == 0)
                ):
                    seen.add(session_rec["event_id"])
                    yielded += 1
                    yield session_rec
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
