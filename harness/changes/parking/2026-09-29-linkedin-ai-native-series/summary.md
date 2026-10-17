---
title: "LinkedIn AI-Native Series"
slug: "linkedin-ai-native-series"
status: "parked"
location: "parking"
phase: "implement"
intake_status: "done"
spec_review: "approved"
plan_review: "approved"
modules:
  - "src/ai_company/orchestrator/routine.py"
  - "src/ai_company/publishing/queue.py"
  - "src/ai_company/publishing/formats.py"
  - "src/ai_company/publishing/publishers.py"
  - "src/ai_company/media/transcription.py"
  - "src/ai_company/mcp/server.py"
  - "templates/pharos/routines/linkedin-series-reminder.md"
  - "config/company/scheduler.yaml"
files:
  - "config/company/routines.yaml"
  - "templates/pharos/routines/linkedin-series-reminder.md"
  - "src/ai_company/cli/publishing.py"
  - "src/ai_company/cli/media.py"
  - "src/ai_company/cli/mcp.py"
  - "src/ai_company/cli/main.py"
  - "pyproject.toml"
  - "uv.lock"
  - "docs/STATUS.md"
  - "tests/unit/test_routine.py"
  - "tests/unit/test_publishing.py"
  - "tests/unit/test_transcription.py"
  - "tests/unit/test_mcp_server.py"
  - "docs/Pharos/linkedin-series/post-01/draft-v1.md"
  - "docs/Pharos/linkedin-series/post-02/draft-v1.md"
  - "docs/Pharos/linkedin-series/post-03/draft-v1.md"
  - "docs/Pharos/linkedin-series/post-01/feed-v1.md"
  - "docs/Pharos/linkedin-series/post-02/feed-v1.md"
  - "docs/Pharos/linkedin-series/post-03/feed-v1.md"
  - "docs/Pharos/linkedin-series/CEO-review-batch-1.md"
  - "static/brand/templates/generate-linkedin-series-visuals.py"
  - "docs/Pharos/linkedin-series/post-01/visuals/"
  - "docs/Pharos/linkedin-series/post-02/visuals/"
  - "docs/Pharos/linkedin-series/post-03/visuals/"
  - "docs/Pharos/linkedin-series/post-01/qa-report.md"
  - "docs/Pharos/linkedin-series/post-02/qa-report.md"
  - "docs/Pharos/linkedin-series/post-03/qa-report.md"
tags:
  - "pharos"
  - "linkedin-series"
  - "content-intelligence"
  - "publishing"
  - "reminder"
validation_status: "pass"
created_at: "2026-09-28"
updated_at: "2026-09-29"
session_id: "63edc9f0-acb4-4e5e-890e-797314ac4020"
owner_agent: "jmlus"
claimed_at: "2026-09-28"
---

# Summary

## Outcome

Drafts v1 for Posts 1–3 rewritten to full LinkedIn long-form spec and **approved by CEO (2026-09-28, `CEO-review-batch-1.md`)**. Step 6 visual production complete: 12 PNGs (hero + 3 carousel cards per post, 1200×627) generated token-driven by `static/brand/templates/generate-linkedin-series-visuals.py`, all pass the mandatory `ls-artifact-qa` gate (see per-post `qa-report.md`). Step 7 scheduling complete: `results/pharos/publish_queue.json` rebuilt with 3 correct `queued` records carrying feed bodies under the 3,000-char cap (CEO format decision) — Post 1 → 2026-10-05 07:00 CAT, Post 2 → 10-07, Post 3 → 10-09 (dates carried in record `notes`; the queue has no `scheduled_at` field, cadence is enforced by the `linkedin_series_reminder` routine, cron `0 7 */2 * *` Africa/Blantyre).

## Decisions

