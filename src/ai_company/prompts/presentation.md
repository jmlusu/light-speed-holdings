# Presentation Prompt Specification

## Overview

This is the single source of truth for presentation prompt templates used by the
AI agent slide deck pipeline. All presentation generation flows through these
prompts to ensure brand compliance and consistent narrative framing.

## Brand Tokens ( enforced in all prompts )

- **Navy**: `#070A40` — primary accent, used for ~80% of visual weight (left rail,
  primary text, primary backgrounds)
- **Red**: `#E63946` — secondary accent, used for ~10% of visual weight (highlight
  text, callout boxes, key metrics)
- **Cyan**: `#00BFFF` — tertiary accent, used for ~10% of visual weight (links,
  secondary highlights, decorative elements)
- **Grey**: `#F2F2F2` — background filler, used for non-brand areas

**80/10/10 Rule**: Navy dominates at 80%, red and cyan each capped at 10% of total
visual accent. No single artifact may exceed these ratios without explicit override.

## Prompt Templates

### Investor Pitch Deck

```
Generate a 14-slide investor pitch deck with the following structure:

1. Executive Summary — concise one-sentence value proposition
2. Problem & Market — quantify the pain and TAM
3. Solution & Product — how the product solves the problem
4. Business Model — revenue streams and pricing
5. Go-to-Market Strategy — launch plan and channels
6. Competitive Landscape — matrix and differentiators
7. Trajectory & Milestones — Y1/Y2 goals and key metrics
8. Key Decisions Required — governance gates (G1-G4) and MSAs/DPA
9. Customer Success Report — retention >90%, NPS >50
10. Financial Projections — ARR targets consistent with KPIs
11. Team & Advisors — founder-led with relevant experience
12. Key Metrics & KPIs — ATC >90%, correction ratio within target
13. Next Steps — before next round, $120K ARR run-rate
14. Closing — Aspire. Act. Achieve. strategic thesis

Brand enforcement:
- Navy left rail on all content slides
- Red used for key metrics and governance gates
- Cyan used for TAM figures and strategic thesis
- Grey #F2F2F2 for secondary backgrounds
- Slide 12 explicitly references: ATC >90% velocity, correction ratio within target
- Slide 14 explicitly references: Aspire. Act. Achieve. closing strategic thesis
```

### Board Meeting Deck

```
Generate a 10-slide board meeting deck with the following structure:

1. Operational Update — quarterly status and strategic direction
2. Financial Performance — revenue vs. board-approved targets
3. Key Metrics & KPIs — KPI trend analysis and performance
4. Product Roadmap — milestones and delivery timeline
5. Customer Success — retention rates and case studies
6. Competitive Landscape — market share analysis
7. Risk & Governance — risk assessment and framework update
8. Key Decisions Required — board authorization items
9. Strategic Priorities — next quarter focus
10. Closing — next meeting date and strategic thrust

Brand enforcement:
- Navy left rail on all content slides
- Red used for risk items and key decisions
- Cyan used for competitive positioning highlights
- Grey #F2F2F2 for financial tables and charts
- Slide 8 explicitly references: key decisions requiring board authorization
- Slide 9 explicitly references: strategic priorities for next quarter
```

### Keynote Deck

```
Generate a 13-slide keynote/presentation deck with the following structure:

1. Opening & Vision — why this moment matters now
2. Market Opportunity — size and growth trajectory
3. Our Solution — unique approach and value proposition
4. Customer Success Stories — real-world results and case studies
5. Competitive Differentiation — our differentiators in the market
6. Technology & Innovation — competitive advantage and IP
7. Roadmap & Milestones — key milestones over coming quarters
8. Key Decisions Required — decisions needed from leadership today
9. Financial Overview — unit economics and trajectory
10. Team Capabilities — execution capacity and team strengths
11. Future Outlook — where we're headed
12. Call to Action — what happens next
13. Closing thesis — aspirational but grounded

Brand enforcement:
- Navy left rail on all content slides
- Red used for key decisions and financial overview
- Cyan used for technology innovation and market opportunity
- Grey #F2F2F2 for roadmaps and future outlook
- Slide 8 explicitly references: decisions needed from leadership today
- Slide 12 explicitly references: call to action: what happens next
- Slide 13 explicitly references: closing thesis: aspirational but grounded
```

### Training Deck

```
Generate an 8-slide training deck with the following structure:

1. Introduction & Objectives — session goals and expected outcomes
2. Core Concepts — foundational knowledge and key concepts
3. Key Processes — how things work day-to-day
4. Best Practices — lessons learned and patterns
5. Hands-on Exercise — apply what you've learned
6. Q&A Session — address questions and clarify concepts
7. Decisions Required from participants — decisions needed
8. Wrap-up & Next Steps — continued learning roadmap

Brand enforcement:
- Navy left rail on all content slides
- Red used for key decisions and highlights
- Cyan used for core concepts and processes
- Grey #F2F2F2 for best practices and exercise instructions
- Slide 7 explicitly references: decisions required from participants
- Slide 8 explicitly references: wrap-up and next steps for continued learning
```

### Prompt Compliance

- All prompt templates MUST reference the brand tokens and 80/10/10 rule
- Slide-specific references (e.g., "Slide 12 explicitly references...") must appear
  exactly as specified — these are validation checkpoints
- No AI-generated wording that violates the brand voice (no generic "cutting-edge"
  "disruptive" language without specific brand-grounded justification)
- Narrative must be data-backed from company-registry.yaml where available
