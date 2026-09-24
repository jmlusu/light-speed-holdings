# ADR-031: Route Consolidation (Single-Hop Redirects)

**Status:** Accepted
**Date:** 2026-09-24
**ECL:** LightSpeed AI Company Builder + Web Experience Architecture v2.0
**Cross-refs:** [ROUTE_MIGRATION_V2.md](../../ROUTE_MIGRATION_V2.md), [WEB_INFORMATION_ARCHITECTURE_V2.md](../../WEB_INFORMATION_ARCHITECTURE_V2.md), [EVIDENCE_ARCHITECTURE.md](../../EVIDENCE_ARCHITECTURE.md)

## Context

`src/App.tsx` has 34 child entries (28 live paths + SPA redirects + catch-all). `vercel.json` edge redirects disagree with SPA finals: `/offerings` → `/solutions` (edge) then `/solutions` → `/what-we-do` (SPA) = **double hop**; `/work` → `/evidence` then `/evidence` → `/proof` = **double hop**. Dead page imports remain wired (`WorkPage`, `OfferingsPage`, `EvidencePage`, `SolutionsPage`, `IndustriesPage`). Sibling docs disagree on non-proof targets (`/offerings` → `/solutions` vs `/what-we-do`; `/industries` → `/sectors` rename). Proof-path targets already agree.

## Decision

1. **Single-hop rule:** every edge redirect destination **equals** the SPA final canonical. Shared/bookmarked/crawler URLs must land in one 301.

   | Legacy source | Final canonical |
   |---------------|-----------------|
   | `/offerings` | `/what-we-do` |
   | `/work` | `/proof` |
   | `/evidence` | `/proof` |
   | `/solutions` (index) | `/what-we-do` |
   | `/industries` (index) | `/what-we-do` |
   | catch-all `*` | `/` |

2. **Canonical hubs:**
   - Capabilities: **`/what-we-do`** absorbs offerings/solutions-index/industries-index browsing (detail routes `/solutions/:slug`, `/industries/:slug` remain live).
   - Evidence: **`/proof`** absorbs work/evidence/outcomes/trust as sections (`#metrics`, `#honesty`, `#cases`, `#outcomes`, `#trust`, `#verify`).
   - `/insights` stays a separate Pharos index (cites Proof; never a second proof hub).

3. **SPA `Navigate` redirects** remain as client fallback for in-app and non-edge hits; edge rules are the source of truth for cold requests. After fix: edge redirect set covers offerings, work, evidence (+ optional solutions/industries indexes).

4. **Framework strategy:** keep **React Router 7 + Vite 6** (see ADR-034). No router or SPA rewrite as part of route consolidation.

5. **Dead imports/page files:** remove from the route table immediately; delete page files only after content salvage (roadmap: P5 gates final deletion). Do not ship new first-class routes for `/work`, `/evidence`, `/offerings`.

6. **Slug drift:** footer/legacy solution slugs and `/industries/development` vs content `education` must align to `siteContent` canonical slugs during implementation (P3), not via additional permanent redirects where a data fix suffices.

7. **Architecture Lead reconciliation (implementation gate):** where WEB_IA and ROUTE_MIGRATION disagreed, this ADR rules **`/what-we-do` for offerings and solutions index** (ROUTE_MIGRATION target). A `/sectors` rename (WEB_IA) is **not** adopted as a required v2 path — if desired later, it requires an amending ADR and a single-hop plan, not an edge/SPA conflict.

## Alternatives

| Option | Why not |
|--------|---------|
| Keep double hops | SEO dilution; cached first-hop chains; crawlers index intermediate URLs |
| Live `/solutions` index + `/what-we-do` | Two hubs for one capability story; IA divergence already flagged |
| SPA-only redirects (drop edge) | Crawlers and shared URLs may not run client router the same way; edge 301 preferred for permanence |
| Full framework rewrite during consolidation | Violates brief constraint; no measured reason (ADR-034) |
| Leave dead imports wired | Bundle confusion; false route inventory |

## Rationale

- Edge destination = SPA final is the only rule that makes cold and warm requests converge.
- Consolidating offerings→what-we-do and work/evidence→proof collapses ownership of content (ADR-033) and nav.
- Keeping Router 7/Vite minimizes blast radius; redirect correctness is independent of framework choice.

## Consequences

- Follow-on ECL edits `vercel.json` redirects and `App.tsx` Navigate set; QA asserts `curl -I` single-hop table.
- In-app links repointed (TrustPage `/evidence` links, footer pillars, relatedLinksByRoute).
- Dead deps (e.g. `recharts` if unused after cleanup) removed in P3; page file deletion waits on P5 salvage.
- `/sectors` rename deferred unless a future ADR adopts it with single-hop design.