- Research evidence matrices completed and verified per existing files.
- Drafts v1 produced for Posts 1–3 in "builder-writer-advocate" voice, no emojis, `™` on first company mention, claims traceable to registry/results/Pharos artifacts.
- Framework layer (H-A-O-M-T-G-V) explicitly named in each draft (H, A, O respectively).
- Malawi/SADC context present in each draft (sovereign data, low-bandwidth, 90-day pilot).
- CTA aligned: Build / Evidence / Shape in all three drafts.
- Visual production: `ls-visual-storytelling` leads hero visual, `k-dense-infographics` produces carousel cards; both feed mandatory `ls-artifact-qa` gate.
- CEO review batch: Posts 1–3 together, 48h SLA via G2 gate. Decision: **approved 2026-09-28**.
- Card selection (visuals): P1 = Definition / 5-Tier HITL / CTA; P2 = 90 Agents / 8 Products / CTA; P3 = Orchestration Layer / Org Metrics / CTA. Rhythm navy → white → navy.
- Renderer: Pillow generator with exact token-palette snap (canonical `brand/tokens/brand-tokens.json` first); icon logo on navy (alpha-trimmed), full logo on white (near-white bg normalized to avoid grey box).
- ™ in visuals: P2 cover "LightSpeed Holdings Limited™", P3 hero "LightSpeed™ AI-native org structure".
- Queue rebuild (Step 7): pre-existing records were wrong — Post 1 marked `posted` without ever publishing (dry-run misrecorded), Post 2 held the X-thread text (🤖 `1/9…9/9`), Post 3 held draft checklist metadata. Queue cleared via `PublishQueue.clear()` and re-enqueued through the public API.
- Publish format decision (CEO, 2026-09-28): **LinkedIn feed post, 3,000-char cap** — `format_linkedin` unchanged, no article API. Queued bodies must pass `truncated=False` so the internal `[continued in queue]` marker never publishes. Full long-form articles remain canonical in `draft-v1.md`; feed bodies are verbatim condensations (no new claims) in each `post-0N/feed-v1.md`, enqueued with the draft's Hashtags line (combined title+body: 2,775 / 2,926 / 2,753 chars).

## Validation

- ECL lint passed, harness-change validate passed (re-run after draft rewrites and visual production).
- `ruff check src/` — all checks passed; `mypy src/` — no issues in 230 files.
- `pytest -m "not e2e"` — 2,568 passed; 4 errors in pre-existing untracked `tests/test_wayfinder_*` files (missing `filepath` fixture, unrelated to this change).
- Focused tests: `test_routine.py`, `test_publishing.py`, `test_transcription.py`, `test_mcp_server.py` — 61 passed.
- Research evidence: Post 1—3/4 claims verified; Post 2—5/5; Post 3—5/5 (unverified claims explicitly excluded from drafts).
- Drafts v1: article bodies 1,200+ words each (spec 1,200–1,800), `™` verified, voice checklist satisfied.
- Visuals: generator `--verify` 12/12 PASS (100.00% on-palette, 1200×627); official `check_brand_palette.py --tolerance 3` 12/12 PASS (0 failures); measured contrast 8/8 pairs pass (body ≥4.5:1, large text ≥3:1); visual inspection of all 12 renders clean after 3 fix pass (cover-body y-cursor, icon alpha-trim + footer alignment, full-logo near-white normalize).
- `ls-artifact-qa` five passes: PASS on all three posts — APPROVE stamped in each `qa-report.md`.
- Step 7 queue: `ai-company publishing list` shows 3 records, all `queued`; `publishing show` previews confirm `truncated=False` (2,775 / 2,926 / 2,753 chars incl. title) — feed bodies fit the 3,000 cap by construction (`enqueue_feed_posts.py` aborts before clearing the queue if any body is over).

## Next Step

- Step 7 scheduling is done (queue built, format decision recorded). Remaining before publish: GitHub issue #194 (LinkedIn Company account provisioning, "Pending") blocks any live POST; then `ai-company publishing publish <id> --live` on each scheduled date.

