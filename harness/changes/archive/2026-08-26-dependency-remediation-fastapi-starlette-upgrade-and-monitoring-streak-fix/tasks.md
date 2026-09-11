# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Triage failing Monitoring & Alerts run `32452147706`-era failure; identify Dashboard Health Check root cause.

## Implementation

- [x] T002 Fix monitoring streak logic (default-branch consecutive failures vs last-5 window) — commit `554aee2`.
- [x] T003 Close stale alert issue #137 after green verification run `32558034171`.
- [x] T004 Refresh `uv.lock`: fastapi 0.109.0→0.141.1, starlette 0.35.1→1.6.0 via targeted upgrade — commit `86a12e9`.
- [x] T005 Merge Dependabot PR #155 (httpx `<0.29.0`) as squash `44b3d85`; sync local main.

## Validation

- [x] T006 Local gates: ruff clean; mypy strict clean (191 files); pytest `-m "not e2e"` 1969 passed; `uv audit --frozen` exit 0.
- [x] T007 Remote gates: CI run `32565696546` success; monitoring run `32652708435` all jobs green, Dependency Health logs `[OK] No known vulnerabilities found`.
- [x] T008 Retroactive ECL record created; STATUS.md updated; lint-ecl.ps1 pass.

## Deferred Tasks

- httpx2 migration — tracked as GitHub issue (opened 2026-08-26): replace unmaintained httpx with Pydantic-maintained httpx2 in 4 src files (`llm/providers/llamacpp.py`, `llm/providers/ollama.py`, `llm/providers/openai_compatible.py`, `llm/oauth2.py`), 2 test files, and drop the `<0.29.0` pin; clears starlette TestClient deprecation before starlette's next major removes the fallback.
