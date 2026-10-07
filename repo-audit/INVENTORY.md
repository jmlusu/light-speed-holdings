# Repository Inventory

**Date:** 2026-10-06
**Branch:** `feat/athena-archive-and-design-system`
**HEAD:** `048627ad fix: correct tsconfig paths and wrapper module types`
**Phase:** 1 (INVENTORY) — non-destructive

> Scope note: sizes are on-disk. Git tracking is reported separately because the
> largest consumers of disk (`models/`, `open-design/`, root `orchestrator/`,
> root `memory/`) are **not** tracked, so disk usage and repository weight
> diverge by roughly 27 GB.

---

## 1. Top-level directory census

69 directories at root, excluding `node_modules/`, `.venv/`, `.git/`.
Total on disk excluding those three: **~28.1 GB**.

| Directory | Files | MB | Tracked | Disposition |
|---|---:|---:|---:|---|
| `models/` | 5 | 24134.7 | 0 | KEEP (local model store) — documented strategy required |
| `open-design/` | 90578 | 2731.8 | 1 | **INVESTIGATE** — nested `.git` repo, 90k files |
| `.opencode/` | 4222 | 757.4 | 2469 | REFACTOR — 692 MB retired skill artifacts |
| `orchestrator/` | 9 | 232.6 | 1 | **INVESTIGATE** — runtime data at root, one tracked file |
| `lab/` | 39 | 216.1 | 39 | ARCHIVE — 216 MB of lab output |
| `packages/` | 4304 | 129.1 | 46 | INVESTIGATE — 4,304 files but only 46 tracked |
| `.mypy_cache/` | 18 | 126.2 | 0 | DELETE — cache |
| `memory/` | 10 | 96.1 | 1 | **INVESTIGATE** — runtime data at root, one tracked file |
| `docs/` | 577 | 90.9 | 565 | KEEP / ARCHIVE split (see DOCUMENTATION_AUDIT.md) |
| `backups/` | 33 | 85.1 | 0 | DELETE — 16 tarballs + 22 MB SQLite, Git has history |
| `.pytest_tmp_ci/` | 6758 | 71.8 | 0 | DELETE — test temp |
| `.pytest_tmp_linkedin/` | 6541 | 70.9 | 0 | DELETE — test temp |
| `bin/` | 51 | 45.1 | 51 | ARCHIVE — compiled/bundled binaries |
| `scrollcraft/` | 13 | 32.3 | 13 | ARCHIVE — feature copies of retired skill |
| `data/` | 30 | 22.6 | 0 | KEEP (runtime, gitignored) |
| `harness/` | 411 | 14.7 | 411 | KEEP — ECL harness, referenced by AGENTS.md |
| `tests/` | 592 | 13.8 | 193 | REFACTOR — high-signal subset (see DEAD_CODE.md) |
| `.pytest_tmp/` | 1316 | 11.8 | 0 | DELETE |
| `.google notebook artifacts/` | 1 | 11.5 | 1 | DELETE — stray notebook artifact |
| `src/` | 833 | 9.5 | 833 | KEEP — canonical source |
| `output/` | 40 | 8.8 | 39 | ARCHIVE — generated deliverables |
| `.archive/` | 17 | 8.7 | 75 | DELETE — 58 files already deleted, uncommitted |
| `.pytest_tmp_commit/` | 1932 | 8.2 | 0 | DELETE |
| `logs/` | 14 | 7.2 | 0 | DELETE (gitignored) |
| `dist/` | 403 | 6.9 | 0 | DELETE — build output, reproducible |
| `.agents/` | 727 | 6.8 | 727 | KEEP — skills, referenced by AGENTS.md |
| `static/` | 166 | 6.7 | 163 | CONSOLIDATE — brand mirror |
| `public/` | 398 | 5.7 | 398 | CONSOLIDATE — brand mirror + build assets |
| `brand/` | 103 | 4.9 | 103 | **KEEP — canonical brand source** |
| `Branding landing page/` | 52 | 2.8 | 52 | ARCHIVE — superseded by `brand/` |
| `results/` | 74 | 1.1 | 0 | DELETE (gitignored) |
| `workflows/` | 3720 | 1.0 | 3720 | KEEP — but see DEAD_CODE.md |
| `.playwright-cli/` | 35 | 0.9 | 0 | DELETE (gitignored) |
| `proposal-deliverables/` | 29 | 0.8 | 29 | ARCHIVE — point-in-time proposal |
| `diagrams/` | 2 | 0.7 | 2 | CONSOLIDATE — move under `docs/` |
| `tmp/` | 126 | 0.6 | 0 | DELETE |
| `company/` | 15 | 0.5 | 15 | KEEP — canonical registry/config (with backups removed) |
| `scripts/` | 49 | 0.4 | 49 | REFACTOR — flat sprawl, needs subdirectories |

