# Claims Audit Cadence

**Status:** ACTIVE — operating procedure
**Source mandate:** `docs/CLAIMS_GOVERNANCE.md` §"Quarterly Claims Audit" (lines 180–188) and §"Pre-Publication Gate" (lines 190–197)
**Accountable owner:** `clo` (CLAIMS_GOVERNANCE.md names "Legal Owner + CISO"; CLO is the Legal function owner)
**Reviewer:** `qa-lead`
**Data of record:** `src/data/registries/claims-registry.json` (canonical claims), `src/data/registries/faq-registry.json`, rendered site components

---

## Purpose

Keep every published claim classified, evidenced, current, and honestly badged. The audit exists to catch claims whose evidence has gone stale, whose status has drifted from reality, or whose wording implies endorsements we do not hold. Non-compliance blocks publication (`docs/CLAIMS_GOVERNANCE.md` §1, §159–175, §291–315).

## Cadence

| Trigger | When | Owner | Reviewer |
|---------|------|-------|----------|
| **Quarterly evidence audit** | Once per calendar quarter; first run due before the 2026-12-28 expiry cluster (see watchlist) | `clo` | `qa-lead` |
| **Pre-publication gate** | Before any public content ships (website, decks, proposals, social, Pharos, sales material) | Content owner | `qa-lead` + `clo` for regulator/government claims |

Output goes to a separate audit report directory, with evidence directories read-only during the audit (CLAIMS_GOVERNANCE.md §221–226). Report findings to CEO + Board (§188). No CI verification is implied by this document.

## Concrete checklist

Run every item against `src/data/registries/claims-registry.json` and the rendered surfaces that consume it.

1. **Evidence refs resolve.** Every `evidenceRef` must point to a file/path that exists and is readable, or to a git-history location that is explicitly documented and accepted. Flag refs to retired or moved files (`see git history`) as conditional — they are not live, resolvable paths for the purposes of the §194 pre-publication gate.
2. **Statuses current.** Each `classification` must still match the definitions in CLAIMS_GOVERNANCE.md §18–31 and the real state of the work. Check status transitions (PILOT → FIELDABLE, FUTURE → PILOT, etc.) per §237–247; a stale rung is a finding.
3. **Expired claims flagged.** Every claim whose `expiryDate` has passed (or passes during the audit window) is flagged for re-verification or archive. Expiry is auto (§243); reuse without re-verification is a finding.
4. **`UNVERIFIED_DO_NOT_PUBLISH` caught.** Scan all published content for claims classified `UNVERIFIED` / `UNVERIFIED_DO_NOT_PUBLISH` (§31, §167–172, §312). Any hit blocks publication and triggers takedown + root cause analysis (§297).
5. **Rendered badge/evidence parity.** The badge rendered on the site must equal the registry `classification` for that claim ID, and the displayed wording must match the registry `text`. Mismatches (e.g. a DEMONSTRATION claim rendered with a stronger badge, or an FAQ `evidence[].status: "verified"` on a DEMONSTRATION-classified claim) are findings.

## Expiry watchlist — `expiryDate` 2026-12-28

The following **23** claims in `src/data/registries/claims-registry.json` expire on 2026-12-28. All must be re-verified or archived in the quarterly audit before any reuse:

1. `claim.agent-count`
2. `claim.department-count`
3. `claim.test-count`
4. `claim.five-tier-approval`
5. `claim.four-governance-gates`
6. `claim.append-only-audit-trails`
7. `claim.rbac-key-rotation`
8. `claim.canonical-registry-numbers`
9. `claim.sovereign-offline-first`
10. `claim.mobile-money-integration`
11. `claim.no-paying-clients`
12. `claim.agricultural-cooperative-pilot`
13. `claim.university-malawi-student-management`
14. `claim.js-stopover-bar-live`
15. `claim.chichewa-ai-piloting`
16. `claim.sadc-governance-framework`
17. `claim.national-ai-strategy-submission`
18. `claim.university-capacity-building`
19. `claim.9-llm-providers`
20. `claim.ai-ethics-board-review`
21. `claim.board-governance-cadence`
22. `claim.data-protection-act-compliance`
23. `claim.historical-agent-counts`

Out of scope for this watchlist (later expiry): `claim.compliance-automation-in-house` (2027-01-26) and `claim.haomtgv-seven-layers` (2027-02-25).

---

## Regulator-facing material — preparation only, not published

**Scope of this section:** prepare material only. Do **not** edit any site component and do **not** publish regulator, counsel, or residency claims. Publication requires CEO sign-off.

