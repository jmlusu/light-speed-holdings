# Plan

## Technical Approach

Implement four additive subsystems on the closed P0 foundation, each self-contained
and unit-tested:

1. **Deep-research routines (extend `RoutineEngine`).** Add a `research_depth`
   field (`standard` | `deep`) to `Routine` (default `standard`, backward
   compatible). Add 2 new routines to `config/company/routines.yaml`
   (`pharos_deep_research_brief` Sat `schedule_day: 6` — day chosen to avoid a
   double-fire with the existing Monday brief — + `pharos_sadc_research_scan`
   Thu `schedule_day: 4`) and 2 prompt templates under
   `templates/pharos/routines/`. Rendered task
   instruction + tags carry the depth so content agents can pick corroboration
   steps. No scheduler/daemon change needed (reuses interval/day gating).

2. **Publishing rails.** New `src/ai_company/publishing/` package:
   - `queue.py`: `PublishQueue` — FileStore-backed JSON store at
     `results/pharos/publish_queue.json`; `enqueue(platform, title, body, ...)`
     appends a record and (optionally) mirrors to the message bus as a task
     tagged `pharos-publish`/`publish:<platform>`; `list()`, `mark_posted()`,
     `mark_failed()`.
   - `formats.py`: `format_linkedin(body)` (plaintext, ~3000-char guard w/
     truncation warning) and `format_substack(body)` (markdown passthrough w/
     length reporting) returning a dict of platform-ready text + diagnostics.
   - `publishers.py`: `LinkedInPublisher` / `SubstackPublisher` with `publish()`
     that reads env (`PHAROS_LINKEDIN_*`, `PHAROS_SUBSTACK_*`) for base URL +
     token; when creds absent returns a **dry-run receipt**; when creds present
     performs an `httpx` POST. No secrets committed.
- CLI surface under the existing `dashboard`/marketing-style lazy subapps:
      `ai-company publishing enqueue|list|show|publish` (new `cli/publishing.py`
      registered in `_LAZY_SUB_APPS`; `publish -L/--live` opts into a real POST,
      dry-run default).

3. **Whisper (local-first, optional).** New `src/ai_company/media/transcription.py`:
   `Transcriber` class whose `transcribe(path)` lazily imports
   `faster_whisper.WhisperModel`; on `ImportError` it returns a structured
   `unavailable` result (not a crash). Add `pharos-whisper = ["faster-whisper>=1.0"]`
   to `[project.optional-dependencies]` and refresh `uv.lock`. `ai-company media
   transcribe <audio>` subcommand.

4. **Pharos MCP server.** New `src/ai_company/mcp/__init__.py` + `server.py`:
   - Minimal stdio JSON-RPC 2.0 server (stdlib only): reads newline-delimited
     JSON from stdin, handles `initialize`, `tools/list`, `tools/call`, `ping`,
     writes responses to stdout. Request id correlation + JSON-RPC error frames.
   - Tools: `knowledge_graph_query` (GraphEngine from `load_registry()`, LazyBuilder),
     `memory_recall` (MemoryStore semantic/string recall), `research_lookup`
     (keyword scan over `docs/Pharos/*` corpus resolved at runtime incl. main-tree
     fallback), `pharos_reference` (read `docs/Pharos/*.md` docs by name/path),
     `publish_queue` (write tool → `PublishQueue.enqueue`).
   - Security: X-API-Key via `authorization` param → `rbac.role_for_key`; read
     tools require `run` (or higher); `publish_queue` requires `approve`/`admin`.
     Outputs pass `security/content_filter.filter_content` + PII masking
     (`detect_and_mask_pii`). Every call written via `AuditWriter`
     (`AuditEventType.TOOL_CALL`).
   - Entrypoint: `ai-company mcp --stdio` (new lazy `cli/mcp.py`).

## Impacted Modules And Files

- `src/ai_company/orchestrator/routine.py` (Routine model: `research_depth`).
- `config/company/routines.yaml` (+2 routines).
- `templates/pharos/routines/` (+2 prompts).
- `src/ai_company/publishing/__init__.py`, `queue.py`, `formats.py`, `publishers.py` (new).
- `src/ai_company/media/__init__.py`, `media/transcription.py` (new).
- `src/ai_company/mcp/__init__.py`, `mcp/server.py` (new).
- `src/ai_company/cli/publishing.py`, `cli/media.py`, `cli/mcp.py` (new lazy subapps).
- `src/ai_company/cli/main.py` (`_LAZY_SUB_APPS` +2/3 entries).
- `pyproject.toml` (add `pharos-whisper` extra) + `uv.lock` (sync).
- `docs/STATUS.md` (close entry).
- Tests: new `tests/unit/test_publishing.py`, `tests/unit/test_transcription.py`,
  `tests/unit/test_mcp_server.py`, extend `tests/unit/test_routine.py`.

## Interfaces, Data, Permissions

- `Routine.research_depth: str = "standard"` — additive; existing YAML valid.
- `PublishQueue` records: `{id, platform, title, body, status, created_at,
  external_url, notes}` persisted at `results/pharos/publish_queue.json`.
- MCP request envelope: `{"jsonrpc":"2.0","id":N,"method":"initialize"|"tools/list"
  |"tools/call","params":{...,"authorization":"Bearer <key>"}}`; responses follow
  JSON-RPC 2.0 result/error.
- Permissions: MCP read tools `run`+; `publish_queue` `approve`/`admin` (existing
  RBAC `role_for_key`). Publishing adapter relies on env-only creds.
- No changes to `CompanyRegistry` schema; no new top-level CLI.

## Spec Gaps Found From Planning

- MCP protocol subset (no `resources/`, no streaming, no `tools/list` changed
  notifications) is adequate for v1; document that.
- `docs/Pharos` corpus lives in the main tree, not this worktree — `pharos_reference`
  must fall back to main-tree path and return graceful empty results otherwise.
- Publish "enqueue mirrors a bus task" — keep bus mirroring optional (flag) so
  tests and CLI can use the queue without a running executor.

## Risks And Mitigations

- **faster-whisper missing → import churn.** Mitigate: lazy import in a
  function + `is_available()`; tests patch/never require it; graceful
  `unavailable` result.
- **MCP protocol drift vs official SDK.** Mitigate: implement the documented
  subset precisely; keep `_handle` pure + unit-tested over JSON frames.
- **Publishing live POST could fire without creds.** Mitigate: creds strictly
  env-gated with dry-run default; tests assert dry-run receipt path.
- **`uv.lock` staleness (ECL §4).** Mitigate: run `uv sync --extra pharos-whisper`
  (or `uv lock`) so lockfile reflects the new extra before closing.
- **Main-tree `docs/Pharos` drift.** Mitigate: runtime path resolution with
  explicit `PHAROS_DOCS_DIR` override env; graceful fallback documented.

## Verification Plan

- `uv run ruff check src/`
- `uv run mypy src/`
- `uv run pytest -q -m "not e2e" --basetemp=".pytest_tmp_p1"` (full suite)
- Focused: `tests/unit/test_publishing.py`, `tests/unit/test_transcription.py`,
  `tests/unit/test_mcp_server.py`, `tests/unit/test_routine.py`
- `pwsh scripts/lint-ecl.ps1` + `.\scripts\harness-change.ps1 validate`
- Record all gate outcomes in `summary.md`; close `completed`.
