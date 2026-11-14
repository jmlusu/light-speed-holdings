# LightSpeed Holdings Limited — Organization Design System

**Document type:** Canonical organization-wide design standard
**Version:** 1.1
**Status:** Reconciled with LightSpeed Holdings Brand Guidelines v1.0.1
**Applies to:** Brand identity, public website, digital products, AI Venture Studio, Pharos Insights, research and policy outputs, presentations, reports, diagrams, social media, and agent-generated artifacts
**Primary principle:** One organization, one recognizable visual language, many fit-for-purpose expressions.

---

## 1. Purpose

This document defines how LightSpeed Holdings Limited should look, sound, communicate, and behave across its public and internal-facing artifacts. It is intended to be usable by human designers, developers, strategists, researchers, vendors, and AI agents.

The design system must make complex strategy, data, automation, and AI easier to understand. It must create confidence without looking cold, communicate innovation without relying on gimmicks, and make the organization feel coherent across different sectors, channels, technologies, and geographies.

This is an organization-wide standard, not a specification for one webpage or one frontend framework.

### 1.1 What this system must achieve
- Establish a distinctive, credible LightSpeed identity.
- Express the idea of an AI-Native Company through useful, understandable design rather than decorative AI tropes.
- Make strategy and complex operating models clear enough to act on.
- Create reusable visual and interaction patterns, reducing one-off design decisions.
- Support public communication, executive decision-making, delivery work, research, and governance.
- Work across light and dark themes, desktop and mobile, digital and print.
- Remain technology-agnostic: design intent must not depend on one coding agent, framework, model provider, or design application.
- Keep public-facing marketing separate from internal operational interfaces and confidential information.
- Enable controlled evolution through explicit tokens, documented decisions, review, and versioning.

### 1.2 Design north star
**Calm Intelligence** — a design experience that moves people through:
> **Calm → Curiosity → Clarity → Confidence → Action**

- **Calm:** The interface feels composed, legible, and intentional.
- **Curiosity:** Visual depth, useful imagery, and well-framed questions invite exploration.
- **Clarity:** Information is structured; jargon and decorative complexity are reduced.
- **Confidence:** Evidence, status, governance, and limitations are visible.
- **Action:** Every important page or artifact gives the audience a clear next step.

### 1.3 Official tagline
```text
ASPIRE. ACT. ACHIEVE.
```
This is the authoritative LightSpeed Holdings tagline. Preserve the exact wording, capitalization, punctuation, and order in all brand applications. Do not substitute a different tagline or treat an alternative campaign line as the corporate tagline. Supporting copy may be developed for specific contexts, but must not be presented as the official tagline.

---

## 2. Organization and brand architecture

LightSpeed Holdings is an AI-native strategy, transformation, technology, and venture-building organization. Its work may span advisory, AI-enabled operating models, automation, intelligence, research, policy, and the creation of new ventures.

The visual system should accommodate these activities without making the organization appear to be a collection of unrelated brands.

### 2.1 Master brand
**LIGHTSPEED HOLDINGS LIMITED™** is the official first-mention form for public-facing and operational brand artifacts. Use the trademark symbol (™) on the first mention of the company name in each standalone artifact, in accordance with the Brand Guidelines. Later references may use “LightSpeed Holdings” or “LightSpeed” when the identity remains unambiguous.

The company name, official tagline, logo assets, palette, typography, and layout rules are governed by Brand Guidelines v1.0.1 and its canonical token files.

Do not imply that LightSpeed is limited to one country or region. The organization is based in Malawi and may work across Malawi, SADC, Africa, and other markets as appropriate.

