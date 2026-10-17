---
title: "CTO ratification G-4..G-7 boundary enforcement actions"
slug: "cto-ratification-g-4-g-7-boundary-enforcement-actions"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "approved"
spec_review: "approved"
plan_review: "approved"
modules: ["scripts/dev", "scripts/test", "docs/organization", "src/ai_company/dashboard"]
files: ["ecosystem.config.cjs", "scripts/dev/verify-port-bindings.ps1", "scripts/dev/health-check.ps1", "scripts/test/check-site-ports.py", ".github/workflows/site-principles-gate.yml", "docs/organization/app-naming-and-port-assignments.md", "src/ai_company/dashboard/scorers.py", "tests/unit/test_scorers.py"]
tags: ["ports", "boundary", "cto-ratification", "pm2", "ci-gate", "org-health"]
validation_status: "pass"
created_at: "2026-10-11"
updated_at: "2026-10-11"
session_id: "286fe445-dde0-46e6-b5c8-24ce3c3423e4"
owner_agent: "jmlus"
claimed_at: "2026-10-11"
---

# Summary

## Outcome

Implement the four remaining CTO-ratification §7 actions (G-4 PM2 portability, G-5 port-binding identity audit, G-6 frontend-only CI port guard, G-7 prod residual-risk note) as one change. G-1..G-3 already shipped (`c79823a0`, archived `2026-10-10-p0-boundary-guards-g-1-g-2-g-3`).

## Decisions

- G-4 keeps PM2 `port:` metadata (G-1 test asserts 1441/1440); only `script:`/`cwd:` become portable.
- G-5 ships as a local PowerShell audit with the §5 contract probes (HTML on 1440/1441, JSON `status` on 8420/8421); non-Windows exits 2.
- G-6 uses `scripts/test/check-site-ports.py` (stdlib, no Python deps) wired into the bun-based site gate, mirroring the existing `check-site-form-backend.py` step; pytest G-1 remains the Python-side surface.
- G-7 documents that prod (Vercel :443 vs Docker 8420) makes cross-serving structurally impossible; the checklist governs local/dev/staging.
- A1–A7 harness-evolution items are a separate track (task named A4–A7 only); A1–A3 left untouched.
- **Scope addition (user-directed, T011):** mid-change the user cited a known org-health datetime error in the logs. Root cause: `scorers.py score_task_throughput` mixes offset-naive/offset-aware datetimes from `fromisoformat` → `TypeError` at `min(timestamps)`, surfaced as org-health `task_throughput` fail-open. Fixed via `_to_utc()` normalisation (naive treated as UTC, matching write convention) + 4 regression tests. Out-of-scope finding left unfixed: `api.py:372` has the same naive/aware subtraction pattern but its TypeError is swallowed by an existing `except`.
- **Pre-existing defect fixed during T004 validation:** `scripts/dev/health-check.ps1` `while` condition was missing an opening paren (present at HEAD) so the script never parsed under PowerShell; 1-char fix required by T004's "script still parses" criterion.

## Validation

- T008: `pytest tests/unit/test_port_assignments.py -q` → **7 passed** (G-1/G-2 parity intact after G-4).
- T009: `check-site-ports.py` exit 0 on clean tree, exit 1 on forced mismatch; `verify-port-bindings.ps1` exit 0 on host (all four ports unbound).
- T009b (T011): `pytest tests/unit/test_scorers.py tests/unit/test_org_health_reliability.py -q` → **14 passed**; `ruff`/`mypy` clean on touched sources.
- G-4: `node -e "require('./ecosystem.config.cjs')"` → vite-dev 1441 / vite-preview 1440, `scriptExists=true` both.
- G-5b: `health-check.ps1` parses clean and executes end-to-end (60s poll → expected failure branch with servers down); PM2 daemon spawned by diagnostic `pm2 status` removed afterwards (zero apps), ports left unbound.
- G-6b: workflow YAML `safe_load` ok; step wired and runs on every PR (no path filter).
- T010: `lint-ecl.ps1` → **PASS** (0 failures / 0 warnings); dirty files outside the listed set all belong to the concurrent journey-events/analytics session, untouched by this session.

## Next Step

- Close via `harness-change.ps1 close completed` (phase validate + validation_status pass), update `docs/STATUS.md`, then run the A4–A7 harness-evolution track.
