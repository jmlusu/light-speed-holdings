# Dashboard Hardening — Plan / Implementation Reconciliation

> Purpose: map the "CEO Dashboard Hardening Team Plan" (Tracks A–D, Phases 1–4)
> to what is actually implemented in this repository. The plan uses a
> `Track A/B/C/D` + item numbering that does **not** match the repo's own
> `A1–A5` / `C1–C5` labels, so this document is the single source of truth for
> sign-off. Statuses are **verified against live source + tests on 2026-08-30**,
> not assumed.

Legend: ✅ done · 🟡 partial · ❌ gap · 🔵 not started

---

## Track A — Security Hardening

| Plan item | Status | Evidence (files / tests) | Notes |
|-----------|--------|--------------------------|-------|
| A.1 Input validation & sanitization (POST/PATCH/DELETE) | ✅ | `src/ai_company/models/models.py`, `dashboard/api.py` (TaskAssign/TaskUpdate/ApprovalUpdate/ApprovalDecision/PaymentEntry/ProjectCostEntry validators; role gating on create_payment/project_cost/onboarding). Tests: `tests/unit/test_audit_payload_guard.py`; `TestInputValidation` cases (11). | Aligns with repo "A1" |
| A.2 CORS policy audit & tightening (GAP-010) | ✅ | `dashboard/app.py` (`CORSMiddleware`, explicit allowlist; `"*"` rejected with credentials; unknown origin rejected). Tests: `tests/unit/test_dashboard_security.py::TestCORS*` (5). | Aligns "A3" |
| A.3 Session token hardening (IP-binding, TTL, replay) | ✅ | `security/rbac.py` — ADR-013 session tokens are IP-bound, checked for expiry; WS role gate too. Tests: `test_dashboard_security.py::TestSession*` (IP-bound, invalid rejected). | Aligns "A3"; also WS auth |
| A.4 Rate limit tuning per endpoint (write vs read) | 🟡 | Global `_RateLimiter` in `dashboard/app.py` (per-IP, window, `DASHBOARD_RATE_LIMIT`); WS message rate limit (60/10s) in `dashboard/ws.py`; `llm/token_bucket.py` + `model_router.py` for LLM tier. Tests: `test_dashboard_security.py::TestRateLimiting`, `tests/unit/test_dashboard_rate_limit.py`, per-endpoint tuning? | Read/write **per-endpoint differential tuning** not explicit — single global limiter + WS limiter |
| A.5 Adversarial testing (prompt injection, via task instructions) | ❌ | No prompt-injection / jailbreak / adversarial test found. `test_dashboard_security.py` covers CORS/API-key/session/rate only. Path-traversal guard (report content) is the only injection-ish test. | Red Team campaign not present |
| A.6 CSP policy review & tightening | 🟡 | `dashboard/app.py` sets `Content-Security-Policy` (script-src self + pinned CDN, connect-src, frame-ancestors 'none'), `X-Frame-Options: DENY`, `X-Content-Type-Options`, Referrer-Policy. No dedicated CSP test. | Policy present; no test |

**Track A residual risk: A.5 (adversarial suite) missing; per-endpoint rate-limit tuning (A.4) partial; no CSP test.**

---

## Track B — Reliability Hardening

| Plan item | Status | Evidence | Notes |
|-----------|--------|----------|-------|
| B.1 File-locking audit on shared JSON/YAML state (GAP-002) | ✅ | `src/ai_company/store/file_lock.py` (platform-reliability-owner work); guarded-write path in `store/repo_write.py` / `store/file_store.py`. | Aligns "A-series/BSeries" reliability |
| B.2 DLQ replay hardening (retryable entries, GAP-008) | 🟡 | `src/ai_company/executor/dead_letter.py`: `DeadLetterQueue.retry_task()`, `retry_dlq_task()`, `move_task`, `detect_stale_tasks`. Retryable-entry semantics present. Tests: `tests/unit/test_dead_letter.py`. | Replay/retry present; "retryable-entry field" classification not explicitly surfaced |
| B.3 Circuit breaker threshold tuning (failure counts, half-open) | ✅ | `src/ai_company/llm/circuit_breaker.py`: OPEN/HALF_OPEN/CLOSED, `failure_threshold`, `recovery_timeout`, `success_threshold`, `_maybe_half_open` probe. Tests: `test_circuit_breaker.py`. | Half-open probe present |
| B.4 Graceful degradation when LLM providers unavailable | 🟡 | `llm/client.py` + provider routing + circuit breaker; no explicit "degradation" marker found. | Failover/breaker exist; explicit degraded-mode strategy not documented |
| B.5 WebSocket connection pooling / backpressure | 🟡 | `dashboard/ws.py`: `_max_ws_clients` 200-ish cap → close 1013 "Too many connections"; bounded receive 65536 → 1009; rate limit → 1008; idle sweep + half-open probe → 1008. Tests: `test_dashboard_ws.py` (15). | Robust connection cap/backpressure; no true "pooling" (single manager) |
| B.6 Audit event schema integrity & BWC evolution | ✅ | `src/ai_company/audit/` (`events.py`, `integrity.py`, `reader.py`, `writer.py`, `schema` checks); C1 hash-chain tamper-evidence (`__prev_hash`/`__seq`). Tests: integrity + audit payload guard. | Aligns repo "C1" + audit-trail-owner |

**Track B residual risk: B.4 explicit degradation strategy, B.2 retryable-field classification, B.5 pooling phrasing — all mostly covered by implementation but worth an explicit doc/commit.**

---

## Track C — Testing & Quality

