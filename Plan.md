# Client-Facing Website Compliance — Execution Plan (Plan.md)

- Owner: chief-of-staff (accountable) → roster owners per ticket
- Source of truth: CMO Guiding Principles v1.0 (`docs/adr/020-client-facing-site-guiding-principles.md`)
- Tickets: tracked under Wayfinder map #251 — see `docs/client-facing/website-compliance-ticket-ledger.md` and GitHub issues #302–#308
- Status date: 2026-09-16

## Compliance matrix (mandate → audit → status)

| # | Mandate requirement | Observed (audit) | Status | Evidence |
|---|---|---|---|---|
| 1 | Every page answers what/who/why/next in 5s (outcome-led) | Homepage is feature-dump; hero not outcome-led | VIOLATION | #308 (T4 #255 prototype) |
| 2 | One outcome-led CTA per route, submits to real backend | CTA labels wrong (see §8); forms submit to real worker | VIOLATION (labels) | #305 |
| 3 | Claims evidenced or qualified; no unqualified absolutes | 18 unqualified (c) claims live | VIOLATION | #302 |
| 4 | §7 visual identity: navy/red/cyan only, Arial scale | Custom hexes, zinc/slate/amber, arbitrary gradients | VIOLATION | #303 |
| 5 | §7.1 tokens supersede #157 (Geist/cream/sage void) | Arial base OK; token layer not enforced | VIOLATION | #303 |
| 6 | Tactical motif confined to diagnostics | ThreeCanvas + tactile + LED site-wide | VIOLATION | #303 |
| 7 | §9 case studies evidenced / anonymised / NDA-qualified | PC-05, POL-03 self-reported | VIOLATION | #306 |
| 8 | Nav five-item: What We Do / Proof / Insights / About / Book a Briefing | 9-item nav; wrong CTA labels | VIOLATION | #305 |
| 9 | §8 CTA labels: "Book an executive briefing" / "Request an AI readiness assessment" | Absent; "Book Discovery Call", "Start a Conversation" | VIOLATION | #305 |
| 10 | §3 forms: no fake success — real backend, HTTP 201 only | PASS — real worker, guard green | COMPLIANT | ContactSection/ExecutiveBriefingModal → `fetch('/api/enquiry')` |
| 11 | §3 SLA copy "within two business days" | PASS — on contact + briefing modal | COMPLIANT | `src/lib/enquiry.ts:2` |
| 12 | §10 form privacy + submission handling | Backend does spam hardening; details to verify | PARTIAL | #305/#306 |
| 13 | §11 a11y clean at 390px, keyboard, dialogs | Label htmlFor gaps, unlabeled inputs, modal semantics | VIOLATION | #306 |
| 14 | §10/§12 analytics (cookieless, no banner) + Appendix A gate in CI | No analytics; gate shipped but not wired | PARTIAL | #307 |
| 15 | Appendix A review gate enforced in PRs/CI | Workflow exists; not a required check | PARTIAL | mark required |

## P1 + P2 execution wave (this pass)

| Step | Work | Owner | Status |
|---|---|---|---|
| A | Plan.md compliance matrix | chief-of-staff | DONE |
| B | Dev-only `/api/enquiry` stub (201, production-gated) + guard re-run | path | DONE |
| C | P1: qualify unqualified claims in `src/data/siteContent.ts` + contradiction sites | content-writer | in progress |
| D | P1.5: blur validation + autocomplete (forms) | frontend | pending |
| E | P2: token sweep (off-token classes/custom hexes → brand tokens) | frontend-architect | pending |
| F | P2: motif confinement (ThreeCanvas/tactile/LED off non-diagnostics) | frontend | pending |
| G | P2: mono confinement (Arial for UI text; mono = metadata only) | frontend | pending |
| H | Verify: `npm run build`, `npm run lint`, `npm test`, guard script | qa | pending |

## Open items (tracked on tickets, not this pass)

- P3 Nav/IA + route consolidation to combined URLs (#305) — user decision: combine URL routes (merge offerings/solutions/industries under What We Do)
- P4 Analytics — Plausible primary / Umami fallback, T3 event schema (#307)
- P5 a11y + Pharos Insights IA (#306)
- ACK registry sweep — 15 roles PENDING → ACKNOWLEDGED (#304)
- Homepage outcome-led restructure + T4 #255 prototype (#308)

## Verification standard (every change)

- `npm run build` (tsc) + `npm test` green
- `python scripts/check-site-form-backend.py` green
- Playwright 390px + keyboard + visible focus + zero console errors
- Before/after screenshots; `ls-artifact-qa` APPROVE on visual work
- Appendix A checklist in PR; §7.1 tokens only
- Local form tests use dev-only stub — never hit live `/api/enquiry`
