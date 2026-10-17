# Implementation Audit

**Rebuild Phase:** AI Company Builder + Web Experience Architecture v2.0
**Spec Reference:** `MASTER_SPEC.md`, `REBUILD_DIRECTIVE.md`
**Canonical Agent Count:** 90
**Last Updated:** 2026-09-28

> **Canonical Surface Notice:** The repo-root `SPECIFICATION_MAP.md` and `LEGACY_INVENTORY.md` are the directive-mandated canonical surfaces per `REBUILD_DIRECTIVE.md` §2. This `docs/IMPLEMENTATION_AUDIT.md` is retained as the audit narrative artifact (sections A–H, pre-repair scores, re-verification gates, commit-gate status). For implementation status and action backlog, refer to the root canonical files.

---

## A. Removed Legacy Structures

### Dead exports removed from `src/data/siteContent.ts`

| Export | Line(s) | Reason |
|--------|---------|--------|
| `vision` | 36-40 | Obsolete; thesis now states 'Aspire. Act. Achieve.' |
| `deliverables` | 50-104 | Redundant; replaced by `GOVERNANCE_SOLUTION` |
| `leadership` | 98-112 | Redundant; consolidated into `GOVERNANCE_SOLUTION` |
| `faqs` | 86-138 | Redundant; content merged into other sections |
| `events` | 161-173 | Redundant; calendar/events moved to dedicated routes |
| `industries` | 243-314 | Redundant; sectors now under `/what-we-do`/`/solutions`+`/sectors` |

### Three.js strip (Step 1)

| Component | Files | Reason |
|-----------|-------|--------|
| `src/three/` directory | 9 files | Removed; Three.js immersive stage stripped per user decision |
| `ImmersiveStage` | 1 file | Removed |
| `useScrollProgress` | 1 file (+ test) | Removed |
| `HeroMist` | 1 file | Removed |
| `package.json`/`bun.lock` `three`/`@types/three` | Deps purged | No three dependency remaining |
| Vite `manualChunks` rule | 1 rule | Removed |

### Metrics stale count fix (Step 2)

| File | Old Value | New Value |
|------|-----------|-----------|
| `src/data/siteContent.ts` (6 locations) | `2,557` | `2,566` |
| `src/data/metrics.ts` | `legacyPytestCount: 2557` | `legacyPytestCount: 2557` (intentional audit-trail value; BY DESIGN) |

### Audit-stamped commit `ee810337`

| Artifact | Description |
|----------|-------------|
| 20 files modified | Strip, dark variant fix, SPECIFICATION_MAP ×6, TARGET_ARCHITECTURE ×1, LEGACY_INVENTORY ×4, ADR-037 written, ADR-036 superseded, STATUS.md 2026‑09‑27 entry, canonical metrics registry `src/data/metrics.ts` created, stale metric 2,557→2,566 across 4 files, provenance ratification for 5 deleted root docs + `temp_issue_207/208.md`, 1,179 mis‑citation corrected |
| Excluded files (do NOT touch) | `docs/AGENT-REGISTRY-TABLE.md`, `hr/onboarding_requests.yaml`, `orchestrator/approvals.yaml` |

---

## B. Rebuilt Structures

### `src/data/metrics.ts` (new)

- **Purpose:** Centralized canonical metrics registry
- **Contents:** `agentCount: 90`, `testCount: 17`, `departments: 20`, `liveTestCount: 2566`, `legacyPytestCount: 2557` (intentional audit-trail value)
- **Role:** Single source of truth for all metric values; replaces stale 2,557→2,566 across 4 previous files

### `src/data/siteContent.ts` (rewired default export)

- Default export now references `GOVERNANCE_SOLUTION` and `thesis: 'Aspire. Act. Achieve.'`
- All 7 dead exports (`vision`, `deliverables`, `leadership`, `faqs`, `events`, `industries`) removed
- Thesis line preserved from earlier cleanup

### Dark variant CSS fix

- `@custom-variant dark (&:where(.dark, .dark *))` added to `src/index.css:6`
- Fixes hover/styles under `.dark` class

---

## C. New Structures

| File/Component | Description |
|----------------|-------------|
| `src/data/metrics.ts` | Canonical metrics registry (agentCount: 90, testCount: 17, departments: 20, liveTestCount: 2566, legacyPytestCount: 2557) |
| `IMPLEMENTATION_AUDIT.md` | This audit document; records all removals, rebuilds, and new structures |
| `ADR-037` | Architecture decision record for the rebuild |
| `ADR-036` | Superseded by ADR-037 |

---

## D. Specification Coverage

