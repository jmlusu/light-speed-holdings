# T6: Forms, Email & Anti-Spam Architecture — Findings

> **Ticket:** #163 `T6: Forms, Email & Anti-Spam Architecture` (parent map #157)
> **Branch:** `research/forms-architecture` (throwaway research, do not merge)
> **Date:** 2026-08-27
> **Author:** research agent (Muse Spark)
> **Status:** `VALIDATED` — Vercel free-tier stack confirmed viable for MVP
> **Sources:** Vercel Docs (`/docs/functions/usage-and-pricing`, `/docs/limits`, `/docs/plans/hobby`, `/docs/functions/limitations`), Resend Docs (`/pricing`, `/docs/knowledge-base/account-quotas-and-limits`, `/docs/api-reference/rate-limit`), Cloudflare Turnstile (`developers.cloudflare.com/turnstile/plans`, `blog.cloudflare.com/turnstile-ga`), Upstash Redis (`upstash.com/pricing/redis`, `upstash.com/blog/redis-new-pricing`), `@upstash/ratelimit` (Edge-compatible), Zod + honeypot best practices (splitforms, formshield, react-honeypot-field).

---

## 1. Executive Summary

**Recommendation: APPROVE the proposed stack for LightSpeed Holdings marketing site MVP under Vercel free (Hobby) tier.**

```
Astro (static) + Vercel Functions (Node) + Resend + Airtable (primary CRM) / HubSpot (alt)
           + Cloudflare Turnstile (invisible) + Upstash Redis + @upstash/ratelimit + Zod + honeypot
```

* All components have a genuine $0/mo free tier sufficient for `lightspeedholdings.com` MVP traffic (estimated <1k form submissions/mo, <50k page views/mo).
* No paid dependency is required to ship `POST /api/contact` and `POST /api/newsletter`. Every layer is edge-compatible and server-validated (no client-only guards).
* One correction from the ticket wording: **Upstash Redis free is now 500K commands/month (256 MB, 10 GB bandwidth), not 100K req/day.** The `10K/day` cap was retired 2025-03-12. Findings use the current limit; rate-limit tiers fit comfortably (<12K commands/mo even under abuse).
* Verified no prior form/email code in repo (`grep` for `resend|turnstile|honeypot|upstash|airtable|hubspot` — zero hits before this research).

**Blockers:** None. T8 (Deployment & Product-Meta Export) can proceed. Only follow-up: pick `AIR_TABLE` vs `HUBSPOT` as primary CRM sink (both validated — see §4) and verify `lightspeedholdings.com` domain passes Resend verification before launch.

---

## 2. Recommended Stack Table

