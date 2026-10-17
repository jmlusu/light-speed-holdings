# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first (continues approved ADR-020 phases P1/P2 on closed P0)
- Questions asked this round: 4 (MCP transport, Whisper packaging, publishing rails scope, deep-research scope) — all resolved with user, recorded in Resolved Clarifications.

## Goal And Evidence

- Real problem or user request: Roll out the next slice of ADR-020 "Pharos Content Intelligence" (P1 core loop + P2 scale) that P0 deferred: (1) deep-research routines, (2) publishing rails for LinkedIn/Substack, (3) Whisper transcription (local-first), (4) the Pharos Content Intelligence MCP server at `src/ai_company/mcp/server.py`. User directive: "Proceed with P1/P2 slice (deep-research routines, publishing rails, Whisper, Pharos MCP)".
- Current behavior: P0 delivered the routine engine (`orchestrator/routine.py`) with 3 daily Pharos routines fired by the daemon, `routine_run_id` idempotency, and `pharos_content` KPIs. There is no research-depth concept, no publish queue/rails, no transcription, and no MCP surface. P1 items NOT in this slice (per user's explicit scoping): CEO voice profile, Boost reverse-engineer fan-out, regional Malawi/SADC corpus collectors, board/tracker workspace, Lighthouse pilot packaging.
- Source of evidence: `docs/adr/020-pharos-content-intelligence.md` (P1/P2 lists + MCP design in section 3), archive `2026-09-14-pharos-content-intelligence-p0-routine-engine-and-content-kpis` (Deferred section), user's slice directive.

## User Scenarios And Success

- Primary user/system scenario:
  - The daemon fires a **deep-research routine** whose task prompt instructs a content agent to gather corroborating source material (knowledge graph, memory recall, docs/Pharos references) before drafting — visible in the inbox with provenance tags like a normal routine fire.
  - A finished piece is **formatted for LinkedIn or Substack** and enqueued to a PublishQueue as a bus task; a humane/agent can list/publish it; live POST only fires when API env creds are configured (default: dry-run receipt).
  - A CEO voice note / interview **audio file is transcribed locally** (faster-whisper when installed), returning text; when the optional dep is absent the transcriber degrades gracefully instead of crashing.
  - An MCP-capable client connects to `ai-company mcp` over stdio, completes initialize, lists tools, and calls read-only `knowledge_graph_query` / `memory_recall` / `research_lookup` / `pharos_reference` (X-API-Key `run` role); `publish_queue` requires `approve`; every call audit-logged.
- Success criteria: All four subsystems exist, are unit-tested, and pass ruff/mypy/full non-e2e pytest; deep routines fire through existing `RoutineEngine`; publish enqueue produces a bus task + a queue record; transcriber returns a graceful result with and without faster-whisper; MCP server passes initialize + tools/list + tools/call round-trips with RBAC gating and audit events.
- Acceptance criteria:
  - `Routine` gains a research-depth field; 2 new deep-research routines + prompt templates under `templates/pharos/routines/`.
  - `ai_company/publishing/` exposes PublishQueue (FileStore-backed) + LinkedIn/Substack formatters + publisher adapters with live-POST opt-in via env, default dry-run.
  - `ai_company/media/transcription.py` transcriber with optional faster-whisper import, graceful fallback; `[project.optional-dependencies] pharos-whisper` extra.
  - `ai_company/mcp/__init__.py` + `server.py`: minimal stdio JSON-RPC 2.0 (initialize, tools/list, tools/call), RBAC per ADR (run=read, approve=write publish queue), content-filter + PII pass, AuditWriter on every call.
  - New unit tests for each area pass; full suite stays green; ECL closed `completed`.

## Non-Goals

- CEO voice profile / voice-preserving drafting (P1, deferred).
- Boost reverse-engineer batch fan-out over the message bus (P1, deferred).
- Regional Malawi/SADC corpus collectors feeding the Monitor (P2, deferred).
- Board/tracker workspace, Lighthouse pilot packaging (P2, deferred).
- Eden MCP consumption (stays behind feature flag, unfunded this slice).
- Any new top-level CLI; MCP/publish/transcribe surface rides subcommands only (`ai-company mcp ...` etc.).
- No schema change to `CompanyRegistry`.

## Constraints

- Canonical tool list and registry contract unchanged (AGENTS.md §8).
- No new top-level CLI entry (`ai-company` root stays single app; ADR-020 consequence "no new top-level CLI").
- Do not ship secrets; live-POST creds come only from env at runtime.
- Optional deps (faster-whisper) must not be required for import; guards degrade gracefully.
- MCP write path must require `approve`/`admin` RBAC role and pass through PII/content guards and audit.
- `pyproject.toml` changeset must keep `uv.lock` in sync (ECL §4).

## Assumptions

- MCP protocol subset (initialize, tools/list, tools/call over newline-delimited JSON over stdio) is sufficient for this slice; no streaming/pagination resources.
- `docs/Pharos/*` reference corpus exists in the MAIN tree (`C:\Users\jmlus\light-speed-holdings\docs\Pharos\`); the worktree does not carry it. MCP `pharos_reference` must resolve the corpus path at runtime (main tree copy when worktree lacks it) and handle absence gracefully.
- Faster-whisper is never installed in the default env; tests mock/skip its import path.
- Registry remains loadable via `ai_company.registry.load_registry()` for GraphEngine wiring; `orchestrator/approval.py` ApprovalGate is available for the publish write gate if needed.

## Open Questions

- (resolved — see below)

## Resolved Clarifications

- MCP transport: **minimal in-house stdio JSON-RPC server** (no third-party MCP SDK; walk stdio `initialize`/`tools/list`/`tools/call` ourselves with stdlib `json` + `sys.stdin`/`stdout`).
- Whisper packaging: **optional `pharos-whisper` extra + graceful fallback** (transcriber returns an `unavailable` result when faster-whisper is not importable; core tests mock it; audio never leaves the machine).
- Publishing rails scope: **queue + formatters, live POST opt-in** (PublishQueue on the message bus with platform-ready artifacts as tasks; LinkedIn/Substack formatters; live POST adapter fires only when endpoint+creds configured via env otherwise dry-run receipt).
- Deep-research scope: **extend the routine engine + 2 new routines** (add research-depth field to `Routine`; new routines + prompt templates reusing graph/memory/reference).