### Material reviewed

| Item | Location | Classification | Evidence ref |
|------|----------|----------------|--------------|
| FAQ "Does LightSpeed work with regulators?" | `src/data/registries/faq-registry.json`, `faq-20` (lines 346–359) | FAQ `evidence[].status: "verified"` for `claim.sadc-governance-framework`; the underlying claim is **DEMONSTRATION** | `claim.sadc-governance-framework`; `sector-registry.json#SADC Agentic AI Governance Framework authored by CEO Jack Mlusu` |
| SADC framework claim | `claims-registry.json` lines 161–168 | **DEMONSTRATION** (owner `ceo`, `lastVerified` 2026-09-28, expires 2026-12-28) | `src/data/sectors.ts (government-public-sector honestyNote); retired CATALOG_POLICIES policy-sadc-framework (useCaseCatalogData.ts, see git history)` |
| National AI Strategy submission claim | `claims-registry.json` lines 169–177 | **VERIFIED** (owner `ceo`, `lastVerified` 2026-09-28, expires 2026-12-28) | `retired CATALOG_POLICIES policy-national-ai (useCaseCatalogData.ts, see git history)` |

Both claims' evidence refs point to a **retired** file (`src/data/useCaseCatalogData.ts`) and carry the note "see git history". The exact `faq-20` answer text includes the caveat: *"We do not claim formal regulatory endorsements or approvals; this is policy work in progress."*

### Read-only re-source check performed

- `git log --all --oneline -- "*useCaseCatalogData.ts"` → file history found; retired in `6a6708b3` (`chore(cleanup): retire useCaseCatalogData, token mirrors, legacyPytestCount; reword Proof labels (#459)`).
- `git show --name-status --oneline 6a6708b3 -- "*useCaseCatalogData.ts"` → `D  src/data/useCaseCatalogData.ts`.
- `git show 6a6708b3^:src/data/useCaseCatalogData.ts` → `CATALOG_POLICIES` contains both entries:
  - `policy-sadc-framework` — title "SADC Agentic AI Governance Framework", honestyBadge "In active development", summary "Regional operational governance standard for autonomous AI across SADC Member States.", description "Authored by CEO Jack Mlusu and submitted to digital ministers, MACRA, CRASA, central banks, and regional development banks. Aligned with AU Continental AI Strategy."
  - `policy-national-ai` — title "National AI Strategy Consultation Submission", honestyBadge "Published", summary "Formal stakeholder submission to the Malawi Dept of E-Government / UNDP Inclusive Digital Transformation project.", description "Advocates for governing actions (Agentic AI) alongside content (Generative AI). Proposes 4-tier HITL risk model, machine-readable agent identity, and data sovereignty."

**Result:** both retired evidence refs were successfully re-sourced from git history. No files were modified by this check.

### Ruling

**(a) — Reusable as preparation, not publication.** The exact existing wording in `faq-20` may be reused *as prepared material* with its **DEMONSTRATION** badge (the classification of `claim.sadc-governance-framework`) and the explicit caveat **"we do not claim formal regulatory endorsements or approvals"** already present in that answer. Re-source evidence is preserved above. Publication is **blocked pending CEO confirmation**; no site component may be edited and no regulator/counsel/residency claim may be published by this audit.

### Risks to carry into the audit

- **History-only evidence.** Both refs resolve only via git history, not to a live file. The pre-publication gate requires "all evidence references resolve" (§194); the CLO/CEO must explicitly accept git-history evidence or require a live replacement before publication.
- **Classification tension.** CLAIMS_GOVERNANCE.md §170 says an implied regulator endorsement should be written as "SADC Agentic AI Governance Framework in development" with `FUTURE`; `claim.sadc-governance-framework` is registered as `DEMONSTRATION`. Confirm the intended rung with the CEO before reuse.
- **Verified-bar risk.** `claim.national-ai-strategy-submission` is classified `VERIFIED`, which CLAIMS_GOVERNANCE.md §84 defines as third-party verified, but the re-sourced evidence is an internal catalog entry with honestyBadge "Published" (self-attestation). Treat as a finding requiring CEO sign-off; do not upgrade wording beyond the sourced text.
- **Badge parity.** `faq-20` marks its evidence `verified` while the underlying claim is `DEMONSTRATION`; reconcile in the badge-parity checklist before any rendering change.
- **Expiry.** Both claims expire 2026-12-28 and appear on the watchlist above; re-verify in the quarterly audit before any reuse.
