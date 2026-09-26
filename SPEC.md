# LightSpeed AI Company Builder v2 — Implementation Specification

**Source:** 9 architecture artifacts under `docs/architecture/` + `LIGHTSPEED_AI_COMPANY_BUILDER_WEB_ARCHITECTURE_V2.md` (primary)
**Target:** P2–P7 implementation phases per `V2_IMPLEMENTATION_ROADMAP.md`
**Constraint:** Zero legacy patterns in new code; every change traceable to an architecture ruling

---

## Phase P2 — Registry Schema + Public Transform (Artifacts 2, 3, 5)

### P2.1 — Extend Registry Schema (Artifact 2: `AI_WORKFORCE_90.md` §5.1)

**Task:** Add 7 MANDATORY fields to `company-registry.yaml` for all 90 agents

| Field | Type | Validation |
|-------|------|------------|
| `decision_rights` | `list[string]` | ≥1 item; non-empty strings |
| `kpis` | `list[string]` | ≥1 item; references `company/config/kpis.yaml` keys |
| `approval_level` | `enum` | `self \| lead \| exec \| ceo \| board` |
| `escalation_path` | `list[string]` | Ordered IDs; terminal = `human_ceo` or `board` |
| `workflows` | `list[string]` | Workflow IDs from registry |
| `inputs` | `list[string>` | Artifact/event IDs consumed |
| `outputs` | `list[string>` | Artifact/event IDs produced |

**Acceptance Criteria:**
- [ ] `company-registry.yaml` has all 7 fields on all 90 entries
- [ ] Registry validator (`src/ai_company/registry/validator.py`) fails fast on missing MANDATORY fields
- [ ] `ruff check src/ && mypy src/ && pytest` pass
- [ ] `python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` regenerates 90 cards without error

### P2.2 — Build Public Transform (Artifact 5: `PUBLIC_AGENT_REGISTRY_SCHEMA.md`)

**Task:** Create transform pipeline `company-registry.yaml` → `src/data/generated/agent-registry.public.json`

**Pipeline Steps (per Artifact 5 §5):**
1. Load `company-registry.yaml` + `company/departments.yaml`
2. Validate counts: 90 agents, 20 departments, type census 19/64/7
3. Allowlist project per §3 field map (ALLOW only)
4. Strip legacy tools: remap `write`→`edit`, `execute`→`bash`, `delegate`→`task`; reject `code_interpreter`
5. Optional joins: KPI labels by department; `decision_rights` when present
6. PII/content filter pass
7. Write `src/data/generated/agent-registry.public.json` with envelope (schema_version, generated_at, meta.counts)
8. JSON Schema validate + denylist grep

**Acceptance Criteria:**
- [ ] `src/data/generated/agent-registry.public.json` exists with 90 agents, 20 departments
- [ ] Zero occurrences of: `guidelines`, `permission`, `model_tier`, `approval_level`, `escalation_path`, `initialTasks`, `initialApprovals`, `initialEscalations`, `write`, `execute`, `delegate`, `code_interpreter`, `web_search`, `DASHBOARD_`, `API_KEY`, `llm_cost`
- [ ] All `tools[]` values ∈ canonical 7: `read`, `edit`, `grep`, `list`, `bash`, `webfetch`, `task`
- [ ] `PublicAgent` TypeScript interface in `src/types.ts` matches JSON Schema (no `guidelines`, `permission`)
- [ ] CI gate: `grep -r "company/agent-registry.json" src/` returns empty

### P2.3 — Swap Public Data Import (Artifact 3: `PUBLIC_INTERNAL_BOUNDARY.md` V1–V5)

**Task:** Update `src/data/companyData.ts` to import only public artifact

**Changes:**
- Remove `import rawAgents from '../../company/agent-registry.json'`
- Add `import publicRegistry from './generated/agent-registry.public.json'`
- Transform `publicRegistry.agents` → `agentsList` (typed as `PublicAgent[]`)
- Remove `initialTasks`, `initialApprovals`, `initialEscalations`, `initialKPIs`, cost/model-tier data from module
- Move operational fixtures to internal-only module (or delete)

**Acceptance Criteria:**
- [ ] `src/data/companyData.ts` has no import of `company/agent-registry.json`
- [ ] `agentsList` typed as `PublicAgent[]` (from `src/types.ts`)
- [ ] Zero forbidden fields in `companyData.ts` exports
- [ ] Builder UX components (`AiCompanyBuilderSection`, `HaomtgvGovernanceFramework`, `AgentModal`) consume `agentsList` without type errors

---

## Phase P3 — Route / IA Migration (Artifacts 4, 6)

### P3.1 — Vercel Edge Redirects (Artifact 6: `ROUTE_MIGRATION_V2.md` M1–M3)

