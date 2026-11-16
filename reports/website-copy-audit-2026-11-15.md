# Website copy audit, 15 November 2026

Scope: the external site at `lightspeedholdings.vercel.app` and the source that builds it
(`src/pages`, `src/components`, `src/data`, `src/site`, `public`, `index.html`).

Reviewed against the house style standard supplied for this audit.

## Method

1. Read `AGENTS.md` and applied its rules (evidence discipline, PowerShell, no edits to files I did not create).
2. Scanned 244 site files for the banned vocabulary list, em dashes, emoji, and empty sentence structures.
3. Loaded 19 live pages (10 routes plus 9 article slugs) in a real browser and measured the deployed text, not the source.
4. Verified every quote in this report against the file or the live page. Three claims from the audit team were wrong and were removed (see Verification log).

## Team

| Role | Agent | Responsibility this pass |
|---|---|---|
| Owner | `cmo` | Accountable for the external site and the fix plan |
| Voice | `thought-leadership-author` | Homepage, hero, proposition, CTA copy |
| Clarity | `technical-documentation-lead` | What We Do, HAOMTGV, capability copy |
| Positioning | `product-marketing-manager` | FAQs, articles, claims, number consistency |
| Verification | `qa-lead` | Forms, legal pages, metadata, severity |

Supporting roles for the fix, not used in this pass: `lead-frontend` (implementation), `product-designer` (labels, alt text, layout), `security-compliance-lead` (disclosure and claims review).

## Verdict

The site fails the standard on four rules and cannot currently be rebuilt from source.

- The deployed build breaks the em dash rule in 17 places and the banned vocabulary list in at least 6 visible labels.
- It speaks to the reader in the third person almost everywhere. "You" or "your" appears 3 times in 1,619 words on the homepage.
- It defines LightSpeed by what it is not, in at least 8 places.
- It makes one claim ("peer-reviewed methodology") that another page on the same site contradicts.
- Three committed files stop the build: `App.tsx`, `HomePage.tsx`, `SiteLayout.tsx`.

The writing itself is not weak. The best passages are specific and honest, and the site publishes numbers that most agencies hide. The problems are mechanical and fixable.

## Blockers

A rebuild is impossible until these are fixed. `npx tsc --noEmit` returns 4 errors, all in `SiteLayout.tsx`, and the syntax errors stop the compiler before it reports the other two.

| File | Problem | Evidence |
|---|---|---|
| `src/components/SiteLayout.tsx` | Line 71 opens a `<div>` that never closes, and line 94 closes a fragment that was never opened | `tsc`: `TS17008`, `TS1381`, `TS1005`, `TS1003` |
| `src/App.tsx` | `FaqPage` imported twice (lines 10 and 20) and `FaqPageRoute` declared twice (lines 26 and 35) | `Select-String` |
| `src/pages/HomePage.tsx` | Renders 8 components it never imports (`WhatWeBuildGrid`, `HAOMTGVSection`, `IntentToExecutionLifecycle`, `InsightsSection`, `AboutSection`, `FaqSection`, `DistinctCTA`, `Footer`) and renders `HumanApprovalMatrix` twice (lines 29 and 42) | File read; `git show HEAD` confirms this is committed, not local work |

The deployed bundle is `index-ZZhwd03A.js`. The local build is `index-BsVIXZl1.js`. The live site is running an older commit than the one on disk, so nothing in this report has shipped.

## Live violations

### 1. Em dashes (17 instances)

Measured on the live site: 8 in running prose, 9 in labels.

| Page | Count | Example |
|---|---|---|
| Homepage | 6 | `turn bold ideas into real-world impact — starting in Malawi` (hero) |
| Homepage | 5 | `AUTO_APPROVE (0) — Fully Autonomous Agent (Zero Human Gate)` (approval matrix) |
| About | 3 | `operating systems—scalable from one agent to the 90-role internal benchmark—that collapse workflow latency` |
| AI assessment | 4 | `Foundational — Fragmented & Siloed Data` |
| 3 of 9 articles | 4 | `are not optional for African institutions — they are architectural requirements` |

