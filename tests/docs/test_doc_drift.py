"""Tests that documentation hasn't drifted from source-of-truth.yaml."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "docs" / "source-of-truth.yaml"


@pytest.fixture(scope="module")
def manifest() -> dict[str, Any]:
    """Load the source-of-truth manifest."""
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        result: dict[str, Any] = yaml.safe_load(f)
        return result


@pytest.fixture(scope="module")
def claims(manifest: dict[str, Any]) -> dict[str, Any]:
    """Extract claims dict from manifest."""
    result: dict[str, Any] = manifest["claims"]
    return result


def _read_doc_text(doc_rel: str) -> str | None:
    """Read a doc file, returning None if it doesn't exist."""
    path = REPO_ROOT / doc_rel
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def _find_numbers_in_text(text: str, pattern: str) -> list[int]:
    """Find all numbers matching pattern in text, return list of ints."""
    regex = re.compile(pattern, re.IGNORECASE)
    matches = regex.findall(text)
    numbers: list[int] = []
    for match in matches:
        num_match = re.search(r"\d+", match)
        if num_match:
            numbers.append(int(num_match.group()))
    return numbers


def _expected_number(current_value: str | int) -> int | None:
    """Extract the first numeric portion of a claim's current_value.

    Mirrors scripts/validate-drift.ps1, which compares the numeric portion of
    the expected value (e.g. ``>=3.12`` -> 3) against numbers found in docs.
    """
    num_match = re.search(r"\d+", str(current_value))
    if not num_match:
        return None
    return int(num_match.group())


# ── Specific tests (as requested) ──────────────────────────────────────


def test_docs_match_department_count(claims: dict[str, Any]) -> None:
    """Validate department_count claim against docs."""
    claim = claims["department_count"]
    expected = _expected_number(claim["current_value"])
    pattern = claim["pattern"]
    docs = claim["docs"]

    for doc_rel in docs:
        text = _read_doc_text(doc_rel)
        if text is None:
            pytest.skip(f"Doc file not found: {doc_rel}")
        numbers = _find_numbers_in_text(text, pattern)
        assert any(n == expected for n in numbers), (
            f"{doc_rel}: expected to find '{expected}' matching pattern '{pattern}', found {numbers}"
        )


def test_docs_match_agent_count(claims: dict[str, Any]) -> None:
    """Validate agent_count claim against docs."""
    claim = claims["agent_count"]
    expected = _expected_number(claim["current_value"])
    pattern = claim["pattern"]
    docs = claim["docs"]

    for doc_rel in docs:
        text = _read_doc_text(doc_rel)
        if text is None:
            pytest.skip(f"Doc file not found: {doc_rel}")
        numbers = _find_numbers_in_text(text, pattern)
        assert any(n == expected for n in numbers), (
            f"{doc_rel}: expected to find '{expected}' matching pattern '{pattern}', found {numbers}"
        )


def test_docs_match_kpi_count(claims: dict[str, Any]) -> None:
    """Validate kpi_count claim against docs."""
    claim = claims["kpi_count"]
    expected = _expected_number(claim["current_value"])
    pattern = claim["pattern"]
    docs = claim["docs"]

    for doc_rel in docs:
        text = _read_doc_text(doc_rel)
        if text is None:
            pytest.skip(f"Doc file not found: {doc_rel}")
        numbers = _find_numbers_in_text(text, pattern)
        assert any(n == expected for n in numbers), (
            f"{doc_rel}: expected to find '{expected}' matching pattern '{pattern}', found {numbers}"
        )


def test_no_stale_path_patterns(claims: dict[str, Any]) -> None:
    """Validate path_resolution_pattern anti_pattern not found in scope."""
    claim = claims["path_resolution_pattern"]
    anti_pattern = claim["anti_pattern"]
    regex_str = anti_pattern["regex"]
    scope = anti_pattern["scope"]

    cli_files = list(REPO_ROOT.glob(scope))

    violations: list[str] = []
    for cli_file in cli_files:
        if not cli_file.is_file():
            continue
        text = cli_file.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            if re.search(regex_str, line):
                violations.append(f"{cli_file.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}")

    assert not violations, "Stale path patterns found:\n" + "\n".join(violations)


