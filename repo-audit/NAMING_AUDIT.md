# Naming Audit

Covers naming-adjacent clutter under §28 (no-duplicate suffixes), §17 (script-purpose grouping), and §18 (root-directory rule). §19 is the .gitignore fix, not a naming section.

---

## 1. Defects — files whose names are actively misleading

| Path | Defect | Why it hurts | Disposition |
|---|---|---|---|
| `.md` (repo root, tracked) | A file named **exactly** `.md`** — an extension with no name, and hidden | Invisible in `ls`, never reviewed, impossible to guess purpose. Most likely a botched write. | **INVESTIGATE → almost certainly DELETE** |
| `orchestrator/escalation_events.jsonl.RUN2GENERATED` (21.92 MB) | Run state encoded in a filename | Nobody can tell if it is current, and "RUN2" implies a RUN1 that does not exist | DELETE (see §9.3 note in SECURITY_AUDIT.md) |
| `memory/vector_index/tmp53nqnhf1.tmp` (42.12 MB) | A **live temp file**, random name, 42 MB | `tmp*` files are never reviewed, never cleaned. §6 classes temporary/intermediate artifacts as generated clutter | DELETE |
| `orchestrator/escalation_events.jsonl.bak` (210.56 MB) | Hand-made `.bak` in the working tree | §28: hand-made `.bak`/`.old`/`.orig` files duplicate what Git history already provides | DELETE (needs sign-off, §9.3) |
| `survey/` (3 tracked files) | Collides with a common word, easy to type into the wrong path | INVESTIGATE → rename under a namespaced data path or remove |
| `_temp_brief.txt`, `_carousel-concepts.txt`, `_linkedin-article-body.txt` (tracked) | Leading underscore marks "temporary", yet they are **committed** | Contradicts tracked status | ARCHIVE to `docs/content/` or DELETE |
| `company/agent-registry.json.bak-2026-09-18`, `.bak-2026-09-18-hybrid` | Two dated hand-made backups | Git history is the backup mechanism | DELETE/ARCHIVE (D-4) |
| `company/models.yaml.executor-bak` | Same anti-pattern, third instance | — | ARCHIVE/DELETE (Q5) |

**Three independent `.bak` conventions exist.** That is the signature of a team without
a backup answer — §31 answers this: Git *is* the backup.

## 2. Conventions in force (no standard)

| Group | Convention | Examples |
|---|---|---|
| Root `.md` (part 1) | `UPPER_SNAKE_CASE.md` | `MASTER_SPEC.md`, `TARGET_ARCHITECTURE.md`, `IMPLEMENTATION_AUDIT.md` |
| Root `.md` (part 2) | `kebab-case.md` | `analysis_taxonomy.md`, `knowledge-model-analysis.md`, `seo-specialist-analysis.md` |
| Root `.md` (part 3) | `snake_case.md` | `dual_environment_compatibility_standard.md`, `issue-381-amended-policy.md` |
| Root `.md` (part 4) | spaces, `&`, Title Case | `GEOGRAPHIC POSITIONING & MARKET ARCHITECTURE REFINEMENT DIRECTIVE.md`, `CUSTOMER_JOURNEY_CONVERSION_ARCHITECTURE.md`, `WA YFINDER…` |
| Root QA output | `qa-<page>-<WxH>.png`, `qa-report-<page>.json` | consistent internally, wrong location |
| Source | `snake_case` + `kebab-case` mixed | `src/ai_company/`, `src/orchestrator/`, `src/memory/`, `src/components/` |

**Four markdown conventions coexist at the repo root.** No directive section prescribes a naming standard — this is an audit recommendation, not a directive requirement.

### Adopt

| Artifact | Convention | Rationale |
|---|---|---|
| Markdown docs | `kebab-case.md` | Already the majority of `docs/`; URL- and shell-friendly |
| Python modules | `snake_case.py` | PEP 8 |
| TS/TSX components | `PascalCase.tsx` | React convention |
| Test files | `test_*.py` / `*.test.ts` | matches existing pytest + vitest |
| Scripts | `kebab-case.{py,ps1}` inside `scripts/<purpose>/` | §17 |
| Archives/backups | `docs/archive/<YYYY-MM>/` | no `.bak` suffixes, ever |

## 3. Verb order in root observability scripts

`count_agents.py` is the only agent-counting script in the repository. If a
company-count tool is ever added it must not repeat the noun-first / verb-first
split seen here. §17 groups by purpose, so the canonical form is kebab-case inside a
purpose directory:

```
scripts/maintenance/count-agents.py
```

> Correction: `company_counts.py` **does not exist** (verified against the tracked
> file list). The earlier audit draft invented this pair; there is no naming conflict
> to resolve today.

## 4. Script extension sprawl

`scripts/` holds 49 files flat across six languages: `.py`, `.ps1`, `.js`, `.ts`,
`.cjs`, `.sh`, plus `start_vite.bat` at root. Two bootstrap entry points exist for the
same job (`start-dev.ps1` and `start_vite.bat`). §17 argues for one
shell of a kind per purpose directory.

## 5. Root-sprawl naming

107 tracked files at root, of which 38 are `.md`, 11 `.py`, 9 `.png`, 6 `.log`,
11 `.json`, 5 `.txt`. None of the QA or log names are wrong *in themselves* — they
are simply in the wrong place. Moving them to `reports/qa/` and `logs/` resolves it
without renaming.

## 6. Cross-reference integrity (§36 documentation validation / §3 source of truth)

`AGENTS.md` §1 and §3 reference `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`, and
`docs/ECL.md`. **All three exist and resolve.** The defect is that their content has
drifted from verified repository reality — stale counts, paths, and cleanup state —
not that the references dangle. `docs/DEPLOYMENT.md`, however, is genuinely missing
while four competing deployment documents exist. See DOCUMENTATION_AUDIT.md §2 and §4.

## 7. Precedence

1. Renames break imports, CI paths, `package.json` scripts, `Makefile` targets,
   `.pre-commit-config.yaml`, and `AGENTS.md` references. Every rename needs a
   reference sweep first.
2. Moves into `docs/archive/` are cheap; pure renames are not.
3. Phase order (from CLEANUP_PLAN.md): **move before rename.** Archive what is
   historical, move what is misplaced, and only then normalise names.
