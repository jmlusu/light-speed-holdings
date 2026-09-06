# Analytics & Tracking Setup — Light Speed Holdings

**Status:** Phase 0 — Week 1
**Owner:** Growth Hacker / Marketing Owner
**Tools:** All free tier

---

## 1. Google Analytics 4 (GA4)

### Property Setup
- **Property Name:** Light Speed Holdings — Social Traffic
- **Data Stream:** Web (lightspeedholdings.com / blog subdomain)
- **Enhanced Measurement:** ON (scrolls, video plays, file downloads, form interactions)
- **Data Retention:** 14 months

### Events to Track
| Event Name | Trigger | Parameters |
|------------|---------|------------|
| `social_click` | Click on social profile link | `platform`, `placement` (bio|post|footer) |
| `email_signup` | Form submit on newsletter | `source`, `lead_magnet` |
| `content_download` | PDF/whitepaper download | `content_type`, `content_title` |
| `video_play` | YouTube/embedded video play | `video_id`, `platform` |
| `cta_click` | CTA button click | `cta_text`, `page_path` |

### Custom Dimensions
| Dimension | Scope | Values |
|-----------|-------|--------|
| `utm_source` | Event | tiktok, instagram, linkedin, youtube, x, facebook |
| `utm_campaign` | Event | pillar1-week1, pillar2-week2, etc. |
| `content_pillar` | Event | architecture, deployments, policy, tooling, community |
| `author_type` | Event | ceo, company, guest |

---

## 2. Google Search Console (GSC)

### Property
- **Type:** Domain property (lightspeedholdings.com)
- **Verification:** DNS TXT record

### Sitemap
- Submit: `https://lightspeedholdings.com/sitemap.xml`
- Blog sitemap: `https://lightspeedholdings.com/blog/sitemap.xml`

### Monitoring
- **Weekly:** Index coverage, performance (clicks, impressions, CTR, position)
- **Monthly:** Core Web Vitals, mobile usability
- **Per pillar:** Query rankings for primary keywords

---

## 3. UTM Parameter Convention

### Standard Format
```
https://destination.com/path?
  utm_source=PLATFORM&
  utm_medium=organic&
  utm_campaign=PILLAR-WEEK&
  utm_content=FORMAT&
  utm_term=KEYWORD
```

### Platform Values
| Platform | utm_source |
|----------|------------|
| TikTok | tiktok |
| Instagram | instagram |
| LinkedIn | linkedin |
| YouTube | youtube |
| X/Twitter | x |
| Facebook | facebook |
| Reddit | reddit |
| Quora | quora |
| Newsletter | newsletter |

### Campaign Values
`pillar{N}-week{N}` (e.g., `pillar1-week1`, `pillar2-week3`)

### Content Values
| Format | utm_content |
|--------|-------------|
| Long-form video | video |
| Short/Reel/TikTok | short |
| Carousel | carousel |
| Thread | thread |
| Article | article |
| PDF/Document | document |
| Image post | image |
| Comment/Reply | comment |

### Keyword Values
Primary keyword from `keyword-master-list.md` (kebab-case)
Example: `ai-agent-hierarchy`, `malawi-ai-strategy`, `python-agent-framework`

---

## 4. Tracking Spreadsheet (Google Sheets)

### Sheet Structure

#### Tab 1: Platform Metrics (Daily/Weekly)
| Date | Platform | Pillar | Followers | Impressions | Reach | Engagement | Saves | Shares | Comments | Profile Visits | Video Views | Avg Watch Time |
|------|----------|--------|-----------|-------------|-------|------------|-------|--------|----------|----------------|-------------|----------------|

#### Tab 2: Website Referrals (Weekly)
| Week | Source | Sessions | Users | New Users | Pages/Session | Avg Duration | Bounce Rate | Conversions (Email) | Conversions (Download) |
|------|--------|----------|-------|-----------|---------------|--------------|-------------|---------------------|------------------------|

#### Tab 3: Content Performance (Per Piece)
| Date | Platform | Pillar | Keyword | Format | URL | UTMs | Impressions | Reach | Engagement Rate | Saves | Shares | Profile Visits | Website Clicks | Followers Gained | Notes |
|------|----------|--------|---------|--------|-----|------|-------------|-------|-----------------|-------|--------|----------------|----------------|------------------|-------|

#### Tab 4: AI Citations (Monthly)
| Date | Platform | Query | Cited? | Position | URL Cited | Notes |
|------|----------|-------|--------|----------|-----------|-------|

#### Tab 5: Email Metrics (Per Send)
| Date | Subject | Sent | Delivered | Opens | Open Rate | Clicks | Click Rate | Unsubscribes | New Subscribers | Total Subscribers |
|------|---------|------|-----------|-------|-----------|--------|------------|--------------|-----------------|-------------------|

#### Tab 6: Monthly KPI Dashboard
| Month | Total Followers | Website Traffic (Social) | Email Subs | Leads | Branded Search | AI Citations | Backlinks | Domain Authority |
|-------|-----------------|--------------------------|------------|-------|----------------|--------------|-----------|------------------|

