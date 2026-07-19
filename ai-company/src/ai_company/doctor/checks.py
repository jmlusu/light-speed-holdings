"""
System health checks for the AI Company Builder.

Each check returns a CheckResult. Additional metadata is available
in the ``details`` dict for programmatic consumers.
"""

from __future__ import annotations

import json
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str
    severity: str = "info"
    details: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Original checks (1-6)
# ---------------------------------------------------------------------------


def check_registry_exists(registry_path: str = "company-registry.yaml") -> CheckResult:
    path = Path(registry_path)
    if path.exists():
        return CheckResult("Registry File", True, f"Found: {path}")
    return CheckResult("Registry File", False, f"Missing: {path}", severity="error")


def check_registry_valid(registry_path: str = "company-registry.yaml") -> CheckResult:
    path = Path(registry_path)
    if not path.exists():
        return CheckResult(
            "Registry Valid", False, "Registry file not found", severity="error"
        )

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not data or "company" not in data:
            return CheckResult(
                "Registry Valid", False, "Invalid registry structure", severity="error"
            )

        agents = data.get("company", {}).get("agents", [])
        if not agents:
            return CheckResult(
                "Registry Valid", False, "No agents defined", severity="warning"
            )

        return CheckResult("Registry Valid", True, f"{len(agents)} agents defined")
    except yaml.YAMLError as e:
        return CheckResult(
            "Registry Valid", False, f"YAML error: {e}", severity="error"
        )


def check_models_importable() -> CheckResult:
    try:
        import ai_company.models.models  # noqa: F401

        return CheckResult("Models Import", True, "All models importable")
    except ImportError as e:
        return CheckResult(
            "Models Import", False, f"Import error: {e}", severity="error"
        )


def check_message_bus() -> CheckResult:
    try:
        from ai_company.orchestrator.message_bus import MessageBus

        MessageBus()
        return CheckResult("MessageBus", True, "MessageBus initialized")
    except Exception as e:
        return CheckResult("MessageBus", False, f"Error: {e}", severity="error")


def check_opencode_directory() -> CheckResult:
    opencode_dir = Path(".opencode")
    if opencode_dir.exists():
        return CheckResult("OpenCode Directory", True, "Directory exists")
    return CheckResult(
        "OpenCode Directory", False, "Directory missing", severity="warning"
    )


def check_company_configs() -> CheckResult:
    config_dir = Path("company")
    if not config_dir.exists():
        return CheckResult(
            "Company Configs", False, "company/ directory missing", severity="warning"
        )

    yaml_files = list(config_dir.glob("*.yaml"))
    if not yaml_files:
        return CheckResult(
            "Company Configs", False, "No YAML configs found", severity="warning"
        )

    return CheckResult("Company Configs", True, f"{len(yaml_files)} config files found")


# ---------------------------------------------------------------------------
# New checks (7-14)
# ---------------------------------------------------------------------------


def check_python_version() -> CheckResult:
    """Verify Python version >= 3.12."""
    version = sys.version_info
    ok = version >= (3, 12)
    msg = f"Python {version.major}.{version.minor}.{version.micro}"
    return CheckResult(
        name="Python Version",
        passed=ok,
        message=msg,
        severity="ok" if ok else "error",
        details={"expected": ">=3.12", "actual": f"{version.major}.{version.minor}.{version.micro}"},
    )


def check_dependencies() -> CheckResult:
    """Check that all required packages are importable."""
    required = ["typer", "pydantic", "fastapi", "jinja2", "yaml", "httpx", "rich"]
    missing: list[str] = []
    installed: list[str] = []

    for pkg in required:
        try:
            __import__(pkg)
            installed.append(pkg)
        except ImportError:
            missing.append(pkg)

    return CheckResult(
        name="Dependencies",
        passed=len(missing) == 0,
        message=f"{len(required) - len(missing)}/{len(required)} installed",
        severity="ok" if not missing else "error",
        details={"installed": installed, "missing": missing},
    )


def check_agent_files() -> CheckResult:
    """Verify .opencode/agents/ has generated .md files."""
    agents_dir = Path(".opencode/agents")
    if not agents_dir.exists():
        return CheckResult(
            name="Agent Files",
            passed=False,
            message="Directory .opencode/agents/ not found",
            severity="error",
        )

    md_files = list(agents_dir.glob("*.md"))
    return CheckResult(
        name="Agent Files",
        passed=bool(md_files),
        message=f"{len(md_files)} agent files found",
        severity="ok" if md_files else "warning",
        details={"count": len(md_files), "files": [f.name for f in md_files]},
    )


