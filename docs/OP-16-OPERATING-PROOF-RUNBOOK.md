# OP-16: One-Day Operating Proof — Runbook

**Issue**: #16 (Run the one-day operating proof)
**Blocked by**: #15 (configured guardrails) — **status: satisfied** (`config/company/guardrails.yaml`)
**Status**: PLANNED — awaiting human sign-off before any LLM spend

## 1. Objective

Prove the executor + dashboard + memory + scheduler loop works end-to-end on the
local Windows daemon: seed a small batch of safe tasks, let the executor process
them under budget caps, verify the supporting cycles (daily briefing, KPI snapshot,
governance retention, memory recall/consolidation), capture live dashboard +
WebSocket state, and record what works / what breaks. Pass → gate #17
(sustained cadence).

**Scope change from the ticket**: #16 originally proposed working "existing pending
inbox tasks" — the inbox was purged in Sprint 8 (`.opencode/inbox.json` is `[]`), so
the proof seeds a small controlled batch instead of the old stale placeholders.

## 2. Pre-flight (no spend)

1. `uv run ai-company executor status` → expect "no daemon" + `Total tasks: 0`.
2. Confirm `.opencode/inbox.json` is `[]`; `logs/` exists.
3. **Provider reachability** — the executor needs at least one configured provider.
   Standard tier tries `GEMINI_API_KEY` → `OPENCODE_API_KEY` → local `ollama`.
   Check at least one is present in the environment (do not print the value).
4. `scripts/backup.ps1` → snapshot of `.opencode/`, `company/`, `results/`.
5. Port check: `8421` free for the dashboard (isolated from prod `8420`).
6. **Canary**: seed + tick ONE trivial task (see §4) via a single
   `executor tick` — proves provider auth end-to-end before the daemon run.
   Abort if the canary fails; diagnose provider config first.

## 3. Guardrails & budget

Loaded automatically from `config/company/guardrails.yaml` by `_resolve_budgets`:

| Cap | Value | Enforced |
|-----|-------|----------|
| Daily LLM budget | $2.00 USD | `CostTracker.daily_budget_exceeded()` + auto-suspend (`suspend_daily`) |
| Per-task budget | $0.50 USD | `AgentLoop.check_budget()` per iteration |
| Overspend action | suspend for rest of day | `Executor.tick()` returns 0 |

**Stop conditions**: task budget per task; daily budget for the whole run;
manual abort (§7). Expected spend for the batch: ≤ ~$0.10 with a cheap model.

## 4. Task batch (3 read-only, standard-tier, no HITL parking expected)

Seeded via `MessageBus.send_task` (python one-liner), `sender_id: human-ceo`,
`priority: MEDIUM`:

| # | Receiver | Instruction (self-contained, read-only) |
|---|----------|------------------------------------------|
| T1 | `technical-documentation-lead` | Read `docs/STATUS.md`; return a 5-bullet summary of current project state and the three biggest risks. Do not modify any files. |
| T2 | `chief-of-staff` | Read `docs/TASK-BOARD.md` and `.opencode/inbox.json`; report open task count and priority distribution. Do not modify any files. |
| T3 | `threat-intelligence-analyst` | Analyze `.opencode/audit` for error-level entries in the last 7 days; summarize recurring patterns. Do not modify any files. |

Rationale: read-only analysis tasks avoid `write`/`bash` tools so the
tier-rules HITL gate (`require_approval_from_tier: 2`) should not park them.
If a task does park: `uv run ai-company orchestrator approval-approve <request_id>`.

## 5. Execution sequence (the run)

1. Seed T1–T3 into the inbox.
2. `uv run ai-company executor start --daemon --governance-interval 60`
   (short retention interval so governance runs within the proof window;
   budgets auto-load from guardrails config).
3. Verify lifecycle: `logs/executor-daemon.pid` + `logs/executor-daemon.json`
   written; `uv run ai-company executor status` shows `state: running`.
4. Wait for task completion (poll `executor status`; expected minutes).
5. `uv run ai-company orchestrator briefing` → regenerates
   `.opencode/daily_briefing.md`.
6. Start dashboard: `uv run ai-company dashboard --port 8421 --no-open`;
   confirm `GET /api/...` health + live task events over WebSocket.
7. Confirm KPI snapshot ran (daemon `kpi-snapshot-interval` 300s) and
   governance retention executed without error.
8. Stop daemon: `uv run ai-company executor stop`; re-run `executor status`
   → `state: stopped`, no orphan `python` executor process.

## 6. Success criteria (from #16)

- [ ] Daemon lifecycle: start → PID/status file → running → graceful stop.
- [ ] ≥2 of 3 tasks COMPLETED with `results/{task_id}/loop_result.json` artifacts;
      no unexpected DLQ entries (`executor dlq-list`).
- [ ] Cost tracking: usage recorded (cost log), per-task ≤ $0.50, daily ≤ $2.00.
- [ ] Daily briefing regenerated.
- [ ] KPI snapshot collected.
- [ ] Governance retention ran without error.
- [ ] Dashboard live on 127.0.0.1:8421 with WebSocket task updates.
- [ ] Memory recall ran before execution; outcomes recorded; consolidation ticked.

## 7. Rollback / abort

- **Abort run**: `uv run ai-company executor stop` (foreground: Ctrl+C).
- **Abort dashboard**: Ctrl+C on the uvicorn process.
- **Budget trip**: auto-suspend halts processing for the day (reset = next
  calendar day or manual cost reset — documented, no data loss).
- **Post-proof cleanup**: purge test tasks from the inbox (restore `[]`),
  keep `results/*` as evidence; optionally archive the batch under
  `docs/archive/2026-08-13-op16-proof/`.

## 8. Evidence to capture

`logs/executor-daemon.log`, `logs/executor-daemon.json` (final state),
`results/*/loop_result.json`, `.opencode/audit`, cost export JSONL,
`.opencode/daily_briefing.md`, dashboard health + WS observations,
final `executor status` + `dlq-list` output. Summarized into the #16 issue.

**Timezone note**: all evidence timestamps are UTC — ISO-8601 with an explicit
`+00:00` offset (e.g. `2026-08-14T09:30:00+00:00`). This includes
`loop_result.json` `timestamp`, DLQ `moved_at`, workflow `started_at` /
`completed_at`, memory `created_at`, KPI snapshot filenames, and dashboard
`created_at` / `responded_at` / `evaluated_at` fields. Audit events, cost
tracking, daemon state, WebSocket broadcasts, and retention records were
already UTC.

## 9. Gate outcome

- **PASS** (all green or minor fix-list): close #16 → plan #17 cadence from what worked.
- **PARTIAL** (core loop works, some cycle fails): log blockers, fix-list, targeted retry.
- **FAIL** (nothing executes end-to-end): diagnose top blocker (provider auth, config path,
  daemon file perms), then re-plan.

## 10. Risks & mitigations

| Risk | Mitigation |
|------|-----------|
| No provider key / auth failure | Pre-flight canary catches before any run; circuit breaker isolates provider |
| HITL parking blocks a task | Read-only task set; approve via `orchestrator approval-approve` if needed |
| Budget runaway | Hard $0.50/task + $2/day caps + auto-suspend (config-enforced) |
| Daemon orphan process | `executor stop` + verify PID gone; fallback `Stop-Process` by PID file |
| Dashboard port clash | Proof uses 8421 (prod is 8420) |
