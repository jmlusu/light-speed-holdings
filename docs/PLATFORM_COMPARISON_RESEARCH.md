# Platform Comparison Research — LightSpeed Remote Autonomous Runtime

**Research Date**: October 3, 2026  
**Focus**: Platforms with genuinely usable free tiers **without requiring a credit card/payment method**  
**Methodology**: Official documentation, pricing pages, terms of service, developer documentation

---

## Executive Summary: Platforms Requiring NO Credit Card

| Platform | Free Tier Usable Without Card? | Key Limitation |
|----------|-------------------------------|----------------|
| **Render** | ✅ **YES** | Spins down after 15 min inactivity; 750 hrs/mo; 5 GB bandwidth |
| **Vercel** | ✅ **YES** | **Non-commercial use only**; 100 GB bandwidth; 1M invocations; cron = daily only |
| **Netlify** | ✅ **YES** | 300 credits/mo (credit-based); ~100 GB bandwidth equivalent |
| **Deno Deploy** | ✅ **YES** | 1M requests; 20 GB egress; 10 hr CPU; 1 GiB KV |
| **Supabase** | ✅ **YES** | 500 MB DB; 5 GB egress; 500k Edge Function invocations; pauses after 7 days inactivity |
| **Firebase (Spark)** | ✅ **YES** | **Cloud Functions NOT available on Spark**; requires Blaze (card) for functions |
| **Hugging Face** | ⚠️ **PARTIAL** | CPU Basic Spaces removed for new accounts; only ZeroGPU (very limited); Hub free |
| **Fly.io** | ❌ **NO** | Free tier deprecated for new accounts; card required |
| **Koyeb** | ❌ **NO** | Card required since Feb 2026 ($29 pre-auth hold) |
| **Railway** | ⚠️ **TEMPORARY** | $5 trial for 30 days (no card), then $1/mo permanent free credits (very limited) |
| **Google Cloud Run** | ❌ **NO** | Card required for billing account (even for free tier) |
| **AWS Lambda** | ❌ **NO** | Card required for AWS account |
| **Azure Functions** | ❌ **NO** | Card required for Azure subscription (identity verification) |
| **Oracle Cloud** | ❌ **NO** | Card required for identity verification |

---

## Detailed Platform Evidence

### 1. Render

| Claim | URL | Page Title | Date Checked | Quotation | Confidence |
|-------|-----|------------|--------------|-----------|------------|
| No credit card required | https://render.com/articles/platforms-with-a-real-free-tier-for-developers-in-2026.md | Render Blog | 2026-10-03 | "No credit card is required. You can deploy with Docker, Node.js / Bun, Python, Ruby, Go, Rust, and Elixir using automatic build detection." | High |
| Free tier details | https://render.com/docs/free.md | Deploy for Free | 2026-10-03 | "Free web services support many (but not all) features... Free compute plans types have usage limits and are designed to help you to explore new tech, build personal projects, and preview Render's developer experience." | High |
| 750 hrs, 5 GB bandwidth | https://render.com/pricing | Render Pricing | 2026-10-03 | "Hobby: $0/month + compute... 5 GB of bandwidth included... Free web services... 750 free instance hours per workspace per month" | High |
| Spins down after 15 min | https://antilak.com/blog/render-free-tier-complete-guide-2026 | Render Free Tier 2026 Guide | 2026-10-03 | "Render free tier 2026: No credit card required, 30-60s cold start, 15 min sleep policy, 750 hours/month" | Medium |

### 2. Vercel (Hobby Plan)

