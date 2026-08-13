# Skill Integration Analysis Report

**Prepared by:** Chief of Staff Agent
**Date:** 2026-08-07
**Context:** Research/analysis only — no code changes made

---

## 1. Current State

### 1.1 Existing Skills Inventory (29 skills in `.agents/skills/`)

| Skill Name | Source (per antigravity manifest) | Category |
|------------|-----------------------------------|----------|
| agenttrace-session-audit | community (luoyuctl/agenttrace) | Observability |
| api-endpoint-builder | community | API Development |
| ax-extract-workflow | community (Necmttn/ax) | Workflow Analysis |
| brooks-lint | community (hyhmrright/brooks-lint) | Code Review |
| bug-hunter | community | Debugging |
| codebase-audit-pre-push | community | Code Quality |
| diagnosing-bugs | community | Debugging |
| docs | local/builtin | Documentation |
| ecl-harness-engineer | community (qinghui316/ecl-harness-engineer) | Process |
| effective-agent-skills | community | Skill Authoring |
| find-skills | vercel-labs/skills (tracked in .skill-lock.json) | Discovery |
| global-chat-agent-discovery | community (pumanitro/global-chat) | Discovery |
| hono | community | Web Framework |
| improve-codebase-architecture | community | Architecture |
| jq | community | Data Processing |
| logic-lens | community (hyhmrright/logic-lens) | Code Review |
| performance-optimizer | community | Performance |
| prototype | community | Prototyping |
| python-pptx-generator | community | Document Generation |
| rayden-code | community | UI Components |
| setup-matt-pocock-skills | community (mattpocock/skills) | Setup |
| skill-check | community | Skill Validation |
| squirrel | community (flyingsquirrel0419/squirrel-skill) | Full-cycle Dev |
| tdd | community | Testing |
| technical-change-tracker | community (Elkidogz/technical-change-skill) | Change Tracking |
| tmux | community | Terminal |
| tree-ring-memory | community (TerminallyLazy/Tree-Ring-Memory) | Memory |
| triage | community | Issue Management |

### 1.2 Lockfile & Manifest State

| File | Purpose | Key Contents |
|------|---------|--------------|
| `.agents/.skill-lock.json` | Skills CLI tracking (v3) | Only `find-skills` from `vercel-labs/skills` tracked; 13 dismissed agents |
| `.agents/skills/.antigravity-install-manifest.json` | Antigravity plugin manifest (schema v1) | Lists all 29 installed skills; updated 2026-07-11 |

### 1.3 Agent Population

- **~130 agent files** in `.opencode/agents/` (OpenCode-native format with `mode: subagent` + `permission:` blocks)
- Generated from `company-registry.yaml` via Jinja2 template (`templates/agents/agent.md.j2`)

### 1.4 ECL Harness Context

- **ECL.md** defines change lifecycle: `new → active → close/park → archive`
- Single active change at a time enforced via `harness/changes/active/`
- Context loading order: `AGENTS.md` → `ECL.md` → active change → `STATUS.md` → source files
- Scripts: `harness-change.ps1`, `harness-evolve.ps1`, `lint-ecl.ps1`

### 1.5 Skill Discovery Mechanism (Critical Finding)

**OpenCode auto-discovers skills from the filesystem.** Evidence:
- No `opencode.json` exists at repo root or in `.opencode/`
- Addyosmani's [opencode-setup.md](https://github.com/addyosmani/agent-skills/blob/main/docs/opencode-setup.md) explicitly states: *"All skills live in: `skills/<skill-name>/SKILL.md`"* and *"OpenCode agents are instructed (via `AGENTS.md`) to: Detect when a skill applies, Invoke the `skill` tool, Follow the skill exactly"*
- The `skill` tool (built into OpenCode) scans `.agents/skills/` directories at runtime
- **AGENTS.md does NOT need to list skills** — it only provides *instructions on how to use them*

---

## 2. Candidate Repository Analysis

### 2.1 addyosmani/agent-skills

