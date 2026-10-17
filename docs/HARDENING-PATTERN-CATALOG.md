# Hardening Pattern Catalog — CEO Dashboard / Org Health Hardening

Adjudicated resolution for wayfinder map #167, ticket #168 ("Define the hardening pattern
catalog (what patterns, where they apply)"), 2026-08-28. Consolidated from
platform-reliability-engineer, observability-engineer, scalability-architect, and CTO
adjudication, corrected against the actual repo tree.

Scope: harden the **CEO Dashboard**, **daemon executor**, **scheduler**, and **message
bus** against operational mistakes and resource exhaustion. **Org Health is the pilot
vertical slice.** This catalog is the checklist the tickets #170-175 implement against and
#176 synthesizes into the final deliverable.

See also: `docs/research/hardening-primitives-reuse.md` (ticket #169 — what we reuse).

## 1. Reuse decision

- **REUSE** `src/ai_company/llm/circuit_breaker.py::CircuitBreaker` as the breaker engine
  everywhere a consecutive-failure breaker applies. Two additive changes, both backward-
  compatible: make it **thread-safe** (adopt the `TokenBucket` lock) and add a
  `metric_prefix` constructor param (default `"circuit_breaker"`, so LLM paths are
  unchanged) used for the emitted counter names.
- **REUSE** `src/ai_company/llm/token_bucket.py::TokenBucket` as-is for pacing producer
  retries / dispatch.
- **NEW — tiny, shared `src/ai_company/reliability/` package** (mirrors `llm/`, `store/`,
  `data/` layout):
  - `reliability/timeout.py` — `call_with_timeout(fn, *, timeout_s, metric_prefix)`,
    raises typed `TimeoutError`, counts the timeout as a breaker failure. Stdlib
    `concurrent.futures` / `asyncio`.
  - `reliability/breaker.py` — factory `build_breaker(component, config)` constructing
    `llm.CircuitBreaker` from config. No re-implementation.
  - `reliability/admission.py` — inbox cap check + rejection helper (for #172).
  - `reliability/config.py` — `load_hardening_config(component)` reading
    `company/config/hardening.yaml` with catalog defaults as fallback.
- **Do NOT** build a new breaker, a new rate limiter, or a generic retry framework. No
  third-party resilience dependency (none exists in the tree; `tenacity` is transitively
  present only via `safety`).

Coupling verdict: `reliability` importing `llm.circuit_breaker` /
`llm.token_bucket` / `dashboard.monitoring` is acyclic and one-directional; the
`monitoring` edge already exists in both primitives. If this ever blocks a non-dashboard
import, invert it with a `reliability.metrics` shim that `dashboard.monitoring` registers
into.

## 2. Pattern x component matrix

CB = circuit breaker · TO = per-call timeout · BH = bulkhead/thread isolation · RT = retry
· BP = backpressure · RC = resource cap · DG = dedup guard · TE = tamper-evident append

| Component | CB | TO | BH | RT | BP | RC | DG | TE |
|-----------|----|----|----|----|----|----|----|----|
| Org Health scorer pipeline (`dashboard/org_health.py`) | ✔ per-scorer | ✔ per-scorer deadline | ✔ worker pool, one slot per scorer | — | — | ✔ pool bound | ✔ dedup `compute()` window | — |
| Daemon tick loop (`executor/daemon.py`) | ✔ tick-level | ✔ per-tick budget | ✔ tick on child + supervisor stays live | ✔ bounded dispatch retry | ✔ skip work when saturated | ✔ cap concurrent ticks | ✔ same task id never double-dispatched | — |
| Scheduler dispatch (`orchestrator/scheduler.py`) | ✔ schedule eval breaker | ✔ per-schedule eval timeout | — | ✔ bounded retry + backoff | ✔ hold/skip when bus full | ✔ cap scheduled-jobs table | ✔ stable dedup key | — |
| Message bus inbox (`orchestrator/message_bus.py`) | — | ✔ per-op timeout | — | ✔ read path (existing `_read_text_with_retry`) | ✔ **reject-new past cap** | ✔ `max_pending` cap | ✔ reject duplicate `correlation_id` | ✔ monotonic seq per entry |
| Audit store (`data/audit_store.py`) | — | ✔ per-append timeout | — | ✔ bounded, then fail-closed alert | — | ✔ size budget | — | ✔ **hash chain (core)** |

**Why CB is NOT applied to inbox/audit:** a breaker amputates scoring/dispatch (accept —
recompute later). Refusing to *accept* a task or *write* an audit record is data loss. Those
two components escalate via **cap + backpressure** and **halt-on-tamper**, never by opening
a breaker.

## 3. Failure philosophy

- **Scoring = fail-open to last-known-good + degraded marker.** A single slow/failing
  scorer degrades gracefully: return the last cached component score; on cold start fall
  back to the existing `value=None` → excluded-from-composite semantics
  (`org_health.py:283-303`, `184-191`). Never block the dashboard thread.
- **Banding = fail-closed only on total failure.** If *every* scorer is unavailable,
  return RED/UNKNOWN + critical alert — an un-scored health must read as bad, never as
  falsely Green. Partial failure stays fail-open.
- **Admission (inbox) = fail-closed reject-new.** Reject new sends with a busy signal;
  never shed old tasks silently (tasks carry HITL approvals, cost, audit correlation).
- **Integrity (audit chain) = fail-closed halt.** On hash mismatch, stop appends + alert;
  no auto-repair, no silent bypass. Integrity beats availability here.
- **Never silent anywhere:** every hardening-path `except` must re-raise, escalate, or emit
  a metric + log.

## 4. Defaults and config

**One config file: `company/config/hardening.yaml`** (matches the existing
`company/config/{kpis,webhooks}.yaml` convention; loaded via `reliability/config.py` with
these catalog numbers as fallbacks). Org-health *domain* thresholds (bands) stay in the
already-loaded `config/org_health.yaml`; *ops* alert parameters go in a new
`config/alerting.yaml`.

| Key | Default | Escalation on exhaustion |
|-----|---------|--------------------------|
| `org_health.call_timeout_s` (per scorer) | `3.0` | fail-open → cached/None + alert |
| `org_health.breaker.{failure_threshold,recovery_timeout_s,success_threshold}` | `3` / `60` / `1` | open → fail-open to cached + alert |
| `org_health.worker_pool_size` (bulkhead) | `min(#scorers, 4)` | excess queues to `queue_cap` 20 then drop-oldest + log |
| `org_health.dedup_window_s` | `5` | duplicate `compute()` returns last result |
| `daemon.tick.timeout_s` | `5.0` | kill tick worker; skip loop phases |
| `daemon.tick.failure_threshold` (consecutive) | `5` | pause claiming/new work, P1 alert, probe every `30s`, resume after `3` ok ticks |
| `daemon.tick.interval_s` | `2` | — |
| `daemon.dispatch.retry.{max_attempts,backoff_base_s,backoff_factor,max_s,jitter}` | `5` / `2.0` / `2.0` / `60` / `0.2` | exhausted → DLQ with reason `dispatch_exhausted` (reuse existing DLQ) |
| `scheduler.dispatch.timeout_s` | `5.0` | fail-closed "not due" this pass + log |
| `scheduler.dispatch.breaker.{failure_threshold,recovery_timeout_s}` | `5` / `120` | open → park schedule + alert |
| `scheduler.dispatch.dedup_ttl_s` | `300` | duplicate skip + `dispatch_duplicate_skipped` |
| `message_bus.inbox.max_pending` | `200` | **reject-new**: raise `InboxFullError`; CLI exit `4`, HTTP **503 + `Retry-After: 30`**; alert at 80% |
| `message_bus.inbox.warn_at_fraction` | `0.8` | warn log + high-watermark metric |
| `message_bus.op_timeout_s` | `5` | fail-closed error to caller; alert if recurring |
| `message_bus.retry.{rate,capacity}` (TokenBucket) | `2/s` / `10` | paced producer retries |
| `message_bus.dedup` | reject duplicate `correlation_id` non-terminal | log + alert (would double-execute) |
| `message_bus.max_inbox_age_days` | `30` | purge oldest *completed* under lock; never `in_progress`/queued |
| `audit.append_timeout_s` | `2` | on-disk-to-memory buffer + critical alert |
| `audit.chain.{hash_algo,verify_on_read}` | `sha256` / `true` | mismatch → halt appends + `audit_chain_break` + critical alert |
| `audit.max_log_size_mb` | `100` | rotate (append-only file per rotation); alert — never overwrite |
| `audit.retention_days` | `30` active, gzip archive, 365 d archive retention | reuse governance archive path (`data/archives/`) |

Sizing rationale (scalability-architect): single laptop runtime, sprint peaks ~30-60
tasks/hr; defaults validated against 10x (~300-600/hr). `200` pending ≈ 2x the 10x
steady-state + stall room for parked HITL approvals; the inbox is O(N) whole-file rewrite
per mutation (`MessageBus._mutate_tasks` → `FileStore.update_json`), so 200 keeps rewrites
~0.5-1.5 MB / ~10 ms on SSD. Dashboard process-wide resource caps (RSS ~1024 MB warn 768,
inflight 8, scoring concurrency 2) remain fog — need pilot data, revisit at #176.

## 5. Metric namespace and alerts (for #171)

- Root prefix **`ai_company_`** (existing convention: `monitoring.py:60-72`), subsystem
  segment per component: `ai_company_org_health_`, `ai_company_message_bus_`,
  `ai_company_daemon_`, `ai_company_audit_`, `ai_company_dashboard_`. Labels carve
  component/band/route/provider — never in the name. No new metric name without touching
  this catalog (#171 owns the contract).
- Extend `dashboard/monitoring.py` with a labeled-series helper (`observe(name, value,
  labels)` + a `HISTOGRAM_BUCKETS` map) and a lock around the registry (it is not
  thread-safe today). Keep the existing `.inc_metric`/flat-counter path.
- **Pilot metric contract (implement exactly in #171):**

| Name | Type | Notes |
|------|------|-------|
| `ai_company_org_health_scoring_duration_seconds` | histogram | label `component`; buckets `[0.01…10]` |
| `ai_company_org_health_compute_duration_seconds` | histogram | full pass |
| `ai_company_org_health_scoring_attempts_total` | counter | label `component` (ratio denominator) |
| `ai_company_org_health_scoring_failures_total` | counter | label `component` |
| `ai_company_org_health_score` | gauge | composite 0-100 |
| `ai_company_org_health_band` | gauge 0/1 | label `band` ∈ green/amber/red |
| `ai_company_org_health_band_transitions_total` | counter | labels `from`,`to` |
| `ai_company_org_health_components_missing` | gauge | guards silent composite drift |
| `ai_company_circuit_breaker_open` | gauge 0/1 | label `provider`/`component` (new) |
| `ai_company_circuit_breaker_trips_total` / `_half_open_total` | counter | add `provider`/`component` label (backward-compatible) |
| `ai_company_dashboard_request_duration_seconds` | histogram | label `route`,`method`,`status` |
| `ai_company_dashboard_page_load_duration_seconds` | histogram | label `page`; server-side first, RUM optional v2 |
| `ai_company_message_bus_inbox_depth` / `_capacity` | gauge | capacity: threshold-free alert expr |
| `ai_company_message_bus_submissions_total` | counter | label `result`, `reason` |
| `ai_company_message_bus_quarantine_events_total` | counter | corruption recovery visibility |
| `ai_company_daemon_ticks_total` | counter | label `result` ∈ success/error |
| `ai_company_daemon_last_tick_timestamp_seconds` | gauge | stale-daemon alert |
| `ai_company_daemon_consecutive_tick_failures` | gauge | one-line alert expr |
| `ai_company_audit_chain_mismatch_total` | counter | integrity breach |

- **Bands (source of truth: `config/org_health.yaml`):** Green 80-100, Amber 50-79, Red
  0-49. Recommended hysteresis to prevent flapping: `amber_to_green_min: 83`,
  `red_to_amber_min: 52` (normal bands on the way down; higher bound on the way up).
- **Alert rules** → `config/alerting.yaml` rendered into `config/prometheus.rules.yml`;
  wire `rule_files:` + Alertmanager in `docker-compose.staging.yml` monitoring profile.
  **Page (P1):** `OrgHealthRed` (band red ≥15m), `OrgHealthScoringFailureRatio` (>10%
  failing, 10m), `CircuitBreakerOpen` (≥10m), `InboxOverCapacity` (depth > cap, 5m),
  `DaemonConsecutiveTickFailures` (≥3), `DaemonStale` (no tick >180s). **Log/Slack:**
  `OrgHealthAmber` (≥30m), `OrgHealthScoringFailureRatioWarn` (>2%), `CircuitBreakerTripStorm`
  (>5 trips/10m), `InboxBacklog` (>80% cap, 10m), `InboxQuarantineEvents`.
- **SLO seeds (checklist artifact for #176):** org-health p95 compute < 2s and scoring
  success ≥ 99.9% (30d); dashboard availability ≥ 99.9%; inbox within capacity ≥ 99.5%;
  daemon tick success ≥ 99.5% (7d) and last-tick age ≤ 2× interval; zero sustained open
  breakers. PromQL snippets live in the observability-engineer's contribution.

## 6. Ticket-specific implementation notes (seams)

**#170 Org Health breaker + timeout** — wrap at the single choke point
`org_health.py:300` (`scorer(database)` inside `_compute_component` 283-303), dispatch by
component name (289-294). Run each scorer via `call_with_timeout` inside the bulkhead
worker pool; per-component breaker from `reliability/breaker.py`. Preserve the
fallback-to-`None` semantics so the composite math (`184-191`) works unchanged. Optionally
dedupe the 3 redundant `_company_window_tasks()` reads (314, 337, 387) via one fetch per
compute + the 5s dedup window. Outer safety net: overall deadline on `compute()`.

**#171 Metrics + alerts** — implement the metric contract (§5) + `config/alerting.yaml` +
Prometheus rules + Alertmanager wiring. Order: histogram helper → instrument scorers → page
latency middleware → bus/daemon metrics → rules. Tests must assert exact metric names in
`/metrics` text output. Reload `org_health.yaml` per `compute()` (currently loaded at
`__init__`, `org_health.py:154`) so band tuning is live.

**#172 Inbox cap + backpressure** — cap check *inside* `MessageBus.send_task` before both
file append and SQLite mirror (`message_bus.py:222-247`; atomic with the write via
`FileStore.update_json`); raise `InboxFullError` rather than changing the `-> None`
contract. Callers to teach the new error: `executor/loop.py:823`,
`executor/dead_letter.py:216,319` (must not lose tasks — keep in DLQ), `scheduler.py:123`,
`services/base.py:133`, `services/client_intake.py:255`, `dashboard/api.py:988` (→ 503),
`cli/specialists.py:156`, `data/etl/pipelines/governance.py:199`.

**#173 Daemon tick breaker + consecutive errors** — wrap `executor.tick()` at
`daemon.py:735`; consecutive-failure counter incremented in the existing `except`
`daemon.py:744-745`, reset on success (`735-742`); skip loop + scheduled phases while OPEN
(`747-789`); expose `consecutive_tick_failures` / `circuit_state` via
`DaemonHealthStatus.write` (`daemon.py:471-502`) + `/api/v1/daemon/status`.

**#174 Scheduler dispatch + dedup** — wrap `bus.send_task(task)` at `scheduler.py:123`;
on `InboxFullError` revert `next_run`/`last_run` (note `mark_completed` runs *before* the
send at `:122` — restore on failure + `_save_config`) so the cycle retries. Dedup key:
`f"sched:{scheduled.id}:{scheduled.next_run.isoformat()}"` stamped as `correlation_id`
(or `scheduler` marker), skip if a matching non-terminal task exists (scanner at
`message_bus.py:249-252`). Guard `create_pending_tasks` in `run_forever` (`scheduler.py:160`).

**#175 Audit hash chain** — chokepoint `AuditStore.write_batch()` (`audit_store.py:38-64`):
read tail hash (`SELECT event_hash … ORDER BY timestamp DESC, rowid DESC LIMIT 1`), compute
`sha256(prev_hash + canonical(event_data))`, insert atomically, rollback on failure. Model
(`audit/events.py:46-93`) + schema (`data/database.py:65-76`) gain `prev_event_hash` and
`event_hash` (default `""` keeps existing rows valid). Documented hazards for the
implementer: `INSERT OR REPLACE` can overwrite an `event_id`; `compact_events`
(`:440-460`) mutates payloads → hash must cover immutable fields or recompute; `archive_before`
(`:547-616`) severs the chain → preserve head hash in archive metadata; the JSONL writer
mirror (`audit/writer.py:150-177`) is a second write channel → same hashing or explicit
SQLite-only scope decision.

## 7. Consistency rules (invariants — every implementation must follow)

1. **Metric namespace:** every new metric carries an `ai_company_<subsystem>_` segment; no
   bare `circuit_breaker_*`/`*_total` without attribution. Extending a primitive with a
   `metric_prefix`/label defaults to today's behavior.
2. **Config-driven thresholds:** zero hard-coded tunables. Every default lives in
   `company/config/hardening.yaml` (domain bands in `config/org_health.yaml`); code reads
   via `reliability/config.py` with catalog fallback.
3. **No silent swallowing:** every hardening-path `except` re-raises, escalates, or emits a
   metric + log. Bare `except: pass` is a merge-blocking review failure.
4. **Explicit timeouts:** every hardened call gets an explicit timeout from config;
   unbounded waits are prohibited; every timeout counts as a breaker failure.
5. **One breaker, one timeout:** breaker usage goes through `llm.CircuitBreaker` (via
   `reliability/breaker.py`); timeout wrapping through `reliability/timeout.py`. No third
   implementation.
6. **Fail direction:** observability fails open with an explicit degraded/UNKNOWN marker;
   admission and integrity fail closed. Never silent in either direction.

## 8. Rollout order and fog graduation

| Step | Ticket | Deliverable | Fog resolution |
|------|--------|-------------|----------------|
| 0 | folded into #170 | `src/ai_company/reliability/` + `company/config/hardening.yaml` + `metric_prefix` on `CircuitBreaker` | — |
| 1 | #170 | Org Health circuit + timeout (pilot validates the layer) | — |
| 2 | #171 | Prometheus metrics + alerts | **Green/Amber/Red thresholds now specified** (80 / 50 / 0, hysteresis 83/52, stale > 2× interval, UNKNOWN band). Alert *routing* tiers stay fog until #176 |
| 3 | #173 | Daemon tick breaker + consecutive error tracking | — |
| 4 | #174 | Scheduler dispatch error handling + dedup | — |
| 5 | #172 | Inbox cap + backpressure | **Inbox cap + retry pacing + rejection codes now specified** (200, reject-new, exit 4 / 503). Dashboard process resource caps stay fog until #176 |
| 6 | #175 | Audit append-only hash chain | **Chain format/algo/verify now specified** (sha256, verify-on-read). Rotation/retention policy stays fog — v1 default is no-rotation append-only, reopened at #176 |
| 7 | #176 | Finish gate: synthesize final checklist | Verify table coverage, invariants, metric presence per component, config keys vs defaults; reopen remaining fog (alert routing, retention, dashboard resource caps) |

Consistency note: the catalog numbers above ARE the working implementation defaults for
#170-175; tickets may tighten per component but must not silently diverge.
