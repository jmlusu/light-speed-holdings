#!/usr/bin/env python3
with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Check subfile 600-630
file_content = "".join(lines[600:630])
print("Subfile parens - open:", file_content.count("("), "close:", file_content.count(")"))
# Show line 615 ending
print("Line 615 ends with ),:", lines[614].endswith("),"))
print("Line 615 last 10 chars repr:", repr(lines[614][-10:]))
print("Line 615 char count:", len(lines[614]))