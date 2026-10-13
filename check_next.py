#!/usr/bin/env python3
with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Show lines 615-625
for i in range(614, 625):
    print(f"Line {i+1} ({len(lines[i])} chars): {repr(lines[i][:80])}...")