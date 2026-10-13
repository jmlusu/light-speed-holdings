#!/usr/bin/env python3
with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Show the exact last 20 chars of line 615
line = lines[614]
print("Line 615 last 30 chars:", repr(line[-30:]))
print("Line 615 last 30 bytes hex:", line[-30:].encode("utf-8").hex())

# Show line 619 last chars
line2 = lines[618]
print("Line 619 last 30 chars:", repr(line2[-30:]))

# Check if line 615 has a closing paren at the end
ends_paren = line.endswith(")")
ends_bracket = line.endswith("]")
print("Line 615 ends with ):", ends_paren)
print("Line 615 ends with ]:", ends_bracket)

# Count all parens in the file around this area
file_content = "".join(lines[600:630])
print("Subfile parens - open:", file_content.count("("), "close:", file_content.count(")"))