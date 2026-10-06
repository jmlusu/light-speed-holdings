# Customer Journey & Conversion Architecture

**Project:** LightSpeed Holdings Website
**Document Type:** Product / UX / Conversion Architecture Specification
**Status:** Implementation Authority
**Audience:** OpenCode agents, frontend engineers, UX/UI agents, content agents, QA agents
**Scope:** Website customer journey, information architecture, navigation, conversion pathways, engagement logic, and journey instrumentation

---

## 1. Purpose

This document defines the **Customer Journey & Conversion Architecture** for the LightSpeed Holdings website.

It is an implementation specification.

Agents implementing the website MUST use this document to understand:

* why each major route exists
* what visitor intent each route serves
* how visitors should move between routes
* what information should be progressively disclosed
* what action each page should encourage
* how Solutions, Sectors, Proof, Insights, About, Ask LightSpeed, and Contact work together
* how the website transitions visitors from awareness to meaningful engagement
* how engagement signals can be used to identify warmer prospects
* how the website supports both education and commercial conversion

This document does **not** replace visual design specifications, brand guidelines, technical architecture, content specifications, or application architecture.

It defines the **journey logic connecting those components**.

---

# 2. Core Principle

The LightSpeed website is an:

> **Intent-driven, progressive-disclosure experience.**

The website must not force visitors through a single linear sequence.

Visitors may enter through any route, page, search result, shared link, insight, or direct URL.

However, the architecture should ensure that visitors can progressively move from:

```text
Awareness
    ↓
Understanding
    ↓
Relevance
    ↓
Credibility
    ↓
Fit
    ↓
Engagement
    ↓
Qualified Opportunity
```

The website should help visitors answer increasingly important questions:

1. **What is LightSpeed?**
2. **What does LightSpeed actually do?**
3. **Could LightSpeed solve a problem I have?**
4. **Does LightSpeed understand my sector or context?**
5. **What evidence supports its claims?**
6. **How would this apply to my organization?**
7. **How can I engage LightSpeed?**

---

# 3. Design Philosophy

The website must balance:

* clarity
* progressive disclosure
* credibility
* transparency
* exploration
* education
* commercial intent
* human connection
* AI-native interaction

The site should feel like a **guided exploration**, not a brochure.

Visitors should be able to explore freely while always having a logical next step.

---

# 4. Primary Journey Model

The canonical customer journey is:

```text
AWARENESS
    ↓
What is LightSpeed?
    ↓
UNDERSTANDING
    ↓
What does LightSpeed do?
    ↓
RELEVANCE
    ↓
Can LightSpeed solve my problem?
    ↓
SECTOR FIT
    ↓
Does LightSpeed understand my context?
    ↓
CREDIBILITY
    ↓
What evidence supports this?
    ↓
FIT
    ↓
Could this work for my organization?
    ↓
ENGAGEMENT
    ↓
Let's talk / Ask LightSpeed / Subscribe
    ↓
QUALIFICATION
    ↓
Discovery
    ↓
Potential Engagement
```

This model should inform page hierarchy, CTA placement, internal linking, and interaction design.

---

# 5. Visitor Types

The website should support multiple visitor types without forcing visitors to explicitly identify themselves.

## 5.1 Executive / Decision Maker

Typical questions:

* What does LightSpeed do?
* What business problems can it address?
* What changes would LightSpeed create?
* What evidence exists?
* How would an engagement work?

Typical journey:

```text
Home
→ Solutions
→ Proof
→ Contact
```

---

## 5.2 Technology / Transformation Leader

Typical questions:

* What is an AI-native company?
* What is the AI Company Builder?
* What is the 90-agent workforce?
* How does the operating model work?
* How could this integrate with existing systems?

Typical journey:

```text
Home
→ AI Company Builder
→ 90-Agent Workforce
→ Solutions
→ Proof
→ Contact
```

---

## 5.3 Sector / Industry Visitor

Typical questions:

* Does LightSpeed understand my sector?
* What problems are relevant to my sector?
* Which solutions apply?
* What evidence exists?

Typical journey:

```text
Home
→ Sectors
→ Relevant Solution
→ Proof
→ Contact
```

