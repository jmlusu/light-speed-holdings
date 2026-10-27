# Deck Gate Known Gaps

## V06 — Clear-space heuristic

- **Status**: RESOLVED
- The clear-space heuristic (V06) now passes when the embedded image bytes match an official asset file in `--logo-dir` **and** the filename contains "transparent".
- Both conditions are now met with `logo-dark-bg-transparent.png`.
- Note: The heuristic is approximate against the full 1254px canvas; it is not a replacement for visual QA.

## V13 — QA verdict

- **Status**: OPEN
- No `ls-artifact-qa` verdict at `static/brand/templates/value-add-pitch-investors-clients.qa-verdict.json`; requires rendered slides + human review.
- The verdict file must be written by the `ls-artifact-qa` skill after rendering the deck images and completing visual review.
- Until a verdict is bound to this deck's sha256, V13 will FAIL the gate.
