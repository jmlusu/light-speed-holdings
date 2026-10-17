import json
import os
from datetime import datetime, timezone

# Read inbox.json
with open(r".opencode\inbox.json") as f:
    data = json.load(f)

# Status breakdown
statuses = {}
for entry in data:
    s = entry.get("status", "unknown")
    statuses[s] = statuses.get(s, 0) + 1
print(f"Status breakdown: {statuses}")

# Age distribution
now = datetime.now(timezone.utc)
entries = list(data)
old_count = 0
recent_count = 0
for e in entries:
    ca = e.get("created_at", "")
    try:
        # Parse ISO format - could have various formats
        if ca.endswith("Z"):
            dt = datetime.fromisoformat(ca.replace("Z", "+00:00"))
        else:
            dt = datetime.fromisoformat(ca)
        delta = (now - dt).days
        if delta > 7:
            old_count += 1
        if delta <= 3:
            recent_count += 1
    except Exception as ex:
        pass  # skip entries with unparseable dates
print(f"Entries older than 7 days: {old_count}")
print(f"Entries in last 3 days: {recent_count}")

# Show a few entries
print(f"\nTotal entries: {len(data)}")
print("First 3 entries:")
for i, e in enumerate(data[:3]):
    print(
        f"  {i}: id={e.get('id', '')[:8]}... status={e.get('status')} created={e.get('created_at')}"
    )

# Check memory directory
mem_dir = r"memory"
if os.path.exists(mem_dir):
    print("\nMemory directory structure:")
    for root, dirs, files in os.walk(mem_dir):
        dirs[:] = [d for d in dirs if d not in [".venv", "node_modules", ".git"]]
        level = root.replace(mem_dir, "").count(os.sep)
        indent = "  " * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = "  " * (level + 1)
        for f in files:
            fp = os.path.join(root, f)
            size = os.path.getsize(fp)
            print(f"{sub_indent}{f} ({size:,} bytes)")

# Check vector index files
vec_dir = r"memory/vector_index"
if os.path.exists(vec_dir):
    print("\nVector index files:")
    for f in os.listdir(vec_dir):
        fp = os.path.join(vec_dir, f)
        size = os.path.getsize(fp)
        print(f"  {f}: {size:,} bytes ({size / 1024 / 1024:.1f} MB)")