**Task:** Update `vercel.json` with single-hop redirects

**Required Redirects:**
```json
{
  "redirects": [
    { "source": "/offerings", "destination": "/solutions", "permanent": true },
    { "source": "/work", "destination": "/proof", "permanent": true },
    { "source": "/evidence", "destination": "/proof", "permanent": true },
    { "source": "/industries", "destination": "/sectors", "permanent": true },
    { "source": "/technology", "destination": "/what-we-do", "permanent": true },
    { "source": "/why", "destination": "/about", "permanent": true },
    { "source": "/process", "destination": "/what-we-do", "permanent": true },
    { "source": "/geography", "destination": "/about", "permanent": true },
    { "source": "/leadership", "destination": "/about", "permanent": true },
    { "source": "/deliverables", "destination": "/what-we-do", "permanent": true },
    { "source": "/outcomes", "destination": "/proof", "permanent": true },
    { "source": "/partnerships", "destination": "/about", "permanent": true },
    { "source": "/trust", "destination": "/proof", "permanent": true },
    { "source": "/how-we-help", "destination": "/what-we-do", "permanent": true },
    { "source": "/how-we-help/engagement", "destination": "/what-we-do", "permanent": true }
  ]
}
```

**Acceptance Criteria:**
- [ ] `curl -I https://<host>/offerings` → single 301 to `/solutions`
- [ ] `curl -I https://<host>/work` → single 301 to `/proof`
- [ ] No double-hop chains (edge → SPA → final)

### P3.2 — SPA Route Table (Artifact 4: `WEB_INFORMATION_ARCHITECTURE_V2.md` §4)

**Task:** Update `src/App.tsx` to v2 route table (20 first-class routes)

**Keep (15):** `/`, `/what-we-do`, `/proof`, `/solutions`, `/solutions/:slug`, `/sectors`, `/sectors/:slug`, `/insights`, `/about`, `/ai-company-builder`, `/ask`, `/contact`, `/legal/privacy`, `/legal/terms`, `/faq`, `/resources`, `/events`, `/news`, `/careers`

**Create (3):** `/solutions` (live index), `/sectors` (live index), `/sectors/:slug`

**Remove SPA Navigate entries** for all redirected paths

**Acceptance Criteria:**
- [ ] All 20 keep/create routes render without 404
- [ ] No `<Navigate>` entries for redirected paths
- [ ] `/solutions` renders live index of 5 solution cards linking to `/solutions/:slug`
- [ ] `/sectors` renders live index of 5 sector cards linking to `/sectors/:slug`

### P3.3 — Footer / Navigation Link Fixes (Artifact 4 §4.1)

**Task:** Fix broken slug references in `SiteFooter.tsx`, `SiteLayout.tsx`, `PillarNavigationCard.tsx`

**Canonical Slugs:**
- Solutions: `ai-company-builder`, `digital-presence`, `business-automation`, `enterprise-deployment`, `boardroom-briefing`
- Sectors: `financial-services`, `healthcare`, `agriculture`, `education`, `government`

**Acceptance Criteria:**
- [ ] All footer/solution links resolve to valid routes
- [ ] `ROUTE_TITLES` in `SiteLayout.tsx` uses only canonical slugs
- [ ] No references to `agentic-ai`, `digital-transformation`, `data-intelligence`, `automation`, `strategy-advisory`, `development`

---

## Phase P4 — AI Company Builder UX (Artifact 8: `AI_COMPANY_BUILDER_UX.md`)

### P4.1 — Five-Mode Switcher (Artifact 8 §3.1)

**Task:** Replace stacked tab chrome with single URL-synced mode switcher

**Modes:** Organization, Agent, Operations, Intelligence, Governance
**URL Sync:** Hash-based (`#organization`, `#agent`, `#operations`, `#intelligence`, `#governance`)
**Component Map:**
- Organization → Infographic + Dept browser (`HaomtgvGovernanceFramework`)
- Agent → Agent list + `AgentModal`
- Operations → Journey (01–04) + Simulated CLI + IaC tree
- Intelligence → Decision engine + Memory types
- Governance → HAOMTGV framework + 5-tier HITL

**Acceptance Criteria:**
- [ ] Single mode switcher (tablist pattern, arrow-key nav, visible focus ring)
- [ ] Mode reflected in URL hash; shareable links work
- [ ] Inner tabs (OsExplorer) demoted to secondary panels within modes
- [ ] `#governance` fragment frozen (deep-link target from all modes)

### P4.2 — AgentModal Refinement (Artifact 8 §5.3)

**Task:** Make `AgentModal` keyboard-trap-safe with canonical tools only