### 2.2 Offerings and practice expressions
Offerings should be expressed as parts of the master brand unless an explicit brand architecture decision approves a distinct identity:
- **AI Venture Studio / AI Company Builder:** Strategy-to-build capability for designing, launching, and improving AI-enabled ventures and companies.
- **Workflow Collapsing:** Simplifying multi-step work into shorter, better-orchestrated processes.
- **Agentic Automation:** Applying governed AI agents and tools to defined workflows.
- **Self-Service Market Intelligence:** Making useful intelligence easier to access, interpret, and act on.
- **Pharos Insights:** Thought leadership, research, analysis, and evidence-led perspectives.
- **Strategy, Build, Govern, Research & Policy:** Capability language that may be used to explain the range of work.

Use a shared visual foundation. Offerings may use different imagery, diagrams, or accent treatments, but must not invent separate logos, unrelated palettes, or incompatible typography.

### 2.3 Audience contexts
Design for several audiences without fragmenting the brand:
- Executives and decision-makers
- Public-sector and institutional leaders
- Private-sector organizations and entrepreneurs
- Development partners and donor-funded programs
- Researchers, universities, and policy stakeholders
- Technical teams and implementation partners
- Prospective venture founders and collaborators

Use audience-appropriate vocabulary and evidence. Do not assume every audience is technical.

### 2.4 Public and internal boundaries
The public website is a client-facing marketing and engagement experience. Internal dashboards, agent workspaces, orchestration systems, operational reports, and confidential CEO materials are separate product contexts.

- Do not expose internal dashboard routes, agent logs, private prompts, internal metrics, credentials, or implementation details on public pages.
- Reuse brand tokens where appropriate, but let internal tools optimize for operational density and task completion.
- Never use a public marketing layout as a reason to weaken internal access control.
- Never use private operational data as public proof without explicit approval and validation.

---

## 3. Brand personality and design principles

### 3.1 Personality
LightSpeed should feel:
- **Strategic:** It understands the whole system, not just a single tool.
- **Technically credible:** It understands architecture, implementation, data, and governance.
- **Calmly ambitious:** It is forward-looking without shouting.
- **Human-centered:** Technology serves human intent and real-world outcomes.
- **Precise:** Claims, labels, diagrams, and interactions are purposeful.
- **Resource-aware:** Solutions should consider cost, maintainability, local capacity, and open-source/open-weight options where appropriate.
- **Accountable:** Limitations, uncertainty, evidence, and decision rights are not hidden.

### 3.2 Core principles
1. **Clarity before spectacle.** Depth and animation should aid comprehension, not compete with it.
2. **Purpose before decoration.** Every visual element should explain, orient, distinguish, or help the user act.
3. **Human authority remains visible.** AI is an instrument of human intent; important decisions and accountability must remain explicit.
4. **Evidence before assertion.** Never invent outcomes, client relationships, statistics, certifications, or endorsements.
5. **Depth with restraint.** Use layered surfaces, topographic contours, spatial composition, and subtle parallax to suggest depth without visual noise.
6. **Consistency without monotony.** Shared tokens and patterns create coherence; content-specific visuals create interest.
7. **Accessible by default.** Contrast, keyboard access, responsive behavior, and reduced motion are core requirements.
8. **Technology-agnostic intent.** The same design can be implemented in React, another web framework, slides, print, or a design tool.
9. **Progressive disclosure.** Show the most useful information first; reveal complexity when it helps.
10. **Honest maturity signals.** Clearly distinguish available services, prototypes, concepts, pilots, and verified results.

### 3.3 What the brand is not
Avoid design that feels:
- Like a generic AI startup template filled with glowing brains, robot heads, or arbitrary neon gradients.
- Aggressive, frantic, noisy, or saturated with animation.
- Overly corporate to the point of being anonymous.
- Like a crypto trading platform, gaming interface, or science-fiction control room.
- Dependent on fake dashboards, invented metrics, or unsupported customer logos.
- So minimalist that navigation, meaning, or the next action becomes unclear.

---

## 4. Logo and identity assets

### 4.1 Logo principle
Use only the approved logo assets in `brand/logo/`. The Brand Guidelines identify the current logo symbol as a lighthouse/shield emblem with signal waves. The logo artwork has an approved artwork palette that is distinct from the general UI tokens under ADR-027. Do not reinterpret, modernize, redraw, or approximate the official mark.

