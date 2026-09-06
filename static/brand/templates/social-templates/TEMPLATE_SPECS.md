# Social Media Template Specifications
**Source of Truth:** `brand/tokens/brand-tokens.json`
**Brand Guidelines:** `docs/superpowers/specs/2026-09-06-social-media-brand-guidelines-design.md`

---

## Brand Tokens (Copy-Paste Ready)

### Colors
```css
/* Primary */
--navy: #070A40;           /* Dominant: backgrounds, headlines, rails */
--red: #E63946;            /* Accent (10%): signal waves, CTAs, highlights */
--cyan: #00BFFF;           /* Accent (10%): shield base, links on dark */

/* Neutrals */
--white: #FFFFFF;          /* Clean backgrounds, text on navy */
--grey-light: #F2F2F2;     /* Card backgrounds, callouts */
--grey-dark: #6B7280;      /* Secondary text, captions */
--grey-light-text: #9CA3AF; /* Tertiary text on dark */

/* On-color text */
--on-navy: #FFFFFF;
--on-red: #FFFFFF;
--on-cyan: #070A40;
```

### Typography Scale
```css
--font-display: Arial, system-ui, sans-serif;  /* Weight: 700 */
--font-body: Arial, system-ui, sans-serif;     /* Weight: 400 */

--size-display-xl: 36pt;  /* Hero headlines */
--size-title-xl: 32pt;    /* Section titles */
--size-title-lg: 28pt;
--size-title-md: 24pt;
--size-title-sm: 18pt;
--size-subtitle: 16pt;
--size-body-lg: 16pt;
--size-body: 14pt;
--size-body-sm: 13pt;
--size-caption: 12pt;
```

### Spacing Scale (base unit: 4px)
`4, 8, 12, 16, 24, 32, 48, 64, 96`

### Logo Clear Space
`1x height of 'L' in LIGHTSPEED` on all sides

### Tagline
**ASPIRE. ACT. ACHIEVE.** — exact spelling, periods, caps, spacing

---

## Template 1: LinkedIn Carousel (5-Slide)
**Dimensions:** 1080 × 1080 px (1:1)
**Format:** PNG/PDF for LinkedIn native document upload

### Slide 1: Cover
- Background: Navy (`#070A40`)
- Left rail: 48px navy rail (brand standard)
- Title: `--size-title-xl` (32pt), White, `--font-display`
- Subtitle: `--size-subtitle` (16pt), Cyan (`#00BFFF`), `--font-body`
- Logo: Bottom-right, Icon Only variant, clear space respected
- Tagline: `--size-caption` (12pt), Grey-light-text, bottom-left

### Slides 2-4: Content
- Background: White
- Left rail: 48px Navy
- Headline: `--size-title-md` (24pt), Navy, `--font-display`
- Body: `--size-body` (14pt), Grey-dark, `--font-body`
- Visual: Diagram/stat/chart (centered, max 80% width)
- Red accent: Key numbers/metrics in Red (`#E63946`)

### Slide 5: CTA
- Background: Navy
- Left rail: 48px Navy
- Headline: "Ready to Build?" `--size-title-lg` (28pt), White
- Subtext: `--size-body` (14pt), Grey-light-text
- CTA Button: Red background, White text, `--size-body-sm` (13pt), radius 8px
- Website URL: Cyan, `--size-caption` (12pt)
- Logo + Tagline bottom

---

## Template 2: Video Thumbnail (YouTube)
**Dimensions:** 1280 × 720 px (16:9)
**Format:** PNG/JPG < 2MB

### Layout
- Background: Navy gradient (subtle)
- Left 40%: Navy rail area (brand standard)
- Title: `--size-title-xl` (32pt), White, `--font-display`, 2 lines max
- Episode badge: Red pill badge, `--size-caption` (12pt), "EP 01" format
- Play button: Red circle (64px), White play icon, center-right
- Logo: Bottom-right, Icon Only, clear space
- Tagline: Bottom-left, Grey-light-text, `--size-caption`

### Safe Zones
- YouTube overlays: bottom 90px, right 180px — keep critical content clear

---

## Template 3: Reels/Shorts Cover (Vertical)
**Dimensions:** 1080 × 1920 px (9:16)
**Format:** PNG

### Layout
- Background: Navy
- Top 15%: Hook text area — `--size-title-md` (24pt), White, centered
- Middle 60%: Visual/content preview (video frame or diagram)
- Bottom 25%: Safe zone for platform UI (caption, handle, sounds, likes)
  - Keep logo/title above 480px from bottom
- Logo: Top-right, Icon Only (32px min), clear space
- Red accent: Bottom progress bar indicator (3px)

### Platform UI Avoidance
- TikTok: Right side (profile, like, comment, share, bookmark)
- Instagram: Bottom (caption, audio, effects), Right side
- YouTube Shorts: Bottom (caption, subscribe), Right side

---

## Template 4: Quote Card
**Dimensions:** 1080 × 1080 px (1:1)
**Format:** PNG

### Layout
- Background: Navy
- Left rail: 48px Navy
- Quote mark: Large Cyan (`#00BFFF`), decorative, top-left of quote
- Quote text: `--size-body-lg` (16pt), White, `--font-body`, italic
- Author: `--size-body-sm` (13pt), Cyan, `--font-display`
- Role: `--size-caption` (12pt), Grey-light-text
- Logo: Bottom-right, Icon Only
- Tagline: Bottom-left, Grey-light-text