---

## 5.4 Research / Thought Leadership Visitor

Typical questions:

* What does LightSpeed think about Agentic AI?
* What is LightSpeed's perspective?
* What research or analysis has LightSpeed published?
* What topics does LightSpeed cover?

Typical journey:

```text
Insights
→ Topic
→ Related Solution / Sector
→ Ask LightSpeed
→ Subscribe
```

---

# 6. Primary Journey Stages

## Stage 1 — Awareness

### Visitor question

> "What is LightSpeed?"

### Primary route

`/`

### Website responsibility

The homepage must establish:

* LightSpeed identity
* core proposition
* relevance
* differentiation
* initial credibility
* available paths for exploration

### Required outcome

The visitor should understand:

> What LightSpeed is, what it does, and where to go next.

### Primary actions

Depending on visitor intent:

* Explore Solutions
* Explore Sectors
* Understand the AI Company Builder
* View Proof
* Read Insights
* Ask LightSpeed
* Contact LightSpeed

---

# 7. Homepage Architecture

The homepage should use progressive disclosure.

The conceptual sequence is:

```text
Orientation
    ↓
Core Proposition
    ↓
Operating Model
    ↓
AI Company Builder
    ↓
90-Agent Workforce
    ↓
Solutions
    ↓
Sectors
    ↓
Proof
    ↓
Insights
    ↓
About
    ↓
Engagement CTA
```

This sequence represents the underlying information architecture.

It does **not** mean visitors must read every section.

The interface should provide opportunities to branch into deeper content.

---

# 8. Homepage Routing Principle

The homepage should quickly establish three major visitor pathways.

## Path 1 — I Have a Business Problem

```text
Home
→ Solutions
```

## Path 2 — I Want to Understand AI-Native Business

```text
Home
→ AI Company Builder
→ Operating Model
→ 90-Agent Workforce
```

## Path 3 — I Want to Work With LightSpeed

```text
Home
→ Proof
→ Contact
```

These pathways should be visually and structurally obvious.

---

# 9. Stage 2 — Exploration & Consideration

The exploration layer consists primarily of:

* Solutions
* Sectors
* Proof
* Insights
* About
* Ask LightSpeed

Visitors may enter any of these directly.

The website must provide contextual links between them.

---

# 10. Solutions Journey

## Route

`/solutions`

## Purpose

Help visitors determine whether LightSpeed can address a specific problem or need.

The existing architecture defines **5 solution categories**.

Each solution should use a consistent framework.

---

## Solution Framework

Each solution should answer:

1. What problem does this address?
2. Who is it for?
3. What changes?
4. What does LightSpeed build or enable?
5. What evidence supports the proposition?

---

## Solution Journey

```text
Problem
    ↓
Solution
    ↓
How it works
    ↓
Relevant sectors
    ↓
Evidence
    ↓
Engagement
```

---

## Solution Page Required Actions

### Primary CTA

**Discuss This Solution**

### Secondary actions

* Explore relevant sectors
* View evidence
* Ask LightSpeed
* Explore another solution
* Contact LightSpeed

---

# 11. Problem → Solution Architecture

The website should not require visitors to already understand LightSpeed's terminology.

Where possible, visitors should be able to enter through a problem.

Example:

```text
"I have too many manual workflows"
        ↓
Workflow Collapsing
        ↓
How LightSpeed approaches the problem
        ↓
Relevant evidence
        ↓
Potential application
        ↓
Discuss This Solution
```

This is a core conversion mechanism.

The site should explain the problem before expecting visitors to understand the solution terminology.

---

# 12. Sector Journey

## Route

`/sectors`

## Purpose

Help visitors determine whether LightSpeed understands their industry or operating context.

The existing architecture defines **9 sectors**.

Each sector must communicate the level of available evidence honestly.

---

## Evidence Tiers

The current journey specification uses:

* Proven experience
* Future opportunity

These sector evidence levels must not be exaggerated.

If additional evidence classifications are introduced, they must be defined consistently across the site.

---

## Sector Journey

