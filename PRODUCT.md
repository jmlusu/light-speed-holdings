# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Three audiences, deliberately weighted equally. The site's visitor-path structure exists specifically to route between them rather than to prioritise one:

1. **Enterprise and parastatal decision-makers** in Malawi and the wider SADC region — COOs, CIOs, and transformation leads. Their job: decide whether an AI-native operating model is credible enough to take to their board, and find a route to a conversation.
2. **Government and regulator audiences** — policy and programme staff at institutions such as MACRA, SADC, and UNDP. Their job: assess governance posture and institutional credibility before any engagement.
3. **Investors and ecosystem partners** — funders, venture partners, and prospective collaborators. Their job: evaluate the venture, the operating model behind it, and the team that runs it.

## Product Purpose

This is the public face of LightSpeed Holdings Limited: a company that both *runs* on an agentic operating model and *sells* the design and governance of such models. The site exists to make the company's intellectual position legible and citable, so that credibility precedes any commercial conversation.

Success is defined as **readership and credibility**, not direct conversion. The primary measure is whether the Pharos research and insight output is read, trusted, and shared. Commercial conversion — briefings, assessments, enquiries — is a downstream effect of that earned credibility, and the site should be designed to protect the reading experience rather than interrupt it with conversion pressure.

## Positioning

**The AI-native company builder for Southern Africa.**

The mechanism a neighbouring consultancy could not truthfully copy: LightSpeed does not advise on agentic operating models in the abstract — it operates one. The company runs 89 AI agents alongside a single human CEO across 20 departments and 5 governance tiers, with all execution subject to a human decision authority. The commercial offer (strategy, design sprints, forward-deployed engineers, venture co-build, platform licensing, industry accelerators, client portal) is derived from that running system rather than from a service catalogue.

Geographic progression is explicit and directional: **Malawi → SADC → Africa**.

## Operating Context

- Visitors arrive from the CEO's public thought-leadership footprint (Pharos), from regional policy forums, and from direct commercial outreach. The site is frequently the second or third touch, not the first.
- Governance vocabulary is load-bearing: HAOMTGV (the operating model), the 5-tier human approval matrix, the intent-to-execution lifecycle, and the honesty badge system are reference concepts visitors are expected to engage with, not decoration.
- Enquiries are qualifying conversations, not transactions. The contact and briefing flows collect context that feeds a human-led response.
- The site is read in both light and dark themes, on desktop and mobile, and is treated as a credibility document that may be shared internally at a target organisation.

## Capabilities and Constraints

- Routes served: `/`, `/what-we-do`, `/haomtgv`, `/ai-assessment`, `/faq`, `/insights`, `/insights/:slug`, `/about`, `/contact`, `/legal/privacy`, `/legal/terms`, plus a not-found page.
- The **AI Readiness Assessment** is a five-step qualitative diagnostic (data maturity, core infrastructure, governance alignment, talent readiness, agentic workflow potential) that ends in a summary the visitor can act on or submit.
- The enquiry flow is protected by Cloudflare Turnstile and writes to a serverless endpoint; it never sends real email from a local dev submission.
- **All public copy is registry-driven.** Company identity, metrics, capabilities, solutions, sectors, insights, FAQs, governance, CTAs, use cases, and claims live under `data/` and are imported rather than hardcoded. Canonical counts (90 roles = 89 agents + 1 human CEO, 20 departments, 5 governance tiers) are enforced by tests.
- **Honesty badges are a product constraint, not a style choice.** Every capability claim carries one of four levels — `proven`, `pilot`, `fieldable`, `development` — and the badge must match the real evidence level.
- Two design-token sources exist and are aliased to one another (`packages/design-system/src/tokens` via `@lightspeed/design-system`, plus `src/design-system/tokens`).
- Deployment is static output on Vercel at `lightspeedholdings.vercel.app`, with serverless functions under `api/`.
- This app is entirely separate from the CEO Dashboard (FastAPI on 8420/8421). Marketing-site ports are 1441 (dev) and 1440 (preview), and Vite refuses to bind the dashboard ports.

## Brand Commitments

- Legal name **LightSpeed Holdings Limited**, short name **LightSpeed Holdings**, trademark form `LightSpeed Holdings Limited™`.
- Tagline: **ASPIRE. ACT. ACHIEVE.**
- North star line: **We build AI-native companies.**
- Human authority statement, to be used verbatim: **AI executes. Humans decide.**
- Founded 2024, Lilongwe, Malawi.
- Committed visual identity: navy `#070A40`, red `#E63946`, cyan `#00BFFF`, morning mist `#F7F8F9`, deep mineral `#121518`; Arial as the single typeface family. Cyan is the trust signal and replaces green in status contexts.
- Voice: declarative, governance-literate, unhyped. Claims are stated at the level they can be defended.

## Evidence on Hand

- **Published research and Pharos output** is the primary proof surface: the insights library (`data/insights/registry.ts`) and the long-form articles it serves. This is the evidence the site is built to carry.
- **The operating model itself** is real and demonstrable: the agent organisation, its department structure, its governance tiers, and its approval matrix are running systems, documented in this repository.
- **No named clients, customer logos, testimonials, or outcome case studies are currently recorded.** Any such material appearing on the site would be fabricated. Do not invent them, and do not imply them through layout that reserves space for logos or quotes.
- Metrics shown publicly must come from `data/metrics/registry.ts`; claims must come from `data/claims/registry.ts`.

## Product Principles

1. **Credibility precedes conversion.** Protect the reading experience; every conversion element must earn its interruption.
2. **Claim only what survives scrutiny.** Honesty badges, registry-sourced numbers, and governed vocabulary exist so the site cannot overstate.
3. **Governance is the product, visibly.** The approval matrix, the lifecycle, and the human authority statement are the differentiation, not supporting material.
4. **One company, three audiences, no diluted middle.** Route each audience explicitly rather than writing copy that tries to address everyone at once.
5. **Southern African specificity is a feature.** Malawi → SADC → Africa is the stated path; local institutional literacy is part of what makes the position defensible.

## Accessibility & Inclusion

- Reduced-motion preference is honoured globally (animation and transition durations collapse to 0.01ms).
- A skip link, visible focus ring (cyan, 3px, 2px offset), and semantic main-content landmark are already established commitments.
- Body copy is set in points at a 16px root, and the type scale assumes comfortable reading rather than dense display use.
