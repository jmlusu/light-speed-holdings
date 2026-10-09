#!/usr/bin/env python3
"""Custom validation script for the prompt-manager skill.

Validates that the skill folder and its contents conform to the
LightSpeed prompt-manager specification.

Usage: python validate_prompt.py

Exit code 0 = PASS, 1 = FAIL, 2 = usage error.
"""

import os
import sys

# Try to import the bundled validator, fall back to basic checks
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from scripts.validate_skill import main as validate_skill
    HAS_BUNDLED = True
except ImportError:
    HAS_BUNDLED = False


KEBAB_RE = __import__("re").compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def check_folder_name(folder):
    """Check that folder name is kebab-case."""
    if not KEBAB_RE.match(folder):
        return f"ERROR: folder name {folder!r} is not kebab-case (lowercase, digits, hyphens only)"
    return None


def check_skill_md(text):
    """Check SKILL.md frontmatter format."""
    errors = []

    if not text.startswith("---"):
        errors.append("ERROR: frontmatter missing or malformed: SKILL.md must start with '---' delimited YAML")
        return errors

    # Check for matching --- delimiters
    if text.count("---") < 2:
        errors.append("ERROR: frontmatter missing second '---' delimiter")
        return errors

    # Check for XML angle brackets in frontmatter block
    match = __import__("re").match(r"^---\s*\n(.*?)\n---\s*\n?", text, __import__("re").DOTALL)
    if not match:
        errors.append("ERROR: frontmatter malformed: cannot parse YAML block")
        return errors

    fm_block = match.group(1)
    if "<" in fm_block or ">" in fm_block:
        errors.append("ERROR: frontmatter contains XML angle brackets (< >) — forbidden for security")

    # Check name field
    name_value = None
    description_value = None
    for line in fm_block.splitlines():
        stripped = line.strip()
        if stripped.startswith("name:"):
            name_value = stripped.split(":", 1)[1].strip().strip('"\'')
        if stripped.startswith("description:"):
            description_value = stripped.split(":", 1)[1].strip().strip('"\'')

    # Check name
    if not name_value:
        errors.append("ERROR: frontmatter is missing required field 'name'")
    else:
        if not KEBAB_RE.match(name_value):
            errors.append(f"ERROR: name {name_value!r} is not kebab-case")
        if name_value.lower() in ("claude", "anthropic"):
            errors.append(f"ERROR: name {name_value!r} uses a reserved word (claude/anthropic)")

    # Check description
    if not description_value:
        errors.append("ERROR: frontmatter is missing required field 'description'")
    else:
        if len(description_value) > 1024:
            errors.append(f"ERROR: description is {len(description_value)} chars (max 1024)")
        else:
            lowered = description_value.lower()
            if len(description_value) < 40:
                warnings.append(f"WARNING: description is very short ({len(description_value)} chars) — likely too vague to trigger")
            if not any(cue in lowered for cue in ("use when", "use this", "use for", "trigger")):
                warnings.append("WARNING: description has no obvious WHEN clause (e.g. 'Use when ...') — add trigger conditions")

    return errors


def main():
    skill_dir = os.path.abspath(".")
    folder = os.path.basename(skill_dir)

    errors = []
    warnings = []

    # Check folder name
    folder_error = check_folder_name(folder)
    if folder_error:
        errors.append(folder_error)

    # Check SKILL.md exists
    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md_path):
        errors.append("ERROR: SKILL.md is missing")
    else:
        with open(skill_md_path, encoding="utf-8") as f:
            text = f.read()

        fm_errors = check_skill_md(text)
        errors.extend(fm_errors)
        for w in __import__("re").finditer(r"(?:scripts|references|assets)/[\w./-]*\w", text):
            rel = w.group(0)
            if not os.path.exists(os.path.join(skill_dir, rel)):
                warnings.append(f"WARNING: SKILL.md references {rel!r} but it does not exist in the skill folder")

    # Report
    for msg in errors:
        print(f"ERROR: {msg}")
    for msg in warnings:
        print(f"WARNING: {msg}")

    verdict = "FAIL" if errors else "PASS"
    print(f"{verdict}: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())