"""Prometheus-compatible /metrics endpoint and deep health checks.

Provides:
- ``/metrics`` — Prometheus text exposition format with agent performance,
  memory usage, LLM cost breakdown, and operational counters
- ``/health`` — Deep health check with dependency, disk, and memory status
- ``/ready`` — Readiness probe (returns 200 when all deps are up)
- ``/api/v1/daemon/status`` — Executor daemon lifecycle status
"""

from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Response

from ai_company.dashboard.repository import get_state_store
from ai_company.version import get_version

logger = logging.getLogger(__name__)

router = APIRouter(tags=["monitoring"])


# GAP-011: metrics parsing reads state through the StateStore repository.
# Fetched lazily so the boot-time explicit configuration (Option B) takes
# effect for request handling rather than being frozen at import time.
def _get_store() -> Any:
    return get_state_store()


def _get_bus() -> Any:
    from ai_company.dashboard.api import get_bus

    return get_bus()


def _state_path(rel_path: str | Path) -> Path:
    """Resolve *rel_path* anchored at the StateStore root (CWD-independent).

    The dashboard state root is bound explicitly at boot (Option B) from
    ``DASHBOARD_DATA_DIR`` / the deterministic project root, so resolving
    against :attr:`StateStore.base_dir` — never ``Path(".")`` — keeps health
    checks correct no matter which directory the server was launched from
    (ticket #61).
    """
    return Path(_get_store().base_dir) / rel_path


# ---------------------------------------------------------------------------
# Metrics store (in-memory counters — reset on process restart)
# ---------------------------------------------------------------------------

_metrics: dict[str, float] = {
    # LLM metrics
    "llm_requests_total": 0,
    "llm_errors_total": 0,
    "llm_cost_usd_total": 0.0,
    "llm_cost_usd_anthropic": 0.0,
    "llm_cost_usd_openai": 0.0,
    "llm_cost_usd_deepseek": 0.0,
    "llm_cost_usd_other": 0.0,
    # Circuit breaker
    "circuit_breaker_trips_total": 0,
    "circuit_breaker_half_open_total": 0,
}

_start_time = time.time()


def inc_metric(name: str, value: float = 1.0) -> None:
    """Increment a named metric by value."""
    _metrics[name] = _metrics.get(name, 0) + value


def record_llm_cost(provider: str, cost_usd: float) -> None:
    """Record LLM cost attributed to a provider."""
    inc_metric("llm_cost_usd_total", cost_usd)
    provider_lower = provider.lower()
    if "anthropic" in provider_lower:
        inc_metric("llm_cost_usd_anthropic", cost_usd)
    elif "openai" in provider_lower:
        inc_metric("llm_cost_usd_openai", cost_usd)
    elif "deepseek" in provider_lower:
        inc_metric("llm_cost_usd_deepseek", cost_usd)
    else:
        inc_metric("llm_cost_usd_other", cost_usd)


# ---------------------------------------------------------------------------
# Prometheus text exposition format
# ---------------------------------------------------------------------------


