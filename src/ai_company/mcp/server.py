"""Pharos Content Intelligence MCP — a minimal in-house stdio JSON-RPC server.

Exposes LightSpeed stores as MCP tools (ADR-020 section 3) without any
third-party MCP SDK:

- ``knowledge_graph_query`` — GraphEngine over the loaded CompanyRegistry.
- ``memory_recall`` — MemoryStore semantic/string recall.
- ``research_lookup`` — keyword scan of the ``docs/Pharos`` regional corpus.
- ``pharos_reference`` — read a ``docs/Pharos`` document by name (path-safe).
- ``publish_queue`` — write tool; enqueues a platform-ready artifact
  (requires ``approve``/``admin`` RBAC role).

Security per ADR-020: X-API-Key authorization (``params.authorization`` →
``rbac.role_for_key``), read tools require ``run`` or higher, the write tool
requires ``approve`` or higher; every call is audit-logged; outputs pass the
content filter and a PII mask before being returned. The protocol subset is
``initialize`` / ``ping`` / ``tools/list`` / ``tools/call`` over newline-
delimited JSON on stdio; no resources/, streaming, or tool-change notifications
yet (documented as a deliberate v1 scope).
"""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Callable, cast

from ai_company.audit.events import AuditEvent, AuditEventType
from ai_company.audit.writer import AuditWriter

logger = logging.getLogger(__name__)

PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "pharos-content-intelligence"
SERVER_VERSION = "0.1.0"

# RBAC role rank (mirrors security/rbac.py _RANK).
_RANK = {"run": 0, "approve": 1, "admin": 2}

_DOCS_DIR_ENV = "PHAROS_DOCS_DIR"
_MAIN_TREE_DOCS = "docs/Pharos"


def _static_text(content: str) -> dict[str, Any]:
    return {"type": "text", "text": content}


def _error(code: int, message: str) -> dict[str, Any]:
    return {"code": code, "message": message}


