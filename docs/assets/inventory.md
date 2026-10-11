# Marketing Site Artifact Inventory

**Source:** Merged from `docs/assets/README.md` (generation tracker, 15 planned assets) and `public/assets/manifest.json` (live site asset map, ~48 entries).
**Dev server:** `http://localhost:1441` — serves from `src/` + `public/` (source mode).
**Preview server:** `http://localhost:1440` — serves from built `dist/` (identical file set, different port).
**Local paths:** Identical for dev and preview; only the serving URL port differs (1441 vs 1440).
**QA gate:** All assets must pass `ls-artifact-qa` before status can change from `pending`.

| # | Name | Description | Status | File type | Local path | Dev URL | Preview URL | Notes |
|---|------|-------------|--------|-----------|------------|---------|-------------|-------|
| 1 | `architecture.html` | Explorable architecture diagram with dark/light toggle switch. Derived from `architecture.mmd` Mermaid source wrapped in archify HTML template. | ⬜ Pending | HTML | `docs/assets/architecture.html` (verified: 15 KB exists) | `http://localhost:1441/assets/architecture.html` | `http://localhost:1440/assets/architecture.html` | **Verified:** Only on-disk artifact from the tracker. All others pending creation. |
| 2 | `grav-yaml-to-agents.png` | Grav character illustration — YAML-to-agents metaphor. Part of the `ls-visual-storytelling` skill pipeline; brand-palette check required post-render (tolerance 3). | ⬜ Pending | PNG | `docs/assets/grav-yaml-to-agents.png` (not yet created; target convention from tracker) | `http://localhost:1441/assets/catalog/grav-yaml-to-agents.png` | `http://localhost:1440/assets/catalog/grav-yaml-to-agents.png` | **Evidence gap:** File not on disk. Target path inferred from `public/assets/catalog/` convention in manifest.json; actual output delegated to `ls-creative-director` → `ls-visual-storytelling` skill chain. |
| 3 | `grav-governance.png` | Grav character illustration — governance metaphor. Same render pipeline as #2; brand-palette check required. | ⬜ Pending | PNG | `docs/assets/grav-governance.png` (not yet created) | `http://localhost:1441/assets/catalog/grav-governance.png` | `http://localhost:1440/assets/catalog/grav-governance.png` | **Evidence gap:** File not on disk. Pipeline identical to #2. |
| 4 | `campaign-hero-1200x600.png` | Campaign hero image, 1200×600 pixels. Platform: custom hero ad. Production skill: `ls-brand-advertising`; dimensions enforced via generation brief. | ⬜ Pending | PNG | `docs/assets/campaign-hero-1200x600.png` (not yet created) | `http://localhost:1441/assets/catalog/campaign-hero-1200x600.png` | `http://localhost:1440/assets/catalog/campaign-hero-1200x600.png` | **Evidence gap:** File not on disk. Brief-based generation via `ls-brand-advertising` skill; dimensions 1200×600 per platform table. |
| 5 | `campaign-linkedin-1200x627.png` | LinkedIn ad creative, 1200×627 pixels. Single-image LinkedIn feed ad. Production skill: `ls-brand-advertising`. | ⬜ Pending | PNG | `docs/assets/campaign-linkedin-1200x627.png` (not yet created) | `http://localhost:1441/assets/catalog/campaign-linkedin-1200x627.png` | `http://localhost:1440/assets/catalog/campaign-linkedin-1200x627.png` | **Evidence gap:** File not on disk. LinkedIn ad format 1200×627 per platform specs. |
| 6 | `campaign-instagram-1080x1080.png` | Instagram feed ad, 1080×1080 pixels. Square format for Instagram feed. Production skill: `ls-brand-advertising`. | ⬜ Pending | PNG | `docs/assets/campaign-instagram-1080x1080.png` (not yet created) | `http://localhost:1441/assets/catalog/campaign-instagram-1080x1080.png` | `http://localhost:1440/assets/catalog/campaign-instagram-1080x1080.png` | **Evidence gap:** File not on disk. Square Instagram ad format. |
| 7 | `campaign-ig-story-1080x1920.png` | Instagram story ad, 1080×1920 pixels. Vertical story format. Production skill: `ls-brand-advertising`. | ⬜ Pending | PNG | `docs/assets/campaign-ig-story-1080x1920.png` (not yet created) | `http://localhost:1441/assets/catalog/campaign-ig-story-1080x1920.png` | `http://localhost:1440/assets/catalog/campaign-ig-story-1080x1920.png` | **Evidence gap:** File not on disk. Vertical story format 1080×1920. |
| 8 | `campaign-facebook-1200x628.png` | Facebook feed ad, 1200×628 pixels. Production skill: `ls-brand-advertising`. | ⬜ Pending | PNG | `docs/assets/campaign-facebook-1200x628.png` (not yet created) | `http://localhost:1441/assets/catalog/campaign-facebook-1200x628.png` | `http://localhost:1440/assets/catalog/campaign-facebook-1200x628.png` | **Evidence gap:** File not on disk. Feed ad format 1200×628. |
| 9 | `campaign-twitter-1600x900.png` | X/Twitter ad, 1600×900 pixels. Production skill: `ls-brand-advertising`. | ⬜ Pending | PNG | `docs/assets/campaign-twitter-1600x900.png` (not yet created) | `http://localhost:1441/assets/catalog/campaign-twitter-1600x900.png` | `http://localhost:1440/assets/catalog/campaign-twitter-1600x900.png` | **Evidence gap:** File not on disk. 1600×900 X/Twitter format. |
| 10 | `campaign-gdn-300x250.png` | Google Display ad, 300×250 pixels (standard banner). Production skill: `ls-brand-advertising`. | ⬜ Pending | PNG | `docs/assets/campaign-gdn-300x250.png` (not yet created) | `http://localhost:1441/assets/catalog/campaign-gdn-300x250.png` | `http://localhost:1440/assets/catalog/campaign-gdn-300x250.png` | **Evidence gap:** File not on disk. 300×250 standard banner. |
| 11 | `campaign-gdn-728x90.png` | Google Display ad, 728×90 pixels (leaderboard). Production skill: `ls-brand-advertising`. | ⬜ Pending | PNG | `docs/assets/campaign-gdn-728x90.png` (not yet created) | `http://localhost:1441/assets/catalog/campaign-gdn-728x90.png` | `http://localhost:1440/assets/catalog/campaign-gdn-728x90.png` | **Evidence gap:** File not on disk. 728×90 leaderboard format. |
| 12 | `campaign-gdn-336x280.png` | Google Display ad, 336×280 pixels. Production skill: `ls-brand-advertising`. | ⬜ Pending | PNG | `docs/assets/campaign-gdn-336x280.png` (not yet created) | `http://localhost:1441/assets/catalog/campaign-gdn-336x280.png` | `http://localhost:1440/assets/catalog/campaign-gdn-336x280.png` | **Evidence gap:** File not on disk. 336×280 format. |
| 13 | `campaign-gdn-970x250.png` | Google Display ad, 970×250 pixels (large rectangle/leaderboard). Production skill: `ls-brand-advertising`. | ⬜ Pending | PNG | `docs/assets/campaign-gdn-970x250.png` (not yet created) | `http://localhost:1441/assets/catalog/campaign-gdn-970x250.png` | `http://localhost:1440/assets/catalog/campaign-gdn-970x250.png` | **Evidence gap:** File not on disk. 970×250 large rectangle. |
| 14 | `campaign-billboard-1400x600.png` | Billboard creative, 1400×600 pixels. Production skill: `ls-brand-advertising`. | ⬜ Pending | PNG | `docs/assets/campaign-billboard-1400x600.png` (not yet created) | `http://localhost:1441/assets/catalog/campaign-billboard-1400x600.png` | `http://localhost:1440/assets/catalog/campaign-billboard-1400x600.png` | **Evidence gap:** File not on disk. 1400×600 billboard format. |
| 15 | `playground-fallback.png` | Terminal screenshot fallback for Playground component, 800×500 pixels. Production skill: `ls-frontend-design`. | ⬜ Pending | PNG | `docs/assets/playground-fallback.png` (not yet created) | `http://localhost:1441/assets/catalog/playground-fallback.png` | `http://localhost:1440/assets/catalog/playground-fallback.png` | **Evidence gap:** File not on disk. Terminal screenshot fallback; brand-palette constrained to `#070A40`/`#E63946`/`#00BFFF`/`#F2F2F2`/`#FFFFFF`/`#6B7280`/`#9CA3AF`. |

