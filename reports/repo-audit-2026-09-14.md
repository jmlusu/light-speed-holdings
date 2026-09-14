# Repository Audit — 2026-09-14

## Run

run_id: 34890797024
mode: scan-only (agent pass unavailable or failed)
probe_count: 20

## Verdict

The agent deep pass did not produce a valid report. This scan-only
report is generated from the deterministic evidence phase. Severity
totals below are provisional and should be validated by a full pass.

## Top Findings

Deterministic probe summary:

- [ok] registry.parse: agents=144
- [ok] cards.reconcile: registry=144 live=144 bak=0 orphan=[] missing=[]
- [fail] cards.tools: non-canonical tools: ['software-architect:Design', 'software-architect:Define', 'software-architect:Evaluate', 'software-architect:Maintain', 'software-architect:Coordinate', 'software-architect:`read`', 'software-architect:`edit`', 'software-architect:`bash`']
- [fail] ruff.check: error: Failed to spawn: `ruff` |   Caused by: No such file or directory (os error 2)
- [fail] pytest.collect: error: Failed to spawn: `pytest` |   Caused by: No such file or directory (os error 2)
- [ok] drift.manifest:   "drifts": [], |   "checked": 81 | }
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
- [fail] graphify.update: error: Failed to spawn: `graphify` |   Caused by: No such file or directory (os error 2)

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
minor=7
orphan=0
stale=0
redundant=0
hitl_pending=0
-->
