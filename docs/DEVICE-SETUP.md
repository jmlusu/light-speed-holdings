# Device Setup — AI Company Builder (light-speed-holdings)

> How to provision a fresh machine at `C:\Users\jmlus\light-speed-holdings`
> using the canonical bootstrap commands.
>
> End-to-end: prerequisites → clone → secrets → dev bootstrap → generate →
> company bootstrap → verify.

## 1. Prerequisites (Phase 0)

Install on the new device:

- **Git** (https://git-scm.com)
- **Ollama** (https://ollama.com) — required; `ai-company bootstrap` exits 1 if missing
- **opencode CLI** (https://opencode.ai) — required; `ai-company bootstrap` exits 1 if missing
- **uv** — optional; the bootstrap auto-installs it via pip if absent
- LLM + dashboard API keys (OpenCode/Big Pickle, Gemini, dashboard)

## 2. Clone (Phase 1)

```powershell
git clone https://github.com/jmlusu/light-speed-holdings.git C:\Users\jmlus\light-speed-holdings
cd C:\Users\jmlus\light-speed-holdings
```

## 3. Secrets (Phase 2) — must precede bootstrap

```powershell
Copy-Item .env.example .env
notepad .env
```

Set at minimum: `OPENCODE_API_KEY`, `GEMINI_API_KEY`, `DASHBOARD_API_KEY`, and the
RBAC keys `DASHBOARD_RUN_KEY`, `DASHBOARD_APPROVE_KEY`, `DASHBOARD_ADMIN_KEY`.

> Placeholder values (`your_..._here`) count as **missing** — the bootstrap's
> environment check fails (exit 1) until real keys are set.

## 4. Dev-machine bootstrap (Phase 3)

```powershell
uv run ai-company bootstrap
```

What it does (idempotent — safe to re-run):

1. Installs uv if missing (pip fallback)
2. Creates `.venv` (`uv venv`)
3. Syncs dependencies (`uv sync --extra dev`, respects `uv.lock`)
4. Installs pre-commit hooks
5. Verifies Python ≥ 3.12, Ollama, opencode CLI, Git, and required env vars

> Alternative all-in-one onboarding: `.\scripts\dev.ps1`
> (setup + lint + test + generate + status).

## 5. Generate agents (Phase 4)

```powershell
uv run ai-company generate
```

Syncs `company-registry.yaml` → `company/agent-registry.json` and renders the
127 agent files to `.opencode/agents/*.md`.

## 6. Company bootstrap (Phase 5)

```powershell
uv run ai-company company run
```

`BootstrapEngine` creates the directory structure and generated configs from
`config/`.

## 7. Verify (Phase 6)

```powershell
uv run ai-company doctor run
uv run ai-company agents list
uv run ai-company validate
uv run pytest                      # full suite (~1856 tests)
.\scripts\verify-agents.ps1        # registry + agent file consistency
```

## 8. Smoke test (optional)

```powershell
uv run ai-company orchestrator tick
uv run ai-company dashboard        # FastAPI dashboard at localhost:8420
```

## Gotchas

- The README clone URL is stale; use the `jmlusu/light-speed-holdings.git` repo above.
- `ai-company init` is **not registered** in the CLI — use
  `bootstrap` → `generate` → `company run` instead.
- `.opencode/agents/*.md` and `company/agent-registry.json` are git-tracked, so a
  fresh clone already contains them; `generate`/`company run` re-sync from the registry.
- `.venv` and `.env` are gitignored — built per machine.