**Changes:**
- Focus trap, Escape to close, `role="dialog"`, restore focus to invoker
- Tools display: only canonical 7 (`read`, `edit`, `grep`, `list`, `bash`, `webfetch`, `task`)
- `onDispatchTask` prop: demo-only if shown; label clearly
- Consumes `PublicAgent` type (post-P2)

**Acceptance Criteria:**
- [ ] Modal passes axe-core accessibility audit
- [ ] No legacy tool names in modal display
- [ ] Keyboard-only navigation works end-to-end

### P4.3 — Simulated CLI Demo Labeling (Artifact 8 §5.2, §6)

**Task:** Explicitly label all CLI demos as non-production

**Changes:**
- Add badge "Interactive demo · not a live session" on CLI panel
- Hard-code output numbers to match source-of-truth (90 agents, 20 depts, 2,373 tests)
- No fake "deployment success" messages for real tenants

**Acceptance Criteria:**
- [ ] CLI demo panel shows demo badge
- [ ] Output numbers match `docs/source-of-truth.yaml`
- [ ] No success/failure messages implying real tenant operations

### P4.4 — Ask LightSpeed (Artifact 8 §4.3)

**Task:** Promote `/ask` to nav CTA (Option A); refine step machine

**Changes:**
- Add Ask button to primary nav (FloatingNav)
- Sector options in context step match `industries[]` slugs exactly
- Results only show solutions from canonical 5 slugs
- Empty match → honest empty state + briefing CTA
- Full keyboard path; `aria-live` on assistant turns

**Acceptance Criteria:**
- [ ] Ask accessible from homepage nav
- [ ] Sector picker uses canonical 5 slugs
- [ ] No fabricated solution cards on empty match
- [ ] Keyboard + screen reader tested

---

## Phase P5 — Evidence / Content (Artifact 7: `EVIDENCE_ARCHITECTURE.md`)

### P5.1 — Proof Consolidation (Artifact 7 §2, §4.2)

**Task:** Merge `/work`, `/evidence`, `/outcomes`, `/trust` content into `/proof` sections

**Section Map:**
- `#metrics` — Platform metrics (single-sourced from `source-of-truth.yaml`)
- `#honesty` — Honesty ladder (from `honestyPolicy[]`)
- `#cases` — Case studies (from `workCaseStudies[]`, rename to `proofCaseStudies`)
- `#outcomes` — Outcomes (from `outcomeCategories[]`)
- `#trust` — Trust band (from `trustEvidence[]`)
- `#policy` — Policy track (from `workPolicy[]`, rename to `proofPolicy`)
- `#verify` — How to verify (code review, governance walkthrough, governed pilot)

**Acceptance Criteria:**
- [ ] `/proof` renders all 7 sections with correct anchors
- [ ] `PLATFORM_METRICS` extracted from `ProofPage.tsx` → shared export keyed to drift values
- [ ] Zero hard-coded metric values in page components
- [ ] `TrustPage` link updated from `/evidence` to `/proof#trust`

### P5.2 — Stale Count Sweep (Artifact 7 §6.4, Artifact 2 §7.3)

**Task:** Remove all non-historical 145/152/140+ claims from public copy

**Targets:**
- `EXECUTIVE-STRATEGY-EXPANSION.md` ("145 specialized agents")
- Homepage About band ("140+ AI Agents")
- Remote GitHub README (152/151)
- `docs/source-of-truth.yaml` comment about missing Pharos
- Any new architecture docs

**Acceptance Criteria:**
- [ ] `grep -r "145 agent\|152 agent\|140+ agent" src/data/ docs/architecture/` → only historical footnotes
- [ ] Remote README synced to 90 agents / 20 departments
- [ ] CI grep gate blocks merge on stale counts in non-history files

---

## Phase P6 — Governance Hardening (Artifacts 2, 3)

### P6.1 — Single-Owner Violation V1 (Artifact 2 §6.1, Primary Doc Ruling 3)

**Task:** Resolve `cso` dual department executive

**Options (Architecture Lead decides):**
- A: `head_of_business_development` = sole executive of `business_development`; `cso` = sole executive of `strategy`
- B: Document dual mandate with separate KPIs per department

**Acceptance Criteria:**
- [ ] `company/departments.yaml` has no department with same executive (unless documented)
- [ ] `decision_rights` encoded for both roles per P2.1

### P6.2 — Decision Rights Encoding (Artifact 2 §6.1 V9, V10)

**Task:** Encode `decision_rights` for bounded violations

| Agent | Decision Rights |
|-------|-----------------|
| `qa_lead` | Quality policy, gates, release criteria |
| `test_engineering_lead` | Automation, evaluation execution, CI health |
| `fullstack_engineer` | Intake routing rule documented (matrix R7) |

**Acceptance Criteria:**
- [ ] `decision_rights` populated for all 90 agents (per P2.1)
- [ ] V9/V10 explicitly encoded; no shared accountability

