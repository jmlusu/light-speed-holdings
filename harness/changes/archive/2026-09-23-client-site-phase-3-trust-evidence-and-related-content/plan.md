# Plan

## Technical Approach

1. Add `trustEvidence` to `siteContent.ts` — 4–6 cards sourced only from `GOVERNANCE_SOLUTION` / securityTopics facts, each with `HonestyLabel`.
2. Create `src/components/site/RelatedLinks.tsx` — theme-aware related nav strip (`links: { to, label }[]`).
3. Extend TrustPage: evidence section (HonestyBadge per card), honesty policy section (reuse `honestyPolicy`), RelatedLinks, CtaBand with `onRequestBriefing`.
4. FAQPage: accept `onRequestBriefing`, pass to CtaBand, add RelatedLinks (Trust, Technology, Leadership).
5. LeadershipPage: same CTA wiring + RelatedLinks (Trust, FAQ, Technology); optional honesty badge on advisory role note if wording stays honest (roles not named individuals — only if already true in data).
6. Refactor News/Insights (and Resources/Events if inline) to use RelatedLinks.
7. Validate lint + build + lint-ecl.

## Impacted Modules And Files

- `src/data/siteContent.ts` — `trustEvidence`
- `src/components/site/RelatedLinks.tsx` — new
- `src/pages/TrustPage.tsx`, `FAQPage.tsx`, `LeadershipPage.tsx`
- `src/pages/NewsPage.tsx`, `InsightsPage.tsx`, `ResourcesPage.tsx`, `EventsPage.tsx`

## Interfaces, Data, Permissions

- `RelatedLinksProps: { theme, links: { to: string; label: string }[] }`
- `trustEvidence: { id, title, description, proof: HonestyLabel }[]`
- No API, secrets, or permission changes.

## Spec Gaps Found From Planning

- None.

## Risks And Mitigations

- Overclaiming certifications → only operational controls with existing proven wording.
- FAQ/Leadership prop currently unused → TypeScript will catch if CtaBand requires wiring; keep optional callback on CtaBand.

## Verification Plan

- `bun run lint`
- `bun run build`
- `pwsh scripts/lint-ecl.ps1`
