# Coding Standards

**Audience: reviewer agents during review — not an implementation checklist.**
This file holds only judgement calls that no linter can decide. Mechanical rules live in
[`.pre-commit-config.yaml`](.pre-commit-config.yaml) (ruff lint+format, mypy, bandit,
trailing-whitespace, end-of-file-fixer, check-yaml) and run on every commit; the Vite/React app
is checked with `npm run lint` (`tsc --noEmit`).

## Standards

1. **Change locality.** Keep a feature's code in its own file; prefer a new component over
   growing a shared one sideways. The `FloatingNav.tsx` accretion (AGENTS.md §16/§17) is the
   cautionary case: overlay logic piled into one nav component until conflict resolution put
   JSX outside the `return` and broke the build.
2. **One source of truth for repeated content.** Reference a canonical table or section; never
   copy it. The duplicated Verification table (AGENTS.md §6 vs §10, exact copies until
   2026-10-12) is the worked example — one lives, one points.
3. **Match the surrounding file.** Follow the style of the file being edited (hooks patterns,
   component conventions, naming) rather than imposing a house style mid-file; no drive-by
   reformatting of untouched lines.
4. **Comments are one-liners by default.** State *why*, not *what*; longer reasoning belongs in
   a doc or a linked issue.

## Cross-references

- Verification minimums per change type: AGENTS.md §6
- Tooling and shell pitfalls (PowerShell 5.1, `gh --jq` quoting): AGENTS.md §17
- Guardrail hooks and what they block: `.pre-commit-config.yaml`
