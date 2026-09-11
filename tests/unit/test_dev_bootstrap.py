"""Tests for the developer-machine bootstrap (DevBootstrap + CLI)."""

from __future__ import annotations

import json
import tempfile
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from ai_company.bootstrap import DevBootstrap
from ai_company.bootstrap.dev_setup import (
    FALLBACK_REQUIRED_ENV_VARS,
    _is_placeholder,
    _parse_env_file,
)
from ai_company.cli.bootstrap import app

runner = CliRunner()


def _venv_target(bootstrap: DevBootstrap) -> Path:
    return bootstrap.venv_python_path()


def _fake_run(bootstrap: DevBootstrap, cmd: list[str], timeout: int = 600) -> tuple[int, str]:
    """Deterministic stand-in for subprocess calls (creates the venv on demand)."""
    name, args = cmd[0], cmd[1:]
    if name == "uv" and args and args[0] == "venv":
        target = _venv_target(bootstrap)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.touch()
        return 0, ""
    if name == "uv" and args == ["--version"]:
        return 0, "uv 0.11.32"
    if name == "uv" and args and args[0] == "sync":
        return 0, "Synced 10 packages"
    if name == "uv" and args and args[0] == "run":
        return 0, "pre-commit installed"
    if name == "pip":
        return 0, ""
    if "python" in name:
        return 0, "Python 3.12.10"
    if "ollama" in name:
        return 0, "ollama version 0.5.0"
    if "opencode" in name:
        return 0, "opencode 0.1.0"
    if "git" in name:
        return 0, "git version 2.55.0"
    return 0, ""


def _default_which() -> dict[str, str]:
    return {
        "uv": "/usr/bin/uv",
        "python": "/usr/bin/python",
        "ollama": "/usr/bin/ollama",
        "opencode": "/usr/bin/opencode",
        "git": "/usr/bin/git",
    }


@contextmanager
def _patched_bootstrap(
    tmp_path: Path,
    which: dict[str, str] | None = None,
    required_env_vars: list[str] | None = FALLBACK_REQUIRED_ENV_VARS,
):
    """Yield a DevBootstrap with all external calls mocked (plus a command log)."""
    boot = DevBootstrap(project_root=tmp_path, required_env_vars=required_env_vars)
    which_map = which if which is not None else _default_which()
    commands: list[list[str]] = []

    def record_run(bootstrap: DevBootstrap, cmd: list[str], timeout: int = 600) -> tuple[int, str]:
        commands.append(list(cmd))
        return _fake_run(bootstrap, cmd, timeout)

    with (
        patch.object(DevBootstrap, "_which", new=lambda self, tool: which_map.get(tool)),
        patch.object(DevBootstrap, "_run", new=record_run),
        patch.object(DevBootstrap, "_ollama_reachable", new=lambda self: None),
    ):
        yield boot, commands


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def test_parse_env_file(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n"
        "# comment\n"
        "OPENCODE_API_KEY=sk-1234\n"
        "export GEMINI_API_KEY='abc'\n"
        'DASHBOARD_CORS_ORIGINS="http://localhost:3000"\n'
        "INVALID_LINE_NO_EQUALS\n"
        "\n",
        encoding="utf-8",
    )
    parsed = _parse_env_file(env_file)
    assert parsed == {
        "OPENCODE_API_KEY": "sk-1234",
        "GEMINI_API_KEY": "abc",
        "DASHBOARD_CORS_ORIGINS": "http://localhost:3000",
    }


def test_parse_env_file_missing(tmp_path: Path) -> None:
    assert _parse_env_file(tmp_path / "nope.env") == {}


def test_is_placeholder() -> None:
    assert _is_placeholder("")
    assert _is_placeholder("your_opencode_api_key_here")
    assert _is_placeholder("changeme")
    assert _is_placeholder("PLACEHOLDER")
    assert not _is_placeholder("sk-abc123")
    assert not _is_placeholder("http://localhost:3000")


# ---------------------------------------------------------------------------
# Project root detection
# ---------------------------------------------------------------------------


