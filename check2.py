with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "rb") as f:
    content = f.read()
# Find line 308 area
lines = content.split(b'\n')
for i, line in enumerate(lines[305:312], start=306):
    # Decode with replacement
    dec = line.decode('utf-8', errors='replace')
    print(f"Line {i+1} (raw bytes preview): {dec[:80]}")
    # Find non-ASCII
    for j, b in enumerate(line):
        if b > 127:
            print(f"  Non-ASCII byte at pos {j}: {b} (U+{b:02X})")