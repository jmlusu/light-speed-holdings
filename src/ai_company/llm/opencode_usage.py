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
from datetime import datetime, timedelta, timezone
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
    # Shadow is always tokens x list rates, independent of cost_source.
    shadow_cost = _recompute_shadow_cost(model, prompt, completion)
    message_metadata: dict[str, Any] = {"raw_cost": raw_cost}
    if _shadow_rate_flag(model) == "shadow-default":
        message_metadata["shadow_cost_source"] = "shadow-default"
    return {
        "model": model,
        "provider": provider or "opencode",
        "agent_name": (str(parsed.get("agent") or "") or session_agent or "desktop") or "desktop",
        "task_id": session_id,
        "prompt_tokens": prompt,
        "completion_tokens": completion,
        "cost_usd": cost,
        "shadow_cost_usd": shadow_cost,
        "iteration": 1,
        "files_read": max(0, int(files_read)),
        "source": "opencode-desktop",
        "session_id": session_id,
        "event_id": f"msg_{message_id}",
        "cache_read": _num(cache.get("read")),
        "cache_write": _num(cache.get("write")),
        "cost_source": cost_source,
        "metadata": message_metadata,
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


def _recompute_shadow_cost(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
) -> float:
    """Recompute list-price shadow cost via ``SHADOW_COSTS``.

    Always tokens x list rates, independent of ``cost_source`` (provider
    vs recomputed) — see :func:`ai_company.llm.cost_tracker._shadow_cost`.
    """
    from ai_company.llm.cost_tracker import _shadow_cost

    return _shadow_cost(model, prompt_tokens, completion_tokens)


def _shadow_rate_flag(model: str) -> str:
    """Return the shadow rate source for *model* (``shadow-default`` flags estimates)."""
    from ai_company.llm.cost_tracker import _shadow_rate_source

    return _shadow_rate_source(model)


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
    # Shadow is always tokens x list rates, independent of cost_source.
    shadow_cost = _recompute_shadow_cost(model, prompt, completion)
    session_metadata: dict[str, Any] = {"raw_cost": float(raw_cost or 0.0)}
    if _shadow_rate_flag(model) == "shadow-default":
        session_metadata["shadow_cost_source"] = "shadow-default"
    return {
        "model": model,
        "provider": provider or "opencode",
        "agent_name": (agent or "desktop") if agent else "desktop",
        "task_id": session_id,
        "prompt_tokens": prompt,
        "completion_tokens": completion,
        "cost_usd": cost,
        "shadow_cost_usd": shadow_cost,
        "iteration": 1,
        "files_read": 0,
        "source": "opencode-desktop",
        "session_id": session_id,
        "event_id": f"ses_{session_id}",
        "cache_read": _num(tokens_cache_read),
        "cache_write": _num(tokens_cache_write),
        "cost_source": cost_source,
        "metadata": session_metadata,
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


# ---------------------------------------------------------------------------
# Read-only cache-read budget readers
# ---------------------------------------------------------------------------
#
# These power the daily cache-read token cap. They are strictly read-only
# (``mode=ro``) and fail soft: a missing or unreadable DB yields zeros/[] so a
# metrics problem can never abort task execution.

# Message tables in priority order. Both names may coexist in one DB (the
# Desktop store keeps ``message`` for older rows and ``session_message`` for
# newer ones), so callers union them and dedupe by message id.
_MESSAGE_TABLES = ("message", "session_message")

# Session tables: ``session_v2`` carries the suspension columns, ``session``
# is the legacy shape without them.
_SESSION_TABLES = ("session_v2", "session")

_SESSION_FIELDS = (
    "id",
    "tokens_cache_read",
    "time_created",
    "time_suspended",
    "resume_attempts",
    "idle_outcome",
    "cost",
    "agent",
    "model",
)


def _connect_readonly(db_path: str | Path | None) -> sqlite3.Connection | None:
    """Open the usage DB read-only, or ``None`` when it is unavailable."""
    path = _resolve_db_path(db_path)
    if not path.exists():
        logger.warning("OpenCode DB not found: %s", path)
        return None
    uri = f"file:{path.as_posix()}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True, timeout=5)
    except sqlite3.Error:
        logger.warning("Could not open OpenCode DB read-only: %s", path)
        return None
    conn.row_factory = sqlite3.Row
    return conn


def _table_columns(conn: sqlite3.Connection) -> dict[str, set[str]]:
    """Return ``{table_name: {column, ...}}`` for the connected DB."""
    tables = [
        str(row["name"])
        for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    ]
    return {
        table: {str(col["name"]) for col in conn.execute(f"PRAGMA table_info({table})")}
        for table in tables
    }


def _day_bounds_ms(day: str) -> tuple[int, int] | None:
    """Return the UTC ``[start, end)`` millisecond bounds for ``YYYY-MM-DD``."""
    try:
        start = datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        logger.warning("Invalid day %r for cache-read totals", day)
        return None
    return int(start.timestamp() * 1000), int((start + timedelta(days=1)).timestamp() * 1000)


def cache_read_tokens_for_day(day: str, db_path: str | Path | None = None) -> int:
    """Sum ``tokens.cache.read`` for messages created on *day* (UTC).

    *day* is ``"YYYY-MM-DD"``. Both the ``message`` and ``session_message``
    tables are read (a Desktop DB keeps one or the other per row range) and
    rows are deduped by message id, so a DB that mirrors both table names is
    never double counted. Rows whose ``data`` JSON lacks
    ``tokens.cache.read`` contribute 0.

    Returns 0 for a missing/unreadable DB or an unparsable *day*; never raises.
    """
    bounds = _day_bounds_ms(day)
    if bounds is None:
        return 0
    start_ms, end_ms = bounds
    conn = _connect_readonly(db_path)
    if conn is None:
        return 0
    total = 0
    seen: set[str] = set()
    try:
        columns_by_table = _table_columns(conn)
        for table in _MESSAGE_TABLES:
            table_columns = columns_by_table.get(table)
            if not table_columns or not {"id", "time_created", "data"}.issubset(table_columns):
                continue
            try:
                rows = conn.execute(
                    f"SELECT id, data FROM {table} WHERE time_created >= ? AND time_created < ?",
                    (start_ms, end_ms),
                ).fetchall()
            except sqlite3.Error:
                logger.warning("Cache-read query failed on %s", table)
                continue
            for row in rows:
                message_id = str(row["id"])
                if message_id in seen:
                    continue
                seen.add(message_id)
                tokens = _parse_json(row["data"]).get("tokens")
                if not isinstance(tokens, dict):
                    continue
                cache = tokens.get("cache")
                if not isinstance(cache, dict):
                    continue
                total += _num(cache.get("read"))
    except sqlite3.Error:
        logger.warning("Cache-read totals unavailable for %s", day)
        return 0
    finally:
        conn.close()
    return total


def sessions_exceeding_cache_read(
    threshold: int, db_path: str | Path | None = None
) -> list[dict[str, Any]]:
    """Return sessions whose ``tokens_cache_read`` exceeds *threshold*.

    Unions ``session_v2`` (which has the suspension columns) and the legacy
    ``session`` table, deduping by session id so ``session_v2`` fields win.
    Columns absent from a table resolve to ``None``/``0`` — value access is
    by key only, never positional.

    Each dict has ``session_id``, ``tokens_cache_read``, ``time_created``,
    ``time_suspended``, ``resume_attempts``, ``idle_outcome``, ``cost``,
    ``agent``, ``model``; the list is ordered by cache-read tokens
    descending. Returns ``[]`` for a missing/unreadable DB; never raises.
    """
    conn = _connect_readonly(db_path)
    if conn is None:
        return []
    rows: list[dict[str, Any]] = []
    try:
        threshold_value = int(threshold)
    except (TypeError, ValueError):
        conn.close()
        logger.warning("Invalid cache-read threshold %r", threshold)
        return []
    seen: set[str] = set()
    try:
        columns_by_table = _table_columns(conn)
        for table in _SESSION_TABLES:
            available = columns_by_table.get(table)
            if not available or not {"id", "tokens_cache_read"}.issubset(available):
                continue
            selected = [field for field in _SESSION_FIELDS if field in available]
            try:
                table_rows = conn.execute(
                    f"SELECT {', '.join(selected)} FROM {table} WHERE tokens_cache_read > ?",
                    (threshold_value,),
                ).fetchall()
            except sqlite3.Error:
                logger.warning("Cache-read session query failed on %s", table)
                continue
            for raw in table_rows:
                rec = dict(raw)
                session_id = str(rec.get("id") or "")
                if not session_id or session_id in seen:
                    continue
                seen.add(session_id)
                model, _provider = _parse_model(rec.get("model"))
                rows.append(
                    {
                        "session_id": session_id,
                        "tokens_cache_read": _num(rec.get("tokens_cache_read")),
                        "time_created": rec.get("time_created"),
                        "time_suspended": rec.get("time_suspended"),
                        "resume_attempts": _num(rec.get("resume_attempts")),
                        "idle_outcome": rec.get("idle_outcome"),
                        "cost": _float(rec.get("cost")),
                        "agent": str(rec.get("agent") or ""),
                        "model": model,
                    }
                )
    except sqlite3.Error:
        logger.warning("Cache-read session lookup unavailable")
        return []
    finally:
        conn.close()
    rows.sort(key=lambda entry: int(entry["tokens_cache_read"]), reverse=True)
    return rows