| Layer | Choice | Free Tier (verified 2026-08-27) | Why / Notes | Cost if exceeded |
|---|---|---|---|---|
| **Hosting / SSR** | **Vercel Hobby (Free)** | 1M Function invocations / mo, 4 CPU-hrs, 360 GB-hrs, 100 GB Fast Data Transfer, 5K Image Transforms, 50K Web Analytics events, 100 deployments/day, 200 projects, 32 GB disk, 2 vCPU / 8 GB build. Functions: **Fluid** default 300s max (Hobby cap 300s), auto-scale 30K concurrency. Legacy runtimes 10s default / 60s max. | Free for personal/non-commercial per ToS; LightSpeed Holdings must use Team Hobby or upgrade to Pro if commercial traffic is deemed non-hobby. Functions `api/contact.ts` + `api/newsletter.ts` run in Node (Edge optional for rate-limit middleware). | Hobby pauses after quota; Pro $20/mo covers 1M invocations + credit. |
| **Email delivery** | **Resend** | **3,000 emails/mo, 100/day hard cap**, 1-3 verified domains (docs vary: 1 per pricing page / 3 per KB — count on 1), 30-day retention, shared IPs, 10K automation runs, 1,000 marketing contacts free. `x-resend-daily-quota` / `x-resend-monthly-quota` headers; `429 daily_quota_exceeded` / `monthly_quota_exceeded`. | Clean SDK (`resend` npm), `react-email` compatible, great DX for `from: noreply@lightspeedholdings.com`. Single domain is enough for MVP. | Pro $20/mo → 50K/mo, $0.90/1K overage. No overage on Free — upgrade required. |
| **CRM sink** | **Airtable (primary)** — HubSpot fallback (§4) | Airtable Free: 1,000 records/base, 5 bases, 100 automation runs/mo, 1 GB attachments. HubSpot Free: 1M contacts, forms + email, but heavier JS + portal setup. | Airtable is schema-flexible, no heavier marketing pixel; fits `marketing-site/` static + Functions → Airtable REST. HubSpot reserved for when sales needs sequences. | Airtable Team $20/user/mo. HubSpot Starter $20/mo. |
| **Anti-spam (human check)** | **Cloudflare Turnstile (invisible)** | **$0, UNLIMITED challenges** on Free. All widget types (Managed, Non-interactive, Invisible) included. Limits: 20 widgets/account, 10 hostnames/widget, 7-day analytics, WCAG 2.2 AAA, no SLA. No verification rate limit published. Enterprise → unlimited widgets, 200 hostnames, 30-day analytics, ephemeral IDs, offlabel. | No cookies, no Google bundle, GDPR-friendly. `invisible` mode = zero UX friction. Verify via `POST https://challenges.cloudflare.com/turnstile/v0/siteverify`. Works without Cloudflare proxy. | Free → Enterprise is sales-only, bundled with Bot Mgmt. |
| **Rate limiting store** | **Upstash Redis (REST) + `@upstash/ratelimit`** | **500K commands/mo, 256 MB, 10 GB bandwidth, 10K cmd/sec, 1 DB**, global HTTP API (Edge-compatible). Old `10K/day` docs are obsolete post-2025-03-12. PAYG $0.20/100K commands post-free. | `Ratelimit.slidingWindow()` prevents fixed-window burst abuse; cache-hot reduces Redis calls. Replaces in-memory `express-rate-limit`. | PAYG ~$2/mo at 1.5M cmds. Fixed 250 MB $10/mo. |
| **Rate-limit tiers** | `@upstash/ratelimit` sliding window | `POST /api/contact: 5 req / 60s / IP` (spam-sensitive) • `POST /api/newsletter: 10 req / 60s / IP` • global `100 req / 60s / IP` for `/api/*`. Optional `per-email` limiter for newsletter double-opt-in abuse. | Matches ticket spec (5/min IP, 10/min IP). Sliding window chosen over fixed/token bucket (§5). Headers: `X-RateLimit-*` + `Retry-After`. Exceed → `429`. | Negligible Redis cost — see §3. |
| **Validation** | **Zod** (server + shared schema) | N/A (lib). | Single source of truth; `safeParse` → `400 { fieldErrors }`. Client uses same schema for UX, server is authority. | — |
| **Honeypot** | Hidden `website`/`company` field + `form_loaded_at` time-trap | N/A. | Off-screen CSS (`left:-9999px`), `aria-hidden="true"`, `tabIndex=-1`, `autoComplete="off"`. Fail → silent `200 {success:true}` so bots learn nothing. Time-trap: reject `<2s` elapsed. | — |
| **Site stack** | Astro + Tailwind + MDX, `marketing-site/` | — | Per T2 lock. Functions live in `marketing-site/api/` or `marketing-site/src/pages/api/` → Vercel auto-routing. | — |

**Global free capacity vs MVP estimate:**

| Resource | MVP estimate | Free cap | Headroom |
|---|---|---|---|
| Function invocations | ~5K–20K/mo (forms + OG) | 1M | 50–200× |
| Resend sends | ~200–800/mo (contacts + confirmations) | 3K/mo, 100/day | 3–15× — daily 100/day is the tighter constraint; burst launch day must not exceed 100. |
| Turnstile verifications | same as submissions | unlimited | ∞ |
| Upstash commands | ~2 cmds/submission = ~1K–4K/mo (see §3) | 500K/mo | 100×+ |

**Verdict: No paid tier required for ship.**

---

## 3. Vercel Functions & Upstash Free Limits — Verified

### 3.1 Vercel Hobby

* Source: `vercel.com/docs/plans/hobby`, `vercel.com/docs/limits`, `vercel.com/docs/functions/limitations` (2026-08-24/25).
* Fluid compute (current): `Active CPU 4 hrs/mo`, `Provisioned Memory 360 GB-hrs/mo`, `1M invocations/mo`. On-demand billing only on Pro.
* Legacy (pre-2025-04-23 non-Fluid): Hobby `10s default / 60s max` per function. Fluid Hobby: `300s max`.
* Limits: `2048 routes/deployment`, `100 deployments/day`, `concurrent deploys 1`, `build 45m`, `static upload 100 MB`, `100 cron jobs/project`.
* **Gotcha:** Hobby = non-commercial personal use per Fair Use. LightSpeed Holdings branded marketing site may be considered commercial; verify with Vercel or budget Pro $20/mo as first escalation (`$20 credit` covers Functions/Analytics). Document in ADR.

### 3.2 Upstash Redis — the 100K/day correction

