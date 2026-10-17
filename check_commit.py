import subprocess

result = subprocess.run(
    ["git", "show", "f5176262", "--oneline"],
    capture_output=True,
    text=True,
    cwd="C:\\Users\\jmlus\\light-speed-holdings",
    encoding="utf-8",
    errors="replace",
)
print("stdout:", result.stdout[:500] if result.stdout else "None")
print("stderr:", result.stderr[:200] if result.stderr else "None")
print("returncode:", result.returncode)
