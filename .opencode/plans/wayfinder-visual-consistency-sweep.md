# Wayfinder chart — Marketing-site visual consistency sweep (38?) — READY TO EXECUTE

Status: chart approved by user ("Chart as planned"). Blocked on plan-mode exit (generic edits denied in-session).

## What executing this chart does

Run on this repo (origin github.com/jmlusu/light-speed-holdings), via `gh`:

1. Create **map issue** (label `wayfinder:map`) with the body below.
2. Create **9 child tickets** (labels `wayfinder:task` / `wayfinder:prototype`) with the bodies below, each starting `Part of: <Map> (#M)`.
3. Wire blockers in a second pass (`gh issue edit` — bodies need ticket ids first): tickets 2,4,5,6,7,8,9 get `Blocked by: ...`.
4. Rebuild the map history: append the `## Tickets` listing (name (#n) — type; blocked-by).
5. Leave charting at that (charting is one session's work), then begin work in ticket order.

## Ticket order (one per session; HITL on the prototype tickets)

1. **Fix the undefined `--ls-edge`** (task, AFK)
2. **Audit gate — crawl every route** (task, AFK) — blocked by 1
3. **Lexicon — codify the second-level system** (prototype, HITL) — the central decision; unblocked
4. **How-It-Works redesign** (prototype, HITL) — blocked by 3
5. **Pricing redesign** (prototype, HITL) — blocked by 3
6. **Contact redesign** (prototype, HITL) — blocked by 3
7. **Agents redesign** (prototype, HITL) — blocked by 3
8. **Stub-family template — 10 pages, one design** (prototype, HITL) — blocked by 3
9. **Utility quartet — changelog / privacy / security / 404** (task, AFK) — blocked by 3

Frontier at chart time: tickets 1 and 3 (both unblocked, unclaimed).

## Issue bodies

### Map — title: "Wayfinder: Visual consistency sweep — every page speaks the Operating Diagram"

```markdown
## Destination

Every page of the marketing site speaks the Operating Diagram visual language — the system `website/src/pages/index.astro` established in the 2026-09 landing redesign: Bricolage Grotesque + JetBrains Mono, mono-caps micro-labels, squared containment (16px cards, 10px buttons, 6px method chips), cream/sage/pearl surfaces, contained dark control-plane panels, and one fixed second-level component vocabulary instead of ad-hoc inline classes.

"Full redesign per page": the 18 non-landing routes are rebuilt page-by-page onto that grammar, each treated with the same design rigor as the landing, while the landing stays the flagship artifact (untouched except the `--ls-edge` defect repair). Done when (a) the shared lexicon (`.ls-btn`, `.ls-label`, `.ls-chip`, `.ls-card`, `.ls-band`) is the single source of the second-level vocabulary, and (b) every route passes the audit crawl.

Spiritual continuation of map #157 (site built, landing redesigned); this map is the sweep that finishes the visual system across the remaining 18 pages.

## Notes

- **Execution carries in the map** — overrides the "decide, don't do" default: each redesign ticket, once signed off by the human, is implemented the same session. The deliverable is the shipped sweep.
- **Domain**: `website/` (Astro 4 + Tailwind, static). The landing is the authority artifact; interior pages design *against* it, never onto it.
- **Rulings already locked by the human**: depth = full redesign per page; the 10 stub pages' bodies are reskin-only (placeholder strings stay frozen); codify the shared classes first, then sweep pages onto them.
- **Skills per session**: /prototype for each redesign ticket (concrete take to react to), /grilling + /domain-modeling where ambiguity resurfaces, /ls-design-system for brand tokens, /ls-artifact-qa after each applied design.
- **Tracker**: GitHub issues via `gh`; type labels `wayfinder:<type>`; blocking by body "Blocked by: Name (#n)" (no native sub-issue/dependency ops on this repo — docs/agents/issue-tracker.md).
- **Verification per ticket**: the audit crawl passes on the built page; `npm run build` green in `website/`.

## Decisions so far

<!-- one line per closed ticket, added on resolution -->

## Not yet specified

- Whether any interior page earns a bespoke component beyond the lexicon — e.g. the pricing calculator's interactive surface — likely graduates inside the pricing ticket, not before it.
- Stub family as a shared Astro partial vs. per-file template inheritance — sharpens when the stub template itself is designed.

## Out of scope

- Writing real marketing content for the 10 stub pages (ruled reskin-only; "Mirrored IA from Foaster…" strings stay frozen).
- Redesigning the landing (`index.astro`) itself — flagship stays; only the `--ls-edge` repair touches it.
- Non-visual IA/content restructuring; dashboard work; anything From map #157 not among these 18 pages.
- Any work that isn't visual consistency.

## Tickets

<!-- populated at charting -->
```

### Ticket 1 — "Fix the undefined `--ls-edge`" — `wayfinder:task`

```markdown
## Question

Nothing to decide — a defect to repair before the audit baseline is honest.

`--ls-edge` is referenced 10 times in `website/src/pages/index.astro` (graph-card border, view-switch border, legend top-borders, SVG graph-edge strokes) but defined nowhere in `src/styles/tokens.css` — the only undefined `--ls-*` token on the site. Unresolved `var(--ls-edge)` collapses the border declarations and drops the SVG strokes to near-black, visibly degrading the flagship's org-graph artifact.

The resolution records: the token added to `tokens.css` (mapped to `--ls-card-border`), and the border/stroke rendering confirmed restored.
```

### Ticket 2 — "Audit gate — crawl every route" — `wayfinder:task`

```markdown
## Question

What precise, machine-checkable assertions define "visually consistent with the Operating Diagram" across the site — so every later ticket and the final sweep has a pass/fail gate?

Build `website/scripts/audit-visual.mjs` (Playwright crawl of every route at 375/768/1440) asserting per page:
- no unresolved `--ls-*` custom properties
- no `rounded-full` on buttons / CTAs / badges / pills / chips
- mono-caps micro-labels (`mono-cap` or `.font-mono` uppercase) where `uppercase tracking-[0.12em]` eyebrows used to be
- no horizontal overflow
- contrast spot-checks on text / secondary pairs

Run a baseline against the current site and record the pass/fail list in the resolution so later tickets can reference it.

Blocked by: Fix the undefined `--ls-edge` (#N).
```

### Ticket 3 — "Lexicon — codify the second-level system" — `wayfinder:prototype` (HITL) — THE decision

```markdown
## Question

What exactly is the second-level component vocabulary all 18 pages consume — the shared classes that make "consistent" a single source rather than 200 inline lookalikes?

Prototype the shared set in `website/src/styles/` (extend global.css or add components.css) and link the result as an asset: `.ls-btn` (ink solid / outline / text-link, radius 10px), `.ls-label` (mono-caps micro-label rule replacing every `uppercase tracking-[0.12em]` eyebrow), `.ls-chip` (square key/value chips, radius 8px), `.ls-card` (white/pearl surface, `--ls-card-border`, radius 16px), `.ls-band` (cream/sage/pearl/dark section bands), and the method number-badge treatment (6px chips, per the landing's 01–04). Also decide exact button radius/height and hover states, and how labels compose with headings. The human signs off before anything blocks on it.
```

### Ticket 4 — "How-It-Works redesign" — `wayfinder:prototype` (HITL)

```markdown
## Question

What is the how-it-works page's redesign — the 01–04 methodology flow rebuilt as Operating-Diagram artifacts (mono number chips, step cards, contained dark panel for the "run it" command, mono-caps labels), with parity to the landing's method section?

Prototype the page, link as asset, get sign-off, apply in the same session.

Blocked by: Lexicon — codify the second-level system (#N).
```

### Ticket 5 — "Pricing redesign" — `wayfinder:prototype` (HITL)

```markdown
## Question

How does the pricing page redesign — billboard cards, "Popular choice" chip, squared provider-pill toggle replacing the current pill switch, calculator surface, FAQ panels — while keeping the interactive calculator intact?

Prototype the page, link as asset, get sign-off, apply in the same session.

Blocked by: Lexicon — codify the second-level system (#N).
```

### Ticket 6 — "Contact redesign" — `wayfinder:prototype` (HITL)

```markdown
## Question

What is the contact page's redesign — fast/human path cards, form surface, Cal.com embed container, contained dark proof panel — aligned to the lexicon?

Prototype the page, link as asset, get sign-off, apply in the same session.

Blocked by: Lexicon — codify the second-level system (#N).
```

### Ticket 7 — "Agents redesign" — `wayfinder:prototype` (HITL)

```markdown
## Question

How does the agents data-directory page redesign — stat cards with mono-caps labels, by-type / by-department directory cards, registry panel parity with the landing — given it ships live data from product.json (no invented copy)?

Prototype the page, link as asset, get sign-off, apply in the same session.

Blocked by: Lexicon — codify the second-level system (#N).
```

### Ticket 8 — "Stub-family template — 10 pages, one design" — `wayfinder:prototype` (HITL)

```markdown
## Question

What is the single redesigned stub template replacing the 10 byte-identical placeholder pages — about, case-study, docs, features, platform, research, solutions, solutions/assessment, solutions/enterprise, solutions/managed-platform — as a shared hero→band + surface layout, applied via one template/partial (or per-file inheritance)?

Body strings stay frozen (reskin-only ruling), so the template must re-skin the existing "Mirrored IA from Foaster…" copy without inventing content. Structure verified identical on about + solutions/enterprise; remaining 8 spot-checked during this ticket — if any diverges structurally, this ticket splits.

Prototype the template, link as asset, get sign-off, apply across all 10 in the same session.

Blocked by: Lexicon — codify the second-level system (#N).
```

### Ticket 9 — "Utility quartet — changelog / privacy / security / 404" — `wayfinder:task`

```markdown
## Question

Apply the signed-off lexicon to the four utility pages whose decisions are all subsumed by the lexicon ticket: changelog (rounded-full CTAs → `.ls-btn`, keep live metadata block), 404 (branded contained panel inline with the system), privacy + security (mono-caps labels / lexicon buttons, prose surfaces untouched beyond that).

Pure application — no new design decisions. The audit crawl must pass on all four.

Blocked by: Lexicon — codify the second-level system (#N).
```

## Chart-time commands (execute after plan-mode exit)

```bash
# 1. map
gh issue create --title "Wayfinder: Visual consistency sweep — every page speaks the Operating Diagram" --label wayfinder:map --body-file .opencode/plans/wf-map.md
# 2. tickets (parallel), bodies minus blockers
# 3. second-pass edits adding "Blocked by:" lines
# 4. rebuild map ## Tickets listing with real numbers
```
