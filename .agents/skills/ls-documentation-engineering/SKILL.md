---
name: ls-documentation-engineering
description: "Information architecture for LightSpeed docs, not visual design. Builds READMEs, API documentation, developer portals, knowledge bases, architecture documentation, tutorials, how-to guides, reference documentation, release notes, changelogs, and FAQs. First classifies content (tutorial / how-to / explanation / reference per the Diátaxis model), then structures it with the right IA; targets Markdown + optional Docusaurus. Wraps the existing documentation-and-adrs skill for decision records. Trigger on: 'write docs', 'documentation', 'README', 'API docs', 'knowledge base', 'developer portal', 'tutorial', 'how-to guide', 'release notes', 'changelog', 'FAQ'."
---

# LightSpeed Documentation Engineering

Documentation is an information-architecture discipline. You classify the content first, then structure the right docs for the right job.

## Preconditions

1. Clarify the audience and the gap the docs close (user onboarding? developer API? internal ops?).
2. Wrap architectural/decision docs through `documentation-and-adrs` for ADRs — this skill handles user/developer-facing structure, not decision records.

## Content Classification (Diátaxis — do this FIRST)

Every doc request maps to one of four needs:

| Type | Answers | Structure | Example |
|------|---------|-----------|---------|
| **Tutorial** | "Teach me, step by step" | lessons, prerequisites, ordered steps, outcomes | "Build your first agent org" |
| **How-to** | "How do I do task X" | goal-first, numbered steps, no conceptual padding | "Rotate dashboard keys" |
| **Explanation** | "Why is it this way" | ideas, trade-offs, context, no numbered steps | "How the message bus works" |
| **Reference** | "What is/where is the exact spec" | exhaustive, stable, terse — tables/code | "CLI command reference" |

If a request mixes types (common), split it into separate docs or section silos — never one blob that tries to be all four.

## Information Architecture

- **Naming:** slug the doc by what it does, not the team that wrote it (`authentication.md`, not `security-team/auth-final-v2.md`).
- **Structure skeleton:** one H1 → few H2 → scannable H3. Headings carry the outline; readers should get the whole story from the H2 list.
- **Code/commands:** use the repo's actual commands (`uv run`, `ai-company`, `astro dev --background`). Never invent flags.
- **Changelogs/release notes:** keep-a-changelog style (Added/Changed/Deprecated/Removed/Fixed/Security).
- **FAQs:** write from real questions (support tickets, issues), 3–8 entries, each with a one-line answer + expansion.

## Formats

- **Markdown-first:** author/commit in the repo (docs/ continues to be the home). This matches the repo's existing `docs/` practice.
- **Developer portal (optional):** Docusaurus project under the repo root or adjacent workspace; content is sourced from the Markdown, so authors keep writing in Markdown.
- **API reference:** derive from the actual CLI/endpoints (`ai-company --help`, dashboard API routes) — keep it mechanically consistent with shipped code.

## Repo Doc Conventions (LightSpeed)

- `AGENTS.md` line is the pointer → module/subproject `AGENTS.md` files are the per-area entry points (already in use: `website/AGENTS.md`, `website/AGENTS.md`).
- ADRs → `docs/adr/` through `documentation-and-adrs`.
- Architecture docs → `docs/ARCHITECTURE.md`; change lifecycle → `docs/ECL.md`.
- Match existing tone: direct, factual, minimal fluff, code-adjacent.

## QA Gates

- [ ] Content type classified (tutorial/how-to/explanation/reference)
- [ ] One job per doc; mixed-type requests split
- [ ] Headings are the outline — scannable on their own
- [ ] Every command/flag verified against the codebase (no invented flags)
- [ ] Navigation/path to the doc exists from the nearest AGENTS.md or index
- [ ] ADRs routed to `documentation-and-adrs`
- [ ] No dead links in inter-doc references
