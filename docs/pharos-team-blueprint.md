# Pharos and Thought Leadership Team Blueprint

**Organization**: Light Speed Holdings
**Team Purpose**: Create thought leadership artifacts, LinkedIn series, executive communications, and Pharos department outputs
**Today's Date**: Mon Oct 26 2026

---

## 1. Team Composition

### Core Pharos Agents (from `pharos-agent-mapping.md`)

| Pharos Agent | Valid `subagent_type` | Primary Role |
|--------------|----------------------|--------------|
| `thought-leadership-lead` | `content-writer` | Strategy, narrative architecture, content calendar |
| `thought-leadership-author` | `content-writer` | Long-form writing, manifestos, LinkedIn posts, white papers |
| `agentic-research-lead` | `general` | Research, evidence synthesis, fact gathering |
| `agentic-policy-analyst` | `general` | Policy analysis, regulatory mapping, consultation drafting |
| `speaker-engagement-lead` | `general` | Speaking programs, workshop design, keynote scripts |
| `community-ecosystem-builder` | `general` | Community building, stakeholder maps, partnerships |
| `media-pr-relations` | `content-writer` | Press materials, op-eds, media pitches, brand consistency |
| `talent-academy-lead` | `general` | Academy design, certification, university partnerships |

### Production Skills (ls-* stack + Open Design render layer)

