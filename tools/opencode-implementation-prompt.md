# Task: implement the deck-gate (deterministic enforcement of AGENTS.md for deck work)

You are implementing enforcement tooling in `C:\Users\jmlus\light-speed-holdings`. Follow AGENTS.md (§4 context loading, §15 evidence/honesty, §17 shell rules) for this task. Shell is **PowerShell**: no `&&`, `||`, `2>/dev/null`; chain with `;` and check `$LASTEXITCODE`.

## Why
A previous deck-building session claimed PASS without running `ls-artifact-qa`, never rendered the slides, shipped numbers with no source ($65B, $500K, $49, "ATC >90%"), and wasted ~20 calls on PowerShell syntax errors. AGENTS.md is advice; this task makes the rules mechanical.

## Inputs (read first, do not modify)
Drop folder: `tools\deck-gate-drop\` containing `verify-deck.py`, `claims.schema.json`, `claims.example.yaml`, `qa-verdict.schema.json`.
If it is missing, STOP and ask. Record the sha256 of each file before you touch anything.

## Hard rules for this task
1. **Never** set any claim to `status: verified`, edit `verified_by`/`verified_on`/`source`, or write a `qa-verdict.json` by hand. Only the owner promotes claims.
2. **Never** use `--skip-qa`, `--allow-agent-verification`, or `--allow-unknown` to get a green result. Never weaken a check to make a test pass. If you find a bug in `verify-deck.py`, fix it, add a self-test case for it, and report it.
3. Do not invent numbers, sources, tool/hook names or APIs. Where you cannot verify something, write **UNKNOWN** and say what would resolve it.
4. Work on branch `feat/deck-gate`. Minimal diffs. No deletions of existing content (move, don't delete). No push. Follow the repo's git rules in AGENTS.md.
5. Measure, don't estimate: every "done" below needs a command and its real output.
6. Ask one consolidated question only if something here conflicts with AGENTS.md or the repo; otherwise proceed.

## Phase 0: preflight
- Read AGENTS.md §4, §14, §15, §17. List existing `.opencode` plugins and CI / pre-commit config; follow their conventions.
- `git status`; note anything dirty. Find the deck generator (`generate-value-add-pitch.py`) and the existing outputs.
- Baseline: run `verify-deck.py` on the existing generated deck (expect FAIL/incomplete). Save the output to `docs/deck-gate/baseline-report.txt`.

## Phase 1: install
- `scripts\deck-gate\verify-deck.py`; schemas to `docs\schemas\`; `docs\claims.yaml` from `claims.example.yaml` unchanged in content.
- Add deps (`python-pptx`, `pyyaml`, `pillow`, `jsonschema`) via the repo's tooling (uv per AGENTS.md); do not global-install silently.
- **Done when**: `verify-deck.py --self-test` prints `SELF-TEST: PASS` (exit 0); `docs\claims.yaml` validates against `claims.schema.json` (show the command).

## Phase 2: generator reads claims, nothing hardcoded
In `generate-value-add-pitch.py`:
- Add `claim(id)` that loads `docs/claims.yaml` and returns the first `display` string only if `status == verified`; otherwise raise with the claim id and status. Replace every hardcoded number/price/market size/KPI/client claim with `claim()` or remove the element (replace with number-free wording; do not invent substitute figures; list each removal for me).
- Make every text run explicit: font Arial, size from the brand scale, colour from tokens. Set logo alt text. Keep the navy 0.15in rail on content slides.
- **Done when**: the deck builds; `verify-deck.py <deck> --root . --logo-slides 1,13` shows V03, V04, V05, V06, V07, V08, V09 as PASS and V13 as FAIL (no verdict yet). Paste the full output. If any other check is not PASS, fix the generator, not the checker.

## Phase 3: render + verdict tooling
Create `scripts\deck-gate\render-verdict.py`:
- `render <deck>`: LibreOffice headless to PDF (detect `soffice` on Windows; if absent report UNKNOWN), then one PNG per slide (>=1280px wide, e.g. PyMuPDF) into `<deck>.renders\`. Prints the paths. Writes **no** verdict.
- `verdict <deck> --reviewed-by <id> --pass visual=PASS --pass brand=PASS --pass ux=PASS --pass accessibility=PASS --pass content=PASS`: refuses unless renders exist and match the current deck build (render manifest holds the deck sha256); writes `<deck>.qa-verdict.json` valid against `qa-verdict.schema.json` with evidence hashes.
- Update the `ls-artifact-qa` skill instructions: for PPTX it must run `render`, **view every PNG**, then call `verdict` with honest results; any FAIL means verdict FIX and a list of defects.
- **Done when**: `render` yields 13 PNGs; after a real visual review `verdict` yields a file; `verify-deck.py` V13 turns PASS; modifying the deck by one byte makes V13 FAIL (show both runs).

## Phase 4: runtime hooks (OpenCode)
Read the current OpenCode plugin docs and an existing plugin in this repo before writing code. Do not guess hook names.
- **Shell guard**: block shell commands containing `&&`, `||`, `2>/dev/null` (and `cd X && ...`) and return the AGENTS.md §17 fix in the error. Alternative if cleaner: configure PowerShell 7 (`pwsh`) as the shell. Pick one, justify it.
- **Done-gate**: the agent must not be able to declare a deck finished without a matching report. Preferred: a custom tool `deck_gate_done(deck)` that runs `verify-deck.py` and returns VERIFIED/REJECTED/INCOMPLETE, plus a session-idle/stop check that re-prompts when the final message contains PASS/APPROVE/"production-ready" but `<deck>.verify.json` is missing, has a different sha256, or `exit_code != 0`. If the plugin API cannot support this, say so (UNKNOWN) and implement the strongest alternative you can prove works (pre-commit/CI check on `.pptx` changes).
- **Done when**: transcript of (a) a blocked `git status && git log`, (b) a false "APPROVE" being rejected, (c) a true VERIFIED being allowed.

## Phase 5: AGENTS.md
- Put a **Non-negotiables** block in the first 40 lines: evidence rule, UNKNOWN rule, "no number without `docs/claims.yaml`", done-contract (`<deck>.verify.json` exit 0 + `<deck>.qa-verdict.json` APPROVE for this sha256), PowerShell rules, "re-run verification after any restart or model switch before reporting".
- Move long sections (§11-§13, §16, §17 tables) to `docs/agents/*.md` with links. Show before/after line counts and prove nothing was lost (diff).
- Fix factual errors: check whether `company-registry.yaml` contains ATC / velocity / capital-efficiency KPIs (grep it). If not, remove the claim that it does and point to `docs/claims.yaml`. Do not touch brand rules.
- Add a mandatory final-report template: Requested / Attempted / Happened / Verified / Unknown, each Verified row with a command and exit code or file path.

## Phase 6: session auditor
Create `scripts\deck-gate\audit-session.py` taking an exported OpenCode session JSON (top-level `info`, `messages[]` with `content[]` blocks of `type: tool`, `name`, `state.input/status/content`) and emitting JSON + a short table: AGENTS.md-mandated reads present; skills invoked; shell parse/syntax errors; final-message PASS/APPROVE claims with no supporting tool call; `verify.json` present and hash-matched; QA verdict present. Test on `<PATH-TO-EXPORTED-SESSION-JSON>` if provided, else on a small synthetic fixture you create (say which). Report actual numbers; do not assume.

## Phase 7: wire into CI / pre-commit
Run `verify-deck.py --self-test` in the repo's existing CI/pre-commit. Add a check: any changed `.pptx` under `static\brand\templates` must have a `.verify.json` with the same sha256 and `exit_code` 0. Prove it by committing a modified deck on a scratch branch and showing the check fail, then discard the scratch branch.

## Final report (use this exact shape)
| Requested | Attempted | Happened | Verified (command -> result) | Unknown |
Then: list of every file created/changed, every hardcoded figure removed from the generator, every decision you made that I should review, and the exact commands to re-run all acceptance checks. If any phase is incomplete, say which and why; do not call the work done.
