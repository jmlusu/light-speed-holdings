#!/usr/bin/env python3
import re

with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Look at line 615 (index 614)
line = lines[614]
print(f"Line 615 ({len(line)} chars):")
print(line)

# Count opening and closing parens in this specific line
open_p = line.count('(')
close_p = line.count(')')
print(f"\nOpen parens: {open_p}, Close parens: {close_p}")
print(f"Difference: {open_p - close_p}")

# Show each parenthesis position
for i, ch in enumerate(line):
    if ch == '(':
        print(f"  Open paren at pos {i}: {repr(line[max(0,i-10):i+10])}")
    elif ch == ')':
        print(f"  Close paren at pos {i}: {repr(line[max(0,i-10):i+10])}")