## Appendix: Live Site Asset Mapping (manifest.json)

The `public/assets/manifest.json` maps ~48 asset IDs to web-relative paths served identically on dev (`:1441`) and preview (`:1440`). These are the **live** catalog/insights/sectors/brand assets the Marketing Site serves at runtime. Key categories:

- **Offers** (`offer-a-digital-presence`, `offer-b-business-automation`, `offer-c-data-analytics`, `offer-d-digital-marketing`, `offer-e-platform-licensing`) — HTML placeholder pages under `public/assets/catalog/`
- **Sectors** (`industry-agri`, `industry-fintech`, `industry-gov`, `industry-health`, `industry-sme`, `sector-education`, `sector-financial-services`, `sector-government`, `sector-healthcare`) — HTML + SVG pairs
- **Capabilities** (`capability-...`) — SVG roadmap/process diagrams
- **Proofs** (`proof-...`) — SVG/diagram hybrids for pilot/demo/audit
- **Scenarios** (`scenario-fow01` through `scenario-fow08`) — Flow/svg scenario diagrams
- **Insights** (`insight-...`) — Dashboard/metrics HTML/SVG

These live assets are **separate** from the 15 planned generation-tracker assets above. The manifest entries are hand-maintained and serve the live site; the tracker assets are planned creative assets yet to be produced. No overlap exists between the two inventories per current repo state.

