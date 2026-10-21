---
name: ls-od-prototype
description: "Generate web, SaaS, mobile, and wireframe prototypes with Open Design templates, then hand them to QA. Trigger on: 'od prototype', 'web prototype', 'saas landing page od', 'mobile prototype', 'wireframe od', 'open design landing page'."
---

# Open Design Prototypes

## When To Use

- A brief calls for a landing page, SaaS marketing page, pricing or waitlist page, mobile flow, wireframe, or WebGL experience.
- The deliverable should be a running prototype rather than a static image.
- LightSpeed branding is required and the artifact will be QA'd before handoff.
- An existing site needs to be re-skinned or extended rather than rebuilt from scratch.

## Template Families

| Need | Template id |
|---|---|
| Web prototype (default) | `web-prototype` |
| Web prototype, brutalist taste | `web-prototype-taste-brutalist` |
| Web prototype, editorial taste | `web-prototype-taste-editorial` |
| Web prototype, soft taste | `web-prototype-taste-soft` |
| SaaS landing page | `saas-landing` |
| Pricing page | `pricing-page` |
| Waitlist page | `waitlist-page` |
| Mobile app | `mobile-app` |
| Mobile onboarding | `mobile-onboarding` |
| Wireframe, annotated | `wireframe-annotated` |
| Wireframe, greybox | `wireframe-greybox` |
| Wireframe, mobile flow | `wireframe-mobile-flow` |
| Wireframe, sketch | `wireframe-sketch` |
| WebGL experience | `webgl-experience` |

Taste variants are the same prototype with a different visual language — pick one, not several. For decks, documents, diagrams, or ads, use the matching `ls-*` production skill instead.

## Brief Structure

Write the brief before running, with these fields:

1. **Artifact** — template id and the single page or flow being built.
2. **Audience** — who uses it, and on what device.
3. **Objective** — the one action the page must drive.
4. **Narrative** — sections or screens in order, with the message of each.
5. **Visual language** — taste variant, imagery, motion, and what to avoid.
6. **Constraints** — real copy vs. placeholder, data sources, links, accessibility bar.

Keep the brief in a file and pass it with `--prompt-file` so the run is reproducible.

## Commands

Create the project once, attaching the skill and brand system:

```bash
od project create --name "Landing page" --skill web-prototype --design-system lightspeed
```

Run generation against that project:

```bash
od run start --project <projectId> --skill web-prototype --prompt-file ./brief.md --agent opencode --json
```

Follow the run in the foreground:

```bash
od run start --project <projectId> --skill web-prototype --prompt-file ./brief.md --follow
```

Watch a running run as an NDJSON event stream:

```bash
od run watch <runId>
```

Steer a run that has drifted, without restarting it:

```bash
od run steer <runId> --message "Keep the hero to one headline and one CTA."
```

Cancel a run that is off-brief:

```bash
od run cancel <runId>
```

Start from an existing folder instead of a blank project:

```bash
od project import-folder ./site --name "Existing site" --skill web-prototype --design-system lightspeed
od run start --project <projectId> --skill web-prototype --json
```

The daemon's `od run` surface is `start`, `redesign`, `watch`, `cancel`, and `steer`; there is no `od run <scenario>` positional form. `--design-system` is a project-creation flag, not a run flag. `od run redesign [--path <folder>]` is the shortcut for restructuring an existing folder.

## Responsive And Accessibility Bar

- One layout per breakpoint: mobile ~375, tablet ~768, desktop ~1440. No horizontal scroll at any width.
- Tap targets at least 44×44 px, with visible focus states on every interactive element.
- Contrast at least 4.5:1 for body text and 3:1 for large text; never signal state by color alone.
- Semantic landmarks (`header`, `nav`, `main`, `footer`), a single `h1`, ordered headings.
- Every image has alt text or is marked decorative; icons carry accessible names; inputs have real labels.
- Motion respects `prefers-reduced-motion`.
- Placeholder copy is labeled as placeholder, never shipped as if final.

## Handoff To QA

1. Record the project id and output path from `od project info <id>`.
2. Confirm the run ended cleanly (`od run watch <runId>` streams to completion without error).
3. Hand the artifact to `ls-artifact-qa` with the brief, project id, and output path.
4. QA returns APPROVE or FIX. On FIX, tighten the brief and re-run; do not hand-edit generated files.

## Verification

```bash
od project info <id>
od run watch <runId>
```

Then load the artifact at 375, 768, and 1440 px and check the accessibility bar above before calling it done.
