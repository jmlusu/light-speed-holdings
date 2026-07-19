"""Smoke tests for release infrastructure."""

from pathlib import Path

import tomllib


def test_pyproject_has_version():
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    assert "version" in data["project"]
    assert isinstance(data["project"]["version"], str)
    parts = data["project"]["version"].split(".")
    assert len(parts) == 3, "Version must be semver (major.minor.patch)"


def test_pyproject_has_build_dependency():
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    dev_deps = data["project"]["optional-dependencies"]["dev"]
    assert "build" in dev_deps, "build must be in dev dependencies"


def test_changelog_exists():
    path = Path("CHANGELOG.md")
    assert path.exists(), "CHANGELOG.md must exist"
    content = path.read_text(encoding="utf-8")
    assert "# Changelog" in content, "CHANGELOG.md must have a header"


def test_release_workflow_exists():
    path = Path(".github/workflows/release.yml")
    assert path.exists(), "release.yml workflow must exist"
    content = path.read_text(encoding="utf-8")
    assert "v*" in content, "release.yml must trigger on v* tags"
    assert "softprops/action-gh-release" in content, "release.yml must use gh-release action"


def test_release_script_exists():
    path = Path("scripts/release.ps1")
    assert path.exists(), "release.ps1 script must exist"
    content = path.read_text(encoding="utf-8")
    assert "BumpType" in content, "release.ps1 must accept BumpType parameter"
