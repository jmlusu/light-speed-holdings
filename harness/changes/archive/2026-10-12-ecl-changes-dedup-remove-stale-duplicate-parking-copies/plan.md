# Plan

## Technical Approach

1. Create this ECL change via `harness-change.ps1 new` on a worktree branched from `origin/main`.
2. `git rm -r` the seven proven-stale parking directories (six indexed + `.gitkeep`-only `ls-mem-phase-2`).
3. `git rm -r` the bare `parts-2-5` stub, then `git mv` the content-bearing `parts-2-5-2` to the canonical bare name.
4. Add a one-line epilogue to `knowledge/technology/bug-fixes/BUG-81c94142a.md` noting the referenced parking dirs were removed by this change.
5. Regenerate INDEX.json via `harness-change.ps1 reindex` (PS 5.1).
6. Validate: `lint-ecl.ps1`, `check-index-freshness.ps1`, `validate-drift.ps1`, full non-e2e pytest with isolated basetemp.
7. Close completed (STATUS handoff per ECL section 7), squash-merge via PR.

## Evidence (Deletion Ledger)

| Directory (parking/) | Ruling |
|---|---|
| `2026-09-22-narrative-and-positioning-track-...` | Superseded intake skeleton (session eb279a8a); spec has NEEDS CLARIFICATION placeholders; same track completed in archive `2026-09-23-narrative-...`. User-approved delete. |
| `2026-09-23-narrative-and-positioning-track-...` | Self-documented stale duplicate ("Stale duplicate of archived narrative track") in its own Transition Note. |
| `2026-09-24-lightspeed-...-v2-0` | Archive superset (left-only 0). |
| `2026-09-24-lightspeed-...-v2-0-2` | Its only "unique" file `backfill_governance_fields.py` is byte-identical (SHA-256 6425ABD2...) to the archive copy under `2026-09-24-v2-implementation-p2-public-registry-transform/`. |
| `2026-09-25-lightspeed-...-v2-0` | Same session as archived 09-24 change; strictly earlier snapshot (reviews pending vs approved; no unique files). User-approved delete. |
| `2026-09-24-ls-mem-phase-2-architecture` | Contains only `.gitkeep`; not indexed. STATUS.md references the archive path, unaffected. |
| `2026-10-03-customer-journey-...` | Archive copy newer/final (updated 10-04 vs 10-03; only summary.md differs, archive is completed/pass). |
| `2026-09-24-ai-venture-studio-execution-plan-parts-2-5` (bare) | Template stub superseded by content-bearing `-2` copy; remove stub, rename `-2` onto canonical name. |

## Impacted Modules And Files

- `harness/changes/parking/` — 8 directory operations (7 deletes + 1 rename).
- `harness/changes/INDEX.json` — regenerated (59 -> 52 entries; 7 indexed parking dups removed, 6 remain; archive 46 unchanged).
- `knowledge/technology/bug-fixes/BUG-81c94142a.md` — epilogue note (L17-18/L30 refs become historical).

## Interfaces, Data, Permissions

- No API/code interface changes. INDEX.json remains script-generated only (never hand-edited).
- No secrets, no permission model impact.

## Spec Gaps Found From Planning

- None.

## Risks And Mitigations

- Broken references to deleted paths: grepped repo-wide; only BUG-81c94142a.md references the deleted v2-0 parking dirs (historical record — epilogue added, not rewritten).
- ECL lifecycle tests sensitive to harness state: run full suite; compare failures against main baseline.

## Verification Plan

- `powershell scripts\maintenance\lint-ecl.ps1` -> PASS
- `powershell scripts\maintenance\check-index-freshness.ps1` -> PASS (guard self-checks PS 5.1)
- `powershell scripts\maintenance\validate-drift.ps1` -> PASS
- `uv run pytest --ignore=tests/e2e -q --basetemp=<unique>` with `git status` snapshot before/after (ECL section 4)
- Post-state audit: INDEX has 51 entries, zero duplicate ids, zero duplicate slugs.