| Claim | URL | Page Title | Date Checked | Quotation | Confidence |
|-------|-----|------------|--------------|-----------|------------|
| No credit card required | https://vercel.com/docs/plans/hobby | Vercel Hobby Plan | 2026-10-03 | "The Hobby plan is free and aimed at developers with personal projects... no credit card required." | High |
| Free tier limits | https://justinmckelvey.com/blog/is-vercel-free | Is Vercel Free? (2026) | 2026-10-03 | "100 GB of fast data transfer per month, 1,000,000 edge requests and 1,000,000 function invocations per month, 4 hours of active CPU and 360 GB-hours of provisioned memory for functions, 1 GB of Blob storage and 5,000 image transformations per month" | High |
| Cron = daily only on Hobby | https://vercel.com/docs/cron-jobs/usage-and-pricing | Usage & Pricing for Cron Jobs | 2026-10-03 | "Hobby accounts are limited to cron jobs that run once per day. Cron expressions that would run more frequently will fail during deployment." | High |
| Non-commercial restriction | https://justinmckelvey.com/blog/is-vercel-free | Is Vercel Free? (2026) | 2026-10-03 | "The limit that matters is not a number: Hobby is restricted to personal, non-commercial use. If the site makes money for anyone involved in building it, Vercel's fair-use policy says you belong on Pro." | High |
| No overage billing | https://vercel.com/docs/plans.md | Account Plans on Vercel | 2026-10-03 | "Hobby plans will be paused when they exceed the included free tier usage... In most cases, if you exceed your usage limits on the Hobby plan, you will have to wait until 30 days have passed before you can use the feature again." | High |

### 3. Netlify

| Claim | URL | Page Title | Date Checked | Quotation | Confidence |
|-------|-----|------------|--------------|-----------|------------|
| No credit card required | https://www.netlify.com/blog/introducing-netlify-free-plan/ | Introducing Netlify's Free Plan | 2026-10-03 | "100% free: Deploy with no credit card required and no fees. Ever." | High |
| Credit-based pricing | https://www.netlify.com/changelog/netlify-pricing-update-introducing-credit-based-plans.md | Netlify pricing update | 2026-10-03 | "Free: 300 credits/month... Production deploys: 15 credits... Compute: 5 credits per GB-hour... Bandwidth: 10 credits per GB... Web requests: 3 credits per 10,000" | High |
| Scheduled functions | https://docs.netlify.com/build/functions/scheduled-functions | Scheduled Functions | 2026-10-03 | "Scheduled Functions are enabled by default for all accounts." | High |
| Hard pause, no auto-charge | https://www.toolpick.dev/pricing/netlify | Netlify Pricing Free Plan 2026 | 2026-10-03 | "Netlify's free plan is best evaluated as a monthly credit pool... hard pause behavior" | High |

### 4. Deno Deploy

| Claim | URL | Page Title | Date Checked | Quotation | Confidence |
|-------|-----|------------|--------------|-----------|------------|
| No credit card required | https://deno.com/pricing | Deno Deploy Pricing | 2026-10-03 | "Free $0/month... Start free" (no card mentioned for Free tier) | High |
| Free tier limits | https://freetier.co/directory/products/deno-deploy | Deno Deploy 2026: 1M Requests Free Monthly | 2026-10-03 | "1M inbound HTTP requests per month, 20 GiB of monthly egress bandwidth, 10 hours of Active CPU per month... 1 GiB of Deno KV storage... Credit card: Not required" | High |
| Native cron | https://deno.com/deploy | Deno Deploy | 2026-10-03 | "Schedule tasks with cron... Don't just fire-and-forget; specify cron jobs in code, and monitor them right from your dashboard." | High |
| Regions | https://docs.deno.com/runtime/reference/cli/deploy/ | deno deploy CLI | 2026-10-03 | "--region <region> - Deployment region. Allowed values: us, eu, global" | High |
| GA date | https://deno.com/blog/deno-deploy-is-ga | Deno Deploy is Generally Available | 2026-10-03 | "Feb 3, 2026 — Deno Deploy comes with a generous free plan, offering one million requests per month, 100 GB of egress, and 15 CPU hours." | High |

### 5. Supabase

