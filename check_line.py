#!/usr/bin/env python3
with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
print(f"Line 615: {repr(lines[614])}")
print(f"Line 616: {repr(lines[615])}")
print(f"Line 614 open parens: {lines[614].count('(')}")
print(f"Line 614 close parens: {lines[614].count(')')}")