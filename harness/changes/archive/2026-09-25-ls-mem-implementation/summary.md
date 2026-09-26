---
title: "LS-MEM Implementation"
slug: "ls-mem-implementation"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "accepted"
spec_review: "approved"
plan_review: "approved"
modules:
  - ai_company.lsmem
files:
  - src/ai_company/lsmem/__init__.py
  - src/ai_company/lsmem/engine.py
  - src/ai_company/lsmem/classification.py
  - src/ai_company/lsmem/redaction.py
  - src/ai_company/lsmem/gateway.py
  - src/ai_company/lsmem/audit.py
  - src/ai_company/lsmem/injector.py
  - src/ai_company/lsmem/scoring.py
  - src/ai_company/lsmem/bridge.py
  - src/ai_company/lsmem/vector.py
  - src/ai_company/lsmem/cli.py
  - src/ai_company/executor/loop.py
  - tests/memory/test_integration.py
  - tests/memory/test_offline.py
  - tests/memory/test_ollama_optional.py
  - tests/memory/test_engine_crud.py
  - tests/memory/test_redaction.py
  - tests/memory/test_git_safety.py
  - tests/memory/test_dual_path_hash.py
tags: ["lsmem", "memory", "implementation", "sqlite", "fts5", "gateway", "audit", "security"]
validation_status: "pass"
created_at: "2026-09-25"
updated_at: "2026-09-25"
session_id: "0ef66804-66ce-4568-ac4f-2841f9d012f7"
owner_agent: "jmlus"
claimed_at: "2026-09-25"
---

# LS-MEM — Implementation

> Retrospective ECL record. The engine implementation and the 4-reviewer
> consensus remediation were executed without an active change; this archive
> was created 2026-09-25 to close the process gap (reviewer blocker 7 of 7).

## Goal

Implement the LS-MEM core system per handoff §34 (steps 5–16, 18) and the
Phase 3 data model: SQLite+FTS5 memory engine, classification/redaction,
permission gateway, hash-chained audit, context injection, one-way JSON
import bridge, optional Ollama vector search, CLI, executor wiring, dual
skill paths, and the test suite — then remediate all 7 "FIX FIRST" blockers
from the 4-reviewer consensus (CoS, CTO, memory-owner, qa-lead).

## Context / Current State

- Phase 0–3 complete (Phase 3 archive: `2026-09-25-ls-mem-phase-3-data-model`).
- ADR-025: JSON `MemoryStore` retained; one-way import bridge only.
- CEO-locked decisions: dual skill paths hash-identical; network
  deny-by-default; Restricted never plaintext; uncertain → BLOCK;
  `[REDACTED_SECRET]` canonical; Ollama optional; storage
  `.lightspeed/memory/` gitignored.
- Reviewer consensus (round 2): 6/10, 6/10, 6/10, 4.2/10 NO-GO with 7
  blockers — several reviewer claims were stale/wrong (skill dirs,
  `vector.py`, threat model, executor wiring all verified fine on disk).

## Outcome

### Modules (src/ai_company/lsmem/, 11 files)

| Module | Responsibility |
|--------|----------------|
| `engine.py` | SQLite+FTS5 schema, CRUD, search (incl. match-all branch), soft-delete `forget`/`purge`/`restore`, `rebuild_fts`, integrity, audit hooks |
| `classification.py` | 5-tier classification (`Tier`), data-classification rules |
| `redaction.py` | Secret detection + `[REDACTED_SECRET]` canonical redaction |
| `gateway.py` | Permission gateway: 5-gate evaluation, deny-by-default, human-approval tokens |
| `audit.py` | Hash-chained audit log, `verify_chain()`, JSONL export |
| `injector.py` | Session context injection, quota-bounded payload, `format_injection()` |
| `scoring.py` | Confidence/recency scoring, `compute_injection_quota()` (tier3=7, tier2=5, tier1=2, max 15) |
| `bridge.py` | One-way JSON MemoryStore → SQLite import + FTS rebuild + restricted upgrades |
| `vector.py` | Ollama optional local embeddings; deterministic FTS first, never cloud fallback |
| `cli.py` | 15 Typer commands (`remember/search/get/forget/purge/restore/pin/verify/status/lifecycle/rebuild_fts/export/integrity/audit/permission`) |
| `__init__.py` | Package surface |