| Attribute | Detail |
|-----------|--------|
| **Skill Count** | 24 (23 lifecycle + 1 meta `using-agent-skills`) |
| **License** | MIT |
| **Maintenance** | Active — 3 core maintainers (Addy Osmani, Federico Bartoli, Joan León); regular commits; issues/PRs active |
| **Install Tooling** | `npx skills` CLI (Vercel Labs); supports 70+ agents; marketplace install for Claude Code, Codex, Gemini CLI, Antigravity, Cursor, Windsurf, Copilot, Kiro, Command Code |
| **SKILL.md Format** | YAML frontmatter (`name`, `description`) + structured sections: Overview, When to Use, Process, Rationalizations, Red Flags, Verification |
| **Naming Convention** | lowercase-hyphen (e.g., `test-driven-development`, `api-and-interface-design`) |
| **Architecture** | Lifecycle-phased: Define → Plan → Build → Verify → Review → Ship; includes `references/` (7 checklists), `agents/` (4 personas), `hooks/`, slash commands for multiple tools |
| **OpenCode Support** | Dedicated `docs/opencode-setup.md` — agent-driven via `AGENTS.md` + `skills/` dir; no plugin needed |
| **Meta-skill** | `using-agent-skills` — automatic task-to-skill mapping flowchart |

#### 24 Skills by Phase

| Phase | Skills |
|-------|--------|
| **Define** | `interview-me`, `idea-refine`, `spec-driven-development` |
| **Plan** | `planning-and-task-breakdown` |
| **Build** | `incremental-implementation`, `test-driven-development`, `context-engineering`, `source-driven-development`, `doubt-driven-development`, `frontend-ui-engineering`, `api-and-interface-design` |
| **Verify** | `browser-testing-with-devtools`, `debugging-and-error-recovery` |
| **Review** | `code-review-and-quality`, `code-simplification`, `security-and-hardening`, `performance-optimization` |
| **Ship** | `git-workflow-and-versioning`, `ci-cd-and-automation`, `deprecation-and-migration`, `documentation-and-adrs`, `observability-and-instrumentation`, `shipping-and-launch` |
| **Meta** | `using-agent-skills` |

---

### 2.2 sickn33/agentic-awesome-skills

| Attribute | Detail |
|-----------|--------|
| **Skill Count** | ~700+ (massive aggregated catalog) |
| **License** | Code: MIT; Docs: CC BY 4.0; upstream skills retain their own licenses |
| **Maintenance** | Active — single maintainer (sickn33) + many community contributors; frequent updates; `CHANGELOG.md`, `skills_index.json` for catalog |
| **Install Tooling** | No dedicated CLI; manual copy / git submodule / Antigravity plugin; `scripts/` for catalog generation |
| **SKILL.md Format** | Extended YAML frontmatter: `name`, `description`, `category`, `risk`, `source`, `source_repo`, `source_type`, `date_added`, `author`, `tags[]`, `tools[]`, `license`, `license_source` |
| **Naming Convention** | Mixed: some lowercase-hyphen, some prefixed (e.g., `00-andruia-consultant`, `agenttrace-session-audit`, `api-endpoint-builder`) |
| **Architecture** | Flat `skills/` directory; aggregator model pulling from 100+ upstream repos; includes `CATALOG.md`, `skills_index.json`, `skill_categorization/` |
| **OpenCode Support** | No dedicated guide; skills are plain Markdown — compatible if placed in `.agents/skills/` |
| **Source Types** | `official` (vendor-maintained), `community` (individual/maintainer), `inspiration` |

#### Representative Skill Categories (sample)

- **AI/ML**: `hugging-face-*`, `langchain-*`, `azure-ai-*`, `gemini-*`
- **Cloud/DevOps**: `aws-*`, `azure-*`, `gcp-*`, `kubernetes-*`, `terraform-*`, `docker-*`
- **Testing**: `playwright-*`, `jest-*`, `cypress-*`, `k6-*`, `bats-*`
- **Frontend**: `react-*`, `vue-*`, `angular-*`, `svelte-*`, `tailwind-*`, `nextjs-*`
- **Security**: `burp-suite-*`, `cloudflare-security-audit`, `oidc-*`, `auth-*`
- **Database**: `postgres-*`, `mongodb-*`, `redis-*`, `drizzle-*`, `prisma-*`
- **Agent Orchestration**: `agent-*`, `multi-agent-*`, `agent-memory-*`, `agent-orchestrator`

---

## 3. Impact / Collision Matrix

