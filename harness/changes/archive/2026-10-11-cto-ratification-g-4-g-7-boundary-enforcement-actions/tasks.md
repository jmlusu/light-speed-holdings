# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation. (Intake complete: requirement-first, 0 open questions.)

## Implementation

- [x] T002 [P] G-4: `ecosystem.config.cjs` → portable `script: "node_modules/vite/bin/vite.js"` + `cwd: __dirname`; keep `port`/`args`/`env`; metadata comment. Validate: `node -e "require('./ecosystem.config.cjs')"` prints both apps with ports 1441/1440. **Evidence: exit 0, vite-dev port=1441 / vite-preview port=1440, scriptExists=true both.**
- [x] T003 [P] G-5a: create `scripts/dev/verify-port-bindings.ps1` (per-port owner mapping + §5 contract probes, exit 0/1/2). Validate: script runs on host end-to-end. **Evidence: ran on host, all four ports unbound → exit 0.**
- [x] T004 [P] G-5b: remove unused `$ProjectRoot` from `scripts/dev/health-check.ps1:4`. Validate: `Select-String ProjectRoot scripts/dev/health-check.ps1` → no match; script still parses. **Evidence: 0 occurrences; parses clean; executed end-to-end (poll → expected exit-1 path with servers down). Found+fixed pre-existing syntax defect: missing paren in `while` condition (present at HEAD) blocked parsing since origin; 1-char fix disclosed in summary Decisions.**
- [x] T005 [P] G-6a: create `scripts/test/check-site-ports.py` (stdlib parity check: vite.config.ts ↔ ecosystem.config.cjs). Validate: exit 0 on clean tree; forced-mismatch temp copy exits 1. **Evidence: clean exit 0; forced mismatch printed `::error::vite.config.ts: server.port = 9999, expected 1441` → exit 1.**
- [x] T006 [P] G-6b: add port-assertion step to `.github/workflows/site-principles-gate.yml`. Validate: YAML parses, step runs `check-site-ports.py`. **Evidence: `yaml.safe_load` → ok; step reads `python3 scripts/test/check-site-ports.py`; gate has no path filter so it runs on every PR.**
- [x] T007 [P] G-7: add "Production residual risk" note to `docs/organization/app-naming-and-port-assignments.md` §5 + revision-history row. Validate: doc renders as Markdown, note states Vercel-443 vs 8420 prod separation. **Evidence: §5 subsection + v1.1 revision row added; states Vercel :443 vs Docker 8420 structural separation.**
- [x] T011 [US-user] User-directed scope addition: fix known org-health datetime comparison error from dashboard logs (`TypeError: can't compare offset-naive and offset-aware datetimes` at `scorers.py:92` via `_score_task_throughput` fail-open). Fix: `_to_utc()` normalisation (naive → UTC) in `src/ai_company/dashboard/scorers.py` + regression tests. Validate: `uv run pytest tests/unit/test_scorers.py tests/unit/test_org_health_reliability.py -q` → 14 passed; `ruff` + `mypy` clean. Related latent issue NOT fixed (recorded as finding): `api.py:372` same pattern, TypeError swallowed by `except (ValueError, TypeError)`.

## Validation

- [x] T008 `uv run pytest tests/unit/test_port_assignments.py -q` → all green (G-1/G-2 parity after edits). **Evidence: 7 passed in 2.69s (G-4 edit did not break G-1 port metadata assertions).**
- [x] T009 `python scripts/test/check-site-ports.py` → exit 0; `pwsh scripts/dev/verify-port-bindings.ps1` → completes with defined exit code. **Evidence: checker exit 0; port audit exit 0 (all ports unbound).**
- [x] T010 `pwsh scripts/maintenance/lint-ecl.ps1` → PASS; `git status --porcelain` shows no changes outside this change's file list (concurrent-session files untouched). **Evidence: lint PASS (0 failures/0 warnings); dirty files outside the list all belong to the concurrent journey-events/analytics session (staged api.py, ci.yml, generator.py, etc.) — none read/written by this session.**

## Deferred Tasks

- None.