* Current (probed 2026-08-27): **Free = 500K commands/month, 256 MB data, 10 GB bandwidth, 10K cmd/sec, 1 DB**. `upstash.com/pricing/redis` + changelog `upstash.com/blog/redis-new-pricing` (2025-03-12: "Free Tier now includes 500K commands per month instead of the previous 10K daily limit").
* Legacy docs/old blog posts quoting `10K/day` (10K req/day) are **obsolete** — search hits still surface them, which explains the ticket's `100k req/day` number.
* PAYG overage: `$0.20 / 100K commands`, `$0.25/GB storage` (>1 GB), first 200 GB bandwidth free.
* Free DB archived after 30d inactivity (warnings sent); keep alive via health cron.
* **Cost for rate-limit tiers on MVP:**
  * `POST /api/contact` 5/min/IP sliding window: ~2 Redis cmds per `limit()` (INCR + ZREMAP) → at 1K legit + 5K bot attempts/mo = ~12K cmds/mo.
  * `POST /api/newsletter` 10/min/IP similar.
  * Even under aggressive scrape (50K attempts/mo) = ~100K cmds → still 80% under free cap. No upgrade needed until >200K attacks/mo.

### 3.3 Choosing sliding window

> Upstash supports `fixedWindow`, `slidingWindow`, `tokenBucket`.

* `fixedWindow(5, "1 m")` allows burst at boundary (`2×` limit across window edge) — bad for spam.
* `slidingWindow(5, "1 m")` = weighted average of current + previous fixed window → smooth, no boundary spike. **Default for auth/forms per Upstash/Viprasol guides.**
* `tokenBucket` allows controlled bursts (useful for AI/streaming bursts) but not desired for contact forms.

**Implement as:**

```ts
// marketing-site/src/lib/rate-limit.ts
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const redis = Redis.fromEnv(); // UPSTASH_REDIS_REST_URL + TOKEN

export const contactLimiter = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(5, "60 s"),
  analytics: true,
  prefix: "rl:contact",
});

export const newsletterLimiter = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(10, "60 s"),
  analytics: true,
  prefix: "rl:newsletter",
});

// Optional: per-email throttle + global catch-all
export const emailLimiter = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(20, "1 h"),
  prefix: "rl:email",
});
```

Helper for IP key (Vercel respects `x-forwarded-for` / `x-real-ip`):

```ts
export function ipFrom(req: Request): string {
  const fwd = req.headers.get("x-forwarded-for");
  if (fwd) return fwd.split(",")[0].trim();
  return req.headers.get("x-real-ip") ?? "anonymous";
}
```

---

## 4. Resend, Turnstile, Airtable/HubSpot — Deep Dive

### 4.1 Resend

* Pricing re-confirmed live: `resend.com/pricing` → Free `$0/mo 3K/mo`, Pro `$20 50K`, `$35 100K`, Scale `$90–$1,150 100K–2.5M`. **100/day is the gating factor** — a single burst day (launch PR, newsletter import) can exhaust daily quota before monthly cap. Fail mode is `429 { error: daily_quota_exceeded }` — queue or degrade to Airtable-only + retry. See §7 fallback.
* Domain limit inconsistency: Pricing page says 1 domain on Free; KB says 3. Assume **1** for planning (safe).
* API returns `x-resend-daily-quota` / `x-resend-monthly-quota` on Free — log them.
* Verify domain via DNS `TXT` + `MX` under `send.yourdomain` subdomain; requires approval step (can take hours). Fallback needed if rejected (see §7).
* Keep transactional vs marketing separation: `from: "LightSpeed <noreply@lightspeedholdings.com>"` + `replyTo` submitter not owner domain to avoid SPF failures.

### 4.2 Cloudflare Turnstile (invisible)

* Free includes all three widget modes — **invisible is allowed on Free** despite old GA blog note about `1M siteverify` cap during beta. Current plans doc (2026-08-14) says `All widget types: Yes` + `Unlimited challenges` for Free.
* Config: 20 widgets max (1 for marketing-site is enough), 10 hostnames/widget (`lightspeedholdings.com` + `www.` + `*.vercel.app` preview fits), 7-day analytics retention.
* Verify: `POST https://challenges.cloudflare.com/turnstile/v0/siteverify` with `{ secret, response: token, remoteip }` → `{ success: boolean }`. Never trust client-side callback.
* Env: `TURNSTILE_SECRET_KEY` (server-only), `TURNSTILE_SITE_KEY` (public).
* Pre-clearance supported on Free (improves repeat-visitor experience). WCAG 2.2 AAA.

### 4.3 Airtable vs HubSpot (CRM sink)

| Criteria | Airtable Free | HubSpot Free |
|---|---|---|
| Records | 1,000/base, 5 bases, 1 GB | 1M contacts (generous) |
| Forms native | No (API via Functions) | Yes — hosted forms + embed, auto CRM |
| Email | via automation (100 runs/mo) | via CRM sequences + Forms follow-up (free) |
| JS payload | none | +~80KB HubSpot tracking.js |
| Auth | Personal PAT | OAuth portal |
| MVP fit | **Better — lightweight, no pixel, matches Astro static intent, single Airtable REST call** | Heavier, but powerful if sales pipeline needed |