```text
Sector
    ↓
Sector challenges
    ↓
Relevant opportunities
    ↓
Relevant LightSpeed solutions
    ↓
Evidence
    ↓
Engagement
```

---

## Sector Page Actions

Primary:

**Explore Solutions for This Sector**

Secondary:

* View Proof
* Ask LightSpeed
* Explore another sector
* Contact

---

# 13. Cross-Linking Between Solutions and Sectors

Solutions and sectors must not operate as isolated sections.

A solution page should identify relevant sectors.

A sector page should identify relevant solutions.

The relationship should be bidirectional:

```text
Solution
   ↕
Sector
```

Example:

```text
Sector Page
    ↓
Relevant Problem
    ↓
Relevant Solution
    ↓
Evidence
    ↓
Contact
```

and:

```text
Solution Page
    ↓
Relevant Sector
    ↓
Sector-specific application
    ↓
Evidence
    ↓
Contact
```

---

# 14. Proof & Trust Journey

## Route

`/proof`

## Purpose

Establish credibility through transparent evidence.

The Proof experience must reinforce LightSpeed's commitment to honest representation.

---

## Evidence Ladder

The current model is:

```text
Proposed
    ↓
Verified
    ↓
Established
    ↓
Market-leading
```

The labels must only be used where supported by evidence.

---

## Proof Principles

The website must:

* avoid inflated metrics
* avoid unsupported claims
* distinguish proposals from demonstrated capabilities
* distinguish demonstrated capabilities from established capabilities
* make evidence understandable
* connect claims to their supporting context

The LightSpeed agent count should remain consistent with the authoritative company registry.

**Current canonical count: 90 agents.**

Agents must not reintroduce older agent-count figures.

---

# 15. Proof Should Exist Throughout the Website

Proof should not be confined to `/proof`.

Relevant claims on:

* Home
* Solutions
* Sectors
* AI Company Builder
* 90-Agent Workforce
* About
* Insights

should link or refer to appropriate evidence where applicable.

The goal is:

```text
Claim
 ↓
Evidence status
 ↓
Supporting context
```

not:

```text
Marketing claim
 ↓
Separate proof page
```

---

# 16. Insights Journey

## Route

`/insights`

## Purpose

Build sustained thought leadership and allow visitors to deepen their understanding of LightSpeed's thinking.

The current architecture defines **12 content categories**.

These include topics such as:

* Agentic AI governance
* AI implementation
* and other LightSpeed-defined thought leadership categories

The authoritative content taxonomy should remain controlled by the project's content specification.

---

## Insights Journey

```text
Topic
    ↓
Insight
    ↓
Related concept
    ↓
Relevant solution / sector
    ↓
Ask LightSpeed
    ↓
Subscribe or engage
```

---

## Insights CTAs

Primary:

**Explore Related Thinking**

Secondary:

* Ask LightSpeed
* Explore Solutions
* Explore Sectors
* Subscribe
* Contact

---

# 17. Newsletter Journey

Newsletter signup is a relationship-building mechanism.

The journey is:

```text
Insight
    ↓
Interest
    ↓
Newsletter signup
    ↓
Verified email
    ↓
Nurture / continued thought leadership
    ↓
Returning visitor
    ↓
Potential engagement
```

Newsletter signup must use the required Turnstile verification.

The website must clearly communicate the purpose of subscribing.

Do not treat newsletter signup as equivalent to a qualified sales lead.

---

# 18. About & Team Journey

## Route

`/about`

## Purpose

Humanize the organization and explain how LightSpeed operates.

The current architecture identifies:

* 20-department structure
* 90-agent operating model
* leadership
* governance transparency

The About experience should answer:

> "Who is behind LightSpeed and how is the organization structured?"

---

## About Journey

```text
Who is LightSpeed?
    ↓
Leadership
    ↓
Operating model
    ↓
Departments
    ↓
AI workforce
    ↓
Governance
    ↓
Proof / credibility
    ↓
Engagement
```

About should not become a generic corporate history page.

It should explain the operating model that makes LightSpeed distinctive.

---

# 19. Ask LightSpeed

## Route

`/ask`

## Purpose

Provide an AI-native conversational entry point into the LightSpeed knowledge experience.

