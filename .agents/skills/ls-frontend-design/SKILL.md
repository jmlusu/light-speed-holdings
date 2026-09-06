---
name: ls-frontend-design
description: "Builds distinctive, on-brand LightSpeed websites, landing pages, and web apps instead of generic AI-generated pages. Enforces the LightSpeed design system (navy/red/cyan, Arial type scale, 4px grid), visual hierarchy, responsive behavior, and the no-AI-slop checklist. Targets the repo's existing frameworks: Astro (marketing-site/) for fast content sites and Next.js 16 (website/) for app-like properties. QA via Playwright screenshots -> ls-artifact-qa. Trigger on: 'build a website', 'landing page', 'redesign the site', 'frontend', 'make a page for X', '/create-website'."
---

# LightSpeed Frontend Design

Build websites and landing pages that look intentional, branded, and human-designed — not like generic AI output.

## Preconditions

1. Load `ls-design-system` first — every layout decision flows from brand tokens.
2. Decide the target repo by project type:
   - **`marketing-site/`** (Astro 7 + Tailwind 4 + React 19) — content/marketing sites: landing pages, blog, docs, case studies. `npm run dev` (background mode: `astro dev --background`), `npm run build`.
   - **`website/`** (Next.js 16 + Tailwind 4 + React 19) — app-like properties. ⚠ Read `website/AGENTS.md` first — this Next.js version has breaking changes; consult `node_modules/next/dist/docs/`.
3. Never hand-write a logo — import from `static/brand/logos/**`. Reference tokens via `brand/tokens/brand-tokens.css`.

## The LightSpeed Web Pattern

### Layout & Structure
- **Hero** — one bold headline (navy, display size), cyan/subtitle supporting line, single primary CTA (navy button, red for primary emphasis), optional product/logo visual.
- **Navigation** — sticky top bar, full logo left, 4–6 links, CTA right; collapses to mobile menu.
- **Primary CTA sections** — pricing (3 tiers), testimonials (careful: only real client quotes), case studies, stats band (navy background, white/cyan accents).
- **Editorial sections** — white or light-grey alternating; spacing from the 4px scale (use 64–96px vertical rhythm between sections).
- **Footer** — navy, full logo + tagline, legal (`™` on first mention), contact.

### Styling (Tailwind + brand tokens)
| Token | Tailwind mapping |
|-------|------------------|
| `--ls-navy` `#070A40` | primary surface, headings |
| `--ls-red` `#E63946` | primary CTA, emphasis |
| `--ls-cyan` `#00BFFF` | links on dark, accents, tagline |
| `--ls-grey-light` `#F2F2F2` | section backgrounds |
| `--ls-white` `#FFFFFF` | page backgrounds |

Type: Arial stack, sizes from the brand scale (36/32/28/24/18/16/14/13/12). Grid: 12-col, 24px gutter, 48px margin, max-width 1200px.

### Interactions (framer-motion + lucide, already dependencies)
- Subtle fade/slide reveals on scroll (opacity + translateY ~16px, 0.4–0.6s).
- Hover states on cards/buttons (border/bg/translate, 150ms).
- Icons from **lucide-react** only. No gratuitous animation.

## The "No AI Slop" Checklist (Design Fundamentals)

- [ ] One clear visual hierarchy: exactly one hero message, one primary CTA per viewport
- [ ] Consistent vertical rhythm — sections breathe (≥64px gaps), no stacked-card wall
- [ ] Real content, not lorem ipsum — wire copy from the company registry / Pharos narrative / product facts (`company/`, `results/`, `static/brand/templates/one-pager.html`)
- [ ] No fake testimonial photos or invented quotes
- [ ] Contrast ≥ 4.5:1 for body text (navy on white passes; verify colored-on-color)
- [ ] Limited palette — brand colors only, accents used sparingly
- [ ] Typography scale respected — never more than 3 text sizes on a viewport
- [ ] Consistent spacing scale — no arbitrary margins
- [ ] Responsive: stack at <768px, no horizontal scroll, tap targets ≥44px
- [ ] Accessible: semantic headings (h1→h2→h3 order), alt text, focus states, nav landmark
- [ ] Iconography consistent (lucide set), same stroke weight everywhere

## Workflow

1. Load `ls-design-system`; pull live token values from `brand/tokens/brand-tokens.json`.
2. Read the brief from `ls-creative-director` (if present), else clarify artifact/audience/objective.
3. Choose target repo (marketing-site Astro vs website Next) per project type.
4. Wireframe section-by-section in the brief/comment, then implement with brand tokens.
5. Use official logo assets (relative imports into `static/brand/`); wire real links/CTAs.
6. Build locally (`npm run build` in the target repo) to verify no errors.
7. Screenshot key viewports via Playwright (see `ls-artifact-qa` `visual_check.js`).
8. Run `ls-artifact-qa` visual + brand + accessibility checks; fix; re-verify; approve.

## Quality Bar

A LightSpeed page should look engineered, not generated: strong hierarchy, lots of whitespace, deliberate color restraint, honest content. If it looks like a "typical AI website" (rainbow gradients, dense cards, meaningless badges, fake avatars), stop and rework until it clears the checklist.
