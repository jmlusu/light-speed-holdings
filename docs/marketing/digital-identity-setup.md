# Digital Identity Setup — LIGHTSPEED HOLDINGS

**Owner:** `social_media_manager` (registry `company-registry.yaml:928`). **Conflict:** [#189](https://github.com/jmlusu/light-speed-holdings/issues/189) decided "no new social-media-manager subagent", yet this agent is present in the working tree only (uncommitted). Ownership unresolved — see ticket.
**Phase:** 0 (Security) → 1 (Claim brand) → 2 (Business infrastructure) → 3 (Branding) → 4 (Content)
**Status:** Active — Phase 0 in progress; account provisioning blocked by [#194](https://github.com/jmlusu/light-speed-holdings/issues/194), cleared by completing the phases below. **Domain control unresolved:** `lightspeedholdings.com` resolves to Afternic marketplace nameservers (for-sale lander, null MX) — confirm ownership before any sending-domain work.
**Source:** Normalized from `social-media/LIGHTSPEED-SOCIAL-MEDIA-SETUP.md` (folder retired 2026-09-17)

This runbook treats the social presence as a single company **digital-identity build**, not a collection of accounts. The rule that matters most: **LIGHTSPEED HOLDINGS LIMITED owns every account**; individuals (and later employees, agencies, and AI agents) receive only delegated access.

## When to use

- **First-time provisioning:** work through Phases 0–4 in order; after each platform is created, update the Digital Asset Register (`docs/marketing/digital-asset-register.md`).
- **Ongoing maintenance:** keep the register current; re-run Phase 2/3 checks whenever an account changes or a new platform is added.

## Digital identity tree

```text
                         LIGHTSPEED HOLDINGS LIMITED
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
               MAIN WEBSITE                EMAIL SYSTEM
                    │                           │
          lightspeedholdings...             info@...
                    │
        ┌───────────┼───────────┬───────────┬───────────┐
        │           │           │           │           │
      LinkedIn    Facebook       X       Instagram    TikTok
        │           │           │           │           │
        └───────────┴───────────┴───────────┴───────────┘
                              │
                       CONTENT ENGINE
                              │
              AI / Strategy / Management / Products
```

## Identity rules

### Company name

Use **LIGHTSPEED HOLDINGS LIMITED** wherever legal/company identity is shown. **LIGHTSPEED** is the brand. Do not alternate spellings (no LightSpeed Holdings, Lightspeed Holding, Light Speed Holdings, LIGHTSPEED AI, or Lightspeed Technologies).

Preferred platform names:

| Platform  | Preferred name               |
|-----------|------------------------------|
| Facebook  | Lightspeed Holdings Limited  |
| Instagram | `@lightspeedholdings`        |
| X         | `@lightspeedholdings`        |
| TikTok    | `@lightspeedholdings`        |
| LinkedIn  | LightSpeed Holdings Limited  |
| YouTube   | LightSpeed Holdings          |
| Threads   | `@lightspeedholdings`        |

### Primary username

Claim **`@lightspeedholdings`** everywhere. Fallbacks in order: **`@lightspeedholdingsmw`**, **`@lightspeedhq`**. No number suffixes (e.g. `lightspeedholdings2026`).

**Claim the username everywhere, even if you do not intend to actively post there yet.**

### Email identity

Start with `info.lightspeed@gmail.com` — do not block provisioning on a company domain. Migrate toward `info@lightspeedholdings.com` (plus `hello@`, `contact@`, `admin@`) once the domain exists; `social@`/`digital@` can become the account-management identity. Migrate the account/recovery email later where platforms permit.

## Ownership model

The company owns the accounts; nobody's personal account is the root.

```text
LIGHTSPEED HOLDINGS LIMITED
        │
        ├── Corporate email
        │
        ├── Business accounts
        │
        └── Jack / employees / agencies / agents
                 ↓
            delegated access
```

This matters as soon as there are employees, marketing staff, AI agents, agencies, developers, or investors. Do not let the entire digital identity depend on one personal account.

## Phase 0 — Security (do first)

1. Secure `info.lightspeed@gmail.com`: enable 2-Step Verification, add a recovery phone and recovery email, enable authenticator/passkey.
2. Create a strong unique password for the account.
3. Use a password manager; never reuse the Gmail password on any social platform.
4. Record platform credentials only in the password manager — **never** in the Digital Asset Register or any ordinary spreadsheet.

## Digital Asset Register

The living record of every platform, owner, and 2FA state lives in `docs/marketing/digital-asset-register.md`. It is owned by `social_media_manager` and is the single source of truth for provisioning status. Passwords are stored in the password manager only.

## Account tiers

| Tier | Platforms | Role |
|------|-----------|------|
| 1 — Core | LinkedIn, Facebook, Instagram, X | Primary presence |
| 2 — Growth / media | YouTube, TikTok | Long-form + short-video distribution |
| 3 — Reserve / distribution | Threads | Claim now, activate later |

### Platform guidance

- **Facebook:** company **Page** for LIGHTSPEED HOLDINGS LIMITED (category ≈ Consulting / Information Technology / Business Service); personal profile is only the administrator. Logo as profile picture; branded cover (e.g. **AI. STRATEGY. TRANSFORMATION.** / Building intelligent enterprises for Africa).
- **Instagram:** Professional/Business account, same logo, bio derived from the master description.
- **Meta Business Suite:** once Facebook + Instagram exist, establish Meta infrastructure (Page, Instagram, Ad Account, Pixel/tracking, people/permissions) before advertising. No ads until ownership, permissions, and security are set.
- **X / Twitter:** `@lightspeedholdings`, convert to **X Professional Account → Business**. X is the company's real-time AI/technology thought-leadership channel.
- **TikTok:** `@lightspeedholdings` as a **Business Account**, then **TikTok Business Center** (multiple admins + two-step verification per TikTok guidance). "60 seconds of AI" content format fits the positioning.
- **LinkedIn:** create the **Company Page** (LIGHTSPEED HOLDINGS LIMITED). Connect the founder profile as **Founder & CEO — LIGHTSPEED HOLDINGS LIMITED** to build a founder + company ecosystem. Prioritize this platform heavily.
- **YouTube:** create the company channel **now** as LIGHTSPEED HOLDINGS, `@lightspeedholdings`. Long-form home (LIGHTSPEED AI LAB) from which TikTok/Instagram/LinkedIn content is adapted.
- **Threads:** reserve `@lightspeedholdings` now; publishing is not required immediately.

## Single brand identity

Every account uses the same:

- **Name:** LIGHTSPEED HOLDINGS LIMITED
- **Logo:** the same official logo (see `brand/tokens/`, `static/brand/social/`)
- **Tagline:** **ASPIRE. ACT. ACHIEVE.**
- **Core positioning:** **AI. Strategy. Transformation.** — e.g. *LIGHTSPEED HOLDINGS is an AI-native management and technology company helping organizations design, build and operate intelligent enterprises.*

## Master company description

One master description; derive platform variants. Do not write ten different bios.

| Platform   | Variant style                  |
|------------|--------------------------------|
| 160 chars  | AI, strategy & transformation company building intelligent enterprises and AI-powered solutions for Africa. |
| LinkedIn   | Longer description             |
| X          | Short, punchy version          |
| Instagram  | Short marketing version        |
| TikTok     | More conversational            |
| YouTube    | Longer company description     |

## Visual asset package

Prepare the LIGHTSPEED SOCIAL MEDIA KIT before posting: primary/white/dark logo + icon, profile images, cover images (Facebook/X/LinkedIn/YouTube), Instagram/LinkedIn/TikTok templates, video intro, brand fonts/colors. Reuse the existing Lightspeed brand system (`brand/guidelines/`, `static/brand/social/`) — do not create a second visual identity.

## First content batch

Do not open accounts and leave them empty. Have **10–15 pieces ready first**, e.g.:

1. Introducing LIGHTSPEED HOLDINGS (who we are)
2. Why AI-native companies are different (thought leadership)
3. What is Agentic AI? (educational)
4. AI transformation in Africa (thought leadership)
5. 5 business processes AI agents can automate (educational)
6. Meet the Lightspeed AI ecosystem (company/product)
7. AI + management consulting (service model)
8. Building for Malawi → SADC → Africa (geographic positioning)
9. AI tools we're experimenting with (behind-the-scenes)
10. What we're building at Lightspeed (founder/company vision)

## Content engine

Social media is the **distribution layer** for Lightspeed IP — not an ad channel. One idea → master content → platform adaptations:

```text
                ONE LIGHTSPEED IDEA
                        │
                        ↓
                MASTER CONTENT
                        │
       ┌────────────────┼────────────────┐
       ↓                ↓                ↓
    LinkedIn            X              YouTube
       │                │                │
       ↓                ↓                ↓
  carousel/text      short post       long video
       │
       └───────────────┬────────────────┘
                       ↓
                  Instagram
                       │
                       ↓
                    TikTok
```

Source the idea pipeline from the Pharos pipeline (`pharos-thought-leadership-*`), the monthly content calendar (`docs/marketing/content-calendar-90day.md`), and the warm-up content pack (`docs/marketing/warmup-content-pack/`); run publishing cadence per `docs/marketing/daily-cadence-checklist.md`.

## Reserve list (brand protection)

Secure before the brand gains visibility: `lightspeedholdings`, `lightspeedholdingsmw`, `lightspeedhq`, `lightspeedai`, `lightspeedafrica`. Not all need to be used; the purpose is protection.

## Phase plan

| Phase | Scope | Items |
|-------|-------|-------|
| 0 — Security | Gmail + 2FA | secure `info.lightspeed@gmail.com`, 2FA, unique password, password manager |
| 1 — Claim the brand | Create/claim accounts | Facebook, Instagram, X, LinkedIn, TikTok, YouTube, Threads — same name + `@lightspeedholdings` |
| 2 — Business infrastructure | Business ownership | Meta Business, TikTok Business Center, YouTube/Google business ownership, LinkedIn company administration, X Professional Account |
| 3 — Branding | Profiles | upload logos, create banners, write bios, add website + contact info, standardize descriptions |
| 4 — Content | Publishing | prepare 10–15 posts, 3–5 short videos, launch announcement, publish consistently |

Work order: **Facebook → Instagram → LinkedIn → X → TikTok → YouTube → Threads**. For each platform, record in the Digital Asset Register: exact account name, username/handle, account type, company email, ownership, administrators, 2FA status, profile image, cover image, category, biography, website, contact information, business-manager relationship, launch status.

## End state

```text
                     LIGHTSPEED HOLDINGS
                             │
       ┌─────────────────────┼─────────────────────┐
       │                     │                     │
    WEBSITE              LINKEDIN                X
       │                     │                     │
       │                 Authority             AI voice
       │
       ├────────────── INSTAGRAM
       │                  │
       │               Visual brand
       │
       ├────────────── TIKTOK
       │                  │
       │              AI education
       │
       └────────────── YOUTUBE
                          │
                    Deep knowledge
```

A coherent ecosystem where social media distributes the company's intellectual property, products, services, and AI expertise.

## Related docs

- Digital Asset Register (single source of truth for provisioning): `docs/marketing/digital-asset-register.md`
- Brand assets & rules: `brand/tokens/brand-tokens.json`, `brand/guidelines/`, `static/brand/social/`
- Daily cadence & publishing: `docs/marketing/daily-cadence-checklist.md`
- Account warm-up protocol: `docs/marketing/warmup-log.md`
- Upload onboarding (profile assets): `docs/SOCIAL_MEDIA_UPLOAD_CHECKLIST.md`
- Content packs: `docs/marketing/warmup-content-pack/`, `docs/marketing/atomized/`
