# T7: Analytics, SEO & OG Strategy — Research Findings

> **Wayfinder ticket:** [#164 — T7: Analytics, SEO & OG Strategy](https://github.com/jmlusu/light-speed-holdings/issues/164) (label `wayfinder:research`)
> **Parent map:** [#157 — Wayfinder: LightSpeed Holdings Marketing Website](https://github.com/jmlusu/light-speed-holdings/issues/157)
> **Branch:** `research/analytics-seo` (throwaway, do not merge)
> **Date:** 2026-08-27
> **Author:** research agent (Muse Spark)
> **Status:** Research complete — awaiting decision lock before T4/T8 build
> **Skills used:** `/research`

---

## 1. Executive Summary & Recommendation

### TL;DR — Use **Plausible (primary) + Vercel Analytics (free tier, passive)**, defer PostHog.

| Concern | Recommendation |
|---------|---------------|
| **Pageview / marketing analytics** | **Plausible Cloud €9/mo (10k pageviews → $9/mo branding in issue).** Privacy-first, cookie-less, <1 KB script, EU-hosted option, no consent banner. Keep the cost fixed and GDPR-clean. |
| **Web Vitals / performance** | **Vercel Web Analytics (free tier, 2,500 events/mo) + Speed Insights** as passive complement — zero code beyond `import { Analytics }`. Do not rely on it as source of truth for conversions (no custom events on Hobby). |
| **Product analytics (funnels, retention, session replay, feature flags)** | **Defer PostHog** until marketing site has real user volume needing funnel/retention analysis. Re-evaluate at 10k+ MAU or when activating A/B tests. PostHog free tier is generous (1M events/mo) but adds ~20–40 KB SDK, cookie/consent burden, and operational surface area premature for an MVP marketing site on Vercel free tier. |
| **Out-of-scope kill** | Do NOT run PostHog self-hosted on Vercel — it wants a real backend (Postgres + ClickHouse + Redis + Kafka). Self-host makes sense only on dedicated infra (fly.io / Railway / Coolify), not Vercel Functions. |

**Rationale in 60 seconds:**

1. Marketing site's MVP job is *brand awareness + community* driving traffic to docs/GitHub/newsletter — not product instrumentation. Plausible answers "where did traffic come from, which CTA converted?" with zero privacy debt.
2. Vercel Analytics is free and requires no vendor relationship; leave it on for Core Web Vitals visibility. It does not support custom events on free tiers, so it cannot replace Plausible for the 6-event schema.
3. PostHog is the right answer for an *app* (dashboard at `src/ai_company/dashboard/app.py`) if/when LightSpeed ships authenticated product usage — not for a static Astro marketing site. Adding it now violates YAGNI and the "lean = Astro+Tailwind+MDX" prior decision. The migration path is trivial: `posthog-js` via Astro island, same event names.

**If budget is $0 and strict:**
- Drop Plausible, run **Vercel Analytics free + Pagefind (no cost) + manual UTM tracking**. You lose custom event granularity until you re-add Plausible/PostHog. Acceptable only for pre-launch.

---

## 2. Comparison Table

### 2.1 Pricing & Limits (verified Aug 2026)

| Dimension | **Plausible Cloud** | **PostHog Cloud** | **Vercel Analytics** |
|-----------|---------------------|--------------------|----------------------|
| **Entry price** | **$9/mo** (10k pageviews), €9/mo EU billing — 10k, then $19/mo 100k, $29/mo 200k. Unlimited team members. | **$0/mo free tier**: 1M product-analytics events + 5K session replays + 1M feature-flag requests / mo. Then usage-based ($0.00005/event). No per-seat fees. | **Free tier**: 2,500 tracked data points. Pro includes analytics at $20/mo team seat (Hobby: limited). |
| **Free tier usable?** | No free hosted tier. Community Edition self-host is free (Elixir + Postgres + ClickHouse — non-trivial). | Yes — 1M events is months of marketing-site traffic at MVP scale. | Yes — but 2,500 is ~days of traffic; best as vitals supplement, not analytics source. |
| **Self-host cost** | Free (CE) but own infra. | Free self-host (OSS) — but needs Postgres+ClickHouse+Redis+Kafka; $5–20/mo infra minimum. Not Vercel-native. | Not self-hostable. |
| **Overage model** | Flat tiers, predictable. | Linear per-event; very cheap at scale ($0.000009/event at 250M). | Seat + usage bundle; opaque if not on Pro. |
| **Team / seats** | Unlimited. | Unlimited. | Vercel team seat model. |

### 2.2 Capability Matrix

| Capability | Plausible | PostHog | Vercel |
|------------|:---------:|:-------:|:------:|
| Pageviews + referrers | ✅ | ✅ | ✅ |
| Custom events + props | ✅ (requires `plausible.js` with `plausible()` custom events; Growth plan for props) | ✅ rich | ❌ (only via paid Web Analytics custom events; Hobby = no) |
| Funnels / retention / cohorts | ❌ | ✅ | ❌ |
| Session replay | ❌ | ✅ | ❌ |
| Feature flags / A/B | ❌ | ✅ | ❌ |
| Web Vitals (LCP/CLS/INP) | Basic | Capture via autocapture | ✅ native Speed Insights |
| Privacy / GDPR | ✅ cookie-less, EU host, no banner | ⚠️ needs consent if replay/ID on; can be cookie-less for anon pageviews but replay forces banner | ✅ privacy-friendly, cookieless |
| Script weight | **~1.2 KB** (gz) | **~30–80 KB** (posthog-js) | **~1 KB** (injected by Vercel) |
| Astro interop | `<script defer data-domain>` | `posthog-js` island + `astro:page-load` | `<Analytics/>` component |
| Sitemap awareness | n/a | n/a | n/a |

### 2.3 Ops & DX

| Dimension | Plausible | PostHog | Vercel |
|-----------|-----------|---------|--------|
| Vercel deploy friction | Zero — script tag | Low — env `PUBLIC_POSTHOG_KEY`, autocapture | Zero — toggle in dashboard |
| Self-host on Vercel? | Possible via proxy (`/js/script.js`) for ad-blocker bypass | No — requires long-running services | n/a |
| Data residency | EU (Germany) or US | US or EU (PostHog EU cloud) | Vercel infra |
| DPA / subprocessors | Yes | Yes | Yes |
| Lock-in | Low — export CSV, API | Medium — event schema owned | High — Vercel-only |

### 2.4 When to pick which

- **Need only marketing numbers + privacy + fixed cost → Plausible.**
- **Need product funnels + replay + flags for a real app → PostHog** (use alongside Plausible; they complement).
- **On Vercel Pro and want zero-vendor vitals → Vercel Analytics** (always on, but not sufficient alone).

---

## 3. Recommendation — Adoption Phases

**Phase 0 (MVP, week 1–2):**
- Plausible Cloud $9/mo + Vercel Analytics (free toggle) + `@astrojs/sitemap` + `robots.txt` + static OG fallback.
- Instrument 6 events via `window.plausible()` (see §4).
- Add `vercel.json` security/SEO headers (§5) + OG edge route (§6).

**Phase 1 (post-MVP, when traffic >10k/mo or blog/docs live):**
- Apply to **Algolia DocSearch** (§7); until approved, ship **Pagefind** fallback (static, no API key, ~5 min build step).
- Add `@vercel/og` dynamic OG per content type (blog/case-study/platform page) — one route parametrized.

**Phase 2 (when product dashboard gains users + needs funnel analysis):**
- Add PostHog: `posthog-js` via `src/components/analytics/PostHog.astro` island, proxy via `api/posthog` to avoid ad-blockers, reuse same 6-event names + add `session_replay` opt-in behind consent.

Do not self-host PostHog on Vercel Functions — if self-host is ever required for data sovereignty, target a persistent host (Hetzner/Fly/Railway) and keep marketing site on Vercel.

---

## 4. Event Schema — 6 Required Events

### 4.1 Conventions

- **Transport:** Plausible custom events via `plausible(event, { props: {...} })` (also compatible with PostHog `posthog.capture()` — same names). Wrap in a tiny helper so provider swap is one file.
- **Naming:** `snake_case` as ticket specifies (`hero_cta_click` …). Plausible normalizes to same.
- **Props:** Lowercase keys, string/number/boolean values only (Plausible custom props are strings). Never send PII (email, name) as prop — only as hashed or as conversion marker.
- **Privacy:** No cookies set; no `user_id` for Plausible. If PostHog is added later, gate `identify()` behind consent.
- **Validation:** Helper validates enum + truncates strings to 120 chars; drops unknown props.

### 4.2 Helper (Astro island / client script)

`src/components/analytics/events.ts`:

```ts
// Thin wrapper so Plausible ↔ PostHog swap is one file change.
type EventName =
  | "hero_cta_click"
  | "workflow_step_view"
  | "demo_requested"
  | "newsletter_subscribed"
  | "github_star_clicked"
  | "docs_viewed";

declare global {
  interface Window {
    plausible?: (event: EventName, opts?: { props?: Record<string, string | number | boolean> }) => void;
    posthog?: { capture: (e: string, p?: Record<string, unknown>) => void };
  }
}

export function track(event: EventName, props: Record<string, string | number | boolean> = {}) {
  // truncate + sanitize
  const clean: Record<string, string> = {};
  for (const [k, v] of Object.entries(props)) {
    clean[k] = String(v).slice(0, 120);
  }
  try { window.plausible?.(event, { props: clean }); } catch {}
  try { window.posthog?.capture(event, clean); } catch {}
  if (import.meta.env.DEV) console.debug("[analytics]", event, clean);
}
```

Usage: `track("hero_cta_click", { cta_id: "primary", location: "hero", variant: "A" })`

### 4.3 JSON Schema (canonical — validate at build + at runtime)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://lightspeedholdings.com/schemas/analytics-events.json",
  "title": "LightSpeed Marketing Site — Analytics Event Schema",
  "description": "6-event schema for Plausible (primary) + PostHog (future). All events cookie-less; no PII in props.",
  "type": "object",
  "required": ["event", "timestamp", "props"],
  "properties": {
    "event": {
      "type": "string",
      "enum": [
        "hero_cta_click",
        "workflow_step_view",
        "demo_requested",
        "newsletter_subscribed",
        "github_star_clicked",
        "docs_viewed"
      ]
    },
    "timestamp": { "type": "string", "format": "date-time" },
    "props": { "type": "object" }
  },
  "allOf": [
    {
      "if": { "properties": { "event": { "const": "hero_cta_click" } } },
      "then": {
        "properties": {
          "props": {
            "type": "object",
            "required": ["cta_id", "location"],
            "properties": {
              "cta_id": { "type": "string", "description": "Identifier of the CTA (e.g. primary, secondary, nav_get_started)" },
              "location": { "type": "string", "enum": ["hero", "nav", "footer", "workflow", "pricing", "docs"] },
              "variant": { "type": "string", "description": "A/B variant label if test active" },
              "destination": { "type": "string", "description": "Href target, e.g. /platform, https://github.com/..." }
            },
            "additionalProperties": false
          }
        }
      }
    },
    {
      "if": { "properties": { "event": { "const": "workflow_step_view" } } },
      "then": {
        "properties": {
          "props": {
            "type": "object",
            "required": ["step"],
            "properties": {
              "step": { "type": "integer", "minimum": 1, "maximum": 3, "description": "Workflow step 1..3" },
              "step_id": { "type": "string", "description": "Slug: e.g. build_team, run_workflow, monitor" },
              "interaction": { "type": "string", "enum": ["scroll", "click", "auto"] }
            },
            "additionalProperties": false
          }
        }
      }
    },
    {
      "if": { "properties": { "event": { "const": "demo_requested" } } },
      "then": {
        "properties": {
          "props": {
            "type": "object",
            "required": ["source"],
            "properties": {
              "source": { "type": "string", "enum": ["hero", "platform", "pricing", "footer", "nav"] },
              "form_id": { "type": "string" },
              "cta_id": { "type": "string" }
            },
            "additionalProperties": false
          }
        }
      }
    },
    {
      "if": { "properties": { "event": { "const": "newsletter_subscribed" } } },
      "then": {
        "properties": {
          "props": {
            "type": "object",
            "required": ["source"],
            "properties": {
              "source": { "type": "string", "enum": ["footer", "hero", "blog", "docs"] },
              "provider": { "type": "string", "enum": ["resend", "airtable", "convertkit"] }
            },
            "additionalProperties": false
          }
        }
      }
    },
    {
      "if": { "properties": { "event": { "const": "github_star_clicked" } } },
      "then": {
        "properties": {
          "props": {
            "type": "object",
            "required": ["location"],
            "properties": {
              "location": { "type": "string", "enum": ["hero", "nav", "footer", "docs", "platform"] },
              "repo": { "type": "string", "description": "owner/repo, e.g. jmlusu/light-speed-holdings" }
            },
            "additionalProperties": false
          }
        }
      }
    },
    {
      "if": { "properties": { "event": { "const": "docs_viewed" } } },
      "then": {
        "properties": {
          "props": {
            "type": "object",
            "required": ["path"],
            "properties": {
              "path": { "type": "string", "description": "Docs path viewed, e.g. /docs/quickstart" },
              "source": { "type": "string", "enum": ["nav", "hero", "cta", "search", "direct"] },
              "query": { "type": "string", "description": "Search query if source=search" }
            },
            "additionalProperties": false
          }
        }
      }
    }
  ]
}
```

### 4.4 Example Payloads (one per event)

```json
{ "event": "hero_cta_click", "timestamp": "2026-08-27T12:00:00Z", "props": { "cta_id": "primary", "location": "hero", "destination": "/platform" } }
{ "event": "workflow_step_view", "timestamp": "2026-08-27T12:00:01Z", "props": { "step": 2, "step_id": "run_workflow", "interaction": "scroll" } }
{ "event": "demo_requested", "timestamp": "2026-08-27T12:00:02Z", "props": { "source": "hero", "form_id": "contact-demo" } }
{ "event": "newsletter_subscribed", "timestamp": "2026-08-27T12:00:03Z", "props": { "source": "footer", "provider": "resend" } }
{ "event": "github_star_clicked", "timestamp": "2026-08-27T12:00:04Z", "props": { "location": "hero", "repo": "jmlusu/light-speed-holdings" } }
{ "event": "docs_viewed", "timestamp": "2026-08-27T12:00:05Z", "props": { "path": "/docs/quickstart", "source": "nav" } }
```

### 4.5 Plausible Dashboard Notes

- Mark `demo_requested` + `newsletter_subscribed` as **Conversions / Goals** in Plausible dashboard (Goals → Custom Events). Needed for funnel "hero view → CTA click → demo requested".
- Custom props require enabling on your Plausible site settings (Growth+ enables props filtering). Without it, props are stored but not filterable.
- PostHog migration: same event names map 1:1 to PostHog funnels/trends; add `$current_url` + `$referrer` auto-props if switching.

---

## 5. SEO — Sitemap / Robots / Meta + `vercel.json` Headers Snippet

### 5.1 Sitemap (Astro-native)

**Library:** `@astrojs/sitemap` v3.7.x (official, zero-config beyond `site`).

```js
// astro.config.mjs
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import tailwind from "@astrojs/tailwind";

export default defineConfig({
  site: "https://lightspeedholdings.com", // REQUIRED — no sitemap emitted without it
  trailingSlash: "never",
  integrations: [
    sitemap({
      filter: (page) =>
        !page.includes("/drafts/") &&
        !page.includes("/admin/") &&
        !page.endsWith("/404/"),
      serialize(item) {
        // Tweak priorities — homepage highest
        if (item.url === "https://lightspeedholdings.com/") item.priority = 1.0;
        else if (item.url.includes("/platform")) item.priority = 0.9;
        else if (item.url.includes("/docs")) item.priority = 0.7;
        else item.priority = 0.5;
        item.changefreq = "weekly";
        item.lastmod = new Date().toISOString();
        return item;
      },
    }),
    tailwind(),
  ],
});
```

Output: `dist/sitemap-index.xml` + `dist/sitemap-0.xml` (index references chunk). Submit `sitemap-index.xml` once in Google Search Console — no ping needed (Google deprecated `https://www.google.com/ping?sitemap=` in Jun 2023 → 404).

**Try / verify locally:**
```bash
npx astro add sitemap
npm run build && ls dist/sitemap*
cat dist/sitemap-index.xml
```

### 5.2 `robots.txt`

Prefer **static** `public/robots.txt` (simpler than dynamic `src/pages/robots.txt.ts` for Vercel static output).

```txt
# public/robots.txt
User-agent: *
Allow: /

# Block draft / internal routes if they ever exist
Disallow: /drafts/
Disallow: /preview/
Disallow: /admin/

# Allow OG image generation to be crawled (Vercel docs recommendation)
Allow: /api/og/*

# Sitemap — keep in sync with site URL
Sitemap: https://lightspeedholdings.com/sitemap-index.xml
```

If site URL must be env-driven, use dynamic alternative `src/pages/robots.txt.ts` reading `site` from `Astro.site`.

### 5.3 Meta / Social Tags (Astro layout)

Add via `src/layouts/Base.astro` head (or `astro:head` if using Astro 4 `Head` API). Every page sets `title`, `description`, `canonical`, `og:*`, `twitter:*`, and `json-ld` where relevant.

```astro
---
interface Props { title: string; description: string; path: string; ogImage?: string; noindex?: boolean }
const { title, description, path, ogImage, noindex } = Astro.props;
const canonical = new URL(path, Astro.site).href;
const og = ogImage ?? new URL(`/api/og?title=${encodeURIComponent(title)}`, Astro.site).href;
---
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title} — LightSpeed Holdings</title>
<meta name="description" content={description} />
<link rel="canonical" href={canonical} />
{noindex && <meta name="robots" content="noindex, nofollow" />}

<!-- Open Graph -->
<meta property="og:type" content="website" />
<meta property="og:site_name" content="LightSpeed Holdings" />
<meta property="og:title" content={title} />
<meta property="og:description" content={description} />
<meta property="og:url" content={canonical} />
<meta property="og:image" content={og} />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content={title} />
<meta name="twitter:description" content={description} />
<meta name="twitter:image" content={og} />

<!-- Favicon / theme -->
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<meta name="theme-color" content="#0a0a0a" />
```

**Per-page frontmatter** (`src/pages/*.mdx`): `title`, `description` (120–160 chars), `ogTitle` override optional. Validate in build — warn if description missing or >160 chars.

### 5.4 `vercel.json` — Headers Snippet (canonical for marketing-site/)

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-XSS-Protection", "value": "0" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" },
        { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload" }
      ]
    },
    {
      "source": "/(.*).html",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" }
      ]
    },
    {
      "source": "/_astro/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    },
    {
      "source": "/api/og/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, immutable, no-transform, max-age=86400, stale-while-revalidate=604800" },
        { "key": "Access-Control-Allow-Origin", "value": "*" }
      ]
    },
    {
      "source": "/sitemap-index.xml",
      "headers": [
        { "key": "Content-Type", "value": "application/xml" },
        { "key": "Cache-Control", "value": "public, max-age=3600, stale-while-revalidate=86400" }
      ]
    },
    {
      "source": "/robots.txt",
      "headers": [
        { "key": "Content-Type", "value": "text/plain" },
        { "key": "Cache-Control", "value": "public, max-age=3600, stale-while-revalidate=86400" }
      ]
    }
  ],
  "redirects": [
    { "source": "/docs", "destination": "/docs/quickstart", "permanent": false }
  ],
  "rewrites": [
    { "source": "/js/script.js", "destination": "https://plausible.io/js/script.js" },
    { "source": "/api/event", "destination": "https://plausible.io/api/event" }
  ],
  "cleanUrls": true,
  "trailingSlash": false
}
```

**Plausible proxy rewrite** (`/js/script.js` → `plausible.io`) is the ad-blocker bypass (recommended by Plausible docs). Requires adding `data-api="/api/event"` to script tag: `<script defer data-domain="lightspeedholdings.com" data-api="/api/event" src="/js/script.js">`. Keep `rewrites` destination host explicit; CSP `connect-src` must allow `plausible.io` if not proxying.

**Security note:** CSP for marketing site should be added once Astro layout is locked — start with `default-src 'self'` + `script-src 'self' plausible.io` + `img-src 'self' data: https:` + `style-src 'self' 'unsafe-inline'` (Tailwind). Do not copy dashboard CSP wholesale — marketing site has no WS.

---

## 6. Dynamic OG via `@vercel/og` — Edge Function Outline

### 6.1 Decision

- **Library:** `@vercel/og` (wraps Satori → SVG → PNG via Resvg). Ships with Vercel templates; ~10–50 ms CPU, edge-cached via `Cache-Control`.
- **Runtime:** **Edge** (`export const config = { runtime: 'edge' }` for Pages Router, or `export const runtime = 'edge'` for App Router). Works on both Node and Edge but Edge has zero cold-start — critical for crawler fetch (Slack/Twitter hit once, must return <1s).
- **Size:** 1200×630 (OG standard). Supports any JSX/CSS subset: Flexbox only — no Grid, no CSS vars, no `overflow:hidden` (partial), fonts must be fetched as `ArrayBuffer`.
- **Vercel free tier:** OG runs count as Function invocations; cache headers make repeat views CDN-only (negligible cost).

### 6.2 Routes (one parametrized API)

For Astro on Vercel, OG endpoints are **Vercel Functions**, not Astro pages. Two integration options:

| Astro adapter mode | OG location | Notes |
|--------------------|-------------|-------|
| `output: 'static'` + Vercel adapter | `api/og.tsx` (Next-style) or `src/pages/api/og.ts` (Astro API route with `export const prerender = false`) | Simpler: use `src/pages/api/og.ts` with edge runtime via `vercel.json` `functions` config |
| `output: 'server'` / hybrid | `src/pages/api/og.ts` as server route | Same shape; caching still via `ImageResponse` headers |

Recommended for marketing-site (static + islands): **`src/pages/api/og.ts`** as a serverless/edge route (`prerender = false`), single entry with `?title=&desc=&type=` params — covers marketing pages without a DB.

### 6.3 Outline — `src/pages/api/og.ts` (Astro + @vercel/og edge)

```ts
// src/pages/api/og.ts
export const prerender = false;

