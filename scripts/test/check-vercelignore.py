#!/usr/bin/env python3
"""Deploy guard: verify .vercelignore keeps site build inputs uploadable.

Vercel applies .vercelignore (gitignore semantics) before uploading files for
the build, while CI builds the full checkout. A build-critical file excluded
by .vercelignore therefore passes CI and fails the deploy with ENOENT - the
root cause of the site-build failures fixed in #436 (data/*/registry.ts
missing for vite aliases defined in vite.config.ts).

The guard derives every vite alias target from vite.config.ts (so new
aliases are covered automatically), adds a static manifest of build inputs,
and evaluates all of them against .vercelignore in an isolated git repo.
Real-repo evaluation is unsound: .gitignore re-inclusion rules would mask
.vercelignore exclusions. Known junk paths must stay excluded so the rules
cannot be neutralised by wholesale deletion.

Exit 0 = safe to deploy; exit 1 = offending paths listed.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# find: '<alias>', ... replacement: path.resolve(__dirname, '<target>')
ALIAS_RE = re.compile(
    r"find:\s*(['\"])(.+?)\1\s*,\s*replacement:\s*path\.resolve\(\s*__dirname\s*,\s*(['\"])(.+?)\3\s*\)",
    re.DOTALL,
)

# Documented build inputs that are not vite aliases (.vercelignore header).
STATIC_REQUIRED: tuple[str, ...] = (
    "index.html",
    "package.json",
    "package-lock.json",
    "tsconfig.json",
    "vite.config.ts",
    "vercel.json",
    "company/agent-registry.json",
    "public/robots.txt",
    # vercel.json ignoreCommand runs this script inside the
    # .vercelignore-filtered tree; if it is excluded the deploy fails at the
    # ignore step with ENOENT exit 127 (incidents c9cecc05 / 2927304d).
    "scripts/deploy/vercel-ignore-build.sh",
)

# Paths that must REMAIN excluded (guards against deleting rules wholesale).
STATIC_EXCLUDED: tuple[str, ...] = (
    "data/use-cases/not-a-registry.json",
    ".env.local",
    "docs/ARCHITECTURE.md",
    "src/ai_company/cli/main.py",
    # scripts/ must stay excluded apart from the single ignoreCommand file;
    # this sibling guards against re-opening the whole tree.
    "scripts/maintenance/lint-ecl.ps1",
)


def alias_targets() -> dict[str, str]:
    """Map each alias target path (repo-relative) to a human-readable origin."""
    text = (REPO_ROOT / "vite.config.ts").read_text(encoding="utf-8")
    pairs = ALIAS_RE.findall(text)
    if len(pairs) != text.count("replacement:"):
        raise SystemExit(
            "FAIL: alias regex matched fewer replacements than vite.config.ts "
            "defines - update ALIAS_RE before relying on this guard"
        )
    required: dict[str, str] = {}
    for _, alias, _, raw in pairs:
        rel = raw[2:] if raw.startswith("./") else raw
        required.setdefault(rel, f"vite alias {alias!r}")
    if not required:
        raise SystemExit("FAIL: no alias targets parsed from vite.config.ts")
    for rel in STATIC_REQUIRED:
        required.setdefault(rel, "static build input")
    return required


def _materialise(root: Path, rel: str) -> None:
    """Create the path in the temp repo with the same type as in the real repo.

    gitignore dir-only rules (trailing "/") only match if the path is known to
    be a directory, so bare string evaluation of a nonexistent path is unsafe.
    """
    dest = root / rel
    if (REPO_ROOT / rel).is_dir():
        dest.mkdir(parents=True, exist_ok=True)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.touch(exist_ok=True)


def evaluate(required_paths: set[str], excluded_paths: set[str]) -> tuple[list[str], list[str]]:
    """Evaluate paths against .vercelignore semantics.

    Returns (wrongly_excluded, wrongly_included): required paths the rules
    exclude, and junk paths the rules no longer exclude.
    """
    vercelignore = (REPO_ROOT / ".vercelignore").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(
        prefix="vercelignore-check-", ignore_cleanup_errors=True
    ) as td:
        root = Path(td)
        proc = subprocess.run(["git", "init", "-q", str(root)], capture_output=True, text=True)
        if proc.returncode != 0:
            raise SystemExit(f"FAIL: git init failed: {proc.stderr.strip()}")
        exclude_file = root / ".git" / "info" / "exclude"
        exclude_file.parent.mkdir(parents=True, exist_ok=True)
        exclude_file.write_text(vercelignore, encoding="utf-8")
        for rel in required_paths | excluded_paths:
            _materialise(root, rel)
        # Neutralise a user/system core.excludesFile so only .vercelignore rules
        # (as info/exclude) plus any ambient .gitignore files apply. The temp
        # repo has no .gitignore files, so evaluation is pure .vercelignore.
        ghost_excludes = root / "no-global-excludes"
        # Binary I/O on purpose: on Windows, text-mode stdin translates \n to
        # \r\n, git treats the trailing \r as part of the path, and every
        # pattern silently stops matching.
        proc = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "-c",
                f"core.excludesFile={ghost_excludes}",
                "check-ignore",
                "--no-index",
                "--stdin",
            ],
            input=("\n".join(sorted(required_paths | excluded_paths)) + "\n").encode(),
            capture_output=True,
        )
        if proc.returncode not in (0, 1):
            raise SystemExit(
                f"FAIL: git check-ignore errored: {proc.stderr.decode(errors='replace').strip()}"
            )
        ignored = set(proc.stdout.decode(errors="replace").splitlines())
    wrongly_excluded = sorted(required_paths & ignored)
    wrongly_included = sorted(excluded_paths - ignored)
    return wrongly_excluded, wrongly_included


def main() -> int:
    required = alias_targets()
    excluded = set(STATIC_EXCLUDED)
    bad_excluded, bad_included = evaluate(set(required), excluded)
    if bad_excluded:
        print(
            "FAIL: .vercelignore would exclude build-critical path(s); "
            "the Vercel deploy would fail:"
        )
        for rel in bad_excluded:
            print(f"  - {rel}  [{required[rel]}]")
    if bad_included:
        print(
            "FAIL: .vercelignore no longer excludes junk path(s) (rules were weakened or deleted):"
        )
        for rel in bad_included:
            print(f"  - {rel}")
    if bad_excluded or bad_included:
        return 1
    print(
        f"OK: {len(required)} build-critical path(s) survive .vercelignore; "
        f"{len(excluded)} junk path(s) stay excluded."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
