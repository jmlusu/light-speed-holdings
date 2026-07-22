"""Reusable test fixtures for dashboard testing.

Provides factory functions and data builders for generating realistic
dashboard data: tasks, agents, KPIs, approvals, and escalations.
"""

from __future__ import annotations

import json
import shutil
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generator
from unittest.mock import patch

import yaml


# ---------------------------------------------------------------------------
# Rate-limiter bypass (for tests that make many rapid requests)
# ---------------------------------------------------------------------------


class _NoopRateLimiter:
    """Infinite-capacity rate limiter for test environments."""

    def is_allowed(self, _key: str) -> tuple[bool, int]:
        return True, 999_999


@contextmanager
def patch_rate_limiter() -> Generator[None, None, None]:
    """Context manager that disables the dashboard rate limiter.

    Patches the ``is_allowed`` method on the ``_RateLimiter`` class in the
    app module so that all existing and future instances allow unlimited
    requests.

    Usage::

        with patch_rate_limiter():
            client.get("/api/dashboard")  # never 429
    """
    from ai_company.dashboard.app import _RateLimiter

    def _unlimited(self: Any, _key: str) -> tuple[bool, int]:
        return True, 999_999

    with patch.object(_RateLimiter, "is_allowed", _unlimited):
        yield


# ---------------------------------------------------------------------------
# Task fixtures
# ---------------------------------------------------------------------------


def make_task(
    *,
    id: str | None = None,
    sender_id: str = "human-ceo",
    receiver_id: str = "test-agent",
    instruction: str = "Test task",
    status: str = "pending",
    priority: str = "medium",
    created_at: str | None = None,
    **extra: Any,
) -> dict[str, Any]:
    """Build a single task dict matching the TaskItem schema."""
    return {
        "id": id or str(uuid.uuid4()),
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "instruction": instruction,
        "status": status,
        "priority": priority,
        "created_at": created_at or datetime.now(timezone.utc).isoformat(),
        **extra,
    }


def make_tasks(count: int, **overrides: Any) -> list[dict[str, Any]]:
    """Build *count* tasks. Keyword args are applied to every task."""
    return [make_task(**overrides) for _ in range(count)]


def make_tasks_with_mixed_statuses() -> list[dict[str, Any]]:
    """Return a realistic mix of tasks across all statuses."""
    statuses = ["pending", "in_progress", "completed", "failed", "escalated"]
    tasks = []
    for i, status in enumerate(statuses):
        tasks.append(make_task(
            receiver_id=f"agent-{i}",
            instruction=f"Task for {status}",
            status=status,
        ))
    # Add extra completed tasks to make the mix realistic
    tasks.extend(make_tasks(5, status="completed", receiver_id="lead-engineering"))
    tasks.extend(make_tasks(3, status="pending", receiver_id="lead-marketing"))
    return tasks


# ---------------------------------------------------------------------------
# Agent fixtures
# ---------------------------------------------------------------------------


def make_agent(
    *,
    name: str = "test-agent",
    role: str = "Test Agent",
    type: str = "Specialist",
    department: str = "Engineering",
    reports_to: str = "chief-of-staff",
    direct_reports: list[str] | None = None,
    description: str = "A test agent",
    tools: list[str] | None = None,
) -> dict[str, Any]:
    """Build a single agent registry entry."""
    return {
        "name": name,
        "role": role,
        "type": type,
        "department": department,
        "reportsTo": reports_to,
        "directReports": direct_reports or [],
        "description": description,
        "tools": tools or ["read", "write", "execute"],
        "permission": "Execute",
    }


def make_agent_registry(count: int = 5) -> list[dict[str, Any]]:
    """Build a realistic agent hierarchy."""
    agents = [
        make_agent(
            name="chief-of-staff",
            role="Chief of Staff",
            type="Executive",
            department="Executive",
            reports_to="human-ceo",
            direct_reports=["lead-engineering", "lead-marketing", "lead-sales"],
        ),
        make_agent(
            name="lead-engineering",
            role="Lead Engineer",
            type="Specialist",
            department="Engineering",
            direct_reports=[],
        ),
        make_agent(
            name="lead-marketing",
            role="Marketing Lead",
            type="Specialist",
            department="Marketing",
            direct_reports=[],
        ),
    ]
    for i in range(max(0, count - 3)):
        agents.append(make_agent(
            name=f"agent-{i}",
            role=f"Agent {i}",
            department="Engineering",
        ))
    return agents[:count]


# ---------------------------------------------------------------------------
# KPI fixtures
# ---------------------------------------------------------------------------


def make_kpi_snapshot(
    *,
    pending: int = 2,
    in_progress: int = 1,
    completed: int = 10,
    failed: int = 1,
    escalated: int = 0,
    approvals: int = 0,
    agents: int = 5,
    uptime: float = 3600.0,
) -> dict[str, Any]:
    """Build a KPI payload matching the KPIs response model."""
    return {
        "pending_tasks": pending,
        "in_progress_tasks": in_progress,
        "completed_tasks": completed,
        "failed_tasks": failed,
        "escalated_tasks": escalated,
        "pending_approvals": approvals,
        "open_escalations": escalated,
        "total_agents": agents,
        "scheduled_tasks": 0,
        "uptime_seconds": uptime,
    }


