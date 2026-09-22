# Fingerprints

Every site you build with **scroll-craft** gets one row here, appended after it
ships. The registry exists so your next build can prove it is a different page
rather than a re-skin of one you already made.

This file is **yours**. It starts empty on purpose: the gate is about not
repeating *yourself*, so it has nothing to say until you have built something.

The rules and the gate live in the skill's
`references/uniqueness.md`. Short version:

**A new build must differ from EVERY row below on at least 4 of the 6
dimensions.** Four against each row individually, not four on average across the
table. If a planned build fails, change the plan. Never edit a row to make room
for it.

The six dimensions are: **grammar**, **nav treatment**, **hero device**,
**act-sequence shape**, **close pattern**, **signature move**.

Dimension 6 is free, because a signature move is unique by definition. So the
gate really asks for three more out of the remaining five, and a build that
changes only grammar and world will fail it.

---

## The registry

| Build | Grammar | Nav treatment | Hero device | Act-sequence shape | Close pattern | Signature move | World | Port |
|---|---|---|---|---|---|---|---|---|
| lightspeed | Chaptered editorial | Folio in the margin, chapter number + title updating as the reader moves; no fixed bar | Title page: type on the navy ground, the fold still, the folio waiting | 6 acts, flow > pin > flow > scrub > flow > pin, ~9.8vh (editorial length, far under the 13.6-13.8 band) | Colophon plate: small type, the CTA as a running text line, three flags standing behind | The three flags raise themselves over a night horizon, one at a time; the page falls still when the third stands | Premium-minimal; navy/crimson/cyan palette; 16:9 night plates + 3:4 founder desk; Arial | 4500 |

---

## What is taken

Add a bullet here whenever a build claims something a later build should avoid
reusing: a grammar, a nav treatment, a close pattern, a signature move, an
act-count-and-length band. The shared columns are what the next build inherits
as a constraint, so writing them down is the whole point.

- **chaptered editorial** grammar (six numbered chapters, folio in the margin, plates with captions)
- **folio-in-the-margin nav** with no fixed top bar (chapter number + title update as the reader moves)
- **title-page hero**: type on the ground, no media above the fold
- **6-act / ~9.8vh band** ending in a short colophon `pin` close, with exactly one `scrub` at the peak
- **colophon-plate close** with the CTA set as a running text line
- **raising-flags signature**: three flags cresting a night horizon one at a time, stillness when the third stands

---

## Appending a row

After shipping, add one line to the table and one bullet to **What is taken** if
the build claimed something new. Fill every column. Say what the build shares
with existing rows.

Rows are append-only. A build that has been superseded stays in the table,
because the space it occupies is still occupied.

---

## Worked example

The skill's author kept a registry of twelve builds across eight page grammars.
If you want to see what a filled-in table looks like, and which shapes tend to
collide, read `EXAMPLES.md` in the scroll-craft repository. Treat it as
illustration only: those rows are somebody else's builds and they do **not**
constrain yours.
