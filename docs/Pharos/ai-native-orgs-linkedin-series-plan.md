# LinkedIn Series Plan: "AI-Native Organizations" (11 Posts)

**Owner:** `thought_leadership_lead` (Pharos)
**Status:** PLAN MODE — not executed
**Date:** 2026-09-24
**Target Launch:** Post-manifesto approval (CEO sign-off pending)

---

## 1. Content Strategy & Voice Alignment

### Core Thesis (1–2 sentences)
> **LightSpeed Holdings operates a live AI-native enterprise (90 agents, 20 departments, 5-tier HITL governance). This series translates our architecture into a repeatable framework for Malawi and SADC institutions: how to design, govern, and deploy organizations where AI agents perform meaningful work while humans remain accountable.**

### CEO Voice: "Builder-Writer-Advocate"
| Dimension | Manifestation |
|-----------|---------------|
| **Builder** | Lead with proof: "We built X. Here's the architecture. Here's the cost. Here's what broke." |
| **Writer** | Evidence-led prose. No emojis. No hype. Claims traceable to registry, results, or published Pharos artifacts. |
| **Advocate** | Frame for institutional SADC audience (ministries, SADC secretariat, UNDP, banks, ICTAM). Policy-ready language. |
| **Tone** | Professional register, authoritative but not academic. First-person plural ("We built...") for company work; first-person singular for CEO reflections. |
| **Tagline** | `™` on first mention: "LightSpeed Holdings Limited™" |
| **Hashtag Set** | `#AgenticAI #AINativeEnterprise #AIGovernance #Malawi #SADC #DigitalTransformation` (3–5 per post) |

### Three-Pillar Mapping (Every Post Maps 1:1)

| Post | Primary Pillar | Secondary Pillar | Framework Layer (H-A-O-M-T-G-V) |
|------|----------------|------------------|----------------------------------|
| 1: What is an AI-Native Organization? | Company Builder | Policy | Human Purpose (H) |
| 2: What does 90 AI agents actually mean? | Company Builder | Use Cases | Agentic Workforce (A) |
| 3: LightSpeed AI-native org structure | Company Builder | — | Orchestration (O) |
| 4: H→A→O→M→T→G→V deep dive | Company Builder | Policy | Full Framework |
| 5: AI agents for Malawian SMEs | Use Cases | Company Builder | Value & Impact (V) |
| 6: Agentic AI in health & M&E | Use Cases | Policy | Tools & Actions (T) |
| 7: Agentic AI & financial inclusion | Use Cases | Policy | Governance (G) |
| 8: AI governance in Malawi | Policy | Company Builder | Governance (G) |
| 9: Measuring AI-native organizations | Company Builder | Policy | Value & Impact (V) |
| 10: What should an AI agent decide? | Policy | Company Builder | Governance (G) |
| 11: Lessons from building LightSpeed | Company Builder | Use Cases | Human Purpose (H) |

---

## 2. Artifact Creation Workflow

### Phase Gate Model (Per Post)

```
RESEARCH → DRAFT → CEO REVIEW → VISUALS → QA → SCHEDULE → PUBLISH → MEASURE
```

### Detailed Workflow (Per Post)

| Step | Owner | Tool/Skill | Output | Gate |
|------|-------|------------|--------|------|
| **1. Research Brief** | `agentic_research_lead` | `k-dense-research-lookup` + webfetch | Evidence matrix + claim-to-source map (1–2 hrs) | — |
| **2. Draft v1** | `thought_leadership_author` | CEO voice profile (semantic memory) | LinkedIn long-form (1,200–1,800 words) | Internal QA |
| **3. CEO Review** | Human CEO | Async (GitHub PR / shared doc) | Approved / revisions requested | **HITL Gate** |
| **4. Visual Production** | `ls-visual-storytelling` + `k-dense-infographics` | Brand-enforced infographics/diagrams | 1 hero visual + 3 carousel cards per post | `ls-artifact-qa` |
| **5. Atomization** | `thought_leadership_author` + `content_creator` | `ls-social-media-design` | X thread, LinkedIn carousel, Substack newsletter section, 1-min video script | — |
| **6. Final QA** | `ls-artifact-qa` | Playwright probe + brand checklist | APPROVE / FIX → re-render | **Mandatory Gate** |
| **7. Schedule** | `thought_leadership_lead` | Pharos publish queue (MCP) | Queued with `scheduledAt` | — |
| **8. Publish** | Automated (P1 rail) | LinkedIn API / Substack RSS | Live post + cross-post | — |
| **9. Measure** | `marketing_kpi_collector` | Dashboard (24h, 7d, 30d) | Engagement, reach, clicks, subscriber delta | Weekly review |