| Plan item | Status | Evidence | Notes |
|-----------|--------|----------|-------|
| C.1 Security-focused test suite | 🟡 | `tests/unit/test_dashboard_security.py` (CORS, API key, session, rate limit), `test_audit_payload_guard.py`, `test_security.py`, role-escalation? | No auth-bypass/role-escalation/adversarial cases → C.1 partial |
| C.2 Contract tests for StateStore path handling | ✅ | `tests/unit/test_state_store_contract.py` (resolve base, chdir, missing-file default, forbidden path, singleton). | Aligns |
| C.3 Smoke test for dashboard health endpoint | ✅ | `tests/unit/test_dashboard_smoke.py`; `/health` + `/metrics` covered in `test_dashboard_api.py::test_metrics_endpoint_text`. | Aligns |
| C.4 WebSocket integration coverage | ✅ | `tests/unit/test_dashboard_ws.py` (15 tests) — caps, rate, unsubscribe, idle sweep, `manager.stats()`. | Aligns |
| C.5 Load test baseline (rate limiter + concurrent connections) | 🟡 | `tests/performance/test_dashboard_performance.py` (page load, API latency, charts, scroll, memory — `-m performance`). | Covers perf/latency, **not** rate-limiter nor concurrent-WS baseline explicitly |
| C.6 Flaky test monitoring & de-flaking | ❌ | No flaky-test tracking/monitoring infra found in CI/config. | Not started |

**Track C residual risk: C.1 (auth-bypass/escalation/adversarial cases), C.5 (rate-limiter + conn concurrency baseline), C.6 (flaky monitoring) remaining.**

---

## Track D — Observability

| Plan item | Status | Evidence | Notes |
|-----------|--------|----------|-------|
| D.1 Security event logging (failed auth, rate-limit hits, injection) | ❌ | `security/rbac.py` + `dashboard/app.py` gate requests but do **not** write failed-auth / rate-limit-hit events to the audit trail. | Gap — event logging for security failures missing |
| D.2 Distributed tracing (auth → rate limit → handler) | 🟡 | `telemetry/tracer.py`, `telemetry/bridge.py`, `logging_config.py`; OTel API (ADR-016, Phase-B OTel change archived). Request-flow spans not confirmed end-to-end. | Framework present; per-request auth→ratelimit→handler span coverage not verified |
| D.3 Metrics for security posture (auth failures, rate limits) | ❌ | `dashboard/monitoring.py` exposes agent/task/org-health metrics; **no** auth-failure / rate-limit / security-posture metric families. | Gap |
| D.4 Alert rules for anomalous patterns (401 spikes, rate-limit breaches) | ❌ | `config/prometheus.rules.yml` has org-health + page-load rules; **no** 401-spike / rate-limit-breach alerts. | Gap |

**Track D residual risk: D.1, D.3, D.4 are genuine gaps; D.2 partial.**

---

## Phase-level mapping

| Plan phase | Plan items | Reconciliation |
|-----------|-----------|----------------|
| Phase 1 — input validation, security tests, auth event logging | A.1-A.3 + C.1-C.2 + D.1 | A.1 ✅ · A.2 ✅ · A.3 ✅ · C.1 🟡 · C.2 ✅ · **D.1 ❌** |
| Phase 2 — rate limits, file-locking, breaker, tracing | A.4-A.6 + B.1-B.3 + D.2 | A.4 🟡 · A.5 ❌ · A.6 🟡 · B.1 ✅ · B.2 🟡 · B.3 ✅ · D.2 🟡 |
| Phase 3 — graceful degradation, WS hardening, load tests, alerts | B.4-B.6 + C.3-C.5 + D.3-D.4 | B.4 🟡 · B.5 🟡 · B.6 ✅ · C.3 ✅ · C.4 ✅ · C.5 🟡 · **D.3 ❌ · D.4 ❌** |
| Phase 4 — de-flaking, full regression, audit report, sign-off | C.6 + Final | **C.6 ❌** · full-suite regression 🟡 (scoped runs only so far) · audit report ❌ · CISO sign-off ❌ · ECL archive 🟡 (C4/C5 change in progress) |

---

## Standing gaps to close before Phase-4 sign-off

1. **A.5** — adversarial/red-team suite (prompt injection, injection via task instructions, role escalation, auth bypass).
2. **D.1** — security event logging: emit audit events on failed auth and rate-limit hits (audit-trail-owner + observability-owner).
3. **D.3** — dashboard security-posture metrics (auth-failure counters, rate-limit-hit counters).
4. **D.4** — Prometheus alert rules for 401 spikes and rate-limit breaches (extend `config/prometheus.rules.yml`).
5. **C.6** — flaky-test monitoring + de-flaking pass.
6. **C.5** — explicit rate-limiter + concurrent-WebSocket load-test baseline (extend `tests/performance/`).
7. **A.4 / A.6 / B.4 / B.2 / B.5 / D.2** — tighten wording/tests where marked 🟡 (per-endpoint limits, CSP test, degradation strategy, retryable-field classification, WS pooling doc, tracing span assertion).
8. **Full regression** — run `pytest -q -m "not e2e"` to close the archive gate for the in-flight C4/C5 ECL change, then **CISO sign-off + ECL archive** (Phase 4 gate).

---

## Verification command surfaced per plan

- Security fix: `ruff check src/ && mypy src/ && pytest tests/unit/test_security*.py`
- Auth/RBAC: `pytest tests/unit/test_dashboard_security.py -v`
- WS: `pytest tests/unit/test_dashboard_ws.py -v`
- Dashboard change: `pytest tests/unit/test_dashboard*.py -v`
- Full hardening: `ruff check src/ && mypy src/ && pytest -q -m "not e2e"`

> Note: the plan's `tests/dashboard/test_rate_limiting.py` path is **correct** —
> it exists at `tests/dashboard/test_rate_limiting.py`, and there is also
> `tests/unit/test_dashboard_rate_limit.py`. Both are valid.
