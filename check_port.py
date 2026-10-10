import subprocess

result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
for line in result.stdout.split("\n"):
    if "3000" in line:
        print(line)
