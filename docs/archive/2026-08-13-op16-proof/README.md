# OP-16 Operating Proof — Evidence Archive (2026-08-13/14)

Gate outcome recorded 2026-08-14: **PASS with minor fix-list** — see issue #16
(closed) and `docs/OP-16-OPERATING-PROOF-RUNBOOK.md`.

## Run summary

| | |
|---|---|
| Proof issue | #16 (Run the one-day operating proof) |
| Gate outcome | PASS with minor fix-list (#54), #16 closed 2026-08-14 |
| Cadence gate unblocked | #17 (Define the sustained operating cadence) |
| Executor run | PID 27624, 10 ticks, graceful stop (`state: stopped`) |
| Tasks | 4/4 completed (canary-001, t1-status-summary, t2-board-audit, t3-audit-analysis); no DLQ entries |
| Spend | `results/cost_log.jsonl` — t1 $0.0314, canary $0.00143, t2/t3 $0.00 (ollama `llama3.1:8b`) |
| Root causes found | Shell-metacharacter rejection (#70, fixed); naive-vs-UTC evidence drift (#55, fixed); decoy `.opencode/audit.jsonl` readers (#71, fixed) |

## Evidence inventory

Copied artifacts (SHA256 prefixes, sizes):

| File | SHA256 (16) | Size |
|------|-------------|------|
| `results/canary-001-loop_result.json` | `683ACF2B4827E977` | 283 B |
| `results/t1-status-summary-loop_result.json` | `EF85B9F06B869445` | 2714 B |
| `results/t2-board-audit-loop_result.json` | `474DD2EDBB221DA8` | 2613 B |
| `results/t3-audit-analysis-loop_result.json` | `1D37BC8F5DC5FE80` | 3370 B |
| `results/cost_log.jsonl` | `864355AB4BF8F1CC` | 18202 B |
| `executor-daemon.json` (final state) | `5DCDB3669295EB31` | 227 B |
| `daily_briefing.md` | `D87ED6D668224CAC` | 130 B |
| `dead_letter.json` | `4F53CDA18C2BAA0C` | 2 B (`[]`) |

Referenced (gitignored, NOT copied — raw operational artifacts):

| Artifact | Path | Size |
|----------|------|------|
| Canonical audit trail | `.opencode/audit` | ~3.4 MB |
| Executor daemon log | `logs/executor-daemon.log` | ~0.9 MB |
| Live inbox | `.opencode/inbox.json` (4 completed tasks) | — |
| KPI snapshots (SQLite) | `data/ai_company.db` (46 entries, 7 departments) | — |

## Caveats

- `loop_result.json` timestamps and inbox `created_at`/`completed_at` for this
  batch are **naive local** — they predate the #55 fix. `cost_log.jsonl` and
  the audit trail were already UTC. New records are UTC-aware.
- t1–t3 all ended with tool-error/plan-request final responses (see runbook
  review). Their two root causes are fixed since (#70, #55).
- `results/results/` at the repo root holds leftover analysis scripts
  (`analyze_costs.py`, `generate_report.py`, etc.) — flagged for cleanup
  (ticket #67 territory).
