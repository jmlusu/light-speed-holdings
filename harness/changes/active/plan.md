# Plan

## Technical Approach

1. Extract the canonical layer list into `src/components/haomtgv/layers.ts` so the page grid and the hero read from one source (`HaomtgvLayer` with `id`, `letter`, `title`, `description`, `heroDescription`, `Icon`).
2. Build `src/components/haomtgv/HaomtgvBlueprintHero.tsx` as a self-contained client component: gradient/graphic backdrop, 3-column desktop grid (headline + CTA | rotated slab stack | layer badges), vertical stack under `lg`.
3. Add hero keyframes to `src/index.css` (`ls-hero-drop`, `ls-hero-drop-text`, `ls-hero-slide`, `ls-hero-draw`, `ls-hero-float`, `ls-hero-breathe`) with a `prefers-reduced-motion` kill switch on `.ls-hero-motion`.
4. Replace the inline `<section>` hero in `src/pages/HAOMTVGPage.tsx` with `<HaomtgvBlueprintHero />` and drive the layer grid from `HAOMTGV_LAYERS`.
5. Wire the route in `src/App.tsx` (`withSite(HaomtgvPage)` at path `haomtgv`) to close the dangling nav link.

## Impacted Modules And Files

- `src/components/haomtgv/layers.ts` — new; shared layer data.
- `src/components/haomtgv/HaomtgvBlueprintHero.tsx` — new; 401 lines, exports `HaomtgvBlueprintHero` and `HaomtgvBlueprintHeroProps { backgroundImage?: string }`.
- `src/pages/HAOMTVGPage.tsx` — hero replaced, `PILLARS`/`Pillar` removed, duplicate `id="haomtgv-title"` removed.
- `src/index.css` — hero keyframes + reduced-motion guard appended to the utilities layer.
- `src/App.tsx` — import, `HAOMTVGPageRoute`, route entry.

## Interfaces, Data, Permissions

- `HaomtgvLayer` interface is the single contract between hero and page grid; adding a layer requires editing only `layers.ts`.
- `backgroundImage?: string` is the only hero prop; omitting it (or an `onError`) leaves the gradient base in place.
- No new permissions, network calls, secrets, or backend surface. No data fetching.

## Spec Gaps Found From Planning

- The blueprint assumes a hero photograph that does not exist in `public/`; resolved by CEO decision (gradient stand-in, swappable image).
- The blueprint's mobile scale (`0.7`) crops the slab stack at narrow widths; implemented `0.26 / 0.4 / 0.42` instead.
- The blueprint implies header branding and a hero photo credit; both omitted because `SiteLayout` already renders the global `Header`.

## Risks And Mitigations

- Palette drift from brand tokens → documented as an explicit deviation; values isolated as local constants so a future token migration is a two-line change.
- Connector geometry breaking at intermediate widths → connectors are desktop-only (`hidden lg:block`) and positioned from the grid, not from percentage-of-column math.
- Animation causing layout thrash or motion-sickness → transforms/opacity only, and `.ls-hero-motion` is disabled wholesale under `prefers-reduced-motion: reduce`.
- Unrelated staged work in the tree being swept into a commit → stage only the five task paths when committing.

## Verification Plan

- `npm run lint` (`tsc --noEmit --pretty false`) — must be silent.
- `npm run build` — must complete; record bundle sizes.
- Optional: Playwright screenshots at 1440×900 and 1024×768 to confirm slab/badge/connector alignment (not run; Playwright is not installed locally).
