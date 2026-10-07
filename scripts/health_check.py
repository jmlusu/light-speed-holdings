#!/usr/bin/env python3
"""
Canonical health check for LightSpeed Holdings repository.

Run this script to verify the repository is in a healthy state.
Exit codes:
  0 = healthy
  1 = unhealthy (details printed to stderr)
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_cmd(cmd: list[str], cwd: Path = None) -> tuple[int, str, str]:
    """Run a command and return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        cmd,
        cwd=cwd or REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def check_ruff() -> bool:
    """Check ruff linting passes."""
    code, out, err = run_cmd(["uv", "run", "ruff", "check", "src/"])
    if code != 0:
        print(f"ruff FAILED:\n{out}\n{err}", file=sys.stderr)
        return False
    print("ruff: PASS")
    return True


def check_mypy() -> bool:
    """Check mypy type checking passes."""
    code, out, err = run_cmd(["uv", "run", "mypy", "src/"])
    if code != 0:
        print(f"mypy FAILED:\n{out}\n{err}", file=sys.stderr)
        return False
    print("mypy: PASS")
    return True


def check_pytest() -> bool:
    """Check critical pytest suite passes."""
    code, out, err = run_cmd(
        [
            "uv",
            "run",
            "pytest",
            "--tb=line",
            "-q",
            "-x",
            "--ignore=tests/integration",
            "-k",
            "not test_endpoint_response_time_p95",
        ]
    )
    if code != 0:
        print(f"pytest FAILED:\n{out}\n{err}", file=sys.stderr)
        return False
    print("pytest: PASS")
    return True


def check_generator() -> bool:
    """Check agent generator round-trip works."""
    code, out, err = run_cmd(
        [
            "uv",
            "run",
            "python",
            "-c",
            "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()",
        ]
    )
    if code != 0:
        print(f"generator FAILED:\n{out}\n{err}", file=sys.stderr)
        return False
    print("generator: PASS")
    return True


def check_cli() -> bool:
    """Check CLI entry point works."""
    code, out, err = run_cmd(["uv", "run", "ai-company", "--help"])
    if code != 0:
        print(f"CLI FAILED:\n{out}\n{err}", file=sys.stderr)
        return False
    print("CLI: PASS")
    return True


def check_lint_ecl() -> bool:
    """Check ECL lint passes."""
    code, out, err = run_cmd(["pwsh", "scripts/maintenance/lint-ecl.ps1"])
    if code != 0:
        print(f"lint-ecl FAILED:\n{out}\n{err}", file=sys.stderr)
        return False
    print("lint-ecl: PASS")
    return True


def main() -> int:
    """Run all health checks."""
    checks = [
        ("ruff", check_ruff),
        ("mypy", check_mypy),
        ("pytest", check_pytest),
        ("generator", check_generator),
        ("CLI", check_cli),
        ("lint-ecl", check_lint_ecl),
    ]

    failed = []
    for name, check_fn in checks:
        print(f"Running {name}...", file=sys.stderr)
        if not check_fn():
            failed.append(name)

    if failed:
        print(f"\nHEALTH CHECK FAILED: {', '.join(failed)}", file=sys.stderr)
        return 1

    print("\nALL HEALTH CHECKS PASSED", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
