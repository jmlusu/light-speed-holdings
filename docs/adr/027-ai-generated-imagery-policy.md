# ADR-027: AI-Generated Imagery Policy — Non-Person Subjects Permitted, Generated People and Avatars Prohibited

**Status:** Accepted
**Date:** 2026-10-21
**Accepted:** 2026-10-21
**Deciders:** Human CEO, CMO, CISO, Creative Director
**Technical Domain:** Marketing / Brand / Governance

## Context

Light Speed Holdings already has a governed media generation capability (ADR-018: `media_generation_owner`, `comfyui-mcp` allowlist, 5-tier HITL), an approved vendor path for image generation (`docs/APPROVED-VENDORS.md:24` Google AI / Gemini Image API, `:25` Comfy Cloud, both scoped to AI-generated imagery under ADR-018), a five-kind media taxonomy in `docs/IMAGE_STRATEGY.md`, and a ratified implementation spec in `docs/IMAGE_SPEC.md` covering `screenshot`, `diagram`, `metrics`, `brand-mark`, and `illustration`.

What the repository does **not** have is a single statement of *when AI-generated imagery is allowed* that agents can act on. The rule is currently scattered and, in places, contradictory:

- `docs/IMAGE_STRATEGY.md:28-32` forbids stock photos and "fake people" but permits AI-generated imagery "for illustration only", while `docs/LIGHTSPEED_DESIGN_SYSTEM.md:623` restricts human imagery to "real people".
- `docs/adr/018-comfyui-media-generation.md:11` names "chatbot avatars" as an Offer B use case, which is incompatible with a ban on generated people.
- `.agents/skills/ls-design-system/SKILL.md` contains **no** imagery policy at all, so the brand system that every creative skill loads first says nothing about generated assets.
- `.agents/skills/ls-artifact-qa/SKILL.md:36` enforces the palette gate with per-pixel exact matching (`check_brand_palette.py <image> --tolerance 3`), which is a category error when applied to photographic or otherwise continuous-tone generated rasters.
- `src/types.ts:207-215` types `IllustrationMedia` with a required literal `generated: true`, so an authored Grav hand-drawn illustration cannot be represented as authored.

Meanwhile the enforcement layer is already permissive: `harness/qa/visual_check.cjs:109` accepts `illustration` as a valid `data-ls-image-type`, and `:117` treats every kind except `brand-mark` as requiring informative alt text. `docs/sectors-media-plan.md:46` already anticipates AI renders as a normal input to the pipeline.

The Human CEO has ruled on the underlying question. This ADR records that ruling, scopes it, and fixes the contradictions so agents do not have to re-derive policy per task.

## Decision

### 1. AI-generated imagery is permitted for non-person subjects, everywhere

AI-generated imagery **may** be used across all Light Speed Holdings content and artifacts, including the marketing site, the CEO Dashboard, slide decks, video, documents and reports, social assets, advertising creative, diagrams, and infographics.

There is no surface-level allowlist and no per-artifact veto. The constraint is on **subject matter and kind**, not on where the asset appears.

### 2. Generated people and avatars are prohibited

- **No AI-generated depictions of people.** No generated faces, bodies, hands, crowds, or person-shaped stand-ins for real individuals, customers, employees, or leadership.
- **No generated avatars.** Profile images, bot/persona avatars, and speaker headshots must not be AI-generated. This supersedes `docs/adr/018-comfyui-media-generation.md:11` ("chatbot avatars") as a permitted use case.
- **Human imagery is commissioned photography only.** Where an artifact needs a person, it uses real, consented, commissioned photography carrying the appropriate model/property release. Where consent or release is absent, no human subject is used.
- **Leadership carries no headshots** in generated or placeholder form (`docs/IMAGE_STRATEGY.md:23` remains in force).

### 3. Hero and narrative imagery uses non-human subjects

The default hero/narrative vocabulary is geometry, infrastructure, environment, product surfaces, and abstract data. A page that "needs a person" to work is a brief that needs rewriting, not an image that needs generating.

### 4. Generated imagery is the `illustration` kind

Generated assets enter the taxonomy as `illustration` (`docs/IMAGE_STRATEGY.md` five-kind table; `docs/IMAGE_SPEC.md:21-31`; `src/types.ts:207-215`). A generated image may not be presented as:

- a `screenshot` of an actual Light Speed surface,
- a `metric` or chart of real data,
- a `brand-mark` (official logos come only from the canonical brand tree, never recreated, resized, or recoloured),
- or documentary evidence of a real event, person, or customer.

Authored (Grav) hand-drawn illustration and AI-generated illustration share the kind; they are distinguished by provenance, not by taxonomy (see §6).

