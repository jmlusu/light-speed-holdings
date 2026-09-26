---
sop_id: SOP-ONBOARD-001
title: Staff & Client Onboarding Procedure
department: devops
owner: devops-lead
version: 1.0
effective_date: 2026-09-25
last_reviewed: 2026-09-25
status: active
---

# Staff & Client Onboarding Procedure

## 1. Purpose

Define the standard process for provisioning a **new staff development machine**
and scaffolding a **new client / venture company folder** from the existing
bootstrap templates, from prerequisites through verification.

## 2. Scope

Applies to:

- New developer machines for human staff working on the AI Company Builder
  (`light-speed-holdings`) repository.
- New client / venture company skeleton scaffolding (**pre-governance only**).

Out of scope: client governance gates (Signed Contract, DPA, Compliance Risk
Assessment, Security Review — the G1–G4 gates from
[`legal/client-onboarding-policy.md`](legal/client-onboarding-policy.md)); they
are enforced separately by `client_intake` / `ApprovalGate`. Also out of scope:
onboarding new **AI agents** into the company hierarchy — that is
[`sop-hr-onboarding.md`](sop-hr-onboarding.md) (SOP-HR-001), a different process.

## 3. Definitions

| Term | Definition |
|------|------------|
| Onboarding (staff) | End-to-end provisioning of a fresh developer machine against this repo |
| Onboarding (client) | Folder-skeleton scaffold for a new client / venture company, before approval gates |
| Bootstrap | `ai-company bootstrap` / `scripts/dev.ps1` idempotent dev-machine setup |
| Generate | `ai-company generate` — `company-registry.yaml` → `company/agent-registry.json` + `.opencode/agents/*.md` |
| Company run | `ai-company company run` — `BootstrapEngine` directory + config scaffolding |

## 4. Roles & Responsibilities

| Role | Responsibility |
|------|----------------|
| Staff Developer | Follows the machine phases on their own device |
| DevOps Lead | Owns the provisioning flow; verifies prerequisites and idempotency |
| Platform Engineer | Toolchain and bootstrap-path validation (Git / Ollama / opencode CLI / uv) |
| Security / Compliance Lead | Secrets step, placeholder detection, gitignore posture |
| Solutions Engineer | Client-scaffolding procedure (`scripts/bootstrap-company.ps1`) |
| Test Engineering Lead | Verification gate (doctor, agents list, validate, pytest) |
| Human Operator | Final confirmation that onboarding completed cleanly |

## 5. Procedure

### Step 1: Verify Phase 0 — Prerequisites

Install on the new device:

