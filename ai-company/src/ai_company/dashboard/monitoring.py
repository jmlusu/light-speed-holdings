"""Prometheus-compatible /metrics endpoint and deep health checks.

Provides:
- ``/metrics`` — Prometheus text exposition format with agent performance,
  memory usage, LLM cost breakdown, and operational counters
- ``/health`` — Deep health check with dependency, disk, and memory status
- ``/ready`` — Readiness probe (returns 200 when all deps are up)
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

logger = logging.getLogger(__name__)

router = APIRouter(tags=["monitoring"])

# ---------------------------------------------------------------------------
# Metrics store (in-memory counters — reset on process restart)
# ---------------------------------------------------------------------------

_metrics: dict[str, float] = {
    # Task metrics
    "tasks_total": 0,
    "tasks_succeeded": 0,
    "tasks_failed": 0,
    "tasks_escalated": 0,
    # Cycle metrics
    "cycle_count": 0,
    "cycle_failures": 0,
    # LLM metrics
    "llm_requests_total": 0,
    "llm_errors_total": 0,
    "llm_cost_usd_total": 0.0,
    "llm_cost_usd_anthropic": 0.0,
    "llm_cost_usd_openai": 0.0,
    "llm_cost_usd_deepseek": 0.0,
    "llm_cost_usd_other": 0.0,
    # Approval / HITL metrics
    "approval_requests_total": 0,
    "approval_auto_approved": 0,
    "approval_human_approved": 0,
    "approval_rejected": 0,
    # Dead letter
    "dead_letters_total": 0,
    # API
    "api_requests_total": 0,
    # Agent performance
    "agent_task_success_total": 0,
    "agent_task_failure_total": 0,
    "agent_total_tokens_in": 0,
    "agent_total_tokens_out": 0,
    # Memory
    "memory_store_bytes": 0.0,
    "memory_entries_total": 0,
    # Circuit breaker
    "circuit_breaker_trips_total": 0,
    "circuit_breaker_half_open_total": 0,
}

_start_time = time.time()


def inc_metric(name: str, value: float = 1.0) -> None:
    """Increment a named metric by value."""
    _metrics[name] = _metrics.get(name, 0) + value


def set_metric(name: str, value: float) -> None:
    """Set a named metric to an exact value."""
    _metrics[name] = value


def get_metrics() -> dict[str, float]:
    """Return a snapshot of all metrics."""
    return dict(_metrics)


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
        "tasks_total": ("ai_company_tasks_total", "Total tasks processed"),
        "tasks_succeeded": ("ai_company_tasks_succeeded_total", "Total tasks succeeded"),
        "tasks_failed": ("ai_company_tasks_failed_total", "Total tasks failed"),
        "tasks_escalated": ("ai_company_tasks_escalated_total", "Total tasks escalated"),
        "cycle_count": ("ai_company_cycles_total", "Total autonomous cycles executed"),
        "cycle_failures": ("ai_company_cycle_failures_total", "Total cycle failures"),
        "llm_requests_total": ("ai_company_llm_requests_total", "Total LLM API requests"),
        "llm_errors_total": ("ai_company_llm_errors_total", "Total LLM API errors"),
        "approval_requests_total": (
            "ai_company_approval_requests_total",
            "Total approval requests",
        ),
        "approval_auto_approved": (
            "ai_company_approval_auto_approved_total",
            "Total auto-approved requests",
        ),
        "approval_human_approved": (
            "ai_company_approval_human_approved_total",
            "Total human-approved requests",
        ),
        "approval_rejected": (
            "ai_company_approval_rejected_total",
            "Total rejected approval requests",
        ),
        "dead_letters_total": (
            "ai_company_dead_letters_total",
            "Total dead-letter queue entries",
        ),
        "api_requests_total": (
            "ai_company_api_requests_total",
            "Total dashboard API requests",
        ),
        "agent_task_success_total": (
            "ai_company_agent_task_success_total",
            "Total agent tasks completed successfully",
        ),
        "agent_task_failure_total": (
            "ai_company_agent_task_failure_total",
            "Total agent tasks that failed",
        ),
        "agent_total_tokens_in": (
            "ai_company_agent_tokens_in_total",
            "Total input tokens consumed by agents",
        ),
        "agent_total_tokens_out": (
            "ai_company_agent_tokens_out_total",
            "Total output tokens produced by agents",
        ),
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

    # ── Memory store gauge ──────────────────────────────────────────
    lines.append("# HELP ai_company_memory_store_bytes Size of memory store in bytes")
    lines.append("# TYPE ai_company_memory_store_bytes gauge")
    lines.append(
        f"ai_company_memory_store_bytes {_metrics.get('memory_store_bytes', 0):.0f}"
    )

    lines.append(
        "# HELP ai_company_memory_entries_total Number of entries in memory store"
    )
    lines.append("# TYPE ai_company_memory_entries_total gauge")
    lines.append(
        f"ai_company_memory_entries_total {_metrics.get('memory_entries_total', 0):.0f}"
    )

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

        usage = resource.getrusage(resource.RUSAGE_SELF)
        # Max RSS in bytes (Linux: bytes, macOS: bytes)
        rss_bytes = usage.ru_maxrss
        lines.append(
            "# HELP ai_company_process_max_rss_bytes "
            "Peak resident set size in bytes"
        )
        lines.append("# TYPE ai_company_process_max_rss_bytes gauge")
        lines.append(f"ai_company_process_max_rss_bytes {rss_bytes}")
    except (ImportError, AttributeError):
        # resource module not available on Windows
        pass

    try:
        import psutil

        proc = psutil.Process()
        mem_info = proc.memory_info()
        lines.append(
            "# HELP ai_company_process_rss_bytes Current RSS in bytes"
        )
        lines.append("# TYPE ai_company_process_rss_bytes gauge")
        lines.append(f"ai_company_process_rss_bytes {mem_info.rss}")

        lines.append(
            "# HELP ai_company_process_vms_bytes Current VMS in bytes"
        )
        lines.append("# TYPE ai_company_process_vms_bytes gauge")
        lines.append(f"ai_company_process_vms_bytes {mem_info.vms}")

        lines.append(
            "# HELP ai_company_process_open_fds Number of open file descriptors"
        )
        lines.append("# TYPE ai_company_process_open_fds gauge")
        lines.append(
            f"ai_company_process_open_fds {proc.num_fds()}"
        )
    except (ImportError, psutil.Error):
        pass

    # CPU times (always available via os.times)
    times = os.times()
    lines.append(
        "# HELP ai_company_cpu_user_seconds_total User CPU time in seconds"
    )
    lines.append("# TYPE ai_company_cpu_user_seconds_total counter")
    lines.append(f"ai_company_cpu_user_seconds_total {times[0]:.3f}")

    lines.append(
        "# HELP ai_company_cpu_system_seconds_total System CPU time in seconds"
    )
    lines.append("# TYPE ai_company_cpu_system_seconds_total counter")
    lines.append(f"ai_company_cpu_system_seconds_total {times[1]:.3f}")


def _append_derived_metrics(lines: list[str]) -> None:
    """Append computed / derived gauges."""
    # Task success rate
    total = _metrics.get("tasks_total", 0)
    succeeded = _metrics.get("tasks_succeeded", 0)
    rate = (succeeded / total * 100.0) if total > 0 else 0.0
    lines.append(
        "# HELP ai_company_task_success_rate_pct Task success rate as percentage"
    )
    lines.append("# TYPE ai_company_task_success_rate_pct gauge")
    lines.append(f"ai_company_task_success_rate_pct {rate:.2f}")

    # Cycle success rate
    cycles = _metrics.get("cycle_count", 0)
    cycle_fail = _metrics.get("cycle_failures", 0)
    cycle_rate = (
        ((cycles - cycle_fail) / cycles * 100.0) if cycles > 0 else 0.0
    )
    lines.append(
        "# HELP ai_company_cycle_success_rate_pct Cycle success rate as percentage"
    )
    lines.append("# TYPE ai_company_cycle_success_rate_pct gauge")
    lines.append(f"ai_company_cycle_success_rate_pct {cycle_rate:.2f}")

    # LLM error rate
    llm_req = _metrics.get("llm_requests_total", 0)
    llm_err = _metrics.get("llm_errors_total", 0)
    llm_rate = (llm_err / llm_req * 100.0) if llm_req > 0 else 0.0
    lines.append(
        "# HELP ai_company_llm_error_rate_pct LLM error rate as percentage"
    )
    lines.append("# TYPE ai_company_llm_error_rate_pct gauge")
    lines.append(f"ai_company_llm_error_rate_pct {llm_rate:.2f}")

    # Average LLM cost per request
    avg_cost = (
        _metrics.get("llm_cost_usd_total", 0.0) / llm_req
        if llm_req > 0
        else 0.0
    )
    lines.append(
        "# HELP ai_company_llm_avg_cost_per_request_usd "
        "Average LLM cost per request in USD"
    )
    lines.append("# TYPE ai_company_llm_avg_cost_per_request_usd gauge")
    lines.append(f"ai_company_llm_avg_cost_per_request_usd {avg_cost:.6f}")


def _append_task_status_breakdown(lines: list[str]) -> None:
    """Read live inbox and emit per-status gauges."""
    inbox_path = Path(".opencode/inbox.json")
    if not inbox_path.exists():
        return
    try:
        tasks = json.loads(inbox_path.read_text(encoding="utf-8"))
        status_counts: dict[str, int] = {}
        for t in tasks:
            s = t.get("status", "unknown")
            status_counts[s] = status_counts.get(s, 0) + 1
        lines.append(
            "# HELP ai_company_tasks_by_status Number of tasks by status"
        )
        lines.append("# TYPE ai_company_tasks_by_status gauge")
        for status, count in sorted(status_counts.items()):
            lines.append(
                f'ai_company_tasks_by_status{{status="{status}"}} {count}'
            )
    except Exception:
        logger.debug("Failed to read inbox for task status breakdown")


def _append_agent_performance(lines: list[str]) -> None:
    """Parse audit log and emit per-agent task success/failure counters."""
    audit_path = Path(".opencode/audit.jsonl")
    if not audit_path.exists():
        return

    agent_tasks: dict[str, dict[str, int]] = {}
    try:
        with open(audit_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                    if event.get("event_type") != "task_complete":
                        continue
                    agent_id = event.get("agent_id", "unknown")
                    success = event.get("metadata", {}).get("success", True)
                    if agent_id not in agent_tasks:
                        agent_tasks[agent_id] = {
                            "success": 0,
                            "failure": 0,
                        }
                    if success:
                        agent_tasks[agent_id]["success"] += 1
                    else:
                        agent_tasks[agent_id]["failure"] += 1
                except (json.JSONDecodeError, TypeError):
                    continue
    except OSError:
        return

    if agent_tasks:
        lines.append(
            "# HELP ai_company_agent_tasks_total "
            "Tasks completed per agent"
        )
        lines.append("# TYPE ai_company_agent_tasks_total counter")
        for agent_id, counts in sorted(agent_tasks.items()):
            total = counts["success"] + counts["failure"]
            lines.append(
                f'ai_company_agent_tasks_total{{agent="{agent_id}"}} {total}'
            )

        lines.append(
            "# HELP ai_company_agent_successes_total "
            "Successful tasks per agent"
        )
        lines.append("# TYPE ai_company_agent_successes_total counter")
        for agent_id, counts in sorted(agent_tasks.items()):
            lines.append(
                f'ai_company_agent_successes_total{{agent="{agent_id}"}} '
                f'{counts["success"]}'
            )

        lines.append(
            "# HELP ai_company_agent_failures_total "
            "Failed tasks per agent"
        )
        lines.append("# TYPE ai_company_agent_failures_total counter")
        for agent_id, counts in sorted(agent_tasks.items()):
            lines.append(
                f'ai_company_agent_failures_total{{agent="{agent_id}"}} '
                f'{counts["failure"]}'
            )


def _append_llm_model_breakdown(lines: list[str]) -> None:
    """Parse audit log and emit per-model LLM cost and call gauges."""
    audit_path = Path(".opencode/audit.jsonl")
    if not audit_path.exists():
        return

    model_stats: dict[str, dict[str, float]] = {}
    try:
        with open(audit_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
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
        lines.append(
            "# HELP ai_company_llm_model_calls_total "
            "LLM calls per model"
        )
        lines.append("# TYPE ai_company_llm_model_calls_total counter")
        for model, stats in sorted(model_stats.items()):
            lines.append(
                f'ai_company_llm_model_calls_total{{model="{model}"}} '
                f'{int(stats["calls"])}'
            )

        lines.append(
            "# HELP ai_company_llm_model_cost_usd "
            "LLM cost per model in USD"
        )
        lines.append("# TYPE ai_company_llm_model_cost_usd gauge")
        for model, stats in sorted(model_stats.items()):
            lines.append(
                f'ai_company_llm_model_cost_usd{{model="{model}"}} '
                f'{stats["cost"]:.6f}'
            )

        lines.append(
            "# HELP ai_company_llm_model_tokens_in_total "
            "Input tokens per model"
        )
        lines.append("# TYPE ai_company_llm_model_tokens_in_total counter")
        for model, stats in sorted(model_stats.items()):
            lines.append(
                f'ai_company_llm_model_tokens_in_total{{model="{model}"}} '
                f'{int(stats["tokens_in"])}'
            )

        lines.append(
            "# HELP ai_company_llm_model_tokens_out_total "
            "Output tokens per model"
        )
        lines.append("# TYPE ai_company_llm_model_tokens_out_total counter")
        for model, stats in sorted(model_stats.items()):
            lines.append(
                f'ai_company_llm_model_tokens_out_total{{model="{model}"}} '
                f'{int(stats["tokens_out"])}'
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
    """Deep health check with dependency, disk, and memory status."""
    checks: dict[str, str] = {}

    # Check inbox.json accessibility
    inbox_path = Path(".opencode/inbox.json")
    checks["inbox"] = "ok" if inbox_path.exists() else "missing"

    # Check company registry
    registry_path = Path("company/agent-registry.json")
    checks["registry"] = "ok" if registry_path.exists() else "missing"

    # Check agents directory
    agents_dir = Path(".opencode/agents")
    if agents_dir.exists():
        agent_count = len(list(agents_dir.glob("*.md")))
        checks["agents"] = f"ok ({agent_count} files)"
    else:
        checks["agents"] = "missing"

    # Check company config
    config_path = Path("company/models.yaml")
    checks["config"] = "ok" if config_path.exists() else "missing"

    # LLM provider availability (env vars)
    providers = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "DEEPSEEK_API_KEY"]
    active_providers = [p for p in providers if os.environ.get(p)]
    checks["llm_providers"] = f"{len(active_providers)} configured"

    # Audit log
    audit_path = Path(".opencode/audit.jsonl")
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
    memory_dir = Path("memory")
    if memory_dir.exists():
        try:
            entry_count = sum(1 for _ in memory_dir.rglob("*.json"))
            checks["memory_store"] = f"ok ({entry_count} entries)"
        except OSError:
            checks["memory_store"] = "error reading"
    else:
        checks["memory_store"] = "missing"

    # Dead letter queue
    dlq_path = Path(".opencode/dead_letter_queue.json")
    if dlq_path.exists():
        try:
            dlq = json.loads(dlq_path.read_text(encoding="utf-8"))
            pending = sum(
                1 for t in dlq if t.get("status") == "pending"
            ) if isinstance(dlq, list) else 0
            checks["dead_letter_queue"] = f"{pending} pending"
        except (json.JSONDecodeError, OSError):
            checks["dead_letter_queue"] = "error reading"
    else:
        checks["dead_letter_queue"] = "empty"

    # Overall status
    degraded = any(
        v.startswith("missing") or v.startswith("error")
        for v in checks.values()
    )
    status = "degraded" if degraded else "ok"

    return {
        "status": status,
        "service": "ai-company-dashboard",
        "version": "0.2.0",
        "uptime_seconds": round(time.time() - _start_time, 1),
        "checks": checks,
        "metrics_summary": {
            "tasks_total": _metrics.get("tasks_total", 0),
            "llm_cost_usd": round(_metrics.get("llm_cost_usd_total", 0), 4),
            "success_rate_pct": round(
                (
                    _metrics.get("tasks_succeeded", 0)
                    / _metrics.get("tasks_total", 1)
                    * 100
                ),
                1,
            ),
        },
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
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
        import psutil

        proc = psutil.Process()
        mem_mb = proc.memory_info().rss / (1024**2)
        return f"{mem_mb:.1f} MB RSS"
    except (ImportError, psutil.Error):
        try:
            import resource

            usage = resource.getrusage(resource.RUSAGE_SELF)
            # ru_maxrss is in KB on Linux, bytes on macOS
            rss_mb = usage.ru_maxrss / 1024
            return f"{rss_mb:.1f} MB peak RSS"
        except (ImportError, AttributeError):
            return "unavailable"


@router.get("/ready")
def readiness_check() -> Response:
    """Kubernetes-style readiness probe. Returns 503 if core deps are missing."""
    checks_ok = True
    reasons: list[str] = []

    # Registry is the only hard requirement
    registry_path = Path("company/agent-registry.json")
    if not registry_path.exists():
        checks_ok = False
        reasons.append("registry missing")

    # Agents directory
    agents_dir = Path(".opencode/agents")
    if not agents_dir.exists():
        checks_ok = False
        reasons.append("agents directory missing")

    if not checks_ok:
        return Response(
            content=json.dumps({
                "status": "not ready",
                "reason": "; ".join(reasons),
            }),
            status_code=503,
            media_type="application/json",
        )

    return Response(
        content=json.dumps({"status": "ready"}),
        status_code=200,
        media_type="application/json",
    )
