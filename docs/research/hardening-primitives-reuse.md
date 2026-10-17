# Research: existing circuit breaker / token bucket APIs for reuse

Resolution asset for wayfinder ticket #169 ("Research: existing circuit breaker / token
bucket APIs for reuse"). Read-only investigation, written 2026-08-28. Every claim cites
`file:line` relative to the repo root.

Ticket question: identify existing resilience implementations in the codebase
(`src/ai_company/llm/circuit_breaker.py`, `src/ai_company/llm/token_bucket.py`) and
evaluate their suitability for reuse in the Orchestration and Dashboard layers.

## Verdict (one line)

Reuse `TokenBucket` as-is anywhere (thread-safe, zero coupling); reuse `CircuitBreaker`
as the breakout engine everywhere a consecutive-failure breaker is needed, but only after
adding thread-safety and a configurable `metric_prefix` — it currently hard-imports the
dashboard metrics module and is not safe under concurrency.

## 1. API surface

### `CircuitBreaker` — `src/ai_company/llm/circuit_breaker.py`

```python
class CircuitState(Enum):            # circuit_breaker.py:11-14  CLOSED / OPEN / HALF_OPEN
def __init__(self, failure_threshold: int = 3,       # circuit_breaker.py:26-31
             recovery_timeout: float = 60.0,
             success_threshold: int = 1) -> None
@property state          -> CircuitState   # circuit_breaker.py:41-50  lazy OPEN->HALF_OPEN
@property is_available    -> bool           # circuit_breaker.py:52-54  True in CLOSED|HALF_OPEN
def record_success() -> None           # circuit_breaker.py:56-63
def record_failure(error_category: str | None = None) -> None  # circuit_breaker.py:65-83
```

- Consecutive-failure counting (not time-windowed). Opens at `failure_threshold`, auto
  half-open after `recovery_timeout`, closes after `success_threshold` consecutive
  successes.
- `record_failure("auth")` is a silent no-op (`circuit_breaker.py:75-76`): auth/config
  errors never trip the breaker.
- **Not thread-safe.** No lock; state mutated on read paths. Safe for single-threaded
  callers only.
- **Metrics coupling:** hard-imports `inc_metric` from `ai_company.dashboard.monitoring`
  (`circuit_breaker.py:8`) and emits `circuit_breaker_trips_total` /
  `circuit_breaker_half_open_total`.

### `TokenBucket` — `src/ai_company/llm/token_bucket.py`

```python
def __init__(self, rate: float, capacity: float) -> None   # token_bucket.py:27-34
def _refill(self) -> None                                  # token_bucket.py:36-40
def try_acquire(self) -> bool                              # token_bucket.py:42-49
def acquire(self, timeout: float = 0.0) -> bool            # token_bucket.py:51-64
```

- Fixed-rate refill capped at burst `capacity`, `time.monotonic()`-based.
- **Thread-safe** (single `threading.Lock`, `token_bucket.py:34`).
- **Zero coupling** — pure `threading` + `time`.

## 2. Usage inventory

`CircuitBreaker` — one per LLM provider in `llm/client.py:77,88`; skip-checked before
calls at `client.py:318-322` / `493-497` (stream) / `executor/agent_loop.py:622-623`;
success/failure recorded at `client.py:352,390,523,560` and `agent_loop.py:645,649`.
`doctor/checks.py:314,322` reads breaker state from the OmniRoute gateway health JSON
(external system, unrelated to this class).

`TokenBucket` — per-provider limiters built from `rate_limit.{rate,capacity}` in
models.yaml (`client.py:78,92-95`); consumed at `client.py:323-324` and `498-499`.
Only created when both `rate` and `capacity` are present.

Metrics: registry keys at `monitoring.py:60-72`, Prometheus text render at
`monitoring.py:101-179`; exported names `ai_company_circuit_breaker_trips_total` /
`ai_company_circuit_breaker_half_open_total`; endpoint `GET /metrics`
(`monitoring.py:393-400`, mounted at `app.py:497`). Counters are **in-memory per
process** — the daemon and dashboard processes each keep their own.

## 3. Coupling (cost of reuse outside the llm layer)

- `TokenBucket`: none. Freely reusable anywhere (sync code).
- `CircuitBreaker`: imports `dashboard.monitoring` (`circuit_breaker.py:8`), which pulls
  in FastAPI, the router, SQLite, psutil — i.e. the whole dashboard stack. It also
  string-couples to `ProviderErrorCategory` semantics (the `"auth"` special-case is a
  hardcoded value; callers outside the LLM layer must know the convention).

## 4. Suitability assessment

| Target | Verdict | Rationale |
|--------|---------|-----------|
| Org Health scorer pipeline (`dashboard/org_health.py`) | **needs-new wrapper** | Scorers are aggregate reads (`org_health.py:305,321,348,374`), not gated live calls. Reuse the breaker engine per component + a new timeout wrapper. |
| Daemon tick loop (`executor/daemon.py`) | **reuse-with-fixes** | `TokenBucket` usable as-is to pace KPI/governance work. `CircuitBreaker` unsafe until thread-safe + metrics decoupled (daemon would otherwise run a second, disconnected in-memory counter set). |
| Dashboard FastAPI process | **reuse-with-fixes** | Same process as the metrics registry (breaker counters already exposed via `/metrics`), but FastAPI runs requests on a thread pool → breaker needs the lock `TokenBucket` already has. |
| Message bus / scheduler (`orchestrator/message_bus.py`, `orchestrator/scheduler.py`) | **reuse-with-fixes / needs-new** | Bus already imports `inc_metric` (`message_bus.py:26`) so a `TokenBucket` pace-guard drops in cleanly. There is no live external call to gate → breaker semantics don't map to the bus itself; cap + backpressure are the right guard (see catalog). |

No third-party resilience dependency exists (`pyproject.toml:14-36`); `tenacity` appears
only transitively via `safety` (uv.lock). The in-repo primitives are the primitives to use.

## 5. Gaps the hardening tickets (#170-175) need but the primitives lack

1. **Per-call timeout wrapper** — neither primitive bounds execution time.
2. **Async support** — both are sync; the dashboard event loop needs async-safe variants.
3. **Bulkhead / concurrency isolation** — no semaphore limiting in-flight calls.
4. **Config-driven breaker thresholds** — currently constructor defaults only
   (`client.py:88` always `CircuitBreaker()`); the bucket *is* config-driven.
5. **Shared/durable metrics sink** — in-memory per process, so daemon and dashboard
   report independent values.
6. **Time-windowed / failure-rate semantics** — consecutive-count only.
7. **Thread-safety on `CircuitBreaker`** — absent; `TokenBucket`'s lock is the model.
8. **Category decoupling** — the `"auth"` special-case should be an injectable classifier.

## 6. Decision this research unblocks

- Create a thin shared layer `src/ai_company/reliability/` that (a) adds a per-call
  `call_with_timeout`, (b) exposes `CircuitBreaker` via a config-driven factory, and
  (c) hosts admission (inbox cap) + config loading. Add `metric_prefix` to
  `CircuitBreaker` (backward-compatible default) and make it thread-safe. Do not fork the
  primitives. Full context: `docs/HARDENING-PATTERN-CATALOG.md`.