def _render_prometheus_text() -> str:
    """Render all metrics in Prometheus text exposition format."""
    lines: list[str] = []
    now_ts = time.time()

    # Process start time gauge
    lines.append("# HELP process_start_time_seconds Process start time (unix timestamp)")
    lines.append("# TYPE process_start_time_seconds gauge")
    lines.append(f"process_start_time_seconds {_start_time:.3f}")

    # Uptime gauge
    lines.append("# HELP ai_company_uptime_seconds Dashboard uptime in seconds")
    lines.append("# TYPE ai_company_uptime_seconds gauge")
    lines.append(f"ai_company_uptime_seconds {now_ts - _start_time:.3f}")

    # ── Process / system metrics ────────────────────────────────────
    _append_process_metrics(lines)

    # ── Counter metrics ─────────────────────────────────────────────
    counter_metrics = {
        "llm_requests_total": ("ai_company_llm_requests_total", "Total LLM API requests"),
        "llm_errors_total": ("ai_company_llm_errors_total", "Total LLM API errors"),
        "circuit_breaker_trips_total": (
            "ai_company_circuit_breaker_trips_total",
            "Total circuit breaker trip events",
        ),
        "circuit_breaker_half_open_total": (
            "ai_company_circuit_breaker_half_open_total",
            "Total circuit breaker half-open transitions",
        ),
    }

    for metric_key, (prom_name, help_text) in counter_metrics.items():
        lines.append(f"# HELP {prom_name} {help_text}")
        lines.append(f"# TYPE {prom_name} counter")
        lines.append(f"{prom_name} {_metrics.get(metric_key, 0):.0f}")

    # ── LLM cost gauges (per-provider breakdown) ────────────────────
    cost_gauges = {
        "llm_cost_usd_total": (
            "ai_company_llm_cost_usd_total",
            "Total LLM cost in USD (all providers)",
        ),
        "llm_cost_usd_anthropic": (
            "ai_company_llm_cost_anthropic_usd",
            "Total LLM cost in USD (Anthropic)",
        ),
        "llm_cost_usd_openai": (
            "ai_company_llm_cost_openai_usd",
            "Total LLM cost in USD (OpenAI)",
        ),
        "llm_cost_usd_deepseek": (
            "ai_company_llm_cost_deepseek_usd",
            "Total LLM cost in USD (DeepSeek)",
        ),
        "llm_cost_usd_other": (
            "ai_company_llm_cost_other_usd",
            "Total LLM cost in USD (other providers)",
        ),
    }

    for metric_key, (prom_name, help_text) in cost_gauges.items():
        lines.append(f"# HELP {prom_name} {help_text}")
        lines.append(f"# TYPE {prom_name} gauge")
        lines.append(f"{prom_name} {_metrics.get(metric_key, 0):.6f}")

    # ── Derived gauges ──────────────────────────────────────────────
    _append_derived_metrics(lines)

    # ── Task status breakdown (from live inbox) ─────────────────────
    _append_task_status_breakdown(lines)

    # ── Agent performance breakdown (from audit log) ────────────────
    _append_agent_performance(lines)

    # ── LLM cost breakdown by model (from audit log) ────────────────
    _append_llm_model_breakdown(lines)

    return "\n".join(lines) + "\n"


def _append_process_metrics(lines: list[str]) -> None:
    """Append OS-level process metrics."""
    try:
        import resource

        usage = resource.getrusage(resource.RUSAGE_SELF)  # type: ignore[attr-defined]
        # Max RSS in bytes (Linux: bytes, macOS: bytes)
        rss_bytes = usage.ru_maxrss
        lines.append("# HELP ai_company_process_max_rss_bytes Peak resident set size in bytes")
        lines.append("# TYPE ai_company_process_max_rss_bytes gauge")
        lines.append(f"ai_company_process_max_rss_bytes {rss_bytes}")
    except (ImportError, AttributeError):
        # resource module not available on Windows
        pass

    try:
        import psutil  # type: ignore[import-untyped]

        proc = psutil.Process()
        mem_info = proc.memory_info()
        lines.append("# HELP ai_company_process_rss_bytes Current RSS in bytes")
        lines.append("# TYPE ai_company_process_rss_bytes gauge")
        lines.append(f"ai_company_process_rss_bytes {mem_info.rss}")

        lines.append("# HELP ai_company_process_vms_bytes Current VMS in bytes")
        lines.append("# TYPE ai_company_process_vms_bytes gauge")
        lines.append(f"ai_company_process_vms_bytes {mem_info.vms}")

        lines.append("# HELP ai_company_process_open_fds Number of open file descriptors")
        lines.append("# TYPE ai_company_process_open_fds gauge")
        lines.append(f"ai_company_process_open_fds {proc.num_fds()}")
    except ImportError:
        # psutil not installed
        pass
    except Exception:  # noqa: BLE001 - pragma: no cover - psutil runtime error
        pass

    # CPU times (always available via os.times)
    times = os.times()
    lines.append("# HELP ai_company_cpu_user_seconds_total User CPU time in seconds")
    lines.append("# TYPE ai_company_cpu_user_seconds_total counter")
    lines.append(f"ai_company_cpu_user_seconds_total {times[0]:.3f}")

    lines.append("# HELP ai_company_cpu_system_seconds_total System CPU time in seconds")
    lines.append("# TYPE ai_company_cpu_system_seconds_total counter")
    lines.append(f"ai_company_cpu_system_seconds_total {times[1]:.3f}")