### 4.2 Approved use
- Canonical source: `brand/logo/`; runtime mirrors may exist at `static/brand/logo/` and `public/brand/logo/`.
- Use an official SVG for scalable digital use and SVG/PDF/EPS for print. Use the correct approved transparent PNG when raster artwork is required, especially on non-white backgrounds.
- Select a variant by inspecting its actual wordmark color and background compatibility. The Brand Guidelines note that some variant labels and descriptive rows conflict; the pixel-verified transparent-variant guidance takes precedence over an ambiguous filename description.
- Preserve proportions, alignment, and internal geometry.
- Maintain clear space equal to 1× the logo's “L” height on all sides.
- Minimum size: full logo 120 px wide on screen and 30 mm wide in print; icon/mark 32 px on screen and 12 mm in print.
- Use the mark alone only where appropriate and where the wordmark is already present or the placement is a recognized icon/avatar context.
- Ensure the logo remains legible at actual display size.

### 4.3 Do not
- Recreate, redraw, stretch, skew, rotate, distort, outline, bevel, or add effects to the logo.
- Change logo colors. The logo artwork's approved palette is a documented exception to general UI tokens; do not normalize it to the UI palette.
- Rebuild the logo with text characters or approximate geometry.
- Place it on a visually busy background without a suitable quiet area.
- Put text, borders, or decorative elements inside the clear-space area.
- Use a low-resolution raster asset where an appropriate vector is available.
- Use the retired legacy lighthouse-in-shield suite from `.archive/legacy-logo-suite-2026-10-23/` in live artifacts.
- Create a sub-brand logo for an offering without explicit brand-owner approval.
- Omit ™ from the first company-name mention in a standalone artifact.

### 4.4 Canonical logo variants and asset management
The Brand Guidelines list the following assets under `brand/logo/` (with runtime mirrors where configured): `logo-full`, `logo-light-bg`, `logo-dark-bg`, `logo-mark`, `logo-mark-mono`, `logo-avatar`, `logo-favicon`, and `logo-og`, generally in SVG and PNG. Transparent variants are also documented in the Brand Guidelines.

The guideline's variant table has a known ambiguity: the named usage rows for `logo-full` and `logo-light-bg` conflict with the pixel-verified wordmark-color notes. Inspect the asset itself and use the transparent-variant guidance when choosing a background. Do not infer background compatibility from a filename alone. `logo-mark-mono-transparent.png` is navy-filled and must not be used on a navy background. No white monochrome mark is currently specified; do not invent one.

Keep approved source assets in a version-controlled brand-assets location. If an asset is missing or ambiguous, request confirmation or inspect the canonical artwork; never substitute an internet image or recreate the logo.

---

## 5. Color system

The Brand Guidelines v1.0.1 are authoritative for the LightSpeed brand palette. The red color is unchanged and must remain `#E63946`. Do not replace it with another red, derive a new brand red, or alter the logo's own approved artwork colors.

### 5.1 Authoritative UI palette

| Token | Hex | Role |
| :--- | :--- | :--- |
| `navy` | `#070A40` | Headlines, logo text, primary brand surfaces, slide rails |
| `red` | `#E63946` | Signal waves, accent elements, calls to action, key highlights |
| `cyan` | `#00BFFF` | Shield base, accent elements, links on dark, taglines on navy |
| `grey-light` | `#F2F2F2` | Backgrounds, cards, callout boxes |
| `white` | `#FFFFFF` | Clean backgrounds, text on navy |
| `grey-dark` | `#6B7280` | Secondary text, captions |
| `grey-light-text` | `#9CA3AF` | Tertiary text on dark surfaces |

These seven colors are the approved general brand/UI palette. Do not add colors or replace these values without a documented brand decision approved by the Brand Strategist / CMO. The logo artwork has its own approved palette under ADR-027; that is a specific exception and does not authorize changing the UI tokens.

