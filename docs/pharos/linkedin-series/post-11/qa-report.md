# QA Report ,  Post 11: Lessons From Building LightSpeed

**Generated:** 2026-09-28
**QA Gate:** `ls-artifact-qa` (visual / brand / UX / accessibility / content)

## Five-Pass Verdict Table

| Pass | Verdict | Notes |
|------|---------|-------|
| Visual QA | PENDING RENDER | Copy complete for 4-card set (Start â†’ Breakthrough â†’ Lesson â†’ Future) per plan Â§4; PNGs not yet generated |
| Brand QA | PENDING RENDER | Copy carries no palette/type assets; enforcement applies at render (80/10/10, Arial scale, official logos, tagline) |
| UX QA | PASS (copy) | One primary CTA (end card); 4-card narrative arc with single dominant idea per card; Gantt 2024â€“2026 + counter 90/20/0 planned per plan Â§4 at render |
| Accessibility QA | PENDING RENDER | Contrast measurement + alt-text binding occur at render/post level |
| Content QA | PASS | Every claim traceable per `research-evidence.md`; excluded claims absent; no emojis; builder register |

**VERDICT (copy): APPROVE ,  render + re-run required before schedule (G3/G6 gate)**

## Content QA Detail

- [x] First-person singular voice throughout (series designated Post 11 lessons voice)
- [x] ADR-032 consolidation 152 â†’ 90 stated exactly; framed as precondition, not cleanup
- [x] Tier sequence `autonomous â†’ HITL-approved â†’ reviewed â†’ snoozed â†’ cleared` exact per ADR-017
- [x] KPI honesty pair cited verbatim: KPI-003 1.5 vs 80; nulls render "n/a"; CEO 2026-08-08 real-sources decision
- [x] Scheduler reliability failure narrated qualitatively ,  no incident count or date attached (per research-evidence exclusions)
- [x] Six lessons consistent across draft / thread / cards / substack / video
- [x] Inversion recommendation framed as personal counsel, not existing program
- [x] Full framework sequence H â†’ A â†’ O â†’ M â†’ T â†’ G â†’ V consistent in draft, cards, substack, video
- [x] Card copy traceable to `post-11/carousel-copy.md` ,  4 content cards + CTA end card
- [x] No revenue/customer/funding figures; no "first in Malawi/Africa" claims; no series performance results (#194 pending)
- [x] No emojis; builder register
- [x] Framework layer H named in draft header and hook ("H ,  Humans Authorize (series close)")
- [x] Malawi/SADC context present (hook, inversion counsel, CTA)
- [x] CTA: Download the Malawi Agentic AI Monitor (standard series CTA)
- [x] Hashtags: 5 (#AgenticAI #AINativeEnterprise #Malawi #SADC #StartupLessons)
- [x] Length: draft within 1,200â€“1,800 word spec
- [x] CEO review status: pending batch (Posts 8â€“11 submitted together)

## Voice Exception Flagged for CEO

- [ ] **`â„¢` usage:** body uses short form "LightSpeed" in title and closing sections; full "LightSpeed Holdings Limitedâ„¢" appears in video script only. Flag for CEO: add explicit full-name `â„¢` mention in LinkedIn body or accept video-only placement.

## Brand QA Checklist (pre-render)

- [ ] Palette 80% navy / 10% red / 10% cyan at `--tolerance 3` â†’ 100% on-palette
- [ ] Arial type scale (36/32/28/24/18/16/14/13/12pt)
- [ ] Official logos only; tagline "ASPIRE. ACT. ACHIEVE." exact on navy surfaces
- [ ] Dimensions 1200Ã—627 per card
- [ ] Plan Â§4 extras: Gantt 2024â€“2026 timeline; counter visual 90 agents / 20 depts / 0 downtime

## Accessibility QA (at render)

- [ ] Contrast â‰¥ 4.5:1 body / â‰¥ 3:1 large text (counter numerals 90/20 need large-text check)
- [ ] Color not the only signal (lesson chips carry labels; counters carry units)
- [ ] Alt text bound at post level: hero = "Lessons from building LightSpeed"; cards mirror titles

## Visual QA (at render)

- [ ] Hierarchy: one dominant element per card
- [ ] 4px-grid spacing, 64px inset, no clipping/overflow (six-lesson card is text-dense ,  watch wrap)
- [ ] Part indicators `n / 4` on every card

## Notes

- Post 11 visual spec (plan Â§4): hero "Lessons learned timeline"; 4 cards Startâ†’Breakthroughâ†’Lessonâ†’Future; Gantt 2024â€“2026; counter 90 agents / 20 departments / 0 downtime.
- Series close: after Post 11 render + QA, next phase is sector deep-dives per plan roadmap.
- Render + `ls-artifact-qa` re-run required before enqueue (Phase Gate: VISUALS â†’ QA â†’ SCHEDULE).

**QA Gate: ls-artifact-qa, copy STYLE PASS, render PENDING**, render **PENDING**
**Review Date:** 2026-09-28
