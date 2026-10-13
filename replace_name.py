#!/usr/bin/env python3
import sys

with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\cli\main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace all references to create-deck with create_deck
new_content = content.replace("create-deck", "create_deck")

with open(r"C:\Users\jmlus\light-speed-holdings\src\ai_company\cli\main.py", "w", encoding="utf-8") as f:
    f.write(new_content)

old_count = content.count("create-deck")
new_count = new_content.count("create_deck")
print(f"Replaced {old_count} occurrences of 'create-deck' with 'create_deck'")
print(f"Remaining 'create-deck': {new_content.count('create-deck')}")
print(f"New 'create_deck': {new_content.count('create_deck')}")