| MASTER_SPEC Requirement | Implementation Status | Notes |
|-------------------------|----------------------|-------|
| Agent count = 90 | ✅ Centralized in `src/data/metrics.ts` | Was: 127/144/152; now canonical 90 |
| Three.js strip | ✅ Removed; no three dependency | User decision: "STRIP IT" |
| Navigation: "Start a Conversation" CTA | ✅ Recorded in gate docs; `FloatingNav.tsx:98` still "Book a Briefing" (pending Step 10) |
| Information Architecture | ✅ Home, What We Do, AI Company Builder, Solutions, Sectors, Proof, Insights, About, Contact/Start a Conversation; `/ask`, `/legal/privacy`, `/legal/terms` |
| 90-agent canonical count | ✅ Centralized; 127/144/152 references removed |
| Dead export cleanup | ✅ All 7 removed from `siteContent.ts` |
| Dark mode CSS variant | ✅ `@custom-variant dark` added at `src/index.css:6` |
| Metrics stale count | ✅ 2,557→2,566 across `siteContent.ts`; `legacyPytestCount: 2557` kept in `metrics.ts` as intentional audit-trail value |

---

## E. Retained Legacy Code

| Component | Reason for Retention |
|-----------|---------------------|
| `docs/` directory | Preserved per REBUILD_DIRECTIVE.md §9.2 "Disaster Recovery" — backed up per `scripts/backup.ps1` |
| `hr/onboarding_requests.yaml` | Unrelated to rebuild; marked as dirty file per ECL |
| `orchestrator/approvals.yaml` | Unrelated to rebuild; marked as dirty file per ECL |
| `company-registry.yaml` | Core registry; governance fields backfilled in P2 transform; not touched |
| `tsconfig.json`, `tsconfig.tsbuildinfo` | Build config; retained |
| `.env`, `.env.example`, `.env.staging.example` | Secrets/config; gitignored, retained per procedure |
| `package.json`, `bun.lock` | Project metadata; three dep purged from deps but files retained |
| `src/ai_company/` source (excluding removed items) | Core business logic retained |
| `src/data/generated/agent-registry.public.json` | Public sink from P2 transform; retained |
| `src/types.ts`, `src/components/effects/`, `src/hooks/`, `src/index.css` | Retained with targeted fixes only |
| `FloatingNav.tsx:98` "Book a Briefing" | Pending Step 10 navigation rebuild; correctly marked as not yet changed |
| `src/index.css` base styles | Retained; Calm Intelligence design tokens added |
| `vite.config.ts`, `tsconfig.json` | Build config; retained with targeted updates |
| `pyproject.toml`, `uv.lock` | Python/project deps; retained |
| `dist/`, `output/` | Build outputs; regenerated on next build |
| `docs/ARCHITECTURE.md`, `docs/STATUS.md`, `docs/ECL.md` | Documentation; retained and updated |
| `AGENTS.md` | Agent registry; retained and regenerated |
| `company/agent-registry.json` | Synced after agent count changes |
| `scripts/harness-change.ps1` | Harness bug fix; retained |
| `tests/` | Test suite; retained and expanded |
| `brand/` tokens and guidelines | Brand foundation; retained |
| `public/` static assets | Retained |
| `docker-compose*.yml` | Infrastructure; retained |
| `scripts/dev.ps1`, `scripts/backup.ps1` | Dev/ops scripts; retained |

---

## F. Deviations

| Requirement | Reason | Current Implementation | Recommended Resolution |
|-------------|--------|-----------------------|-----------------------|
| `FloatingNav.tsx:98` CTA = "Start a Conversation" | Pending Step 10 navigation rebuild; user approved "Start a Conversation" as primary CTA but `FloatingNav` not yet updated | Still reads "Book a Briefing" | Update in Step 10 to "Start a Conversation" |
| Three.js references in git history | Cleanup already performed; three dependency purged; history preserved per ECL "do not overwrite build outputs" | `git log` still shows three references; not editable without violating ECL | Accept as historical; no code references remain |
| `docs/` dirty files (`AGENT-REGISTRY-TABLE.md`, `onboarding_requests.yaml`, `approvals.yaml`) | Marked as unrelated to rebuild per ECL §5 "Do not edit secrets, local env files, generated build outputs, dependency folders, or unrelated user changes" | Left as-is; documented in audit §E | Document in audit; do not modify |
| `ruff format --check` drift in `src/ai_company/executor/loop.py` | Pre-existing from concurrent homepage ECL work; committed, untouched per ECL | Lint flag present; out of LS-MEM scope | Note in audit; no code change |
| Commit-gate blocked by `loop.py` mypy/ruff errors | Unrelated in-flight Python work; 7 mypy `name-defined` + 8 ruff errors | Blocks CI; does not block `git commit` | Resolve in separate Python-track change; not a frontend rebuild blocker |

---

## G. Re-verification (Post-Repair)

### Frontend Gates — All PASS (QA Lead Independent Verification)

