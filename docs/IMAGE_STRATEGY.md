# Image Strategy and Placement Policy

Decision record for GitHub issue `#381`. Supplies the placement, taxonomy, long-tail
and accessibility rules consumed by `#382` (content-model media fields) and `#386`
(build-ready image spec).

Provenance: authored by Claude Code from the repository as it stands. The delegating
process produced no reviewable artifact. Filed on the tracking issue for ratification.
Exception: the `#385` decision record below was ratified interactively by the delegating
operator on 2026-10-21.

Amended 2026-10-21 during `#382`: the delegating operator directed that AI-generated
imagery is permitted across the organization — marketing site, CEO Dashboard, slide
decks and video — and the taxonomy gains an `illustration` kind accordingly. The
amendment changes scope, not the honesty rules.

Ratified 2026-10-21 by the Human CEO in
[ADR-027](adr/027-ai-generated-imagery-policy.md): AI-generated imagery is permitted for
non-person subjects across every content surface, generated people and avatars are
prohibited, and human imagery is commissioned photography only. ADR-027 is the governing
record where this document and it disagree; the honesty rules below are unchanged by it,
and the `#385` section remains separately ratified.

## Constraints this policy inherits

These come from the repository, not from this document, and are not open to re-decide here.

- Honesty tones are `proven | pilot | fieldable | development` (`siteContent.ts:8`).
  `honestyLabel()` resolves them in the order `proven > pilot > fieldable > development`,
  with `development` as the fallback for any unrecognised label
  (`siteContent.ts:25-33`). Note that `pilot` is checked before `fieldable`, so a label
  containing both words resolves to `pilot`. This document preserves that order rather
  than imposing a severity ranking the code does not have.
- No stock photos, no fake people, no illustrative stand-ins for real customers.
  AI-generated imagery is permitted for non-person subjects across every content
  surface per [ADR-027](adr/027-ai-generated-imagery-policy.md); generated people and
  avatars are prohibited. It may never stand in for a screenshot, a customer,
  a person or documentary evidence,
  and the organization design system's ban on AI images presented as documentary
  evidence still applies.
- Leadership carries no headshots; credibility is evidenced by other imagery.
- Diagrams are authored as inline React/SVG, not exported raster files.
- Screenshots must be freshly captured at implementation time; an existing
  `output/playwright/` file is a reference, never a source to copy.
- Official logos live in the canonical brand tree; they are never recreated.
- `company-registry.yaml` and the test suite are the source of truth for platform
  figures. A rendered image is not a citable source for a number.

## Principle 1 — Default to no image

Absence of a suitable asset is the normal, shippable state. Every page, section and
content record renders correctly with zero images. An image is an addition that has to
earn its place, not a gap to be filled. Never place an image for visual balance alone.

## Principle 2 — Ship honest labels with honest images

An image may not assert or imply a capability, maturity level, scale or customer
relationship beyond its subject's honesty tier. The surrounding rendered page must carry
the same `honestyBadge` as the record the image illustrates. A pilot screenshot labelled
only by a page heading that implies production readiness violates this principle. Where
a metric is shown, its badge travels with it.

## Principle 3 — No image depicts a human who has not consented

No stock photography, no generated people, no avatars standing in for real customers or
staff. A person's likeness may appear only when that person is a named, consenting
subject and the image is filed against their record. This subsumes the leadership
headshot exclusion; `leadership.ts` stays as it is and gains no media field.

## Principle 4 — One claim, one image

An image makes exactly one claim. Where a record carries several claims, pick the single
one the image actually supports. Do not combine unrelated points into a collage to fill
space, and do not let a decorative image sit next to unrelated text in a way that implies
association.

## Principle 5 — Implementation must not invent the diagram

Inline diagrams are authored as React/SVG against the real model. An image may not
present a flow, relationship or architecture that the code does not implement. If a
diagram requires a claim the repository cannot support, the diagram is wrong, not the
code.

## Principle 6 — Reuse is preferred; one source per image

Ship one canonical asset. Reuse it wherever the same claim recurs. Never keep two
divergent copies of the same image, and never resize-and-save a derivative as a new
source. A later derivative must be generated from the canonical original at build time.

## Principle 7 — Alt text describes purpose, not pixels

The alt text states what the image contributes to the page, not what it looks like. Never
restate the adjacent caption, never begin "image of" or "picture of", never stuff
keywords. The test is whether the sentence would lose meaning if the image failed to
load; if it would, the alt text is right.

## Principle 8 — Every image is responsive and self-describing

Every image is fluid, carries intrinsic `width` and `height` to prevent layout shift,
and must work in both themes — the site ships light and dark (30 `dark:` variant usages
in `src/`, and `output/playwright/` holds `-light-` and `-dark-` captures of the same
pages). A raster asset that only reads on one theme is a defect. No image may depend on
hover to convey information. Where an asset is decorative under `aria-hidden`, the
decorative treatment is an explicit, recorded decision rather than a default.

