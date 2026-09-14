# Repository Audit — 2026-09-14

## Run

run_id: 34892751142
mode: scan-only (agent pass unavailable or failed)
probe_count: 22

## Verdict

The agent deep pass did not produce a valid report. This scan-only
report is generated from the deterministic evidence phase. Severity
totals below are provisional and should be validated by a full pass.

## Top Findings

Deterministic probe summary:

- [ok] registry.parse: agents=144
- [ok] cards.reconcile: registry=144 live=144 bak=0 orphan=[] missing=[]
- [ok] cards.tools: non-canonical tools: []
- [ok] ruff.check: All checks passed!
- [ok] pytest.collect:  | -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html | 2368/2435 tests collected (67 deselected) in 6.49s
- [ok] pytest.collect: tests/unit/test_validate_opencode.py::test_valid_v2_card_has_no_errors
- [ok] drift.manifest:   "timestamp": "2026-09-14T20:25:48.9182379+00:00", |   "drifts": [] | }
- [ok] drift.manifest: drifts=0 checked=81
- [fail] cards.verify_script: [31;1mWrite-Error: [31;1mRegistry entry 'media-pr-relations' is missing a file path.[0m | [31;1mWrite-Error: [31;1mRegistry entry 'talent-academy-lead' is missing a file path.[0m | [31;1mWrite-Error: [31;1mRegistry entry 'media-generation-owner' is missing a file path.[0m
- [warn] tree.departments: config/departments=1 company/departments=0
- [ok] tree.data_etl: data/etl present
- [ok] tree.prompts: prompts/*.md=2
- [ok] gitignore.orchestrator.scheduler.yaml: orchestrator/scheduler.yaml ignored while required by cli/validate.py
- [ok] gitignore.orchestrator.escalation.yaml: orchestrator/escalation.yaml ignored while required by cli/validate.py
- [warn] gitignore.graphify: graphify-out tracked
- [warn] gitignore..playwright-cli: .playwright-cli/ present
- [ok] gitignore.screenshots: screenshots/ present
- [ok] gitignore.results: results/ present
- [ok] ci.registry_gate: ci.yml never validates agent registry
- [warn] ecl.active: active change files=0
- [ok] graphify.update: Code graph updated. For doc/paper/image changes run /graphify --update in your AI assistant. | Tip: set GEMINI_API_KEY or GOOGLE_API_KEY to use Gemini for semantic extraction. |   warning: 2 file(s) had syntax errors and may be partially extracted: src/ai_company/dashboard/static/js/command-bar.js (first error at line 1, 16 symbol(s) extracted), src/components/SadcGovernanceFramework.tsx (first error at line 226, 2 symbol(s) extracted)
- [ok] graphify.graph: nodes=25801 edges=0

## Critical Blockers

## Major Findings

## Minor Findings

## Orphans / Stale / Redundant

## Governance Notes

Run degraded: see Actions run for probe details.

<!-- AUDIT_VMETA
mode=scan-only
verdict=attention
critical=0
major=2
minor=3
orphan=0
stale=0
redundant=0
hitl_pending=0
-->
