# Architecture Map — Current As-Is (not aspirational)

**Purpose:** describe the architecture *as it actually exists*, per §11. Planned or
aspirational elements are labelled `PLANNED`.

---

## 1. Observed runtime chain

```
Human CEO (jmlus)
  ↓
AI Company Builder  (Python 3.12+, Typer CLI, `ai-company`)
  ↓
Company config      company-registry.yaml · company/*.yaml · company/config/*.yaml
  ↓
Agent definitions   .opencode/agents/*.md   (90 cards, OpenCode-native)
  ↓
Execution host      OpenCode (external runtime — not in this repo)
  ↓
Runtime state       root orchestrator/ · root memory/ · data/ · results/ · logs/
  ↓
Local models        models/*.gguf (Ollama / llama.cpp servers)
```

The company is an **agent-hosting repo**, not a hosted service. The AI Company Builder
generates agent cards for an external runtime; it does not itself execute agents in a
server. This is the single most important architectural fact and it is currently
described nowhere coherently.

## 2. Canonical source of truth (verified, not assumed)

| Capability | CURRENT CANONICAL | Competing / non-canonical | Confidence |
|---|---|---|---|
| Company model (90 agents) | `company-registry.yaml` | `company/agent-registry.json`, `.opencode/agents/*.md` | **High — all three agree at 90** |
| Brand tokens | `brand/tokens/` | `public/brand/tokens/`, `static/brand/tokens/` (byte-identical) | **High — MD5 verified identical** |
| Python package | `src/ai_company/` + `pyproject.toml` | root-level scripts | High |
| Frontend app | repo-root Vite SPA in `src/` | — | High |
| Local model store | `models/` (untracked, 24 GB) | — | High |
| ECL harness | `harness/` + `harness/changes/` | `.archive/` (58 files pending deletion) | High |
| Agent operating model | `AGENTS.md` (only root contract) | `.mimocode/`, `.agents/` (tool config, not instructions); `open-design/AGENTS.md` (nested scope); root `CLAUDE.md` **absent** | High — verified, no content conflict |
| Orchestration **code** | `src/ai_company/orchestrator/` | root `orchestrator/` (runtime data only) | **Medium — INVESTIGATE** |
| Memory **code** | `src/ai_company/memory/`, `src/ai_company/lsmem/` | root `memory/` (runtime data only) | **Medium — INVESTIGATE** |
| Health check | **NO CANONICAL REPO-WIDE COMMAND** | Partial gates exist: `scripts/dev.ps1`, `scripts/validate-drift.ps1`, `scripts/validate-architecture.ps1`, `scripts/health_check_models.py` (models only), `tests/docs/test_doc_drift.py` | High (§26 gap) |

### Agent count reconciliation (§12)

```
company-registry.yaml          90 agents
company/agent-registry.json    90 agents
.opencode/agents/*.md          90 cards
```

**One canonical count: 90 agentic units.** No 144/152/127-era counts were found in
live config. Competing *registry files* exist (two `.bak` snapshots) but they are
backups, not divergent counts. This is the healthiest area of the repository.

## 3. Repository strata (the actual, working organisation)

| Stratum | Directories | Purpose |
|---|---|---|
| **A. Source** | `src/` (833), `tests/` (592) | Python package + Vite SPA |
| **B. Config-of-record** | `company/`, `company-registry.yaml`, `brand/`, `config/`, `templates/` | Declarative truth |
| **C. Agent runtime scaffolding** | `.opencode/agents/`, `.agents/skills/`, `.opencode/skills/`, `workflows/`, `harness/` | Generated + maintained cards |
| **D. Operational** | `scripts/`, `Makefile`, `scripts/dev.ps1` | Human/agent entry points |
| **E. Runtime state (gitignored)** | `models/`, `data/`, `results/`, `logs/`, root `orchestrator/`, root `memory/` | Local only |
| **F. Vendored external project** | `open-design/` | Nested `.git`, own AGENTS.md/LICENSE — NOT LightSpeed code |
| **G. Vestigial** | `archive/`, `.archive/`, `backups/`, `scrollcraft/`, `lab/`, `Branding landing page/`, `whitepaper/`, `proposal-deliverables/`, `diagrams/`, `output/`, `board/`, `dashboard/`, `api/`, `hr/`, `survey/` | History, experiments, or unclear |

