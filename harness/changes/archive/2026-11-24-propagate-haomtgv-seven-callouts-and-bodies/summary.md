---
title: "Propagate HAOMTGV seven callouts and bodies"
slug: "propagate-haomtgv-seven-callouts-and-bodies"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "complete"
spec_review: "approved"
plan_review: "approved"
modules: ["docs/pharos", "docs/pharos/linkedin-series", "src/components/home", "src/pages", "scripts/maintenance"]
files: [
  "docs/pharos/h-a-o-m-t-g-v-framework.md",
  "docs/pharos/articles/h-a-o-m-t-g-v-seven-layers.md",
  "docs/pharos/whitepaper/h-a-o-m-t-g-v-chapter.md",
  "docs/pharos/linkedin-series/post-01/draft-v1.md",
  "docs/pharos/linkedin-series/post-02/draft-v1.md",
  "docs/pharos/linkedin-series/post-03/draft-v1.md",
  "docs/pharos/linkedin-series/post-03/feed-v1.md",
  "docs/pharos/linkedin-series/post-04/draft-v1.md",
  "docs/pharos/linkedin-series/post-04/feed-v1.md",
  "docs/pharos/linkedin-series/post-04/video-script.md",
  "docs/pharos/linkedin-series/post-04/x-thread.md",
  "docs/pharos/linkedin-series/post-04/substack-section.md",
  "docs/pharos/linkedin-series/post-05/draft-v1.md",
  "docs/pharos/linkedin-series/post-06/draft-v1.md",
  "docs/pharos/linkedin-series/post-07/draft-v1.md",
  "docs/pharos/linkedin-series/post-08/draft-v1.md",
  "docs/pharos/linkedin-series/post-09/draft-v1.md",
  "docs/pharos/linkedin-series/post-10/draft-v1.md",
  "docs/pharos/linkedin-series/post-11/draft-v1.md",
  "docs/pharos/linkedin-series/post-11/substack-section.md",
  "scripts/maintenance/enqueue_post1.py",
  "src/components/home/HAOMTGVSection.tsx",
  "src/data/registries/faq-registry.json",
  "src/pages/HAOMTGVPage.tsx"
]
tags: ["haomtgv", "documentation", "copy-propagation"]
validation_status: "pass"
validation_results:
  - "npm run lint (tsc --noEmit): PASS"
  - "npm run test (vitest): 17 files, 154 tests passed"
  - "npm run build (tsc + vite build): PASS"
  - "git diff --check: PASS (CRLF notices only, no whitespace errors)"
  - "grep old callout strings in scoped files: zero survivors"
  - "ECL lint (lint-ecl.ps1): PASS"
  - "ruff check src/ tests/ scripts/presentation/: PASS"
  - "mypy src/: PASS (248 files)"
  - "check-cost-tracker.py: PASS"
  - "check-confidential-artifacts.py: PASS"
  - "bandit -r src/: PASS (exit 0)"
  - "uv-audit shim: PASS (exit 0)"
  - "pytest -q -m 'not e2e' --basetemp=.pytest_tmp_haomtgv --cov=src/ai_company --cov-fail-under=72: 2948 passed, 2 skipped, 67 deselected, coverage 78.87%"
  - "version sync: pyproject.toml 0.6.0 == CHANGELOG 0.6.0"
  - "side-effect files restored before archive: data/orchestrator/cost_tracker.json, src/data/generated/agent-registry.public.json"
created_at: "2026-11-24"
updated_at: "2026-11-24"
session_id: "0fc024b7-92f4-4f96-b12a-2107761c95dd"
owner_agent: "jmlus"
claimed_at: "2026-11-24"
---

# Summary

## Outcome

Propagate the approved seven-callout rewrite through the canonical framework docs, the LinkedIn sequence copy, and website prose. Scope was confirmed by the user: canonical + sequence only; docs and code only; no visual assets and no normalization of alternate pillar names elsewhere.

## Decisions

- Callouts are two or three words, name first: Humans authorize / Agents act / Orchestration orders / Memory persists / Tools stay sandboxed / Governance gates / Value verified.
- V stays named Value; verification is its mechanism.
- M keeps the pillar name first; sovereign inference stays in the body.
- Short `title:` / `name:` / `layer:` UI labels are not renamed.
- Historical audit records, alternate-name docs, visual assets, visual generator template, and the root `haomtgv-committed.tsx` artifact are out of scope.

## Validation

- Frontend: typecheck, 154 tests, and production build all pass.
- Docs: all three tiers applied; grep for old callout strings returns zero in scoped files.
- Python: ruff, mypy, cost-tracker, confidential-artifact, bandit, and uv-audit checks all pass.
- Full suite: 2948 passed, 2 skipped, 67 deselected; coverage 78.87% against a 72% gate.
- ECL lint: PASS. Side-effect files restored after the test run.

## Next Step

Commit by explicit path, push branch, open PR, and read CI status with `gh pr checks`.
