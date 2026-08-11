from ai_company.data import (
    AuditStore,
    CostAnalytics,
    EscalationStore,
    KPIPipeline,
    TaskStore,
    init_database,
)
from ai_company.paths import get_database_path, get_project_root

root = get_project_root()
db = init_database(str(get_database_path()))

print("Backfilling SQLite data layer at", db.path)
print("=" * 60)

counts = {}

# Tasks (.opencode/inbox.json)
try:
    counts["tasks"] = TaskStore(db).import_json(root / ".opencode" / "inbox.json")
except Exception as exc:  # noqa: BLE001 - optional source, skip on any error
    print("  [skip] tasks: " + str(exc))
print("  tasks: " + str(counts.get("tasks", 0)))

# Audit events (.opencode/audit.jsonl)
try:
    counts["audit_events"] = AuditStore(db).import_jsonl(root / ".opencode" / "audit.jsonl")
except Exception as exc:  # noqa: BLE001 - optional source, skip on any error
    print("  [skip] audit_events: " + str(exc))
print("  audit_events: " + str(counts.get("audit_events", 0)))

# LLM cost records (results/cost_log.jsonl)
try:
    counts["cost_records"] = CostAnalytics(db).import_from_jsonl(
        root / "results" / "cost_log.jsonl"
    )
except Exception as exc:  # noqa: BLE001 - optional source, skip on any error
    print("  [skip] cost_records: " + str(exc))
print("  cost_records: " + str(counts.get("cost_records", 0)))

# Escalations (orchestrator/escalation.yaml)
try:
    counts["escalations"] = EscalationStore(db).import_from_yaml(
        root / "orchestrator" / "escalation.yaml"
    )
except Exception as exc:  # noqa: BLE001 - optional source, skip on any error
    print("  [skip] escalations: " + str(exc))
print("  escalations: " + str(counts.get("escalations", 0)))

# KPI history (dashboard/kpi_history/*_history.ndjson)
kpi_history_dir = root / "dashboard" / "kpi_history"
kpi_total = 0
if kpi_history_dir.exists():
    pipeline = KPIPipeline(db)
    for ndjson in sorted(kpi_history_dir.glob("*_history.ndjson")):
        department = ndjson.name.replace("_history.ndjson", "")
        try:
            kpi_total += pipeline.import_from_ndjson(department, ndjson)
        except Exception as exc:  # noqa: BLE001 - optional source, skip on any error
            print("  [skip] kpi " + department + ": " + str(exc))
print("  kpi_entries: " + str(kpi_total))

print("=" * 60)
print("Backfill complete.")
