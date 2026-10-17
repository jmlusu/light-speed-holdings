---
title: "Pharos Content Intelligence P1/P2 - Deep-Research, Publishing Rails, Whisper, MCP"
slug: "pharos-content-intelligence-p1-p2-deep-research-publishing-rails-whisper-mcp"
status: "completed"
location: "archive"
phase: "implement"
intake_status: "done"
spec_review: "approved"
plan_review: "approved"
modules:
  - "src/ai_company/orchestrator/routine.py"
  - "src/ai_company/publishing/queue.py"
  - "src/ai_company/publishing/formats.py"
  - "src/ai_company/publishing/publishers.py"
  - "src/ai_company/media/transcription.py"
  - "src/ai_company/mcp/server.py"
files:
  - "config/company/routines.yaml"
  - "templates/pharos/routines/deep-research-brief.md"
  - "templates/pharos/routines/sadc-research-scan.md"
  - "src/ai_company/cli/publishing.py"
  - "src/ai_company/cli/media.py"
  - "src/ai_company/cli/mcp.py"
  - "src/ai_company/cli/main.py"
  - "pyproject.toml"
  - "uv.lock"
  - "docs/STATUS.md"
  - "tests/unit/test_publishing.py"
  - "tests/unit/test_transcription.py"
  - "tests/unit/test_mcp_server.py"
  - "tests/unit/test_routine.py"
tags:
  - "pharos"
  - "content-intelligence"
  - "deep-research"
  - "publishing"
  - "whisper"
  - "mcp"
validation_status: "pass"
created_at: "2026-09-14"
updated_at: "2026-09-14"
---

# Summary

## Outcome

P1/P2 slice of ADR-020 "Pharos Content Intelligence" (user-scoped subset):
deep-research routines, publishing rails (LinkedIn/Substack), local-first
Whisper transcription, and the Pharos Content Intelligence MCP server —
built as additive subsystems on the P0 routine engine. CEO voice profile,
Boost fan-out, and regional corpus collectors remain deferred per user scoping.

## Decisions

- MCP transport: minimal in-house stdio JSON-RPC 2.0 server (no third-party SDK);
  import-safe, pure handler unit-tested over JSON frames. Documented subset:
  initialize / tools/list / tools/call / ping; no resources/ or streaming yet.
- Whisper: optional `pharos-whisper` extra + lazy faster-whisper import with
  graceful `unavailable` result; audio stays local; core tests never require it.
- Publishing rails: PublishQueue (FileStore-backed, optional message-bus mirror)
  + LinkedIn/Substack formatters + publisher adapters with env-gated live POST
  (default dry-run receipt). No credentials committed.
- Deep-research routines: additive `Routine.research_depth` field + 2 new
  routines/prompts; no scheduler or daemon changes required.
- `docs/Pharos` corpus lives in the MAIN tree; MCP resolves it at runtime with
  main-tree fallback + `PHAROS_DOCS_DIR` override, graceful empty result.
- Security: MCP read tools require `run` RBAC role; `publish_queue` requires
  `approve`/`admin`; outputs pass content-filter + PII masking; every call
  audit-logged (`AuditWriter` / `tool_call`).

## Validation

All gates green. Full non-e2e suite: **2162 passed, 0 failed, 67 deselected**
(prior baseline 2117 + 45 new; ~488s). New unit tests: `test_mcp_server.py`
(20), `test_publishing.py` (11), `test_transcription.py` (5), `test_routine.py`
(+7 deep-research). `uv run ruff check src/` clean, `uv run mypy src/` clean
(209 source files). CLI smoke: `ai-company --help` shows `publishing`, `media`,
`mcp`; `publishing --help` (`enqueue/list/show/publish`, dry-run default),
`media --help` (`transcribe`), `mcp --help` (`stdio`, `tools`).
`uv lock` refreshed: `provides-extras` includes `pharos-whisper`, lock pins
faster-whisper v1.2.1 (not installed in default env).

## Next Step

- Update `docs/STATUS.md`, run `pwsh scripts/lint-ecl.ps1` + `harness-change.ps1 validate`, then close `completed`.
