#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from ai_company.cli.main import app

for cmd in app.registered_commands:
    name = cmd.name
    callback_name = cmd.callback.__name__ if hasattr(cmd.callback, '__name__') else type(cmd.callback).__name__
    print(f'  {name}: {callback_name}')