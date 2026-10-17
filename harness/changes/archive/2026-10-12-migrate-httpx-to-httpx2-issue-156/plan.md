# Plan

## Technical Approach

Alias-migration: swap `import httpx` -> `import httpx2 as httpx` in every source and test file; retarget literal mock strings `"httpx.get"` -> `"httpx2.get"`; swap the direct dependency pin; keep `httpx` in the lock only as a transitive of huggingface-hub/safety (documented, expected).

## Impacted Modules And Files

- `pyproject.toml:24` — remove `"httpx<0.29.0"`, add `"httpx2>=2.12"`
- `.pre-commit-config.yaml` (~line 44) — mypy hook `additional_dependencies`: httpx -> httpx2
- src (10 files): `llm/providers/{llamacpp,ollama,openai_compatible}.py`, `llm/oauth2.py`, `llm/client.py:181`, `model_router.py:26`, `executor/agent_loop.py:76`, `publishing/publishers.py:121,155`, `cli/main.py:419`, `doctor/checks.py:128,288,335` (128 = required-package list -> `httpx2`)
- tests: `tests/unit/conftest.py:66,71`, `tests/unit/test_doctor.py:41,51,295`, `tests/unit/test_omniroute_integration.py:29,726,767,779,794`, `tests/unit/test_llm.py`, `tests/unit/test_oauth2.py:14`, `tests/test_llm_streaming.py:9`
- docs: `docs/ARCHITECTURE.md:242`, `.ai-company/constitution/02-ARCHITECTURE.md:549`, `docs/DEPLOYMENT-GUIDE.md:148,207`

## Interfaces, Data, Permissions

- No API/behavioral change; public HTTP surface of providers unchanged.
- conftest `patch_local_only_httpx`: line 71 string target -> `"httpx2.get"`; lines 103-104 module-path targets unchanged (alias keeps attribute name `httpx`).

## Spec Gaps Found From Planning

- Issue #156 exposure table stale (4 src/2 test files); actual 10 src / 10 test — recorded in spec.
- Issue checklist "verify no transitive dep still requires httpx" resolves to: huggingface-hub + safety keep it in lock; document, do not fail.

## Risks And Mitigations

- Exception-class mismatch (real `httpx.ConnectError` raised where code catches `httpx2.HTTPError`): mitigated by aliasing in every test that raises/catches exceptions, plus full suite run.
- mock.patch target misses: only literal `"httpx.*"` strings break; enumerated all 6 sites via grep before editing.
- Version drift: uv.lock pins resolved version; floor `>=2.12`.

## Verification Plan

1. `uv run ruff check src/ tests/`
2. `uv run mypy src/`
3. `uv run pytest -m "not e2e"` (full suite, must complete green)
4. `uv audit --frozen` (confirm exact subcommand at run time)
5. Grep pytest output for `StarletteDeprecationWarning` -> zero occurrences (baseline run 2026-10-12 had 1)
6. `uv run python -c "import httpx2; from httpx2 import MockTransport, AsyncClient"`
7. `pwsh scripts/maintenance/lint-ecl.ps1`
8. Regenerate agents if generator/template touched (not expected)