The About sentence is the worst of the set. It uses two unspaced em dashes as if they were commas, in a sentence that also runs to 51 words.

The source is worse than the deployment. 77 lines in the site source contain an em dash. Fixing the build without a copy sweep would ship more, not fewer.

### 2. Banned vocabulary

| Term | Live instances | Where |
|---|---|---|
| `Insights` | 18+ | Breadcrumb on every article page, `ALL INSIGHTS` in every footer, `PHAROS INSIGHTS` on 5 pages |
| `ecosystem` | 4 | Homepage visitor path, two on About, one file path in an article |
| `human oversight` | 2 | What We Do, HAOMTGV |
| `paradigm` | 1 | `THE ARCHITECTURAL PARADIGM` (HAOMTGV) |
| `highlight` | 1 | `Treat superlatives as a red flag, not a highlight` (evidence article) |

The naming is the bigger problem. One section carries three names: the navigation says `PHAROS`, related links say `PHAROS INSIGHTS`, and the meta title says `Insights | LightSpeed Holdings`. Pick one. `PHAROS` is the only one that avoids the banned word and matches the brand.

`elevate` appears once, in `zero authority to elevate privileges`. That is a security term, not marketing language. Leave it.

### 3. Negative contrast

The site keeps telling readers what it is not. Eight visible examples:

- `We design, build and operate with AI at the core, not as an add-on.` (home)
- `Building Governed Operating Capability, Not Isolated Tools` (home heading)
- `LightSpeed does not sell point-solution chatbots or experimental AI widgets.` (home)
- `Not AI for its own sake. AI for work that matters.` (home)
- `BUILT, NOT PREDICTED.` (home closing CTA)
- `Not a Copilot Reseller. Not an Outsourcing Shop.` (About)
- `We are not a generic software outsourcer.` (About)
- `Governance in HAOMTGV is not an afterthought or a final checkpoint.` (HAOMTGV)

Each one makes the reader do the work of inferring the offer. A direct claim does the job better. For the About card, `We build the agent, the approval rules, and the audit trail, then hand you the keys` says more than two negations.

The `From X to Y` construction also survives in four headings, including a live article title: `From Digital Transformation to AI-Native Transformation`.

### 4. Reader address

| Page | Words | "you" or "your" |
|---|---|---|
| Homepage | 1,619 | 3 |
| What We Do | 1,202 | 3 |
| HAOMTGV | 1,346 | 2 |
| About | 889 | 2 |

The privacy and terms pages use "you" or "your" 15 and 11 times. The legal pages address the reader more directly than the sales pages. That is backwards.

The page speaks about "the enterprise", "human leadership" and "organisations" in the third person, then switches to "you" only in the closing CTA. The fix is not to sprinkle pronouns. Rewrite each section lead as an instruction or a promise to the reader.

### 5. Claims that break the site's own honesty rule

The site's strongest value is `Evidence Over Claims`. Three places break it.

1. `/insights` says `Original research, peer-reviewed methodology`. The evidence article on the same site says its one academic citation `was not peer-reviewed`. Change the page copy to `cited sources` or list the actual review status.
2. The article listing says `Inside a 90-Agent Company`. The article it links to is titled `Inside a 91-Agent Company`. The canonical count is 90 roles (89 agents plus 1 CEO), so the article title is wrong and the listing is right.
3. FAQ evidence chips render raw repo paths to visitors. Expanding the first FAQ shows `src/data/siteContent.ts#no client-facing deliverable ships without human (verified)`. That is an internal file path with a truncated sentence, marked as verified by citing the site's own copy.

The article pages do the same thing at the foot of each piece, with citations like `SRC/DATA/INSIGHTS.TS:69 · DOCS/CLIENT-FACING/USE-CASE-CATALOG.MD:76`. A reader cannot use that.

### 6. Metadata

Every page serves the same title and description. Measured on 3 live pages:

```
/about       LIGHTSPEED HOLDINGS LIMITED™ | ASPIRE. ACT. ACHIEVE.
/contact     LIGHTSPEED HOLDINGS LIMITED™ | ASPIRE. ACT. ACHIEVE.
/what-we-do  LIGHTSPEED HOLDINGS LIMITED™ | ASPIRE. ACT. ACHIEVE.
```

