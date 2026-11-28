# Image Usage Map — Marketing Site

Every image referenced by the marketing site resolves to a registered entry in
`src/data/registries/media-registry.json`. Big imagery (full-bleed / carousel /
infographic) is provided by `BigImageSection`, `ImageCarousel`, and
`InfographicBlock`.

## Big imagery placements

| Image | Page / Section | Component |
|---|---|---|
| hero_cinematic_landscape_day / night | Home — Hero | HeroSection |
| identity_triptych_foundations | Home — Mission image | BigImageSection |
| solution_company_builder | Home — Infographic (Mission) | InfographicBlock |
| solution_market_intelligence | Home — Infographic (Vision) | InfographicBlock |
| solution_workflow_collapsing | Home — Infographic (Values) | InfographicBlock |
| pharos_editorial_hero | Home — Carousel | ImageCarousel |
| pharos_canonical_architecture | Home — Carousel | ImageCarousel |
| pharos_ai_orchestration | Home — Carousel | ImageCarousel |
| agent_network_topology | What We Do — Big image | BigImageSection |
| pharos_cta_pure | HAOMTGV — Big image | BigImageSection |
| philosophy_triptych_clean | About — Big image | BigImageSection |
| pharos_editorial_hero | Insights — Big image | BigImageSection |
| cta_pathway_destination | Contact — Big image | BigImageSection |
| pharos_ai_governance | FAQ — Big image | BigImageSection |
| solution_agentic_automation | AI Assessment — Big image | BigImageSection |
| val_prop_bg_night | Privacy — Big image | BigImageSection |
| before_after_sector_bg_light | Terms — Big image | BigImageSection |

## Notes
- All referenced paths use published `/assets/images/*.avif` (or registered `.jpg`) variants.
- New image references must be added to `media-registry.json` (enforced by `media-registry.test.ts`).
- Remaining registered images are consumed by existing sections (siteContent, insights, whitepapers).