### 5.2 Color hierarchy and rules
- **Navy is dominant.** On brand-dominant surfaces, use roughly 60% navy / 20% red / 20% cyan as a composition guide.
- **Red and cyan are accents.** Use them deliberately rather than distributing them evenly across every component.
- On navy surfaces, use white text; on cyan surfaces, use navy text; on red surfaces, use white text, as specified by the Brand Guidelines.
- Do not use the palette's grey values as small text unless contrast is sufficient for the specific background. Accessibility requirements still apply.
- Do not rely on color alone to communicate status or meaning; pair color with text, shape, icon, or pattern.
- Do not add semantic colors, new neutrals, new gradient stops, or arbitrary chart colors without a documented brand decision.
- If a functional status requires a color not present in the approved palette, document the need and obtain approval rather than silently extending the palette.

### 5.3 Logo artwork palette exception
The logo artwork uses a distinct approved palette: navy `#02062F`, speed gradient `#01AFFD` to `#01DFFD`, and red range `#FD0231` to `#FD315D`, as recorded in ADR-027. These are logo-artwork colors only. Do not use them as replacements for the authoritative UI palette, and do not recolor the logo to match UI tokens.

### 5.4 Contrast and application
Use the approved colors with accessible pairings. Brand compliance does not override readability: verify text and UI contrast for each foreground/background pairing and adapt layout or use an approved contrasting variant where necessary. Avoid placing red or cyan body text on similarly saturated backgrounds. Use cyan for links on dark backgrounds as specified, and ensure links remain distinguishable beyond color alone.

### 5.5 Gradients
Use gradients only when they are part of approved logo artwork or have been explicitly approved as a brand treatment. Do not introduce general-purpose gradients with new colors or stops. Any new gradient treatment outside the official logo requires a documented brand decision.

---

## 6. Typography

Typography follows the Brand Guidelines v1.0.1. Use Arial for display, headings, body copy, captions, and secondary text. Do not substitute Inter or introduce a new display family as a default.

### 6.1 Typeface and weights
- **Display/headings:** Arial Bold (700).
- **Body:** Arial Regular (400).
- **Captions/secondary text:** Arial Regular (400), using grey-dark where contrast permits.
- **Web fallback:** Arial followed by a sans-serif fallback stack.

```css
font-family: Arial, Helvetica, sans-serif;
```

### 6.2 Type scale
Use the canonical type scale in `brand/tokens/brand-tokens.json`, with the human-readable overview in `brand/tokens.md`. The Brand Guidelines identify the range from `title-xl` (32 pt) through `caption` (12 pt). Do not invent headline sizes outside the canonical scale. Responsive implementations may scale within documented token behavior, but should not create competing type scales.

### 6.3 Editorial hierarchy
- Use weight, spacing, and scale to establish hierarchy.
- Use sentence case for most headings and UI labels.
- Use uppercase sparingly, except for the official tagline and short, intentionally styled labels.
- Keep body copy readable and line lengths controlled.
- Do not shrink critical text simply to fit a layout.
- Ensure exported documents and slides preserve legibility at presentation and print sizes.

The exact named size values should be read from the canonical `brand/tokens/brand-tokens.json`; this document does not invent missing token values.

---

## 7. Layout, grid, spacing, and density

### 7.1 Layout character
The layout should combine editorial whitespace with architectural precision. Use strong alignment, deliberate asymmetry, and layered composition to suggest systems thinking. Avoid arbitrary card grids where a clearer narrative sequence would work better.

### 7.2 Responsive grid
For web layouts, use the guideline's 12-column grid, 24 px gutter, 48 px margin, and 1200 px maximum content width as the canonical desktop baseline. Adapt responsively for smaller viewports without changing the underlying alignment logic. Keep reading measure comfortable and allow wide diagrams only when their content requires it.