### 5. The palette gate is differentiated by asset class

The brand gate is not weakened wholesale. It is applied per asset class:

- **Flat graphic and diagram assets** (SVG/vector, charts, diagrams, infographics, logos, illustration with flat fills): per-pixel exact matching stays, via `check_brand_palette.py <image> --tolerance 3`. These are authored to token values and should hit them exactly.
- **Generated raster / photographic / continuous-tone imagery**: exact per-pixel matching does not apply. Compliance is assessed as **brand-token presence and dominant-colour compliance** — the asset must read as on-brand (navy-dominant, with red and cyan as accents per `.agents/skills/ls-artifact-qa/SKILL.md:37`) rather than match hexes pixel-for-pixel. The intent of `docs/sectors-media-plan.md:46` ("post-process and checker-verified") is preserved as "post-process until it reads on-brand", not "post-process until it is pixel-exact".

This requires a change to `.agents/skills/ls-artifact-qa/SKILL.md:35-37`. That change is a follow-up implementation task, tracked separately; this ADR sets the rule.

### 6. Provenance must be recorded

Every `illustration` asset records how it was produced: authored by the Grav IP, or AI-generated. Vendor, model, and prompt provenance attach to the asset record, not to the taxonomy.

`IllustrationMedia.generated` currently being a required literal `true` (`src/types.ts:214`) prevents expressing authored work. Widening it (to `generated: boolean` plus a `provenance` field, or equivalent) is a follow-up task; until then, provenance for authored illustrations is recorded out-of-band and the gap is known rather than hidden.

### 7. Vendor and disclosure obligations are unchanged

Generation still routes only through allow-listed vendors (`docs/APPROVED-VENDORS.md:24-25`, windows currently to `2026-12-30`; `docs/research/ai-gen-image-feasibility.md:76` still cites the earlier `2026-12-22` and should be reconciled when next touched). Sending prompts or reference images to a third-party host remains subject to `docs/SKILL_CURATION_POLICY.md` § Skill Third-Party Transmission Ban. Customer-facing AI-content disclosures remain governed by `docs/legal/terms-of-service.md:80-83, 158-160, 190` and are not relaxed by this ADR.

## Rationale

**Why a blanket permit with a narrow prohibition.** A surface-by-surface allowlist would force an agent to check a table before generating anything, and would leave most artifacts unaddressed. Ruling on subject matter instead is one rule that covers every surface: generate whatever the artifact needs, as long as it is not a person.

**Why the person/avatar ban is absolute rather than "disclose it".** Generated people create an identity, consent, and misrepresentation surface that disclosure does not close — a disclosure does not create a release. The existing `docs/LIGHTSPEED_DESIGN_SYSTEM.md:623` "real people" intent is correct; the problem was that it was unproducible. Commissioned photography makes it producible.

**Why the palette gate is split.** Exact per-pixel matching on a photograph cannot pass and cannot be made to pass without destroying the image's purpose. Keeping that gate universal would have made the permission a dead letter — an agent would either generate nothing or ship assets that fail QA by construction. Differentiating by asset class keeps the strict gate where it is achievable and meaningful, and substitutes a defined, checkable standard where it is not.

**Why provenance is a first-class requirement.** Once the same taxonomy kind contains both authored and generated work, "illustration" stops implying authorship. Recording provenance is what keeps the assets auditable and keeps the honesty posture intact.

## Consequences

- **Positive:** One actionable rule replaces scattered, contradictory guidance; agents can generate non-person imagery for any surface without a policy lookup; the avatar ban is explicit and closes the ADR-018 Offer B conflict; the taxonomy and `visual_check.cjs:109` already support `illustration`, so no enforcement rewrite is needed for the kind itself; the palette gate becomes achievable for generated rasters instead of failing by construction; commissioned photography becomes the stated path for human imagery, which is both compliant and producible.
- **Negative / risk:** Generated imagery is not reproducible from the repository, so assets must be committed with provenance rather than regenerated; brand drift in continuous-tone assets is judged rather than measured, which is softer than a pixel gate and depends on `ls-artifact-qa` discipline; the `illustration` kind now has mixed provenance until `src/types.ts:214` is widened, so an authored asset can be mistyped as generated; `static/brand/templates/generate-social-assets.py` already produces **avatar** assets locally, which this policy prohibits — that tool needs an explicit carve-out (non-person social assets only) or a change, and is a follow-up; there is no video production skill in the Creative Production Stack, so "video" in §1 currently routes only through Comfy/Seedance and its governance is undocumented.
- **Neutral:** No change to `company-registry.yaml`, no new specialist, no `pyproject.toml` dependency, and no change to the 5-tier HITL matrix. ADR-018 remains Accepted in full except line 11; this ADR supersedes only that use case. `docs/BRAND_ADOPTION_ROADMAP.md:125-135` Phase 6 (illustration style guide 6.1, photography guidelines 6.3) becomes the home for the detailed art direction and is not blocked by this ADR.

