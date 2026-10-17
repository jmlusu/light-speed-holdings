# Dead Code & Unused Asset Audit

**Status: PRELIMINARY — not yet proven dead.**
Directive §27 ("Before deleting") requires, before any deletion: CHECK REFERENCES,
CHECK DYNAMIC IMPORTS, CHECK BUILD, CHECK TESTS, CHECK DOCUMENTATION. **None of those
checks has been completed for the items below.** Everything below is therefore a
*candidate* list, not a verdict.
No code has been deleted.

---

## 1. Method required before any deletion (§27)

The directive's gate is five checks. They must each pass for a specific file before
that file is treated as dead:

```
1. CHECK REFERENCES     → grep the repo (incl. tests, config, workflows, .github/)
                          for the module/filename/export name
2. CHECK DYNAMIC IMPORTS→ resolve non-literal import/require paths
                          (importlib, __import__, glob, require.context,
                          entry_points, get:attr / import: maps in .github/,
                          Vite dynamic import(), PowerShell/JS shims)
3. CHECK BUILD          → full build/test suite green BEFORE the change, so any
                          later failure is attributable to the deletion
4. CHECK TESTS          → run pytest + vitest; the suite must stay green AFTER
                          the deletion, and coverage.py / vitest coverage may be
                          used as supporting evidence
5. CHECK DOCUMENTATION  → confirm no doc, README, or agent card advertises it
```

Only when all five pass may a file be classified DEAD. Coverage figures and runtime
traces are supporting evidence inside checks 3–4; they are not themselves the gate.
§25 lists `dead-code analysis` among its example tools with the objective of fast
feedback and high signal — a tool that automates the five checks above, not a
mandate to delete anything on its own.

**None of the five checks has been run for the items below**, so source-code
deletion stays blocked. Deleting caches, build output, and duplicate *artifacts*
(not source) is outside this gate and remains proposable.

## 2. High-confidence dead code (non-source, safe to propose)

| Path | Evidence | Disposition |
|---|---|---|
| `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`, `.hypothesis/` | tool caches, regenerable | DELETE |
| `.pytest_tmp/`, `.pytest_tmp_ci/`, `.pytest_tmp_ci2/`, `.pytest_tmp_commit/`, `.pytest_tmp_linkedin/` | pytest tmpdir leftovers, 6,758+6,541+1,932+1,316 files | DELETE |
| `dist/` (403 files) | build output, reproducible from `npm run build` | DELETE |
| `install.log`, `probe.log`, `runtask.log`, `vite.log`, `vite_start.log`, `vite-dev.log` | **tracked** runtime logs, 0 bytes of value | DELETE + gitignore |
| `git_ls_files.txt` (413 KB) | generated `git ls-files` dump, committed by accident | DELETE |
| `.google notebook artifacts/` (11.5 MB, 1 tracked) | stray notebook output | DELETE |
| `tmp/` (126 files, untracked) | scratch | DELETE |
| `.playwright-cli/` (untracked) | tool scratch | DELETE |

## 3. Root-level one-off scripts — the clearest §18 violation

11 tracked `.py` files sit at the repo root instead of `scripts/`:

```
check_audit_db.py      debug_analysis.py     enqueue_post1.py
check_correlation.py   debug_git.py          enqueue_post2.py
count_agents.py        fix_whatwedo.py       enqueue_post3.py
                        temp_types.py        temp_verify.py
```

Signals of throwaway code:
- `temp_types.py`, `temp_verify.py` — "temp" in the filename of a *tracked* file
- `enqueue_post1/2/3.py` — numbered ad-hoc variants, a §28 smell
- `debug_analysis.py`, `debug_git.py`, `check_correlation.py` — debugging one-offs

**Disposition: CONSOLIDATE into `scripts/maintenance/`** (the §17 subdirectory the
directive asks for). Keep the scripts — they may be genuinely useful — but remove them
from root. `count_agents.py` is the one legitimate observability tool in this set and
belongs in `scripts/maintenance/`.

> Correction: there is **no `company_counts.py`** anywhere in the repository (verified
> against the tracked-file list). The only observability script is `count_agents.py`.

**Not yet determined:** are any of the 11 imported by `src/`, `scripts/`, CI, or
`Makefile`? A grep sweep is required before moving, so that no import breaks.

## 4. `scripts/` sprawl (49 files, flat, 6 languages)

Extension mix in one directory: `.py`, `.ps1`, `.js`, `.ts`, `.cjs`, `.sh`, `.bat`.

§17 requires `scripts/{dev,build,test,deploy,maintenance,research}/`. The repo has
none of that structure; it also has no `scripts/health_check.py`.

**Disposition: REFACTOR** into the six subdirectories, preserving relative paths in
`package.json` / `Makefile` / `.pre-commit-config.yaml` / `AGENTS.md` (each of which
references script paths and will break otherwise).

Notable: `scripts/check-package-manager.cjs` (1.6 KB) and `scripts/sync-brand.ps1`
are the kind of guard script that must be located first, not relocated blind.

## 5. Suspicious-but-unproven

| Path | Why suspicious | Status |
|---|---|---|
| `Clean-LSMEM.ps1` (root, tracked) | references `lsmem`; a one-off cleanup script | INVESTIGATE |
| `survey/` (3 tracked files) | small near-empty data dir; name collides with a common word | INVESTIGATE — classify or relocate |
| `api/` (near-empty) | stub directory | INVESTIGATE |
| `dashboard/` (9 files) | near-empty; conflicts with the real FastAPI dashboard in `src/` | INVESTIGATE |
| `hr/`, `tasks/`, `prompts/`, `survey/`, `.crush/`, `.mimocode/` | 1–3 files each | INVESTIGATE |
| `company/models.yaml.executor-bak` | obsolete config | ARCHIVE/DELETE (Q5) |
| `company/agent-registry.json.bak-*` ×2 | hand-made backups in Git | DELETE/ARCHIVE (D-4) |
| `scrollcraft/` (13 tracked, 32.3 MB) | feature copy of a retired skill | DELETE (Q1) |
| `.archive/` (75 tracked, 58 already deleted unstaged) | pre-existing in-flight deletion | LEAVE ALONE — user work |

## 6. Explicitly NOT dead (do not touch)

- `.archive/**` deletions — already staged as unstaged deletions by the user before
  this audit. Not mine to finish, revert, or extend.
- `harness/` (411 files) — ECL change-tracking infrastructure, referenced by `AGENTS.md`.
- `workflows/` (3,720 tracked files) — looks alarming but is a legitimate declarative
  asset class. Needs reference verification, not deletion.
- `tests/` — 592 on disk / 193 tracked. The 399 untracked files need triage, but
  untracked tests may be an in-progress suite. **INVESTIGATE, do not bulk-delete.**
- `src/`, `company/`, `brand/`, `config/`, `templates/`, `docs/`.

## 7. Blocker on the dead-code gate

The §27 pre-deletion checks (references, dynamic imports, build, tests,
documentation) have not been run, so source-code deletion stays blocked. §25 lists
`dead-code analysis` among its example tools, with the objective of fast feedback and
high signal; that objective is **not yet satisfiable** for source. It *is* satisfiable
now for the non-source categories in §2 above.