// Choose one: Node vs Edge. Edge = faster, but fetch fonts differently.
// For Vercel, set via vercel.json or adapter config.
// If using @vercel/og on Astro, prefer Node runtime (simpler font fetch).
// Set `export const config = { runtime: 'edge' }` via vercel.json functions mapping below if Edge desired.

import { ImageResponse } from "@vercel/og";

const BRAND = {
  bg: "#0a0a0a",
  fg: "#fafafa",
  accent: "#22c55e", // green — replace with LightSpeed token after T1
  muted: "#a1a1aa",
};

// Cache fonts at module scope (reuse across warm invocations)
let geistBold: ArrayBuffer | null = null;
async function getFonts() {
  if (!geistBold) {
    // Use CDN TTF — must be ArrayBuffer, not CSS URL
    geistBold = await fetch("https://cdn.jsdelivr.net/fontsource/fonts/geist:vf@latest/files/geist-latin-700-normal.woff").then(r => r.arrayBuffer());
  }
  return geistBold;
}

export async function GET({ url }: { url: URL }) {
  const title = (url.searchParams.get("title") ?? "LightSpeed Holdings").slice(0, 100);
  const desc = (url.searchParams.get("desc") ?? "Build and orchestrate AI agent hierarchies.").slice(0, 160);
  const type = url.searchParams.get("type") ?? "page"; // page | docs | blog | platform

  const fontData = await getFonts();

  const typeBadge: Record<string, string> = {
    page: "LightSpeed",
    docs: "Documentation",
    blog: "Blog",
    platform: "Platform",
    changelog: "Changelog",
  };

  return new ImageResponse(
    (
      {
        // JSX-like via React.createElement equivalent — @vercel/og supports JSX in .tsx files.
        // Below is the shape; file MUST be .tsx if using JSX syntax.
      } as any
    ),
    {
      width: 1200,
      height: 630,
      fonts: [{ name: "Geist", data: fontData, weight: 700, style: "normal" }],
      headers: {
        "Cache-Control": "public, immutable, no-transform, max-age=86400, stale-while-revalidate=604800",
      },
    }
  );
}