Ask LightSpeed should help visitors answer questions without requiring them to navigate manually through every page.

---

## Example questions

Visitors may ask:

* What is LightSpeed?
* What is an AI-native company?
* What is the AI Company Builder?
* What is workflow collapsing?
* What solutions does LightSpeed provide?
* What sectors does LightSpeed serve?
* What is the 90-agent workforce?
* What evidence supports this capability?
* How can I work with LightSpeed?

---

## Knowledge Boundary

Ask LightSpeed must operate within an explicit knowledge boundary.

It must not invent:

* capabilities
* clients
* results
* metrics
* sector experience
* agent counts
* partnerships
* certifications
* evidence

The system must distinguish between:

* documented fact
* proposed capability
* interpretation
* unavailable information

When the answer is outside the defined knowledge boundary, the system should clearly communicate that limitation.

---

# 20. Contact & Engagement Journey

## Route

`/contact`

## Purpose

Convert meaningful interest into direct engagement.

The primary contact framing is:

> **Tell Us Where You Are**

The contact experience should encourage visitors to describe their situation rather than simply asking:

> "How can we help?"

---

## Contact Journey

```text
Visitor understands problem
        ↓
Explores relevant solution
        ↓
Reviews evidence
        ↓
Determines potential fit
        ↓
Tell Us Where You Are
        ↓
Inquiry submitted
        ↓
Qualification
        ↓
Discovery
```

---

## Contact Form Principles

The form should capture enough information to support qualification without creating unnecessary friction.

At minimum, the experience should allow the visitor to communicate:

* who they are
* organization/context
* problem or opportunity
* relevant area of interest
* desired next step

Turnstile verification is required.

---

# 21. Commercial Journey

The website is part of the LightSpeed commercial system.

The commercial journey is:

```text
Awareness
    ↓
Problem recognition
    ↓
Solution exploration
    ↓
Sector relevance
    ↓
Evidence
    ↓
Potential fit
    ↓
Contact
    ↓
Qualification
    ↓
Discovery
    ↓
Problem definition
    ↓
Potential solution
    ↓
Proposal
    ↓
Engagement
```

The website itself does not need to implement every downstream commercial stage.

However, the website architecture must support the transition into them.

---

# 22. Content Journey vs Commercial Journey

These journeys must be treated separately.

## Content Journey

```text
Home
→ Insights
→ Topic
→ Sector
→ Solution
→ Proof
→ Ask LightSpeed
```

Purpose:

**Education and authority**

---

## Commercial Journey

```text
Home
→ Problem
→ Solution
→ Evidence
→ Contact
→ Discovery
→ Engagement
```

Purpose:

**Qualified opportunity**

---

## Relationship Journey

```text
Insight
→ Newsletter
→ Returning visitor
→ Ask LightSpeed
→ Further content
→ Conversation
```

Purpose:

**Long-term relationship**

---

# 23. Visitor Intent Model

Every major page should be designed around visitor intent.

| Intent            | Visitor question             | Primary destination |
| ----------------- | ---------------------------- | ------------------- |
| Awareness         | What is LightSpeed?          | `/`                 |
| Problem discovery | Can LightSpeed solve this?   | `/solutions`        |
| Sector relevance  | Do you understand my sector? | `/sectors`          |
| Credibility       | Can I trust the claim?       | `/proof`            |
| Expertise         | What does LightSpeed think?  | `/insights`         |
| Organization      | Who is behind this?          | `/about`            |
| Immediate answer  | Can I ask a question?        | `/ask`              |
| Commercial intent | I want to talk               | `/contact`          |

---

# 24. Page CTA Architecture

Every major page MUST have:

1. one primary action
2. contextual secondary actions
3. at least one logical path deeper into the journey

The primary action must reflect the visitor's likely intent.

---

## Example: Solutions

Primary:

**Discuss This Solution**

Secondary:

* Relevant sectors
* Proof
* Ask LightSpeed

---

## Example: Sectors

Primary:

**Explore Solutions for This Sector**

Secondary:

* Proof
* Ask LightSpeed
* Contact

---

## Example: Proof

Primary:

**Discuss an Engagement**

