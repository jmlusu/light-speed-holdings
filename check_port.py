import subprocess

result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
for line in result.stdout.split("\n"):
    if "1441" in line or "1440" in line:
        print(line)