---

## Template 5: Stat Card
**Dimensions:** 1080 × 1080 px (1:1)
**Format:** PNG

### Layout
- Background: White
- Left rail: 48px Navy
- Metric number: `--size-display-xl` (36pt), Red (`#E63946`), `--font-display`
- Metric label: `--size-title-sm` (18pt), Navy, `--font-display`
- Context: `--size-body` (14pt), Grey-dark, 2 lines max
- Visual: Small chart/icon in Cyan (top-right area)
- Logo: Bottom-right, Full Logo Transparent
- Tagline: Bottom-left

---

## Template 6: Thread Header (X / LinkedIn)
**Dimensions:** 1200 × 675 px (16:9)
**Format:** PNG

### Layout
- Background: Navy
- Left rail: 48px Navy
- Thread indicator: Red vertical bar (4px) + "THREAD" in Red, `--size-caption`
- Title: `--size-title-xl` (32pt), White, `--font-display`
- Subtitle: `--size-subtitle` (16pt), Cyan
- Part indicator: "1/8" format, Grey-light-text, top-right
- Logo: Bottom-right, Icon Only

---

## Template 7: Lower-Third Video Overlay
**Dimensions:** 1920 × 360 px (16:9, bottom third)
**Format:** PNG with transparency (for video editing)

### Layout
- Background: Navy at 90% opacity
- Name: `--size-title-sm` (18pt), White, `--font-display`
- Title/Role: `--size-body` (14pt), Cyan, `--font-body`
- Red accent line: 4px height, full width, between name and title
- Logo: Right side, Icon Only (48px), clear space

---

## Template 8: Hook Card (First 3 Seconds)
**Dimensions:** 1080 × 1920 px (9:16)
**Format:** PNG

### Layout
- Background: Navy
- Large number/question: `--size-display-xl` (36pt), Red, `--font-display`, centered
- Hook text: `--size-title-lg` (28pt), White, `--font-display`, 2 lines max
- "Watch for..." teaser: `--size-body` (14pt), Grey-light-text
- Logo: Top-right, Icon Only
- Red accent: Animated pulse ring (motion spec: 1.5s ease-in-out)

---

## Template 9: End-Screen CTA
**Dimensions:** 1920 × 1080 px (16:9)
**Format:** PNG

### Layout
- Background: Navy
- Left rail: 48px Navy
- Headline: "Get the Framework" `--size-title-xl` (32pt), White
- Subtext: `--size-body` (16pt), Grey-light-text
- Email capture visual: Input field mockup (Grey-light bg, Navy border, Cyan focus)
- CTA Button: Red, White text, "Subscribe Free" `--size-body-lg` (16pt), radius 8px
- Arrow/pointer: Red, toward button
- Logo + Tagline: Bottom center

---

## Template 10: YouTube Chapter Marker
**Dimensions:** 1920 × 180 px (16:9, thin)
**Format:** PNG with transparency

### Layout
- Background: Navy at 95% opacity
- Chapter number: Red circle (32px), White number, `--size-caption`
- Chapter title: `--size-body` (14pt), White, `--font-display`
- Progress indicator: Cyan line (2px) filling left to right
- Timestamp: Grey-light-text, `--size-caption` (12pt), right-aligned

---

## Template 11: Facebook Group Cover
**Dimensions:** 1640 × 856 px (1.91:1)
**Format:** PNG/JPG

### Layout
- Background: Navy
- Centered content (Group name centered on desktop/mobile)
- Group name: "Agentic AI Malawi & SADC" `--size-title-xl` (32pt), White
- Tagline: "ASPIRE. ACT. ACHIEVE." `--size-subtitle` (16pt), Cyan
- Description line: `--size-body` (14pt), Grey-light-text
- Logo: Below name, Full Logo Transparent
- CTA: "Join the Conversation" Red button style, `--size-body-sm`

---

## Template 12: Email Newsletter Header
**Dimensions:** 600 × 200 px (3:1, email width)
**Format:** PNG

### Layout
- Background: Navy
- Left rail: 4px Navy (thin, email-safe)
- Logo: Left, Full Logo (120px wide min)
- Publication name: "The Agentic Builder" `--size-title-md` (24pt), White
- Issue: "Issue #01 • September 2026" `--size-caption` (12pt), Cyan
- Tagline: Right-aligned, Grey-light-text, `--size-caption`

---

## Quality Checklist (Every Template)

- [ ] Only brand palette colors used
- [ ] Logo from official assets, clear space respected
- [ ] Type sizes from token scale only
- [ ] Tagline spelled exactly "ASPIRE. ACT. ACHIEVE."
- [ ] No emojis, no off-brand elements
- [ ] Exported at correct dimensions
- [ ] File named: `platform-purpose-variant.png` (e.g., `linkedin-carousel-cover.png`)

---

## Motion Specifications (For Video Templates)

| Element | Animation | Duration | Easing |
|---------|-----------|----------|--------|
| Navy rail slide-in | Left to right | 0.3s | ease-out |
| Red accent pulse | Scale 1→1.05→1 | 1.5s | ease-in-out (loop) |
| Cyan line draw | Left to right | 0.5s | ease-out |
| Text fade-in | Opacity 0→1 | 0.3s | ease-out |
| Hook card number | Count-up | 1.0s | ease-out |

---

*Templates to be built in Canva/Figma using these specs. Source files saved in `static/brand/templates/social-templates/`.*
