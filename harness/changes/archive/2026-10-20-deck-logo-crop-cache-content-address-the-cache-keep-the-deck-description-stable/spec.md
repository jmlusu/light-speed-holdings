# Spec

## Intake Review

- Intake type: Small Change
- Input shape: requirement-first (issue #485, raised by the audit of PR #480)
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: the deck generator caches its pre-cropped logo under a fixed name and re-cuts it only when the source asset is *newer* than the cache. mtime is not content identity, so a brand asset replaced by a file carrying an older timestamp (backup restore, artifact copy, a build step that sets timestamps) silently reuses the stale crop and the deck ships the wrong logo.
- Current behavior: `scripts/presentation/generate-ai-venture-studio-deck.py` compares `source_mtime > cache_mtime`; the cache file name is fixed (`ai-venture-studio-lockup-880x713.png`).
- Source of evidence: issue #485 (raised by the read-only audit of PR #480), `knowledge/technology/bug-fixes/BUG-bb0f72551.md`.

## User Scenarios And Success

- Primary user/system scenario: the brand team replaces `brand/logo/logo-full.png` and rebuilds the deck. The new logo must be in the deck, whatever timestamps the new file carries.
- Success criteria:
  - A same-size asset with different content always produces a different crop, regardless of mtime.
  - The deck artifact stays byte-identical across machines (the picture description must not carry the cache file name), so the drift guard `test_committed_deck_matches_the_generator` keeps passing.
  - The generator still refuses a brand asset whose size is not `LOGO_SRC_SIZE`.
- Acceptance criteria: `pytest tests/presentation` green, `ruff check` and `ruff format --check` clean, the verifier reports `ALL 11 CHECKS PASSED` on the committed deck, the render gate reports `ALL RENDER CHECKS PASSED`, the committed deck is unchanged, and CI is green.

## Non-Goals

- Changing the crop box, the logo placement or the deck content.
- Touching `src/` (the dashboard-side work is issue #484, a separate change).
- Changing the picture `name` attribute (only `descr` is set today).

## Constraints

- The cache file name must not leak into the deck: `descr` is compared by the drift guard, so the deck must not vary between machines.
- `main` is protected: branch, PR, required checks green before merge.
- ECL allows one active change; `haomtgv-blueprint-hero-and-page-wiring` was parked with the harness script and is resumed after this change closes.

## Assumptions

- The brand asset stays 1254x1254; a size change is still a hard failure by design.
- Hashing a ~150 KB asset on each build is free.

## Open Questions

- None.

## Resolved Clarifications

- Cache key versus artifact identity: the cache is content-addressed (SHA-256 prefix of the source), and the deck-facing picture description is set explicitly to a stable name. This keeps both properties: no stale crop, and a machine-independent artifact.