### Integration & tests

- Executor wiring verified: `src/ai_company/executor/loop.py` (`create_injector`,
  `inject_context`, injection fallback paths).
- Dual skill paths present and hash-identical
  (`.agents/skills/ls-memory/SKILL.md` = `.opencode/skills/ls-memory/SKILL.md`;
  report: `tests/memory/dual_path_hash_report.txt`).
- Test suite `tests/memory/` (7 files): gateway 5-gate, audit
  `verify_chain` tamper detection, bridge import, injector quotas, CLI
  end-to-end lifecycle, offline isolation (13 tests), Ollama-optional,
  redaction, git safety, dual-path hash, engine CRUD.

### Reviewer-consensus remediation (7/7 blockers)

1. mypy semantic fixes: 38 → **0 errors** across the 11 lsmem source files.
2. Executor wiring: verified (loop.py) — reviewer claim was stale.
3. Integration tests: written (gateway/audit/bridge/injector/CLI).
4. `vector.py` + `test_ollama_optional.py`: present — reviewer claim stale.
5. `test_offline.py`: 13 offline/deny-by-default tests.
6. Threat model: Approved (CEO/security sign-off 2026-09-24) — claim stale.
7. ECL archives: this change + Phase 3 data-model archive (process gap closed).

### Bug fixes found during remediation

- `engine.search()` match-all branch: `query.strip() in ("", "*")` bypassed
  FTS5 so empty/`*` queries returned nothing.
- `bridge.py`: tokenizer `remove_diacritics` FTS5 parse-error fix;
  `restricted_upgraded` count fix; `_rebuild_fts()` after import.
- `cli.py`: 37 `typer.Option(value, flags)` calls converted to Typer 0.27
  Annotated-correct `Option(flags) = value` form (first positional was being
  consumed as an option flag → `TypeError: Name ... defined twice`).

## Decisions

1. Retrospective ECL records created rather than silently skipping the
   process gap (reviewer blocker 7).
2. Soft-delete semantics: `forget` sets `status=ARCHIVED` (row retrievable by
   ID for restore; excluded from search) — `get` exits 0 showing ARCHIVED.
3. Gateway all-pass behavior: `allowed=False, requires_human_approval=True`
   (human approval is always the top gate).
4. Known gaps recorded as follow-ups, not silently dropped (see Handoff).

## Validation

- `uv run ruff check src/ai_company/lsmem/`: clean.
- `uv run mypy src/ai_company/lsmem/`: `Success: no issues found in 11 source files`.
- `uv run python -X utf8 -m pytest tests/memory/ -q`: **93 passed, 1 skipped**.
- `pwsh scripts/lint-ecl.ps1`: pass.

## Validation Results

| Gate | Result |
|------|--------|
| mypy (11 lsmem files, 0 errors) | pass |
| ruff (src/ai_company/lsmem/) | pass |
| pytest tests/memory/ (93 passed, 1 skipped) | pass |
| CLI end-to-end lifecycle (remember→search→get→forget→status) | pass |
| Audit verify_chain tamper detection | pass |
| Gateway 5-gate + human approval | pass |
| Offline / network deny-by-default (13 tests) | pass |
| Ollama optional (skip-when-absent) | pass |
| Dual skill paths hash-identical | pass |
| lint-ecl.ps1 (docs/harness) | pass |

## Handoff Notes / Audit Trail

- Retrospective record created 2026-09-25; work executed across 2026-09-24/25.
- **Known follow-ups (deliberately out of scope):**
  - lsmem CLI is not registered in `src/ai_company/cli/main.py`
    (`memory` subcommand still maps to the legacy `ai_company.cli.memory`).
  - Audit chain has no persisted head — tampering the *last* event is
    undetectable (anchoring is prev_hash only).
  - All LS-MEM deliverables are **untracked in git**; commit awaits explicit
    user instruction.
- Pre-existing unrelated test failures (dashboard/websocket/daemon/perf) are
  excluded via `--ignore`; not caused by this change.
- Do not hand-edit `harness/changes/INDEX.json` — reindex only.