// ---- Actual JSX body (use .tsx) ----
/*
<div style={{
  width: "100%", height: "100%", display: "flex", flexDirection: "column",
  backgroundColor: BRAND.bg, color: BRAND.fg, padding: 48, fontFamily: "Geist"
}}>
  <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
    <div style={{ width: 40, height: 40, borderRadius: 8, background: BRAND.accent, display: "flex", alignItems: "center", justifyContent: "center", color: "#000", fontSize: 18, fontWeight: 700 }}>LS</div>
    <span style={{ fontSize: 18, color: BRAND.muted }}>{typeBadge[type] ?? type}</span>
  </div>
  <div style={{ display: "flex", flexDirection: "column", marginTop: 32 }}>
    <div style={{ fontSize: title.length > 60 ? 40 : 52, fontWeight: 700, lineHeight: 1.15 }}>{title}</div>
    <div style={{ fontSize: 20, color: BRAND.muted, marginTop: 16, lineHeight: 1.4 }}>{desc}</div>
  </div>
  <div style={{ display: "flex", justifyContent: "space-between", marginTop: "auto", borderTop: `1px solid #27272a`, paddingTop: 16 }}>
    <span style={{ fontSize: 14, color: BRAND.muted }}>lightspeedholdings.com</span>
    <span style={{ fontSize: 14, color: BRAND.muted }}>AI Company Builder</span>
  </div>
</div>
*/
```

**Vercel function config** (if Edge preferred):

```json
// vercel.json — add to top-level
{
  "functions": {
    "src/pages/api/og.ts": { "runtime": "edge" }
  }
}
```

**Astro wiring notes:**
- File must be `.ts` (Astro API route) returning `new Response`. `@vercel/og`'s `ImageResponse` *is* a `Response` — return it directly.
- If Astro's Vite JSX complains, rename to `og.tsx` or add `jsx: "react-jsx"` in `tsconfig.json` for that route only.
- For static output, `export const prerender = false` makes Vercel deploy it as a Function, not a prerendered file.

**Per-page usage** (after T1 tokens locked):

```astro
---
const ogUrl = new URL(`/api/og?title=${encodeURIComponent(title)}&desc=${encodeURIComponent(description)}&type=docs`, Astro.site).href;
---
<meta property="og:image" content={ogUrl} />
<meta name="twitter:image" content={ogUrl} />
```

**Fallback static image:** Ship `public/og-default.png` (1200×630) for pages without dynamic OG. `Base.astro` uses `ogImage ?? "/og-default.png"`.

**Constraints (Satori):** Flexbox only; no Grid, no `var(--token)`, no external `<img>` without absolute URL, no web-font CSS import (fetch TTF). Test with `?title=Hello` after deploy; use `?debug=true` pattern to dump layout if text overflows.

**Local dev:** `@vercel/og` requires Node 18+. Add `pnpm add @vercel/og` + `npm run dev` — route at `http://localhost:4321/api/og?title=Test`.

