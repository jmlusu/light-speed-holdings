#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from ai_company.cli.main import app

cmd_names = [c.name for c in app.registered_commands]
print('Registered commands:', cmd_names)
print('create_deck registered:', 'create_deck' in cmd_names)