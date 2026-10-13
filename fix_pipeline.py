#!/usr/bin/env python3
"""Fix encoding issues in pipeline.py"""

with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "rb") as f:
    content = f.read()

# Find and replace problematic bytes
# Look for the × (multiplication sign) or other non-ASCII chars in the KPI sections
text = content.decode("utf-8", errors="replace")

# Replace any remaining problematic characters
# The × character might be getting converted - replace with regular x
text = text.replace("×", "x")
text = text.replace("–", "-")  # en dash to hyphen
text = text.replace("—", "-")  # em dash to hyphen
text = text.replace("\u20ac", "-")  # Euro sign to hyphen
text = text.replace("\u00e2\u0082\u00ac", "-")  # UTF-8 bytes of Euro sign

# Write back
with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed encoding issues")