---

## 7. Search — Algolia DocSearch + Fallback (Pagefind / FlexSearch)

### 7.1 Algolia DocSearch Eligibility & Application

**What DocSearch is:** Free Algolia Crawler + hosted Algolia index + frontend package (`@docsearch/js` / `@docsearch/react`) that Algolia operates for eligible sites. You keep "Search by Algolia" attribution; they handle crawling/reindexing.

**Eligibility (per [who-can-apply](https://docsearch.algolia.com/docs/who-can-apply/)):**

| Requirement | LightSpeed status |
|-------------|-------------------|
| **Public technical documentation or technical blog** | ✅ Pass — AI Company Builder docs + changelog + technical blog are the indexable surface. |
| **Open source** OR technical content on production site | ✅ Open-source repo `jmlusu/light-speed-holdings` + docs satisfy; marketing pages are not crawled (only docs). |
| **No non-technical marketing crawl** — free crawler indexes only docs/blog | ⚠️ Configure crawler `startUrls` to `/docs/*`, `/changelog/*`, `/blog/*` — exclude `/`, `/platform`, `/pricing`. |
| **Search-by-Algolia logo kept** | ✅ Acceptable. |
| **Domain ownership verified within 7 days** | Owner must add DNS TXT or meta tag after approval. |
| **Production-ready site (not behind auth, not “coming soon”)** | ⚠️ Apply only after marketing-site MVP is live on `lightspeedholdings.com` with real docs pages (≥10 pages). Don't apply with localhost preview. |
| **Non-technical content rejected** | Risk if application is for homepage marketing copy — scope to docs. |

**Typical rejection reasons:** not production, non-technical landing page, gated/private repo, application before crawlable content exists. **Manual review 1–2 business days** if auto-check cannot verify.

**Application steps (dashboard flow as of Aug 2026):**

1. **Pre-check:** Ensure live site at `https://lightspeedholdings.com` with `/docs/*` populated (≥5 MDX pages, real content, not Lorem). Link to GitHub repo from docs footer.
2. **Apply:** Go to [docsearch.algolia.com/apply](https://docsearch.algolia.com/apply) (redirects to Algolia dashboard onboarding). Sign in / create free Algolia account.
3. **Submit domain:** Enter `lightspeedholdings.com` → automated validation runs (checks for docs-like content, public access, sitemap).
4. **If auto-eligible:** Dashboard prompts to **create crawler**. Choose config — start with `Default` crawler config (selectors for `h1/h2/h3 + p + code`). Set `schedule: weekly` or `on-demand`.
5. **If manual review:** Wait 1–2 days. Keep site live. Watch email.
6. **After approval:** In dashboard, **edit crawler** → confirm `startUrls: ["https://lightspeedholdings.com/docs"]`, `sitemapUrls: ["https://lightspeedholdings.com/sitemap-index.xml"]`. Trigger **Initial crawl** → monitor log for errors (selectors mismatched → fix `recordProps`).
7. **Verify ownership:** Add the TXT record shown in dashboard within 7 days (`algolia-site-verification=...`).
8. **Frontend integration:** Install one of:
   - `@docsearch/js` (vanilla) for Astro: `npm i @docsearch/js` + add `src/components/Search.astro` with `<DocSearch appId indexName apiKey>`.
   - `@astrojs/starlight` has built-in DocSearch integration if docs adopt Starlight template.
   - Existing Astro integration listed in [DocSearch packages](https://docsearch.algolia.com/docs/docsearch-library/) — use `v5` (Autocomplete-based).
9. **Keep attribution:** Ensure `<a href="https://www.algolia.com">Search by Algolia</a>` visible near input (added automatically by package; do not hide).
10. **Ongoing:** Re-crawl on schedule; trigger manual **Reindex** after each docs deploy (optional webhook: Algolia Crawler API `POST /1/crawlers/{id}/reindex` with `ALGOLIA_CRAWLER_API_KEY` in CI).

**If eligible but want to self-manage without free program:**
- Create own Algolia app → use free plan (10k records, sufficient for MVP docs) → run legacy DocSearch crawler yourself or push records via `@algolia/client-search` at build.

### 7.2 Fallback — **Pagefind** (recommended) vs FlexSearch

**Recommendation:** **Pagefind** for the Astro static site. Zero service dependency, no API key, builds a search index at `npm run build` time, ships a tiny WASM indexer.

| Dimension | **Pagefind** (recommended fallback) | FlexSearch | Algolia DocSearch fallback |
|-----------|-------------------------------------|------------|----------------------------|
| Install | `npm i pagefind` (build-time) | `npm i flexsearch` + manual index | Same Algolia client but own app |
| Index source | Post-build crawl of `dist/` HTML — no manual indexing code | Manual: index MDX at build via script | Push JSON to Algolia at build |
| Runtime cost | Static files under `/_pagefind/` + ~15 KB WASM | ~6 KB flexsearch client | Network to Algolia, needs API key |
| Works offline / Vercel free | ✅ Yes — purely static | ✅ Yes | ⚠️ Needs Algolia quota |
| Astro interop | Official `@pagefind` UI or `pagefind-search` component; many Astro recipes | Manual | DocSearch JS if you have credentials |
| Search quality | Good TF-IDF + filters, excerpt + ranking; no typo tolerance as strong as Algolia | Configurable tokenization, but no hosted ranking | Algolia ranking is strongest |
| Maintenance | None — rebuild regenerates | Maintain index JSON + code | Maintain Algolia index + quota |
| When to use | **Default until DocSearch approved** — ships first deploy, remove after approval | If you want zero-WASM and full control | If DocSearch approved but want ownership |

**Pagefind integration (Astro):**

```bash
# install
npm i -D pagefind
```

```json
// package.json
{
  "scripts": {
    "build": "astro build && pagefind --site dist",
    "dev": "astro dev"
  }
}
```

```astro
<!-- src/components/SearchFallback.astro -->
<div id="search" data-pagefind-ui />
<script>
  import { PagefindUI } from "@pagefind/default-ui";
  new PagefindUI({ element: "#search", showSubResults: true });
</script>
<link href="/_pagefind/pagefind-ui.css" rel="stylesheet" />
```

Alternative without UI lib: `import * as pagefind from "/_pagefind/pagefind.js"; pagefind.init()` + custom `<input>` + `pagefind.search(query)` — ~30 lines, documented at [pagefind.app](https://pagefind.app/).

**`dist` note:** Pagefind reads `dist/` — requires `site` set in `astro.config.mjs` (same as sitemap). Exclude `pagefind` from crawl filters if needed.

**Migration path:** When DocSearch approved, keep Pagefind behind a feature flag / env check (`PUBLIC_SEARCH_PROVIDER=algolia|pagefind`) so a bad DocSearch deploy can be reverted by flipping env without a code change.

---

## 8. Privacy / GDPR Posture (Cookie-less)

### 8.1 Plausible posture

- **No cookies** set. Uses `plausible.io` anonymized, aggregated pageviews; IPs not stored; no cross-site tracking. **No consent banner required** under GDPR (Plausible markets this as DPA-ready).
- Hosted on **EU (Germany) infra** option — choose `plausible.io` EU endpoint or self-host CE if residency is strict.
- Data processing agreement available via Plausible account → Settings → DPA.

### 8.2 Vercel Analytics posture

- Cookie-less, anonymized, GDPR-friendly. No banner.

### 8.3 PostHog posture (if added Phase 2)

- Default `posthog-js` sets a cookie (`ph_*`) and captures IPs → **requires consent banner** if used with `identify()` or session replay.
- Two paths:
  - **Cookie-less anon mode:** `posthog.init(key, { persistence: 'memory', opt_out_capturing_by_default: true })` + only `capture()` anon events until consent granted (see PostHog "cookieless tracking" docs). Retains Plausible-like GDPR posture but loses replay/flags until consent.
  - **Full tracking:** Show a lightweight consent banner (Turnstile is anti-bot only — not consent; add `vanilla-cookieconsent` or `osano`-style banner) gating `posthog.opt_in_capturing()`.

**Decision for MVP:** No banner needed — Plausible + Vercel are cookie-less. Add banner only when PostHog replay/identify is activated.

### 8.4 Implementation checklist (MVP)

- [ ] Plausible script with `data-domain="lightspeedholdings.com"` + `data-api="/api/event"` if proxying.
- [ ] No `localStorage`/`cookie` writes from analytics helper.
- [ ] No PII in `track()` props (enforced by schema `additionalProperties: false` + review).
- [ ] `vercel.json` headers include `Permissions-Policy` minimal surface.
- [ ] Privacy page (`/privacy`) documents Plausible as sub-processor (template from Plausible docs).

---

## 9. Repo Findings — Existing Analytics / Sitemap State

Grep for `analytics|plausible|posthog|sitemap|vercel` across repo (2026-08-27):

- **No marketing-site directory** (`marketing-site/` does not exist yet) — expected before T2 stack lock. No existing `astro.config.*`, `vercel.json`, `robots.txt`, or `sitemap` code.
- `package.json` is the milestones-deck generator (`pptxgenjs`) — unrelated.
- Analytics references are internal (`dashboard/analytics.py` — KPI history, not web analytics; `company/agent-registry.json` — Business Intelligence Engineer).
- `graphify-out/`, `.agents/`, `.opencode/` contain no marketing analytics.
- **No existing Plausible/PostHog/Vercel snippet** — greenfield. No migration needed.

** implication:** This research defines the initial integration — no legacy to unwind. T2/T8 should scaffold `marketing-site/` as a separate Astro project (own `package.json`, `astro.config.mjs`, `vercel.json`) and not intermix with Python CLI `src/`.

---

## 10. Open Questions / Risks

| # | Question | Owner | Mitigation |
|---|----------|-------|------------|
| 1 | Plausible $9/mo vs Astro/Vercel free-only constraint — is $9/mo allowed? Map notes say "Vercel free tier (out-of-scope: paid hosting tiers)" but Plausible is SaaS analytics, not hosting. | #157 / T7 approver | If $0 hard constraint, fall back to Vercel free + Pagefind. Recommend approving $9/mo as infra exception (fixed, predictable, GDPR-clean). |
| 2 | Custom domain final (`lightspeedholdings.com` assumed) — affects `site`, sitemap, og canonical, Plausible `data-domain`. | T2 | Use env `SITE_URL` in `astro.config.mjs` (`site: process.env.SITE_URL ?? "https://lightspeedholdings.com"`) so DNS choice is one var. |
| 3 | DocSearch: will Algolia approve a *new* site with thin docs content? Risk of rejection if docs <10 pages at application time. | T3 / docs IA | Apply only after T3 docs IA + at least 8 pages live; ship Pagefind meanwhile (zero risk). |
| 4 | `@vercel/og` on Astro static output — runtime config via `vercel.json` functions vs adapter `edgeMiddleware`. Needs a real Vercel deploy to validate Satori rendering (no Grid). | T8 | T8 deploy ticket should include a preview deploy + Slack/Twitter card tester check. |

---

## 11. Recommended Next Steps (for T2/T8 executors)

1. **T2 (Stack Lock):** Scaffold `marketing-site/` as `npm create astro@latest -- --template basics --no-git` + `npx astro add tailwind sitemap` + copy `vercel.json` headers from §5.4 and `robots.txt` from §5.2. Register `Plausible` domain before first deploy.
2. **T8 (Deployment):** Wire `SITE_URL` env, `astro.config.mjs` `site`, sitemap, robots, `/_pagefind` exclusion, and `/api/og` route. Add a CI check `npm run build && test -f dist/sitemap-index.xml`.
3. **Search:** Ship Pagefind fallback first; open DocSearch application as soon as `/docs` is live (track in issue #164 checklist).
4. **Content:** T3 should enforce per-page `title`/`description` frontmatter + build-time validation (warn if missing).
5. **Verification gate (per map):** `npm run build` + Lighthouse >90 + a11y check on marketing-site — add `lighthouse-ci` in GitHub Actions for T8.

---

## 12. References

- Plausible pricing & privacy: https://plausible.io/#pricing, https://plausible.io/data-policy, https://plausible.io/docs/proxy/introduction
- PostHog pricing (verified Aug 2026): https://posthog.com/pricing — 1M events/mo free, usage-based above; self-host docs https://posthog.com/docs/self-host
- Vercel Analytics & Web Vitals: https://vercel.com/docs/analytics, https://vercel.com/docs/speed-insights
- `@vercel/og`: https://vercel.com/docs/og-image-generation, npm https://www.npmjs.com/package/@vercel/og (v1.0.2, MPL-2.0), Satori https://github.com/vercel/satori, CSS constraints (Flexbox only)
- Algolia DocSearch: https://docsearch.algolia.com/docs/who-can-apply/, https://docsearch.algolia.com/docs/docsearch-program/, https://docsearch.algolia.com/
- Astro sitemap: https://docs.astro.build/en/guides/integrations-guide/sitemap/, `@astrojs/sitemap` v3.7.x
- Pagefind: https://pagefind.app/
- FlexSearch: https://github.com/nextapps-de/flexsearch
- Google sitemap ping deprecation (Jun 2023): https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping
- GDPR cookie-less analytics: https://plausible.io/blog/gdpr-ccpa-p number, https://posthog.com/docs/product-analytics/cookieless-tracking (PostHog)

---

## 13. Decision Record (for #157 wayfinder map)

When this research is accepted, append to `## Decisions so far` in #157:

> **T7 (2026-08-27): Analytics/SEO/OG locked** — Plausible Cloud €9/mo (primary) + Vercel Analytics free (vitals). Event schema §4 (6 events). Sitemap via `@astrojs/sitemap` + `robots.txt` + `vercel.json` headers (§5). OG via `@vercel/og` edge route parametrized by `?title=&desc=&type=` with static fallback (§6). Search: Algolia DocSearch application post `/docs` live, **Pagefind fallback** until approved (§7). GDPR: cookie-less, no banner for MVP (§8). Research branch: `research/analytics-seo` → `research/analytics-seo/FINDINGS.md`.

---

*End of findings — branch is throwaway research; do not merge. Await `ready-for-human` → `ready-for-agent` transition to scaffold `marketing-site/`.*
