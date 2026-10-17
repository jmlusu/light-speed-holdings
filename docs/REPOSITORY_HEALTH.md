# Repository Health — Post-Sanitization (2026-10-06, refreshed 2026-10-07)

> Produced by Stage 8 of the 2026-10-06 repository sanitization
> (ECL change `2026-10-06-repository-sanitization`, LightSpeed Phased
> Approval & Rollback Protocol). BEFORE numbers come from `repo-audit/`
> (2026-10-06); AFTER numbers are measured on this tree. Refreshed
> 2026-10-07: residue sweep + live-runtime-state untracking; AFTER
> numbers re-measured.

## BEFORE → AFTER

| Metric | Before | After |
|--------|--------|-------|
| Tracked root files | ~107 | **32** (`git ls-tree HEAD`) |
| Top-level entries | 69 dirs + files | 74 entries (41 dirs + 32 files + 1 submodule, re-counted 2026-10-07) |
| `scripts/` layout | 49 flat files, 6 languages | `dev/`, `build/`, `test/`, `deploy/`, `maintenance/`, `research/` + `scripts/health_check.py` |
| Retired skill corpus (tracked) | ~1,020 MB (scroll-craft 692 + scrollcraft 32 + lab 216 + case-study artifacts 79) | **0** (removed; history preserves) |
| Cache/tmp/build waste on disk | ~290 MB caches + 6.9 MB `dist/` + notebook strays | **0** after 2026-10-07 re-sweep (56 `__pycache__`, 110 MB `.mypy_cache`, 2,012 `.bak` ≈ 137 MB removed; caches regrow during dev — all gitignored) |
| In-repo backups | 85 MB (`backups/`) | **0** (output → `~/.lightspeed/backups`) |
| `git_ls_files.txt` / tracked logs / QA pngs | tracked | untracked + gitignored |
| Registry backups in `company/` | 3 hand-made `.bak` files | 0 (superseded deleted; hybrid copy swept from `docs/archive/` 2026-10-07, no references) |
| Package-manager lockfiles | 2 (`bun.lock` + `package-lock.json`) + guard script enforcing bun | 1 (`package-lock.json`); guard enforces npm |
| `open-design` gitlink | no `.gitmodules` (fresh clones broken) | declared submodule (`.gitmodules`, origin verified) |
| `.env.example` | personal path + 6 duplicate keys | clean template |
| Brand mirrors | 3 identical copies, undocumented sync state | `brand/` canonical; mirrors verified byte-identical by `sync-brand -Verify`; do-not-edit rule in `brand/CANONICAL_SOURCES.md` |
| `Branding landing page/` (superseded) | root dir, 52 files | `docs/archive/branding-landing-page/` |
| Cumulative diff vs `cleanup/c0-baseline` | — | 745 files, +5,955 / −71,142 (measured at `552c6cb8`, 2026-10-07; excludes this doc's update) |

## Validation (this tree)

All gates re-run 2026-10-07 — **PASS** (`scripts/health_check.py` + `sync-registry --verify`):

- `ruff check src/` — **PASS**
- `mypy src/` — **PASS** (236 files, no issues)
- `pytest` — **PASS** with documented exclusions (see below)
- Generator round-trip (`AgentGenerator().generate_all()`) — **PASS**, no drift in `.opencode/agents/`, `company/*.yaml`
- `sync-registry --verify` — **PASS** (90 agents, YAML→JSON in sync)
- `pwsh scripts/maintenance/lint-ecl.ps1` — **PASS**
- Canonical gate: `uv run python scripts/health_check.py`

### Known pre-existing failures (not caused by this cleanup)

- `tests/test_scraper_inventory.py` — **RESOLVED 2026-10-07**: module removed. The Athena archive (`d2fa83aa`) deleted `company/athena/*.jsonl` and the Athena unit tests but missed this one, leaving the required CI Test jobs red; `scripts/health_check.py` exclusions for it dropped in the same change.
- `test_endpoint_response_time_p95[/api/v1/dashboard]` — perf flake (210 ms vs 200 ms budget, single slow first request); still excluded in `scripts/health_check.py`.

## Improvements

1. Root is sparse and reviewable; every root file earns its place.
2. Scripts are discoverable by purpose; repo-root resolution repaired after the move (verified by `sync-brand -Verify`).
3. ~1.1 GB of tracked dead weight removed across 11 atomic commits, each independently revertable (`cleanup/c0-baseline` → `cleanup/c7-large-tools`).
4. Policy-as-code: backup output banished from the tree, bun/npm dispute resolved in favor of npm with an executable guard, submodule declared.
5. Governance docs match reality again (AGENTS.md §9.2 retirement claim is now true).
6. Refresh (2026-10-07): regenerated residue swept (~130 MB caches + 6.8 MB dated backups, 2,012 files); live runtime state (`orchestrator/approvals.yaml`, `memory/memory-index.yaml`) untracked — restored to HEAD first (dropped +411 pytest `hitl-*` scaffold lines), files remain on disk as working state; README's stale LS-MEM `memory remember` row fixed.

## Regressions

None known. Every stage validated with ruff + targeted pytest + generator round-trip before tagging its checkpoint.

## Known Limitations / Remaining Technical Debt

1. **Memory duality (Q4):** **RESOLVED 2026-10-07** — LS-MEM decommissioned in `42284c54` (`src/ai_company/lsmem/` removed; residue swept); `src/ai_company/memory/` (legacy JSON store) is the sole engine, still imported by executor, dashboard, MCP server, doctor, and CLI. README's stale `memory remember` row fixed in `a1bdf5b5`. Follow-up closed 2026-10-07: `docs/STATUS.md` LS-MEM entries now carry superseded-correction notes.
2. **Runtime-state relocation (D-6):** **RESOLVED 2026-10-07** — `orchestrator/` runtime state (approvals, escalation, scheduler, cost tracker, dead letters, escalation events, postmortems) now lives in gitignored `data/orchestrator/`, resolved via `state_path()` (`src/ai_company/paths.py`) which self-migrates the legacy tree on first access and falls back to the legacy path if migration fails (rollback-safe); callers, docs, workflows and tests updated (supersedes the 2026-10-07 partial note: survey of ~93 refs across 21 files). **Remaining:** the 12 `memory/memory-index.yaml` refs — `memory/` was out of D-6 scope. Ledger of truth remains `.opencode/audit`.
3. **Milestones deck duality (Q3):** **RESOLVED** — `.js` twin (`scripts/build/generate-milestones-deck.js`) deleted in `70921d50`; the Python generator is canonical.
4. **`tmp/` tracked scratch:** **RESOLVED** — 126 files deleted in `d77ea526`; `git ls-files tmp/` = 0.
5. **`whitepaper/` outputs:** out of this cleanup's scope; revisit.
6. **Fresh-clone verification** of the open-design submodule pin is a Stage 9 item.
7. **Pre-existing working-tree changes untouched:** `hr/onboarding_requests.yaml` (onboarding intake state) remains modified by other in-flight work and was never staged here. The rest of the previously dirty set (brand tokens, site content, `.archive/athena/` deletions, `repo-audit/`, knowledge bug-fix records) was landed by a concurrent remediation session in `526f33d5`.