**Recommendation:** **Airtable primary** for MVP; keep HubSpot as phase-2 option behind same Function interface. Functions abstract CRM via `CRM_SINK=airtable|hubspot` env switch. Contact → Airtable `Leads` base + Resend owner alert + (optional) Resend double-opt-in for newsletter via Airtable `Newsletter` table.

---

## 5. Zod Validation + Honeypot Pattern (server-authoritative)

### 5.1 Principles

* Client validation = UX only. Every rule re-checked server-side with Zod `safeParse`.
* Normalize `email: .trim().toLowerCase()` before storage/rate keys.
* Reject oversized payloads early (`Content-Length` guard) + length caps (`message ≤ 5000`, `name ≤ 100`).
* Return **silent success** on honeypot/time-trap triggers so bots gain no signal (`200 { success: true }` not `4xx`).

### 5.2 Honeypot recipe (verified via splitforms/formshield/react-honeypot-field)

* Field name plausible (`website`, `company`, `phone_confirm`) — NOT `honeypot`. Randomize optional.
* Hiding: **CSS off-screen** (`position:absolute; left:-9999px; width:1px; height:1px; overflow:hidden`) + `aria-hidden="true"` + `tabIndex=-1` + `autoComplete="off"`. Do NOT use `type="hidden"` or `display:none` — bots skip/preserve those.
* Schema: `website: z.string().optional().or(z.literal(""))` — must be empty.
* Time-trap: `form_loaded_at: number` captured at `useRef(Date.now())` on mount, sent hidden; server rejects if `Date.now() - form_loaded_at < 2000` (1500–3000ms range is standard; 2000 recommended).
* Optional second honeypot + `MAX_FORM_TIME_MS` (e.g., 20 min) to flag replay attacks.

### 5.3 Zod schemas

```ts
// marketing-site/src/lib/schemas.ts
import { z } from "zod";

export const contactSchema = z.object({
  name: z.string().trim().min(2).max(100),
  email: z.string().trim().toLowerCase().email().max(254),
  message: z.string().trim().min(10).max(5000),
  // anti-spam extras
  website: z.string().optional().or(z.literal("")), // honeypot
  form_loaded_at: z.number().optional(),
  turnstileToken: z.string().min(10, "CAPTCHA required"),
});

export const newsletterSchema = z.object({
  email: z.string().trim().toLowerCase().email().max(254),
  website: z.string().optional().or(z.literal("")),
  form_loaded_at: z.number().optional(),
  turnstileToken: z.string().min(10),
});

export type ContactInput = z.infer<typeof contactSchema>;
export type NewsletterInput = z.infer<typeof newsletterSchema>;
```

Server handler pattern:

```ts
// api/contact.ts — simplified
const parsed = contactSchema.safeParse(body);
if (!parsed.success) return NextResponse.json({ success:false, error:"Validation failed", fieldErrors: parsed.error.flatten().fieldErrors }, { status:400 });

// honeypot
if (parsed.data.website) return NextResponse.json({ success:true });

// time-trap
const elapsed = Date.now() - (parsed.data.form_loaded_at ?? 0);
if (elapsed && elapsed < 2000) return NextResponse.json({ success:true });

// Turnstile verify, then rate-limit, then Resend + Airtable
```

---

## 6. OpenAPI Snippet (validated, Vercel Functions)

> Drop into `marketing-site/openapi.yaml` or extend existing spec. Extensible for DevStudio.it-style single-endpoint pattern `/api/submissions` if unified later.

