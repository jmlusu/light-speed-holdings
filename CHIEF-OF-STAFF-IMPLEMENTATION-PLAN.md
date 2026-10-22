# Chief-of-Staff Implementation Plan: Organization Name Change
## Mandate: "LightSpeed Holdings Limited" — Effective Immediately

**Owner:** Chief of Staff (primary orchestrator and strategic alignment agent)
**Sponsor:** Human CEO
**Decision Rights:** Chief of Staff — Align company goals across all departments; Orchestrate agent communication and task delegation; Monitor operational bottlenecks

---

## 1) Departmental Responsibilities and Ownership

| Department | Owner | Responsibilities | Priority |
|-----------|-------|-----------------|----------|
| **Executive** | Chief of Staff | Overall coordination, escalation to CEO, progress tracking, final sign-off on all changes | P0 — Executive sponsorship |
| **Technology** | CTO / Registry Owner | Update company-registry.yaml (source of truth), company.yaml, agent-registry.json, all JSON configs, source code files (.ts, .tsx, .py), dashboard title and branding | P0 — System of record |
| **Product** | CPO | Update product-related docs, templates, generators, whitepapers; ensure consistency across pitch decks, board meetings, social assets | P0 — Public-facing product assets |
| **Marketing** | CMO / Marketing Owner | Update all public-facing documentation, website content, social media profiles, brand materials, marketing collateral, SEO/SEM references | P0 — Public-facing brand integrity |
| **Legal** | CLO / Legal Owner | Update legal_name field, ensure contractual references are consistent, review Inc. → Limited transition implications, validate compliance | P0 — Legal compliance |
| **Operations** | COO / Workflow Owner | Update internal process docs, SOPs, organizational charts, RACI matrices, dashboards, KPI collectors | P1 — Internal operations |
| **Customer Success** | Head of CS | Update customer-facing materials, onboarding docs, success metrics references, playbooks | P1 — Customer-facing consistency |
| **Sales** | Head of Sales | Update sales decks, proposal templates, outreach materials, pipeline docs | P1 — Sales enablement |
| **Data & Analytics** | CDO | Update data dictionaries, semantic layers, metric definitions, dashboards referencing company name | P1 — Data consistency |
| **Human Resources** | CHRO | Update internal policies, employee-facing materials, organizational charts, role definitions | P2 — Internal HR systems |
| **Pharos / Thought Leadership** | Thought Leadership Lead | Update thought-leadership assets, Pharos publications, CEO speaking materials, external positioning | P2 — External reputation |

### Key Cross-Dependencies

| Dependency | blocking | blocked by |
|------------|----------|------------|
| Technology → Product | registry.yaml changes required before template updates | product can template-generation after registry update |
| Technology → Marketing | source code/website updates before public comms | marketing can coordinate messaging while tech works on code |
| Legal → Technology | legal_name validation before registry finalization | tech can proceed with "Limited" placeholder pending legal sign-off |
| Executive → All departments | Chief of Staff orchestrates timeline and dependencies | all departments execute within assigned timelines |

---

## 2) Prioritized Update Sequence

### Phase 1: Core System of Record (Days 1-3)
1. **Update `company-registry.yaml`** — Change `name: Light Speed Holdings` to `name: LightSpeed Holdings Limited` (line 2)
2. **Update `company.yaml`** — Change `name: "Light Speed Holdings"` to `name: "LightSpeed Holdings Limited"` (line 3) and `legal_name: "Light Speed Holdings, Inc."` to `legal_name: "LightSpeed Holdings Limited"` (line 4)
3. **Update `config/company/ai_caas_offers.yaml`** — Fix product description reference (line 9)
4. **Run generator to regenerate agent cards** — `uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"`
5. **Verify `company-registry.yaml` propagates correctly** through the generator

### Phase 2: Brand Assets and Tokens (Days 3-5)
6. **Update `brand/tokens/brand-tokens.json`** — Change `"legalName": "LIGHTSPEED HOLDINGS LIMITED"` to `"legalName": "LIGHTSPEED HOLDINGS LIMITED"` — Note: The new mandate is "LightSpeed Holdings Limited" (capital S, no all-caps in running text, but the legal token uses uppercase for the legal entity name). Need to determine the exact format.
   - *Clarification needed:* The mandate says "LightSpeed Holdings Limited" — should the `legalName` token be `"LightSpeed Holdings Limited"` or `"LIGHTSPEED HOLDINGS LIMITED"`? Given the brand guidelines currently use `LIGHTSPEED HOLDINGS LIMITED` (all-caps), and the mandate says "stylized as LightSpeed Holdings Limited", I recommend keeping the token as `LIGHTSPEED HOLDINGS LIMITED` (all-caps for legal/formal use) but updating all running-text references to use title case "LightSpeed Holdings Limited".
