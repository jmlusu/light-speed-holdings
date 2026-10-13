#!/usr/bin/env python3
"""Test the create-deck command help"""
import sys
import io
sys.path.insert(0, '.')
from typer.testing import CliRunner
from ai_company.cli.main import app

runner = CliRunner()
result = runner.invoke(app, ["create-deck", "--help"])
print("Exit code:", result.exit_code)
# Capture stdout as bytes to avoid encoding issues
output = result.stdout.encode('utf-8', errors='replace') if result.stdout else b''
print("stdout bytes:", output[:200])
print("stderr:", result.stderr[:200] if result.stderr else 'no stderr')
if result.exit_code != 0:
    print("FAILED - exit code:", result.exit_code)
else:
    print("SUCCESS - command help works")