Cause: `SiteLayout.tsx:39` sets that title on every route change, and `usePageMeta` is never called by any page. The 11 well-written per-page descriptions in `usePageMeta.ts` are dead code. So is its `Insights | LightSpeed Holdings` title, which would have broken the vocabulary rule if it had shipped.

## Source-only issues

These are not live today. They ship the moment the build is fixed or the file is wired up.

| File | Issue |
|---|---|
| `src/data/useCases.ts` | Fabricated metrics: `68%`, `34%`, `71%`, `45 days vs the industry average of 180`, `23 recorded incidents`. No file imports this module. Delete it or replace the numbers with mechanisms. |
| `src/data/insights.ts` | 17 mentions of a 91-agent count, some inside correction notes that explain the count is wrong |
| `src/data/registries/faq-registry.json` | Corrupted arrow characters on line 148 (`â€†â€™` instead of `→`), plus a Tier 1 to 5 model that contradicts Tier 0 to 4 elsewhere |
| `src/components/TelemetryBar.tsx` | Hardcoded `UPTIME`, `LAT: 12ms`, `SYNC: 98.7%` presented as live data. No file imports it. |
| `src/data/faqs.ts` | `There is no public rate card yet` while other pages publish MWK 800,000, 1,800,000 and 3,500,000 |

## What passes

- No emoji. The 18 hits were `✓` and `✕` dingbats used as list markers, which is a typographic choice, not a breach.
- No `Why it matters` section anywhere.
- No `not only ... but also` construction.
- No `Subsequently`, `Hustle`, `Revolutionize`, `Fostering`, `Reimagine`, `Showcase`, `Profound`, `Groundbreaking`, `Delve`, `Whisper`, `Enablement`, `Meanwhile`, `Game changer`, `Unleash`, `Harness`, `Synergies`, `Cross-functional` or `Touch point` in visible copy.
- The legal pages use active voice and "you" well: `We take no card details on this site. We invoice by Airtel Money, TNM Mpamba, or bank transfer.`
- The best sentence on the site is already in the right style: `Share a brief of up to 500 words. We will assess feasibility, outline governance, and tell you plainly what it takes to start.`

## Fix order

1. Repair the three build blockers. Nothing else can ship until this is done.
2. Pick one name for the research section. Replace `Insights` and `PHAROS INSIGHTS` with `PHAROS` in the breadcrumb, related links and footer.
3. Sweep em dashes in the site source, not just the deployed pages. Target the 77 flagged lines.
4. Fix the 90 versus 91 article title, and the `peer-reviewed` claim on `/insights`.
5. Rewrite the 8 negative-contrast lines and the four `From X to Y` headings.
6. Replace the FAQ evidence chips with human-readable source names.
7. Wire up `usePageMeta` or delete it. One title per page, or none.

## Verification log

Verified by command or by live read in this session:

- `npx tsc --noEmit -p tsconfig.json` returned 4 errors.
- `git show HEAD:src/components/SiteLayout.tsx` confirms the broken JSX is committed.
- `git show HEAD:src/pages/HomePage.tsx` confirms the missing imports are committed.
- Live text extracted from 19 pages via a real browser session.
- Every quoted string in this report checked with `String.Contains` or `Select-String`, or seen in live output.

Claims from the audit team that were checked and rejected:

- A subagent said `START A CONVERSATION` is the canonical CTA and `ENGAGE LIGHTSPEED` conflicts with it. Wrong. `src/data/ctas.ts` states `ENGAGE LIGHTSPEED` is the single primary CTA.
- A subagent reported `TelemetryBar` as live hardcoded data. It is never imported.
- A subagent reported that `capabilities.ts` ships emoji. Only `capabilityTitles` is imported, and that contains no emoji.

Not verified, and therefore not asserted: whether CI currently gates on `tsc`, the origin of the stale deployment, and whether the 1,200 cooperative member figure is measured.
