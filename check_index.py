import json
with open("harness/changes/INDEX.json", encoding="utf-8-sig") as f:
    d = json.load(f)
print("Type:", type(d))
print("Count:", len(d))
for i, e in enumerate(d[:3]):
    keys = list(e.keys())
    print("Entry", i, ": keys =", keys)
    print("  id=", e.get("id"))
    print("  title=", e.get("title"))
    print("  status=", e.get("status"))
    print("  location=", e.get("location"))
    print("  slug=", e.get("slug"))
    print("  session_id=", e.get("session_id"))
    print("  validation_status=", e.get("validation_status"))
    print("  phase=", e.get("phase"))
    print("  spec_review=", e.get("spec_review"))

print("\nCompleted entries:")
for e in d:
    if e.get("status") == "completed":
        print(f"  id={e['id']} validation_status={e.get('validation_status')} phase={e.get('phase')} spec_review={e.get('spec_review')}")