#!/usr/bin/env python3
with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\presentation\pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()
import ast
try:
    ast.parse(code)
    print("File parses successfully!")
except SyntaxError as e:
    print(f"Syntax error: {e}")
    print(f"Line: {e.lineno}, Offset: {e.offset}")