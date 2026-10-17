# Plan

## Technical Approach

Complete LS-MEM per `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md` §34 steps 19–20 and §36 DoD, in six workstreams (A/B/C/E/F direct, D reserved). No executor or memory-engine behavior changes beyond the audit head; no `.opencode/tools/`; no global skill copy.

### WS-A — CLI dispatch repoint (decision 1)
- `src/ai_company/cli/main.py`: `_LAZY_SUB_APPS["memory"]` → `("ai_company.lsmem.cli", "app", ...)`; add `knowledge` → legacy `ai_company.cli.memory` app; keep the canonical 7-tool vocabulary untouched.
- `tests/unit/test_cli_commands.py`: `EXPECTED_SUB_APPS` gains `knowledge`; `test_knowledge_stats_runs`; `test_memory_status_lsmem_runs`.
- Docs rename legacy examples to `knowledge`: `README.md`, `docs/USER-GUIDE.md`, `docs/ux/CLI-DESIGN.md`, `docs/DECISION-FRAMEWORK.md`, `config/company/scheduler.yaml`; fix stale flags (`--type` → `--memory-type`, `--query` → positional).

### WS-B — Persisted audit chain head
- `src/ai_company/lsmem/audit.py`: `audit_meta` table; `_load_chain_head()` (meta row, fallback `rowid DESC`); `verify_chain()` walks rowid ASC and compares the final hash to the persisted head; `prune()` recomputes and persists the new head.
- `tests/memory/test_audit_chain_head.py`: 9 tamper-tail tests (missing head, stale head, appended/reordered/deleted events, rebuild after prune).

### WS-C — Operator documentation
- `docs/LS-MEM-USER-GUIDE.md`: §27 backup/restore/export/import/migrate/rebuild/corruption/uninstall, offline notes, skill-script surface.
- `docs/security/LS-MEM-SECURITY-VERIFICATION.md`: §33 20-question report, evidence with path:line, deviation note (decision 2), §6 audit output, §7 CEO/HITL items.

### WS-E — Independent security audit (ciso)
- Findings F-01…F-11 recorded in report §6; severity split 0 Critical / 0 High / 7 Medium / 4 Low, all documented or deferred; sign-off APPROVE-WITH-FINDINGS; citation corrections applied; zero source changes from audit itself.

### WS-F — Gates + stdio fix
- `_ensure_utf8_stdio()` in `src/ai_company/lsmem/cli.py` (reconfigure stdout/stderr to utf-8, errors=replace, tolerant of ValueError/OSError) + `tests/memory/test_cli_stdio.py` (3 tests) for cp1252 consoles.
- Gate of record: `ruff check`, `ruff format --check`, `mypy`, full `pytest`, CLI + skill-script smoke.

## Impacted Modules / Files

| File | Change | WS |
|------|--------|----|
| `src/ai_company/cli/main.py` | lazy-app mapping `memory`/`knowledge` | A |
| `src/ai_company/lsmem/audit.py` | persisted chain head | B |
| `src/ai_company/lsmem/cli.py` | utf-8 stdio guard | F |
| `tests/unit/test_cli_commands.py` | sub-app expectations | A |
| `tests/memory/test_audit_chain_head.py` | new | B |
| `tests/memory/test_cli_stdio.py` | new | F |
| `docs/LS-MEM-USER-GUIDE.md` | new | C |
| `docs/security/LS-MEM-SECURITY-VERIFICATION.md` | new | C/E |
| `README.md`, `docs/USER-GUIDE.md`, `docs/ux/CLI-DESIGN.md`, `docs/DECISION-FRAMEWORK.md`, `config/company/scheduler.yaml` | `knowledge` renames, flag fixes | A |
| `docs/STATUS.md` | close-out bullet | T009 |

## Interfaces

- `ai-company memory …` → LS-MEM Typer app (remember/search/get/forget/status; `remember` requires `--title`; `search` takes positional query).
- `ai-company knowledge …` → legacy JSON CLI (unchanged behavior; `add` uses `--memory-type`).
- Skill scripts `.agents/skills/ls-memory/scripts/memory-*` shell out to `ai-company memory`.
- `verify_chain() -> ChainVerificationResult` semantics unchanged for callers; now additionally head-checked.

## Spec Gaps

- None blocking: five intake clarifications resolved (recorded in `spec.md`); no `[NEEDS CLARIFICATION]` markers.

## Risks

- Concurrent homepage session writing to shared `harness/changes/active/` (mitigated: preserve-into-parking before restore; re-check mtimes before close).
- cp1252/legacy consoles (mitigated: utf-8 stdio guard + tests).
- Chain head absent on existing databases (mitigated: lazy fallback to last event row).

## Verification Plan

- Gates: `uv run ruff check src/`, `uv run ruff format --check`, `uv run mypy src/`, `uv run pytest -q`.
- Targeted: `tests/unit/test_cli_commands.py`, `tests/memory` (105 expected).
- Smoke: temp-dir CLI lifecycle + skill-script forwarding; `pwsh scripts/lint-ecl.ps1` before and after close.