### 3.1 Direct Name Collisions (Existing vs. Candidate Repos)

| Existing Skill | addyosmani Repo | sickn33 Repo | Collision Risk |
|----------------|-----------------|--------------|----------------|
| `bug-hunter` | ❌ (has `debugging-and-error-recovery`) | ✅ Exact match | **HIGH** — sickn33 has same name |
| `diagnosing-bugs` | ❌ | ✅ Exact match | **HIGH** |
| `tdd` | ✅ `test-driven-development` (semantic) | ✅ `tdd` (multiple) | **HIGH** — name vs semantic |
| `performance-optimizer` | ✅ `performance-optimization` (semantic) | ✅ Multiple perf skills | **MEDIUM** |
| `api-endpoint-builder` | ✅ `api-and-interface-design` (semantic) | ✅ `api-endpoint-builder` (exact) | **HIGH** — sickn33 exact |
| `codebase-audit-pre-push` | ❌ | ✅ Exact match | **HIGH** |
| `technical-change-tracker` | ❌ | ✅ Exact match | **HIGH** |
| `tree-ring-memory` | ❌ | ✅ Exact match | **HIGH** |
| `effective-agent-skills` | ❌ | ✅ Exact match | **HIGH** |
| `improve-codebase-architecture` | ❌ | ✅ Exact match | **HIGH** |
| `setup-matt-pocock-skills` | ❌ | ✅ Exact match (from mattpocock/skills) | **HIGH** |
| `ecl-harness-engineer` | ❌ | ✅ Exact match (from qinghui316) | **HIGH** |
| `ax-extract-workflow` | ❌ | ✅ Exact match (from Necmttn/ax) | **HIGH** |
| `agenttrace-session-audit` | ❌ | ✅ Exact match (from luoyuctl/agenttrace) | **HIGH** |
| `global-chat-agent-discovery` | ❌ | ✅ Exact match (from pumanitro/global-chat) | **HIGH** |
| `hono` | ❌ | ✅ Exact match | **HIGH** |
| `brooks-lint` | ❌ | ✅ Exact match (from hyhmrright) | **HIGH** |
| `logic-lens` | ❌ | ✅ Exact match (from hyhmrright) | **HIGH** |
| `jq` | ❌ | ✅ Exact match | **HIGH** |
| `tmux` | ❌ | ✅ Exact match | **HIGH** |
| `triage` | ❌ | ✅ Exact match | **HIGH** |
| `squirrel` | ❌ | ✅ Exact match (from flyingsquirrel0419) | **HIGH** |
| `prototype` | ❌ | ✅ Exact match | **HIGH** |
| `skill-check` | ❌ | ✅ Exact match | **HIGH** |
| `find-skills` | ✅ `using-agent-skills` (meta-skill) | ✅ `find-skills` (exact) | **HIGH** — both repos |

> **Key Insight:** sickn33/agentic-awesome-skills **aggregates the exact same upstream sources** as your current `.antigravity-install-manifest.json`. 27 of your 29 skills have direct name matches in sickn33. addyosmani has fewer direct collisions but significant *semantic* overlap.

### 3.2 System-Prompt Bloat & Context Cost

| Factor | Current (29 skills) | + addyosmani (24) | + sickn33 (subset) |
|--------|---------------------|-------------------|-------------------|
| **Available skills in system prompt** | 29 | 53 | 29 + N |
| **Est. token cost (skill descriptions)** | ~15-20K tokens | ~30-40K tokens | Linear growth |
| **Trigger dilution risk** | Low | Medium | High if >50 |
| **Skill selection latency** | Fast | Slower | Degrades with count |

**OpenCode behavior:** The `available_skills` block in the system prompt lists *all* discovered skills. Each skill's `description` field is included. Adding 24 skills from addyosmani adds ~15K tokens. Adding even 50 from sickn33 adds ~30K+ tokens.

### 3.3 Duplicate-Name Resolution Order

OpenCode's `skill` tool loads skills by scanning `.agents/skills/` directories. **Resolution is filesystem-order dependent** (non-deterministic across OS). If two folders have the same `name` in frontmatter:
- First one loaded wins (undefined behavior)
- No namespacing or conflict resolution built in
- **Risk:** Silent shadowing — you may invoke the wrong skill

