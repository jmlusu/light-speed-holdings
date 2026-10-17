"""Unit tests for the Pharos MCP server (ADR-020 P1, stdio JSON-RPC)."""

from __future__ import annotations

import json
import types
from pathlib import Path

import pytest

from ai_company.mcp.server import PROTOCOL_VERSION, PharosMcpServer

# ── fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture()
def rbac_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Provide run/approve/admin keys so RBAC is exercised deterministically."""
    monkeypatch.setenv("DASHBOARD_RUN_KEY", "run-secret")
    monkeypatch.setenv("DASHBOARD_APPROVE_KEY", "approve-secret")
    monkeypatch.setenv("DASHBOARD_ADMIN_KEY", "admin-secret")
    monkeypatch.delenv("DASHBOARD_AUTH_MODE", raising=False)


@pytest.fixture()
def server(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> PharosMcpServer:
    """A server with no side-effects: no audit writes, stub graph+memory."""

    class FakeGraphEngine:
        def list_graphs(self) -> list[str]:
            return ["knowledge_graph"]

        def get_graph(self, name: str):
            graph = FakeGraph()
            graph.name = name
            return graph

        def build_knowledge_graph(self) -> None:
            return None

    class FakeGraph:
        name = "knowledge_graph"

        def to_dict(self) -> dict:  # type: ignore[no-untyped-def]
            return {
                "name": self.name,
                "nodes": [{"id": "n1", "label": "Lighthouse pilot", "node_type": "initiative"}],
                "edges": [],
            }

    class FakeMemoryStore:
        def recall(self, memory_type: str, query: str = "", limit: int = 10):
            entry = types.SimpleNamespace(
                id="m1",
                memory_type=memory_type,
                content="Client call notes with phone 265-999-1234",
                tags=["pharos"],
                created_at="2026-09-01T00:00:00+00:00",
            )
            return [entry]

    class FakeMemoryFactory:
        def __call__(self):  # type: ignore[no-untyped-def]
            return FakeMemoryStore()

    monkeypatch.setenv("PHAROS_PUBLISH_DIR", str(tmp_path))
    return PharosMcpServer(
        use_audit=False,
        graph_factory=lambda: FakeGraphEngine(),
        memory_factory=FakeMemoryFactory(),
        docs_dir=tmp_path,
    )


def _call(
    server: PharosMcpServer, method: str, params: dict | None = None, rid: int | None = 1
) -> dict:
    request = {"jsonrpc": "2.0", "method": method, "id": rid, "params": params or {}}
    response = server.handle(json.dumps(request))
    assert response is not None
    return json.loads(response)


# ── protocol basics ───────────────────────────────────────────────────────────


def test_initialize(rbac_env: None) -> None:
    server = PharosMcpServer(use_audit=False)
    result = _call(server, "initialize", {"protocolVersion": PROTOCOL_VERSION})["result"]
    assert result["protocolVersion"] == PROTOCOL_VERSION
    assert result["capabilities"]["tools"] == {}
    assert result["serverInfo"]["name"] == "pharos-content-intelligence"


def test_initialize_echoes_supported_client_version(rbac_env: None) -> None:
    server = PharosMcpServer(use_audit=False)
    result = _call(server, "initialize", {"protocolVersion": "2024-11-05"})["result"]
    assert result["protocolVersion"] == "2024-11-05"


def test_ping(rbac_env: None) -> None:
    server = PharosMcpServer(use_audit=False)
    response = _call(server, "ping")
    assert response["result"] == {}


def test_tools_list(rbac_env: None, server: PharosMcpServer) -> None:
    result = _call(server, "tools/list")["result"]
    names = {tool["name"] for tool in result["tools"]}
    assert names == {
        "knowledge_graph_query",
        "memory_recall",
        "research_lookup",
        "pharos_reference",
        "publish_queue",
    }
    assert all("inputSchema" in tool for tool in result["tools"])


def test_unknown_method(rbac_env: None) -> None:
    server = PharosMcpServer(use_audit=False)
    response = _call(server, "bogus/method")
    assert response["error"]["code"] == -32601


def test_parse_error() -> None:
    server = PharosMcpServer(use_audit=False)
    response = json.loads(server.handle("{not json"))
    assert response["id"] is None
    assert response["error"]["code"] == -32700


def test_notification_returns_none(rbac_env: None) -> None:
    server = PharosMcpServer(use_audit=False)
    response = server.handle(
        json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
    )
    assert response is None


# ── auth gating ───────────────────────────────────────────────────────────────


def test_unauthorized_without_key(rbac_env: None, server: PharosMcpServer) -> None:
    response = _call(
        server, "tools/call", {"name": "memory_recall", "arguments": {"memory_type": "semantic"}}
    )
    assert response["error"]["code"] == -32001


def test_run_role_can_read(rbac_env: None, server: PharosMcpServer) -> None:
    response = _call(
        server,
        "tools/call",
        {
            "name": "memory_recall",
            "arguments": {"memory_type": "semantic"},
            "authorization": "run-secret",
        },
    )
    assert "error" not in response
    payload = json.loads(response["result"]["content"][0]["text"])
    assert payload["results"][0]["memory_type"] == "semantic"


def test_run_role_cannot_write(rbac_env: None, server: PharosMcpServer) -> None:
    response = _call(
        server,
        "tools/call",
        {
            "name": "publish_queue",
            "arguments": {"platform": "linkedin", "title": "T", "body": "B"},
            "authorization": "run-secret",
        },
    )
    assert response["error"]["code"] == -32001


def test_approve_role_can_write(rbac_env: None, server: PharosMcpServer) -> None:
    response = _call(
        server,
        "tools/call",
        {
            "name": "publish_queue",
            "arguments": {"platform": "linkedin", "title": "Queued", "body": "Body"},
            "authorization": "approve-secret",
        },
    )
    assert "error" not in response
    payload = json.loads(response["result"]["content"][0]["text"])
    assert payload["queued"] is True


def test_bearer_token_accepted(rbac_env: None, server: PharosMcpServer) -> None:
    response = _call(
        server,
        "tools/call",
        {
            "name": "memory_recall",
            "arguments": {"memory_type": "semantic"},
            "authorization": "Bearer admin-secret",
        },
    )
    assert "error" not in response


# ── tool behaviors ────────────────────────────────────────────────────────────


def test_knowledge_graph_get(rbac_env: None, server: PharosMcpServer) -> None:
    response = _call(
        server,
        "tools/call",
        {
            "name": "knowledge_graph_query",
            "arguments": {"graph_name": "knowledge_graph"},
            "authorization": "run-secret",
        },
    )
    payload = json.loads(response["result"]["content"][0]["text"])
    assert payload["name"] == "knowledge_graph"
    assert payload["nodes"][0]["label"] == "Lighthouse pilot"


def test_research_lookup_scans_corpus(
    rbac_env: None, server: PharosMcpServer, tmp_path: Path
) -> None:
    (tmp_path / "readme.md").write_text("Malawi architecture pilot summary.\n", encoding="utf-8")
    response = _call(
        server,
        "tools/call",
        {
            "name": "research_lookup",
            "arguments": {"query": "Malawi"},
            "authorization": "run-secret",
        },
    )
    payload = json.loads(response["result"]["content"][0]["text"])
    assert payload["corpus_dir"] == str(tmp_path)
    assert payload["results"][0]["path"] == "readme.md"


def test_pharos_reference_reads_doc(
    rbac_env: None, server: PharosMcpServer, tmp_path: Path
) -> None:
    (tmp_path / "positioning.md").write_text("# Positioning\n\nA strategy doc.\n", encoding="utf-8")
    response = _call(
        server,
        "tools/call",
        {
            "name": "pharos_reference",
            "arguments": {"name": "positioning"},
            "authorization": "run-secret",
        },
    )
    payload = json.loads(response["result"]["content"][0]["text"])
    assert payload["found"] is True
    assert "A strategy doc." in payload["body"]


def test_pharos_reference_unknown(rbac_env: None, server: PharosMcpServer) -> None:
    response = _call(
        server,
        "tools/call",
        {
            "name": "pharos_reference",
            "arguments": {"name": "missing_doc"},
            "authorization": "run-secret",
        },
    )
    payload = json.loads(response["result"]["content"][0]["text"])
    assert payload["found"] is False


def test_pharos_reference_path_traversal_blocked(
    rbac_env: None, server: PharosMcpServer, tmp_path: Path
) -> None:
    (tmp_path / "evil.md").write_text("secret\n", encoding="utf-8")
    response = _call(
        server,
        "tools/call",
        {
            "name": "pharos_reference",
            "arguments": {"name": "../evil"},
            "authorization": "run-secret",
        },
    )
    payload = json.loads(response["result"]["content"][0]["text"])
    assert payload["found"] is False


def test_memory_recall_masks_pii(rbac_env: None, server: PharosMcpServer) -> None:
    response = _call(
        server,
        "tools/call",
        {
            "name": "memory_recall",
            "arguments": {"memory_type": "episodic"},
            "authorization": "run-secret",
        },
    )
    payload = json.loads(response["result"]["content"][0]["text"])
    assert "265-999-1234" not in payload["results"][0]["content"]


def test_unknown_tool(rbac_env: None, server: PharosMcpServer) -> None:
    response = _call(
        server,
        "tools/call",
        {"name": "nonexistent_tool", "arguments": {}, "authorization": "run-secret"},
    )
    assert response["error"]["code"] == -32602


# ── audit wiring ──────────────────────────────────────────────────────────────


def test_tool_call_is_audited(rbac_env: None, tmp_path: Path) -> None:
    """Every authorized tool call is recorded with its auth role."""

    class Recorder:
        def __init__(self) -> None:
            self.events = []

        def write(self, event) -> None:  # type: ignore[no-untyped-def]
            self.events.append(event)

    recorder = Recorder()

    class FakeGraph:
        def to_dict(self) -> dict:  # type: ignore[no-untyped-def]
            return {"name": "knowledge_graph", "nodes": [], "edges": []}

    class FakeEngine:
        def list_graphs(self) -> list[str]:
            return ["knowledge_graph"]

        def get_graph(self, name: str):
            return FakeGraph()

        def build_knowledge_graph(self) -> None:
            return None

    server = PharosMcpServer(
        use_audit=True,
        audit_writer=recorder,
        graph_factory=lambda: FakeEngine(),
        docs_dir=tmp_path,
    )
    response = _call(
        server,
        "tools/call",
        {
            "name": "knowledge_graph_query",
            "arguments": {"graph_name": "knowledge_graph"},
            "authorization": "run-secret",
        },
    )
    assert "error" not in response
    events = recorder.events
    assert any(e.tool == "knowledge_graph_query" for e in events)
    assert any(e.metadata.get("auth_role") == "run" for e in events)