Secondary:

* Solutions
* Sectors
* Ask LightSpeed

---

## Example: Insights

Primary:

**Explore Related Thinking**

Secondary:

* Subscribe
* Ask LightSpeed
* Solutions
* Contact

---

# 25. Navigation Architecture

The global navigation should make the major journey paths discoverable.

Core navigation destinations:

```text
Solutions
Sectors
Proof
Insights
About
Ask LightSpeed
Contact
```

The exact visual navigation implementation is governed by the visual/design specifications.

The journey architecture requires that these destinations remain logically connected.

---

# 26. Contextual Navigation

Every content page should expose relevant next steps.

Avoid dead-end pages.

A visitor reading a solution should be able to reach:

* relevant sectors
* relevant proof
* related insights
* Ask LightSpeed
* Contact

A visitor reading an insight should be able to reach:

* related solutions
* relevant sectors
* Ask LightSpeed
* newsletter
* Contact

A visitor viewing a sector should be able to reach:

* relevant solutions
* proof
* related insights
* Contact

---

# 27. Engagement Levels

The site should conceptually distinguish engagement intensity.

## Level 1 — Awareness

Examples:

* Homepage visit
* Basic page view

---

## Level 2 — Exploration

Examples:

* Multiple pages viewed
* Solution exploration
* Sector exploration

---

## Level 3 — Consideration

Examples:

* Proof viewed
* Multiple solutions explored
* Ask LightSpeed interaction
* Repeated site visits

---

## Level 4 — Intent

Examples:

* Contact CTA clicked
* Contact page reached
* Solution-specific CTA selected
* Engagement request initiated

---

## Level 5 — Conversion

Examples:

* Qualified inquiry
* Discovery initiated
* Commercial conversation

The site should not expose these internal engagement classifications to visitors unless explicitly designed to do so.

---

# 28. Lead Qualification Signals

Potentially useful signals include:

* number of relevant pages viewed
* solutions explored
* sectors explored
* proof content viewed
* Ask LightSpeed usage
* newsletter signup
* contact CTA interaction
* contact form submission
* repeat engagement

These signals are informational.

They must not be treated as proof of buying intent by themselves.

A newsletter subscriber is not automatically a qualified lead.

---

# 29. Post-Engagement Journey

After contact submission:

```text
Inquiry
    ↓
Receipt / acknowledgement
    ↓
Qualification
    ↓
Discovery
    ↓
Problem definition
    ↓
Potential solution
    ↓
Evidence / demonstration
    ↓
Proposal
    ↓
Engagement
```

The website should provide a clear confirmation after form submission.

The visitor should understand:

* that the submission was received
* what happens next
* what information may be required
* how LightSpeed will follow up

---

# 30. Trust Architecture

Trust should accumulate progressively.

The journey should move from:

```text
Identity
    ↓
Clarity
    ↓
Specificity
    ↓
Evidence
    ↓
Transparency
    ↓
Human connection
    ↓
Conversation
```

Important trust mechanisms include:

* honest evidence tiers
* accurate 90-agent count
* transparent operating model
* leadership visibility
* clear governance
* clear knowledge boundaries
* privacy and terms
* truthful representation of experience

---

# 31. Legal / Compliance Journey

The website must provide access to:

* Privacy
* Terms
* other required legal/compliance information

These are not primary conversion pages.

They support:

```text
Due diligence
    ↓
Trust
    ↓
Informed engagement
```

Legal content must remain accessible without interrupting the primary journey.

---

# 32. SEO / Direct Entry

Visitors may enter through:

* search engines
* shared links
* social media
* LinkedIn
* direct URL
* newsletter
* external references
* internal navigation

Therefore, every major page must be able to function as a **valid entry point**.

A visitor arriving directly at:

`/solutions`

should not need to visit the homepage first.

The page must establish:

* what the visitor is viewing
* why it matters
* where they can go next

---

# 33. No Dead Ends

No major journey page should end without a meaningful next action.

Bad:

```text
Content
↓
END
```

Preferred:

```text
Content
↓
Relevant next action
↓
Related content / solution / proof / Ask / Contact
```

---

