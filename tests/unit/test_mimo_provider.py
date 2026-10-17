"""MiMo (Xiaomi) tenth-provider integration contract.

Guards the invariants that make MiMo a *non-behaviour-changing* addition:

- ``mimo`` is a configuration-only provider (``backend: openai_compatible``).
- MiMo sits at the END of the ``standard`` and ``premium`` fallback chains and is
  absent from ``fast`` (primary routing is unchanged).
- Both MiMo models are priced in ``MODEL_COSTS``.
- ``MIMO_API_KEY`` is threaded through every env template / compose / CI surface.
- ``provider_count`` drift stays in sync with the provider catalog.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from ai_company.llm.cost_tracker import MODEL_COSTS

REPO_ROOT = Path(__file__).resolve().parents[2]


def _models() -> dict:
    return yaml.safe_load((REPO_ROOT / "company" / "models.yaml").read_text(encoding="utf-8"))


def test_mimo_provider_is_config_only() -> None:
    mimo = _models()["providers"]["mimo"]
    assert mimo["backend"] == "openai_compatible"
    assert mimo["api_base"] == "https://api.xiaomimimo.com/v1"
    assert mimo["default_model"] == "mimo-v2.5"


def test_mimo_is_last_in_standard_and_premium_and_absent_from_fast() -> None:
    tiers = _models()["tiers"]

    standard = tiers["standard"]["providers"]
    assert standard[-1] == {"provider": "mimo", "model": "mimo-v2.5"}

    premium = tiers["premium"]["providers"]
    assert premium[-1] == {"provider": "mimo", "model": "mimo-v2.5-pro"}

    fast = tiers["fast"]["providers"]
    assert not any(entry["provider"] == "mimo" for entry in fast)


def test_mimo_models_are_priced() -> None:
    assert MODEL_COSTS["mimo-v2.5"] == {"input": 0.14, "output": 0.28}
    assert MODEL_COSTS["mimo-v2.5-pro"] == {"input": 0.435, "output": 0.87}


def test_mimo_key_present_in_env_and_deploy_surfaces() -> None:
    surfaces = [
        ".env.example",
        ".env.staging.example",
        "docker-compose.yml",
        "docker-compose.staging.yml",
        ".github/workflows/autonomous.yml",
        ".github/workflows/repo-audit.yml",
        "AGENTS.md",
    ]
    for rel in surfaces:
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert "MIMO_API_KEY" in text, f"{rel} does not mention MIMO_API_KEY"


def test_provider_count_drift_matches_catalog() -> None:
    drift = yaml.safe_load(
        (REPO_ROOT / "docs" / "source-of-truth.yaml").read_text(encoding="utf-8")
    )
    count = drift["claims"]["provider_count"]["current_value"]
    assert count == len(_models()["providers"]), "provider_count drift is out of sync"


def test_mimocode_project_config_is_tracked_and_runtime_ignored() -> None:
    config = REPO_ROOT / ".mimocode" / "mimocode.jsonc"
    assert config.is_file(), ".mimocode/mimocode.jsonc must be tracked as project config"

    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    lines = {line.strip() for line in gitignore.splitlines()}
    assert ".mimocode/*" in lines
    assert "!.mimocode/mimocode.jsonc" in lines
    assert "/mimocode.jsonc" in lines
    assert "/mimocode.json" in lines
    # Unanchored patterns would also match `.mimocode/mimocode.jsonc` and defeat
    # the negation above, so they must never appear.
    assert "mimocode.jsonc" not in lines
    assert "mimocode.json" not in lines
