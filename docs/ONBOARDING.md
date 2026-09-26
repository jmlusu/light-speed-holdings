# Onboarding — AI Company Builder (light-speed-holdings)

> Single reference for provisioning a **new staff machine** and scaffolding a
> **new client company**, consolidating the canonical sources below. It is
> intentionally documentation-only — every command it runs already exists.

| Canonical source | Responsibility |
|---|---|
| [`DEVICE-SETUP.md`](DEVICE-SETUP.md) | Fresh-machine phases 0–6 (staff) |
| [`../scripts/dev.ps1`](../scripts/dev.ps1) | All-in-one staff onboarding (setup/lint/test/generate/status) |
| [`../scripts/seed-agents.ps1`](../scripts/seed-agents.ps1) | Regenerate the 18 executive + board agent cards via the factory |
| [`../scripts/bootstrap-company.ps1`](../scripts/bootstrap-company.ps1) | Client/company folder scaffolding (**pre-governance only**) |
| [`../scripts/remind-bootstrap.ps1`](../scripts/remind-bootstrap.ps1) | Re-reminder time-boxing alias |
| [`sop-hr-onboarding.md`](sop-hr-onboarding.md) | SOP-HR-001: adding **AI agents** to the hierarchy (not human staff) |

Client **governance** (Signed Contract, DPA, Compliance Risk Assessment, Security
Review — the G1–G4 gates) is out of scope for this document; it is enforced
separately by `client_intake` / `ApprovalGate` per
[`legal/client-onboarding-policy.md`](legal/client-onboarding-policy.md). This doc
covers scaffolding that happens **before** any approval gate.

---

## 1. Staff — new developer machine

End-to-end: prerequisites → clone → secrets → dev bootstrap → generate →
company bootstrap → verify.

### Phase 0 — Prerequisites

Install on the new device:

