# Review

## Intake Review

- Status: approved
- Notes: the directive specified artifact types, exact pixel sizes, palette constraints and the two gates by name. Nothing high-impact was ambiguous, so no clarifying round was run. One implementation choice (render engine) was genuinely open and is recorded as a resolved clarification in `spec.md` rather than raised as a question.

## Spec Review

- Status: approved
- Open high-impact clarifications: none. The `[NEEDS CLARIFICATION]` placeholder was removed after the render-engine choice was settled.
- WHAT/HOW separation: the directive is WHAT (seven assets, fixed dimensions, both gates). `spec.md` keeps to WHAT plus acceptance criteria; the renderer choice, the `scope_of()` design and the `STATUS:` contract live in `plan.md`.

## Plan Review

- Status: approved
- Spec gaps found from planning: two, both recorded in `plan.md` and resolved rather than deferred — (a) the platform matrix requires a Facebook 1200×628 infographic and six carousel source pages that the directive did not name, so they are emitted too; (b) the carousel PDF aspect was unspecified and is resolved as a single 1080×1080 document that works as a LinkedIn post alongside the Instagram PNGs.
- Testability: every acceptance criterion maps to a named gate in `generate_all_assets.py`, and the gate outputs are recorded in `qa/assets/assets-manifest.json`, so a later reviewer can re-check the claim without re-reading the script.

## Code Review

- Status: approved
- Grounding: no generated sentence is invented. Where layout needed filler it is verbatim source text (ghost numerals from the source's own counts, pull quotes lifted from the dossier). The one place invented copy had crept in — "decision gate at day 90" — was found in review and replaced with the dossier's actual phrasing.
- Honesty of the palette claim: the video gate measures source frames because a lossy decode is not evidence of what was rendered. The decoded number is kept but labelled informational, so the manifest cannot be read as claiming an asset is off-brand when it is not.
- Known sharp edge accepted: a member of the 420 line count is layout, not logic, and the file is large for one module. Splitting it was considered and rejected — the asset layouts share one fact set and one palette helper, and splitting would have meant threading that state through five modules for no testability gain. mypy does not cover `scripts/`.

## Validation Review

- Status: approved
- Evidence: `qa/assets/assets-manifest.json` (all 11 gates with values) and `qa/generate-run.log` (full run output, twice). Dimensions verified independently with `ffprobe`, not only from the script's own report.
- Negative control: the palette gate was confirmed capable of failing — a decoded video frame measures ~98.6% off-palette at the same 3% tolerance, which is exactly the failure mode the source-frame decision exists to avoid, and it demonstrates the gate is not a no-op.
- Not verified, and not claimed: the Open Design render path, audio, and any visual QA by a human reviewer. `ls-artifact-qa` ran as the in-script gate suite; no independent human sign-off on the visual design has been recorded.