### Artifact Checklist Per Post

| Asset | Format | Dimensions | Channel |
|-------|--------|------------|---------|
| Long-form article | Markdown → LinkedIn native | N/A | LinkedIn (CEO profile) |
| Carousel | 3–5 cards | 1200×627 each | LinkedIn (CEO + Company) |
| X/Twitter thread | 8–10 tweets | 1600×900 hero | X (CEO) |
| Substack section | Markdown | N/A | Substack (monthly digest) |
| Short video script | Text + shot list | 1080×1920 | Reels/TikTok/Shorts (Company) |
| Hero infographic | SVG/PNG | 1200×627 | All channels |
| Framework diagram | SVG | 1200×627 | LinkedIn article embed |

---

## 3. Reminder/Notification System Design (Every 2 Days)

### Architecture: Pharos Routine + MCP Publish Queue

```yaml
# config/company/scheduler.yaml addition
- id: linkedin_series_reminder
  name: "LinkedIn AI-Native Series Reminder"
  cron: "0 7 */2 * *"  # Every 2 days at 7:00 AM CAT
  timezone: "Africa/Blantyre"
  tags: ["pharos-routine", "linkedin-series", "reminder"]
  prompt_file: templates/pharos/routines/linkedin-series-reminder.md
  budget_tokens: 2000
  model_tier: standard
```

### Reminder Template (`templates/pharos/routines/linkedin-series-reminder.md`)

```markdown
# LinkedIn Series Reminder — {{series_post_number}}/11

**Series:** AI-Native Organizations
**Post {{series_post_number}}:** {{post_title}}
**Scheduled For:** {{publish_date}} (in {{days_until}} days)

## Status Check
- [ ] Research complete (evidence matrix linked)
- [ ] Draft v1 written
- [ ] CEO review: {{review_status}}
- [ ] Visuals produced & QA'd
- [ ] Atomized assets ready (X thread, carousel, Substack, video script)
- [ ] Scheduled in publish queue

## Action Required
{{#if ceo_review_pending}}
⚠️ **CEO REVIEW PENDING** — Draft shared {{days_since_share}} days ago. Escalate if >48h.
{{/if}}
{{#if visuals_pending}}
🎨 **Visuals needed** — Brief `ls-visual-storytelling` with creative brief.
{{/if}}

## Next Steps
1. {{next_action}}
2. Owner: {{next_owner}}
3. Deadline: {{next_deadline}}

## Series Progress
| Post | Title | Status | Publish Date |
|------|-------|--------|--------------|
| 1 | What is an AI-Native Organization? | {{status_1}} | {{date_1}} |
| 2 | What does 90 AI agents actually mean? | {{status_2}} | {{date_2}} |
...
| 11 | Lessons from building LightSpeed | {{status_11}} | {{date_11}} |
```

### Notification Channels

| Channel | Trigger | Recipient |
|---------|---------|-----------|
| **Inbox (MessageBus)** | Routine fires | `thought_leadership_lead`, `thought_leadership_author`, `agentic_research_lead` |
| **Email (Resend)** | CEO review >48h overdue | Human CEO, `chief_of_staff` |
| **Dashboard KPI** | Post published | Marketing dashboard (`posts_published_30d`) |
| **Slack/Teams (future)** | Manual escalation | Pharos team channel |

### Escalation Ladder

| Delay | Action | Owner |
|-------|--------|-------|
| 0–24h | Routine reminder (auto) | System |
| 24–48h | Email nudge to assignee | `thought_leadership_lead` |
| 48–72h | CEO escalation (if review gate) | `chief_of_staff` |
| >72h | Series pause — retrospective | Human CEO |

---

## 4. Visual Asset Requirements Per Post

### Visual System: LightSpeed Brand (navy `#070A40` / red `#E63946` / cyan `#00BFFF`)

