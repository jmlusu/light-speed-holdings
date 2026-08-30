# LightSpeed Holdings Website

This is the LightSpeed Holdings company website — a [Next.js](https://nextjs.org) (App Router) project bootstrapped with `create-next-app`. It models the structure of [webuild-ai.com](https://www.webuild-ai.com): hero, 7 services, 3 industries, partners, case studies, insights, plus contact and newsletter forms.

## Getting Started

```bash
npm install
npm run dev        # http://localhost:3000
```

## Quality gates

```bash
npm run lint       # ESLint
npm run build      # Production build + TypeScript check
npm start          # Serve the production build locally
```

## Project layout

- `src/app/` — routes: `/`, `/get-in-touch`, `/about-us`, `/our-approach`, `/careers`, `/faq`, `/privacy-policy`, plus dynamic routes for services, industries, insights, and customers
- `src/components/` — ui primitives (`ui/`), sections (`sections/`), layout (`layout/`)
- `src/data/homepage-data.ts` — all site content (services, industries, partners, case studies, insights)
- `src/app/api/` — `contact` and `newsletter` endpoints (currently validate + acknowledge; wire to CRM/email provider before production)
- `src/app/globals.css` — Tailwind v4 dark theme design tokens

## Deploy on Vercel (free)

The authenticated deploy needs you to log in once.

### Option A — Web dashboard (simplest)

1. Push this repo to GitHub.
2. Go to https://vercel.com/new, import the repo, and select the `website` directory as the root and framework preset `Next.js`.
3. Deploy. Vercel gives you a `<project>.vercel.app` preview URL automatically and picks up pushes.

### Option B — CLI

```bash
cd website
npx vercel login          # one-time browser auth
npx vercel                # creates project + preview deployment
npx vercel --prod         # promote to production
```

One-liner with a token (create at https://vercel.com/account/tokens):

```bash
cd website
VERCEL_TOKEN=<your-token> npx vercel --prod --yes
```

### Custom domain (later, still free)

Add your domain under **Vercel → Project → Settings → Domains** and point its DNS (A/CNAME records shown in the dashboard) at Vercel.