---

## 5. Platform Native Analytics Access

| Platform | Access Method | Key Metrics to Export Weekly |
|----------|---------------|------------------------------|
| TikTok | Analytics tab (Pro account) | Views, likes, comments, shares, saves, profile visits, follower growth, traffic sources |
| Instagram | Insights (Business account) | Reach, accounts engaged, content interactions, profile visits, website taps, follower growth |
| LinkedIn | Analytics (Page + Personal) | Impressions, clicks, engagement rate, followers, visitor demographics, post analytics |
| YouTube | YouTube Studio | Views, watch time, subscribers, traffic sources, audience retention, CTR |
| X | Analytics (analytics.twitter.com) | Impressions, engagements, engagement rate, link clicks, profile visits, follower growth |
| Facebook | Meta Business Suite | Reach, engagement, video views, follower growth, group insights |

---

## 6. Baseline Metrics (Record Week 1)

| Platform | Followers | Avg Reach/Post | Avg Engagement Rate | Profile Visits/Week | Website Clicks/Week |
|----------|-----------|----------------|---------------------|---------------------|---------------------|
| TikTok | 0 | — | — | — | — |
| Instagram | 0 | — | — | — | — |
| LinkedIn (Company) | 0 | — | — | — | — |
| LinkedIn (CEO) | 0 | — | — | — | — |
| YouTube | 0 | — | — | — | — |
| X | 0 | — | — | — | — |
| Facebook | 0 | — | — | — | — |

**Target: Update baselines every Monday. First real baseline at Week 4 (post-warm-up).**

---

## 7. Automated Reporting (Free Tools)

### Google Looker Studio (Free)
- Connect GA4 + GSC + Google Sheets
- Dashboard: Social Traffic Overview, Content Performance, Audience Geography
- Auto-refresh: Daily

### Platform Exports (Manual Weekly)
- Monday: Export all platform CSVs → Import to Tracking Spreadsheet
- Time: 30 min/week

### Monthly AI Citation Audit (Manual)
- Query 20 keywords in: ChatGPT, Perplexity, Gemini, Google AI Overviews
- Record: Cited? Position? URL?
- Time: 45 min/month

---

## 8. Lead Magnet Tracking

### Lead Magnet: "AI Agent Company Builder Starter Kit"
- **Format:** PDF (generated from brand templates)
- **Delivery:** Email automation (self-hosted)
- **Tracking:** `email_signup` event with `lead_magnet=starter-kit`

### UTM for Lead Magnet Links
```
utm_source=platform&utm_medium=organic&utm_campaign=lead-magnet&utm_content=pdf&utm_term=starter-kit
```

---

## 9. Monthly Reporting Template

### Executive Summary (1 page)
- **Top 3 Wins:** Metric + context
- **Top 3 Learnings:** What worked/didn't
- **Next Month Focus:** 2-3 priorities
- **Blockers:** Resource/time/approval needs

### KPI Scorecard
| KPI | Target | Actual | Δ | Status |
|-----|--------|--------|---|--------|
| Total Followers | | | | 🟢🟡🔴 |
| Social Website Traffic | | | | 🟢🟡🔴 |
| Email Subscribers | | | | 🟢🟡🟡 |
| Leads Generated | | | | 🟢🟡🔴 |
| Branded Search Volume | | | | 🟢🟡🔴 |

### Channel Breakdown
| Channel | Followers | Reach | Engagement | Website Clicks | Cost (Time) | ROI |
|---------|-----------|-------|------------|----------------|-------------|-----|

---

## 10. Tools Stack (All Free)

| Tool | Purpose | Cost |
|------|---------|------|
| GA4 | Website analytics | Free |
| GSC | Search performance | Free |
| Google Looker Studio | Dashboards | Free |
| Google Sheets | Tracking spreadsheet | Free |
| TikTok/IG/LI/YT/X/FB Native | Platform analytics | Free |
| LynkDog (20 links) | Backlink monitoring | Free |
| Google Trends | Keyword research | Free |
| TikTok Creator Search Insights | TikTok keyword data | Free |
| YouTube Search Insights | YouTube keyword data | Free |

---

## 11. Implementation Checklist (Week 1)

- [ ] GA4 property created + data stream connected
- [ ] GSC domain property verified
- [ ] Enhanced measurement ON in GA4
- [ ] Custom events created in GA4 (`social_click`, `email_signup`, `content_download`, `video_play`, `cta_click`)
- [ ] Custom dimensions registered in GA4
- [ ] Sitemap submitted to GSC
- [ ] Tracking spreadsheet created with 6 tabs
- [ ] UTM builder bookmarked (Google's Campaign URL Builder)
- [ ] Platform analytics access confirmed for all 6
- [ ] Baseline metrics recorded (all zeros initially)
- [ ] Looker Studio dashboard connected to GA4 + GSC
- [ ] LynkDog account created (free tier)
- [ ] Monthly AI citation audit calendar invite set

---

*Analytics infrastructure must be live before first content publish (Week 3).*
