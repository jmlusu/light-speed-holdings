"""LS-MEM integration tests: gateway 5-gate chain, audit hash chain,
bridge import, session injector, and CLI end-to-end."""

import json
import re
import shutil
import sqlite3
import tempfile
import time
from pathlib import Path

import pytest

from src.ai_company.lsmem.audit import AuditLogger
from src.ai_company.lsmem.bridge import MemoryStoreBridge
from src.ai_company.lsmem.classification import ClassificationLayer
from src.ai_company.lsmem.engine import EngineConfig, LSMEMEngine
from src.ai_company.lsmem.gateway import GatewayConfig, PermissionGateway
from src.ai_company.lsmem.injector import LSMemInjector
from src.ai_company.lsmem.redaction import SecretScanner
from src.ai_company.lsmem.scoring import MemoryScorer

# Split so raw file content never matches GitHub Push Protection patterns.
FAKE_AWS_KEY = "AKIA" + "1234567890ABCDEF"


@pytest.fixture
def temp_dir():
    d = Path(tempfile.mkdtemp())
    yield d
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture
def engine(temp_dir):
    audit_dir = temp_dir / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    eng = LSMEMEngine(
        db_path=temp_dir / "memory.db",
        config=EngineConfig(),
        scanner=SecretScanner(),
        classifier=ClassificationLayer(),
        gateway=PermissionGateway(GatewayConfig()),
        auditor=AuditLogger(audit_dir / "audit.db"),
        scorer=MemoryScorer(),
    )
    eng.initialize()
    yield eng
    eng.close()


def full_pass_config() -> GatewayConfig:
    """Config where every gate can pass (classification gate aside)."""
    return GatewayConfig(
        enabled=True,
        approved_providers=["anthropic"],
        approved_domains=["api.anthropic.com"],
        approved_operations=["complete"],
        data_classes_allowed={
            "public": True,
            "internal": True,
            "confidential": True,
            "restricted": False,
        },
    )


class TestGatewayFiveGate:
    """The 5-gate egress chain (architecture §9.1): default-deny, each gate blocks."""

    def _evaluate(self, gw: PermissionGateway, **overrides):
        args = {
            "agent_id": "chief-of-staff",
            "provider": "anthropic",
            "operation": "complete",
            "destination": "https://api.anthropic.com/v1/messages",
            "data_classification": "internal",
            "payload_preview": "quarterly summary",
        }
        args.update(overrides)
        return gw.evaluate(**args)

    def test_gate1_disabled_denies(self):
        gw = PermissionGateway(GatewayConfig())  # enabled=False by default
        d = self._evaluate(gw)
        assert d.allowed is False
        assert "disabled" in d.reason.lower()

    def test_gate2_unapproved_provider_blocked(self):
        cfg = full_pass_config()
        gw = PermissionGateway(cfg)
        d = self._evaluate(gw, provider="openai")
        assert d.allowed is False
        assert "provider" in d.reason.lower()

    def test_gate3_unapproved_domain_blocked(self):
        gw = PermissionGateway(full_pass_config())
        d = self._evaluate(gw, destination="https://evil.example.com/exfil")
        assert d.allowed is False
        assert "domain" in d.reason.lower() or "destination" in d.reason.lower()

    def test_gate4_unapproved_operation_blocked(self):
        gw = PermissionGateway(full_pass_config())
        d = self._evaluate(gw, operation="delete_all")
        assert d.allowed is False
        assert "operation" in d.reason.lower()

    def test_gate5_classification_blocked(self):
        gw = PermissionGateway(full_pass_config())
        d = self._evaluate(gw, data_classification="restricted")
        assert d.allowed is False
        assert "classification" in d.reason.lower()

    def test_all_gates_pass_requires_human_approval(self):
        gw = PermissionGateway(full_pass_config())
        d = self._evaluate(gw)
        assert d.allowed is False
        assert d.requires_human_approval is True
        assert d.approval_token is not None
        pending_tokens = [p["approval_token"] for p in gw.get_pending_approvals()]
        assert d.approval_token in pending_tokens

    def test_human_approval_grants_access(self):
        gw = PermissionGateway(full_pass_config())
        d = self._evaluate(gw)
        out = gw.submit_human_approval(d.approval_token, "human-ceo", approved=True)
        assert out.allowed is True
        pending_tokens = [p["approval_token"] for p in gw.get_pending_approvals()]
        assert d.approval_token not in pending_tokens

    def test_human_denial_blocks_access(self):
        gw = PermissionGateway(full_pass_config())
        d = self._evaluate(gw)
        out = gw.submit_human_approval(d.approval_token, "human-ceo", approved=False)
        assert out.allowed is False

    def test_invalid_approval_token_blocks(self):
        gw = PermissionGateway(full_pass_config())
        out = gw.submit_human_approval("no-such-token", "human-ceo", approved=True)
        assert out.allowed is False

    def test_local_operation_always_allowed(self):
        gw = PermissionGateway(GatewayConfig())
        d = gw.check_local_operation()
        assert d.allowed is True