## Alternatives Considered

- **Per-surface allowlist (marketing site yes, dashboard no, decks yes, …):** Rejected — it is a lookup table agents must consult per task, it leaves most surfaces unaddressed, and it re-litigates the same question every time a new artifact type appears.
- **Permit generated people with disclosure:** Rejected — disclosure does not create consent or a release, and a generated face of a plausible employee or customer is a misrepresentation risk regardless of labelling.
- **Keep the exact-match palette gate for all assets:** Rejected — exact per-pixel matching is unachievable for continuous-tone imagery, so it would make the permission unusable and push agents either to generate nothing or to ship known-failing assets.
- **Restrict generated imagery to `docs/assets/` and internal artifacts:** Rejected — the same asset classes serve customer-facing and internal surfaces, and splitting policy by destination doubles the rule set for no governance gain.
- **Leave the policy in `IMAGE_STRATEGY.md` only:** Rejected — that document is scoped to website content media, does not bind decks, video, documents, social, or ads, and is not loaded by the creative skills that actually produce those artifacts.

## Status

Accepted and effective 2026-10-21 on the authority of the Human CEO.

Follow-up implementation tasks (tracked separately, not part of this ADR):

1. `.agents/skills/ls-artifact-qa/SKILL.md:35-37` — differentiate the palette gate by asset class and correct the stale `#E63946` reference. **Done 2026-10-21.**
2. `.agents/skills/ls-design-system/SKILL.md` — add the imagery policy (previously absent). **Done 2026-10-21.**
3. `docs/IMAGE_STRATEGY.md` — complete the 2026-10-21 amendment: alt-text policy, consequences for `#382` items 3 and 4, and the illustrative TS block. **Done 2026-10-21.**
4. `docs/IMAGE_SPEC.md:23` — correct the `src/types.ts` citation (declared 219–270; actual 205–227). **Done 2026-10-21.**
5. `src/types.ts:214` — widen `IllustrationMedia.generated` so authored illustrations are expressible.
6. `static/brand/templates/generate-social-assets.py` — remove or gate the avatar output path.
7. Video production path — either add a video skill to the Creative Production Stack or document the Comfy/Seedance exception.
8. **Brand red divergence (pre-existing, blocks reliable palette gates).** `reports/WCAG_AA_FIX_SUMMARY.md` records red moving `#E63946` → `#DC3641` (rgb 220, 54, 65) for WCAG AA, and most skills/templates already use `#DC3641`, but `brand/tokens/brand-tokens.json:21`, `brand/tokens/brand-tokens.css:8,75` and `docs/LIGHTSPEED_DESIGN_SYSTEM.md:89,119,171,185,537` still carry `#E63946`. `tasks/brand-update/todo.md` WS-B is still unchecked. Until the token files move, `check_brand_palette.py` (which reads the token file) will accept a hex the brand documents reject. Owner: CMO with design-system owner; needs a token-file change plus mirror re-sync (`pwsh scripts/build/sync-brand.ps1`).

## Links

- ADR-018 — `docs/adr/018-comfyui-media-generation.md` (superseded only at line 11, "chatbot avatars")
- `docs/IMAGE_STRATEGY.md` — five-kind taxonomy, honesty tones, no-stock/no-fake-people constraints
- `docs/IMAGE_SPEC.md` — media spec v1.0, taxonomy field shapes, `#DC3641`, screenshot pipeline
- `docs/LIGHTSPEED_DESIGN_SYSTEM.md:612-633` — Imagery & Media art direction, `:623` human imagery
- `src/types.ts:195-227` — `DiagramMedia`, `MetricMedia`, `IllustrationMedia`, `ContentMedia`, `SectorMedia`, `CatalogMedia`
- `.agents/skills/ls-artifact-qa/SKILL.md:35-37` — palette gate and dominance rule
- `.agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py` — exact-match gate, default tolerance 3.0
- `harness/qa/visual_check.cjs:109,117` — valid `data-ls-image-type` values; informative-alt-text set
- `docs/APPROVED-VENDORS.md:24-25` — Google AI / Gemini Image API, Comfy Cloud
- `docs/sectors-media-plan.md:46` — prior AI-render post-processing precedent
- `docs/BRAND_ADOPTION_ROADMAP.md:125-135` — Phase 6 illustration style guide and photography guidelines
- `docs/legal/terms-of-service.md:80-83, 158-160, 190` — AI-content disclosure and liability clauses
