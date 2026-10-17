import subprocess
import time

# Kill the existing node process on port 3000
print("Killing existing node process on port 3000...")
result = subprocess.run(["taskkill", "/F", "/PID", "12284"], capture_output=True, text=True)
print(f"taskkill stdout: {result.stdout}")
print(f"taskkill stderr: {result.stderr}")
print(f"taskkill returncode: {result.returncode}")

# Wait a moment
print("\nWaiting 2 seconds...")
time.sleep(2)

# Try to start the dev server
print("\nStarting npm run dev...")
result = subprocess.run(
    ["npm", "run", "dev"],
    capture_output=True,
    text=True,
    cwd="C:\\Users\\jmlus\\light-speed-holdings",
    timeout=30,
)
print(f"stdout: {result.stdout[:1000] if result.stdout else 'None'}")
print(f"stderr: {result.stderr[:1000] if result.stderr else 'None'}")
print(f"returncode: {result.returncode}")

# Check if port 3000 is still in use
print("\nChecking port 3000...")
result2 = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
for line in result2.stdout.split("\n"):
    if "3000" in line:
        print(f"Port 3000: {line}")
