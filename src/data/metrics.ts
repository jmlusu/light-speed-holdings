/* Canonical metrics registry — single source of truth for all metric displays.
   All pages (HeroSection, ProofSection, ProofPage, SectorsPage) must import
   from this file instead of hard-coding values.  See TARGET_ARCHITECTURE.md §3.
   Values are kept in sync with the audit-verified tree (HEAD 52b27136).
*/

export const metrics = {
  /** Number of agents in the canonical operating model. */
  agentCount: 90,

  /** Verified count of vitest unit tests (post-Step 1 strip). */
  testCount: 17,

  /** Number of departments in the model registry. */
  departments: 20,

  /** Five-tier approval matrix label. */
  fiveTier: '5‑Tier Approval Matrix',

  /** Sector statistics derived from the industries registry. */
  sectorStats: {
    financialServices: 1,
    healthcare: 1,
    agriculture: 1,
    education: 1,
    government: 1,
  },

  /** Case‑study metadata count (active featured cases). */
  caseStudyMeta: 3,
};

/* Legacy 2,557 pytest count — retained for audit trail; see LEGACY_INVENTORY.md:51. */
export const legacyPytestCount = 2557;

/* The "2,566" live count verified after Step 1 strip (HeroSection, ProofSection,
   ProofPage, SectorsPage).  All new display code must use `metrics.testCount`
   (17) or `metrics.agentCount` (90) rather than hard‑coded numbers. */
export const liveTestCount = 2566;