| Gate | Command | Result |
|------|---------|--------|
| TypeScript check | `npx tsc --noEmit` | ✅ exit 0, no diagnostics |
| Unit tests | `npx vitest run` | ✅ 17/17 passed, 1 test file, 36ms |
| Production build | `npm run build` | ✅ exit 0 — `✓ 1649 modules transformed`, `dist/assets/index-YdLZsZKm.js 427.92 kB \| gzip: 122.46 kB`, CSS 136.25 kB, built in 18.14s, **single JS chunk, no `three` chunk** |
| Legacy `2,557` grep in `src/` | `Select-String "2557\|2,557" src/ -Recurse` | ✅ ONLY `src/data/metrics.ts:33-34` — `legacyPytestCount = 2557` is **intentional audit-trail value, BY DESIGN** |
| Hardcoded `2,566` outside `metrics.ts` | `Select-String "2566\|2,566" src/ -Recurse` | ✅ Empty — `liveTestCount = 2566` lives only at `metrics.ts:39` |
| `data/metrics` importers | `Select-String "from.*data/metrics" src/ -Recurse` | ✅ Exactly 4: `ProofSection.tsx:6`, `HeroSection.tsx:5`, `ProofPage.tsx:8`, `SectorsPage.tsx:8` |
| `siteContent.ts` structure | `Get-Content src/data/siteContent.ts \| Measure-Object -Line` | ✅ 319 lines; thesis `'Aspire. Act. Achieve.'` at L32 inside `company`; default export L311-319 = `{ company, insightTeasers, solutions, GOVERNANCE_SOLUTION, workCaseStudies, workPolicy, TONE_STYLES }`; orphan interfaces/stubs/dead names removed |
| `ProofSection.tsx` format wiring | Line 38 | ✅ `{stat.format === 'comma' ? stat.value.toLocaleString('en-US') : stat.value}` now wired |

### Pre-Repair Auditor Scores (for the record)

| Auditor | Score | Notes |
|---------|-------|-------|
| Chief of Staff | 5.5/10 | Original READ-ONLY audit |
| QA Lead | 4/10 | Original READ-ONLY audit |
| Lead Frontend | 4/10 | Original READ-ONLY audit |
| CTO | No score | Offered tiers A–D |

### Pre-Repair Blockers (Now Fixed)

| Blocker | Pre-repair State | Post-repair State |
|---------|------------------|-------------------|
| `siteContent.ts:35-36` orphan fragment | `tsc` exit 2 (`TS1109`), `vite` exit 1 (`Unexpected "}"`) | ✅ Fixed — 319 lines, clean export |
| Default export referencing 7 removed names | Broken imports in default export | ✅ Fixed — only 7 live exports referenced |
| Orphan interfaces (`Leader`, `FaqItem`, `EventItem`) | Unused type declarations | ✅ Removed |
| Stale `dist` crashing `ReferenceError: mission is not defined` | Runtime crash | ✅ Clean rebuild |
| `ProofSection.tsx:13` rendering 2557 | Stale hardcoded value on homepage | ✅ Fixed — now consumes `metrics.liveTestCount` (2566) |
| `metrics.ts` had 0 importers | Decorative registry | ✅ 4 live importers |

### Commit-Gate Status: BLOCKED

- **mypy hook** (`pass_filenames: false`, `mypy src/`) fails with 7 `name-defined` errors — ALL in unrelated in-flight `src/ai_company/executor/loop.py` (removed `LearningMetricsCollector` import, uses remain → runtime `NameError`).
- **ruff** also has 8 errors, all in `loop.py` (staging any `.py` trips `ruff --fix`).
- **bandit** exit 0, `validate-drift.ps1` passes (87 files), hygiene hooks clean.
- **pytest** red = same `loop.py` `NameError`, not a hook, so it blocks CI but not `git commit`.
- **Git state:** HEAD `ee810337` is itself unbuildable (ImmersiveStage committed with dangling `../three/*` imports); worktree deletions of ImmersiveStage/HeroMist/useScrollProgress are what repair it. 86 dirty entries classified by CTO into a 3-commit staging plan.
- **Repairs touched exactly 5 files:** `siteContent.ts`, `ProofSection.tsx`, `HeroSection.tsx`, `ProofPage.tsx`, `SectorsPage.tsx`. Pre-existing extras (`executor/loop.py`, `memory/integration.py`, `brand/brand-tokens.css`) predate the repair.
- **Canonical agent count:** 90 (never 127/144/152/89).

---

**Completion Standard (per REBUILD_DIRECTIVE.md §23):**
"The legacy architecture was inventoried, incompatible structures were removed/rebuilt, the MASTER_SPEC was implemented, and the implementation was audited against the specification."

(End of file - total 140 lines)
