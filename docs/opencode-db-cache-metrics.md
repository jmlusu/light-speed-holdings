# opencode.db — Cache metering notes (P2-T1)

**Date:** 2026-11-08 · **Owner:** llm-platform-owner (dashboard: dashboard-owner)

`tokens_cache_write` is **0 in every ledger** (session, session_v2,
message, step-finish) — a recorder/provider mapping quirk, not an audit
artefact (baseline: `session.tokens_cache_read = 15,210,842,514`).

## Rule (frozen)

Never compute a cache hit-rate from `cache_write`. Renormalized metrics:

| KPI | Definition | Baseline (2026-11-08) |
|---|---|---|
| `cache_read` volume | `SUM(tokens_cache_read)` | 15.21B (v1) + 809.9M (v2) |
| `cache_read_ratio` | `cache_read / (input + cache_read)` | ~0.90 |
| `burn_multiplier` | `(input + cache_read) / input` | 8.95× (v1) / 9.72× (v2) |
| `cache_write_reported` (bool) | any row with `cache_write > 0` | False → "unmetered provider" banner |

Dashboard code: `CostAnalytics.cache_metrics()` in
`src/ai_company/data/cost_analytics.py` (delegates to
`src/ai_company/llm/cache_metrics.compute_cache_metrics`). The hit-rate
tile must stay hidden while `cache_write_reported` is False.

## Recorder fix (upstream harness, not this repo)

Map the provider's write-side key (`cache_creation_input_tokens` /
`cache_creation`) into `tokens_cache_write`, persist `$.tokens.raw`
verbatim, and add a regression test: synthetic usage
`{input:100, cache_read:900, cache_creation:50}` must yield
`cache_write=50`. Until the harness lands this, `cache_write=0` history
is marked pre-fix and no backfill is inferred.

Reproduce (read-only, counts only):

```sql
SELECT SUM(tokens_cache_read), SUM(tokens_cache_write) FROM session;
-- Expected: 15210842514|0
```