Use consistent gutters and align major sections, page titles, and primary content edges.

### 7.3 Spacing scale
Use a 4 px base rhythm and the canonical scale: 4, 8, 12, 16, 24, 32, 48, 64, and 96 px. Do not introduce new spacing tokens without a recurring need and documented decision.

| Value | Typical use |
| :--- | :--- |
| **4 px** | Fine alignment and compact gaps |
| **8 px** | Related elements |
| **12 px** | Compact component spacing |
| **16 px** | Standard control or paragraph gap |
| **24 px** | Card padding and grouped content |
| **32 px** | Section subgroups |
| **48 px** | Major section spacing |
| **64 px** | Large section separation |
| **96 px** | Hero and major transition spacing |

Use fewer, consistent spacing values rather than one-off measurements.


---

## 12. Content design and voice

### 12.1 Voice
LightSpeed's voice is professional, confident, builder-oriented, direct, and evidence-led, with no hype. Public content should avoid emojis and generic AI commentary. Pharos thought leadership uses a builder-advocate voice: lead with proof, then principle. Explanations should remain practical and clear enough for the intended audience.

### 12.2 Writing principles
- Start with the audience's problem or intended outcome.
- Use active voice and specific verbs.
- Explain what a service does, who it helps, and what the engagement produces.
- Keep paragraphs focused.
- Use headings that communicate a point rather than generic labels.
- Distinguish facts, proposals, hypotheses, and aspirations.
- Explain acronyms on first use unless the audience clearly knows them.
- Use “AI” precisely; do not imply autonomy or capability that has not been implemented.
- Describe governance and human oversight where they are material to the offer.
- Prefer “use cases” to unsupported claims of proof or impact.

### 12.3 Avoid
- Avoid empty superlatives, inflated claims, excessive jargon, vague calls to action, and marketing language that could describe any technology consultancy.
- Avoid these terms in brand copy unless directly quoted or essential to a specific technical context: *Elevate*, *Leverage*, *Ecosystem*, *Deep dive*, *Game changer*.
- Do not use the phrase “Why it matters” as a default section heading.
- Do not use em dashes in published LightSpeed copy.
- Do not use emojis in formal or informational brand communication.

### 12.4 Calls to action
Each page should have one clear primary action and a small number of secondary actions.

**Preferred patterns:**
- Discuss an opportunity
- Explore the AI Company Builder
- Talk to LightSpeed
- Read the insight
- See how the approach works

Use the wording that matches the destination. Do not use a button that suggests a completed capability when the destination is only a concept or a contact form.

### 12.5 Claims and proof integrity
- Any metric, testimonial, client name, case study, partnership, credential, regulatory statement, or performance claim must be supported by an approved source.
- Use a canonical content/claims registry where the website uses one.
- Record the owner, source, date checked, permitted wording, and review date for sensitive claims.
- Do not invent metrics to make a design look complete.
- Use clearly marked placeholders during development.
- Remove unapproved placeholder content before release.
- Label conceptual diagrams as conceptual when they do not represent a deployed system.
- Never describe an intended future capability as a live feature.

---

## 13. Information architecture and page patterns

The system defines reusable page patterns but does not force every pattern into the current MVP.

### 13.1 General page structure
A typical public page may contain:
1. Global header and navigation
2. Clear page title and introductory statement
3. Primary content or service explanation
4. Relevant visual, diagram, or example
5. Evidence, method, deliverables, or practical detail where approved
6. Clear next action
7. Consistent footer and legal/contact information

Not every page needs every section. Use the shortest structure that fully answers the audience's question.

### 13.2 Hero pattern
A hero should establish, within a few seconds:
- What LightSpeed does or what this page is about
- Who it is for
- Why the topic is relevant
- What the visitor can do next

Use a strong headline, concise supporting copy, one primary action, and one relevant visual focal point. Do not crowd the hero with several competing CTAs, a large text wall, and multiple decorative objects.