| Skill | Role in Thought Leadership Pipeline | Open Design Integration |
|-------|-------------------------------------|-------------------------|
| `ls-creative-director` | Orchestrator — routes brief to right production skill | Routes to `ls-od-deck` (slides mode), `ls-od-image` (image mode), `ls-od-catalogue` (template selection) |
| `ls-visual-storytelling` | Creates infographics, data stories, visual abstracts | Renders via `ls-od-image`; palette enforced post-render via `ls-od-brand` + checker |
| `ls-social-media-design` | Creates LinkedIn/X/IG/FB campaigns from a thesis | Renders via `ls-od-image`; `ls-od-catalogue` selects right template per platform |
| `ls-presentation-design` | Creates decks/keynotes/pitch decks (13-slide PPTX) | Renders via `ls-od-deck` (Slides mode); navy rail, cyan tagline "ASPIRE. ACT. ACHIEVE.", red accent |
| `ls-diagramming` | Creates architecture/strategy/process diagrams (Mermaid/SVG) | Renders via `ls-od-image`; brand palette applied post-render |
| `ls-brand-advertising` | Creates ads/banners/campaign collateral | Renders via `ls-od-image` (Image mode); budget gate enforced |
| `ls-document-design` | Creates whitepapers/reports/proposals/PDFs | Renders via `ls-od-image` (Document mode) or `ls-od-deck` |
| `ls-artifact-qa` | Final gatekeeper — visual/brand/UX/content QA | Validates Open Design output; runs palette checker green before APPROVE |
| `ls-od-runtime` | Daemon lifecycle, CLI verbs, MCP wiring, Windows failure modes | Starts/stops `od` daemon; verifies MCP registration; troubleshoots render failures |
| `ls-od-brand` | `design-systems/lightspeed/DESIGN.md`, brand-token handoff, brand QA | Ensures every Open Design render remaps to LightSpeed palette (navy #070A40, red #E63946, cyan #00BFFF) |
| `ls-od-catalogue` | Choosing between functional skills and design templates; id selection rules | Selects right Open Design template for each artifact type (deck, infographic, image, document) |

---

## 2. Toolset (Canonical 7 Tools + Open Design CLI)

All agents and skills use the canonical tool vocabulary:

| Tool | Purpose |
|------|---------|
| `read` | Read file contents |
| `edit` | Exact string replacement in files |
| `grep` | Search file contents with regex |
| `list` | List directory entries |
| `bash` | Execute shell commands |
| `webfetch` | Fetch web content (HTTP/HTTPS) |
| `task` | Launch sub-agent for complex work |

**Alias policy**: Only canonical names accepted in agent cards; legacy names (`write`, `execute`, `delegate`, `web_search`) must not appear in newly generated cards.

### Open Design CLI

| Command | Purpose |
|---------|---------|
| `od daemon start --headless` | Start the Open Design daemon |
| `od daemon status --json` | Check daemon status and installed plugins |
| `od daemon stop` | Stop the Open Design daemon |
| `od mcp` | Install MCP server in root opencode.json |
| `od mcp install opencode --print --json` | Print MCP registration JSON |
| `od skill list --json` | List all discoverable skills |
| `od design-systems list` | List available design systems |
| `od run start --project <projectId> --skill <id> --json` | Run a design template skill |
| `od media generate ...` then `od media wait <taskId>` | Generate images with budget gate |
| `open-design create --model claude-sonnet-4.5 --prompt "..." --brand brand/tokens/brand-tokens.json --output output/design/ --format html` | Create artifact via Open Design CLI |

**Open Design Config**: Location: `.opencode/integrations/open-design/config.json`
**Team Composition**: Location: `.opencode/integrations/open-design/team.json`

---

## 3. Workflow for LinkedIn Thought Leadership Series

### 3.1. End-to-End Pipeline (with Open Design Render Layer)

```text
thought-leadership-author
    │
    ├─► provides core thesis + narrative arc
    │
    ▼
ls-creative-director (orchestrator)
    │
    ├─► routes to ls-visual-storytelling for infographics → ls-od-image → remap palette via ls-od-brand → ls-artifact-qa
    │   │
    │   ├─► creates visual narrative (headline → key stat → context → problem → comparison → implication → opportunity → CTA)
    │   │
    │   └─► enforces LightSpeed palette post-render:
    │       - Remap to LS palette (navy #070A40 dominant, cyan #00BFFF secondary, red #E63946 for CTA)
    │       - Run palette checker: `uv run python .agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py <image> --tolerance 3`
    │       - Must PASS before submitting to ls-artifact-qa
    │
    ├─► routes to ls-social-media-design for campaign → ls-od-image (per-platform) → ls-artifact-qa
    │   │
    │   ├─► builds channel map (LinkedIn article + carousel + single image; X thread; IG carousel)
    │   │
    │   ├─► produces on-brand copy (builder register, no emojis, evidence-led)
    │   │
    │   ├─► ensures platform dimensions via ls-od-catalogue:
    │   │   - LinkedIn: 1200×627 (image mode)
    │   │   - X/Twitter: 1600×900 (image mode)
    │   │   - Instagram: 1080×1080 square (image mode), 1080×1920 story (image mode)
    │   │   - Facebook: 1200×628 (image mode)
    │   │
    │   └─► generates hashtag set (3–5 focused, #™ on first company mention)
    │
    └─► routes to ls-artifact-qa as final gate
        │
        ├─► visual QA (hierarchy, spacing, balance, contrast, whitespace, alignment, overflow)
        ├─► brand QA (palette green from checker, logo, type, tagline "ASPIRE. ACT. ACHIEVE.", ™ on first mention)
        ├─► UX QA (CTA clarity, navigation, responsive, tap targets ≥44px)
        ├─► accessibility QA (alt text, semantic heading order, focus indicators)
        └─► content QA (traceable facts, no invented stats, voice, citations)
```

### 3.2. Detailed Phase Breakdown (with Open Design Integration)

#### Phase 1: Strategy & Narrative (thought-leadership-lead + thought-leadership-author)
- **thought-leadership-lead**: Defines content calendar, narrative architecture, KPI targets (ATC >90%, velocity <60d, correction ratio, 3x capital efficiency)
- **thought-leadership-author**: Writes the core LinkedIn article, manifesto, or white paper
- **agentic-research-lead**: Gathers evidence, cites sources file:line, verifies registry counts against published figures
- **agentic-policy-analyst**: Maps regulatory context (National AI Strategy, Data Protection Act 2024, AU Continental AI Strategy, SADC digital transformation)

#### Phase 2: Visual Design (ls-visual-storytelling → ls-od-image → ls-od-brand)
- Creates infographics, data stories, visual abstracts using the visual narrative template:
  - Headline → Key statistic → Context → Problem visualization → Comparison → Implication → Opportunity → CTA
- Enforces LightSpeed brand palette post-render (Open Design path):
  - Render via `ls-od-image` with `--brand brand/tokens/brand-tokens.json`
  - Remap to LS palette (navy dominant, cyan accents, red for key number/CTA)
  - Run palette checker: `uv run python .agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py <image> --tolerance 3`
  - Must PASS before submitting to ls-artifact-qa

#### Phase 3: Campaign Packaging (ls-social-media-design → ls-od-image → ls-artifact-qa)
- Builds the complete multi-channel campaign from one thesis:
  - **LinkedIn**: long-form article (1), carousel (3), single image (1) — via `ls-od-image`
  - **X/Twitter**: thread (5 posts), single image — via `ls-od-image`
  - **Instagram**: carousel (up to 5), single post, story — via `ls-od-image`
  - **Facebook**: post + image — via `ls-od-image`
- Ensures every asset is on-brand (navy/red/cyan, official logo, tagline) — enforced by `ls-od-brand`
- Ensures every asset matches platform dimensions exactly — via `ls-od-catalogue`
- Carousels follow one consistent visual system across cards
- Copy: no emojis, no hype, evidence-led, `™` on first mention

#### Phase 4: Quality Gate (ls-artifact-qa)
- Runs all 5 QA passes (same as before, now also validates Open Design palette checker green):
  1. **Visual QA**: hierarchy, spacing, balance, contrast, whitespace, alignment, overflow
  2. **Brand QA**: palette (navy/red/cyan/greys/white only), logo, type, tagline, ™ — validates palette checker green
  3. **UX QA**: CTA clarity, navigation, responsive, interaction
  4. **Accessibility QA**: alt text (missingAltCount === 0), semantic heading order (emptyHeadingCount === 0), color not only signal
  5. **Content QA**: traceable facts/numbers, consistent names/spelling, grammar, voice (builder register, no emojis), citations/resolve links
- Verdict: APPROVE or FIX → RENDER AGAIN → RE-APPROVE

---

## 4. Skill Chains for Common Artifact Types (with Open Design Render Layer)

### 4.1. LinkedIn Series (Single Post + Carousel)

```
thought-leadership-author → ls-creative-director → ls-social-media-design → ls-od-image → ls-artifact-qa
                                                   ↘          ↙
                                              ls-visual-storytelling   (produces infographic for carousel)
```

**Outputs**:
- LinkedIn long-form article (1200×627, builder register voice, no emojis, evidence-led)
- LinkedIn carousel (3 cards, 1200×627 each, consistent visual system)
- LinkedIn single image (1200×627, navy background, official logo, white headline, cyan accent line)
- Hashtag set (3–5 focused, #™ on first company mention)
- CTA text (single action)

---

### 4.2. Executive Deck / Pitch Deck (13-slide PPTX)

```
thought-leadership-author → ls-creative-director → ls-presentation-design → ls-od-deck → ls-artifact-qa
```

**Open Design CLI** (executed behind the scenes):
```bash
open-design create \
  --model claude-sonnet-4.5 \
  --prompt "13-slide pitch deck for Series A investors in governed agentic AI organization" \
  --brand brand/tokens/brand-tokens.json \
  --output output/design/pitch-deck/ \
  --format pptx
```

**Outputs**:
- 13-slide pitch deck (navy cover, cyan tagline "ASPIRE. ACT. ACHIEVE.", red accent divider)
- Speaker notes (2–4 sentences per slide, proof point, transition)
- KPI cards (light-grey rounded rects, big navy figure, dark-grey label)
- Branded palette enforced throughout (navy #070A40, red #E63946, cyan #00BFFF)

---

### 4.3. Whitepaper / Report

```
thought-leadership-author → ls-creative-director → ls-document-design → ls-od-image → ls-artifact-qa
```

**Outputs**:
- Whitepaper/PDF with branded cover (navy, cyan tagline, red accent)
- Executive summary with traceable facts and sources
- KPI callout sections with brand palette
- No invented statistics — every number traces to company/, results/, or research

---

### 4.4. Infographic / Data Story

```
thought-leadership-author → ls-creative-director → ls-visual-storytelling → ls-od-image → ls-od-brand → ls-artifact-qa
```

**Outputs**:
- Infographic with LightSpeed palette enforcement
- Palette checker must PASS: `uv run python .agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py <image> --tolerance 3`
- Visual narrative: headline → key statistic → context → problem visualization → comparison → implication → opportunity → CTA
- Source trail for key statistic (file:line citation)
- Open Design render remapped to LightSpeed tokens before QA

---

### 4.5. Architecture / Strategy Diagram

```
agentic-research-lead → ls-creative-director → ls-diagramming → ls-od-image → ls-artifact-qa
```

**Outputs**:
- Mermaid diagram (flowchart, sequenceDiagram, stateDiagram, gantt, journey, erDiagram)
- Custom SVG with brand palette when Mermaid is too rigid — rendered via `ls-od-image`
- Node fills: navy `#070A40` (primary), white/grey-light `#F2F2F2` (supporting), cyan `#00BFFF` (accent), red `#E63946` (CTAs/warnings)
- Edge labels: dark-grey `#6B7280`; highlighted paths cyan
- Labels: Arial, 12–14pt node labels, 10–11pt edge labels

---

## 5. Pharos Department KPIs & Success Metrics

| KPI | Target | Source |
|-----|--------|--------|
| **ATC (Agent Trust Capacity)** | >90% | company-registry.yaml agent roles |
| **Velocity** | <60 days | cycle time from concept to published artifact |
| **Correction Ratio** | Low | percentage of FIX cycles in ls-artifact-qa |
| **3x Capital Efficiency** | 3x output per input unit | rough metric for artifact production cost |
| **Content Quality Score** | High | ls-artifact-qa content QA pass rate |
| **Brand Consistency Score** | High | ls-artifact-qa brand QA pass rate |
| **Research Citation Accuracy** | 100% | every claim has file:line source |

---

## 6. Approval & Governance

### 6.1. HITL Expiry Sweep (per §9.1 AGENTS.md)
- The `ApprovalGate` runs a periodic sweep that transitions expired `PENDING` approval requests to `EXPIRED`
- `EXPIRED` is a terminal state requiring re-submission
- Prevents stale approvals from blocking the inbox indefinitely

### 6.2. Skill Third-Party Transmission Ban (per §9.2 AGENTS.md)
- Skills must not send LightSpeed local data (code, docs, screenshots, prompts, memory) to third-party hosts unless the vendor is allow-listed in `docs/APPROVED-VENDORS.md` within the 90-day exception window
- CISO of record: Jack Mlusu (Human CEO)
- On unexpected transmission: stop the skill, do not retry, report skill + host + payload class to the CEO

### 6.3. Audit Evidence Separation (per §9.3 AGENTS.md)
- Auditor's read set and write set must be disjoint
- Evidence directory: `reports/evidence/`, `audit/*.jsonl`, `.opencode/audit/*`, `harness/changes/*/reviews/`, etc.
- Auditor output goes outside the evidence set: `reports/repo-audit-<AUDIT_DATE>.md`

### 6.4. Key Rotation (per §11 AGENTS.md)
- Every 90 days scheduled; immediately on suspected compromise
- Generate new keys, update `.env` (never commit to git), update deployed environments
- Verify health endpoints respond with new keys
- Revoke old keys after confirming new ones work
- Update `.env.example` if key format/naming changed
- Document rotation in CHANGELOG.md

---

## 7. Example: LinkedIn Intro Post Prompt

```
You are the thought-leadership-author for Light Speed Holdings Pharos department.

Write a LinkedIn intro post that introduces our agentic AI company building organization.

Requirements:
- Builder register voice: professional, no emojis, no hype, evidence-led
- One core thesis: governed agentic AI is the region's next growth lever
- Must cite exact agent count, department count, and governance mechanisms from company-registry.yaml
- File:line citations for every statistic
- Core thesis in first 2 sentences
- CTA: "Read our full whitepaper on lightspeedholdings.vercel.app"
- Hashtag set: max 5, #™ on first mention of company name
- Platform dimension: 1200×627 for accompanying visual
- No invented statistics
```

---

## 8. Example: Full LinkedIn Campaign Brief

```
ARTIFACT TYPE: social media campaign
AUDIENCE: SADC policymakers, AI regulators, prospective enterprise clients
OBJECTIVE: Establish authority, drive whitepaper downloads, generate inbound inquiries
CORE THESIS: Governed agentic AI organization delivers 3x capital efficiency vs. unstructured agent deployments
NARRATIVE ARC: hook → problem (unstructured agents → risk) → proof (3x efficiency data) → implication (region needs governance) → opportunity (LightSpeed's HITL model) → CTA (download whitepaper)
VISUAL LANGUAGE: LightSpeed design system default (navy/red/cyan, Arial)
BRAND BASE: always LightSpeed design system
STRUCTURE: hero → problem → proof → opportunity → CTA
CHANNELS: LinkedIn, X/Twitter, Instagram, Facebook
CTA: Download our free whitepaper on governed agentic AI
QA GATE: ls-artifact-qa (visual/brand/UX/content passes)
```

**Production Chain**: `ls-creative-director` → `ls-social-media-design` → `ls-visual-storytelling` → `ls-artifact-qa`

---

## 9. Related Resources & Cross-References

- **Pharos Agent → Valid `subagent_type` Mapping**: `docs/agents/pharos-agent-mapping.md`
- **Creative Production Stack**: `ls-creative-director` → one primary production skill + support → `ls-artifact-qa`
- **Brand Tokals**: `brand/tokens/brand-tokens.json`, `brand/guidelines/brand-guidelines.md`
- **LightSpeed Design System**: navy `#070A40`, red `#E63946`, cyan `#00BFFF`, Arial type scale, 4px grid
- **Digital Asset Register**: `docs/marketing/digital-asset-register.md`
- **Key Rotation Procedure**: `docs/DASHBOARD_KEY_ROTATION.md`
- **Approved Vendors**: `docs/APPROVED-VENDORS.md`
- **Skill Curration Policy**: `docs/SKILL_CURATION_POLICY.md`

---

## 10. Quick Start Commands

```bash
# Regenerate all agent cards
uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"

# Run thought leadership author
task(subagent_type="content-writer", prompt="You are the Thought Leadership Author for Light Speed Holdings Pharos department. Write a LinkedIn intro post introducing our agentic AI company building organization. Use builder register voice, cite exact metrics from company-registry.yaml, and include a CTA.")

# Run creative director to orchestrate a LinkedIn campaign
task(subagent_type="general", prompt="You are the LightSpeed Creative Director. Orchestrate a LinkedIn thought leadership campaign for our agentic AI organization. One core thesis, multi-channel campaign (LinkedIn article + carousel + X thread + Instagram carousel + Facebook post). Enforce LightSpeed brand palette (navy #070A40, red #E63946, cyan #00BFFF). No emojis, evidence-led voice, every claim must have a source.")

# Run QA on finished artifact
task(subagent_type="general", prompt="You are the ls-artifact-qa critic. Review the LinkedIn campaign artifact for: visual hierarchy, brand palette (navy/red/cyan), CTA clarity, accessibility (alt text, heading order), and content QA (traceable facts, no invented statistics, builder register voice). Output PASS/FAIL for each of the 5 passes with findings and fix instructions if any FAIL.")
```

---
*Blueprint generated Mon Oct 26 2026 for the Pharos and Thought Leadership Team at Light Speed Holdings.*
