#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from ai_company.cli.main import app

print("AI Company Builder CLI")
print("=" * 50)
print()
print("Available commands:")

# Get subparsers or commands
if hasattr(app, 'commands') and app.commands:
    for cmd_name in sorted(app.commands.keys()):
        print(f"  ai-company {cmd_name}")
else:
    # Try to list via typer
    print("  (no subcommands found via commands attribute)")

print()
print("Use: ai-company <command> --help for command-specific help")