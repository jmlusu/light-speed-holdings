# Design System: LightSpeed Holdings

## Overview

**Creative North Star: "The Editorial Sanctuary"**

LightSpeed Holdings is the AI-native company builder for Southern Africa. The visual system reflects institutional credibility with a disciplined, geometry-first aesthetic: navy as the anchoring authority, cyan as the trust signal, and red as the accent that demands attention. The design language treats the web as a set of editorial pages — structured, scannable, and grounded in hierarchy. Every element either serves the content or recedes. The North Star metaphor ("sanctuary") signals a space where AI governance feels not cold or abstract, but intentionally curated for human decision-makers.

**Key Characteristics:**

- Governance‑visible: the approval matrix, lifecycle, and honesty badges are not decoration — they are the product
- Typographic rhythm: Arial as the single system font, with a clear display‑to‑body scale
- Navy‑first colour strategy: the primary accent is rare by design, making its appearance meaningful
- Mobile‑first spacing: the 4px grid resolves to compact mobile units before expanding to desktop rhythm
- Transparency in evidence: the four-level honesty badge system (proven / pilot / fieldable / development) is surface‑visible, not hidden

## Colors

- **Primary: navy `#070A40`** — The anchoring authority. Used on ≤10% of any given screen. Its rarity is the point. (Rule: The One Voice Rule — the primary accent is used on ≤10% of any given screen.)
- **Accent: red `#E63946`** — The call‑to‑action signal. Used sparingly on buttons, link states, and error indicators.
- **Trust: cyan `#00BFFF`** — The trust and information signal. Replaces green in all status contexts. Used on focus rings, link colours, and success indicators.
- **Morning mist: `#F7F8F9`** — Light‑mode background. The almost‑white neutral that lets the navy and cyan breathe.
- **Deep mineral: `#121518`** — Dark‑mode background. The surface that navy type sits against.
- **White: `#FFFFFF`** — Used for card backgrounds, form surfaces, and text on navy/red.
- **Neutral palette (Material‑derived):** grey‑50 through grey‑900 for supporting roles: borders, muted text, disabled states.

### Named Rules

**The One Voice Rule.** The primary accent (navy `#070A40`) is used on ≤10% of any given screen. Its rarity is the point.

**The Cyan‑Is‑Trust Rule.** Cyan `#00BFFF` is the sole trust signal. It replaces green in all status, success, and error contexts.

## Typography

**Font family:** Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif (system font for performance and credibility)

**Font weight scale:** normal 400, medium 500, semibold 600, bold 700, black 900

**Font size scale (all in points, rendered at the 16px root):**

| Key | Size | Approx. px | Purpose |
|---|---|---|---|
| displayXl | 36pt | 48px | Hero headlines, cover titles |
| titleXl | 32pt | 42.7px | Major section titles |
| titleLg | 28pt | 37.3px | Section titles |
| titleMd | 24pt | 32px | Subsection titles |
| titleSm | 18pt | 24px | Card titles |
| subtitle | 16pt | 21.3px | Lead paragraphs, intros |
| bodyLg | 16pt | 21.3px | Comfortable body reading |
| body | 14pt | 18.7px | Default body text |
| bodySm | 13pt | 17.3px | Secondary body |
| caption | 12pt | 16px | Captions, footnotes, disclaimers |
| overline | 11pt | 14.7px | Uppercase labels, badges |

**Line height scale:** tight 1.1, snug 1.15, normal 1.25, relaxed 1.5, loose 1.6

**Letter spacing:** tight -0.02em, normal 0, wide 0.02em, wider 0.1em (for uppercase labels)

### Named Rules

**The Typographic Hierarchy Rule.** Display sizes are for hero and cover surfaces only; title sizes cascade through section heads; body is the default reading size; captions and overline are for meta information.

**The Arial‑Only Rule.** No custom web fonts are loaded. Arial is the single typeface family across all surfaces and modes.

## Layout

**Grid:** 12‑column, 1200px max width, 16px base unit (4px scale). The container pads 48px horizontally (spacing‑12) and has a vertical section rhythm of 64px (spacing‑16).

**Container:** max‑width 1200px, horizontal padding 48px.

**Section spacing:**
- Vertical: 64px (spacing‑16) on desktop
- Horizontal: 48px (spacing‑12) on desktop
- Mobile vertical: 48px (spacing‑12)
- Mobile horizontal: 24px (spacing‑6)

**Breakpoints:**
- mobile: 640px ( `(max-width: 639px)` )
- tablet: 640px (same as mobile in this implementation — the design is mobile‑first and the tablet breakpoint merges with mobile)
- laptop: 1024px ( `(min-width: 1024px) and (max-width: 1279px)` )
- desktop: 1280px ( `(min-width: 1280px) and (max-width: 1535px)` )
- largeDesktop: 1536px ( `(min-width: 1536px)` )