## Image taxonomy

Five kinds. A record carries at most one visual, so a record never holds two image
files and never holds a diagram alongside a screenshot.

| Kind | Purpose | Form | Alt treatment | Honesty coupling |
|------|---------|------|---------------|------------------|
| `screenshot` | A capture of a real surface in the product | Raster image, freshly captured | Informative — alt required | Tier travels with the image |
| `diagram` | A flow, relationship or architecture the code implements | Inline React/SVG; never an exported raster | Informative — alt required; adjacent text carries the detail | Must not exceed implemented capability |
| `metric` | A single number with its context | Inline component reading canonical data; never an exported raster | Informative — alt required, names the figure and unit | Badge travels with the number |
| `brand` | An official mark: LightSpeed logo, partner or client logo | SVG from the canonical brand tree | Decorative — `alt=""` beside an adjacent text mark | Not applicable |
| `illustration` | An image that explains or evokes an idea, explicitly not a capture of any real surface | Raster image, generated (Gemini Image API or Comfy Cloud) or authored | Informative — alt required | Must not imply a tier its subject does not evidence |

Six consequences of this table:

- `metric` is inline only. It exists as a kind because the metrics case needs a governed
  slot in the taxonomy, not because every number must be a file. A static export of a
  chart is a `screenshot` of that chart and is governed as one; it is never a `metric`.
- `diagram` and `metric` are not image files, so they carry no `src` and no intrinsic
  dimensions. Their size comes from the layout.
- A record holds one visual, so it never holds a `diagram` and a `screenshot` at once.
  Both would be two renderings of the same claim, which Principle 4 already forbids.
- `brand` is the only kind that may be decorative, because it is always adjacent to a text
  mark. No other kind may claim decorative status.
- `illustration` is the only kind that may be synthetic. Because it is never a capture, it
  cannot satisfy a surface that requires a `screenshot`, and an AI render of a product
  screen is an `illustration` at best, never a `screenshot`.
- `illustration` records its own provenance: `generated: true` is a literal on the type, so
  a synthetic asset cannot be typed as an authored or captured one. The literal cannot
  currently distinguish a hand-drawn Grav illustration from an AI render; widening it is
  tracked as follow-up #5 in [ADR-027](adr/027-ai-generated-imagery-policy.md).

## Long-tail defaults

Default to no image. These surfaces take no image unless an explicit exception is
recorded against the page:

- `legal/privacy`, `legal/terms`, `legal/dpa`
- `contact` and `ask`
- `404` and error states
- Job listings and any surface whose content is generated at runtime
- Sitemap, feed and print stylesheets

Shared chrome is exempt from this rule, because it is not a page: a header or footer
logo is permitted and is governed by the `brand` kind, not by this list.

Per-page exceptions are written into the page record, not into this document, and each
carries the reason it overrides the default.

## Alt-text policy

Extends a rule the codebase already applies: `aria-hidden` appears 108 times across 33
files in `src/`, almost always to suppress decorative iconography. This policy does not
introduce a new convention; it names the one already in use and extends it to images.

- **Informative** — `screenshot`, `diagram`, `metric`, `illustration`. Requires a real
  `alt`. It names the claim, not the appearance. An informative image with an empty or
  missing `alt` is a build failure. An AI-generated `illustration` is informative: the
  `alt` describes what it depicts, and never the fact that a model produced it.
- **Decorative** — `brand` only. Renders `alt=""` plus `aria-hidden="true"`. `alt=""` and
  `aria-hidden` are correct together: `alt=""` marks the element decorative, and
  `aria-hidden` stops the redundant text mark from being announced twice. Do not write
  an alt for a logo beside its own name.
- Never `alt="..."` on a decorative image. Screen readers announce it, and the reader now
  hears the brand name twice.
- A bare URL in the `alt` field is a defect, not a placeholder.

`ls-artifact-qa` checks alt presence and empty-heading presence on the rendered page. It
checks the rendered result, not the model, so a correct model with a missing render-site
still fails QA and must be fixed at the render site.

## Consequences for `#382`

1. `InsightBlock` stays the closed union `h | p | ul | quote`. `coverImage` is an
   optional field on `InsightArticle`, never a fifth block kind. Adding a block kind
   would break every exhaustive switch and every content document.
2. `Leader` gains nothing. There is no headshot field.
3. Sectors expose one optional visual of kind `screenshot`, `diagram` or `illustration`.
   `status` keeps gating the visual's tier.
4. Catalog records expose one optional visual of kind `screenshot`, `brand`, `metric` or
   `illustration`.
5. Shared media shape, discriminated on `kind` so the two inline kinds cannot carry a
   `src` and the raster kinds cannot omit it:

