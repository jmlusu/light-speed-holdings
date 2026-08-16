"""Regression tests for scripts/validate_opencode.py (issue #87).

The validator must enforce the OpenCode v2 format: a ``permission`` block with
``allow``/``ask``/``deny`` values over the canonical runtime tool vocabulary
(read, edit, grep, list, bash, webfetch, task), and reject the legacy
``tools``/``name`` fields.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT_PATH = _REPO_ROOT / "scripts" / "validate_opencode.py"


def _load_validator() -> Any:
    spec = importlib.util.spec_from_file_location("validate_opencode_script", _SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_validator = _load_validator()


def _card(tmp_path: Path, frontmatter: str) -> Path:
    """Return a Path to a card file whose frontmatter is the given YAML."""
    path = tmp_path / "agent.md"
    path.write_text(f"---\n{frontmatter}\n---\n\n# Card\n", encoding="utf-8")
    return path


_VALID_FRONTMATTER = """\
description: A valid v2 agent card.
mode: subagent
permission:
  read: allow
  edit: allow
  bash: deny
  grep: ask
  list: allow
  webfetch: ask
  task: deny
"""


def test_valid_v2_card_has_no_errors(tmp_path: Path) -> None:
    assert _validator.validate_agent(_card(tmp_path, _VALID_FRONTMATTER)) == []


def test_legacy_tools_field_is_rejected(tmp_path: Path) -> None:
    errors = _validator.validate_agent(
        _card(tmp_path, "description: legacy card\nmode: subagent\ntools:\n  read: true\n")
    )
    assert any("Forbidden field present: tools" in e for e in errors)


def test_legacy_name_field_is_rejected(tmp_path: Path) -> None:
    errors = _validator.validate_agent(
        _card(
            tmp_path,
            "name: chief-of-staff\ndescription: card\nmode: subagent\npermission:\n  read: allow\n",
        )
    )
    assert any("Forbidden field present: name" in e for e in errors)


def test_code_interpreter_permission_is_rejected(tmp_path: Path) -> None:
    errors = _validator.validate_agent(
        _card(
            tmp_path,
            "description: removed tool\nmode: subagent\npermission:\n  read: allow\n  code_interpreter: allow\n",
        )
    )
    assert any("code_interpreter" in e and "canonical" in e for e in errors)


def test_non_allow_ask_deny_value_is_rejected(tmp_path: Path) -> None:
    errors = _validator.validate_agent(
        _card(tmp_path, "description: bad value\nmode: subagent\npermission:\n  read: true\n")
    )
    assert any("permission.read must be one of" in e for e in errors)


def test_missing_permission_is_rejected(tmp_path: Path) -> None:
    errors = _validator.validate_agent(
        _card(tmp_path, "description: no permission\nmode: subagent\n")
    )
    assert any("Missing required field: permission" in e for e in errors)
