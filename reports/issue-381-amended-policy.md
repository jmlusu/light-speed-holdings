## Image placement policy — **AMENDED FOR RATIFICATION** (replaces AI-authored draft)

> **Status: AMENDED, AWAITING HUMAN RATIFICATION.** This amendment corrects multiple falsified claims and internal contradictions in the original AI-authored draft. Every item below requires explicit human sign-off before it becomes binding, before the related implementation ticket (`#382`) proceeds, and before this issue is closed.

---

### ❌ Falsified claims in the original draft (now corrected)

| Original Claim | Reality | Correction |
|----------------|---------|------------|
| "zero `<img>` tags across `src/`" | **False** — infrastructure for images exists; policy must govern them | Removed. Policy now governs image placement where images *are* used. |
| `brand` kind forces `alt: ""` (decorative) | **Contradicts `visual_check.cjs`** which requires first instance `alt="LightSpeed Holdings Limited"` | Fixed: `brand-mark` kind now distinguishes **first instance** (informative alt) vs **repeats** (aria-hidden). |
| Four kinds: `screenshot`, `brand`, `diagram`, `metric` | **Mismatches `visual_check.cjs`** which expects: `screenshot`, `diagram`, `metrics`, `brand-mark`, `illustration` | Fixed: Union now uses exact `visual_check.cjs` taxonomy. |
| `honestyLabel()` substring matching is robust | **Fragile** — substring matching on badge labels breaks on wording changes | Fixed: Policy acknowledges fragility; recommends explicit `tone` field on records. |
| `metric` is inline-only, no component named | **Open question blocks `#382`** | Fixed: Policy names `MetricKpi` as the canonical inline component. |
| Brand logos are organized | **71 files with legacy/experimental duplicates** | Fixed: Policy designates canonical files and deprecates `_legacy*`, `.eps`, `.pdf`, experimental folders. |

---

### ✅ Corrected Core Principles

1. **No image by default.** Most content is stronger as type, space, and color. Add media only when it earns its weight.
2. **Provenance over decoration.** Every visual must be either an official brand asset or freshly captured from the running product. No stock photography, no generated people, no customer stand-ins, no recreated logos, no leadership headshots.
3. **Structure renders as structure.** Diagrams are inline React/SVG, not rasterized images.
4. **Diagrams inline; screenshots external.** Diagrams compose with surrounding type. Screenshots are real captures of the live product, referenced by path.
5. **One visual anchor per record.** At most one `ContentMedia` per record so each record has a single focal point.
6. **Honesty in the label, never the image.** Evidence tier (`proven > pilot > fieldable > development`) is carried by the existing `HonestyBadge` text component — never baked into an image. **Note:** `honestyLabel()` in `siteContent.ts:25-33` uses fragile substring matching; records should carry explicit `tone` fields where possible.
7. **Accessibility is structural.** Meaningful images carry real `alt`; purely decorative images use `aria-hidden="true"`. **Enforced by `ls-artifact-qa` via `visual_check.cjs`.**

---

### ✅ Corrected `ContentMedia` Union (aligns with `visual_check.cjs` expected types)

```ts
// File: src/types.ts (new exports)

type ScreenshotMedia = {
  kind: "screenshot";
  src: string;                    // Path to Playwright capture or static chart export
  alt: string;                    // REQUIRED, descriptive, ≤125 chars
  width: number;
  height: number;
  tone: "light" | "dark";         // Theme variant captured
  dataLsImageType: "screenshot";  // For visual_check.cjs
};

type BrandMarkMedia = {
  kind: "brand-mark";
  src: string;                    // MUST be from canonical brand/logos/ (see § Canonical Brand Files)
  alt: string;                    // First instance: "LightSpeed Holdings Limited"
  // Repeats: aria-hidden="true" (no alt)
  width: number;
  height: number;
  dataLsImageType: "brand-mark";
  dataLsLogoInstance: "first" | "repeat";  // For visual_check.cjs
};

type DiagramMedia = {
  kind: "diagram";
  alt: string;                    // REQUIRED, descriptive
  tone: "light" | "dark";
  dataLsImageType: "diagram";
  // No src, no intrinsic dimensions — inline React/SVG
};

type MetricsMedia = {
  kind: "metrics";
  alt: string;                    // REQUIRED, descriptive
  tone: "light" | "dark";
  dataLsImageType: "metrics";
  // No src, no intrinsic dimensions — inline component (MetricKpi)
};

type IllustrationMedia = {
  kind: "illustration";
  src: string;                    // Grav hand-drawn asset
  alt: string;                    // REQUIRED, descriptive
  dataLsImageType: "illustration";
  // Out of brand palette scope (white bg, black line, red/orange/blue accents)
};

type ContentMedia =
  | ScreenshotMedia
  | BrandMarkMedia
  | DiagramMedia
  | MetricsMedia
  | IllustrationMedia;
```

