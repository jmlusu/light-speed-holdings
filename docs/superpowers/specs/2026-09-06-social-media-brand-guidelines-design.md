# Social Media Brand Guidelines Design — Light Speed Holdings

**Date:** 2026-09-06
**Status:** Approved
**Owner:** CMO / Brand Strategist
**Applies to:** All public-facing social media content across TikTok, Instagram, LinkedIn, YouTube, X (Twitter), Facebook

---

## 1. Brand Voice & Tone (Social Media Adaptation)

| Element | Social Media Adaptation |
|---------|------------------------|
| **Core Voice** | Professional, evidence-led, no hype, no emojis |
| **Builder-Advocate Tone** | "We built this agent hierarchy. Here's the architecture. Here's the cost. Here's what broke." |
| **CEO Voice** | First-person insights, policy commentary, speaking highlights, behind-the-scenes |
| **Company Voice** | Case studies, technical artifacts, deployment proof, team spotlights |
| **Tagline Integration** | "ASPIRE. ACT. ACHIEVE." as closing sign-off or section headers |
| **Language** | English primary; Chichewa greetings/phrases for local authenticity (sparingly) |
| **Formatting** | No emojis. Clean line breaks. Numbered frameworks. Bold key metrics. |

**Voice Principles:**
- Lead with proof (code, metrics, deployments), then principle
- No generic AI commentary — every post ties to real engineering
- African context is native, not performative — use local terminology naturally
- Technical depth respected; jargon used precisely, not decoratively

---

## 2. Visual System for Social Media

### 2.1 Brand Tokens (Source of Truth: `brand/tokens/brand-tokens.json`)

| Token | Hex | Usage |
|-------|-----|-------|
| `navy` | `#070A40` | Dominant brand color — backgrounds, headlines, rails |
| `red` | `#E63946` | Accent — signal waves, CTAs, key highlights (~10%) |
| `cyan` | `#00BFFF` | Accent — shield base, links on dark, taglines on navy (~10%) |
| `grey-light` | `#F2F2F2` | Card backgrounds, callout boxes |
| `white` | `#FFFFFF` | Clean backgrounds, text on navy |
| `grey-dark` | `#6B7280` | Secondary text, captions |
| `grey-light-text` | `#9CA3AF` | Tertiary text on dark surfaces |

**Ratio Rule:** Approximately 80/10/10 navy/red/cyan on brand-dominant surfaces.

### 2.2 Platform-Specific Logo & Template Requirements

| Platform | Logo Variant | Color Application | Template Needs |
|----------|-------------|-------------------|----------------|
| **TikTok/Reels/Shorts** | Icon Only (32px min) | Navy background, Red/Cyan accent text overlays | Lower-third templates, hook cards, end-screen CTAs |
| **LinkedIn** | Full Logo Transparent | Navy rail left edge (per brand), White text on navy | Carousel templates (1080x1080), document covers |
| **X/Twitter** | Icon Only | Navy header, Cyan accent links | Thread header images, quote cards |
| **YouTube** | Full Logo | Navy channel art, Red play button accent | Thumbnail template (1280x720), chapter markers |
| **Facebook** | Full Logo | Navy cover, Cyan accent | Group cover, Reels overlay templates |

### 2.3 Static Assets Inventory

**Existing (in `static/brand/social/`):**
- Twitter profile/header, LinkedIn profile/banner, GitHub profile, Facebook cover, avatar

**To Create (Canva/Figma):**
- 12 social post templates: carousel (5-slide), quote card, stat card, video thumbnail (YouTube), thread header, Reels cover, Shorts end-screen, lower-third, hook card, CTA card, chapter marker, group cover
- Motion guidelines: 0.3s ease transitions, navy rail slide-in (left), red accent pulse on CTAs

### 2.4 Typography (Per Brand Tokens)

- **Display/Headings:** Arial 700 (fallback: system sans-serif stack on web)
- **Body:** Arial 400
- **Captions/Secondary:** Arial 400, `grey-dark` (`#6B7280`)
- **Scale:** Use type scale in `brand-tokens.json` (32pt → 12pt). No invented sizes.

---

## 3. Content Waterfall Workflow

### 3.1 Weekly Production Cadence

```
MONDAY          TUESDAY         WEDNESDAY       THURSDAY        FRIDAY
────────────────────────────────────────────────────────────────────────
CEO writes      Content team    Publish         Atomize to      Community
LinkedIn post   produces        pillar to       all platforms   engagement
(pillar)        video/asset     YouTube +       (waterfall)     (comments,
                                      Blog)                       replies)
```

