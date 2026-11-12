# Plan

## Technical Approach

- **competitive-landscape.md refresh**: Baseline v2 (2026-10-07) → v3 (2026-11-10); write §8 "November 2026 Delta" (first-ever §8); update per-player delta lines where verified moves exist; advance §7 monthly checklist to 2026-12-16; source URLs stamped with (accessed 2026-11-__); baseline header updated to v3; honesty tags VERIFIED / VENDOR CLAIM / UNCONFIRMED per ADR-020/033; note the missing Oct §8 gap transparently.
- **venture-studio/scoreboard-v1.md**: Add decision entry 7 mirroring entry 6 (T4 #420) for T5 #447 Nov refresh; reference new §8 and baseline v3.
- **social-media-positioning-status.md**: Gap 5 ("No competitive landscape document exists") corrected as a follow-on — but this change focuses on competitive-landscape.md only; Gap 5 correction noted in plan and scheduled separately.

## Impacted Modules And Files

- docs/marketing/competitive-landscape.md — baseline v2 → v3 refresh (header, §8, baseline text, section edits, source URLs)
- docs/venture-studio/scoreboard-v1.md — decision entry 7 added (T5 #447 Nov refresh)
- harness/changes/active/ — spec, plan, summary, tasks, review artifacts (already scaffolded)
- ECL lifecycle: complete → validate → lint-ecl.ps1 → phase transition

## Interfaces, Data, Permissions

- No new interfaces or permission changes.

## Spec Gaps Found From Planning

- None.

## Risks And Mitigations

- Honesty tag risk: every player claim tagged VERIFIED / VENDOR CLAIM / UNCONFIRMED per ADR-020/033; never fabricate dates/quotes.
- Missing Oct §8 gap: mitigated by transparent note in Nov §8 header/link area.
- Main-protected branch: merge only when 6 CI checks green.

## Verification Plan

- competitive-landscape.md: ruff + mypy + pytest pass on repo; Section 8 content validated against source URLs; honesty tags present and correct per ADR-020/033; no fabricated metrics/dates/quotes.
- §7 monthly checklist: next update 2026-12-16 confirmed.
- scoreboard-v1.md: decision entry 7 present and maps to new §8.
