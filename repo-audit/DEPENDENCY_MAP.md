# Dependency Map

**Stack:** dual-stack repo — Python 3.12+ (CLI/package) + TypeScript/React 18 (Vite SPA)
**Manifests:** `pyproject.toml`, `uv.lock`, `package.json`, `package-lock.json`, `bun.lock`,
`open-design/pnpm-lock.yaml`

---

## 1. The package-manager problem (§21)

| Lockfile | Manager | Root package? | Assessment |
|---|---|---|---|
| `uv.lock` | `uv` | yes — `ai-company` | **CANONICAL for Python.** `Makefile` and `AGENTS.md` are `uv`-based throughout. |
| `package-lock.json` | `npm` | yes — Vite SPA | **CANONICAL for JS.** `AGENTS.md` references npm scripts (`uv run`, `pytest`, and the repo-root `src/` Vite app). |
| `bun.lock` | `bun` | yes — same Vite SPA | **DUPLICATE MANAGER — INVESTIGATE** |
| `open-design/pnpm-lock.yaml` | `pnpm` | third-party nested repo | Not LightSpeed's concern |

**Finding:** two package managers (npm **and** bun) lock the same root `package.json`.
This is exactly the §21 "conflicting versions / duplicate libraries" class.
Two resolvable states can exist for one dependency tree, which makes builds
non-reproducible and makes "did CI match my machine?" unanswerable.

**Disposition:** `bun.lock` = **INVESTIGATE → likely DELETE**, contingent on
confirming nothing (CI, hooks, deploy, docs, agent prompts) invokes `bun`.
Not decided unilaterally — see OPEN_QUESTIONS.md Q3.

There is also `scripts/check-package-manager.cjs` (1.6 KB) already in the repo,
which suggests the conflict was *noticed* and a guard partially written. It needs to
be reconciled with whichever manager is chosen.

## 2. Python dependencies

Source: `pyproject.toml` (`ai-company` v0.6, `requires-python >=3.12`).

| Dependency | Classification | Notes |
|---|---|---|
| `typer` | USED | CLI entry point (37 subcommands) |
| `pydantic` | USED | domain models (`models/models.py`) |
| `fastapi`, `uvicorn` | USED | dashboard REST API |
| `pyyaml` / `yaml` | USED | registry + company config |
| `httpx` | USED | provider/web calls |
| `jinja2` | USED | agent-card template rendering |
| `python-dotenv` | USED | env loading (`verify_keys()`) |
| `websockets` | USED | dashboard WebSocket broadcast |
| `structlog` / logging extras | UNKNOWN | needs import sweep |
| dev group (`pytest`, `ruff`, `mypy`, `bandit`) | DEVELOPMENT | correct separation |
| e2e group (`playwright`) | OPTIONAL | referenced by `.agents/skills/playwright` |
| otel group | OPTIONAL | observability; verify actually wired |

Rule from §21 applied: **no dependency removed until dynamic-import check passes.**
Python plugin/optional-group and `importlib` usage in `src/ai_company/services/`
make static grep insufficient; a runtime import trace is required.

## 3. Frontend dependencies

Source: `package.json` — React 18 + Vite + TypeScript, Vitest + Playwright.

Notable surface: `react-router-dom`, chart library, `lucide-react`, motion/animation,
`framer-motion`, Vercel Blob (mail/asset path). Per AGENTS.md the repo-root Vite SPA
is also the render target for `ls-frontend-design` / `ls-presentation-design`, so
some of these are load-bearing for creative tooling, not just the website.

| Item | Classification | Notes |
|---|---|---|
| `react`, `react-dom` | USED | — |
| `react-router-dom` | USED | site routes |
| `vite`, `typescript` | USED | build/dev |
| `vitest`, `playwright` | DEVELOPMENT | test |
| chart lib | USED | referenced by dashboard/analytics surfaces |
| `lucide-react`, `framer-motion` | USED | per design-system skills |
| `@vercel/blob` | USED? | verify — asset or mail path |

## 4. Cross-cutting: npm deps inside the Python repo

`packages/` holds **4,304 files but only 46 tracked**. That gap means `packages/`
currently mixes a tracked package definition with a large untracked install.
Similarly `.opencode/` has 4,222 files on disk / 2,469 tracked. Before any
`npm ci` guarantee can be claimed, the tracked-vs-untracked split in `packages/`
must be resolved — see OPEN_QUESTIONS.md Q4.

## 5. Docker / infra dependencies

`docker-compose.staging.yml`, `Dockerfile`, `vercel.json`, `.vercel/`.
`AGENTS.md` §5 documents staging port mapping (host 8421 → container 8420).
Deployment config must remain valid post-cleanup (§36 Runtime gate).

## 6. Dependency actions queued (not executed)

| # | Action | Gate |
|---|---|---|
| D1 | Choose npm **or** bun; delete the other lockfile | user decision (Q3) |
| D2 | Resolve `packages/` tracked/untracked split | investigation |
| D3 | Import sweep → mark USED / UNUSED for each Python dep | runtime trace |
| D4 | Verify `@vercel/blob` and otel group actually imported | grep + import trace |
| D5 | Record `scripts/check-package-manager.cjs` as either the guard or delete it | depends on D1 |