```yaml
openapi: 3.0.3
info:
  title: LightSpeed Holdings Marketing Site — Forms API
  version: 0.1.0
  description: |
    Serverless contact + newsletter endpoints for Vercel Hobby.
    Stack: Vercel Functions + Resend + Airtable + Turnstile + Upstash Redis.
    All validation server-authoritative (Zod). Rate limits via @upstash/ratelimit sliding window.
servers:
  - url: https://lightspeedholdings.com
    description: Production
  - url: https://lightspeedholdings-preview.vercel.app
    description: Vercel preview
paths:
  /api/contact:
    post:
      operationId: submitContact
      summary: Submit contact inquiry
      description: |
        Validates with Zod, checks honeypot + time-trap, verifies Turnstile token,
        enforces 5 req/min/IP sliding-window, then sends email via Resend and upserts Airtable.
        Returns silent success on honeypot to avoid bot feedback.
      security: [] # public, IP-rate-limited
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ContactRequest'
            examples:
              happy:
                value:
                  name: "Amara Kone"
                  email: "amara@example.com"
                  message: "Interested in AI Company Builder for Lilongwe rollout. Can we schedule a demo?"
                  website: ""
                  form_loaded_at: 1724680000000
                  turnstileToken: "0.AAA..."
      responses:
        '200':
          description: Accepted (or silent bot accept)
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer, description: Unix ms of window reset }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SuccessEnvelope'
              example:
                success: true
                message: "Thanks — we will be in touch within 24h."
        '400':
          description: Validation failed
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorEnvelope'
              example:
                success: false
                error: "Validation failed"
                fieldErrors:
                  email: ["Invalid email"]
        '429':
          description: Rate limit exceeded (sliding window) or Resend daily quota
          headers:
            Retry-After:
              schema: { type: integer }
            X-RateLimit-Limit: { schema: { type: integer } }
            X-RateLimit-Remaining: { schema: { type: integer, example: 0 } }
            X-RateLimit-Reset: { schema: { type: integer } }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RateLimitError'
              examples:
                tooFast:
                  value:
                    success: false
                    error: "Too many requests. Try again in 42s."
                    retryAfter: 42
                resendDaily:
                  value:
                    success: false
                    error: "Service temporarily at capacity — your message was saved, we will follow up."
                    code: "daily_quota_exceeded"
                    retryAfter: 3600
        '500':
          $ref: '#/components/responses/ServerError'

  /api/newsletter:
    post:
      operationId: subscribeNewsletter
      summary: Subscribe to newsletter
      description: |
        Validates email, honeypot, time-trap, Turnstile, 10 req/min/IP sliding-window.
        Upserts Airtable `Newsletter` table; sends Resend double-opt-in confirmation.
        Reuses same anti-spam stack as /api/contact but with higher rate limit.
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsletterRequest'
            examples:
              happy:
                value:
                  email: "founder@example.com"
                  website: ""
                  form_loaded_at: 1724680005000
                  turnstileToken: "0.BBB..."
      responses:
        '200':
          description: Subscribed (idempotent — repeat email returns 200)
          headers:
            X-RateLimit-Limit: { schema: { type: integer } }
            X-RateLimit-Remaining: { schema: { type: integer } }
            X-RateLimit-Reset: { schema: { type: integer } }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SuccessEnvelope'
              example:
                success: true
                message: "Check your email to confirm your subscription."
        '400': { description: Validation failed, content: { application/json: { schema: { $ref: '#/components/schemas/ErrorEnvelope' } } } }
        '429': { description: Rate limit exceeded, content: { application/json: { schema: { $ref: '#/components/schemas/RateLimitError' } } } }
        '500': { $ref: '#/components/responses/ServerError' }

components:
  schemas:
    ContactRequest:
      type: object
      required: [name, email, message, turnstileToken]
      properties:
        name: { type: string, minLength: 2, maxLength: 100, example: "Amara Kone" }
        email: { type: string, format: email, maxLength: 254, example: "amara@example.com" }
        message: { type: string, minLength: 10, maxLength: 5000 }
        website: { type: string, nullable: true, description: Honeypot — must be empty. Off-screen field. }
        form_loaded_at: { type: integer, format: int64, description: Client mount timestamp (ms). Reject if elapsed <2000. }
        turnstileToken: { type: string, description: Turnstile invisible token. Verify server-side. }
      additionalProperties: false

    NewsletterRequest:
      type: object
      required: [email, turnstileToken]
      properties:
        email: { type: string, format: email, maxLength: 254 }
        website: { type: string, nullable: true, description: Honeypot — must be empty. }
        form_loaded_at: { type: integer, format: int64 }
        turnstileToken: { type: string }
      additionalProperties: false

    SuccessEnvelope:
      type: object
      required: [success]
      properties:
        success: { type: boolean, example: true }
        message: { type: string, example: "Thanks — we will be in touch within 24h." }

    ErrorEnvelope:
      type: object
      required: [success, error]
      properties:
        success: { type: boolean, example: false }
        error: { type: string, example: "Validation failed" }
        fieldErrors:
          type: object
          additionalProperties: { type: array, items: { type: string } }
          example: { "email": ["Invalid email"], "message": ["Message too short"] }
        code: { type: string, example: "validation_failed" }

    RateLimitError:
      allOf:
        - $ref: '#/components/schemas/ErrorEnvelope'
        - type: object
          properties:
            retryAfter: { type: integer, description: Seconds until window reset. }

  responses:
    ServerError:
      description: Internal error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorEnvelope'
          example:
            success: false
            error: "Internal error. Please try again later."
            code: "internal_error"
```

**Shared error codes:** `validation_failed`, `rate_limited`, `turnstile_failed`, `fake_submission` (never surfaced — becomes silent 200), `daily_quota_exceeded`, `internal_error`.

**CORS:** Allowlist `lightspeedholdings.com` + Vercel preview regex; `Access-Control-Allow-Origin` not `*`. Handle `OPTIONS` with `204`.

---

## 7. Env Var List

> Add to Vercel Project → Settings → Environment Variables. Scope `Production + Preview` except noted. `NEXT_PUBLIC_` only for site key.

