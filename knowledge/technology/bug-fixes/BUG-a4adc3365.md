# fix(site): remove unsupported client and performance claims

**ID:** BUG-a4adc3365
**Date:** 2026-10-26
**Resolved:** resolved
**Commit:** a4adc336514214aa1a950d0129443da93075b5a8
**Issue:** none — found during a claims audit after the investor deck review; fixed in `fix/site-false-claims`

## Original Issue Body

No issue was filed. Three statements on the public site and in the site registries
asserted delivered client work and measured performance that nothing in the repository
supports:

1. `ws-01` — "Malawi Central Bank Compliance Automation": a regional financial
   institution, 14 departments, 40% reduction in reporting time. Badged
   **Proven In-House** while its own text described a deployment.
2. `data/faqs/registry.ts:251` — defined `LIVE` as *"Paying client, measurable
   outcomes (currently: compliance automation for regional financial institution)"*.
3. A `97.4%` task-completion rate published as `proven-in-house`, with a
   94.0 → 97.4 series for 3–9 September 2026.

## Root Cause

Two causes, both structural rather than editorial.

**The claim had no single source of truth.** The same sentence is hand-maintained in
`data/*/registry.ts`, `src/data/registries/*.json`, `src/data/sectors*.ts` and
`packages/data-use-cases/src/registry.ts`. There is no generator and no drift check,
so one false sentence had to be edited in 14 files. A partial fix would have left the
claim live on another surface.

**Nothing in CI can tell a capability apart from a delivery.** The case study was
classified `PROVEN_IN_HOUSE` on the badge while its prose claimed a client outcome.
The registries accept both, and no guard compares prose against evidence. The same
gap that let the deck ship an unsupported SOC 2 statement (BUG-cd32f71b7) applies here.

Supporting evidence that the numbers are unsupported:

- `docs/client-facing/USE-CASE-CATALOG.md` records no delivered client work.
- `data/claims/registry.ts` `CLM-023` claimed `LIVE=1`; the only `LIVE` use case is
  `uc-js-bar` (J&S StopOver Bar), documented as **unpaid**.
- The repo contains no LOI, MOU, invoice, deposit or signed contract for this work —
  only blank templates (`docs/legal/msa-template.md`, `docs/sow-template.md`,
  `docs/templates/invoice.md`).
- `content/drafts/homepage.md:182` had already resolved the ambiguity:
  *"treat the 40% figure as PROVEN IN-HOUSE, not a client testimonial."*
- For the 97.4% figure: every table in `data/ai_company.db` has 0 rows and the
  hash-chained trail (`reports/evidence/audit-2026-10-0{1,3,4}.jsonl`) contains
  171 events but zero `task_completed`/`task_failed`, so no denominator exists.

Scope note, recorded because an earlier verbal report to the CEO overstated it: only
the case study was rendering publicly. The rendered FAQ was already corrected in
`#519` (`src/data/registries/faq-registry.json:408` answers *"Honestly: no…"*), and
`reports/website-contamination-audit.md:132` records `companyData.ts` as *"Not
bundled"*. Items 2 and 3 were latent, not live. They are fixed here so they cannot be
reused as evidence.

## Fix

Every change is a removal or a qualification. No new figure, client, date or outcome
was introduced.

| Was | Now |
|---|---|
| `ws-01` "Malawi Central Bank Compliance Automation", 14 departments, 40% faster | "Regulatory Reporting Automation — Proven In-House": report assembly, validation, SHA-256 sealed audit trail. No client, department count or percentage |
| Financial-services `evidence` / `honestyNote`: "for a regional financial institution … cutting reporting time by 40%" | "proven in LightSpeed's own operations: 5-tier approval gating and SHA-256 sealed audit trails. No client deployment yet." |
| `claim.compliance-automation-40-percent` | `claim.compliance-automation-in-house`, new text and `evidenceRef`, `lastVerified 2026-10-26` |
| FAQ `LIVE`: "Paying client, measurable outcomes (… compliance automation for regional financial institution)" | "Running in a real organisation's operations (currently one: J&S StopOver Bar, unpaid)" |
| `CLM-023`: "LIVE=1, PROVEN_IN_HOUSE=multiple…" | Explicit status definitions ending "Paying clients: zero." |
| `97.4%` metric entry and its 94.0 → 97.4 history | removed from both registries |
| Image alt text: "regulatory reporting across 14 departments" | "regulatory report assembly with audit trails" |

## Files Changed

- `src/data/registries/use-case-registry.json` — `ws-01` title, problem, workflow, agents, inputs, output, business value
- `src/data/registries/sector-registry.json`, `src/data/sectors.ts`, `src/data/sector-registry.ts`, `data/sectors/registry.ts` — financial-services evidence / `honestyNote` / `keyMetrics`
- `src/data/registries/claims-registry.json` — claim id, text, `evidenceRef`, verification dates
- `src/data/siteContent.ts` — `proofCaseStudies[ws-01]`, `outcomeCategories[oc-01]`
- `data/use-cases/registry.ts`, `packages/data-use-cases/src/registry.ts` — package copies of the case study
- `data/faqs/registry.ts`, `data/claims/registry.ts` — `LIVE` definition, `CLM-023`
- `data/media/registry.ts` — image alt text
- `data/metrics/registry.ts`, `src/data/companyData.ts` — 97.4% entries removed

## Diagnostic Commands

```powershell
# every surviving copy of the claim
Get-ChildItem src,data,packages -Recurse -Include *.ts,*.tsx,*.json -File |
  Select-String -Pattern "regional financial institution|14 departments|Malawi Central Bank|40% reduction|97\.4|Paying client, measurable"

# confirm no client instrument exists
Get-ChildItem docs -Recurse -Include *.md |
  Select-String -Pattern "invoice|deposit|signed" | Select-Object -First 20

# confirm the metrics database has no denominator
uv run python -c "import sqlite3; c=sqlite3.connect('data/ai_company.db'); print([(t, c.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]) for (t,) in c.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")])"

# confirm #519 already fixed the rendered FAQ
Select-String -Path src\data\registries\faq-registry.json -Pattern "paying-client"
```

## Verification

```powershell
npx vitest run                       # 15 files, 140 tests passed
npm run build                        # tsc --noEmit && vite build — success
uv run python scripts/test/check-vercelignore.py   # 24 build-critical paths survive; 5 junk paths excluded
# residual sweep: no match for any of the six patterns above
```

CI: Site Build + Principles Gate, Test (ubuntu/windows), E2E.

## Known, deliberately not fixed

1. `UseCaseStatus` declares `'PROVEN_IN_HOUSE'` (`src/data/use-cases/registry.ts:3`)
   while the data uses `"PROVEN IN-HOUSE"` with a space, so
   `getUseCasesByStatus('PROVEN_IN_HOUSE')` returns `[]`. Normalising the data is a
   behaviour change, not a claim removal.
2. No generator or drift check unifies the duplicated registries. This fix needed 14
   files for one sentence.
3. `vite.config.ts:52-58` aliases `@lightspeed/data/*` to `data/*` while
   `tsconfig.json:24-30` maps the same aliases to `src/data/*`; nothing imports the
   aliases, which is how the stale FAQ claim survived `#519`.
