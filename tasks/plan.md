# Implementation Plan: Light Speed Holdings Digital & Social Media SEO Strategy

## Overview

Execute a comprehensive organic social media and SEO strategy for Light Speed Holdings across 6 platforms (TikTok, Instagram, LinkedIn, YouTube, X, Facebook) with zero paid promotion. The strategy uses the Content Waterfall Method (1 pillar → atomize everywhere) with CEO-led voice targeting African tech leaders. Implementation follows the approved brand guidelines design in `docs/superpowers/specs/2026-09-06-social-media-brand-guidelines-design.md`.

## Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| **Content Waterfall Method** | Maximizes reach per effort; single pillar creates 7+ platform assets; proven for solo/small teams |
| **CEO-Led Voice** | Research shows CEO LinkedIn posts outperform company pages 3-5x; builds personal brand authority |
| **Builder-Advocate Tone** | Aligns with existing Pharos thought-leadership; differentiates from generic AI commentary |
| **No Paid Promotion** | Constraint accepted; organic compounds long-term; email list becomes owned audience |
| **6-Platform Simultaneous** | Social SEO requires presence where audience searches; TikTok/IG for discovery, LinkedIn for B2B, YouTube for search bridge |
| **4-Week Account Warm-Up** | Platform algorithms throttle new accounts using schedulers; manual engagement establishes authenticity |
| **Quarterly Brand Audits** | Ensures compliance with brand tokens; catches drift before it compounds |

## Task List

### Phase 0: Foundation (Weeks 1-2)

#### Task 1: Create Social Media Template Library
**Description:** Build 12 Canva/Figma templates for consistent brand application across all platforms using brand tokens from `brand/tokens/brand-tokens.json`.

**Acceptance Criteria:**
- [ ] LinkedIn carousel (5-slide) template created with navy rail, Arial typography
- [ ] Video thumbnail template (1280x720) with navy background, red accent play button
- [ ] Reels/Shorts cover template (1080x1920) with safe zones for UI overlays
- [ ] Quote card template (1080x1080) with logo placement and tagline
- [ ] Stat card template (1080x1080) for metrics visualization
- [ ] Thread header template (1200x675) for X/LinkedIn
- [ ] Lower-third video overlay template with navy background, cyan text
- [ ] Hook card template (first 3 seconds) for TikTok/Reels
- [ ] End-screen CTA template with email capture prompt
- [ ] Chapter marker template for YouTube
- [ ] Facebook Group cover template
- [ ] Email newsletter header template