- **Git** (https://git-scm.com)
- **Ollama** (https://ollama.com) — required; `ai-company bootstrap` exits 1 if missing
- **opencode CLI** (https://opencode.ai) — required; `ai-company bootstrap` exits 1 if missing
- **uv** — optional; the bootstrap auto-installs it via pip if absent
- LLM + dashboard API keys (OpenCode/Big Pickle, Gemini, dashboard)

> The README clone URL is stale — use the repo below.

### Phase 1 — Clone

```powershell
git clone https://github.com/jmlusu/light-speed-holdings.git C:\Users\jmlus\light-speed-holdings
cd C:\Users\jmlus\light-speed-holdings
```

### Phase 2 — Secrets (must precede bootstrap)

```powershell
Copy-Item .env.example .env
notepad .env
```

Set at minimum: `OPENCODE_API_KEY`, `GEMINI_API_KEY`, `DASHBOARD_API_KEY`, and the
RBAC keys `DASHBOARD_RUN_KEY`, `DASHBOARD_APPROVE_KEY`, `DASHBOARD_ADMIN_KEY`.

> Placeholder values (`your_..._here`) count as **missing** — the bootstrap's
> environment check fails (exit 1) until real keys are set. `.env` is gitignored;
> never commit it.

### Phase 3 — Dev-machine bootstrap

Option A (canonical, outputs a per-step table):

```powershell
uv run ai-company bootstrap
```

Option B (all-in-one: setup + lint + test + generate + status):

```powershell
.\scripts\dev.ps1
```

Both are idempotent — safe to re-run. What they do:

1. Install uv if missing (pip fallback)
2. Create `.venv` (`uv venv`)
3. Sync deps (`uv sync --extra dev`, respects `uv.lock`)
4. Install pre-commit hooks (`pre-commit install` with pre-commit + post-commit)
5. Verify Python ≥ 3.12, Ollama, opencode CLI, Git, and required env vars

`.\scripts\dev.ps1` accepts a single action: `setup`, `test`, `lint`, `status`,
`clean`, `generate`, or `all` (default).

### Phase 4 — Generate agents

```powershell
uv run ai-company generate
```

Syncs `company-registry.yaml` → `company/agent-registry.json` and renders the
~135 agent files to `.opencode/agents/*.md`.

### Phase 5 — Company bootstrap

```powershell
uv run ai-company company run
```

`BootstrapEngine` creates the directory structure and generated configs from
`config/`.

### Phase 6 — Verify

```powershell
uv run ai-company doctor run
uv run ai-company agents list
uv run ai-company validate
uv run pytest                      # full suite (~1856 tests)
uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"  # regen agent cards (git diff must be clean)
```

### Smoke test (optional)

```powershell
uv run ai-company orchestrator tick
uv run ai-company dashboard        # FastAPI dashboard at localhost:8420
```

### Staff day-2 checklist

- Regenerate the canonical executive/board card set via the factory:
  ```powershell
  .\scripts\seed-agents.ps1          # -DryRun to review all 18 first
  ```
  (`seed-agents.ps1` passes each agent spec to `scripts/new-agent.ps1`; safe to
  re-run, the factory de-duplicates by name.)
- `git diff --exit-code` after regeneration — committed cards must match output.
- Confirm `.\scripts\dev.ps1 status` reports: venv active, package installed,
  agents generated, tests present.

---

## 2. Client — new company scaffolding (pre-governance)

Intended for standing up a client / venture company **folder skeleton** before any
client work begins. Governance gates (POL-CL-001 G1–G4) are **not** part of this
step — they run later through `client_intake` / `ApprovalGate`.

### Steps

```powershell
# 1. Create the target directory (name per client)
New-Item -ItemType Directory -Path C:\path\to\<client> -Force

# 2. Scaffold from the template
Copy-Item scripts\bootstrap-company.ps1 C:\path\to\<client>\
cd C:\path\to\<client>
.\bootstrap-company.ps1
```

### What it creates

- Root folders: `.agents`, `board`, `executives`, `departments`, `knowledge`,
  `memory`, `prompts`, `tools`, `workflows`, `config`, `templates`, `projects`,
  `reports`, `logs`, `docs`, `tests`
- `executives/<role>/` for 12 roles (`chief-of-staff`, `ceo-office`, `coo`, `cto`,
  `cfo`, `chief-ai-officer`, `cpo`, `cmo`, `sales`, `customer-success`, `legal`,
  `hr`) — each with `Agent.md`, `Mission.md`, `Tasks.md`, `Memory.md`, `SOP.md`,
  `KPIs.md`, and `Prompts/`, `Templates/`, `Tools/` subfolders
- `board/<committee>/` for 8 committees (`strategy`, `finance`, `technology`,
  `operations`, `product`, `customer`, `risk`, `venture`) — each with `Agent.md`,
  `Frameworks.md`, `Questions.md`, `ReadingList.md`

### After scaffolding

1. Populate the executive `Agent.md` / `Mission.md` / `SOP.md` / `KPIs.md` files.
2. Push the client through onboarding **governance** (contract → DPA → risk
   assessment → security review) via the standard client-intake flow — see
   [`legal/client-onboarding-policy.md`](legal/client-onboarding-policy.md).
3. Only after gates pass may client tasks be admitted to the inbox
   (client work is `PENDING`/`BLOCKED_GATES` until satisfied).

---

## 3. Gotchas

- The README clone URL is stale; use `jmlusu/light-speed-holdings.git` (Phase 1).
- `ai-company init` is **not registered** in the CLI — use
  `bootstrap` → `generate` → `company run` instead.
- `.opencode/agents/*.md` and `company/agent-registry.json` are git-tracked, so a
  fresh clone already contains them; `generate`/`company run` re-sync from the registry.
- `.venv` and `.env` are gitignored — built per machine.
- SOP-HR-001 (`sop-hr-onboarding.md`) governs onboarding **AI agents** into the
  hierarchy — a different process from human-staff onboarding above.
- Client governance gates are intentionally **out of scope** of this doc; do not
  open client work until `client_intake` reports all gates satisfied.
