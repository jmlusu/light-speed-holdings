# Design Team Quick Reference

## Team Roster

### Orchestrator
| Agent | Role | Department | Key Skills |
|-------|------|------------|------------|
| `creative-director` | Brief intake, routing, brand enforcement | Marketing | ls-creative-director, ls-design-system |

### Production Agents
| Agent | Role | Department | Key Skills |
|-------|------|------------|------------|
| `product-designer` | Websites, landing pages, web apps | Product | ls-frontend-design, ls-design-system, ls-artifact-qa |
| `presentation-designer` | Decks, keynotes, pitch decks | Marketing | ls-presentation-design, ls-design-system, ls-diagramming |
| `document-designer` | Whitepapers, reports, proposals | Marketing | ls-document-design, ls-design-system, ls-artifact-qa |
| `diagram-designer` | Architecture, process diagrams | Engineering | ls-diagramming, ls-design-system |
| `visual-storyteller` | Infographics, one-pagers, data stories | Marketing | ls-visual-storytelling, ls-design-system, ls-diagramming |
| `brand-advertising-designer` | Ads, banners, campaign collateral | Marketing | ls-brand-advertising, ls-design-system, ls-artifact-qa |

### Support Agents
| Agent | Role | Department | Key Skills |
|-------|------|------------|------------|
| `research-lead` | Evidence-bounded content | Marketing | k-dense-literature-review, k-dense-research-lookup |
| `artifact-qa-reviewer` | Final approval gate | Quality | ls-artifact-qa, ls-design-system |

## Brand Tokens (Memorize)

| Token | Hex | Usage |
|-------|-----|-------|
| Navy | `#070A40` | Primary surfaces, headlines, slide rails, logo text |
| Red | `#E63946` | Accent — CTAs, highlights, signal waves, key results |
| Cyan | `#00BFFF` | Accent — shield base, links on dark, taglines on navy |
| Light Grey | `#F2F2F2` | Backgrounds, cards, callouts |
| White | `#FFFFFF` | Clean backgrounds, text on navy |

## Typography
- Display/headings: **Arial 700**
- Body: **Arial 400**
- Scale: 36/32/28/24/18/16/14/13/12 pt

## Spacing
- Base unit: **4px**
- Scale: 4/8/12/16/24/32/48/64/96

## Routing Table

| Artifact Type | Production Skill | Open Design Mode |
|---------------|------------------|------------------|
| Website / landing page | `ls-frontend-design` | AI UI Generator |
| Deck / keynote / pitch | `ls-presentation-design` | Slides mode |
| Whitepaper / report / proposal | `ls-document-design` | Document mode |
| Campaign (social) | `ls-social-media-design` | Image + HTML |
| Ads / banners / posters | `ls-brand-advertising` | Image mode |
| Architecture / process diagram | `ls-diagramming` | Diagram mode |
| Infographic / one-pager | `ls-visual-storytelling` | Infographic mode |

## Quick Commands

### Via OpenCode
```bash
# Create a website
opencode --agent creative-director "Create a landing page for SADC policymakers"

# Create a deck
opencode --agent creative-director "Create a pitch deck for Series A investors"

# Create a whitepaper
opencode --agent creative-director "Create a whitepaper on Agentic AI in Malawi"

# Create an infographic
opencode --agent creative-director "Create an infographic showing AI adoption in SADC"
```

### Via Open Design CLI
```bash
# Basic creation
open-design create --model claude-sonnet-4.5 --prompt "Your prompt here"

# With brand tokens
open-design create --model claude-sonnet-4.5 --prompt "Your prompt" --brand brand/tokens/brand-tokens.json

# With output format
open-design create --model claude-sonnet-4.5 --prompt "Your prompt" --output output/design/ --format html
```

## QA Checklist

Before delivering any artifact, verify:

- [ ] Colors resolve to `brand-tokens.json` values only
- [ ] Logo is an official asset (path under `brand/logos/`)
- [ ] Type sizes are on the brand scale
- [ ] Spacing follows the 4px base scale
- [ ] Template used where one exists
- [ ] `™` on first mention; tagline correct
- [ ] Accessibility: contrast, alt text, focus, headings
- [ ] Content: claims, citations, consistency

## Escalation Path

| Issue | Escalate To |
|-------|-------------|
| Architectural decisions | cto |
| Cross-team coordination | cmo |
| Brand compliance issues | brand-strategist |
| Quality gate failures | qa-lead |
| Budget/cost concerns | cfo |