```ts
import type { HonestyTone } from './siteContent';

export type ScreenshotMedia = {
  kind: 'screenshot';
  src: string;
  alt: string;      // always a real description; never ''
  width: number;
  height: number;
  tone: HonestyTone;
};

export type BrandMedia = {
  kind: 'brand';
  src: string;
  alt: '';          // the empty literal is the only value this type accepts
  width: number;
  height: number;
};

export type DiagramMedia = {
  kind: 'diagram';
  alt: string;      // always a real description; never ''
  tone: HonestyTone;
};

export type MetricMedia = {
  kind: 'metric';
  alt: string;      // always a real description; never ''
  tone: HonestyTone;
};

export type IllustrationMedia = {
  kind: 'illustration';
  src: string;
  alt: string;      // always a real description; never ''
  width: number;
  height: number;
  tone: HonestyTone;
  generated: true;  // provenance literal; a synthetic asset cannot be typed as authored
};

export type ContentMedia =
  | ScreenshotMedia
  | BrandMedia
  | DiagramMedia
  | MetricMedia
  | IllustrationMedia;

export type SectorMedia = ScreenshotMedia | DiagramMedia | IllustrationMedia;

export type CatalogMedia =
  | ScreenshotMedia
  | BrandMedia
  | MetricMedia
  | IllustrationMedia;
```

The split is deliberate on three points. `BrandMedia.alt` is typed as the literal `''`, so
the compiler enforces the decorative rule from the alt-text policy instead of leaving it
to a comment, and `BrandMedia` carries no `tone` at all, so a brand mark cannot imply a
tier. The informative kinds type `alt` as a required `string`; that the value is
non-empty stays a review and `ls-artifact-qa` check, because the type system cannot
express "this string is not empty". `tone` reuses the existing `HonestyTone` rather than
redeclaring the four literals, so the media model cannot drift from `siteContent.ts`.
`illustration` carries `generated: true` as a literal, so a synthetic asset cannot be
typed as authored or captured; a real capture must use `ScreenshotMedia`, which has no
`generated` field at all. `SectorMedia` and `CatalogMedia` are narrower aliases because
each model exposes one visual only, and neither permits a brand mark standing in for
evidence.

## Decision record for `#385` — asset pipeline and performance

Ratified by the delegating operator in a grilling session on 2026-10-21. Supplies the
pipeline and performance half of the build-ready image spec consumed by `#386`.
Implementation stays tracked on `#385` (formally blocked by `#380` and `#387`); this
section records the policy, not the work.

### Corrections to stale premises

`#385` and `#380` were written against a tree that no longer exists:

- "`public/` currently serves only `brand/`" — false. `public/` also carries
  `assets/{catalog,diagrams,insights,sectors,...}` with its own `manifest.json`, plus
  `infographics/`, `visuals/`, `og-default.png`, the favicon chain and
  `robots.txt`/`sitemap.xml`.
- `#380`'s premise that the og image and favicons are undecided — both are already in
  `index.html` (`og:image` = `/og-default.png`, `favicon.svg`, `favicon.ico`). What
  remains open there is `twitter:card`, the canonical link tag, and favicon
  regeneration from the official icon-only mark (BRAND_ADOPTION_ROADMAP TODO 3.6).
- "the repo has zero `.webp`/`.avif`" — still true for `public/`: 259 image files,
  15.5 MB, PNG/JPG/SVG only, no `.avif` anywhere in the tree. But
  `data/media/registry.ts` already declares `.webp` and `.avif` sources that resolve
  to nothing on disk.

### Decision 1 — asset namespace: `public/assets/` is canonical

No new `public/images/`. The canonical tree is the one `docs/MEDIA_ARCHITECTURE.md`
already mandates — `public/assets/{brand,diagrams,hero,use-cases,insights,sectors,leadership}/`
with `manifest.json` alongside. `public/brand/` remains a copy-overlay sync mirror of
canonical `brand/`, owned by `scripts/build/sync-brand.ps1`, and is not a pipeline
input. `public/` itself stays web-root only: og image, favicons, robots, sitemap.

Consequences: `public/infographics/` and `public/visuals/` migrate into the canonical
tree as a tracked follow-up, not a blocker; `public/assets/catalog/` is archival per
the MEDIA_ARCHITECTURE migration table and takes no new content.

### Decision 2 — formats: MEDIA_ARCHITECTURE matrix, committed variants

The format matrix in `docs/MEDIA_ARCHITECTURE.md` is confirmed as-is: photography
AVIF → WebP → JPEG, diagrams and illustrations SVG (WebP where raster is needed), UI
icons SVG, PNG as lossless fallback. `#385` introduces no new format policy.

