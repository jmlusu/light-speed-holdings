# QA Report ,  Post 10: What Should an AI Agent Decide?

**Generated:** 2026-09-28
**QA Gate:** `ls-artifact-qa` (visual / brand / UX / accessibility / content)

## Five-Pass Verdict Table

| Pass | Verdict | Notes |
|------|---------|-------|
| Visual QA | PENDING RENDER | Copy complete for 4-card set (Human-only â†’ Shared â†’ Agent-only â†’ Forbidden) per plan Â§4; PNGs not yet generated |
| Brand QA | PENDING RENDER | Copy carries no palette/type assets; enforcement applies at render (80/10/10, Arial scale, official logos, tagline) |
| UX QA | PASS (copy) | One primary CTA (end card); 4-card tier narrative with single dominant idea per card; RACI heatmap + pie planned per plan Â§4 at render |
| Accessibility QA | PENDING RENDER | Contrast measurement + alt-text binding occur at render/post level |
| Content QA | PASS | Every claim traceable per `research-evidence.md`; excluded claims absent; no emojis; builder register |

**VERDICT (copy): APPROVE ,  render + re-run required before schedule (G3/G6 gate)**

## Content QA Detail

- [x] Tier sequence `autonomous â†’ HITL-approved â†’ reviewed â†’ snoozed â†’ cleared` exact per ADR-017 (draft, table, substack, video script)
- [x] Tiers attach to action classes, not agents ,  stated in draft, thread, cards, video
- [x] Tier-5 forbidden list consistent across draft/substack: secret exfiltration, self-modifying governance, unauthorized tier changes, irreversible external commitments without co-signature
- [x] Approval sweep PENDING â†’ EXPIRED terminal semantics per AGENTS.md Â§9.1
- [x] Seven-tool vocabulary exact: read, edit, grep, list, bash, webfetch, task (AGENTS.md Â§8)
- [x] RACI table flagged as series synthesis in research-evidence (not attributed to a repo artifact)
- [x] Duplicate "M ,  Models Run Sovereign" section removed during drafting (edit applied)
- [x] Card copy traceable to `post-10/carousel-copy.md` ,  4 content cards + CTA end card
- [x] No invented statistics; no regulatory positions attributed; no "first/unique" claims
- [x] No emojis; builder register; first-person plural for company work
- [x] Framework layer G named in draft header and hook ("G (Gates Approve)")
- [x] Malawi/SADC context present (copy blocks, regulator framing, CTA)
- [x] CTA: Download the Malawi Agentic AI Monitor (standard series CTA)
- [x] Hashtags: 5 (#AgenticAI #AIGovernance #DecisionRights #Malawi #SADC)
- [x] Length: draft within 1,200â€“1,800 word spec
- [x] CEO review status: pending batch (Posts 8â€“11 submitted together)

## Voice Exception Flagged for CEO

- [ ] **`â„¢` usage:** first body mention is "building LightSpeed" (Post 11 teaser) ,  not the full "LightSpeed Holdings" form; video script carries the required `â„¢` placement. Flag for CEO: add an explicit "LightSpeed Holdingsâ„¢" mention in the LinkedIn body or accept video-only placement.

## Brand QA Checklist (pre-render)

- [ ] Palette 80% navy / 10% red / 10% cyan at `--tolerance 3` â†’ 100% on-palette
- [ ] Arial type scale (36/32/28/24/18/16/14/13/12pt)
- [ ] Official logos only; tagline "ASPIRE. ACT. ACHIEVE." exact on navy surfaces
- [ ] Dimensions 1200Ã—627 per card
- [ ] Plan Â§4 extras: RACI heatmap visual; pie showing % of decisions by tier

## Accessibility QA (at render)

- [ ] Contrast â‰¥ 4.5:1 body / â‰¥ 3:1 large text (tier numbers 1â€“5 need large-text check)
- [ ] Color not the only signal (tier color paired with tier name labels ,  verify at render)
- [ ] Alt text bound at post level: hero = "What should an AI agent decide"; cards mirror titles

## Visual QA (at render)

- [ ] Hierarchy: one dominant element per card
- [ ] 4px-grid spacing, 64px inset, no clipping/overflow (Tier-5 wall card is text-dense ,  watch wrap)
- [ ] Part indicators `n / 4` on every card

## Notes

- Post 10 visual spec (plan Â§4): hero decision matrix; 4 cards Human-onlyâ†’Sharedâ†’Agent-onlyâ†’Forbidden; RACI heatmap; pie % of decisions by tier.
- Render + `ls-artifact-qa` re-run required before enqueue (Phase Gate: VISUALS â†’ QA â†’ SCHEDULE).

**QA Gate: ls-artifact-qa, copy STYLE PASS, render PENDING**, render **PENDING**
**Review Date:** 2026-09-28
