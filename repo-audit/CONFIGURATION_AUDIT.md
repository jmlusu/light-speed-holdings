# Configuration Audit

**107 tracked files at repo root.** 11 `.json`, 38 `.md`, 11 `.py`, 9 `.png`,
6 `.log`, 5 `.txt`. Root is not sparse (§18).

---

## 1. Configuration files at root

| File | Concern | Disposition |
|---|---|---|
| `package.json` | npm scripts are the documented operational surface | KEEP |
| `package-lock.json` + `bun.lock` | **two managers, one manifest** | INVESTIGATE (D-1/§21) |
| `pyproject.toml` + `uv.lock` + `.python-version` | coherent Python stack | KEEP |
| `opencode.json` | primary OpenCode config | KEEP |
| `opencode.local.json` | local override — is it secret-bearing? | INVESTIGATE (see SECURITY_AUDIT.md) |
| `index.html` | Vite entry — must stay root for Vite | KEEP |
| `vite.config.ts`, `vitest.config.ts`, `tsconfig.json` | build/test/TS config — all must be root | KEEP |
| `vercel.json` | deploy config | KEEP |
| `metadata.json` | purpose unclear — site metadata? MCP config? | INVESTIGATE |
| `openapi.json` | API spec — generated from FastAPI or hand-written? | INVESTIGATE |
| `Makefile` | canonical command surface per AGENTS.md | KEEP |
| `.pre-commit-config.yaml` | ruff, mypy, bandit, capture-fix hooks | KEEP |
| `docker-compose.yml` | base | KEEP |
| `docker-compose.staging.yml` | staging (host 8421 → 8420) | KEEP |
| `docker-compose.opendesign.yml` | third-party tool only | INVESTIGATE — belongs with `open-design` |
| `Dockerfile`, `.dockerignore`, `.vercelignore` | build/deploy | KEEP |
| `CODEOWNERS` | ownership | KEEP |
| `git_ls_files.txt` | 413 KB generated dump | DELETE |
| `qa-report.json`, `qa-report-home.json`, `qa-report-og.json`, `qa-report-twitter.json` | generated QA output at root | DELETE (regenerable) |
| `qa-*.png` ×9 | generated screenshots at root, **tracked** | DELETE + gitignore |
| `install.log`, `probe.log`, `runtask.log`, `vite.log`, `vite_start.log`, `vite-dev.log` | **tracked** logs | DELETE + gitignore |
| `_temp_brief.txt`, `_carousel-concepts.txt`, `_linkedin-article-body.txt` | scratch content drafts | ARCHIVE or DELETE |
| `scan_terms_report.txt` | generated report | ARCHIVE to `reports/` |
| `start-dev.ps1`, `start_vite.bat`, `Clean-LSMEM.ps1` | entry-point scripts at root | MOVE to `scripts/` |
| `.md` (a file literally named `.md`) | **filename defect** — see NAMING_AUDIT.md | INVESTIGATE |
| `GEOGRAPHIC POSITIONING & MARKET ARCHITECTURE REFINEMENT DIRECTIVE.md`, `REBUILD_DIRECTIVE.md`, `WEBSITE TRANSFORMATION & REPOSITORY CONSOLIDATION DIRECTIVE.md`, `lightspeed-*-directive.md`, `lightspeed-opencode-migration-directive.md` | 6+ historical directives at root | ARCHIVE to `docs/directives/` |
| `AGENTS.md`, `README.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODEOWNERS` | legitimate root files | KEEP |
| `test_fragment.tsx` | stray fragment at root | MOVE to `src/` or DELETE |

## 2. Config sprawl across competing stacks

```
agent/runtime config :  opencode.json + opencode.local.json + .crush/ + .mimocode/ + .agents/ + .opencode/
python package        :  pyproject.toml + uv.lock + Makefile
js app                :  package.json + package-lock.json + bun.lock + tsconfig.json + vite.config.ts + vitest.config.ts
deploy                :  Dockerfile + docker-compose{,.staging,.opendesign}.yml + vercel.json + .vercel/
hook/quality          :  .pre-commit-config.yaml + Makefile + scripts/dev.ps1
```

§9 (Configuration Consolidation) and §26 (Repository Health Check) require one
obvious command entry point. There are currently **four**
competing surfaces: `make`, `npm run`, `scripts/dev.ps1`, and direct `uv run ...`.

**Disposition:** keep `make` + `scripts/dev.ps1` as the two documented entry points
(AGENTS.md already teaches both); ensure `package.json` scripts are thin wrappers;
document the precedence order in README.

## 3. Ignore-rule conflicts (`.gitignore`)

| Conflict | Symptom | Fix |
|---|---|---|
| `backups/` ignored **but** `scripts/backup.ps1` writes here | backup policy vs hygiene | move backups outside repo |
| `results/`, `logs/`, `data/` ignored, and no directive section declares one canonical output home | unclear canonical output dir (§18/§35) | declare one output dir |
| 9 root `qa-*.png` + 6 root `.log` **tracked** | ignore rules not applied to those patterns | add patterns |
| `open-design` tracked as a gitlink **with no `.gitmodules`** | unresolvable on fresh clone | add `.gitmodules` or untrack |
| `.env`, `.env.*` ignored, `.env.example`/`.env.staging.example` tracked | correct | KEEP as-is |

## 4. Missing configuration

| Gap | Directive § | Status |
|---|---|---|
| Canonical repo-wide health-check command/output | §26 | **MISSING** — partial gates exist but no single entry point: `scripts/dev.ps1`, `scripts/validate-drift.ps1`, `scripts/validate-architecture.ps1`, `scripts/health_check_models.py` (models only), `tests/docs/test_doc_drift.py` |
| `scripts/{dev,build,test,deploy,maintenance,research}/` layout | §17 | MISSING |
| Documented canonical output directory | §18/§35 | MISSING |
| `.gitmodules` for the `open-design` gitlink | — | MISSING (breaks clone) |

## 5. Structural vs cosmetic

- **Cosmetic (safe):** move root scripts into `scripts/`; move directives into
  `docs/directives/`; delete generated root artifacts (`qa-*`, `*.log`,
  `git_ls_files.txt`, `qa-report*.json`).
- **Structural (needs decisions):** package-manager choice; `open-design` gitlink;
  `docker-compose.opendesign.yml` placement; `opencode.local.json` secret exposure;
  output-directory declaration; agent-config consolidation.
