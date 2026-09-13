# Marketing Standard Operating Procedure

**Document ID:** SOP-MKT-001
**Department:** Marketing
**Owner:** Marketing Executive
**Classification:** Internal
**Last Updated:** July 2026

---

## 1. Purpose

This Standard Operating Procedure establishes the processes for content creation, brand management, campaign coordination, and audience engagement within Light Speed Holdings' AI Company Builder project. It ensures consistent, high-quality marketing output that reflects the company's position as an AI-native organization.

## 2. Scope

This SOP applies to all marketing activities including:

- Technical content creation (documentation, blog posts, guides)
- Social media asset design and distribution
- Brand guidelines enforcement
- Campaign planning and execution
- Content distribution channel management
- Engagement metrics tracking
- Competitive analysis and market research
- Product marketing for the AI Company Builder tool

## 3. Roles and Responsibilities

| Role | Agent/Person | Responsibilities |
|------|-------------|-----------------|
| Marketing Lead | Executive | Strategy, brand oversight, campaign approval |
| Content Creator | Specialist | Content production, visual design, social media assets |
| Content Manager | Manager | Editorial calendar, quality control, distribution |
| CTO | `cto` | Technical accuracy review for technical content |
| CEO / Founder | Human operator | Brand vision, final approval on public-facing content |

## 4. Content Creation Workflow

### 4.1 Content Types

| Content Type | Channel | Frequency | Approval Required |
|-------------|---------|-----------|-------------------|
| Documentation | `docs/` directory | As needed | CTO review |
| Blog post | Website / Medium | Biweekly | Marketing Lead |
| Social media post | Twitter, LinkedIn | 3x per week | Content Manager |
| Technical tutorial | YouTube / Blog | Monthly | CTO + Marketing Lead |
| Product update | Changelog, email | Per release | CEO |
| Case study | Website | Quarterly | Marketing Lead + CEO |

### 4.2 Content Production Process

**Step 1: Planning**

- Content Manager maintains an editorial calendar in `workflows/`
- Content themes are aligned with product milestones and company strategy
- Content Creator receives task assignments via `MessageBus`

**Step 2: Research**

- Gather technical details from `docs/ARCHITECTURE.md` and source code
- Review competitive landscape and market trends
- Identify target audience and key messaging points

**Step 3: Creation**

- Write content following the brand voice guidelines (Section 5)
- Include accurate technical references (component names, command syntax)
- Create accompanying visual assets using the design system
- Save drafts in `reports/` or designated content directories

**Step 4: Review**

- Technical accuracy review by CTO or Lead Developer
- Brand consistency review by Content Manager
- Legal/compliance review for claims and disclosures
- SEO review for public-facing web content

**Step 5: Publication**

- Content Manager publishes to the appropriate channel
- Content Creator creates distribution assets (social posts, email teasers)
- Track initial engagement metrics within 24 hours

**Step 6: Measurement**

- Review engagement metrics after 7 days
- Compare against KPI targets (Section 9)
- Document lessons learned for future content

### 4.3 Content Approval Matrix

| Content Type | Creator | Technical Review | Brand Review | Final Approval |
|-------------|---------|-----------------|-------------|---------------|
| Documentation | Content Creator | CTO | Content Manager | CTO |
| Blog post | Content Creator | CTO (if technical) | Content Manager | Marketing Lead |
| Social media | Content Creator | None | Content Manager | Content Manager |
| Product update | Content Creator | CTO | Content Manager | CEO |
| Case study | Content Creator | CTO | Marketing Lead | CEO |

## 5. Brand Management

### 5.1 Brand Voice

Light Speed Holdings' brand voice is:

- **Professional**: Clear, authoritative, data-driven
- **Innovative**: Forward-looking, technical, AI-native
- **Accessible**: Complex topics explained simply, no unnecessary jargon
- **Transparent**: Honest about capabilities and limitations

### 5.2 Brand Guidelines

All marketing materials must adhere to:

- Company name: "Light Speed Holdings" (not "LightSpeed" or "LSH")
- Product name: "AI Company Builder" (not "AI Company" or "the tool")
- Logo usage: Per brand assets in `static/` directory
- Color palette: Consistent with dashboard and website design
- Typography: Professional, readable fonts for all published content

### 5.3 Technical Accuracy

All marketing content that references the AI Company Builder must accurately describe:

- Component names: `AgentLoop`, `CostTracker`, `HITLGate`, `MessageBus`, `ModelRouter`
- Architecture: ReAct pattern, agentic loops, provider fallback chains
- Features: Multi-turn agentic loops, budget enforcement, HITL approval gates
- Commands: `ai-company` CLI syntax, `--help` output
- Never fabricate features or capabilities that do not exist in the codebase

### 5.4 Competitive Positioning

Key differentiators to emphasize:

1. **AI-native company structure**: Not just a tool, but a complete organizational framework
2. **Cost transparency**: Built-in LLM cost tracking and budget enforcement
3. **Human-in-the-loop**: Safety gates for dangerous operations
4. **Multi-provider support**: OpenAI, Anthropic, DeepSeek, Ollama with automatic fallback
5. **Local-first option**: Ollama integration for zero-cost local inference

## 6. Content Distribution