### P6.3 — Boundary Enforcement Automation (Artifact 3 §7 Q10)

**Task:** Wire PII/content filter on transform egress; CI assertion on internal imports

**Acceptance Criteria:**
- [ ] Transform pipeline step 7 (PII filter) runs and passes
- [ ] CI fails on any `import ... from '../../company/agent-registry.json'` in `src/`
- [ ] Public artifact passes denylist scan (P2.2 criteria)

---

## Phase P7 — QA + Release (Artifact 9 §6)

### P7.1 — Verification Matrix

| Check | Command | Expected |
|-------|---------|----------|
| Lint + Typecheck | `ruff check src/ && mypy src/` | Clean |
| Tests | `pytest` | All pass |
| Drift | `pwsh scripts/validate-drift.ps1` | 90/20 green |
| Redirect Matrix | `pwsh scripts/verify-redirects.ps1` | All single-hop |
| Boundary | `pwsh scripts/validate-architecture.ps1` | Zero violations |
| Count Audit | `pwsh scripts/lint-ecl.ps1` | Clean |
| Accessibility | `npm run a11y` (Playwright) | WCAG AA |

### P7.2 — Canonical Host Cutover (Artifact 3 Ruling 4)

**Task:** Declare Vercel SPA from `main` as sole production origin; redirect/re-scope `ai.studio`

**Acceptance Criteria:**
- [ ] Production traffic serves from Vercel `main` build
- [ ] `lightspeedholdings.ai.studio` redirects or re-scoped
- [ ] Remote GitHub README shows 90 agents / 20 departments

---

## Cross-Cutting Constraints (All Phases)

1. **No legacy tool names** in any new public surface (canonical 7 only)
2. **No hard-coded counts** — all metrics read from `source-of-truth.yaml` or public artifact
3. **Honesty badges** on all claim-bearing surfaces (ADR-020)
4. **Demo labeling** on all simulated CLI/builder outputs
5. **Accessibility** — WCAG AA on all new/modified components
6. **Brand tokens only** — navy `#070A40`, red `#E63946`, cyan `#00BFFF`, Arial scale

---

## Traceability Matrix

| Architecture Artifact | Spec Sections | Key Rulings |
|----------------------|---------------|-------------|
| `AI_WORKFORCE_90.md` | P2.1, P6.1, P6.2 | 90/20 canonical; 7 MANDATORY fields; V1 resolution |
| `PUBLIC_INTERNAL_BOUNDARY.md` | P2.2, P2.3, P6.3 | NEVER/EXPOSE lists; V1–V5 violations; transform pipeline |
| `PUBLIC_AGENT_REGISTRY_SCHEMA.md` | P2.2 | Field map; JSON Schema; sink path `src/data/generated/` |
| `WEB_INFORMATION_ARCHITECTURE_V2.md` | P3.2, P3.3, P5.1 | Route table; homepage 13 sections; slug canon |
| `ROUTE_MIGRATION_V2.md` | P3.1 | Single-hop redirects; edge destination = SPA final |
| `EVIDENCE_ARCHITECTURE.md` | P5.1, P5.2 | `/proof` consolidation; lifecycle; HITL tiers |
| `AI_COMPANY_BUILDER_UX.md` | P4.1–P4.4 | Five modes; journeys; AgentModal; Ask; demo labeling |
| `AGENT_CONSOLIDATION_152_TO_90.md` | P2.1 (context) | Migration matrix; residual risks R1–R10 |
| `V2_IMPLEMENTATION_ROADMAP.md` | All | Phase dependencies; risk register; DoD |

---

## Definition of Done (Per Phase)

**P2 Done:**
- [ ] Registry schema extended + validator fail-fast
- [ ] Public transform pipeline runs in CI, emits valid artifact
- [ ] `src/` imports only public artifact; zero internal registry imports
- [ ] All 3 verification commands pass

**P3 Done:**
- [ ] Vercel redirects single-hop; SPA routes match v2 table
- [ ] Footer/nav links use canonical slugs only
- [ ] Redirect verification script passes

**P4 Done:**
- [ ] Five-mode switcher live with URL sync
- [ ] AgentModal accessible + canonical tools only
- [ ] CLI demos labeled; Ask promoted to nav

**P5 Done:**
- [ ] `/proof` has 7 sections; metrics single-sourced
- [ ] Stale count sweep clean (CI gate passes)
- [ ] Dead page prose salvaged before deletion

**P6 Done:**
- [ ] V1 resolved; decision_rights encoded for all 90
- [ ] Boundary CI checks pass (no internal imports, PII filter)

**P7 Done:**
- [ ] Full verification matrix green
- [ ] Canonical host declared; remote README synced
- [ ] CHANGELOG updated; follow-up ECL closed