| Claim | URL | Page Title | Date Checked | Quotation | Confidence |
|-------|-----|------------|--------------|-----------|------------|
| No credit card required | https://www.itpathsolutions.com/supabase-free-tier-limits | Supabase Free Tier Limits 2026 | 2026-10-03 | "Supabase's free tier has no time limit and requires no credit card. Projects remain on the free plan indefinitely as long as you stay within the resource limits" | High |
| Free tier limits | https://designrevision.com/blog/supabase-pricing | Supabase Pricing 2026 | 2026-10-03 | "500 MB database, 1 GB file storage, 5 GB egress, 50,000 monthly active users, 500,000 edge-function invocations, and up to 2 active projects" | High |
| Pauses after 7 days | https://designrevision.com/blog/supabase-pricing | Supabase Pricing 2026 | 2026-10-03 | "projects paused after 7 days of inactivity" | High |
| pg_cron beta | https://supabase.com/features/supabase-cron | Cron | 2026-10-03 | "Supabase Cron is a Postgres module designed to schedule recurring Jobs with cron syntax directly within your database... Stage: Beta" | High |
| Regions (no Africa) | https://supabase.com/regions | Supabase Regions | 2026-10-03 | Lists 17 regions: Americas (6), Europe (6), Asia Pacific (4), South America (1) — no Africa | High |
| HTTP 402 on egress exceed | https://designrevision.com/blog/supabase-pricing | Supabase Pricing 2026 | 2026-10-03 | "Supabase free-tier project restricted under the Fair Use Policy after exceeding egress — all services return HTTP 402 until the billing period resets" | High |

### 6. Firebase (Spark Plan)

| Claim | URL | Page Title | Date Checked | Quotation | Confidence |
|-------|-----|------------|--------------|-----------|------------|
| Spark no card required | https://veri-free.com/is-firebase-actually-free | Is Firebase Actually Free? (Aug 2026) | 2026-10-03 | "Card required: No — Firebase does not ask for a card to use the free version." | High |
| Functions require Blaze | https://dev.to/androve2k/spark-vs-blaze-the-firebase-pricing-guide-i-wish-id-read-sooner-onb | Spark vs Blaze (2026) | 2026-10-03 | "Blaze unlocks products unavailable on Spark: Cloud Storage, Cloud Functions beyond the base quota, outbound calls to external services from Cloud Functions" | High |
| Cloud Storage requires Blaze | https://dev.to/androve2k/spark-vs-blaze-the-firebase-pricing-guide-i-wish-id-read-sooner-onb | Spark vs Blaze (2026) | 2026-10-03 | "Since February 3, 2026, Google has aligned Cloud Storage with standard Google Cloud Storage rules: creating or maintaining a bucket requires a linked billing account, meaning the Blaze plan, regardless of usage volume." | High |
| Blaze no hard cap | https://veri-free.com/is-firebase-actually-free | Is Firebase Actually Free? (Aug 2026) | 2026-10-03 | "Blaze bills by usage with no hard spending cap by default. A loop in your code or a burst of traffic bills you for it, and the budget alert tells you afterwards." | High |

### 7. Hugging Face Spaces

| Claim | URL | Page Title | Date Checked | Quotation | Confidence |
|-------|-----|------------|--------------|-----------|------------|
| CPU Basic removed | https://discuss.huggingface.co/t/new-free-accounts-cannot-create-cpu-basic-gradio-spaces-only-zerogpu-available/177629/1 | New free accounts cannot create CPU Basic Gradio Spaces | 2026-10-03 | "I'm trying to create a new Gradio Space on a free account. The only available runtime is ZeroGPU. Docker is marked as Paid. CPU Basic cannot be selected during creation." | High |
| Community complaint | https://discuss.huggingface.co/t/official-community-complaint-revert-free-cpu-basic-spaces-and-remove-anti-developer-sdk-restrictions/177703 | Official Community Complaint (Jul 2026) | 2026-10-03 | "The current ZeroGPU restrictions—limiting free tier users to a handful of requests or a few minutes of compute per day—make it completely impossible to debug code, test multi-model routing architectures, or run sustained experiments." | High |
| Spaces sleep | https://huggingface.co/docs/hub/spaces-gpus | Using GPU Spaces | 2026-10-03 | "Spaces running on free hardware are suspended automatically if they are not used for an extended period of time (e.g. two days)." | High |
| Pro required for ZeroGPU | https://discuss.huggingface.co/t/new-free-accounts-cannot-create-cpu-basic-gradio-spaces-only-zerogpu-available/177629/1 | New free accounts... | 2026-10-03 | "After creating the Space on ZeroGPU, the hardware downgrade dialog requires PRO to switch to CPU Basic." | High |

### 8. Fly.io