- **Git** (https://git-scm.com)
- **Ollama** (https://ollama.com) — required; `ai-company bootstrap` exits 1 if missing
- **opencode CLI** (https://opencode.ai) — required; `ai-company bootstrap` exits 1 if missing
- **uv** — optional; the bootstrap auto-installs it via pip if absent
- LLM + dashboard API keys (OpenCode/Big Pickle, Gemini, dashboard)

**Expected Result:** All required tools present; keys on hand.

> The README clone URL is stale — use the repo below.

### Step 2: Phase 1 — Clone

```powershell
git clone https://github.com/jmlusu/light-speed-holdings.git C:\Users\jmlus\light-speed-holdings
cd C:\Users\jmlus\light-speed-holdings
```

**Expected Result:** Working tree present at the target path.

### Step 3: Phase 2 — Secrets (must precede bootstrap)

```powershell
Copy-Item .env.example .env
notepad .env
```

Set at minimum: `OPENCODE_API_KEY`, `GEMINI_API_KEY`, `DASHBOARD_API_KEY`, and
the RBAC keys `DASHBOARD_RUN_KEY`, `DASHBOARD_APPROVE_KEY`, `DASHBOARD_ADMIN_KEY`.

Placeholder values (`your_..._here`) count as **missing** — the bootstrap's
environment check fails (exit 1) until real keys are set. `.env` is gitignored;
never commit it.

**Expected Result:** Real keys present in `.env`; environment check passes.

### Step 4: Phase 3 — Dev-machine bootstrap

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

**Expected Result:** `.venv` present, deps synced, hooks installed, all checks green.

### Step 5: Phase 4 — Generate agents

```powershell
uv run ai-company generate
```

Syncs `company-registry.yaml` → `company/agent-registry.json` and renders the
~135 agent files to `.opencode/agents/*.md`.

**Expected Result:** Agent registry + cards are up to date.

### Step 6: Phase 5 — Company bootstrap

```powershell
uv run ai-company company run
```

`BootstrapEngine` creates the directory structure and generated configs from
`config/`.

**Expected Result:** Company directories and generated configs exist.

### Step 7: Phase 6 — Verify

```powershell
uv run ai-company doctor run
uv run ai-company agents list
uv run ai-company validate
uv run pytest                      # full suite (~1856 tests)
uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"  # regen agent cards (git diff must be clean)
```

Optional smoke test:

```powershell
uv run ai-company orchestrator tick
uv run ai-company dashboard        # FastAPI dashboard at localhost:8420
```

**Expected Result:** Doctor clean, agents listed, validation passes, full test
suite green, regenerated cards produce a clean `git diff`.

### Step 8: Staff day-2 checklist

- Regenerate the canonical executive/board card set via the factory:
  ```powershell
  .\scripts\seed-agents.ps1          # -DryRun to review all 18 first
  ```
  (`seed-agents.ps1` passes each agent spec to `scripts/new-agent.ps1`; safe to
  re-run, the factory de-duplicates by name.)
- `git diff --exit-code` after regeneration — committed cards must match output.
- Confirm `.\scripts\dev.ps1 status` reports: venv active, package installed,
  agents generated, tests present.

**Expected Result:** Default card set regenerates cleanly; status report green.

### Step 9: Client — new company scaffolding (pre-governance)

Intended for standing up a client / venture company **folder skeleton** before any
client work begins. Governance gates (POL-CL-001 G1–G4) are **not** part of this
step — they run later through `client_intake` / `ApprovalGate`.

```powershell
# 1. Create the target directory (name per client)
New-Item -ItemType Directory -Path C:\path\to\<client> -Force

# 2. Scaffold from the template
Copy-Item scripts\bootstrap-company.ps1 C:\path\to\<client>\
cd C:\path\to\<client>
.\bootstrap-company.ps1
```

What it creates:

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

After scaffolding:

1. Populate the executive `Agent.md` / `Mission.md` / `SOP.md` / `KPIs.md` files.
2. Push the client through onboarding **governance** (contract → DPA → risk
   assessment → security review) via the standard client-intake flow — see
   [`legal/client-onboarding-policy.md`](legal/client-onboarding-policy.md).
3. Only after gates pass may client tasks be admitted to the inbox
   (client work is `PENDING`/`BLOCKED_GATES` until satisfied).

**Expected Result:** Client folder skeleton scaffolded; governance flagged as
pending via `client_intake`.

## 6. Escalation Path

| Condition | Action | Contact |
|-----------|--------|---------|
| Bootstrap exits 1 on missing prerequisite | Install the reported tool and re-run | Platform Engineer |
| Environment check fails on placeholder key | Set a real key in `.env` and re-run | Security / Compliance Lead |
| Tests fail after generate | Debug and fix | Test Engineering Lead |
| Client scaffolding fails | Investigate `bootstrap-company.ps1` and re-run | Solutions Engineer |
| Human operator unavailable > 24h | Escalate to Chief of Staff | chief-of-staff |

## 7. Verification Checklist

- [ ] Prerequisites installed (Git, Ollama, opencode CLI)
- [ ] Repository cloned
- [ ] `.env` populated with real keys (no placeholders)
- [ ] `bootstrap` / `dev.ps1` completed idempotently
- [ ] `generate` synced registry + cards
- [ ] `company run` created directories/configs
- [ ] `doctor run`, `agents list`, `validate`, `pytest` all pass
- [ ] Agent-card regeneration produces a clean `git diff`
- [ ] Staff day-2 checklist confirmed
- [ ] Client scaffold created (if applicable)

## 8. References

- `docs/ONBOARDING.md` — Comprehensive onboarding reference (this SOP's runbook)
- `docs/DEVICE-SETUP.md` — Fresh-machine phases 0–6 (staff)
- `scripts/dev.ps1` — All-in-one staff onboarding script
- `scripts/seed-agents.ps1` — 18-agent card regenerator via `scripts/new-agent.ps1`
- `scripts/bootstrap-company.ps1` — Client pre-governance folder scaffold
- `scripts/remind-bootstrap.ps1` — Re-reminder time-boxing alias
- `docs/sop-hr-onboarding.md` — SOP-HR-001: onboarding **AI agents** into the hierarchy
- `docs/legal/client-onboarding-policy.md` — POL-CL-001 G1–G4 governance gates
- `company-registry.yaml` — Agent source of truth
- `.env.example` — Canonical environment-variable template

## 9. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-25 | devops-lead | Initial release |

---

*SOP Owner: devops-lead*
*Next Review: 2026-12-25*