7. **Update `static/brand/tokens/brand-tokens.json`** — Same as above
8. **Update `public/brand/tokens/brand-tokens.json`** — Same as above
9. **Update `brand/guidelines/brand-guidelines.md`** — Change Company Name row from `LIGHTSPEED HOLDINGS LIMITED` to `LightSpeed Holdings Limited`
10. **Update `static/brand/guidelines/brand-guidelines.md`** — Same
11. **Update `public/brand/guidelines/brand-guidelines.md`** — Same
11. **Run brand sync script** — `pwsh scripts/build/sync-brand.ps1` to propagate canonical → mirrors

### Phase 3: Agent Registry and JSON Configs (Days 5-7)
12. **Update `company/agent-registry.json`** — Lines 868, 871: Change `LIGHTSPEED HOLDINGS LIMITED` to `LightSpeed Holdings Limited`
13. **Update `src/data/generated/agent-registry.public.json`** — Lines 1093, 1099, 1102: Same
14. **Update all `.agents/skills/` files** referencing the name (social-media-manager, ls-artifact-qa, pharos-community-ecosystem, pharos-thought-leadership-author)

### Phase 4: Source Code and Website (Days 7-10)
15. **Update `src/ai_company/dashboard/app.py`** — Change title from "Light Speed Holdings — CEO Dashboard" to "LightSpeed Holdings Limited — CEO Dashboard"
16. **Update `src/ai_company/dashboard/templates/base.html`** — Lines 6, 226, 507: Update page title and H1
17. **Update `src/data/homeImmersiveCopy.ts`** — Change heroEyebrow from `'LIGHTSPEED HOLDINGS // AI-NATIVE COMPANY BUILDER'` to `'LightSpeed Holdings Limited // AI-Native Company Builder'`
18. **Update `src/components/SiteLayout.tsx`** — Change document.title from `LIGHTSPEED HOLDINGS | ...` to `LightSpeed Holdings Limited | ...`
19. **Update `src/ai_company/cli/main.py`** — Change `typer.echo("Company: Light Speed Holdings")` to `typer.echo("Company: LightSpeed Holdings Limited")`
20. **Update `src/ai_company/executor/prompts.py`** — Lines 30, 40, 50, 60, 72: Update system prompts referencing company name
21. **Update `src/ai_company/executor/optimized_prompts.py`** — Line 55: Same

### Phase 5: Templates and Generators (Days 10-14)
22. **Update `static/brand/templates/generate-social-assets.py`** — Line 206: Change `company_name = "LIGHTSPEED HOLDINGS LIMITED"` to `company_name = "LightSpeed Holdings Limited"`
23. **Update `static/brand/templates/generate-post-templates.py`** — Line 129: Change `"legalName": "LIGHTSPEED HOLDINGS LIMITED"` to `"legalName": "LightSpeed Holdings Limited"`
24. **Update `static/brand/templates/generate-pitch-deck.py`** — Line 109: Same
25. **Update `static/brand/templates/generate-board-meeting.py`** — Line 90: Same
26. **Update `static/brand/templates/one-pager.html`** — Line 57: Update `<div class="company-name">LightSpeed Holdings Limited</div>`
27. **Update `static/brand/templates/investor-update-email.html`** — Line 37: Update `<div class="header-text">LightSpeed Holdings Limited</div>`
28. **Update `static/brand/templates/email-signature.html`** — Line 29: Update signature text
29. **Update `static/brand/templates/email-signature-team.html`** — Lines 55, 86, 118: Update signature text

### Phase 6: Documentation (Days 14-30)
30. **Update all doc files** referencing the old name (prioritized by customer/public facing status):
   - `docs/MISSION_AND_VISION.md` — legal name format
   - `docs/CEO-DIRECTIVE-BLUEPRINT-ADOPTION.md` — "Light Speed Holdings, Inc." references
   - `docs/BRAND_ADOPTION_ROADMAP.md` — Company Name field
   - `docs/AGENT-REGISTRY-TABLE.md` — Title and references
   - `docs/ORGANIZATION.md` — "Light Speed Holdings is organized as..."
   - All marketing docs, warmup content, provisioning docs
   - All directive files referencing the name
31. **Update dashboard documentation** and CEO guide references
32. **Update task/SEO files** (todo.md, plan.md, etc.)

