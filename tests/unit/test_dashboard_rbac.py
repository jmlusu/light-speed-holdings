"""Tests for ADR-012 — dashboard RBAC + ``open``-mode loopback restriction."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from typer.testing import CliRunner

# Shared role keys used across the HTTP tests.
RUN_KEY = "test-run-key"
APPROVE_KEY = "test-approve-key"
ADMIN_KEY = "test-admin-key"
LEGACY_KEY = "test-legacy-key"


@pytest.fixture(autouse=True)
def _anchor_data_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Anchor DASHBOARD_DATA_DIR so the dashboard writes to a per-test dir."""
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))


def _setup_minimal_data(tmp_path: Path) -> None:
    """Write the minimal data files the dashboard endpoints read."""
    (tmp_path / "company").mkdir(exist_ok=True)
    (tmp_path / "company" / "agent-registry.json").write_text("[]", encoding="utf-8")
    (tmp_path / ".opencode").mkdir(exist_ok=True)
    (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
    (tmp_path / "orchestrator").mkdir(exist_ok=True)
    (tmp_path / "orchestrator" / "approvals.yaml").write_text(
        "requests:\n"
        "  - id: apr-rbac-1\n"
        "    status: pending\n"
        "    agent_id: eng-1\n"
        "    action: run_pipeline\n"
        "    description: Approve pipeline run\n"
        "    priority: high\n",
        encoding="utf-8",
    )
    (tmp_path / "orchestrator" / "escalation.yaml").write_text(
        "rules: []\n"
        "events:\n"
        "  - task_id: tsk-rbac-1\n"
        "    resolved: false\n"
        "    from_agent: eng-1\n"
        "    to_agent: ceo\n"
        "    reason: test escalation\n",
        encoding="utf-8",
    )
    (tmp_path / "orchestrator" / "scheduler.yaml").write_text("tasks: []", encoding="utf-8")
    (tmp_path / "company" / "departments.yaml").write_text("departments: []", encoding="utf-8")

    real_models = Path(__file__).resolve().parents[2] / "company" / "models.yaml"
    if real_models.exists():
        shutil.copy2(str(real_models), str(tmp_path / "company" / "models.yaml"))


def _enable_role_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DASHBOARD_RUN_KEY", RUN_KEY)
    monkeypatch.setenv("DASHBOARD_APPROVE_KEY", APPROVE_KEY)
    monkeypatch.setenv("DASHBOARD_ADMIN_KEY", ADMIN_KEY)
    monkeypatch.setenv("DASHBOARD_API_KEY", LEGACY_KEY)
    monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)


# ── role_for_key / hierarchy (unit) ───────────────────────────────────


