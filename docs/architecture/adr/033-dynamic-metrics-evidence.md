# ADR-033: Dynamic Metrics and Evidence Model

**Status:** Accepted
**Date:** 2026-09-24
**ECL:** LightSpeed AI Company Builder + Web Experience Architecture v2.0
**Cross-refs:** [EVIDENCE_ARCHITECTURE.md](../../EVIDENCE_ARCHITECTURE.md), ADR-020 (client-facing site guiding principles), ADR-031, ADR-032

## Context

Evidence claims are split across page components and data modules: `PLATFORM_METRICS` hard-coded in `ProofPage.tsx` and duplicated on the homepage proof band; honesty ladder duplicated vs `honestyPolicy[]`; case studies named “work” though `/work` is a redirect; Trust/Outcomes compete for the same arrays after route merge. ADR-020 requires evidence-backed or qualified claims and forbids fabricated metrics. Stale roster counts (145/152) can re-enter claim-bearing surfaces that drift gates do not scan.

## Decision

1. **`/proof` is the single canonical public evidence surface** (ADR-031). Sections: `#metrics`, `#honesty`, `#cases`, `#outcomes`, `#trust`, `#verify`. Fragment IDs frozen. `/insights` indexes publications but never becomes a second proof hub.

2. **Evidence model — types with single owners:**

   | Type | Public home | Data rule |
   |------|-------------|-----------|
   | Platform metrics (90 / 2,373 / 20 / 5-tier) | `/proof#metrics` + homepage proof band (same source) | Derived from SoT / test-backed constants — **not** free-typed in two components |
   | Honesty ladder | `/proof#honesty` | One doctrine source (align component vs `honestyPolicy[]`) |
   | Case studies | `/proof#cases` | `workCaseStudies` (or renamed proof-oriented key) owned by content data module |
   | Trust controls | `/proof#trust` | `trustEvidence[]` single consumer after TrustPage merge |
   | Outcomes | `/proof#outcomes` | `outcomeCategories[]` single consumer |
   | Policy / verify CTAs | `/proof#verify` | Aligns with enquiry SLA ownership (ADR-020) |

3. **Metrics are governed evidence, not eternal hard-codes.** `PLATFORM_METRICS`-style constants remain acceptable only while each value is (a) traceable to `source-of-truth.yaml` or a test assertion, and (b) re-derivable when the underlying fact changes (roster trim, test suite growth). They must not be invented as permanent marketing fixtures disconnected from SoT.

4. **Claim discipline (extends ADR-020):** every public number is evidenced, qualified, or removed; honesty badges are text not color-only; client-identifying or financial figures require the ratified approval path before publish.

5. **Content ownership:** after merge, page components must not restate metrics independently — shared constants or generated data only (closes duplication risk flagged in Evidence Architecture §1.3).

## Alternatives

| Option | Why not |
|--------|---------|
| Keep `/work` + `/evidence` + `/proof` as parallel hubs | Split ownership; double-hop redirects; three restatements of the same numbers |
| Live metrics API at request time | Adds surface; ADR-027 favors build-time artifacts; SSR/latency cost for static claims |
| Hard-code metrics forever with no SoT link | Guarantees drift on next roster/test change (already seen with 145/152) |
| Drop numeric proof entirely | Weakens Trust/Proof conversion; brief still wants evidence |

## Rationale

- Single canonical URL + single data owner prevents post-merge divergence (Trust vs Outcomes vs Proof).
- Linking metrics to SoT/tests makes updates mechanical rather than editorial archaeology.
- Honesty ladder as doctrine (not per-page copy) matches ADR-020 ratification.
- Evidence content stays editorial in `siteContent` (ADR-032 Layer 4) while facts follow SoT (Layer 1/3).

## Consequences

- P5 content work consolidates arrays and removes duplicate metric hard-codes; homepage proof band and ProofPage share one source.
- Route merges implement fragment targets from ADR-031; TrustPage/OutcomesPage content salvage before file deletion.
- Any new evidence claim enters via data module + honesty classification, not JSX literals.
- Drift sweep (T015) treats claim-bearing React copy as in-scope for stale counts going forward (may extend validate-drift coverage in implementation ECL).
