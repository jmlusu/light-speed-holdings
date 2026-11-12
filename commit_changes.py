import subprocess

result = subprocess.run(
    [
        "C:\\Program Files\\Git\\bin\\git.exe",
        "commit",
        "-m",
        "T5 #447: Nov 2026 competitive landscape refresh",
    ],
    capture_output=True,
    text=True,
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("RC:", result.returncode)