| Post | Hero Visual | Carousel Cards | Diagram Type | Data Viz |
|------|-------------|----------------|--------------|----------|
| **1** | "AI-Native Org" definition framework | 3: Definition → Comparison → HAOMTGV intro | 2×2 matrix: Traditional vs AI-Native | Org chart: 90 agents → 20 depts |
| **2** | Agent registry visualization | 4: Agent types → Specialization → Reporting → Cost | Sankey: Human → Agent → Task → Value | Bar: 90 agents by dept |
| **3** | LightSpeed org chart (live) | 3: Depts → Reporting → Governance → Cadence | C4 container: Departments + agents | Tree: Exec → Specialists |
| **4** | HAOMTGV 7-layer framework | 7 cards (1 per layer) | Layered architecture diagram | Radar: Maturity per layer |
| **5** | SME case study (J&S StopOver) | 4: Problem → Agent → Result → Scale | Journey map: Manual → Agentic | KPI delta: Revenue/Cost/Time |
| **6** | Health M&E workflow | 4: Data → Agent → Alert → Report | Sequence diagram: Facility → Agent → Dashboard | Funnel: Cases → Detected → Resolved |
| **7** | VSLA/SACCO agentic flow | 4: Group → Mobile money → Agent → Inclusion | Data flow: Airtel/TNM → Agent → Ledger | Map: Malawi coverage |
| **8** | Malawi governance framework | 4: Reservations → Answers → Policy → Adoption | 4-quadrant: Reservations vs Engineering | Timeline: Strategy → Act → Law |
| **9** | Measurement dashboard | 4: Input → Process → Output → Outcome | OKR tree: Org → Dept → Agent → Human | Sparkline: 90-day trends |
| **10** | Decision rights matrix | 4: Human-only → Shared → Agent-only → Forbidden | RACI heatmap | Pie: % decisions by tier |
| **11** | LightSpeed journey timeline | 4: Start → Breakthrough → Lesson → Future | Gantt: 2024–2026 milestones | Counter: 90 agents, 20 depts, 0 downtime |

### Production Pipeline

```
Research Data → k-dense-infographics (Nano Banana Pro) → ls-visual-storytelling (brand enforcement) → ls-artifact-qa → Static assets
```

**Brand Enforcement Rules:**
- Palette: 80% navy / 10% red / 10% cyan
- Type: Arial scale (36/32/28/24/18/16/14/13/12pt)
- Logo: `brand/logos/fulllogo/fulllogo_transparent.png` on navy
- Clear space: 1× "L" height
- `™` on first company mention
- No emojis in visuals

---

## 5. Posting Cadence Recommendation

### Recommended: **Every 2 Days (Mon/Wed/Fri)**

| Post | Day | Date (CAT) | Rationale |
|------|-----|------------|-----------|
| 1 | Monday | 2026-10-05 | Series launch — high visibility |
| 2 | Wednesday | 2026-10-07 | Build log Wednesday alignment |
| 3 | Friday | 2026-10-09 | Policy Friday alignment |
| 4 | Monday | 2026-10-12 | Framework deep-dive — week start |
| 5 | Wednesday | 2026-10-14 | Use case Wednesday |
| 6 | Friday | 2026-10-16 | Health/M&E — policy relevance |
| 7 | Monday | 2026-10-19 | Financial inclusion — week start |
| 8 | Wednesday | 2026-10-21 | Governance — policy audience |
| 9 | Friday | 2026-10-23 | Measurement — builder audience |
| 10 | Monday | 2026-10-26 | Decision rights — provocative close |
| 11 | Wednesday | 2026-10-29 | Lessons — reflective, high engagement |

### Why Every 2 Days (Not Daily)?
1. **CEO bandwidth** — 45 min/write session × 11 = ~8 hrs protected time
2. **Algorithm favor** — LinkedIn rewards consistent 2–3×/week over daily bursts
3. **Engagement compounding** — Comments on Post N drive reach for Post N+1
4. **Substack sync** — Monthly newsletter (6 posts per issue) aligns naturally
5. **Visual production** — 2-day cycle allows `ls-artifact-qa` gate without rush

### Alternative Cadences (If CEO Prefers)

