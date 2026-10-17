# Plan

> Recorded retroactively on 2026-08-26. The plan was approved by the user in-session before execution; this documents it for handoff continuity.

## Technical Approach

1. Fix monitoring streak logic to judge default-branch consecutive failures instead of a last-5 window (commit `554aee2`).
2. Root-cause vulnerable-deps warning: stale `uv.lock` (fastapi 0.109.0 / starlette 0.35.1, Jan 2024) — constraints were already satisfiable.
3. Targeted lock refresh only: `uv lock --upgrade-package fastapi --upgrade-package starlette` → fastapi 0.141.1, starlette 1.6.0.
4. Full local verification, then commit lockfile-only change (`86a12e9`), push, watch CI, dispatch monitoring workflow and assert clean Dependency Health log.
5. Deep-dive follow-ups: Dependabot PR #155 disposition + concurrent-session dirty files characterization.

## Impacted Modules And Files

- `.github/workflows/monitoring.yml` (streak logic)
- `uv.lock` (fastapi/starlette resolution)
- `pyproject.toml` (via merged PR #155: httpx ceiling `<0.29.0`)
- `docs/STATUS.md` (handoff update)

## Interfaces, Data, Permissions

- No API/model/permission changes. Runtime dependency versions only; dashboard test surface exercised via `fastapi.testclient` (starlette fallback path).

## Spec Gaps Found From Planning

- None blocking; httpx2 deprecation surfaced post-upgrade and was deliberately deferred to its own tracked issue.

## Risks And Mitigations

- Major-version jump breakage risk → mitigated by pre-upgrade grep (no direct starlette imports; stable test APIs) and full-suite run (1969 passed).
- Concurrent session interference → mitigated by surgical staging (`git add` of specific paths only); verified zero file overlap.

## Verification Plan

- `ruff check src/`, `mypy src/`, `pytest -q -m "not e2e"` locally.
- `uv audit --frozen` must exit 0.
- CI green on push; monitoring dispatch shows `[OK] No known vulnerabilities found` with no warning annotation.
