#!/usr/bin/env python3
import re

with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find the Key Decisions Required section
match = re.search(r'\(["\']Key Decisions Required["\']", content)
if match:
    start = match.start()
    # Get a chunk after the match
    chunk = content[start:start+2000]
    print("Chunk around Key Decisions Required:")
    print(chunk)
    
    # Count parens in each line
    lines = chunk.split('\n')
    for i, line in enumerate(lines):
        open_p = line.count('(')
        close_p = line.count(')')
        if open_p != close_p:
            print(f"Line {i}: open={open_p}, close={close_p}")
            print(f"  {repr(line[:100])}")