### 13.3 Service and offering pattern
Describe an offering with:
- Audience or problem
- Approach
- What is included
- Expected deliverables or decision support
- Dependencies and limitations where material
- A relevant next step

Do not imply that every offering is a packaged, standardized product if the engagement is advisory or bespoke.

### 13.4 Insight and research pattern
Use a readable editorial layout with:
- Clear title and summary
- Author/organization and publication date when applicable
- Topic labels only where useful
- Strong hierarchy and comfortable reading width
- Charts and diagrams with source notes
- Citations and references where appropriate
- A clear distinction between evidence and opinion

### 13.5 MVP discipline
The current public website should prioritize a plausible, credible minimum viable experience that can launch. Future sections and advanced functionality can be introduced later.
- Do not add a page, navigation item, or interactive feature just because the design system defines a pattern for it.
- Do not let future architecture prevent the current site from shipping.
- Keep the navigation concise and aligned with the actual published content.
- Remove dead links, placeholder routes, and incomplete sections from the public journey.
- Make contact and engagement pathways work end-to-end.

---

## 14. Component system

Components should be designed around semantic purpose and predictable behavior. Each component must define default, hover, focus, active, disabled, loading, success, and error states where applicable.

### 14.1 Buttons
**Variants:**
- **Primary:** One dominant action per content region.
- **Secondary:** A lower-emphasis alternative.
- **Tertiary / text:** Lightweight action within content.
- **Destructive:** Irreversible or destructive action in internal products only when needed.

**Rules:**
- Use concise, verb-led labels.
- Keep button heights consistent within a context.
- Provide visible keyboard focus.
- Include loading and disabled states when actions can take time.
- Do not use multiple visually dominant primary buttons side by side without a strong reason.
- Ensure the whole visual button surface is clickable.

### 14.2 Links
- Links must be visually distinguishable from body text.
- Use descriptive link text, not “click here.”
- Provide hover and keyboard focus states.
- Do not rely on color alone to identify a link.
- Indicate external destinations when the context requires it.
- Avoid styling ordinary navigation links as buttons unless they are genuine calls to action.

### 14.3 Cards and panels
Use cards when grouping related information or actions. Do not put every paragraph into its own card.

A card should have:
- Clear heading
- Optional concise description
- Optional relevant icon or image
- Consistent padding and radius
- A clear interaction affordance if clickable

Avoid nesting multiple cards inside one another without a meaningful information hierarchy.

### 14.4 Forms
- Every input has a persistent, programmatically associated label.
- Placeholder text is an example or hint, not a replacement for a label.
- Explain required fields and validation rules.
- Validate near the relevant field and provide a helpful error message.
- Preserve entered values when validation fails.
- Confirm successful submission and explain the next step.
- Avoid requesting personal information that is not necessary for the task.

### 14.5 Navigation
- Keep global navigation concise.
- Clearly indicate the current page or section.
- Ensure keyboard access and logical focus order.
- Provide a mobile navigation pattern with a visible open/close state.
- Do not expose internal application routes through public navigation.
- Keep footer navigation useful without duplicating every top-level link.

### 14.6 Accordions and disclosure
Use disclosure patterns for secondary details, FAQs, or progressive explanation. Keep important information visible when hiding it would materially reduce understanding or trust.

### 14.7 Tables and data displays
- Use real table semantics for tabular data.
- Align numbers consistently.
- Include units and date ranges.
- Keep column labels clear.
- Provide a mobile strategy: responsive overflow, prioritization, or a meaningful alternate presentation.
- Distinguish zero, missing, unavailable, and not applicable values.
- Never use color alone to communicate a status.

### 14.8 Status badges
Use badges only for concise, meaningful states such as *Draft*, *In review*, *Published*, *Verified*, *Pilot*, or *Deprecated*. Avoid using badges as decoration or as a substitute for explanatory text.

