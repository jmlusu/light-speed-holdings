# QA Report ,  Post 8: AI Governance in Malawi

**Generated:** 2026-09-28
**QA Gate:** `ls-artifact-qa` (visual / brand / UX / accessibility / content)

## Five-Pass Verdict Table

| Pass | Verdict | Notes |
|------|---------|-------|
| Visual QA | PENDING RENDER | Copy complete for 4-card set (Reservations → Answers → Policy → Adoption) per plan §4; PNGs not yet generated |
| Brand QA | PENDING RENDER | Copy carries no palette/type assets; enforcement applies at render (80/10/10, Arial scale, official logos, tagline) |
| UX QA | PASS (copy) | One primary CTA (end card); cards follow 4-card narrative with single dominant idea each |
| Accessibility QA | PENDING RENDER | Contrast measurement + alt-text binding occur at render/post level |
| Content QA | PASS | Every claim traceable per `research-evidence.md`; excluded claims absent; no emojis; builder register |

**VERDICT (copy): APPROVE ,  render + re-run required before schedule (G3/G6 gate). Em dashes: 0 occurrences. Unslop rule 13 satisfied (draft and all supporting files enforced).**

## Content QA Detail

- [x] Four reservations framed as design requirements, not arguments (matches Reservations Playbook structure)
- [x] Card copy traceable to `post-08/carousel-copy.md` ,  4 content cards + CTA end card
- [x] Tier sequence `autonomous → HITL-approved → reviewed → snoozed → cleared` exact per ADR-017
- [x] DPA 2017/2024 cited as statute, not paraphrased beyond source; no penalty amounts or MACRA positions attributed
- [x] No invented statistics (+30% productivity, SME leapfrog, subscriber projections all absent)
- [x] No emojis; builder register; first-person plural for company work
- [x] Framework layer G named in draft header and hook ("G (Governance)")
- [x] Malawi/SADC context present (DPA, MACRA, National AI Strategy, SADC framework, UNDP)
- [x] `™` on first company mention ("LightSpeed Holdings Limited™" in draft hook)
- [x] CTA: Download the Malawi Agentic AI Monitor (standard series CTA)
- [x] Hashtags: 5 (#AgenticAI #AIGovernance #Malawi #SADC #DigitalTransformation)
- [x] Length: draft within 1,200–1,800 word spec (10.7 KB markdown ≈ 1,500 words)
- [x] CEO review status: pending batch (Posts 4–11 submitted together; only Posts 1–3 approved via CEO-review-batch-1.md 2026-09-28)

## Brand QA Checklist (pre-render)

- [ ] Palette 80% navy / 10% red / 10% cyan at `--tolerance 3` → 100% on-palette
- [ ] Arial type scale (36/32/28/24/18/16/14/13/12pt)
- [ ] Official logos only (`icononly_transparent.png` on navy / `fulllogo_transparent.png` on white)
- [ ] Tagline "ASPIRE. ACT. ACHIEVE." exact on navy surfaces
- [ ] Dimensions 1200×627 per card

## Accessibility QA (at render)

- [ ] Contrast ≥ 4.5:1 body / ≥ 3:1 large text on all pairs
- [ ] Color not the only signal (chips carry labels, indicators numeric)
- [ ] Alt text bound at post level: hero = "AI Governance in Malawi"; cards mirror titles

## Visual QA (at render)

- [ ] Hierarchy: one dominant element per card
- [ ] 4px-grid spacing, 64px inset, no clipping/overflow
- [ ] Part indicators `n / 4` on every card

## Notes

- Post 8 is a policy-edition post: copy approved for CEO review; visuals follow the plan's Post 8 spec (4-card Reservations→Answers→Policy→Adoption; 4-quadrant Reservations vs Engineering; timeline Strategy→Act→Law).
- Render + `ls-artifact-qa` re-run required before enqueue (Phase Gate: VISUALS → QA → SCHEDULE).

**QA Gate:** `ls-artifact-qa` ,  copy **APPROVE**, render **PENDING**
**Review Date:** 2026-09-28