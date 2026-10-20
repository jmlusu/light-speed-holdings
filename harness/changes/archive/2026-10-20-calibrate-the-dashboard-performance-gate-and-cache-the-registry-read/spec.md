# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: requirement-first (issue #484, raised by the audit of PR #483)
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: the CI performance gate `test_endpoint_response_time_p95[/api/v1/org-chart]` fails intermittently. On PR #483 it failed with `P95 response time 202ms exceeds 200ms` while nine of its ten samples were ~4 ms - one outlier, a 2 ms overshoot. The same test passed on the windows runner in the same run and passed on re-run.
- Current behavior: the gate asserts on `sorted(times)[int(len(times) * 0.95)]` over 10 samples, which resolves to the **maximum**. It has no warm-up, and its 200 ms limit is ~50x the typical response, so it can only trip on runner jitter and would not catch a real 10x regression.
- Contributing inefficiency: `get_org_chart` calls `_load_registry()` on every request, which re-reads and re-parses the 96 KB `company/agent-registry.json` through the state store. Measured locally: 8.4 ms median per call, against a 4 ms baseline for the endpoint. Ten-plus endpoints share this path.
- Source of evidence: issue #484, the CI failure log on PR #483, and local measurements of the registry read and of every endpoint in the gate.

## User Scenarios And Success

- Primary user/system scenario: the dashboard's shared CI gate must fail on a real performance regression and must not fail on a slow runner.
- Success criteria:
  - The gate fails when an endpoint is consistently several times slower, and passes when one request is slow on a contended runner.
  - The gate is calibrated per endpoint from measured medians, so a slow endpoint is not judged against a budget meant for a fast one.
  - Registry-backed endpoints stop re-reading and re-parsing the registry on every request, and never serve a stale registry.
- Acceptance criteria: `pytest tests/performance` green and repeatable, new registry-cache unit tests green, no dashboard test regressions, `ruff check` and `ruff format --check` clean, `mypy src/` clean, full non-e2e pytest green, CI green on the PR.

## Non-Goals

- Changing the dashboard's behaviour, the registry format, the auth model or any endpoint's response shape.
- Caching anything other than the registry read.
- Making the perf suite non-blocking. That remains the last resort if the gate still flaps, and is not needed while the measurement is sound.

## Constraints

- The gate must stay meaningful: a real regression has to fail it.
- The dashboard must never show a stale org chart after a registry write; the registry writer runs in another process, so invalidation cannot rely on an in-process signal alone.
- `main` is protected: branch, PR, required checks green before merge.
- ECL allows one active change; `haomtgv-blueprint-hero-and-page-wiring` was parked with the harness script and is resumed after this change closes.

## Assumptions

- The registry file's mtime and size identify its content revision for the purposes of this cache. A write that changed the content without changing either is not a realistic case.
- Callers of `_load_registry()` treat the result as read-only. The cache therefore hands out per-call normalized copies, and a test pins that no mutable state is shared.

## Open Questions

- None.

## Resolved Clarifications

- The gate keeps a hard ceiling as a safety net (2000 ms, the convention already used in the same file for load-tolerant smoke gates) and moves the real assertion to a per-endpoint median budget, so a single slow sample cannot fail the run and a consistent regression still can.
