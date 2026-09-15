# ADR-020: Client-Facing Website Guiding Principles (CMO v1.0) — Ratified Scope

**Status:** Accepted
**Date:** 2026-09-15
**Deciders:** Human CMO/CEO (ratification), CMO agent, Frontend Architect, Chief of Staff
**Technical Domain:** Client-facing website (lightspeedholdings.com) / frontend SPA

## Context

The CMO mandate — "LightSpeed Holdings — Guiding Principles for the Client-Facing
Website (lightspeedholdings.com), version 1.0" — introduces binding rules for the
external site: outcome-led 5-second pages, evidence-backed or qualified claims,
canonical brand tokens, no fake success states, and an Appendix A review gate with
an Appendix B acknowledgment roster.

The current live site (repo-root Vite React SPA at `index.html` -> `src/main.tsx`,
built to `dist` for Vercel) violates the mandate across all 12 Appendix C items
(e.g. fake-success enquiry forms, unqualified claims, off-palette surfaces,
tactical motif outside diagnostics, no analytics events). Wayfinder map #251 was
created 2026-09-15 to drive the remediation; T1 (#252) delivered a public claims
& evidence ledger (65 claims: 18 evidenced / 29 qualified / 18 unqualified), and
T8 (#259) shipped the acknowledgment registry + Appendix A review gate.

Three migration-target decisions and three scope gaps required human ratification
before any implementation (T2, #253).

## Decision

Human CMO/CEO ratified (2026-09-15, no redlines):

1. **Migration target — migrate in place.** The repo-root Vite React SPA is the
   migration target. No new rebuild, no marketing-site (Astro) revival, no redesign
   per wayfinder map #157.
2. **Sprint scope — full compliance.** All 12 Appendix C items plus the whole
   "Appendices A-D" bundle (evidence rules, ACK roster, review gate, QA gate).
3. **Design authority — section 7.1 supersedes map #157.** Canonical tokens only:
   navy `#070A40` / red `#E63946` / cyan `#00BFFF` / white / `#F2F2F2`, Arial type
   scale. Prior locks (Geist font, cream/sage palette) are void.
4. **Form SLA copy** — ship "We respond to qualified enquiries within two business
   days" next to every contact surface (ContactSection, ExecutiveBriefingModal,
   Executive Briefing, Info Requests).
5. **Enquiry delivery ownership** — sales-owner owns the enquiry-to-lead pipeline
   and the 2-business-day response SLA; customer-success-owner owns the
   follow-up/no-show loop; cfo owns the audit record. Backend "how" deferred to
   research ticket T5 (#256).
6. **Remediation priority order** — P1 fake-success forms/backend (§10) and
   unqualified claims (§5); P2 brand-token + tactical-motif confinement (§6/§7);
   P3 navigation/IA consolidation + outcome-led restructure (§4); P4 analytics &
   funnel instrumentation; P5 consistency fixes + Pharos IA.

## Consequences

- Wayfinder T2 (#253) closed; T5 (#256, enquiry backend research) and T6 (#257,
  token/component migration grilling) are unblocked.
- The fake-form guard (`scripts/check-site-form-backend.py`) and the Appendix A PR
  template now have ratified SLA copy and ownership to enforce against.
- Any deviation from section 7.1 tokens on lightspeedholdings.com is a violation,
  not a stylistic choice.