`src/ai_company/` (833 tracked files under `src/`) is the canonical Python package —
see ARCHITECTURE_MAP.md §2. There is **no** root-level `ai_company/` directory.

Low-count tracked dirs needing classification (not all near-empty): `.benchmarks/`,
`api/`, `dashboard/` (9 files), `board/` (63 files), `hr/` (2), `tasks/` (3),
`survey/` (3), `prompts/` (2), `.crush/`, `.mimocode/`, `.vscode/`,
`ai_development_constitution/` (1).

## 2. Root files — the "dumping ground" problem

Root must stay sparse (§18). Currently present beyond the legitimate set:

| Path | Problem | Disposition |
|---|---|---|
| `LIGHTSPEED REPOSITORY SANITATION & STREAMLINING DIRECTIVE.md` | Active directive, working material | ARCHIVE after Phase 10 |
| 11 one-off root `.py` scripts (`count_agents.py`, `check_audit_db.py`, `check_correlation.py`, `debug_analysis.py`, `debug_git.py`, `enqueue_post1/2/3.py`, `fix_whatwedo.py`, `temp_types.py`, `temp_verify.py`) | One-off root scripts (§18). **No `company_counts.py` exists** — see DEAD_CODE.md §3. **No `survery/` directory exists either** | CONSOLIDATE into `scripts/maintenance/` |
| `git_ls_files.txt` | 413 KB generated listing | DELETE |
| `Makefile`, `package.json`, `pyproject.toml`, `bun.lock`, `package-lock.json`, `uv.lock` | Three lockfiles, two package managers | INVESTIGATE (§21) |
| `.env.example`, `.env.staging.example` | Correct — secrets externalized | KEEP |
| `tasklist.json`, `opencode.json`, `opencode.local.json` | Multiple agent-config files | INVESTIGATE (§9) |
| `DEPLOYMENT.md`, `SECURITY.md`, `CHANGELOG.md` + others at root | Docs competing with `docs/` | CONSOLIDATE |

## 3. Tracked file census (highest-count areas)

```
.opencode/       2469      tests/          193 (of 592 on disk)
.opencode/agents   90      .opencode/skills ~700
workflows/       3720      src/            833
public/           398      .agents/        727
harness/          411      docs/           565
```

## 4. Generated / machine-produced volume

| Artifact | MB | Reproducible | Tracked |
|---|---:|---|---|
| `models/*.gguf` (5 local models) | 24134.7 | Yes — `scripts/download_models.py` | No |
| `open-design/node_modules` + nested repo | 2731.8 | Yes | No |
| `.opencode/skills/scroll-craft/` | 692.3 | No (artifacts) | 13 |
| root `orchestrator/*.jsonl*` | 232.6 | Runtime | 1 |
| root `memory/vector_index/*` | 96.1 | Yes | No |
| `backups/*.tar.gz` (16) | 85.1 | No, but Git has history | No |
| `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, `.hypothesis/` | 127 | Yes | No |
| `.pytest_tmp*` (4 dirs) | 162.7 | Yes | No |
| `dist/` | 6.9 | Yes | No |

See GENERATED_FILES.md for the full disposition table.

## 5. What is NOT in the inventory

Deliberately not enumerated line-by-line (low signal, high volume):
`node_modules/`, `.venv/`, `.git/`, `open-design/node_modules`, `__pycache__/`,
`.pytest_tmp*/`, `*.pyc`, `.mypy_cache/`, `.ruff_cache/`, `.hypothesis/`.

The full per-file table required by §5 of the directive (path/extension/size/
modified/tracking/references/runtime relevance/generated/disposition) should be
generated mechanically into `repo-audit/inventory.csv` only after the source-of-truth
decisions in OPEN_QUESTIONS.md are answered — producing it earlier would encode
guesses as facts.
