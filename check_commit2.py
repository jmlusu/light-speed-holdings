import subprocess

result = subprocess.run(
    ["git", "show", "f5176262", "--stat"],
    capture_output=True,
    text=True,
    cwd="C:\\Users\\jmlus\\light-speed-holdings",
    encoding="utf-8",
    errors="replace",
)
print("stdout:", result.stdout[:2000] if result.stdout else "None")
print("---stderr---")
print("stderr:", result.stderr[:200] if result.stderr else "None")
