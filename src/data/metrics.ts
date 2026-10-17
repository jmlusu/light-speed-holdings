/* Canonical metrics registry — single source of truth for all metric displays.
   All page components (HeroSection, UseCasesSection, SectorsPage, WorkforceSection)
   must import from this file instead of hard-coding values.  See TARGET_ARCHITECTURE.md §3.
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

/* Live pytest collection count (uv run pytest --collect-only -q, 2026-10-13).
   Display code must use `metrics.testCount` (vitest, 17) or `metrics.agentCount`
   (90) rather than this number; this is the Python suite size for the hero
   "passing tests" figure. */
export const liveTestCount = 2586;