### Phase 7: Legal and Inc. Transition (Ongoing)
33. **Legal review of "Inc." → "Limited" transition** — Determine if formal filing required
34. **Update legal contracts and agreements** referencing the old entity name
35. **Update Delaware/Malawi company registration** if applicable
36. **Update bank accounts, tax IDs, legal stationary** with new legal name

---

## 3) Coordination Framework

### Steering Committee
- **Chair:** Chief of Staff
- **Members:** Human CEO, CTO, CMO, CLO, COO
- **Meeting Cadence:** Daily standups (Days 1-7), then twice-weekly until completion
- **Decision Authority:** CEO has final sign-off on legal name format; Chief of Staff coordinates implementation

### Communication Channels
| Channel | Purpose | Frequency |
|---------|---------|-----------|
| `#org-name-change` (Slack/Teams) | Real-time coordination, quick questions | As needed |
| Weekly status report | Progress tracking, blockers, decisions | Every Monday |
| Escalation path | Issues requiring CEO board approval | As needed, via Chief of Staff |

### Change Management Process
1. **Change request** — Department submits name change item to Chief of Staff
2. **Impact assessment** — Chief of Staff evaluates cross-departmental dependencies
3. **Scheduled update** — Chief of Staff assigns target date and owner
4. **Execution** — Owner implements change within assigned window
5. **Verification** — Chief of Staff verifies change is complete and consistent
6. **Closure** — Change marked complete in progress tracker

### Synchronization Mechanism
- **Brand sync script** runs after each batch of canonical changes: `pwsh scripts/build/sync-brand.ps1`
- **Git branching** — All changes on a `name-change/<ticket>` branch from `main`
- **PR required** — All changes via pull request with 6 required checks (per `.ai-company\constitution\11-GIT-STANDARDS.md`)
- **Post-merge validation** — `uv run graphify query "company name LightSpeed Holdings Limited"` to verify consistency

---

## 4) Resource Allocation

### Personnel Allocation (per phase)

| Role | FTE Commitment | Duration | Primary Tasks |
|------|---------------|----------|---------------|
| Chief of Staff | 1.0 FTE | Weeks 1-4 | Overall coordination, escalation, progress tracking, final sign-off |
| CTO / Registry Owner | 0.5 FTE | Weeks 1-3 | Registry.yaml, company.yaml, JSON configs, generator updates |
| CMO / Marketing Owner | 0.5 FTE | Weeks 2-5 | Brand guidelines, public docs, social media, marketing collateral |
| CLO / Legal Owner | 0.3 FTE | Weeks 1-4 | Legal name format, Inc. → Limited transition, contract reviews |
| CPO / Product Owner | 0.5 FTE | Weeks 3-6 | Templates, generators, whitepapers, product docs |
| COO / Operations Owner | 0.3 FTE | Weeks 4-7 | Internal SOPs, dashboards, organizational docs |
| Specialized Agents (task delegations) | As needed | Weeks 2-8 | Specific file edits, grep-replace operations, verification |

### Tooling and Infrastructure
- **Git branch**: `name-change/lightspeed-holdings-limited` branched from `origin/main`
- **Pre-commit hooks** — Ensure no stale references remain (ruff, mypy, bandit)
- **Graphify query** — `uv run graphify query "company name LightSpeed Holdings Limited"` for knowledge graph validation
- **Brand sync script** — `pwsh scripts/build/sync-brand.ps1` for canonical → mirror propagation
- **Test suite** — `uv run pytest` to verify no breaking changes
- **Ruff/mypy** — `uv run ruff check src/` and `uv run mypy src/` for code quality

### Budget Impact
- **Estimated person-weeks:** 18 person-weeks total
- **Primary cost:** Staff time (no external vendor costs)
- **Risk mitigation:** 20% contingency included in timeline (4 additional days)

---

## 5) Progress Tracking Methodology

### Tracking Artifact: `CHIEF-OF-STAFF-IMPLEMENTATION-PLAN.md` (this file)
- All sections updated in real-time as changes progress
- Checkbox format for trackable items

### Daily Standup Format (Chief of Staff → Steering Committee)
```
STATUS: [what was done yesterday] | BLOCKERS: [what's preventing progress] |
PLAN: [what will be done today] | DECISIONS: [any decisions needed from CEO/board]
```

### Progress Tracking Table (updated daily)

