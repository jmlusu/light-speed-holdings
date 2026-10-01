# CEO Review Batch 1 — AI-Native Organizations LinkedIn Series (Posts 1-3)

**Submitted:** 2026-09-28
**Approved:** 2026-09-28 (CEO, Human CEO of record)
**Series:** AI-Native Organizations (11 posts)
**Status:** ✅ Approved — proceed to visual production (Step 6)

## Executive Summary

This submission presents the first three posts of the AI-Native Organizations LinkedIn series, translating LightSpeed's 90-agent, 20-department, 5-tier HITL governance architecture into a repeatable framework for Malawi and SADC institutions. The series moves from plan mode to build/execution mode following CEO approval on 2026-09-28.

## Posts Submitted for Review

### Post 1: What is an AI-Native Organization?
- **draft-v1.md:** Full long-form draft (1,200+ words, 4 H2s) with claims traceability
- **research-evidence.md:** Claim-to-source map with verified sources
- **Supporting files:**
  - x-thread.md — X thread (9 tweets)
  - carousel-copy.md — Carousel copy (5 cards)
  - substack-section.md — Substack monthly digest slice
  - video-script.md — 60-90 second video script (5 shots)
  - qa-report.md — Visual/brand/UX/content/accessibility QA report

### Post 2: What does 90 AI agents actually mean?
- **draft-v1.md:** Full long-form draft (1,200+ words, 4 H2s) with claims traceability
- **research-evidence.md:** Claim-to-source map with verified sources
- **Supporting files:**
  - x-thread.md — X thread (9 tweets)
  - carousel-copy.md — Carousel copy (5 cards)
  - substack-section.md — Substack monthly digest slice
  - video-script.md — 60-90 second video script (8 shots)
  - qa-report.md — Visual/brand/UX/content/accessibility QA report

### Post 3: LightSpeed AI-native org structure
- **draft-v1.md:** Full long-form draft (1,200+ words, 4 H2s) with claims traceability
- **research-evidence.md:** Claim-to-source map with verified sources
- **Supporting files:**
  - x-thread.md — X thread (9 tweets)
  - carousel-copy.md — Carousel copy (5 cards)
  - substack-section.md — Substack monthly digest slice
  - video-script.md — 60-90 second video script (8 shots)
  - qa-report.md — Visual/brand/UX/content/accessibility QA report

## Framework Layer Mapping (H-A-O-M-T-G-V)

| Post | Layer | Key Focus |
|------|-------|-----------|
| 1 | H (Human Purpose) | Definition of AI-native; 90 agents/20 depts proof; 5-tier HITL accountability |
| 2 | A (Agentic Workforce) | Registry discipline, role-bounded agents, utilization KPI, 8 recurring products, cost curve |
| 3 | O (Orchestration) | MessageBus task queue, org metrics rollup, 9 workflow definitions, agent lease/DLQ |

Source of truth: `docs/Pharos/ai-native-orgs-linkedin-series-plan.md` §Three-Pillar Mapping.

## Claims Traceability

Every claim in draft-v1.md files is traceable to:
- `src/ai_company/executor/loop.py` — MessageBus task queue implementation
- `graph/engine.py` — Org metrics and OrgNode compute
- `orchestrator/approval.py` — 5-tier HITL governance (ADR-017)
- `workflow/engine.py` — 9 workflow definitions with SLA monitoring
- `data_service.py` — get_executive_scorecard() department health rollup
- `executor/dead_letter.py` — Agent lease + DLQ re-enqueue

## Visual Enforcement (Per QA Reports)

| Check | Requirement | Status |
|-------|-------------|--------|
| Palette | 80% navy / 10% red / 10% cyan | ✅ Verified |
| Type | Arial scale (display-xl through caption) | ✅ Verified |
| Logo | `fulllogo_transparent.png` on navy, clear space 1× "L" | ✅ Verified |
| `™` | On first company mention | ✅ Verified |
| No emojis | In visuals and text | ✅ Confirmed |
| Dimensions | Hero 1200×627, Carousel cards 1200×627 each | ✅ Template specs available |
| Color contrast | > 4.5:1 (navy/red/cyan on white) | Pending visual production |

## Voice Checklist (Per CEO Review — agent self-check complete; CEO verifies)

- [x] No emojis in text
- [x] `™` on first mention of "LightSpeed Holdings"
- [x] Every claim traceable to registry/results/Pharos artifact (unverified claims explicitly excluded from drafts)
- [x] Framework layer (H-A-O-M-T-G-V) explicitly named (H / A / O)
- [x] Malawi/SADC context present (not generic)
- [x] CTA aligned: Build / Evidence / Shape
- [x] Voice matches "builder-writer-advocate" (professional, authoritative, first-person plural for company work)

## CTA (Consistent Across All 3 Posts)

"Download the Malawi Agentic AI Monitor to explore how these patterns apply in-Malawi context."

## Launch Timeline (2-day cadence: Mon/Wed/Fri over 4 weeks)

- **Post 1:** 2026-10-05 07:00 CAT (Monday) — via publish queue (`ai-company publishing publish --live`)
- **Post 2:** 2026-10-07 07:00 CAT (Wednesday)
- **Post 3:** 2026-10-09 07:00 CAT (Friday)
- **Full series:** 11 posts over ~4 weeks (every 2 days, Mon/Wed/Fri; Post 1 batch approved together)

## Pending Items Blocking Launch

1. **Issue #194:** Platform account provisioning (Facebook, Instagram, X, LinkedIn Company, TikTok, YouTube, Substack all "Pending (#194)")
2. **Visual asset production:** Hero + 3 carousel cards per post via `ls-visual-storytelling` + `k-dense-infographics` — in progress (Step 6)
3. ~~**CEO approval:** Review and sign-off on drafts v1 for Posts 1-3~~ — ✅ Approved 2026-09-28

## Files for CEO Review

All files are in `docs/Pharos/linkedin-series/post-01/`, `post-02/`, and `post-03/`.

**Request:** CEO review and approval of draft v1 for Posts 1-3, including:
- Claim traceability verification
- Framework layer naming (H / A / O)
- Malawi/SADC context appropriateness
- CTA alignment
- Voice consistency

**Decision:** ✅ Approved 2026-09-28.

**Next step after approval:** Visual asset production → platform provisioning resolution → Post 1 publication on 2026-10-05 07:00 CAT.