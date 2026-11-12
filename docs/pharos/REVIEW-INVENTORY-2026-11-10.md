# Pharos Review Inventory — Outstanding Content (as of 2026-11-10)

**Compiled:** Tue Nov 10 2026
**Purpose:** Single source of all outstanding Pharos thought-leadership and Lightspeed social media artifacts requiring review, approval, or production.

---

## 1. LinkedIn Series: "AI-Native Organizations" (11 posts)

**Plan location:** `docs/pharos/ai-native-orgs-linkedin-series-plan.md` — status **PLAN MODE — not executed**
**CEO gate record:** `docs/pharos/linkedin-series/CEO-review-batch-1.md` — Posts 1–3 approved 2026-09-28
**Launch schedule:** Mon/Wed/Fri starting 2026-10-05, every 2 days over ~4 weeks
**Blocker:** Platform provisioning issue #194 (LinkedIn/X/TikTok/YouTube/Substack all "Pending #194")

| # | Title | Draft status | Atomized assets | Visuals | CEO review | QA verdict |
|---|-------|-------------|-----------------|---------|------------|------------|
| 1 | What is an AI-Native Organization? | ✅ draft-v1 + feed-v1 | ✅ x-thread, carousel, substack, video | ✅ hero + 3 cards | ✅ Approved 2026-09-28 | APPROVE |
| 2 | What does 90 AI agents actually mean? | ✅ | ✅ | ✅ hero + 3 cards | ✅ Approved 2026-09-28 | APPROVE |
| 3 | LightSpeed AI-native org structure | ✅ | ✅ | ✅ hero + 3 cards | ✅ Approved 2026-09-28 | APPROVE |
| 4 | What the H-A-O-M-T-G-V Framework Actually Means | ✅ | ✅ | ❌ none | ⏳ **Batch 2 pending** | STYLE PASS (copy) |
| 5 | AI Agents for Malawian SMEs | ✅ | ✅ | ❌ none | ⏳ **Batch 2 pending** | STYLE PASS (copy) |
| 6 | Agentic AI in Health & M&E | ✅ | ✅ | ❌ none | ⏳ **Batch 2 pending** | STYLE PASS (copy) |
| 7 | Agentic AI & Financial Inclusion | ✅ | ✅ | ❌ none | ⏳ **Batch 2 pending** | STYLE PASS (copy) |
| 8 | AI Governance in Malawi | ✅ | ✅ | ❌ none | ⏳ **Batch 2 pending** | APPROVE (copy), render pending |
| 9 | Measuring AI-native Organizations | ✅ | ✅ | ❌ none | ⏳ **Batch 2 pending** | APPROVE (copy), render pending |
| 10 | What Should an AI Agent Decide? | ✅ | ✅ | ❌ none | ⏳ **Batch 2 pending** | APPROVE (copy), render pending |
| 11 | Lessons From Building LightSpeed | ✅ | ✅ | ❌ none | ⏳ **Batch 2 pending** | APPROVE (copy), render pending |

### Series-level gaps:
- **Posts 4–11 have no CEO approval record** — every QA report flags "CEO review batch-2 pending (Posts 4–11 submitted together; only Posts 1–3 approved via CEO-review-batch-1.md 2026-09-28)."
- **Posts 4–11 have zero rendered visuals** — only Posts 1–3 have `visuals/` PNGs in `docs/pharos/linkedin-series/post-N/visuals/`.
- **Nothing has published.** Launch was blocked by #194.
- Reminder script: `templates/pharos/routines/linkedin-series-reminder.md`.
- Visual generation script: `static/brand/templates/generate-linkedin-series-visuals.py`.

---

## 2. Other Pharos Thought-Leadership in Pipeline

### Anchor documents awaiting Human CEO review/approval:

| Artifact | Path | Status |
|----------|------|--------|
| Manifesto — *What Agentic AI Company-Building Actually Means for Malawi & SADC* | `docs/pharos/manifesto-draft.md` | **Draft — awaiting Human CEO review** |
| Article — H-A-O-M-T-G-V seven layers | `docs/pharos/articles/h-a-o-m-t-g-v-seven-layers.md` | **Draft for CEO review** |
| Whitepaper — *Agentic AI in Resource-Constrained Environments* | `docs/pharos/whitepaper/resource-constrained-deployment-playbook.md` | ✅ **Approved by Human CEO 2026-10-13**; ready for publication (needs rendering path — plan gate B4) |
| Whitepaper chapter — H-A-O-M-T-G-V | `docs/pharos/whitepaper/h-a-o-m-t-g-v-chapter.md` | **Draft for review** (policy/regulator-facing) |
| Pillar 01 — Built a 90-Agent Company | `docs/pharos/pillars/01-built-a-90-agent-company.md` | **Draft — awaiting CEO approval** |
| Pillar 02 — 5-Tier Human-in-the-Loop | `docs/pharos/pillars/02-5-tier-human-in-the-loop.md` | **Draft — awaiting CEO approval** |
| Pillar 03 — The Four Reservations | `docs/pharos/pillars/03-agentic-ai-resource-constrained-africa.md` | **Draft — awaiting CEO approval** |
| Policy — National AI Strategy comments | `docs/pharos/policy-drafts/national-ai-strategy-comments.md` | **DRAFT** for validation against live consultation format before filing |
| Policy — SADC Agentic AI Governance Framework | `docs/pharos/policy-drafts/sadc-agentic-ai-governance-framework.md` | Authored policy proposal (explicitly "not adopted and not verified as submitted") |

### Research briefs (3):
- `docs/pharos/research-briefs/2026-10-12-africa-open-source-ecosystem.md`
- `docs/pharos/research-briefs/2026-10-12-ai-economics-sadc.md`
- `docs/pharos/research-briefs/2026-10-12-open-source-costs.md`