def test_no_stale_kpi_path_pattern(claims: dict[str, Any]) -> None:
    """Validate kpi_config_location anti_pattern not found in scope."""
    claim = claims["kpi_config_location"]
    anti_pattern = claim["anti_pattern"]
    regex_str = anti_pattern["regex"]
    scope = anti_pattern["scope"]

    cli_files = list(REPO_ROOT.glob(scope))

    violations: list[str] = []
    for cli_file in cli_files:
        if not cli_file.is_file():
            continue
        text = cli_file.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            if re.search(regex_str, line):
                violations.append(f"{cli_file.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}")

    assert not violations, "Stale KPI path patterns found:\n" + "\n".join(violations)


def test_source_files_exist(claims: dict[str, Any]) -> None:
    """For each claim with a source (not 'dynamic'), verify the source file exists."""
    missing: list[str] = []
    for name, claim in claims.items():
        source = claim.get("source")
        if not source or source == "dynamic":
            continue
        source_path = REPO_ROOT / source
        if not source_path.exists():
            missing.append(f"{name}: {source}")

    assert not missing, "Source files missing:\n" + "\n".join(missing)


# ── Parametrized test for all claims ───────────────────────────────────


def _get_all_claim_ids(claims: dict[str, Any]) -> list[str]:
    """Get list of all claim IDs."""
    return list(claims.keys())


def _get_claims_with_docs(claims: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """Get claims that have docs to check."""
    result: list[tuple[str, dict[str, Any]]] = []
    for name, claim in claims.items():
        docs = claim.get("docs", [])
        if docs and claim.get("current_value") is not None:
            result.append((name, claim))
    return result


def _get_claims_with_anti_pattern(claims: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """Get claims that have anti_pattern to check."""
    result: list[tuple[str, dict[str, Any]]] = []
    for name, claim in claims.items():
        if claim.get("anti_pattern"):
            result.append((name, claim))
    return result


# Load manifest once for parametrize


def _load_manifest_claims() -> dict[str, Any]:
    """Load manifest claims for parametrize."""
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        result: dict[str, Any] = yaml.safe_load(f)["claims"]
        return result


_with_docs_manifest = _load_manifest_claims()
_with_anti_manifest = _load_manifest_claims()


@pytest.mark.parametrize(
    "claim_name",
    _get_all_claim_ids(claims=_load_manifest_claims()),
)
def test_all_claims_source_files_exist(claim_name: str, claims: dict[str, Any]) -> None:
    """Parametrized: verify source files exist for each claim."""
    claim = claims[claim_name]
    source = claim.get("source")
    if not source or source == "dynamic":
        pytest.skip("No static source file")
    source_path = REPO_ROOT / source
    assert source_path.exists(), f"Source file missing for claim '{claim_name}': {source}"


@pytest.mark.parametrize(
    "claim_name,claim",
    _get_claims_with_docs(claims=_with_docs_manifest),
    ids=[name for name, _ in _get_claims_with_docs(claims=_with_docs_manifest)],
)
def test_drift_docs_parametrized(claim_name: str, claim: dict[str, Any]) -> None:
    """Parametrized: validate docs match for all claims with docs."""
    expected = _expected_number(claim["current_value"])
    pattern = claim["pattern"]
    docs = claim["docs"]

    for doc_rel in docs:
        text = _read_doc_text(doc_rel)
        if text is None:
            pytest.skip(f"Doc file not found: {doc_rel}")
        numbers = _find_numbers_in_text(text, pattern)
        assert any(n == expected for n in numbers), (
            f"[{claim_name}] {doc_rel}: expected '{expected}' matching '{pattern}', found {numbers}"
        )


@pytest.mark.parametrize(
    "claim_name,claim",
    _get_claims_with_anti_pattern(claims=_with_anti_manifest),
    ids=[name for name, _ in _get_claims_with_anti_pattern(claims=_with_anti_manifest)],
)
def test_drift_anti_patterns_parametrized(claim_name: str, claim: dict[str, Any]) -> None:
    """Parametrized: validate anti-patterns not found in scope."""
    anti_pattern = claim["anti_pattern"]
    regex_str = anti_pattern["regex"]
    scope = anti_pattern["scope"]

    cli_files = list(REPO_ROOT.glob(scope))

    violations: list[str] = []
    for cli_file in cli_files:
        if not cli_file.is_file():
            continue
        text = cli_file.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            if re.search(regex_str, line):
                violations.append(f"{cli_file.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}")

    assert not violations, f"[{claim_name}] Anti-pattern found:\n" + "\n".join(violations)
