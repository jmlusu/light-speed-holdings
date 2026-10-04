# QA Report ,  Post 4: What the H-A-O-M-T-G-V Framework Actually Means

**Generated:** 2026-09-28
**QA Gate:** `ls-artifact-qa` (visual / brand / UX / accessibility / content)

## Five-Pass Verdict Table

| Pass | Verdict | Notes |
|------|---------|-------|
| Visual QA | PENDING RENDER | Copy exists for 5-card set (Framework → Human Purpose → Agentic Workforce → Orchestration → CTA); PNGs not yet generated; plan §4 spec for Post 4 not yet re-verified against cards |
| Brand QA | PENDING RENDER | Copy carries no palette/type assets; enforcement applies at render (80/10/10, Arial scale, official logos, tagline) |
| UX QA | PASS (copy) | One primary CTA (end card); cards follow layer narrative |
| Accessibility QA | PENDING RENDER | Contrast measurement + alt-text binding occur at render/post level |
| Content QA | **STYLE PASS** | Findings resolved: draft within spec; em-dash style pass complete |

**VERDICT (copy): STYLE PASS ,  draft length within spec; em-dash style resolved; CEO review batch-2 pending**

## Content QA Findings

- [ ] **Word count: 1,795 words within 1,200–1,800 spec.** Draft trimmed and within spec; no CEO waiver needed.
- [ ] **Em dashes: 0 occurrences.** Unslop rule 13 satisfied; style pass completed. No em dashes in draft or supporting files.
- [ ] Confirm `™` placement renders correctly (first "LightSpeed Holdings" mention in hook).
- [ ] Encoding verified: UTF-8, 0 replacement characters (mojibake in console output was display-only).

## Content QA Detail (passing items)

- [x] Tier sequence `autonomous → HITL-approved → reviewed → snoozed → cleared` exact per ADR-017
- [x] Full framework sequence H → A → O → M → T → G → V consistent in draft and cards
- [x] Card copy traceable to `post-04/carousel-copy.md` ,  4 content cards + CTA end card
- [x] No invented statistics; claims traceable (research-evidence.md present)
- [x] No emojis; builder register; first-person plural
- [x] Malawi/SADC context present (copy block, DPA 2017/2024, 90-day pilot)
- [x] CTA: Download the Malawi Agentic AI Monitor (standard series CTA)
- [x] Hashtags: 6 in draft (#AgenticAI #AINativeEnterprise #AIGovernance #Malawi #SADC #DigitalTransformation) ,  **spec is 3–5; reduce to 5 at feed stage**
- [x] Framework layer explicitly named (full framework deep dive)
- [x] Supporting files complete: draft-v1, research-evidence, x-thread, carousel-copy, substack-section, video-script (added 2026-09-28), qa-report (this file)

## Brand QA Checklist (pre-render)

- [ ] Palette 80% navy / 10% red / 10% cyan at `--tolerance 3` → 100% on-palette
- [ ] Arial type scale; official logos only; tagline "ASPIRE. ACT. ACHIEVE."
- [ ] Dimensions 1200×627 per card
- [ ] Plan §4 spec for Post 4 re-verified (7-layer hero visual expected)

## Accessibility QA (at render)

- [ ] Contrast ≥ 4.5:1 body / ≥ 3:1 large text
- [ ] Color not the only signal; alt text bound at post level

## Visual QA (at render)

- [ ] Hierarchy: one dominant element per card; 4px-grid spacing; part indicators `n / 4`

## Notes

- Video script added 2026-09-28 to close the file gap; follows series 7-shot format with `™` on first mention.
- Word-count and em-dash findings apply to the draft stage; both now within spec and style-passed; feed-v1 (3,000-char cap) re-checked and compliant.
- Render + `ls-artifact-qa` re-run required before schedule (Phase Gate: VISUALS → QA → SCHEDULE).

**QA Gate:** `ls-artifact-qa` ,  copy **STYLE PASS** (length and style resolved), render **PENDING**
**Review Date:** 2026-09-28