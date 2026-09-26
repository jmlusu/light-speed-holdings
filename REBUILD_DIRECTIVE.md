# LIGHTSPEED HOLDINGS — REBUILD DIRECTIVE

**Status:** MANDATORY
**Mode:** STRUCTURAL REBUILD
**Companion specification:** `MASTER_SPEC.md`

---

# 1. THIS IS NOT A PATCH

The existing LightSpeed Holdings website contains legacy structure.

You are NOT being asked to update the legacy site while preserving its architecture.

You are being asked to **replace the incompatible legacy architecture with the architecture defined in MASTER_SPEC.md.**

The objective is:

> **Implement the approved specification, not preserve the existing implementation.**

---

# 2. NON-NEGOTIABLE RULE

When the existing code conflicts with `MASTER_SPEC.md`:

**MASTER_SPEC.md WINS.**

Do not preserve a legacy component simply because:

- it already works
- it is already styled
- it is reusable
- it would be faster
- it has existing content
- deleting it requires more work

Architectural fidelity takes priority over minimizing code changes.

---

# 3. DO NOT PERFORM A CONTENT SWAP

The following does NOT count as a rebuild:

- changing old headings
- changing paragraphs
- changing button text
- changing colors
- replacing images
- renaming cards
- adding a few new sections
- keeping the old page hierarchy
- keeping the old navigation
- keeping old sections and inserting new ones around them

If the structure is wrong, remove it.

---

# 4. FIRST: READ THE SPECIFICATION

Before modifying implementation code:

1. Read `MASTER_SPEC.md` completely.
2. Inspect the repository.
3. Identify the existing application architecture.
4. Compare the two.
5. Create a legacy inventory.
6. Create a specification-to-code map.
7. Define the target architecture.
8. Only then begin implementation.

Do not begin by editing the first page you encounter.

---

# 5. CREATE LEGACY_INVENTORY.md

Document the existing application.

For each major item classify it:

## KEEP

Directly compatible with the new specification.

## MODIFY

Useful functionality that can be retained without preserving incompatible structure.

## REBUILD

Functionality whose underlying structure must be recreated.

## DELETE

Obsolete code, pages, components, routes, styles, assets, or content.

Use evidence from the repository.

---

# 6. CREATE SPECIFICATION_MAP.md

Map the specification to implementation.

Example:

| Requirement | Target implementation | Existing implementation | Action |
|---|---|---|---|
| New navigation | ... | ... | Rebuild |
| AI Company Builder | ... | ... | Rebuild |
| 90-agent model | ... | ... | Rebuild |
| Calm Intelligence | ... | ... | Rebuild |
| Light/Dark modes | ... | ... | Rebuild |
| Public/internal boundary | ... | ... | Rebuild |

Every major requirement must have a destination in the implementation.

---

# 7. DESIGN THE TARGET ARCHITECTURE

Before implementation, define:

- routes
- pages
- layouts
- navigation
- content/data model
- components
- design tokens
- state boundaries
- public/internal boundaries
- agent registry boundaries
- animation system
- responsive strategy

Do not derive this from the legacy page tree.

Derive it from `MASTER_SPEC.md`.

---

# 8. REBUILD THE INFORMATION ARCHITECTURE

The target architecture must support the approved public structure:

- Home
- What We Do
- AI Company Builder
- Solutions
- Sectors
- Proof
- Insights
- About
- Contact / Start a Conversation

Exact labels may be refined only when the underlying information architecture remains faithful to the specification.

---

# 9. REBUILD THE NAVIGATION

Inspect the existing navigation.

Delete obsolete:

- links
- dropdowns
- labels
- routes
- CTAs
- terminology

Implement navigation based on the target information architecture.

Do not preserve navigation merely because users are accustomed to it.

---

# 10. REBUILD THE HOMEPAGE

The homepage should follow the approved narrative:

1. Orientation
2. Core proposition
3. Strategy / Build / Govern / Research & Policy
4. AI Company Builder
5. 90-agent operating model
6. Solutions
7. Sectors
8. Proof
9. Insights
10. CTA

The legacy section ordering is not authoritative.

---

# 11. REMOVE LEGACY COMPONENTS

For every major legacy component ask:

> Would this component exist if we were building LightSpeed from MASTER_SPEC.md today?

If NO:

**DELETE IT.**

If YES:

verify that its implementation still matches the specification.

If uncertain, prefer rebuilding rather than carrying forward incompatible assumptions.

---

# 12. DO NOT HIDE THE LEGACY

