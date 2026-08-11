# Audit Fixes — 2026-08-10

**Scope:** Tool-vocabulary canonicalization, template boilerplate deduplication, registry path independence, and associated test repairs across the AI Company Builder.

**Status:** Complete and verified (1801 tests passing, ruff + mypy clean).

---

## Fix 1–3 — Registry path independence & CLI cleanup

Anchored registry loading to the package-located project root so the CLI no longer depends on the process CWD:

- `registry/loader.py` — `load_registry()` resolves the project root deterministically (`AI_COMPANY_ROOT` env override with package-root fallback); no longer CWD-relative.
- `registry/__init__.py`, `registry/sync.py` — aligned resolver/sync entry points with the anchored loader.
- `cli/main.py` — lazy sub-app registration (`_LAZY_SUB_APPS`) so `ai-company --help` and hot paths never import every subcommand module.
- `cli/executor.py` — `dlq_retry` delegates re-enqueue logic to `DeadLetterQueue.retry_dlq_task` instead of duplicating it inline.

## Fix 4 — Canonicalize tool vocabulary

Generated agent cards previously used a mix of tool names (`websearch`, `web_search`, `code_interpreter`, `webfetch`). Reduced to one canonical set per OpenCode v2 permission keys:

| Permission key | Agents | Notes |
|----------------|--------|-------|
| `read` | 127 | |
| `edit` | 120 | `write`/`edit` aliases → `edit` |
| `grep` / `list` | 102 | |
| `bash` | 77 | `execute`/`code_interpreter` → `bash` |
| `webfetch` | 17 | `websearch`/`web_search` → `webfetch` |
| `task` | 1 | `delegate` |

Changes:

- `generator.py` — `_TOOL_MAP` maps legacy aliases to the canonical permission keys (`websearch`/`web_search` → `webfetch`; `code_interpreter` → `bash`; `write` → `edit`; `delegate` → `task`).
- Regenerated `company/agent-registry.json` and all 127 `.opencode/agents/*.md`.
- Verified zero residual `websearch`/`code_interpreter` in the registry and zero `websearch: allow` blocks in agent cards.

**Known gap (pre-existing, out of scope):** the executor's runtime tool set (`executor/tool_runner.py`) still includes `code_interpreter` and has no `web_search` implementation. Cards now advertise `webfetch`, which is the correct OpenCode permission, but the runtime runner has no matching tool. Untouched by this session; flagged for a follow-up.

## Fix 5 — Deduplicate template boilerplate into shared standards doc

Operating Principles were byte-identical across all 127 agents (rendered inline from every template). Moved to a single source of truth:

- New `templates/agents/operating-standards.md` (5 principles: Evidence over opinion / Customer first / Security by design / Automate repetitive work / Escalate uncertainty).
- All 5 templates (`base.md.j2`, `executive.md.j2`, `specialist.md.j2`, `board.md.j2`, `agents/agent.md.j2`) replaced inline principles with a `## Shared Standards` reference to `../operating-standards.md`.
- `generator.py` — `_write_shared_standards()` writes the shared doc to `.opencode/operating-standards.md`; `_validate_generated_agents()` passes the path into spec validation.
- `executor/context.py` — `SHARED_STANDARDS_FILENAME` constant + `_load_shared_standards()` fallback so `parse_agent_spec()` / `parse_agent_spec_content()` resolve operating principles from the shared doc when a card carries no inline copy (backward compatible with legacy cards).
- Verified: 0 inline Operating Principles blocks, 127 shared references, `parse_agent_spec('cto')` returns all 5 principles via the fallback.

**Design note:** Only Operating Principles were deduplicated. Success Metrics and Escalation differ by agent type (executive/specialist/board/default), so collapsing them into one shared doc would have lost type-specific content — a deliberate deviation from the literal audit wording to respect the no-capability-loss constraint.

## Verification

| Gate | Result |
|------|--------|
| `AgentGenerator().generate_all()` | 127 agents generated, 0 validation errors |
| `agents validate` (CLI) | 127 OK / 1 pre-existing warning (`board-chair` missing `reports_to`) |
| `pytest` (full suite) | **1801 passed, 0 failed** (53 e2e deselected) |
| `ruff check` (changed files) | clean |
| `mypy` (changed files) | no issues |

## Test repair

`tests/unit/test_cli_commands.py::test_agents_list_missing_registry_fails_gracefully` — added `AI_COMPANY_ROOT` env override (fix 3 made registry loading CWD-independent, so the old CWD-relative assumption no longer held). Now passes.

## Files changed

- `src/ai_company/generator.py`, `src/ai_company/executor/context.py`
- `src/ai_company/registry/{__init__,loader,sync}.py`
- `src/ai_company/cli/main.py`, `src/ai_company/cli/executor.py`
- `templates/{base,executive,specialist,board}.md.j2`, `templates/agents/agent.md.j2`
- `templates/agents/operating-standards.md` (new), `.opencode/operating-standards.md` (new, generated)
- `company-registry.yaml`, `company/agent-registry.json`, `.opencode/agents/*.md` (generated)
- `tests/unit/test_cli_commands.py`
