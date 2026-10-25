# Repository Audit — 2026-10-25

## Run

run_id: 40184679558
mode: scan-only (agent pass unavailable or failed)
probe_count: 19

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
- [ok] pytest.collect: tests/unit/test_write_through.py::TestMessageBusWriteThrough::test_without_database_writes_file_only | tests/unit/test_write_through.py::TestAuditWriterWriteThrough::test_write_mirrors_to_sqlite | tests/unit/test_write_through.py::TestAuditWriterWriteThrough::test_write_batch_mirrors_to_sqlite | tests/unit/test_write_through.py::TestAuditWriterWriteThrough::test_without_database_writes_file_only | tests/unit/test_write_through.py::TestCostTrackerWriteThrough::test_record_usage_mirrors_to_sqlite 
- [ok] pytest.collect: tests/unit/test_validate_opencode.py::test_valid_v2_card_has_no_errors
- [ok] drift.manifest: { |   "drifts": [], |   "warnings": [], |   "timestamp": "2026-10-25T10:25:45.4516024+00:00", |   "checked": 87, |   "status": "clean" | }
- [ok] drift.manifest: drifts=0 checked=87
- [ok] cards.generated_drift: no drift after regeneration
- [ok] tree.departments: company=20 config=20 only_company=[] only_config=[]
- [ok] tree.data_etl: data/etl present
- [ok] tree.prompts: prompts/*.md=29
- [ok] gitignore.data.orchestrator.scheduler.yaml: data/orchestrator/scheduler.yaml ignored while required by cli/validate.py
- [ok] gitignore.data.orchestrator.escalation.yaml: data/orchestrator/escalation.yaml ignored while required by cli/validate.py
- [ok] gitignore..playwright-cli: .playwright-cli/ present
- [ok] gitignore.screenshots: screenshots/ present
- [ok] gitignore.results: results/ present
- [ok] ci.registry_gate: ci.yml never validates agent registry
- [warn] ecl.active: active change files=0

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
