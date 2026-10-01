# Plan

## Technical Approach

Implement the LinkedIn AI-Native Series "AI-Native Organizations" (11 posts) as additive subsystems on the closed P0 foundation, each self-contained and unit-tested:

### 1. **Reminder Routine** (Pharos routine integration)
- Add `linkedin_series_reminder` to `config/company/scheduler.yaml`:
  - cron: `0 7 */2 * *` (every 2 days at 7:00 AM CAT, Africa/Blantyre)
  - timezone: `Africa/Blantyre`
  - tags: `["pharos-routine", "linkedin-series", "reminder"]`
  - prompt_file: `templates/pharos/routines/linkedin-series-reminder.md`
  - budget_tokens: 2000
  - model_tier: standard
- Adds 2 new routines to `config/company/routines.yaml`:
  - `pharos_deep_research_brief` (Sat schedule_day: 6, avoids double-fire with existing Monday brief)
  - `pharos_sadc_research_scan` (Thu schedule_day: 4)
- Adds 2 prompt templates under `templates/pharos/routines/`:
  - `deep-research-brief.md`
  - `sadc-research-scan.md`

### 2. **Publishing Rails** (LinkedIn/Substack formatters + queue)
- New `src/ai_company/publishing/` package (extends P1 build already in place):
  - `queue.py`: `PublishQueue` — FileStore-backed JSON store at `results/pharos/publish_queue.json`; `enqueue(platform, title, body, ...)` appends a record and (optionally) mirrors to the message bus as a task tagged `pharos-publish`/`publish:<platform>`; `list()`, `mark_posted()`, `mark_failed()`.
  - `formats.py`: `format_linkedin(title, body)` (plaintext, ~3000-char guard with truncation warning) and `format_substack(title, body)` (markdown passthrough with length reporting) returning a dict of platform-ready text + diagnostics.
  - `publishers.py`: `LinkedInPublisher` / `SubstackPublisher` with `publish()` that reads env (`PHAROS_LINKEDIN_*`, `PHAROS_SUBSTACK_*`) for base URL + token; when creds absent returns a **dry-run receipt**; when creds present performs an `httpx` POST. No secrets committed.
- CLI surface under existing lazy subapps:
  - `ai-company publishing enqueue|list|show|publish` (new `cli/publishing.py` registered in `_LAZY_SUB_APPS`; `publish -L/--live` opts into a real POST, dry-run default).

### 3. **Research Evidence Matrices** (Posts 1–3)
- `agentic_research_lead` produces evidence matrices for Posts 1–3 via `k-dense-research-lookup` + webfetch.
- Output: claim-to-source map + verification status, stored in `docs/Pharos/linkedin-series/research-evidence.md` per post.

### 4. **Drafts v1** (Posts 1–3, CEO review)
- `thought_leadership_author` writes Drafts v1 for Posts 1–3 in CEO "builder-writer-advocate" voice (1,200–1,800 words each, no emojis, evidence-led, claims traceable to registry/results/Pharos artifacts).
- Output: `pharos/linkedin-series/post-01/draft-v1.md`, `post-02/draft-v1.md`, `post-03/draft-v1.md` per review artifact package structure.
- Each draft includes: research-evidence.md, x-thread.md, carousel-copy.md, substack-section.md, video-script.md, visuals/ directory, qa-report.md.

### 5. **Visual Assets** (Posts 1–3)
- `ls-visual-storytelling` + `k-dense-infographics` produce per post:
  - Hero visual (1200×627) — framework diagram or org chart
  - 3 carousel cards (1200×627 each) — per the visual requirements table in the series plan
- Brand enforcement: palette 80% navy / 10% red / 10% cyan; type: Arial scale (36/32/28/24/18/16/14/13/12pt); logo on navy; clear space 1× "L" height; `™` on first company mention; no emojis in visuals.
- QA via `ls-artifact-gate` → `ls-artifact-qa` (mandatory gate: visual/brand/UX/content/accessibility).

### 6. **CEO Review Batch 1** (Posts 1–3)
- Human CEO reviews drafts v1 for Posts 1–3 via GitHub PR (pharos/linkedin-series/post-N/).
- SLA: 48h per G2 gate. Reviews requested async via shared doc/PR.
- CEO review checklist per post: voice match, claim traceability, framework layer (H-A-O-M-T-G-V) named, Malawi/SADC context, CTA alignment, visuals on-brand, hashtag set correct (3–5, no spam), cross-post assets consistent.

