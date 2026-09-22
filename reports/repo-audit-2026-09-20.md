# Repository Audit — 2026-09-20

## Run

run_id: 35505778874
mode: scan-only (agent pass unavailable or failed)
probe_count: 22

## Verdict

The agent deep pass did not produce a valid report. This scan-only
report is generated from the deterministic evidence phase. Severity
totals below are provisional and should be validated by a full pass.

## Top Findings

Deterministic probe summary:

- [ok] registry.parse: agents=152
- [ok] cards.reconcile: registry=152 live=152 bak=0 orphan=[] missing=[]
- [ok] cards.tools: non-canonical tools: []
- [ok] ruff.check: All checks passed!
- [ok] pytest.collect: tests/unit/test_write_through.py::TestExecutorWiring::test_executor_passes_database_to_components | tests/unit/test_write_through.py::TestExecutorWiring::test_executor_without_database_keeps_file_only |  | =============================== warnings summary =============================== | .venv/lib/python3.12/site-packages/fastapi/testclient.py:1 |   /home/runner/work/light-speed-holdings/light-speed-holdings/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning:
- [ok] pytest.collect: tests/unit/test_validate_opencode.py::test_valid_v2_card_has_no_errors
- [ok] drift.manifest: { |   "status": "clean", |   "drifts": [], |   "warnings": [], |   "checked": 87, |   "timestamp": "2026-09-20T10:42:07.6048665+00:00" | }
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
- [ok] ecl.active: active change files=5
- [ok] graphify.update:   AST extraction: 1500/1525 uncached files (98%) [4 workers] |   AST extraction: 1525/1525 uncached files (100%) [4 workers] | Graph has 26745 nodes (above 5000 limit). Building aggregated community view... | graph.html written (aggregated: 1697 community nodes, 1720 cross-community edges) | Tip: run with --obsidian for full node-level detail. | [graphify watch] Rebuilt: 26745 nodes, 40475 edges, 1697 communities | [graphify watch] graph.json, graph.html and GRAPH_REPORT.md updated in graphify-o
- [ok] graphify.graph: nodes=26745 edges=0

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