**Key alignment points with `visual_check.cjs`:**
- Every `<img>` **must** have `data-ls-image-type` with one of the 5 valid values
- `brand-mark` **must** have `data-ls-logo-instance="first|repeat"`
- Informative types (`screenshot`, `diagram`, `metrics`, `illustration`) **must** have descriptive `alt` (quality heuristics enforced)
- Decorative `brand-mark` repeats **must** have `aria-hidden="true"` and **no `alt` attribute**
- Alt quality heuristics (enforced by `visual_check.cjs`):
  - Rejects generic words: "image", "photo", "screenshot", "diagram", "chart", "graphic", "logo", "icon", "visualization", "figure"
  - Requires ≥10 characters
  - Requires ≥2 meaningful words (noun + verb/prepositional phrase)
  - Example good: `"LightSpeed agent registry dashboard showing 12 active agents across 3 departments"`
  - Example bad: `"Dashboard screenshot"` / `"Image of agent registry"`

---

### ✅ Canonical Brand Files (resolves 71-file mess)

**Canonical sources (only these 6 files are approved for production):**

| Use Case | Canonical File | Mirror |
|----------|----------------|--------|
| Headers/covers/light backgrounds | `brand/logos/fulllogo/fulllogo.png` | `static/brand/logos/fulllogo/fulllogo.png` |
| Dark backgrounds/overlays | `brand/logos/fulllogo/fulllogo_transparent.png` | `static/brand/logos/fulllogo/fulllogo_transparent.png` |
| Avatars/favicons/small spaces | `brand/logos/icononly/icononly.png` | `static/brand/logos/icononly/icononly.png` |
| Print (vector) | `brand/logos/fulllogo/vector/print.svg` | `static/brand/logos/fulllogo/vector/print.svg` |
| Legal/B&W | `brand/logos/grayscale/grayscale.png` | `static/brand/logos/grayscale/grayscale.png` |
| Text-only mark | `brand/logos/textonly/textonly.png` | `static/brand/logos/textonly/textonly.png` |

**Deprecated (do not use in new work):**
- All `_legacy*` files
- All `.eps` and `.pdf` files (use `.svg` for vector)
- All experimental folders: `Analog Nostalgia & Tech-Retro/`, `Glassmorphism/`, `Skeuomorphism/`
- All `Logo1.*`, `Logo2.*`, `Logo3.*` variants (use `fulllogo/` canonical)
- All `*_nobuffer*`, `*_nobuffer_legacy*` variants

**Action required:** Run `pwsh scripts/sync-brand.ps1` after cleanup so mirrors pick up canonical-only set.

---

### ✅ Placement Map for Implementation Ticket `#382`

| Surface | Decision | Media Kinds Allowed | Rationale |
|---------|----------|---------------------|-----------|
| `InsightBlock` | **Keep** closed `h \| p \| ul \| quote` union | None | Article-level media lives on `InsightArticle`, not inside a block |
| `InsightArticle` | Add one optional `ContentMedia` | `screenshot`, `diagram`, `metrics`, `illustration` | Captures a full article with one focal visual |
| `Leader` | **No** headshot field | None | Policy prohibits leadership headshots |
| `Sector` (`sector-registry.ts`) | One optional `screenshot` **or** `diagram` | `screenshot`, `diagram` | `sector-registry.ts` is canonical (5 page/component consumers); `sectors.ts` is legacy |
| Catalog record (`useCaseCatalogData.ts`) | Optional `screenshot`, `brand-mark`, or `metrics` | `screenshot`, `brand-mark`, `metrics` | Highest media density (logos, proof, metrics) |
| `CatalogIndustryVertical` | Keep `iconName` (Lucide) only | None | Not a `ContentMedia`; icon rendered inline via Lucide |

> **Ownership gate:** An active ECL change currently owns all of `src/data` and created `src/data/insights.ts`. `#382` implementation **must not proceed** until that active change is parked or closed and `src/data` ownership is released. This is a hard sequencing gate.

---

### ✅ Sourcing and Citation Rules

- `company-registry.yaml` (and its tests) remain the authoritative source for platform figures.
- Rendered images are **not** citable sources for metrics; numbers come from structured data, and the image visualizes that data.
- Screenshots must be **fresh captures** taken at implementation time from the running product. The checked-in `output/playwright/` directory is reference-only, not a shipping source.
- `brand-mark` assets **must** come from canonical files listed above.
- `illustration` assets come from `article-illustrations` skill output (Grav character IP).

