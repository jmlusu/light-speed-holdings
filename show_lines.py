#!/usr/bin/env python3
with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Show lines 613-620
for i in range(612, 621):
    print(f"{i+1}: {lines[i]}", end="")
print()