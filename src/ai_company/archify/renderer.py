"""Archify renderer — wraps the bundled Archify Node.js CLI.

Locates the skill checkout (``.opencode/skills/archify``), invokes
``node bin/archify.mjs`` for ``validate`` / ``deliver`` / ``compare``, and
parses the machine-readable JSON receipts the CLI emits on ``--json``.

When Node.js (>=18) is unavailable the renderer degrades cleanly: validators
raise :class:`ArchifyNotAvailable`, and the CLI surfaces a readable hint
instead of a raw subprocess traceback.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from ai_company.paths import get_project_root

# Relative path (repo root -> skill checkout). Overridable for tests via
# the constructor argument, and by ARCHIFY_SKILL_DIR env var in ``resolve``.
_DEFAULT_SKILL_REL = Path(".opencode/skills/archify")
_BIN_REL = Path("bin/archify.mjs")


class ArchifyError(RuntimeError):
    """Base error for Archify rendering failures."""


class ArchifyNotAvailable(ArchifyError):
    """Node.js or the Archify skill is missing; cannot render diagrams."""


def resolve_skill_dir(explicit: str | Path | None = None) -> Path:
    """Resolve the Archify skill checkout directory.

    Env ``ARCHIFY_SKILL_DIR`` wins over the default repo-relative path; an
    explicit argument wins over both.
    """
    if explicit is not None:
        return Path(explicit).resolve()
    env_val = __import__("os").environ.get("ARCHIFY_SKILL_DIR", "")
    if env_val:
        env = Path(env_val)
        if env.exists():
            return env.resolve()
    return (get_project_root() / _DEFAULT_SKILL_REL).resolve()


def resolve_bin(explicit: str | Path | None = None) -> Path:
    """Resolve the Archify CLI entry point."""
    return resolve_skill_dir(explicit) / _BIN_REL


def _node_available() -> bool:
    return shutil.which("node") is not None


def _run_cli(
    bin_path: Path, args: list[str], timeout: int = 300
) -> subprocess.CompletedProcess[str]:
    """Run the Archify CLI, returning a completed process (no exception)."""
    if not _node_available():
        raise ArchifyNotAvailable(
            "Node.js (>=18) is required to render Archify diagrams. "
            "Install Node or disable diagram generation."
        )
    if not bin_path.exists():
        raise ArchifyNotAvailable(
            f"Archify skill not found at {bin_path}. Run: "
            "npx skills add tt-a1i/archify (or restore .opencode/skills/archify)."
        )
    from ai_company.paths import get_project_root

    cmd = ["node", str(bin_path), *args]
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(get_project_root()),
    )


def _json_from_process(proc: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    """Extract the JSON receipt from a CLI process (``--json`` mode).

    The Archify CLI pretty-prints its JSON receipt (multi-line), so parse the
    outermost ``{...}`` block from the combined output rather than requiring a
    single-line object. Falls back to the last parseable JSON object if several
    appear (e.g. human messages before the machine receipt).
    """
    blob = (proc.stdout or "") + "\n" + (proc.stderr or "")
    start = blob.find("{")
    if start == -1:
        return {}
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(blob)):
        ch = blob[i]
        if esc:
            esc = False
            continue
        if ch == "\\" and in_str:
            esc = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if not in_str:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    candidate = blob[start : i + 1]
                    try:
                        parsed = json.loads(candidate)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(parsed, dict):
                        return parsed
    return {}


def validate(
    diagram_type: str,
    json_path: str | Path,
    *,
    quality: str = "showcase",
    skill_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Validate a JSON IR source. Returns the CLI receipt.

    Raises:
        ArchifyNotAvailable: Node.js or the skill is missing.
        ArchifyError: the CLI exited non-zero (validation failed).
    """
    bin_path = resolve_bin(skill_dir)
    proc = _run_cli(
        bin_path,
        ["validate", diagram_type, str(json_path), "--quality", quality, "--json"],
    )
    receipt = _json_from_process(proc)
    if proc.returncode != 0:
        raise ArchifyError(
            f"Archify validation failed (exit {proc.returncode}): {proc.stdout} {proc.stderr}"
        )
    return receipt


def deliver(
    diagram_type: str,
    json_path: str | Path,
    html_path: str | Path,
    *,
    quality: str = "showcase",
    open_html: bool = False,
    skill_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Render and validate a JSON IR source to an HTML artifact.

    Only a passing artifact is written (the CLI atomically replaces the target).
    Returns the delivery receipt with SHA-256 and byte counts.
    """
    bin_path = resolve_bin(skill_dir)
    args = ["deliver", diagram_type, str(json_path), str(html_path), "--quality", quality, "--json"]
    if open_html:
        args.append("--open")
    proc = _run_cli(bin_path, args)
    receipt = _json_from_process(proc)
    if proc.returncode != 0:
        raise ArchifyError(
            f"Archify delivery failed (exit {proc.returncode}): {proc.stdout} {proc.stderr}"
        )
    return receipt


def compare(
    diagram_type: str,
    base_path: str | Path,
    head_path: str | Path,
    output_html: str | Path,
    *,
    skill_dir: str | Path | None = None,
    open_html: bool = False,
) -> dict[str, Any]:
    """Render a single Before/Delta/After comparison HTML from two validated snapshots."""
    bin_path = resolve_bin(skill_dir)
    args = [
        "compare",
        diagram_type,
        str(base_path),
        str(head_path),
        str(output_html),
        "--json",
    ]
    if open_html:
        args.append("--open")
    proc = _run_cli(bin_path, args)
    receipt = _json_from_process(proc)
    if proc.returncode != 0:
        raise ArchifyError(
            f"Archify compare failed (exit {proc.returncode}): {proc.stdout} {proc.stderr}"
        )
    return receipt


def guide(
    scenario: str,
    *,
    skill_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Ask Archify which diagram type fits a scenario (type routing helper)."""
    bin_path = resolve_bin(skill_dir)
    proc = _run_cli(bin_path, ["guide", scenario, "--json"])
    if proc.returncode != 0:
        raise ArchifyError(
            f"Archify guide failed (exit {proc.returncode}): {proc.stdout} {proc.stderr}"
        )
    return _json_from_process(proc)