def _append_derived_metrics(lines: list[str]) -> None:
    """Append computed / derived gauges."""
    # Task success rate (live from the MessageBus, matching _live_task_summary)
    rate = 0.0
    try:
        tasks = _get_bus().get_all_tasks_raw()
        if isinstance(tasks, list):
            total = len(tasks)
            succeeded = sum(
                1 for t in tasks if isinstance(t, dict) and t.get("status") == "completed"
            )
            rate = (succeeded / total * 100.0) if total > 0 else 0.0
    except Exception:  # noqa: BLE001 - metric collection is best-effort
        logger.debug("Failed to read live tasks for task success rate")
    lines.append("# HELP ai_company_task_success_rate_pct Task success rate as percentage")
    lines.append("# TYPE ai_company_task_success_rate_pct gauge")
    lines.append(f"ai_company_task_success_rate_pct {rate:.2f}")

    # LLM error rate
    llm_req = _metrics.get("llm_requests_total", 0)
    llm_err = _metrics.get("llm_errors_total", 0)
    llm_rate = (llm_err / llm_req * 100.0) if llm_req > 0 else 0.0
    lines.append("# HELP ai_company_llm_error_rate_pct LLM error rate as percentage")
    lines.append("# TYPE ai_company_llm_error_rate_pct gauge")
    lines.append(f"ai_company_llm_error_rate_pct {llm_rate:.2f}")

    # Average LLM cost per request
    avg_cost = _metrics.get("llm_cost_usd_total", 0.0) / llm_req if llm_req > 0 else 0.0
    lines.append(
        "# HELP ai_company_llm_avg_cost_per_request_usd Average LLM cost per request in USD"
    )
    lines.append("# TYPE ai_company_llm_avg_cost_per_request_usd gauge")
    lines.append(f"ai_company_llm_avg_cost_per_request_usd {avg_cost:.6f}")


def _append_task_status_breakdown(lines: list[str]) -> None:
    """Read live task state and emit per-status gauges (via MessageBus)."""
    try:
        tasks = _get_bus().get_all_tasks_raw()
        if tasks is None:
            return
        status_counts: dict[str, int] = {}
        for t in tasks:
            s = t.get("status", "unknown")
            status_counts[s] = status_counts.get(s, 0) + 1
        lines.append("# HELP ai_company_tasks_by_status Number of tasks by status")
        lines.append("# TYPE ai_company_tasks_by_status gauge")
        for status, count in sorted(status_counts.items()):
            lines.append(f'ai_company_tasks_by_status{{status="{status}"}} {count}')
    except Exception:  # noqa: BLE001 - metric collection is best-effort
        logger.debug("Failed to read inbox for task status breakdown")


def _append_agent_performance(lines: list[str]) -> None:
    """Parse audit log and emit per-agent task success/failure counters."""
    agent_tasks: dict[str, dict[str, int]] = {}
    try:
        for line in _get_store().iter_jsonl(".opencode/audit"):
            try:
                if line.get("event_type") != "task_complete":
                    continue
                agent_id = line.get("agent_id", "unknown")
                success = line.get("metadata", {}).get("success", True)
                if agent_id not in agent_tasks:
                    agent_tasks[agent_id] = {
                        "success": 0,
                        "failure": 0,
                    }
                if success:
                    agent_tasks[agent_id]["success"] += 1
                else:
                    agent_tasks[agent_id]["failure"] += 1
            except (TypeError, AttributeError):
                continue
    except OSError:
        return

    if agent_tasks:
        lines.append("# HELP ai_company_agent_tasks_total Tasks completed per agent")
        lines.append("# TYPE ai_company_agent_tasks_total counter")
        for agent_id, counts in sorted(agent_tasks.items()):
            total = counts["success"] + counts["failure"]
            lines.append(f'ai_company_agent_tasks_total{{agent="{agent_id}"}} {total}')

        lines.append("# HELP ai_company_agent_successes_total Successful tasks per agent")
        lines.append("# TYPE ai_company_agent_successes_total counter")
        for agent_id, counts in sorted(agent_tasks.items()):
            lines.append(
                f'ai_company_agent_successes_total{{agent="{agent_id}"}} {counts["success"]}'
            )

        lines.append("# HELP ai_company_agent_failures_total Failed tasks per agent")
        lines.append("# TYPE ai_company_agent_failures_total counter")
        for agent_id, counts in sorted(agent_tasks.items()):
            lines.append(
                f'ai_company_agent_failures_total{{agent="{agent_id}"}} {counts["failure"]}'
            )