def check_inbox_health() -> CheckResult:
    """Check inbox.json is valid JSON with no stuck tasks."""
    inbox_path = Path(".opencode/inbox.json")

    if not inbox_path.exists():
        return CheckResult(
            name="Inbox",
            passed=True,
            message="No inbox (clean slate)",
        )

    try:
        tasks = json.loads(inbox_path.read_text(encoding="utf-8"))
        stuck = [t for t in tasks if t.get("status") == "in_progress"]
        pending = [t for t in tasks if t.get("status") == "pending"]
        return CheckResult(
            name="Inbox",
            passed=True,
            message=f"{len(pending)} pending, {len(stuck)} in-progress, {len(tasks)} total",
            details={
                "pending": len(pending),
                "in_progress": len(stuck),
                "total": len(tasks),
            },
        )
    except Exception as e:
        return CheckResult(
            name="Inbox",
            passed=False,
            message=f"Invalid JSON: {e}",
            severity="error",
        )


def check_memory_engine() -> CheckResult:
    """Verify memory store initializes correctly."""
    try:
        from ai_company.memory.engine import MemoryStore

        store = MemoryStore()
        stats = store.stats()
        total = sum(stats.values())
        return CheckResult(
            name="Memory Engine",
            passed=True,
            message=f"{total} memories across {len(stats)} types",
            details=stats,
        )
    except Exception as e:
        return CheckResult(
            name="Memory Engine",
            passed=False,
            message=str(e),
            severity="error",
        )


def check_disk_space() -> CheckResult:
    """Check available disk space (warns below 1 GB free)."""
    total, used, free = shutil.disk_usage(".")
    free_gb = free / (1024**3)
    total_gb = total / (1024**3)
    ok = free_gb > 1.0
    return CheckResult(
        name="Disk Space",
        passed=ok,
        message=f"{free_gb:.1f} GB free of {total_gb:.1f} GB",
        severity="ok" if ok else "warning",
        details={"free_gb": round(free_gb, 2), "total_gb": round(total_gb, 2)},
    )


def check_cost_tracker() -> CheckResult:
    """Check cost tracker state."""
    log_path = Path("results/cost_log.jsonl")

    if not log_path.exists():
        return CheckResult(
            name="Cost Tracker",
            passed=True,
            message="No cost log yet",
        )

    try:
        line_count = sum(1 for _ in log_path.open(encoding="utf-8"))
        return CheckResult(
            name="Cost Tracker",
            passed=True,
            message=f"{line_count} usage records in cost_log.jsonl",
            details={"record_count": line_count},
        )
    except Exception as e:
        return CheckResult(
            name="Cost Tracker",
            passed=False,
            message=f"Error reading cost log: {e}",
            severity="error",
        )


def check_llm_providers() -> CheckResult:
    """Check if configured LLM providers are reachable."""
    import os

    providers: dict[str, dict[str, Any]] = {}

    # --- Ollama ---
    ollama_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    try:
        import httpx

        resp = httpx.get(f"{ollama_url}/api/tags", timeout=3.0)
        if resp.status_code == 200:
            tags = resp.json().get("models", [])
            providers["ollama"] = {
                "status": "ok",
                "message": f"{len(tags)} models available",
                "models": [m.get("name", "") for m in tags],
            }
        else:
            providers["ollama"] = {
                "status": "error",
                "message": f"HTTP {resp.status_code}",
            }
    except Exception as e:
        providers["ollama"] = {"status": "unreachable", "message": str(e)}

    # --- OpenAI ---
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    providers["openai"] = {
        "status": "ok" if openai_key else "no_key",
        "message": "API key configured" if openai_key else "OPENAI_API_KEY not set",
    }

    # --- Anthropic ---
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    providers["anthropic"] = {
        "status": "ok" if anthropic_key else "no_key",
        "message": (
            "API key configured" if anthropic_key else "ANTHROPIC_API_KEY not set"
        ),
    }

    reachable = sum(
        1 for p in providers.values() if p["status"] in ("ok", "no_key")
    )
    total = len(providers)
    all_ok = all(p["status"] in ("ok", "no_key") for p in providers.values())

    return CheckResult(
        name="LLM Providers",
        passed=all_ok,
        message=f"{reachable}/{total} providers configured",
        severity="ok" if all_ok else "warning",
        details=providers,
    )


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

ALL_CHECKS = [
    check_registry_exists,
    check_registry_valid,
    check_models_importable,
    check_message_bus,
    check_opencode_directory,
    check_company_configs,
    check_python_version,
    check_dependencies,
    check_agent_files,
    check_inbox_health,
    check_memory_engine,
    check_disk_space,
    check_cost_tracker,
    check_llm_providers,
]


def run_all_checks() -> list[CheckResult]:
    """Execute every registered check and return results."""
    return [fn() for fn in ALL_CHECKS]
