#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from ai_company.cli.main import app

for i, cmd in enumerate(app.registered_commands):
    print(f'  [{i}] name={repr(cmd.name)}, callback={type(cmd.callback).__name__ if cmd.callback else None}')