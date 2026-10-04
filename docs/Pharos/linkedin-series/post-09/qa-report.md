# QA Report ,  Post 9: Measuring AI-native Organizations

**Generated:** 2026-09-28
**QA Gate:** `ls-artifact-qa` (visual / brand / UX / accessibility / content)

## Five-Pass Verdict Table

| Pass | Verdict | Notes |
|------|---------|-------|
| Visual QA | PENDING RENDER | Copy complete for 4-card set (Input → Process → Output → Outcome) per plan §4; PNGs not yet generated |
| Brand QA | PENDING RENDER | Copy carries no palette/type assets; enforcement applies at render (80/10/10, Arial scale, official logos, tagline) |
| UX QA | PASS (copy) | One primary CTA (end card); 4-card chain narrative, one dominant idea per card; part indicators `n / 4` planned at render |
| Accessibility QA | PENDING RENDER | Contrast measurement + alt-text binding occur at render/post level |
| Content QA | PASS | Every claim traceable per `research-evidence.md`; excluded claims absent; no emojis; builder register |

**VERDICT (copy): APPROVE ,  render + re-run required before schedule (G3/G6 gate)**

## Content QA Detail

- [x] KPI-003 formula and values cited verbatim from `config/company/kpis.yaml` (target 80, current 1.5 snapshot, source `.opencode/inbox.json + company-registry.yaml`)
- [x] KPI-004 cited verbatim (target 99.5, current 100.0)
- [x] Null KPIs (KPI-001/002/005) described accurately as `current: null` rendering "n/a"
- [x] CEO 2026-08-08 real-sources decision attributed correctly (recorded in `kpis.yaml` header)
- [x] ADR-032 registry role as denominator described accurately
- [x] Tier sequence `autonomous → HITL-approved → reviewed → snoozed → cleared` exact per ADR-017
- [x] Card copy traceable to `post-09/carousel-copy.md` ,  4 content cards + CTA end card
- [x] No invented statistics; no benchmark comparisons; no subscriber results (series not yet published, #194)
- [x] No emojis; builder register; first-person plural for company work
- [x] Framework layer V named in draft header and V section ("V ,  Value & Impact")
- [x] Malawi/SADC context present in copy blocks and CTA
- [x] CTA: Download the Malawi Agentic AI Monitor (standard series CTA)
- [x] Hashtags: 5 (#AgenticAI #AINativeEnterprise #ValueImpact #Malawi #SADC)
- [x] **1,792 words within 1,200‑1,800 spec.**
- [ ] Em dashes: 0 occurrences. Unslop rule 13 satisfied (draft and all supporting files enforced).
- [x] **CEO review: pending batch (Posts 4‑11 submitted together; only Posts 1‑3 approved via CEO-review-batch-1.md 2026‑09‑28).**
- [x] CEO review status: pending batch (Posts 8–11 submitted together)

## Voice Exception Flagged for CEO

- [ ] **`™` usage:** Post 9 draft contains no company mention in the body; `™` rule applies only on first mention. Video script carries the required `™`. Flag for CEO preference: add an explicit company mention in the LinkedIn body or accept video-only placement.

## Brand QA Checklist (pre-render)

- [ ] Palette 80% navy / 10% red / 10% cyan at `--tolerance 3` → 100% on-palette
- [ ] Arial type scale (36/32/28/24/18/16/14/13/12pt)
- [ ] Official logos only; tagline "ASPIRE. ACT. ACHIEVE." exact on navy surfaces
- [ ] Dimensions 1200×627 per card; sparkline 90-day trend visual per plan §4

## Accessibility QA (at render)

- [ ] Contrast ≥ 4.5:1 body / ≥ 3:1 large text (data-viz numerals need large-text check: 1.5% / 80% / 100% displays)
- [ ] Color not the only signal (trend ticks carry labels; nulls rendered as text "n/a")
- [ ] Alt text bound at post level: hero = "Measuring AI-native organizations"; cards mirror titles

## Visual QA (at render)

- [ ] Hierarchy: one dominant element per card
- [ ] 4px-grid spacing, 64px inset, no clipping/overflow (KPI rows are text-dense ,  watch wrap)
- [ ] Part indicators `n / 4` on every card

## Notes

- Post 9 visual spec (plan §4): hero "Measurement dashboard"; 4 cards Input→Process→Output→Outcome; OKR tree diagram Org→Dept→Agent→Human; 90-day sparkline.
- Render + `ls-artifact-qa` re-run required before enqueue (Phase Gate: VISUALS → QA → SCHEDULE).

**QA Gate:** `ls-artifact-qa` ,  copy **STYLE PASS**, render **PENDING**
**Review Date:** 2026-09-28