# 34. Mobile Journey

The journey architecture applies equally to mobile.

Mobile implementation must preserve:

* primary CTA visibility
* contextual navigation
* progressive disclosure
* Ask LightSpeed accessibility
* readable evidence
* clear form progression

Do not solve mobile by simply stacking the desktop layout.

The visitor journey must remain coherent.

---

# 35. Accessibility

Journey-critical interactions must remain accessible.

This includes:

* navigation
* CTAs
* forms
* accordions
* filters
* evidence indicators
* Ask LightSpeed
* newsletter signup
* contact flow

Visitors must not be required to rely exclusively on animation, hover, color, or visual effects to understand the journey.

---

# 36. Analytics / Journey Instrumentation

The implementation should provide a foundation for measuring journey progression.

Recommended event categories:

```text
page_view
solution_view
sector_view
proof_view
insight_view
ask_started
ask_completed
newsletter_started
newsletter_completed
contact_started
contact_completed
cta_clicked
```

Where practical, contextual metadata should identify:

* route
* content type
* solution
* sector
* CTA
* journey stage

Do not collect unnecessary personal information merely for analytics.

---

# 37. Journey KPI Framework

Recommended measurement model:

| Stage         | Example measurement           |
| ------------- | ----------------------------- |
| Awareness     | Homepage engagement           |
| Exploration   | Solution / sector exploration |
| Consideration | Proof engagement              |
| Education     | Insight engagement            |
| Interaction   | Ask LightSpeed usage          |
| Relationship  | Newsletter signup             |
| Intent        | Contact CTA interaction       |
| Conversion    | Qualified inquiry             |
| Commercial    | Discovery meeting             |
| Pipeline      | Qualified opportunity         |

These metrics are measurement categories, not predetermined targets.

---

# 38. Cross-Route Relationship Model

The conceptual relationship between major routes is:

```text
                         ┌──────────────┐
                         │     HOME     │
                         └──────┬───────┘
                                │
              ┌─────────────────┼─────────────────┐
              ↓                 ↓                 ↓
        ┌───────────┐     ┌───────────┐     ┌───────────┐
        │ SOLUTIONS │ ←→  │  SECTORS  │     │  INSIGHTS │
        └─────┬─────┘     └─────┬─────┘     └─────┬─────┘
              │                 │                 │
              └─────────────────┼─────────────────┘
                                ↓
                         ┌──────────────┐
                         │    PROOF     │
                         └──────┬───────┘
                                │
                    ┌───────────┼───────────┐
                    ↓           ↓           ↓
               ┌────────┐ ┌──────────┐ ┌──────────┐
               │ ABOUT  │ │   ASK    │ │ CONTACT  │
               └────────┘ │LIGHTSPEED│ └──────────┘
                          └──────────┘
```

This is a conceptual journey model, not a literal UI requirement.

---

# 39. Implementation Rules for OpenCode Agents

## Rule 1 — Do not implement routes in isolation

Every route must be evaluated as part of the larger journey.

---

## Rule 2 — Do not create dead-end pages

Every major page needs logical next actions.

---

## Rule 3 — Preserve the canonical 90-agent model

Do not reintroduce previous agent counts.

The canonical model is:

**90 agents.**

---

## Rule 4 — Preserve evidence honesty

Do not upgrade:

* Proposed → Verified
* Verified → Established
* Established → Market-leading

without authoritative project evidence.

---

## Rule 5 — Do not invent proof

Agents must not invent:

* clients
* metrics
* case studies
* results
* partnerships
* certifications
* market position
* sector experience

---

## Rule 6 — Do not flatten progressive disclosure

Do not turn every page into a large wall of information.

Use:

* hierarchy
* sections
* progressive disclosure
* contextual links
* expandable content where appropriate
* focused CTAs

---

## Rule 7 — Do not make every CTA “Contact Us”

The CTA must reflect visitor intent.

Use contextual actions such as:

* Explore Solutions
* Explore This Sector
* View Evidence
* Ask LightSpeed
* Discuss This Solution
* Subscribe
* Contact LightSpeed

---

## Rule 8 — Do not force linear navigation