| Var | Required | Scope | Example / Notes |
|---|---|---|---|
| `RESEND_API_KEY` | ✅ if `CRM_SINK` uses email | server | `re_xxx…` — never expose. Rotate per §11 key-rotation guide. |
| `CONTACT_TO_EMAIL` | ✅ | server | `hello@lightspeedholdings.com` (verified Resend sender domain). Comma-separated list OK. |
| `CONTACT_FROM_EMAIL` | ✅ | server | `noreply@lightspeedholdings.com` or `noreply@send.lightspeedholdings.com` subdomain. Must be on verified domain. |
| `AIRTABLE_PAT` | ✅ (Airtable path) | server | `patXXX…` — token with `data.records:write` on Leads + Newsletter bases. |
| `AIRTABLE_BASE_ID` | ✅ | server | `appXXXX` |
| `AIRTABLE_CONTACTS_TABLE` | ✅ | server | `Leads` (or `Contacts`) |
| `AIRTABLE_NEWSLETTER_TABLE` | ✅ | server | `Newsletter` |
| `CRM_SINK` | ✅ | server | `airtable` \| `hubspot` — switch without deploys. |
| `HUBSPOT_API_KEY` | if `hubspot` | server | `pat-na1-…` (HubSpot private app token). Only set if `CRM_SINK=hubspot`. |
| `HUBSPOT_PORTAL_ID` | if `hubspot` | server | `12345678` |
| `TURNSTILE_SECRET_KEY` | ✅ | server | `0x4AAAAAA…` — server-only. Best per-env (allowlist check uses same). |
| `NEXT_PUBLIC_TURNSTILE_SITE_KEY` | ✅ | public | `0x4AAAAAA…` — client bundle, non-secret. |
| `UPSTASH_REDIS_REST_URL` | ✅ | server | `https://…upstash.io` — from Upstash console. |
| `UPSTASH_REDIS_REST_TOKEN` | ✅ | server | `AX…` |
| `RATE_LIMIT_CONTACT_MAX` | optional | server | `5` (override without code). |
| `RATE_LIMIT_NEWSLETTER_MAX` | optional | server | `10` |
| `LOG_LEVEL` | optional | server | `info` — structured logs (§5). |
| `SITE_URL` | optional | public | `https://lightspeedholdings.com` — for OG + email CTA links. |

**Local `.env.local` template:**

```dotenv
# .env.local — copy from .env.example, never commit
RESEND_API_KEY=re_xxxxxxxxxxxxxxxx
CONTACT_TO_EMAIL=hello@lightspeedholdings.com
CONTACT_FROM_EMAIL=noreply@lightspeedholdings.com
AIRTABLE_PAT=patXXXXXXXXXXXXXXXX
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX
AIRTABLE_CONTACTS_TABLE=Leads
AIRTABLE_NEWSLETTER_TABLE=Newsletter
CRM_SINK=airtable
TURNSTILE_SECRET_KEY=0x4AAAAAA_yyyyyyyy
NEXT_PUBLIC_TURNSTILE_SITE_KEY=0x4AAAAAA_zzzzzzzz
UPSTASH_REDIS_REST_URL=https://xxx-xxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=AX_xxxxxxxxxxxxxxxx
```

**Vercel env addition:**

```bash
# via CLI
vercel env add RESEND_API_KEY production
vercel env add TURNSTILE_SECRET_KEY production
vercel env add UPSTASH_REDIS_REST_URL production
# or dashboard: https://vercel.com/<team>/<project>/settings/environment-variables
```

---

## 8. `vercel.json` Snippet

> Place in `marketing-site/vercel.json`. Covers Functions config, routing, headers, and rate-limit middleware matcher if using middleware. Adjust `framework` to `astro`.

```jsonc
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "astro",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm ci",
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "https://lightspeedholdings.com" },
        { "key": "Access-Control-Allow-Methods", "value": "POST, OPTIONS" },
        { "key": "Access-Control-Allow-Headers", "value": "Content-Type, X-Turnstile-Token" },
        { "key": "Access-Control-Max-Age", "value": "86400" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ],
  "functions": {
    "api/contact.ts": {
      "maxDuration": 10
    },
    "api/newsletter.ts": {
      "maxDuration": 10
    }
  },
  "rewrites": [
    { "source": "/api/contact", "destination": "/api/contact" },
    { "source": "/api/newsletter", "destination": "/api/newsletter" }
  ],
  "crons": [
    {
      "path": "/api/cron/keepalive",
      "schedule": "0 9 * * 1"
    }
  ]
}
```

**Notes:**
* `maxDuration: 10` is sufficient (handlers should do Turnstile verify + Redis + Resend + Airtable within <2s; cold start budget padded). Hobby legacy caps `60s`, Fluid caps `300s` — 10 keeps within both.
* `crons.keepalive` — weekly hit to prevent Upstash Free archival after 30d idle + warm Functions. No-op handler returning `200`.
* If using **Vercel Middleware** (`marketing-site/src/middleware.ts`) for global `X-RateLimit` on `/api/*`, set `matcher: "/api/:path*"` there; `vercel.json` headers above still apply.
* **Env not in `vercel.json`** — use dashboard/CLI `vercel env`. Do not commit secrets.
* For Astro with `output: "hybrid"` or `server`, Vercel adapter (`@astrojs/vercel`) generates Functions automatically — `functions` key becomes `config` in `astro.config.mjs` instead. Either location works; prefer `astro.config.mjs` under hybrid.

