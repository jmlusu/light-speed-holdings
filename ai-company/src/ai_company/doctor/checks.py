"""
System health checks for the AI Company Builder.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import yaml


@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str
    severity: str = "info"


def check_registry_exists(registry_path: str = "company-registry.yaml") -> CheckResult:
    path = Path(registry_path)
    if path.exists():
        return CheckResult("Registry File", True, f"Found: {path}")
    return CheckResult("Registry File", False, f"Missing: {path}", severity="error")


def check_registry_valid(registry_path: str = "company-registry.yaml") -> CheckResult:
    path = Path(registry_path)
    if not path.exists():
        return CheckResult("Registry Valid", False, "Registry file not found", severity="error")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not data or "company" not in data:
            return CheckResult("Registry Valid", False, "Invalid registry structure", severity="error")

        agents = data.get("company", {}).get("agents", [])
        if not agents:
            return CheckResult("Registry Valid", False, "No agents defined", severity="warning")

        return CheckResult("Registry Valid", True, f"{len(agents)} agents defined")
    except yaml.YAMLError as e:
        return CheckResult("Registry Valid", False, f"YAML error: {e}", severity="error")


def check_models_importable() -> CheckResult:
    try:
        from ai_company.models.models import Executive, Specialist, Department, Company
        return CheckResult("Models Import", True, "All models importable")
    except ImportError as e:
        return CheckResult("Models Import", False, f"Import error: {e}", severity="error")


def check_message_bus() -> CheckResult:
    try:
        from ai_company.orchestrator.message_bus import MessageBus
        bus = MessageBus()
        return CheckResult("MessageBus", True, "MessageBus initialized")
    except Exception as e:
        return CheckResult("MessageBus", False, f"Error: {e}", severity="error")


def check_opencode_directory() -> CheckResult:
    opencode_dir = Path(".opencode")
    if opencode_dir.exists():
        return CheckResult("OpenCode Directory", True, "Directory exists")
    return CheckResult("OpenCode Directory", False, "Directory missing", severity="warning")


def check_company_configs() -> CheckResult:
    config_dir = Path("company")
    if not config_dir.exists():
        return CheckResult("Company Configs", False, "company/ directory missing", severity="warning")

    yaml_files = list(config_dir.glob("*.yaml"))
    if not yaml_files:
        return CheckResult("Company Configs", False, "No YAML configs found", severity="warning")

    return CheckResult("Company Configs", True, f"{len(yaml_files)} config files found")


def run_all_checks() -> List[CheckResult]:
    checks = [
        check_registry_exists(),
        check_registry_valid(),
        check_models_importable(),
        check_message_bus(),
        check_opencode_directory(),
        check_company_configs(),
    ]
    return checks