### 7. **Launch** (Post 1)
- Post 1 publishes Monday 2026-10-05 07:00 CAT via Pharaoh publish queue.
- Subsequent posts follow 2-day cadence (Wed/Fri/Mon).

## Impacted Modules And Files

- `config/company/scheduler.yaml` (+new routine `linkedin_series_reminder`)
- `config/company/routines.yaml` (+2 routines: `pharos_deep_research_brief`, `pharos_sadc_research_scan`)
- `templates/pharos/routines/` (+2 prompts: `deep-research-brief.md`, `sadc-research-scan.md`)
- `templates/pharos/routines/linkedin-series-reminder.md` (new reminder prompt)
- `src/ai_company/publishing/__init__.py`, `queue.py`, `formats.py`, `publishers.py` (extends P1 build)
- `src/ai_company/cli/publishing.py` (new lazy subapp)
- `src/ai_company/cli/main.py` (_LAZY_SUB_APPS +1 entry)
- `pyproject.toml` (if new deps added) + `uv.lock` (sync)
- `docs/STATUS.md` (close entry at archive)
- `docs/Pharos/linkedin-series/` (research evidence, drafts, visuals, QA reports per post)
- Tests: extend `tests/unit/test_routine.py`, new `tests/unit/test_publishing.py`, new `tests/unit/test_transcription.py`, new `tests/unit/test_mcp_server.py`

## Interfaces, Data, Permissions

- `Routine.research_depth: str = "standard"` — additive; existing YAML valid.
- `PublishQueue` records: `{id, platform, title, body, status, created_at, external_url, notes}` persisted at `results/pharos/publish_queue.json`.
- MCP request envelope: `{"jsonrpc":"2.0","id":N,"method":"initialize"|"tools/list"|"tools/call","params":{...,"authorization":"Bearer <key>"}}`; responses follow JSON-RPC 2.0 result/error.
- Permissions: MCP read tools `run`+; `publish_queue` `approve`/`admin` (existing RBAC `role_for_key`). Publishing adapter relies on env-only creds.
- No changes to `CompanyRegistry` schema; no new top-level CLI.
- `config/company/scheduler.yaml` cron runs in `Africa/Blantyre` timezone.

## Spec Gaps Found From Planning

- MCP protocol subset (no `resources/`, no streaming, no `tools/list` changed notifications) is adequate for v1; document that.
- `docs/Pharos` corpus lives in the main tree, not this worktree — `pharos_reference` must fall back to main-tree path and return graceful empty results otherwise.
- Publish "enqueue mirrors a bus task" — keep bus mirroring optional (flag) so tests and CLI can use the queue without a running executor.
- `uv.lock` staleness (ECL §4). Mitigate: run `uv sync --extra pharos-whisper` (or `uv lock`) so lockfile reflects the new extra before closing.
- Main-tree `docs/Pharos` drift. Mitigate: runtime path resolution with explicit `PHAROS_DOCS_DIR` override env; graceful fallback documented.

## Risks And Mitigations

- **faster-whisper missing → import churn.** Mitigate: lazy import in a function + `is_available()`; tests patch/never require it; graceful `unavailable` result.
- **MCP protocol drift vs official SDK.** Mitigate: implement the documented subset precisely; keep `_handle` pure + unit-tested over JSON frames.
- **Publishing live POST could fire without creds.** Mitigate: creds strictly env-gated with dry-run default; tests assert dry-run receipt path.
- **`uv.lock` staleness (ECL §4).** Mitigate: run `uv sync --extra pharos-whisper` (or `uv lock`) so lockfile reflects the new extra before closing.
- **Main-tree `docs/Pharos` drift.** Mitigate: runtime path resolution with explicit `PHAROS_DOCS_DIR` override env; graceful fallback documented.
- **CEO review bottleneck** (48h SLA). Mitigate: batch draft reviews (Posts 1–3 together, efficiency); if SLA exceeded, escalate via `chief_of_staff` per ladder (48–72h → series pause retrospective).

## Verification Plan

- `uv run ruff check src/`
- `uv run mypy src/`
- `uv run pytest -q -m "not e2e" --basetemp=".pytest_tmp_linkedinn"` (full non-e2e suite)
- Focused: `tests/unit/test_routine.py`, `tests/unit/test_publishing.py`, `tests/unit/test_transcription.py`, `tests/unit/test_mcp_server.py`
- `pwsh scripts/lint-ecl.ps1` + `.\scripts\harness-change.ps1 validate`
- Record all gate outcomes in `summary.md`; close `completed`.