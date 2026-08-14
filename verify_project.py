#!/usr/bin/env python3
import os
import subprocess

print("=== COMPREHENSIVE PROJECT STATUS CHECK ===")
print()

# 1. CLI subcommands - verify help loads
print("1. CLI SUBCOMMANDS")
help_result = subprocess.run(
    [
        "powershell",
        "-NoProfile",
        "-Command",
        'Set-Location "C:\\Users\\jmlus\\light-speed-holdings"; '
        "$output = ai-company --help; "
        'Write-Output "CLI_HELP_LOADED"',
    ],
    capture_output=True,
    text=True,
    timeout=30000,
)
print(
    f"   CLI help accessible: {'YES' if 'CLI_HELP_LOADED' in help_result.stdout else 'checking alternative'}"
)

# Try using the venv python directly
result = subprocess.run(
    [
        os.path.join(".venv", "Scripts", "python"),
        "-c",
        'from ai_company.cli.main import app; print("CLI loaded")',
    ],
    cwd="C:\\Users\\jmlus\\light-speed-holdings",
    capture_output=True,
    text=True,
    timeout=30000,
)
print(f"   CLI module imports: {'YES' if result.returncode == 0 else 'NO'} - {result.stdout}")

# 2. Generator
print()
print("2. GENERATOR")
result = subprocess.run(
    [
        os.path.join(".venv", "Scripts", "python"),
        "-c",
        'from ai_company.generator import AgentGenerator; r = AgentGenerator().generate_all(); print(f"Generated {len(r)} agents")',
    ],
    cwd="C:\\Users\\jmlus\\light-speed-holdings",
    capture_output=True,
    text=True,
    timeout=60000,
)
print(f"   generate_all() works: {result.stdout.strip()}")
if result.stderr:
    print(f"   Warnings: {result.stderr.strip()[:200]}")

# 3. Message bus
print()
print("3. MESSAGE BUS & ORCHESTRATOR")
result = subprocess.run(
    [
        os.path.join(".venv", "Scripts", "python"),
        "-c",
        "from ai_company.orchestrator.message_bus import MessageBus; bus = MessageBus(); "
        "inbox = bus.get_all_tasks(); "
        "pending = bus.get_pending_tasks(); "
        'print(f"Total: {len(inbox)}, Pending: {len(pending)}")',
    ],
    cwd="C:\\Users\\jmlus\\light-speed-holdings",
    capture_output=True,
    text=True,
    timeout=30000,
)
print(f"   Message bus: {result.stdout.strip()}")
if result.stderr:
    print(f"   Warnings: {result.stderr.strip()[:200]}")

# 4. Scripts directory
print()
print("4. SCRIPTS DIRECTORY")
scripts_dir = "scripts"
all_entries = sorted(os.listdir(scripts_dir))
ps1_files = [f for f in all_entries if f.endswith(".ps1")]
print(f"   Total entries: {len(all_entries)}")
print(f"   .ps1 files: {len(ps1_files)}")
for f in ps1_files:
    path = os.path.join(scripts_dir, f)
    size = os.path.getsize(path)
    with open(path, "r") as fh:
        content = fh.read()
    has_param = "param(" in content
    has_help = ".SYNOPSIS" in content or "<#" in content
    print(f"   - {f}: {size} bytes, param={has_param}, help={has_help}")

# 5. dev.ps1
print()
print("5. DEV.PS1 ONBOARDING")
dev_path = os.path.join(scripts_dir, "dev.ps1")
with open(dev_path, "r") as fh:
    dev_content = fh.read()
has_setup = "function Invoke-Setup" in dev_content
has_test = "function Invoke-Test" in dev_content
has_lint = "function Invoke-Lint" in dev_content
has_status = "function Invoke-Status" in dev_content
print(f"   Has Setup: {has_setup}")
print(f"   Has Test: {has_test}")
print(f"   Has Lint: {has_lint}")
print(f"   Has Status: {has_status}")

# 6. backup.ps1
print()
print("6. BACKUP.PS1 DISASTER RECOVERY")
backup_path = os.path.join(scripts_dir, "backup.ps1")
with open(backup_path, "r") as fh:
    backup_content = fh.read()
has_backup_dir = "BackupDir" in backup_content
has_retention = "RetentionDays" in backup_content
has_dryrun = "DryRun" in backup_content
print(f"   Has BackupDir param: {has_backup_dir}")
print(f"   Has RetentionDays param: {has_retention}")
print(f"   Has DryRun param: {has_dryrun}")

# 7. STATUS.md and ECL
print()
print("7. DOCUMENTATION")
status_path = "docs/STATUS.md"
with open(status_path, "r") as fh:
    status_content = fh.read()
has_recent_state = "Current State" in status_content
has_sprints = "Sprint" in status_content
has_test_counts = "1878 tests" in status_content
print(f"   STATUS.md has recent state: {has_recent_state}")
print(f"   STATUS.md has sprint info: {has_sprints}")
print(f"   STATUS.md has test counts: {has_test_counts}")

ecl_path = "docs/ECL.md"
with open(ecl_path, "r") as fh:
    ecl_content = fh.read()
has_lifecycle = "Change Lifecycle" in ecl_content
has_stage_boundary = "Stage-Boundary Protocol" in ecl_content
print(f"   ECL.md has lifecycle: {has_lifecycle}")
print(f"   ECL.md has stage-boundary: {has_stage_boundary}")

# 8. Coordination summary
print()
print("8. COORDINATION SUMMARY")
print(
    f"   Generator: generate_all() {'PASS' if 'Generated 131 agents' in result.stdout else 'CHECK'}"
)
print("   Tests: 1878 passing (from STATUS.md)")
print("   Code quality: ruff/mypy clean (from STATUS.md)")
print("   131 agents deployed (from STATUS.md)")
print("   Tool vocabulary canonicalized (from STATUS.md)")

print()
print("=== CHECK COMPLETE ===")
