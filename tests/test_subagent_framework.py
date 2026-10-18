"""Test subagent-driven development framework verification."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_subagent_framework_available() -> None:
    """Verify the subagent-driven development framework is properly configured."""
    skill_path = REPO_ROOT / ".agents" / "skills" / "writing-plans" / "SKILL.md"
    checks = {
        "writing_plans_skill_exists": skill_path.exists(),
    }
    assert checks["writing_plans_skill_exists"], f"missing {skill_path}"

    # Read and verify SKILL.md content
    with open(skill_path, encoding="utf-8") as f:
        skill_content = f.read()

    # Check for required name field
    name_match = re.search(r"name:\s*([\w-]+)", skill_content)
    assert name_match, "SKILL.md missing 'name:' field"
    # Verify it matches expected pattern (writing-plan or writing-plans)
    assert name_match.group(1) in ("writing-plan", "writing-plans"), (
        "SKILL.md name '{}' not in expected values".format(name_match.group(1))
    )

    # Check for required description field
    desc_match = re.search(r"description:\s*(.+)", skill_content)
    assert desc_match, "SKILL.md missing 'description:' field"

    # Check for task structure patterns
    assert re.search(r"Step 1: Write the failing test", skill_content), (
        "SKILL.md missing task structure pattern"
    )
    assert re.search(r"Step 2: Run test to verify it fails", skill_content), (
        "SKILL.md missing step 2 pattern"
    )
    assert re.search(r"Step 3: Write minimal implementation", skill_content), (
        "SKILL.md missing step 3 pattern"
    )
    assert re.search(r"Step 4: Run test to verify it passes", skill_content), (
        "SKILL.md missing step 4 pattern"
    )
    assert re.search(r"Step 5: Commit", skill_content), "SKILL.md missing step 5 pattern"

    # Check for no placeholders section
    assert re.search(r"## No Placeholders", skill_content), (
        "SKILL.md missing '## No Placeholders' section"
    )
    assert re.search(r"## Self-Review", skill_content), "SKILL.md missing '## Self-Review' section"
