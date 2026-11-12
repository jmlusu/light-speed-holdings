"""Verify the agent skills installed in this repository expose valid frontmatter.

History: this module used to assert a repo-local copy of the ``writing-plans``
skill at ``.agents/skills/writing-plans/SKILL.md``. That copy was deliberately
removed in 405b5f4a (skills are installed under ``.agents/.agents/skills`` and
pulled from the shared catalogue), which left the assertion pointing at a path
that no longer exists and turned the suite red on main. The check now follows
the skills that actually ship, so a malformed or nameless skill still fails the
gate instead of the gate failing on a removed file.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".agents" / ".agents" / "skills"


def test_subagent_framework_available() -> None:
    """Every installed skill has a name and a description in its frontmatter."""
    skill_paths = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    assert skill_paths, f"no installed skills found under {SKILLS_DIR}"

    for skill_path in skill_paths:
        skill_content = skill_path.read_text(encoding="utf-8")
        name_match = re.search(r"(?m)^name:\s*(\S+)", skill_content)
        assert name_match, f"{skill_path} missing 'name:' field"
        assert name_match.group(1) == skill_path.parent.name, (
            f"{skill_path} name '{name_match.group(1)}' does not match its folder name"
        )
        desc_match = re.search(r"(?m)^description:\s*(\S.*)$", skill_content)
        assert desc_match, f"{skill_path} missing 'description:' field"
        assert len(desc_match.group(1).split()) >= 4, (
            f"{skill_path} description is too short to be useful"
        )
