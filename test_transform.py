import json
import os

from ai_company.registry.public_transform import transform_public_registry

# Test 1: Run once, save output
result1 = transform_public_registry()
with open("test_output1.json", "w") as f:
    json.dump(result1, f)

# Test 2: Run again, compare
result2 = transform_public_registry()
with open("test_output2.json", "w") as f:
    json.dump(result2, f)

# Verify idempotency
with open("test_output1.json") as f:
    data1 = json.load(f)
with open("test_output2.json") as f:
    data2 = json.load(f)

# Compare meta
assert data1["meta"] == data2["meta"], "Meta differs between runs!"
print(
    f"Idempotent: meta matches - Agents: {data1['meta']['agents']}, Departments: {data1['meta']['departments']}"
)

# Compare agents list
agents1 = data1.get("agents", [])
agents2 = data2.get("agents", [])
assert len(agents1) == len(agents2) == 90, (
    f"Expected 90 agents, got {len(agents1)} and {len(agents2)}"
)

# Compare department info
dept1 = data1.get("departments", {})
dept2 = data2.get("departments", {})
assert dept1 == dept2, "Departments differ between runs!"

print("All P7 regression tests passed!")

# Cleanup

os.remove("test_output1.json")
os.remove("test_output2.json")
