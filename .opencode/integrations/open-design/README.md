# Open Design Integration Guide

## Overview

This document describes how LightSpeed Holdings integrates with Open Design (open-design.ai) for designing and creating project artifacts using our agent-based creative production stack.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LightSpeed Design Stack                      │
├─────────────────────────────────────────────────────────────────┤
│  User Brief → Creative Director → Production Skill → QA Gate   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Open Design Integration                      │
├─────────────────────────────────────────────────────────────────┤
│  Brand Tokens → Design Prompt → Open Design CLI/Desktop → Export│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┤
│                    Output Formats                              │
├─────────────────────────────────────────────────────────────────┤
│  HTML │ SVG │ PNG │ PDF │ PPTX │ DOCX │ MP4 │ WebP            │
└─────────────────────────────────────────────────────────────────┘
```

## Team Composition

### Orchestrator
- **Creative Director** (`creative-director`)
  - Reads creative briefs
  - Routes to production skills
  - Enforces brand compliance
  - Manages artifact QA

### Production Agents
| Agent | Department | Primary Output | Open Design Use |
|-------|------------|----------------|-----------------|
| Product Designer | Product | Websites, landing pages, web apps | UI generation, prototypes |
| Presentation Designer | Marketing | Decks, keynotes, pitch decks | Slide design, animations |
| Document Designer | Marketing | Whitepapers, reports, proposals | Document layout, PDF export |
| Diagram Designer | Engineering | Architecture, process diagrams | Mermaid, SVG, D3 visuals |
| Visual Storyteller | Marketing | Infographics, one-pagers | Data visualization |
| Brand Advertising Designer | Marketing | Ads, banners, campaign collateral | Ad creative, social assets |

### Support Agents
| Agent | Department | Role |
|-------|------------|------|
| Research Lead | Marketing | Evidence-bounded content |
| Artifact QA Reviewer | Quality | Final approval gate |

## Integration Workflow

### 1. Brand System Loading
```python
# Load brand tokens
brand_tokens = load("brand/tokens/brand-tokens.json")

# Apply to Open Design
open_design.set_brand({
    "primary": brand_tokens["color"]["navy"]["value"],      # #070A40
    "accent1": brand_tokens["color"]["red"]["value"],       # #E63946
    "accent2": brand_tokens["color"]["cyan"]["value"],      # #00BFFF
    "typography": brand_tokens["typography"]["display"]["family"],  # Arial
    "spacing": brand_tokens["spacing"]["baseUnit"]          # 4px
})
```

### 2. Creative Brief Intake
The Creative Director asks 5 questions:
1. **Artifact type** - what class of output
2. **Audience** - who consumes it
3. **Objective** - what must it change
4. **Narrative** - core thesis/message
5. **Visual language** - constraints/desired feel

### 3. Production Routing
Based on artifact type, the Creative Director routes to:

| Brief Says | Production Skill | Open Design Mode |
|------------|------------------|------------------|
| Website / landing page | `ls-frontend-design` | AI UI Generator |
| Deck / keynote | `ls-presentation-design` | Slides mode |
| Whitepaper / report | `ls-document-design` | Document mode |
| Campaign (social) | `ls-social-media-design` | Image + HTML |
| Ads / banners | `ls-brand-advertising` | Image mode |
| Architecture diagram | `ls-diagramming` | Diagram mode |
| Infographic | `ls-visual-storytelling` | Infographic mode |

### 4. Open Design Execution

#### Option A: CLI Integration (Recommended)
```bash
# Create artifact via Open Design CLI
open-design create \
  --model claude-sonnet-4.5 \
  --prompt "Design a landing page for SADC policymakers..." \
  --brand brand/tokens/brand-tokens.json \
  --output output/design/landing-page.html \
  --format html
```

#### Option B: Desktop App Integration
1. Open Open Design desktop app
2. Sign in with AMR (no API key needed)
3. Select model (claude-sonnet-4.5 recommended)
4. Paste creative brief from Creative Director
5. Export artifact in required format

### 5. Quality Assurance
The Artifact QA Reviewer runs final checks:

- **Visual QA**: Spacing, hierarchy, balance, contrast, whitespace, alignment
- **Brand QA**: Colors, type, logo, tagline compliance
- **UX QA**: CTA clarity, overflow, navigation, responsiveness
- **Accessibility QA**: Contrast ratios, alt text, focus management, headings
- **Content QA**: Claims, citations, consistency, grammar, numbers

## Configuration Files

### Open Design Config
Location: `.opencode/integrations/open-design/config.json`

### Team Composition
Location: `.opencode/integrations/open-design/team.json`

### Brand Tokens
Location: `brand/tokens/brand-tokens.json`

### Brand Guidelines
Location: `brand/guidelines/brand-guidelines.md`

## Quick Start

### 1. Install Open Design
```bash
# Windows (portable zip)
# Download from https://github.com/nexu-io/open-design/releases

# Linux (Docker)
docker compose -f docker-compose.opendesign.yml up
```

### 2. Configure Integration
```bash
# The config files are already in place at:
# .opencode/integrations/open-design/config.json
# .opencode/integrations/open-design/team.json
```

### 3. Create First Artifact
```bash
# Via OpenCode (using Creative Director agent)
opencode --agent creative-director "Create a one-page landing page for SADC policymakers to download our Agentic AI whitepaper"

# Via Open Design CLI directly
open-design create --model claude-sonnet-4.5 --prompt "Design a SADC landing page"
```

## Brand Compliance Checklist

- [ ] Colors resolve to `brand-tokens.json` values only
- [ ] Logo is an official asset (path under `brand/logos/`)
- [ ] Type sizes are on the brand scale
- [ ] Spacing follows the 4px base scale
- [ ] Template used where one exists
- [ ] `™` on first mention; tagline correct

## Output Formats

| Format | Use Case | Tool |
|--------|----------|------|
| HTML | Web pages, landing pages | Open Design → HTML export |
| SVG | Diagrams, logos, icons | Open Design → SVG export |
| PNG | Social media, presentations | Open Design → PNG export |
| PDF | Whitepapers, reports | Open Design → PDF export |
| PPTX | Slide decks | python-pptx or Open Design |
| DOCX | Documents, proposals | python-docx or Open Design |
| WebP | Optimized web images | Open Design → WebP export |

## Troubleshooting

### Open Design CLI Not Found
```bash
# Verify installation
open-design --version

# Reinstall if needed
# Windows: Download portable zip from GitHub
# Linux: docker compose -f docker-compose.opendesign.yml up --build
```

### Brand Tokens Not Loading
```bash
# Verify token file exists
cat brand/tokens/brand-tokens.json

# Sync canonical assets
pwsh scripts/sync-brand.ps1
```

### Agent Not Routing Correctly
- Check `ls-creative-director` routing table
- Verify artifact type matches routing rules
- Ensure `ls-design-system` is loaded first

## References

- Open Design Documentation: https://open-design.ai/docs
- Open Design GitHub: https://github.com/nexu-io/open-design
- LightSpeed Design System: `brand/guidelines/brand-guidelines.md`
- Agent Registry: `company-registry.yaml`