### Named Rules

**The Mobile‑First Rhythm Rule.** Vertical spacing steps up from 24px on narrow screens to 64px on desktop. The horizontal gutter is always half the vertical step. There is no separate tablet breakpoint — the mobile size carries through until the laptop query.

**The Navy‑Width Rule.** The 1200px max‑width center‑mass only expands when the content demands it — the navy rail on the left of dashboard‑style pages is a separate concern; on the marketing site the container stays fixed.

## Shapes

**Corner radius scale:** small 4px, medium 8px, large 16px, full 9999px

The design uses small (4px) and medium (8px) radii consistently. Full radius appears only on avatars and pill‑style badges. No surface uses border-radius: 0 as a default — even buttons have a 4px or 8px corner.

## Components

### Buttons

**Shape:** 4px (small) radius unless otherwise stated.

**Primary** (light mode):
- Background: red `#E63946`
- Text: white `#FFFFFF`
- Padding: 16px 48px (spacing‑4 horizontal, spacing‑8 vertical... wait, 16+48 = spacing‑4 + spacing‑12? Actually the token says padding: "16px 48px" which maps to spacing-4 horizontal and spacing-12 vertical? Let me re-check. The spacing scale is [4, 8, 12, 16, 24, 32, 48, 64, 96]. So 16px = spacing-4, 48px = spacing-12. So padding: spacing-4 vertical, spacing-12 horizontal. Actually the order in CSS is padding: vertical horizontal, so 16px top/bottom, 48px left/right = spacing-4 vertical, spacing-12 horizontal.)
- Border: none
- Hover: background `rgba(230, 57, 70, 0.9)`, shadow `rgba(230, 57, 70, 0.3)`, transform: translateY(-2px)
- Focus: same as hover + outline via `:focus-visible` (cyan 3px, 2px offset)

**Primary** (dark mode):
- Background: red `#E63946`
- Text: white `#FFFFFF`
- Same padding and hover treatments, but colors invert for the dark background

**Secondary** (ghost):
- Border: navy `#070A40` (light) / white `#FFFFFF` (dark)
- Text: navy `#070A40` (light) / white `#FFFFFF` (dark)
- Background: transparent
- Hover: background `rgba(7, 10, 64, 0.05)` (light) / rgba(255,255,255,0.1) (dark)

### Navigational elements

**Nav links:** colour cyan `#00BFFF`, underline on hover, transition 0.2s colour.

**CTA band:** The `CtaBand` component uses the primary red button and a secondary navy-stroked call to action.

### Honesty badges

Four-tier system displayed as border-color + background-color + text-color combinations:

- **Proven:** border `rgba(0, 191, 255, 0.4)`, background `rgba(0, 191, 255, 0.1)`, text `#00BFFF`
- **Pilot:** border `rgba(230, 57, 70, 0.4)`, background `rgba(230, 57, 70, 0.1)`, text `#E63946`
- **Fieldable:** border `rgba(156, 163, 175, 0.4)`, background `rgba(156, 163, 175, 0.1)`, text `#9CA3AF`
- **Development:** border `rgba(107, 114, 128, 0.4)`, background `rgba(107, 114, 128, 0.1)`, text `#6B7280`

### Page structure

- **Skip link** at top‑left, colour navy, focus state moves to top
- **Main content** landmark with id="main-content"
- **Section divider:** navy 1px horizontal rule on alternating sections, cyan on the in‑between sections
- **Focus ring:** cyan 3px with 2px offset on :focus-visible

## Do's and Don'ts

### Do

- Use navy `#070A40` as the primary accent, keeping it ≤10% of any screen surface
- Cyan `#00BFFF` as the trust signal — on focus rings, link colours, and success states
- Red `#E63946` as the CTA accent; use it sparingly
- Honesty badge colours exactly as specified — do not substitute or remix
- Arial as the single typeface family across all themes and surfaces
- 4px corner radius on buttons, inputs, cards, and containers
- 16px base unit / 4px scale for all spacing
- Vertical section rhythm of 64px on desktop, 48px on mobile
- The cyan focus‑visible ring (3px, 2px offset) on every focusable element
- Reduced‑motion: honour `prefers-reduced-motion` by collapsing all animation/transition durations to 0.01ms

### Don't

- Use green for status or success — cyan is the trust signal, not green
- Invent additional colour roles beyond primary/accent/trust/neutral
- Apply custom web fonts; Arial only
- Use border-radius: 0 on interactive components (buttons, inputs, cards)
- Add decorative drop shadows beyond the specified elevation tokens
- Layer more than one primary accent colour on a single surface
- Skip the skip link or focus-visible ring on the marketing site
