#!/usr/bin/env python3
"""Execution-manifest persistence.

Layout: ``<out_root>/<run_id>/manifest.json`` next to that run's outputs.
One directory per run, so a failure and its rerun are both inspectable.
"""

from __future__ import annotations

from pathlib import Path

from ai_company.creative.models import ExecutionManifest
from ai_company.paths import get_project_root

#: Repo-relative default output root for creative runs.
DEFAULT_OUT_SUBDIR = ("output", "creative")


def default_out_root(project_root: Path | None = None) -> Path:
    """Default output root: ``<project_root>/output/creative``."""
    root = Path(project_root) if project_root is not None else get_project_root()
    return root.joinpath(*DEFAULT_OUT_SUBDIR)


def run_dir(out_root: Path, run_id: str) -> Path:
    """Directory of a single run."""
    return Path(out_root) / run_id


def save_manifest(manifest: ExecutionManifest, out_root: Path) -> Path:
    """Persist ``manifest.json`` into the run directory; return its path."""
    target = run_dir(out_root, manifest.run_id)
    target.mkdir(parents=True, exist_ok=True)
    path = target / "manifest.json"
    path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
    return path


def load_manifest(run_id: str, out_root: Path) -> ExecutionManifest:
    """Load a previously persisted manifest."""
    path = run_dir(out_root, run_id) / "manifest.json"
    return ExecutionManifest.model_validate_json(path.read_text(encoding="utf-8"))


def list_runs(out_root: Path) -> list[str]:
    """Run ids that have a persisted manifest (sorted)."""
    root = Path(out_root)
    if not root.is_dir():
        return []
    return sorted(
        entry.name
        for entry in root.iterdir()
        if entry.is_dir() and (entry / "manifest.json").exists()
    )