Variants are generated by an opt-in maintenance script (sharp-based, run manually or
periodically), committed to git, and enforced in CI on two axes: the per-kind budgets
from MEDIA_ARCHITECTURE (hero ≤ 150 KB, thumbnail ≤ 30 KB, SVG ≤ 50 KB) and existence
of every `src` the registry declares. Committed rather than build-time because the
deploy is a static Vercel SPA with no image transform service — assets rarely change,
and a native sharp dependency in every CI run buys nothing a maintenance pass does
not. The existence check is the fix for the currently-404 `.webp`/`.avif` paths in
`data/media/registry.ts`.

### Decision 3 — loading and responsiveness: one `SmartImage` wrapper

Principle 8 and MASTER_SPEC §25 become enforceable through a single shared wrapper
component (working name `SmartImage`) instead of per-component hand-rolling. It
mandates:

1. Lazy loading by default; `eager` only for declared above-fold/hero use (the pattern
   `OfferHeroMedia.tsx` already implements).
2. Intrinsic `width`/`height` on every raster `<img>` — today layout stability rests
   solely on CSS `aspect-*` wrappers, and no raster image carries intrinsic dimensions.
3. `<picture>` with AVIF/WebP `srcset`/`sizes` when variants exist, single-`src`
   fallback when they do not, so the wrapper works against today's PNG/JPG-only tree.
4. Required `alt` per the alt-text policy: a real description for informative kinds,
   `alt=""` + `aria-hidden` for `brand`.

No `srcset` exists anywhere in `src/` today (grep-verified); the wrapper is where that
gap closes. Existing components migrate opportunistically — no big-bang rewrite.

### Decision 4 — build integration

- **Registries.** `data/media/registry.ts` is canonical: typed, imported by components
  via `@lightspeed/data/media`. `public/assets/manifest.json` is generated from it by
  the maintenance script. CI fails on drift between the two, or on any registry `src`
  that does not resolve.
- **`sync-brand.ps1`.** Stays brand-only. It mirrors canonical `brand/` (logo,
  guidelines, logos, print, digital) to `static/brand/` and `public/brand/` with
  `-DryRun`/`-Prune`/`-Verify` modes; it never widens to content assets.
- **`#380` statics.** Land in `public/` root (og image, favicons — already there) and
  `public/assets/brand/` for anything brand-collateral-shaped; social-card templates
  belong in mirror-only `static/brand/social/`.
- **`#387` screenshots.** The migration table's "screenshots — delete, not strategic
  media" rule is honoured: only finalized exports are committed, into the matching
  canonical folder (`public/assets/{hero,diagrams,...}/`). Raw captures never land
  under `public/` at all; they stay outside the served tree (e.g. `output/playwright/`
  references and `reports/` evidence).

## Open items for ratification

1. `metric` has no canonical value source yet. It needs a decision between a typed
   reference to an existing figure in the model and sourcing the value at render time.
   The media union is shaped so either choice fits without reopening the taxonomy, but
   this decision is a genuine open question, not a detail.
2. No content image exists yet. The image files already in the tree are brand
   collateral — 68 under `brand/` and 72 under `public/brand/`, spanning full-colour
   logos, print pieces, social covers and email signatures — plus two dashboard icon
   SVGs in `src/ai_company/dashboard/static/icons/`, and 33 Playwright captures under
   `output/playwright/` that are visual references only, never asset sources. So no
   `width`/`height` values can be inherited from a precedent; they must be established
   per asset at implementation. Generation is now a lawful source for `illustration`:
   the delegating operator directed on 2026-10-21 that AI-generated imagery is permitted
   across the organization, and Gemini Image API and Comfy Cloud are already allow-listed
   under ADR-018 in `docs/APPROVED-VENDORS.md` (exception window expiring 2026-12-30). A
   raw model output is still not an asset — generated rasters must be post-processed to
   the brand palette and verified against `brand/tokens/brand-tokens.json` before
   commit, and they may only ever be typed `illustration`.

   The palette check is differentiated by asset class, per
   [ADR-027](adr/027-ai-generated-imagery-policy.md) §5. Flat graphic, diagram and vector
   assets keep the exact-match per-pixel gate (`check_brand_palette.py --tolerance 3`).
   Generated raster, photographic and continuous-tone imagery is checked for brand-token
   presence plus dominant-colour compliance instead: exact per-pixel matching on a
   photograph has no meaningful pass state, and applying it would make the permission a
   dead letter. Generated people and avatars are prohibited outright, not graded.
3. `CatalogIndustryVertical.iconName` remains a decorative Lucide icon name rather than a
   `ContentMedia`. This document does not change it; converting it is a separate change.
4. This draft tightened `metric` to the inline form. An earlier revision also permitted a
   rendered image of the metric component, which contradicted the "one visual per record"
   rule and would have needed `src`/`width`/`height` on `MetricMedia`. Restore the image
   form if a surface genuinely cannot render the component, and extend `MetricMedia` in
   the same change.
