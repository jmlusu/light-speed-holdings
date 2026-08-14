import os
import subprocess

scripts_dir = "scripts"
ps1_files = sorted([f for f in os.listdir(scripts_dir) if f.endswith(".ps1")])

for f in ps1_files:
    path = os.path.join(scripts_dir, f)
    # Try to parse the PowerShell script help
    result = subprocess.run(
        ["pwsh", "-NoProfile", "-Command", '. "' + path + '" -Help 2>&1 | Out-Null'],
        capture_output=True,
        text=True,
        cwd=os.path.join(os.getcwd(), scripts_dir),
    )
    status = "OK" if result.returncode == 0 else "ISSUE"
    out_preview = (result.stdout[:60] + "...") if result.stdout else ""
    err_preview = (result.stderr[:60] + "...") if result.stderr else ""
    print(f"{f}: {status} (exit={result.returncode}) out={out_preview} err={err_preview}")