### 14.9 Dialogs and overlays
- Use only when a focused interruption is justified.
- Provide a clear title and dismissal method.
- Keep keyboard focus within a modal while it is open and restore focus on close.
- Avoid dialogs for information that belongs inline.


---

## 16. Data visualization

Charts should make a decision or insight easier to see.

### 16.1 Chart selection
- **Bar chart:** compare categories.
- **Line chart:** show change over time.
- **Scatter plot:** explore relationships or distributions.
- **Stacked chart:** show composition only when comparison remains legible.
- **Table:** show exact values when precise lookup matters.
- **Diagram:** explain a process or relationship rather than numeric magnitude.

### 16.2 Chart rules
- Lead with the insight in the title where possible.
- Label axes, units, dates, and sources.
- Use a neutral base palette and one or two meaningful accents.
- Avoid 3D charts, unnecessary gradients, and decorative effects.
- Do not truncate axes in ways that exaggerate change without clear disclosure.
- Show uncertainty or sample limitations where relevant.
- Distinguish zero from missing data.
- Provide a text summary or table for important chart content when practical.
- Use direct labels when they reduce the need for a legend.
- Never invent data to complete a visual.

### 16.3 Trust and provenance
For charts used in research, policy, strategy, or public claims, record the source, retrieval date, transformation method, and relevant limitations. If data is estimated, modeled, or illustrative, label it clearly.

---

## 17. Accessibility and inclusive design

Accessibility is a release requirement, not a later enhancement.

### 17.1 Baseline
- Target WCAG 2.2 AA for public digital experiences where applicable.
- Text contrast: at least 4.5:1 for normal text and 3:1 for large text.
- Essential UI boundaries and graphical indicators: target at least 3:1 against adjacent colors.
- All interactive elements must be keyboard operable.
- Focus must be visible and not obscured.
- Provide semantic headings, landmarks, labels, and names.
- Provide alt text for informative images.
- Use captions or transcripts for meaningful audiovisual content.
- Support zoom and reflow without loss of content or function.
- Avoid relying on color, motion, sound, or position alone to communicate meaning.
- Make touch targets comfortably usable; aim for at least 44 × 44 CSS pixels where practical.
- Respect reduced-motion preferences.

### 17.2 Inclusive content
- Use plain language where possible.
- Avoid stereotypes and tokenistic imagery.
- Consider varied connectivity, device capability, and data costs.
- Optimize media and avoid unnecessary heavy effects.
- Ensure the experience remains useful on mobile devices and lower-bandwidth connections.
- Do not treat one regional or cultural visual shorthand as representative of all African audiences.

---

## 18. Light and dark themes

Both themes are first-class expressions of the same brand, not separate designs.

### 18.1 Light theme
- **Canvas:** `#F2F2F2` or `#FFFFFF`
- **Primary text and structural anchors:** Navy `#070A40`
- **Supporting text:** accessible slate tones
- **Accent:** Cyan and Red used selectively
- **Borders:** subtle neutral gray

### 18.2 Dark theme
- **Canvas:** Navy `#070A40`
- **Primary text:** white or near-white
- **Secondary text:** light neutral with adequate contrast
- **Surfaces:** progressively lighter dark tones, not a stack of identical black panels
- **Cyan and red:** adjust tonal variants if needed to preserve contrast

### 18.3 Theme behavior
- Use semantic tokens so components adapt automatically.
- Preserve the meaning of statuses across themes.
- Avoid hard-coded white or black in components unless they are part of a logo asset.
- Do not assume the user prefers a theme based solely on device type.
- Ensure images, diagrams, charts, borders, shadows, and focus rings are tested in both modes.

---

## 19. Responsive behavior and performance

