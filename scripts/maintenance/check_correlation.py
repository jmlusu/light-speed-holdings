from ai_company.orchestrator.escalation_events import get_escalation_event_store
from ai_company.orchestrator.dead_letter import get_dead_letter_store
from ai_company.audit.export import export_audit_log

# Check escalation events
store = get_escalation_event_store()
events = store.list_all()
print(f"Escalation events: {len(events)}")
for e in events[:3]:
    print(f"  correlation_id: {e.correlation_id}")

# Check dead letter
dl_store = get_dead_letter_store()
dl_events = dl_store.list_all()
print(f"Dead letter entries: {len(dl_events)}")
for e in dl_events[:3]:
    print(f"  correlation_id: {e.correlation_id}")
