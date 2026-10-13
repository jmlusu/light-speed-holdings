#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from ai_company.cli.main import app

cmd_names = [c.name for c in app.registered_commands]
print('All command names:', cmd_names)
print()
print('create-deck in names:', 'create-deck' in cmd_names)
print('create_deck in names:', 'create_deck' in cmd_names)
print()
# Show all with non-None names
for i, name in enumerate(cmd_names):
    if name is not None:
        print(f'  [{i}] name={name}')