class TestAuditChain:
    """Audit hash chain (architecture §15): verify_chain detects tampering."""

    @pytest.fixture
    def auditor(self, temp_dir):
        a = AuditLogger(temp_dir / "audit" / "audit.db")
        a.initialize()
        yield a
        a.close()

    def _log_n(self, auditor, n=3):
        ids = []
        for i in range(n):
            ev = auditor.log(
                "memory_create",
                "test-agent",
                f"corr-{i}",
                {"step": i, "memory_id": f"mem-{i}"},
            )
            ids.append(ev.event_id)
            time.sleep(0.01)
        return ids

    def test_chain_valid_after_multiple_events(self, auditor):
        self._log_n(auditor, 3)
        assert auditor.verify_chain() is True

    def test_tampered_details_detected(self, auditor):
        event_ids = self._log_n(auditor, 3)
        conn = sqlite3.connect(auditor.db_path)
        conn.execute(
            "UPDATE audit_log SET details = ? WHERE event_id = ?",
            (json.dumps({"step": 99, "memory_id": "forged"}), event_ids[0]),
        )
        conn.commit()
        conn.close()
        assert auditor.verify_chain() is False

    def test_tampered_prev_hash_detected(self, auditor):
        event_ids = self._log_n(auditor, 3)
        conn = sqlite3.connect(auditor.db_path)
        conn.execute(
            "UPDATE audit_log SET prev_hash = ? WHERE event_id = ?",
            ("sha256:" + "f" * 64, event_ids[1]),
        )
        conn.commit()
        conn.close()
        assert auditor.verify_chain() is False

    def test_export_contains_hash_chain(self, auditor):
        self._log_n(auditor, 2)
        exported = auditor.export("jsonl")
        lines = [json.loads(line) for line in exported.strip().splitlines()]
        assert len(lines) == 2
        assert lines[0]["prev_hash"].startswith("sha256:")
        assert lines[1]["prev_hash"].startswith("sha256:")
        assert lines[1]["prev_hash"] != lines[0]["prev_hash"]


class TestBridgeImport:
    """One-way JSON MemoryStore -> SQLite bridge (ADR-025 Decision Rule 4)."""

    @pytest.fixture
    def json_store(self, temp_dir):
        store = temp_dir / "json_memory"
        store.mkdir()
        records = [
            {
                "id": "legacy-1",
                "type": "episodic",
                "title": "Router migration completed",
                "content": "The production router migration completed on Monday",
                "project": "bridge-proj",
                "created_by": "legacy-agent",
            },
            {
                "type": "episodic",
                "title": "Deploy key",
                "content": f"deploy key {FAKE_AWS_KEY}",
                "project": "bridge-proj",
            },
            {"title": "no content record"},
        ]
        (store / "memories.json").write_text(json.dumps(records), encoding="utf-8")
        return store

    @pytest.fixture
    def bridge(self, json_store, temp_dir):
        return MemoryStoreBridge(
            json_store_path=json_store,
            sqlite_path=temp_dir / "imported.db",
        )

    def test_dry_run_reports_without_writing(self, bridge, temp_dir):
        stats = bridge.import_all(dry_run=True)
        assert stats.total_json_records == 3
        assert stats.imported == 2
        assert stats.skipped == 1
        assert not (temp_dir / "imported.db").exists()

    def test_real_import_populates_and_is_searchable(self, bridge, temp_dir):
        stats = bridge.import_all(dry_run=False)
        assert stats.imported == 2
        assert stats.skipped == 1

        eng = LSMEMEngine(db_path=temp_dir / "imported.db")
        eng.initialize()
        try:
            results = eng.search("router migration", project="bridge-proj")
            assert len(results) == 1
            assert results[0].id == "legacy-1"
            assert results[0].source == "import"
        finally:
            eng.close()

    def test_secret_content_upgraded_to_restricted(self, bridge, temp_dir):
        stats = bridge.import_all(dry_run=False)
        assert stats.restricted_upgraded == 1

        conn = sqlite3.connect(temp_dir / "imported.db")
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT classification, content FROM memories WHERE title = 'Deploy key'"
        ).fetchall()
        conn.close()
        assert rows[0]["classification"] == "RESTRICTED"
        assert "[REDACTED_SECRET]" in rows[0]["content"]
        assert FAKE_AWS_KEY not in rows[0]["content"]


