#!/usr/bin/env python
# Script to fix cost_analytics.py - add department tracking

import ast

# Read the original file
with open("cost_analytics.py", "r", encoding="utf-8") as f:
    content = f.read()

# Parse to check it's valid first
try:
    ast.parse(content)
    print("Original file parses OK")
except SyntaxError as e:
    print(f"Original file has syntax error: {e}")
    exit(1)

lines = content.split("\n")

# Find and modify record_usage signature
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.strip().startswith("def record_usage("):
        # We need to add department parameter after task_id
        # Find the task_id line and add department after it
        j = i
        while j < len(lines) and "task_id" not in lines[j]:
            j += 1
        # Now j points to the line with task_id
        # Copy lines from i to j (inclusive of task_id line)
        new_lines.extend(lines[i : j + 1])
        # Add the department line after task_id
        new_lines.append("        department: str,")
        # Skip past the original lines we've already handled
        # We need to figure out how many lines we consumed
        # The record_usage signature spans from def record_usage( to the closing )
        # Let's find the closing paren
        k = j + 1
        indent_count = 0
        while k < len(lines):
            line = lines[k]
            if line.strip().startswith(")"):
                # Check if this is the closing paren of record_usage
                # by counting parentheses
                open_parens = l.count("(") - l.count(")")
                if open_parens <= 0:
                    # This might be the closing paren
                    # Skip this line and the next (the -> int line)
                    k += 2  # skip ) and -> int
                    break
            k += 1
        i = k
    else:
        new_lines.append(line)
        i += 1

content = "\n".join(new_lines)

# Verify it still parses
try:
    ast.parse(content)
    print("After record_usage change: parses OK")
except SyntaxError as e:
    print(f"Syntax error after record_usage change: {e}")
    # Show context around the error
    lines2 = content.split("\n")
    for i in range(max(0, e.lineno - 5), min(len(lines2), e.lineno + 5)):
        print(f"  {i}: {lines2[i]}")
    exit(1)

# Write back
with open("cost_analytics.py", "w", encoding="utf-8") as f:
    f.write(content)

print("File written successfully with record_usage change")

# Now do the same for check_budget - add department parameter
with open("cost_analytics.py", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.strip().startswith("def check_budget("):
        # Add department parameter after task_id
        j = i
        while j < len(lines) and "task_id" not in lines[j]:
            j += 1
        new_lines.extend(lines[i : j + 1])
        new_lines.append("        department: str | None = None,")
        # Find the closing
        k = j + 1
        while k < len(lines):
            cl = lines[k]
            if cl.strip().startswith(")") and "->" in "\n".join(lines[k : k + 2]):
                k += 2
                break
            k += 1
        i = k
    else:
        new_lines.append(line)
        i += 1

content = "\n".join(new_lines)

try:
    ast.parse(content)
    print("After check_budget change: parses OK")
except SyntaxError as e:
    print(f"Syntax error after check_budget change: {e}")
    exit(1)

with open("cost_analytics.py", "w", encoding="utf-8") as f:
    f.write(content)

print("File written successfully with check_budget change")

# Continue with other edits...
# get_daily_total
with open("cost_analytics.py", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.strip().startswith("def get_daily_total("):
        # Add department parameter
        new_lines.append(
            "    def get_daily_total(self, day: str | None = None, department: str | None = None) -> float:"
        )
        # Skip the old line
        i += 1
        # Now copy the body lines until we hit the next def
        # Actually this approach is getting complicated - let me use a different strategy
        break
    new_lines.append(line)
    i += 1

print("Attempting get_daily_total modification...")
# For now, let's just use the edit tool approach but be more careful
