"""Git-Safety Test for LS-MEM Memory Paths.

Verifies that `.lightspeed/memory/` and `memory.db*` are properly gitignored
and that LS-MEM code never attempts to git add/commit/push memory paths.

Per:
- Architecture §2 (Constraints: "Memory DB never committed to Git")
- Architecture §2 Storage table (Git: `.lightspeed/memory/` + `memory.db*` ignored)
- Threat model T21–T22
- ADR-025 Decision Rule 7
- Conflict resolution C4 (resolved)
"""

import subprocess
import tempfile
from pathlib import Path

import pytest


def get_gitignore_patterns() -> list[str]:
    """Read .gitignore and return patterns related to LS-MEM."""
    gitignore = Path(".gitignore")
    if not gitignore.exists():
        return []

    patterns = []
    with open(gitignore) as f:
        for line in f:
            line = line.strip()
            if (
                line
                and not line.startswith("#")
                and ("lightspeed" in line.lower() or "memory.db" in line)
            ):
                patterns.append(line)
    return patterns


def test_gitignore_contains_lsmem_patterns():
    """Verify .gitignore has the required LS-MEM patterns."""
    patterns = get_gitignore_patterns()

    # Check for .lightspeed/memory/
    assert any(".lightspeed/memory/" in p for p in patterns), (
        "Missing `.lightspeed/memory/` pattern in .gitignore"
    )

    # Check for memory.db patterns
    assert any("memory.db" in p for p in patterns), "Missing `memory.db*` pattern in .gitignore"


def test_gitignore_effective():
    """Verify git respects the ignore patterns for LS-MEM paths."""
    # Create a temp repo to test
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = Path(tmpdir) / "test_repo"
        repo.mkdir()

        # Initialize git
        subprocess.run(["git", "init"], cwd=repo, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)

        # Copy .gitignore
        import shutil

        shutil.copy(".gitignore", repo / ".gitignore")

        # Create LS-MEM structure
        lsmem_dir = repo / ".lightspeed" / "memory"
        lsmem_dir.mkdir(parents=True)
        (lsmem_dir / "memory.db").write_text("fake db content")
        (lsmem_dir / "memory.db-wal").write_text("wal content")
        (lsmem_dir / "memory.db-shm").write_text("shm content")
        (lsmem_dir / "config.yaml").write_text("test: true")

        # Check git status - should show only .gitignore as untracked (or nothing if already committed)
        result = subprocess.run(
            ["git", "status", "--porcelain"], cwd=repo, capture_output=True, text=True, check=True
        )

        # LS-MEM files should NOT appear in git status
        untracked = result.stdout.strip().split("\n") if result.stdout.strip() else []
        lsmem_untracked = [f for f in untracked if ".lightspeed/memory" in f]

        assert not lsmem_untracked, (
            f"LS-MEM files appear in git status (not ignored): {lsmem_untracked}"
        )


def test_no_memory_db_in_git_history():
    """Verify no memory.db files exist in git history."""
    result = subprocess.run(
        ["git", "log", "--all", "--full-history", "--", "*.db", "*.db-*", ".lightspeed/memory/"],
        capture_output=True,
        text=True,
    )
    # Should have no commits touching these paths
    assert "memory.db" not in result.stdout or result.stdout.strip() == "", (
        "Found memory.db files in git history - these should never be committed"
    )


def test_lsmem_code_no_git_commands():
    """Verify LS-MEM source code doesn't contain git add/commit/push calls."""
    lsmem_root = Path("src/ai_company/lsmem")
    if not lsmem_root.exists():
        pytest.skip("LS-MEM package not yet created")

    forbidden_patterns = [
        "git add",
        "git commit",
        "git push",
        "subprocess.run.*git",
        "subprocess.call.*git",
        "subprocess.Popen.*git",
    ]

    violations = []
    for py_file in lsmem_root.rglob("*.py"):
        content = py_file.read_text()
        for pattern in forbidden_patterns:
            if pattern in content:
                violations.append(f"{py_file}: contains '{pattern}'")

    assert not violations, (
        "LS-MEM code contains git commands (violates Rule 5 / T21–T22):\n" + "\n".join(violations)
    )


def test_no_gitignore_negation_for_lsmem():
    """Verify .gitignore doesn't have negation patterns for LS-MEM paths."""
    gitignore = Path(".gitignore")
    content = gitignore.read_text()

    # Check for negation patterns that would re-include LS-MEM
    negation_patterns = [
        "!.lightspeed/memory",
        "!memory.db",
    ]

    for pattern in negation_patterns:
        assert pattern not in content, (
            f"Found negation pattern '{pattern}' in .gitignore - "
            "this would cause LS-MEM files to be tracked"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
