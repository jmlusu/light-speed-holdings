#!/usr/bin/env python3
"""Guard: no client/commercial/personal artifacts may be tracked in this repo.

Incident (2026-11-10): 26 files under ``proposal-deliverables/`` — client
proposals, an executive summary and their generator scripts — reached the
public ``main`` branch of ``github.com/jmlusu/light-speed-holdings`` via
PR #473 (a broad ``git add``). They carried a named individual, an engagement
value (USD 45,000), budget splits, a live USSD short code and district-level
project detail. ``.vercelignore`` already excluded the directory from the
Vercel upload, so the files never shipped to the website — but that rule does
nothing about a public git remote, and the content was fetched unauthenticated
from ``raw.githubusercontent.com`` (HTTP 200) during the investigation.

This repository is public. Anything tracked here is world-readable forever,
including in history after deletion. Confidential commercial material belongs
in a private engagement folder, never in this tree.

Rule (checked against the git index, so pre-commit catches a staged ``git add``
before it can be committed, and CI catches anything that slipped through):

  1. No tracked path may live in a confidential top-level directory
     (``proposal-deliverables/``, ``client-deliverables/``, ...).
  2. No tracked path may contain a client-identifying marker in its file name
     (``jack-mlusu``, ``villagereach``, ``digital-health-consultant``).
  3. No tracked Office/PDF document may be named as a proposal
     (``*Proposal*.docx`` / ``.pptx`` / ``.pdf`` and friends).

Usage:
    python scripts/test/check-confidential-artifacts.py
    python scripts/test/check-confidential-artifacts.py --staged
    python scripts/test/check-confidential-artifacts.py --path <file-list>

Exit 0 = clean; exit 1 = confidential artifact tracked (or about to be).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Directories whose entire contents are confidential by definition.
CONFIDENTIAL_DIRS = frozenset(
    {
        "proposal-deliverables",
        "client-deliverables",
        "consulting-deliverables",
        "confidential",
    }
)

# Client-identifying markers that must never appear in a tracked file name.
CLIENT_MARKERS = re.compile(
    r"(jack[-_ ]?mlusu|villagereach|digital[-_ ]?health[-_ ]?consultant)",
    re.IGNORECASE,
)

# Commercial proposal documents (binary formats carry the content inline and
# cannot be reviewed or redacted in a diff).
PROPOSAL_DOCUMENT = re.compile(
    r"proposal.*\.(docx|doc|pptx|ppt|pdf|xlsx|xls|odt|odp)$", re.IGNORECASE
)

# Historical tree already purged from the index; listed so the guard's intent
# is explicit if the paths ever reappear (e.g. a re-added stray copy).
_REMEDIATION = (
    "Move the file out of the repository (private engagement folder) and "
    "untrack it with `git rm --cached <path>`. If the content was ever "
    "committed, treat it as disclosed: deleting it does not un-publish it."
)


def _tracked_files(staged: bool) -> list[str]:
    """Return tracked paths from the git index (staged-only when requested).

    Staged mode looks only at additions/copies/modifications/renames: a staged
    *deletion* is the remediation for a leaked file and must never fail the
    gate that exists to remove it.
    """
    if staged:
        args = [
            "git",
            "-C",
            str(REPO_ROOT),
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=ACMR",
            "-z",
        ]
    else:
        args = ["git", "-C", str(REPO_ROOT), "ls-files", "-z"]
    result = subprocess.run(args, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            "git ls-files failed: " + result.stderr.decode("utf-8", "replace").strip()
        )
    return [p for p in result.stdout.decode("utf-8", "replace").split("\0") if p]


def _violations(paths: list[str]) -> list[tuple[str, str]]:
    """Return (path, reason) for every confidential path."""
    found: list[tuple[str, str]] = []
    for raw in paths:
        path = raw.replace("\\", "/")
        segments = path.split("/")
        name = segments[-1]

        confidential_dir = next((seg for seg in segments[:-1] if seg in CONFIDENTIAL_DIRS), None)
        if confidential_dir is not None:
            found.append((path, f"inside confidential directory '{confidential_dir}/'"))
            continue
        if CLIENT_MARKERS.search(name):
            found.append((path, "client-identifying marker in file name"))
            continue
        if PROPOSAL_DOCUMENT.search(name):
            found.append((path, "commercial proposal document"))
    return found


def _check(paths: list[str]) -> tuple[bool, list[str]]:
    violations = _violations(paths)
    if not violations:
        return True, [f"OK: none of {len(paths)} tracked paths is a confidential artifact."]

    lines = [f"FAIL: {len(violations)} confidential artifact(s) tracked in this public repo:"]
    lines.extend(f"  - {path} ({reason})" for path, reason in violations)
    lines.append(_REMEDIATION)
    lines.append(
        "See .gitignore 'Confidential Client & Commercial Artifacts' and the "
        "incident note in this script's docstring."
    )
    return False, lines


def main(argv: list[str]) -> int:
    staged = "--staged" in argv
    paths: list[str] | None = None

    if "--path" in argv:
        idx = argv.index("--path")
        if idx + 1 >= len(argv):
            print("FAIL: --path requires a file argument")
            return 1
        source = Path(argv[idx + 1])
        if not source.is_file():
            print(f"FAIL: file list not found: {source}")
            return 1
        paths = [
            line.strip() for line in source.read_text(encoding="utf-8").splitlines() if line.strip()
        ]

    try:
        candidates = paths if paths is not None else _tracked_files(staged)
    except RuntimeError as exc:
        print(f"FAIL: {exc}")
        return 1

    passed, report = _check(candidates)
    for line in report:
        print(line)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