Design for content priority, not merely for smaller screen widths.
- Start with the smallest usable layout and progressively enhance.
- Preserve the headline, core explanation, and primary action on mobile.
- Reflow multi-column layouts into a readable order.
- Avoid horizontal scrolling except for content where it is the appropriate interaction, such as wide data tables.
- Keep navigation and controls usable by touch.
- Use responsive image sizes and modern formats where supported.
- Lazy-load noncritical media.
- Reserve image dimensions to reduce layout shift.
- Avoid loading large animation or 3D libraries for effects that are not essential.
- Provide static fallbacks for advanced visuals.
- Monitor Core Web Vitals and real-device performance.
- Performance budgets should be set and tested per release. Do not claim a page is fast or optimized without measurement.

---

## 20. Brand applications

### 20.1 Public website
The website is the primary public expression of the brand. It should communicate what LightSpeed does, make the AI Venture Studio / AI Company Builder easy to understand, explain relevant capabilities, establish credibility through clear methods and approved evidence, and provide a working path to engagement.

The visual system should be coherent across the full site. Do not treat the hero as a one-off design experiment while leaving the rest of the site generic.

### 20.2 AI Venture Studio / AI Company Builder
The visual story should communicate disciplined movement from opportunity to venture:
1. Identify a real problem or opportunity
2. Shape a proposition and operating model
3. Design the AI-enabled workflow and governance
4. Build and test a usable solution
5. Launch, learn, and improve

Use stage diagrams, tangible deliverables, and clear human decision points. Do not suggest that a fully autonomous company can be created without human direction, governance, or ongoing operational responsibility.

### 20.3 Pharos Insights
Use an editorial, evidence-led style:
- Clear headlines and concise summaries
- Comfortable reading width
- Strong chart and citation standards
- Distinction between analysis, opinion, and verified fact
- Calm cover imagery and restrained brand accents
- Consistent metadata and publication patterns

### 20.4 Presentations and executive documents
- Use the prebuilt canonical templates where appropriate, including `static/brand/templates/pitch-deck.pptx`, `board-meeting.pptx`, the corresponding generators, and the approved one-pager and email templates.
- Default PowerPoint slide size is 10 × 7.5 inches (4:3), unless the brief explicitly requires 16:9.
- Content slides use the 0.15-inch navy rail on the left edge as specified by the canonical pitch-deck template.
- One primary message per slide or page.
- Use large, legible headings and concise body copy.
- Align elements to a grid.
- Prefer meaningful diagrams over dense paragraphs.
- Keep footnotes readable.
- Label assumptions, recommendations, decisions, risks, and open questions explicitly.
- Use a consistent title page, section divider, chart, and closing-slide system.
- Ensure the artifact remains understandable when printed or exported to PDF.

### 20.5 Social media and campaigns
- Preserve the logo clear space.
- Use one dominant message per asset.
- Keep text legible at feed size.
- Use the core palette and geometric/topographic motifs consistently.
- Ensure claims match the approved source copy.
- Do not use engagement bait or promise outcomes that cannot be substantiated.
- Maintain a consistent visual signature across formats, while respecting each platform's dimensions and cropping.

### 20.6 Research, policy, and institutional outputs
- Prioritize evidence, source transparency, and methodological clarity.
- Use restrained layouts and accessible charts.
- Identify the publication owner and date.
- Clearly distinguish findings, interpretation, recommendation, and uncertainty.
- Avoid promotional language that undermines analytical credibility.

### 20.7 Internal tools and agent-generated reports
Internal tools may be denser and more utilitarian than public pages, but should retain the same tokens, typography, interaction states, and information clarity.

AI-generated artifacts must follow this system and must not:
- Invent approval or status.
- Fabricate evidence or metrics.
- Expose confidential content in public-facing output.
- Introduce a new visual identity without authorization.
- Silently alter canonical brand tokens.

---

## 21. Design tokens and implementation guidance

### 21.1 Token principles
- Store tokens in a canonical, version-controlled location.
- Use semantic tokens in components.
- Keep raw values centralized.
- Document exceptions and their rationale.
- Ensure CSS, design files, and documentation agree.
- Avoid multiple competing “source of truth” files.
