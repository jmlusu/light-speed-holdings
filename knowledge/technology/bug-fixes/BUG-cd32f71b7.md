# fix(deck): correct unsupported compliance statements

**ID:** BUG-cd32f71b7
**Date:** 2026-10-25
**Resolved:** resolved
**Commit:** cd32f71b774c53d024c8453bd53ead5b480e946d
**Issue:** none — found by legal review during the deck restructure (PR #522)

## Original Issue Body

No issue was filed. The defect surfaced during a legal audit of the 11-slide investor deck: six statements asserted capabilities or legal postures that no artefact in the repository supports.

## Root Cause

The deck's compliance language was carried over from template text and never traced to a source. The deck gate did not catch it for three structural reasons:

1. **`verify-deck.py` V09 only checks figures.** It matches numbers against `display` strings in `docs/claims.yaml`. Free-text claims like "SOC 2 readiness" contain no digits, so V09 has nothing to match.
2. **`docs/claims.yaml:223,226` files "SOC 2" and "GDPR" under `structural:`** — a layout-constants section with no `status:` field — so V10's source check never evaluates them. This gap is already recorded as accepted at `docs/deck-gate/KNOWN-GAPS.md:18`.
3. **`Malawi DPA 2017` was simply the wrong statute.** The operative act is the Data Protection Act 2024 (Act No. 3 of 2024), in force 3 June 2024 (`docs/marketing/newsletter/monitor-01.md:61`). Nothing in the pipeline could detect a stale legal citation.

Net effect: a deck could pass all twelve structural checks while naming the wrong law and claiming a certification nobody had performed.

## Fix

Removed or corrected six statements in `static/brand/templates/generate-pitch-deck.py`:

| Was | Now | Grounds |
|---|---|---|
| `Malawi DPA 2017, GDPR opinion, SOC 2 readiness` (Risks) | `Built to DPA 2024 and GDPR-grade handling; SOC 2 planned, not certified` | Wrong statute; no GDPR opinion exists (`CEO-DIRECTIVE-BLUEPRINT-ADOPTION.md:179` is a budget line to buy one); SOC 2 is an unchecked task |
| `Compliance — Malawi DPA 2017, GDPR, SOC 2 readiness` (Ask) | `Compliance — DPA 2024 alignment, GDPR opinion, SOC 2 prep` | Same, phrased as forward-looking spend |
| `Governance gates operating under audit` (Ask) | `Governance gates live with tamper-evident audit trail` | No external audit engagement exists |
| `Human approval gates ratified` (Traction) | `Human approval gates enforced in code` | Tiers 0–4 are enforced pre-execution (`src/ai_company/executor/tool_runner.py:18-19,463`); "ratified" was self-ratification |
| `agent registry in production` (Traction) | `Platform built, running this company internally` | Nothing is in production without a client |

Two statements were verified as genuinely backed and left unchanged: the five-tier approval matrix (`src/ai_company/orchestrator/tier_rules.py:1-10,29-35`) and the hash-chained audit trail (`src/ai_company/audit/integrity.py:1-6`).

## Files Changed

- `static/brand/templates/generate-pitch-deck.py` — five string corrections
- `static/brand/templates/pitch-deck.pptx` — regenerated

## Diagnostic Commands

```powershell
# find the offending strings
Select-String -Path static\brand\templates\generate-pitch-deck.py -Pattern "DPA 2017|SOC 2|GDPR|in production|ratified|under audit"

# confirm the statute
Select-String -Path docs\marketing\newsletter\monitor-01.md -Pattern "DPA 2024|Act No. 3"

# confirm no attestation or audit exists
Select-String -Path docs\sop\legal-sop.md -Pattern "SOC 2"
```

## Verification

```powershell
uv run ruff check static/brand/templates/generate-pitch-deck.py   # clean
uv run --with python-pptx --with lxml python static/brand/templates/generate-pitch-deck.py
uv run --with pyyaml python scripts/deck-gate/verify-deck.py `
  static/brand/templates/pitch-deck.pptx --root . --slides 11 `
  --logo-slides 1 --rail-exempt 1 --logo-dir brand/logo --logo-dir static/brand/logo `
  --skip-qa
# V01-V12 PASS, V13 SKIPPED, exit 2 INCOMPLETE (no verified claims), 11 slides
```

Rendered to PDF and extracted the text layer to confirm the new strings appear as intended on slides 7, 10 and 11.

## Residual

The gate still cannot catch unbacked prose claims — it checks numbers, not nouns. Two follow-ups recorded in `docs/deck-open-decisions.md`: move the `SOC 2` / `GDPR` entries out of `structural:` in `claims.yaml` so V10 evaluates them, and add a prose-claim review to the deck QA verdict (V13), which requires a human.

## Link an Issue

Fixed as part of PR #522.
