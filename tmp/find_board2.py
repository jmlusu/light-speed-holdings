from ai_company.registry import load_registry
reg = load_registry()
# Search for any entry with board in name or department
print("=== Executives with 'board' ===")
for e in reg.executives:
    if 'board' in e.name.lower():
        print(f"  {e.id}: {e.name}, reports_to: {e.reports_to}")

print("\n=== Specialists with 'board' or 'chair' ===")
for s in reg.specialists:
    if 'board' in s.name.lower() or 'chair' in s.name.lower():
        print(f"  {s.id}: {s.name}, reports_to: {s.reports_to}, dept: {s.department}")

print("\n=== All departments ===")
depts = set()
for e in reg.executives:
    if e.department:
        depts.add(e.department)
for s in reg.specialists:
    if s.department:
        depts.add(s.department)
for d in sorted(depts):
    print(f"  Department: {d}")

print("\n=== Company structure ===")
# Print company attributes
for attr in dir(reg.company):
    if not attr.startswith('_'):
        val = getattr(reg.company, attr)
        if not callable(val):
            print(f"  company.{attr}: {val}")