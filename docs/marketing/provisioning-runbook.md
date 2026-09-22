# Provisioning Runbook — LIGHTSPEED HOLDINGS (hand-off kit for #194)

**Owner:** `social_media_manager` (registry `company-registry.yaml:928`), confirmed accountable owner 2026-09-22.
**Gate decisions (see [#194](https://github.com/jmlusu/light-speed-holdings/issues/194) comment 2026-09-22):** domain work **deferred** (platforms claim on `info.lightspeed@gmail.com`); password manager **Bitwarden**; owner = **`social_media_manager`**.
**Purpose:** everything the operator needs to execute Phase 0–4 of `docs/marketing/digital-identity-setup.md` — exact fill values, paste-ready bios, and the asset manifest. Complement (not replace) `docs/marketing/provisioning-kit.md`.
**Blocked by:** nothing for Phase 0/1 — platforms proceed on the Gmail identity. Resend sending-domain work stays parked pending a company domain (ties to #192).

---

## Phase 0 — Security (do first; ~20 min)

- [ ] Create Bitwarden org vault **"LIGHTSPEED HOLDINGS"** (or a dedicated free org).
- [ ] Create collection **"Social Media Accounts"**; add the operators who need access under the delegated-access model (§ Ownership model in `digital-identity-setup.md`).
- [ ] Secure `info.lightspeed@gmail.com`:
  - [ ] 2-Step Verification **on** (Authenticator app + backup codes saved to Bitwarden).
  - [ ] Recovery phone added.
  - [ ] Recovery email added.
  - [ ] Passkey registered.
- [ ] Generate a **strong unique password** for the Gmail account; store it in the Bitwarden vault. Never reuse it on a platform.
- [ ] As each platform is created below, enable its 2FA and seed the TOTP secret **only in Bitwarden** (never in the register or any spreadsheet).
- [ ] Confirm no credentials exist in `digital-asset-register.md` (they must not).

## Phase 1 — Claim the brand (work order & exact values)

Work order: **Facebook → Instagram → LinkedIn → X → TikTok → YouTube → Threads → Substack/resend**. For every platform claim the username everywhere, then update the register row to `Live` (+ URL + admins).

### Global fill values

| Field | Value |
|---|---|
| Company / brand name | LIGHTSPEED HOLDINGS LIMITED (brand: LIGHTSPEED) |
| Primary username | `@lightspeedholdings` (fallbacks `@lightspeedholdingsmw` → `@lightspeedhq`) |
| Email | `info.lightspeed@gmail.com` |
| Website | `https://lightspeedholdings.com` (parked lander today; refresh once domain live) |
| Tagline | ASPIRE. ACT. ACHIEVE. |
| Positioning | AI. Strategy. Transformation. |
| Logo | `static/brand/social/avatar-1024.png` (universal profile image) |

> Display-name note: use **LIGHTSPEED HOLDINGS** as the visible name everywhere. This corrects an older "LightSpeed Holdings" spelling in `docs/SOCIAL_MEDIA_UPLOAD_CHECKLIST.md` (identity rules forbid alternating spellings).

### 1. Facebook (company **Page**)

- Name: **Lightspeed Holdings Limited** · Category: Consulting / Information Technology / Business Service.
- Personal profile is only the administrator; the Page is owned by the company.
- Profile image: `avatar-1024.png` · Cover: branded cover — **AI. STRATEGY. TRANSFORMATION.** (gap: use `static/brand/social/templates/facebook-group-cover.png` or regenerate via `python static/brand/templates/generate-social-assets.py`).
- Bio: use the **Facebook variant** below; website `https://lightspeedholdings.com`.
- Register: set `Status: Live`, `URL: https://www.facebook.com/…`, admins.

### 2. Instagram (Professional/Business)

- Handle: `@lightspeedholdings` · Professional/Business account (link with the FB Page in Meta Business Suite, Phase 2).
- Profile image: `static/brand/social/instagram-profile.png` · Story frame: `instagram-story.png`.
- Bio: **Instagram variant** + link `https://lightspeedholdings.com` (link-in-bio).
- Register: set `Live` + URL + admins.

### 3. LinkedIn (Company Page; highest priority)

- Name: **LIGHTSPEED HOLDINGS LIMITED**.
- Logo: `linkedin-profile.png` (400×400) · Banner: `linkedin-banner.png` (1584×396).
- Tagline: **ASPIRE. ACT. ACHIEVE.**
- About: **LinkedIn variant** below.
- Admin: connect the founder profile as **Founder & CEO — LIGHTSPEED HOLDINGS LIMITED** (founder = admin, company owns the Page).
- Register: set `Live` + URL + "Founder as admin".

### 4. X (→ Professional Account → Business)

- Handle: `@lightspeedholdings` · Convert to **X Professional Account → Business**.
- Profile photo: `twitter-profile.png` (400×400, crop to circle) · Header: `twitter-header.png` (1500×500).
- Bio: **X variant**; website `https://lightspeedholdings.com`.
- Register: set `Live` + URL + admins.

### 5. TikTok (Business Account → TikTok Business Center)

- Handle: `@lightspeedholdings` · **Business Account**, two-step verification.
- Profile image: `tiktok-profile.png`.
- Bio: **TikTok variant**; link/website `https://lightspeedholdings.com` (bio link when available).
- Register: set `Live` + URL + admins.

### 6. YouTube (company channel)

- Channel name: **LIGHTSPEED HOLDINGS** · Handle `@lightspeedholdings` (long-form home for adapted shorts).
- Profile: `youtube-profile.png` (800×800) · Banner: `youtube-channel-art.png` (2560×1440, safe area 1546×423).
- About: **YouTube variant**; Google business ownership (Phase 2).
- Register: set `Live` + URL + admins.

### 7. Threads (reserve only)

- Handle: `@lightspeedholdings` (reserve now; activation/publishing not required yet). Tie to the IG account.
- Profile: `avatar-1024.png`.
- Register: keep `Status: Reserved` but confirm the handle is claimed; add URL when resolvable.

### 8. Substack + Resend (stand up now; delivery later)

- Substack: create publication **@lightspeedholdings** on `info.lightspeed@gmail.com`; set `email-newsletter-header.png` as the header; archive/land long-form before broadcast migration. Delivery stays on **Resend** (#192).
- Resend: account exists (`resend.com`, row in register). Sending domain **parked** until the company domain is settled — DKIM/SPF/DMARC records then land in #194.

## Bio variants (paste-ready, from the master description)

Master: *LIGHTSPEED HOLDINGS is an AI-native management and technology company helping organizations design, build and operate intelligent enterprises.*

| Platform | Bio |
|---|---|
| Facebook (about/intro) | LIGHTSPEED HOLDINGS is an AI-native management and technology company helping organizations design, build and operate intelligent enterprises across Africa. ASPIRE. ACT. ACHIEVE. AI. Strategy. Transformation. |
| Instagram (≤150) | AI, strategy & transformation company building intelligent enterprises and AI-powered solutions for Africa. ASPIRE. ACT. ACHIEVE. |
| X (≤160) | AI. Strategy. Transformation. We help organizations design, build and operate intelligent enterprises across Africa. ASPIRE. ACT. ACHIEVE. |
| LinkedIn (about) | LIGHTSPEED HOLDINGS LIMITED is an AI-native management and technology company helping organizations design, build and operate intelligent enterprises. We combine strategy and AI engineering so companies go from intention to operating AI-native systems — starting in Malawi and scaling across SADC and Africa. Specialties: AI strategy, agentic AI systems, intelligent-enterprise design and operation, management consulting. ASPIRE. ACT. ACHIEVE. |
| TikTok (conversational) | We're LIGHTSPEED HOLDINGS — an AI-native company building intelligent enterprises across Africa. 60 seconds of AI every day: explainers, behind-the-scenes builds, and real transformation playbooks. Follow to see how AI agents run a company. |
| YouTube (about) | LIGHTSPEED HOLDINGS is an AI-native management and technology company helping organizations design, build and operate intelligent enterprises. This channel is the long-form home for our AI education and transformation content — adapted shorts, deep dives, and the LIGHTSPEED AI LAB. |
| Threads | AI, strategy & transformation company building intelligent enterprises and AI-powered solutions across Africa. ASPIRE. ACT. ACHIEVE. |

## Phase 2 — Business infrastructure (after accounts exist)

- Meta Business Suite (FB + IG): Page, IG account, business ownership, permissions, people before any ads.
- TikTok Business Center: add admins, two-step verification.
- YouTube/Google: business-ownership verification on the channel.
- LinkedIn: confirm company administration (founder admin).
- X: Professional Account → Business category confirmed.
- No ads until ownership, permissions, and security are all set (platform guidance).

## Phase 3 — Branding (assets ready)

| Platform | Profile image | Cover / banner | Assets ready |
|---|---|---|---|
| Facebook | `avatar-1024.png` | `templates/facebook-group-cover.png` (or regenerate branded cover) | 1 |
| Instagram | `instagram-profile.png` | `instagram-story.png` (+ `templates/instagram-reels-cover.png`, `reels-shorts-cover.png`) | ✅ |
| LinkedIn | `linkedin-profile.png` | `linkedin-banner.png` (+ `templates/linkedin-carousel-*`) | ✅ |
| X | `twitter-profile.png` | `twitter-header.png` | ✅ |
| TikTok | `tiktok-profile.png` | — | ✅ |
| YouTube | `youtube-profile.png` | `youtube-channel-art.png` (+ `templates/youtube-thumbnail.png`, overlays) | ✅ |
| Threads | `avatar-1024.png` | `templates/thread-header.png` (optional) | ✅ |
| Newsletter | — | `templates/email-newsletter-header.png` | ✅ (for #317) |

All under `static/brand/social/`. Content-card templates for later posts: `templates/hook-card.png`, `quote-card.png`, `stat-card.png`, `chapter-marker.png`, `end-screen-cta.png`, `lower-third-video-overlay.png`.

## Warm-up re-baseline (Track 6)

Per the #194 decision, the 4-week warm-up window re-bases to start the day the register shows **all Tier 1–3 platforms `Live`**. `warmup-log.md` will be re-stamped then (its 2026-09-06 start predated provisioning; no daily tables carry data). After accounts ship, follow `provisioning-kit.md` Day-0 sequence and §3 gaps rule: never open a platform and leave it empty.

## Definition of done (this ticket)

Register shows Tier 1–3 platforms `Live` with public URLs, 2FA on, business ownership set, and admins recorded. Then #194 closes and unblocks **Warm-up (#313)** and **Newsletter kickoff (#317)**. Resend sending-domain verification remains a parked sub-item of #194 until the domain is settled.

## Related docs

- `docs/marketing/digital-identity-setup.md` (runbook + phases + master description)
- `docs/marketing/digital-asset-register.md` (single source of truth; update per platform)
- `docs/marketing/provisioning-kit.md` (Day-0 sequence, 15-post buffer, short-video plan)
- `docs/marketing/warmup-log.md` (protocol; re-baseline on Live)
- `docs/SOCIAL_MEDIA_UPLOAD_CHECKLIST.md` (per-platform upload steps)
- `static/brand/social/`, `brand/tokens/`, `brand/guidelines/` (brand assets)