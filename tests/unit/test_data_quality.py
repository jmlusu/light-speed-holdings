"""Tests for data-quality audit, staleness indicators, and section errors."""

from __future__ import annotations

from pathlib import Path

# ── Data Gap Audit ─────────────────────────────────────────────────


class TestDataGapAudit:
    """Tests for DataGovernance.data_gap_audit()."""

    def test_data_gap_audit_returns_expected_shape(self, tmp_path: Path) -> None:
        """data_gap_audit returns a structured report with all required fields."""
        from ai_company.data.database import init_database
        from ai_company.data.governance import DataGovernance

        db = init_database(tmp_path / "test.db")
        gov = DataGovernance(db)
        report = gov.data_gap_audit()

        assert "generated_at" in report
        assert "total_sources" in report
        assert "available" in report
        assert "gaps" in report
        assert "sources" in report
        assert isinstance(report["sources"], list)
        assert report["total_sources"] > 0

    def test_data_gap_audit_classifies_sources(self, tmp_path: Path) -> None:
        """Each source has a status of available, empty, missing, or unreadable."""
        from ai_company.data.database import init_database
        from ai_company.data.governance import DataGovernance

        db = init_database(tmp_path / "test.db")
        gov = DataGovernance(db)
        report = gov.data_gap_audit()

        valid_statuses = {"available", "empty", "missing", "unreadable"}
        for source in report["sources"]:
            assert source["status"] in valid_statuses
            assert "source_id" in source
            assert "name" in source
            assert "required_for" in source

    def test_data_gap_audit_identifies_gaps(self, tmp_path: Path) -> None:
        """Gaps are listed for non-available sources."""
        from ai_company.data.database import init_database
        from ai_company.data.governance import DataGovernance

        db = init_database(tmp_path / "test.db")
        gov = DataGovernance(db)
        report = gov.data_gap_audit()

        # With no operational files, most sources should be gaps
        assert len(report["gaps"]) > 0
        for gap in report["gaps"]:
            assert "source_id" in gap
            assert "severity" in gap
            assert gap["severity"] in ("high", "medium", "low")

    def test_data_gap_audit_counts_available(self, tmp_path: Path) -> None:
        """available counts sources with status='available'."""
        from ai_company.data.database import init_database
        from ai_company.data.governance import DataGovernance

        db = init_database(tmp_path / "test.db")
        gov = DataGovernance(db)
        report = gov.data_gap_audit()

        available_count = sum(1 for s in report["sources"] if s["status"] == "available")
        assert report["available"] == available_count


# ── Data Quality API Endpoint ──────────────────────────────────────


class TestDataQualityEndpoint:
    """Tests for GET /api/v1/data-quality."""

    def test_data_quality_endpoint_returns_shape(self) -> None:
        """The data-quality endpoint returns the expected response shape."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/data-quality")
        assert resp.status_code == 200
        data = resp.json()
        assert "available" in data
        assert "generated_at" in data
        assert "total_sources" in data
        assert "gaps" in data
        assert "sources" in data
        assert "completeness_pct" in data

    def test_data_quality_endpoint_always_returns_200(self) -> None:
        """The endpoint never raises — always returns 200."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/data-quality")
        assert resp.status_code == 200


# ── Org Health Staleness ───────────────────────────────────────────


class TestOrgHealthStaleness:
    """Tests for staleness indicators in org-health response."""

    def test_org_health_returns_staleness(self) -> None:
        """The org-health endpoint returns a staleness object."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/org-health")
        assert resp.status_code == 200
        data = resp.json()
        assert "staleness" in data
        staleness = data["staleness"]
        assert "last_updated" in staleness
        assert "is_stale" in staleness

    def test_org_health_returns_missing_components(self) -> None:
        """The org-health endpoint returns missing_components list."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/org-health")
        assert resp.status_code == 200
        data = resp.json()
        assert "missing_components" in data
        assert isinstance(data["missing_components"], list)


# ── CEO Dashboard Section Errors ───────────────────────────────────


class TestCEODashboardSectionErrors:
    """Tests for section_errors in CEO dashboard response."""

    def test_ceo_dashboard_has_section_errors(self) -> None:
        """The CEO dashboard returns section_errors field."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/ceo-dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert "section_errors" in data
        assert isinstance(data["section_errors"], list)

    def test_ceo_dashboard_has_data_quality(self) -> None:
        """The CEO dashboard returns data_quality metadata."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/ceo-dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert "data_quality" in data
        dq = data["data_quality"]
        assert "completeness" in dq
        assert "notes" in dq

    def test_ceo_dashboard_has_staleness(self) -> None:
        """The CEO dashboard returns staleness info."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/ceo-dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert "staleness" in data
        staleness = data["staleness"]
        assert "overall" in staleness


# ── Company KPI Data Quality Fields ────────────────────────────────


class TestCompanyKPIDataQuality:
    """Tests for data_quality, data_gap, computed_at fields on company KPIs."""

    def test_company_kpis_have_data_quality_fields(self) -> None:
        """Each company KPI includes data_quality, data_gap, and computed_at."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/company-kpis")
        assert resp.status_code == 200
        data = resp.json()
        for kpi in data.get("kpis", []):
            assert "data_quality" in kpi, f"Missing data_quality on {kpi.get('id')}"
            assert "data_gap" in kpi, f"Missing data_gap on {kpi.get('id')}"
            assert "computed_at" in kpi, f"Missing computed_at on {kpi.get('id')}"
            assert kpi["data_quality"] in ("real", "config", "no_data", "fallback", "error")

    def test_company_kpis_summary_includes_no_data(self) -> None:
        """The summary includes a no_data count."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/company-kpis")
        assert resp.status_code == 200
        data = resp.json()
        summary = data.get("summary", {})
        assert "no_data" in summary
        assert isinstance(summary["no_data"], int)