### 6.1 Distribution Channels

| Channel | Content Type | Frequency | Metrics |
|---------|-------------|-----------|---------|
| GitHub repository | Code, documentation, changelog | Continuous | Stars, forks, issues |
| Project website | Blog, tutorials, case studies | Biweekly | Page views, time on page |
| Twitter / X | Short-form updates, threads | 3x per week | Impressions, engagement |
| LinkedIn | Long-form posts, company updates | 2x per week | Reach, clicks |
| YouTube | Tutorials, demos, webinars | Monthly | Views, subscribers |
| Email newsletter | Product updates, blog digest | Monthly | Open rate, CTR |

### 6.2 Content Repurposing

Maximize content value through repurposing:

1. **Blog post** -> Social media thread -> Email newsletter excerpt
2. **Technical tutorial** -> YouTube video -> Blog post summary
3. **Case study** -> LinkedIn post -> Sales enablement material
4. **Documentation update** -> Tweet thread -> Email announcement

### 6.3 SEO Strategy

- Target keywords: "AI agent orchestration", "AI company builder", "LLM cost tracking"
- Each blog post targets 1-2 primary keywords
- Documentation pages are structured for search engine indexing
- Technical tutorials include structured data markup

## 7. Campaign Coordination

### 7.1 Campaign Planning

Campaigns follow a structured, approved process owned by the `cmo`:

1. **Objective**: Define measurable goals (signups, awareness, engagement) tied to pipeline targets
2. **Audience**: Identify target persona and channels with `sales_lead` input
3. **Messaging**: Develop core narrative aligned with brand voice (Section 5)
4. **Content**: Plan asset list; tasks issued to Content Creator via `MessageBus`
5. **Timeline**: Set milestones; load into editorial calendar under `Content Manager`
6. **Budget**: Estimate LLM generation cost + ad spend; submit to `cfo` if > $500
7. **Measurement**: Define KPIs (Section 9) **before** launch sign-off

The `cmo` approves the campaign brief; the `chief_of_staff` is notified for cross-department alignment.

### 7.2 Launch Campaign Template

For product launches or major updates:

| Phase | Duration | Activities |
|-------|----------|-----------|
| Pre-launch | 2 weeks | Teaser content, influencer outreach, press prep |
| Launch day | 1 day | Announcement, social blitz, email blast |
| Post-launch | 2 weeks | Follow-up content, user testimonials, metrics review |
| Sustained | Ongoing | SEO content, community engagement, iteration |

### 7.3 Content Approval & Brand Compliance

| Asset | Reviewer | Gate | Final Sign-off |
|-------|----------|------|----------------|
| Technical blog/tutorial | `cto` | Accuracy check | `cmo` |
| Public social post | `Content Manager` | Brand voice | `cmo` |
| Product claim / case study | `clo` | Compliance + claims | `cmo` + `ceo` |

Brand compliance is enforced by the `Content Manager` against Section 5. Any deviation is an escalation condition (Section 8).

### 7.4 Metrics Handoff to Sales

Weekly, the `cmo` publishes a campaign-performance summary to the `sales_lead`:

- Lead source volume by channel (GitHub, docs site, social, content)
- Marketing-qualified lead (MQL) count and BANT pre-score
- Top-performing assets for sales enablement

Handoff is recorded as a `MessageBus` task (`sender_id: cmo`, `receiver_id: sales_lead`) so pipeline attribution is auditable.

## 8. Escalation Procedures

| Condition | Escalate To | SLA |
|-----------|------------|-----|
| Brand violation detected | Marketing Lead | Immediate |
| Negative social media mention | Marketing Lead + CEO | 4 hours |
| Content approval delay | Content Manager | 24 hours |
| Budget overrun on campaign | CFO | 24 hours |
| Technical inaccuracy in published content | CTO | Immediate |
| Legal concern about content | Legal department | Immediate |

## 9. Key Performance Indicators

| KPI | Target | Frequency | Owner |
|-----|--------|-----------|-------|
| Blog post views | 500+ per post | Per post | Content Manager |
| Social media engagement rate | > 3% | Weekly | Content Creator |
| Email newsletter open rate | > 25% | Monthly | Content Manager |
| Documentation page views | 1000+ per month | Monthly | Content Manager |
| GitHub stars growth | > 10% MoM | Monthly | Marketing Lead |
| Content production volume | 8+ pieces per month | Monthly | Content Manager |
| Brand consistency score | >= 95% | Quarterly | Marketing Lead |

## 10. Compliance Requirements

- All published content must be reviewed before publication
- Technical claims must be verifiable against the codebase
- Copyright and licensing notices must be included where required
- Content must comply with platform-specific advertising guidelines
- User testimonials require written consent
- Content archives must be maintained for 2 years

## 11. Related Documents

- `docs/ARCHITECTURE.md` - Technical architecture for accurate content creation
- `docs/USER-GUIDE.md` - User-facing documentation
- `CHANGELOG.md` - Product updates for marketing announcements
- `docs/COMPANY-CONSTITUTION.md` - Brand values and messaging guidelines
- `static/` - Brand assets (logo, design system)

---

*This document is maintained by the Marketing department. Updates require Marketing Lead approval.*
