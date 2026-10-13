with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(305, 312):
    line = lines[i]
    print(f"Line {i+1}: {repr(line[:100])}")