def _append_llm_model_breakdown(lines: list[str]) -> None:
    """Parse audit log and emit per-model LLM cost and call gauges."""
    model_stats: dict[str, dict[str, float]] = {}
    try:
        for event in _get_store().iter_jsonl(".opencode/audit"):
            try:
                event_type = event.get("event_type", "")
                if event_type not in ("tool_call", "tool_result"):
                    continue
                meta = event.get("metadata", {})
                model = meta.get("model", "unknown")
                cost = float(meta.get("cost", 0))
                tokens_in = float(meta.get("tokens_in", 0))
                tokens_out = float(meta.get("tokens_out", 0))
                if model not in model_stats:
                    model_stats[model] = {
                        "calls": 0,
                        "cost": 0.0,
                        "tokens_in": 0.0,
                        "tokens_out": 0.0,
                    }
                model_stats[model]["calls"] += 1
                model_stats[model]["cost"] += cost
                model_stats[model]["tokens_in"] += tokens_in
                model_stats[model]["tokens_out"] += tokens_out
            except (json.JSONDecodeError, TypeError):
                continue
    except OSError:
        return

    if model_stats:
        lines.append("# HELP ai_company_llm_model_calls_total LLM calls per model")
        lines.append("# TYPE ai_company_llm_model_calls_total counter")
        for model, stats in sorted(model_stats.items()):
            lines.append(
                f'ai_company_llm_model_calls_total{{model="{model}"}} {int(stats["calls"])}'
            )

        lines.append("# HELP ai_company_llm_model_cost_usd LLM cost per model in USD")
        lines.append("# TYPE ai_company_llm_model_cost_usd gauge")
        for model, stats in sorted(model_stats.items()):
            lines.append(f'ai_company_llm_model_cost_usd{{model="{model}"}} {stats["cost"]:.6f}')

        lines.append("# HELP ai_company_llm_model_tokens_in_total Input tokens per model")
        lines.append("# TYPE ai_company_llm_model_tokens_in_total counter")
        for model, stats in sorted(model_stats.items()):
            lines.append(
                f'ai_company_llm_model_tokens_in_total{{model="{model}"}} {int(stats["tokens_in"])}'
            )

        lines.append("# HELP ai_company_llm_model_tokens_out_total Output tokens per model")
        lines.append("# TYPE ai_company_llm_model_tokens_out_total counter")
        for model, stats in sorted(model_stats.items()):
            lines.append(
                f'ai_company_llm_model_tokens_out_total{{model="{model}"}} '
                f"{int(stats['tokens_out'])}"
            )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/metrics")
def metrics() -> Response:
    """Prometheus-compatible metrics endpoint."""
    body = _render_prometheus_text()
    return Response(
        content=body,
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )


@router.get("/health")
def health_check() -> dict[str, Any]:
    """Deep health check with dependency, disk, and memory status.

    Every file check is anchored at the configured :class:`StateStore` root
    (``DASHBOARD_DATA_DIR`` / project root) — never the process CWD — and
    task counts are read live from the MessageBus (ticket #61 / GAP-011).
    """
    checks: dict[str, str] = {}
    store = _get_store()

    # Check inbox.json accessibility (through the StateStore allowlist)
    checks["inbox"] = "ok" if store.exists(".opencode/inbox.json") else "missing"

    # Check company registry
    checks["registry"] = "ok" if store.exists("company/agent-registry.json") else "missing"

    # Check agents directory (anchored at the StateStore root)
    agents_dir = _state_path(".opencode/agents")
    if agents_dir.exists():
        agent_count = len(list(agents_dir.glob("*.md")))
        checks["agents"] = f"ok ({agent_count} files)"
    else:
        checks["agents"] = "missing"

    # Check company config
    checks["config"] = "ok" if store.exists("company/models.yaml") else "missing"

    # LLM provider availability (env vars)
    providers = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "DEEPSEEK_API_KEY",
        "GEMINI_API_KEY",
        "KIMI_API_KEY",
    ]
    active_providers = [p for p in providers if os.environ.get(p)]
    checks["llm_providers"] = f"{len(active_providers)} configured"

    # Audit log (canonical trail: <data root>/.opencode/audit, ticket #59/#71)
    audit_path = _state_path(".opencode/audit")
    if audit_path.exists():
        try:
            size_kb = audit_path.stat().st_size / 1024
            checks["audit_log"] = f"ok ({size_kb:.1f} KB)"
        except OSError:
            checks["audit_log"] = "error reading"
    else:
        checks["audit_log"] = "missing"

    # Disk space
    checks["disk_space"] = _check_disk_space()

    # Process memory
    checks["process_memory"] = _check_process_memory()

    # Memory store
    memory_dir = _state_path("memory")
    if memory_dir.exists():
        try:
            entry_count = sum(1 for _ in memory_dir.rglob("*.json"))
            checks["memory_store"] = f"ok ({entry_count} entries)"
        except OSError:
            checks["memory_store"] = "error reading"
    else:
        checks["memory_store"] = "missing"

    # Dead letter queue (through the StateStore allowlist)
    dlq = store.read_json(".opencode/dead_letter_queue.json", default=[])
    if isinstance(dlq, list) and dlq:
        pending = sum(1 for t in dlq if isinstance(t, dict) and t.get("status") == "pending")
        checks["dead_letter_queue"] = f"{pending} pending"
    elif dlq:
        checks["dead_letter_queue"] = "error reading"
    else:
        checks["dead_letter_queue"] = "empty"

    # Overall status
    degraded = any(v.startswith("missing") or v.startswith("error") for v in checks.values())
    status = "degraded" if degraded else "ok"

    return {
        "status": status,
        "service": "ai-company-dashboard",
        "version": get_version(),
        "uptime_seconds": round(time.time() - _start_time, 1),
        "checks": checks,
        "metrics_summary": _live_task_summary(),
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }


def _live_task_summary() -> dict[str, Any]:
    """Return a task summary read live from the MessageBus.

    The bus is rooted at the configured :class:`StateStore` directory, so
    counts reflect the live inbox (not a CWD-relative file) and stay correct
    when the dashboard is launched from another directory (ticket #61).
    Falls back to the in-memory process counters if the bus is unavailable.
    """
    tasks: Any = None
    try:
        tasks = _get_bus().get_all_tasks_raw()
    except Exception:  # noqa: BLE001 - health checks must never raise
        logger.debug("Failed to read live tasks for health summary", exc_info=True)

    if not isinstance(tasks, list):
        # Fall back to the LLM cost counter (task counters no longer exist).
        return {
            "tasks_total": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "llm_cost_usd": round(_metrics.get("llm_cost_usd_total", 0), 4),
            "success_rate_pct": 0.0,
        }

    total = len(tasks)
    succeeded = sum(1 for t in tasks if isinstance(t, dict) and t.get("status") == "completed")
    failed = sum(1 for t in tasks if isinstance(t, dict) and t.get("status") == "failed")
    rate = (succeeded / total * 100.0) if total > 0 else 0.0
    return {
        "tasks_total": total,
        "tasks_completed": succeeded,
        "tasks_failed": failed,
        "llm_cost_usd": round(_metrics.get("llm_cost_usd_total", 0), 4),
        "success_rate_pct": round(rate, 1),
    }