Do not leave obsolete architecture underneath a new visual layer.

Remove:

- dead routes
- obsolete pages
- unused components
- duplicate components
- unused CSS
- obsolete design tokens
- legacy content
- dead imports
- obsolete assets
- duplicate constants
- old agent counts
- obsolete terminology

Search the entire repository after implementation.

---

# 13. 90 AGENTS IS THE CURRENT CANONICAL COUNT

The current LightSpeed operating model contains:

**90 AI agents**

Remove or replace references to:

- 127
- 144
- 152

unless they are explicitly required as historical information.

Do not introduce another agent count.

Centralize the canonical value.

---

# 14. PUBLIC SAFETY

Do not expose private implementation information.

Never publish:

- API keys
- credentials
- private prompts
- internal system prompts
- private memory
- private endpoints
- confidential client data
- internal orchestration instructions
- secrets
- security-sensitive configuration

Public agent information must come from an approved public-safe registry.

---

# 15. DESIGN REBUILD

Do not simply inherit the old CSS.

Implement the Calm Intelligence design direction:

**Calm → Curiosity → Clarity → Confidence → Action**

Use:

- Morning Mist / Alabaster `#F7F8F9`
- Slate / Deep Mineral `#121518`
- established LightSpeed brand accents
- stone
- water
- mist
- light
- space
- restrained depth
- subtle motion

Avoid:

- excessive neon
- cyberpunk aesthetics
- noisy gradients
- excessive glassmorphism
- animation for decoration alone
- visual clutter

---

# 16. LIGHT AND DARK MODE

Both themes must be intentionally designed.

Do not implement dark mode as a simple color inversion.

Check:

- contrast
- typography
- surfaces
- borders
- shadows
- imagery
- focus states
- motion
- readability

Test both modes on all major pages.

---

# 17. MOTION

Motion should be:

- restrained
- fluid
- purposeful
- performant

Use the principle:

**Slow to the eye. Fast to the mind.**

Implement reduced-motion behavior.

Do not allow animation to become a performance or accessibility problem.

---

# 18. CONTENT MODEL

Business facts must have canonical data sources.

Avoid duplicate hard-coded claims.

Especially centralize:

- agent count
- capabilities
- solutions
- sectors
- proof
- insights
- metrics
- leadership
- CTAs

If the same fact appears in multiple views, it should come from a common source.

---

# 19. PROOF AND CLAIMS

Do not fabricate:

- clients
- logos
- testimonials
- metrics
- awards
- partnerships
- project results
- revenue
- impact

If something is a prototype or demonstration, label it.

If evidence does not exist, do not imply that it does.

---

# 20. VALIDATION AFTER IMPLEMENTATION

Run:

- type checks
- linting
- tests
- production build
- route validation
- accessibility checks where available
- responsive checks
- light/dark checks
- broken-link checks
- unused-code checks

Then perform a specification audit.

---

# 21. CREATE IMPLEMENTATION_AUDIT.md

The audit must include:

## A. Removed Legacy Structures

List what was deleted.

## B. Rebuilt Structures

List what was rebuilt.

## C. New Structures

List what was created.

## D. Specification Coverage

Map each major MASTER_SPEC requirement to implementation.

## E. Retained Legacy Code

List every significant legacy structure retained and explain why.

"Already existed" is not a valid reason.

## F. Deviations

List anything that could not be implemented exactly.

For each deviation provide:

- requirement
- reason
- current implementation
- recommended resolution

---

# 22. FINAL LEGACY SEARCH

Before declaring completion, search for:

- old navigation labels
- obsolete page names
- duplicate components
- old agent counts
- old positioning statements
- obsolete CTA structures
- unused routes
- dead imports
- old CSS
- unused assets
- duplicate metrics
- legacy terminology

Any remaining legacy element must be either:

1. intentionally retained and documented, or
2. removed.

---

# 23. COMPLETION STANDARD

Do not report:

> "The website has been updated."

Report:

> "The legacy architecture was inventoried, incompatible structures were removed/rebuilt, the MASTER_SPEC was implemented, and the implementation was audited against the specification."

Only use that completion statement if the evidence supports it.

---

# 24. FINAL DECISION RULE

When choosing between:

**A. Preserve the legacy implementation**

and

**B. Implement MASTER_SPEC.md correctly**

always choose:

# B. IMPLEMENT MASTER_SPEC.md

The goal is a new LightSpeed Holdings experience.

**REBUILD. DO NOT PATCH.**
