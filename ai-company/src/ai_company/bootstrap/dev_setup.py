"""Developer machine bootstrap for AI Company Builder.

Prepares a fresh checkout for development:
- installs the uv package manager
- creates the virtual environment
- synchronizes packages with uv (also installs the project's dependencies)
- installs pre-commit hooks
- verifies Python, Ollama, OpenCode, Git, and required environment variables

Every step is idempotent: re-running the bootstrap is safe, skips already-done
work, and produces the same result shape.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

MIN_PYTHON = (3, 12)
DEFAULT_ENV_FILE = ".env"
DEFAULT_ENV_TEMPLATE = ".env.example"

# Fallback required vars when no .env.example is present in the project.
FALLBACK_REQUIRED_ENV_VARS = (
    "OPENCODE_API_KEY",
    "DEEPSEEK_API_KEY",
    "GEMINI_API_KEY",
    "KIMI_API_KEY",
    "DASHBOARD_API_KEY",
)

_PLACEHOLDER_HINTS = ("your_", "changeme", "placeholder", "example", "xxxx")


@dataclass
class StepResult:
    """Outcome of a single bootstrap step."""

    name: str
    ok: bool
    message: str
    severity: str = "ok"
    details: dict[str, object] = field(default_factory=dict)


def _parse_env_file(path: Path) -> dict[str, str]:
    """Parse a ``KEY=VALUE`` env file (ignoring comments and blank lines)."""
    parsed: dict[str, str] = {}
    if not path.exists():
        return parsed

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            parsed[key] = value
    return parsed


def _is_placeholder(value: str) -> bool:
    """True when a value looks like an unfilled template placeholder."""
    lowered = value.lower()
    return not lowered or any(hint in lowered for hint in _PLACEHOLDER_HINTS)


class DevBootstrap:
    """Idempotent developer-machine bootstrap for the AI Company project."""

    def __init__(
        self,
        project_root: str | Path | None = None,
        env_file: str | Path = DEFAULT_ENV_FILE,
        required_env_vars: Sequence[str] | None = None,
    ) -> None:
        self.project_root = self._resolve_project_root(project_root)
        self.env_file = self.project_root / env_file
        self.env_template = self.project_root / DEFAULT_ENV_TEMPLATE
        self.required_env_vars = (
            list(required_env_vars)
            if required_env_vars is not None
            else self._discover_required_env_vars()
        )
        self._steps: list[StepResult] = []

    # ------------------------------------------------------------------
    # Orchestration
    # ------------------------------------------------------------------

    def run(self) -> dict[str, object]:
        """Run every bootstrap step and return a machine-readable summary."""
        self._steps = []
        self.ensure_uv()
        self.create_venv()
        self.sync_packages()
        self.install_hooks()
        self.verify_python()
        self.verify_ollama()
        self.verify_opencode()
        self.verify_git()
        self.verify_env_vars()

        failures = [s for s in self._steps if s.severity == "fail"]
        warnings = [s for s in self._steps if s.severity == "warn"]
        return {
            "project_root": str(self.project_root),
            "ok": not failures,
            "errors": len(failures),
            "warnings": len(warnings),
            "steps": [vars(step) for step in self._steps],
        }

    # ------------------------------------------------------------------
    # Install / sync steps (all idempotent)
    # ------------------------------------------------------------------

    def ensure_uv(self) -> StepResult:
        """Install the uv package manager if it is missing."""
        if self._which("uv"):
            code, out = self._run(["uv", "--version"])
            if code == 0:
                return self._record(
                    "package-manager", True, f"uv: {out}", details={"installed": True}
                )
            return self._record(
                "package-manager", False, f"uv --version failed: {out}", severity="fail"
            )

        pip = self._which("pip")
        if not pip:
            return self._record(
                "package-manager",
                False,
                "uv missing and pip unavailable — install uv from https://docs.astral.sh/uv/",
                severity="fail",
            )

        code, out = self._run([pip, "install", "--quiet", "uv"])
        if code != 0:
            return self._record(
                "package-manager",
                False,
                f"pip install uv failed: {out[-300:]}",
                severity="fail",
            )
        if self._which("uv"):
            return self._record(
                "package-manager",
                True,
                "uv installed via pip",
                details={"installed": True},
            )
        return self._record(
            "package-manager",
            False,
            "uv installed via pip but not on PATH — restart your shell",
            severity="warn",
        )

    def create_venv(self) -> StepResult:
        """Create .venv with uv if it does not already exist."""
        venv_python = self.venv_python_path()
        if venv_python.exists():
            return self._record("virtualenv", True, f".venv exists ({self.project_root / '.venv'})")

        code, out = self._run(["uv", "venv", str(self.project_root / ".venv")])
        if code == 0 and venv_python.exists():
            return self._record("virtualenv", True, "created .venv", details={"created": True})
        return self._record("virtualenv", False, f"uv venv failed: {out[-300:]}", severity="fail")

    def sync_packages(self, extra: str = "dev") -> StepResult:
        """Install and synchronize all dependencies from the uv lockfile."""
        code, out = self._run(["uv", "sync", "--extra", extra], timeout=900)
        if code == 0:
            return self._record(
                "dependencies",
                True,
                f"uv sync --extra {extra} (up to date with uv.lock)",
            )
        return self._record("dependencies", False, f"uv sync failed: {out[-500:]}", severity="fail")

    def install_hooks(self) -> StepResult:
        """Install pre-commit hooks (non-blocking)."""
        code, out = self._run(["uv", "run", "pre-commit", "install"])
        if code == 0:
            return self._record("hooks", True, "pre-commit hooks installed")
        return self._record(
            "hooks", False, f"pre-commit install failed: {out[-300:]}", severity="warn"
        )

    # ------------------------------------------------------------------
    # Verification steps
    # ------------------------------------------------------------------

    def verify_python(self) -> StepResult:
        """Verify Python >= 3.12 is available."""
        exe = self._which("python")
        if not exe:
            venv_python = self.venv_python_path()
            if not venv_python.exists():
                return self._record("python", False, "python not found on PATH", severity="fail")
            exe = str(venv_python)

        code, out = self._run([exe, "--version"])
        if code != 0:
            return self._record("python", False, f"python --version failed: {out}", severity="fail")

        match = re.search(r"Python (\d+)\.(\d+)(?:\.(\d+))?", out)
        if not match:
            return self._record(
                "python", False, f"unexpected version output: {out}", severity="warn"
            )

        major, minor = int(match.group(1)), int(match.group(2))
        ok = (major, minor) >= MIN_PYTHON
        min_version = f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]}"
        version = f"{major}.{minor}"
        return self._record(
            "python",
            ok,
            f"Python {version} (requires >= {min_version})",
            severity="ok" if ok else "fail",
            details={"version": version, "minimum": min_version},
        )

    def verify_ollama(self) -> StepResult:
        """Verify the Ollama binary is installed and its server is reachable."""
        exe = self._which("ollama")
        if not exe:
            return self._record(
                "ollama",
                False,
                "ollama not found — install from https://ollama.com",
                severity="fail",
            )

        code, out = self._run([exe, "--version"])
        if code != 0:
            return self._record("ollama", False, f"ollama --version failed: {out}", severity="fail")

        reachable = self._ollama_reachable()
        if reachable is True:
            return self._record(
                "ollama", True, f"ollama server reachable: {out}", details={"server": "ok"}
            )
        if reachable is False:
            return self._record(
                "ollama",
                True,
                f"ollama installed but server not running: {out}",
                severity="warn",
                details={"server": "unreachable"},
            )
        return self._record("ollama", True, f"ollama installed: {out}")

    def verify_opencode(self) -> StepResult:
        """Verify the OpenCode CLI is installed."""
        exe = self._which("opencode")
        if not exe:
            return self._record(
                "opencode",
                False,
                "opencode not found — install from https://opencode.ai",
                severity="fail",
            )

        code, out = self._run([exe, "--version"])
        if code != 0:
            return self._record(
                "opencode", False, f"opencode --version failed: {out}", severity="fail"
            )
        return self._record("opencode", True, f"opencode: {out or '(no version output)'}")

    def verify_git(self) -> StepResult:
        """Verify Git is installed."""
        exe = self._which("git")
        if not exe:
            return self._record(
                "git", False, "git not found — install from https://git-scm.com", severity="fail"
            )

        code, out = self._run([exe, "--version"])
        if code != 0:
            return self._record("git", False, f"git --version failed: {out}", severity="fail")
        return self._record("git", True, f"git: {out}")

    def verify_env_vars(self) -> StepResult:
        """Verify all required environment variables are configured."""
        file_vars = _parse_env_file(self.env_file)
        configured: list[str] = []
        missing: list[str] = []

        for var in self.required_env_vars:
            value = os.environ.get(var) or file_vars.get(var)
            if value and not _is_placeholder(value):
                configured.append(var)
            else:
                missing.append(var)

        source = f" from {self.env_file.name}" if self.env_file.exists() else ""
        details: dict[str, object] = {
            "required": list(self.required_env_vars),
            "configured": configured,
            "missing": missing,
            "env_file": str(self.env_file) if self.env_file.exists() else None,
        }

        if not missing:
            return self._record(
                "environment",
                True,
                f"{len(configured)}/{len(self.required_env_vars)} required variables configured{source}",
                details=details,
            )

        return self._record(
            "environment",
            False,
            f"missing {len(missing)}/{len(self.required_env_vars)} required variables: "
            f"{', '.join(missing)}; copy {DEFAULT_ENV_TEMPLATE} to {self.env_file.name} and fill in values",
            severity="fail",
            details=details,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _record(
        self,
        name: str,
        ok: bool,
        message: str,
        severity: str = "ok",
        details: dict[str, object] | None = None,
    ) -> StepResult:
        step = StepResult(
            name=name, ok=ok, message=message, severity=severity, details=details or {}
        )
        self._steps.append(step)
        return step

    def _which(self, tool: str) -> str | None:
        """Return the path to an executable on PATH, or None."""
        return shutil.which(tool)

    def _run(self, cmd: Sequence[str], timeout: int = 600) -> tuple[int, str]:
        """Run a command in the project root; returns (exit_code, output)."""
        try:
            result = subprocess.run(
                list(cmd),
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.project_root),
            )
        except (subprocess.SubprocessError, FileNotFoundError) as exc:
            return 1, str(exc)
        output = (result.stdout or "") + (result.stderr or "")
        return result.returncode, output.strip()

    def _ollama_reachable(self) -> bool | None:
        """Check if the Ollama server answers; None means it was not checked."""
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
        try:
            with urllib.request.urlopen(f"{host}/api/tags", timeout=3) as resp:
                return bool(resp.status == 200)
        except Exception:  # noqa: BLE001 - reachability check must not crash
            return False

    def venv_python_path(self) -> Path:
        """Path to the interpreter inside the project virtual environment."""
        if os.name == "nt":
            return self.project_root / ".venv" / "Scripts" / "python.exe"
        return self.project_root / ".venv" / "bin" / "python"

    def _discover_required_env_vars(self) -> list[str]:
        """Read required vars from .env.example, falling back to a default set."""
        keys = [k for k in _parse_env_file(self.env_template) if k]
        return keys or list(FALLBACK_REQUIRED_ENV_VARS)

    @staticmethod
    def _resolve_project_root(start: str | Path | None = None) -> Path:
        """Find the project root (dir containing pyproject.toml).

        An explicit ``start`` is used as-is; otherwise the current directory
        is scanned, then its parents, then direct subdirectories.
        """
        if start is not None:
            return Path(start).resolve()
        cwd = Path.cwd()
        for parent in (cwd, *cwd.parents):
            if (parent / "pyproject.toml").exists():
                return parent
        for child in cwd.iterdir():
            if child.is_dir() and (child / "pyproject.toml").exists():
                return child
        return cwd
