#!/usr/bin/env python3
import ast
import sys

try:
    with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\cli\main.py", "r", encoding="utf-8") as f:
        code = f.read()
    ast.parse(code)
    print("File parses successfully")
    sys.exit(0)
except SyntaxError as e:
    print(f"Syntax error: {e}")
    print(f"Line: {e.lineno}, Offset: {e.offset}")
    sys.exit(1)