## Generation Workflow Reference

Per `docs/assets/README.md` generation commands:

- **Architecture diagram:** `cd docs/assets; npx -y @mermaid-js/mermaid-cli -i architecture.mmd -o architecture.svg` then wrap in HTML with archify template for dark/light toggle.
- **Grav illustrations:** Invoke `article-illustrations` skill with prompts; post-render palette check: `uv run python .agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py <file> --tolerance 3`
- **Campaign assets:** Dispatch to `media-generation-owner` via task; use generation brief template from spec with per-platform dimensions; QA each with `ls-artifact-qa`.
- **React components:** Implement in `src/components/`; use brand tokens `@import '../../brand/tokens/brand-tokens.css'`; import logos from ` '../../brand/logos/fulllogo/fulllogo.png'` (canonical); build & test with `bun run build` / `bun run lint`; visual QA with Playwright.

## QA Checklist (all assets)

- Palette: only `#070A40`, `#E63946`, `#00BFFF`, `#F2F2F2`, `#FFFFFF`, `#6B7280`, `#9CA3AF`
- Logo: official asset from `brand/logos/`, clear space = 1× "L" height
- Typography: Arial 700/400 only, sizes from brand scale
- Spacing: 4px base grid (4/8/12/16/24/32/48/64/96)
- Contrast: ≥ 4.5:1 for all text
- Grav illustrations (additional): floating gap under feet; performs core action (not decoration); original metaphor; accent colors (Orange flow, Red warnings, Blue system state); max 8 labels, 2–5 words each; ≥35% whitespace; palette checker PASS
- Campaign assets (additional): dimension-exact per platform; text in safe zones (≥15% inset); persuasion arc complete (6 beats); proof is traceable fact; Red reserved for CTA only
