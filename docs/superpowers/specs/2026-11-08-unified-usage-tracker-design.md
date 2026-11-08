# Spec: Unified Usage Tracker (CLI + OpenCode Desktop)

## Objective
Track every real LLM call regardless of entry point — `ai_company` CLI/AgentLoop today, plus OpenCode Desktop sessions that currently bypass `CostTracker` entirely (verified: `data/orchestrator/cost_tracker.json` and `results/cost_log.jsonl` missing after a desktop session). One truthful, deduped cost store for reporting; no dummy/fabricated rows. User is on CLI + Desktop; success = `ai-company llm sync-opencode` imports real Desktop usage once, reruns add 0 rows, and `ai-company llm usage --source opencode-desktop` matches the dashboard `by_source` totals.

## Ground Truth (verified read-only by 3 subagents)
- `CostTracker` (`src/ai_company/llm/cost_tracker.py:92`): `UsageRecord(timestamp, model, provider, agent_name, task_id, prompt_tokens, completion_tokens, cost_usd, tokens_saved, iteration, files_read, metadata)`. Instantiated only in `executor/loop.py:171` and `cli/llm.py:49`. Records via `AgentLoop.run()` (`agent_loop.py:438`, requires `task_id`) and `LLMClient._record_usage()` (`client.py:578`, early-returns if no `task_id`). Desktop chat never enters this chain — architectural bypass.
- Desktop store `C:\Users\jmlus\.local\share\opencode\opencode.db` (3.0 GiB + 2.95 GiB WAL, 26 tables): `session` (3131 rows) / `session_v2` (75), `message` (153k, per-turn `data.tokens{input,output,reasoning,cache{read,write}}`, `cost`, `providerID/modelID`), `part` (670k, `step-finish` tokens, `tool=read/edit/bash`, `files[]`). Cost is ~0 for free/router models. `log/opencode.log` (57 MiB) has no request bodies — not a token source.
- Config: `C:\Users\jmlus\.config\opencode\opencode.json` (337 KB, omniroute only, 1260 models with `limit`, no numeric `temperature`); project `opencode.json` sets `maxContextTokens=64000`, `autoReadFiles=false`.

## Architecture (Option A — pull reader, approved)
`opencode.db (ro) → reader → normalizer → CostTracker/CostAnalytics (existing stores, source-tagged) → cost_tracker.json (gains by_source)`. Zero changes to OpenCode runtime/config. CLI records unchanged. Field map: `prompt=input+cache_write`, `completion=output+reasoning`, `cache_*` in metadata, `files_read`=count `part.tool==read`, `agent_name`=message/session agent, `task_id=session.id`, `source=opencode-desktop`, `session_id=ses_…`, `event_id=msg_<id>`; `tokens_saved=0` (no compressor baseline — do not fabricate). Cost: if provider `cost>0` use it (`cost_source=provider`), else recompute via `MODEL_COSTS` (add `crouton-alpha-free`, `nemotron-3.5-lightning-free`, `big-pickle` at 0.0); unknown → `_default` + `cost_source=recomputed-default`.

## Components
1. `src/ai_company/llm/opencode_usage.py` (NEW): read-only `sqlite3` (`file:?mode=ro`) reader + normalizer; union `session`/`session_v2`, join `message`/`session_message` + `part/step-finish`, project-scoped by `directory`.
2. `src/ai_company/llm/cost_tracker.py` (EXTEND): `UsageRecord` gains `source`, `session_id`, `event_id`, `cache_read`, `cache_write`, `cost_source` (backward-compat defaults); `MODEL_COSTS` gains 3 free entries.
3. `src/ai_company/data/cost_analytics.py` (EXTEND): `record_usage()` additive kwargs, `event_id` insert-or-ignore dedup; `get_usage_summary(source=...)` + `by_source`.
4. `src/ai_company/data/database.py` (EXTEND): additive migration `ALTER cost_records ADD COLUMN source/session_id/event_id/cache_read/cache_write/cost_source` + unique index on `event_id`, indexes on `source`/`session_id`.
5. `src/ai_company/cli/llm.py` (EXTEND): `sync-opencode [--since] [--project] [--all] [--dry-run] [--limit]` + `usage --source`.
6. `tests/unit/test_opencode_usage.py` (NEW): normalizer + dedup + cost-recompute vs in-memory SQLite + canned JSON (no real-DB writes in CI).

## Boundaries
- Always: read-only DB access; idempotent sync; real sessions only; `ruff`+`mypy`+`pytest` green; test fixtures stay in tests.
- Ask first: any change to root `opencode.json` / plugin hooks (Option B/C) — out of scope.
- Never: write to `opencode.db`/log; dump secrets from `service.json`/`auth.json`; fabricate tokens/cost; delete `dead_letter.jsonl` or `approvals.yaml`; send local data to third parties.

## Success Criteria
- `sync-opencode --project <repo> --dry-run` totals equal `SUM()` over `session_v2` for those sessions.
- Second sync reports `0 new rows`.
- `ai-company llm usage --source opencode-desktop` equals dashboard `by_source` totals.
- 6-check CI green (ruff, mypy, pytest, Archify, etc.).

## Open Questions
None blocking — CLI vs Desktop are separate namespaces (disjoint `ses_…` vs `task_id`), so no cross-source double-count.