class _McpError(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class PharosMcpServer:
    """Stdio JSON-RPC 2.0 MCP server with RBAC + audit on every tool call."""

    def __init__(
        self,
        *,
        audit_writer: Any | None = None,
        use_audit: bool = True,
        graph_factory: Callable[[], Any] | None = None,
        memory_factory: Callable[[], Any] | None = None,
        docs_dir: str | Path | None = None,
    ) -> None:
        self._audit_writer = audit_writer
        self._use_audit = use_audit
        self._graph_factory = graph_factory
        self._memory_factory = memory_factory
        self._docs_dir = Path(docs_dir) if docs_dir else None
        self._tools: dict[str, Callable[..., Any]] = {
            "knowledge_graph_query": self._tool_knowledge_graph_query,
            "memory_recall": self._tool_memory_recall,
            "research_lookup": self._tool_research_lookup,
            "pharos_reference": self._tool_pharos_reference,
            "publish_queue": self._tool_publish_queue,
        }

    # ── public handler ────────────────────────────────────────────────────

    def handle(self, raw: str) -> str | None:
        """Parse one JSON line and return the response line (or None for notifications).

        The only entry point used by both ``run_stdio`` and tests, so the
        protocol logic stays pure and unit-testable.
        """
        try:
            request = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return self._serialize(
                {"jsonrpc": "2.0", "id": None, "error": _error(-32700, "Parse error")}
            )

        if not isinstance(request, dict):
            return self._serialize(
                {"jsonrpc": "2.0", "id": None, "error": _error(-32600, "Invalid Request")}
            )

        method = request.get("method", "")
        request_id = request.get("id")
        params = request.get("params") or {}

        # Notifications carry no id and produce no response.
        if request_id is None:
            self._handle_notification(method, params)
            return None

        try:
            if method == "initialize":
                result = self._handle_initialize(params)
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": self._tool_schemas()}
            elif method == "tools/call":
                result = self._handle_tools_call(params)
            else:
                raise _McpError(-32601, f"Method not found: {method}")
        except _McpError as exc:
            return self._serialize(
                {"jsonrpc": "2.0", "id": request_id, "error": _error(exc.code, exc.message)}
            )
        except Exception:  # noqa: BLE001 - traps unexpected tool failures
            logger.exception("MCP request %s failed", method)
            return self._serialize(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": _error(-32603, "Internal error"),
                }
            )

        return self._serialize({"jsonrpc": "2.0", "id": request_id, "result": result})

    # ── protocol methods ──────────────────────────────────────────────────

    def _handle_initialize(self, params: dict[str, Any]) -> dict[str, Any]:
        """Echo capabilities and the negotiated protocol version."""
        client_version = params.get("protocolVersion", "")
        version = (
            client_version
            if client_version in {"2024-11-05", "2025-03-26", "2025-06-18"}
            else PROTOCOL_VERSION
        )
        return {
            "protocolVersion": version,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
        }

    def _handle_notification(self, method: str, params: dict[str, Any]) -> None:
        # No response for notifications; record only what matters (nothing for v1).
        return None

    def _handle_tools_call(self, params: dict[str, Any]) -> dict[str, Any]:
        name = params.get("name", "")
        arguments = params.get("arguments") or {}
        tool = self._tools.get(name)
        if tool is None:
            raise _McpError(-32602, f"Unknown tool: {name}")

        role = self._resolve_role(params)
        self._require_role(tool, role, name)
        try:
            result = tool(arguments, role)
        except _McpError:
            raise
        except Exception as exc:  # noqa: BLE001 - convert tool errors to JSON-RPC errors
            logger.exception("Tool %s raised", name)
            raise _McpError(-32603, f"{name} failed: {exc}") from exc

        self._audit(name, arguments, result, role)
        return {"content": [_static_text(json.dumps(result, sort_keys=True))], "isError": False}

    # ── auth ────────────────────────────────────────────────────────────────

    def _resolve_role(self, params: dict[str, Any]) -> str:
        """Resolve X-API-Key to a lowercase role via the existing RBAC."""
        from ai_company.security.rbac import Role, role_for_key

        authorization = params.get("authorization", "") or ""
        if authorization.lower().startswith("bearer "):
            api_key = authorization[7:].strip()
        else:
            api_key = authorization.strip()

        if os.environ.get("DASHBOARD_AUTH_MODE", "api_key") == "open":
            role = Role.ADMIN.value
        else:
            role_obj = role_for_key(api_key)
            if role_obj is None:
                raise _McpError(-32001, "Unauthorized: invalid or missing API key")
            role = role_obj.value
        self._audit("auth", {"role": role}, {}, role)
        return role

    def _require_role(self, tool: Callable[..., Any], role: str, name: str) -> None:
        required = "approve" if name == "publish_queue" else "run"
        if _RANK.get(role, -1) < _RANK[required]:
            raise _McpError(-32001, f"Permission denied: {name} requires role '{required}'")

    # ── tools ───────────────────────────────────────────────────────────────

    def _tool_schemas(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "knowledge_graph_query",
                "description": "Query the company knowledge graph (org chart, decision, workflow, knowledge graphs).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "graph_name": {
                            "type": "string",
                            "enum": [
                                "org_chart",
                                "decision_graph",
                                "workflow_graph",
                                "knowledge_graph",
                            ],
                        },
                        "action": {
                            "type": "string",
                            "enum": ["get", "list", "search"],
                            "default": "get",
                        },
                        "query": {"type": "string"},
                    },
                },
            },
            {
                "name": "memory_recall",
                "description": "Recall memories from the company memory store (episodic, semantic, procedural, relational, temporal, aggregate).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "memory_type": {"type": "string"},
                        "query": {"type": "string"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10},
                    },
                },
            },
            {
                "name": "research_lookup",
                "description": "Keyword search the Pharos regional corpus under docs/Pharos. Returns matching .md documents with snippets.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 20, "default": 5},
                    },
                },
            },
            {
                "name": "pharos_reference",
                "description": "Read a Pharos reference document from docs/Pharos (e.g. 'README', 'positioning', 'stakeholder-map'). Path-safe.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                },
            },
            {
                "name": "publish_queue",
                "description": "Enqueue a platform-ready artifact for LinkedIn or Substack. Requires approve/admin role.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "platform": {"type": "string", "enum": ["linkedin", "substack"]},
                        "title": {"type": "string"},
                        "body": {"type": "string"},
                    },
                },
            },
        ]

    def _tool_knowledge_graph_query(self, args: dict[str, Any], role: str) -> dict[str, Any]:
        graph_name = args.get("graph_name", "knowledge_graph")
        action = args.get("action", "get")
        query = (args.get("query") or "").strip()

        if self._graph_factory is not None:
            engine = self._graph_factory()
        else:
            from ai_company.graph.engine import GraphEngine
            from ai_company.registry import load_registry

            engine = GraphEngine(load_registry())

        if action == "list":
            return {"graphs": engine.list_graphs()}

        if action == "search":
            if not query:
                raise _McpError(-32602, "search requires a 'query' argument")
            hits = []
            for graph_name_candidate in (
                "org_chart",
                "decision_graph",
                "workflow_graph",
                "knowledge_graph",
            ):
                graph = engine.get_graph(graph_name_candidate)
                if graph is None:
                    continue
                for node in graph.to_dict().get("nodes", []):
                    if query.lower() in node.get("label", "").lower():
                        hits.append(
                            {
                                "graph": graph_name_candidate,
                                "node_id": node.get("id"),
                                "label": node.get("label"),
                                "node_type": node.get("node_type"),
                            }
                        )
            return {"results": self._sanitize_payload(hits)}

        graph = engine.get_graph(graph_name)
        if graph is None:
            engine.build_knowledge_graph()
            graph = engine.get_graph(graph_name)
        if graph is None:
            raise _McpError(-32602, f"Unknown graph: {graph_name}")
        return cast(dict[str, Any], self._sanitize_payload(graph.to_dict()))

    def _tool_memory_recall(self, args: dict[str, Any], role: str) -> dict[str, Any]:
        from ai_company.memory.engine import MemoryStore

        memory_type = (args.get("memory_type") or "").strip()
        query = (args.get("query") or "").strip()
        limit = int(args.get("limit") or 10)

        store = self._memory_factory() if self._memory_factory is not None else MemoryStore()

        entries = store.recall(memory_type, query=query, limit=limit)
        payload = [
            {
                "id": e.id,
                "memory_type": e.memory_type,
                "content": self._mask_pii(e.content),
                "tags": e.tags,
                "created_at": e.created_at,
            }
            for e in entries
        ]
        return {"results": payload}

    def _tool_research_lookup(self, args: dict[str, Any], role: str) -> dict[str, Any]:
        query = (args.get("query") or "").strip()
        limit = int(args.get("limit") or 5)
        if not query:
            raise _McpError(-32602, "research_lookup requires a 'query' argument")

        docs_dir = self._resolve_docs_dir()
        results = []
        if docs_dir is not None:
            q = query.lower()
            for path in sorted(docs_dir.rglob("*.md")):
                try:
                    text = path.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                if q in text.lower():
                    snippet = self._snippet(text, q)
                    results.append(
                        {
                            "path": str(path.relative_to(docs_dir)),
                            "snippet": self._mask_pii(snippet),
                        }
                    )
                if len(results) >= limit:
                    break
        return {"results": results, "corpus_dir": str(docs_dir) if docs_dir else "(unavailable)"}

    def _tool_pharos_reference(self, args: dict[str, Any], role: str) -> dict[str, Any]:
        name = (args.get("name") or "").strip()
        docs_dir = self._resolve_docs_dir()
        if docs_dir is None:
            return cast(
                dict[str, Any],
                self._sanitize_payload(
                    {"error": "docs/Pharos corpus not found in this workspace", "found": False}
                ),
            )

        # Path-safe: interpret name as a filename stem under docs_dir only.
        candidate = docs_dir / f"{name}.md"
        if not (candidate.exists() and candidate.is_file()) or not self._is_within(
            docs_dir, candidate
        ):
            return cast(
                dict[str, Any],
                self._sanitize_payload(
                    {"error": f"Unknown Pharos reference: {name}", "found": False}
                ),
            )

        text = candidate.read_text(encoding="utf-8", errors="replace")
        return cast(
            dict[str, Any],
            self._sanitize_payload(
                {
                    "name": name,
                    "path": str(candidate.relative_to(docs_dir)),
                    "found": True,
                    "body": self._mask_pii(text),
                }
            ),
        )

    def _tool_publish_queue(self, args: dict[str, Any], role: str) -> dict[str, Any]:
        from ai_company.publishing.queue import PublishQueue

        platform = (args.get("platform") or "").lower()
        title = (args.get("title") or "").strip()
        body = (args.get("body") or "").strip()

        queue_dir = os.environ.get("PHAROS_PUBLISH_DIR", "results/pharos")
        queue = PublishQueue(queue_dir)
        record = queue.enqueue(platform, title, body)
        return {
            "record_id": record.id,
            "platform": record.platform,
            "status": record.status,
            "queued": True,
        }

    # ── sanitize + PII ──────────────────────────────────────────────────────

    def _mask_pii(self, text: str) -> str:
        from ai_company.security.pii_detector import detect_and_mask_pii

        return detect_and_mask_pii(text).masked

    def _sanitize_payload(self, payload: Any) -> Any:
        """JSON-roundtrip to check content-filterability; mask if a string payload."""
        from ai_company.security.content_filter import filter_content

        if isinstance(payload, str):
            if not filter_content(payload).is_safe:
                return {"error": "Content rejected by the safety filter", "blocked": True}
            return self._mask_pii(payload)
        serialized = json.dumps(payload, sort_keys=True, default=str)
        if not filter_content(serialized).is_safe:
            return {"error": "Content rejected by the safety filter", "blocked": True}
        return payload

    # ── audit ───────────────────────────────────────────────────────────────

    def _audit(self, tool: str, args: dict[str, Any], result: Any, role: str) -> None:
        if not self._use_audit:
            return
        writer = self._audit_writer or AuditWriter()
        event = AuditEvent(
            event_type=AuditEventType.TOOL_CALL,
            agent_id="pharos-mcp",
            tool=tool,
            args=args,
            result={} if result is None else result,
            metadata={"auth_role": role},
        )
        try:
            writer.write(event)
        except Exception:  # noqa: BLE001 - audit failure must not break the tool call
            logger.warning("Failed to write MCP audit event", exc_info=True)

    # ── corpus resolution ──────────────────────────────────────────────────

    def _resolve_docs_dir(self) -> Path | None:
        if self._docs_dir is not None:
            return self._docs_dir if self._docs_dir.is_dir() else None

        env_dir = os.environ.get(_DOCS_DIR_ENV)
        if env_dir:
            env_path = Path(env_dir)
            return env_path if env_path.is_dir() else None

        from ai_company.paths import get_project_root

        root = get_project_root()
        candidates = [root / _MAIN_TREE_DOCS]
        # Worktree fallback: the MAIN tree usually lives one level up.
        parent = root.parent
        for companion in parent.iterdir():
            if companion.name != root.name and (companion / _MAIN_TREE_DOCS).is_dir():
                candidates.append(companion / _MAIN_TREE_DOCS)
        for candidate in candidates:
            if candidate.is_dir():
                return candidate
        return None

    @staticmethod
    def _is_within(base: Path, path: Path) -> bool:
        try:
            path.resolve().relative_to(base.resolve())
            return True
        except ValueError:
            return False

    @staticmethod
    def _snippet(text: str, query: str, radius: int = 300) -> str:
        """Return a snippet around the first query hit."""
        idx = text.lower().find(query)
        start = 0 if idx < 0 else max(0, idx - radius)
        end = min(len(text), start + radius * 2)
        snippet = text[start:end].replace("\n", " ").strip()
        return snippet

    # ── serialization ──────────────────────────────────────────────────────

    @staticmethod
    def _serialize(response: dict[str, Any]) -> str:
        return json.dumps(response, ensure_ascii=False)

    def run_stdio(self) -> int:
        """Serve newline-delimited JSON-RPC from stdin to stdout until EOF.

        Returns 0 on clean EOF. Deliberately minimal — talks the MCP stdio
        transport with zero external dependencies.
        """
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            response = self.handle(line)
            if response is not None:
                sys.stdout.write(response + "\n")
                sys.stdout.flush()
        return 0


__all__ = ["PROTOCOL_VERSION", "PharosMcpServer", "SERVER_NAME", "SERVER_VERSION"]
