# Website Compliance — Ticket Ledger

Status: TRACKING · Owner: chief-of-staff (accountable) · Updated: 2026-09-23
Source of truth: CMO Guiding Principles v1.0 · ADR-020 (ratified) · Wayfinder map #251 (closed) · Audit + T1–T8 resolutions

## Ticket map (all under `site-compliance` label)

| # | Ticket | Priority / Order | Owner (body) | Status | Blocked by |
|---|--------|------------------|--------------|--------|------------|
| #302 | P1 — Dispose unqualified claims (18 (c)-class rows + severe contradictions) | P1 (1) | content-creator | OPEN (`ready-for-agent`) | — first wave |
| #303 | P2 — Token + motif confinement (gray sweep, motif removal, mono confinement) | P2 (2) | frontend-architect (+product-marketing-manager design authority) | OPEN (`ready-for-agent`) | — first wave |
| #304 | Gate — ACK registry sign-off sweep (15 roles PENDING → ACKNOWLEDGED) | Gate (0) | vp-engineering (chief-of-staff accountable) | **CLOSED** 2026-09-23 via #360 squash → main @ 8f2e73d7 (15/15 ACK + 6/6 required checks) | — gate met |
| #305 | P3 — Nav/IA restructure (5-item CTA-led nav, route consolidation, §8 labels) | P3 (3) | lead-frontend (+product-designer IA) | OPEN (`ready-for-agent`) | #303, #304 |
| #306 | P5 — A11y + consistency + Pharos Insights IA | P5 (5) | product-designer (+senior-frontend-engineer, content-creator) | OPEN (`ready-for-agent`) | #302, #303, #304 |
| #307 | P4 — Analytics (Plausible primary / Umami fallback + event schema) | P4 (4) | ux-analytics-lead (+frontend-architect) | OPEN (`ready-for-agent`) | #305, #304 |
| #308 | P3 — Homepage outcome-led restructure | P3 (3; prototype unblocked) | product-designer → lead-frontend (impl) | OPEN (`ready-for-agent`) | #255, #303, #305, #307, #304 |

## Dependency graph

```
Gate #304 (ACK sweep)          — first; unblocks every merge below
P1 #302 (claims)               — first wave      ├── blocks #306
P2 #303 (tokens/motif)         — first wave      ├── blocks #305, #306, #308
P3 #305 (nav/IA)               — after #303      ├── blocks #307, #308
P4 #307 (analytics)            — after #305      └── blocks #308
P5 #306 (a11y/Pharos)          — after #302+#303
P3 #308 (homepage)             — after #255 prototype + #303 + #305 + #307
T4 #255 (homepage prototype)   — OPEN, unblocked, product-designer
```

## Verification standard (MANDATORY gate on every site PR — same across all tickets)

1. `npm run build` (tsc) green + `npm test` green.
2. Playwright at 390px + keyboard nav + visible focus + zero console errors.
3. before/after screenshots via `before-and-after` skill for every changed surface.
4. Appendix A checklist completed in PR description (`.github/PULL_REQUEST_TEMPLATE.md`).
5. `ls-artifact-qa` APPROVE on any visual work.
6. `python scripts/check-site-form-backend.py` green.
7. Tokens ONLY: navy #070A40 / red #E63946 / cyan #00BFFF / white / #F2F2F2 + Arial scale; no gray/zinc/slate/stone/neutral/amber/emerald/custom hex on the public SPA.
8. Local form tests use the dev-only stub on `/api/enquiry` (Vite dev middleware returning 201, excluded from prod builds); NEVER hit the live worker during tests.
9. Working agent signs `.ai-company/state/WEBSITE_PRINCIPLES_ACKNOWLEDGMENTS.md` (15/15) before merge.

## SLA ownership (post-launch)

- Recurring SLA (two business days): sales-owner, customer-success-owner, cfo (funding).
- New Web Form entry in SLA section: ma (mandatory) / mo (monthly) / ad-hoc entries to Holistics + revenue dashboards (business-intelligence-engineer).

## Risk log

- (c)-class claims must be fully disposed by #302 before any merge touches copy (enforced by merge gate on #302).
- ThreeCanvas/WebGL + tactile motif confined to internal diagnostics only (#303).
- Homepage restructure (#308) may not merge before #255 prototype → CMO reaction; prototype work is unblocked NOW.
- #304 ACK sweep must reach 15/15 before any compliance PR merges; build agents sign the registry, skill leads sign once per skill.

## Completeness check (updated on each change)

- [x] 7/7 child tickets exist, labeled `site-compliance` (+ `wayfinder:task`, `ready-for-agent`), owners in body.
- [x] Map #251 commented with child ticket list.
- [x] T4 #255 labelled + commented (feeds #308).
- [x] All blocker wiring verified (gh issue view shows `Blocked by:` lines).
- [x] #304 required status check `Site Build + Principles Gate` added to ruleset `main zero-red gate` (2026-09-23); workflow PR trigger has no path filter so the check always reports.
- [x] #304 closed 2026-09-23 after PR #360 squash merge (main @ 8f2e73d7); bulk-history strip landed in same PR (13MB / 22 retained binaries). Gate unblocks first-wave #302/#303.