## 4. Findings against §11 / §13

- **The execution path is not documented as one path.** Nothing states that agent
  cards are *generated* into `.opencode/agents/` from `company-registry.yaml`. That
  generator relationship is the backbone of the architecture and is undocumented.
- **Two "orchestrators" by name.** §13 forbids "old/new orchestrator". Root
  `orchestrator/` is not a second implementation — it is **runtime output**
  (`escalation_events.jsonl`, `dead_letter.jsonl`, `approvals.yaml`,
  `scheduler.yaml`, `cost_tracker.json`). Naming makes it look like source.
  → **Rename is not the fix; relocate to a `runtime/`-style data path.**
- **Two memory subsystems by name.** `src/ai_company/memory/` and
  `src/ai_company/lsmem/` both exist, plus a root `memory/` holding
  `vector_index.json`, `aggregate.json`, `episodic/semantic/procedural/temporal/
  relational.json`. §14 requires the persistent / working / cache / logs / audit /
  vector-index distinction be explicit. It currently is not.
- **Nested `.git` at `open-design/.git`.** A 2.7 GB, 90,578-file, 69-directory
  third-party design-system monorepo (pnpm workspace, own `AGENTS.md`, `LICENSE`,
  `CONTEXT.md`, `vercel.json`) sits inside the LightSpeed repo. It is untracked
  (1 tracked file) and was pulled in by `scripts/setup-open-design.ps1` /
  `scripts/open-design-quickstart.ps1`. It is **not** LightSpeed architecture and
  must not be read as such.
- **`docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`, and `docs/ECL.md` all exist** and
  are non-trivial (16.1 KB, 8.3 KB, 7.6 KB). The earlier audit draft claiming they
  were absent was wrong. The real defect is **staleness**, not absence:
  - `docs/ARCHITECTURE.md` — last modified 2026-09-21
  - `docs/DEVELOPMENT.md` — last modified 2026-10-01
  - `docs/ECL.md` — last modified 2026-09-16
  → **Disposition: REFACTOR** (refresh against verified reality; this audit's
  `ARCHITECTURE_MAP.md` plus `docs/REPOSITORY_CLEANUP_PLAN.md` are source material).

## 5. External integrations (as evidenced)

- OpenCode (agent host, `.opencode/`, `opencode.json`, `opencode.local.json`)
- OpenAI-compatible local servers (GGUF via llama.cpp / Ollama) — `scripts/start_llamacpp_servers.py`, `scripts/download_models.py`
- GitHub (`gh` CLI for issue tracker per `docs/agents/issue-tracker.md`)
- Resend-style transactional email surface (present in dependency list; verify)
- Vercel (`vercel.json`, `.vercel/`)
- Playwright (visual/E2E checks)

## 6. Deployment model

Staging via `docker-compose.staging.yml` (host port 8421 → container 8420);
production 8420. See `AGENTS.md` §5. Not yet independently verified in this audit.

## 7. Architecture documentation gaps (accurate restatement)

- `docs/ARCHITECTURE.md` — **exists**; needs accuracy refresh (see §4)
- `docs/DEPLOYMENT.md` — **MISSING.** Neither `docs/DEPLOYMENT.md` nor root
  `DEPLOYMENT.md` exists. Four competing deployment docs do exist:
  `docs/DEPLOYMENT-GUIDE.md`, `docs/BRAND_DEPLOYMENT_GUIDE.md`,
  `docs/OCI-FREE-TIER-DEPLOYMENT.md`, `RUNBOOK-LightspeedAI-Deployment-2026-10-03.md`
  (plus `DEPLOY_TEST.md`). → **CONSOLIDATE**, not relocate
- Canonical repo-wide health check command/output — **MISSING** (see row in §2)
- `docs/REPOSITORY_HEALTH.md` — genuinely absent; §37 requirement, due after cleanup
