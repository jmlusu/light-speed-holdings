---
name: ls-document-design
description: "The LightSpeed whitepaper / report / proposal factory. Produces whitepapers, strategy and research reports, policy papers, proposals, investment memoranda, executive reports, case studies, annual reports, and concept notes. Pipeline: research -> executive narrative -> document architecture -> typography -> charts/tables -> callouts -> render (Markdown->HTML->PDF via Playwright, or DOCX via python-docx through the k-dense-docx skill) -> ls-artifact-qa. Enforces the LightSpeed brand on cover, palette, type scale, and layout. Trigger on: 'write a whitepaper', 'report', 'proposal', 'policy paper', 'executive report', 'investment memo', 'concept note', '/create-whitepaper'."
---

# LightSpeed Document Design

The whitepaper / report / proposal factory. Turns research and narrative into professional, on-brand documents.

## Preconditions

1. Load `ls-design-system` — cover, palette, type scale, logo rules.
2. **Facts must exist before design.** Long-form documents never invent numbers. Source facts from:
   - `company/` registry, `results/`, `docs/`, `knowledge/`, `harness/evolution/`
   - `research` skill / `k-dense-literature-review` / `k-dense-research-lookup` for evidence
   - The `ls-creative-director` brief's supplied facts
   If research is missing, stop and run research first — do not fabricate.
3. Pick the document type to set structure and depth.

## Document Types & Structure

| Type | Suggested arc |
|------|---------------|
| Whitepaper / policy paper | Executive summary → Context/Problem → Framework → Evidence → Policy ask → Appendix |
| Strategy report | Mandate → Where we are → Options → Recommendation → Roadmap → Risks |
| Investment memorandum | Summary → Company → Market → Product → Financials → Use of funds → Risk |
| Proposal / concept note | Objective → Approach → Deliverables → Timeline → Budget → Team |
| Case study | Client → Problem → Solution → Results (with numbers) → Implications |
| Annual / executive report | Letter → Highlights → Operations → Financials → Outlook |

Length guidance: whitepaper 8–20 pages; report 4–12; concept note 3–6; one-pager 1.

## The LightSpeed Document Anatomy

- **Cover:**
  - Navy `#070A40` full-bleed background; official full logo (transparent variant on navy); document title in white display, 32–36pt; subtitle in cyan 16–18pt; red accent divider; date + confidentiality class.
  - If exporting PDF via HTML/CSS, the cover is a full-page (`page-break-after: always`).
- **Body:**
  - White background, navy headings (Arial 700), body text Arial 400 11–12pt, line-height 1.5–1.6.
  - Headings: H1 24pt / H2 18pt / H3 14pt, all navy-bold.
  - Callouts: light-grey `#F2F2F2` rounded boxes; key-stat callouts may use a red left border accent.
  - Tables: navy header row, light-grey alternating rows, dark-grey captions.
  - Charts: `ls-diagramming` output embedded, brand palette only.
- **Footers:** page numbers navy; `™` on first company mention; tagline optional on closing page.

## Render Paths

**Path A — Markdown → HTML → PDF (recommended):**
1. Author in Markdown with a title-page block, headings, tables, callouts.
2. Wrap in an HTML print stylesheet using `brand/tokens/brand-tokens.css` (+ cover, footer, page rules: `@page { size: A4; margin: 20mm }`, `-webkit-print-color-adjust: exact`).
3. Render to PDF with Playwright's `page.pdf()` (Chromium is available) — no extra installs needed:
   `npx playwright` / a small Node script using `playwright`.
   This is the zero-dependency PDF route for the repo (WeasyPrint/reportlab are NOT installed — do not assume them).

**Path B — DOCX (Word deliverables):**
- Use the `k-dense-docx` skill (python-docx): cover with logo, heading styles mapped to the brand type scale, navy table headers.

**Path C — Hybrid submission package:**
- PDF for review + DOCX for client edits + the source Markdown committed to `proposal-deliverables/` or a working folder.

## Quality Gates

- [ ] Cover matches the LightSpeed anatomy (navy, logo, red divider, cyan subtitle)
- [ ] All facts trace to source (research output, registry, brief) — zero invented numbers
- [ ] Executive summary first; recommendation/ask explicit
- [ ] Brand palette + type scale throughout
- [ ] Tables/charts legible in print (navy headers, no clipped columns)
- [ ] Callouts used for emphasis, not decoration
- [ ] PDF renders without overflow/cutoff; page count matches intent
- [ ] `™` on first mention; tagline correct if used

Deliver the rendered file(s), a citation trail for every fact, and QA verdict.