### 3.2 Monthly Pillar Rotation (4-Week Cycle)

| Week | Pillar Theme | Primary Format | Atomized Outputs |
|------|--------------|----------------|------------------|
| 1 | Agent Architecture Deep-Dive | YouTube Tutorial (10-15 min) + Blog Post | 5 YouTube Shorts, 3 LinkedIn Carousels, 5 TikToks, 1 X Thread (6-10 tweets) |
| 2 | Malawi/SADC Deployment Case Study | LinkedIn Article + PDF One-Pager | 3 Instagram Reels, 2 TikToks, 1-Pager download, 1 Quora Answer |
| 3 | CEO Policy/Strategy Commentary | CEO LinkedIn Post + X Thread | 2 YouTube Shorts, 1 Instagram Reel, Newsletter Section |
| 4 | Technical Framework/Tooling | YouTube Tutorial + GitHub Repo Release | 4 YouTube Shorts, 2 LinkedIn Carousels, 1 Dev Community Post |

### 3.3 Waterfall Mapping (1 Pillar → 7+ Platforms)

| Source Asset | TikTok | Instagram | LinkedIn | YouTube | X | Facebook | Blog/SEO |
|--------------|--------|-----------|----------|---------|---|----------|----------|
| YouTube Video (10-15 min) | 3-5 clips (vertical) | 3-5 Reels (repurposed) | 1 Carousel (key frames) | ✅ Full + Shorts | Thread summary | 2 Reels | Embed + transcript |
| LinkedIn Article | Script → TikTok | Carousel → Reel | ✅ Native | Script → Short | Thread | Group prompt | Republish (canonical) |
| CEO LinkedIn Post | Clip → TikTok | Quote → Reel | ✅ Native | — | ✅ Native thread | Reshare | Newsletter |
| Case Study PDF | Stat cards | Carousel slides | ✅ Document | — | Thread stats | Group PDF | Download page |

---

## 4. Platform-Specific Rules

### TikTok
- **Do:** Keyword in voiceover + on-screen text + caption (3 signals); hook in first 1.5s; reply to every comment in 1st hour with video reply; 3-5 niche hashtags
- **Don't:** Over-edit; watermark from other platforms; post >5/day during warm-up
- **Warm-up:** 4 weeks manual, 1 post/day, consistent device/IP

### Instagram
- **Do:** Lead with Reels (only format with discovery); 3-5 niche hashtags; carousels for education (highest save rate); DM-share worthy content
- **Don't:** 30 hashtags (spam signal); TikTok watermark on Reels; link in bio only (no link stickers)
- **Reels:** <30s for reach; carousel for depth

### LinkedIn
- **Do:** Text-only posts with strong first line; native documents/carousels; comment 30 min/day on peer posts; post 7-9 AM local; external links in 1st comment only
- **Don't:** External links in post body (deprioritized); generic "great post" comments; >2 posts/day
- **CEO posts:** 3-5x reach of company page — prioritize CEO voice

### YouTube
- **Do:** Chapters matching sub-questions; corrected captions; thumbnails showing use case; embed on blog page with FAQs; title = core query
- **Don't:** Clickbait titles; missing transcripts; generic thumbnails
- **Shorts:** 4/week + 1 long-form/week

### X (Twitter)
- **Do:** Reply to large accounts in niche > own tweets; threads (6-10 tweets); curate feed aggressively (mute/block); 5 posts/day under 10K followers
- **Don't:** Link in post body; generic broadcasting; ignore replies

### Facebook
- **Do:** Reels only (skip static/link posts); Group participation for community; cross-post TikTok Reels (older audience converts)
- **Don't:** Page static posts (1.65% reach); Business Manager dependency for organic

---

## 5. CEO vs Company Account Protocols

### CEO Personal Accounts (Primary Driver)
| Account | Platform | Content | Cadence |
|---------|----------|---------|---------|
| CEO LinkedIn | LinkedIn | Thought leadership, policy, speaking, behind-scenes | 3-5x/week |
| CEO X | X | Real-time commentary, threads, engagement | 5-10x/day |
| CEO Instagram | Instagram | Visual behind-scenes, speaking clips | 2-3x/week |

### Company Accounts (Amplifier + Artifacts)
| Account | Platform | Content | Cadence |
|---------|----------|---------|---------|
| Light Speed Holdings | LinkedIn | Case studies, product updates, team spotlights | 2-3x/week |
| Light Speed Holdings | X | Announcements, reshares, technical threads | 3-5x/day |
| Light Speed Holdings | YouTube | Tutorials, deep-dives, interviews | 1 long + 4 Shorts/week |
| Light Speed Holdings | TikTok | Quick demos, tips, day-in-life | 3-5x/day |
| Light Speed Holdings | Instagram | Reels + carousels, visual brand | 1 img + 4 Reels/day |
| Light Speed Holdings | Facebook | Reels + Group management | 4 Reels/day |

