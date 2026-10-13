#!/usr/bin/env python3
"""
Validate that company name references use the current brand format.

Checks for regressions to old name formats:
  - "Light Speed Holdings" (with spaces, outdated)
  - "Light Speed Holdings, Inc." (with Inc suffix, outdated)

The canonical current name is "LightSpeed Holdings Limited" (no space between
Light and Speed, capital S, "Limited" at end).

This script is designed to be called from a pre-commit hook or CI/CD pipeline.
It exits with code 1 if old name patterns are found, code 0 if the check passes.
"""

import os
import re
import sys
from pathlib import Path

# Configuration ────────────────────────────────────────────────────────
# Old name patterns case-insensitive regex patterns
OLD_NAME_PATTERNS = [
    re.compile(r"Light Speed Holdings", re.IGNORECASE),
    re.compile(r"Light Speed Holdings,? Inc\.?", re.IGNORECASE),
]

# Directories to scan (relative to repo root)
SCAN_DIRS = ["src", "docs", "config", "brand"]

# Directories to exempt from checking (won't be scanned)
EXEMPT_DIRS = {".venv", ".git", "__pycache__", ".agents/skills", ".gitmodules"}

# File extensions to include (None = include all text files)
INCLUDE_EXTS = None  # Set to e.g. {".py", ".md", ".yaml", ".json"} to restrict


def should_exempt(path: Path, repo_root: Path) -> bool:
    """Check if a path falls within an exempt directory."""
    try:
        path.relative_to(repo_root)
    except ValueError:
        return True  # Path outside repo root - skip

    parts = path.relative_to(repo_root).parts
    for exempt in EXEMPT_DIRS:
        if exempt in parts:
            return True
    return False


def read_file_lines(filepath: Path) -> list:
    """Read file lines, handling encoding gracefully."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return f.readlines()
    except (UnicodeDecodeError, PermissionError, OSError):
        return []


def check_file_for_old_names(filepath: Path, patterns: list) -> list:
    """Check a single file for old name pattern matches. Returns list of violations."""
    violations = []
    lines = read_file_lines(filepath)

    for line_num, line in enumerate(lines, 1):
        for pattern in patterns:
            if pattern.search(line):
                violations.append(
                    {
                        "file": str(filepath),
                        "line": line_num,
                        "matched": line.rstrip(),
                        "pattern": pattern.pattern,
                    }
                )
                break  # Only report one pattern match per line

    return violations


def main() -> int:
    """Main entry point. Returns exit code: 0 = clean, 1 = violations found."""
    # Determine repo root: go up from scripts/maintenance/ to the repo root
    # Script location: CWD/ai-company/scripts/maintenance/validate-company-name.py
    # Repo root: CWD/ai-company/
    script_dir = Path(__file__).resolve().parent  # scripts/maintenance
    repo_root = script_dir.parent.parent  # ai-company/ (two levels up from scripts/maintenance)

    # Ensure paths are absolute
    repo_root = repo_root.resolve()

    all_violations = []
    files_checked = 0

    # Walk each scan directory
    for scan_dir_name in SCAN_DIRS:
        scan_dir = repo_root / scan_dir_name
        if not scan_dir.exists():
            continue

        for dirpath, dirnames, filenames in os.walk(scan_dir):
            # Apply exempt directory filtering
            dirnames[:] = [d for d in dirnames if d not in EXEMPT_DIRS]

            for filename in filenames:
                filepath = Path(dirpath) / filename

                # Skip if path is exempt
                if should_exempt(filepath, repo_root):
                    continue

                # Filter by extension if configured
                if INCLUDE_EXTS is not None:
                    if filepath.suffix.lower() not in INCLUDE_EXTS:
                        continue

                files_checked += 1
                violations = check_file_for_old_names(filepath, OLD_NAME_PATTERNS)
                all_violations.extend(violations)

    # Report results
    if all_violations:
        print("FAIL COMPANY NAME REGRESSION DETECTED")
        print(f"  {len(all_violations)} violation(s) found in {files_checked} file(s)")
        print("  Current canonical name: LightSpeed Holdings Limited")
        print("  Old formats prohibited:")
        print("    1. 'Light Speed Holdings' (with spaces)")
        print("    2. 'Light Speed Holdings, Inc.' (with Inc suffix)")
        print("  Violations:")

        # Group by file for cleaner output
        violations_by_file = {}
        for v in all_violations:
            fname = v["file"]
            if fname not in violations_by_file:
                violations_by_file[fname] = []
            violations_by_file[fname].append(v)

        for filepath, violations in sorted(
            violations_by_file.items(), key=lambda x: len(x[1]), reverse=True
        ):
            print(f"    File: {filepath}")
            for v in violations:
                # Sanitize matched text for ASCII-safe display (PowerShell 5.1 compat)
                matched_safe = v["matched"].encode("ascii", errors="replace").decode("ascii")
                matched_short = (
                    matched_safe[:95] + "..." if len(matched_safe) > 95 else matched_safe
                )
                print(f"      Line {v['line']}: {matched_short}")
                print(f"            Pattern: {v['pattern']}")

        print("  Fix: Update references to use 'LightSpeed Holdings Limited'")
        return 1  # Exit code 1 = violations found = hook fails

    print("PASS COMPANY NAME VALIDATION")
    print(f"  {files_checked} file(s) checked - no old name patterns found")
    print("  Canonical name: LightSpeed Holdings Limited")
    return 0  # Exit code 0 = clean = hook passes


if __name__ == "__main__":
    sys.exit(main())