**Verification:**
- [ ] All templates use only brand palette colors (navy #070A40, red #E63946, cyan #00BFFF, greys, white)
- [ ] Logo clear space (1x "L" height) maintained in all templates
- [ ] Type sizes match brand-tokens.json scale (32pt → 12pt)
- [ ] Tagline "ASPIRE. ACT. ACHIEVE." rendered correctly

**Dependencies:** None

**Files Likely Touched:**
- `static/brand/templates/social-templates/` (new directory)
- Canva/Figma project files

**Estimated Scope:** Medium (3-5 files/templates per session)

---

#### Task 2: Optimize All 6 Platform Profiles
**Description:** Set up or optimize profiles on TikTok, Instagram, LinkedIn, YouTube, X, Facebook with consistent branding, keyword-rich bios, and cross-links.

**Acceptance Criteria:**
- [ ] All 6 profiles use correct logo variant per platform spec (icon-only for TikTok/IG/X, full logo transparent for LinkedIn/YouTube/Facebook)
- [ ] Bios include primary keyword "AI agent company builder" + "Malawi" + "SADC"
- [ ] Profile/cover images from `static/brand/social/` uploaded
- [ ] Website link in bio (linktree or direct to blog)
- [ ] Cross-platform links in bio descriptions
- [ ] Location set to "Malawi" / "Lilongwe, Malawi"
- [ ] Contact email configured

**Verification:**
- [ ] Manual check: all 6 profiles display correctly on mobile and desktop
- [ ] Brand compliance: logo, colors, tagline per checklist in design doc Section 7

**Dependencies:** Task 1 (templates for cover images if regenerating)

**Files Likely Touched:**
- Platform profile settings (no code files)

**Estimated Scope:** Small (1-2 files/configs per platform)

---

#### Task 3: Create Keyword Master List & Content Calendar (90-Day)
**Description:** Research and document 50+ target keywords across 5 content pillars; build 90-day content calendar with weekly pillar rotation.

**Acceptance Criteria:**
- [ ] 50+ keywords categorized by pillar (Agent Architecture, SADC Deployments, Policy, Technical Frameworks, Community)
- [ ] Keywords include search volume estimates (Google Trends, TikTok Creator Search Insights, YouTube keyword tools)
- [ ] 90-day calendar with Mon-Fri cadence, weekly pillar themes, atomization mapping
- [ ] CEO personal content slots identified (LinkedIn 3-5x/week, X 5-10x/day)
- [ ] Company content slots identified per platform cadence limits

**Verification:**
- [ ] Calendar review: no gaps >2 days on any P1 platform (TikTok, LinkedIn)
- [ ] Keyword validation: each pillar has 10+ keywords with intent classification

**Dependencies:** None

**Files Likely Touched:**
- `docs/marketing/keyword-master-list.md` (new)
- `docs/marketing/content-calendar-90day.md` (new)

**Estimated Scope:** Medium (2-3 files)

---

#### Task 4: Account Warm-Up Protocol Execution (4 Weeks)
**Description:** Execute 4-week manual warm-up for all 6 accounts: consistent device/IP, profile completion, follow 20-50 relevant accounts, 1 native post/day, engage authentically.

**Acceptance Criteria:**
- [ ] Week 1: Profiles 100% complete, 20 relevant follows/platform, 1 post/day
- [ ] Week 2: 50 relevant follows/platform, 1 post/day, 15 min/day commenting on peer posts
- [ ] Week 3: 1 post/day, 30 min/day engagement, begin using content templates
- [ ] Week 4: Full cadence test (TikTok 3/day, LinkedIn 1/day, etc.), no scheduler use

**Verification:**
- [ ] No shadowban indicators (reach >0 on test posts)
- [ ] Follower growth >0 on all platforms by end of Week 4
- [ ] Engagement rate baseline established

**Dependencies:** Task 2 (profiles must be complete)

**Files Likely Touched:**
- `docs/marketing/warmup-log.md` (daily tracking)

**Estimated Scope:** Ongoing (daily 30-60 min, no code files)

---

#### Task 5: Set Up Analytics & Tracking Infrastructure
**Description:** Configure GA4, Google Search Console, platform native analytics, and tracking spreadsheet for KPIs.

**Acceptance Criteria:**
- [ ] GA4 property created with enhanced measurement
- [ ] GSC property verified for website domain
- [ ] UTM parameter convention documented (utm_source=platform, utm_medium=organic, utm_campaign=pillar-week)
- [ ] Tracking spreadsheet with tabs: Platform Metrics, Website Referrals, AI Citations, Email Subscribers
- [ ] Baseline metrics recorded for all platforms (followers, reach, engagement)

**Verification:**
- [ ] GA4 real-time test: visit from social link shows correct source/medium
- [ ] GSC: sitemap submitted, no coverage errors

**Dependencies:** None

**Files Likely Touched:**
- `docs/marketing/analytics-setup.md` (new)
- Tracking spreadsheet (Google Sheets/Excel)

**Estimated Scope:** Small (1-2 files)

---

### Checkpoint: Foundation Complete (End of Week 2)
- [ ] All 12 templates created and brand-compliant
- [ ] All 6 profiles optimized and live
- [ ] Keyword list (50+) and 90-day calendar complete
- [ ] Warm-up Week 2 complete (on track for 4-week protocol)
- [ ] Analytics infrastructure operational
- [ ] **Human review before proceeding to Phase 1**

---

### Phase 1: Content Engine Launch (Weeks 3-6)

#### Task 6: Produce Pillar 1 — Agent Architecture Deep-Dive
**Description:** Create first flagship content: YouTube tutorial (10-15 min) + blog post on agent hierarchy architecture, multi-provider LLM routing, or governance framework.

**Acceptance Criteria:**
- [ ] YouTube video published: 10-15 min, chapters matching sub-questions, corrected captions, custom thumbnail from template
- [ ] Blog post published: 2000+ words, schema markup (Article, VideoObject), target keyword in title/H1/first 100 words
- [ ] Video embedded in blog post with FAQ section
- [ ] SEO: meta title <60 chars, meta description <155 chars, H2/H3 structure, internal links to related content

**Verification:**
- [ ] YouTube: video processes in HD, chapters appear, captions accurate
- [ ] Blog: GSC indexes within 48 hours, no schema errors in Rich Results Test
- [ ] Cross-link: blog → video, video description → blog

**Dependencies:** Task 1 (thumbnail template), Task 3 (keyword for topic)

**Files Likely Touched:**
- Video production files
- Blog post markdown/HTML
- YouTube Studio

**Estimated Scope:** Large (5+ files) — **Split into sub-tasks if needed**

---

#### Task 7: Atomize Pillar 1 to All Platforms
**Description:** Repurpose Pillar 1 assets into platform-native formats per waterfall mapping.

**Acceptance Criteria:**
- [ ] 5 YouTube Shorts created from tutorial (vertical, <60s, hook in 1.5s)
- [ ] 3 LinkedIn carousels (5 slides each): architecture diagram, cost breakdown, governance flow
- [ ] 5 TikToks: quick demo, tip, myth-bust, behind-scenes, CTA to YouTube
- [ ] 1 X thread (6-10 tweets): key insights with diagrams/stats
- [ ] 2 Instagram Reels: repurposed TikToks (no watermark)
- [ ] 2 Facebook Reels: cross-posted from TikTok
- [ ] All assets use templates from Task 1, brand-compliant

**Verification:**
- [ ] All 18+ assets published within 48 hours of pillar launch
- [ ] UTM parameters on all links
- [ ] CEO comments on company posts within 1 hour

**Dependencies:** Task 6 (source assets), Task 1 (templates)

**Files Likely Touched:**
- Social media scheduling/drafting (manual posting during warm-up)

**Estimated Scope:** Medium (3-5 files/assets per session)

---

#### Task 8: Produce Pillar 2 — Malawi/SADC Deployment Case Study
**Description:** Create case study on real deployment (J&S StopOver Bar, health/M&E, or VSLA/SACCO) as LinkedIn article + PDF one-pager.

**Acceptance Criteria:**
- [ ] LinkedIn article published: 1500+ words, native document upload, CEO authored
- [ ] PDF one-pager: branded template, metrics, quotes, download link in article
- [ ] Case study includes: problem, solution, architecture, results, lessons learned
- [ ] Anonymized/client-approved data only

**Verification:**
- [ ] Article gets >100 impressions in first 48 hours
- [ ] PDF downloaded >10 times in first week

**Dependencies:** Task 1 (one-pager template), Task 3 (calendar slot)

**Files Likely Touched:**
- LinkedIn article
- PDF one-pager (generated from template)

**Estimated Scope:** Medium (2-3 files)

---

#### Task 9: Atomize Pillar 2 + Launch Facebook Group
**Description:** Repurpose case study; create "Agentic AI Malawi/SADC" Facebook Group with 20 seed members.

**Acceptance Criteria:**
- [ ] 3 Instagram Reels from case study stats/quotes
- [ ] 2 TikToks: client outcome, local context insight
- [ ] 1 Quora answer: "How is AI being used in Malawi businesses?"
- [ ] Facebook Group created: name, description, rules, cover image
- [ ] 20 seed members invited (team, partners, early followers)
- [ ] First Group discussion prompt posted

**Verification:**
- [ ] Group: 20+ members, 5+ discussions in first week
- [ ] Quora answer: >5 upvotes in first week

**Dependencies:** Task 8 (source content), Task 1 (Reels templates)

**Files Likely Touched:**
- Social assets
- Facebook Group settings

**Estimated Scope:** Small-Medium

---

#### Task 10: Produce Pillar 3 — CEO Policy/Strategy Commentary
**Description:** CEO publishes thought leadership on AI policy, SADC governance, or national AI strategy.

**Acceptance Criteria:**
- [ ] CEO LinkedIn post: 800-1200 words, strong hook, framework visual, 3-5x engagement of company posts
- [ ] X thread (8-10 tweets): same framework, threaded for readability
- [ ] Newsletter Section 1: "CEO Perspective" drafted for Week 4 send

**Verification:**
- [ ] LinkedIn: >500 impressions, >20 substantive comments in 48 hours
- [ ] X thread: >10 retweets, >50 likes in 24 hours

**Dependencies:** Task 3 (CEO slots in calendar)

**Files Likely Touched:**
- LinkedIn post
- X thread
- Newsletter draft

**Estimated Scope:** Small

---

#### Task 11: Produce Pillar 4 — Technical Framework/Tooling
**Description:** YouTube tutorial + GitHub repo release for a technical component (e.g., agent generator, message bus, decision engine).

**Acceptance Criteria:**
- [ ] YouTube video: 10-15 min tutorial, code walkthrough, repo link in description
- [ ] GitHub repo: README, MIT license, usage examples, linked from video
- [ ] 4 YouTube Shorts from key moments
- [ ] 2 LinkedIn carousels: code snippets, architecture diagram

**Verification:**
- [ ] GitHub: >10 stars in first week
- [ ] Video: >50% avg view duration

**Dependencies:** Task 1 (templates), CTO/Lead Backend for code readiness

**Files Likely Touched:**
- Video production
- GitHub repository
- Social assets

**Estimated Scope:** Medium-Large

---

#### Task 12: Establish Daily Posting Cadence & Community Engagement
**Description:** Transition from warm-up to full production cadence across all platforms; implement 30-min daily engagement protocol.

**Acceptance Criteria:**
- [ ] TikTok: 3-5 videos/day, spaced 1-2 hours
- [ ] Instagram: 1 image + 4 Reels/day
- [ ] LinkedIn: 1-2 posts/day (CEO + company)
- [ ] YouTube: 4 Shorts + 1 long-form/week
- [ ] X: 5 posts/day (replies > original tweets)
- [ ] Facebook: 4 Reels/day
- [ ] Daily: 30 min commenting on peer/ICP posts (LinkedIn, X)
- [ ] Daily: Reply to every comment in first hour (video reply on TikTok when possible)

**Verification:**
- [ ] 4 consecutive weeks of full cadence without gaps
- [ ] Engagement rate baselines: TikTok 5%+, IG 3%+, LinkedIn 2%+

**Dependencies:** Task 4 (warm-up complete), Tasks 6-11 (content bank)

**Files Likely Touched:**
- `docs/marketing/daily-cadence-checklist.md` (new)

**Estimated Scope:** Ongoing (operational)

---

### Checkpoint: Engine Launch Complete (End of Week 6)
- [ ] 4 pillars produced and atomized (72+ total assets published)
- [ ] Full daily cadence running on all 6 platforms
- [ ] Facebook Group active (20+ members, daily discussions)
- [ ] First analytics review: baseline metrics established
- [ ] Email capture forms live on website + social bios
- [ ] **Human review before proceeding to Phase 2**

---

### Phase 2: Growth & Optimization (Weeks 7-12)

#### Task 13: First Analytics Deep-Dive & Format Optimization
**Description:** Analyze 6 weeks of data; identify top-performing formats, topics, posting times; double down on winners.

**Acceptance Criteria:**
- [ ] Performance report: reach, engagement, saves/shares, profile visits, website clicks per platform
- [ ] Top 3 formats identified per platform (e.g., TikTok: myth-bust > demo > tip)
- [ ] Top 3 topics identified (e.g., "agent architecture" > "governance" > "cost optimization")
- [ ] Format optimization guide: recommended format mix per platform
- [ ] Low-performing formats (<25th percentile) dropped or redesigned

**Verification:**
- [ ] Data-backed decisions documented
- [ ] Next 4-week calendar reflects optimization

**Dependencies:** Task 12 (6 weeks of data)

**Files Likely Touched:**
- `docs/marketing/analytics-report-6week.md` (new)
- `docs/marketing/format-optimization-guide.md` (new)

**Estimated Scope:** Medium

---

#### Task 14: Launch Cross-Platform Collaborations
**Description:** Execute 3+ collaborations with complementary accounts in African tech/AI space.

**Acceptance Criteria:**
- [ ] 3+ collaboration targets identified (African AI founders, tech VCs, policy makers)
- [ ] Collaboration formats: co-created video, guest appearance, joint LinkedIn Live, comment thread exchange
- [ ] 2+ collaborations executed and published
- [ ] Cross-pollination: each collab drives >50 profile visits to Light Speed accounts

**Verification:**
- [ ] Collaboration tracker: partner, format, date, results
- [ ] Follower spike attributed to collab days

**Dependencies:** Task 12 (established presence for credibility)

**Files Likely Touched:**
- `docs/marketing/collaboration-tracker.md` (new)

**Estimated Scope:** Small-Medium

---

#### Task 15: Create Content Repurposing SOP
**Description:** Document the waterfall workflow as a repeatable SOP for the team.

**Acceptance Criteria:**
- [ ] SOP document: `docs/sop-content-repurposing.md`
- [ ] Step-by-step: pillar selection → asset creation → atomization checklist → publishing → UTM tagging → analytics logging
- [ ] Role assignments: who does what (CEO, Content Writer, Content Creator, Marketing Owner)
- [ ] Quality gates: brand compliance check, SEO check, link check
- [ ] Template links and naming conventions

**Verification:**
- [ ] SOP review: new team member could execute waterfall independently
- [ ] Checklist used for next 2 pillars without missing steps

**Dependencies:** Tasks 6-11 (workflow proven)

**Files Likely Touched:**
- `docs/sop-content-repurposing.md` (new)

**Estimated Scope:** Small

---

#### Task 16: Begin Reddit Community Engagement
**Description:** Establish authentic presence in 3+ relevant subreddits (r/AfricaTech, r/MachineLearning, r/artificial, r/Malawi).

**Acceptance Criteria:**
- [ ] 3+ target subreddits identified with rules reviewed
- [ ] 10+ helpful, non-promotional comments/posts per week
- [ ] 2+ original posts sharing genuine insights (not links)
- [ ] Disclosure of affiliation in profile/bio
- [ ] Track: upvotes, comments, profile clicks, website referrals from Reddit

**Verification:**
- [ ] Reddit karma >100 in first month
- [ ] 1+ post reaches >50 upvotes
- [ ] GA4 shows Reddit referral traffic

**Dependencies:** Task 5 (UTM tracking ready)

**Files Likely Touched:**
- `docs/marketing/reddit-engagement-log.md` (new)

**Estimated Scope:** Ongoing (operational)

---

#### Task 17: Optimize for AI Search Engines (GEO/AEO)
**Description:** Audit and optimize content for AI citation (ChatGPT, Perplexity, Gemini, Google AI Overviews).

**Acceptance Criteria:**
- [ ] AI citation audit: query 20 target keywords in ChatGPT/Perplexity/Gemini; note if Light Speed cited
- [ ] llms.txt added to website root with key pages
- [ ] Organization schema on homepage with social profiles
- [ ] FAQ schema on pillar pages
- [ ] Entity consistency check: name, description, URLs identical across all platforms
- [ ] Wikidata entry created/claimed for Light Speed Holdings

**Verification:**
- [ ] AI audit: baseline citation rate recorded
- [ ] Schema validation: Rich Results Test passes
- [ ] Wikidata: entity exists with correct attributes

**Dependencies:** Task 3 (keywords), Task 6-11 (content exists)

**Files Likely Touched:**
- `llms.txt` (website root)
- Website schema markup
- Wikidata entry

**Estimated Scope:** Medium

---

#### Task 18: Launch Email Newsletter (Hub)
**Description:** Convert social followers to owned email list; weekly newsletter with CEO perspective + curated content.

**Acceptance Criteria:**
- [ ] Email platform configured (ConvertKit, Beehiiv, or similar)
- [ ] Lead magnet created: "AI Agent Company Builder Starter Kit" (PDF from templates)
- [ ] Signup forms: website, LinkedIn bio, YouTube descriptions, TikTok/IG bio links
- [ ] Newsletter #1 sent: CEO letter + 3 curated pillars + community highlight
- [ ] Welcome sequence: 3 emails (deliver magnet, intro to pillars, community invite)

**Verification:**
- [ ] 50+ subscribers in first 2 weeks
- [ ] Open rate >35%, click rate >5%
- [ ] Lead magnet delivery tested end-to-end

**Dependencies:** Task 5 (analytics), Task 1 (newsletter header template)

**Files Likely Touched:**
- Email platform setup
- Lead magnet PDF
- Website signup forms

**Estimated Scope:** Medium

---

#### Task 19: Build Quora Presence
**Description:** Answer 10+ questions on Quora in AI agent, African tech, Malawi business categories.

**Acceptance Criteria:**
- [ ] 10+ answers published with credentials (CEO/CTO profile)
- [ ] Answers include: specific data, framework, link to relevant pillar content
- [ ] Track: views, upvotes, referral clicks to website
- [ ] Profile optimized: bio, credentials, website link

**Verification:**
- [ ] 1+ answer >1000 views
- [ ] Quora referral traffic in GA4

**Dependencies:** Task 3 (keywords for question research)

**Files Likely Touched:**
- Quora answers
- `docs/marketing/quora-tracker.md` (new)

**Estimated Scope:** Small

---

### Checkpoint: Growth Phase Complete (End of Week 12)
- [ ] Analytics-driven format optimization implemented
- [ ] 2+ collaborations executed with measurable cross-pollination
- [ ] Repurposing SOP documented and in use
- [ ] Reddit presence established (karma >100)
- [ ] AI search optimization baseline recorded
- [ ] Email newsletter launched with 100+ subscribers
- [ ] Quora presence active
- [ ] **Human review before proceeding to Phase 3**

---

### Phase 3: Authority & Scale (Weeks 13-24)

#### Task 20: Publish First White Paper
**Description:** Produce flagship white paper "The Sovereign Agentic Enterprise" (5000+ words) with original research/framework.

**Acceptance Criteria:**
- [ ] White paper PDF: branded, executive summary, framework visual, citations, methodology
- [ ] Landing page with gated download (email capture)
- [ ] PR outreach: pitch to 5+ African tech publications
- [ ] Atomization: 5 LinkedIn carousels, 3 YouTube Shorts, 5 TikToks, X thread series
- [ ] Track: downloads, citations, speaking invitations

**Verification:**
- [ ] 100+ downloads in first month
- [ ] 1+ publication pickup or citation
- [ ] Speaking invitation generated

**Dependencies:** Task 15 (SOP), Agentic Research Lead for research rigor

**Files Likely Touched:**
- White paper (Google Docs → PDF)
- Landing page
- Atomized social assets

**Estimated Scope:** Large (5+ files) — **Split into sub-tasks**

---

#### Task 21: Launch "Malawi Agentic AI Monitor" Monthly Publication
**Description:** Monthly research publication tracking AI developments in Malawi/SADC.

**Acceptance Criteria:**
- [ ] Issue #1 published: 3-5 page PDF, original data, policy tracking, use-case census
- [ ] Distribution: newsletter, LinkedIn document, website, partner shares
- [ ] Issue #2 drafted and scheduled
- [ ] Editorial calendar for 12 months

**Verification:**
- [ ] Issue #1: 200+ downloads, 50+ shares
- [ ] Cited in 1+ external publication

**Dependencies:** Task 20 (white paper establishes credibility), Agentic Research Lead

**Files Likely Touched:**
- Monthly publication PDFs
- Distribution assets

**Estimated Scope:** Medium (recurring)

---

#### Task 22: Secure First Speaking Engagement
**Description:** Book CEO speaking slot at ICTAM, COMESA/IDEA, IDC CIO Summit, SADC, or Smart Africa.

**Acceptance Criteria:**
- [ ] 5+ target events identified with CFP deadlines
- [ ] 3+ speaking proposals submitted (keynote, panel, workshop)
- [ ] 1+ acceptance confirmed
- [ ] Speaker one-sheet prepared (bio, topics, past talks, audience fit)
- [ ] Talk assets prepared: slides (brand template), handout, recording plan

**Verification:**
- [ ] Speaking slot confirmed with date
- [ ] Pre-event promotion: 3+ social posts, newsletter mention

**Dependencies:** Task 20 (white paper as credibility asset), Speaker Engagement Lead agent

**Files Likely Touched:**
- Speaker one-sheet (from template)
- Slide deck (brand template)
- Proposal documents

**Estimated Scope:** Medium

---

#### Task 23: Build Google Knowledge Panel & Wikidata Presence
**Description:** Achieve verified Knowledge Panel for "Light Speed Holdings" and complete Wikidata entity.

**Acceptance Criteria:**
- [ ] Wikidata entity: Q-ID created, all properties filled (inception, location, industry, website, social profiles, key people)
- [ ] Google Knowledge Panel: claimed/verified via Search Console
- [ ] Consistent entity data across: website schema, social profiles, Wikidata, Crunchbase, LinkedIn company page
- [ ] Third-party citations: 5+ credible sources (news, directories, publications)

**Verification:**
- [ ] Search "Light Speed Holdings" → Knowledge Panel appears with logo, description, social links
- [ ] Wikidata: no "instance of" conflicts, all references verified

**Dependencies:** Task 17 (entity consistency), Task 20 (white paper as citation)

**Files Likely Touched:**
- Website schema
- Wikidata edits
- Third-party directory submissions

**Estimated Scope:** Medium

---

#### Task 24: Create Case Studies from Real Deployments
**Description:** Produce 2+ detailed case studies with client approval (anonymized if needed).

**Acceptance Criteria:**
- [ ] 2+ case studies: 2000+ words each, problem/solution/results structure, metrics
- [ ] Formats: blog post, PDF one-pager, LinkedIn document, 2-min video testimonial (if possible)
- [ ] Distribution: website case study page, newsletter, sales enablement
- [ ] SEO: target "AI agent implementation [industry]" keywords

**Verification:**
- [ ] Case study page: >500 visits in first month
- [ ] Sales team uses in 2+ proposals

**Dependencies:** Customer Success Owner for client coordination, Task 15 (SOP)

**Files Likely Touched:**
- Case study blog posts
- PDF one-pagers
- Video assets

**Estimated Scope:** Medium per case study

---

#### Task 25: Implement Backlink Monitoring
**Description:** Set up continuous backlink health monitoring to protect authority signals.

**Acceptance Criteria:**
- [ ] Monitoring tool configured (LynkDog free tier or Ahrefs/SEMrush)
- [ ] All earned backlinks from Phase 1-2 imported
- [ ] Directory listings (G2, Capterra, Product Hunt, etc.) imported
- [ ] Alert rules: status code changes, anchor text changes, rel attribute changes
- [ ] Monthly backlink health report in analytics review

**Verification:**
- [ ] Tool shows >90% healthy links
- [ ] First alert test: manually break a link, verify alert fires

**Dependencies:** Task 5 (analytics), Tasks 6-19 (backlinks earned)

**Files Likely Touched:**
- Monitoring tool configuration
- `docs/marketing/backlink-health-report.md` (monthly)

**Estimated Scope:** Small

---

#### Task 26: 90-Day Strategy Review & Revision
**Description:** Comprehensive review of strategy performance; revise roadmap for months 4-12.

**Acceptance Criteria:**
- [ ] KPI dashboard: followers, traffic, leads, brand awareness vs. targets
- [ ] Channel ROI analysis: effort hours vs. outcomes per platform
- [ ] Content audit: top 20% posts driving 80% of results
- [ ] Revised 9-month roadmap with adjusted platform priorities, format mix, resource allocation
- [ ] Budget proposal (if any paid amplification justified)

**Verification:**
- [ ] Review document presented to CEO/CMO
- [ ] Decisions documented: continue/pivot/stop per channel
- [ ] Updated roadmap committed to `docs/marketing/roadmap-revision-90day.md`

**Dependencies:** All Phase 1-2 tasks (data required)

**Files Likely Touched:**
- `docs/marketing/strategy-review-90day.md` (new)
- `docs/marketing/roadmap-revision-90day.md` (new)

**Estimated Scope:** Medium

---

### Checkpoint: Authority Phase Complete (End of Week 24)
- [ ] White paper published with 100+ downloads
- [ ] Monthly Monitor launched (2+ issues)
- [ ] Speaking engagement secured and executed
- [ ] Knowledge Panel verified
- [ ] 2+ case studies published
- [ ] Backlink monitoring operational
- [ ] 90-day review complete with revised roadmap
- [ ] **Final human review — strategy graduates to ongoing operations**

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Algorithm changes kill reach on primary platform | High | Diversified 6-platform strategy; no single-platform dependency; email list as owned audience |
| Content burnout (daily cadence unsustainable) | High | Waterfall method reduces creation load; batch production days; AI-assisted drafting; SOP enables delegation |
| 60-90 day plateau before traction | Medium | Leading indicators tracked (saves, shares, comments > likes); warm-up protocol; realistic expectations set |
| New account throttling / shadowban | Medium | 4-week manual warm-up; no schedulers initially; consistent device/IP; engagement-first approach |
| Competitor with established presence | Medium | Malawi/SADC niche differentiation; builder-advocate proof over promises; local authenticity |
| AI search visibility doesn't materialize | Medium | Entity authority building from Day 1; structured data; consistent citations; Wikidata/Knowledge Panel focus |
| Client confidentiality blocks case studies | Medium | Anonymized "pattern" case studies; synthetic but realistic data; internal deployments as proof |
| Team capacity insufficient for cadence | High | Phase-gated scope; SOP enables contractor/agency support; template system reduces decision fatigue |

## Open Questions

1. **Video Production Capacity:** Who shoots/edits video? Internal (Content Creator agent) or contractor? Need decision before Task 6.
2. **CEO Time Commitment:** 3-5 LinkedIn posts/week + X engagement requires ~5 hrs/week. Confirmed available?
3. **Client Approvals for Case Studies:** What's the clearance process? Timeline?
4. **Email Platform Selection:** ConvertKit, Beehiiv, or self-hosted? Decision needed before Task 18.
5. **Monitoring Tool Budget:** Free tier (LynkDog 20 links) vs. paid (Ahrefs/SEMrush)? Decision before Task 25.
6. **Legal Review for Public Content:** Does Pharos/Legal need to pre-approve policy commentary? Process needed.

---

## Parallelization Opportunities

| Safe to Parallelize | Must Be Sequential | Needs Coordination |
|---------------------|-------------------|-------------------|
| Template creation (Task 1) + Keyword research (Task 3) | Profile setup → Warm-up → Full cadence | Content creation ↔ Template availability |
| Platform profile setup (Task 2) across 6 platforms | Pillar production → Atomization | CEO content ↔ Company content calendar |
| Analytics setup (Task 5) + Keyword list (Task 3) | Phase 0 → Phase 1 → Phase 2 → Phase 3 | Collaboration outreach ↔ Content calendar |
| Reddit engagement (Task 16) + Quora (Task 19) | White paper research → Writing → Design | Speaking proposals ↔ White paper completion |

---

*Plan created 2026-09-06. Ready for human review before implementation begins.*