Visitors must be able to enter and exit through any major route.

---

## Rule 9 — Preserve direct-entry usability

Every major route must make sense when entered directly.

---

## Rule 10 — Preserve the LightSpeed knowledge boundary

Ask LightSpeed must not manufacture answers outside the authoritative knowledge base.

---

# 40. Definition of Done

The customer journey implementation is not complete merely because all routes exist.

The implementation is complete when:

### Architecture

* [ ] All major journey routes exist
* [ ] Routes are logically connected
* [ ] Direct-entry routes are understandable
* [ ] No major page is a dead end

### Visitor Intent

* [ ] Each major page has a clear visitor purpose
* [ ] Primary CTAs reflect page intent
* [ ] Secondary paths provide contextual exploration

### Solutions

* [ ] Solutions connect to sectors
* [ ] Solutions connect to proof
* [ ] Solutions provide clear engagement pathways

### Sectors

* [ ] Sectors connect to relevant solutions
* [ ] Sector evidence is represented honestly
* [ ] Sector pages provide clear next actions

### Proof

* [ ] Evidence ladder is implemented consistently
* [ ] Unsupported claims are not introduced
* [ ] Proof is connected contextually to claims
* [ ] Canonical 90-agent count is preserved

### Insights

* [ ] Insights connect to relevant solutions/sectors
* [ ] Newsletter journey works
* [ ] Ask LightSpeed pathway is available

### Ask LightSpeed

* [ ] Knowledge boundary is respected
* [ ] Unknown/out-of-bound questions are handled appropriately
* [ ] Relevant site content can be discovered through the interaction

### Contact

* [ ] Contact journey is clear
* [ ] Form has appropriate qualification information
* [ ] Turnstile verification works
* [ ] Submission confirmation exists

### Conversion

* [ ] Engagement pathways are measurable
* [ ] CTA interactions can be instrumented
* [ ] Contact and newsletter events can be tracked
* [ ] Post-contact transition is clearly defined

### UX

* [ ] Desktop journey works
* [ ] Mobile journey works
* [ ] Accessibility is preserved
* [ ] Progressive disclosure remains intact
* [ ] Visual design remains consistent with the authoritative LightSpeed design system

---

# 41. Agent Priority Order

When implementation conflicts arise, agents should prioritize:

```text
1. Authoritative project specifications
2. Brand / design system
3. Customer Journey & Conversion Architecture
4. Existing functional requirements
5. Route-specific content specifications
6. Implementation convenience
```

Implementation convenience must never override the intended customer journey.

---

# 42. Change Control

Agents must not silently redefine:

* journey stages
* visitor intent
* CTA meaning
* evidence levels
* canonical agent count
* knowledge boundaries
* route responsibilities

If implementation reveals a genuine architectural conflict, document the conflict rather than silently changing the specification.

---

# 43. Canonical Journey Summary

The LightSpeed website should ultimately enable this experience:

```text
                    LIGHTSPEED
                         │
                         ↓
                "What is this?"
                         │
                         ↓
                "What does it do?"
                         │
                         ↓
              "Can it solve my problem?"
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
         "My sector?"          "My problem?"
              ↓                     ↓
          SECTORS               SOLUTIONS
              └──────────┬──────────┘
                         ↓
                 "Can I trust this?"
                         │
                         ↓
                       PROOF
                         │
                         ↓
              "Could this work for me?"
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
            ASK       INSIGHTS    ABOUT
              └──────────┼──────────┘
                         ↓
                 "I want to engage"
                         │
                         ↓
                      CONTACT
                         │
                         ↓
                    QUALIFIED
                    CONVERSATION
                         │
                         ↓
                    ENGAGEMENT
```

---

# 44. Final Implementation Principle

The LightSpeed website should not merely answer:

> **"What pages should we build?"**

It should answer:

> **"What does the visitor need to understand next, and what is the most useful action we can offer them at that point?"**

Every implementation decision should reinforce that principle.

The website is successful when a visitor can move naturally from:

**understanding → relevance → trust → fit → engagement**

without being forced through a rigid sequence and without being overwhelmed by information.

---

**End of Customer Journey & Conversion Architecture**