### 3.4 Conflict with `.skill-lock.json` (v3)

| Aspect | Current State | Risk |
|--------|---------------|------|
| **Tracked skills** | Only `find-skills` from vercel-labs | Low — most skills unmanaged by Skills CLI |
| **Version tracking** | Folder hash + timestamps | Adding skills manually bypasses lockfile |
| **Update mechanism** | `npx skills update` | Won't detect manually added skills |
| **Dismissed agents** | 13 agents listed | Unrelated to skill conflicts |

**Conclusion:** Manual skill addition creates "unmanaged copies" — the lockfile becomes stale. Either adopt the Skills CLI fully or accept manual manifest maintenance.

### 3.5 Conflict with ECL Harness

| ECL Rule | Skill Addition Impact |
|----------|----------------------|
| Single active change | Adding 24+ skills = multi-file change → **requires ECL change** |
| `harness/changes/INDEX.json` auto-generated | New skills won't appear in INDEX unless change is archived |
| Context loading order | New skills auto-loaded → may alter agent behavior mid-change |
| `lint-ecl.ps1` validation | No skill-specific lints today — gap |

---

## 4. Verified Facts: Skill Discovery & AGENTS.md

| Question | Answer | Evidence |
|----------|--------|----------|
| Does OpenCode require `opencode.json` to discover skills? | **No** | No such file exists in repo; addyosmani docs confirm filesystem scan |
| Does AGENTS.md need to list skills? | **No** | AGENTS.md is for *instructions*, not inventory |
| What triggers skill loading? | Presence of `SKILL.md` in `.agents/skills/<name>/` | OpenCode `skill` tool scans directory at session start |
| Can skills be added without touching AGENTS.md? | **Yes** | Just drop folder in `.agents/skills/` |
| Does `.skill-lock.json` control discovery? | **No** | Only used by `npx skills` CLI for update tracking |

**Conclusion:** AGENTS.md is **not** a skill registry. It's an *agent instruction file*. Skills are discovered purely by filesystem convention.

---

## 5. Recommended Workaround: Add Skills Without Modifying AGENTS.md

### 5.1 Core Principle

> **Drop skill folders into `.agents/skills/` + update `.antigravity-install-manifest.json` = zero AGENTS.md changes required.**

### 5.2 Prerequisite Checks

| Check | Tool/Method | Pass Criteria |
|-------|-------------|---------------|
| Name collision scan | `ls .agents/skills/` + grep frontmatter `name:` | No duplicate `name` values |
| SKILL.md format validation | `skill-check` skill (if installed) or manual review | Valid YAML frontmatter + required sections |
| License compatibility | Check upstream `LICENSE` or frontmatter `license` | MIT/Apache-2.0/BSD-3 compatible |
| Security review | `aptratcn/skill-audit` skill or manual scan | No shell injection, no secret exfiltration, no excessive permissions |
| Upstream source health | GitHub stars, recent commits, issue response | >100 stars, commits <6 months, active maintainer |

### 5.3 Staging Area Structure

```
.agents/
├── skills-staging/          # ← NEW: staging directory (gitignored)
│   ├── candidate-skill-1/
│   │   └── SKILL.md
│   └── candidate-skill-2/
│       └── SKILL.md
├── skills/                  # ← production (auto-discovered)
│   ├── existing-skill-1/
│   └── ...
└── .antigravity-install-manifest.json
```

### 5.4 Vetting Checklist (Per Skill)

