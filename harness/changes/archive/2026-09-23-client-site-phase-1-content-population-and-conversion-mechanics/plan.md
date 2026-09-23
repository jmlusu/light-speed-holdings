# Plan

## Technical Approach

1. Extend `CtaBand` with optional `onRequestBriefing` so pages can open the briefing modal instead of only navigating.
2. Wire ResourcesPage cards + CTA to `onRequestBriefing(\`Resource request: ${title}\`)`.
3. Wire EventsPage cards + CTA to speaker inquiry via `onRequestBriefing`.
4. Add `NewsletterSignup` component (email + name, honeypot, Turnstile action `contact`) posting to `/api/enquiry`.
5. Mount NewsletterSignup on NewsPage and InsightsPage; optional cross-links News ↔ Insights.
6. Validate lint + build.

## Impacted Modules And Files

- `src/components/site/CtaBand.tsx` — optional briefing callback
- `src/pages/ResourcesPage.tsx` — clickable cards, briefing prefill
- `src/pages/EventsPage.tsx` — clickable cards, speaker CTA
- `src/components/NewsletterSignup.tsx` — new
- `src/pages/NewsPage.tsx`, `src/pages/InsightsPage.tsx` — mount signup
- `src/lib/enquiry.ts` — no API change required; document newsletter enquiryType

## Interfaces, Data, Permissions

- `CtaBandProps.onRequestBriefing?: (summary?: string) => void`
- Enquiry payload: existing `enquiryPayload`; newsletter uses `form: 'contact'`, `enquiryType: 'Newsletter subscription'`.
- No new secrets or admin keys.

## Spec Gaps Found From Planning

- None.

## Risks And Mitigations

- Turnstile action mismatch → use `contact` for newsletter (already in `EXPECTED_ACTIONS`).
- Dead CTAs → ensure Resources/Events cards always fire a handler.

## Verification Plan

- `bun run lint`
- `bun run build`
- Manual: resource card opens modal with prefill; newsletter form validates empty email.