| Cadence | Duration | Pros | Cons |
|---------|----------|------|------|
| **Weekly (Mon only)** | 11 weeks | Lowest CEO time | Momentum loss, algorithm penalty |
| **Daily (Mon–Fri)** | 2.5 weeks | Maximum buzz | CEO burnout, quality risk, visual bottleneck |
| **Tue/Thu only** | 5.5 weeks | Mid-week engagement | Misses Mon/Wed/Fri pillar alignment |

---

## 6. CEO Review/Approval Gates

### Gate Definition

| Gate | Trigger | Reviewer | SLA | Tool |
|------|---------|----------|-----|------|
| **G1: Concept Approval** | Series plan (this doc) | Human CEO | 24h | GitHub PR / shared doc |
| **G2: Draft v1** | Per-post draft complete | Human CEO | 48h | GitHub PR (pharos/linkedin-series/post-N/) |
| **G3: Visual Sign-off** | Visuals QA'd | Human CEO | 24h | Figma link / PNG preview |
| **G4: Schedule Confirmation** | All assets ready | Human CEO | 4h | Publish queue preview |
| **G5: Post-Publish** | Live + 24h metrics | Human CEO | Async | Dashboard snapshot |

### Review Artifact Package (Per Post)

```
pharos/linkedin-series/post-01/
├── draft-v1.md              # LinkedIn long-form
├── research-evidence.md     # Claim-to-source map
├── x-thread.md              # 8–10 tweets
├── carousel-copy.md         # 3–5 card copy
├── substack-section.md      # Newsletter slice
├── video-script.md          # 60–90s shot list
├── visuals/
│   ├── hero-1200x627.png
│   ├── carousel-1-1200x627.png
│   ├── carousel-2-1200x627.png
│   ├── carousel-3-1200x627.png
│   └── framework-diagram.svg
└── qa-report.md             # ls-artifact-qa output
```

### CEO Review Checklist (Per Post)

- [ ] Voice matches "builder-writer-advocate" (no emojis, evidence-led, `™` correct)
- [ ] Every claim traceable to registry/results/Pharos artifact
- [ ] Framework layer (H-A-O-M-T-G-V) explicitly named
- [ ] Malawi/SADC context present (not generic)
- [ ] CTA aligned: Build / Evidence / Shape
- [ ] Visuals on-brand (palette, logo, type, dimensions)
- [ ] Hashtag set correct (3–5, no spam)
- [ ] Cross-post assets consistent with LinkedIn master

---

## 7. Cross-Posting to Substack Newsletter

### Strategy: "Series as Monthly Digest"

| Month | Substack Issue | LinkedIn Posts Included | Format |
|-------|----------------|-------------------------|--------|
| **October** | "AI-Native Organizations: The Framework" | Posts 1–4 | Long-read + framework diagram |
| **November** | "AI-Native Organizations: Use Cases & Governance" | Posts 5–10 | Case study anthology + policy brief |
| **December** | "AI-Native Organizations: Lessons from the Lab" | Post 11 + retrospective | CEO reflection + 2027 preview |

### Technical Implementation

