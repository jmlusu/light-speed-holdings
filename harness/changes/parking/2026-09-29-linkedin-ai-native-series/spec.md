# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first (LinkedIn series plan approved via G1 gate)
- Questions asked this round: 0 (plan already approved, all clarifications resolved)

## Goal And Evidence

- Real problem or user request: Roll out the LinkedIn AI-Native Series "AI-Native Organizations" (11 posts) per the approved plan in `docs/Pharos/ai-native-orgs-linkedin-series-plan.md`. Series translates LightSpeed's 90-agent, 20-department, 5-tier HITL governance architecture into a repeatable framework for Malawi and SADC institutions.
- Current behavior: No LinkedIn series exists. Pharos P0 routine engine exists with 3 daily routines. Publishing rails (LinkedIn/Substack) are P1-built but not yet populated with series content. No reminder/notification system for series posts.
- Source of evidence: `docs/Pharos/ai-native-orgs-linkedin-series-plan.md` (full plan approved via G1 gate), `docs/adr/020-pharos-content-intelligence.md` (P1/P2 lists + MCP design), `harness/changes/archive/2026-09-14-pharos-content-intelligence-p1-p2-deep-research-publishing-rails-whisper-mcp` (P0 foundation delivered).

## User Scenarios And Success

- Primary user/system scenario:
  - **Routine reminder**: Pharos routine `linkedin_series_reminder` fires every 2 days at 7:00 AM CAT, prompting status checks and actions for the next due post.
  - **Research sprint**: `agentic_research_lead` produces evidence matrices for the next 3 posts (claim-to-source maps via `k-dense-research-lookup` + webfetch).
  - **Draft sprint**: `thought_leadership_author` writes Drafts v1 for Posts 1–3 in CEO "builder-writer-advocate" voice (1,200–1,800 words each, no emojis, evidence-led).
  - **CEO review**: Human CEO reviews drafts via GitHub PR (SLA: 48h, G2 gate). Reviews requested async via shared doc/PR.
  - **Visual production**: `ls-visual-storytelling` + `k-dense-infographics` produce hero visual + 3 carousel cards per post, brand-enforced (navy/red/cyan, Arial type scale, 4px grid, logo, `™` on first company mention).
  - **Schedule & publish**: Post queued via Pharos publish queue (MCP) with `scheduledAt`; live POST fires when `PHAROS_LINKEDIN_*` env creds configured (default: dry-run receipt).
  - **Measure**: `marketing_kpi_collector` tracks impressions, engagement rate, comments, profile visits, follower growth, Substack subscribers.

- Success criteria:
  - `linkedin_series_reminder` routine configured in `config/company/scheduler.yaml` with cron `0 7 */2 * *` (Africa/Blantyre), budget 2000 tokens, model tier standard.
  - 2 new routines in `config/company/routines.yaml` (`pharos_deep_research_brief`, `pharos_sadc_research_scan`) + 2 prompt templates under `templates/pharos/routines/`.
  - `thought_leadership_author` Drafts v1 for Posts 1–3 written and submitted for CEO review.
  - Visual assets (hero + 3 carousel cards) QA'd via `ls-artifact-qa` gate for Posts 1–3.
  - Posts 1–3 enqueued in Pharos publish queue, scheduled for Mon/Wed/Fri cadence.
  - KPI collector shows initial engagement metrics flowing.

## Non-Goals

- Full 11-post series execution (focus on Posts 1–3 sprint first).
- CEO voice profile / voice-preserving drafting (deferred per P0 scoping).
- Boost reverse-engineer batch fan-out over the message bus (deferred).
- Regional Malawi/SADC corpus collectors feeding the Monitor (P2, deferred).
- Board/tracker workspace, Lighthouse pilot packaging (P2, deferred).
- Any new top-level CLI; series surface rides existing `ai-company` subcommands only.

## Constraints

- Canonical tool list and registry contract unchanged (AGENTS.md §8).
- No new top-level CLI entry (`ai-company` root stays single app; ADR-020 consequence).
- No secrets committed; live-POST creds come only from env at runtime (`PHAROS_LINKEDIN_API_URL`, `PHAROS_LINKEDIN_TOKEN`).
- Optional deps and gracefully degrading guards (e.g., faster-whisper for transcription not required).
- MCP write path must require `approve`/`admin` RBAC role and pass through PII/content guards and audit.
- `pyproject.toml` changeset must keep `uv.lock` in sync (ECL §4).
- Brand enforcement: palette 80% navy / 10% red / 10% cyan; type: Arial scale; logo on navy; clear space 1× "L" height; `™` on first company mention; no emojis in visuals.
- Series cadence: every 2 days (Mon/Wed/Fri) per plan; alternative cadences documented but not primary.

## Assumptions

- `docs/Pharos/` corpus exists in the MAIN tree (`C:\Users\jmlus\light-speed-holdings\docs\Pharos\`); MCP `pharos_reference` must resolve the corpus path at runtime (main tree copy when worktree lacks it) and handle absence gracefully.
- Faster-whisper is never installed in the default env; tests mock/skip its import path.
- Registry remains loadable via `ai_company.registry.load_registry()` for GraphEngine wiring.
- `orchestrator/approval.py` ApprovalGate is available for the publish write gate if needed.
- Human CEO review SLA of 48h is realistic for draft v1 submissions.

## Open Questions

- [RESOLVED: Post 1–3 research sprint runs sequential order (Post 1 first, then 2, then 3) to allow iterative evidence incorporation per the G2 CEO review gate.]
- [RESOLVED: `ls-visual-storytelling` leads visual production workflow first, producing hero visual; `k-dense-infographics` produces carousel cards second; both feed into mandatory `ls-artifact-qa` gate per plan step 5.]

## Resolved Clarifications

- Series title: "AI-Native Organizations" (approved via G1 gate).
- Series cadence: Every 2 days (Mon/Wed/Fri) per plan — confirmed.
- CEO voice: "Builder-Writer-Advocate" (no emojis, evidence-led, `™` on first company mention) — confirmed.
- Cross-post to Substack: Series as monthly digest (4 posts/issue), launch with Post 1 capture early subscribers — confirmed.
- Publish rail: LinkedIn API directly (P1 buy-side) with env-gated live POST, dry-run default — confirmed.
- reminder routine cron: `0 7 */2 * *` Africa/Blantyre 7AM CAT — confirmed.
- 11-post series map to 3 pillars (Company Builder, Use Cases, Policy) — confirmed.
- HITL gates G1-G5 defined and approved — confirmed.