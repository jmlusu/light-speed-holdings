# fix(ci): repair stale skill test, Pharos path casing and ECL clarification

**ID:** BUG-0e4c05a6d
**Date:** 2026-11-12
**Resolved:** resolved
**Commit:** 0e4c05a6d97c70aa0a5f5634d4d7744cd118e169
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

Recorded in the commit message: Resolves the failing gates on #581: update the subagent skill test to the installed catalogue, align docs/Pharos -> docs/pharos references in site data, record MIMO_API_KEY in AGENTS.md, and clear the active spec clarification marker.

_Source: commit 0e4c05a6d97c70aa0a5f5634d4d7744cd118e169 message (verbatim excerpt)._

## Fix (filled by the resolving engineer)

Resolves the failing gates on #581: update the subagent skill test to the installed catalogue, align docs/Pharos -> docs/pharos references in site data, record MIMO_API_KEY in AGENTS.md, and clear the active spec clarification marker.

_Source: commit 0e4c05a6d97c70aa0a5f5634d4d7744cd118e169 message (verbatim)._

## Files Changed

AGENTS.md
docs/STATUS.md
docs/pharos/qa/_probe-90agent.json
docs/pharos/qa/_probe-ladder.json
docs/pharos/qa/_probe-oss.json
knowledge/technology/bug-fixes/BUG-461bce0a0.md
src/components/AssessmentWizard.tsx
src/components/BeforeAfterWorkflow.tsx
src/data/insights.ts
src/data/pharos.ts
src/data/registries/faq-registry.json
src/pages/AiAssessmentPage.tsx
src/pages/PharosPage.tsx
src/pages/WhatWeDoPage.tsx
tests/test_subagent_framework.py
.audit/reconciliation/deliverable19-session-recovery-and-verification.md
content/pharos-2026-10-12/01-open-source-cost-architecture.ts
content/pharos-2026-10-12/02-five-tier-approval-matrix.ts
content/pharos-2026-10-12/03-inside-a-90-agent-company.ts
content/pharos-2026-10-12/04-offline-first-ai-for-africa.ts
content/pharos-2026-10-12/05-dual-economy-ai-pricing.ts
content/pharos-2026-10-12/06-evidence-ladder-honest-claims.ts
data/orchestrator/cost_tracker.json
harness/changes/active/spec.md
harness/changes/active/summary.md
packages/data-use-cases/src/insights.ts
static/brand/templates/generate-linkedin-series-visuals.py
static/brand/templates/generate-post-templates.py

_Source: GitHub commit 0e4c05a6d97c70aa0a5f5634d4d7744cd118e169 file list, filtered to text/source files._

## Diagnostic Commands

Not recorded in the commit message.

## Verification

Not recorded in the commit message.

Commit is present in the current origin/main history; CI was not re-run for this record.

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
