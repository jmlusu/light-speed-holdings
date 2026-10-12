# Spec

## Intake Review

- Intake type: Small Change
- Input shape: plan-first
- Questions asked this round: 2 (ECL handling, version pin) — answered by user 2026-10-12

## Goal And Evidence

- Real problem or user request: Issue #156 — `httpx` project is unmaintained; migrate to the Pydantic-maintained fork `httpx2` (https://github.com/pydantic/httpx2).
- Current behavior: `httpx<0.29.0` direct dep in `pyproject.toml:24`; 10 src files / 12 import sites; 10 test files; starlette 1.6.0 emits `StarletteDeprecationWarning` (httpx fallback deprecated, removed in next starlette major).
- Source of evidence: repo greps (src/tests/docs), `uv.lock`, PyPI `httpx2` 2.13.1 metadata, issue #156 checklist.

## User Scenarios And Success

- Primary user/system scenario: all LLM provider calls, doctor checks, model router, publishing HTTP calls, and dashboard TestClient traffic run on `httpx2` with unchanged behavior.
- Success criteria: zero direct `httpx` imports in `src/` and `tests/`; `pytest -m "not e2e"` green; no `StarletteDeprecationWarning` in test output.
- Acceptance criteria: ruff + mypy pass; full non-e2e suite passes; issue #156 checklist items addressed (including documented transitive-httpx expectation).

## Non-Goals

- Removing `httpx` from `uv.lock` entirely (impossible: `huggingface-hub` 1.26.1 runtime + `safety` 3.7.0 dev still require it).
- Renaming historical docs (SPRINT/PHASE3/CODE_REVIEW/diagrams) that mention httpx as history.
- Upgrading/downgrading FastAPI or starlette.

## Constraints

- Alias style: `import httpx2 as httpx` everywhere — keeps annotations, exception uses, and conftest module-path patches (`...openai_compatible.httpx.Client`) working with minimal diff.
- Literal string patch targets (`"httpx.get"`) must become `"httpx2.get"` (mock resolves the literal module name).
- `Dockerfile` healthcheck uses curl — no change; stale `docs/DEPLOYMENT-GUIDE.md:148,207` httpx examples updated to httpx2.

## Assumptions

- httpx2 2.13.1 API is source-compatible with httpx 0.28.1 for the surface used (`Client`, `AsyncClient`, `get`, `ConnectError`, `HTTPError`, `MockTransport`, `.stream`).
- Starlette 1.6.0 auto-switches TestClient to httpx2 once installed.

## Open Questions

- None.

## Resolved Clarifications

- ECL handling (2026-10-12): close previous merge-conflict change first (done — archived as `2026-10-12-resolve-merge-conflicts-main-branch-build`), then start this change.
- Version pin (2026-10-12): `httpx2>=2.12` (floor at issue baseline, uv picks current 2.13.1).
