#!/usr/bin/env python3
with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Show lines 617-622
for i in range(616, 623):
    print(f"{i+1}: {lines[i]}", end="")
print()