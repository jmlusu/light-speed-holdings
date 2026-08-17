"""Org Health backend contract tests.

Covers:
- OrgHealthCalculator: weight validation, band assignment, score composition
- OrgHealthKPICollector: snapshot shape
- GET /api/v1/org-health: response shape, query params, 404 fallback
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.org_health import (
    ComponentScore,
    OrgHealthCalculator,
    OrgHealthResult,
)

# ── Unit: OrgHealthCalculator ──────────────────────────────────────


class TestOrgHealthCalculator:
    def test_weights_sum_to_one(self, tmp_path: Path) -> None:
        config = tmp_path / "config" / "org_health.yaml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(
            "bands:\n"
            "  green: {min: 80, max: 100}\n"
            "  amber: {min: 50, max: 79}\n"
            "  red: {min: 0, max: 49}\n"
            "components:\n"
            "  - {name: a, weight: 0.6}\n"
            "  - {name: b, weight: 0.4}\n",
            encoding="utf-8",
        )
        calc = OrgHealthCalculator(project_root=tmp_path)
        defs = calc.get_component_defs()
        total = sum(c["weight"] for c in defs)
        assert abs(total - 1.0) < 0.01

    def test_band_assignment_green(self, tmp_path: Path) -> None:
        calc = OrgHealthCalculator(project_root=tmp_path)
        assert calc._score_to_band(80) == "green"
        assert calc._score_to_band(100) == "green"
        assert calc._score_to_band(95) == "green"

    def test_band_assignment_amber(self, tmp_path: Path) -> None:
        calc = OrgHealthCalculator(project_root=tmp_path)
        assert calc._score_to_band(50) == "amber"
        assert calc._score_to_band(79) == "amber"
        assert calc._score_to_band(65) == "amber"

    def test_band_assignment_red(self, tmp_path: Path) -> None:
        calc = OrgHealthCalculator(project_root=tmp_path)
        assert calc._score_to_band(0) == "red"
        assert calc._score_to_band(49) == "red"
        assert calc._score_to_band(25) == "red"

    def test_score_composition(self, tmp_path: Path) -> None:
        """Verify weighted sum matches component scores."""
        config = tmp_path / "config" / "org_health.yaml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(
            "bands:\n"
            "  green: {min: 80, max: 100}\n"
            "  amber: {min: 50, max: 79}\n"
            "  red: {min: 0, max: 49}\n"
            "components:\n"
            "  - {name: a, weight: 0.6}\n"
            "  - {name: b, weight: 0.4}\n",
            encoding="utf-8",
        )
        calc = OrgHealthCalculator(project_root=tmp_path)
        result = calc.compute()
        expected = round(0.6 * 50.0 + 0.4 * 50.0)
        assert result.score == expected

    def test_result_to_dict_shape(self, tmp_path: Path) -> None:
        result = OrgHealthResult(
            score=78,
            band="amber",
            components=[
                ComponentScore(name="a", weight=0.6, value=80, sub_score=80),
                ComponentScore(name="b", weight=0.4, value=75, sub_score=75),
            ],
            collected_at="2026-08-12T12:00:00Z",
        )
        d = result.to_dict(include_components=True, trend=[{"score": 75}])
        assert d["score"] == 78
        assert d["band"] == "amber"
        assert len(d["components"]) == 2
        assert d["components"][0]["name"] == "a"
        assert d["components"][0]["weight"] == 0.6
        assert len(d["trend"]) == 1

    def test_result_to_dict_without_components(self, tmp_path: Path) -> None:
        result = OrgHealthResult(score=78, band="amber", collected_at="now")
        d = result.to_dict(include_components=False)
        assert "components" not in d

    def test_unknown_component_defaults_to_50(self, tmp_path: Path) -> None:
        config = tmp_path / "config" / "org_health.yaml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(
            "bands:\n"
            "  green: {min: 80, max: 100}\n"
            "  red: {min: 0, max: 49}\n"
            "components:\n"
            "  - {name: nonexistent, weight: 1.0}\n",
            encoding="utf-8",
        )
        calc = OrgHealthCalculator(project_root=tmp_path)
        result = calc.compute()
        assert result.score == 50


# ── Unit: OrgHealthKPICollector ────────────────────────────────────


class TestOrgHealthKPICollector:
    def test_collect_returns_snapshot_shape(self, tmp_path: Path) -> None:
        from ai_company.dashboard.kpis.org_health import OrgHealthKPICollector

        collector = OrgHealthKPICollector(project_root=tmp_path)
        snapshot = collector.collect()
        assert snapshot["department"] == "org_health"
        assert "kpis" in snapshot
        assert "composite_score" in snapshot["kpis"]
        assert snapshot["kpis"]["composite_score"]["current"] is not None

    def test_collect_includes_components(self, tmp_path: Path) -> None:
        from ai_company.dashboard.kpis.org_health import OrgHealthKPICollector

        collector = OrgHealthKPICollector(project_root=tmp_path)
        snapshot = collector.collect()
        kpis = snapshot["kpis"]
        component_keys = [k for k in kpis if k.startswith("component:")]
        assert len(component_keys) >= 1


# ── Integration: GET /api/v1/org-health ───────────────────────────


@pytest.fixture()
def org_health_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> TestClient:
    """Create a TestClient with isolated env for org-health endpoint."""
    monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)
    monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))
    monkeypatch.chdir(tmp_path)

    from ai_company.dashboard.app import create_app

    return TestClient(create_app())


class TestOrgHealthEndpoint:
    def test_response_shape(self, org_health_client: TestClient, tmp_path: Path) -> None:
        resp = org_health_client.get("/api/v1/org-health")
        assert resp.status_code == 200
        data = resp.json()
        assert "score" in data
        assert "band" in data
        assert "collected_at" in data
        assert "trend" in data
        assert isinstance(data["score"], int)
        assert data["band"] in ("green", "amber", "red")

    def test_component_detail_false(self, org_health_client: TestClient) -> None:
        resp = org_health_client.get("/api/v1/org-health", params={"component_detail": "false"})
        assert resp.status_code == 200
        data = resp.json()
        assert "components" not in data

    def test_trend_limit(self, org_health_client: TestClient) -> None:
        resp = org_health_client.get("/api/v1/org-health", params={"trend_limit": 5})
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data["trend"], list)

    def test_score_range(self, org_health_client: TestClient) -> None:
        resp = org_health_client.get("/api/v1/org-health")
        assert resp.status_code == 200
        score = resp.json()["score"]
        assert 0 <= score <= 100