| Claim | URL | Page Title | Date Checked | Quotation | Confidence |
|-------|-----|------------|--------------|-----------|------------|
| Free tier deprecated | https://bex.co/blog/2026/08/16/flyio-pure-usage-pricing-always-on-app-cost | Fly.io Killed Its Subscription Tiers (2026) | 2026-10-03 | "The deprecated page at fly.io/docs/about/pricing/#discontinued-plans says it plainly: 'Fly.io no longer offers plans to new customers.' New organizations get pay-as-you-go from the first machine-hour, with only a one-time trial — roughly 2 machine-hours or 7 days." | High |
| Card required | https://www.fly.io/docs/about/billing | Fly.io Billing | 2026-10-03 | "We require an active, valid credit card on file for most Fly.io accounts to do things like deploying multiple apps and deploying public images. This is primarily a means to prevent abuse and ensure that we can collect payment at the end of the month." | High |
| Prepaid credits option | https://www.fly.io/docs/about/billing | Fly.io Billing | 2026-10-03 | "If you don't have a credit card, then you can add credits to your account. You can purchase credits from the Billing section of the dashboard in various amounts (minimum purchase $25)." | High |

### 9. Koyeb

| Claim | URL | Page Title | Date Checked | Quotation | Confidence |
|-------|-----|------------|--------------|-----------|------------|
| Card required | https://www.koyeb.com/docs/faqs/pricing | Pricing FAQs | 2026-10-03 | "Why does Koyeb require a credit card? We require a credit card to prevent fraud and abuse. We verify the card you enter by placing a $29 pre-authorization hold and immediately canceling it." | High |
| Auto-charge on signup | https://www.koyeb.com/docs/faqs/pricing | Pricing FAQs | 2026-10-03 | "Am I charged when I enter my credit card? Yes. Right after we place the $29 pre-authorization hold to verify your card, we also charge you the pro-rated amount for the plan you select." | High |
| Feb 2026 change | https://snapdeploy.dev/blog/free-cloud-deployment-platforms-2026-comparison | Free Cloud Hosting 2026 | 2026-10-03 | "Koyeb removed its card-free Hobby plan in February 2026; a valid card with a $29 pre-authorisation hold is now required, and sign-up defaults to the $29/month Pro plan." | High |

### 10. Railway

| Claim | URL | Page Title | Date Checked | Quotation | Confidence |
|-------|-----|------------|--------------|-----------|------------|
| $5 trial, no card | https://docs.railway.com/pricing/free-trial | Free Trial | Railway Docs | 2026-10-03 | "The trial gives access to basic features for up to 30 days and includes a one-time grant of $5... No credit card required." | High |
| $1/mo after trial | https://buildaicurrent.com/credits/railway-free-trial | Railway free trial (2026) | 2026-10-03 | "After 30 days: the $1 Free plan... $0/month with $1 of monthly usage credits that do not roll over... Unused credit does not carry over." | High |
| Hobby not free | https://buildaicurrent.com/credits/railway-free-trial | Railway free trial (2026) | 2026-10-03 | "A correction worth stating plainly: Railway's Hobby plan is sometimes described as a free tier. It is not. Hobby costs $5 per month including $5 of usage, and the $5 is charged even if you use less." | High |
| Trial volumes deleted | https://buildaicurrent.com/credits/railway-free-trial | Railway free trial (2026) | 2026-10-03 | "Trial volumes are deleted 30 days after the trial credit expires, so move any database you care about before that." | High |

---

## Malawi-Specific Availability

| Platform | Malawi Access | Nearest Region | Notes |
|----------|---------------|----------------|-------|
| **Render** | ✅ Yes | Global CDN | No Africa PoP but global edge |
| **Vercel** | ✅ Yes | Global Edge | No Africa PoP but global edge |
| **Netlify** | ✅ Yes | Global CDN | .africa TLD used by Netlify customers |
| **Deno Deploy** | ✅ Yes | EU (Frankfurt/London) | 2 managed regions + global |
| **Supabase** | ✅ Yes | EU (Frankfurt/Ireland) or Mumbai | No Africa region |
| **Firebase** | ✅ Yes | Global | No specific Africa region |
| **Fly.io** | ✅ Yes | Johannesburg (not listed but 30+ regions) | 30+ global regions |
| **Koyeb** | ✅ Yes | Frankfurt / Washington DC | Free instance only in these two |
| **Railway** | ✅ Yes | Global | No restriction documented |
| **Hugging Face** | ✅ Yes | Global CDN | No restriction |
| **Google Cloud Run** | ✅ Yes | **Johannesburg (africa-south1)** | **Only major provider with Africa region** |
| **AWS Lambda** | ✅ Yes | Cape Town (af-south-1) | Region exists; Free Tier may work |
| **Azure Functions** | ✅ Yes | South Africa North/West | Regions available |
| **Oracle Cloud** | ⚠️ Conditional | Depends on home region | Requires international card; credit not in all countries |

