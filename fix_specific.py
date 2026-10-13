#!/usr/bin/env python3
with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Fix each slide's tuple to close on the same line
# Slide 7 (lines 603-604 area) - fix line 603
# Slide 8 (lines 611-612 area) - fix line 611  
# Slide Key Decisions (lines 619-620 area) - fix line 619
# Slide 9 (lines 623-624 area) - fix line 623

# First, let me see the exact content to fix
for i in [602, 610, 618, 622]:  # 0-indexed, so lines 603, 611, 619, 623
    print(f"Line {i+1}: {repr(lines[i])}")
    print(f"  open: {lines[i].count('(')}, close: {lines[i].count(')')}")