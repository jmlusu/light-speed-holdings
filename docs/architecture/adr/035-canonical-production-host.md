# ADR-035: Canonical Production Host

**Status:** Accepted
**Date:** 2026-09-24
**ECL:** LightSpeed AI Company Builder + Web Experience Architecture v2.0
**Cross-refs:** `harness/changes/active/ref/deployment-comparison.md`, ADR-031, ADR-034

## Context

Phase 0 discovery compared three public targets:

| Target | Observation |
|--------|-------------|
| GitHub `jmlusu/light-speed-holdings` | Source of truth for code; remote README still claimed **152 agents / 151 AI** (stale vs local 90) at comparison time |
| Vercel `light-speed-holdings.vercel.app` | Serves the public React SPA (“AI-Native Operator and Partner”) |
| AI Studio `lightspeedholdings.ai.studio` | **Separate** marketing stack/titles — not guaranteed same build as Vercel |

Two live front doors with divergent narratives create SEO split, claim drift, and operational ambiguity. Repo↔deploy build-hash sync was **not** proven in Phase 0 (titles/README only).

## Decision

1. **Canonical production origin for the public web experience = Vercel deployment of the repo-root Vite React SPA built from `main`** (URL class: `light-speed-holdings.vercel.app` / project alias as configured).

2. **AI Studio is non-canonical.** Options (execute in implementation ECL): **(a)** HTTP redirect to the Vercel canonical host (301), or **(b)** explicit re-scope as a demo/lab property with no independent claims — Architecture Lead picks (a) or (b) before P7 cutover; default recommendation **(a) redirect** unless a documented demo purpose is ratified.

3. **GitHub remains SoT for code**, not a web front door. Remote README agent counts must be synced to **90** as part of doc-drift work (not architecture authoring).

4. **Single canonical host rule for new links, badges, and press:** only the Vercel primary URL is published as “the site” until an amending ADR changes host.

5. **Deployment verification (follow-up):** confirm builds on canonical host match `main` (route inventory, registry counts in artifact, version hash) — Phase 0 left deep compare optional; treat as P7 exit evidence.

## Alternatives

| Option | Why not |
|--------|---------|
| AI Studio canonical | Divergent stack/claims; no evidence it builds from same `main` |
| Dual-canon (both primary) | Permanently splits SEO and narrative; root cause of v2 IA pain |
| GitHub Pages from `docs/` | Would fork delivery from SPA `vercel.json` redirects; contradicts current edge model |
| Self-host only | Not required for v2; adds ops before consolidation ships |
| Do nothing | Leaves two front doors and stale remote README claims live |

## Rationale

- Vercel already serves the ratified SPA target (ADR-020/034) with `vercel.json` edge redirects needed for ADR-031 single-hop rule.
- AI Studio title/H1 divergence proves separate publishing — treating it as equal multiplies every content fix.
- Redirect-or-rescope preserves optionality without keeping two sources of public truth.

## Consequences

- Implementation ECL: choose AI Studio redirect vs re-scope; update canonical tags/sitemaps if present; scrub external links to non-canonical URLs.
- Doc-drift task updates GitHub README counts to 90 and fixes clone path if still wrong.
- P7 cutover checklist includes host confirmation + build sync evidence.
- Status of this ADR may move to **Proposed** only if Architecture Lead rejects Vercel-as-canonical before implementation — currently Accepted against Phase 0 evidence.
