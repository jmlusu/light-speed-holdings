# Provisioning Kit — LIGHTSPEED HOLDINGS

**Owner:** `social_media_manager` (registry `company-registry.yaml:928`). **Reconciled (2026-09-19):** `social_media_manager` is the confirmed owner; see the #189 reconciliation record in the Digital Asset Register.
**Purpose:** everything needed to go from "accounts provisioned" to "publishing" within 48 hours. Fires the moment [#194](https://github.com/jmlusu/light-speed-holdings/issues/194) clears and the Digital Asset Register shows all Tier 1–3 platforms `Live`.
**Blocked by:** [#194](https://github.com/jmlusu/light-speed-holdings/issues/194) (accounts provisioned), domain control of `lightspeedholdings.com` (sending-domain work), and [#192](https://github.com/jmlusu/light-speed-holdings/issues/192) (Resend sending domain). Content below is ready to ship the day accounts go live.

## 1. Pre-flight dependencies (must be true before Day 0)

| Dependency | Status | Owner | Where tracked |
|---|---|---|---|
| All Tier 1–3 accounts provisioned + 2FA + business ownership | Pending (#194) | `social_media_manager` | `digital-asset-register.md` |
| `info.lightspeed@gmail.com` secured (2FA, recovery phone/email, passkey) | Pending (#194) | `social_media_manager` | Phase 0, `digital-identity-setup.md` |
| Domain `lightspeedholdings.com` under company control (currently an Afternic for-sale lander) | Unresolved (#194) | CEO | `digital-identity-setup.md` |
| Resend sending domain verified (needs company domain) | Blocked (#194/#192) | `social_media_manager` | `digital-asset-register.md` (Resend row) |
| 10–15 post buffer + 3–5 short videos drafted, QA'd, scheduled | **Ready (this kit)** | `social_media_manager` | Section 4 + Section 5 below |
| Brand asset package staged (logo, banners, cover images, templates) | Pending (#194) | `social_media_manager` | `static/brand/social/`, Phase 3 |

## 2. Per-platform setup (run in Phase 1–3 order)

Work order per `digital-identity-setup.md` **Phase plan**: Facebook → Instagram → LinkedIn → X → TikTok → YouTube → Threads. For each platform complete all of:

1. **Account claim** — exact name from the identity rules; username `@lightspeedholdings` (fallbacks `@lightspeedholdingsmw` → `@lightspeedhq`). Claim every platform even if not active yet.
2. **Security** — company-owned root account only; 2FA enabled; credentials in the password manager only (never in the register).
3. **Business ownership** — Meta Business Suite (FB+IG), TikTok Business Center, YouTube/Google business ownership, LinkedIn company administration, X Professional Account.
4. **Branding** — logo, branded cover/banner, platform bio variant from the master description, website (`lightspeedholdings.com` or the afternic-bypass placeholder until domain resolves), contact info.
5. **Register update** — set `Status: Live`, add the public URL to the `URL` column, record administrators.

Platform-specific notes (from `digital-identity-setup.md` § Platform guidance):

| Platform | Setup specifics |
|---|---|
| Facebook | Company **Page** (category ≈ Consulting / IT / Business Service); personal profile is only the administrator; logo + branded cover **AI. STRATEGY. TRANSFORMATION.** |
| Instagram | Professional/Business account; same logo; bio from master → IG variant |
| LinkedIn | Company Page **LIGHTSPEED HOLDINGS LIMITED**; founder connected as **Founder & CEO**; highest priority platform |
| X | `@lightspeedholdings`, convert to X Professional Account → Business; real-time AI/technology thought-leadership channel |
| TikTok | `@lightspeedholdings` Business Account → TikTok Business Center (two-step verification per platform guidance) — "60 seconds of AI" format |
| YouTube | Company channel **LIGHTSPEED HOLDINGS** `@lightspeedholdings`; long-form home for adapted shorts |
| Threads | Reserve `@lightspeedholdings`; activation not required immediately |
| Email (gmail → domain) | Start `info.lightspeed@gmail.com`; migrate to `info@lightspeedholdings.com` (+ `hello@`, `contact@`, `admin@`) when domain exists; `social@`/`digital@` for account management |
| Resend | Needs a verified company sending domain before broadcast delivery; blocked by #194/#192 |

## 3. Day-0 launch sequence

Ordered to match the daily cadence so the first publishing day looks like a normal cadence day:

1. **Launch announcement** (post on LinkedIn company + CEO + X) — "We're live" + what LIGHTSPEED builds.
2. **Positioning post** (LinkedIn carousel / article, "AI. Strategy. Transformation.").
3. **First X thread** (Mon-slot pillar adapted to a thread).
4. **First short video** (YouTube Short + TikTok + IG Reel cross-post) — "What is Agentic AI?".
5. **Reshare** CEO LinkedIn on company page with added context; company X reshare.
6. Update Digital Asset Register launch status; log in warm-up log.

Launch-day gap rule: never open a platform and leave it empty — every platform publishes at least one item on launch day (Threads excluded; reserve-only).

## 4. First-post buffer (15 pieces, QA'd before Day 0)

Mapped from the **First content batch** in `digital-identity-setup.md` (items 1–10) plus launch items. Each gets an `ls-artifact-qa` pass and a cadence slot. Sourced from Pharos pipeline + `content-calendar-90day.md` + `warmup-content-pack/`.

| # | Piece | Primary platform | Adaptation | Cadence slot |
|---|---|---|---|---|
| 1 | Introducing LIGHTSPEED HOLDINGS (who we are) | LinkedIn | X thread + IG story | Day 0 |
| 2 | Why AI-native companies are different | LinkedIn carousel | X thread | Mon/LinkedIn slot |
| 3 | What is Agentic AI? (educational) | X + TikTok | Short video (see §5.1) | Daily TikTok |
| 4 | AI transformation in Africa | LinkedIn article | X thread + IG | Mon pillar siblings |
| 5 | 5 business processes AI agents can automate | LinkedIn carousel | IG carousel + TikTok | Wed hub |
| 6 | Meet the Lightspeed AI ecosystem | LinkedIn | X thread + YouTube short | Thu |
| 7 | AI + management consulting (service model) | LinkedIn | X + IG | Wed |
| 8 | Building for Malawi → SADC → Africa | LinkedIn | YouTube long-form + X | Mon pillar |
| 9 | AI tools we're experimenting with (BTS) | TikTok + IG | X + LinkedIn | Tue video |
| 10 | What we're building at Lightspeed (founder vision) | LinkedIn | CEO X thread | Fri |
| 11 | Launch announcement | All | mirrored everywhere | Day 0 |
| 12 | Positioning statement "AI. Strategy. Transformation." | LinkedIn | cover/bio alignment | Day 0 |
| 13 | Client value / offer explainer | LinkedIn | X thread | Wed |
| 14 | Follow the journey (CEO insight) | CEO LinkedIn | company reshare | Fri |
| 15 | Community opener (what should we build next?) | X + IG | conversation prompt | Fri |

## 5. Short-video plan (5 videos, ≤60s each)

Per platform guidance, "60 seconds of AI" format. Hook-first; brand fonts/colors from the design system; captions always-on; end CTA = follow + website.

| # | Concept | Hook | B-roll / visual | Platform targets |
|---|---|---|---|---|
| 1 | What is Agentic AI? | "Your AI could run itself." | AI orchestration diagrams, lightboard | TikTok, IG Reel, YT Short |
| 2 | Why AI-native companies win | "The companies that ship fastest run on agents." | Split-screen manual vs automated workflow | TikTok, YT Short |
| 3 | 3 processes AI agents can automate | "Reply to leads, triage tasks, draft reports — on autopilot." | Screen-recorded agent demo | TikTok, IG Reel |
| 4 | Building intelligent enterprises in Africa | "Africa's scale-up playbook is being rewritten." | Local b-roll, city timelapse, founder voiceover | YT Short, LinkedIn native video |
| 5 | Meet the Lightspeed stack | "An AI company, run by AI — with a human CEO." | Dashboard / agent cards, studio intro | TikTok, IG Reel |

Production notes: shoot/assemble in batches of 5; captions + brand watermark via the social template kit; `ls-artifact-qa` before publish; post 3–5 videos on TikTok spaced 1–2 hrs per the midday cadence.

## 6. Quality gates (every piece, every platform)

1. **Brand** — official logo + navy/red/cyan palette; tagline ASPIRE. ACT. ACHIEVE.; positioning AI. Strategy. Transformation. Never invent brand colors/fonts.
2. **Approvals matrix** — Tier 1 ships on Marketing + CEO sign-off; Tier 2 (CEO policy commentary, client case studies) requires CLO pre-review before CEO approval — see the #196 approvals-matrix comment.
3. **artifact QA** — `ls-artifact-qa` on every artifact (visual / brand / UX / accessibility / content).
4. **Register + warm-up log** — the moment a platform ships, update the register (`Status: Live` + URL) and log the warm-up step.

## 7. Definition of done

Day 0 (≤48h after #194 clears): all Tier 1–3 registers `Live`, 15-post buffer scheduled across the platforms, 5 short videos published or queued, launch announcement delivered, first cadence day logged, warm-up re-baselined (Track 6).

## Related docs

- Digital Asset Register (provisioning status): `docs/marketing/digital-asset-register.md`
- Digital Identity Setup (runbook, phases, master description): `docs/marketing/digital-identity-setup.md`
- Daily cadence (slots this kit feeds): `docs/marketing/daily-cadence-checklist.md`
- Warm-up protocol + re-baseline: `docs/marketing/warmup-log.md`
- Brand assets: `brand/tokens/`, `brand/guidelines/`, `static/brand/social/`
- Approvals: #196 approvals-matrix comment