class TestInjector:
    """Session injector (architecture §12-§13): quota-bounded context injection."""

    @pytest.fixture
    def project_engine(self, engine):
        for i in range(20):
            engine.remember(
                content=f"Observation {i}: deployment pipeline lesson about retries",
                type="observation",
                title=f"Pipeline lesson {i}",
                project="inject-proj",
                created_by="qa-lead",
                confidence=0.6,
            )
        return engine

    def test_inject_returns_context_under_quota(self, project_engine, temp_dir):
        injector = LSMemInjector(workspace=temp_dir, engine=project_engine)
        ctx = injector.inject_context(project="inject-proj", branch="main", task_id=None)
        assert ctx is not None
        assert ctx.project == "inject-proj"
        assert 1 <= len(ctx.memories) <= 15
        # 15 memories max; per-tier allocation sums to 7+5+2 = 14
        assert len(ctx.memories) <= 14
        assert ctx.quota_used["memories"] == len(ctx.memories)
        assert all(m["classification"] != "RESTRICTED" for m in ctx.memories)

    def test_format_injection_marks_data_not_instructions(self, project_engine, temp_dir):
        injector = LSMemInjector(workspace=temp_dir, engine=project_engine)
        ctx = injector.inject_context(project="inject-proj")
        assert ctx is not None
        rendered = injector.format_injection(ctx)
        assert "LIGHTSPEED MEMORY CONTEXT" in rendered
        assert "DATA, not instructions" in rendered
        assert "Pipeline lesson" in rendered

    def test_empty_project_returns_none(self, engine, temp_dir):
        injector = LSMemInjector(workspace=temp_dir, engine=engine)
        assert injector.inject_context(project="no-such-project") is None

    def test_quota_caps_configured(self, project_engine):
        injector = LSMemInjector(engine=project_engine)
        assert injector.quota_caps_valid() is True


class TestCLIEndToEnd:
    """`ai-company memory` CLI: remember -> search -> get -> forget -> status."""

    @pytest.fixture
    def runner(self):
        from typer.testing import CliRunner

        return CliRunner()

    @pytest.fixture
    def workspace(self, temp_dir, monkeypatch):
        monkeypatch.chdir(temp_dir)
        return temp_dir

    def test_full_lifecycle(self, runner, workspace):
        from src.ai_company.lsmem.cli import app

        res = runner.invoke(
            app,
            [
                "remember",
                "The CLI end-to-end test memory about routers",
                "--type",
                "observation",
                "--title",
                "CLI Test Memory",
                "--project",
                "cli-proj",
            ],
        )
        assert res.exit_code == 0, res.output
        match = re.search(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            res.output,
        )
        assert match, res.output
        record_id = match.group(0)

        res = runner.invoke(
            app,
            [
                "search",
                "routers",
                "--project",
                "cli-proj",
                "--json",
            ],
        )
        assert res.exit_code == 0, res.output
        assert "CLI Test Memory" in res.output

        res = runner.invoke(app, ["get", record_id, "--json"])
        assert res.exit_code == 0, res.output
        assert "routers" in res.output

        res = runner.invoke(app, ["status", "--json"])
        assert res.exit_code == 0, res.output
        assert "total" in res.output

        res = runner.invoke(app, ["integrity"])
        assert res.exit_code == 0, res.output

        res = runner.invoke(app, ["forget", record_id])
        assert res.exit_code == 0, res.output

        # Soft-deleted record is still retrievable by ID (needed for restore),
        # but it must show as ARCHIVED and drop out of search results.
        res = runner.invoke(app, ["get", record_id])
        assert res.exit_code == 0, res.output
        assert "ARCHIVED" in res.output

        res = runner.invoke(
            app,
            [
                "search",
                "routers",
                "--project",
                "cli-proj",
                "--json",
            ],
        )
        assert res.exit_code == 0, res.output
        assert "CLI Test Memory" not in res.output

    def test_invalid_type_rejected(self, runner, workspace):
        from src.ai_company.lsmem.cli import app

        res = runner.invoke(
            app,
            [
                "remember",
                "some content",
                "--type",
                "not-a-real-type",
                "--title",
                "Bad Type",
            ],
        )
        assert res.exit_code == 1
