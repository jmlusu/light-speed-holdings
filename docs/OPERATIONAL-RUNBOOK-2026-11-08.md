# Operational Runbook — 2026-11-08

## git reset --hard Safety

`git reset --hard` is the nuclear option for resetting the working tree to match `HEAD`. Use only when explicitly directed by a lead engineer or the CTO.

### Behavior with `data/ai_company.db`

- `data/ai_company.db` is **explicitly gitignored** (`.gitignore` lines 145–153).
- A plain `git reset --hard` on `data/ai_company.db` **leaves it unchanged** — it stays ignored (`!!` status). The file is not tracked, so `--hard` has no effect on it.
- **Never** commit `data/ai_company.db`. It is a local SQLite mirror of `results/cost_log.jsonl`; committing it would lock the live 117k-row mirror into history and cause data loss on reset.

### When `git reset --hard` is safe

- Refreshing the working tree after a force-push rewrite.
- Recovering from a corrupted local state that cannot be resolved via merge/rebase.
- **Never** use to "undo" committed changes to tracked source files — use `git revert` or `git reset --soft --hard` with a saved branch instead.

### Recovery after force-push rewrite

```powershell
# Fetch the latest main from origin (may have rewritten history)
git fetch origin

# Reset the working tree + index to match origin/main
git reset --hard origin/main
```

### What to do after

1. Rebuild the `data/ai_company.db` mirror:
   ```powershell
   uv run ai-company dashboard backfill
   # Expected duration: ~4 minutes for 117k rows
   ```
2. Run the cost-tracker guard:
   ```powershell
   python scripts/test/check-cost-tracker.py
   # Exit 0 = totals match (safe)
   # Exit 1 = mismatch / untagged spend / missing log (fail — do not merge)
   ```
3. Verify the dashboard health endpoint responds.

---

## Mirror Rebuild (Fresh Clone Onboarding)

When onboarding a fresh clone (e.g. after a force-push rewrite or new developer machine), the `data/ai_company.db` mirror must be rebuilt from the source of truth: `results/cost_log.jsonl`.

### Command

```powershell
uv run ai-company dashboard backfill
```

### Expected behavior

- Reads `results/cost_log.jsonl` (117k rows).
- Regenerates `data/ai_company.db` with the correct schema and row counts.
- Typical duration: **~4 minutes** for the full 117k-row backfill.
- Progress is logged to stdout; no additional verification steps are needed if the command completes without error.

### Post-rebuild verification

```powershell
# 1. Confirm the DB file exists and has reasonable size
ls -la data/ai_company.db

# 2. Run the cost-tracker guard
python scripts/test/check-cost-tracker.py
# Must exit 0

# 3. Start the dashboard and verify health
uv run ai-company dashboard --port 8421
# curl -s http://localhost:8421/health
```

---

## Guard Bypass Conditions

The cost-tracker guard is the gate between a safe state and a dummy/spent-data trap. A guard bypass is only authorized when all three conditions below are met.

### Guard: `python scripts/test/check-cost-tracker.py`

| Exit code | Meaning | Action |
|-----------|---------|--------|
| **0** | **Safe** — totals match, `by_source` tag present, line-count completeness OK | Proceed; no bypass needed. |
| **1** | **Fail** — dummy/untagged spend or truncated export | **Do not merge.** Investigate the root cause before proceeding. |

### Guard bypass conditions (all must hold)

1. **Zero-state confirmation** — The `cost_tracker.json` is in zero state (`call_count=0`, all totals 0, no breakdowns). This is the only state where a bypass is automatically approved, since no real spend is involved.

2. **Explicit CTO sign-off** — If the guard fails due to a known, intentional data update (e.g. a planned cost export sync), the CTO must approve the bypass in writing (Slack or email) and the override must be recorded in the change log.

3. **No untagged non-zero blocks** — The `by_source` field must be a non-empty dict. If `by_source` is missing or empty, the guard **must not** pass, regardless of other conditions.

### Emergency bypass procedure (rare)

If the guard exits 1 and you are certain the data is valid (e.g. you just ran `sync-opencode` and the log file is present):

```powershell
# Re-run the guard with explicit log path
python scripts/test/check-cost-tracker.py --log-path results/cost_log.jsonl

# If still failing, escalate to CTO — do not commit without approval.
```

### CEO-relevant notes (always keep in mind)

- **Never commit `data/ai_company.db`**. It is intentionally gitignored to prevent it from being tracked in history. The `.gitignore` explicit entries (`data/ai_company.db`, `data/ai_company.db-*`) ensure it stays ignored even after `git reset --hard`.
- **Shadow costs are in JSON only, not the SQLite column yet**. The `total_shadow_cost_usd` field in `data/orchestrator/cost_tracker.json` tracks shadow spend separately; the SQLite `data/ai_company.db` column for shadow costs has not been implemented yet. Do not attempt to sync shadow costs into the DB until the corresponding ETL pipeline is built.
- The `data/ai_company.db` mirror is a **local dev convenience only**. Production dashboards read from `ai-company/data/ai_company.db` (the canonical warehouse), not the parent-root `data/ai_company.db`.