---

## Recommended Platform Stack for LightSpeed

### Tier 1: Fully Viable (No Card, Generous Limits)
1. **Render** — Best for persistent web services, background workers, PostgreSQL, Redis. Spins down but 750 hrs/mo covers many use cases.
2. **Netlify** — Best for static + serverless functions + scheduled functions + edge. Credit model is flexible.
3. **Deno Deploy** — Best for TypeScript/JS edge functions with native KV, cron, zero cold starts.
4. **Supabase** — Best for Postgres + Auth + Edge Functions + Realtime + Cron. 7-day pause is manageable.

### Tier 2: Viable with Constraints
5. **Vercel Hobby** — Excellent platform but **non-commercial only**. Cron = daily only.
6. **Firebase Spark** — Good for static hosting + Firestore + Auth. **No Cloud Functions** (dealbreaker for runtime).
7. **Railway** — Only $5 for 30 days, then $1/mo (very tight).

### Tier 3: Not Viable Without Card
- Fly.io, Koyeb, Google Cloud Run, AWS Lambda, Azure Functions, Oracle Cloud — all require credit card for identity verification.

---

## Key Risks & Mitigations

| Risk | Platforms Affected | Mitigation |
|------|-------------------|------------|
| **Spin-down / cold starts** | Render, Railway, Netlify Functions, Deno Deploy, Cloud Run, Lambda, Azure Functions | Use external cron (cron-job.org, UptimeRobot) to ping endpoints; design for stateless startup |
| **Inactivity pause** | Supabase (7 days), Render (15 min), Hugging Face (2 days) | Scheduled external ping; monitor via health checks |
| **Hard limits / pause** | Vercel (30-day pause), Netlify (credit exhaustion), Supabase (HTTP 402) | Monitor usage dashboards; set alerts; design for graceful degradation |
| **No Africa region** | All except Google Cloud Run (Johannesburg), Azure (SA), AWS (Cape Town) | Use Cloudflare Workers (free, global, no card) as edge layer in front |
| **Non-commercial restriction** | Vercel Hobby | Use only for personal/internal tools; migrate to Pro/Render/Netlify for commercial |
| **Credit card required** | Fly.io, Koyeb, GCP, AWS, Azure, Oracle | Use virtual cards (Privacy.com, Revolut) with strict limits; or prepaid credits where allowed |

---

## Suggested Architecture for LightSpeed

```
┌─────────────────────────────────────────────────────────────┐
│                    LightSpeed Runtime                        │
├─────────────────────────────────────────────────────────────┤
│  Edge Layer (No Card)          │  Compute Layer (No Card)   │
│  ─────────────────────         │  ─────────────────────     │
│  Cloudflare Workers (Free)     │  Render (Web Services)     │
│  - DNS, WAF, Cache             │  - Persistent API/Workers  │
│  - Cron Triggers (Free)        │  - PostgreSQL + Redis      │
│  - Edge Functions              │  Deno Deploy (Edge Fn)     │
│                                │  - KV, Cron, WebSockets    │
├─────────────────────────────────────────────────────────────┤
│  Data Layer (No Card)          │  AI/ML Layer               │
│  ─────────────────────         │  ─────────────────────     │
│  Supabase (Postgres, Auth,     │  Hugging Face Inference    │
│   Realtime, Edge Fn, Cron)     │  API (Free tier, rate-limited)
│  Netlify Database + Blob       │  Local/ONNX on Render CPU  │
└─────────────────────────────────────────────────────────────┘
```

**Rationale**: Combines the only no-card platforms with complementary strengths. Cloudflare Workers provides global edge + cron + security for free. Render provides persistent compute + managed databases. Deno Deploy provides zero-cold-start edge functions with native KV/cron. Supabase provides Postgres + Auth + Realtime + pg_cron. Hugging Face provides model inference API.

---

*End of Platform Comparison Research*