```markdown
## Skill Vetting Record: <skill-name>

- [ ] **Name collision check**: `name:` in frontmatter unique vs `.agents/skills/*/SKILL.md`
- [ ] **Format compat**: Frontmatter has `name`, `description`; body has `When to Use`, `Process`, `Verification`
- [ ] **License**: Upstream license recorded; compatible with project (MIT/Apache-2.0/BSD-3)
- [ ] **Security**: No `bash`/`shell` commands with user input; no network calls to unknown hosts; no secret handling
- [ ] **Source health**: Stars >100, commits <6mo, issues responded
- [ ] **Dependencies**: Documents any external tools (CLI, MCP servers) — note in `tools[]` if using sickn33 format
- [ ] **ECL alignment**: Skill doesn't mandate multi-file changes without ECL awareness
```

### 5.5 Install Procedure

```powershell
# 1. Stage candidate skills
mkdir .agents/skills-staging
# Copy skill folders from source (git clone / download / submodule)

# 2. Run vetting checklist (manual or scripted)
# 3. For each approved skill:
Copy-Item ".agents/skills-staging/<skill>" ".agents/skills/<skill>" -Recurse

# 4. Update antigravity manifest
$manifest = Get-Content .agents/skills/.antigravity-install-manifest.json | ConvertFrom-Json
$manifest.entries += "<skill-name>"
$manifest.updatedAt = (Get-Date).ToString("o")
$manifest | ConvertTo-Json -Depth 5 | Set-Content .agents/skills/.antigravity-install-manifest.json

# 5. (Optional) Update .skill-lock.json if using Skills CLI
# npx skills add <source> --skill <skill-name>  # will update lockfile

# 6. Validate load
opencode --skill-test  # or start session and verify `skill` tool lists it
```

### 5.6 Validation Steps

| Step | Command | Expected |
|------|---------|----------|
| 1. Filesystem check | `Test-Path ".agents/skills/<skill>/SKILL.md"` | True |
| 2. Frontmatter parse | `grep -A5 "^---" ".agents/skills/<skill>/SKILL.md"` | Valid YAML |
| 3. OpenCode discovery | Start OpenCode session; check `available_skills` includes `<skill>` | Listed |
| 4. Skill invocation | Ask agent: "Use <skill> for X" | Agent loads and follows skill |
| 5. No regression | Run existing skill tests (if any) | Pass |

### 5.7 Rollback Procedure

```powershell
# Remove skill folder
Remove-Item ".agents/skills/<skill>" -Recurse -Force

# Update manifest
$manifest = Get-Content .agents/skills/.antigravity-install-manifest.json | ConvertFrom-Json
$manifest.entries = $manifest.entries | Where-Object { $_ -ne "<skill-name>" }
$manifest.updatedAt = (Get-Date).ToString("o")
$manifest | ConvertTo-Json -Depth 5 | Set-Content .agents/skills/.antigravity-install-manifest.json

# Verify removal
opencode --skill-test  # skill no longer listed
```

### 5.8 Documentation Policy (Outside AGENTS.md)

Create **`docs/SKILL_CURATION_POLICY.md`** (not in AGENTS.md):

```markdown
# Skill Curation Policy

## Adding New Skills

1. Stage in `.agents/skills-staging/`
2. Complete vetting checklist (Section 5.4)
3. Copy to `.agents/skills/`
4. Update `.agents/skills/.antigravity-install-manifest.json`
5. Validate via OpenCode session
6. Record in this doc: skill name, source, date, vetting result

## Removing Skills

1. Remove from `.agents/skills/`
2. Update manifest
3. Record removal reason here

## Conflict Resolution

- **Name collision**: Prefix with source (e.g., `addyo-test-driven-development` vs `matt-tdd`)
- **Semantic overlap**: Keep the more specific/maintained one; document decision here
- **Lockfile drift**: Run `npx skills update` quarterly; reconcile manifest

## Current Inventory

| Skill | Source | Added | Vetted By | Status |
|-------|--------|-------|-----------|--------|
| ... | ... | ... | ... | Active |
```

---

## 6. Execution Plan: Sequencing, Parallelization & Ownership

### 6.1 Phase 1: Preparation (Serial — Chief of Staff)

| Step | Owner | Duration | Dependencies |
|------|-------|----------|--------------|
| 1.1 Create `SKILL_CURATION_POLICY.md` | Chief of Staff | 30 min | — |
| 1.2 Create `.agents/skills-staging/` (gitignore) | Chief of Staff | 5 min | 1.1 |
| 1.3 Audit current 29 skills for format consistency | Chief of Staff | 1 hr | — |
| 1.4 Document current name→source mapping | Chief of Staff | 30 min | 1.3 |

### 6.2 Phase 2: Candidate Evaluation (Parallel — Specialist Agents)

| Step | Owner | Duration | Dependencies |
|------|-------|----------|--------------|
| 2.1 Fetch addyosmani 24 skills to staging | **generator-owner** | 15 min | 1.2 |
| 2.2 Fetch sickn33 target skills to staging | **generator-owner** | 30 min | 1.2 |
| 2.3 Run name collision matrix (automated) | **registry-owner** | 10 min | 2.1, 2.2 |
| 2.4 Run format validation on all candidates | **generator-owner** | 20 min | 2.1, 2.2 |
| 2.5 License scan (automated) | **caio** | 15 min | 2.1, 2.2 |
| 2.6 Security audit (skill-audit or manual) | **cto** | 1 hr | 2.1, 2.2 |
| 2.7 Source health check | **coo** | 30 min | 2.1, 2.2 |

> **Parallelization:** Steps 2.1–2.2 can run in parallel. Steps 2.3–2.7 can run in parallel after 2.1/2.2 complete.

### 6.3 Phase 3: Selection & Approval (Serial — Human + Chief of Staff)

| Step | Owner | Duration | Dependencies |
|------|-------|----------|--------------|
| 3.1 Present collision/overlap matrix to human | Chief of Staff | 30 min | 2.3 |
| 3.2 Human selects approved skills (per repo) | **Human** | — | 3.1 |
| 3.3 Record decisions in `SKILL_CURATION_POLICY.md` | Chief of Staff | 15 min | 3.2 |

### 6.4 Phase 4: Installation (Parallel per skill — generator-owner)

| Step | Owner | Duration | Dependencies |
|------|-------|----------|--------------|
| 4.1 Copy approved skills to `.agents/skills/` | **generator-owner** | 5 min/skill | 3.2 |
| 4.2 Update `.antigravity-install-manifest.json` | **generator-owner** | 1 min/skill | 4.1 |
| 4.3 (Optional) `npx skills add` for lockfile sync | **generator-owner** | 2 min/skill | 4.1 |
| 4.4 Validate each skill loads in OpenCode | **generator-owner** | 3 min/skill | 4.1 |

> **Parallelization:** Each skill's 4.1–4.4 can run in parallel across skills. Total wall time ≈ 10 min for 10 skills.

### 6.5 Phase 5: Integration Testing (Serial — Chief of Staff + cto)

| Step | Owner | Duration | Dependencies |
|------|-------|----------|--------------|
| 5.1 Full OpenCode session: verify `available_skills` count | Chief of Staff | 10 min | 4.4 |
| 5.2 Trigger each new skill via natural language | **cto** | 5 min/skill | 5.1 |
| 5.3 Run existing test suite (pytest, lint) | **cto** | 10 min | 5.1 |
| 5.4 Run `lint-ecl.ps1` | Chief of Staff | 5 min | 5.3 |

### 6.6 Phase 6: ECL Change Closure (Chief of Staff)

| Step | Owner | Duration | Dependencies |
|------|-------|----------|--------------|
| 6.1 Create ECL change for skill batch add | Chief of Staff | 10 min | 5.4 |
| 6.2 Archive change → rebuild INDEX.json | Chief of Staff | 5 min | 6.1 |
| 6.3 Update `docs/STATUS.md` | Chief of Staff | 10 min | 6.2 |

---

## 7. Open Questions Requiring Human Decision

| # | Question | Options | Recommendation |
|---|----------|---------|----------------|
| **Q1** | Which repo(s) to pull from? | A) addyosmani only (24, curated)<br>B) sickn33 only (selective, ~50)<br>C) Both (hybrid)<br>D) Neither | **A** — addyosmani is curated, lifecycle-aligned, has OpenCode guide, MIT license, active maintenance. sickn33 is an aggregator with duplicate-name minefield. |
| **Q2** | How to handle semantic overlaps (e.g., `tdd` vs `test-driven-development`)? | A) Keep both, rename one<br>B) Keep existing, skip candidate<br>C) Replace existing with candidate<br>D) Namespace: `addyo-test-driven-development` | **B** for most — your existing skills are battle-tested in this repo. Only adopt candidate if it adds distinct value (e.g., `using-agent-skills` meta-skill). |
| **Q3** | Adopt Skills CLI (`npx skills`) for future management? | A) Yes — full adoption<br>B) No — manual manifest only<br>C) Hybrid — CLI for addyosmani, manual for others | **A** — addyosmani skills are designed for the CLI; lockfile stays current; updates automated. |
| **Q4** | Namespace convention for collision avoidance? | A) Prefix with source (`addyo-`, `matt-`, `sick-`)<br>B) Suffix with source (`-addyo`, `-matt`)<br>C) Keep original names, accept risk<br>D) Curate to zero collisions | **A** — explicit, searchable, matches sickn33's `source_repo` metadata. |
| **Q5** | Maximum skill count before context degradation? | A) 40 (current + 11)<br>B) 50<br>C) 60<br>D) No limit | **A** — ~40 keeps system prompt ~25K tokens; beyond 50 triggers measurable latency. |
| **Q6** | Should `using-agent-skills` meta-skill be installed? | A) Yes — enables auto-routing<br>B) No — conflicts with `find-skills`<br>C) Yes, but rename to `addyo-using-agent-skills` | **C** — valuable for agent-driven workflow; rename to avoid collision with your `find-skills`. |
| **Q7** | Create ECL change for this batch or individual skills? | A) Single batch change<br>B) One change per skill<br>C) One change per repo | **A** — single batch is atomic, simpler INDEX, cleaner STATUS. |

---

## Appendix A: Addyosmani Skills Recommended for Adoption (No Direct Collision)

| Skill | Phase | Why Valuable Here |
|-------|-------|-------------------|
| `using-agent-skills` | Meta | Auto-routes tasks to skills — reduces manual selection |
| `interview-me` | Define | Extracts real requirements before spec — prevents assumption bugs |
| `idea-refine` | Define | Structured ideation — useful for greenfield features |
| `spec-driven-development` | Define | PRD-before-code — aligns with your ECL "spec before implement" |
| `planning-and-task-breakdown` | Plan | Atomic tasks with acceptance criteria — fits ECL task decomposition |
| `incremental-implementation` | Build | Vertical slices + feature flags — safe deployment |
| `context-engineering` | Build | Right context at right time — reduces token waste |
| `source-driven-development` | Build | Doc-verified code — reduces hallucination |
| `doubt-driven-development` | Build | Adversarial review — catches high-stakes errors |
| `frontend-ui-engineering` | Build | Production UI standards — if you do frontend |
| `api-and-interface-design` | Build | Contract-first APIs — complements your `api-endpoint-builder` |
| `browser-testing-with-devtools` | Verify | Chrome DevTools MCP — runtime verification |
| `debugging-and-error-recovery` | Verify | Structured debugging — complements `diagnosing-bugs` |
| `code-review-and-quality` | Review | Five-axis review — quality gate before merge |
| `code-simplification` | Review | Chesterton's Fence — reduces complexity |
| `security-and-hardening` | Review | OWASP Top 10 — security gate |
| `performance-optimization` | Review | Measure-first — complements `performance-optimizer` |
| `git-workflow-and-versioning` | Ship | Atomic commits, clean history |
| `ci-cd-and-automation` | Ship | Shift Left, quality gates |
| `deprecation-and-migration` | Ship | Code-as-liability — retirement discipline |
| `documentation-and-adrs` | Ship | ADRs — architectural memory |
| `observability-and-instrumentation` | Ship | RED metrics, OpenTelemetry |
| `shipping-and-launch` | Ship | Pre-launch checklist, rollback |

**Total: 23 skills (excluding meta-skill)** — all fill gaps in your current lifecycle coverage.

---

## Appendix B: Sickn33 Skills Worth Cherry-Picking (If Opting In)

| Skill | Upstream Source | Value Add |
|-------|-----------------|-----------|
| `agent-memory-mcp` | webzler/agentMemory | MCP-based memory — complements `tree-ring-memory` |
| `spec-driven-development` | addyosmani (aggregated) | Same as addyosmani original |
| `test-driven-development` | addyosmani (aggregated) | Same as addyosmani original |
| `code-review-and-quality` | addyosmani (aggregated) | Same as addyosmani original |
| `architect-review` | Various | Architecture review persona |
| `security-audit` | cloudflare/security-audit-skill | Production security audit |
| `performance-audit` | brendangregg-use-tsa | USE/TSA method — deep perf analysis |

> **Warning:** Each requires individual vetting; name collisions guaranteed with your existing 29.

---

*End of Report*