| # | File/System | Status | Owner | Target Date | Actual Date | Verified By |
|---|-------------|--------|-------|-------------|-------------|-------------|
| 1 | company-registry.yaml name field | ☐ Not Started | CTO | Day 1 | | |
| 2 | company.yaml name/legal_name | ☐ Not Started | CTO | Day 1 | | |
| 3 | ai_caas_offers.yaml reference | ☐ Not Started | CTO | Day 1 | | |
| 4 | Agent regeneration | ☐ Not Started | CTO | Day 2 | | |
| 5 | brand-tokens.json legalName | ☐ Not Started | CMO | Day 3 | | |
| 6 | brand guidelines update | ☐ Not Started | CMO | Day 3 | | |
| 7 | Brand sync propagation | ☐ Not Started | Chief of Staff | Day 4 | | |
| 8 | agent-registry.json updates | ☐ Not Started | CTO | Day 5 | | |
| 9 | Source code (.ts, .tsx, .py) | ☐ Not Started | CTO | Days 7-10 | | |
| 10 | Templates/generators | ☐ Not Started | CPO | Days 10-14 | | |
| 11 | Documentation | ☐ Not Started | Chief of Staff | Weeks 3-5 | | |
| 12 | Legal/Inc. transition | ☐ Not Started | CLO | Ongoing | | |
| 13 | Final verification | ☐ Not Started | Chief of Staff | Week 5 | | |

### Verification Checklist (run after all changes)
- [ ] `uv run graphify query "company name LightSpeed Holdings Limited"` — no errors
- [ ] `uv run ruff check src/` — no lint errors
- [ ] `uv run mypy src/` — no type errors
- [ ] `uv run pytest` — all tests pass
- [ ] `git status` — no untracked modified files outside branch
- [ ] Brand sync: `pwsh scripts/build/sync-brand.ps1 -Verify` — no drift detected
- [ ] Search all files: `rg -l "Light Speed Holdings" .` — zero results (except historical archive)
- [ ] Search all files: `rg -l "LIGHTSPEED HOLDINGS" .` — zero results (except historical archive)
- [ ] Key files verified:
  - `company-registry.yaml` line 2: `name: LightSpeed Holdings Limited`
  - `company.yaml` lines 3-4: updated
  - `brand/tokens/brand-tokens.json` line 5: legalName updated
  - `brand/guidelines/brand-guidelines.md` line 14: Company Name updated
  - `src/components/SiteLayout.tsx` title updated
  - `src/ai_company/dashboard/app.py` title updated
  - `static/brand/templates/*.html` — all updated
  - `static/brand/templates/*.py` — all updated
  - `company/agent-registry.json` — all updated
  - `src/data/generated/agent-registry.public.json` — all updated

### Success Criteria
- [ ] Zero references to "Light Speed Holdings" (with spaces) in active code/docs
- [ ] Zero references to "LIGHTSPEED HOLDINGS" (all-caps) in active code/docs
- [ ] All references use "LightSpeed Holdings Limited" (title case)
- [ ] Company registry is the single source of truth and propagates correctly
- [ ] Brand guidelines reflect the new name
- [ ] All generated agents/cards reflect the new name
- [ ] Dashboard and website display correct name
- [ ] Legal name field updated consistently
- [ ] No breaking changes from the update (all tests pass)
- [ ] CEO sign-off on completion

### Rollback Plan
If critical issues are discovered:
1. **Immediately** `git checkout main` and `git branch -D name-change/lightspeed-holdings-limited`
2. **Revert** all changes from the branch
3. **Restore** original name in all files
4. **Escalate** to CEO with issue summary
5. **Re-plan** with revised timeline after root cause analysis

---

## Execution Timeline Summary

| Week | Focus | Key Deliverables |
|------|-------|------------------|
| **Week 1** (Days 1-5) | Core System of Record | registry.yaml, company.yaml, JSON configs, initial generator run |
| **Week 2** (Days 6-10) | Brand Assets & Tokens | brand guidelines, tokens, brand sync propagation |
| **Week 3** (Days 11-15) | Agent Registry & JSON configs | agent-registry.json, all skill files |
| **Week 4** (Days 16-20) | Source Code & Website | .ts, .tsx, .py files, dashboard, CLI |
| **Week 5** (Days 21-25) | Templates & Generators | pitch decks, board meetings, social assets, emails |
| **Week 6** (Days 26-30) | Documentation & Legal | all docs, legal transition, final verification |
| **Week 7** (Day 31+) | Closure | CEO sign-off, rollback plan activation (if needed), knowledge transfer |

**Total estimated duration:** 3-4 weeks for core changes, 6-7 weeks for full organizational alignment.

---
*This plan is living document. Update weekly via Chief of Staff standup. All changes tracked in git branch `name-change/lightspeed-holdings-limited`.*
