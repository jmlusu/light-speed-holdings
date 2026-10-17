# Baseline Appendix — Deployment Comparison (§7.4)

**Date:** 2026-09-24 (Phase 0 discovery, read-only)

## Targets

| Target | URL / path | Observed |
|--------|------------|----------|
| GitHub (SoT) | https://github.com/jmlusu/light-speed-holdings | Public repo, 404 commits on `main`. README still claims **152 agents / 151 AI** and "generates 152 agents" — **stale vs local repo** (local README: 90). Clone URL in README points at `light-speed-holdings/ai-company` (org path) while repo lives at `jmlusu/light-speed-holdings`. |
| Vercel | https://light-speed-holdings.vercel.app/ | Title: "LightSpeed Holdings Limited - AI-Native Operator and Partner". Serves public React SPA. GitHub "About" also links `light-speed-holdings-jmlusu-8288s-projects.vercel.app` (preview alias). |
| AI Studio | https://lightspeedholdings.ai.studio | Title: "LIGHTSPEED HOLDINGS — From Strategy to Intelligent Execution". Distinct marketing stack from the Vercel SPA (different title/h1 pattern) — treat as **separate deployment**, not guaranteed same build as Vercel. |

## Deltas / risks

1. **GitHub README is behind local** on agent count (152 vs 90) — remote not fully synced with `e2bdb0c7` trim, or README on remote not updated; verify before public claims.
2. **Two live front doors** (Vercel SPA vs AI Studio) with divergent narratives — v2 IA must declare a canonical production origin and redirect policy for the other.
3. **Repo vs deploy sync is unproven** — brief requires verification; this pass only compared titles/README, not build hashes. Deep compare (route inventory, registry JSON, bundle) is a Phase 0 optional follow-up.
4. Local working tree = technical SoT per brief; remote main may lag.

## Actions for roadmap

- Confirm which host is canonical (recommend: Vercel SPA from `main` for public web; AI Studio either redirects or is re-scoped as demo).
- Sync GitHub README counts to 90 as part of doc-drift sweep (Phase 1/doc task, not this architecture authoring pass unless approved).
