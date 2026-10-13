#!/usr/bin/env python3
with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# The structure appears to be:
# Line with tuple: ("Title", [bullets]),  - the ), closes the tuple
# Description text line
# Line with {}), - this seems to be: dict {} + ), where ) closes tuple above + , separates slides
# But Python doesn't allow ) to close a tuple from 2 lines above

# The fix: ensure every tuple has ) on the same line as (

# For lines 603, 611, 619 - these currently have "})," but need analysis
# Let me just rebuild the structure properly

# First, let me see what the full slide definitions look like
# I'll look at a complete slide pattern

# Slide 7 pattern (around lines 600-610)
print("=== Slide 7 structure ===")
for i in range(599, 612):
    print(f"Line {i+1}: {repr(lines[i])}")

print("\n=== Slide 8 structure ===")
for i in range(609, 621):
    print(f"Line {i+1}: {repr(lines[i])}")

print("\n=== Key Decisions structure ===")
for i in range(615, 625):
    print(f"Line {i+1}: {repr(lines[i])}")

print("\n=== Closing structure ===")
for i in range(621, 632):
    print(f"Line {i+1}: {repr(lines[i])}")