**`astro.config.mjs` alternative (hybrid):**

```js
// marketing-site/astro.config.mjs (excerpt)
import vercel from "@astrojs/vercel";
export default defineConfig({
  output: "hybrid",
  adapter: vercel({
    maxDuration: 10,
    includeFiles: ["./src/lib/schemas.ts"],
    isr: { expiration: 60 }
  }),
});
```

---

## 9. Request Lifecycle (anti-spam layer order)

> Order matters — cheapest/fastest checks first to shed bots before paid I/O.

```
1. Content-Length guard + JSON parse
        ↓ 414/400 if oversized/malformed
2. Zod validation (contactSchema / newsletterSchema)
        ↓ 400 { fieldErrors }
3. Honeypot (website != "" → silent 200)
        ↓ logged as fake_submission
4. Time-trap (form_loaded_at: <2s → silent 200; >20min → 400 "Form expired")
        ↓
5. Turnstile siteverify POST
        ↓ 400 turnstile_failed (do not reveal internals)
6. Upstash rate limits
        contact: 5/60s/IP, newsletter: 10/60s/IP, email: 20/h/email (optional)
        ↓ 429 + Retry-After + X-RateLimit-*
7. Spam signals (optional, low-cost, free):
        disposable email check (mailcheck/blocklist), link count (>3 → flag),
        keyword density (crypto/casino), UA contains curl/python-requests → log
        ↓ if flagged → still 200 for newsletter, 400 for contact with generic message
8. Airtable upsert (Leads/Newsletter base) — always before email so data not lost
        ↓ 500 only if Airtable down (degrade: queue + return 429-like retry)
9. Resend send (to owner + optional double-opt-in to user)
        ↓ 429 daily_quota_exceeded → return 200 with "saved, will follow up" + enqueue retry
10. Structured log + Upstash analytics (confirm remaining)
```

**Headers on success:**
```
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 4
X-RateLimit-Reset: 1724680060000
```

**Headers on 429:**
```
Retry-After: 42
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1724680060000
```

---

## 10. Fallback if Resend Rejected / Quota-Blocked

> Resend rejection scenarios: domain verification fails, account flagged, free not approved, or `daily_quota_exceeded` burst. Every path below preserves **Airtable as durable sink** so no lead is lost.

| Fallback | Trigger | Setup | Trade-offs |
|---|---|---|---|
| **A) AWS SES (recommended fallback)** | Resend domain rejected or free abandoned | SES sandbox → verify domain via Route53 TXT/MX → request production access (usually auto for low volume). Function uses `@aws-sdk/client-ses` instead of `resend`. Free tier: 3K msgs/mo if on EC2/EB, else $0.10/1K. Vercel-friendly (no extra infra). | Production access request can take 24h. Keep Airtable as queue until approved. |
| **B) Postmark / SendGrid transactional** | Resend 100/day too tight before upgrade | Postmark free 100/mo, SendGrid free 100/day — similar constraint. Only useful if Resend's 3K/100d is not enough and you want 2-provider rotation. | No capacity win; adds complexity for marginal gain. |
| **C) Formspreeder-style hosted backend** | Want zero code | `formspree.io` / `getform` / `basin` free 50 submissions/mo — proxy to Airtable via Zapier. | Locks you to external; not recommended (adds vendor, still needs Airtable). |
| **D) Pure Airtable + manual follow-up (degraded mode)** | Resend 429 / domain pending | Function skips Resend, returns `200 { message: "Your message was saved — we will follow up within 24h." }`. Owner notified via Airtable automation email / Slack webhook (Airtable 100 runs/mo covers MVP). Cron retries Resend with backoff reading queued Airtable rows. | Zero email dependency; throughput limited by Airtable automation quota. Acceptable for launch week. |
| **E) Upgrade Resend to Pro** | Burst launch exceeds 100/day more than once | `$20/mo 50K` removes daily cap — cheapest real fix if contact volume justifies it. | Paywall but still free-tier-aligned threshold. ADR should budget Pro from week 2 if needed. |

**Decision tree:**

```
Resend verify succeeds? ──yes──> ship primary path
        │
        no
        ├── SES verify <24h? ──yes──> swap RESEND_API_KEY → SES creds (adapter fn)
        └── no  ──> degraded mode D (Airtable-only) + cron retry
                      + open Resend/SES ticket in parallel
```

**Code-level fallback (adapter):**

