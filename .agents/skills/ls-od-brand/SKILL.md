---
name: ls-od-brand
description: Use when applying LightSpeed Holdings brand tokens, typography, logo, or design-system handoff rules to an Open Design project, or when auditing an Open Design artifact for brand compliance. Trigger on: 'open design brand', 'OD brand system', 'brand tokens in Open Design', 'design system handoff', 'brand QA'.
---

# Open Design Brand

Open Design resolves the LightSpeed design system from `open-design/design-systems/lightspeed/` (committed on `lightspeed/format-pass`). Treat the canonical brand files as the source of truth and attach the design system at project creation, not at run time.

## When To Use

- An Open Design project must use LightSpeed colors, Arial typography, or the lighthouse/shield logo.
- You need to choose tokens for a page, deck, dashboard, or document.
- You must attach the LightSpeed design system to a project before the first run.
- You are reviewing an Open Design artifact for brand compliance.

## Brand Tokens

| Token | Value | Name | Usage |
|---|---|---|---|
| `navy` | `#070A40` | Navy Primary | Headlines, logo text, primary brand surfaces |
| `red` | `#E63946` | Red Accent | Signal waves, accent elements, key highlights, CTAs |
| `cyan` | `#00BFFF` | Cyan Accent | Shield base, accent elements, links on dark |
| `morning-mist` | `#F7F8F9` | Morning Mist | Light surfaces, backgrounds, subtle dividers |
| `deep-mineral` | `#121518` | Deep Mineral | Primary dark text, pronounced contrast |
| `grey-light` | `#F2F2F2` | Light Grey | Backgrounds, cards, callouts |
| `white` | `#FFFFFF` | White | Clean backgrounds, text on navy |
| `grey-dark` | `#6B7280` | Dark Grey | Secondary text, captions, muted labels |
| `grey-light-text` | `#9CA3AF` | Light Text Grey | Tertiary text on dark surfaces |
| `onNavy` | `#FFFFFF` | — | Text on navy surfaces |
| `onRed` | `#FFFFFF` | — | Text on red accent surfaces |
| `onCyan` | `#070A40` | — | Text on cyan accent surfaces |

Company name: `LightSpeed Holdings Limited`. Legal name: `LIGHTSPEED HOLDINGS LIMITED`. Tagline: `ASPIRE. ACT. ACHIEVE.` Trademark: `LightSpeed Holdings Limited™`.

## Typography And Spacing

| Style | Family | Weight | Usage |
|---|---|---|---|
| Display | Arial | 700 | Hero headlines, cover titles, section banners |
| Heading | Arial | 700 | Section titles, slide titles |
| Body | Arial | 400 | Paragraph text, slide body |
| Caption | Arial | 400 | Captions, footnotes, disclaimers |

| Size Token | Value |
|---|---|
| `displayXl` | 36pt |
| `titleXl` | 32pt |
| `titleLg` | 28pt |
| `titleMd` | 24pt |
| `titleSm` | 18pt |
| `subtitle` | 16pt |
| `bodyLg` | 16pt |
| `body` | 14pt |
| `bodySm` | 13pt |
| `caption` | 12pt |

- Spacing scale: `4, 8, 12, 16, 24, 32, 48, 64, 96`; base unit `4`.
- Grid: 12 columns, `24px` gutter, `48px` margin.
- Radius: `4px` small, `8px` medium, `16px` large.
- Slide canvas: `10in × 7.5in`, navy rail `0.15in`.
- Web page: max width `1200px`, navy rail `4px`.

## Logo Rules

- Symbol: lighthouse/shield emblem with signal waves.
- Clear space: `1x` height of the "L" in "LIGHTSPEED" on all sides.
- Minimum full-logo width: `30mm` print, `120px` screen.
- Minimum icon-only width: `12mm` print, `32px` screen.
- Never redraw, recolor, stretch, or crop the logo. Use the supplied asset files.
- Do not use the CEO Dashboard's internal J.A.R.V.I.S. theme or "LS" placeholder as public brand.

## Design System Handoff

- The `lightspeed` design system ships at `open-design/design-systems/lightspeed/DESIGN.md`. Confirm it with `od design-systems list` before attaching it.
- Canonical brand files: `brand/tokens/brand-tokens.json` and `brand/CANONICAL_SOURCES.md`. `brand/**` is canonical; never hand-edit `static/brand/**` or `public/brand/**` mirrors. Sync mirrors with `pwsh scripts/build/sync-brand.ps1`.
- Attach the design system when the project is created, then start the run:

```bash
od design-systems list
od design-systems show <id>
od project create --name "<name>" --design-system lightspeed
od run start --project <projectId> --skill <skillId> --message "..."
```

- `--design-system` is a project-creation and import flag, not a run flag. `od run start` and `od run redesign` reject it. `od design-systems import-local <path>` is the verified local import path for a design system that is not committed to this repo.
- If the design system must be extracted from a live site, use only the documented brand flow after confirming the command with `od brand --help`; `extract-from-html` is not a verified command.

## Brand Commands

```bash
od brand list --json
od brand extract <url> --json
od brand create <url> --prompt-file <path> --locale <locale> --json
od brand continue <id>
od brand preview <id> --project <projectId>
od brand finalize <id> --project <projectId>
```

- These commands manage brand extraction/previews. They do not install the LightSpeed design system; the repo ships it under `open-design/design-systems/lightspeed/`.
- Use `od design-systems list` to find the id actually available to a project.

## Brand QA

- Colors match the token table exactly; no approximations or invented shades.
- Typography uses Arial at the specified weights and sizes.
- Logo has correct clear space, minimum size, and unmodified artwork.
- Text contrast is legible; navy, red, cyan, and light surfaces use their paired `on*` colors.
- Spacing follows the 4px grid and 12-column layout.
- No public artifact uses the internal dashboard theme or placeholder "LS" mark.
- Escalate the final artifact to `ls-artifact-qa`; this skill defines brand rules, not final approval.

## Verification

```bash
Test-Path brand/tokens/brand-tokens.json
od design-systems list --json
od design-systems show <id>
od project create --name "<name>" --design-system lightspeed
od run start --project <projectId> --skill <skillId> --message "..."
```
