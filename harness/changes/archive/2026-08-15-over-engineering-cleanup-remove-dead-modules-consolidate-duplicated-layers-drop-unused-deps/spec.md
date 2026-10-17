# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first (repo-wide ponytail audit already delivered and vetted)
- Questions asked this round: 1 (how to open the ticket while Security Hardening was active — resolved: park it first)

## Goal And Evidence

- Real problem or user request: The repo carries ~13K lines of zero-caller modules, duplicated layers (2 eval stacks, 3 atomic-write helpers, 3 WS broadcast bridges, 2 dead_letter modules), dead methods/keys, and declared-but-unused deps. User asked for a repo-wide ponytail audit and then a second-opinion review of the cuts; this ticket captures the verified implementation plan.
- Current behavior: Dead code is imported only through `__init__` re-export chains and tests; live code paths are unaffected.
- Source of evidence: ponytail-audit findings + two independent review rounds (ceo-advisor/chief-of-staff/cto, then cdo/cio/solution-architect/software-architect), all import-graph-verified with `Select-String` over `git ls-files '*.py'`.

## User Scenarios And Success

- Primary user/system scenario: An engineer/agent runs `ruff check src/ && mypy src/ && pytest` and `AgentGenerator().generate_all()` after the change; everything passes and generated agent files are unchanged.
- Success criteria:
  - No live module imports a removed module (import-graph clean after each batch).
  - `pytest` green after the ~13 test-file co-changes.
  - Generated agents regenerate identically (CI `generated-check` passes).
  - CLI help (`ai-company --help` + each subcommand) unchanged.
- Acceptance criteria:
  - Dead modules listed in plan.md are gone; `__init__.py` slims land in the same commit.
  - Keep-list is intact (verified by import searches + smoke of memory init path and `cli/client.py`).
  - `uv.lock` regenerated with the dep drop; all `--frozen` flows (Dockerfile, ci.yml, autonomous.yml, governance.yml) still resolve.
  - Docs/SOPs that promised cut features are updated in lockstep (see plan.md).
  - Parked Security Hardening change is resumed and still validates after this change lands.

## Non-Goals

- No behavior changes to live execution paths: no LLM prompt semantics change beyond removing the verified double-wrap, no endpoint/contract changes, no metric-name changes without the derived-gauge rework.
- No new feature work (no networkx adoption, no rebuild of evals/anomaly).
- Correctness bugs, security holes, and performance issues found en route are out of scope (noted for a normal review pass, e.g. `AnomalyDetector.set_threshold` no-op, `monitoring.py:560` ghost read of `.opencode/dead_letter_queue.json`).
- Do NOT delete `models/task.py`, `registry/resolver.py`, `ml/embeddings.py`, `memory/vector_store._fallback_search`, `llm/oauth2.py`, `llm/token_bucket.py`, HITLGate blocking path, `dashboard/monitoring.py` module, `dashboard/mobile_api.py`, `MessageBus.acknowledge_task`, `cost_tracker._export_summary`.
- The 90-day anomaly-detection / predictive-analytics vision is deferred deliberately (documented), not implemented here.

## Constraints

- `harness/changes/INDEX.json` is script-generated only; never hand-edit.
- ECL: one active change at a time; Security Hardening was parked to open this ticket and is resumed after this lands.
- Gate every batch on `ruff check src/ && mypy src/ && pytest` (AGENTS.md section 6); template changes additionally run the generator and re-check `generated-check`.
- Do not touch `.env`, `.env.*`, `docker-compose*.yml` auth config, `release.yml`, `scripts/backup.ps1` — those belong to the parked Security Hardening change.

## Assumptions

- The parked Security Hardening change resumes after this cleanup lands and before any security-file deletions (cut of `security/keys.py`/`secrets_scanner.py` is sequenced last, after that change closes).
- No external consumers of the in-repo API (ADR-014 states all consumers are in-repo), so removing dead metric names is safe provided staging Prometheus has no alert rules on them (verified: none).

## Open Questions

- (none — all resolved by the two review rounds)

## Resolved Clarifications

- Whether `ml/complexity.py` is live: it is imported only inside the dead `resolve_with_complexity` (model_router.py:584) — both cut together.
- Whether `MessageBus.acknowledge_task` is dead: it is test-covered (`test_concurrent_inbox.py:123`) — excluded from the cut.
- Whether dead-template count is 7 or 8: 8, incl. `department.md.j2`; `postmortem.md.j2` is live and excluded.
- Whether `resolve_with_complexity`/`TaskComplexityScorer` remain: no — deleted with `ml/complexity.py`.
- Whether `execute_task`/`execute_task_stream` are cut: no — they become orphaned public API after `ai/evals/` is cut but remain tested; `_parse_response` is live (`client.py:240,366`).