def make_department_kpis() -> dict[str, Any]:
    """Build department KPI config matching the kpis.yaml file structure.

    The file is wrapped in a ``departments`` key because the API reads
    ``kpi_data.get("departments", {})``.
    """
    return {
        "departments": {
            "engineering": {
                "name": "Engineering",
                "kpis": [
                    {
                        "id": "eng-1",
                        "name": "Sprint Velocity",
                        "target": 50,
                        "current": 42,
                        "unit": "points",
                        "frequency": "weekly",
                        "description": "Story points per sprint",
                    },
                    {
                        "id": "eng-2",
                        "name": "Deployment Frequency",
                        "target": 5,
                        "current": 3,
                        "unit": "deploys/week",
                        "frequency": "weekly",
                        "description": "Deployments per week",
                    },
                ],
            },
            "marketing": {
                "name": "Marketing",
                "kpis": [
                    {
                        "id": "mkt-1",
                        "name": "Lead Conversion",
                        "target": 15,
                        "current": 12,
                        "unit": "%",
                        "frequency": "monthly",
                        "description": "Lead to customer conversion rate",
                    },
                ],
            },
        },
    }


# ---------------------------------------------------------------------------
# Approval fixtures
# ---------------------------------------------------------------------------


def make_approval(
    *,
    id: str | None = None,
    task_id: str = "t-1",
    agent_id: str = "lead-engineering",
    action: str = "deploy",
    description: str = "Deploy to production",
    status: str = "pending",
    tier: int = 2,
) -> dict[str, Any]:
    """Build a single approval request."""
    return {
        "id": id or f"req-{uuid.uuid4().hex[:8]}",
        "task_id": task_id,
        "agent_id": agent_id,
        "action": action,
        "description": description,
        "status": status,
        "tier": tier,
    }


def make_approvals_yaml(count: int = 2) -> str:
    """Build YAML content for the approvals fixture file."""
    requests = [make_approval() for _ in range(count)]
    return yaml.dump({"requests": requests})


# ---------------------------------------------------------------------------
# Escalation fixtures
# ---------------------------------------------------------------------------


def make_escalation(
    *,
    task_id: str | None = None,
    rule_id: str = "timeout",
    from_agent: str = "agent-a",
    to_agent: str = "agent-b",
    reason: str = "Task exceeded time limit",
    resolved: bool = False,
) -> dict[str, Any]:
    """Build a single escalation event."""
    return {
        "task_id": task_id or f"esc-{uuid.uuid4().hex[:8]}",
        "rule_id": rule_id,
        "from_agent": from_agent,
        "to_agent": to_agent,
        "reason": reason,
        "resolved": resolved,
    }


def make_escalations_yaml(count: int = 1) -> str:
    """Build YAML content for the escalation fixture file."""
    events = [make_escalation() for _ in range(count)]
    return yaml.dump({"rules": [], "events": events})


# ---------------------------------------------------------------------------
# Workspace setup helpers
# ---------------------------------------------------------------------------


def seed_dashboard_workspace(
    base_path: Path,
    *,
    task_count: int = 5,
    agent_count: int = 3,
    approval_count: int = 1,
    escalation_count: int = 1,
) -> None:
    """Write all fixture files into *base_path* for dashboard API testing."""
    # Agent registry
    (base_path / "company").mkdir(parents=True, exist_ok=True)
    registry = make_agent_registry(agent_count)
    (base_path / "company" / "agent-registry.json").write_text(
        json.dumps(registry), encoding="utf-8"
    )

    # Departments
    departments = {
        "departments": [
            {
                "name": dept,
                "executive": f"lead-{dept.lower()}",
                "agents": [f"lead-{dept.lower()}"],
                "total_agents": 1,
            }
            for dept in ["Executive", "Engineering", "Marketing"]
        ]
    }
    (base_path / "company" / "departments.yaml").write_text(
        yaml.dump(departments), encoding="utf-8"
    )

    # KPI config -- prefer the real file if available for full compatibility
    config_dir = base_path / "company" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    real_kpis = Path(__file__).resolve().parents[2] / "company" / "config" / "kpis.yaml"
    if real_kpis.exists():
        shutil.copy2(str(real_kpis), str(config_dir / "kpis.yaml"))
    else:
        kpi_data = make_department_kpis()
        (config_dir / "kpis.yaml").write_text(yaml.dump(kpi_data), encoding="utf-8")

    # Orchestrator dirs
    (base_path / "orchestrator").mkdir(exist_ok=True)
    (base_path / ".opencode").mkdir(exist_ok=True)

    # Inbox (tasks)
    tasks = make_tasks(task_count)
    (base_path / ".opencode" / "inbox.json").write_text(
        json.dumps(tasks), encoding="utf-8"
    )

    # Approvals
    (base_path / "orchestrator" / "approvals.yaml").write_text(
        make_approvals_yaml(approval_count), encoding="utf-8"
    )

    # Escalations
    (base_path / "orchestrator" / "escalation.yaml").write_text(
        make_escalations_yaml(escalation_count), encoding="utf-8"
    )

    # Scheduler
    (base_path / "orchestrator" / "scheduler.yaml").write_text(
        yaml.dump({"tasks": []}), encoding="utf-8"
    )

    # Models config (copy from real project if available)
    real_models = Path(__file__).resolve().parents[2] / "company" / "models.yaml"
    if real_models.exists():
        shutil.copy2(str(real_models), str(base_path / "company" / "models.yaml"))
