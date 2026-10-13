#!/usr/bin/env python3
with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Show lines 600-630 with parenthesis analysis
for i in range(599, 631):
    line = lines[i]
    open_p = line.count("(")
    close_p = line.count(")")
    status = "OK" if open_p == close_p else f"MISMATCH: open={open_p}, close={close_p}"
    print(f"Line {i+1:3d} ({len(line):3d} chars): {status} {repr(line[:60])}")