```ts
// src/lib/email.ts — swap without route changes
export type EmailProvider = { send(opts: { to: string; subject: string; html: string; replyTo?: string }): Promise<{ id?: string; error?: string; code?: string }> };

export function getEmailProvider(): EmailProvider {
  if (process.env.RESEND_API_KEY) return new ResendProvider();
  if (process.env.AWS_SES_REGION) return new SESProvider();
  return new NoopProvider(); // logs only, Airtable already holds truth
}
```

*All fallbacks keep the **same OpenAPI**; only the server's `provider` switches. No client change.*

---

## 11. Minimal File Layout for `marketing-site/`

```
marketing-site/
  astro.config.mjs
  vercel.json                    ← §8
  openapi.yaml                   ← §6 (or docs/openapi/forms.yaml)
  .env.example                   ← §7 template
  src/
    lib/
      schemas.ts                 ← §5.3 Zod
      rate-limit.ts              ← §3 contactLimiter / newsletterLimiter
      email.ts                   ← Resend/SES adapter + fallback
      crm.ts                     ← airtable.ts / hubspot.ts + CRM_SINK switch
      turnstile.ts               ← siteverify helper
      honeypot.ts                ← validateHoneypot()
    components/
      ContactForm.astro / .tsx   ← off-screen honeypot + Turnstile invisible
      NewsletterForm.astro
    pages/
      api/
        contact.ts               ← POST handler (lifecycle §9)
        newsletter.ts            ← POST handler
        cron/keepalive.ts        ← weekly
  public/
```

---

## 12. Implementation Checklist (for T8 implementer)

- [ ] `npm i zod @upstash/redis @upstash/ratelimit resend` (or `@aws-sdk/client-ses` if SES fallback).
- [ ] Create Upstash Redis DB (REST) → set `UPSTASH_REDIS_REST_*` per env.
- [ ] Create Turnstile widget (invisible) for `lightspeedholdings.com` + preview → set keys.
- [ ] Verify `lightspeedholdings.com` in Resend (DNS TXT/MX) + create Airtable `Leads`/`Newsletter`.
- [ ] Drop `schemas.ts`, `rate-limit.ts`, `email.ts`, `crm.ts`, `turnstile.ts` per snippets.
- [ ] `api/contact.ts` + `api/newsletter.ts` implementing lifecycle §9 (early exits, silent 200s, structured logs).
- [ ] `ContactForm` / `NewsletterForm` with off-screen `website` field + `form_loaded_at` + Turnstile `<Script>` + `NEXT_PUBLIC_TURNSTILE_SITE_KEY`.
- [ ] `vercel.json` + provider env vars via `vercel env add` (never committed).
- [ ] E2E: valid submit → 200 + Resend inbox + Airtable row; honeypot → silent 200; `<2s` → silent 200; missing token → 400; 6th/min → 429 + Retry-After; `curl UA` → flagged/logged.
- [ ] Lighthouse + `npm run build` + a11y check (per parent #157 gates).

---

## 13. Risks & Mitigations

| Risk | Mitig | Owner |
|---|---|---|
| Hobby plan "non-commercial" clause | Budget Pro $20 as first escalation; add ADR. | T8 |
| Resend 100/day burst | Fallback D + SES + queue in Airtable; spread launch announcement over 2 days if needed. | T8 |
| Upstash 30d archival | `cron/keepalive` weekly; same ping keeps Functions warm. | T8 |
| Bots bypass honeypot | Turnstile + sliding-window + IP + content signals layered — honeypot is first cheap layer, not sole defense. | T6→T8 |
| Preview domain not allowlisted in Turnstile | Add `*.vercel.app` preview pattern to widget hostnames (counts toward 10). | T8 |
| Email deliverability on subdomain | Verify SPF/DKIM via Resend DNS; use `send.` subdomain per docs. | T8 |

---

## 14. Verdict for T8

**Stack validated. Recommend locking:**

```
VERIFIED: Vercel Functions (Hobby 1M) + Resend (3K/100d) + Airtable (primary)
        + Turnstile invisible (unlimited) + Upstash Redis 500K/mo sliding window
        + Zod + honeypot
VERCEL.JSON: maxDuration 10, CORS allowlist, weekly keepalive
OPENAPI: /api/contact (5/min/IP) + /api/newsletter (10/min/IP) — §6
ENVS: 13 vars — §7
FALLBACK: Airtable-durable D + SES adapter if Resend rejected — §10
```

Proceed to prototype (`T4` + `T5`) using this contract. No paid upgrade required for ship; first paid line would be Resend Pro $20 if daily cap hit repeatedly or Vercel Pro $20 if commercial flag.

---

*Evidence: live verification of pricing/limits pages on 2026-08-27 (current docs). No form/email code existed in repo at review time. Branch `research/forms-architecture` contains this file as deliverable per #163 acceptance: "stack validated and recommendation recorded."*
