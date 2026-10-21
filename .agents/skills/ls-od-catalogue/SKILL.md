---
name: ls-od-catalogue
description: Use when choosing an Open Design template or functional skill for a new project, mapping a request to a verified template id, or explaining how the template and skill catalogues differ. Trigger on: 'open design template', 'which OD template', 'od skill', 'design template id', 'start from template'.
---

# Open Design Catalogue

Open Design ships two separate catalogues. Pick the right one before naming an id.

## When To Use

- A request should start from an Open Design template ("landing page", "deck", "dashboard", "prototype").
- You need a functional skill (`design-brief`, `design-review`, `brand-extract`) rather than a rendering template.
- You must decide whether a scenario is prototype, deck, document, image, or video work.
- You need the exact CLI or API surface for listing, inspecting, or starting from a catalogue entry.

## Two Catalogues

| Catalogue | Location | API | What It Gives You |
|---|---|---|---|
| Functional skills | `open-design/skills/` | `/api/skills`, `/api/skills/:id` | Instructions only: design briefs, reviews, brand extraction, copywriting. |
| Design templates | `open-design/design-templates/` | `/api/design-templates`, `/api/design-templates/:id` | A `SKILL.md` plus `assets/`, `references/`, optional preview entry. |

- A project's `skillId` may point at either root. Slugs are kept unique across both catalogues.
- `validateProjectSkillId` resolves through `listAllSkillLikeEntries`, which combines functional skills and design templates. Passing a template id to `--skill` is valid.
- `GET /api/skills` lists functional skills only. `GET /api/design-templates` lists templates.
- Templates declare `od:` frontmatter: `mode`, `platform`, `scenario`, optional `preview`, and `design_system` requirements. Example `web-prototype`: `mode: prototype`, `platform: desktop`, `scenario: design`, `preview: {type: html, entry: index.html}`, `design_system.requires: true` with sections `[color, typography, layout, components]`.

## Decision Tree

1. **Landing page or marketing site** → `saas-landing`, `pricing-page`, `waitlist-page`, `kami-landing`, `gamified-app`, or `web-prototype` for an open-ended page.
2. **App prototype or product UI** → `web-prototype`, `mobile-app`, `mobile-onboarding`, `wireframe-annotated`, `wireframe-greybox`, `wireframe-mobile-flow`, `wireframe-sketch`, or an `orbit-*` shell (`orbit-general`, `orbit-github`, `orbit-gmail`, `orbit-linear`, `orbit-notion`).
3. **Dashboard** → `dashboard`, `live-dashboard`, `github-dashboard`, `social-media-dashboard`, `kanban-board`, `trading-analysis-dashboard-template`, `flowai-live-dashboard-template`, or `worker-visualizer` for agent activity.
4. **Deck** → `html-ppt`, a style variant such as `html-ppt-pitch-deck`, `guizang-ppt`, `kami-deck`, `ib-pitch-book`, `simple-deck`, or `replit-deck`.
5. **Document or report** → `finance-report`, `invoice`, `meeting-notes`, `email-marketing`, `clinical-case-report`, `dcf-valuation`, `eng-runbook`, `docs-page`, or `blog-post` for an article; pair with the functional skill `article-magazine` when a magazine treatment is wanted.
6. **Image or static visual** → `image-poster`, `magazine-poster`, `social-carousel`, `contact-widget`, or `critique` when the goal is a review artifact rather than a page.
7. **Video or motion** → `video-shortform`, `hyperframes`, `motion-frames`, or `sprite-animation`.
8. **No template fits** → use `web-prototype` and load the relevant functional skill (`design-brief`, `frontend-design`, `copywriting`) with `--skill`.

## Template Selection

| Need | Verified Ids |
|---|---|
| SaaS landing | `saas-landing`, `kami-landing`, `dating-web` |
| Conversion page | `pricing-page`, `waitlist-page` |
| Desktop product UI | `web-prototype`, `web-prototype-taste-*`, `orbit-general` |
| Mobile flow | `mobile-app`, `mobile-onboarding` |
| Early wireframe | `wireframe-annotated`, `wireframe-greybox`, `wireframe-mobile-flow`, `wireframe-sketch` |
| Analytics | `dashboard`, `live-dashboard`, `trading-analysis-dashboard-template` |
| Social analytics | `social-media-dashboard`, `github-dashboard` |
| Board or investor deck | `html-ppt`, `html-ppt-pitch-deck`, `ib-pitch-book`, `kami-deck` |
| Written report | `finance-report`, `eng-runbook`, `clinical-case-report`, `dcf-valuation` |
| Marketing collateral | `email-marketing`, `social-carousel`, `image-poster` |
| Motion | `video-shortform`, `motion-frames`, `sprite-animation` |

A template may require a design system (`design_system.requires: true`). Attach one to the project at creation with `--design-system`, or expect the template's default styling; `od run start` does not accept it.

## Commands

```bash
od skill list --json
od skill show design-brief
od run start --project <projectId> --skill web-prototype --message "..."
od run start --project <projectId> --skill design-brief,web-prototype --message "..."
```

- `od skill list` reads `/api/skills` (functional skills only). `--json` is supported by the CLI parser and prints the raw payload.
- `od skill show <id>` resolves `/api/skills/:id`, so it only works for functional skills; a template id returns 404. Inspect a template through `/api/design-templates/:id` or `Test-Path`.
- `--skill` takes a comma-separated list. One id becomes `body.skillId`; several become `body.skillId` (first) plus `body.skillIds` (all).
- There is no `od design-templates` subcommand. Browse templates in the new-project "Start from" rails or call `/api/design-templates` directly.
- `od templates` lists project snapshots, not the design-template catalogue. Do not use it for discovery.

## Rules

- Name only ids that exist in the repository or were returned by `/api/skills`/`od skill show` (functional skills) or `/api/design-templates` (templates).
- Do not treat functional skills and design templates as interchangeable catalogues even though both resolve through `skillId`.
- Do not claim `od skill list` shows templates; it does not.
- Do not invent `wireframe-mobile`, `wireframe-web`, `orbit-landing`, or `orbit-app`; the verified wireframes are `wireframe-annotated`, `wireframe-greybox`, `wireframe-mobile-flow`, `wireframe-sketch`.
- Pair a functional skill with a template when the task needs both narrative guidance and a rendering scaffold.

## Verification

```bash
od skill list --json
od skill show <skillId>
Test-Path open-design/design-templates/<templateId>/SKILL.md
Test-Path open-design/skills/<skillId>/SKILL.md
```
