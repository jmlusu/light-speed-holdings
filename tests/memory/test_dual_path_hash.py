"""Dual-Path Skill Hash Identity Test.

Verifies that `.agents/skills/ls-memory/` and `.opencode/skills/ls-memory/`
are content-identical (byte-for-byte) as required by:
- Threat model §4.4 (open item 4)
- ADR-025 Decision Rule 5
- Architecture §11 (Locked decision 1)
- Failure mode FM4 (architecture §17)
"""

import hashlib
import os
from pathlib import Path

import pytest

# Skill paths (architecture §11, locked decision 1)
AGENTS_SKILL_PATH = Path(".agents/skills/ls-memory")
OPENCODE_SKILL_PATH = Path(".opencode/skills/ls-memory")
GLOBAL_SKILL_PATH = Path.home() / ".agents" / "skills" / "ls-memory"


def compute_file_hash(filepath: Path) -> str:
    """Compute SHA256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_all_files(skill_path: Path) -> list[Path]:
    """Get all files in a skill directory, relative to the skill root."""
    if not skill_path.exists():
        return []
    files = []
    for root, dirs, filenames in os.walk(skill_path):
        # Skip __pycache__ and .git
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
        for filename in filenames:
            if not filename.endswith(".pyc"):
                full = Path(root) / filename
                rel = full.relative_to(skill_path)
                files.append(rel)
    return sorted(files)


def test_both_skill_paths_exist():
    """Both skill paths must exist."""
    assert AGENTS_SKILL_PATH.exists(), f"Discovery authority path missing: {AGENTS_SKILL_PATH}"
    assert OPENCODE_SKILL_PATH.exists(), f"Parallel deploy target missing: {OPENCODE_SKILL_PATH}"


def test_skill_file_lists_identical():
    """Both skill directories must contain the same files."""
    agents_files = get_all_files(AGENTS_SKILL_PATH)
    opencode_files = get_all_files(OPENCODE_SKILL_PATH)

    assert agents_files == opencode_files, (
        f"File lists differ:\n"
        f"  Only in .agents: {set(agents_files) - set(opencode_files)}\n"
        f"  Only in .opencode: {set(opencode_files) - set(agents_files)}"
    )


def test_skill_files_byte_identical():
    """Corresponding files in both skill paths must be byte-identical."""
    agents_files = get_all_files(AGENTS_SKILL_PATH)

    mismatches = []
    for rel_path in agents_files:
        agents_file = AGENTS_SKILL_PATH / rel_path
        opencode_file = OPENCODE_SKILL_PATH / rel_path

        agents_hash = compute_file_hash(agents_file)
        opencode_hash = compute_file_hash(opencode_file)

        if agents_hash != opencode_hash:
            mismatches.append((str(rel_path), agents_hash, opencode_hash))

    assert not mismatches, (
        f"Byte-identical check failed for {len(mismatches)} file(s):\n"
        + "\n".join(
            f"  {path}: .agents={agents_h[:16]}... vs .opencode={opencode_h[:16]}..."
            for path, agents_h, opencode_h in mismatches
        )
    )


def test_global_skill_optional_but_identical_if_exists():
    """Global skill copy is optional but must be identical if it exists."""
    if not GLOBAL_SKILL_PATH.exists():
        pytest.skip("Global skill copy not present (optional)")

    agents_files = get_all_files(AGENTS_SKILL_PATH)
    global_files = get_all_files(GLOBAL_SKILL_PATH)

    assert agents_files == global_files, "Global skill file list differs from discovery authority"

    mismatches = []
    for rel_path in agents_files:
        agents_file = AGENTS_SKILL_PATH / rel_path
        global_file = GLOBAL_SKILL_PATH / rel_path

        agents_hash = compute_file_hash(agents_file)
        global_hash = compute_file_hash(global_file)

        if agents_hash != global_hash:
            mismatches.append((str(rel_path), agents_hash, global_hash))

    assert not mismatches, (
        f"Global skill differs from discovery authority in {len(mismatches)} file(s)"
    )


def test_skill_hash_report():
    """Generate a hash report for CI artifact."""
    agents_files = get_all_files(AGENTS_SKILL_PATH)
    report = []

    for rel_path in agents_files:
        agents_file = AGENTS_SKILL_PATH / rel_path
        opencode_file = OPENCODE_SKILL_PATH / rel_path

        agents_hash = compute_file_hash(agents_file)
        opencode_hash = compute_file_hash(opencode_file)

        match = "[OK]" if agents_hash == opencode_hash else "[FAIL]"
        report.append(f"{match} {rel_path}: {agents_hash[:16]}...")

    # Write report for CI
    report_path = Path("tests/memory/dual_path_hash_report.txt")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report) + "\n")

    # Also print for CI logs
    print("\n=== Dual-Path Skill Hash Report ===")
    for line in report:
        print(line)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
