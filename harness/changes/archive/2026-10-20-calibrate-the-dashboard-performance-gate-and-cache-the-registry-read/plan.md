# Plan

## Technical Approach

1. **Calibrate the gate** (`tests/performance/test_dashboard_performance.py`).
   - Warm-up request excluded from the sample set.
   - 20 samples instead of 10.
   - The assertion moves from the maximum (the "P95" of 10 samples) to the **median**, which is robust to a single slow sample.
   - Per-endpoint budgets, calibrated from measured medians (see the table below) at roughly 3-5x headroom, because the endpoints differ by an order of magnitude in cost.
   - A load-tolerant ceiling (2000 ms) keeps the pathological case covered, matching the style already used elsewhere in the file.
   - The endpoint list becomes the budget table's keys, so a new endpoint cannot be added without a budget.

   Measured medians on a quiet developer machine (2026-10-20, after the registry cache):

   | endpoint | median (ms) | budget (ms) |
   |---|---|---|
   | /api/v1/dashboard | 38.3 | 120 |
   | /api/v1/agents | 11.4 | 50 |
   | /api/v1/tasks | 16.8 | 120 |
   | /api/v1/org-chart | 10.3 | 50 |
   | /api/v1/departments | 19.7 | 100 |
   | /api/v1/kpis | 59.3 | 200 |
   | /api/v1/kpis/summary | 77.6 | 250 |
   | /api/v1/models | 89.9 | 250 |
   | /metrics | 26.0 | 120 |
   | /health | 23.0 | 120 |

2. **Cache the registry read** (`src/ai_company/dashboard/api.py`).
   - `_load_registry()` parses the registry once per file revision instead of once per request.
   - The cache key is the registry file's **path, mtime and size**, so a write invalidates it immediately - including a write from another process, such as the registry writer that `PATCH /agents/{name}/reports-to` calls. No TTL, no in-process invalidation signal to get wrong.
   - Callers receive per-call normalized copies, so no mutable state is shared between requests.
   - Measured: `_load_registry()` 8.4 ms -> 0.26 ms median (33x).

3. **Pin the cache contract** (`tests/unit/test_dashboard_registry_cache.py`, new).
   - The file is read once while unchanged.
   - A rewritten registry is visible on the very next read.
   - The legacy camelCase normalization still applies to cached data.
   - Two calls do not share mutable state.

4. **Documentation.** `docs/known-issues.md` row, `CHANGELOG.md`, `docs/STATUS.md`.

## Impacted Modules And Files

- `tests/performance/test_dashboard_performance.py` - warm-up, 20 samples, median against a per-endpoint budget table, load-tolerant ceiling.
- `src/ai_company/dashboard/api.py` - `_load_registry()` cache keyed on the file revision.
- `tests/unit/test_dashboard_registry_cache.py` (new) - four tests pinning the cache contract.
- `docs/known-issues.md`, `CHANGELOG.md`, `docs/STATUS.md` - documentation.
- `harness/changes/**` - ECL record.

## Interfaces, Data, Permissions

- `_load_registry()` keeps its signature and return type; only its internals change. No public API, response shape, permission or registry format change.
- `mobile_api.py` has its own `_load_registry()` and is left alone: it is a separate module with a separate contract and no reported latency problem.

## Spec Gaps Found From Planning

- The audit proposed a single global threshold. Measurement showed the endpoints differ by an order of magnitude (`/api/v1/agents` 11 ms versus `/api/v1/models` 90 ms), so one threshold either flapped on the slow ones or was too loose on the fast ones. The plan therefore uses per-endpoint budgets.
- The audit proposed a TTL cache. The registry is written by another process, so a TTL would show a stale org chart for the TTL window after a write. Keying on the file revision removes that window.

## Risks And Mitigations

- **Stale registry.** Mitigated by keying on path + mtime + size, and pinned by `test_registry_change_is_picked_up_immediately`.
- **Shared mutable state between callers.** Mitigated by returning per-call normalized copies, pinned by `test_callers_do_not_share_mutable_state`.
- **A test that writes the registry and expects an immediate read.** The mtime changes on write, so the cache invalidates; the full suite verifies this.
- **The gate becomes too loose to catch regressions.** Mitigated by keeping the budgets at 3-5x of the measured medians, so a 3x+ regression still fails, and by the hard ceiling.
- **The budgets drift from reality.** The comment in the test records the calibration date and how to recalibrate.

## Verification Plan

- `uv run pytest tests/performance -q` (28 tests) and a repeat run to check stability.
- `uv run pytest tests/unit -k "dashboard or org_chart or registry"` (414 tests).
- `uv run pytest tests/unit/test_dashboard_registry_cache.py -q` (4 tests).
- `uv run ruff check` / `ruff format --check` on the touched files; `uv run mypy src/`.
- Full non-e2e pytest suite.
- `pwsh scripts/maintenance/lint-ecl.ps1` and `check-index-freshness.ps1`.
- CI on the PR: the `Test (ubuntu-latest)` and `Test (windows-latest)` jobs must both be green, repeatedly.
