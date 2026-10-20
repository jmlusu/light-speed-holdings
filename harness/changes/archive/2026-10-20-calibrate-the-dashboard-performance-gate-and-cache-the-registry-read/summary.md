---
title: "Calibrate the dashboard performance gate and cache the registry read"
slug: "calibrate-the-dashboard-performance-gate-and-cache-the-registry-read"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "completed"
spec_review: "approved"
plan_review: "approved"
modules: ["src/ai_company/dashboard", "tests/performance", "tests/unit"]
files:
  - "src/ai_company/dashboard/api.py"
  - "tests/performance/test_dashboard_performance.py"
  - "tests/unit/test_dashboard_registry_cache.py"
  - "docs/known-issues.md"
  - "docs/STATUS.md"
  - "CHANGELOG.md"
tags: ["dashboard", "performance", "ci", "correctness"]
validation_status: "pass"
created_at: "2026-10-20"
updated_at: "2026-10-20"
session_id: "3b71c0a4-8f2d-4c15-9a77-2b6d4e8f1a90"
owner_agent: "jmlus"
claimed_at: "2026-10-20"
---

# Summary

## Outcome

Closes issue #484.

The shared CI performance gate asserted on `sorted(times)[int(len(times) * 0.95)]` over 10 samples, which resolves to the **maximum**. One outlier on a contended runner therefore failed it - PR #483 failed with `P95 response time 202ms exceeds 200ms` while nine of the ten samples were ~4 ms - while a real 10x regression (40 ms against that baseline) would have passed. With no warm-up and a 200 ms limit roughly 50x the typical response, the gate could only trip on jitter.

The gate now drops a warm-up request, measures a **median** over 20 samples, and compares it against a **per-endpoint budget** calibrated from measured latencies at 3-5x headroom, keeping a load-tolerant 2000 ms ceiling in the style already used in that file. Per-endpoint budgets were necessary: the endpoints differ by an order of magnitude (`/api/v1/agents` 11 ms median against `/api/v1/models` 90 ms), so one threshold either flapped on the slow ones or was too loose on the fast ones.

The contributing inefficiency is fixed at the source: the dashboard re-read and re-parsed the 96 KB agent registry on every request, and ten-plus endpoints share that path. `_load_registry()` is now cached, keyed on the registry file's **path, mtime and size**, so a write invalidates it immediately - including a write from another process, such as the registry writer behind `PATCH /agents/{name}/reports-to`. No TTL, so there is no window in which the dashboard could show a stale org. Callers receive per-call normalized copies, so no mutable state is shared between requests.

Measured: `_load_registry()` 8.4 ms -> 0.26 ms median (33x).

## Decisions

- Median plus a per-endpoint budget, rather than a single threshold or a tightened percentile: the median is the statistic that survives a contended runner, and per-endpoint budgets are the only way to keep the gate meaningful across endpoints that differ tenfold in cost.
- Key the cache on the file revision rather than a TTL: the registry is written by another process, so a TTL would show a stale org chart for the TTL window after a write.
- Keep the hard ceiling: dropping the maximum entirely would have removed the pathological case the original gate was there to catch.
- Leave `mobile_api.py` alone: it has its own `_load_registry()` with a separate contract and no reported latency problem.
- Do not make the perf suite non-blocking. That was the last resort if the gate still flapped; the measurement problem was the cause, so the gate stays a required check.

## Validation

- `uv run pytest tests/performance -q`: **28 passed**, twice (56.9 s and 90.2 s) - stability confirmed on consecutive runs.
- `uv run pytest tests/unit/test_dashboard_registry_cache.py -q`: **4 passed**.
- `uv run pytest tests/unit -k "dashboard or org_chart or registry"`: **414 passed** (no regression from the cache).
- Registry read benchmark, before and after: `store.read_json` 8.34 ms median, `_load_registry()` 8.44 ms -> **0.256 ms** median, `os.stat` 0.030 ms.
- Endpoint medians measured for the calibration (after the cache): dashboard 38.3 ms, agents 11.4 ms, tasks 16.8 ms, org-chart 10.3 ms, departments 19.7 ms, kpis 59.3 ms, kpis/summary 77.6 ms, models 89.9 ms, metrics 26.0 ms, health 23.0 ms.
- `uv run ruff check` and `uv run ruff format --check` on the three touched files: **All checks passed!** / **3 files already formatted**.
- `uv run mypy src/`: **Success: no issues found in 232 source files**.
- Full non-e2e pytest suite (`uv run pytest --basetemp=<isolated> -q`): **2666 passed / 2 skipped / 67 deselected / 0 failed** (rc=0, 6m51s). The known side-effect file `src/data/generated/agent-registry.public.json` was restored; the before/after `git status` snapshot showed no other change.
- `pwsh scripts/maintenance/lint-ecl.ps1`: **ECL lint passed**.
- `pwsh scripts/maintenance/check-index-freshness.ps1` under Windows PowerShell 5.1: **PASS**.
- CI on the PR: `Test (ubuntu-latest)` and `Test (windows-latest)` both green, plus all other required checks.

## Next Step

- Merge the PR, then confirm the parked HAOMTGV change is back in `harness/changes/active/`.
- The perf budgets carry their calibration date and method in the comment above the table; recalibrate them if an endpoint's cost profile changes.
