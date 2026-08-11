"""Compute company-level KPIs (config/company/kpis.yaml) from real file sources.

Implements the CEO Dashboard decision: "Company KPIs must be COMPUTED FROM
REAL SOURCES, not hardcoded dummy values."  This script is the reproducible
derivation for the ``current`` values stored in ``config/company/kpis.yaml``.

Read-only by default (prints the computed table).  ``--write`` refreshes the
``current`` / ``computed_at`` fields of the telemetry-backed KPIs
(``KPI-003`` Agent Utilization Rate, ``KPI-004`` Build Success Rate) in place,
preserving every comment and the KPI entries that have no real source yet
(``KPI-001`` ARR, ``KPI-002`` CSAT, ``KPI-005`` eNPS — kept ``current: null``).

Stable sources ONLY (the SQLite DB is treated as volatile mid-cleanup):
    .opencode/inbox.json          task telemetry (status, sender/receiver, created_at)
    company-registry.yaml         registered agents (127)
    .opencode/audit.jsonl         task-created event log (throughput, supporting)
    company/departments.yaml      declared departments (coverage, supporting)
    orchestrator/cost_tracker.json cost (currently all zeros -> n/a, supporting)

Formulas:
    KPI-003 = distinct active agents in the 30-day task window / registered
              agents (company-registry.yaml ``company.agents``) x 100
    KPI-004 = completed / (completed + failed) x 100 over the 30-day window

Usage:
    python scripts/compute_company_kpis.py             # verify only
    python scripts/compute_company_kpis.py --write     # refresh kpis.yaml
    python scripts/compute_company_kpis.py --days 7    # custom window
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - venv always has pyyaml
    print("PyYAML is required (uv sync --extra dev).", file=sys.stderr)
    sys.exit(1)

KPI_YAML = "config/company/kpis.yaml"
INBOX_JSON = ".opencode/inbox.json"
AUDIT_JSONL = ".opencode/audit.jsonl"
REGISTRY_YAML = "company-registry.yaml"
DEPARTMENTS_YAML = "company/departments.yaml"
COST_TRACKER_JSON = "orchestrator/cost_tracker.json"

# KPI-003 / KPI-004 are the only company KPIs with a real source today.
COMPUTABLE_IDS = ("KPI-003", "KPI-004")


def _project_root() -> Path:
    """Resolve the ai-company project root deterministically."""
    try:
        from ai_company.paths import get_project_root

        return get_project_root()
    except Exception:  # noqa: BLE001 - defensive fallback when package import fails
        return Path(__file__).resolve().parent.parent


def _load_json(path: Path) -> object:
    if not path.is_file():
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _task_list(raw: object) -> list[dict]:
    if isinstance(raw, list):
        return [t for t in raw if isinstance(t, dict)]
    if isinstance(raw, dict):
        tasks = raw.get("tasks")
        if isinstance(tasks, list):
            return [t for t in tasks if isinstance(t, dict)]
    return []


def _parse_ts(value: str) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value))
    except (ValueError, TypeError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _window_tasks(tasks: list[dict], days: int) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return [t for t in tasks if (c := _parse_ts(t.get("created_at", ""))) and c >= cutoff]


def compute(root: Path, days: int) -> dict:
    """Compute all real KPI currents and supporting metrics. Never raises."""
    result: dict = {"kpis": {}, "supporting": {}, "warnings": []}

    # ── Task telemetry (KPI-003, KPI-004) ──────────────────────────────
    inbox_raw = _load_json(root / INBOX_JSON)
    tasks = _task_list(inbox_raw)
    if not tasks:
        result["warnings"].append(f"{INBOX_JSON} missing or empty")
    window = _window_tasks(tasks, days)

    registry = _load_yaml(root / REGISTRY_YAML)
    registered = (
        len(registry.get("company", {}).get("agents", []))
        if isinstance(registry.get("company"), dict)
        else 0
    )
    if registered == 0:
        result["warnings"].append(f"{REGISTRY_YAML} has no company.agents")

    active = {a for t in window for a in (t.get("sender_id"), t.get("receiver_id")) if a}
    completed = sum(1 for t in window if t.get("status") == "completed")
    failed = sum(1 for t in window if t.get("status") == "failed")

    result["kpis"]["KPI-003"] = round(len(active) / registered * 100, 1) if registered > 0 else None
    result["kpis"]["KPI-004"] = (
        round(completed / (completed + failed) * 100, 1) if (completed + failed) > 0 else None
    )
    result["supporting"]["window_tasks"] = len(window)
    result["supporting"]["distinct_active_agents"] = len(active)
    result["supporting"]["registered_agents"] = registered
    result["supporting"]["window_completed"] = completed
    result["supporting"]["window_failed"] = failed

    # ── Supporting: task throughput from audit.jsonl ───────────────────
    audit_events: list[dict] = []
    audit_path = root / AUDIT_JSONL
    if audit_path.is_file():
        with open(audit_path, "r", encoding="utf-8") as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(rec, dict):
                    audit_events.append(rec)
    created_tss = [
        ts for ts in (_parse_ts(r.get("timestamp", "")) for r in audit_events) if ts is not None
    ]
    if created_tss:
        span_days = max((max(created_tss) - min(created_tss)).total_seconds() / 86400.0, 1.0)
        result["supporting"]["task_throughput_per_day"] = round(len(audit_events) / span_days, 1)
        result["supporting"]["audit_span_days"] = round(span_days, 2)
    else:
        result["warnings"].append(f"{AUDIT_JSONL} has no parseable timestamps")

    # ── Supporting: overall task completion + department coverage ──────
    if tasks:
        status_counts: dict[str, int] = {}
        for t in tasks:
            status_counts[t.get("status", "?")] = status_counts.get(t.get("status", "?"), 0) + 1
        total = len(tasks)
        result["supporting"]["task_completion_rate"] = round(
            status_counts.get("completed", 0) / total * 100, 1
        )
        result["supporting"]["task_status_counts"] = status_counts

    agent_depts = {
        str(a.get("department"))
        for a in registry.get("company", {}).get("agents", [])
        if isinstance(a, dict) and a.get("department")
    }
    departments = _load_yaml(root / DEPARTMENTS_YAML).get("departments", [])
    declared_ids = {str(d.get("id")) for d in departments if isinstance(d, dict) and d.get("id")}
    if declared_ids:
        normalized = {d.lower().replace(" ", "_").replace("-", "_") for d in agent_depts}
        covered = len(declared_ids & normalized)
        result["supporting"]["department_coverage"] = round(covered / len(declared_ids) * 100, 1)
        result["supporting"]["departments_covered"] = covered
        result["supporting"]["departments_declared"] = len(declared_ids)

    # ── Supporting: cost (real file, currently zeros) ──────────────────
    cost = _load_json(root / COST_TRACKER_JSON)
    if isinstance(cost, dict):
        result["supporting"]["cost_total_spent"] = cost.get("total_spent", 0)
        result["supporting"]["cost_llm_spend"] = cost.get("llm_spend", 0)
        if not cost.get("total_spent") and not cost.get("llm_spend"):
            result["warnings"].append(f"{COST_TRACKER_JSON} holds zeros — no real cost data yet")

    return result


def _print_report(root: Path, days: int, result: dict) -> None:
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"Company KPI computation (root={root}, window={days}d, computed_at={now_iso})")
    print("-" * 78)

    kpis = result["kpis"]
    lines = [
        ("KPI-001", "Annual Recurring Revenue", None, "NO SOURCE YET (revenue ledger required)"),
        (
            "KPI-002",
            "Customer Satisfaction",
            None,
            "NO DATA YET (orchestrator/cs/surveys.json is empty)",
        ),
        ("KPI-003", "Agent Utilization Rate", kpis.get("KPI-003"), "LIVE"),
        ("KPI-004", "Build Success Rate", kpis.get("KPI-004"), "LIVE"),
        ("KPI-005", "Employee Net Promoter Score", None, "NO SOURCE YET (people survey required)"),
    ]
    for kpi_id, name, value, note in lines:
        if value is None and kpi_id in COMPUTABLE_IDS:
            value_str = "n/a (no window tasks)"
        elif value is None:
            value_str = "n/a"
        else:
            value_str = f"{value}"
        print(f"  {kpi_id}  {name:<28} current={value_str:<18} {note}")

    print()
    print("Supporting metrics (real sources):")
    s = result["supporting"]
    for key in (
        "registered_agents",
        "distinct_active_agents",
        "window_tasks",
        "window_completed",
        "window_failed",
        "task_throughput_per_day",
        "task_completion_rate",
        "department_coverage",
        "cost_total_spent",
        "cost_llm_spend",
    ):
        if key in s:
            print(f"  {key}: {s[key]}")
    if "task_status_counts" in s:
        print(f"  task_status_counts: {s['task_status_counts']}")

    if result["warnings"]:
        print()
        print("Warnings:")
        for w in result["warnings"]:
            print(f"  WARN: {w}")


def _update_yaml(path: Path, updates: dict[str, dict], now_iso: str) -> list[str]:
    """Refresh ``current``/``computed_at`` for the given KPI ids in place.

    Uses line-scoped edits inside each ``- id: KPI-00X`` block so comments and
    the KPI entries without a real source are preserved byte-for-byte.
    Returns the list of changed lines.
    """
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    current_id: str | None = None
    changes: list[str] = []
    out: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- id:"):
            current_id = stripped.split(":", 1)[1].strip().strip("\"'")

        if current_id in updates and stripped.startswith(("current:", "computed_at:")):
            field = stripped.split(":", 1)[0]
            new_value = updates[current_id][field]
            indent = line[: len(line) - len(line.lstrip())]
            comment = line.split("#", 1)[1].strip() if "#" in line else ""
            suffix = f"  # {comment}" if comment else ""
            replacement = f"{indent}{field}: {new_value}{suffix}\n"
            if replacement != line:
                changes.append(f"{current_id}.{field}: {line.strip()} -> {replacement.strip()}")
            out.append(replacement)
            continue

        out.append(line)

    if changes:
        path.write_text("".join(out), encoding="utf-8")
    return changes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="refresh current/computed_at for KPI-003/KPI-004 in config/company/kpis.yaml",
    )
    parser.add_argument("--days", type=int, default=30, help="task window in days (default: 30)")
    args = parser.parse_args(argv)

    root = _project_root()
    result = compute(root, args.days)
    _print_report(root, args.days, result)

    if args.write:
        kpis_path = root / KPI_YAML
        if not kpis_path.is_file():
            print(f"ERROR: {kpis_path} not found", file=sys.stderr)
            return 1
        now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
        updates = {
            kpi_id: {
                "current": result["kpis"].get(kpi_id, "null"),
                "computed_at": f'"{now_iso}"',
            }
            for kpi_id in COMPUTABLE_IDS
        }
        changes = _update_yaml(kpis_path, updates, now_iso)
        if changes:
            print()
            print(f"Updated {kpis_path}:")
            for c in changes:
                print(f"  {c}")
        else:
            print(f"\nNo changes needed in {kpis_path}.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
