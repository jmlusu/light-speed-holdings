"""Pharos Content Intelligence MCP — minimal in-house stdio JSON-RPC server.

See ``mcp/server.py`` for the protocol implementation and tool surface
(ADR-020 section 3): ``knowledge_graph_query``, ``memory_recall``,
``research_lookup``, ``pharos_reference``, and gated ``publish_queue``.
"""

from ai_company.mcp.server import PROTOCOL_VERSION, SERVER_NAME, SERVER_VERSION, PharosMcpServer

__all__ = ["PROTOCOL_VERSION", "PharosMcpServer", "SERVER_NAME", "SERVER_VERSION"]
