# Pharos Agentic Research Lead Skill

**Purpose:** Conduct primary, authoritative research that converts Lightspeed Holdings' engineering into citable public artifacts. Use when you need evidence synthesis, use-case census, benchmark methodology, or source-cited fact gathering for Pharos thought-leadership content.

## When to Use

- Need quantified metrics for CEO communications (agent counts, governance mechanisms, deployment numbers)
- Building the "State of Agentic AI in Malawi" or SADC readiness research
- Maintaining a use-case census (SME, health/M&E, VSLA/SACCO finance, public services)
- Tracking policy milestones (National AI Strategy, Data Protection Act 2024, AU Continental AI Strategy, SADC digital transformation)
- Normalizing Lightspeed KPIs into public benchmarks
- Any claim that needs a high-trust primary source

## Inputs

- Research question or content area
- Target artifact type (post, white paper, manifesto, monitor, briefing)

## Workflow

1. **Scope the claim** — identify what needs evidence
2. **Search repo sources** — company-registry.yaml, manifesto-draft.md, positioning.md, README.md, config/company/*.yaml, BRAND_DEPLOYMENT_GUIDE.md
3. **Verify live data** — cross-check registry counts against published figures
4. **Cite sources** — file:line for every fact
4. **Return structured findings** — no drafting, just verified facts with citations

## Outputs

- Fact sheet with source citations
- Discrepancy flags (e.g., 143 vs 144 agents)
- Policy context summary with dates

## Quality Gates

- Every claim has a file:line citation
- Live registry verified against published docs
- No invented numbers
- Distinguishes "published figure" from "live registry"

## Example Prompt

> "You are the Pharos Agentic Research Lead. Research the exact current metrics for the LinkedIn intro post: agent count, department count, governance mechanisms, use cases, policy context. Cite file:line for each."
