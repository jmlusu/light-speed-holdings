#!/usr/bin/env python3
"""Test the create-deck command help"""
import sys
sys.path.insert(0, '.')
from typer.testing import CliRunner
from ai_company.cli.main import app

runner = CliRunner()
result = runner.invoke(app, ["create-deck", "--help"])
print("Exit code:", result.exit_code)
print("stdout:", result.stdout)
print("stderr:", result.stderr)
if result.exit_code != 0:
    print("FAILED")
else:
    print("SUCCESS - command help works")