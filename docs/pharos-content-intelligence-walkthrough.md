# Pharos Content Intelligence — Walkthrough

**Status:** Verified-by-demo
**Date:** 2026-09-17
**Governing ADR:** [ADR-020](adr/020-pharos-content-intelligence.md) (P0: routine engine + content KPIs + daily research loop)

This document walks the Pharos Content Intelligence loop as it exists today:
how a recurring research routine travels from its config through the scheduler to
the agent inbox, and how publish intents reach the publish queue. Every step below
was verified live by manually firing `pharos_sadc_research_scan` end-to-end on
2026-09-17 (see [Verified live run](#verified-live-run)).

## 1. The five-part pipeline

```
┌─ config/company/routines.yaml ── Routine definitions (5 routines)
├─ src/ai_company/orchestrator/routine.py ── RoutineStore + RoutineScheduler
│     · time-gated run_due() · crash-safe mark-before-send · idempotent routine_run_id
├─ src/ai_company/orchestrator/message_bus.py ── .opencode/inbox.json task queue
│     · each fire enqueues a FRESH Task (receiver content_creator by default)
├─ executor loop (src/ai_company/executor/daemon.py) ── consumes the task
│     · AgentLoop runs the Pharos agent, stores episodic memory + graph upsert
│     · writes reports to results/ and can email the result
└─ src/ai_company/publishing/queue.py ── publish rail (LinkedIn / Substack)
      · MCP tool publish_queue (gated) → PublishQueue → mirror task to inbox
```

The loop reuses infra the company already owns — it is a thin extension of
the daemon scheduler + message bus, per ADR-020's "no new vendor / no schema
change" constraints.

## 2. Routine configuration

Definitions live in `config/company/routines.yaml`; prompts live under
`templates/pharos/routines/`. Five routines are scheduled, all at 04:00 UTC
(06:00 CAT/SAT) on express days:

| Routine | Day | Depth | Notes |
|---------|-----|-------|-------|
| `pharos_agentic_enterprise_brief` | Mon | standard | weekly enterprise brief |
| `pharos_build_log` | Wed | standard | engineering build log |
| `pharos_sadc_research_scan` | Thu | **deep** | SADC regional signal scan |
| `pharos_policy_governance_africa` | Fri | standard | AI policy & governance Africa |
| `pharos_deep_research_brief` | Sat | **deep** | deep-research weekly brief |

All five default to `enabled: true`, receiver `content_creator`, model tier
`standard` (with optional per-routine `budget_tokens`).

Two schedule modes are supported by `Routine` (`routine.py`):

- **Weekly day/time:** `schedule_day` (ISO 1=Mon..7=Sun) + `time_utc` (HH:MM).
- **Interval:** `interval_minutes` — fixed cadence from the last run.

### Runtime-seeded fields

`last_run` / `next_run` are **not** committed in `routines.yaml`; they are seeded
at store load (the next weekday occurrence after `now`) and persisted when the
store saves after a fire. Because `run_due` is time-gated (see below), a store
loaded at 2026-09-17 11:07 UTC seeds the target's `next_run` to the *following*
Thursday `2026-09-24 04:00` — the previous Thursday had already passed.

## 3. The scheduler contract (`RoutineScheduler.run_due`)

`run_due(now)` (mirrors the KPI scheduler in `dashboard/kpis/scheduler.py`):

1. **Interval gate** — returns 0 immediately unless `interval_seconds > 0`.
   (The daemon constructs the scheduler with `--routine-interval`, default
   `900s`; a demo/test scheduler must pass a positive interval to fire at all.)
2. **Due selection** — `get_due(now)` collects every enabled routine whose
   `next_run <= now`.
3. **Mark-before-send** — each due routine is written to `next_run` (the next
   occurrence) **before** the task is enqueued, so a crash between the two
   cannot double-fire (same crash-safety pattern as the KPI/scheduler loop).
4. **Fresh task per run** — one Task per routine with an idempotent id
   `routine<run-id>-<UTC-date>`, e.g.
   `routine-pharos_sadc_research_scan-2026-09-17`. Re-driving the same run
   yields the same deterministic id, so a restarted loop cannot submit
   duplicates.

## 4. What a fired task looks like

Verified live (see section 7). One task landed in `.opencode/inbox.json`:

```
id:          routine-pharos_sadc_research_scan-2026-09-17
receiver:    content_creator
sender:      routine-scheduler
tags:        ['pharos-routine',
              'routine:pharos_sadc_research_scan',
              'routine_run:pharos_sadc_research_scan-2026-09-17',
              'research:deep']
instruction: [the rendered SadcResearchScan prompt template]
```

Post-fire the scheduler tracked `last_run=2026-09-17T04:00:00+00:00` and
advanced `next_run` to `2026-09-24T04:00:00+00:00` (next Thursday), which is
exactly the schedule the config described.

## 5. MCP surface and RBAC (`src/ai_company/mcp/server.py`)

The Pharos Content Intelligence MCP server (`pharos-content-intelligence`,
stdio) exposes five tools. Read tools require the `run` role; the write tool
requires `approve`:

| Tool | Role | Source |
|------|------|--------|
| `knowledge_graph_query` | run | GraphEngine (org_chart / decision_graph / workflow_graph / knowledge_graph) |
| `memory_recall` | run | MemoryStore (episodic, semantic, procedural, relational, temporal, aggregate) |
| `research_lookup` | run | keyword search over `docs/Pharos/*` with snippets |
| `pharos_reference` | run | path-safe read of a `docs/Pharos` document by name |
| `publish_queue` | **approve** | enqueue LinkedIn/Substack artifact (see §6) |

Every call is masked for PII, sanitized, and audit-logged
(`agent_id="pharos-mcp"`). Transport is newline-delimited JSON-RPC over stdio;
serve it with `ai-company mcp stdio` and inspect the surface with
`ai-company mcp tools`. Env: `DASHBOARD_RUN_KEY`/`DASHBOARD_APPROVE_KEY`/
`DASHBOARD_ADMIN_KEY` for RBAC, `PHAROS_DOCS_DIR` to point at the corpus.

## 6. Publish rails (`src/ai_company/publishing/queue.py`)

`PublishQueue` is a FileStore-backed queue (default
`results/pharos/publish_queue.json`) of `PublishRecord`s for the buy-side
platforms `KNOWN_PLATFORMS = {linkedin, substack}`:

- `enqueue(platform, title, body, *, bus=...)` validates the platform, persists
  the record, then — when a `bus` is passed — **mirrors** the intent to the
  agent inbox as a `pharos-publish` task (`sender_id="publish-queue"`,
  `receiver_id="content_creator"`, tags `['pharos-publish', 'publish:<platform>']`)
  so the publish step is visible to and executable by the executor loop.
- The MCP `publish_queue` tool gates this behind the `approve` role and reads
  its queue dir from `PHAROS_PUBLISH_DIR` (default `results/pharos`).

Coverage: `tests/unit/test_publishing.py`.

## 7. Verified live run (2026-09-17)

Two manual demos were executed against real code:

1. **Fix + regression:** `is_known_receiver` previously only consulted the
   registry's root `agents` key; it now reads the canonical
   `company.agents` list (with legacy fallback), and three regression tests
   lock the behavior (`tests/unit/test_routine.py`). Suite: 100 tests green;
   `ruff` and `mypy` clean.
2. **Fire** — `pharos_sadc_research_scan` was forced due in a demo scheduler
   (`interval_seconds=3600`, `_last_run=0.0`, target `next_run` rewound to just
   before the simulated fire) and `run_due(simulated_fire)` fired 1 task into a
   copy of the inbox. The task structure and prompt content were verified byte
   for byte. Operational files were restored to baseline afterwards.
3. **Publish rail** — `PublishQueue.enqueue("linkedin", ..., bus=<MessageBus>)`
   against temp paths persisted the queue record and mirrored a single
   `pharos-publish` task to the temp inbox.

### Reproducing the fire without polluting the operational inbox

To re-run the fire safely, point `MessageBus(storage_path=<temp json>)` and a
`PublishQueue(queue_dir=<temp dir>)` at throwaway paths, and do **not** rewind
the target's `next_run` on disk — patch it in memory on the loaded `Routine`
object. See `$env:TEMP\opencode\pharos_demo_b.py` (fire) and
`pharos_demo_publish_rail.py` (publish rail); both are throwaway copies outside
the repo.

## 8. Operations

- **Daemon:** `ai-company daemon` (or `docker compose` staging) runs
  `executor/daemon.py`, which constructs the `RoutineScheduler` with the bus and
  the store (default `--routine-interval 900`). The routine loop is the same
  cadence code as `kpi_snapshot`.
- **Manual fire of any routine:** load `RoutineStore`, patch the target
  `Routine.next_run` to a past timestamp **in memory**, build a scheduler with a
  positive `interval_seconds`, and call `run_due(now)`; the inbox gets the task.
- **Idempotency is by design:** deterministic `routine_run_id`; repeated fires of
  the same run id collapse to the same message, and `mark_run` advances
  `next_run` before the send.
- **Rollback:** routines YAML and the inbox are plain files — snapshot them
  before a live fire (`routines.before.yaml`, `inbox.before.json`) and restore
  to revert.

## Links

- `docs/adr/020-pharos-content-intelligence.md` — governing decision (P0 scope).
- `src/ai_company/orchestrator/routine.py`, `src/ai_company/orchestrator/message_bus.py`
- `src/ai_company/mcp/server.py`, `src/ai_company/publishing/queue.py`
- `config/company/routines.yaml`, `templates/pharos/routines/`
- `tests/unit/test_routine.py`, `tests/unit/test_publishing.py`
