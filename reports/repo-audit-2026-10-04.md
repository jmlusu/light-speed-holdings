# Repository Audit — 2026-10-04

## Run

run_id: 37200026812
mode: scan-only (agent pass unavailable or failed)
probe_count: 22

## Verdict

The agent deep pass did not produce a valid report. This scan-only
report is generated from the deterministic evidence phase. Severity
totals below are provisional and should be validated by a full pass.

## Top Findings

Deterministic probe summary:

- [ok] registry.parse: agents=90
- [ok] cards.reconcile: registry=90 live=90 bak=0 orphan=[] missing=[]
- [ok] cards.tools: non-canonical tools: []
- [ok] ruff.check: All checks passed!
- [ok] pytest.collect: tests/unit/test_write_through.py::TestExecutorWiring::test_executor_passes_database_to_components | tests/unit/test_write_through.py::TestExecutorWiring::test_executor_without_database_keeps_file_only |  | =============================== warnings summary =============================== | .venv/lib/python3.12/site-packages/fastapi/testclient.py:1 |   /home/runner/work/light-speed-holdings/light-speed-holdings/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning:
- [ok] pytest.collect: tests/unit/test_validate_opencode.py::test_valid_v2_card_has_no_errors
- [ok] drift.manifest: { |   "drifts": [], |   "checked": 87, |   "status": "clean", |   "warnings": [], |   "timestamp": "2026-10-04T11:50:21.9823692+00:00" | }
- [ok] drift.manifest: drifts=0 checked=87
- [ok] cards.generated_drift: no drift after regeneration
- [ok] tree.departments: company=20 config=20 only_company=[] only_config=[]
- [ok] tree.data_etl: data/etl present
- [ok] tree.prompts: prompts/*.md=2
- [ok] gitignore.orchestrator.scheduler.yaml: orchestrator/scheduler.yaml ignored while required by cli/validate.py
- [ok] gitignore.orchestrator.escalation.yaml: orchestrator/escalation.yaml ignored while required by cli/validate.py
- [ok] gitignore.graphify: ignored=True tracked_files=0
- [ok] gitignore..playwright-cli: .playwright-cli/ present
- [ok] gitignore.screenshots: screenshots/ present
- [ok] gitignore.results: results/ present
- [ok] ci.registry_gate: ci.yml never validates agent registry
- [warn] ecl.active: active change files=0
- [ok] graphify.update:   AST extraction: 1700/1801 uncached files (94%) [4 workers] |   AST extraction: 1800/1801 uncached files (99%) [4 workers] |   AST extraction: 1801/1801 uncached files (100%) [4 workers] | Graph has 31157 nodes (above 5000 limit). Building aggregated community view... | graph.html written (aggregated: 1986 community nodes, 1798 cross-community edges) | Tip: run with --obsidian for full node-level detail. | [graphify watch] Rebuilt: 31157 nodes, 46867 edges, 1986 communities | [graphify watch] g
- [ok] graphify.graph: nodes=31157 edges=0

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
major=0
minor=0
orphan=0
stale=0
redundant=0
hitl_pending=0
-->