### Cross-Posting Rules
- CEO posts → Company reshares with added context (not blind retweet)
- Company artifacts → CEO comments with personal insight
- Never duplicate identical content simultaneously — stagger by 4+ hours

---

## 6. Template Inventory

### Existing Templates (Ready to Use)
| Template | Path | Status |
|----------|------|--------|
| Social assets generator | `static/brand/templates/generate-social-assets.py` | ✅ Exists |
| Pitch deck | `static/brand/templates/pitch-deck.pptx` | ✅ Exists |
| One-pager | `static/brand/templates/one-pager.html` | ✅ Exists |
| Brand tokens CSS | `brand/tokens/brand-tokens.css` | ✅ Exists |
| Profile/cover images | `static/brand/social/*.png` | ✅ Exists (6 platforms) |

### Templates to Create (Phase 0)
| Template | Format | Priority |
|----------|--------|----------|
| LinkedIn carousel (5-slide) | Canva/Figma | P1 |
| Video thumbnail (1280x720) | Canva/Figma | P1 |
| Reels/Shorts cover (1080x1920) | Canva/Figma | P1 |
| Quote card (1080x1080) | Canva/Figma | P1 |
| Stat card (1080x1080) | Canva/Figma | P1 |
| Thread header (1200x675) | Canva/Figma | P1 |
| Lower-third (video overlay) | Canva/Figma | P2 |
| Hook card (first 3s) | Canva/Figma | P2 |
| End-screen CTA | Canva/Figma | P2 |
| Chapter marker | Canva/Figma | P2 |
| Facebook Group cover | Canva/Figma | P3 |
| Email newsletter header | Canva/Figma | P3 |

---

## 7. Compliance Checklist

Every social media artifact must pass:

- [ ] **Logo:** From official assets only (`static/brand/logos/`); never recreated
- [ ] **Clear Space:** 1× "L" height on all sides maintained
- [ ] **Colors:** Only palette colors used (navy/red/cyan/greys/white); no off-palette
- [ ] **Format:** Vector (SVG/PDF/EPS) for print; transparent PNG on dark backgrounds
- [ ] **Trademark:** `™` on first mention: "LightSpeed Holdings Limited™"
- [ ] **Type Scale:** Sizes from brand-tokens.json only (32pt → 12pt)
- [ ] **Tagline:** Spelled exactly "ASPIRE. ACT. ACHIEVE." (periods, caps, spacing)
- [ ] **Voice:** No emojis; evidence-led; builder-advocate tone
- [ ] **Attribution:** CEO posts attributed to CEO; company posts to Light Speed Holdings

---

## 8. Measurement Alignment

| Brand Consistency Signal | Feeds KPI | Measurement |
|--------------------------|-----------|-------------|
| Consistent entity (name, logo, bio) | AI Citation Rate | Manual audit: ChatGPT/Perplexity/Gemini |
| Cross-platform keyword consistency | Social SEO Rankings | Platform search impressions |
| Visual identity coherence | Brand Recall | Survey / aided awareness |
| CEO + Company dual-track | Branded Search Volume | Google Trends, GSC |
| Content waterfall completion | Content Velocity | Weekly production tracker |
| Template compliance rate | Brand Governance | Automated check (quarterly audit) |

---

## 9. Exceptions & Governance

- **CEO Dashboard:** Uses internal J.A.R.V.I.S. theme with "LS" placeholder — NOT public-facing brand. Do NOT rebrand.
- **Deviations:** Any exception requires documented brand decision approved by Brand Strategist / CMO.
- **Review Cycle:** Quarterly brand audit (Q1, Q2, Q3, Q4) — check 50 random posts across platforms for compliance.

---

## 10. Implementation Phases

| Phase | Timeline | Deliverables |
|-------|----------|--------------|
| **Phase 0: Foundation** | Weeks 1-2 | Templates created, accounts optimized, warm-up started |
| **Phase 1: Engine Launch** | Weeks 3-6 | First 3 pillars published, daily cadence established |
| **Phase 2: Growth** | Weeks 7-12 | Data-driven optimization, collaborations, newsletter |
| **Phase 3: Authority** | Weeks 13-24 | White papers, Knowledge Panel, speaking, academy |

---

*Design approved by user on 2026-09-06. Ready for implementation planning.*
