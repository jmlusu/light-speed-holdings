# Repository Health — Post-Sanitization (2026-10-06)

> Produced by Stage 8 of the 2026-10-06 repository sanitization
> (ECL change `2026-10-06-repository-sanitization`, LightSpeed Phased
> Approval & Rollback Protocol). BEFORE numbers come from `repo-audit/`
> (2026-10-06); AFTER numbers are measured on this tree.

## BEFORE → AFTER

| Metric | Before | After |
|--------|--------|-------|
| Tracked root files | ~107 | **32** (`git ls-tree HEAD`) |
| Top-level entries | 69 dirs + files | 76 entries (dirs consolidated, files fewer) |
| `scripts/` layout | 49 flat files, 6 languages | `dev/`, `build/`, `test/`, `deploy/`, `maintenance/`, `research/` + `scripts/health_check.py` |
| Retired skill corpus (tracked) | ~1,020 MB (scroll-craft 692 + scrollcraft 32 + lab 216 + case-study artifacts 79) | **0** (removed; history preserves) |
| Cache/tmp/build waste on disk | ~290 MB caches + 6.9 MB `dist/` + notebook strays | **0** (deleted; all gitignored) |
| In-repo backups | 85 MB (`backups/`) | **0** (output → `~/.lightspeed/backups`) |
| `git_ls_files.txt` / tracked logs / QA pngs | tracked | untracked + gitignored |
| Registry backups in `company/` | 3 hand-made `.bak` files | 0 (superseded deleted; hybrid archived to `docs/archive/`) |
| Package-manager lockfiles | 2 (`bun.lock` + `package-lock.json`) + guard script enforcing bun | 1 (`package-lock.json`); guard enforces npm |
| `open-design` gitlink | no `.gitmodules` (fresh clones broken) | declared submodule (`.gitmodules`, origin verified) |
| `.env.example` | personal path + 6 duplicate keys | clean template |
| Brand mirrors | 3 identical copies, undocumented sync state | `brand/` canonical; mirrors verified byte-identical by `sync-brand -Verify`; do-not-edit rule in `brand/CANONICAL_SOURCES.md` |
| `Branding landing page/` (superseded) | root dir, 52 files | `docs/archive/branding-landing-page/` |
| Cumulative diff vs `cleanup/c0-baseline` | — | 433 files, +2,796 / −20,771 |

## Validation (this tree)

- `ruff check src/` — **PASS**
- `mypy src/` — **PASS** (236 files, no issues)
- `pytest` — **PASS** with documented exclusions (see below)
- Generator round-trip (`AgentGenerator().generate_all()`) — **PASS**, no drift in `.opencode/agents/`, `company/*.yaml`
- `sync-registry --verify` — **PASS** (90 agents, YAML→JSON in sync)
- `pwsh scripts/maintenance/lint-ecl.ps1` — **PASS**
- Canonical gate: `uv run python scripts/health_check.py`

### Known pre-existing failures (not caused by this cleanup)

- `tests/test_scraper_inventory.py` — `company/athena/*.jsonl` absent (Athena archived; data files deleted in-flight by the owner — left untouched)
- `test_endpoint_response_time_p95[/api/v1/dashboard]` — perf flake (210 ms vs 200 ms budget, single slow first request)
- (Both excluded in `scripts/health_check.py` with reasons.)

## Improvements

1. Root is sparse and reviewable; every root file earns its place.
2. Scripts are discoverable by purpose; repo-root resolution repaired after the move (verified by `sync-brand -Verify`).
3. ~1.1 GB of tracked dead weight removed across 11 atomic commits, each independently revertable (`cleanup/c0-baseline` → `cleanup/c7-large-tools`).
4. Policy-as-code: backup output banished from the tree, bun/npm dispute resolved in favor of npm with an executable guard, submodule declared.
5. Governance docs match reality again (AGENTS.md §9.2 retirement claim is now true).

## Regressions

None known. Every stage validated with ruff + targeted pytest + generator round-trip before tagging its checkpoint.

## Known Limitations / Remaining Technical Debt

1. **Memory duality (Q4):** `src/ai_company/memory/` (legacy JSON store) is still imported by the executor, dashboard, MCP server, doctor, and CLI — `lsmem/` has NOT replaced it in code despite the LS-MEM completion record. Consolidation deferred; needs a human architecture decision. Do not delete either.
2. **Runtime-state relocation (D-6):** root `orchestrator/` + `memory/` still hold live state (approvals, vector index). Untracked junk (`.bak`, `.tmp`, `RUN2GENERATED`) is deletable anytime; relocating tracked/live paths needs code + config changes. Deferred.
3. **Milestones deck duality (Q3):** `generate-milestones-deck.py` runs on the installed toolchain (`python-pptx` present); the `.js` twin needs `pptxgenjs`, which is not installed. Neither is referenced anywhere. Awaiting owner pick.
4. **`tmp/` tracked scratch:** ~40 tracked files (`mut_backup/`, probe outputs, hash logs) look like another session's scaffolding. Left untouched; needs owner triage.
5. **`whitepaper/` outputs:** out of this cleanup's scope; revisit.
6. **Fresh-clone verification** of the open-design submodule pin is a Stage 9 item.
7. **Pre-existing working-tree changes untouched:** brand tokens, site content (`AboutSection`, `SectorsPage`, `WhatWeDoPage`, registries), `harness/changes/INDEX.json`, `orchestrator/approvals.yaml`, `hr/onboarding_requests.yaml`, `.archive/athena/` deletions — all belong to other in-flight work and were never staged here.