| Component | Status | Detail |
|-----------|--------|--------|
| **Substack provisioning** | Pending (#194) | `@lightspeedholdings` reserved |
| **Publishing rail** | P1 (ADR-020) | Buy-side (no platform API churn) |
| **RSS → Substack** | Not yet built | Zapier/Make or custom MCP tool |
| **Canonical URL** | LinkedIn first | Substack `rel=canonical` to LinkedIn |
| **Subscriber capture** | Pharos KPI target: 2,000 | `pharos_subscribers.json` tracked |

### Substack Asset Requirements Per Issue

| Asset | Source |
|-------|--------|
| Cover image | Hero visual from Post 1 / Post 5 / Post 11 |
| Table of contents | Auto-generated from H2s |
| Framework diagram | Post 4 HAOMTGV (full resolution) |
| Case study deep-dive | Posts 5–7 expanded (2,500 words each) |
| Policy brief | Posts 8–10 synthesized |
| CEO reflection | Post 11 + unpublished lessons |
| CTA | "Join the Malawi Agentic AI Roundtable" |

---

## 8. Engagement/Response Management Protocol

### Response Triage (First 4 Hours Post-Publish)

| Priority | Trigger | Response | Owner |
|----------|---------|----------|-------|
| **P0** | Policy maker / minister / SADC official comments | Personal CEO reply (thoughtful, 2–3 sentences) | CEO |
| **P1** | Peer CEO / CTO / investor engages | CEO reply + DM for coffee chat | CEO |
| **P2** | Substantive question (technical/policy) | `thought_leadership_author` drafts → CEO approves | Pharos team |
| **P3** | Generic praise / emoji-only | Like + "Thank you" (template) | `community_ecosystem_builder` |
| **P4** | Criticism / skepticism | Reservations Playbook → honest, engineered answer | `agentic_policy_analyst` |

### Response Playbook

```markdown
# Reservations Playbook Mapping (per positioning.md)

| Reservation | Engineered Answer | Voice |
|-------------|-------------------|-------|
| "Won't work in low bandwidth" | Offline-first, local models, WhatsApp-native, PWA queues | "We operate in this reality daily" |
| "Where does data go?" | Sovereign in-country, DPA 2017/2024 + GDPR default | "Architected for Fortune 500 regulated estates" |
| "Tech debt / lock-in" | 90-day pilot, no rip-and-replace, visible variable cost | "We track and pay down our own debt" |
| "AI failed before" | 5-tier HITL, audit trails, risk tiers, circuit breakers, honesty badges | "Governance is the product" |
```

### Community Building Actions

| Action | Frequency | Owner |
|--------|-----------|-------|
| Comment on 5 peer/ICP posts (ICTAM, UNDP, MACRA, banks) | Daily (30 min) | CEO + `community_ecosystem_builder` |
| Invite 3 relevant voices to comment | Per post | `community_ecosystem_builder` |
| Curate "Best of Comments" carousel | Weekly | `content_creator` |
| Malawi Agentic AI Forum thread | Post-series | `community_ecosystem_builder` |

---

## 9. Metrics Tracking Per Post

### Dashboard: `src/ai_company/dashboard/kpis/marketing.py` (KPIs)

| KPI | Target | Measurement | Frequency |
|-----|--------|-------------|-----------|
| **Impressions** | >5,000/post | LinkedIn Analytics API | 24h, 7d, 30d |
| **Engagement Rate** | >5% | (Likes + Comments + Shares) / Impressions | 24h, 7d |
| **Comments (Substantive)** | >10/post | Manual tag: `substantive` | 7d |
| **Profile Visits** | >200/post | LinkedIn Analytics | 7d |
| **Follower Growth** | +50/week | LinkedIn Analytics | Weekly |
| **Substack Subscribers** | +100/month | `pharos_subscribers.json` | Monthly |
| **Click-Through (Substack)** | >3% | UTM tracking | Per post |
| **X Thread Engagement** | >50 RT+Likes | X Analytics | 24h, 7d |
| **Video Views (Reels)** | >1,000 | Meta/YouTube Analytics | 7d |

### Series-Level Metrics (Cumulative)

| Metric | Target | Source |
|--------|--------|--------|
| **Total Impressions** | >55,000 | Sum of posts |
| **Total Substantive Comments** | >110 | Manual audit |
| **Substack Subscribers (from series)** | >300 | UTM attribution |
| **Speaking Inquiries** | ≥3 | Inbound tracker |
| **Policy Meeting Requests** | ≥2 | `speaker_engagement_lead` log |
| **AI Citation Rate** | Baseline +20% | 20-keyword audit (ChatGPT/Perplexity/Gemini) |

### Reporting Cadence

| Report | Frequency | Audience | Format |
|--------|-----------|----------|--------|
| **Post Mortem** | 48h post-publish | Pharos team | Dashboard snapshot + qualitative notes |
| **Weekly Roll-up** | Friday 5 PM | CEO, CMO, CoS | 1-pager: metrics + top comments + actions |
| **Series Midpoint** | Post 6 | CEO, Board | 3-page: trajectory, adjustments, resource needs |
| **Series Retrospective** | Post 11 + 2 weeks | All execs | Full report: metrics, lessons, next series plan |

---

## 10. Clarifying Questions for CEO (Before Starting)

### Strategic Alignment

1. **Series Title Finalization** — "AI-Native Organizations" or "Building AI-Native Enterprises in Africa" or "The AI-Native Enterprise: A Malawi Playbook"?
2. **Personal vs. Company Voice** — All 11 posts from CEO personal LinkedIn, or Posts 1, 4, 11 from CEO + others from Company page?
3. **Policy Sensitivity** — Posts 8 & 10 (governance, decision rights) may attract regulator attention. Pre-brief MACRA/UNDP contacts?
4. **Competitive Disclosure** — How much internal architecture (agent registry, message bus, cost data) is publishable vs. proprietary?

### Operational

5. **CEO Writing Capacity** — 45 min/post × 11 = ~8.5 hrs over 4 weeks. Protected calendar blocks confirmed?
6. **Review SLA** — 48h for draft review realistic? Or prefer 24h with shorter drafts?
7. **Visual Approval** — CEO reviews every visual, or delegates to `thought_leadership_lead` after Post 1–2 pattern established?
8. **Cross-Post Timing** — X thread same morning as LinkedIn? Or 2h later for algorithm separation?

### Content Decisions

9. **Post 2 "152 Agents"** — Current canonical count is **90 agents** (per `source-of-truth.yaml` and ADR-032). Title says "152" — use "90" or explain the 152→90 consolidation story?
10. **Post 11 "Lessons"** — Include failures/mistakes (e.g., agent consolidation, scheduler reliability)? Honesty badges require it.
11. **CTA Family** — All posts end with same CTA ("Download the Malawi Agentic AI Monitor") or varied (Build/Evidence/Shape)?

### Technical

12. **Publish Rail** — Use LinkedIn API directly (P1 buy-side) or manual CEO post + company reshare?
13. **Substack** — Launch with Post 1 (capture early subscribers) or wait for Month 1 digest (higher quality)?
14. **MCP Server** — Expose `publish_queue` write tool for this series (gated by `approve` role)?

### Risk

15. **Platform Readiness** — LinkedIn company page still `Pending (#194)`. CEO personal profile is live. Proceed on personal only?
16. **Domain/Email** — `lightspeedholdings.com` parked (Afternic). Substack on `info.lightspeed@gmail.com` acceptable for launch?

---

## Appendix: Creative Brief Template (Per Post)

```markdown
# Creative Brief: Post {{N}} — {{Title}}

**ARTIFACT TYPE:** LinkedIn long-form + carousel + X thread + Substack slice + video script
**AUDIENCE:** SADC policymakers, Malawi CIOs, development partners, African enterprise leaders
**OBJECTIVE:** {{Build credibility / Demonstrate evidence / Shape policy}} — choose one primary
**CORE THESIS:** {{1–2 sentence thesis from Pharos pipeline}}
**NARRATIVE ARC:** Hook (builder proof) → Framework layer → Malawi/SADC evidence → Policy implication → CTA
**VISUAL LANGUAGE:** LightSpeed design system (navy/red/cyan, Arial, 4px grid)
**BRAND BASE:** `brand/tokens/brand-tokens.json` (canonical)
**STRUCTURE:**
  - LinkedIn: 1200–1800 words, 3–5 H2s, 1 framework diagram, 3 carousel cards
  - X: 8–10 tweets, 1 hero image, thread emoji: 🧵
  - Substack: 800-word slice + diagram
  - Video: 60–90s, 5-shot list, captions
**CHANNELS:** LinkedIn (CEO), X (CEO), LinkedIn (Company reshare), Substack (monthly), Reels/TikTok (Company)
**CTA:** {{Primary CTA from Build/Evidence/Shape family}}
**QA GATE:** ls-artifact-qa (visual/brand/ux/content/accessibility)
```

---

## Next Steps (Upon CEO Approval)

1. **G1 Gate** — CEO approves this plan (GitHub PR or signed PDF)
2. **Kickoff** — `thought_leadership_lead` creates ECL change `linkedin-ai-native-series`
3. **Template Setup** — `ls-social-media-design` builds post templates in `static/brand/templates/social-templates/`
4. **Research Sprint** — `agentic_research_lead` produces evidence matrices for Posts 1–3 (Week 1)
5. **Draft Sprint** — `thought_leadership_author` writes Drafts v1 for Posts 1–3 (Week 1–2)
6. **CEO Review Batch 1** — Posts 1–3 drafts submitted together (efficiency)
7. **Visual Production** — `ls-visual-storytelling` + `k-dense-infographics` for Posts 1–3
8. **Launch** — Post 1 publishes Monday 2026-10-05 07:00 CAT

---

*Plan prepared by `thought_leadership_lead` (Pharos). For approval by Human CEO.*