---

### ✅ The `MetricKpi` Component (resolves open question)

**Canonical inline component for `metrics` kind:** `MetricKpi` (to be created in `src/components/MetricKpi.tsx`)

```tsx
// Props align with MetricsMedia
interface MetricKpiProps {
  label: string;           // e.g., "40% reduction in compliance reporting time"
  value: string | number;  // The headline number
  tone: "light" | "dark";  // Theme variant
  trend?: "up" | "down" | "stable";
  honestyBadge?: HonestyBadge; // Optional inline badge
}
```

- Renders as inline SVG/HTML (no `src`, no intrinsic dimensions)
- Uses LightSpeed palette (navy/red/cyan) — passes `check_brand_palette.py --tolerance 3`
- Carries `data-ls-image-type="metrics"` for `visual_check.cjs`
- Replaces the ambiguous "inline-only" description with a named, testable component

---

### ✅ `ls-artifact-qa` Gate as Enforcement Point (full rule set acknowledged)

The `visual_check.cjs` probe enforces **all** of the following (exit code 2 on any failure):

| Check | Blocker/Major | What It Catches |
|-------|---------------|-----------------|
| `horizontalOverflowPx > 0` | Blocker | Horizontal scroll at any viewport |
| `missingAltCount > 0` | Blocker | Any `<img>` without `alt` attribute |
| `emptyHeadingCount > 0` | Blocker | Empty `<h1>`, `<h2>`, `<h3>` |
| `untypedImageCount > 0` | Blocker | `<img>` missing `data-ls-image-type` |
| `invalidImageTypeCount > 0` | Blocker | `data-ls-image-type` not in 5 valid values |
| `decorativeWithAltCount > 0` | Blocker | `brand-mark` with `aria-hidden` **and** `alt` present |
| `informativeMissingAltCount > 0` | Blocker | `screenshot`/`diagram`/`metrics`/`illustration` missing `alt` |
| `altQualityFailures > 0` | Major | Alt text fails quality heuristics (generic, too short, insufficient descriptiveness) |
| `logoAltMismatchCount > 0` | Blocker | First logo not `alt="LightSpeed Holdings Limited"`; repeat logo missing `aria-hidden="true"`; missing `data-ls-logo-instance` |

**Policy implication:** Every production skill (`ls-frontend-design`, `ls-document-design`, `ls-presentation-design`, `ls-social-media-design`, `ls-brand-advertising`, `ls-diagramming`, `ls-visual-storytelling`) must emit images with these attributes. The `ls-artifact-qa` gate is non-negotiable.

---

### ✅ Human Ratification Checklist

Please react or reply to **each row** with **approve** / **amend** / **reject**:

- [ ] **Corrected core principles** (no-image default, provenance, structure-as-diagram, one anchor, honesty in label, alt accessibility, `honestyLabel()` fragility acknowledged)
- [ ] **Five-kind `ContentMedia` union** with exact field shapes matching `visual_check.cjs` taxonomy (`screenshot`, `brand-mark`, `diagram`, `metrics`, `illustration`)
- [ ] **Brand logo rule**: first instance `alt="LightSpeed Holdings Limited"` + `data-ls-logo-instance="first"`; repeats `aria-hidden="true"` + `data-ls-logo-instance="repeat"`
- [ ] **Canonical brand files** (6 approved) and deprecation of 65 legacy/experimental files
- [ ] **`MetricKpi` named as canonical inline component** for `metrics` kind
- [ ] **Placement map** for `InsightArticle`, `Sector`, catalog, `Leader` (no headshot), `CatalogIndustryVertical` (iconName only)
- [ ] **Sourcing rules**: `company-registry.yaml` authoritative; images not citable; screenshots fresh; brand assets canonical-only
- [ ] **Full `visual_check.cjs` rule set acknowledged** (alt quality, logo context, decorative-with-alt, untyped images, overflow, headings)
- [ ] **`src/data` ownership sequencing gate** before `#382` proceeds

---

### 🔗 Related Issues

- `#382` (implementation, **blocked on this ratification**)
- `#386` (build-ready image spec, blocked by `#382`)
- `#383`–`#385`, `#387` (grilling issues dependent on this policy)
- `#378` (depends on `docs/IMAGE_STRATEGY.md` — this policy supersedes)

---

**This issue stays open until a human ratifies (or amends) the above.** Implementation of the related tickets is blocked on ratification.

<sub>Policy authored by creative-director after adversarial review of AI draft. Grounded in `ls-design-system`, `ls-artifact-qa`/`visual_check.cjs`, `src/data/siteContent.ts`, `src/types.ts`, `brand/logos/` audit.</sub>