def test_resolve_project_root_with_explicit_start(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("", encoding="utf-8")
    assert DevBootstrap._resolve_project_root(tmp_path) == tmp_path


def test_resolve_project_root_autodetect_from_cwd(monkeypatch) -> None:
    outside = Path(tempfile.mkdtemp())
    monkeypatch.chdir(outside)
    assert DevBootstrap._resolve_project_root() == outside


def test_resolve_project_root_autodetect_subdirectory(monkeypatch) -> None:
    outside = Path(tempfile.mkdtemp())
    sub = outside / "ai-company"
    sub.mkdir()
    (sub / "pyproject.toml").write_text("", encoding="utf-8")
    monkeypatch.chdir(outside)
    assert DevBootstrap._resolve_project_root() == sub


# ---------------------------------------------------------------------------
# Install / sync steps
# ---------------------------------------------------------------------------


def test_ensure_uv_skips_when_present(tmp_path: Path) -> None:
    with _patched_bootstrap(tmp_path) as (boot, _):
        step = boot.ensure_uv()
    assert step.ok
    assert step.name == "package-manager"


def test_ensure_uv_installs_via_pip(tmp_path: Path) -> None:
    boot = DevBootstrap(project_root=tmp_path, required_env_vars=[])
    installed = {"done": False}

    def which(self, tool: str) -> str | None:
        if tool == "uv":
            return "/usr/bin/uv" if installed["done"] else None
        if tool == "pip":
            return "/usr/bin/pip"
        return None

    def fake_install(
        bootstrap: DevBootstrap, cmd: list[str], timeout: int = 600
    ) -> tuple[int, str]:
        if "pip" in cmd[0]:
            installed["done"] = True
            return 0, ""
        return _fake_run(bootstrap, cmd, timeout)

    with (
        patch.object(DevBootstrap, "_which", new=which),
        patch.object(DevBootstrap, "_run", new=fake_install),
    ):
        step = boot.ensure_uv()

    assert step.ok
    assert "installed via pip" in step.message


def test_ensure_uv_fails_when_missing(tmp_path: Path) -> None:
    with _patched_bootstrap(tmp_path, which={}) as (boot, _):
        step = boot.ensure_uv()
    assert not step.ok
    assert step.severity == "fail"


def test_create_venv_is_idempotent(tmp_path: Path) -> None:
    with _patched_bootstrap(tmp_path) as (boot, commands):
        first = boot.create_venv()
        second = boot.create_venv()
    assert first.ok
    assert second.ok
    assert "exists" in second.message
    venv_calls = [c for c in commands if c[:2] == ["uv", "venv"]]
    assert len(venv_calls) == 1


def test_sync_packages_ok(tmp_path: Path) -> None:
    with _patched_bootstrap(tmp_path) as (boot, _):
        step = boot.sync_packages()
    assert step.ok


# ---------------------------------------------------------------------------
# Verification steps
# ---------------------------------------------------------------------------


def test_verify_python_ok(tmp_path: Path) -> None:
    with _patched_bootstrap(tmp_path) as (boot, _):
        step = boot.verify_python()
    assert step.ok
    assert step.details["version"] == "3.12"


def test_verify_python_too_old(tmp_path: Path) -> None:
    def old_python(bootstrap: DevBootstrap, cmd: list[str], timeout: int = 600) -> tuple[int, str]:
        if "python" in cmd[0]:
            return 0, "Python 3.11.9"
        return _fake_run(bootstrap, cmd, timeout)

    with (
        _patched_bootstrap(tmp_path) as (boot, _),
        patch.object(DevBootstrap, "_run", new=old_python),
    ):
        step = boot.verify_python()
    assert not step.ok
    assert step.severity == "fail"


def test_verify_python_missing(tmp_path: Path) -> None:
    with _patched_bootstrap(tmp_path, which={}) as (boot, _):
        step = boot.verify_python()
    assert not step.ok
    assert step.severity == "fail"


def test_verify_ollama_ok(tmp_path: Path) -> None:
    with _patched_bootstrap(tmp_path) as (boot, _):
        step = boot.verify_ollama()
    assert step.ok


def test_verify_ollama_server_down(tmp_path: Path) -> None:
    with (
        _patched_bootstrap(tmp_path) as (boot, _),
        patch.object(DevBootstrap, "_ollama_reachable", new=lambda self: False),
    ):
        step = boot.verify_ollama()
    assert step.ok
    assert step.severity == "warn"


def test_verify_ollama_missing(tmp_path: Path) -> None:
    with _patched_bootstrap(tmp_path, which={"ollama": None}) as (boot, _):
        step = boot.verify_ollama()
    assert not step.ok
    assert step.severity == "fail"


def test_verify_opencode_ok(tmp_path: Path) -> None:
    with _patched_bootstrap(tmp_path) as (boot, _):
        step = boot.verify_opencode()
    assert step.ok


def test_verify_opencode_missing(tmp_path: Path) -> None:
    with _patched_bootstrap(tmp_path, which={"opencode": None}) as (boot, _):
        step = boot.verify_opencode()
    assert not step.ok
    assert step.severity == "fail"


def test_verify_git_ok(tmp_path: Path) -> None:
    with _patched_bootstrap(tmp_path) as (boot, _):
        step = boot.verify_git()
    assert step.ok


def test_verify_git_missing(tmp_path: Path) -> None:
    with _patched_bootstrap(tmp_path, which={"git": None}) as (boot, _):
        step = boot.verify_git()
    assert not step.ok
    assert step.severity == "fail"


# ---------------------------------------------------------------------------
# Environment variables
# ---------------------------------------------------------------------------


def test_verify_env_vars_all_configured(tmp_path: Path, monkeypatch) -> None:
    for var in FALLBACK_REQUIRED_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    (tmp_path / ".env").write_text(
        "OPENCODE_API_KEY=sk-1\n"
        "DEEPSEEK_API_KEY=sk-2\n"
        "GEMINI_API_KEY=sk-3\n"
        "KIMI_API_KEY=sk-4\n"
        "DASHBOARD_API_KEY=sk-5\n",
        encoding="utf-8",
    )
    with _patched_bootstrap(tmp_path) as (boot, _):
        step = boot.verify_env_vars()
    assert step.ok
    assert step.details["configured"] == list(FALLBACK_REQUIRED_ENV_VARS)


def test_verify_env_vars_missing(tmp_path: Path, monkeypatch) -> None:
    for var in FALLBACK_REQUIRED_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    (tmp_path / ".env").write_text("OPENCODE_API_KEY=sk-1\n", encoding="utf-8")
    with _patched_bootstrap(tmp_path) as (boot, _):
        step = boot.verify_env_vars()
    assert not step.ok
    assert step.severity == "fail"
    assert "OPENCODE_API_KEY" not in step.details["missing"]
    assert "DASHBOARD_API_KEY" in step.details["missing"]


def test_verify_env_vars_placeholder_counts_missing(tmp_path: Path, monkeypatch) -> None:
    for var in FALLBACK_REQUIRED_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    (tmp_path / ".env").write_text(
        "OPENCODE_API_KEY=your_opencode_api_key_here\n", encoding="utf-8"
    )
    with _patched_bootstrap(tmp_path) as (boot, _):
        step = boot.verify_env_vars()
    assert not step.ok
    assert "OPENCODE_API_KEY" in step.details["missing"]


def test_verify_env_vars_prefers_environment(tmp_path: Path, monkeypatch) -> None:
    for var in FALLBACK_REQUIRED_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("OPENCODE_API_KEY", "sk-from-env")
    with _patched_bootstrap(tmp_path) as (boot, _):
        step = boot.verify_env_vars()
    assert "OPENCODE_API_KEY" not in step.details["missing"]


def test_verify_env_vars_no_requirements(tmp_path: Path, monkeypatch) -> None:
    for var in FALLBACK_REQUIRED_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    with _patched_bootstrap(tmp_path, required_env_vars=[]) as (boot, _):
        step = boot.verify_env_vars()
    assert step.ok
    assert step.details["missing"] == []


# ---------------------------------------------------------------------------
# Full run
# ---------------------------------------------------------------------------


def test_run_is_idempotent(tmp_path: Path) -> None:
    with _patched_bootstrap(tmp_path, required_env_vars=[]) as (boot, commands):
        first = boot.run()
        second = boot.run()
    assert first["ok"] is True
    assert second["ok"] is True
    assert first["errors"] == 0
    assert second["errors"] == 0
    assert len(first["steps"]) == len(second["steps"])
    venv_calls = [c for c in commands if c[:2] == ["uv", "venv"]]
    assert len(venv_calls) == 1


def test_run_reports_failures(tmp_path: Path) -> None:
    with _patched_bootstrap(tmp_path, which={"opencode": None}) as (boot, _):
        summary = boot.run()
    assert summary["ok"] is False
    assert summary["errors"] >= 1
    names = {step["name"] for step in summary["steps"]}
    assert "opencode" in names


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


class _FakeBootstrap:
    def __init__(self, project_root=None, env_file=".env"):
        self.project_root = project_root
        self.env_file = env_file

    def run(self) -> dict:
        return {
            "project_root": str(self.project_root or ""),
            "ok": True,
            "errors": 0,
            "warnings": 0,
            "steps": [
                {
                    "name": "python",
                    "ok": True,
                    "message": "Python 3.12.10",
                    "severity": "ok",
                    "details": {},
                }
            ],
        }


def test_cli_bootstrap_json(tmp_path: Path) -> None:
    with patch("ai_company.cli.bootstrap.DevBootstrap", new=_FakeBootstrap):
        result = runner.invoke(app, ["run", "--json", "--project-root", str(tmp_path)])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["ok"] is True
    assert data["steps"][0]["name"] == "python"


def test_cli_bootstrap_bare_invocation(tmp_path: Path) -> None:
    with patch("ai_company.cli.bootstrap.DevBootstrap", new=_FakeBootstrap):
        result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "Developer machine bootstrap" in result.output


def test_cli_bootstrap_exit_code_on_failure(tmp_path: Path) -> None:
    class _FailingBootstrap(_FakeBootstrap):
        def run(self) -> dict:
            summary = super().run()
            summary["ok"] = False
            summary["errors"] = 1
            return summary

    with patch("ai_company.cli.bootstrap.DevBootstrap", new=_FailingBootstrap):
        result = runner.invoke(app, ["run", "--project-root", str(tmp_path)])
    assert result.exit_code == 1