def _check_disk_space() -> str:
    """Return a summary of disk space on the current volume."""
    try:
        import shutil

        usage = shutil.disk_usage(".")
        free_gb = usage.free / (1024**3)
        total_gb = usage.total / (1024**3)
        pct_free = (usage.free / usage.total) * 100
        return f"{free_gb:.1f} GB free / {total_gb:.1f} GB ({pct_free:.0f}%)"
    except OSError:
        return "unavailable"


def _check_process_memory() -> str:
    """Return current process memory usage."""
    try:
        import psutil  # type: ignore[import-untyped]

        proc = psutil.Process()
        mem_mb = proc.memory_info().rss / (1024**2)
        return f"{mem_mb:.1f} MB RSS"
    except ImportError:
        # psutil not installed — fall back to resource module.
        try:
            import resource

            usage = resource.getrusage(resource.RUSAGE_SELF)  # type: ignore[attr-defined]
            # ru_maxrss is in KB on Linux, bytes on macOS
            rss_mb = usage.ru_maxrss / 1024
            return f"{rss_mb:.1f} MB peak RSS"
        except (ImportError, AttributeError):
            return "unavailable"
    except Exception:  # noqa: BLE001 - pragma: no cover - psutil runtime error
        return "unavailable"


@router.get("/api/v1/daemon/status")
def daemon_status() -> dict[str, Any]:
    """Executor daemon lifecycle status.

    Reads the daemon health file (``logs/executor-daemon.json``) written by
    :class:`ai_company.executor.daemon.ExecutorDaemon` and returns a
    structured view of the daemon's current state, uptime, and scheduler
    cadence timestamps.

    When no daemon has ever been started the endpoint returns ``state:
    "not_running"`` so callers can distinguish ``stopped`` from ``never
    started``.
    """
    from ai_company.executor.daemon import DaemonHealthStatus, _is_process_alive

    status_path = Path("logs") / "executor-daemon.json"
    health = DaemonHealthStatus(status_path).read()

    if health is None:
        return {
            "state": "not_running",
            "pid": None,
            "started_at": None,
            "uptime_seconds": 0,
            "ticks_completed": 0,
            "last_tick_at": None,
            "is_pid_alive": False,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        }

    pid = health.get("pid")
    is_alive = _is_process_alive(pid) if isinstance(pid, int) else False

    # Detect stale status: status file says "running" but process is dead.
    state = health.get("state", "unknown")
    if state == "running" and not is_alive:
        state = "stale (process dead)"

    return {
        "state": state,
        "pid": pid,
        "started_at": health.get("started_at"),
        "uptime_seconds": health.get("uptime_seconds", 0),
        "ticks_completed": health.get("ticks_completed", 0),
        "last_tick_at": health.get("last_tick_at"),
        "updated_at": health.get("updated_at"),
        "is_pid_alive": is_alive,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }


@router.get("/ready")
def readiness_check() -> Response:
    """Kubernetes-style readiness probe. Returns 503 if core deps are missing.

    Dependency checks are anchored at the configured :class:`StateStore` root
    so readiness is accurate regardless of the process CWD (ticket #61).
    """
    checks_ok = True
    reasons: list[str] = []
    store = _get_store()

    # Registry is the only hard requirement
    if not store.exists("company/agent-registry.json"):
        checks_ok = False
        reasons.append("registry missing")

    # Agents directory (anchored at the StateStore root)
    agents_dir = _state_path(".opencode/agents")
    if not agents_dir.exists():
        checks_ok = False
        reasons.append("agents directory missing")

    if not checks_ok:
        return Response(
            content=json.dumps(
                {
                    "status": "not ready",
                    "reason": "; ".join(reasons),
                }
            ),
            status_code=503,
            media_type="application/json",
        )

    return Response(
        content=json.dumps({"status": "ready"}),
        status_code=200,
        media_type="application/json",
    )