class TestRoleForKey:
    def test_maps_role_keys(self, monkeypatch: pytest.MonkeyPatch) -> None:
        _enable_role_keys(monkeypatch)
        from ai_company.security.rbac import Role, role_for_key

        assert role_for_key(RUN_KEY) is Role.RUN
        assert role_for_key(APPROVE_KEY) is Role.APPROVE
        assert role_for_key(ADMIN_KEY) is Role.ADMIN

    def test_unknown_and_empty_keys_rejected(self, monkeypatch: pytest.MonkeyPatch) -> None:
        _enable_role_keys(monkeypatch)
        from ai_company.security.rbac import role_for_key

        assert role_for_key("totally-unknown-key") is None
        assert role_for_key("") is None

    def test_legacy_dashboard_api_key_is_admin_alias(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DASHBOARD_RUN_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_APPROVE_KEY", raising=False)
        monkeypatch.delenv("DASHBOARD_ADMIN_KEY", raising=False)
        monkeypatch.setenv("DASHBOARD_API_KEY", LEGACY_KEY)
        from ai_company.security.rbac import Role, role_for_key

        assert role_for_key(LEGACY_KEY) is Role.ADMIN

    def test_role_rank_hierarchy(self) -> None:
        from ai_company.security.rbac import _RANK, Role

        assert _RANK[Role.RUN] < _RANK[Role.APPROVE] < _RANK[Role.ADMIN]


# ── open-mode loopback restriction (unit) ─────────────────────────────


class TestLoopbackRestriction:
    def test_is_loopback_host(self) -> None:
        from ai_company.dashboard.app import is_loopback_host

        assert is_loopback_host("127.0.0.1")
        assert is_loopback_host("127.0.0.2")
        assert is_loopback_host("::1")
        assert is_loopback_host("localhost")
        assert not is_loopback_host("0.0.0.0")
        assert not is_loopback_host("192.168.1.5")
        assert not is_loopback_host("example.com")

    def test_open_mode_rejects_non_loopback_host(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DASHBOARD_HOST", raising=False)
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "open")
        from ai_company.dashboard.app import create_app

        monkeypatch.setenv("DASHBOARD_HOST", "0.0.0.0")
        with pytest.raises(RuntimeError, match="loopback"):
            create_app()

    def test_open_mode_allows_loopback_host(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "open")
        monkeypatch.setenv("DASHBOARD_HOST", "127.0.0.1")
        monkeypatch.chdir(tmp_path)
        _setup_minimal_data(tmp_path)
        from ai_company.dashboard.app import create_app

        assert create_app() is not None

    def test_api_key_mode_allows_non_loopback_host(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "api_key")
        monkeypatch.setenv("DASHBOARD_HOST", "0.0.0.0")
        monkeypatch.chdir(tmp_path)
        _setup_minimal_data(tmp_path)
        from ai_company.dashboard.app import create_app

        assert create_app() is not None

    def test_cli_refuses_open_mode_on_non_loopback(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", "open")
        from ai_company.cli.dashboard import app as cli_app

        runner = CliRunner()
        result = runner.invoke(cli_app, ["--host", "0.0.0.0"])
        assert result.exit_code == 1
        assert "loopback" in result.output


# ── RBAC on HTTP endpoints ────────────────────────────────────────────


class TestEndpointRBAC:
    """Verify role keys gate dashboard write endpoints end-to-end."""

    def _api_client(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        mode: str = "api_key",
    ) -> TestClient:
        _enable_role_keys(monkeypatch)
        monkeypatch.setenv("DASHBOARD_AUTH_MODE", mode)
        monkeypatch.delenv("DASHBOARD_HOST", raising=False)
        monkeypatch.chdir(tmp_path)
        _setup_minimal_data(tmp_path)

        from ai_company.dashboard.app import create_app

        return TestClient(create_app())

    def test_task_create_requires_run(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        client = self._api_client(monkeypatch, tmp_path)
        body = {"receiver_id": "agent", "instruction": "do something"}
        assert client.post("/api/tasks", json=body).status_code == 401
        assert (
            client.post("/api/tasks", json=body, headers={"X-API-Key": "wrong-key"}).status_code
            == 401
        )
        assert (
            client.post("/api/tasks", json=body, headers={"X-API-Key": RUN_KEY}).status_code == 201
        )
        # approve/admin outrank run — allowed by the role hierarchy.
        assert (
            client.post("/api/tasks", json=body, headers={"X-API-Key": APPROVE_KEY}).status_code
            == 201
        )
        assert (
            client.post("/api/tasks", json=body, headers={"X-API-Key": ADMIN_KEY}).status_code
            == 201
        )

    def test_task_update_and_delete_require_run(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        client = self._api_client(monkeypatch, tmp_path)
        created = client.post(
            "/api/tasks",
            json={"receiver_id": "agent", "instruction": "do something"},
            headers={"X-API-Key": RUN_KEY},
        ).json()
        task_id = created["id"]

        patch = {"priority": "high"}
        # approve outranks run — allowed by the role hierarchy.
        assert (
            client.patch(
                f"/api/tasks/{task_id}", json=patch, headers={"X-API-Key": APPROVE_KEY}
            ).status_code
            == 200
        )
        assert (
            client.patch(
                f"/api/tasks/{task_id}", json=patch, headers={"X-API-Key": RUN_KEY}
            ).status_code
            == 200
        )
        assert (
            client.delete(f"/api/tasks/{task_id}", headers={"X-API-Key": RUN_KEY}).status_code
            == 200
        )
        # Second task: admin key may also delete.
        created2 = client.post(
            "/api/tasks",
            json={"receiver_id": "agent", "instruction": "do something else"},
            headers={"X-API-Key": RUN_KEY},
        ).json()
        assert (
            client.delete(
                f"/api/tasks/{created2['id']}", headers={"X-API-Key": ADMIN_KEY}
            ).status_code
            == 200
        )

    def test_approve_and_reject_require_approve(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        client = self._api_client(monkeypatch, tmp_path)
        approve_url = "/api/approvals/apr-rbac-1/approve"
        reject_url = "/api/approvals/apr-rbac-1/reject"

        assert client.post(approve_url, headers={"X-API-Key": RUN_KEY}).status_code == 403
        assert client.post(approve_url, headers={"X-API-Key": APPROVE_KEY}).status_code == 200
        # Rejected the second time — the request was already processed.
        assert client.post(approve_url, headers={"X-API-Key": ADMIN_KEY}).status_code == 404
        assert client.post(reject_url, headers={"X-API-Key": RUN_KEY}).status_code == 403

    def test_resolve_escalation_requires_approve(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        client = self._api_client(monkeypatch, tmp_path)
        url = "/api/escalations/tsk-rbac-1/resolve"

        assert client.post(url, headers={"X-API-Key": RUN_KEY}).status_code == 403
        assert client.post(url, headers={"X-API-Key": APPROVE_KEY}).status_code == 200

    def test_mobile_approval_writes_require_approve(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        client = self._api_client(monkeypatch, tmp_path)

        # Batch actions
        assert (
            client.post(
                "/api/mobile/actions/batch",
                json={"actions": []},
                headers={"X-API-Key": RUN_KEY},
            ).status_code
            == 403
        )
        assert (
            client.post(
                "/api/mobile/actions/batch",
                json={"actions": []},
                headers={"X-API-Key": APPROVE_KEY},
            ).status_code
            == 200
        )

        # Quick-approve all
        assert (
            client.post(
                "/api/mobile/actions/quick-approve",
                json={"confirm": True},
                headers={"X-API-Key": RUN_KEY},
            ).status_code
            == 403
        )
        assert (
            client.post(
                "/api/mobile/actions/quick-approve",
                json={"confirm": True},
                headers={"X-API-Key": APPROVE_KEY},
            ).status_code
            == 200
        )

        # Swipe gesture
        swipe = {"request_id": "apr-rbac-1", "decision": "skip"}
        assert (
            client.post(
                "/api/mobile/approvals/swipe",
                json=swipe,
                headers={"X-API-Key": RUN_KEY},
            ).status_code
            == 403
        )
        assert (
            client.post(
                "/api/mobile/approvals/swipe",
                json=swipe,
                headers={"X-API-Key": APPROVE_KEY},
            ).status_code
            == 200
        )

        # Sync (processes approve/reject/resolve actions)
        assert (
            client.post(
                "/api/mobile/sync",
                json={"pending_actions": []},
                headers={"X-API-Key": RUN_KEY},
            ).status_code
            == 403
        )
        assert (
            client.post(
                "/api/mobile/sync",
                json={"pending_actions": []},
                headers={"X-API-Key": APPROVE_KEY},
            ).status_code
            == 200
        )

    def test_mobile_device_writes_require_run(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        client = self._api_client(monkeypatch, tmp_path)
        reg = {"device_token": "tok-1", "platform": "ios"}

        assert (
            client.post(
                "/api/mobile/notifications/register",
                json=reg,
                headers={"X-API-Key": "wrong-key"},
            ).status_code
            == 401
        )
        assert (
            client.post(
                "/api/mobile/notifications/register",
                json=reg,
                headers={"X-API-Key": RUN_KEY},
            ).status_code
            == 200
        )
        # approve is a higher role — allowed by hierarchy.
        assert (
            client.post(
                "/api/mobile/notifications/register",
                json=reg,
                headers={"X-API-Key": APPROVE_KEY},
            ).status_code
            == 200
        )
        assert (
            client.patch(
                "/api/mobile/notifications/preferences",
                json={"device_token": "tok-1", "preferences": {}},
                headers={"X-API-Key": RUN_KEY},
            ).status_code
            == 200
        )
        assert (
            client.request(
                "DELETE",
                "/api/mobile/notifications/unregister",
                json=reg,
                headers={"X-API-Key": RUN_KEY},
            ).status_code
            == 200
        )

    def test_open_mode_treats_all_requests_as_admin(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        client = self._api_client(monkeypatch, tmp_path, mode="open")
        body = {"receiver_id": "agent", "instruction": "do something"}
        assert client.post("/api/tasks", json=body).status_code == 201
        assert client.post("/api/approvals/apr-rbac-1/approve").status_code == 200