### LinkedIn intro post:
- `docs/pharos/linkedin-intro-post.md` — **Ready — awaiting account + CEO approval** (blocked #194)

### Distribution & publishing infrastructure:
- Distribution package: `docs/pharos/distribution-package-2026-10-12.md` — 6 article post drafts, ready, tied to site article slate
- Publishing plan: `docs/pharos/publishing-plan-2026-10-12.md` — ready for review; gates B1–B10 open
- Site articles: 6 new + 3 legacy (`sadc-ai-opportunity`, `agentic-ai-african-governments`, `digital-to-ai-native-transformation`) in `src/data/insights.ts`
- Case-study pipeline: `docs/pharos/case-study-pipeline.md` — J&S StopOver Bar = priority, **not yet documented**; health/M&E, VSLA/SACCO, meta-case all undeveloped

### QA verdicts on 3 HTML visuals (2026-10-12):
| Artifact | Verdict |
|----------|---------|
| `public/infographics/inside-the-90-agent-company.html` | APPROVE (one off-palette `#0077A8` noted, not blocking) |
| `public/infographics/open-source-stack.html` | FIX → re-render (mobile horizontal overflow 394 px at 375×667) |
| `public/visuals/graduated-autonomy-ladder.html` | APPROVE |

---

## 3. Social Media Artifacts — LightSpeed Holdings

### Platform account assets — `static/brand/social/` (37 files):
- Profile/banner images: LinkedIn, X, Facebook, Instagram, TikTok, YouTube, Threads, GitHub, avatar, business card, letterhead
- Post templates: 17 P1 PNGs in `static/brand/social/templates/` covering LinkedIn carousel, quote card, stat card, hook card, thread header, Reels/Shorts cover, YouTube thumbnail, end-screen CTA, etc.

### Full campaign artifact set — `artifacts/campaigns/2026-10-26-pipeline-test/`:
- `dossier.md` + text variants (`linkedin-primary.md`, `variant-policy.md`, `variant-enterprise.md`)
- `social-copy/threads-and-captions.md`
- `carousels/` — social-carousel.pdf + 6 Instagram cards
- `infographics/` — 3 sizes (1080×1080, 1600×900, 1200×628)
- Videos — 16×9 overview + 1080×1920 short
- `notebooklm/` — source pack + 6 studio prompts
- `open-design/` — executive briefing HTML + branded PDF, carousel PDF + 5 cards
- `reports/comprehensive-report-branded.pdf`

### Platform first-post copy — `docs/marketing/atomized/`:
- `linkedin-first-post.md`, `x-first-post.md`, `facebook-first-post.md`, `instagram-first-post.md`, `tiktok-first-post.md`, `youtube-first-short.md`, `substack-first.md`, `threads-first-post.md`
- 3 pillar social packs (`01/02/03-pillar--social-pack.md`) — **Draft, awaiting CEO approval; post only after #194**

### Warm-up content — `docs/marketing/warmup-content-pack/`:
- FB/IG/LI/TikTok/X/YouTube posts + `week2-runbook.md`

### Newsletter — `docs/marketing/newsletter/`:
- `monitor-01.md` (Issue #1 content + HTML layout ready — **send flow blocked** by #192/#194)
- `monitor-plan.md`

### Account status — `docs/marketing/digital-asset-register.md`:
| Platform | Status |
|----------|--------|
| Website | Pending |
| LinkedIn | **Pending (#194)** |
| Facebook | Live (2026-10-03) |
| Instagram | Live (2026-10-03) |
| X | **Pending (#194)** |
| TikTok | **Pending (#194)** |
| YouTube | **Pending (#194)** |
| Threads | Live (2026-10-03) |
| Substack | **Pending (#194)** |
| Resend | Blocked (#192/#194) |

---

## 4. Blockers Summary

| Blocker | ID | Impact |
|---------|-----|--------|
| **Platform provisioning** | #194 | All social accounts (LinkedIn/X/TikTok/YouTube/Substack) stuck in "Pending" — zero can publish |
| **Email send decision** | #192/#194 | Newsletter send flow blocked; `Resend` account pending domain settlement |
| **CEO review batch 2 (Posts 4–11)** | — | 8 of 11 series posts unapproved; zero visual production for Posts 4–11 |
| **Visual production Posts 4–11** | — | No hero/carousel PNGs exist for any post beyond #3 |
| **CEO reviews — anchor documents** | — | 6 documents awaiting sign-off: manifesto, 3 pillars, H-A-O-M-T-G-V article, National AI Strategy comments |
| **Whitepaper rendering path (B4)** | — | Approved 2026-10-13 but no public route or PDF render; gate B4 open |
| **`open-source-stack.html` mobile overflow** | — | QA FIX → re-render (394px overflow at 375×667); non-blocking for desktop but blocks mobile ship |

---

## 5. Prioritized Next Steps (recommended)

### Immediate (Week of Nov 10):
1. **Resolve #194** — provision LinkedIn Company, X Professional, TikTok Business, YouTube Company, Substack publication accounts. Without this, zero social content can go live.
2. **CEO review batch 2** — compile and submit Posts 4–11 drafts for CEO approval (single PR or shared doc). All 8 drafts exist with copy QA passed; only visual production and formal approval remain.
3. **Visual production for Posts 4–11** — generate hero PNGs + 3 carousel cards per post using `ls-visual-storytelling` + `ls-artifact-qa` gate.

### Short-term:
4. **Whitepaper rendering** — decide route vs. PDF (gate B4); the paper is approved and ready.
5. **Manifesto + 3 pillars CEO review** — fastest path to unlocking the foundation content.
6. **National AI Strategy comments validation** — validate draft against live consultation format, then file or mark ready.
7. **`open-source-stack.html` re-render** — apply the 3 CSS fixes for mobile overflow; re-run QA.

### Medium-term:
8. **Build remaining social post templates** (P2/P3 from social-media-positioning-status.md).
9. **Extend `generate-social-assets.py`** for Instagram, TikTok, YouTube profile/banner assets.
10. **AI citation baseline** — run 20-keyword audit across ChatGPT, Perplexity, Gemini.

---

**Next action:** What would you like to tackle first? I can:
- Write the CEO batch-2 review package (Posts 4–11 drafts + QA reports)
- Start the #194 provisioning runbook
- Begin visual production for Posts 4–11
- Begin CEO reviews of the 6 anchor documents
- Re-render `open-source-stack.html` to fix the mobile overflow

Or let me know your preference.
