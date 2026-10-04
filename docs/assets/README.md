# Website Assets — Generation Tracker

**Spec:** `../website-imagery-spec.md`
**Brand:** `../../brand/tokens/brand-tokens.json`
**QA Gate:** All assets must pass `ls-artifact-qa` before deploy

---

## Asset Inventory

| # | Asset | Type | Dimensions | Production Skill | Status | QA |
|---|-------|------|------------|------------------|--------|----|
| 1 | `architecture.html` | Explorable HTML (archify) | 1200×800 responsive | `ls-diagramming` + `archify` | ⬜ Pending | ☐ |
| 2 | `grav-yaml-to-agents.png` | Grav illustration | 1920×1080 | `article-illustrations` | ⬜ Pending | ☐ |
| 3 | `grav-governance.png` | Grav illustration | 1920×1080 | `article-illustrations` | ⬜ Pending | ☐ |
| 4 | `campaign-hero-1200x600.png` | Campaign hero | 1200×600 | `ls-brand-advertising` | ⬜ Pending | ☐ |
| 5 | `campaign-linkedin-1200x627.png` | LinkedIn ad | 1200×627 | `ls-brand-advertising` | ⬜ Pending | ☐ |
| 6 | `campaign-instagram-1080x1080.png` | Instagram feed | 1080×1080 | `ls-brand-advertising` | ⬜ Pending | ☐ |
| 7 | `campaign-ig-story-1080x1920.png` | Instagram story | 1080×1920 | `ls-brand-advertising` | ⬜ Pending | ☐ |
| 8 | `campaign-facebook-1200x628.png` | Facebook feed | 1200×628 | `ls-brand-advertising` | ⬜ Pending | ☐ |
| 9 | `campaign-twitter-1600x900.png` | X/Twitter | 1600×900 | `ls-brand-advertising` | ⬜ Pending | ☐ |
| 10 | `campaign-gdn-300x250.png` | Google Display | 300×250 | `ls-brand-advertising` | ⬜ Pending | ☐ |
| 11 | `campaign-gdn-728x90.png` | Google Display | 728×90 | `ls-brand-advertising` | ⬜ Pending | ☐ |
| 12 | `campaign-gdn-336x280.png` | Google Display | 336×280 | `ls-brand-advertising` | ⬜ Pending | ☐ |
| 13 | `campaign-gdn-970x250.png` | Google Display | 970×250 | `ls-brand-advertising` | ⬜ Pending | ☐ |
| 14 | `campaign-billboard-1400x600.png` | Billboard | 1400×600 | `ls-brand-advertising` | ⬜ Pending | ☐ |
| 15 | `playground-fallback.png` | Terminal screenshot | 800×500 | `ls-frontend-design` | ⬜ Pending | ☐ |

**Total:** 15 assets

---

## React Components (Code, Not Assets)

| Component | File | Skill | Status |
|-----------|------|-------|--------|
| Hero | `src/components/Hero.tsx` | `ls-frontend-design` | ⬜ |
| FeatureGrid | `src/components/FeatureGrid.tsx` | `ls-frontend-design` | ⬜ |
| FeatureCard | `src/components/FeatureCard.tsx` | `ls-frontend-design` | ⬜ |
| KPIBand | `src/components/KPIBand.tsx` | `ls-frontend-design` | ⬜ |
| TrustStrip | `src/components/TrustStrip.tsx` | `ls-frontend-design` | ⬜ |
| CaseStudyCard | `src/components/CaseStudyCard.tsx` | `ls-frontend-design` | ⬜ |
| LeadershipStrip | `src/components/LeadershipStrip.tsx` | `ls-frontend-design` | ⬜ |
| LeaderCard | `src/components/LeaderCard.tsx` | `ls-frontend-design` | ⬜ |
| Playground | `src/components/Playground.tsx` | `ls-frontend-design` | ⬜ |
| TerminalSimulator | `src/components/TerminalSimulator.tsx` | `ls-frontend-design` | ⬜ |

**Pages:**
- `src/pages/Index.tsx` — Homepage assembly
- `src/pages/Architecture.tsx` — Architecture embed
- `src/pages/Build.tsx` — Offer A landing
- `src/pages/OfferB.tsx` — Offer B landing
- `src/pages/OfferC.tsx` — Offer C landing
- `src/pages/OfferE.tsx` — Offer E landing

---

## Generation Commands

### Architecture Diagram
```bash
# From repo root
cd docs/assets
# Use archify skill or mermaid-cli
npx -y @mermaid-js/mermaid-cli -i architecture.mmd -o architecture.svg
# Then wrap in HTML with archify template for dark/light toggle
```

### Grav Illustrations
```bash
# Invoke article-illustrations skill with prompts from spec
# Skill will use generate_image tool
# Post-render palette check REQUIRED:
uv run python .agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py grav-yaml-to-agents.png --tolerance 3
uv run python .agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py grav-governance.png --tolerance 3
```

### Campaign Assets
```bash
# For each platform, dispatch to media-generation-owner via task
# Use generation brief template from spec with per-platform dimensions
# QA each with ls-artifact-qa
```

### React Components
```bash
# Implement in src/components/
# Use brand tokens: @import '../../brand/tokens/brand-tokens.css';
# Import logos from '../../brand/logos/fulllogo/fulllogo.png' (canonical)
# Build & test:
bun run build
bun run lint
# Visual QA:
npx playwright install chromium
node .agents/skills/ls-artifact-qa/scripts/visual_check.js
```

---

## QA Checklist Per Asset

### All Assets
- [ ] Palette: only `#070A40`, `#E63946`, `#00BFFF`, `#F2F2F2`, `#FFFFFF`, `#6B7280`, `#9CA3AF`
- [ ] Logo: official asset from `brand/logos/`, clear space = 1× "L" height
- [ ] Typography: Arial 700/400 only, sizes from brand scale
- [ ] Spacing: 4px base grid (4/8/12/16/24/32/48/64/96)
- [ ] Contrast: ≥ 4.5:1 for all text

### Grav Illustrations (Additional)
- [ ] Grav floating (visible gap under feet)
- [ ] Grav performs core action (not decoration)
- [ ] Original metaphor (not reused)
- [ ] Accent colors: Orange flow only, Red warnings only, Blue system state only
- [ ] Max 8 labels, 2–5 words each
- [ ] ≥35% whitespace
- [ ] Palette checker PASS (post-render remap if needed)

### Campaign Assets (Additional)
- [ ] Dimension-exact per platform table
- [ ] Text in safe zones (≥15% inset)
- [ ] Persuasion arc complete (6 beats)
- [ ] Proof is traceable fact
- [ ] Red reserved for CTA only

### React Components (Additional)
- [ ] Responsive: stacks at <768px, no horizontal scroll
- [ ] Accessible: semantic HTML, focus states, alt text, landmarks
- [ ] Tap targets ≥44px
- [ ] Reduced motion respected
- [ ] Keyboard navigable

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Creative Director | | | |
| Brand Owner (CMO) | | | |
| Frontend Lead | | | |
| QA Lead | | | |

---

**Next Action:** Creative Director briefs production skills per spec
