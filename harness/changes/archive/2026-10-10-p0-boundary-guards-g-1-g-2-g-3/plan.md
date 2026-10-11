# Plan

## Technical Approach

1. **G-3** — Add a small inline Vite plugin in `vite.config.ts` that uses `configResolved` to assert the resolved `server.port` / `preview.port` are not 8420/8421, throwing with a message naming the CEO Dashboard.
2. **G-2** — In `src/ai_company/cli/dashboard.py`, after the ADR-012 guard, refuse `--port 1440` / `--port 1441` with a message naming the Marketing Site, `raise typer.Exit(1)`.
3. **G-1** — New `tests/unit/test_port_assignments.py`:
   - Parse `vite.config.ts` for `server.port == 1441`, `preview.port == 1440`.
   - Parse `ecosystem.config.cjs` for `vite-dev → 1441`, `vite-preview → 1440`.
   - Parse `src/ai_company/cli/dashboard.py` (or invoke Typer callback default) for dashboard default `== 8420`.
   - Parse `docker-compose.yml` for `8420:8420`; `docker-compose.staging.yml` for staging default `8421`.
   - Assert `dashboard_ports ∩ vite_ports == ∅`.

## Impacted Modules And Files

- `vite.config.ts` (G-3)
- `src/ai_company/cli/dashboard.py` (G-2)
- `tests/unit/test_port_assignments.py` (G-1, new)

## Interfaces, Data, Permissions

- No data or permission changes. Runtime behavior only: both applications refuse the other's ports at startup.

## Spec Gaps Found From Planning

- None.

## Risks And Mitigations

- Regex-based static parsing of TS/CJS/YAML can break on refactor → keep patterns minimal (port number + nearby key); CI gate is the signal.
- Vite plugin runs only when Vite loads config → `vite --port 8420` still caught via `configResolved` (CLI override is in resolved config).

## Verification Plan

- `uv run pytest tests/unit/test_port_assignments.py`
- `uv run ruff check src/ && uv run mypy src/ && uv run pytest`
- `pwsh scripts/maintenance/lint-ecl.ps1`
